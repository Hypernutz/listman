#!/usr/bin/env python3
import sys
import datetime
import os
import getpass
from pathlib import Path
def cute(cmd):
    os.system(cmd)
def rm(path):
    os.system(f"rm '{path}'")
def touch(path):
    os.system(f"touch '{path}'")
username = getpass.getuser()
listdir = f"/home/{username}/.listman"
base = Path.home() / ".listman"
(base / "absolute").mkdir(parents=True, exist_ok=True)
(base / "listlist.txt").touch(exist_ok=True)

args = sys.argv[1:len(sys.argv)]
try:
    x = args[0]
except:
    exit()
newlist = {}
with open(f"{listdir}/listlist.txt", "r+") as f:
    try:
        newlist = dict(eval(f.read()))
    except:
        f.write("{}")
    f.close()
def append(clist, textlist, editabsolute=True):
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second
    text = textlist
    toappend = ""
    style = newlist[clist]['liststyle']
    toappend = "\n"
    stylechar = newlist[clist]['borderchar']
    stylewidth = int(newlist[clist]['borderwidth'])
    prefix = newlist[clist]['prefix']
    left = (stylechar*stylewidth)
    space = (' '*(stylewidth-1))
    prefixspace = ' '*len(prefix['prefix'])
    leftp = ""
    rightp = ""
    topp = ""
    bottomp = ""
    match prefix['position']:
        case 'left':
            leftp = eval(prefix['prefix'])
        case 'right':
            rightp = eval(prefix['prefix'])
        case 'above':
            topp = eval(prefix['prefix'])
        case 'below':
            bottomp = eval(prefix['prefix'])
    toappend+=topp+"\n"
    for i in text:
        if i == "":
            continue
        i = i.strip()
        if style == "1":
            for k in range(0, 3):
                if k == 1:
                    dstring = (stylechar*(stylewidth*2+(stylewidth-1)*2+len(i)))[0:len(stylechar)*stylewidth*2 + len(i) + (stylewidth-1)*2]
                    dstring = dstring[len(left+space*2+i):len(dstring)]
                    toappend += f"{' '*len(leftp)}{left+space+(' '*len(i))+space+dstring}{' '*len(rightp)}\n"
                    toappend += f"{leftp}{left+space+i+space+dstring}{rightp}\n"
                    toappend += f"{' '*len(leftp)}{left+space+(' '*len(i))+space+dstring}{' '*len(rightp)}\n"     
                for f in range(0, stylewidth):
                    if k == 0 or k == 2:
                        toappend += ' '*len(leftp)+(stylechar*(stylewidth*2+(stylewidth-1)*2+len(i)))[0:len(stylechar)*stylewidth*2 + len(i) + (stylewidth-1)*2]+"\n"
            toappend+=bottomp+"\n"
            toappend += "\n\n"


        elif style == "2":
            toappend += f"{i}\n"
        if editabsolute:
            with open(f"{listdir}/absolute/{clist}.txt", "a") as f:
                f.write(i+";")
    with open(f"{listdir}/{clist}.txt", "a") as f:
        f.write(toappend)


# add list -----------------------------------------------------------------------------------------------------------------------------------
if args[0] == "add":
    listname = input("Enter list name: ")
    try:
        open(f"{listdir}/absolute/{listname}.txt", "x")
        open(f"{listdir}/{listname}.txt", "x")
    except:
        print("Error: List already exists.")
        f = input("Do you want to override the existing list? (y/n): ")
        if f == "n":
            exit()
        elif f == "" or f == "y":
            pass
        else:
            print("learn to type")
            exit()
    liststyle = input("Bordered list? (enter 1 for bordered, 2 for plain): ")
    if liststyle == "1":
        borderchar = input("Enter border character: ")
        borderthic = input("Enter border thickness (how many characters thick?): ")

    elif liststyle == "2":
        borderchar = "none"
        borderthic = "0"
    else:
        liststyle = "2"
        print("Selected plain style. Reason: user doesn't know how to type")
    print("Enter a prefix\nLeave blank for no prefix\nYou can use the variables:\ndate, time, day, month, year, hour, minute, second\ninside '{}' to use current time information in the prefix.")
    prefix = input("")
    prefpos = ""
    if prefix:
        prefpos = input("Enter prefix position (left, right, above, below): ")

    newlist[listname] = {
        'liststyle': liststyle, 
        'borderchar': borderchar, 
        'borderwidth': borderthic,
    }
    newlist[listname]['prefix'] = {
            'prefix': f"f\'{prefix}\'",
            'position': prefpos
        }
    
    with open(f"{listdir}/listlist.txt", "w") as f:
        f.write(f"{newlist}")
        f.close()

# show list -----------------------------------------------------------------------------------------------------------------------------------

elif args[0] == "list":
    with open(f"{listdir}/{args[1]}.txt", "r") as f:
        print(f.read())

# reset -----------------------------------------------------------------------------------------------------------------------------------

