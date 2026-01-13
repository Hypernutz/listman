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
def copy(path, dest_path):
    os.system(f"cp -r '{path}' '{dest_path}'")
def mkdir(path):
    os.system(f"mkdir -p '{path}'")
username = getpass.getuser()
listdir = f"/home/{username}/.listman"
base = Path.home() / ".listman"
(base / "absolute").mkdir(parents=True, exist_ok=True)
(base / "prefixes").mkdir(parents=True, exist_ok=True)
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
def append(clist, textlist, editabsolute=True, newlist=newlist, prefixfromfile=False):
    now = datetime.datetime.now()
    date = now.date()
    time = now.time()
    day = now.day
    month = now.month
    year = now.year
    hour = now.hour
    minute = now.minute
    second = now.second
    text = textlist
    toappend = ""
    style = newlist[clist]['liststyle']
    toappend = "\n"
    stylechar = newlist[clist]['borderchar']
    stylewidth = int(newlist[clist]['borderwidth'])
    prefix = newlist[clist]['prefix']
    left = (stylechar*stylewidth)
    space = (' '*(stylewidth-1))
    leftp = ""
    rightp = ""
    topp = ""
    bottomp = ""
    y = 0
    match prefix['position']:
        case 'left':
            leftp = eval(prefix['prefix'])
        case 'right':
            rightp = eval(prefix['prefix'])
        case 'above':
            topp = eval(prefix['prefix'])
        case 'below':
            bottomp = eval(prefix['prefix'])
    for i in text:
        if prefixfromfile:
            with open(f"{listdir}/prefixes/{clist}.txt", "r") as f:
                x = f.read()
            if y > len(x.split(";:;"))-1:
                exit()
            match prefix['position']:
                case 'left':
                    leftp = x.split(";:;")[y]
                case 'right':
                    rightp = x.split(";:;")[y]
                case 'above':
                    topp = x.split(";:;")[y]
                case 'below':
                    bottomp = x.split(";:;")[y]
            y+=1
        else:
            with open(f"{listdir}/prefixes/{clist}.txt", "a") as f:
                f.write(eval(prefix['prefix'])+";:;")
                f.close()
        if i == "":
            continue
        i = i.strip()
        toappend+=topp+"\n"
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

        elif style == "2":
            toappend += f"{leftp}{i}{rightp}\n"
        toappend+=bottomp+"\n"
        toappend += "\n\n"
        if editabsolute:
            with open(f"{listdir}/absolute/{clist}.txt", "a") as f:
                f.write(i+";")
    with open(f"{listdir}/{clist}.txt", "a") as f:
        f.write(toappend)


# add list -----------------------------------------------------------------------------------------------------------------------------------
if args[0] == "add":
    listname = input("Enter list name: ")
    if " " in listname:
        print("NOTE: the spaces in your listname will be replaced by '_'. Please use _ in place of the spaces whenever refering to the list in other commands.")
        listname.replace(' ', "_")
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
    try:
        preserve1 = args[2] == "-pp"
    except:
        preserve1 = False
    if not preserve1:
        print("WARNING: updating lists will reset specific prefixes (prefixes which contain specific date or time)\nUse listman update list_name -pp to keep prefixes unchanged")
        cont = input("Continue? (y/n): ")
        if cont != "y":
            print("cancelled")
            exit()
    if args[1] == "all":
        for clist in newlist:
            textlist = []
            with open(f"{listdir}/absolute/{clist}.txt", "r") as f:
                textlist = f.read().split(";")
                f.close()
            rm(f"{listdir}/{clist}.txt")
            touch(f"{listdir}/{clist}.txt")
            append(clist=clist, textlist=textlist, editabsolute=False, prefixfromfile=preserve1)
    else:
        clist = str(args[1])
        textlist2 = []
        with open(f"{listdir}/absolute/{clist}.txt", "r") as f:
            textlist2 = f.read().split(";")
            f.close()
        rm(f"{listdir}/{clist}.txt")
        touch(f"{listdir}/{clist}.txt")
        append(clist=clist, textlist=textlist2, editabsolute=False, prefixfromfile=preserve1)
        

        
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
        for i in ['left', 'right', 'above', 'below', '']:
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
elif args[0] == "export":
    mkdir(args[2]+"/absolute")
    mkdir(args[2]+"/prefixes")
    if args[1] == "all":
        for key in newlist:
            copy(path=f"{listdir}/{key}.txt", dest_path=args[2])
            copy(path=f"{listdir}/absolute/{key}.txt", dest_path=args[2]+"/absolute")
            copy(path=f"{listdir}/prefixes/{key}.txt", dest_path=args[2]+"/prefixes")
    else:
        mkdir(args[2]+"/absolute")
        mkdir(args[2]+"/prefixes")
        copy(path=f"{listdir}/{args[1]}.txt", dest_path=args[2])
        copy(path=f"{listdir}/absolute/{args[1]}.txt", dest_path=args[2]+"/absolute")
        copy(path=f"{listdir}/prefixes/{args[1]}.txt", dest_path=args[2]+"/prefixes")
elif args[0] == "help":
# GENERAL
    cmd_general = [
        "listman help ->",
        "listman add ->",
        "listman update list_name(s)/all ->",
    ]
    desc_general = [
        "show this",
        "add new list",
        "'all' will update all lists after executing listman change, or a list can be specified",
    ]
    # OUTPUT / PRESENT
    cmd_output_present = [
        "listman list list_name ->",
        "listman lists ->",
        "listman export list_name/all export_path ->",
        "listman exportprog list_name export_path ->",
    ]
    desc_output_present = [
        "show the specified list",
        "show all lists and list settings",
        "export a list",
        "export a list for use in programs of languages like python, java, c++",
    ]
    # INPUT / MODIFY
    cmd_input_modify = [
        "listman settings ->",
        "listman change ->",
        "listman append list_name new_list_item(s) ->",
        "listman rename old_list_name new_list_name ->",
        "listman edit list_name list_item_index(starting with 0) ->",
    ]
    desc_input_modify = [
        "adjust listman settings like autobackup, etc.",
        "change lists settings: style, border, borderwidth, prefix",
        "add a new item(s) to a list(s)",
        "rename a list",
        "edit a list item",
    ]
    # REMOVAL
    cmd_removal = [
        "listman rm list_name exactlistitem ->",
        "listman clear listname(s) ->",
        "listman remove list_name(s) ->",
        "listman reset ->",
    ]
    desc_removal = [
        "remove the specified item from specified list",
        "clear the specified lists",
        "remove the specified list",
        "delete all lists and list settings",
    ]
    CATEGORIES = ['GENERAL', 'OUTPUT/PRESENT', 'INPUT/MODIFY', 'REMOVAL']
    for c in CATEGORIES:
        k = c.lower().replace("/", "_")
        print(f"\n\n{c}\n\n")
        for i in range(0, len(eval(f"cmd_{k}"))):
            print(eval(f"cmd_{k}[i]") + (' '*(70-len(eval(f"cmd_{k}[i]")))) + eval(f"desc_{k}[i]")+"\n")