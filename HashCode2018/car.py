import ride
import math as mt
import numpy as np
import random as rd
from enum import Enum

class status(Enum):
    goingToRide = 0 # significa che la macchine non ha raggiunto il punto di inizio di una ride
    completingRide = 1 # significa che la macchina ha raggiunto il punto di inizio di una ride ED è passato il tempo minimo di start della ride
    completedRide = 2 # significa che la macchina è arrivata al punto finale della ride che voleva completare


class car(object):
    def __init__(self, id, goal, posit_x, posit_y, C):
        self.id = id

        # rideToGo: descrive l'obiettivo della macchina, stabilisce cioe' verso quale ride la macchina si sta dirigendo
        # e' un oggetto "ride"
        # se e' "None" la macchina non ha un obiettivo
        self.rideToGo = goal

        self.completedRides = []

        # status dice se la macchina sta facendo la ride rappresentata da rideToGo oppure no
        # dice anche se ha appena completato la ride che stava facendo
        # e' un tipo di dato "status"
        self.status = status.goingToRide # questa variabile non viene mai modificata dentro la classe

        self.x = posit_x
        self.y = posit_y

        # rappresenta una variabile che mi dice quanto la macchina sceglie a caso dove andare
        self.C = C

    # muove la macchina nella direzione del suo obiettivo; 
    # due possibilita': la macchina e' gia' dentro la ride che vuole fare -> muovo la macchina dentro la ride
    # oppure la macchina vuole andare a prendere una ride -> muovo la macchina verso il punto di partenza della ride
    # restituisco False se, nonostante la chiamata a questa funzione, non c'e' stato movimento
    def move_car(self):

        if self.status == status.completedRide:
            raise Exception("Non puoi muovere una macchina nello stato 'completedRide'")
        
        if self.status == status.goingToRide:
            # la macchina non sta facendo alcuna ride, ma sta andando verso un obiettivo
            if self.rideToGo == None:
                # non c'e' obiettivo, qualcosa e' andato storto
               raise Exception("Non puoi muovere una macchine nello stato 'goingToRide' che non ha obiettivo")
            else:
               if self.rideToGo.a > self.x:
                   self.x += 1
               elif self.rideToGo.a < self.x:
                   self.x -= 1
               elif self.rideToGo.a == self.x:
                   if self.rideToGo.b > self.y:
                       self.y += 1
                   elif self.rideToGo.b < self.y:
                       self.y -= 1
                   elif self.rideToGo.b == self.y:
                       # la macchina è già dove vuole andare, la lascio lì
                       return False
               return True
        
        if self.status == status.completingRide:
            # la macchina sta facendo una ride, vuole completarla
            if self.rideToGo.x > self.x:
                self.x += 1
            elif self.rideToGo.x < self.x:
                self.x -= 1
            else:
                if self.rideToGo.y > self.y:
                    self.y += 1
                elif self.rideToGo.y < self.y:
                    self.y -= 1
                else:
                    # ho gia' completato la ride
                    raise Exception("La macchina ha completato la ride ma il suo status è 'completingRide'")
            return True

    def greedy_cost(self, ride, t, T, bonus):
        space = mt.fabs(self.x - ride.a) + mt.fabs(self.y - ride.b)
        if t + space + ride.get_price_time() > ride.f:
            return mt.inf
        else:
            if ride.s - t - space >= 0:
                return ride.s - t - bonus # = space + raid.s - t - space
            else:
                return space

    # FUNZIONE choose_ride: seleziona la prossima ride assegnando ad ognuna una probabilità
    # quando arrivo vicino al tempo limite T, le probabilità diventano tutte nulle
    # in quel caso la funzione restituisce None
    # la macchina non ha nessuna ride da scegliere
    def choose_ride(self, ridesToDo, t, T, bonus):
        probabilities = np.zeros(len(ridesToDo))

        scaling = 0
        index_max = 0
        for index in range(len(ridesToDo)):
            cost = self.greedy_cost(ridesToDo[index], t, T, bonus)
            if cost == mt.inf:
                probabilities[index] = 0
            else:
                probabilities[index] = np.exp( - (1 / self.C) * self.greedy_cost(ridesToDo[index], t, T, bonus) )
                scaling += probabilities[index]

        if not scaling == 0:
            probabilities = probabilities / scaling
        else:
            return None

        # Draw from distribution probabilites
        draw = rd.uniform(0, 1)
        sum = 0
        for i in range(len(probabilities)):
            if sum <= draw and draw < sum + probabilities[i]:
                return ridesToDo[i]
            sum += probabilities[i]
        return None