#London Underground by Miles Burne 22/3/18 - 27/3/18
import random
import math


#station class
class Station():
    #constructor
    def __init__(self, ID, name, lat, long, zone):
        self.ID = ID
        self.name = name
        self.lat = lat
        self.long = long
        self.zone = zone
        self.neighbour = {} #{obj: [time, line]}

    def add_station(self, obj, line, time):
        self.neighbour[obj] = [time, line]

    def get_stations(self):
        return(self.neighbour)

    def get_name(self):
        return(self.name)

    def get_pos(self):
        return([self.lat, self.long])

    def get_zone(self):
        return(self.zone)

    def get_ID(self):
        return(self.ID)

def searchForLeastCost(costs, processed):
    lowestCost = math.inf
    lowestCostNode = None
    for node in costs:
        cost = costs[node]
        #check if cheapest
        if cost < lowestCost and node not in processed:
            lowestCost = cost
            lowestCostNode = node
    return(lowestCostNode)

def formulate(graph, startNode):
    costs = {}
    parents = {}
    processed = []
    #making costs
    for w in graph:
        costs[w] = math.inf
    #adding costs from start node
    costs[startNode] = 0
    for x in graph[startNode]:
        costs[x] = graph[startNode][x]
    #creating parents
    for y in graph:
        parents[y] = None
    #adding parents from start node
    parents[startNode] = 0
    for z in graph[startNode]:
        parents[z] = startNode
    #creating processed
    processed.append(startNode)
    return(parents, costs, processed)

def dijkstra(graph, startNode):
    parents, costs, processed = formulate(graph, startNode)
    node = searchForLeastCost(costs, processed)
    #if while loop over nodes all processed
    while node is not None:
        #get all neighbours from node & their total costs
        cost = costs[node]
        neighbours = graph[node]
        for n in neighbours:
            newCost = cost + neighbours[n]
            #if newcost less than previous noted 'shortest' cost...
            if costs[n] > newCost:
                #then update costs and parents to say so
                costs[n] = newCost
                parents[n] = node
        #now all neighbours noted node has been processed
        processed.append(node)
        #find next node
        node = searchForLeastCost(costs, processed)
    return(parents, costs, processed)
        
def dijksta_main(stations, station, target):
    if station == 0:
        station = 0
    target = "End"
    #make graph
    graph = {}
    #nodes
    graph["Start"] = {}
    graph["A"] = {}
    graph["B"] = {}
    graph["End"] = {}
    #node connections
    graph["Start"]["A"] = 6
    graph["Start"]["B"] = 2
    graph["A"]["End"] = 1
    graph["B"]["A"] = 3
    graph["B"]["End"] = 5

    #use dijkstras
    parents, costs, processed = dijkstra(graph, "Start")
    #give answer
    travelList = [target]
    parent = parents[target]
    if parent == 0:
        pass
    else:
        travelList.insert(0, parent)
    while parent != 0:
        parent = parents[parent]
        if parent == 0:
            pass
        else:
            travelList.insert(0, parent)
    #formatting the answers
    print("The path of "+", ".join(travelList)+" was taken")
    print("With a total cost of "+str(costs[target]))
    print("The nodes were processed in the order "+", ".join(parents))

#reads in the station_data file to initialise each station
def station_read():
    stations = {}
    f = open("station_data.csv","r")
    file = f.read()
    file = file.split("\n")
    file.pop(0)
    for x in file:
        line = x.split(",")
        station = Station(line[0], line[3], line[1], line[2], line[5])
        stations[line[0]] = station
    return(stations)            

#reads the line_data file to create a dictionary of every line
def line_read():
    lines = {}
    f = open("line_data.csv","r")
    file = f.read()
    file = file.split("\n")
    file.pop(0)
    for x in file:
        line = x.split(",")
        lines[line[0]] = line[1]
    return(lines)

#reads the connection_data file to create connections between the objects
def connection_read(stations):
    lines = line_read()
    f = open("london.connections.csv","r")
    file = f.read()
    file = file.split("\n")
    file.pop(0)
    for x in file:
        line = x.split(",")
        try:
            station1 = line[0]
            station2 = line[1]
            station1 = stations[station1]
            station2 = stations[station2]
            station1.add_station(station2, line[2], line[3])
            station2.add_station(station1, line[2], line[3])
        except:
            pass
    


