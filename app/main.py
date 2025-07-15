class Node:
    def __init__(self, key, value, hash_value):
        self.key = key
        self.value = value
        self.hash = hash_value
        self.next = None


class Dictionary:
    def __init__(self, initial_capacity=8, load_factor=0.75):
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.length = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key):
        return hash(key) & 0x7FFFFFFF

    def _index(self, hash_value):
        return hash_value % self.capacity

    def __setitem__(self, key, value):
        h = self._hash(key)
        idx = self._index(h)
        node = self.buckets[idx]

        while node:
            if node.hash == h and node.key == key:
                node.value = value
                return
            node = node.next

        new_node = Node(key, value, h)
        new_node.next = self.buckets[idx]
        self.buckets[idx] = new_node
        self.length += 1

        if self.length / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key):
        h = self._hash(key)
        idx = self._index(h)
        node = self.buckets[idx]

        while node:
            if node.hash == h and node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key '{key}' not found in dictionary")

    def __len__(self):
        return self.length

    def __delitem__(self, key):
        h = self._hash(key)
        idx = self._index(h)
        prev = None
        node = self.buckets[idx]

        while node:
            if node.hash == h and node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[idx] = node.next
                self.length -= 1
                return
            prev = node
            node = node.next

        raise KeyError(f"Key '{key}' not found for deletion")

    def clear(self):
        self.buckets = [None] * self.capacity
        self.length = 0

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.length = 0

        for head in old_buckets:
            node = head
            while node:
                self[node.key] = node.value
                node = node.next
