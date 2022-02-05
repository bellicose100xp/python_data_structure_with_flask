class Node:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next_node = next_node


class Queue:
    def __init__(self):
        '''
        Here we are tracking head and tail of the queue
        '''
        self.head = None
        self.tail = None

    def enqueue(self, data):
        '''
        Always adds to the tail of the queue
        '''
        if not self.tail and not self.head:
            self.tail = self.head = Node(data)
            return

        self.tail.next_node = Node(data)
        self.tail = self.tail.next_node
        return

    def dequeue(self):
        '''
        Always removes from the head of the queue
        '''
        if not self.head:
            return None

        removed = self.head
        self.head = self.head.next_node

        # If next_node of the head being removed is None then self.tail will also be done as we just removed the last item in the queue
        if not self.head:
            self.tail = None

        return removed
    
    def print_queue(self):
        q_items = ''
        node = self.head
        while node:
            q_items += f' {node.data} -->'
            node = node.next_node
        q_items += ' None'
        print(q_items)

if __name__ == "__main__":
    q = Queue()

    q.enqueue('Latte')
    q.print_queue()
    q.enqueue('Cappuchino')
    q.print_queue()
    q.enqueue('Mocha')
    q.print_queue()
    q.enqueue('Java')
    q.print_queue()

    q.dequeue()
    q.print_queue()
    q.dequeue()
    q.print_queue()
    q.dequeue()
    q.print_queue()
    q.dequeue()
    q.print_queue()

