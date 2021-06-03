class Car():
    def __init__(self,id,path,long,feux):
        self.id = id
        self.path = path
        self.path_length = long
        self.etape = 0
        self.street_curr = path[0]
        self.dist_feu = 0
        self.queue = True
        self.queue_pos = feux[self.street_curr].queue_length + 1
        feux[self.street_curr].queue_length += 1
        feux[self.street_curr].queue.append(self)

    def __str__(self):
        texte='Voiture n°'+str(self.id)+' dans la '+self.street_curr+' à '+str(self.dist_feu)+' du feu'
        return texte

    def avance(self,feux,rues,cars):
        if self.dist_feu > 0 : # si pas au feu, la voiture avance
            self.dist_feu -= 1
            if self.dist_feu == 0 : # si elle arrive à un feu
                if self.etape == self.path_length-1 : # si on est au bout de la dernière rue, elle est arrivée
                    cars.remove(self)
                    return 'Avance et arrivée'
                else : # sinon la met en queue
                    self.queue=True
                    self.queue_pos = feux[self.street_curr].queue_length + 1
                    feux[self.street_curr].queue_length += 1
                    feux[self.street_curr].queue.append(self)
                    if self.queue and self.queue_pos == 1 and feux[self.street_curr].green : # si elle est en queue et en 1ere position et que le feu est vert, elle passe le feu mais sans avancer
                        feux[self.street_curr].queue.remove(self)
                        feux[self.street_curr].queue_length -= 1
                        self.etape+=1
                        self.street_curr = self.path[self.etape]
                        self.dist_feu = rues[self.street_curr][2]
                        self.queue=False
                        self.queue_pos = 0
                        return 'Avance et traverse carrefour'
            else : return 'Avance dans la rue'

        if self.queue and self.queue_pos == 1 and feux[self.street_curr].green : # si elle est en queue et en 1ere position et que le feu est vert à présent, elle passe le feu et avance
            feux[self.street_curr].queue.remove(self)
            feux[self.street_curr].queue_length -= 1
            self.etape+=1
            self.street_curr = self.path[self.etape]
            self.dist_feu = rues[self.street_curr][2]-1
            if self.dist_feu == 0 :  # si elle arrive à un feu
                if self.etape == self.path_length-1 : # si on est au bout de la dernière rue, elle est arrivée
                    cars.remove(self)
                    return 'Traverse et arrivée'
                else : # sinon la met en queue
                    self.queue = True
                    self.queue_pos = feux[self.street_curr].queue_length + 1
                    feux[self.street_curr].queue_length += 1
                    feux[self.street_curr].queue.append(self)
                    if self.queue and self.queue_pos == 1 and feux[self.street_curr].green : # si elle est en queue et en 1ere position et que le feu est vert, elle passe le feu mais sans avancer
                        feux[self.street_curr].queue.remove(self)
                        feux[self.street_curr].queue_length -= 1
                        self.etape+=1
                        self.street_curr = self.path[self.etape]
                        self.dist_feu = rues[self.street_curr][2]
                        self.queue=False
                        self.queue_pos = 0
                        return 'Traverse, avance et traverse carrefour'
            else : return 'Traverse et avance'                 
        if self.queue and self.queue_pos != 1 and feux[self.street_curr].green : #le feu est vert mais il y a du monde devant, elle avance seulement dans la queue
            self.queue_pos -= 1
            return 'Avance dans la queue'
        return 'Bloquée au feu'

class Feu():
    def __init__(self, street_name,duree_green,carrefour_id,green,duration):
        self.id = street_name
        self.queue = []
        self.queue_length = 0
        self.green = green
        self.duree_green = duree_green
        self.duree_red = duration
        self.temps = 0
        self.carrefour_id=carrefour_id

    def __str__(self):
        texte = 'Feu '+self.id + ' Queue de '+str(self.queue_length)+' voitures : Vert = '+str(self.green)+' Durée du vert= '+str(self.duree_green)+' Durée du rouge= '+str(self.duree_red)+'\n'
        for voiture in self.queue :
            texte = texte + voiture.__str__()+'\n'
        return texte

    def iteration_temps(self):
        if self.duree_green != 0 :
            self.temps += 1
            if self.green :
                if self.temps == self.duree_green :
                    self.green=not(self.green)
                    self.temps = 0
            else :
                if self.temps == self.duree_red :
                    self.green=not(self.green)
                    self.temps = 0

def score(rues,voitures,carrefours,duration,bonus,juge):
    """
    rues est un dictionnaire des rues de la forme { nom : [départ, arrivée, longueur]}
    voitures est une liste de la forme [[longueur trajet, [rue1, rue2, ...]]]
    carrefours est un dictionnaire dont les clés sont les id des intersection et les valeurs des objets de la classe Intersection avec les attributs suivants :
    self.id=id # numéro unique de l'intersection
    self.incoming_streets={} # dictionnaire des rues entrantes de la forme {'nom de la rue' : [trafic total, longueur de la rue, queue initiale]} où trafic est le nombre de voiture arrivant par cette rue pendant toute la simulation, et queue initiale est le nombre de voitures démarrant dans cette rue au départ de la simulation
    self.outgoing_streets={} # dictionnaire des rues sortantes de la forme {'nom de la rue' : trafic} où trafic est le nombre de voiture sortant par cette rue
    self.nb_in=0 # nombre de rues entrantes sur cette intersection
    self.nb_out=0 # nombre de rues sortantes sur cette intersection
    self.always_green=False # devient vrai si une seule rue entrante et une seule sortante
    self.schedule=[] # planning des feux pour toutes les rues entrantes
    self.priority=[] # à chaque fois qu'une voiture démarre sur une rue entrante de cette intersection, on l'ajoute ici
    """
    score = 0

    feux={}

    for id,carrefour in carrefours.items() :
        for nom in carrefour.incoming_streets :
            feux[nom]=Feu(nom,0,id,False,duration) # on met tous les feux au rouge fixe
        schedule = carrefour.schedule
        if len(schedule) != 0 : # on modifie ceux qui sont schedulés
            i=0
            duree_red=0
            for ligne in schedule :
                duree_red += ligne[1]
                if i == 0 : green = True
                else : green = False
                feux[ligne[0]].green = green
                feux[ligne[0]].duree_green = ligne[1]
                i += 1
            for ligne in schedule :
                feux[ligne[0]].duree_red = duree_red - feux[ligne[0]].duree_green

    cars=[]
    i=0
    for voiture in voitures :
        cars.append(Car(i,voiture[1],voiture[0],feux))
        i += 1
    """if not(juge):
        print("Feux :")
        for feu in feux.values() : print(feu)
        print("Voitures :")
        for car in cars : print(car)"""
    nb_bloques = 0
    nb_queues = 0
    for t in range(duration) : # t est le temps
        """if not(juge):
            print ('Itération n°',t)
            print("Etat des voitures : ")
            for car in cars :
                print(car)
            print("Etat des feux : ")
            for feu in feux.values() :
                print(feu)"""
        for car in cars :
            result=car.avance(feux,rues,cars)
            # print('Action de la voiture '+str(car.id)+' : ', result)
            if result == 'Traverse et arrivée' or result == 'Avance et arrivée' :
                score += bonus + (duration - (t+1))
            if result == 'Bloquée au feu' : nb_bloques += 1
            if result == 'Avance dans la queue' : nb_queues += 1
        for feu in feux.values() :
            feu.iteration_temps()
    if not(juge) : print ('Nb de feux rouges bloquants : ', nb_bloques, ' Nb de secondes passées dans la queue : ', nb_queues)
    return score
