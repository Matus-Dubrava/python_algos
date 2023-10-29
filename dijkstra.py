from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple
import sys
import heapq


@dataclass
class Node:
    value: int
    adjacent_nodes: Dict[int, "Node"] = field(default_factory=dict)
    visited: bool = False
    cost: int = sys.maxsize
    prev_node: Optional["Node"] = None

    def traverse(self):
        self.visited = True
        print(self.value)
        for node in self.adjacent_nodes.values():
            if not node.visited:
                node.traverse()


@dataclass
class Graph:
    nodes: Dict[int, Node] = field(default_factory=dict)

    def add_connection(
        self, src_node_value: int, dest_node_value: int, bidirectional: bool = False
    ):
        if src_node_value not in self.nodes:
            src_node = Node(src_node_value)
            self.nodes[src_node_value] = src_node
        else:
            src_node = self.nodes[src_node_value]

        if dest_node_value not in self.nodes:
            dest_node = Node(dest_node_value)
            self.nodes[dest_node_value] = dest_node
        else:
            dest_node = self.nodes[dest_node_value]

        if dest_node_value not in src_node.adjacent_nodes:
            src_node.adjacent_nodes[dest_node_value] = dest_node

        if bidirectional:
            if src_node_value not in dest_node.adjacent_nodes:
                dest_node.adjacent_nodes[src_node_value] = src_node

    def find_node(self, value: int) -> Optional[Node]:
        return self.nodes.get(value)

    def traverse(self, start: int):
        current_node = self.find_node(start)
        if current_node is not None:
            current_node.visited = True
            print(current_node.value)
            for node in current_node.adjacent_nodes.values():
                if not node.visited:
                    node.traverse()


def dijkstra(g: Graph, start: int, end: int) -> Optional[Tuple[int, List[int]]]:
    def get_shortest_path(end_node: Node) -> List[int]:
        path: List[int] = []
        current_node = end_node
        while current_node is not None:
            path.append(current_node.value)
            current_node = current_node.prev_node

        return list(reversed(path))

    queue: List[Node] = []
    current_node = g.find_node(start)
    if current_node is None:
        return None

    current_node.cost = 0
    heapq.heappush(queue, (0, current_node))

    while len(queue) != 0:
        current_node: Node
        _, current_node = heapq.heappop(queue)
        for node in current_node.adjacent_nodes.values():
            if node.value == end:
                node.prev_node = current_node
                return current_node.cost + 1, get_shortest_path(node)

            if node.cost > current_node.cost + 1:
                node.prev_node = current_node
                node.cost = current_node.cost + 1
                heapq.heappush(queue, (node.cost, node))

    return -1


if __name__ == "__main__":
    g = Graph()
    g.add_connection(1, 2)
    g.add_connection(2, 3)
    g.add_connection(3, 4)
    g.add_connection(4, 5)
    g.add_connection(5, 6)
    g.add_connection(3, 6)

    begin = g.find_node(1)

    print(dijkstra(g, 1, 6))
