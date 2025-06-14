def problema1():
    print("La meitat del doble de 12, més 8, dividit per 4.")
    resposta = input("Resposta: ")
    if resposta == "5":
        print("Molt bè, ho has aconseguit!")
        print("Passes a la següent sala")
    else:
        while(resposta != "5"):
            print("Torna a intentar!")
            print("La meitat del doble de 12, més 8, dividit per 4.")
            resposta = input("Resposta: ")
        print("Molt Bé")
        print("Passes a la següent sala")


import random

def problema2():
    print("En aquesta segona sala hauràs de descobrir quina és la paraula amagada")
    pistes = [
        "Comença amb la lletra 'o'.",
        "Té la lletra 'b' al mig.",
        "Acaba amb la lletra 'a'.",
        "Es relaciona amb la llum i la foscor.",    
    ]
    pista = random.choice(pistes)
    print("Sóc una paraula de 5 lletres.")
    print("Si treus la primera lletra, encara so com abans.")
    print("Si treus la segona lletra, també.")
    print("Fins i tot si només queda una lletra, la paraula segueix sent la mateixa.")
    print("Quina paraula sóc?")
    resposta = input("Resposta: ")
    if resposta in ["ombra","Ombra","OMBRA"]:
        print("Molt bé, a la primera!")
        print("Passes a la següent sala")
    else:
        while resposta not in ["ombra","Ombra","OMBRA"]:
            if len(pistes) > 0:
                pista = random.choice(pistes)
                print("Pista:", pista)
                pistes.remove(pista)
                resposta = input("Resposta: ")
            else:
                print("No hi ha més pistes disponibles")
                resposta = input("Resposta: ")
        print("Molt bé, passes a la següent sala!")
