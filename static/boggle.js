const submitButton = document.querySelector('.submit')
const input = document.querySelector('input')
const form = document.querySelector('form')
const results = document.querySelector('#results')
const scoreDisp = document.querySelector('#score')

let score = 0
let gameActive = true;


const guess = async function makeGuess(event) {
    /** 
     * take the value store in the input and sen it as post request to localhost
     * update the score based on the status code received back ('ok, not-a-word, not-on-board')
     */
    event.preventDefault()
    let guess = input.value
    let response = await axios.post('http://127.0.0.1:5000/play', { 'guess': guess })

    results.className = 'showing'
    if (response.data.status == 'ok') {
        score += response.data.guess.length;
    }
    results.innerText = response.data.status
    scoreDisp.innerText = `Score: ${score}`
    input.value = ''
}

async function game_over() {
    /**
     * when the timer runs out, remove event listener for form submissions, create restart button, display high sore and plays
     */
    // display game over and stop submissions
    timer.innerText = "Game Over!";
    timer.style.color = 'red';
    timer.className = 'game_over'
    submitButton.removeEventListener('click', guess);
    clearInterval(time);

    // take the current score and send it to back end
    let game_over_response = await axios.post('http://127.0.0.1:5000/update', { 'score': score });
    console.log(game_over_response);
    const go_msg = document.createElement('span');
    go_msg.innerText = `High Score: ${game_over_response.data.highScore} | Plays: ${game_over_response.data.numPlays}`;
    document.body.prepend(go_msg);

    // create restart link
    const restartLink = document.createElement('a')
    restartLink.innerText = 'Restart'
    restartLink.className = 'restart'
    restartLink.setAttribute('href','http://127.0.0.1:5000/')
    scoreDisp.appendChild(restartLink)

}

// handle submit click
submitButton.addEventListener('click', guess)
form.addEventListener('submit', e => e.preventDefault())

let timeLeft = 30;
const timer = document.createElement('span')

document.body.prepend(timer)


// timer
const time = setInterval(function () {
    timeLeft--;
    timer.innerText = `Time Remaining: ${timeLeft}`
    if (timeLeft <= 0) {
        game_over();
    }
}, 1000)

