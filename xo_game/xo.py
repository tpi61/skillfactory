field = [
    ['_','_','_'],
    ['_','_','_'],
    ['_','_','_']
]

# check if the coordinates are correct
def coordinate_check(num_1,num_2):
    return (0 < num_1 <= len(field)) and (0 < num_2 <= len(field))

# occupied field checking
def field_check(num_1,num_2):
    if field[num_1-1][num_2-1] == '_':
        return True

# no comment        
def print_fild():
    print('  1 2 3')
    for caunt,value in enumerate(field, start=1):
        print(caunt, *value)

# no comment
def get_coordinate(sign):
    x,y = map(int,input(f'input coordinates for {sign}: '))
    return [x,y]

# put mark on the field
def lets_play(sign):
    lets_play = True
    while lets_play:
        coordinates = get_coordinate(sign)
        if coordinate_check(*coordinates) and field_check(*coordinates):
            field[coordinates[0]-1][coordinates[1]-1] = sign
            print_fild()
            lets_play = False
        else:
            continue

# XO generator
def repeat_sign(sig_list):
    while True:
        for i in sig_list:
            yield str(i)

def winner_check(field,sign):
    n = len(field)
    win = True

    # check rows
    for y in range(n):
        win = True
        for x in range(n):
            if field[y][x] != sign:
                win = False
                break
        if win:
            return win

    # check col
    for y in range(n):
        win = True
        for x in range(n):
            if field[x][y] != sign:
                win = False
                break
        
        if win:
            return win
    
    # check diagonal
    for x in range(n):
        win = True
        if field[x][x] != sign:
            win = False
            break

    if win:
        return win
    
    # check back diagonal    
    for x in range(n):
        win = True
        if field[x][n-1-x] != sign:
            win = False
            break
    
    if win:
        return win
    
print_fild()
for sign in repeat_sign(['X','O']):
    lets_play(sign)
    if winner_check(field,sign):
        print(f'\ncongrats {sign} is winner!')
        break