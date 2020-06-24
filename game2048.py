from flask import Flask, render_template, url_for, request
import random

app = Flask(__name__)

key = ''
score = 0
gamestate = [[ 0,2,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ]]
message = ''

def add_two(mat):
    # we add 2 in some random place if key is pressed and there are free spaces
    while (True):
        randx = random.randint(0,3)
        randy = random.randint(0,3)
        if mat[randy][randx] == 0:
            mat[randy][randx] = 2
            break
    return mat

def reduce_horizontal(mat, key):
    for row in [0,1,2,3]:
        # remove zeroes - build temp_row list
        temp_row = mat[row]
        mat[row] = [0,0,0,0]
        temp_row = [i for i in temp_row if i != 0]
        # reduce the same numbers
        x = 0
        while(x < len(temp_row)-1):
            if (temp_row[x] == temp_row[x+1]):
                temp_row[x] = temp_row[x]*2
                temp_row.pop(x+1)
                x += 2
            x += 1
        # remove zeroes again
        print('temp_row: ', temp_row)
        temp_len = len(temp_row)
        print('temp_len: ', temp_len)
        if key == 'righ':
            temp_row.reverse()
        for x in range(temp_len):
            print('x: ', x)
            if key == 'left':
                mat[row][x] = temp_row[x]
            else:
                mat[row][3-x] = temp_row[x]
        print('mat[row] post-temp: ', mat[row])
    print('mat final: ', mat)
    return mat
    

@app.route('/')
def home():
    global key, score, gamestate, message
    key = request.args.get('key')

    # if you reach 2048 you win!
    if any(32 in sublist for sublist in gamestate):
        message = 'You won!'
    
    elif key != '' and any (0 in sublist for sublist in gamestate):
        # we stack values horizontally if we press left or right
        gamestate = reduce_horizontal(gamestate, key)
        gamestate = add_two(gamestate)
    
    else:
        message = 'You lost!'

    return render_template('main.html', key=key, score=score, gamestate=gamestate, message=message)

if __name__ == '__main__':
    app.run(debug=True)