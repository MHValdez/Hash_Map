hash = 0
for letter in 'str14':
    hash += ord(letter)

hash %= 53

address = hash
print(hash)
print()

address = hash + (1 ^ 2)
print(address)
print(1**2)