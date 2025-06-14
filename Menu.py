import requests
import os
import json
import time
import threading
import random

NOM_FITXER = "jugador.json"
POST_URL = "https://fun.codelearn.cat/hackathon/game/store_progress"


enviant_progres = False

def mostrar_menu():
    print("\n🎮 MENÚ PRINCIPAL")
    print("1. Nova partida")
    print("2. Continuar")
    print("3. Sortir")

    opcio = input("Selecciona una opció (1-3): ")
    return opcio

def enviar_progress(game_id, dades_partida):
    """
    Funció que fa la petició POST per enviar el progrés.
    """
    cos = {
        "game_id": game_id,
        "data": dades_partida
    }
    try:
        resposta = requests.post(POST_URL, json=cos)
        if resposta.status_code == 200:
            print(f"✅ Progrés enviat correctament a {POST_URL}")
        else:
            print(f"⚠️ Error enviant progrés: codi {resposta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de connexió enviant progrés: {e}")

def loop_enviar_progress(game_id):
    """
    Funció que corre en un fil paral·lel i envia progress cada 5-10 segons.
    """
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
    nom = input("👤 Introdueix el teu nom: ").strip()
    print(f"\n🆕 Iniciant nova partida per {nom}...")

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
            print("✅ Nova partida iniciada correctament.")
            print("📦 Resposta del servidor:")
            print(dades)

            
            game_id = dades.get("game_id")
            if not game_id:
                print("⚠️ No s'ha trobat 'game_id' a la resposta. Assignant 999999 per defecte.")
                game_id = 999999

            
            fil = threading.Thread(target=loop_enviar_progress, args=(game_id,), daemon=True)
            fil.start()

            print("\n⏳ Estàs jugant... prem Enter per parar i sortir.")
            input()  

            
            global enviant_progres
            enviant_progres = False
            fil.join()
            print("🔴 Progrés aturat. Fins aviat!")

        else:
            print(f"⚠️ Error en iniciar la partida. Codi: {resposta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de connexió: {e}")

def continuar_partida():
    if not os.path.exists(NOM_FITXER):
        print("⚠️ No hi ha cap partida guardada. Comença una nova partida primer.")
        return

    with open(NOM_FITXER, "r") as f:
        dades_jugador = json.load(f)

    print(f"\n🔄 Continuant partida per {dades_jugador['nom']}...")
    print(f"Punts: {dades_jugador.get('punts', 0)}")
    print(f"Nivell: {dades_jugador.get('nivell', 1)}")

def main():
    accio = mostrar_menu()

    if accio == "1":
        iniciar_nova_partida()
    elif accio == "2":
        continuar_partida()
    elif accio == "3":
        print("👋 Fins la propera!")
    else:
        print("❌ Opció no vàlida.")

if __name__ == "__main__":
    main()
