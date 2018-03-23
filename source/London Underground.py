#London Underground by Miles Burne 22/3/18
import random

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
    f = open("connection_data.csv","r")
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
    

def manual_traversal(stations):
    station = stations[str(random.randint(1, 306))]
    traversal = True
    print("Type 'x' at any time to exit")
    while traversal == True:
        print("You are at "+(station.get_name()).strip('"'))
        print("From here you can travel to: ")
        options = {}
        number = 1
        for x in station.get_stations() :
            print(str(number)+". "+str(x.get_name()))
            options[number] = x
            number +=1
        choice = (input())
        if choice == "x" or choice == "X":
            traversal = False
        else:
            station = options[int(choice)]

def BFS(stations):
    station = stations[str(random.randint(1, 306))]
    #station = stations["192"]
    visit_list = []
    visited = []
    count = 0
    while count != 305:
        count +=1
        if station not in visited:
            visited.append(station)
            
        for x in station.get_stations():
            #treating 'visit_list' as a queue
            if x not in visited and x not in visit_list:
                visit_list.append(x)
                
            else:
                pass
        try:
            station = visit_list.pop(0)
        except:
            print(count)

        





stations = station_read()
connection_read(stations)
BFS(stations)
manual_traversal(stations)
