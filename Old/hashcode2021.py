<<<<<<< HEAD:Old/hashcode2021.py
#lecture des entrées
fichier = open ("a.txt", "r")
ligne = fichier.readline()
# tmp=input().split(' ') # version juge
tmp=ligne.split(' ')
duration=int(tmp[0])
nb_intersections=int(tmp[1])
nb_streets=int(tmp[2])
nb_cars=int(tmp[3])
bonus=int(tmp[4])
lignes = fichier.readlines()
# dictionnaire des rues de la forme { nom : [départ, arrivée, longueur]}
rues={}
for i in range(nb_streets):
    # temp=input().split() # version juge
    temp=lignes[i].split()
    start=int(temp[0])
    end=int(temp[1])
    name=temp[2]
    length=int(temp[3])
    rues[name]=[start,end,length]
print(rues)
# dictionnaire des voitures de la forme {id :[longueur trajet, [rue1, rue2, ...]]}
voitures={}
for i in range(nb_cars):
    temp=lignes[nb_streets+i].split()
    # temp=input().split(' ') # version juge
    path_length=int(temp[0])
    path=[]
    for j in range(path_length):
        path.append(temp[1+j])
    voitures[i]=[path_length,path]
print(voitures)

# Classe pour les carrefours
class Intersection():
    def __init__(self, id):
        self.id=id # numéro unique de l'intersection
        self.incoming_streets={} # dictionnaire des rues entrantes de la forme {'nom de la rue' : trafic} où trafic est le nombre de voiture arrivant par cette rue
        self.outgoing_streets={} # dictionnaire des rues sortantes de la forme {'nom de la rue' : trafic} où trafic est le nombre de voiture sortant par cette rue
        self.nb_in=0 # nombre de rues entrantes sur cette intersection
        self.nb_out=0 # nombre de rues sortantes sur cette intersection
        self.always_green=False # devient vrai si une seule rue entrante et une seule sortante
        self.schedule=[] # planning des feux pour toutes les rues entrantes

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
        for i in range(self.nb_in):
            texte=texte+self.schedule[i][0]+' '+str(self.schedule[i][1])+'\n'
        return texte
          
    def add_street_in(self,street): # pour ajouter une rue entrante
        self.incoming_streets[street]=0 # pas de trafic pour le moment
        self.nb_in+=1 # une rue entrante de plus pour cette intersection
        if self.nb_in == 1 : self.schedule.append([street,duration]) # si c'est la première rue entrante, le feu est toujours vert
        else :
            duree=duration//self.nb_in # sinon il sera vert le temps total divisé par le nombre de rues entrantes (à modifier)
            for i in range(self.nb_in-1):
                self.schedule[i][1]=duree # on modifie la durée des rues entrantes précédentes
            self.schedule.append([street,duree]) # on ajoute la nouvelle

    def add_street_out(self,street): # pour ajouter une rue sortante
        self.outgoing_streets[street]=0 # pas de trafic pour le moment
        self.nb_out+=1 # une rue sortante de plus pour cette intersection

    def sens_unique(self): # pour tester à la fin l'intersection est à sens unique (pas vraiment une intersection du coup)
        if self.nb_in == 1 and self.nb_out == 1 : self.always_green=True

    def add_car(self,street): # pour ajouter du trafic à cette intersection
        if street in self.incoming_streets : self.incoming_streets[street]+=1 # si c'est une rue entrante
        if street in self.outgoing_streets : self.outgoing_streets[street]+=1 # si c'est une rue sortante

# Construction des intersections
carrefours={}
for i in range(nb_intersections):
    carrefours[i]=Intersection(i) # on construit autant d'intersections vides que nécessaires
for rue, parametres in rues.items() : # on parcourt les rues pour remplir les rues des intersections
    carrefours[parametres[1]].add_street_in(rue)  # ajout d'une rue entrante
    carrefours[parametres[0]].add_street_out(rue) # ajout d'une rue sortante

for voiture in voitures.values() : # on parcourt les voitures pour remplir le trafic des intersections
    i=0
    for rue in voiture[1]: # on parcourt voiture[1] aui est la liste des noms de rue parcourues par cette voiture
        start_inter=rues[rue][0] # identifiant de l'intersection de départ de cette rue
        end_inter=rues[rue][1] # identifiant de l'intersection d'arrivée de cette rue
        if i == 0 : carrefours[end_inter].add_car(rue) # si c'est la première rue on ajoute que du trafic entrant
        elif i == voiture[0]-1 : carrefours[start_inter].add_car(rue) # si c'est la dernière, on ajoute que du trafic sortant
        else : # sinon on ajoute les deux
            carrefours[end_inter].add_car(rue)
            carrefours[start_inter].add_car(rue)
        i+=1
# on cherche les carrefours à sens unique        
for carrefour in carrefours.values() :
    carrefour.sens_unique()
# on affiche toutes nos intersections
for carrefour in carrefours.values() :
    print(carrefour)

# affichage pour le juge
print(nb_intersections)
for carrefour in carrefours.values() :
	print(carrefour.id)
	print(carrefour.nb_in)
	for feu in carrefour.schedule :
		print(feu[0]+' '+str(feu[1]))
=======
#lecture des entrées
fichier = open ("a.txt", "r")
ligne = fichier.readline()
# tmp=input().split(' ') # version juge
tmp=ligne.split(' ')
duration=int(tmp[0])
nb_intersections=int(tmp[1])
nb_streets=int(tmp[2])
nb_cars=int(tmp[3])
bonus=int(tmp[4])
lignes = fichier.readlines()
# dictionnaire des rues de la forme { nom : [départ, arrivée, longueur]}
rues={}
for i in range(nb_streets):
    # temp=input().split() # version juge
    temp=lignes[i].split()
    start=int(temp[0])
    end=int(temp[1])
    name=temp[2]
    length=int(temp[3])
    rues[name]=[start,end,length]
