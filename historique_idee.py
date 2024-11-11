# ---------------------- HISTORIQUE DES IDEES UTILISEE DANS L'ACCOMPLISSEMENT DU DEVOIR --------------------------------

from collections import Counter

import crypt

# Cette partie utilise des fonctions du module crypt pour charger deux textes depuis le Projet Gutenberg.
# Les URL représentent des ressources en ligne, et les textes sont combinés en une seule variable text.
url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
text = crypt.load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
text = text + crypt.load_text_from_web(url)


caracteres = list(set(list(text)))
nb_caracteres = len(caracteres)
nb_bicaracteres = 256-nb_caracteres
bicaracteres = [item for item, _ in Counter(crypt.cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
symboles = caracteres + bicaracteres


# On extrait ici les caractères uniques dans text et on calcule le nombre de paires de caractères (bichar) les plus
# fréquents pour les ajouter à une liste appelée symboles. Ces symboles et bicharacteres sont analysés pour leur
# fréquence dans le texte.
def frequence(text, symbole):
  long = len(text)
  compteur = 0
  len_symbole = len(symbole)

  for i in range(long - len_symbole + 1): # ca oui
    if text[i:i + len_symbole] == symbole:
      compteur += 1

  return compteur

# Cette fonction crée un dictionnaire avec les occurrences de chaque symbole dans text. Elle considère les bicharactères
# (deux caractères consécutifs) et les caractères simples pour remplir le dictionnaire d, et trie ensuite les symboles
# par fréquence décroissante.
def occurence_dictionnaire(text, symboles):
  long = len(text)

  d = {}

  for s in symboles:
    d[s] = 0

  i = 0
  while i < long:
    if i + 1 < long:
      bichar = text[i] + text[i + 1]
      if bichar in symboles:
        i += 2
        d[bichar] += 1
        continue
      else:
        d[text[i]] += 1
    else:
      d[text[i]] += 1
    i += 1

  l = []
  for s in symboles:
    l.append([s, d[s]])

  l = sort_liste(l)
  return l


# La fonction gen_Liste crée une liste de symboles avec leur fréquence, en utilisant la fonction
# frequence sur une séquence donnée.
def gen_Liste(text, sequence):
  liste = []

  for symbole in sequence:
    element = []

    freq = frequence(text, symbole)


    element.append(symbole)
    element.append(freq)
    liste.append(element)

  return liste


def sort_liste(liste):
  return sorted(liste, key=lambda k: k[1], reverse=True)


# Cette fonction segmente une chaîne de caractères chiffrée C en segments de 8 caractères (octets). Elle génère les
# occurrences des octets (set_bytes) et crée une traduction entre les octets et les symboles les plus
# fréquents dans le texte de référence.
def decrypt(C):
  liste_bytes = [C[i:i+8] for i in range(0, len(C), 8)]
  set_bytes = list(set(liste_bytes))
  liste_bytes_freq = gen_Liste(C, set_bytes)
  occurances_liste = occurence_dictionnaire(text, symboles)
  sorted_bytes = sort_liste(liste_bytes_freq)
  traduction = creer_Traduction(occurances_liste, sorted_bytes)

  M = [traduction[i] for i in liste_bytes]
  return ''.join(M)




def creer_Traduction(liste_symbole, liste_bytes):
  dico = {}

  for i in range(len(liste_bytes)):
    dico[liste_bytes[i][0]] = liste_symbole[i][0]
  return dico


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


import string
from collections import Counter
from random import shuffle

import crypt


url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
text = crypt.load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
text = text + crypt.load_text_from_web(url)


# On calcule les combinaisons les plus fréquentes de deux caractères (bicaracteres) pour compléter le nombre
# de symboles à un total de 256 (pour correspondre aux valeurs de 8 bits possibles).
caracteres = list(set(list(text)))
nb_caracteres = len(caracteres)
nb_bicaracteres = 256-nb_caracteres
bicaracteres = [item for item, _ in Counter(crypt.cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
symboles = caracteres + bicaracteres
symboles.sort()


# Afin de  vérifier le sens du texte une fois déchiffré, le fichier mots.txt est chargé, et chaque mot est ajouté
# à l’ensemble mots_francais, avec également la ponctuation et les espaces
with open("mots.txt", encoding="utf-8") as file:
  mots_francais = set(line.strip().lower() for line in file)

mots_francais.add(string.punctuation)
mots_francais.add(' ')


# Le code définit la fonction occurence_dictionnaire2 qui calcule combien de fois chaque symbole ou paire de
# symboles apparaît dans le texte. Cette fonction construit un dictionnaire où chaque symbole a un compteur d'occurrence
def occurence_dictionnaire2(text, symboles):
  long = len(text)

  d = {}

  for s in symboles:
    d[s] = 0

  i = 0
  while i < long:
    if i + 1 < long:
      bichar = text[i] + text[i + 1]
      if bichar in symboles:
        i += 2
        d[bichar] += 1
        continue
      else:
        d[text[i]] += 1
    else:
      d[text[i]] += 1
    i += 1

  l = []
  for s in symboles:
    l.append([s, d[s]])

  l = sort_liste(l)
  return l


def sort_liste(liste):
  return sorted(liste, key=lambda k: k[1], reverse=True)



# La fonction principale decrypt prend en entrée un code binaire (C) et procède comme suit :

# On divise le code en segments de 8 bits (octets) et compte les occurrences de chaque segment.

# On trie ensuite ces octets et les associe aux symboles fréquents du texte original pour créer
# une correspondance probable.

# On tente de reconstruire le texte déchiffré en mappant chaque segment d'octet à son
# caractère correspondant à travers un dictionnaire de traduction.

def decrypt2(C):
  liste_bytes = [C[i:i + 8] for i in range(0, len(C), 8)]

  bytes_occ = {}

  for byte in liste_bytes:
    if byte in bytes_occ:
      bytes_occ[byte] += 1
    else:
      bytes_occ[byte] = 1

  sorted_bytes = []

  for byte in bytes_occ:
    sorted_bytes.append([byte, bytes_occ[byte]])

  sorted_bytes = sort_liste(sorted_bytes)

  occurances_liste = occurence_dictionnaire2(text, symboles)


  traduction = creer_Traduction(occurances_liste, sorted_bytes)

  M = []
  for byte in liste_bytes:
    caractere = traduction.get(byte, '')  # Utilisation de get() pour éviter les erreurs si l'élément est absent
    M.append(caractere)

  M = ''.join(M)

  print(traduction)
  while not analyser_trad(M.split(' '), occurances_liste, sorted_bytes, traduction):
    M = []
    for byte in liste_bytes:
      caractere = traduction.get(byte, '')
      M.append(caractere)
    M = ''.join(M)

  return ''.join(M)


def creer_Traduction(liste_symbole, liste_bytes):
  dico = {}

  for i in range(len(liste_bytes)):
    dico[liste_bytes[i][0]] = liste_symbole[i][0]
  return dico


# Afin de s’assurer que le texte déchiffré a un sens, analyser_trad vérifie si les 10 premiers mots du texte
# appartiennent à la liste mots_francais. Si le texte ne fait pas sens, la traduction est réessayée avec une correspondance différente
def analyser_trad(M, liste_symbole, liste_bytes, traduction):
  print(M[0:10])

  for i in M[0:10]:
    if i not in mots_francais:  # Assurez-vous que 'mots_francais' est bien défini
      shuffle(liste_symbole)
      traduction = creer_Traduction(liste_symbole, liste_bytes)  # Mettre à jour 'traduction'
      return False
  return True

code_chiffre = "00010100100100100000010111100011000111000010011011111011011111010110111110001011011111110100000010101010011101111111111000011011001100001000100001010111101010101011111001010100001010010111110100011000001100011111011111010000100011011101110001000000110011111100011101111010110000000011000110011101010100010100000010001001111001101000100001010111001001100001011001100101111000000110010100011000110100000110110111000111000101111010101101000000111001000001001101000000110111000001010000011100110110111111111001010100001010010000101000011010001011010011110000001101110001111101010110111110011011011100101010001001111001101000100001010111101010101011111001010100001010010000100011010001110110110010011010000111010001011000110100000000001001110011000111111100001001010010000000110001111110111101110001000000110011111100011111110111000111000111000111110011011001010011110010010000011011001010010000010011000101111001010000110001000111001100000011001110001100011110100011011010110011110101000010011001101001100000111100100110111001101000100001010111101010101011111001010100001010010111110111001011000111010110001100110001000011100011000111100100110010110100110100000001010111100110101001000010000010001111101111110011110011000001001010010000111000110011000100001110001100011001110101010001010000000101010000101001001001100000110110111011000001010110110101110000001001110000101001101010010001101010010000011001101111100000011010001001111001101000100001010111101010101011111001010100001010011010111011010101110001111001100100100111111100111011110111100110101010100001001000111011101001100011000001000000101010100111011101111001110010111000001100001001000011000001001000001110001111110001001000110001111010001101101001001001100101111101010001101010010000100111111111001000011000000100000011101110110111000100000011001111100111010101000101000000010101000010100101110010000110100010110001110000000111010001011111100000000101001111000000101001111000011001000011001010011100010010011011111011010101000010100111001111100111011000111111001110001100000100110110110100010101100000110111100110111001110001010011110111010010011000110100000110110011101011001100000110111011000001010011100000011001011011111100011001110011100000101000110101000111001100000011001110110111001000010000001100100111111001110101010001000101000010011111001111110001110001001000000001110101010101001110011100001011010011111110001101110110100100000101101011011001011110000000010100011010110101001011110110101101001011011001010111111011110101000100111000010110111000001001101001101101100111000011100000000101000110101111001100001001101000111110000111000010100001010010010100011110100101001110001100000101000101101110000111111100000011000111001001001010011100101000001000000011100011000100010110101101000111011000110001100101000101011011011011111001101110011001001000001001110111011000001000000011100101011000101100110001110001010000100111000010100011010100111111100011010010011001101100000110100001001010111111110110110000111001010011110011011100101001011011110000000111000110110110011100001100101000000000001111110001010111010000010111010011111111001110100010011111101101111111000000001111000100000110110100010010110010011011011110100011000101011000011010110101001011010100010010001110011000001110010101100100000000100110011011111001001000000101111000110001110001110001111100111101101111111110000001111111000000111011010000001001010001100001001100010000111001100001001100000000011011011011011101110111101100001000010110001111011101110010010111100110000100010100001001110111111110000000110101111000101100110000100111011010011001011101001001101010010001100001111011111101101000111100001010011100111010110110011100001010010001100001110011110001001011100110111101111000101100100000000010100100000011001111100111010101000101000000011111000010011000100110011001000110100001011010101000111)"
print(decrypt2(code_chiffre))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------