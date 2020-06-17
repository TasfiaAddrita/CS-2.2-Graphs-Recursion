# Homework 2: Graph Traversals

## Discussion Questions

1. Compare and contrast Breadth-first Search and Depth-first Search by providing one similarity and one difference.

BFS uses a queue to traverse the graph while DFS uses a stack. BFS goes through ALL of the current vertex's neighbors before going to one of the neighbors. DFS follows the path of one neighbor of the current vertex until there are no neighbors, which will then go back to the next neighbor of the current vertex. Both require a way to see which nodes have been visited so we can avoid visiting one node 2 or more times.

2. Explain why a Depth-first Search traversal does not necessarily find the shortest path between two vertices. What is one such example of a graph where a DFS search would not find the shortest path?

Depth-first search is not a good method to find the shortest path because as it traverses through each vertex, the next vertex will be one of the neighbors of the vertex we are currently on. This could create a plethora of paths to get to the destination, many of which are not the shortest path to the final target. For example, we can have an undirected graph of A <-> B <-> C, B <-> D, and C <-> D. The shortest path to get from A to D is through A B D, but DFS might go through C to get to D (A B C D).

3. Explain why we cannot perform a topological sort on a graph containing a cycle.
We can not perform topological sort on a graph that contains a cycle because it will cause an infinite loop -- there is no node to end the traversal on. 


<hr>

# Homework 1: Graph ADT

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

1. How is Breadth-first Search different in graphs than in trees? Describe the differences in your own words.

The key difference between a tree and a graph is that a tree is **acyclic**, meaning that it does not contain any cycles. This is important in regards to breadth-first search because we can expect to visit every node *once* in a tree. You can use a queue without having to dequeue until you reach the end of the tree. However, a graph can contain cycles, which means we may have to visit nodes several times. To avoid this, we visit a node, enqueue it's children, and dequeue the current node and place it in a "seen" list. This way, if we reach a node where we have already *seen* the parents (therefore its parents is also its children) we can continue traversing through the graph without being stuck in a cycle by starting at the next node in the queue.

2. What is one application of Breadth-first Search (besides social networks)? Describe how BFS is used for that application. If you need some ideas, check out [this article](https://www.geeksforgeeks.org/applications-of-breadth-first-traversal/?ref=rp).

An interesting way BFS is used in the real world is through garbage collection. The algorithm is used by an algorithm called the **copying collection**. This algorithm divides the memory heap into two spaces, a *from-space* and a *to-space*. Objects are stored in the from-space until it becomes full. Once it becomes full, the algorithm copies all *live* objects (objects currently being used) to the to-space. The caveat to this is to make sure any objects pointing towards an object in the from-space has to point to the copied object in the to-space. Here, BFS is used to facilitate this step by using the to-space as a queue. [Source](https://www2.cs.arizona.edu/~collberg/Teaching/553/2011/Handouts/Handout-10.pdf)