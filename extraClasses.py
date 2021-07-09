class LimitedListIterator:
    """
    Iterator Class 
    -------- -----

    Iterator class for LimitedList class 

    Citations
    ---------
        Found information on this type of class and class method calling from here: https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/

    """

    def __init__(self, lst):
        self._lst = lst #internal list reference
        self._index = 0 #internal index reference
    
    def __next__(self):
        """
        Returns next value from list

        """

        if self._index < self._lst.length: #make sure index is in range of list, else fall back to raising StopIteration
            value = self._lst[self._index] #get value at current index from list class
            self._index += 1 #increase index by 1

            return value
        
        #Once iteration ends 
        raise StopIteration

class LimitedList:
    """ 
    A new class object that is essentially a list, however has a limited size. This object also includes
    additional functionality for iteration and variable assignment. 

    Parameters 
    ----------

    length: int 
        Length of list. This cannot be changed once object is initialized.

    """

    def __init__(self, length):
        self.length = length
        self._lst = [None] * self.length #create list of None values with specified length 

        self._observingIndex = 0 #when looping with self.next(), this variable used to store current location in loop (special implemantation of form of iteration)

    def __repr__(self):
        return repr(self._lst) #when printing class, simply do what would happen if printing internal list

    def __getitem__(self, indices):
        """ 
        Handle indexing into this custom list-like data storage type. Same usage as 
        indexing into python list

        Raises 
        ------
        
        IndexOutOfRangeError 
            If index passed into list is out of range of specified list length

        IndexObjectNotAcceptedError 
            If index object passed is not an int, tuple, or slice

        Citations 
        ---------
            Found this class method here: https://stackoverflow.com/questions/41686020/python-custom-class-indexing=

            Further information and inspiration from: https://riptutorial.com/python/example/1571/indexing-custom-classes----getitem------setitem---and---delitem--

            Found information on slicing from: https://www.programiz.com/python-programming/methods/built-in/slice

        """

        if isinstance(indices, int): #simply return value at index if only one number is passes (signified by integer being passed)
            if indices <= (self.length - 1) and indices >= 0: #only return if specified index is in range of list 
                return (self._lst[indices])
            else:
                raise self.IndexOutOfRangeError(indices, 0, self.length - 1)
        
        elif isinstance(indices, (int, slice)): #if a slice is passed, return a list of all values within slice (inclusive first value, exclusive second)
            if (indices.start == None or indices.start >= 0) and (indices.stop == None or indices.stop <= self.length-1): #if slice values provided are within the range of the list
                return self._lst[indices] #return simply the slice of the internal list object 
            else: #if the slice bounds are out of range of the list, return out of range error 
                if not (indices.start == None or indices.start >= 0): #if it was the starting value that caused issues
                    raise self.IndexOutOfRangeError(indices.start, 0, self.length - 1)
                elif not (indices.stop == None or indices.stop <= self.length-1): #if the stop value is causing issues 
                    raise self.IndexOutOfRangeError(indices.stop, 0, self.length - 1)
                else: #this shouldn't ever be called as in every case the starting or stopping variable will trigger this if/else... However, this is in place as a fallback in case unknown error occurs 
                    raise self.IndexOutOfRangeError(indices, 0, self.length - 1) 

        elif isinstance(indices, tuple): #return all values at all indicies if multiple indicies are passed (signified by tuple being passed)
            result = [] #empty list to return 
            for index in indices:
                if index <= (self.length - 1) and index >= 0: #make sure index is within range of list 
                    result.append(self._lst[index])
                else: #raise exception if one of passed indices is out of range of list
                    raise self.IndexOutOfRangeError(index, 0, self.length - 1)
            return result  
        else:
            raise self.IndexObjectNotAcceptedError(type(indices), [int, tuple, slice])
        
    def __setitem__(self, key, value):
        """ 
        Handle setting value of specific position. Similar to lists where: lst[key] = value sets 
        lst[key] to value. 

        Can also handle multiple positions by calling: lst[key1, key2, key3, ...] = value. 
        Note: in this instance, if value is a tuple, it must be the same length of keys supplied
        and each key will be set to corrisponding value in tuple in order. With value as any other
        datatype, this will set all specificed keys to the same value. 

        Raises 
        ------
        
        IndexOutOfRangeError 
            If key passed into list is out of range of specified list length

        IndexObjectNotAcceptedError 
            If key object passed is not int or tuple

        Citations
        ---------
            Found this class method here: https://stackoverflow.com/questions/13736718/how-to-make-python-class-support-item-assignment

            Further information and inspiration from: https://riptutorial.com/python/example/1571/indexing-custom-classes----getitem------setitem---and---delitem--

        """
        if isinstance(key, int): #if single key is passed, set only one key to specified value
            if key <= (self.length - 1) and key >= 0: #only set value if key is within set "boundries" of list
                self._lst[key] = value
            else:
                raise self.IndexOutOfRangeError(key, 0, self.length-1)

        elif isinstance(key, tuple) and isinstance(value, tuple) and len(key) == len(value): #handle setting multiple keys all to different values
            for index, specificValue in zip(key, value): #loop through values in key argument and value argument at the same time
                if index <= (self.length - 1) and index >= 0: #only set value if index is within range of list 
                    self._lst[index] = specificValue 
                else: #if index not in range, raise exception
                    raise self.IndexOutOfRangeError(index, 0, self.length-1)
        
        elif isinstance(key, tuple): #handle assignment of multiple keys to same value (depended on value not being tuple, will be caught by above elif otherwise)
            for index in key: 
                if index <= (self.length - 1) and index >= 0: #only set value if index is within range of list 
                    self._lst[index] = value
                else: #if index not in range, raise exception
                    raise self.IndexOutOfRangeError(index, 0, self.length-1)
        
        else: #if key object is niether a tuple or a integer, raise exception
            raise self.IndexObjectNotAcceptedError(type(key), [int, tuple])

    #functions for handling custom iterator that loops over list
    def current(self):
        """ 
        Part of internal looping iterator. Will return value in list of current "position" in iterator. 

        Returns 
        -------

        currentValue: any 
            Current value at current index being observed in list 
        
        """

        return(self._lst[self._observingIndex])

    def next(self, skip=1):
        """
        Move internal looping iterator to next position. Will wrap list if next index is larger than max index
        in list. Will also return next value (value at next position in list). If skip value is defined, next 
        position will increase by that amount, instead of just 1. If a skip value is negative, you will loop 
        backward through list.

        Parameters
        ----------
        skip: int, optional 
            How many index values will be skiped (ie, if set to 2, the observed index will jump 2 forward)

        Returns 
        -------

        nextValue: any 
            Next value in list (will be value at next index)

        """

        tempObservingIndex = self._observingIndex + skip #make temporary variable to find next index when adding "skip" value
        self._observingIndex = tempObservingIndex % self.length #account for looping over list by taking the temporary index mod the length of the list

        return (self._lst[self._observingIndex])

    def seek_position(self, pos):
        """
        Set position observing for internal, looping iteration 

        Parameters 
        ----------

        pos: int 
            Integer for index at which iterator is currently observing 

        Raises
        ------

        IndexOutOfRangeError 
            If position passed is out of range of list

        """

        if pos <= (self.length - 1) and pos >= 0: #only set position if in range of list 
            self._observingIndex = pos
        else: 
            raise self.IndexOutOfRangeError(pos, 0, self.length-1)

    #handle normal iteration over list
    def __iter__(self):
        """
        Handles iteration by returning Iterator Object. See: LimitedListIterator
        
        """

        return LimitedListIterator(self)


    #Defining Exceptions 
    class IndexOutOfRangeError(Exception):
        """ 
        Exception raised if key used to index into list is out of range of list

        Citations
        ---------
            Looked at code from: https://www.programiz.com/python-programming/user-defined-exception
        """

        def __init__(self, key, expectedLower, expectedHigher, message="The key {} is out of range. Expected a value between [{}, {}]."):
            self.key = key
            self.expectedLower = expectedLower
            self.expectedHigher = expectedHigher
            self.message = message.format(self.key, self.expectedLower, self.expectedHigher) 

            super().__init__(self.message)

    class IndexObjectNotAcceptedError(Exception):
        """ 
        Exception raised if object other than the accepted object is passed into the function

        """

        def __init__(self, objectType, expectedObjectTypes, message="Object type {} is not accepted when indexing. Expected: {}"):
            self.objectType = objectType
            self.expectedObjectTypes = expectedObjectTypes
            self.message = message.format(self.objectType, self.expectedObjectTypes)
            super().__init__(self.message)

