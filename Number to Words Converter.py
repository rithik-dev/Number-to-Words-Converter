from math import floor
from tkinter import *
import pyttsx3

names = {
    "0": "",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
    "10": "ten",
    "11": "eleven",
    "12": "twelve",
    "13": "thirteen",
    "14": "fourteen",
    "15": "fifteen",
    "16": "sixteen",
    "17": "seventeen",
    "18": "eighteen",
    "19": "nineteen",
    "20": "twenty",
    "30": "thirty",
    "40": "forty",
    "50": "fifty",
    "60": "sixty",
    "70": "seventy",
    "80": "eighty",
    "90": "ninety"
}

unit_names = (
    "hundred",
    "thousand",
    "lakhs",
    "crores",
    "arab",
    "kharab",
    "neel",
    "padma"
)

MAX_LENGTH = 1+len(unit_names)*2


def insertInString(string, element, index):
    return string[:index] + element + string[index:]


def getAnswer(num, string, is_negative, is_decimal=0):
    if is_decimal == 0:
        num = addComma(num)

    if is_negative:
        num = "-"+num
        string = "minus "+string

    return num,string.upper()


def addComma(number):
    number = str(number)
    length = len(number)
    if length > 3:
        comma_places = [3]
        for x in range(0, floor(length/2)-2):
            comma_places.append(comma_places[x]+2+1)
            length += 1

        number = number[::-1]

        for comma in range(0, len(comma_places)):
            number = insertInString(number, ',', comma_places[comma])

        number = number[::-1]

    return number


def convertToLowestMultiple(num, multiple):
    return num//multiple


def calculate(n, string, power):

    if len(str(n)) == 3:
        msg = convertToLowestMultiple(n, 10**power)
        ans = f"{names[str(msg)]} {string} "
        msg = convertToEnglish(str(n-msg*(10**power)))
        ans += msg

    if n >= 1000:
        if len(str(n)) % 2 == 0:
            msg = convertToLowestMultiple(n, 10**power)
            ans = f"{names[str(msg)]} {string} "
            msg = convertToEnglish(str(n-msg*(10**power)))
            ans += msg
        else:
            msg = convertToLowestMultiple(n, 10**power)
            ans = f"{convertToEnglish(str(msg))} {string} "
            msg = convertToEnglish(str(n-msg*(10**power)))
            ans += msg

    return ans


def convertToEnglish(num):
    length = len(num)
    msg, ans = "", ""
    n = int(num)

    if length == 1:
        ans = names[num]
    elif length == 2:
        if n >= 10 and n <= 20:
            ans = names[num]
        else:
            msg = convertToLowestMultiple(n, 10)*10
            ans = f"{names[str(msg)]} {names[str(n-msg)]}"
    elif length == 3:
        ans = calculate(n, unit_names[0], 2)
    elif length <= MAX_LENGTH:
        if length % 2 == 0:
            ans = calculate(n, unit_names[length//2-1], length-1)
        else:
            ans = calculate(n, unit_names[length//2-1], length-2)

    else:
        return "-1"

    return ans


def calculateAfterDecimal(second_half):
    ans = ""
    for x in range(0, len(second_half)):
        if second_half[x] == "0":
            ans += "zero "
        else:
            ans += names[second_half[x]]+" "
    return ans


def verifyNumber(number):
    counter = 0
    for x in range(0, len(number)):
        if number[x] == ".":
            counter += 1
            if(counter > 1):
                return False
    counter = 0
    for x in range(0, len(number)):
        if number[x] == "-":
            counter += 1
            if(counter > 1):
                return False

    return True


def calculateDecimal(number, is_negative):
    first_half = number.split(".")[0]
    second_half = number.split(".")[1]

    if is_negative:
        first_half = str(-1*int(first_half))

    if int(first_half) == 0:
        first_half = str(int(first_half))
        ans1 = "zero"
    else:
        first_half = str(int(first_half))
        ans1 = convertToEnglish(first_half)

    second_half = second_half[::-1]
    second_half = str(int(second_half))
    second_half = second_half[::-1]

    ans2 = calculateAfterDecimal(second_half)

    if ans1 == "-1":
        ANSWER=('ERROR',f"\nSorry , {len(number)} digits are not supported at the moment !")
    else:
        ANSWER =  getAnswer(first_half+"."+second_half, ans1 +
                " POINT "+ans2, is_negative, 1)

    return ANSWER


def MAIN(number):
    is_decimal = False
    if number.find(".") > 0:
        is_decimal = True
    if verifyNumber(number):
        if number[0] == "-":
            is_negative = 1
            if not is_decimal:
                number = str(int(number.replace("-", "")))
        else:
            is_negative = 0

        if is_decimal:    # decimal input
            if int(number.split(".")[0]) == 0 and int(number.split(".")[1]) == 0:
                ANSWER =  getAnswer("0.0", "zero point zero", is_negative, 1)
            else:
                ANSWER = calculateDecimal(number, is_negative)
        else:                       # int input
            number = str(int(number))
            if int(number) == 0:
                ANSWER =  getAnswer(number, "zero", is_negative)
            else:
                ans = convertToEnglish(number)
                if not ans == "-1":
                    ANSWER =  getAnswer(number, ans, is_negative)
    else:
        ANSWER=('ERROR',"\nNumber Input is not valid !")

    return ANSWER

def gui():
    number=e.get()

    if number == "" or any(c.isalpha() for c in number):
        ANSWER=('ERROR',"\nNumber Input is not valid !")
    elif len(number)>MAX_LENGTH and number.count(".")==0:
        ANSWER=('ERROR',f"\nSorry , {len(number)} digits are not supported at the moment !")
    else:
        ANSWER = MAIN(number)

    num_text.set(ANSWER[0])
    ans_text.set(ANSWER[1])

    win.update()

    if TTS_ENABLED.get():
        textToSpeech(ANSWER[1])
    

if __name__ == "__main__":
    # initialisation of text to speech engine
    engine = pyttsx3.init()

    def textToSpeech(message):
        engine.say(message)
        engine.runAndWait()

    win = Tk()
    win.geometry('400x200')
    win.resizable(False,False)
    win.title("Number to Words Converter")

    Label(win, text='ENTER NUMBER BELOW').pack(side=TOP)

    global e
    e = Entry(win, justify=CENTER)
    e.pack(side=TOP,fill=X)

    global TTS_ENABLED
    TTS_ENABLED = IntVar()
    Checkbutton(win, text='Text to Speech',variable=TTS_ENABLED).pack(side=TOP)

    Button(win,text='CONVERT',command=gui).pack(side=TOP)

    global num_text
    num_text=StringVar()
    global ans_text
    ans_text=StringVar()

    num_text.set('')
    ans_text.set('')

    Label(win,textvariable=num_text,font='Helvetica 18 bold',justify=CENTER).pack()
    Label(win,textvariable=ans_text,wraplength=390,justify=CENTER).pack()

    win.mainloop()
