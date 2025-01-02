# Writing to the file
f = open('Story.txt', 'w')
f.write(''' The Rabbit and Tortoise
Once upon a time there was a Rabbit who was the fastest creature in the forest.
He once challenged the Tortoise to a race.
The Rabbit, halfway through, became too confident that he could win and took a nap.
When he woke up, he realized that he had lost to the Tortoise, all thanks to his overconfidence.
The End''')
f.close()

# Reading from the file and performing calculations
f = open('Story.txt', 'r')
s = 0  # Space count
u = 0  # Uppercase letter count
lo = 0  # Lowercase letter count
t = f.tell()  # Store the current file pointer position
a = f.read()  # Read the entire content
l = a.split()  # Split content into words

# Count spaces, uppercase and lowercase letters
for i in a:
    if i.isspace():
        s += 1
    elif i.isalpha():
        if i.isupper():
            u += 1
        else:
            lo += 1

# Reset file pointer to the stored position for line count
f.seek(t)
li = f.readlines()  # Read lines for line count
f.close()

# Printing the results
print('Number of blanks present in the file:', s)
print('Number of lines present in the file:', len(li))
print('Number of capital letters present in the file:', u)
print('Number of words present in the file:', len(l))
print('Number of lowercase letters present in the file:', lo)
