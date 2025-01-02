import mysql.connector as m

# Establishing connection to the database
con = m.connect(
    host='localhost',
    user='root',
    passwd='adis',
    db='Project'
)
c = con.cursor()

# Creating the Hotel table
sql = """
CREATE TABLE IF NOT EXISTS Hotel (
    Room_no INT(3) PRIMARY KEY,
    First_Name VARCHAR(25),
    Last_Name VARCHAR(25),
    Phone_no VARCHAR(10),
    Room_type VARCHAR(20),
    Date_of_checkin DATE,
    Date_of_checkout DATE
)
"""
c.execute(sql)
con.commit()

# Creating the GAMING table
GT = """
CREATE TABLE IF NOT EXISTS GAMING (
    CID INT(3),
    GAMES VARCHAR(30),
    HOURS VARCHAR(30),
    GAMING_BILL INT,
    FOREIGN KEY (CID) REFERENCES Hotel(Room_no)
)
"""
c.execute(GT)
con.commit()

# Creating the RESTAURANT table
RT = """
CREATE TABLE IF NOT EXISTS RESTAURANT (
    RID INT(3),
    First_name VARCHAR(30),
    RESTAURANT_BILL INT,
    FOREIGN KEY (RID) REFERENCES Hotel(Room_no)
)
"""
c.execute(RT)
con.commit()

# Creating the TOTAL table
TOTAL = """
CREATE TABLE IF NOT EXISTS TOTAL (
    CID INT(3),
    First_name VARCHAR(30),
    ROOMRENT INT,
    RESTAURANT_BILL INT,
    GAMING_BILL INT,
    TOTAL_AMOUNT INT
)
"""
c.execute(TOTAL)
con.commit()

def Checkin():
    choice = 'y'
    while choice == 'y':
        print('----------------------------------------------------------------------')
        nA = int(input('No of Adults: '))
        nC = int(input('No of kids: '))
        print('''
        *----------------------------------------------------------*
        | Please enter the corresponding number to select a room   |
        |                                                          |
        | (1) Standard Rs. 150/night                               |
        | (2) Deluxe Rs. 350/night                                 |
        | (3) Family (with connected rooms) Rs. 200/night          |
        *----------------------------------------------------------*
        ''')

        rt = int(input('Room type: '))
        Rt = room_type(rt)
        nR = int(input('No of rooms: '))
        doci = input('Date of Check In (YYYY/MM/DD): ')
        doco = input('Date of Checkout (YYYY/MM/DD): ')
        fN = input('Enter First Name: ')
        lN = input('Enter your Last Name: ')
        ph = input('Enter your phone no: ')

        print('----------------------------------------------------------------------')
        print('')
        print('----------------------------------------------------------------------')
        print('''Do you wish to proceed?''')
        print('----------------------------------------------------------------------')
        print('First name:', fN)
        print('Last name:', lN)
        print('Phone no:', ph)
        print('No of Adults:', nA)
        print('No of kids:', nC)
        print('No of rooms:', nR)
        print('Room Type:', Rt)
        print('Date of Check In:', doci)
        print('Date of Checkout:', doco)
        print('----------------------------------------------------------------------')
        ch = input('Enter yes or no: ')
        print('----------------------------------------------------------------------')

        if ch == 'yes':
            Insert(nR, fN, lN, ph, Rt, doci, doco)
            choice = 'n'
        elif ch == 'no':
            choice = 'n'
        else:
            print('Invalid')

def room_assg(x, y):
    # roomtype Rt Deluxe Family y
    # nR no of rooms x
    a = []
    R = []
    A = []
    s = "SELECT * FROM Hotel"
    c.execute(s)
    d = c.fetchall()

    if d != []:
        for j in d:
            a.append(j[0])

    if y == 'Standard':
        for i in a:
            if 101 <= i <= 230:
                A.append(i)

    elif y == 'Deluxe':
        for i in a:
            if 501 <= i <= 530:
                A.append(i)

    elif y == 'Family':
        for i in a:
            if 301 <= i <= 430:
                A.append(i)

    else:
        pass

    if A == []:
        if y == 'Standard':
            for k in range(0, x):
                R.append(101 + k)

        elif y == 'Deluxe':
            for k in range(0, x):
                R.append(501 + k)

        else:
            for k in range(0, x):
                R.append(301 + k)

        return R

    elif A[-1] in {230, 430, 530}:
        print('Sorry, no rooms available')

    else:
        for j in range(0, x):
            R.append(A[-1] + j + 1)
        return R


