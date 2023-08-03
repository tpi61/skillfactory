from pprint import pprint

class Ship:
    def __init__(self, size, msg):
        self.__size = size
        self.__coordinates = []
        counter = 0
        while counter != self.__size:
            coordinates = input(msg)
            coordinates = coordinates.split(' ')
            for coordinate in coordinates:
                if self.__size != counter:
                    try:
                        coordinate = tuple(map(int, [number for number in coordinate]))
                    except:
                        print('Only digit can be used')
                        continue
                    
                    if len(coordinate) != 2:
                        print('2 digits need to be set')
                    elif not all(0 < number < 7 for number in coordinate):
                        print('digits must be in range 1-6')
                    else:
                        self.__coordinates.append(coordinate)
                        counter+=1

    @property
    def size(self):
        return self.__size
    
    @property
    def coordinates(self):
        return self.__coordinates
    
    @coordinates.setter
    def coordinates(self, coordinate):
        self.__coordinates = coordinate

class Board:
    def __init__(self):
        self.__coordinates = {}
        for y in range(1,7):
            for x in range(1,7):
                self.__coordinates.setdefault((y,x), "O") 
        
    @property    
    def coordinates(self):
        return self.__coordinates
    
    @coordinates.setter
    def coordinates(self, ship):
        #ship = tuple([int(index) for index in ship])
        self.__coordinates
        self.__coordinates[ship] = "■"
    
   
class BattleField:
    def __init__(self, player_board,enemy_board):
        self.__player_board = player_board
        self.__enemy_board = enemy_board

    def display_bf(self):
        def index():
            for n in range(1,7):
                    yield n

        board = f'\tENEMY BOARD\t\t\tPLAYER BOARD\n'    
        board += f'  | 1 | 2 | 3 | 4 | 5 | 6 |\t  | 1 | 2 | 3 | 4 | 5 | 6 |\n'
        for y in index():
            board += f"{y} "
            for x in index():
                board += f'| {self.__enemy_board.coordinates[y,x]} '
            board += "|\t"
            board += f"{y} "
            for x in index():
                board += f'| {self.__player_board.coordinates[y,x]} '
            board += "|\n"
        return board

class Main:
    def __init__(self):
        self.player_board = Board()
        self.enemy_board = Board()
        self.mask_board = Board()
        self.bf = BattleField(self.player_board,self.mask_board)


    def initiate(self):
        print(self.bf.display_bf(),'\n')
        print('Please set ships')

        def ship_check(coordinates):
            for coordinate in coordinates:
                if self.player_board.coordinates[coordinate] == 'O':

                    if self.player_board.coordinates.get((coordinate[0]-1,coordinate[1])) != "■" \
                        and self.player_board.coordinates.get((coordinate[0]+1,coordinate[1])) != "■" \
                        and self.player_board.coordinates.get((coordinate[0],coordinate[1]-1)) != "■" \
                        and self.player_board.coordinates.get((coordinate[0],coordinate[1]+1)) != "■" :
                        return True
                    else:
                        print('Ships are to close')
                        return
                else:
                    print('Plase for the ship is busy')
                    return

        # while True:
        #     treaple = Ship(3, 'Add coordinates of Treaple-ship ')            


        while True:
            treaple = Ship(3, 'Add coordinates of Treaple-ship (example: 23 24 25): ')
            if ship_check(treaple.coordinates):
                print(treaple.coordinates)
                self.player_board.coordinates = treaple.coordinates
                break
        print(self.bf.display_bf(),'\n')

        while True:
            uno1 = Ship(1, 'Add coordinates of first Solo-ship (example: 23): ')
            if ship_check(uno1.coordinates):
                self.player_board.coordinates = uno1.coordinates
                break
        print(self.bf.display_bf(),'\n')

        while True:
            uno2 = Ship(1, 'Add coordinates of second Solo-ship: ')
            if ship_check(uno2.coordinates):
                self.player_board.coordinates = uno2.coordinates
                break
        
        print(self.bf.display_bf(),'\n')


start = Main()
start.initiate()

# #pl_b.board = '23'
# pl_b.board[(2,4)] = '■'
# #pl_b.board((1,1))
# print(bf.display_bf())
# print('Please set ships')
# # a = input('Enter coordinates for Duble-ship: ')
# # print(a)
# #pprint(pl_b.board)