"""
File: linkedbst.py
Author: Ken Lambert
"""
from random import sample, random, shuffle
from time import time
from math import log
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        self._size = 0
        self._positions = list()
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node is not None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)


        def find_rebuild(node):
            while node:
                if node is None:
                    return None
                if node.data == item:
                    return node.data
                if item < node.data:
                    node = node.left
                elif item > node.data:
                    node = node.right
        return find_rebuild(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        def add_rebuild(node):
            while node:
                if node.data > item:
                    if node.left is None:
                        node.left = BSTNode(item)
                        node = None
                    else:
                        node = node.left
                elif node.right is None:
                    node.right = BSTNode(item)
                    node = None
                else:
                    node = node.right

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            add_rebuild(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right is None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode is None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left is None \
                and not currentNode.right is None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left is None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def size(self):
        '''
        Return number of nodes in a tree
        :return: int'''
        return self._size

    def is_root(self, node):
        '''
        Return True if node is root
        :rnode: BSTNode
        :return: bool'''
        return self._root.data == node.data

    def parent(self, node):
        '''Return parent of node
        :rnode: BTSNode
        :rtype: BTSNode'''
        if not isinstance(node, BSTNode):
            raise ValueError('Argument has to be a node')

        def recursive(checker):
            if checker.left:
                if checker.left.data == node.data:
                    return checker
                result = recursive(checker.left)
                if result:
                    return result
            if checker.right:
                if checker.right.data == node.data:
                    return checker
                result = recursive(checker.right)
                if result:
                    return result
            return None

        return recursive(self._root)

    def find_all_nodes(self):
        '''Returns all nodes, that are in the tree
        :rtype: list[BTSNode]'''
        self._positions.append(self._root)
        # print(self._root.data)
        def positions(self, root):
            if root is None:
                return
            if root.left is not None:
                if root.left.data is not None:
                    # print(root.left.data)
                    self._positions.append(root.left)
                    positions(self, root.left)

            if root.right is not None:
                if root.right.data is not None:
                    # print(root.right.data)
                    self._positions.append(root.right)
                    positions(self, root.right)
        positions(self, self._root)
        return self._positions

    def height(self):
        '''
        Returns heigth of a tree
        :rtype: int
        '''
        return max([self.node_height(node) for node in self.find_all_nodes()])

    def node_height(self, node):
        '''
        Return the node_height of tree
        :rnode: BSTNode
        :return: int
        '''
        if self.is_root(node):
            return 0
        else:
            return 1 + self.node_height(self.parent(node))

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < (2*log(self._size+1) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low: int
        :param high: int
        :return: list(int)
        '''
        items = list()

        def recursion(root, low, high):
            if root is None:
                return None
            if root.left is not None:
                if root.left.data >= low:
                    recursion(root.left, low, high)
            if low <= root.data <= high:
                items.append(root.data)
            recursion(root.right, low, high)
        recursion(self._root, low, high)
        return items

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        inorder_traversal = list(self.inorder())
        self.clear()
        inorder_traversal = sorted(inorder_traversal, key=lambda x: x)
        def recursive(lst):
            if len(lst) != 0:
                self.add(lst[len(lst)//2])
                recursive(lst[:len(lst)//2])
                recursive(lst[len(lst)//2 + 1:])
        recursive(inorder_traversal)

    def successor(self, item=None):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if item is not None:
            finded_node = \
min([node for node in self.find_all_nodes() if node.data > item], key=lambda x: x.data)
            if finded_node:
                return finded_node.data
        else:
            finded_node =  min([node for node in self.find_all_nodes()], key=lambda x: x.data)
            if finded_node:
                return finded_node.data
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        finded_node = \
max([node for node in self.find_all_nodes() if node.data < item], key=lambda x: x.data)
        if finded_node:
            return finded_node.data
        return None

    def demo_bst(self, path, NUMBER=10000):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words = self.read_file(path)

        def find_list(words):
            random_words = sample(words, NUMBER)
            iterator = 0
            key = random_words[iterator]

            start_test = time()
            for word in random_words:
                while True:
                    if key == word :
                        iterator = 0
                        break
                    elif iterator != len(words) - 1:
                        iterator += 1
                        key = words[iterator]
                    elif iterator == len(words) - 1:
                        iterator = 0
                        break
            end_test = time()

            print(f'Success: Finded list version: {end_test - start_test}')
            return end_test - start_test

        def find_sorted_tree(words):
            Tree_exp = LinkedBST()
            random_words = sample(words, NUMBER)

            for word in words:
                Tree_exp.add(word)


            start_test = time()
            for word in random_words:
                Tree_exp.find(word)
            end_test = time()

            print(f'Success: Finded sorted tree version {end_test - start_test}')
            return end_test - start_test

        def find_random_tree(words):
            Tree_exp = LinkedBST()
            random_words = sample(words, NUMBER)
            shuffle(words)

            for word in words:
                Tree_exp.add(word)

            start_test = time()
            for word in random_words:
                Tree_exp.find(word)
            end_test = time()

            print(f'Success: Finded random tree version {end_test - start_test}')
            return end_test - start_test

        def find_rebalanced_tree(words):
            Tree_exp = LinkedBST()
            random_words = sample(words, NUMBER)
            shuffle(words)
            for word in words:
                Tree_exp.add(word)

            Tree_exp.rebalance()

            start_test = time()
            for word in random_words:
                Tree_exp.find(word)
            end_test = time()

            print(f'Success: Finded rebalanced tree version {end_test - start_test}')
            return end_test - start_test


        return find_list(words), \
            find_sorted_tree(words), \
            find_random_tree(words), \
            find_rebalanced_tree(words)

    @staticmethod
    def read_file(path):
        '''
        Returns list of words that file contain
        :type path: int
        :rtype: int
        '''
        words = list()
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                words.append(line.strip())
        return words

Tree = LinkedBST()
print(Tree.demo_bst('words.txt', 100))
