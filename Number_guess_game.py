import random

print('''
Welcome to guess the number!!
You will be given a range of numbers to select from
From there you will guess a number by entering the number you want to guess
Good Luck!!
''')

ch = 'y'
while ch == 'y':
    a, b = random.randint(0, 100), random.randint(0, 100)
    lower, upper = min(a, b), max(a, b)
    
    print(f'Guess a number from {lower} to {upper}')
    target = random.randint(lower, upper)
    
    g = int(input('Enter the number you want to guess: '))
    
    if g == target:
        print('Yay!! You guessed correctly')
    else:
        print(f'''Oh no!
The number was {target}, Better luck next time!!''')
    
    ch = input('Do you wish to play again? (y/n): ')

print('Thanks for playing!!')