elif args[0] == "reset":
    print("WARNING: ALL YOUR LISTS AND LIST RECORDS WILL BE LOST")
    confirm = input("Proceed? (y/n): ")
    if confirm.casefold()=="y":
        with open(f"{listdir}/listlist.txt", "w") as f:
            f.write("{}")
        for key in newlist:
            name = key
            rm(f"{listdir}/{name}.txt")
            rm(f"{listdir}/absolute/{name}.txt")

    else:
        print("cancelled")
        exit()

# append -----------------------------------------------------------------------------------------------------------------------------------

elif args[0] == "append":
    clist = str(args[1])
    textlist = args[2:len(args)]
    text = ""
    toappend = ""
    for df in textlist:
        text += df+" "
    text = text.split(",,")
    append(clist=clist, textlist=text)

elif args[0] == "remove":
    clist = str(args[1])
    newlist.pop(clist)
    with open(f"{listdir}/listlist.txt", "w") as f:
        f.write(str(newlist))
    rm(f"{listdir}/{clist}.txt")
    rm(f"{listdir}/absolute/{clist}.txt")
elif args[0] == "update":

    if args[1] == "all":
        for clist in newlist:
            textlist = []
            with open(f"{listdir}/absolute/{clist}.txt", "r") as f:
                textlist = f.read().split(";")
                f.close()
            rm(f"{listdir}/{clist}.txt")
            rm(f"{listdir}/absolute/{clist}.txt")
            touch(f"{listdir}/{clist}.txt")
            touch(f"{listdir}/absolute/{clist}.txt")
            append(clist=clist, textlist=textlist)
    else:
        clist = str(args[1])
        textlist = []
        with open(f"{listdir}/absolute/{clist}.txt", "r") as f:
            textlist = f.read().split(";")
            f.close()
        rm(f"{listdir}/{clist}.txt")
        touch(f"{listdir}/{clist}.txt")
        append(clist=clist, textlist=textlist, editabsolute=False)
elif args[0] == "change":
    def setstyle():
        listname = input("Enter listname: ")
        style = input("Enter list style (1 for bordered, 2 for plain): ")
        newlist[listname]['liststyle'] = style
    def setchar():
        listname = input("Enter listname: ")
        char = input("Enter border character: ")
        newlist[listname]['borderchar'] = char
    def setwidth():
        listname = input("Enter listname: ")
        widthinchar = input("Enter borderwidth (number of characters thick): ")
        try:
            test = int(widthinchar)
            newlist[listname]['borderwidth'] = widthinchar
        except:
            print("Error: type properly bich")
    def setprefix():
        listname = input("Enter listname: ")
        prefix = input("Enter prefix: ")
        prefixpos = input("Enter prefix position (left, right, above, below): ")
        test = False
        for i in ['left', 'right', 'above', 'below']:
            if i in prefixpos:
                test = True
        if test:
            newlist[listname]['prefix'] = {'prefix': f"f\'{prefix}\'", 'position': prefixpos}
        else:
            print("Choose from the options gay")
    print("Lists -----------------------------------------------------------\n")
    for key in newlist:
        print(key)
    print("\n\ncommands -----------------------------------------------------------\n\n")
    print("setstyle()\n")
    print("setchar()\n")
    print("setwidth()\n")
    print("setprefix()\nThe datetime module is imported. You can add date or time to your prefix by just typing the variable inside {}. No need to make the prefix an fstring\nSome variables like date, time, day, month, year, hour, minute, second have been predefined for you to use.\nPlease use \\\\ for newline or tabspaces (do not use \\\\ in listman add)")
    print("\nCtrl+C to save, use listman update all to update all lists")
    while True:
        try:
            cmd = input("command: ")
            exec(cmd)
        except KeyboardInterrupt:
            with open(f"{listdir}/listlist.txt", "w") as f:
                f.write(str(newlist))
                f.close()
            print("\ndone")
            exit()
elif args[0] == "lists":
    st = ""
    st += ("\n"+"     Name     " + "Style     " + "BorderChar     " + "BorderWidth     "+"Prefix     \n\n")
    for key in newlist:
        st += (f"     {str(key)}{' '*(9-len(key))}{newlist[key]['liststyle']}{' '*9}{newlist[key]['borderchar']}{' '*(15-len(newlist[key]['borderchar']))}{newlist[key]['borderwidth']}{' '*(16-len(newlist[key]['borderwidth']))}{newlist[key]['prefix']}\n")
    print(st+"\n")

elif args[0] == "help":
    print("""
1. listman help - show this
2. listman add - add new list
3. listman list listname - show the specified list
4. listman reset - delete all lists and list settings
5. listman remove listname - remove the specified list
6. listman update listname/all - 'all' will update all lists after executing listman change, or a list can be specified
7. listman change - change lists settings: style, border, borderwidth, prefix
8. listman lists - show all lists and list settings
9. listman append listname newlistitem - add a new item to a list (separate different items using ',,')
""")