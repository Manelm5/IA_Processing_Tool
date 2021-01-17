# This file contains all the required routines to make an A* search algorithm.
#
__authors__='TO_BE_FILLED'
__group__='DL01'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
import math


class Node:
    # __init__ Constructor of Node Class.
    def __init__(self, station, father):
        """
        __init__: 	Constructor of the Node class
        :param
                - station: STATION information of the Station of this Node
                - father: NODE (see Node definition) of his father
        """
        
        self.station = station      # STATION information of the Station of this Node
        self.g = 0                  # REAL cost - depending on the type of preference -
                                    # to get from the origin to this Node
        self.h = 0                  # REAL heuristic value to get from the origin to this Node
        self.f = 0                  # REAL evaluate function
        if father ==None:
			self.parentsID=[]
        else:
			self.parentsID = [father.station.id]
			self.parentsID.extend(father.parentsID)         # TUPLE OF NODES (from the origin to its father)
        self.father = father        # NODE pointer to his father
        self.time = 0               # REAL time required to get from the origin to this Node
                                    # [optional] Only useful for GUI
        self.num_stopStation = 0    # INTEGER number of stops stations made from the origin to this Node
                                    # [optional] Only useful for GUI
        self.walk = 0               # REAL distance made from the origin to this Node
                                    # [optional] Only useful for GUI
        self.transfers = 0          # INTEGER number of transfers made from the origin to this Node
                                    # [optional] Only useful for GUI


    def setEvaluation(self):
        """
        setEvaluation: 	Calculates the Evaluation Function. Actualizes .f value
       
        """
        self.f=self.g+self.h


    def setHeuristic(self, typePreference, node_destination,city):
        """"
        setHeuristic: 	Calculates the heuristic depending on the preference selected
        :params
                - typePreference: INTEGER Value to indicate the preference selected: 
                                0 - Null Heuristic
                                1 - minimum Time
                                2 - minimum Distance 
                                3 - minimum Transfers
                                4 - minimum Stops
                - node_destination: PATH of the destination station
                - city: CITYINFO with the information of the city (see CityInfo class definition)
        """
        xf=self.station.x-node_destination.station.x
        yf=self.station.y-node_destination.station.y
        
        if typePreference == 0:
            self.h=0
        elif typePreference == 1:
            tiempoEstaciones= (math.sqrt(xf*xf + yf*yf)) / city.velocity_lines[node_destination.station.line -1]
            if self.station.name == node_destination.station.name:
                self.h=0
            
            elif self.station.line==node_destination.station.line:
                self.h= tiempoEstaciones
            
            else:
                if self.station.id in city.multipleLines:
                     if node_destination.station.line in city.multipleLines[self.station.id]:
                         self.h= tiempoEstaciones
                
                elif node_destination.station.id in city.multipleLines:
                    if self.station.line in city.multipleLines[node_destination.station.id]:
                         self.h= tiempoEstaciones
                
                else:
                    
                    self.h= tiempoEstaciones
                    mediaTiempoTransbordo = sum(city.transfers_time)/len(city.transfers_time)
                    self.h=tiempoEstaciones+mediaTiempoTransbordo
                    
        elif typePreference == 2:
            distanciaEstaciones= (math.sqrt(xf*xf + yf*yf))
            self.h=distanciaEstaciones
            
        elif typePreference==3:
            if self.station.line != node_destination.station.line :
                self.h = 1 
            else:
                self.h= 0
                
        elif typePreference==4:
            if self.station.name == node_destination.station.name:
                self.h=0
            elif self.station.line != node_destination.station.line :
                self.h = 1 
            else:
                self.h= 0


    def setRealCost(self,  costTable):
        """
        setRealCost: 	Calculates the real cost depending on the preference selected
        :params
                 - costTable: DICTIONARY. Relates each station with their adjacency an their real cost. NOTE that this
                             cost can be in terms of any preference.
        """
        
        estacioOrigen=self
        estacioAuxiliar=self
        while estacioOrigen.father!=None:
            estacioOrigen=estacioOrigen.father
            self.g=self.g+costTable[estacioAuxiliar.station.id][estacioOrigen.station.id]
            estacioAuxiliar=estacioOrigen
        
        
        




def Expand(fatherNode, stationList, typePreference, node_destination, costTable,city):
    lista=[]
   
    listaAdyacente=costTable[fatherNode.station.id].keys()
    for i in listaAdyacente:
       lista.append(Node(stationList[i-1],fatherNode))
    return lista
    
     
    
    
    



def RemoveCycles(childrenList):
    """
        RemoveCycles: It removes from childrenList the set of childrens that include some cycles in their path.
        :params
                - childrenList: LIST of the set of child Nodes for a certain Node
        :returns
                - listWithoutCycles:  LIST of the set of child Nodes for a certain Node which not includes cycles
    """
    listWithoutCycles=[]
    idList=[]
    
    stationAct=childrenList[0].father
    id=stationAct.station.id
    idList.append(id)
    while stationAct.father != None:
        stationAct=stationAct.father
        id=stationAct.station.id
        idList.append(id)

 
    for child in childrenList:
        if child.station.id not in idList:
            listWithoutCycles.append(child)
            
   
    return listWithoutCycles
        
        



