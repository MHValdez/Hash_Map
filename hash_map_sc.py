# Name: Marcos Valdez
# OSU Email: valdezmar@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/10/2022
# Description: A class implementation of a chaining hash map ADT built
#              from a dynamic array for the table and a linked list for
#              buckets. Includes a basic test suite that runs when file
#              is run as a script. Depends on a6_include.py.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    """
    Represents a hash map that handles collision with chaining
    and maintains a prime number of buckets. Includes methods
    to update and query contents as well as various helper
    functions. Depends on multiple classes and functions
    imported from a6_include.py.
    """
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #
    # Begin student implementation

    def put(self, key: str, value: object) -> None:
        """
        Adds a new SLNode class object to the hash map with data
        members key and value. If the key already exists in the
        hash map, the value is updated.

        :param key: A string representing a hash key
        :param value: Any object with implementations for comparison
                      operators and string representation.

        :return: None
        """
        # Determine hash and check chain for key
        hashPos = self._hash_function(key) % self.get_capacity()
        chain = self._buckets[hashPos]
        node = chain.contains(key)

        # Insert key/value pair or update value
        if node is None:
            chain.insert(key, value)
            self._size += 1
        else:
            node.value = value

    def empty_buckets(self) -> int:
        """
        :return empty: Integer representing the number of empty
                       buckets in the hash table.
        """
        empty = 0

        for pos in range(self._capacity):
            bucket = self._buckets[pos]

            if bucket.length() == 0:
                empty += 1

        return empty

    def table_load(self) -> float:
        """
        :return: A floating point number representing the load factor
                 (elements / buckets) of the hash map.
        """
        return self.get_size() / self.get_capacity()

    def clear(self) -> None:
        """
        Clears the contents of the hash map.

        :return: None
        """
        # Do nothing for already empty hash maps
        if self._size != 0:
            for pos in range(self.get_capacity()):
                bucket = self._buckets[pos]

                # Clear non-empty buckets
                if bucket.length() != 0:
                    self._buckets[pos] = LinkedList()

            self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table to the next smallest prime number
        >= new_capacity. Does nothing if new_capacity is < 1.

        :param new_capacity: An integer >= 1 representing the minimum
                             new hash table size.

        :return: None
        """
        if new_capacity >= 1:
            newBuckets = DynamicArray()

            # Capacity must be a prime number
            if self._is_prime(new_capacity):
                newCap = new_capacity
            else:
                newCap = self._next_prime(new_capacity)

            for pos in range(newCap):
                newBuckets.append(LinkedList())

            # Rehash all elements
            for pos in range(self._capacity):
                chain = self._buckets[pos]

                if chain.length() != 0:
                    for node in chain:
                        key = node.key
                        value = node.value

                        # Determine hash and check chain for key
                        hashPos = self._hash_function(key) % newCap
                        newChain = newBuckets[hashPos]
                        newNode = newChain.contains(key)

                        # Insert key/value pair or update value
                        if newNode is None:
                            newChain.insert(key, value)
                        else:
                            newNode.value = value

            self._buckets = newBuckets
            self._capacity = newCap

    def get(self, key: str) -> object:
        """
        Gets the value associated with key in the hash map.

        :param key: A string representing a hash key

        :return: The object representing the value associated with the key
                 if the key exists in the hash map.
                 None otherwise.
        """
        # Don't search empty tables
        if self._size == 0:
            return None

        # Determine hash and check chain for key
        hashPos = self._hash_function(key) % self.get_capacity()
        chain = self._buckets[hashPos]
        node = chain.contains(key)

        if node is None:
            return None

        return node.value

    def contains_key(self, key: str) -> bool:
        """
        Determines if key is present in the hash map.

        :param key: A string representing a hash key

        :return: True if the key is in the hash map
                 False otherwise
        """
        # Don't search empty tables
        if self._size == 0:
            return False

        # Determine hash and check chain for key
        hashPos = self._hash_function(key) % self.get_capacity()
        chain = self._buckets[hashPos]
        node = chain.contains(key)

        return node is not None

    def remove(self, key: str) -> None:
        """
        Removes the node with key as its key data member from the
        hash map. Does nothing if the key is not in the hash map.

        :param key: A string representing a hash key

        :return: None
        """
        # Don't search empty tables
        if self._size != 0:
            # Determine hash and check chain for key
            hashPos = self._hash_function(key) % self.get_capacity()
            chain = self._buckets[hashPos]
            node = chain.contains(key)

            # Remove key/value pair
            if node is not None:
                chain.remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Creates a DynamicArray containing tuples of all key/value
        pairs in the hash map.

        :return elements: A DynamicArray as described above.
        """
        elements = DynamicArray()

        # Don't search empty tables
        if self._size != 0:
            # Process all elements
            for pos in range(self._capacity):
                chain = self._buckets[pos]

                if chain.length() != 0:
                    for node in chain:
                        key = node.key
                        value = node.value
                        elements.append((key, value))

        return elements

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Creates a tuple in which the first value is a DynamicArray
    of all mode values in da and the second value is an integer
    representing their frequency. Depends on the HashMap class.

    :param da: A DynamicArray containing at least one element
               in which all elements are strings.

    :return: A tuple as described above
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    mapSize = map.get_capacity()
    maxFreq = 0
    modes = DynamicArray()

    # Resize table for performance
    if da.length() / mapSize > 1:
        map.resize_table(mapSize)

    # Build hash map where keys are da elements and
    # values are their respective number of occurrences
    for pos in range(da.length()):
        key = da[pos]
        count = map.get(key)

        if count is None:
            count = 1
        else:
            count += 1

        map.put(key, count)

        if count > maxFreq:
            maxFreq = count

    # Get all counts and populate array of modes
    mapValues = map.get_keys_and_values()

    for pos in range(mapValues.length()):
        pair = mapValues[pos]

        if pair[1] == maxFreq:
            modes.append(pair[0])

    return modes, maxFreq

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
