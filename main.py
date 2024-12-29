import hashlib
import random
import sys

# Tăng giới hạn đệ quy (nếu cần thiết)
sys.setrecursionlimit(2000)

# Số bit xác định không gian khóa (ID space)
M = 5  # 2^5 = 32 ID space

# Hàm băm để tạo ID từ chuỗi
def hash_key(key):
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2**M)

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.successor = self  # Ban đầu, successor là chính nó
        self.predecessor = None
        self.finger_table = []

    def join(self, known_node):
        """Tham gia mạng Chord qua một nút đã biết."""
        if known_node:
            self.init_finger_table(known_node)
            self.update_others()
        else:
            # Là nút đầu tiên trong mạng
            for i in range(M):
                self.finger_table.append(self)
            self.successor = self
            self.predecessor = self

    def init_finger_table(self, known_node):
        """Khởi tạo bảng finger."""
        print(f"Node {self.id}: Initializing finger table using node {known_node.id}")
        self.successor = known_node.find_successor((self.id + 1) % (2**M))
        self.finger_table = [self.successor]

        for i in range(1, M):
            finger_id = (self.id + 2**i) % (2**M)
            self.finger_table.append(known_node.find_successor(finger_id))

    def find_successor(self, key_id):
        """Tìm successor của một khóa."""
        print(f"Node {self.id}: Finding successor for key {key_id}")
        if self.id == key_id or (self.id < key_id <= self.successor.id):
            print(f"Node {self.id}: Successor of {key_id} is {self.successor.id}")
            return self.successor
        else:
            closest_node = self.closest_preceding_node(key_id)
            if closest_node == self:
                return self.successor
            return closest_node.find_successor(key_id)

    def closest_preceding_node(self, key_id):
        """Tìm node gần nhất trước key_id trong finger table."""
        for i in range(M - 1, -1, -1):
            finger = self.finger_table[i]
            if self.id < finger.id < key_id:
                print(f"Node {self.id}: Closest preceding node to {key_id} is {finger.id}")
                return finger
        return self

    def update_others(self):
        """Cập nhật finger table của các nút khác."""
        for i in range(M):
            pred_id = (self.id - 2**i + 2**M) % (2**M)
            pred = self.find_successor(pred_id)
            pred.update_finger_table(self, i)

    def update_finger_table(self, node, i):
        """Cập nhật finger table."""
        if self.id <= node.id < self.finger_table[i].id:
            self.finger_table[i] = node
            pred = self.predecessor
            if pred:
                pred.update_finger_table(node, i)

    def __str__(self):
        """Hiển thị thông tin node."""
        fingers = ', '.join([str(finger.id) for finger in self.finger_table])
        return f"Node {self.id} -> Successor: {self.successor.id}, Predecessor: {self.predecessor.id if self.predecessor else 'None'}, Fingers: {fingers}"
# Khởi tạo các node
def simulate_chord():
    print("Initializing Chord Network...")

    # Tạo nút đầu tiên
    node1 = Node(hash_key('Node1'))
    node1.join(None)  # Node đầu tiên không có known_node

    # Thêm node khác
    node2 = Node(hash_key('Node2'))
    node2.join(node1)

    node3 = Node(hash_key('Node3'))
    node3.join(node1)

    node4 = Node(hash_key('Node4'))
    node4.join(node1)

    # In ra thông tin node
    print("\nChord Ring State:")
    for node in [node1, node2, node3, node4]:
        print(node)

    # Tìm successor cho một khóa
    key = hash_key('some_key')
    print(f"\nFinding successor for key: {key}")
    successor = node1.find_successor(key)
    print(f"Successor of key {key} is Node {successor.id}")


if __name__ == "__main__":
    simulate_chord()
