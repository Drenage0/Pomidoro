# CS50x-Final-Project

🍅Final project after completing CS50x🍅

# POMIDORO website

#### Video Demo: https://youtu.be/3N1mWEpvv7g

## Description:

### == 🍅Overview🍅 ==

<div style="background-color: salmon;
            color: whitesmoke;
            text-shadow: 1px 1px 5px black;
            padding: 2rem">
Pomidoro website is my little tweak on popular 'Pomodoro' timer application.
In a nutshell it is a website that you can use to organize study time and receive rewards after you complete work mode cycle that is more or equal to 10 minutes. Why 'Pomidoro'? 'Pomidor' is a polish word for 'tomato' and it sounds similar to 'Pomodoro' so I thought why not do 'Pomodoro' but with a slight tomato motive.

Well... I thought I was being original, but 'pomodoro' actually was called after
the tomato-shaped kitchen timer('timer a forma di pomodoro') that Francesco Cirillo, the Italian inventor of the Pomodoro Technique, used during its development.

</div>
There are 3 modes on the website:

- work mode - time to study (default time 25 minutes)
- short break (default time 5 minutes)
- long break (default time 15 minutes)

Modes come in order: work-s_break-work-s_break-work-l_break and repeat.
For every completed work mode you receive 'pomidors' - fake currency that you can later spend on a shop page. Times of modes are adjustable in two places:

- quick set time input on main screen (NOT saved - one time setup)
- set time window in settings menu (Saved in database after adjusting)

You can jump between modes using 'pomidoro--info' controls right above
'pomidoro--setTime' input which is the quick set time input described before.

After starting timer you can pause/restart/unpause it using 'pomidoro--controls' controls below timer.

In the right corner there are settings appearing after hovering over gear icon and
users username. Frome there you can navigate between other websites, log out and set times for modes that will be saved in database.

A brief description of websites linked in settings menu:

- Pomidoro - main page with timer
- Shop - website where you can spend 'pomidors' in two ways. At first you can buy medals which will be displayed in your 'medals display case'. Other option is to spend 'pomidors' on experience which will unlock 'Wisdom Pomidors' representing your level of engagement and wizdom obtained during learning. After gaining enough experience points 'unlock button' will show up and after clicking it there will be an animation unlocking colorful 'Wisdom Pomidor', its name and description. Moreover unlocked 'Wizdom Pomidor' will also be present in the main header on every website.
- History - website tracking users actions: receiving rewards, buying medals,
  training(spending 'pomidors' on experience) and unlocking 'Wisdom Pomidors'.
- Feedback - website where users can leave comments and give feedback

== Explaining files structure ==
Pomidoro project is written using HTML/CSS/JavaScript/Python. Also it uses GIT to connect to my GitHub profile. The project contains files according to flask files structure. From the main folder we can see (excluding 'pycache' , '.git' and 'flask_session' folders which are created automatically):

- 'static' folder - it contains all static files used in project: icons, images, JS scripts, CSS stylesheet, and a text file
- 'templates' folder - contains all HTML files. There is one layout.html file that is the shared part of HTML for all websites, and other HTML files that have different content written using Jinja template

Except folders inside Pomidoro project we can find:

- app.py - main python file containing all server side logic
- helpers.py - helpers python file with functions for app.py
- helpers.sql - helpers SQL code for quicker database manipulation, inserting tables etc.
- pomidoro.db - database containing all tables used in project
- README.md - This file 🙂

### == 🍅Design choices and encountered challenges🍅 ==

The project itself is probably not most complicated and for sure is not perfectly written, but it allowed me in rather interesting way to solidify my understanding of topics covered in CS50x course. In my Pomidoro project I used:

- Flask framework to manage routing between websites, handling session, doing server side validation, using decorators
- Jinja template to connect all HTML templates with one shared layout, conditionally display certain elements on the page, using for loop to display reapeted fragments of code
- SQLite database to store personalized information for every registered user. In total I used 5 tables: 'users'(id/username/hashed password/number of pomidors, current level and experience), 'usersTimeSettings'(individual times for modes), 'usersHistory'(track of users actions and time when they took place), 'usersComment'(comments posted by users), 'usersMedals'('count of purchased items'). Tables are relative by unique user_id.
- JavaScript to manipulate the DOM, send forms to server and fetch data from client to server using JSON. There are 2 JS scripts - one for page with timer, other for the shop.

It doesn't make much sense to explain every line of code, instead I will mention few things I got to learn thanks to that project:

- sending information, variables between Python HTML and JavaScript. One of the challenges I encountered was updating database when user will perform certain action. One example is updating user database with new pomidoro count when timer completes. It is done by using fetch in JavaScript. The function is called right before switching to another mode
- changing background colors using CSS - I could probably do that by using JS, but it was really fun to learn about :has pseudo-class that lets you modify style of the parent element according to something changing inside of its child element. In my project this 'something' is a class '.active' that I add using JS to <p> elements with a class name of 'pomidoro\_\_info--item' inside index.html
- making 'Unlock Wisdom Pomidors' section inside shop.html. 'Pomidors' were generated using DALL·E, and their descriptions using GPT4. I combined images in GIMP to make one image called Wizdom_pomidors.png. So every displayed picture is just a one picture with different XY positions. Also unlocking animation is achieved by changing background-position-y by 150px. Descriptions and names are stored inside of the pomidors_description.txt. In app.py I created a global variable 'descriptions' which is a list of dictionaries containing the 'Pomidors' data. This information is sent during '/shop' routing.
- storing data inside databases, making my own relational databases, selecting information from databases using CASE statement

### == 🍅Future improvement plans for Pomidoro🍅 ==

I know that probably many of the solutions I used in my project are not optimal. However I'm glad that this project is some sort of a skeleton that I plan to flesh out with additional functionalities and refine its design for better optimization and visual appeal. Some of the ideas for improvement:

--Additional features --

- make some sort of guest visitor that will not require registration/login to use the website, but at the same time it will cut off some functionalities - guest will only be able to use timer and won't get any rewards. Instead he will have some notifications/advertisements encouraging to register
- history page with sorting/filtering
- feedback comments with likes/replies/edit/delete/filtering/sorting
- adding more stuff to shop (sounds, color modes, more items)

-- Improve visual appeal --

- more responsive design for smaller screens (using dynamic font size, changing layout on smaller screens)
- animation for the timer and better animations for unlocking 'Wizdom Pomidors'
- sounds
- changing medals looks to be more 'pomidor' related
- changing descriptions/names to be more epic xd

-- Code changes --

- change how the setTime is stored in usersTimeSettings table (probably there is a better
  data type to store time than minutes/seconds separately)
- more password validation, changing hashing method to more secure one
- more precise CSS BEM standardization

-- Asking others --

- Asking other people about advices/code review in order to see other perspective about ways to improve this project
