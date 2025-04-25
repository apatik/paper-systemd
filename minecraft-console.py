#!/usr/bin/python3
import curses
import subprocess
import threading
import sys
import shlex

instance = " ".join(map(shlex.quote, sys.argv[1:]))
systemd_instance=f'minecraft@{instance}'

def run_journalctl(win):
    process = subprocess.Popen(['journalctl', '-u', systemd_instance, '--follow'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        win.addstr(line.decode())
        win.refresh()

def input_commands(win):
    with open(f'/run/minecraft-{instance}.stdin', 'a') as f:
        while True:
            win.clear()
            win.addstr("Enter  command (Ctrl-C to exit): ")
            curses.echo()
            win.move(1, 0)
            commandRaw = win.getstr()
            if (len(commandRaw) != 0 and commandRaw[0] == 3):
                # Input was only a Ctrl+C
                break
            else: 
                command=commandRaw.decode()
                f.write(command + "\n")
                f.flush()
                curses.noecho()
                win.clear()

def main(stdscr):
    try:
        curses.curs_set(1)
        stdscr.clear()
        
        height, width = stdscr.getmaxyx()
        journal_height = int(height * 0.9)
        input_height = height - journal_height

        journal_win = stdscr.subwin(journal_height, width, 0, 0)
        journal_win.scrollok(True)
        input_win = stdscr.subwin(input_height, width, journal_height, 0)

        thread = threading.Thread(target=run_journalctl, args=(journal_win,))
        thread.daemon = True
        thread.start()

        input_commands(input_win)
        
    except KeyboardInterrupt:
        stdscr.clear()
        stdscr.refresh()
    finally:
        curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
