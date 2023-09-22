import requests
import urllib.request
import os
import re


def default_folders_check():
    print("[+] Após usar, apagar a pasta result ou os arquivos dentro dela")
    print("[+] Ainda estou automatizando essa parte, rs")
    print()
    try:
        os.mkdir("result")
    except FileExistsError:
        print()


#         files_qty = len(os.listdir("result"))
#         if files_qty > 0:
#             for file in os.listdir("result"):
#                 file_path = os.path.join("result", file)
#                 os.removedirs(file_path)


def get_images_by_list():
    print("rs")


def create_folder(folder_name):
    os.mkdir(folder_name)


def download_images(url, folder_path):
    picture_id = url.split("/")[-1].split("-")[0]
    image_path = os.path.join(folder_path, f"{picture_id}.jpg")
    urllib.request.urlretrieve(url, image_path)


def get_images():
    mlb = input("Informe um MLB: ")
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
            folder_name = f"result/{variation_name}-{variation['id']}"
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

    input("Pressione ENTER para finalizar")


if __name__ == "__main__":
    default_folders_check()

    option = int(input("[1] MLB Individual\n"
              "[2] Lista de MLBs (nao funcionakkkk)\n"
              "[3] ...?\n"
              "R: "))

    if option == 1:
        get_images()
