import copy


class Node:
    def __init__(self, key, next_node=None):
        self.key = key
        self.next = next_node


class HMSeparateChainingSet:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return (hash(key) & 0x7fffffff) % self.size

    @staticmethod
    def _insert_node(head, key):
        if not head:
            return Node(key)
        else:
            return Node(head.key, HMSeparateChainingSet._insert_node
                        (head.next, key))

    @staticmethod
    def _remove_node(head, key):
        if not head:
            return None
        if head.key == key:
            return head.next
        else:
            return Node(head.key, HMSeparateChainingSet._remove_node
                        (head.next, key))

    @staticmethod
    def _to_list(node):
        lst = []
        while node:
            lst.append(node.key)
            node = node.next
        return lst

    def __copy__(self):
        # 创建一个新的HMSeparateChainingSet对象
        new_hmscs = HMSeparateChainingSet(self.size)
        new_hmscs.table = copy.deepcopy(self.table)  # 创建table属性的深拷贝
        return new_hmscs

    def insert(self, key):
        index = self._hash(key)
        new_table = self.table[:]
        new_table[index] = self._insert_node(new_table[index], key)
        new_obj = HMSeparateChainingSet(self.size)
        new_obj.table = new_table
        return new_obj

    def remove(self, key):
        index = self._hash(key)
        new_table = self.table[:]
        new_table[index] = self._remove_node(new_table[index], key)
        new_obj = HMSeparateChainingSet(self.size)
        new_obj.table = new_table
        return new_obj

    def contains(self, key):
        index = self._hash(key)
        node = self.table[index]
        while node:
            if node.key == key:
                return True
            node = node.next
        return False

    def to_list(self):
        # 如果有键值对列表就返回它
        if hasattr(self, 'mapped_items'):
            return self.mapped_items
        # 否则就返回键的列表
        result = []
        for head in self.table:
            result.extend(self._to_list(head))
        return result

    @staticmethod
    def empty():
        return HMSeparateChainingSet()

    @staticmethod
    def from_list(lst):
        hmap = HMSeparateChainingSet.empty()
        for key in lst:
            hmap = hmap.insert(key)
        return hmap

    def filter(self, condition):
        result_list = [key for key in self.to_list() if condition(key)]
        return HMSeparateChainingSet.from_list(result_list)

    def map(self, transform):
        mapped_list = []
        for key in self.to_list():
            transformed_pair = transform(key, key)
            mapped_list.append(transformed_pair)
        new_hmscs = HMSeparateChainingSet(self.size)
        for k, v in mapped_list:
            new_hmscs.insert(k)
        new_hmscs.mapped_items = mapped_list
        return new_hmscs

    def reduce(self, combine, initial):
        result = initial
        for key in self.to_list():
            result = combine(result, key)
        return result

    def length(self):
        count = sum(1 for node in self.to_list())
        return count

    def __str__(self):
        elements = ', '.join(str(key) if key is not None else 'None'
                             for key in self.to_list())
        return f'{{{elements}}}'


def cons(key, hmscs: HMSeparateChainingSet):
    new_hmscs = hmscs.__copy__()  # 实现__copy__方法来复制当前实例
    new_hmscs.insert(key)  # 使用上文定义的insert方法
    return new_hmscs
