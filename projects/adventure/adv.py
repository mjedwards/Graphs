from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def _search(player, moves, _map):

    q = Queue()
    q.enqueue([player.current_room.id])

    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        current_room = path[-1]

        if current_room not in visited:
            visited.add(current_room)

            for exit in _map[current_room]:

                if _map[current_room][exit] == '?':
                    return path

                else:
                    new_path = list(path)
                    new_path.append(_map[current_room][exit])
                    q.enqueue(new_path)
    return []


def never_searched(player, queue, _map):
    exits = _map[player.current_room.id]

    not_used = []

    for direction in exits:
        if exits[direction] == "?":
            not_used.append(direction)
    if len(not_used) == 0:
        not_explored = _search(player, queue, _map)

        new_room = player.current_room.id
        for room in not_explored:
            for direction in _map[new_room]:
                if _map[new_room][direction] == room:
                    queue.enqueue(direction)
                    new_room = room
                    break
    else:
        queue.enqueue(not_used[random.randint(0, len(not_used) - 1)])


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

_map = {}
queue = Queue()

not_visited = {}

for i in player.current_room.get_exits():
    not_visited[i] = "?"

_map[world.starting_room.id] = not_visited


never_searched(player, queue, _map)

reverse_dir = {"n": "s", "s": "n", "e": "w", "w": "e"}


while queue.size() > 0:
    cur_room = player.current_room.id
    move = queue.dequeue()

    player.travel(move)
    traversal_path.append(move)
    next_room = player.current_room.id

    _map[cur_room][move] = next_room

    if next_room not in _map:
        _map[next_room] = {}

        for exit in player.current_room.get_exits():
            _map[next_room][exit] = "?"

   
    _map[next_room][reverse_dir[move]] = cur_room

    if queue.size() == 0:
        never_searched(player, queue, _map)





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
 


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
