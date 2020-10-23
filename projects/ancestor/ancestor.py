test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

# my initial attempt before looking over the solution of Artem provided was to look at each value in the list of tuples and determine which tuples contained the starting node. Determining this helps me limit my focus to a few tuples now. I then grab each tuple from the track list and find the largest value. The idea is that if the starting_node is in multiple tuples then it has some ancestry but if it is in only in 1 then it has no ancestry.
# def earliest_ancestor(ancestors, starting_node):
#     track = []
#     earliest = None
#     early_peeps = -1
#     for i in ancestors:
#         if i[1] == starting_node:
#             track.append(i)

#             while len(track) > 0:
#                 early_peeps = track.pop()
#                 earliest = max(early_peeps)
        
#                 if early_peeps == -1:
#                     print(-1)

#     print(earliest)


def earliest_ancestor(ancestors, starting_node):
    graph = {}

    for pairs in ancestors:
        # print(pairs[0], "first number in each tuple we traverse over")
        # print(pairs[1], "second number in each tuple we traverse over")
        if pairs[0] not in graph:
            graph[pairs[0]] = set()
        
        if pairs[1] not in graph:
            graph[pairs[1]] = set()

        graph[pairs[1]].add(pairs[0])


    queue = [ [starting_node] ]
    visited = set()

    max_length = 1
    curent_ancestor = -1

    while len(queue) > 0:
        cur_path = queue.pop(0)
        # print(cur_path)
        cur_vertex = cur_path[-1]
        # print(cur_vertex)
        if cur_vertex not in visited:
            visited.add(cur_vertex)

        if len(cur_path) > max_length or len(cur_path) >= max_length and cur_vertex < curent_ancestor:
            max_length = len(cur_path)
            curent_ancestor = cur_vertex

        for n in graph[cur_vertex]:
            new_path = list(cur_path)
            new_path.append(n)
            queue.append(new_path)
    
    return curent_ancestor

    # print(graph)

        

    


earliest_ancestor(test_ancestors, 3)