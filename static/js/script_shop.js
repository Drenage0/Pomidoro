let level = document.getElementById("usersLevel").innerHTML;
console.log(level);
window.onload = () => {
}


function addExperience() {
  /* add Experience function calls /addExperience
  where experience is updated in users database */
  const experience = document.getElementById("inputRange").value;
  const data = { 'experience': experience, 'action_type': 'train' };

  fetch('/addExperience', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data),
  })
    // page needs to reload after updating experience
    .then(response => response.text())
    .then(html => {

      // window.location.href = '/'; //* alternative reload page to the top
      location.reload();

    })
    //catch error if it happens
    .catch(error => console.error('Error', error));
}


function unlockPomidor(element) {
  /* 
  unlockPomidor function unlock wizdom pomidor
  and call updateUsersLevel func 
   */
  const value = element.value
  const toUnlockElement = document.getElementsByClassName(
    'unlock__element--' + value

  );
  toUnlockElement[0].style.backgroundPositionY = '-150px';
  toUnlockElement[0].innerHTML = '';
  updateUsersLevel(value);

};

function updateUsersLevel(number) {
  /* 
  updateUsersLevel function fetches level number to /updateLevel
  */
  const data = { 'level': number };

  fetch('/updateLevel', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data),
  })
    //reload page after 2 seconds
    .then(response => response.text())
    .then(html => {
      //* window.location.href = '/'; //* alternative reload page to the top
      setTimeout(() => {
        location.reload();
      }, 2000);
    })
}



function changeInputValue() {
  /* 
  changeInputValue function shows value of slider in /shop
  */
  const rangeSliderValue = document.getElementById("rangeSliderValue")
  const slider = document.getElementById("inputRange");
  rangeSliderValue.innerHTML = '🍅' + slider.value;
}
