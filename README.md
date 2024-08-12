# Игра "Змейка".

### Автор

1. Николай Моденов  
   - Аккаунт GitHub: [NikolayModenov](https://github.com/NikolayModenov)

## Описание

Классическая игра "змейка".
Приложение реализовано на PyGame.
экран разделён на квадраты. Фон игрового поля серого цвета, на котором появляются "яблоко" красного и "змейка" зелёного цветов.
Змейка перемещается безостановочно, изменение направления перемещения производится нажатием стрелок на клавиатуре.
В игре есть возможность изменять сложность игры нажатием клавиши x или z, которая влияет на скорость перемешения змейки.
Цель игры - накормить змейку яблоками, для этого надо переместить змейку на ячейку с яблоком. После поедания яблока змейкой увеличивается счёт текущей игры, а змейка вырастает на одну клетку.
Если змейка укусит себя то игра начинается сначала из центра игрового поля в случайном направлении с длиной змейки в одну клетку.
Если игровой счёт был больше рекорда, то записывается новый рекорд.

### Запуск приложения

1. Форкните проект [the_snake](https://github.com/NikolayModenov/the_snake/) на свой аккаунт Git Hub и склонируйте на свой локальный компьютер. 

      ```git clone git@github.com:<ваше_имя_пользователя_на_GitHub>/the_snake.git ```

2. Создайте виртуальное окружение и подключитель к нему.

- ```python -m venv venv``` - создание окружения
- ```source venv/Scripts/activate``` - подключение к созданному окружению

3. Для запуска приложения введите команду:

      ```python the_snake.py```