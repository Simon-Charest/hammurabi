#!/usr/bin/python
# coding=utf-8

__author__ = 'Simon Charest'
__copyright__ = 'Copyright 2019, SLCIT inc.'
__credits__ = ['Doug Dyment', 'David H. Ahl']
__email__ = 'simoncharest@gmail.com'
__license__ = 'GPL'
__maintainer__ = 'Simon Charest'
__project__ = 'Hammurabi'
__status__ = 'Developement'
__version__ = '1.0.0'

import math
from os import system
from random import randint
from random import uniform


def get_plant_rate():
    return randint(1, 8)


def get_trade_rate():
    return randint(17, 26)


year = 1792
lastYear = 1750
peopleInitial = 100
foodInitial = 2800
landInitial = 1000
people = peopleInitial
peopleStarved = 0
food = foodInitial
land = landInitial
plantRate = get_plant_rate()
tradeRate = get_trade_rate()
peopleDelta = -1 * people
foodDelta = 0
landDelta = 0
score = 0


def main():
    run_menu()


def run_menu():
    global year
    global people
    global peopleStarved
    global food
    global land
    global plantRate
    global tradeRate
    global peopleDelta
    global foodDelta
    global landDelta

    _ = system('clear')

    print('╔═════════════════╗')
    print('║    Hammurabi    ║')
    print('╚═════════════════╝')
    print('Year: %d BC' % year)
    print('People: %dK (%dK)' % (people, peopleDelta))
    print('People starved: %dK' % peopleStarved)
    print('Food: %dK (%dK)' % (food, foodDelta))
    print('Land: %dK (%dK)' % (land, landDelta))
    print('Plant rate: %d' % plantRate)
    print('Trade rate: %d' % tradeRate)
    print('┌────────────────┐')
    print('│ b: Buy land    │')
    print('│ s: Sell land   │')
    print('│ f: Feed people │')
    print('│ p: Plant food  │')
    print('│ e: End turn    │')
    print('│ q: Quit game   │')
    print('└────────────────┘')
    choice = input('Hammurabi, King of Babylon, I beg to ask for your orders: ')

    if choice == 'b':
        response = eval(input('How much K land shall you buy (max: %d)? ' % math.floor((food + foodDelta) / tradeRate)))
        if response >= 0 and response * tradeRate <= food + foodDelta:
            foodDelta -= response * tradeRate
            landDelta += response
        else:
            print('Invalid amount.')

    elif choice == 's':
        response = eval(input('How much K land shall you sell (max: %d)? ' % land + landDelta))
        if 0 <= response <= land + landDelta:
            foodDelta += response * tradeRate
            landDelta -= response
        else:
            print('Invalid amount.')

    elif choice == 'f':
        print('Each 1K people need to be fed 20K foods.')
        response = eval(input('How much K food shall you feed the people (max: %d)? ' % (food + foodDelta)))

        if 0 <= response <= food + foodDelta:
            peopleDelta += math.floor(response / 20)
            foodDelta -= response
        else:
            print('Invalid amount.')

    elif choice == 'p':
        print('Each 1K food requires 1K land and 0.1K people.')
        response = eval(input('How much food shall you plant (max: %d)? ' % min(people * 10,
                                                                                food + foodDelta, land + landDelta)))
        if 0 <= response <= people * 10 and response <= food + foodDelta and response <= land + landDelta:
            foodDelta -= response
            foodDelta += response * plantRate
        else:
            print('Invalid amount.')

    elif choice == 'e':
        year -= 4
        people += peopleDelta
        food += foodDelta
        land += landDelta
        plantRate = get_plant_rate()
        tradeRate = get_trade_rate()

        if peopleDelta < 0:
            peopleStarved += abs(peopleDelta)

        peopleDelta = -1 * people
        foodDelta = 0
        landDelta = 0

        get_plague_chance()
        get_rat_chance()

        if people / peopleInitial < 0.5 or year <= lastYear:
            end_game()

    elif choice == 'q':
        print('You have resigned from your position as King of Babylon.')
        end_game()

    else:
        print('Invalid choice.')

    run_menu()


def get_plague_chance():
    global people

    if randint(1, 100) <= 15:
        print('Alas! A horrible plague has struck and killed half of your population!')
        people = math.ceil(people / 2)


def get_rat_chance():
    global food

    if randint(1, 100) <= 40:
        print('Alas! A rat infestation ate some of your food supply!')
        food *= uniform(0.7, 0.9)


def end_game():
    global score

    _ = system('clear')

    print('┌──────────────────┐')
    print('│ End Game Summary │')
    print('└──────────────────┘')

    if people / peopleInitial < 0.5:
        print('More than half of your population was starved to death.')
        print('Following a revolt, you have been found, arrested and publicly executed in the city center.')

    elif year <= lastYear:
        # People
        if people / peopleInitial >= 2:
            print('Congratulations! Your population has more than doubled during your reign!')
            score += 25

        elif people / peopleInitial >= 1.5:
            print('Good job! Your population has increased steadily during your reign.')
            score += 20

        elif people / peopleInitial >= 1:
            print('Your population stayed constant during your reign.')
            score += 15

        else:
            print('Unfortunately, your population decreased during your reign.')
            score += 0

        # Starved people
        if peopleStarved / peopleInitial == 0:
            print('Congratulations! Nobody has died from starvation during your reign!')
            score += 25

        elif peopleStarved / peopleInitial >= 0.3:
            print('Good job! Very few people have died from starvation during your reign.')
            score += 20

        elif peopleStarved / peopleInitial >= 0.7:
            print('Some of your people have died from starvation during your reign.')
            score += 15

        else:
            print('Unfortunately, a great amount of people have died of starvation during your reign.')
            score += 0

        # Food
        if food / foodInitial >= 6.5:
            print('Congratulations! Your food has increased significantly during your reign!')
            score += 25

        elif food / foodInitial >= 3.5:
            print('Good job! Your food has increased steadily during your reign.')
            score += 20

        elif food / foodInitial >= 1:
            print('Your food stayed constant during your reign.')
            score += 15

        else:
            print('Unfortunately, your food decreased during your reign.')
            score += 0

        # Land
        if land / landInitial >= 1.5:
            print('Congratulations! You have expanded your land significantly during your reign!')
            score += 25

        elif land / landInitial >= 1:
            print('Good job! You have expanded your land steadily during your reign.')
            score += 20

        elif land / landInitial >= 0.5:
            print('You have slightly decreased your land during your reign.')
            score += 15

        else:
            print('Unfortunately, you have dramatically decreased you land during your reign.')
            score += 0

        # Score
        if score == 100:
            print('You have achieved a perfect score! Your name will forever be remembered throughout history!')

        elif score >= 80:
            print('You have reached an excellent score! \
                People write poetry and sign songs to praise your great leadership.')

        elif score >= 60:
            print('You have an okay score. You should have taken better decisions for your people.')

        else:
            print('Your leadership was despotic. Your people hate you. You were forced to run and hide into exile.')

    print('Year: %d BC' % year)
    print('People: %dK' % people)
    print('People starved: %dK' % peopleStarved)
    print('Food: %dK' % food)
    print('Land: %dK' % land)
    print('Score: %d%%' % score)
    exit(0)


main()
