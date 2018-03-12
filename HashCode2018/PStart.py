import numpy as np
import math as mt
import random as rd
from ride import ride
from car import car, status
import sys


#filename = "c_no_hurry.in"
filename = "b_should_be_easy.in"

file = open(filename, "r")

R, C, F, N, B, T = [int(x) for x in file.readline().split(" ")]

# matrix = np.zeros([R,C])


# Crea oggetti car

cars_to_assign = []

for i in range(F):
    macchina = car(i, None, 0, 0, 100)
    cars_to_assign.append(macchina)


# Crea oggetti ride

indexRide = 0
rides = [] # lo costruisco in modo che sia ordinato, cosi' la scelta iniziale delle ride e' facile

for line in file:
    a, b, x, y, s, f = [int(x) for x in line.split(" ")]
    raid = ride(indexRide, a, b, x, y, s, f)

    costo = cars_to_assign[0].greedy_cost(raid, 0, T, B) # al tempo 0, visto che le macchine partono dalla stessa posizione, il costo e' lo stesso per tutte le macchine
    
    if len(rides) == 0:
        rides.append(raid)
    else:
        j = 0
        
        while j < len(rides):
            costo_j = cars_to_assign[0].greedy_cost(rides[j], 0, T, B)
            if costo < costo_j:
                # swap
                tmp = rides[j]
                rides[j] = raid
                raid = tmp
                costo = costo_j
            j += 1
            
        if j == len(rides):
            rides.append(raid)
    
    indexRide += 1
    
assert(indexRide == N)

file.close()

##################################################################

fileToWriteName = "results.txt"

fileToWrite = open(fileToWriteName, "w")

# rides_car_dict deve essere un dizionario
# le keys del dizionario sono le corse che devono ancora essere fatte
# ad ogni key è associata una macchina che vuole fare quella corsa (o l'oggetto None)
def simulate(t, cars_on_ride, cars_to_assign, rides_car_dict):

    ridesAvailable = list(rides_car_dict.keys())
    
    print("Assigning rides", end="")

    index = 0
    while index < len(cars_to_assign):
        ridesAvailableHere = ridesAvailable.copy()

        foundRide = False
        while not foundRide:
            print(".", end="")
            sys.stdout.flush()

            car = cars_to_assign[index]
            rideChosen = car.choose_ride(ridesAvailableHere, t, T, B)

            if rideChosen == None:
                #car_completed.append(car)
                cars_to_assign.remove(cars_to_assign[index])
                break

            if rides_car_dict[rideChosen] == None:
                rides_car_dict[rideChosen] = car
                car.rideToGo = rideChosen
                car.status = status.goingToRide
                foundRide = True
                index += 1
            else:
                # conflict among cars
                if rides_car_dict[rideChosen].greedy_cost(rideChosen, t, T, B) > car.greedy_cost(rideChosen, t, T, B):
                    # swap
                    temp = rides_car_dict[rideChosen]
                    car.rideToGo = rideChosen
                    car.status = status.goingToRide
                    rides_car_dict[rideChosen] = car
                    cars_to_assign[index] = temp
                    ridesAvailableHere = ridesAvailable.copy()
                    # smaltire la lista dele ride available
                else:
                    ridesAvailableHere.remove(rideChosen)

    cars_to_assign = []

    temp_to_remove = []
    for car in cars_on_ride:
        assert(car.status == status.completingRide)
        car.move_car()
        if car.x == car.rideToGo.x and car.y == car.rideToGo.y:
            car.status = status.completedRide
            car.completedRides.append(car.rideToGo)
            car.rideToGo = None
            temp_to_remove.append(car) # to avoid duplicating cars_on_ride
            cars_to_assign.append(car)
    for car in temp_to_remove:
        cars_on_ride.remove(car)
                      
    # move other cars
    # if a car reaches the beginning of a ride -> update car properties & rides_car_dict.pop(car.rideToGo)

    for ride, car in rides_car_dict.copy().items():
        if not car == None:
            car.rideToGo = ride
            car.status = status.goingToRide
            car.move_car()
            if car.x == car.rideToGo.a and car.y == car.rideToGo.b:
                print("\nCar " + str(car.id) + " takes ride " + str((car.rideToGo.a, car.rideToGo.b)) + "->" + str((car.rideToGo.x, car.rideToGo.y)))
                fileToWrite.write(str(car.id) + ", " + str(ride.id) + "\n")
                cars_on_ride.append(car)
                car.status = status.completingRide
                rides_car_dict.pop(ride)

    return cars_on_ride, cars_to_assign, rides_car_dict


##################################################################
print("Time 0")
rides_car_dict = {}
#car_completed = []
index_car = 0
for ride in rides: # verificare che Python prende le ride partendo da quella di indice 0, andando a quella di indice 1 e cosi' via
    if index_car < len(cars_to_assign):
        rides_car_dict[ride] = cars_to_assign[index_car]
        index_car += 1
    else:
        rides_car_dict[ride] = None
print(rides_car_dict)
cars_on_ride, cars_to_assign, rides_car_dict = simulate(0, [], [], rides_car_dict)

for i in range(1, T):
    print("\nTime " + str(i))
    cars_on_ride, cars_to_assign, rides_car_dict = simulate(i, cars_on_ride, cars_to_assign, rides_car_dict)

print("\n\nRIDES STILL TO ASSIGN: " + str( len( list(rides_car_dict.keys()) ) ) + "\n")

#cars_remained = 0
#for ride, car in rides_car_dict.items():
#    if not car == None:
#        cars_remained += 1
#assert(len(cars_on_ride) + len(cars_to_assign) + len(car_completed) + cars_remained == F)