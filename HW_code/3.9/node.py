class Node:

    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state."""

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.state == other.state and self.action == other.action \
                   and self.depth == other.depth and self.parent == other.parent
        else:
            return False

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self)]

    def child_node(self, problem, action):
        return problem.result(self, action)

    @property
    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path[1:]]

    @property
    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