def room_type(x):
    t = ''

    if x == 1:
        t = 'Standard'
    elif x == 2:
        t = 'Deluxe'
    elif x == 3:
        t = 'Family'
    else:
        print('Invalid Entry')

    return t


def Insert(x, y, z, a, b, d, e):
    rm = room_assg(x, b)
    for app in rm:
        s = "INSERT INTO Hotel VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s')" % (app, y, z, a, b, d, e)
        c.execute(s)
        con.commit()

    print('----------------------------------------------------------------------')
    print('Room no:', rm)
    print('Enjoy your Stay! :)')
    print('----------------------------------------------------------------------')

def Checkout():
    ch = 'yes'
    while ch == 'yes':
        print('----------------------------------------------------------------------')
        n1 = input('Enter your first name: ')
        n2 = input('Enter your last name: ')
        print('----------------------------------------------------------------------')

        s = "SELECT COUNT(*) FROM Hotel WHERE First_Name='%s' AND Last_Name='%s'" % (n1, n2)
        c.execute(s)
        j = c.fetchall()

        if j != [(0,)]:
            pr = int(j[0][0])  # Number of rooms
            sq = """SELECT Room_type, Date_of_checkout, 
                     Date_of_checkout - Date_of_checkin, CURDATE() 
                     FROM Hotel WHERE First_Name='%s' AND Last_Name='%s'""" % (n1, n2)
            c.execute(sq)
            d = c.fetchall()

            doc = d[0][1]  # Date of checkout
            R_T = d[0][0]  # Room type
            nd = d[0][2]   # Number of days
            cur = d[0][3]  # Current date

            if doc == cur:
                P = Payment(pr, R_T, nd, n1, n2)  # Calculate payment
                ch = Bill(P, n1, n2)  # Generate bill

            elif doc < cur:
                P = Payment(pr, R_T, nd, n1, n2) + 250
                print('OVERSTAY FINE: 250')
                ch = Bill(P, n1, n2)

            else:
                print('----------------------------------------------------------------------')
                ch = input('Are you sure you want to check out? ')
                print('----------------------------------------------------------------------')

                sqe = "SELECT (SELECT CURDATE()) - Date_of_checkin FROM Hotel"
                c.execute(sqe)
                d = c.fetchall()
                nde = d[0][0]  # Number of days extended

                if ch == 'yes':
                    P = Payment(pr, R_T, nde, n1, n2)  # Calculate payment
                    ch = Bill(P, n1, n2)
                else:
                    print('----------------------------------------------------------------------')
                    print('No room assigned under this name')
                    print('----------------------------------------------------------------------')
                    ch = 'n'

def Payment(x, y, z, a, b):
    Pay = 0
    if y == 'Standard':
        Pay += 150 * x * z
    elif y == 'Deluxe':
        Pay += 350 * x * z
    elif y == 'Family':
        Pay += 200 * x * z
    else:
        pass

    if Pay < 0:
        return 0
    else:
        print('----------------------------------------------------------------------')
        print("""
**** HOTEL LAVIES ****
**** CUSTOMER BILLING ****
""")
        print('CUSTOMER NAME: ', a, b)
        print('ROOM RENT: ', Pay)
        print('RESTAURANT BILLING: ', Cost_Rest())
        print('GAMING BILL: ', Cost_gaming())
        Pay += Cost_gaming() + Cost_Rest()
        return Pay


