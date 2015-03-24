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

"""Never lose the dice again!

The default is to print dice with `chr(183)` as the dots,
this can be changed by giving the first argument as a single character.
"""

def join(*faces):
    faces = [face.split("\n") for face in faces]

    lines = ['' for _ in faces[0]]
    for face in faces:
        for line in range(len(face)):
            lines[line] += face[line]

    return "\n".join(lines)

def str(number, dice_dots=chr(183)):
    """Returns the multi-line str relivant to number"""
    line = " | {0:^5} | "
    top = bottom = "  -------  "

    s = [top] + [line.format(x) for x in side(number)] + [bottom]

    return ("\n".join(s)).replace("x", dice_dots)

def side(number):
    """Returns the dots (x) relivant to number"""
    one = ["     ", "  x  ", "     "]
    two = ["x    ", "     ", "    x"]
    three = ["x    ", "  x  ", "    x"]
    four = ["x   x", "     ", "x   x"]
    five = ["x   x", "  x  ", "x   x"]
    six = ["x   x", "x   x", "x   x"]
    return [one, two, three, four, five, six][(number - 1)]

if __name__ == "__main__":
    raise RuntimeError("dice.py is a module")
