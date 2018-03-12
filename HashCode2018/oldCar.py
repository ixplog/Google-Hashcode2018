import ride
import math as mt

class car(object):
    def __init__(self, goal, posit_x, posit_y, C):
        # rideToGo: descrive l'obiettivo della macchina, stabilisce cioe' verso quale ride la macchina si sta dirigendo
        # e' un oggetto "ride"
        # se e' "None" la macchina non ha un obiettivo
        self.rideToGo = goal

        # status dice se la macchina sta facendo la ride rappresentata da rideToGo oppure no
        # dice anche se ha appena completato la ride che stava facendo
        # e' un tipo di dato "status"
        self.status = status()

        self.x = posit_x
        self.y = posit_y

        # rappresenta una variabile che mi dice quanto la macchina sceglie a caso dove andare
        self.C = C

    # muove la macchina nella direzione del suo obiettivo; 
    # due possibilita': la macchina e' gia' dentro la ride che vuole fare -> muovo la macchina dentro la ride
    # oppure la macchina vuole andare a prendere una ride -> muovo la macchina verso il punto di partenza della ride
    # restituisco False se, nonostante la chiamata a questa funzione, non c'e' stato movimento
    def move_car(self):
        if self.status.completingRide == True:
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
                    # ho gia' completato la ride, qualcosa e' andato storto
                    self.status.completedRide = True
                    return False
            return True
        elif self.status.goingToRide == True:
            # la macchina non sta facendo alcuna ride, ma sta andando verso un obiettivo
            if self.rideToGo == None:
                # non c'e' obiettivo, qualcosa e' andato storto
               return False
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
                       # la macchina e' gia' dove vuole andare, la lascio li'
                       self.status.completingRide = True
                       return False
               return True

    def greedy_cost(self, raid, t):
        space = mt.fabs(self.x - raid.a) + mt.fabs(self.y - raid.b)
        if t + space + raid.get_price_time() > raid.s and t + space + raid.get_price_time() > T:
            return mt.inf
        else:
            if raid.s - t > 0:
                return space + raid.s - t
            else:
                return space


class status:
    def __init__(self):
        self.__goingToRide = True
        self.__completingRide = False
        self.__completedRide = False

    # getters and setters
    @property
    def goingToRide(self):
        return self.__goingToRide

    @property
    def completingRide(self):
        return self.__completingRide

    @property
    def completedRide(self):
        return self.__completedRide

    @goingToRide.setter
    def goingToRide(self, goingToRide):
        if goingToRide == True:
            self.__completedRide = False
            self.__completingRide = False
        else:
            if self.__completedRide == False and self.__completingRide == False:
                raise Exception("Status has to have one True value")

    @completedRide.setter
    def completedRide(self, completedRide):
        if completedRide == True:
            self.__goingToRide = False
            self.__completingRide = False
        else:
            if self.__goingToRide == False and self.__completingRide == False:
                raise Exception("Status has to have one True value")

    @completingRide.setter
    def completingRide(self, completingRide):
        if completingRide == True:
            self.__goingToRide = False
            self.__completedRide = False
        else:
            if self.__completedRide == False and self.__goingToRide == False:
                raise Exception("Status has to have one True value")

