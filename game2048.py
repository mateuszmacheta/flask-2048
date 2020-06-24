from flask import Flask, render_template, url_for, request
import random

app = Flask(__name__)

def add_two(mat):
    # we add 2 in some random place if key is pressed and there are free spaces
    while (True):
        randx = random.randint(0,3)
        randy = random.randint(0,3)
        if mat[randy][randx] == 0:
            mat[randy][randx] = 2
            break
    return mat

def transpose_arr(mat):
    mat = [list(x) for x in zip(*mat)]
    return mat

def reduce_tiles(mat, key, score):
    #print('mat init: ', mat)
    if  key == 'up' or key == 'down':
        mat = transpose_arr(mat)
    #print('mat trans: ', mat)
    for row in [0,1,2,3]:
        # remove zeroes - build temp_row list
        temp_row = mat[row]
        #print('temp_row: ', temp_row)
        mat[row] = [0,0,0,0]
        temp_row = [i for i in temp_row if i != 0]
        # reduce the same numbers
        x = 0
        while(x < len(temp_row)-1):
            if (temp_row[x] == temp_row[x+1]):
                temp_row[x] = temp_row[x]*2
                score += temp_row[x]
                temp_row.pop(x+1)
                x += 2
            x += 1
        # remove zeroes again
        #print('temp_row: ', temp_row)
        temp_len = len(temp_row)
        #print('temp_len: ', temp_len)
        if key == 'right' or key == 'down':
            temp_row.reverse()
        for x in range(temp_len):
            #print('x: ', x)
            if key == 'left' or key == 'up':
                mat[row][x] = temp_row[x]
            else:
                mat[row][3-x] = temp_row[x]
        #print('mat[row] post-temp: ', mat[row])
    if  key == 'up' or key == 'down':
        mat = transpose_arr(mat)
    #print('mat final: ', mat)
    return mat, score

def game_reset():
    gamestate = [[ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ]]
    gamestate = add_two(gamestate)
    score = 0
    message = ''
    return  gamestate, score, message

winValue = 2048
key = ''
score = 0
gamestate = [[ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ]]
gamestate = add_two(gamestate)
message = ''
   

@app.route('/')
def home():
    global key, score, gamestate, message, winValue
    key = request.args.get('key')
    reset = request.args.get('reset')

    # if you reach winValue you win!
    if any(winValue in sublist for sublist in gamestate):
        message = 'You won!'
    
    elif key != '' and any (0 in sublist for sublist in gamestate):
        # we stack values horizontally if we press left or right
        gamestate, score = reduce_tiles(gamestate, key, score)
        gamestate = add_two(gamestate)
    
    else:
        message = 'You lost!'

    if reset == '1':
        gamestate, score, message = game_reset()

    return render_template('main.html', key=key, score=score, gamestate=gamestate, message=message)

if __name__ == '__main__':
    app.run(debug=True)