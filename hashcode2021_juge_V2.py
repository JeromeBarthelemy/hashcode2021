from collections import defaultdict

juge=True # mettre à True pour utilisation avec le juge et à False sinon

#lecture des entrées
if juge : tmp=input().split(' ')
else :
    fichier = open ("b.txt", "r")
    ligne = fichier.readline()
    tmp=ligne.split(' ')

duration=int(tmp[0])
nb_intersections=int(tmp[1])
nb_streets=int(tmp[2])
nb_cars=int(tmp[3])
bonus=int(tmp[4])
if not(juge) : lignes = fichier.readlines()

# dictionnaire des rues de la forme { nom : [départ, arrivée, longueur]}
rues={}
for i in range(nb_streets):
    if juge : temp=input().split(' ')
    else : temp=lignes[i].split()
    start=int(temp[0])
    end=int(temp[1])
    name=temp[2]
    length=int(temp[3])
    rues[name]=[start,end,length]
#if not(juge) : print(rues)

# liste des voitures de la forme [[longueur trajet, [rue1, rue2, ...]]]
# NB : on utilise pas un dictionnaire afin que l'ordre d'entrée des voitures soit conservé
voitures=[]
for i in range(nb_cars):
    if juge : temp=input().split(' ')
    else : temp=lignes[nb_streets+i].split()
    path_length=int(temp[0])
    path=[]
    for j in range(path_length):
        path.append(temp[1+j])
    voitures.append([path_length,path])
#if not(juge) : print(voitures)

# Classe pour les carrefours
class Intersection():
    def __init__(self, id):
        self.id=id # numéro unique de l'intersection
        self.incoming_streets={} # dictionnaire des rues entrantes de la forme {'nom de la rue' : [trafic total, longueur de la rue, queue initiale]} où trafic est le nombre de voiture arrivant par cette rue pendant toute la simulation, et queue initiale est le nombre de voitures démarrant dans cette rue au départ de la simulation
        self.outgoing_streets={} # dictionnaire des rues sortantes de la forme {'nom de la rue' : trafic} où trafic est le nombre de voiture sortant par cette rue
        self.nb_in=0 # nombre de rues entrantes sur cette intersection
        self.nb_out=0 # nombre de rues sortantes sur cette intersection
        self.always_green=False # devient vrai si une seule rue entrante et une seule sortante
        self.schedule=[] # planning des feux pour toutes les rues entrantes
        self.priority=[] # à chaque fois qu'une voiture démarre sur une rue entrante de cette intersection, on l'ajoute ici

    def __str__(self): # pour imprimer proprement une intersection
        texte='Intersection ID : '+str(self.id)+'\n'
        texte=texte+'Rues entrantes, trafic : \n'
        for rue,traf in self.incoming_streets.items():
            texte=texte+rue+', '+str(traf)+'\n'
        texte=texte+'Rues sortantes, trafic : \n'
        for rue,traf in self.outgoing_streets.items():
            texte=texte+rue+', '+str(traf)+'\n'
        texte=texte+'1 seul feu toujours vert ? ' +str(self.always_green)+'\n'
        texte=texte+'Schedule :\n'
        for i in range(len(self.schedule)):
            texte=texte+self.schedule[i][0]+' '+str(self.schedule[i][1])+'\n'
        return texte
          
    def add_street_in(self,street,parametres): # pour ajouter une rue entrante
        self.incoming_streets[street]=[0,parametres[2],0] # pas de trafic, ni de queues pour le moment mais on initialise la longueur de la rue
        self.nb_in+=1 # une rue entrante de plus pour cette intersection
        if self.nb_in == 1 : self.schedule.append([street,duration]) # si c'est la première rue entrante, le feu est toujours vert
        else :
            #duree=duration//self.nb_in # sinon il sera vert le temps total divisé par le nombre de rues entrantes (à modifier)
            duree=1
            for i in range(self.nb_in-1):
                self.schedule[i][1]=duree # on modifie la durée des rues entrantes précédentes
            self.schedule.append([street,duree]) # on ajoute la nouvelle

    def add_street_out(self,street,parametres): # pour ajouter une rue sortante
        self.outgoing_streets[street]=[0,parametres[2],0] # pas de trafic, ni de queues pour le moment mais on initialise la longueur de la rue
        self.nb_out+=1 # une rue sortante de plus pour cette intersection

    def sens_unique(self): # pour tester à la fin l'intersection est à sens unique (pas vraiment une intersection du coup) ou si des voitures arrivent par une seule route
        #if self.nb_in == 1 : self.always_green=True
        if len(self.schedule) == 1 : # on regarde le nombre de feux plannifiés, s'il n'y en a qu'un c'est que les voitures n'arrivent que par celui-là
            self.always_green=True
            self.schedule [0][1]=duration # on met le feu au vert tout le temps

    def add_car(self,street,initial): # pour ajouter du trafic à cette intersection
        if street in self.incoming_streets : # si c'est une rue entrante
            if initial :
                self.incoming_streets[street][2]+=1 # si c'est la rue de départ, on incrémente la queue initiale
                if not(street in self.priority) : self.priority.append(street) # si la rue n'apparait pas encore dans les rues prioritaires, on l'ajoute
            self.incoming_streets[street][0]+=1 # une rue entrante de plus
        if street in self.outgoing_streets : self.outgoing_streets[street][0]+=1 # si c'est une rue sortante

    def order(self): # pour ordonner le premier passage au vert en fonction des voitures qui attendent au départ
        if len(self.priority) != 0 : # si il y a des voitures qui démarrent à cette intersection
            if not(juge) : print(self.id,self.priority) # debugage
            self.schedule=priority_sort(self.schedule,self.priority,default_priority=len(self.priority)) # on met en premier dans schedule les rues où une voiture attend pour démarrer
    
    def rue_vide(self): # pour mettre au rouge les rues où jamais aucune voiture ne passe
        rues_vides=[]
        for nom,rue in self.incoming_streets.items(): # on parcourt les rues de cette intersection
            if rue[0] == 0 : rues_vides.append(nom) # on ajoute les rues vides à rues_vide
        i=0
        for feu in self.schedule : # on parcourt les feux de cette intersection
            if feu[0] in rues_vides :
                del self.schedule[i] # on élimine de schedule les rues vides
                self.nb_in-=1 # on met à jour le nombre de feux actifs pour cette intersection
            i+=1
        if len(self.schedule) == 0 : return True #on renvoie True si plus aucune voiture ne passe par cette intersection

