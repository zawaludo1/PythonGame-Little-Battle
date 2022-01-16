class Resource(object):
    def __init__(self, ww, ff, gg, *args, **kwargs):
        self.r = [ww, ff, gg]

    def __str__(self):
        return 'Your Asset: Wood - %d Food - %d Gold - %d' % (tuple(self.r))


class PlayerResource(Resource):
    def __init__(self, ww=2, ff=2, gg=2, *args, **kwargs):
        super().__init__(ww, ff, gg, *args, **kwargs)

    def cost(self, x):
        if all([x.r[0] <= self.r[0], x.r[1] <= self.r[1], x.r[2] <= self.r[2]]):
            return True
        else:
            return False

    def add(self, name, value=2):
        if name == 'Gold':
            self.r[2] += value
        elif name == 'Food':
            self.r[1] += value
        else:
            self.r[0] += value







RECRUITMENT = {
    'S': {  # SpearMan
        'Name': 'Spearman',
        'Cost': [1, 1, 0],  # 1W，1F
        'Move': 1,
    },
    'A': {  # Archer
        'Name': 'Archer',
        'Cost': [1, 0, 1],  # 1W，1G
        'Move': 1,
    },
    'K': {  # Knight
        'Name': 'Knight',
        'Cost': [0, 1, 1],  # 1F, 1G
        'Move': 1,
    },
    'T': {  # Scout
        'Name': 'Scout',
        'Cost': [1, 1, 1],  # 1W, 1F, 1G
        'Move': 2,
    }
}

RESOURCE_DICT = {
    'Water': {
        'Acr': 'WW',
        'Show': '~~',
    },
    'Food': {
        'Acr': 'FF',
        'Show': 'FF',
    },
    'Wood': {
        'Acr': 'WW',
        'Show': 'WW',
    },
    'Gold': {
        'Acr': 'GG',
        'Show': 'GG',
    },
}

FIGHT_RESULTS = {
    ('S', 'S'): 0,
    ('S', 'K'): 1,
    ('S', 'A'): -1,
    ('S', 'T'): 1,

    ('K', 'S'): -1,
    ('K', 'K'): 0,
    ('K', 'A'): 1,
    ('K', 'T'): 1,

    ('A', 'S'): 1,
    ('A', 'K'): -1,
    ('A', 'A'): 0,
    ('A', 'T'): 1,

    ('T', 'S'): -1,
    ('T', 'K'): -1,
    ('T', 'A'): -1,
    ('T', 'T'): 0,
}











from res import Resource
from settings import RECRUITMENT


class Army(object):
    def __init__(self, pos, army_info):
        self.pos = pos
        self.max_move_step = army_info['Move']
        self.r = Resource(*army_info['Cost'])
        self.moved = False


class SpearMan(Army):
    def __init__(self, pos=None, army_info=RECRUITMENT['S']):
        super().__init__(pos, army_info)
        self.name = 'S'


class Archer(Army):
    def __init__(self, pos=None, army_info=RECRUITMENT['A']):
        super().__init__(pos, army_info)
        self.name = 'A'


class Knight(Army):
    def __init__(self, pos=None, army_info=RECRUITMENT['K']):
        super().__init__(pos, army_info)
        self.name = 'K'


class Scout(Army):
    def __init__(self, pos=None, army_info=RECRUITMENT['T']):
        super().__init__(pos, army_info)
        self.name = 'T'

import re
import sys
from settings import RESOURCE_DICT, RECRUITMENT, FIGHT_RESULTS


