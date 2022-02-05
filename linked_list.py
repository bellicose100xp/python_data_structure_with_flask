class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def to_array(self):
        arr = []
        if self.head is None:
            return arr

        node = self.head
        while node:
            arr.append(node.data)
            node = node.next_node

        return arr

    def print_ll(self):
        ll_string = ''
        node = self.head
        while node:
            ll_string += f'{node.data} -> '
            node = node.next_node
        ll_string += ' None'
        print(ll_string)

    def insert_beginning(self, data):
        if self.head is None:
            self.head = Node(data)
            self.tail = self.head
            return

        self.head = Node(data, self.head)

    def insert_at_end(self, data):
        node_to_add = Node(data)

        if self.head == None:
            self.insert_beginning(data)
            return

        self.tail.next_node = node_to_add
        self.tail = node_to_add

    def get_user_by_id(self, id):
        node = self.head
        
        while node:
            if node.data["id"] == int(id):
                print(node.data["id"])
                return node.data
            node = node.next_node
        
        return f'user_id: {id} not found.'

# For testing purposes
# ll = LinkedList()
# ll.insert_beginning({"id": 'a'})
# ll.insert_beginning({"id": 'b'})
# ll.insert_beginning({"id": 'c'})
# ll.insert_beginning({"id": 'd'})
# ll.insert_beginning({"id": 'e'})
# ll.insert_at_end({"id": 'x'})
# ll.insert_at_end({"id": 'y'})
# ll.insert_at_end({"id": 'z'})
# # ll.print_ll()
# ll.get_user_by_id('c')
