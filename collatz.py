import pickle
from inspect import getouterframes, currentframe


def collatz_sequence(n):
    """Generate the Collatz sequence from n to 1; return a list.

    Argument:
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


class CollatzTree(object):
    """A data-structure and collection of methods to examine lists of numbers generated
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
        fill_sequences -- calculates (if needed) and stores all sequences of numbers in the tree to 1
        get_sequence -- returns the list of numbers in the sequence from n to 1
        longest_sequence -- returns longest sequence to 1 for numbers in the tree
        stopping_time -- returns the stopping time of n (length of the sequence from n to 1)
        save_list -- save the current tree and sequence structure to file (pickle)
        load_list -- load a tree and sequence structure from file (pickle)
    Non-public mehtods:
        _calc_sequence -- calculate and store the sequence from n to 1
        _info -- print debugging information to the console (if verbose == True)
    Instance variables:
        collatz_tree -- dict; each pair represents {parent: child} such that collatz(parent) = child
        seqs -- dict; each pair represents {number: sequence}, where sequence is a list
        verbose -- turns on debugging information printed to console
    See https://en.wikipedia.org/wiki/Collatz_conjecture for more details.
    """
    
    __DEFAULT_FILENAME = 'collatz_pickle'
    
    def __init__(self):
        """Create a new CollatzTree with a single sequence: 1."""
        self.collatz_tree = {1: 4}  # 1 loops back to 4 (3*1 + 1)
        self.seqs = {1: [1]}
        self.verbose = True
        self._longest = 1
    
    def __len__(self):
        return len(self.collatz_tree)
    
    def _info(self, *s):
        """Non-public method to print debugging information if the verbose 
        instance variable is True.  Uses inspect to determine the calling 
        function to prepend to the given message strings.
        
        Argument:
        *s -- 0 or more strings to be printed in order.
        """
        if self.verbose: 
            try:
                frame = currentframe()
                outerframes = getouterframes(frame)
                calling_func = outerframes[1].function
                print(calling_func + ':', *s)
            finally:
                del frame
                del outerframes
  
    def load_list(self, filename=__DEFAULT_FILENAME):
        """Overwrite the current Collatz tree structure with a saved list in a file.
        
        Keyword argument:
        filename -- name of the pickle file to use (default CollatzTree.__DEFAULT_FILENAME)
        """
        try:
            f = open(filename, 'rb')
        except FileNotFoundError:
            print(filename, 'does not exist yet.')
        else:
            self.collatz_tree, self.seqs = pickle.load(f)
            f.close()
    
    def save_list(self, filename=__DEFAULT_FILENAME):
        """Save the current Collatz tree structure to file.
        
        Keyword argument:
        filename -- name of the pickle file to use (default CollatzTree.__DEFAULT_FILENAME)
        """
        f = open(filename, 'wb')
        pickle.dump((self.collatz_tree, self.seqs), f)
        f.close()

    def add(self, n):
        """Add the sequence of (n -> 1) to the Collatz list. 
        
        Argument:
        n -- the number to start from
        """
        info = self._info
        if n in self.collatz_tree:
            info(n, 'in the list already')
            return
    
        # Follow the Collatz algorithm:
        #   IF n is even, n = n/2 ELSE n = 3n + 1
        # until 1 is reached. Will this happen for every number n? So far, yes...
        while n > 1:
            if n % 2 == 0:
                next_ = n // 2
            else:
                next_ = 3*n + 1

            self.collatz_tree[n] = next_
            info(n, '->', str(self.collatz_tree[n]))
            n = next_
              
            # If the next value of n is in the dict already, we can stop.
            # The rest of the chain already exists.
            if n in self.collatz_tree:
                info(n, 'in list already (and rest of sequence)')
                break
    
    def fill(self, n):
        """Adds the sequences of all (i -> 1) for i from n down to 1 to the Collatz 
        tree that are not currently in the tree.
        
        Argument:
        n -- the number to start from
        """
        while n > 1:
            if n in self.collatz_tree:
                self._info(n, 'in tree already')
            else:
                self.add(n)
            n -= 1

    def _calc_sequence(self, n):
        """Calculate the sequence from n -> 1 via the Collatz algorithm and add it to 
        the instance's list of sequences.
        
        First checks if n is in the Collatz tree yet, if not add it. Then checks to see if the
        sequence already exists (don't reinvent the wheel). Once the sequence is built, also save
        every sub-sequence (by removing the first element each time) if it hasn't already been
        calculated.  This saves time later.

        Argument:
        n -- number to begin sequence from
        """
        info = self._info
        if n not in self.collatz_tree:
            info(n, 'not in list; adding.')
            self.add(n)
        if n in self.seqs:
            info(n, "sequence already filled.")
            return

        # create a new sequence from n to 1 (inclusive)
        seq = [n]
        i = n
        while i > 1:
            next_ = self.collatz_tree[i]
            # if the next number's sequence is filled, combine with current sequence and end
            if next_ in self.seqs:
                seq += self.seqs[next_]
                break
            
            seq.append(next_)
            i = next_

        # new longest sequence?
        if len(seq) > len(self.seqs[self._longest]):
            info("new longest sequence ({})".format(n))
            self._longest = n

        # save any sub-sequences that have not yet been filled:
        info("backfilling sequences...")
        for i in range(len(seq)):
            if seq[i] in self.seqs:
                info(seq[i], "already exists in sequences list; breaking...")
                break
            else:
                self.seqs[seq[i]] = seq[i:]
                info("seq from {} -> 1 added: {}".format(seq[i], str(seq[i:])))

    def fill_sequences(self):
        """Fill all of the sequences 1 for all numbers currently in the tree."""
        for n in self.collatz_tree:
            if n not in self.seqs:
                self._calc_sequence(n)

    def get_sequence(self, n):
        """Return the Collatz sequence (n -> 1) as a list of integers.
        
        Argument:
        n -- the number to start from
        """
        if n not in self.collatz_tree:
            self._info(n, 'not in tree; adding.')
            self.add(n)
        if n not in self.seqs:
            self._info(n, "sequence not yet filled...")
            self._calc_sequence(n)
        return self.seqs[n]
  
    def longest_sequence(self):
        """Returns a list representing the longest Collatz sequence currently in the list."""
        self.fill_sequences()

        # Look at this complex line of code! Impressive yeah? Sure, but unnecessary.
        #index, length = sorted(list(zip(self.seqs.keys(), map(len, self.seqs.values()))), key=lambda x: x[1], reverse=True)[0]

        # Instead, longest sequence is stored as an instance variable and updated after
        # every new sequence is calculated.
        return self.seqs[self._longest]
  
    def stopping_time(self, n):
        """Return the stopping time for n (number of steps from the number n to 1) in the Collatz sequence.

        If n is not aleady in the list, it is added first.  If the sequence from n 
        down to 1 has not already been filled, that method is called here.
        
        Argument:
        n -- the number to start from
        """
        if n not in self.collatz_tree:
            self._info(n, 'not in tree; adding.')
            self.add(n)
        if n not in self.seqs:
            self._info(n, 'sequence not filled; filling.')
            self._calc_sequence(n)
        # -1 from len of sequence because sequence includes n
        return len(self.seqs[n]) - 1
