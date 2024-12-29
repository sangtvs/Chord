import hashlib
import time

class Node:
    def __init__(self, id):
        self.id = id
        self.finger_table = []

    def find_successor(self, key):
        print(f"[DEBUG] Node {self.id} handling lookup for key {key}")
        if self.id == key or (self.id < key <= self.finger_table[0].id):
            return self.finger_table[0]
        for i in range(len(self.finger_table) - 1, -1, -1):
            if self.finger_table[i].id < key:
                return self.finger_table[i].find_successor(key)
        return self

class ChordRing:
    def __init__(self, m):
        self.m = m
        self.nodes = []

    def add_node(self, id):
        new_node = Node(id)
        self.nodes.append(new_node)
        self.nodes.sort(key=lambda node: node.id)
        self.update_finger_tables()

    def remove_node(self, id):
        self.nodes = [node for node in self.nodes if node.id != id]
        self.update_finger_tables()

    def update_finger_tables(self):
        for node in self.nodes:
            node.finger_table = [
                self.find_successor((node.id + 2**i) % (2**self.m))
                for i in range(self.m)
            ]

    def find_successor(self, key):
        for node in self.nodes:
            if node.id >= key:
                return node
        return self.nodes[0]

    def lookup(self, key):
        hops = 0
        current_node = self.nodes[0]  # Start lookup at the first node
        while True:
            hops += 1
            successor = current_node.find_successor(key)
            if successor.id == key or key <= successor.id:
                return successor, hops
            current_node = successor

    def print_finger_tables(self):
        print("\nFinger Tables:")
        for node in self.nodes:
            print(f"Node {node.id}: {[n.id for n in node.finger_table]}")
        print()

def hash_key(data, m):
    return int(hashlib.sha1(data.encode()).hexdigest(), 16) % (2**m)

# Configuration
M = 4  # Chord ring size
ring = ChordRing(M)

# Add nodes
nodes = [1, 5, 9, 12]
for node_id in nodes:
    ring.add_node(node_id)

# Print finger tables after adding nodes
ring.print_finger_tables()

# Test case 1: Lookup with no failed nodes
print("Test Case 1: No Failed Nodes")
keys_to_lookup = [hash_key(f"file{i}", M) for i in range(3)]
for key in keys_to_lookup:
    start_time = time.time()
    successor, hops = ring.lookup(key)
    end_time = time.time()
    print(f"Key {key} found at Node {successor.id} in {hops} hops (Time: {end_time - start_time:.5f}s)")

# Test case 2: Lookup with a failed node
print("\nTest Case 2: Node Failure")
ring.remove_node(9)
ring.print_finger_tables()  # Print finger tables after node removal

for key in keys_to_lookup:
    start_time = time.time()
    successor, hops = ring.lookup(key)
    end_time = time.time()
    print(f"Key {key} found at Node {successor.id} in {hops} hops (Time: {end_time - start_time:.5f}s)")