def RemoveRedundantPaths(childrenList, nodeList, partialCostTable):
    """
        RemoveRedundantPaths:   It removes the Redundant Paths. They are not optimal solution!
                                If a node is visited and have a lower g in this moment, TCP is updated.
                                In case of having a higher value, we should remove this child.
                                If a node is not yet visited, we should include to the TCP.
        :params
                - childrenList: LIST of NODES, set of childs that should be studied if they contain rendundant path
                                or not.
                - nodeList : LIST of NODES to be visited
                - partialCostTable: DICTIONARY of the minimum g to get each key (Node) from the origin Node
        :returns
                - childrenList: LIST of NODES, set of childs without rendundant path.
                - nodeList: LIST of NODES to be visited updated (without redundant paths)
                - partialCostTable: DICTIONARY of the minimum g to get each key (Node) from the origin Node (updated)
    """
    
    for child in list(childrenList):
            if child.station.id in partialCostTable:
                cost = partialCostTable[child.station.id]
                if child.g < cost:
                    partialCostTable[child.station.id] = child.g
                    for node in nodeList:
                        if child.station.id == node.station.id:
                            nodeList.remove(node)
                            break
                else:
                    childrenList.remove(child)
            else:
                partialCostTable[child.station.id] = child.g
    return childrenList, nodeList, partialCostTable

def sorted_insertion(nodeList,childrenList):
	""" Sorted_insertion: 	It inserts each of the elements of childrenList into the nodeList.
							The insertion must be sorted depending on the evaluation function value.
							
		: params:
			- nodeList : LIST of NODES to be visited
			- childrenList: LIST of NODES, set of childs that should be studied if they contain rendundant path
                                or not.
		:returns
                - nodeList: sorted LIST of NODES to be visited updated with the childrenList included 
	"""

        for node in childrenList:
            nodeList.append(node)
        return nodeList


def setCostTable( typePreference, stationList,city):
    """
    setCostTable :      Real cost of a travel.
    :param
            - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
            - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)
            - city: CITYINFO with the information of the city (see CityInfo class definition)
    :return:
            - costTable: DICTIONARY. Relates each station with their adjacency an their g, depending on the
                                 type of Preference Selected.
    """
    costTable={}
    if typePreference == 1:
        
        for station in stationList:
            costTable[station.id]={}
            for key,cost in station.destinationDic.items():
                costTable[station.id][key]=cost
                
       
        
    elif typePreference==2:
        for station in stationList:
            costTable[station.id]={}
            for key,cost in station.destinationDic.items():
                costTable[station.id][key]=0
                destino=stationList[key-1]
                if(station.name != destino.name):
                    costTable[station.id][key]=cost*city.velocity_lines[station.line-1]
             
               
              
                
    elif typePreference==3:
        for station in stationList:
            costTable[station.id]={}
            for key in station.destinationDic.items():
                destino=stationList[key[0]-1]
                if(station.line != destino.line):
                    costTable[station.id][key[0]]=1
                else:
                    costTable[station.id][key[0]]=0
                    
    elif typePreference==4:
        for station in stationList:
            costTable[station.id]={}
            for key in station.destinationDic.items():
                destino=stationList[key[0]-1]
                if(station.name == destino.name):
                    costTable[station.id][key[0]]=0
                else:
                    costTable[station.id][key[0]]=1
   
    return costTable
         



def coord2station(coord, stationList):
    """
    coord2station :      From coordinates, it searches the closest station.
    :param
            - coord:  LIST of two REAL values, which refer to the coordinates of a point in the city.
            - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)

    :return:
            - possible_origins: List of the Indexes of the stationList structure, which corresponds to the closest
            station
    """
    
    distance=[]
    possible_origins=[]
    
    for station in stationList:
        distance.append(math.sqrt((coord[0]-station.x)**2+(coord[1]-station.y)**2))
    
    minimum=min(distance)
    id=0
    for i in distance:  
        if i==minimum:
            possible_origins.append(id)
        id=id+1
    
    return possible_origins
     
        
        
    

	

def AstarAlgorithm(stationList, coord_origin, coord_destination, typePreference,city,flag_redundants):
    """
     AstarAlgorithm: main function. It is the connection between the GUI and the AStar search code.
     INPUTS:
            - stationList: LIST of the stations of a city. (- id, name, destinationDic, line, x, y -)
            - coord_origin: TUPLE of two values referring to the origin coordinates
            - coord_destination: TUPLE of two values referring to the destination coordinates
            - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
            - city: CITYINFO with the information of the city (see CityInfo class definition)
			- flag_redundants: [0/1]. Flag to indicate if the algorithm has to remove the redundant paths (1) or not (0)
			
    OUTPUTS:
            - time: REAL total required time to make the route
            - distance: REAL total distance made in the route
            - transfers: INTEGER total transfers made in the route
            - stopStations: INTEGER total stops made in the route
            - num_expanded_nodes: INTEGER total expanded nodes to get the optimal path
            - depth: INTEGER depth of the solution
            - visitedNodes: LIST of INTEGERS, IDs of the stations corresponding to the visited nodes
            - idsOptimalPath: LIST of INTEGERS, IDs of the stations corresponding to the optimal path
            (from origin to destination)
            - min_distance_origin: REAL the distance of the origin_coordinates to the closest station
            - min_distance_destination: REAL the distance of the destination_coordinates to the closest station
            


            EXAMPLE:
            return optimalPath.time, optimalPath.walk, optimalPath.transfers,optimalPath.num_stopStation,
            len(expandedList), len(idsOptimalPath), visitedNodes, idsOptimalPath, min_distance_origin,
            min_distance_destination
    """




