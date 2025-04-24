class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Minimum degree
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.next = None  # Used to link leaf nodes

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def insert(self, k):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            # Root is full, split it
            new_root = BTreeNode(self.t, False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(self.root, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def _split_child(self, parent, i):
        t = self.t
        y = parent.children[i]
        z = BTreeNode(t, y.leaf)
        parent.keys.insert(i, y.keys[t - 1])
        parent.children.insert(i + 1, z)

        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]
        else:
            z.next = y.next
            y.next = z

    def traverse_leaves(self):
        node = self.root
        while not node.leaf:
            node = node.children[0]
        while node:
            print(node.keys, end=" -> ")
            node = node.next
        print("None")

# Example usage
btree = BTree(t=2)
for key in [10, 20, 5, 6, 12, 30, 7, 17]:
    btree.insert(key)

btree.traverse_leaves()
