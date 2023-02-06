from boggle import Boggle
from flask import Flask, request, session, render_template, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



@app.route('/', methods = ['GET'])
def setup():
       """ generate game board and save it in storage, redirect to /play"""
       session['game_board'] = boggle_game.make_board()
       return redirect('/play')

@app.route('/play')
def disp_board():
    """ render html using current gameboard"""
    return render_template('base.html', board = session['game_board'])

@app.route('/play', methods =['POST'])
def respond_guess():
    """interpret user guess check if its valid. respond back with status and the guess"""
    user_guess = request.json['guess']
    word_status = boggle_game.check_valid_word(session['game_board'], user_guess)
    resp = {'status': word_status, 'guess': user_guess}
    return jsonify(resp)

@app.route('/update', methods = ['POST'])
def update_score():
    """interpret request icluding the current score. """
    # set high score
    last_score = request.json['score']
    print(last_score)
    high_score = session.get('high_score', last_score)
    if last_score >= high_score:
        session['high_score'] = last_score

    return jsonify(update_session())

def update_session():
    """increment number of plays and generate a response for front end with high score and num plays data"""
    # increment number of plays
    plays = session.get('num_plays', 0)
    plays +=1
    session['num_plays'] = plays

    #create response including num_plays and highscore
    resp = {'highScore': session['high_score'], 'numPlays': session['num_plays']}
    return resp