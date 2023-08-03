import random

class Board:
    def __init__(self, size=6) -> None: 
        self.__size = size
        self.__fields: dict[tuple, int] = {}
        for y in range(1,self.__size+1):
            for x in range(1,self.__size+1):
                self.__fields.setdefault((y,x), 0)
        self.__ships: list = []
        self.__unshot = list(self.__fields.keys())

    @property
    def get_size(self) -> int:
        return self.__size
    
    @property
    def fields(self) -> dict:
        return self.__fields
    
    @fields.setter
    def fields(self,change_field) -> None:
        for key,value in change_field:
            self.__fields[key] = value
    
    @property
    def ships(self) -> list:
        return self.__ships
    
    @ships.setter
    def ships(self, ship) -> None:
        for pos in ship.coordinates:
            self.__ships.append(pos)
            self.__fields[pos] = 1

    def rm_ship(self, shot) -> None:
        self.__ships.remove(shot)
    
    @property
    def unshot(self) -> list:
        return self.__unshot
    
    @unshot.setter
    def unshot(self, shot) -> None:
        self.__unshot.remove(shot)

class EnamyBoard(Board):
    def __init__(self,size=6) -> None:
        super().__init__(size)
        self.__fields_mist = self.fields.copy()

    @property
    def fields_mist(self) -> dict[tuple, int]:
        return self.__fields_mist
    
    @fields_mist.setter
    def fields_mist(self, change_field) -> None:
        for key,value in change_field:
            self.__fields_mist[key] = value

class Ship:
    def __init__(self,size,coordinates) -> None:
        self.__size = size
        self.__coordinates = coordinates

    @property
    def size(self) -> int:
        return self.__size
    
    @property
    def coordinates(self) -> list:
        return self.__coordinates

class Shot:
    def shot_check(self, shot, target_board) -> bool:
        if target_board.fields[shot] in [2,3]:
            return False
        else:
            return True

    def random_shot(self, unshot) -> tuple:
        return random.choice(unshot)
    
    def __init__(self, target_board, hyman=True) -> None:
        self.win = False
        while True:
            try:
                shot = None
                if hyman:
                    print('Please make a shot: ', end=' ')
                    shot = tuple(map(int,list(input())))
                else:
                    shot = self.random_shot(target_board.unshot)
                if len(shot) == 2:
                    if self.shot_check(shot, target_board):
                        if not hyman: print(f'Enamy shot {shot}\n')
                        if shot in target_board.ships:
                            target_board.rm_ship(shot)
                            target_board.fields[shot] = 2
                            if hyman: target_board.fields_mist[shot] = 2
                            target_board.unshot = shot
                            if hyman:
                                print('Hit!\n')
                            else:
                                print('Enamy Hit\n')
                            if not target_board.ships:
                                self.win = True
                                break
                            continue
                        else:
                            target_board.fields[shot] = 3
                            if hyman: target_board.fields_mist[shot] = 3
                            target_board.unshot = shot
                            break
                    else:
                        if hyman: print('Try to do anather shot')
                        continue
                else:
                    if hyman: print('Please input two digit (example: 23): ')
                    continue
            except:
                if hyman: print('\nPlease input only digits!\n')
                continue

class BattleField:
    def __init__(self, player_board,enemy_board):
        self.__player_board = player_board
        self.__enemy_board = enemy_board

    def display_bf(self):
        def index():
            for n in range(1,7):
                yield n

        def digit_to_sign(value):
            if value == 0:
                    return "O"
            elif value == 1:
                    return "■"
            elif value == 2:
                    return "X"
            elif value == 3:
                    return "."

        board = f'\tENEMY BOARD\t\t\tPLAYER BOARD\n'    
        board += f'  | 1 | 2 | 3 | 4 | 5 | 6 |\t  | 1 | 2 | 3 | 4 | 5 | 6 |\n'
        for y in index():
            board += f"{y} "
            for x in index():
                board += f'| {digit_to_sign(self.__enemy_board.fields_mist[y,x])} '
            board += "|\t"
            board += f"{y} "
            for x in index():
                board += f'| {digit_to_sign(self.__player_board.fields[y,x])} '
            board += "|\n"
        return board    

