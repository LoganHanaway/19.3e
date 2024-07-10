from flask import Flask, render_template, redirect, session, request, flash
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/begin', methods=["POST"])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get('responses')

    if responses is None:
        return redirect('/')
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
    if len(responses) != qid:
        flash("Invalid question number")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', survey=satisfaction_survey, question_num=qid, question=question)

@app.route('/answer', methods=["POST"])
def handle_answer():
    answer = request.form['answer']
    qid = int(request.form['qid'])

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/complete')
def complete():
    return render_template('complete.html', survey=satisfaction_survey)

if __name__ == '__main__':
    app.run(debug=True)