#allows the user to 'move' through the stations
def manual_traversal(stations, station=0):
    lines = line_read()
    if type(station) == type(0):
        station = stations[str(random.randint(1, 307))]
    traversal = True
    print("Type 'x' at any time to exit")
    while traversal == True:
        print("You are at "+(station.get_name()).strip('"'))
        print("From here you can travel to: ")
        options = {}
        number = 1
        for x in station.get_stations() :
            print(str(number)+". "+str(x.get_name())+" on the "+str(lines[str(station.get_stations()[x][1])]))
            options[number] = x
            number +=1
        choice = (input())
        print()
        if choice == "x" or choice == "X":
            traversal = False
        else:
            station = options[int(choice)]

#Breadth First Search
def BFS(stations, station = 0):
    if type(station) == type(0):
        station = stations[str(random.randint(1, 307))]
    visit_list = []
    visited = []
    count = 0
    output = []
    while count != 310:
        count +=1
        if station not in visited:
            visited.append(station)
            output.append(station.get_name())
        for x in station.get_stations():
            #treating 'visit_list' as a queue
            if x not in visited and x not in visit_list:
                visit_list.append(x)
                
            else:
                pass
        try:
            station = visit_list.pop(0)
        except:
            pass
    return(output)


#Depth First Search
def DFS(stations, station=0):
    if type(station) == type(0):
        station = stations[str(random.randint(1, 307))]
    visit_stack = []
    visited = []
    output = []
    count = 0
    while count != 310:
        count +=1
        if station not in visited:
            visited.append(station)
            output.append(station.get_name())

        for x in station.get_stations():
            #treating 'visit_list' as a stack
            if x not in visited and x not in visit_stack:
                visit_stack.append(x)
            else:
                pass
        try:
            station = visit_stack.pop()
        except:
            pass
    return(output)
    

#allows user to manually search all the stations
def manual_search(stations):
    input_loop = True
    while input_loop == True:
        user_data = input("Please enter the name or ID of the station: \n")
        try:
            #testing for ID
            user_data = int(user_data)
            if user_data < 0 or user_data > 308:
                end = int("hello")
            found = False
            for x in stations:
                if str(user_data) == x:
                    chosen_station = stations[x]
                    found = True
                else:
                    pass
            if found == True:
                input_loop = False
            else:
                input_loop = True
        except:
            #testing for name
            if type(user_data) == type("string"):
                user_data.strip('"')
                found = False
                for x in stations:
                    if user_data == stations[x].get_name().strip('"'):
                        chosen_station = stations[x]
                        found = True
                    else:
                        pass
                if found == True:
                    input_loop = False
                else:
                    input_loop = True

    #final data
    neigh = chosen_station.get_stations()
    lines = line_read()
    lat, long = chosen_station.get_pos()
    print("Station Data: ")
    print("   ID: "+chosen_station.get_ID())
    print("   Name: "+chosen_station.get_name().strip('"'))
    print("   Zone: "+chosen_station.get_zone())
    print("   Latitude: "+lat)
    print("   Longitude: "+long)
    print("   Connected to: ")
    for x in neigh:
        print(" "*17+x.get_name()+" on line "+lines[neigh[x][1]]+" time: "+neigh[x][0])
    print("\nThis station has been set as your station of choice")
    print()
    return(chosen_station)
    
            



   

#the main menu
def main_menu():
    station = 0
    stations = station_read()
    print((stations))
    connection_read(stations)
    print("Welcome to the London Underground Program by Miles Burne")
    while True:
        input_loop = True
        print("Please select an option")
        print("1. Manual Traversal")
        print("2. Manual Search")
        print("3. Depth First Search")
        print("4. Breadth First Search")
        print("5. Dijkstra's Algorithm")
        print("6. Remove Station Choice")
        while input_loop == True:
            choice = input()
            print()
            if choice == "1":
                manual_traversal(stations, station)
                input_loop = False
            elif choice == "2":
                station = manual_search(stations)
                input_loop = False
            elif choice == "3":
                print(DFS(stations,station))
                print()
                input_loop = False
            elif choice == "4":
                print(BFS(stations,station))
                print()
                input_loop = False
            elif choice == "5":
                target = input("Please enter a target station name\n")
                dijkstra_main(stations, station)
                input_loop = False
                print()
            elif choice == "6":
                station = 0
                input_loop = False
                print("Choice Removed")
            else:
                print("Please select an option")
            
    
main_menu()

