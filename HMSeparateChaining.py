
class Node:
    def __init__(self, key, next_node=None):
        self.key = key
        self.next = next_node


class HMSeparateChainingSet:
    def __init__(self, head=None):
        self.head = head

    def __str__(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.key) if current.key
                            is not None else "None")
            current = current.next
        return "{" + ", ".join(elements) + "}"

    def __eq__(self, other):
        if other is None:
            return False
        return set(to_list(self.head)) == set(to_list(other.head))

    def __iter__(self):
        self.current = self.head
        return self

    def __next__(self):
        if self.current:
            key = self.current.key
            self.current = self.current.next
            return key
        else:
            raise StopIteration


def cons(element, hm):
    if hm is None:
        return HMSeparateChainingSet(Node(element))
    else:
        return HMSeparateChainingSet(Node(element, hm.head))


def empty():
    """Return an empty linked list"""
    return HMSeparateChainingSet()


def length(hm):
    """Return the length of the linked list"""
    count = 0
    current = hm.head
    while current:
        count += 1
        current = current.next
    return count


def intersection(hm1, hm2):
    """Return the intersection of two immutable linked lists"""
    common_keys = set(to_list(hm1)).intersection(set(to_list(hm2)))
    return from_list(list(common_keys))


def remove(hm, key):
    """Remove the first occurrence of key in the
    immutable linked list and return a new list"""
    filtered_list = filter(hm, lambda x: x != key)
    return filtered_list


def member(key, hm):
    """Check if the key is a member of the linked list"""
    if hm is None:
        return False
    current = hm.head
    while current:
        if current.key == key:
            return True
        current = current.next
    return False


def to_list(hm):
    """Convert the linked list to a Python list"""
    lst = []
    current = hm.head if isinstance(hm, HMSeparateChainingSet) else hm  # 修正这里
    while current:
        lst.append(current.key)
        current = current.next
    return lst


def from_list(lst):
    """Create a linked list from a Python list,
    allowing duplicates and None values."""
    hm = None
    for key in reversed(lst):
        # Reverse the list to maintain order when constructing the linked list
        hm = Node(key, hm)
    return HMSeparateChainingSet(hm)


def concat(hm1, hm2):
    """Concatenate two linked lists"""
    lst1 = to_list(hm1)
    lst2 = to_list(hm2)
    return from_list(lst1 + lst2)


def filter(hm, predicate):
    """Filter the linked list by a predicate function"""
    filtered = None
    for key in reversed(to_list(hm)):
        if predicate(key):
            filtered = cons(key, filtered)
    return filtered


def tmap(hm, func):
    """Apply a function to each element in the linked list
    and return a new list with the results"""
    result_list = []
    current = hm.head
    while current:
        result_list.append(func(current.key))
        current = current.next
    return from_list(result_list)


def reduce(hm, func, initial):
    """Reduce the linked list using a binary function and initial value"""
    result = initial
    current = hm.head
    while current:
        result = func(result, current.key)
        current = current.next
    return result