def Bill(x, y, z):
    print('----------------------------------------------------------------------')
    print('Total amount to be paid: ', x)
    print('----------------------------------------------------------------------')

    Ch = int(input('''
Choose the corresponding no to select your method of payment:
(1) Card
(2) Cash
(3) Quit
:'''))

    print('----------------------------------------------------------------------')

    if Ch == 1:
        Del_Gaming(y, z)
        Del_Rest(y, z)
        SQ = "DELETE FROM Hotel WHERE First_name='%s' AND Last_name='%s'" % (y, z)
        c.execute(SQ)
        con.commit()

        crdn = 'a'
        crdcv = 'v'
        while len(crdn) != 19 or len(crdcv) != 3:
            print('----------------------------------------------------------------------')
            crdn = input('Enter your card no: ')
            crdna = input('Enter name of Cardholder: ')
            crdcv = input('Enter the CV number of your card: ')
            print('----------------------------------------------------------------------')

        print('''
Hope you enjoyed your stay! :)
----------------------------------------------------------------------''')

    elif Ch == 2:
        Del_Gaming(y, z)
        Del_Rest(y, z)
        SQ = "DELETE FROM Hotel WHERE First_name='%s' AND Last_name='%s'" % (y, z)
        c.execute(SQ)
        con.commit()

        print('''
Hope you enjoyed your stay! :)
----------------------------------------------------------------------''')

    elif Ch == 3:
        return 'no'

    else:
        print('----------------------------------------------------------------------')
        print('Invalid Entry')
        print('----------------------------------------------------------------------')

def Gaming():
    Rm = []
    gamingbill = 0
    S = 'SELECT Room_no FROM Hotel'

    c.execute(S)
    d = c.fetchall()
    for i in d:
        Rm.append(i[0])

    print('----------------------------------------------------------------------')
    room = int(input('Enter your room no: '))

    print('----------------------------------------------------------------------')
    if room not in Rm:
        print('----------------------------------------------------------------------')
        print('This facility is only available for hotel guests')
        print('----------------------------------------------------------------------')
        return ''

    ch = ''
    while ch == '':
        print("""
*--------------------------------------------*
| 1. Table Tennis 150 Rs./HR                |
| 2. Bowling 100 Rs./HR                     |
| 3. Snooker 250 Rs./HR                     |
| 4. VR World Gaming 400 Rs./HR             |
| 5. Video Games 300 Rs./HR                 |
| 6. Swimming Pool Games 350 Rs./HR         |
| 7. Exit                                   |
*--------------------------------------------*
""")
        print('----------------------------------------------------------------------')
        game = int(input("Select your option by entering the corresponding no: "))
        print('----------------------------------------------------------------------')

        if game == 1:
            print('----------------------------------------------------------------------')
            print("YOU HAVE SELECTED TO PLAY: Table Tennis")
            hour = int(input("Enter No Of Hours You Want To Play: "))
            print('----------------------------------------------------------------------')
            gamingbill += hour * 150
            Insert_g(gamingbill, room, 'Table Tennis', hour)
            ch = input('Press enter to continue: ')

        elif game == 2:
            print('----------------------------------------------------------------------')
            print("YOU HAVE SELECTED TO PLAY: Bowling")
            hour = int(input("Enter No Of Hours You Want To Play: "))
            print('----------------------------------------------------------------------')
            gamingbill += hour * 100
            Insert_g(gamingbill, room, 'Bowling', hour)
            ch = input('Press enter to continue: ')

        elif game == 3:
            print('----------------------------------------------------------------------')
            print("YOU HAVE SELECTED TO PLAY: Snooker")
            hour = int(input("Enter No Of Hours You Want To Play: "))
            print('----------------------------------------------------------------------')
            gamingbill += hour * 250
            Insert_g(gamingbill, room, 'Snooker', hour)
            ch = input('Press enter to continue: ')

        elif game == 4:
            print('----------------------------------------------------------------------')
            print("YOU HAVE SELECTED TO PLAY: VR World Gaming")
            hour = int(input("Enter No Of Hours You Want To Play: "))
            print('----------------------------------------------------------------------')
            gamingbill += hour * 400
            Insert_g(gamingbill, room, 'VR World Gaming', hour)
            ch = input('Press enter to continue: ')

        elif game == 5:
            print('----------------------------------------------------------------------')
            print("YOU HAVE SELECTED TO PLAY: Video Games")
            hour = int(input("Enter No Of Hours You Want To Play: "))
            print('----------------------------------------------------------------------')
            gamingbill += hour * 300
            Insert_g(gamingbill, room, 'Video Games', hour)
            ch = input('Press enter to continue: ')

        elif game == 6:
            print('----------------------------------------------------------------------')
            print("YOU HAVE SELECTED TO PLAY: Swimming Pool Games")
            hour = int(input("Enter No Of Hours You Want To Play: "))
            print('----------------------------------------------------------------------')
            gamingbill += hour * 350
            Insert_g(gamingbill, room, 'Swimming Pool Games', hour)
            ch = input('Press enter to continue: ')

        elif game == 7:
            print('----------------------------------------------------------------------')
            print("Your Total Gaming Bill Is: Rs.", gamingbill)
            print('Have a good day!')
            print('----------------------------------------------------------------------')
            break

        else:
            print("Invalid Entry!!")

