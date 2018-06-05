class CollatzTree():
    """
    A data-structure and collection of methods to examine lists of numbers generated
    by the Collatz conjecture algorithm.

    A tree of numbers is stored such that the parents are the previous and
    children are the next terms in the sequence.  Children and parents are 
    not guaranteed to be in numerical order.  Terms are calulated as follows:
        0) If a_n is 1, stop.
        1) If a_n is even, then a_(n+1) = (a_n)/2
        2) If a_n is odd, then a_(n+1) = 3(a_n) + 1
        
    The Collatz conjecture states that all sequences will eventually lead to 1.

    Public methods:
        add -- add n and its sequence to 1 to the tree
        fill -- add all numbers up to n and their paths to 1 to the tree
        fill_path -- store the path from n to 1
        fill_all_paths -- stores all paths from numbers in the tree to 1
        get_path -- returns the list of numbers in the path from n to 1
        get_longest_path -- returns longest path to 1 for numbers in the tree
        get_steps_to_one -- returns the length of the path from n to 1

        save_list -- save the current tree and path structure to file (pickle)
        load_list -- load a tree and path structure from file (pickle)

    Static methods:
        collatz_sequence -- generate the Collatz sequence from n to 1; return list

    Instance variables:
        collatz_tree -- dict; each pair represents {parent: child}
        paths -- dict; each pair represents {number: path}, where path is a list
        verbose -- turns on debugging information printed to console

    See https://en.wikipedia.org/wiki/Collatz_conjecture for more details.

    """
    
    __DEFAULT_FILENAME = 'collatz_pickle'
    
    def __init__(self):
        """Create a new CollatzTree with a single path: 1."""
        self.collatz_tree = {1: 4}  # 1 loops back to 4 (3*1 + 1)
        self.paths = {1: [1]}
        self.verbose = True
    
    def __len__(self):
        return len(self.collatz_tree)
    
    def _info(self, *s):
        """
        Non-public method to print debugging information if the verbose 
        instance variable is True.  Uses inspect to determine the calling 
        function to prepend to the given message strings.
        
        Arguments:
        *s -- 0 or more strings to be printed in order.
        """
        if self.verbose: 
            from inspect import getouterframes, currentframe
            try:
                frame = currentframe()
                outerframes = getouterframes(frame)
                calling_func = outerframes[1].function
                print(calling_func + ':', *s)
            finally:
                del frame
                del outerframes
  
    def load_list(self, filename=__DEFAULT_FILENAME):
        """
        Overwrite the current Collatz tree structure with a saved list in a file.
        
        Keyword arguments:
        filename -- name of the pickle file to use 
          (default CollatzTree.__DEFAULT_FILENAME)
        """
        import pickle

        try:
            f = open(filename, 'rb')
        except FileNotFoundError:
            print(filename, 'does not exist yet.')
        else:
            self.collatz_tree, self.paths = pickle.load(f)
            f.close()
    
    def save_list(self, filename=__DEFAULT_FILENAME):
        """
        Save the current Collatz tree structure to file.
        
        Keyword arguments:
        filename -- name of the pickle file to use 
          (default CollatzTree.__DEFAULT_FILENAME)
        """
        import pickle

        f = open(filename, 'wb')
        pickle.dump((self.collatz_tree, self.paths), f)
        f.close()

    def add(self, n):
        """
        Add the chain (n -> 1) to the Collatz list. 
        
        Arguments:
        n -- the number to start from
        """
        if n in self.collatz_tree:
            self._info(n, 'in the list already')
            return
    
        # Follow the Collatz algorithm:
        #   IF n is even, n = n/2 ELSE n = 3n + 1
        # until 1 is reached. Will this happen for every number n? So far, yes...
        while n > 1:
            if n%2 == 0:
                next_ = n // 2
            else:
                next_ = 3*n + 1
                
            # Add current number -> next number as key, value pair to dict
            # Advance n to the next number
            self.collatz_tree[n] = next_
            self._info(n, '->', str(self.collatz_tree[n]))
            n = next_
              
            # If the next value of n is in the dict already, we can stop.
            # The rest of the chain already exists.
            if n in self.collatz_tree:
                self._info(n, 'in list already (and rest of path)')
                break
    
    def fill(self, n):
        """
        Adds the chains of all (i -> 1) for i from n down to 1 to the Collatz 
        tree that are not currently in the tree.
        
        Arguments:
        n -- the number to start from
        """
        while n > 1:
            if n in self.collatz_tree:
                self._info(n, 'in tree already')
            else:
                self.add(n)
            n -= 1

    def fill_path(self, n):
        if n not in self.collatz_tree:
            self._info(n, 'not in list; adding.')
            self.add(n)
        
        if n in self.paths:
            self._info(n, "path already filled.")
            return

        # create a new path from n to 1 (inclusive)
        path = [n]
        while n > 1:
            next_ = self.collatz_tree[n]
            # if the next number's path is filled, combine with current path and end
            if next_ in self.paths:
                path += self.paths[next_]
                break
            
            path.append(next_)
            n = next_
        
        # save any sub paths that have not yet been filled:
        self._info("backfilling paths...")
        for i in range(len(path)):
            if path[i] in self.paths:
                self._info(path[i], "already exists in paths list; breaking...")
                break
            else:
                self.paths[path[i]] = path[i:]
                self._info("path from {} -> 1 added: {}".format(path[i], str(path[i:])))

    def fill_all_paths(self):
        """
        Fill all of the paths-to-1 for all numbers currently in the tree.
        """
  
        for n in self.collatz_tree:
            if n not in self.paths:
                self.fill_path(n)

    def get_path(self, n):
        """
        Return the Collatz path (n -> 1) as a list of integers.
        
        Arguments:
        n -- the number to start from
        """
        if n not in self.collatz_tree:
            self._info(n, 'not in tree; adding.')
            self.add(n)
        
        if n not in self.paths:
            self._info(n, "path not yet filled...")
            self.fill_path(n)

        return self.paths[n]
  
    def get_longest_path(self):
        """
        Returns a list representing the longest Collatz sequence currently 
        in the list.   
        """
        self.fill_all_paths()
            
        index, length = sorted(list(zip(self.paths.keys(), map(len, self.paths.values()))), key=lambda x: x[1], reverse=True)[0]
        return self.paths[index]
  
    def get_steps_to_one(self, n):
        """
        Return the number of steps from the number n to 1 in the Collatz sequence.

        If n is not aleady in the list, it is added first.  If the path from n 
        down to 1 has not already been filled, that method is called here.
        
        Arguments:
        n -- the number to start from
        """
        if n not in self.collatz_tree:
            self._info(n, 'not in tree; adding.')
            self.add(n)
    
        if n not in self.paths:
            self._info(n, 'path not filled; filling.')
            self.fill_path(n)

        # -1 from len of path because path includes n
        return len(self.paths[n]) - 1
       
    @staticmethod
    def collatz_sequence(n):
        """Generate the Collatz sequence from n to 1; return a list.

        Arguments:
        n -- the number to start from.
        """
        seq = []
        while n > 1:
            seq.append(n)
            if n%2 == 0:
                n = n // 2
            else:
                n = 3*n + 1
      
        seq.append(n)
        return seq
    
