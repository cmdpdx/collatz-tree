from collatz import CollatzTree

def print_menu():
    print('Collatz list')
    print('  a - add a number')
    print('  p - print a number chain')
    print('  f - fill list up to a number')
    print('  l - prints the number of items in the list')
    print('  e - steps from number to 1')
    print('  v - toggle verbose mode (default = True)')
    print('  cp - calculates all paths to 1 of numbers in the list')
    print('  lp - prints the longest current path to 1')
    print()
    print('  c - print the Collatz chain of a number independently')
    print()
    print('  t - test')
    print('  s - save the list to file')
    print('  o - load a list from file')
    print('  q - quit')
    print('>>', end='')

c_list = CollatzTree()
ch = ''

while ch != 'q':
    print_menu()
    ch = input()

    try:
        if ch == 'a':
            c_list.add(int(input('Number to add: ')))
      
        elif ch == 'p':
            n = int(input('Number to print: '))
            path = c_list.get_path(n)
            print(' -> '.join([str(n) for n in path]))
        
        elif ch == 'f':
            c_list.fill(int(input('Number to fill to: ')))
        
        elif ch == 'e':
            n = int(input('Number to find steps to 1: '))
            steps = c_list.get_steps_to_one(n)
            print('Steps from {} to 1: {}'.format(n, steps))
            path = c_list.get_path(n)
            print(' -> '.join([str(n) for n in path]))
        
        
        elif ch == 'l':
            print('Length of Collatz list:', len(c_list))
        
        elif ch == 'v':
            c_list.verbose = not c_list.verbose
            print('Verbose mode is now', c_list.verbose)
        
        elif ch == 'lp':
            path = c_list.get_longest_path()
            print('Longest path: {} -> 1 in {} steps'.format(path[0], len(path)-1))
            print(' -> '.join([str(n) for n in path]))
        
        elif ch == 'cp':
            print('Filling all paths to 1...')
            c_list.fill_all_paths()
            print('...Finished.')
            
            #path = c_list.get_longest_path()
            #print('Longest path: {} -> 1 in {} steps'.format(path[0], len(path)-1))
            #print(' -> '.join([str(n) for n in path]))
        
        elif ch == 'c':
            CollatzTree.collatz(int(input('Number to get Collatz chain: ')))
            print()
        
        elif ch == 't':
            item1 = CollatzTree.Item(4)
            item2 = CollatzTree.Item(4)
            print(item1 == item2)
            print(item1 == 5)
            print()
        
        elif ch == 's':
            c_list.save_list()
        
        elif ch == 'o':
            c_list.load_list()
        
    except ValueError:
        print('Invalid input. Must be an integer.')
       
    print()