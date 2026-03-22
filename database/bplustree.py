"""
bplustree.py — B+ Tree Implementation for CallHub Phone Directory
CS 432 Databases | Module A

Follows the exact boilerplate structure provided by the instructor.
Node structure: BPlusTreeNode(order, is_leaf)
Tree structure: BPlusTree(order=8)
"""

from graphviz import Digraph


class BPlusTreeNode:
    def __init__(self, order, is_leaf=True):
        self.order    = order       
        self.is_leaf  = is_leaf     
        self.keys     = []         
        self.values   = []         
        self.children = []          
        self.next     = None        

    def is_full(self):
        return len(self.keys) >= self.order - 1


class BPlusTree:
    def __init__(self, order=8):
        self.order = order                       
        self.root  = BPlusTreeNode(order)       

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node.is_leaf:
            for i, k in enumerate(node.keys):
                if k == key:
                    return node.values[i]
            return None
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            return self._search(node.children[i], key)

    def insert(self, key, value):

        root = self.root

        if root.is_full():
            new_root          = BPlusTreeNode(self.order, is_leaf=False)
            new_root.children = [self.root]
            self._split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        
        if node.is_leaf:
           
            for i, k in enumerate(node.keys):
                if k == key:
                    node.values[i] = value
                    return

            i = len(node.keys) - 1
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and node.keys[i] > key:
                node.keys[i + 1]   = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1]   = key
            node.values[i + 1] = value
        else:
            i = len(node.keys) - 1
            while i >= 0 and node.keys[i] > key:
                i -= 1
            i += 1 

            if node.children[i].is_full():
                self._split_child(node, i)
                if key >= node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, index):
        order = self.order
        child = parent.children[index]
        mid   = (order - 1) // 2 

        new_node          = BPlusTreeNode(order, is_leaf=child.is_leaf)

        if child.is_leaf:
            new_node.keys   = child.keys[mid:]
            new_node.values = child.values[mid:]
            child.keys      = child.keys[:mid]
            child.values    = child.values[:mid]
            new_node.next   = child.next
            child.next      = new_node
            push_up_key     = new_node.keys[0]
        else:
            push_up_key       = child.keys[mid]
            new_node.keys     = child.keys[mid + 1:]
            new_node.children = child.children[mid + 1:]
            child.keys        = child.keys[:mid]
            child.children    = child.children[:mid + 1]
        parent.keys.insert(index, push_up_key)
        parent.children.insert(index + 1, new_node)

    def delete(self, key):
        result = self._delete(self.root, key)
        if not self.root.is_leaf and len(self.root.keys) == 0:
            self.root = self.root.children[0]
        return result

    def _delete(self, node, key):
        t = (self.order - 1) // 2 
        if node.is_leaf:
            if key in node.keys:
                idx = node.keys.index(key)
                node.keys.pop(idx)
                node.values.pop(idx)
                return True
            return False
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            if len(node.children[i].keys) < t:
                self._fill_child(node, i)

                i = 0
                while i < len(node.keys) and key >= node.keys[i]:
                    i += 1

            result = self._delete(node.children[i], key)

            for j in range(len(node.keys)):
                if node.keys[j] == key:

                    leaf = node.children[j + 1]
                    while not leaf.is_leaf:
                        leaf = leaf.children[0]
                    if leaf.keys:
                        node.keys[j] = leaf.keys[0]
                    break

            return result

    def _fill_child(self, node, index):
        t = (self.order - 1) // 2

        if index > 0 and len(node.children[index - 1].keys) > t:
            self._borrow_from_prev(node, index)
        elif index < len(node.children) - 1 and len(node.children[index + 1].keys) > t:
            self._borrow_from_next(node, index)
        else:
            if index < len(node.children) - 1:
                self._merge(node, index)
            else:
                self._merge(node, index - 1)

    def _borrow_from_prev(self, node, index):
        child    = node.children[index]
        left_sib = node.children[index - 1]

        if child.is_leaf:
            child.keys.insert(0, left_sib.keys.pop())
            child.values.insert(0, left_sib.values.pop())
            node.keys[index - 1] = child.keys[0]
        else:
            child.keys.insert(0, node.keys[index - 1])
            child.children.insert(0, left_sib.children.pop())
            node.keys[index - 1] = left_sib.keys.pop()

    def _borrow_from_next(self, node, index):

        child     = node.children[index]
        right_sib = node.children[index + 1]

        if child.is_leaf:
            child.keys.append(right_sib.keys.pop(0))
            child.values.append(right_sib.values.pop(0))
            node.keys[index] = right_sib.keys[0]
        else:
            child.keys.append(node.keys[index])
            child.children.append(right_sib.children.pop(0))
            node.keys[index] = right_sib.keys.pop(0)

    def _merge(self, node, index):
        left  = node.children[index]
        right = node.children[index + 1]

        if left.is_leaf:
            left.keys.extend(right.keys)
            left.values.extend(right.values)
            left.next = right.next
        else:
            left.keys.append(node.keys[index])
            left.keys.extend(right.keys)
            left.children.extend(right.children)
        node.keys.pop(index)
        node.children.pop(index + 1)

    def update(self, key, new_value):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        for i, k in enumerate(node.keys):
            if k == key:
                node.values[i] = new_value
                return True
        return False

    def range_query(self, start_key, end_key):
        results = []
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and start_key >= node.keys[i]:
                i += 1
            node = node.children[i]
        while node is not None:
            for i, k in enumerate(node.keys):
                if k > end_key:
                    return results
                if k >= start_key:
                    results.append((k, node.values[i]))
            node = node.next
        return results


    def get_all(self):
        result = []
        self._get_all(self.root, result)
        return result

    def _get_all(self, node, result):
        if node.is_leaf:
            for i, k in enumerate(node.keys):
                result.append((k, node.values[i]))
        else:
            for child in node.children:
                self._get_all(child, result)

    def height(self):
        node, h = self.root, 1
        while not node.is_leaf:
            node = node.children[0]
            h += 1
        return h

    def count(self):
        return len(self.get_all())

    def min_key(self):
        node = self.root
        while not node.is_leaf: node = node.children[0]
        return node.keys[0] if node.keys else None

    def max_key(self):
        node = self.root
        while not node.is_leaf: node = node.children[-1]
        return node.keys[-1] if node.keys else None

    def visualize_tree(self, filename=None):
        dot = Digraph()
        dot.attr(rankdir='TB', splines='line')
        dot.attr('node', fontname='Times New Roman', fontsize='12')

        if self.root.keys:
            self._add_nodes(dot, self.root)
            self._add_edges(dot, self.root)

        if filename:
            dot.render(filename, format='png', cleanup=True)

        return dot

    def _add_nodes(self, dot, node):
        node_id = str(id(node))

        if node.is_leaf:
            label = ' | '.join(str(k) for k in node.keys)
            dot.node(node_id, label=label, shape='box',
                     style='filled', fillcolor='lightgreen',
                     tooltip='Leaf Node')
        else:
            label = ' | '.join(str(k) for k in node.keys)
            dot.node(node_id, label=label, shape='box',
                     style='filled', fillcolor='lightblue',
                     tooltip='Internal Node')
            for child in node.children:
                self._add_nodes(dot, child)

    def _add_edges(self, dot, node):
        node_id = str(id(node))

        if not node.is_leaf:
            for i, child in enumerate(node.children):
                child_id = str(id(child))
                if i < len(node.keys):
                    dot.edge(node_id, child_id)
                else:
                    dot.edge(node_id, child_id)
                self._add_edges(dot, child)
        else:
            if node.next is not None:
                next_id = str(id(node.next))
                dot.edge(node_id, next_id,
                         style='dashed', color='darkgreen',
                         tooltip='Next Leaf', constraint='false')
