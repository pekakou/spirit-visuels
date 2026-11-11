#!/usr/bin/env python3
"""Texte LinkedIn d'une Minute Conseil, prêt pour le scénario Make 7923864 (reseau=linkedin_video).

Usage : python3 outils/minute_conseil_message.py <date AAAA-MM-JJ>
Lit minute_conseil/programme.json, prend la publication de la date, et écrit sur la sortie standard
le texte LinkedIn échappé (format « little text », puis échappement JSON sans guillemets).
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linkedin_video_message import little_text

if __name__ == '__main__':
    date = sys.argv[1]
    prog = json.load(open('minute_conseil/programme.json', encoding='utf-8'))
    pub = next(p for p in prog['publications'] if p['date'] == date)
    sys.stdout.write(json.dumps(little_text(pub['textes']['LI']), ensure_ascii=False)[1:-1])
