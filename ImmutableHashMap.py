class ImmutableHashMap:
    def __init__(self, bucket_size=10):
        self.bucket_size = bucket_size
        self.buckets = tuple([[] for _ in range(bucket_size)])
        self.keys_order = []

    def _hash_function(self, key):
        return hash(key) % self.bucket_size

    def _make_new_buckets(self, key, value, index, replace=False, remove_key=False):
        new_buckets = list(map(list, self.buckets))  # 复制现有的存储结构
        new_keys_order = list(self.keys_order)

        if remove_key and key in new_keys_order:
            new_keys_order.remove(key)  # 移除键的顺序

        if replace and new_buckets[index]:
            for i, (existing_key, _) in enumerate(new_buckets[index]):
                if existing_key == key:
                    new_buckets[index][i] = (key, value)
                    return new_buckets, new_keys_order

        new_buckets[index] = new_buckets[index] + [(key, value)] if not remove_key else [item for item in new_buckets[index] if item[0] != key]

        if not replace and not remove_key:
            new_keys_order.append(key)

        return new_buckets, new_keys_order

    def add(self, key, value):
        index = self._hash_function(key)
        new_buckets, new_keys_order = self._make_new_buckets(key, value, index)
        return ImmutableHashMap(bucket_size=self.bucket_size)._with_data(new_buckets, new_keys_order)

    def remove(self, key):
        index = self._hash_function(key)
        new_buckets, new_keys_order = self._make_new_buckets(key, None, index, remove_key=True)
        return ImmutableHashMap(bucket_size=self.bucket_size)._with_data(new_buckets, new_keys_order)

    def _with_data(self, buckets, keys_order):
        new_map = ImmutableHashMap(self.bucket_size)
        new_map.buckets = tuple(map(tuple, buckets))
        new_map.keys_order = keys_order
        return new_map

    def get(self, key):
        index = self._hash_function(key)
        for k, v in self.data[index]:
            if k == key:
                return v
        return None

    def set_element(self, key, value):
        return self._put(key, value)

    def _put(self, key, value):
        index = self._hash_function(key)
        new_bucket = []
        replaced = False

        for k, v in self.data[index]:
            if k == key:
                new_bucket.append((key, value))
                replaced = True
            else:
                new_bucket.append((k, v))
            
        if not replaced:
            new_bucket.append((key, value))
            
        new_data = self.data[:index] + (new_bucket,) + self.data[index + 1:]
        return ImmutableHashMap(new_data, self.bucket_size)
            
    def remove(self, key):
        index = self._hash_function(key)
        new_bucket = [(k, v) for k, v in self.data[index] if k != key]
        new_data = self.data[:index] + (new_bucket,) + self.data[index + 1:]
        return ImmutableHashMap(new_data, self.bucket_size)

    def is_member(self, key):
        return self.get(key) is not None
    
    def to_builtin_list(self):
        return [(key, value) for bucket in self.data for key, value in bucket]

class MonoidHashMap(ImmutableHashMap):
    @staticmethod
    def empty(bucket_size=10):
        # 返回一个空的哈希映射实例
        return MonoidHashMap(bucket_size=bucket_size)

    def concat(self, other):
        # 合并两个哈希映射
        new_map = self
        for key, value in other.to_builtin_list():
            new_map = new_map.set_element(key, value)
        return new_map

    def map_by_function(self, func):
        # 应用函数到所有值
        new_data = tuple([[(k, func(v)) for k, v in bucket] for bucket in self.data])
        return MonoidHashMap(new_data, self.bucket_size)

    def reduce(self, func, initial=None):
        # 对所有值进行归约操作
        result = initial
        for key, value in self.to_builtin_list():
            result = func(result, value) if result is not None else value
        return result