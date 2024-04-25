# ==== Import  Libraries ====
from cs50 import SQL
# * flask import
from flask import Flask, flash, redirect, render_template, request, session, make_response
from flask_session import Session
# * library for safer password
from werkzeug.security import check_password_hash, generate_password_hash
# * import json
import json
# * my functions
from helpers import login_required

# ==== Description====
descriptions = []
with open("static/txt/pomidors_description.txt", "r") as file:
    lines = file.readlines()
for line in lines:
    index, text = line.split('.\t')
    name, description = text.split(':')
    # print(index, name, description)
    description = {"index": int(index)-1,
                   "name": name,
                   "description": description}
    descriptions.append(description)

# ==== Configure application ====
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# ==== Configure CS50 LibrXXXary to use SQLite database ====
db = SQL("sqlite:///pomidoro.db")

# ==== ROUTES ====


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # todo make for user
    # REQUEST METHOD POST - setting times
    if request.method == "POST":
        # access individual set time values through name from form and make sure it is a number
        try:
            workMins = int(request.form.get("workMins"))
            workSecs = int(request.form.get("workSecs"))
            breakShortMins = int(request.form.get("breakShortMins"))
            breakShortSecs = int(request.form.get("breakShortSecs"))
            breakLongMins = int(request.form.get("breakLongMins"))
            breakLongSecs = int(request.form.get("breakLongSecs"))
        except ValueError:
            return redirect("/")

        # make sure time is correct
        workMins = workMins if workMins < 60 else 59
        workSecs = workSecs if workSecs < 60 else 59
        breakShortMins = breakShortMins if breakShortMins < 60 else 59
        breakShortSecs = breakShortSecs if breakShortSecs < 60 else 59
        breakLongSecs = breakLongSecs if breakLongSecs < 60 else 59
        breakLongMins = breakLongMins if breakLongMins < 60 else 59

        # update usersTimeSettings table
        db.execute("""
                    UPDATE usersTimeSettings
                    SET
                        workMins = ?,
                        workSecs = ?,
                        breakShortMins = ?,
                        breakShortSecs = ?,
                        breakLongMins = ?,
                        breakLongSecs = ?
                    WHERE users_id = ?""", workMins, workSecs, breakShortMins, breakShortSecs, breakLongMins, breakLongSecs, session["user_id"]
                   )
        return redirect("/")
    # REQUEST METHOD GET
    db_TimeSettings = db.execute(""" 
        SELECT * FROM usersTimeSettings
        WHERE users_id = ?""", session["user_id"]
                                 )

    # check if loaded settings from database
    if not db_TimeSettings:
        return render_template("index.html", mes="Error loading TimeSet")

    # load time settings from json
    users_time_settings = json.dumps(db_TimeSettings[0])

    # read level from users database
    level = db.execute("""
                SELECT level FROM users
                WHERE id = ?""", session["user_id"]
                       )
    message = "Hello, message"
    return render_template("index.html",
                           user_username=session["user_username"],
                           users_time_settings=users_time_settings,
                           mes=message,
                           level=level[0]["level"])


