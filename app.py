from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

@app.route("/")
def survey_intro_page():
    """ Select your desired survey"""

     return render_template("survey_intro.html", survey=survey)


@app.route("/start", methods=["POST"])
def start_survey():
    "Starts Survey, clears repsonses"

    session[RESPONSES] = []

    return redirect("/questions/0")


@app.route("/questions/<int:qnum>")
def show_question(qnum):
    """shows current question"""
    responses = session.get(RESPONSES)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/thank-you")

    if (len(responses) != qnum):
        flash(f"You are trying to acces the incorrect question number: {qnum}.")
        return  redirect(f"/questions/{len(responses)}")

    question = survey.questions[qnum]
    return render_template("questions.html", question_number=qnum, question=question)


@app.route("/answer", methods=["POST"])
def handling_answer():
    """save response in list and redirect to next question"""

    choice = request.form['answer']

    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/thank-you")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/thank-you")
def thank_you_page():
    """All surveys are complete, show thank you page"""

    return render_template("thank-you.html")


    

