import requests
import urllib.request
import os


def default_folders_check():
    print("[+] Após usar, apagar a pasta result ou os arquivos dentro dela")
    print("[+] Ainda estou automatizando essa parte, rs")
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


def get_images():
    mlb = str(input("Informe um MLB: "))
    url = f"https://api.mercadolibre.com/items/{mlb}"

    response = requests.get(url)
    response = response.json()

    variations_quantity = len(response["variations"])

    if variations_quantity > 0:
        variations_control = 0
        for variation in response["variations"]:
            folder_name = variation["id"]
            os.mkdir(f"result/{folder_name}")
            picture_ids = []
            for picture_id in variation["picture_ids"]:
                picture_ids.append(picture_id)

            for picture_id in picture_ids:
                url = f"https://http2.mlstatic.com/D_{picture_id}-F.jpg"
                urllib.request.urlretrieve(url, f"result/{folder_name}/{picture_id}.jpg")

            variations_control += 1

    if variations_quantity == 0:
        pictures_ids = []
        for picture_id in response["pictures"]:
            pictures_ids.append(picture_id["id"])

        folder_name = mlb
        os.mkdir(f"result/{folder_name}")

        for picture_id in pictures_ids:
            url = f"https://http2.mlstatic.com/D_{picture_id}-F.jpg"
            urllib.request.urlretrieve(url, f"result/{folder_name}/{picture_id}.jpg")

    input("Pressione ENTER para finalizar")


if __name__ == "__main__":
    default_folders_check()

    option = int(input("[1] MLB Individual\n"
              "[2] Lista de MLBs (nao funcionakkkk)\n"
              "[3] ...?\n"
              "R: "))

    if option == 1:
        get_images()