@app.route("/login", methods=["GET", "POST"])
def login():
    # == Forget users_id if somehow here and logged in ==
    session.clear()
    # REQUEST METHOD POST
    if request.method == "POST":
        # == Validate Inputs ==
        # validate username
        if not request.form.get("username"):  # *check if anything in username
            return render_template("login.html",
                                   errormessage="Username required")
        # get username from form and strip it from whitespace
        username = request.form.get("username").strip()
        # validate password
        if not request.form.get("password"):  # *check if anything in password
            return render_template("login.html",
                                   errormessage="Password required")
        password = request.form.get("password")

        # == Check database for user/password ==
        # query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # *check if username exists and password ok
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            return render_template("login.html",
                                   errormessage="Wrong username or password")

        # == Remember which user has logged in ==
        session["user_username"] = rows[0]["username"]
        session["user_id"] = rows[0]["id"]
        session["click"] = 0

        return redirect("/")
    # REQUEST METHOD GET
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    # == Clear user_id ==
    session.clear()
    # == Flash info and redirect to login ==
    flash("Logged out!")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    # == Forget users_id if somehow here and logged in ==
    session.clear()
    # REQUEST METHOD POST
    if request.method == "POST":
        # == Validate Inputs ==
        # validate username
        if not request.form.get("username"):  # *check if anything in username
            return render_template("register.html",
                                   errormessage="Username required")
        # get username from form and strip it from whitespace
        username = request.form.get("username").strip()
        # validate password
        if not request.form.get("password"):  # *check if anything in password
            return render_template("register.html",
                                   errormessage="Password required")
        password = request.form.get("password")
        if len(password) < 2:  # *check if password has acceptable length
            return render_template("register.html",
                                   errormessage="Password needs to have at least 2 char")
        if password != request.form.get("confirm"):  # * check confirmation
            return render_template("register.html",
                                   errormessage="Passwords are NOT the same")
        # == Check if given username already in database ==
        check_username = db.execute("""
                   SELECT * FROM users
                   WHERE username = ?""", username)
        if check_username != []:
            return render_template("register.html",
                                   errormessage=f"Username '{username}' already exists. Try something else!")
        # == Insert username/hash(password) into users database ==
        db.execute("""
                   INSERT INTO users
                   (username, password_hash) VALUES
                   (?, ?)""", username, generate_password_hash(password, method="scrypt")
                   )

        #!!!! --- idk if that matters
        ''' USING USERNAME IN SESSION FOR NOW '''
        # *find id of inserted user
        user_id = db.execute("""
                   SELECT id FROM users
                   WHERE username = ?""", username
                             )

        # == Insert username into usersTimeSettings database ==
        db.execute("""
                   INSERT INTO usersTimeSettings 
                   (users_id) VALUES
                   (?)""", user_id[0]['id']
                   )

        # *add 2 values into session
        session["user_username"] = username
        session["user_id"] = user_id[0]['id']

        # == Redirect to main page ==
        flash("Registered!")
        return redirect("/")

    # REQUEST METHOD GET
    return render_template("register.html")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    # /history displays everything from databases
    # REQUEST METHOD POST
    if request.method == "POST":
        # todo request post inserts pomidors into database
        # get earned pomidors from json sent by fetch
        earned_pomidors = request.get_json()['earned_pomidors']
        # get action type from json sent by fetch
        action_type = request.get_json()['action_type']
        # update earned pomidors
        db.execute("""
                   UPDATE users 
                   SET pomidors = pomidors + ?
                   WHERE id = ?""", earned_pomidors, session["user_id"]
                   )
        db.execute("""
                    INSERT INTO usersHistory
                   (users_id, action_type, pomidors_number)
                   VALUES (?, ?, ?)
                   """, session["user_id"], action_type, earned_pomidors
                   )
        # return in fetch
        return redirect("/history")

    # REQUEST METHOD GET
    usersHistory_table = db.execute("""
                SELECT  u."username", 
                        uH."timestamp_info",
                        uH."action_type",
                        CASE
                            WHEN uH."action_type" = 'buy' THEN ('-' || uH."pomidors_number")
                            WHEN uH."action_type" = 'reward' THEN ('+' || uH."pomidors_number")
                            WHEN uH."action_type" = 'train' THEN ('-' || uH."pomidors_number")
                            WHEN uH."action_type" = 'unlock' THEN ('🔓')
                        END             
                    FROM usersHistory as uH
                    JOIN users AS u ON uH.users_id = u.id
                WHERE users_id = ?
                ORDER BY uH."timestamp_info" DESC""", session["user_id"]
                                    )
   # read level from users database
    level = db.execute("""
                SELECT level FROM users
                WHERE id = ?""", session["user_id"]
                       )
    return render_template("history.html",
                           user_username=session["user_username"],
                           usersHistory_table=usersHistory_table,
                           level=level[0]["level"])


@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    # REQUEST METHOD POST - add comment to usersComments table
    if request.method == "POST":
        comment = request.form.get("comment")
        if comment:
            db.execute("""
                    INSERT INTO usersComments
                    (users_id, comment) VALUES 
                    (?, ?)""", session["user_id"], comment
                       )
            return redirect("/feedback")
        # empty form submitted - redirect
        else:
            return redirect("/feedback")
    # REQUEST METHOD GET
    # get all the comments from usersComments
    comments = db.execute("""
                SELECT u.username, uC.comment, uC.timestamp_info
                 FROM usersComments AS uC
                 JOIN users AS u ON uC.users_id = u.id
                ORDER BY uC.timestamp_info DESC
                """)
    # read level from users database
    level = db.execute("""
                SELECT level FROM users
                WHERE id = ?""", session["user_id"]
                       )

    return render_template("feedback.html",
                           user_username=session["user_username"],
                           comments=comments,
                           level=level[0]["level"]
                           )


