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