print(rues)
# dictionnaire des voitures de la forme {id :[longueur trajet, [rue1, rue2, ...]]}
voitures={}
for i in range(nb_cars):
    temp=lignes[nb_streets+i].split()
    # temp=input().split(' ') # version juge
    path_length=int(temp[0])
    path=[]
    for j in range(path_length):
        path.append(temp[1+j])
    voitures[i]=[path_length,path]
print(voitures)

# Classe pour les carrefours
class Intersection():
    def __init__(self, id):
        self.id=id # numéro unique de l'intersection
        self.incoming_streets={} # dictionnaire des rues entrantes de la forme {'nom de la rue' : trafic} où trafic est le nombre de voiture arrivant par cette rue
        self.outgoing_streets={} # dictionnaire des rues sortantes de la forme {'nom de la rue' : trafic} où trafic est le nombre de voiture sortant par cette rue
        self.nb_in=0 # nombre de rues entrantes sur cette intersection
        self.nb_out=0 # nombre de rues sortantes sur cette intersection
        self.always_green=False # devient vrai si une seule rue entrante et une seule sortante
        self.schedule=[] # planning des feux pour toutes les rues entrantes

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
        for i in range(self.nb_in):
            texte=texte+self.schedule[i][0]+' '+str(self.schedule[i][1])+'\n'
        return texte
          
    def add_street_in(self,street): # pour ajouter une rue entrante
        self.incoming_streets[street]=0 # pas de trafic pour le moment
        self.nb_in+=1 # une rue entrante de plus pour cette intersection
        if self.nb_in == 1 : self.schedule.append([street,duration]) # si c'est la première rue entrante, le feu est toujours vert
        else :
            duree=duration//self.nb_in # sinon il sera vert le temps total divisé par le nombre de rues entrantes (à modifier)
            for i in range(self.nb_in-1):
                self.schedule[i][1]=duree # on modifie la durée des rues entrantes précédentes
            self.schedule.append([street,duree]) # on ajoute la nouvelle

    def add_street_out(self,street): # pour ajouter une rue sortante
        self.outgoing_streets[street]=0 # pas de trafic pour le moment
        self.nb_out+=1 # une rue sortante de plus pour cette intersection

    def sens_unique(self): # pour tester à la fin l'intersection est à sens unique (pas vraiment une intersection du coup)
        if self.nb_in == 1 and self.nb_out == 1 : self.always_green=True

    def add_car(self,street): # pour ajouter du trafic à cette intersection
        if street in self.incoming_streets : self.incoming_streets[street]+=1 # si c'est une rue entrante
        if street in self.outgoing_streets : self.outgoing_streets[street]+=1 # si c'est une rue sortante

# Construction des intersections
carrefours={}
for i in range(nb_intersections):
    carrefours[i]=Intersection(i) # on construit autant d'intersections vides que nécessaires
for rue, parametres in rues.items() : # on parcourt les rues pour remplir les rues des intersections
    carrefours[parametres[1]].add_street_in(rue)  # ajout d'une rue entrante
    carrefours[parametres[0]].add_street_out(rue) # ajout d'une rue sortante

for voiture in voitures.values() : # on parcourt les voitures pour remplir le trafic des intersections
    i=0
    for rue in voiture[1]: # on parcourt voiture[1] aui est la liste des noms de rue parcourues par cette voiture
        start_inter=rues[rue][0] # identifiant de l'intersection de départ de cette rue
        end_inter=rues[rue][1] # identifiant de l'intersection d'arrivée de cette rue
        if i == 0 : carrefours[end_inter].add_car(rue) # si c'est la première rue on ajoute que du trafic entrant
        elif i == voiture[0]-1 : carrefours[start_inter].add_car(rue) # si c'est la dernière, on ajoute que du trafic sortant
        else : # sinon on ajoute les deux
            carrefours[end_inter].add_car(rue)
            carrefours[start_inter].add_car(rue)
        i+=1
	

	
# on cherche les carrefours à sens unique        
for carrefour in carrefours.values() :
    carrefour.sens_unique()
# on affiche toutes nos intersections
for carrefour in carrefours.values() :
    print(carrefour)


# Reglage d'une intersection
def Reglageintersection(id):    
    Nbintersection= carrefours[id].nb_in# nombre d'intersection dans le carrefour    
    trafic=[Nbintersection] # tableau des qtés de circulation
    cpt=0
    for rue,traf in carrefours[id].incoming_streets.items():
        trafic.append(traf) #on remplit le tableau avec la qté de voitures
        cpt=cpt+traf #on compte toutes les voitures
    #Le réglage
    limitant=min(trafic)
    for i in range(len(trafic)):
        trafic[i]=trafic[i]//limitant #on ramène à 1 s le plus petit feu
    #change la valeur
    for i in range(len(carrefours[id].schedule)):
        carrefours[id].schedule[i][1]=trafic[i]
    


# affichage pour le juge
print(nb_intersections)
for carrefour in carrefours.values() :
	print(carrefour.id)
	print(carrefour.nb_in)
	for feu in carrefour.schedule :
		print(feu[0]+' '+str(feu[1]))
>>>>>>> 78d2868bee8bb21a7bccdb75d971c8762d42aa49:hashcode2021.py
