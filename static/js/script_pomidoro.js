// TODO: ======== todo ========

// ==== VARIABLES ====
// external global variables from database
// *usersTimeSettings object
let usersTimeSettings = JSON.parse(globalTimeSettings);

// set time and running time
//* set time to work at the beggining
let minutesSet = usersTimeSettings.workMins;
let secondsSet = usersTimeSettings.workSecs;
//* running time:
let minutesRun = minutesSet;
let secondsRun = secondsSet;
//* intervalID - I want to reset instant
let intervalId;
// let level = document.getElementById("usersLevel").innerHTML;


// flags
let countdownStarted = false;
let countdownPaused = false; //* stops timer
let cycleInfo = 0; //* how many work times passed
//* is it ok that mode has names like id from info?
let currentMode = "mode--work";

// ==== DISPLAY TIME ====
window.onload = () => {
  displayTime(minutesSet, secondsSet);
  displayTimeSetting();
}

function displayTime(min, sec) {
  document.getElementById('minutes').innerHTML = min.toString().padStart(2, '0');
  document.getElementById('seconds').innerHTML = sec.toString().padStart(2, '0');;
}
function displayTimeSetting() {
  document.getElementById('setWorkMins').value = usersTimeSettings.workMins.toString().padStart(2, '0');
  document.getElementById('setWorkSecs').value = usersTimeSettings.workSecs.toString().padStart(2, '0');


  document.getElementById('setBreakShortMins').value = usersTimeSettings.breakShortMins.toString().padStart(2, '0');
  document.getElementById('setBreakShortSecs').value = usersTimeSettings.breakShortSecs.toString().padStart(2, '0');


  document.getElementById('setBreakLongMins').value = usersTimeSettings.breakLongMins.toString().padStart(2, '0');
  document.getElementById('setBreakLongSecs').value = usersTimeSettings.breakLongSecs.toString().padStart(2, '0');
}
// ==== MANAGE MODES ====

function switchMode(modeName) {
  currentMode = modeName;
}


function switchToNextMode() {
  // == Switch modes function => work, shortBreak, work, shortBreak, work, longBreak ==
  // *cycleInfo - global variable tells how many work cycles passed
  if (currentMode == "mode--work" && cycleInfo % 3 != 2) {
    //* increase cycle info after successfully finishing work
    cycleInfo++;
    switchMode("mode--break-short");
    // *add an active class
    activateMode(currentMode);
  }
  else if (currentMode == "mode--work" && cycleInfo % 3 == 2) {
    //* increase cycle info after successfully finishing work
    cycleInfo++;
    switchMode("mode--break-long");
    // *add an active class
    activateMode(currentMode);
  }
  else {
    switchMode("mode--work");
    // *add an active class
    activateMode(currentMode);
  }
}



function activateMode(modeName) {
  /* 
    Activate mode function adds an "active" class 
    to a proper mode in mode info in HTML
 */
  work = document.getElementById("mode--work")
  break_short = document.getElementById("mode--break-short")
  break_long = document.getElementById("mode--break-long")

  if (modeName == "mode--work") {
    work.classList.add("active")
    break_short.classList.remove("active")
    break_long.classList.remove("active")
  }
  else if (modeName == "mode--break-short") {
    break_short.classList.add("active")
    work.classList.remove("active")
    break_long.classList.remove("active")
  }
  else if (modeName == "mode--break-long") {
    break_long.classList.add("active")
    work.classList.remove("active")
    break_short.classList.remove("active")
  }
}

function updateSetTimeByMode(modeName) {
  switch (modeName) {
    case "mode--work":
      minutesSet = usersTimeSettings.workMins;
      secondsSet = usersTimeSettings.workSecs;
      break;
    case "mode--break-short":
      minutesSet = usersTimeSettings.breakShortMins;
      secondsSet = usersTimeSettings.breakShortSecs;
      break;
    case "mode--break-long":
      minutesSet = usersTimeSettings.breakLongMins;
      secondsSet = usersTimeSettings.breakLongSecs;
      break;
    default:
      console.log("Hello World");
  }
  resetTimer();
  displayTime(minutesSet, secondsSet);
}

// Event listener to .pomidoro__info to change modes
//* == get to children IDs using Event Bubbling ==
//*  event.target.id
let pomidoro__info = document.querySelector(".pomidoro__info");
pomidoro__info.addEventListener("click", function (event) {

  switchMode(event.target.id);
  updateSetTimeByMode(currentMode);
  activateMode(currentMode);

});


