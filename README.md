RiskBattler
===========

Throw ncurses dice and speed up your Risk game!

---

Files
-----
 - dice.py: Takes a number in [1,6] and creates an ascii art die. Also has the ability to join two ascii art dice in the same line.
 - risk.py: Main ncurses program.

Using this program
------------------
 1. Set up your Risk game like usual.
 2. Put away the dice.
 3. Start this program (python 2.7 or 3.x).
 4. When a player attacks, enter the troops they are using as offensive count.
 5. Start the battle with "space" to automatically finish the battle OR any other key to battle by one roll at time.

Known Issues
------------
 - In rare cases the offensive side may fall to zero, in this case just assume it's actually one.
 - You may only quit the program at the start of a battle with 'q'. This is a flaw in the way `get_int` function works.
