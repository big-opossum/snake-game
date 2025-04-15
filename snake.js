const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const box = 20; // Размер клетки
const canvasSize = 400;
let snake;
let direction;
let food;
let score;
let gameInterval;

function initGame() {
    snake = [{ x: 9 * box, y: 9 * box }];
    direction = 'RIGHT';
    food = randomFood();
    score = 0;
    document.getElementById('score').textContent = 'Счёт: ' + score;
    clearInterval(gameInterval);
    gameInterval = setInterval(draw, 100);
}

function randomFood() {
    return {
        x: Math.floor(Math.random() * (canvasSize / box)) * box,
        y: Math.floor(Math.random() * (canvasSize / box)) * box
    };
}

document.addEventListener('keydown', directionHandler);
document.getElementById('restartBtn').onclick = initGame;

function directionHandler(e) {
    if (e.key === 'ArrowLeft' && direction !== 'RIGHT') direction = 'LEFT';
    else if (e.key === 'ArrowUp' && direction !== 'DOWN') direction = 'UP';
    else if (e.key === 'ArrowRight' && direction !== 'LEFT') direction = 'RIGHT';
    else if (e.key === 'ArrowDown' && direction !== 'UP') direction = 'DOWN';
}

function draw() {
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, canvasSize, canvasSize);

    // Рисуем змейку
    for (let i = 0; i < snake.length; i++) {
        ctx.fillStyle = i === 0 ? '#ff69b4' : '#ffb6d5'; // Розовая голова и светло-розовое тело
        ctx.fillRect(snake[i].x, snake[i].y, box, box);
    }

    // Рисуем еду
    ctx.fillStyle = '#f00';
    ctx.fillRect(food.x, food.y, box, box);

    // Движение змейки
    let head = { x: snake[0].x, y: snake[0].y };
    if (direction === 'LEFT') head.x -= box;
    if (direction === 'RIGHT') head.x += box;
    if (direction === 'UP') head.y -= box;
    if (direction === 'DOWN') head.y += box;

    // Проверка на столкновение с границами
    if (
        head.x < 0 || head.x >= canvasSize ||
        head.y < 0 || head.y >= canvasSize ||
        collision(head, snake)
    ) {
        clearInterval(gameInterval);
        ctx.fillStyle = '#fff';
        ctx.font = '30px Arial';
        ctx.fillText('Игра окончена!', 80, 200);
        return;
    }

    // Проверка на еду
    if (head.x === food.x && head.y === food.y) {
        score++;
        document.getElementById('score').textContent = 'Счёт: ' + score;
        food = randomFood();
    } else {
        snake.pop();
    }

    snake.unshift(head);
}

function collision(head, array) {
    for (let i = 0; i < array.length; i++) {
        if (head.x === array[i].x && head.y === array[i].y) return true;
    }
    return false;
}

initGame();
