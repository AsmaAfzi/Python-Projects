def PALINDROME(x):
    if x == x[::-1]:
        print(x, 'is a palindrome')
    else:
        print(x, 'is not a palindrome')

def CHAR(x):
    c = 0
    for i in x:
        c += 1
    print('No of characters in "', x, '" is:', c)

def WORD(x):
    a = x.split()
    print('No of words in "', x, '" is:', len(a))

def LCASE(x):
    l = 0
    for i in x:
        if i.isalpha() and i.islower():
            l += 1
    print('No of lower case characters in "', x, '" is:', l)

def UCASE(x):
    u = 0
    for i in x:
        if i.isalpha() and i.isupper():
            u += 1
    print('No of upper case characters in "', x, '" is:', u)

def DIGIT(x):
    d = 0
    for i in x:
        if i.isdigit():
            d += 1
    print('No of digits in "', x, '" is:', d)

def MENU(w):
    while True:
        o = int(input('''
Enter the corresponding number to select an option:
(1) To check if string is a palindrome
(2) Number of characters
(3) Number of words
(4) Number of lowercase characters
(5) Number of uppercase characters
(6) Number of digits
(7) Quit
:'''))
        
        if o == 1:
            PALINDROME(w)
        elif o == 2:
            CHAR(w)
        elif o == 3:
            WORD(w)
        elif o == 4:
            LCASE(w)
        elif o == 5:
            UCASE(w)
        elif o == 6:
            DIGIT(w)
        elif o == 7:
            print('Have a nice day!')
            break
        else:
            print('Invalid entry')
        
        input('Press enter to continue')

def main():
    c = 'y'
    while c == 'y':
        wrd = input('Enter a string\n: ')
        MENU(wrd)
        c = input('Do you wish to continue? (y/n)\n: ')
    print('Have a nice day!!')

main()
