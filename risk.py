#!/usr/bin/env python3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

"""Speeds up the battle part of risk

By default it will roll until a winner is found
You have the option to go by one attack at a time so
you can stop the battle before you lose your advantage
"""

__all__ = ['main', 'get_int', 'Army', 'Battle']
__author__ = "Cody A. Taylor ( codemister99@yahoo.com )"
__version__ = "2.0 Alpha"

import curses
import dice
from random import randint

class Army:
    """An army of troops

    Keeps track of the number of troops you have
    As well as the roll for each individual attack
    """
    def __init__(self, troops):
        """Initializes the army with the given number of troops

        Sets roll to Zero to indicate no attack has occured
        """
        self.__start = troops
        self.__troops = troops
        self.__roll = []

    def __repr__(self):
        return "{0!r} troops".format(self.__troops)

    def __str__(self):
        return "{} troops; {} lost".format(self.__troops, self.lost())

    def __eq__(self, other):
        """Compares number of troops"""
        return self.__troops == other.__troops

    def __ne__(self, other):
        """Compares number of troops"""
        return self.__troops != other.__troops

    def __lt__(self, other):
        """Compares last roll"""
        return self.__roll < other.__roll

    def __le__(self, other):
        """Compares last roll"""
        return self.__roll <= other.__roll

    def __gt__(self, other):
        """Compares last roll"""
        return self.__roll > other.__roll

    def __ge__(self, other):
        """Compares last roll"""
        return self.__roll >= other.__roll

    def lose(self, troops=1):
        """Lose the given number of troops

        By default One troop is lost
        Returns self for conveince
        """
        self.__troops -= troops
        return self

    def roll(self, number=1):
        """Set the roll to a new random number [1, 6]

        Returns a list of sorted random numbers
        """
        self.__roll = []

        if number > self.__troops:
            number = self.__troops

        for roll in range(number):
            self.__roll.append(randint(1, 6))

        self.__roll.sort()
        self.__roll.reverse()

        return self.__roll

    def lost(self):
        """The number of troops lost since start of battle"""
        return self.__start - self.__troops

    def can_attack(self):
        """True when this army can still attack"""
        return self.__troops > 1

    def can_defend(self):
        """True when this army can still defend"""
        return self.__troops > 0

class Battle:
    """A Battle between two Armies"""
    def __init__(self, offense, defense):
        self.__offense = offense
        self.__defense = defense

    def __repr__(self):
        return "Offense: {0!r}    \nDefense: {1!r}    ".format(self.__offense, self.__defense)

    def __str__(self):
        return "Offense: {0}    \nDefense: {1}    ".format(self.__offense, self.__defense)

    def action(self):
        """True if the Offense can still attack and the defense can still defend"""
        return self.__offense.can_attack() and self.__defense.can_defend()

    def attack(self):
        """Roll for both armies, lose troops accordingly

        Returns (offense_roll, defense_roll, str_result)
        """
        o_roll = self.__offense.roll(3)
        d_roll = self.__defense.roll(2)
        result = ""

        assert "No die for offense", len(o_roll) == 0
        assert "No die for defense", len(d_roll) == 0

        if o_roll[0] > d_roll[0]:
            self.__defense.lose()
            result += "Won "
        else:
            self.__offense.lose()
            result += "Lost "

        if len(o_roll) > 1 and len(d_roll) > 1:
            if o_roll[1] > d_roll[1]:
                self.__defense.lose()
                result += "and Won"
            else:
                self.__offense.lose()
                result += "and Lost"

        return o_roll, d_roll, result

def get_int(scr, x, msg):
    """Basic ncurses get_int

    clears away any text it writes before returning
    allow the use of the entire line (x)
    so that the user has plenty of room for input
    """
    curses.echo()
    curses.curs_set(1)
    scr.addstr(x, 0, "{}: ".format(msg))
    scr.refresh()

    i = ""
    while type(i) != int:
        i = scr.getstr()
        try:
            i = int(i)
        except ValueError:
            scr.addstr(x, len(msg) + 2, " " * len(i))
            scr.move(x, len(msg) + 2)

    scr.addstr(x, 0, " " * ( len(msg) + 2 + len(str(i)) ) )
    curses.noecho()
    curses.curs_set(0)
    return i

def main(stdscr):
    curses.curs_set(0)

    stdscr.addstr(0, 20, "Welcome to the Risk Battler!")
    stdscr.addstr(4,  0, "  Offense    Defense")
    stdscr.addstr(6,  0, dice.join(dice.str(1), dice.str(1)))
    stdscr.addstr(12, 0, dice.join(dice.str(1), dice.str(1)))
    stdscr.addstr(18, 0, dice.str(1))

    ch = ord('1')
    while ch != ord('q'):
        offense = get_int(stdscr, 2, "Number of offensive troops")
        defense = get_int(stdscr, 2, "Number of defensive troops")

        stdscr.addstr(2, 0, "Hit ' ' to automatically finish battles, 'q' to quit, any other for manual play")

        battle = Battle(Army(offense), Army(defense))
        stdscr.addstr(24, 0, str(battle))

        stdscr.refresh()
        ch = stdscr.getch()

        auto = True if ch == ord(' ') else False

        if auto == False:
            stdscr.addstr(2, 0, "Hit ' ' to continue battle, 'q' to quit, any other to stop                     ")
        else:
            stdscr.addstr(2, 0, "                                                                               ")

        while battle.action() and ch != ord('q'):
            stdscr.refresh()

            if auto == False:
                ch = stdscr.getch()
                if ch != ord(' '):
                    break
            else:
                curses.napms(600)

            o_roll, d_roll, result = battle.attack()

            stdscr.addstr(6, 0, dice.join(dice.str(o_roll[0]), dice.str(d_roll[0])))

            if len(o_roll) > 1 and len(d_roll) > 1:
                stdscr.addstr(12, 0, dice.join(dice.str(o_roll[1]), dice.str(d_roll[1])))
            elif len(o_roll) > 1:
                stdscr.addstr(12, 0, "{:30}\n".format(" ") * 5)
                stdscr.addstr(12, 0, dice.str(o_roll[1]))
            else:
                stdscr.addstr(12, 0, "{:30}\n".format(" ") * 5)

            if len(o_roll) > 2:
                stdscr.addstr(18, 0, dice.str(o_roll[2]))
            else:
                stdscr.addstr(18, 0, "{:30}\n".format(" ") * 5)

            stdscr.addstr(24, 0, str(battle))
            stdscr.addstr(27, 0, "Offense roll {}          ".format(result))

        if auto == False:
            stdscr.addstr(2, 0, "                                                          ")

        stdscr.refresh() # must refresh one last time to show final result

    return 0

if __name__ == "__main__":
    curses.wrapper(main)
