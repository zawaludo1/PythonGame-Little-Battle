import sys


# Please implement this function according to Section "Read Configuration File"
def load_config_file(filepath):
    # It should return width, height, waters, woods, foods, golds based on the file
    # Complete the test driver of this function in file_loading_test.py
    width, height = 0, 0
    waters, woods, foods, golds = [], [], [], []  # list of position tuples

    return width, height, waters, woods, foods, golds


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 little_battle.py <filepath>")
        sys.exit()
    width, height, waters, woods, foods, golds = load_config_file(sys.argv[1])


# ===========================================================
# Create Class: Soldiers, Resources, Water, Player, Map
# ===========================================================

# -----------------------------------------------------------
# Create Soldier Class
class Soldier:

    def __init__(self, player_id, soldier_type, x, y):
        self.x = x
        self.y = y
        self.player = player_id
        self.soldier_type = soldier_type

        if self.soldier_type == 'Spearman':
            self.symbol_init = 'S'
            self.step = 1
            self.defeated = ['A']

        elif self.soldier_type == 'Archer':
            self.symbol_init = 'A'
            self.step = 1
            self.defeated = ['K']

        elif self.soldier_type == 'Knight':
            self.symbol_init = 'K'
            self.step = 1
            self.defeated = ['S']

        elif self.soldier_type == 'Scout':
            self.symbol_init = 'T'
            self.step = 2
            self.defeated = ['K', 'S', 'A']

    def __str__(self):
        return self.symbol_init + str(self.player)


# -----------------------------------------------------------
# Create Water Class
class Water:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = '~~'

    def __str__(self):
        return self.symbol


# -----------------------------------------------------------
# Create Resource Class
class Resource:
    def __init__(self, resource_type, x, y):
        self.x = x
        self.y = y
        self.resource_type = resource_type
        if resource_type == 'Wood':
            self.symbol = 'WW'
        elif resource_type == 'Food':
            self.symbol = 'FF'
        elif resource_type == 'Gold':
            self.symbol = 'GG'

    def __str__(self):
        return self.symbol


# -----------------------------------------------------------
# Create Player Class
class Player:
    def __init__(self, player_id, x, y):
        self.x = x
        self.y = y
        self.symbol = 'H'
        self.player_id = player_id
        self.soldiers = []
        self.resource = {'WW': 2, 'FF': 2, 'GG': 2}

    def __str__(self):
        return self.symbol + str(self.player_id)

    def get_resource(self, resource_symbol):
        self.resource[resource_symbol] += 2

    def asset_inf(self):
        return '[Your Asset: Wood - {} Food - {} Gold - {}]'. \
            format(self.resource['WW'],
                   self.resource['FF'],
                   self.resource['GG'])

    def affordable(self):
        determine_affordable = (self.resource['WW'] >= 1 and self.resource['GG']) \
                               or (self.resource['WW'] >= 1 and self.resource['FF'] >= 1) \
                               or (self.resource['GG'] >= 1 and self.resource['FF'] >= 1)
        return determine_affordable

    def recruit(self, soldier_type):
        recruit_dictionary = {
            'Spearman': {'WW': 1, 'FF': 1, 'GG': 0},
            'Archer': {'WW': 1, 'FF': 0, 'GG': 1},
            'Knight': {'WW': 0, 'FF': 1, 'GG': 1},
            'Scout': {'WW': 1, 'FF': 1, 'GG': 1}
        }
        checklist = recruit_dictionary[soldier_type]
        for resource_type, numbers in checklist.items():
            if self.resource[resource_type] < numbers:
                return False
        return True

    def recruit_set(self, soldier_type, x, y):
        recruit_dictionary = {
            'Spearman': {'WW': 1, 'FF': 1, 'GG': 0},
            'Archer': {'WW': 1, 'FF': 0, 'GG': 1},
            'Knight': {'WW': 0, 'FF': 1, 'GG': 1},
            'Scout': {'WW': 1, 'FF': 1, 'GG': 1}
        }
        checklist = recruit_dictionary[soldier_type]
        for resource_type, numbers in checklist.items():
            self.resource[resource_type] = self.resource[resource_type] - numbers
        self.soldiers.append(Soldier(self.player_id, soldier_type, x, y))

    def soldier_not_none(self):
        return len(self.soldiers) > 0


