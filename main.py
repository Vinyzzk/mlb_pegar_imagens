import requests
import urllib.request
import os
import re
import pandas as pd
import os


def default_folders_check():
    try:
        os.mkdir("result")
    except FileExistsError:
        pass


def create_folder(folder_name):
    os.mkdir(folder_name)


def download_images(url, folder_path):
    picture_id = url.split("/")[-1].split("-")[0]
    image_path = os.path.join(folder_path, f"{picture_id}.jpg")
    urllib.request.urlretrieve(url, image_path)


def get_images(mlb):
    url = f"https://api.mercadolibre.com/items/{mlb}"

    response = requests.get(url)
    response_data = response.json()
    variations = response_data.get("variations", [])
    pictures = response_data.get("pictures", [])

    if variations:
        for variation in variations:
            variation_name_parts = [
                f"{attribute['name']}-{attribute['value_name']}"
                for attribute in variation.get("attribute_combinations", [])
            ]
            variation_name = "-".join(variation_name_parts)
            variation_name = re.sub(r'[^a-zA-Z-]', '', variation_name)
            folder_name = f"result/{mlb}-{variation_name}-{variation['id']}"
            create_folder(folder_name)

            for picture_id in variation.get("picture_ids", []):
                url = f"https://http2.mlstatic.com/D_{picture_id}-F.jpg"
                download_images(url, folder_name)

    elif pictures:
        folder_name = f"result/{mlb}"
        create_folder(folder_name)

        for picture in pictures:
            url = f"https://http2.mlstatic.com/D_{picture['id']}-F.jpg"
            download_images(url, folder_name)

    os.system('cls')
    print("[+] Imagens baixadas com sucesso!")
    print(f"[+] Pasta gerada: {folder_name}")
    print("----------")
    print("[+] Digite 0 para parar, ou continue baixando imagens.")


def get_images_by_list():
    df = pd.read_excel("mlbs.xlsx")
    column = df["MLB"]
    mlbs = column.values
    
    for mlb in mlbs:
        get_images(mlb)

        input("Pressione ENTER para finalizar")
        

if __name__ == "__main__":
    default_folders_check()

    print(
        """Individual: Voce fornece um MLB unico
Lista: Voce fornece um arquivo .xlsx com apenas uma coluna chamada MLB e os IDs embaixo
""")

    option = int(input("[1] MLB Individual\n"
              "[2] Lista de MLBs\n"
              "[>] "))
    
    os.system('cls')

    if option == 1:
        while True:
            mlb = str(input("[>] Informe um MLB: "))
            if mlb == "0":
                break
            if mlb.startswith("MLB"):
                get_images(mlb)
            else:
                print("[!] Insira um MLB valido.")
                continue

    if option == 2:
        get_images_by_list()