def Insert_g(x, y, z, a):
    s = "INSERT INTO GAMING VALUES(%s, '%s', '%s', %s)" % (y, z, a, x)
    c.execute(s)
    con.commit()

def Del_Gaming(x, y):
    Rm = []
    s = "SELECT Room_no FROM Hotel WHERE First_Name='%s' AND Last_Name='%s'" % (x, y)
    c.execute(s)
    d = c.fetchall()
    for i in d:
        S = 'DELETE FROM GAMING WHERE CID=%s' % (i[0])
        c.execute(S)
        con.commit()

def Cost_gaming():
    cog = 0
    Rm = []
    S = 'SELECT Room_no FROM Hotel'
    c.execute(S)
    d = c.fetchall()
    for i in d:
        Rm.append(i[0])
    
    for k in Rm:
        s1 = 'SELECT gaming_bill FROM GAMING WHERE CID=%s' % (k)
        c.execute(s1)
        D = c.fetchall()
        for j in D:
            cog += j[0]
    
    return cog

def Restaurant():
    food = []
    list_1 = []
    Rf = []  # Room list
    S = 'SELECT Room_no FROM Hotel'
    c.execute(S)
    d = c.fetchall()
    for i in d:
        Rf.append(i[0])

    room = int(input('Enter your room no: '))
    if room not in Rf:
        print('This facility is only available for hotel guests')
        return ''

    Nom = input('Enter your First name: ')
    ch = ''
    while ch == '':
        print("""
        *-----------------*
        | 1. Beverages   |
        | 2. Soup        |
        | 3. Starters    |
        | 4. Main Course |
        | 5. Biryani     |
        | 6. Roti        |
        | 7. Rice        |
        | 8. South Indian|
        | 9. Ice Cream   |
        | 10. Exit       |
        *-----------------*
        """)
        
        menu = int(input("Select your option by entering the corresponding no: "))

        if menu == 1:
            beverages(food, list_1)
            ch = input('Press enter to continue:')
        elif menu == 2:
            soups(food, list_1)
            ch = input('Press enter to continue:')
        elif menu == 3:
            starters(food, list_1)
            ch = input('Press enter to continue:')
        elif menu == 4:
            main_course(food, list_1)
            ch = input('Press enter to continue:')
        elif menu == 5:
            biryani(food, list_1)
            ch = input('Press enter to continue:')
        elif menu == 6:
            roti(food, list_1)
            ch = input('Press enter to continue:')
        elif menu == 7:
            rice(food, list_1)
            ch = input('Press enter to continue:')
        elif menu == 8:
            south_indian(food, list_1)
            ch = input('Press enter to continue:')
        elif menu == 9:
            ice_cream(food, list_1)
            ch = input('Press enter to continue:')
        elif menu == 10:
            print('Your order:')
            for a in list_1:
                print(a)
            print(f"Your Total Restaurant Bill Is: Rs. {sum(food)}")
            Insert_R(room, Nom, sum(food))
            print('Have a good day! :)')
            break
        else:
            print("Invalid Entry!!")

def Insert_R(x, y, z):
    s = "INSERT INTO RESTAURANT VALUES (%s, '%s', %s)" % (x, y, z)
    c.execute(s)
    con.commit()

