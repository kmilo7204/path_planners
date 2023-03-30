#!/usr/bin/env
from __future__ import annotations

import math

class nodeTree():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.children = []
        self.parent = None

        self.nearestDistance = 5.0
        self.nearestNode = None

    def printInfo(self):
        print("Point X: {}, Point Y: {b}".format(self.x, self.y))

    # This one is working, we need to reset the nearest node and the distance, when adding the node
    def findNearest(self, root: nodeTree, node: nodeTree) -> nodeTree:
        distance = self.findDistance(root, node)
        if distance <= self.nearestDistance:
            print("Distance: {}, for Node {}, {}".format(distance, root.x, root.y))
            self.nearestDistance = distance
            self.nearestNode = root
        for child in root.children:
            self.findNearest(child, node)

        return self.nearestNode

    def findDistance(self, node1: nodeTree, node2: nodeTree) -> float:
        return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

    # print("Nearest node at: {} - {}".format(nearestNode.x, nearestNode.y))
    # This will return the nearest point

# I have to create a function to add a Child to the node.
def addNode(root, point):
    # The addition will depend on the closest given node
    # First find the nearest
    # Add the node
    print("Adding")
    newNode = nodeTree(point[0], point[1])
    root.children.append(newNode)

def printTree(root):
    """
        This function will iterate over all the Tree and will print all the elements
    """
    print(root.x, root.y)
    for child in root.children:
        printTree(child)

class RRT():
    def __init__(self, start, end):
        self.start_pos = start
        self.end_pos = end

        self.tree = None

    def find_path(self):
        self.tree = nodeTree(0)
        pass

if __name__ == "__main__":
    # This is the root
    tree = nodeTree(0, 1)
    addNode(tree, [1, 2])
    addNode(tree, [4, 2])
    addNode(tree, [7, 1])
    addNode(tree, [12, 2])

    new_elem = nodeTree(12, 5)
    printTree(tree)

    # Find nearest node, to the new point
    nearestNode = tree.findNearest(tree, new_elem)

    print("Nearest node at: {} - {}".format(nearestNode.x, nearestNode.y))

"""
    We create the root
    We add a random point
    We interpolate the random point within the desired range
    We find the nearest node (Based on its distance)
    We append the node to the nearest (Child). And we set the nearest as parent of our node.
    Keep iterating
"""