def priority_sort(to_sort, order, default_priority=-1): # renvoie la liste to_sort triée selon la liste order. defauls_priority permet de traiter les éléments de to_sort qui ne sont pas dans order
    priorities = defaultdict(lambda: default_priority, {e:p for p, e in enumerate(order)})
    return sorted(to_sort, key=lambda e: priorities[e[0]])

# Construction des intersections
carrefours={}
for i in range(nb_intersections):
    carrefours[i]=Intersection(i) # on construit autant d'intersections vides que nécessaires
for rue, parametres in rues.items() : # on parcourt les rues pour remplir les rues des intersections
    carrefours[parametres[1]].add_street_in(rue,parametres)  # ajout d'une rue entrante
    carrefours[parametres[0]].add_street_out(rue,parametres) # ajout d'une rue sortante

for voiture in voitures : # on parcourt les voitures pour remplir le trafic des intersections
    i=0
    for rue in voiture[1]: # on parcourt voiture[1] aui est la liste des noms de rue parcourues par cette voiture
        start_inter=rues[rue][0] # identifiant de l'intersection de départ de cette rue
        end_inter=rues[rue][1] # identifiant de l'intersection d'arrivée de cette rue
        if i == 0 : carrefours[end_inter].add_car(rue, initial=True) # si c'est la première rue on ajoute que du trafic entrant
        # A priori, il y a un bug dans le juge. Normalement, il n'y a pas besoin de passer au vert le feu au bout de la dernière rue ou s'arrête une voiture.
        # Mais si on fait ça, ça marche pas. Dans le jeu a, par exemple, le juge veut que le feu de la rue de Rome à l'intersection 3 soit vert pour laisser sortir la voiture orange.
        #elif i == voiture[0]-1 : carrefours[start_inter].add_car(rue, initial=False) # si c'est la dernière, on ajoute que du trafic sortant
        else : # sinon on ajoute les deux
            carrefours[end_inter].add_car(rue, initial=False)
            carrefours[start_inter].add_car(rue, initial=False)
        i+=1

# on cherche les carrefours à sens unique        
for carrefour in carrefours.values() :
    if carrefour.rue_vide() : nb_intersections-=1 # on commence par éliminer les feux inactifs placés sur des rues sans voitures
    carrefour.sens_unique() # on met au vert les feux des carrefours où les voitures n'arrivent que par une seule rue
            
def Reglageintersection(id):    
    Nbintersection= carrefours[id].nb_in# nombre d'intersection dans le carrefour    
    trafic=[] # tableau des qtés de circulation
    cpt=0
    for rue,traf in carrefours[id].incoming_streets.items():
        trafic.append(traf[0]) #on remplit le tableau avec la qté de voitures
        cpt=cpt+traf[0] #on compte toutes les voitures
    #Le réglage
    limitant=min(trafic)
    if limitant != 0 :
        for i in range(Nbintersection):
            carrefours[id].schedule[i][1]=trafic[i]//limitant #on ramène à 1 s le plus petit feu

# on modifie le schedule des carrefours en fonction du trafic       
for carrefour in carrefours.values() :
    if not(carrefour.always_green) :
        #Reglageintersection(carrefour.id) # pas utilisé car dégrade le score
        carrefour.order()


# on affiche toutes nos intersections dans la console
if not(juge) :
    for carrefour in carrefours.values() :
        if len(carrefour.schedule) != 0 :
            print('Carrefour n°', carrefour.id,' Nb rues entrantes : ',carrefour.nb_in,' Nb rues sortantes : ', carrefour.nb_out, ' Nb de rues de ce carrefour occupées au départ : ', len(carrefour.priority))
            #print(carrefour)
# on affiche toutes nos intersections pour le juge
else :
    print(nb_intersections)
    for carrefour in carrefours.values() :
        if len(carrefour.schedule) != 0 :
            print(carrefour.id)
            print(carrefour.nb_in)
            for feu in carrefour.schedule :
                print(feu[0]+' '+str(feu[1]))
