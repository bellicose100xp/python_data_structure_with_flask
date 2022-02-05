class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, table_size):
        self.table_size = table_size
        self.hash_table = [None] * table_size  # instantiating a fixed size array equal to table_size filled with value None

    def custom_hash(self, key):
        return hash(key) % self.table_size

    def add_key_value(self, key, value):
        hashed_keys = self.custom_hash(key)
        if self.hash_table[hashed_keys] is None:
            self.hash_table[hashed_keys] = Node(Data(key, value), None)
        else:
            node = self.hash_table[hashed_keys]
            while node.next_node:
                node = node.next_node
            node.next_node = Node(Data(key, value), None)

    def get_value(self, key):
        hashed_keys = self.custom_hash(key)
        if self.hash_table[hashed_keys] is not None:
            node = self.hash_table[hashed_keys]
            if node.next_node is None:
                return node.data.value
            while node.next_node:
                if key == node.data.key:
                    return node.data.value
                node = node.next_node

            if key == node.data.key:
                return node.data.value
        return None

    def print_table(self):
        print('{')
        for idx, item in enumerate(self.hash_table):
            if item is not None:
                node = item
                multi_node_display_string = ''
                while node.next_node:
                    multi_node_display_string += f'{node.data.key}: {node.data.value} --> '
                    node = node.next_node
                multi_node_display_string += f'{node.data.key}: {node.data.value}'
                print(f' [{idx}] {multi_node_display_string}')
            else:
                print(f' [{idx}]')
        print('}')


# ht = HashTable(8)
# ht.add_key_value('hi', 'there')
# ht.add_key_value('be', 'there')
# ht.add_key_value('hi', 'mark')
# ht.add_key_value('hi', 'john')
# ht.add_key_value('run', 'there')
# ht.print_table()
