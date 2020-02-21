running = True
num = 1
while running:
    for index in range(num):
        print(index)
    num += 1
    if input("enter: ").lower() == 'quit':
        running = False