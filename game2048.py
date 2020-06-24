from flask import Flask, render_template, url_for, request
import random

app = Flask(__name__)

key = ''
score = 0
gamestate = [[ 0,16,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ],[ 0,0,0,0 ]]
message = ''

@app.route('/')
def home():
    global key, score, gamestate, message
    key = request.args.get('key')

    # if you reach 2048 you win!
    if any(32 in sublist for sublist in gamestate):
        message = 'You won!'
    
    elif key != '' and any (0 in sublist for sublist in gamestate):
        # we stack values horizontally if we press left or right
        if key == 'left' or key == 'right':
            for row in [0,1,2,3]:
                gamestate[row].sort()
                x = 0
                while(x < 3):
                    if (gamestate[row][x] == gamestate[row][x+1]) and gamestate[row][x] != 0:
                        gamestate[row][x] = gamestate[row][x]*2
                        gamestate[row][x+1] = 0
                        x += 2
                    x += 1
            if key == 'right':
                gamestate[row].sort()
                gamestate[row].reverse()
            else:
                gamestate[row].sort()
        # we add 2 in some random place if key is pressed and there are free spaces
        while (True):
            randx = random.randint(0,3)
            randy = random.randint(0,3)
            if gamestate[randy][randx] == 0:
                gamestate[randy][randx] = 2
                break
    
    return render_template('main.html', key=key, score=score, gamestate=gamestate, message=message)

if __name__ == '__main__':
    app.run(debug=True)