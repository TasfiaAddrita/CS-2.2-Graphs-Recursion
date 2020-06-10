# Homework 1: Graph ADT & Traversals

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

1. How is Breadth-first Search different in graphs than in trees? Describe the differences in your own words.

The key difference between a tree and a graph is that a tree is **acyclic**, meaning that it does not contain any cycles. This is important in regards to breadth-first search because we can expect to visit every node *once* in a tree. You can use a queue without having to dequeue until you reach the end of the tree. However, a graph can contain cycles, which means we may have to visit nodes several times. To avoid this, we visit a node, enqueue it's children, and dequeue the current node and place it in a "seen" list. This way, if we reach a node where we have already *seen* the parents (therefore its parents is also its children) we can continue traversing through the graph without being stuck in a cycle by starting at the next node in the queue.

2. What is one application of Breadth-first Search (besides social networks)? Describe how BFS is used for that application. If you need some ideas, check out [this article](https://www.geeksforgeeks.org/applications-of-breadth-first-traversal/?ref=rp).

An interesting way BFS is used in the real world is through garbage collection. The algorithm is used by an algorithm called the **copying collection**. This algorithm divides the memory heap into two spaces, a *from-space* and a *to-space*. Objects are stored in the from-space until it becomes full. Once it becomes full, the algorithm copies all *live* objects (objects currently being used) to the to-space. The caveat to this is to make sure any objects pointing towards an object in the from-space has to point to the copied object in the to-space. Here, BFS is used to facilitate this step by using the to-space as a queue. [Source](https://www2.cs.arizona.edu/~collberg/Teaching/553/2011/Handouts/Handout-10.pdf)