class Node:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next_node = next_node


class Stack:
    def __init__(self):
        self.top = None
    
    def peek(self):
        return self.top

    def push(self, data):
        if not self.top:
            self.top = Node(data)
            return

        new_node = Node(data)
        new_node.next_node = self.top
        self.top = new_node
        return

    def pop(self):
        if not self.top:
            return None
        
        removed_node = self.top
        self.top = self.top.next_node
        return removed_node
    
    def print(self):
        stack_string = ''
        node = self.top
        while node:
            stack_string += f' {node.data} -->'
            node = node.next_node
        stack_string += ' None'
        print(stack_string)

if __name__ == "__main__":
    s = Stack()
    s.push('Cappuchino')
    s.print()
    s.push('Latte')
    s.print()
    s.push('Mocha')
    s.print()
    s.push('Java')
    s.print()

    s.pop()
    s.print()
    s.pop()
    s.print()
    s.pop()
    s.print()
    s.pop()
    s.print()