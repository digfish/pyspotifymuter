import subprocess
import sys
import time

WAITING_TIME = 2
muted = False


def exec_output(some_command):
    """executes and returns the output of some shell program"""
    output = subprocess.check_output(some_command, shell=True)
    return output


def spotify_playing():
    out = exec_output('tasklist /fi "imagename eq Spotify.exe" /fo csv /v ')
    lines = str(out,encoding='windows-1252').split('\r\n')
    line2 = lines[1]
    fields = line2.split(',')
    return fields[8].strip('"')


def mute_div(what):
    base_cmd = "nircmd muteappvolume spotify.exe"
    out = ''
    if what == 'yes':
        out = exec_output(base_cmd + ' 1')
    elif what == 'no':
        out = exec_output(base_cmd + ' 0')
    print (out)


def does_file_contains(filename, expr):
    f = open(filename, 'r')
    lines = []
    for line in f.readlines():
        lines.append(line.rstrip('\n'))
    f.close()
    return expr in lines


def do():
    global muted
    playing = (spotify_playing())
    print ("Playing " + playing)
    is_playing_ad = does_file_contains('blacklist.txt', playing)
    if is_playing_ad and (not muted):
        print ("Detected ad!")
        mute_div('yes')
        print ('MUTING!')
        muted = True
    elif not (is_playing_ad) and muted:
        mute_div('no')
        print ('UNMUTING!')
        muted = False


def main():
    global WAITING_TIME
    if (len(sys.argv) > 1):
        WAITING_TIME = int(sys.argv[1])

    print ("Waiting period is " + str(WAITING_TIME) + " seconds")

    while True:
        do()
        time.sleep(WAITING_TIME)


if __name__ == '__main__':
    main()