@app.route("/shop", methods=["GET", "POST"])
@login_required
def shop():
    # REQUEST METHOD POST
    if request.method == "POST":
        value = int(request.form.get("prices"))
        # check if enough pomidors
        pomidors = db.execute("""
                SELECT pomidors, level, experience FROM users WHERE id = ?
                              """, session["user_id"])
        if value > pomidors[0]["pomidors"]:
            # * check how many medals user has
            medals = db.execute("""
                                SELECT gold, silver, bronze
                                FROM usersMedals
                                WHERE users_id = ?""", session["user_id"]
                                )
            # * if any medals then assign value, else 0
            if medals:
                gold = medals[0]['gold']
                silver = medals[0]['silver']
                bronze = medals[0]['bronze']
            else:
                gold, silver, bronze = 0, 0, 0
            return render_template("shop.html",
                                   errorm="NOT ENOUGH POMIDORS",
                                   pomidors=pomidors[0]["pomidors"],
                                   experience=pomidors[0]["experience"],
                                   level=pomidors[0]["level"],
                                   descriptions=descriptions,
                                   user_username=session["user_username"],
                                   gold=gold,
                                   silver=silver,
                                   bronze=bronze
                                   )
        # update pomidors after transaction
        db.execute("""
                   UPDATE users 
                   SET pomidors = pomidors - ?
                   WHERE id = ?""", value, session["user_id"]
                   )
        # add transaction to usersHistory table

        db.execute("""
                   INSERT INTO usersHistory
                   (users_id, action_type, pomidors_number) VALUES
                   (?, ?, ?)""", session["user_id"], "buy", value
                   )
        # check if user has any medals
        medals = db.execute("""
                            SELECT * FROM usersMedals
                            WHERE users_id = ?""", session["user_id"]
                            )
        if not medals:
            # just create new user
            db.execute("""
                    INSERT INTO usersMedals
                   (users_id) VALUES
                   (?)""", session["user_id"]
                       )
        # add medal to usersMedals
        db.execute("""
                UPDATE usersMedals
                SET
                    bronze = CASE
                                WHEN ? = 20 THEN bronze + 1
                                ELSE bronze
                             END,
                    silver = CASE
                                WHEN ? = 50 THEN silver + 1
                                ELSE silver
                            END,
                    gold = CASE
                                WHEN ? = 100 THEN gold + 1
                                ELSE gold
                            END
                WHERE users_id = ?
                    """, value, value, value, session["user_id"]
                   )
        # flash information about purchased value
        flash(f"Bought medal for 🍅{value}")
        return redirect("/shop")

    # REQUEST METHOD GET
    users_info = db.execute("""
                SELECT pomidors, level, experience FROM users WHERE id = ?
                """, session["user_id"]
                            )
    # * check how many medals user has
    medals = db.execute("""
                        SELECT gold, silver, bronze
                        FROM usersMedals
                        WHERE users_id = ?""", session["user_id"]
                        )
    # * if any medals then assign value, else 0
    if medals:
        gold = medals[0]['gold']
        silver = medals[0]['silver']
        bronze = medals[0]['bronze']
    else:
        gold, silver, bronze = 0, 0, 0
    # jsonify pomidors descriptions
    # print(f"level is {users_info[0]['level']} which is {type()}")
    # descriptions_json = json.dumps(descriptions)
    # generate response with no cache
    response = make_response(render_template("shop.html",
                                             user_username=session["user_username"],
                                             pomidors=users_info[0]["pomidors"],
                                             experience=users_info[0]["experience"],
                                             level=users_info[0]["level"],
                                             descriptions=descriptions,
                                             gold=gold,
                                             silver=silver,
                                             bronze=bronze))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/addExperience", methods=["POST"])
@login_required
def addExperience():
    if request.method == "POST":
        # try to get experience and action type
        try:
            # get experience from user
            experience = int(request.get_json()['experience'])
            # get action type from json sent by fetch
            action_type = request.get_json()['action_type']

            # update experience to
        except ValueError:
            return redirect("/shop")

        # check if enough pomidors
        pomidors = db.execute("""
                SELECT pomidors from users WHERE id = ?
                                """, session["user_id"])
        # refresh page if not enough experience or less than 0
        if experience > pomidors[0]["pomidors"] or experience <= 0:
            return redirect("/shop")

        # update pomidors count, experience
        db.execute("""
                UPDATE users
                SET
                    pomidors = pomidors - ?,
                    experience = experience + ?
                WHERE id = ?""", experience, experience, session["user_id"]
                   )
        # update usersHistory
        db.execute("""
                INSERT INTO usersHistory
                (users_id, action_type, pomidors_number) VALUES
                (?, ?, ?)""", session["user_id"], action_type, experience
                   )
        return redirect("/")


@app.route("/updateLevel", methods=["POST"])
@login_required
def updateLevel():

    # try to get level from fetch
    try:
        # get level
        level = int(request.get_json()['level'])
    except ValueError:
        return redirect("/shop")
    # change users level
    db.execute("""
            UPDATE users
            SET
                level = ?
            WHERE id = ?""", level, session["user_id"]
               )
    # update usersHistory
    db.execute("""
           INSERT INTO usersHistory
                   (users_id, action_type, pomidors_number)
                   VALUES (?, ?, ?)
                   """, session["user_id"], 'unlock', 0
               )

    return redirect("/shop")
