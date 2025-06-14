import requests
import os
import json
import time
import threading
import random

NOM_FITXER = "jugador.json"
POST_URL = "https://fun.codelearn.cat/hackathon/game/store_progress"

enviant_progres = False
score = 0


def actualitzar_puntuacio():
    if os.path.exists(NOM_FITXER):
        with open(NOM_FITXER, "r") as f:
            dades = json.load(f)
        dades["punts"] = score
        with open(NOM_FITXER, "w") as f:
            json.dump(dades, f)


def mostrar_menu():
    print("\n   SCAPE ROOM")
    print("\n MENÚ PRINCIPAL")
    print("1. Nova partida")
    print("2. Sortir")

    opcio = input("Selecciona una opció (1-2): ")
    return opcio


def problema1():
    global score
    print("""
          Mires a el teu voltant.
          Les parets són de fusta i, just al teu davant hi ha una pissarra amb operacions matemàtiques i un problema:
          Quin és el resultat de fer la meitat del doble de 12, més 8, dividit per 4?""")
    resposta = input("Resposta: ")
    if resposta == "5":
        print("Molt bé, ho has aconseguit!")
        score += 3
    else:
        while resposta != "5":
            print("Torna a intentar!")
            resposta = input("Resposta: ")
        print("Molt Bé")
        score += 1
    print("Passes a la següent sala")
    actualitzar_puntuacio()


def problema2():
    global score
    print("En aquesta segona sala hauràs de descobrir quina és la paraula amagada")
    pistes = [
        "Comença amb la lletra 'o'.",
        "Té la lletra 'b' al mig.",
        "Acaba amb la lletra 'a'.",
        "Es relaciona amb la llum i la foscor.",
    ]
    print("""
    Sóc una paraula de 5 lletres.
    Si treus la primera lletra, encara sona com abans.
    Si treus la segona lletra, també.
    Fins i tot si només queda una lletra, la paraula segueix sent la mateixa.
    Quina paraula sóc?""")

    resposta = input("Resposta: ")
    intents = 1
    while resposta.lower() != "ombra":
        if len(pistes) > 0:
            pista = random.choice(pistes)
            print("Pista:", pista)
            pistes.remove(pista)
        else:
            print("No es això. No hi ha més pistes disponibles")
        resposta = input("Resposta: ")
        intents += 1

    if intents == 1:
        print("Molt bé, a la primera!")
        score += 3
    else:
        print("Molt bé, passes a la següent sala!")
        score += 1
    actualitzar_puntuacio()


def problema3():
    global score
    print("Heu entrat a la sala d'història")

    resposta = input("Sabeu quin any es va descobrir Amèrica, quin? ")
    intents = 1
    while resposta != "1492":
        print("Torna a intentar!")
        resposta = input("Resposta: ")
        intents += 1
    if intents == 1:
        print("Tu no seràs un expert en història, no?")
        score += 3
    else:
        print("Molt Bé")
        score += 1

    respostaf = input("Quin any va ser la revolució francesa? ")
    intents = 1
    while respostaf != "1789":
        print("Torna a intentar!")
        respostaf = input("Resposta: ")
        intents += 1
    if intents == 1:
        print("Fàcil?")
        score += 3
    else:
        print("Molt Bé")
        score += 1

    print("Ara passaràs a la següent sala")
    actualitzar_puntuacio()


def problema4():
    global score
    print("Quin gas és el més abundant a l’atmosfera terrestre?")
    resposta = input("Resposta: ")
    if resposta.lower() == "nitrogen":
        print("Mare meva que bo!")
        score += 3
    else:
        while resposta.lower() != "nitrogen":
            print("Torna a intentar!")
            resposta = input("Resposta: ")
        print("Molt Bé")
        score += 1

    print("Passes a la última sala")
    actualitzar_puntuacio()


def problema5():
    global score
    print("Quin planeta és conegut com el planeta vermell?")
    resposta = input("Resposta: ")
    if resposta.lower() == "mart":
        print("Super Bé")
        print("Has aconseguit escapar!")
        score += 3
    else:
        while resposta.lower() != "mart":
            print("Torna a intentar!")
            resposta = input("Resposta: ")
        print("Molt Bé")
        print("Has aconseguit escapar!")
        score += 1
    actualitzar_puntuacio()


def enviar_progress(game_id, dades_partida):
    cos = {
        "game_id": game_id,
        "data": dades_partida
    }
    try:
        requests.post(POST_URL, json=cos)
    except requests.exceptions.RequestException as e:
        print(f" Error de connexió enviant progrés: {e}")


def loop_enviar_progress(game_id):
    global enviant_progres
    enviant_progres = True

    while enviant_progres:
        if os.path.exists(NOM_FITXER):
            with open(NOM_FITXER, "r") as f:
                dades_partida = json.load(f)
        else:
            dades_partida = {}

        enviar_progress(game_id, dades_partida)
        espera = random.randint(5, 10)
        time.sleep(espera)


def iniciar_nova_partida():
    nom = input(" Introdueix el teu nom: ").strip()
    print(f"\n Iniciant nova partida per {nom}...")

    dades_jugador = {
        "nom": nom,
        "punts": 0,
        "nivell": 1
    }

    with open(NOM_FITXER, "w") as f:
        json.dump(dades_jugador, f)

    url = "https://fun.codelearn.cat/hackathon/game/new"

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dades = resposta.json()
            print(" Nova partida iniciada correctament.")

            mostrar_historia(nom)

            game_id = dades.get("game_id", 999999)

            fil = threading.Thread(target=loop_enviar_progress, args=(game_id,), daemon=True)
            fil.start()

            problema1()
            problema2()
            problema3()
            problema4()
            problema5()

            global enviant_progres
            enviant_progres = False
            fil.join()

            finalitzar_partida(game_id, nom)
        else:
            print(f"Error en iniciar la partida. Codi: {resposta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f" Error de connexió: {e}")


def mostrar_historia(nom):
    historia = f"""
    Un dia {nom} estava acampant amb els seus amics al bosc. Tots van decidir anar a explorar, però {nom} es va perdre.
    Va trobar una petita casa de fusta i va decidir entrar a buscar ajuda.
    Va picar a la porta, però va veure que era oberta.
    Va entrar amb una mica de por.
    Tot era fosc, i just quan va posar els dos peus a dins, la porta es va tancar a la seva esquena.
    I, ara tu tens que ajudar a {nom} a sortir d'aquí. Bona sort!
    """
    print(historia)


def finalitzar_partida(game_id, nom):
    print(f"""
              {nom} surt corrents de la casa, feliç per haver aconseguit sortir senser d'allà.
              Corre pel bosc i aconsegueix trobar-se a els seus amics, que l'estaven buscant.
              Fi.""")

    if not os.path.exists(NOM_FITXER):
        print(" No s'ha trobat el fitxer de la partida.")
        return

    with open(NOM_FITXER, "r") as f:
        dades_partida = json.load(f)

    cos = {
        "game_id": game_id,
        "data": dades_partida,
        "score": dades_partida.get("punts", 0)
    }

    try:
        resposta = requests.post("https://fun.codelearn.cat/hackathon/game/finalize", json=cos)
        if resposta.status_code == 200:
            print(" Partida finalitzada correctament!")
        else:
            print(f" Error en finalitzar la partida: codi {resposta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f" Error de connexió finalitzant la partida: {e}")


def main():
    accio = mostrar_menu()

    if accio == "1":
        iniciar_nova_partida()
    elif accio == "2":
        print("Fins la propera!")
    else:
        print("Opció no vàlida.")


if __name__ == "__main__":
    main()

