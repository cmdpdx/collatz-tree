import time
from collatz import CollatzTree

def print_menu():
    print('Collatz tree')
    print('  a - add a number')
    print('  p - print sequence from n to 1')
    print('  f - add numbers from 1 to n to tree')
    print('  l - prints the number of items in the list')
    print('  st - stopping time for n (steps to 1)')
    print('  v - toggle verbose mode (default = True)')
    print('  fs - fills all sequences to 1 of numbers in the list')
    print('  ls - prints the longest current path to 1')
    print()
    print('  s - save the list to file')
    print('  o - load a list from file')
    print('  q - quit')
    print('>>', end='')

c_tree = CollatzTree()
ch = ''

while ch != 'q':
    print_menu()
    ch = input()

    try:
        if ch == 'a':
            c_tree.add(int(input('Number to add: ')))
      
        elif ch == 'p':
            n = int(input('Number to print: '))
            seq = c_tree.get_sequence(n)
            print(' -> '.join([str(n) for n in seq]))
        
        elif ch == 'f':
            n = int(input('Number to fill to: '))
            print("Adding numbers up to {} to the tree...".format(n))
            start = time.perf_counter()
            c_tree.fill(n)
            print("...finished in {:.4f} seconds".format(time.perf_counter() - start))
        
        elif ch == 'st':
            n = int(input('Number to find stopping time: '))
            steps = c_tree.stopping_time(n)
            print('Steps from {} to 1: {}'.format(n, steps))
            seq = c_tree.get_sequence(n)
            print(' -> '.join([str(n) for n in seq]))
        
        
        elif ch == 'l':
            print('Length of Collatz list:', len(c_tree))
        
        elif ch == 'v':
            c_tree.verbose = not c_tree.verbose
            print('Verbose mode is now', c_tree.verbose)
        
        elif ch == 'ls':
            seq = c_tree.longest_sequence()
            print('Longest seq: {} -> 1 in {} steps'.format(seq[0], len(seq)-1))
            print(' -> '.join([str(n) for n in seq]))
        
        elif ch == 'fs':
            print('Filling all sequences to 1...')
            start = time.perf_counter()
            c_tree.fill_sequences()
            print('...Finished in {:.4f} seconds.'.format(time.perf_counter() - start))
        
        elif ch == 's':
            c_tree.save_list()
        
        elif ch == 'o':
            c_tree.load_list()

        elif ch != 'q':
            print("Option not recognized:", ch)
        
    except ValueError:
        print('Invalid input. Must be an integer.')
       
    print()