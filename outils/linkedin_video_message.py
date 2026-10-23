#!/usr/bin/env python3
"""Prépare le texte d'un post vidéo LinkedIn pour le scénario Make 7923864 (reseau=linkedin_video).

Usage : python3 outils/linkedin_video_message.py <date AAAA-MM-JJ>
Lit linkedin/file_attente.json, prend l'entrée de la date, et écrit sur la sortie standard
le texte échappé (format « little text » de LinkedIn, puis échappement JSON sans guillemets),
prêt à passer tel quel dans le champ « message ».
"""
import json, re, sys

RESERVES = set('\\|{}@[]()<>#*_~')

def little_text(texte: str) -> str:
    morceaux = []
    pos = 0
    for m in re.finditer(r'#(\w+)', texte):
        morceaux.append(_echappe(texte[pos:m.start()]))
        morceaux.append('{hashtag|\\#|' + m.group(1) + '}')
        pos = m.end()
    morceaux.append(_echappe(texte[pos:]))
    return ''.join(morceaux)

def _echappe(s: str) -> str:
    return ''.join('\\' + c if c in RESERVES else c for c in s)

if __name__ == '__main__':
    date = sys.argv[1]
    file = json.load(open('linkedin/file_attente.json', encoding='utf-8'))
    entree = next(e for e in file if e['date'] == date)
    sys.stdout.write(json.dumps(little_text(entree['texte']), ensure_ascii=False)[1:-1])