# -----------------------------------------------------------
# Create Map Class
class Map:
    def __init__(self, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.player = []
        self.player.append(Player(1, 1, 1))
        self.player.append(Player(2, self.x_axis - 2, self.y_axis - 2))
        self.resources = []
        self.water = []
        self.turn = 1
        self.current_player = self.player[self.turn - 1]
        if self.turn - 1 == 0:
            self.another_player = self.player[1]
        else:
            self.another_player = self.player[0]
        self.game_over = False

    def resource_factor(self, resource_type, x, y):
        self.resources.append(Resource(resource_type, x, y))

    def water_factor(self, x, y):
        self.water.append(Water(x, y))

    def change_turn(self):
        self.turn = self.turn % 2 + 1
        self.current_player = self.player[self.turn - 1]
        if self.turn - 1 == 0:
            self.another_player = self.player[1]
        else:
            self.another_player = self.player[0]

    def map_structure(self):
        map_structure = [['  ' for _ in range(self.x_axis)] for _ in range(self.y_axis)]
        for p in self.player:
            map_structure[p.y][p.x] = p
            for s in p.soldiers:
                map_structure[s.y][s.x] = s
        for r in self.resources:
            map_structure[r.y][r.x] = r
        for w in self.water:
            map_structure[w.y][w.x] = w
        return map_structure

    def have_place(self):
        x = self.current_player.x
        y = self.current_player.y
        return Map.map_structure()[y - 1][x] == '  ' or \
               Map.map_structure()[y][x - 1] == '  ' or \
               Map.map_structure()[y + 1][x] == '  ' or \
               Map.map_structure()[y][x + 1] == '  '

    def move(self, x0, y0, x1, y1):
        # 检测在不在，或者是否已经走过
        value_in = False
        for i in armies_can_move.values():
            for j in i:
                if (x0, y0) == j:
                    value_in = True
        if value_in == False:
            return 'Invalid move. Try again.\n'

        if not (0 <= x1 <= self.x_axis and 0 <= y1 <= self.y_axis) or \
                not (0 <= x0 <= self.x_axis and 0 <= y0 <= self.y_axis) or \
                (x0 == x1 and y0 == y1) or \
                (x0 != x1 and y0 != y1) or \
                self.map_structure()[y1][x1] == self.current_player:
            return 'Invalid move. Try again.\n'

        soldier_want_move = self.map_structure()[y0][x0]
        if not isinstance(soldier_want_move, Soldier) or \
                not soldier_want_move.player == self.current_player.player_id:
            return 'Invalid move. Try again.\n'

        move_step = abs(x0 + y0 - x1 - y1)
        if move_step > soldier_want_move.step:
            return 'Invalid move. Try again.\n'
        # 碰到自己的士兵
        if isinstance(self.map_structure()[y1][x1], Soldier) and \
                self.map_structure()[y1][x1] == self.turn:
            return 'Invalid move. Try again.\n'

        feedback = '\nYou have moved {} from ({}, {}) to ({}, {}).\n'. \
            format(soldier_want_move.soldier_type, x0, y0, x1, y1)

        move_action = []
        if move_step == 2:
            move_action.append(((x0 + x1) // 2, (y0 + y1) // 2))
        move_action.append((x1, y1))

        for action in move_action:
            # action1 : y_axis; action0: x_axis.
            target = self.map_structure()[action[1]][action[0]]

            if isinstance(target, Water):
                self.current_player.soldiers.remove(soldier_want_move)
                feedback += 'We lost the army {} due to your command!\n'.format(soldier_want_move.soldier_type)

            elif isinstance(target, Resource):
                self.current_player.get_resource(target.symbol)
                self.resources.remove(target)
                feedback += 'Good. We collected 2 {}.\n'.format(target.resource_type)

            elif target == '  ':
                continue

            elif isinstance(target, Soldier):
                if target.player == self.turn:
                    continue
                elif target.soldier_type == soldier_want_move.soldier_type:
                    self.current_player.soldiers.remove(soldier_want_move)
                    self.another_player.soldiers.remove(target)
                    feedback += 'We destroyed the enemy {} with massive loss!\n'.format(target.soldier_type)
                elif target.symbol_init in soldier_want_move.defeated:
                    feedback += 'We lost the army {} due to your command!\n'.format(soldier_want_move.soldier_type)
                    self.current_player.soldiers.remove(soldier_want_move)
                else:
                    feedback += 'Great! We defeated the enemy {}!\n'.format(target.soldier_type)
                    self.another_player.soldiers.remove(target)

            elif isinstance(target, Player):
                if target.player_id == self.turn:
                    continue
                self.game_over = True
                feedback += 'The army {} captured the enemy’s capital.'.format(soldier_want_move.soldier_type)
                break

        armies_can_move[soldier_want_move.soldier_type].remove((soldier_want_move.x, soldier_want_move.y))
        soldier_want_move.x = x1
        soldier_want_move.y = y1

        return feedback, True

    def __str__(self):

        map_structure = self.map_structure()
        map_show = 'Please check the battlefield, commander.\n'
        map_show += '  X'

        for x in range(self.x_axis - 1):
            map_show += '{:02d} '.format(x)

        map_show += '{:02d}X\n'.format(self.x_axis - 1)

        map_show += ' Y+' + '---' * (self.x_axis - 1) + '--+\n'

        for y in range(self.y_axis):
            map_show += '{:02d}|'.format(y)
            for x in range(self.x_axis):
                map_show += '{}|'.format(map_structure[y][x])
            map_show += '\n'
        map_show += ' Y+' + '---' * (self.x_axis - 1) + '--+'
        return map_show


# ===========================================================
# START
# ===========================================================
File = open("config.txt", 'r')
Frame = File.readlines()
if Frame[0][5] != ':' or Frame[0].split(':')[0] != 'Frame' or \
        Frame[1][5] != ':' or Frame[1].split(':')[0] != 'Water' or \
        Frame[2][4] != ':' or Frame[2].split(':')[0] != 'Wood' or \
        Frame[3][4] != ':' or Frame[3].split(':')[0] != 'Food' or \
        Frame[4][4] != ':' or Frame[4].split(':')[0] != 'Gold' or len(Frame) != 5:
    raise SyntaxError('Invalid Configuration File: format error! ')
File.close()

File = open("config.txt", 'r')

Frame = File.readline().split(':')

if not (Frame[1].strip()[1] == 'x' and
        Frame[1].strip()[0].isdigit() and
        Frame[1].strip()[2].isdigit()):
    raise SyntaxError('Invalid Configuration File: \
frame should be in format widthxheight!')

if int(Frame[1].strip()[0]) < 5 or \
        int(Frame[1].strip()[2]) < 5 or \
        int(Frame[1].strip()[0]) > 7 or \
        int(Frame[1].strip()[2]) > 7:
    raise ArithmeticError('Invalid Configuration File: \
width and height should range from 5 to 7!')

Frame = Frame[1].strip().split('x')
Map = Map(int(Frame[0]), int(Frame[1]))

Water_And_Resource = {}
position_list = []

for i in range(4):

    item = File.readline().split(':')
    item_key = item[0]
    item_value = item[1].strip().split(' ')

    if len(item_value) % 2 != 0:
        raise SyntaxError('Invalid Configuration File: {} has an odd number of elements!'.format(item_key))

    Water_And_Resource[item_key] = item_value

File.close()

for key, value in Water_And_Resource.items():

    for j in range(0, len(value), 2):

        if not (value[j].isdigit() and value[j + 1].isdigit() and
                float(value[j]) % 1 == 0 and float(value[j + 1]) % 1 == 0):
            raise ValueError('Invalid Configuration File: {} contains non integer characters!'.format(key))

        x_ = int(value[j])
        y_ = int(value[j + 1])

        if not (0 <= x_ <= Map.x_axis and 0 <= y_ <= Map.y_axis):
            raise ArithmeticError(' Invalid Configuration File: {} contains a position that is out of map.\
                                    '.format(key))
        position = (x_, y_)

        if position in [(1, 1), (Map.x_axis - 2, Map.y_axis - 2), (0, 1), (1, 0), (2, 1), (1, 2),
                        (Map.x_axis - 3, Map.y_axis - 2), (Map.x_axis - 2, Map.y_axis - 3),
                        (Map.x_axis - 1, Map.y_axis - 2), (Map.x_axis - 2, Map.y_axis - 1)]:
            raise ValueError('Invalid Configuration  File:  The  positions  of  home  bases  or  the  positions '
                             'next to the home bases are occupied!')

        if position in position_list:
            print(position)
            raise SyntaxError(' Invalid Configuration File: Duplicate position (x,  y)!')

        position_list.append(position)
        # --------------------------------------------------------------------------
        if key == 'Water':
            Map.water_factor(x_, y_)
        else:
            Map.resource_factor(key, x_, y_)


def common_cmd(command):
    if command == 'QUIT':
        exit(0)
    if command == 'DIS':
        print(Map)
        print('')
        return True
    if command == 'PRIS':
        print('''Recruit Prices:
  Spearman (S) - 1W, 1F
  Archer (A) - 1W, 1G
  Knight (K) - 1F, 1G
  Scout (T) - 1W, 1F, 1G''')
        return True
    return False


def print_armies():
    if armies_can_move['Spearman']:
        msg = '  Spearman: '
        for j in range(0, len(armies_can_move['Spearman']) - 1, 1):
            msg += str(armies_can_move['Spearman'][j]) + ', '
        msg += str(armies_can_move['Spearman'][-1])
        print(msg)

    if armies_can_move['Archer']:
        msg = '  Archer: '
        for j in range(0, len(armies_can_move['Archer']) - 1, 1):
            msg += str(armies_can_move['Archer'][j]) + ', '
        msg += str(armies_can_move['Archer'][-1])
        print(msg)

    if armies_can_move['Knight']:
        msg = '  Knight: '
        for j in range(0, len(armies_can_move['Knight']) - 1, 1):
            msg += str(armies_can_move['Knight'][j]) + ', '
        msg += str(armies_can_move['Knight'][-1])
        print(msg)

    if armies_can_move['Scout']:
        msg = '  Scout: '
        for j in range(0, len(armies_can_move['Scout']) - 1, 1):
            msg += str(armies_can_move['Scout'][j]) + ', '
        msg += str(armies_can_move['Scout'][-1])
        print(msg)

    print('')


print('Configuration file config.txt was loaded.')
print('Game Started: Little Battle! (enter QUIT to quit the game)\n')
print(Map)
print('(enter DIS to display the map)\n')
print('''Recruit Prices:
  Spearman (S) - 1W, 1F
  Archer (A) - 1W, 1G
  Knight (K) - 1F, 1G
  Scout (T) - 1W, 1F, 1G\n(enter PRIS to display the price list)''')

Year = 617
# 流程
while True:
    # 5a
    print('')
    print('-Year {}-\n'.format(Year))
    print('''+++Player {}'s Stage: Recruit Armies+++'''.format(str(Map.turn)))
    print('')
    # 5c 买兵
    No_resource = False
    Do_not_continue = False
    # 打印资产
    while not No_resource and not Do_not_continue:

        No_resource = False
        Do_not_continue = False
        print(Map.current_player.asset_inf())

        # 5d 判断资产
        while True:
            if not Map.current_player.affordable():
                print('No resources to recruit any armies.')
                No_resource = True
                break
            if not Map.have_place():
                print('No place to recruit new armies.')
                break

            # 买哪个兵
            cmd = input('\nWhich type of army to recruit, (enter) ‘S’, ‘A’, ‘K’, or ‘T’? \
Enter ‘NO’ to end this stage.\n')
            # 全局命令
            if common_cmd(cmd):
                continue
            if cmd not in ['S', 'A', 'K', 'T', 'NO']:
                print('Sorry, invalid input. Try again.')
                continue
            if cmd == 'NO':
                Do_not_continue = True
                break
            # 设置位置
            while True:

                Soldier_index = {'S': 'Spearman', 'K': 'Knight', 'T': 'Scout', 'A': 'Archer'}
                if Map.current_player.recruit(Soldier_index[cmd]):
                    set_soldier = input('\nYou want to recruit a {}. \
Enter two integers as format ‘x y’ to place your army.\n'.format(Soldier_index[cmd]))
                    # 判断位置信息合法，待添加
                    if len(set_soldier) != 3:
                        print('Sorry, invalid input. Try again.\n')
                        continue

                    if common_cmd(set_soldier):
                        continue

                    Available_position = []

                    if Map.map_structure()[Map.current_player.y - 1][Map.current_player.x] == '  ':
                        Available_position.append(str(Map.current_player.x) + ' ' + str(Map.current_player.y - 1))

                    if Map.map_structure()[Map.current_player.y + 1][Map.current_player.x] == '  ':
                        Available_position.append(str(Map.current_player.x) + ' ' + str(Map.current_player.y + 1))

                    if Map.map_structure()[Map.current_player.y][Map.current_player.x + 1] == '  ':
                        Available_position.append(str(Map.current_player.x + 1) + ' ' + str(Map.current_player.y))

                    if Map.map_structure()[Map.current_player.y][Map.current_player.x - 1] == '  ':
                        Available_position.append(str(Map.current_player.x - 1) + ' ' + str(Map.current_player.y))

                    if set_soldier not in Available_position:
                        print('You must place your newly recruited unit \
in an unoccupied position next to your home base. Try again.')
                        continue
                    # 此方法加入佣兵信息到地图中
                    Map.current_player.recruit_set(Soldier_index[cmd], int(set_soldier[0]), int(set_soldier[-1]))

                    print('\nYou has recruited a {}.\n'.format(Soldier_index[cmd]))
                    # next_step = '5c'
                    print(Map.current_player.asset_inf())
                    break



                else:
                    print('Insufficient resources. Try again.')
                    # next_step = '5d'
                    break

    # 5e
    print('')
    print('''===Player {}'s Stage: Move Armies===\n'''.format(str(Map.turn)))
    # 移动阶段
    armies_can_move = {}
    Spearman = []
    Archer = []
    Knight = []
    Scout = []

    for i in Map.current_player.soldiers:
        if i.soldier_type == 'Spearman':
            Spearman.append((i.x, i.y))
        elif i.soldier_type == 'Archer':
            Archer.append((i.x, i.y))
        elif i.soldier_type == 'Knight':
            Knight.append((i.x, i.y))
        elif i.soldier_type == 'Scout':
            Scout.append((i.x, i.y))

    armies_can_move = {
        'Spearman': Spearman,
        'Archer': Archer,
        'Knight': Knight,
        'Scout': Scout
    }

    while True:

        if not (armies_can_move['Spearman'] or armies_can_move['Knight'] or \
                armies_can_move['Archer'] or armies_can_move['Scout']):
            print('No Army to Move: next turn.')
            break
        # 打印所有的士兵位置
        print('Armies to Move:')

        print_armies()

        cmd = input('''Enter four integers as a format ‘x0 y0 x1 y1’ \
to represent move unit from (x0, y0) to (x1, y1) or ‘NO’ to end this turn.\n''')
        if common_cmd(cmd):
            continue
        if cmd == 'NO':
            break
            # 5a
        # 四位整数判断
        end = False
        try:
            move_inf = cmd.split(' ')
            feedback, success = Map.move(int(move_inf[0]), int(move_inf[1]), int(move_inf[2]), int(move_inf[3]))
            print(feedback)

            if Map.game_over:
                Winner = input('''What’s your name, commander?\n''')
                print('***Congratulation! Emperor {} unified the country in {}.***'.format(Winner, Year))
                end = True

        except:
            print('Invalid move. Try again.\n')
        if end == True:
            exit(0)
        continue

    Map.change_turn()
    if Map.current_player.player_id == 1:
        Year += 1