// ==== MANAGE TIMER ====


function startTimer() {
  /* This function will start the timer when:
  *1 - flag countdownStarted is false
  *2 - flag countdownStarted true, but counter was paused */
  if (!countdownStarted) {
    countdown(minutesSet, secondsSet);
  }
  else if (countdownStarted && countdownPaused) {
    //* unpause
    countdownPaused = false;
    //* if paused run with global timerunning values 
    countdown(minutesRun, secondsRun);
  }

}

function pauseTimer() {
  // set countdownPaused flag to true when button clicked
  //** you can pause only when countdownStarted - 1 empty run and stop
  if (countdownStarted) {
    countdownPaused = true;
    clearInterval(intervalId);
  }
}

function resetTimer() {
  // Reset timer function 
  //** clear global intervalId
  if (intervalId) {
    clearInterval(intervalId);
    //** display resetted time
    displayTime(minutesSet, secondsSet)
    //** reset flags
    countdownStarted = false;
    countdownPaused = false; //** stops timer
  }
}


function countdown(minutes, seconds) {
  // = Countdown function = 
  // *use global variables to keep current time
  minutesRun = minutes;
  secondsRun = seconds;
  // *flag countdownStarted turned on
  countdownStarted = true;
  // countdownLoop funcition looping every 1s
  let countdownLoop = () => {
    // * -1 seconds 
    if (secondsRun > 0) { secondsRun--; }
    //  *check if finished counting - if yes than READY TO EXIT
    if (secondsRun == 0 && minutesRun == 0) {
      //* stop coutdownLoop
      clearInterval(intervalId);
      //* last change of HTML
      displayTime(minutesRun, secondsRun);
      //* reset flag variable
      countdownStarted = false;
      // !!!!!!!!!!!!!!!!!!!!
      // add pomidors after completing work timer

      setTimeout(() => {
        if (currentMode == "mode--work" && minutesSet > 4) {
          addEarnedPomidors(minutesSet);

        };
        switchToNextMode();
        updateSetTimeByMode(currentMode);
        return 0;
      }, 10);
    }
    else if (secondsRun == 0) {
      // * -1 minutes and reset seconds to 59
      minutesRun--;
      secondsRun = 59;
    }
    //* if coundown paused clear Interval
    if (countdownPaused) { clearInterval(intervalId); }
    // *change display HTML = every loop
    displayTime(minutesRun, secondsRun)
  }
  // set interval to 1s for countdownLoop function
  intervalId = setInterval(countdownLoop, 1000); //*1000 = 1s
}


function updateSetTimeByInput() {
  // = Update timer by input function = 
  // update work only when timer paused or not started
  if (countdownPaused | !countdownStarted) {
    //* update minutesSet and work Seconds
    //* by getting their values from "set_minutes" and "set_seconds" input
    minutesSet = document.getElementById("set_minutes").value;
    secondsSet = document.getElementById("set_seconds").value;
    //make sure time is correct if more than 59 or less than 0 set to 59
    minutesSet = minutesSet < 59 && minutesSet >= 0 ? minutesSet : 59;
    secondsSet = secondsSet < 59 && secondsSet >= 0 ? secondsSet : 59;
    displayTime(minutesSet, secondsSet);
    //* user settings BREAK minutes
    resetTimer();

  }

}


// ==== Fetch info to server to add pomidors to database ====
function addEarnedPomidors(earned_pomidors) {
  // == add earned pomidors to pomidors count == 
  const data = { 'earned_pomidors': earned_pomidors, 'action_type': 'reward' };

  fetch('/history', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data),
  })


  alert("✨ You just earned 🍅" + earned_pomidors + " pomidors! ✨\n" + "Now have a little break 😺");
}

// ==== SHOW/HIDE POMIDORO SET TIME MENU ====

function showHideTimeSettings() {
  random = document.getElementsByClassName("pomidoro__setTimeWindow offscreen");
  // remove default offscreen class
  if (random[0]) {
    random[0].classList.remove("offscreen")
  }
  // add class if offscreen not present
  else {
    random = document.getElementsByClassName("pomidoro__setTimeWindow");
    random[0].classList.add("offscreen")
  }
}