class BattleMap(object):
    def __init__(self, data, player_list):
        self.pos = data['position']
        self.base_list = [data['base1'][0], data['base2'][0]]
        self.battle_map = None
        self.w = data['size'][0]
        self.h = data['size'][1]
        self.map_pos_range = [[i, j] for i in range(self.w) for j in range(self.h)]
        self.update_map(init=True)
        self.player_list = player_list

    def check_move(self, index):
        for k, pos_list in self.pos.items():
            if k.endswith(str(index)):
                if len(pos_list) != 0:
                    armies = self.player_list[index - 1].armies
                    for army in armies:
                        if not army.moved:
                            return True
                    else:
                        return False
        else:
            return False

    def find_army(self, index, src):
        for k, pos_list in self.pos.items():
            if k.endswith(str(index)):
                for pos in pos_list:
                    if pos == src:
                        return k
        else:
            return None

    def check_legal_pos(self, src, tgt, base_number, name):
        if tgt == self.base_list[base_number]:  # 如果在基地位置，移动无效
            return False
        if src not in self.map_pos_range or tgt not in self.map_pos_range:
            return False
        if src == tgt:
        
            return False
        if src not in self.pos[name]:
            return False
        for k, v in self.pos.items():
            if k.endswith(name[-1]):
                if tgt in v:
                    return False
        dis = (tgt[0] - src[0]) ** 2 + (tgt[1] - src[1])**2  
        if name in ['A', 'S', 'k']:
            if dis == 1:
                return True
        else:
            if 1 <= dis <= 2:
                return True
            else:
                return False

    def get_all_passed_pos(self, name, src, tgt):
        self.pos[name].remove(src)
        self.pos[name].append(tgt)
        x1, y1 = src
        x2, y2 = tgt
        sqr = int(pow((x1 - x2), 2) + pow((y1 - y2), 2))
        if sqr == 1:
            pass_list = [tgt]
        else:
            tgt_ = [(x1 + x2) // 2, (y1 + y2) // 2]
            pass_list = [tgt_, tgt]
        return pass_list

    def move_army(self, name, src, pass_list, year):
        player = self.player_list[int(name[-1]) - 1]
        enemy = [p for p in self.player_list if p != player][0]
        has_moved = False
        for army in player.armies:
            if army.pos == src:
                if army.moved:
                    has_moved = True
                    break
        if has_moved:
            self.pos[name].remove(pass_list[-1])
            self.pos[name].append(src)
            return False
        else:
            end_move = False
            base_around = player.base_around
            if src in base_around:
                base_around.append(src)
            for pass_pos in pass_list:
                if end_move:
                    break
                for frame, pos_values in self.pos.items():
                    a1 = name[0]
                    a2 = frame[0]
                    if frame in ['Wood', 'Food', 'Gold']:  # 移动到资源位置
                        for pos_value in pos_values:
                            if pos_value == pass_pos:
                                pos_values.remove(pos_value)
                                print('Good. We collected 2 <%s>' % frame)
                                player.resource.add(frame)
                                if src in player.base_around and src not in player.left_around:
                                    player.left_around.append(src)
                    elif frame == 'Water':  # 移动到了水的位置
                        for pos_value in pos_values:
                            if pos_value == pass_pos:
                                army_name = RECRUITMENT[a1]['Name']
                                self.pos[name].remove(pass_pos)
                                print('We lost the army <%s> due to your command!' % army_name)
                                end_move = True
                                break
                    else:  # 判断其他玩家的军队
                        if frame[-1] != name[-1]:
                            if pass_pos == enemy.base:
                                army_name = RECRUITMENT[a1]['Name']
                                print('The army <%s> captured the enemy’s capital.' % army_name)
                                name = input("What's your name, commander?")
                                print('***Congratulation! Emperor <%s> unified the country in <%s>.***' % (name, year))
                                sys.exit(0)

                            for pos_value in pos_values:
                                if pass_pos == pos_value:
                                    res = FIGHT_RESULTS[(a1, a2)]  # 战斗结果
                                    if res == 0:
                                        self.pos[name].remove(pass_pos)
                                        self.pos[frame].remove(pass_pos)
                                        army_name = RECRUITMENT[a2]['Name']
                                        print('We destroyed the enemy <%s> with massive loss!' % army_name)
                                        end_move = True
                                        break
                                    elif res == 1:
                                        army_name = RECRUITMENT[a2]['Name']
                                        self.pos[frame].remove(pos_value)
                                        print('Great! We defeated the enemy <%s>!' % army_name)
                                    else:
                                        army_name = RECRUITMENT[a1]['Name']
                                        self.pos[name].remove(pos_value)
                                        print('We lost the army <%s> due to your command!' % army_name)
                                        end_move = True
                                        break
            for army in player.armies:
                if army.pos == src:
                    army.pos = pass_pos
                    army.moved = True
            return True

    def update_position(self, init, pos_dict, year):

        if init:
            for army in ['A', 'S', 'K', 'T']:
                for player in [1, 2]:
                    self.pos['%s%s' % (army, player)] = []
        else:
            name = list(pos_dict.keys())[0]  # A1, A2, S1, S2
            pos_list = pos_dict[name]
            if isinstance(pos_list[0], list):
                base_number = int(name[-1]) - 1
                src = pos_list[0]
                tgt = pos_list[1]
                is_legal_pos = self.check_legal_pos(src, tgt, base_number, name)
                if is_legal_pos:
                    pass_list = self.get_all_passed_pos(name, src, tgt)
                    self.move_army(name, src, pass_list, year)
                else:
                    return False
            else:
                src = pos_list
                if src not in self.pos[name]:
                    self.pos[name].append(src)
        return True

    def get_all_position(self):
        pos_dict = {}
        for k, v in self.pos.items():
            try:
                column = RESOURCE_DICT[k]['Show']
            except KeyError:
                column = k
            for n in v:
                pos_dict[tuple(n)] = column
        return pos_dict

    def add_x_y_axis(self, string):
        lines = string.split('\n')
        w = len(lines[0]) // 2
        h = len(lines)
        new_text_list = []
        for index, line in enumerate(lines):
            text_list = re.findall(".{2}", line)
            new_text = str(index).zfill(2) + "|" + "|".join(text_list) + "|"
            new_text_list.append(new_text)
        new_text_list.insert(0, '  X' + ' '.join([str(i).zfill(2) for i in range(w)]) + 'X')
        new_text_list.insert(1, ' Y+' + '-'.join(['--' for i in range(w)]) + '+')
        new_text_list.append(' Y+' + '-'.join(['--' for i in range(w)]) + '+')
        return new_text_list

    def update_map(self, init=False, pos_dict={}, year=None):
        res = self.update_position(init, pos_dict, year)
        pos_dict = self.get_all_position()
        string = ''
        for i in range(self.h):
            for j in range(self.w):
                t = pos_dict.get((j, i), '  ')
                string += t
            if i != self.h - 1:
                string += '\n'
        self.battle_map = self.add_x_y_axis(string)
        return res

    def show(self):
        for line in self.battle_map:
            print(line)








import os
import re



class Configure(object):
    def __init__(self):
        self.frames = [
            'Frame',
            'Water',
            'Wood',
            'Food',
            'Gold'
        ]
        self.w = None
        self.h = None
        self.base1_list = [
            [1, 1],
            [0, 1],
            [1, 0],
            [1, 2],
            [2, 1]
        ]
        self.base2_list = [

        ]
        self.pos_list = []
        self.map_data = {
            'base1': self.base1_list,
            'position': {i + j: [] for i in ['A', 'S', 'K', 'T'] for j in ['1', '2']},
            'size': None,
        }

    @staticmethod
    def check_file(path):
        """
        check whether it exist, or return
        :param path:
        :return:
        """
        if not os.path.exists(path):
            raise FileNotFoundError
        else:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        return content

    def check_frame(self, lines):
        """
        check title
        :param lines:
        :return:
        """
        for line in lines:
            frame = line.split(':', 1)[0]
            if frame not in self.frames:
                raise SyntaxError('Invalid Configuration File: format error!')
        return True

    def check_size(self, lines):
        """
        check length and height
        :param lines:
        :return:
        """
        ff = lines[0].split(':')[-1]
        if re.match('(\d)x(\d)', ff):
            wh = re.findall('(\d)x(\d)', ff)[0]
            w = int(wh[0])
            h = int(wh[1])
            if not (5 <= w <= 7 and 5 <= h <= 7):
                raise ArithmeticError('Invalid Configuration File: width and height should range from 5 to 7!')
            else:
                self.w = w
                self.h = h
                self.map_data['size'] = [self.w, self.h]
                self.base2_list.extend(
                    [
                        [self.w - 2, self.h - 2],
                        [self.w - 3, self.h - 2],
                        [self.w - 2, self.h - 3],
                        [self.w - 1, self.h - 2],
                        [self.w - 2, self.h - 1],
                    ]
                )
                self.map_data['base2'] = self.base2_list
            return True
        else:
            raise SyntaxError('Invalid Configuration File: frame should be in format width x height!')

    def check_numbers(self, lines):
        """
        check the number
        :param lines:
        :return:
        """
        for line in lines[1:]:
            frame, num_string = line.split(':', 1)
            numbers = num_string.split()
            if len(numbers) % 2 != 0:
                raise SyntaxError('Invalid ConfigurationFile: <line_name (e.g., %s)> has an odd number of elements!' % frame)
            try:
                is_int = all(list(map(lambda x: isinstance(int(x), int), numbers)))
            except ValueError:
                raise ValueError('Invalid Configuration File: (e.g., %s) contains non integer characters!' % frame)
            else:
                if not is_int:
                    raise ValueError('Invalid Configuration File: (e.g., %s) contains non integer characters!' % frame)
            num_even_list = numbers[0::2]
            num_odd_list = numbers[1::2]
            is_in_x = all(list(map(lambda x: 0 <= int(x) < self.w, num_even_list)))
            is_in_y = all(list(map(lambda y: 0 <= int(y) < self.h, num_odd_list)))
            if not is_in_x or not is_in_y:
                raise ArithmeticError('Invalid Configuration File: <%s> contains a position that is out of map.' % frame)
            self.map_data['position'][frame] = []
            for i, j in zip(num_even_list, num_odd_list):
                pos = [int(i), int(j)]
                if pos not in self.pos_list:
                    if pos not in [i for i in self.base1_list + self.base2_list]:
                        self.pos_list.append(pos)
                        self.map_data['position'][frame].append(pos)
                    else:
                        raise ValueError('Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!')
                else:
                    raise SyntaxError('Invalid Configuration File: Duplicate position (%s, %s)!' % (pos[0], pos[1]))

        return True

    def check(self, path):
        content = self.check_file(path)
        lines = [i for i in content.split('\n') if i.strip()]
        status = self.check_frame(lines)
        if status:
            status = self.check_size(lines)
        if status:
            status = self.check_numbers(lines)
        if status:
            print('Configuration file <%s> was loaded.' % path)
        return True

    def load_file(self, path):
        status = self.check(path)
        if status:
            return self.map_data












from copy import deepcopy
from army import SpearMan, Archer, Knight, Scout
from res import PlayerResource
from settings import RECRUITMENT


class Player(object):
    def __init__(self, base_around):
        self.resource = PlayerResource()
        self.base_around = base_around[1:]
        self.base = base_around[0]
        self.left_around = deepcopy(base_around)
        self.armies = []

    def has_enough_res(self):
        for k, v in RECRUITMENT.items():
            cost = v['Cost']
            if all([i - j >= 0 for i, j in zip(self.resource.r, cost)]):
                f = True
                break
        else:
            f = False
        return f

    def has_enough_place(self, ):
        if len(self.base_around) != 0:
            return True
        else:
            return False

    def recruit(self, name, pos=None):
        if name == 'S':
            army = SpearMan(pos)
        elif name == 'A':
            army = Archer(pos)
        elif name == 'K':
            army = Knight(pos)
        else:
            army = Scout(pos)
        n = self.resource.cost(army.r)
        if not n:
            return False
        else:
            if pos is not None:
                self.resource.r = [i - j for i, j in zip(self.resource.r, army.r.r)]
                self.left_around.remove(pos)
                self.armies.append(army)
            return True

    def remove_army(self, pos):
        for army in self.armies:
            if army.pos == pos:
                self.armies.remove(army)















import sys
from map import BattleMap
from configure import Configure
from player import Player



class Game(object):
    def __init__(self, file_data):
        self.year = 617
        self.file_data = file_data
        p1 = Player(file_data['base1'])
        p2 = Player(file_data['base2'])
        self.players = [p1, p2]
        self.m = BattleMap(self.file_data, self.players)

    def show_map(self):
        self.m.update_map()

    def play(self):
        print('Game Started: Little Battle! (enter QUIT to quit the game)')
        print('enter PRIS to display the price list\nenter DIS to display the map')
        while True:
            print('-Year %s-' % self.year)
            for i in range(len(self.players)):
                player = self.players[i]
                end_recruit = False
                print("+++Player %d's Stage: Recruit Armies+++" % (i + 1))
                while True:  # 5-c
                    print(player.resource)
                    if end_recruit:
                        break
                    while True:  # 5-d
                        if end_recruit:
                            break
                        r = player.has_enough_res()
                        p = player.has_enough_place()
                        if not r:
                            print('No resources to recruit any armies.')
                            end_recruit = True
                            break
                        if not p:
                            print('No place to recruit any armies.')
                            end_recruit = True
                            break
                        cmd_str = input('Which type of army to recruit, (enter) S, A, K, or T?\n')
                        if cmd_str == 'QUIT':
                            sys.exit(0)
                        elif cmd_str == 'PRIS':
                            print('Recruiting Prices：\n\tSpearman (S) - 1W, 1F;\n\tArcher (A) - 1W, 1G;'
                                  '\n\tKnight (K) - 1F, 1G;\n\tScout (T) - 1W, 1F, 1G;')
                        elif cmd_str == 'DIS':
                            self.m.show()
                        elif cmd_str == 'NO':
                            end_recruit = True
                            break
                        elif cmd_str in ['S', 'A', 'K', 'T']:
                            if cmd_str == 'S':
                                army = 'Spearman'
                            elif cmd_str == 'A':
                                army = 'Archer'
                            elif cmd_str == 'K':
                                army = 'Knight'
                            else:
                                army = 'Scout'
                            s = player.recruit(cmd_str)
                            if not s:
                                print('Insufficient resources. Try again.')
                                continue
                            else:
                                while True:  # 5-i
                                    pos_str = input("You want to recruit a <%s>. "
                                          "Enter two integers as format 'x y' to place your army.\n" % army)
                                    if pos_str == 'QUIT':
                                        sys.exit(0)
                                    elif pos_str == 'PRIS':
                                        print(
                                            'Recruiting Prices：\n\tSpearman (S) - 1W, 1F;\n\tArcher (A) - 1W, 1G;'
                                            '\n\tKnight (K) - 1F, 1G;\n\tScout (T) - 1W, 1F, 1G;')
                                        break
                                    elif pos_str == 'DIS':
                                        self.m.show()
                                        break
                                    elif pos_str == 'QUIT':
                                        return
                                    elif pos_str == 'NO':
                                        end_recruit = True
                                        break
                                    else:
                                        try:
                                            x, y = pos_str.split()
                                            pos = [int(x), int(y)]
                                        except ValueError:
                                            print('Sorry，invalid input. Try again.')
                                            continue
                                        else:
                                            if pos not in player.left_around or not pos not in self.m.pos.values():
                                                print('You must place your newly recruited unit in an '
                                                      'unoccupied position next to your home base. Try again.')
                                                continue
                                            else:
                                                player.recruit(cmd_str, pos)
                                                pos_dict = {
                                                    cmd_str + str(i + 1): pos
                                                }
                                                self.m.update_map(pos_dict=pos_dict)
                                                print('You has recruited a <%s>.' % army)
                                                break
                        else:
                            print('Sorry, invalid input. Try again.')

                print("\n===Player %d's Stage: Move Armies===\n" % (i + 1))
                while True:  # 5-f
                    m = self.m.check_move(i+1)
                    if not m:
                        print('No Army to Move: next turn.\n')
                        break
                    cmd_str = input("Enter four integers as a format 'x0 y0 x1 y1' to represent move "
                                    "unit from (x0, y0) to (x1, y1) or 'NO' to end this turn.\n")
                    if cmd_str == 'NO':
                        break
                    elif cmd_str == 'QUIT':
                        sys.exit(0)
                    elif cmd_str == 'PRIS':
                        print('Recruiting Prices：\n\tSpearman (S) - 1W, 1F;\nArcher (A) - 1W, 1G;'
                              '\nKnight (K) - 1F, 1G;\nScout (T) - 1W, 1F, 1G;')
                    elif cmd_str == 'DIS':
                        self.m.show()
                    else:
                        try:
                            x1, y1, x2, y2 = [int(i) for i in cmd_str.split()]
                        except ValueError:
                            print('Invalid move. Try again.')
                        else:
                            src = [x1, y1]
                            tgt = [x2, y2]
                            sqr = int(pow((x1 - x2), 2) + pow((y1 - y2), 2))
                            if sqr == 1:
                                name = self.m.find_army(i+1, src)
                                name2 = self.m.find_army(i+1, tgt)
                                if name and not name2:
                                    map_pos_list = [src, tgt]
                                    self.m.update_map(pos_dict={name: map_pos_list}, year=self.year)
                                else:
                                    print('Invalid move. Try again.')
                                    continue
                            elif sqr == 4:
                                if not x1 == x2 or y1 == y2:
                                    print('Invalid move. Try again.')
                                    continue
                                name = self.m.find_army(i+1, src)
                                if name:
                                    map_pos_list = [src, tgt]
                                    res = self.m.update_map(pos_dict={name: map_pos_list}, year=self.year)
                                    if res:
                                        player.resource.add(res)
                            else:
                                print('Invalid move. Try again.')
                                continue
                for army in player.armies:
                    army.moved = False
            self.year += 1


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        file = args[1]
        data = Configure().load_file(file)
        g = Game(data)
        g.play()
    else:
        print('Usage:\n\tpython3 little_battle.py <filepath>')