class Game:
    def __init__(self) -> None:
        self.p_board = Board()
        self.e_board = EnamyBoard()
        self.bf = BattleField(self.p_board,self.e_board)
    
    def refresh(self) -> None:
        print(self.bf.display_bf())

    def ship_check(self, coordinates, any_board, hyman):

        def is_range(check_list):
            srt = sorted(check_list)
            return srt == list(range(srt[0], srt[0] + len(srt)))

            ### CHECK ON BUSY
        if all([True if any_board.fields[coordinate] == 0 else False for coordinate in coordinates]):
            ### CHECK ON NEAR BUSY
            if all([True if any_board.fields.get((coordinate[0]-1,coordinate[1])) != 1 else False for coordinate in coordinates])\
                and all([True if any_board.fields.get((coordinate[0]+1,coordinate[1])) != 1 else False for coordinate in coordinates])\
                and all([True if any_board.fields.get((coordinate[0],coordinate[1]-1)) != 1 else False for coordinate in coordinates])\
                and all([True if any_board.fields.get((coordinate[0],coordinate[1]+1)) != 1 else False for coordinate in coordinates]):
                ### HORIZONTAL ONE LINE CHECK
                if all(coordinate[0] == coordinates[0][0] for coordinate in coordinates):
                    if is_range([coordinate[1] for coordinate in coordinates]):
                        return True
                    else:
                        if hyman: print('No white spase can be in ship')
                        return
                ### VERTICAL ONE LINE CHECK
                elif all(coordinate[1] == coordinates[0][1] for coordinate in coordinates):
                    if is_range([coordinate[0] for coordinate in coordinates]):
                        return True
                    else:
                        if hyman: print('No white spase can be in ship')
                        return
                else:
                    if hyman: print('Ship must be in one line')
                    return
            else:
                if hyman: print('Ships are to close')
                return
        else:
            if hyman :print('Place for the ship is busy')
            return

    def initiate(self, any_board, hyman=True) -> None:
        greetings = {
            'Add coordinates of a Treaple-ship (example: 23 24 25): ':3,
            'Add coordinates of first Duble-ship (example: 23 24): ':2,
            'Add coordinates of second Duble-ship (example: 23 24): ':2,
            'Add coordinates of first Solo-ship (example: 23): ':1,
            'Add coordinates of second Solo-ship (example: 23): ':1,
            'Add coordinates of third Solo-ship (example: 23): ':1,
        }

        def rnd_coordinates(ship_size):
            rand_coordinates = []
            n = ship_size
            while n:
                n-=1
                rand_coordinates.append((random.randint(1, 6),random.randint(1, 6)))

            return rand_coordinates
        
        if hyman: print('Please set ships\n')
        for greeting,size in greetings.items():

            while True:
                if hyman: print(greeting, end='')
                try:
                    coordinates = []
                    if hyman:
                        coordinates = [tuple(map(int,list(n))) for n in input().split(' ')]
                    else:
                        coordinates = rnd_coordinates(size)

                    if len(coordinates) != size or not self.ship_check(coordinates, any_board, hyman):
                        continue
                    else:
                        any_board.ships = Ship(size,coordinates)
                        break
                except:
                    if hyman: print('\nPlease input only digits!\n')
                    continue

    def fight(self):
        while True:
            self.refresh()
            shot = Shot(self.e_board)
            if shot.win:
                print('CONGRATS! YOU ARE WIN')
                self.refresh()
                break
            self.refresh()
            shot = Shot(self.p_board, hyman=False)
            if shot.win:
                self.refresh()
                print('YOU ARE LOOSE')
                break

    def run(self):
        self.refresh()
        self.initiate(self.p_board, hyman=False)
        self.initiate(self.e_board, hyman=False)
        self.fight()

gm = Game()
gm.run()