def beverages(x, y):
    ch = 'y'
    while ch == 'y':
        print("""
        *---------------------------------------*
        | BEVERAGES |
        | 1 Regular Tea............. 20.00 Rs. |
        | 2 Masala Tea.............. 25.00 Rs. |
        | 3 Coffee.................. 25.00 Rs. |
        | 4 Lassi................... 30.00 Rs. |
        | 5 Cold Drink.............. 25.00 Rs. |
        | 6 Quit |
        *---------------------------------------*
        """)
        c = int(input("Enter your choice: "))
        if c == 1:
            y.append('Regular tea')
            x.append(20)
        elif c == 2:
            y.append('Masala tea')
            x.append(25)
        elif c == 3:
            y.append('Coffee')
            x.append(25)
        elif c == 4:
            y.append('Lassi')
            x.append(30)
        elif c == 5:
            y.append('Cold drink')
            x.append(25)
        elif c == 6:
            break
        else:
            print("Invalid choice")

def soups(x, y):
    ch = 'y'
    while ch == 'y':
        print("""
        *---------------------------------------*
        | SOUPS |
        | 1 Tomato Soup............ 110.00 Rs. |
        | 2 Hot & Sour............. 110.00 Rs. |
        | 3 Veg. Noodle Soup....... 110.00 Rs. |
        | 4 Sweet Corn............. 110.00 Rs. |
        | 5 Quit |
        *---------------------------------------*
        """)
        c = int(input("Enter your choice: "))
        if c == 1:
            y.append('Tomato Soup')
            x.append(110)
        elif c == 2:
            y.append('Hot & Sour')
            x.append(110)
        elif c == 3:
            y.append('Veg. Noodle Soup')
            x.append(110)
        elif c == 4:
            y.append('Sweet Corn')
            x.append(110)
        elif c == 5:
            break
        else:
            print("Invalid choice")

# Similar functions for `starters`, `main_course`, `roti`, `rice`, `south_indian`, `biryani`, and `ice_cream` can be defined here.


def Cost_Rest():
    coe = 0
    Rm = []
    S = 'SELECT Room_no FROM Hotel'
    c.execute(S)
    d = c.fetchall()
    for i in d:
        Rm.append(i[0])
    for k in Rm:
        s1 = 'SELECT restaurant_bill FROM restaurant WHERE rid=%s' % (k)
        c.execute(s1)
        D = c.fetchall()
        for j in D:
            coe += j[0]
    return coe

def Del_Rest(x, y):
    Rm = []
    s = "SELECT Room_no FROM Hotel WHERE First_Name='%s' AND Last_Name='%s'" % (x, y)
    c.execute(s)
    d = c.fetchall()
    for i in d:
        S = 'DELETE FROM restaurant WHERE RID=%s' % (i[0])
        c.execute(S)
    con.commit()

print('''
WELCOME TO HOTEL LAVIES
---------------------------

We hope that we can make your stay as comfortable as

possible!

------------------------------------------------------------------

''')

op = ''
while op == '':
    print('''
    *----------------------------------------------------------------------------*
    | Please select one of the following options by entering the corresponding no: |
    | (1) Checkin                                                                 |
    | (2) Checkout                                                                |
    | (3) Gaming                                                                  |
    | (4) Catering                                                                |
    | (5) Quit                                                                    |
    *----------------------------------------------------------------------------*
    ''')

    print('----------------------------------------------------------------------')
    opt = int(input('Enter option: '))
    if opt == 1:
        Checkin()
        op = input('Press Enter to continue: ')
    elif opt == 2:
        Checkout()
        op = input('Press Enter to continue: ')
    elif opt == 3:
        Gaming()
        op = input('Press Enter to continue: ')
    elif opt == 4:
        Restaurant()
        op = input('Press Enter to continue: ')
    elif opt == 5:
        print('----------------------------------------------------------------------')
        print('''
        Have a good day!
        ''')
        print('----------------------------------------------------------------------')
        con.close()
        break
    else:
        print('Invalid entry!')
        con.close()
