import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as patches
from  scipy.interpolate  import  griddata
import numpy as np
import random
import os
from PIL import Image
import cv2
from pathlib import Path



# folder_dir = "dataset-original/train/images/dossier_de_test"
# images = Path(folder_dir).glob('*.jpg')


def crop_images(input_path, output_path, crop_size=(160, 240), overlap=0.2):
    """
    Découpe toutes les images du dossier spécifié par input_path en plusieurs images
    de taille crop_size, avec un chevauchement de overlap, et enregistre ces images
    dans le dossier spécifié par output_path.
    """
    # Vérifie que le dossier output_path existe, sinon le crée.
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Liste tous les fichiers du dossier input_path.
    files = os.listdir(input_path)

    # Parcourt tous les fichiers du dossier input_path.
    for file in files:
        # Vérifie que le fichier est une image.
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            # Ouvre l'image.
            image_path = os.path.join(input_path, file)
            image = Image.open(image_path)

            # Obtient les dimensions de l'image.
            width, height = image.size

            # Initialise les coordonnées de départ pour le crop.
            y_start = 0

            # Parcourt toutes les lignes de l'image.
            while y_start < height:
                x_start = 0
                # Parcourt toutes les colonnes de l'image.
                while x_start < width:
                    # Calcule les coordonnées de fin du crop.
                    x_end = min(x_start + crop_size[0], width)
                    y_end = min(y_start + crop_size[1], height)

                    # Effectue le crop.
                    cropped_image = image.crop((x_start, y_start, x_end, y_end))

                    # Construit le nom de l'image enregistrée.
                    i = y_start // (crop_size[1] - overlap)
                    j = x_start // (crop_size[0] - overlap)
                    name = f"{file.split('.')[0]}_{i}_{j}_{crop_size[1]}_{crop_size[0]}.jpg"

                    # Enregistre l'image cropée.
                    #print(cropped_image.size[0])
                    if cropped_image.size[0]>=160 and cropped_image.size[1]>= 160:
                        cropped_image.save(os.path.join(output_path, name))

                    # Passe à la prochaine colonne.
                    x_start += crop_size[0] - overlap

                # Passe à la prochaine ligne.
                y_start += crop_size[1] - overlap

#crop_images("dataset-original/train/images/dossier_de_test","dataset-original/train/images/dossier_de_test/output")

def show_same_prefix_images(folder_path, prefix):
    """
    Affiche toutes les images du dossier spécifié par folder_path
    qui ont le même préfixe que celui spécifié par prefix,
    en les affichant dans le même canvas.
    """
    # Obtenir la liste de tous les fichiers dans le dossier.
    files = os.listdir(folder_path)

    # Parcourir la liste de fichiers et afficher les images avec le même préfixe.
    images = []
    for file in files:
        # Vérifier si le fichier est une image (extension jpg, png, etc.)
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            # Vérifier si le préfixe est présent au début du nom de fichier.
            if file.startswith(prefix + '_'):
                # Ouvrir l'image et l'ajouter à la liste des images.
                image_path = os.path.join(folder_path, file)
                image = Image.open(image_path)
                images.append(image)

    # Calculer la taille totale du canvas.
    canvas_width = sum([image.width for image in images])
    canvas_height = max([image.height for image in images])

    # Créer le canvas et copier les images dedans.
    canvas = Image.new("RGB", (canvas_width, canvas_height))
    x = 0
    for image in images:
        canvas.paste(image, (x, 0))
        x += image.width

    # Afficher le canvas.
    canvas.show()

#show_same_prefix_images("dataset-original/train/images/dossier_de_test/output",'abigotte')
