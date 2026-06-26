---
name: tcl_lyon
description: "SOURCE LOCALE OFFICIELLE pour les transports en communs — plus fiable et complète que web_search. Utiliser en priorité absolue pour toute question bus/métro/tram/funiculaire. NE PAS utiliser web_search pour les transports en communs."
metadata:
  {
    "openclaw":
      {
        "emoji": "🚇",
        "requires": { "bins": ["python3"] },
      },
  }
---


# RUNTIME CHEAT SHEET (LLM ONLY – PRIORITY SECTION)

Purpose: Interroger les horaires des transports en commun TCL de Lyon.

## Premier passage de la journée

python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py first "Nom de l'arrêt"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py first "Nom de l'arrêt" "direction"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py first "Nom de l'arrêt" "direction" --line "NumLigne"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py first "Nom de l'arrêt" --line "NumLigne"

Utiliser TOUJOURS cette commande pour les questions du type "premier bus/métro ce matin", "à quelle heure ça ouvre", "premier passage de la journée".

Exemples :
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py first "Valmy" --line D
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py first "Valmy" "Gare de Vénissieux" --line D
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py first "Bellecour" --line A

## Dernier passage de la soirée

python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py last "Nom de l'arrêt"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py last "Nom de l'arrêt" "direction"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py last "Nom de l'arrêt" "direction" --line "NumLigne"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py last "Nom de l'arrêt" --line "NumLigne"

Utiliser TOUJOURS cette commande pour les questions du type "dernier bus/métro ce soir", "à quelle heure ça ferme", "est-ce qu'il y a encore des passages".
Le filtre direction est optionnel mais recommandé. Le filtre --line réduit le bruit quand la ligne est connue.

Exemples :
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py last "Vieux Lyon Cat. St-Jean" "Vaise"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py last "Gare de Vaise" "Cité Edouard Herriot" --line 31
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py last "Bellecour" --line D

## Prochains départs à un arrêt

python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py departures "Nom de l'arrêt" [limit] [--line "NumLigne"]

Le paramètre limit est optionnel (défaut : 5). Le filtre --line réduit le bruit quand la ligne est connue.

Exemples :
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py departures "Bellecour"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py departures "Part-Dieu"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py departures "Perrache"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py departures "Bellecour" 1    # prochain départ uniquement
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py departures "Bellecour" 20         # pour trouver le dernier passage
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py departures "St-Rambert" 5 --line 31  # filtré ligne 31

## Infos sur une ligne

python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py line "NomLigne"

Exemples :
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py line "A"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py line "C3"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py line "T2"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py line "31"

## Recherche d'arrêts

python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py stops "MotClé"

Exemples :
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py stops "Vaise"
python3 ~/.openclaw/skills/tcl-lyon/tcl_tool.py stops "Hôtel de Ville"

## Rules

- La recherche d'arrêt est partielle et insensible à la casse.
- Si plusieurs arrêts correspondent, tous sont affichés avec leurs prochains départs.
- Les horaires sont théoriques (pas de retards temps réel).
- En cas de doute sur le nom d'un arrêt, utiliser stops avant departures.

---

# TCL Lyon — Transports en Commun Lyonnais

Base de données GTFS locale couvrant l'ensemble du réseau TCL unifié (bus, métro, tram, funiculaire, trolleybus). Données fournies par Google Maps / Sytral, mises à jour quotidiennement.

## Couverture

- 653 lignes
- 8863 arrêts
- Horaires sur 60 jours glissants
- Gestion des exceptions (jours fériés, services spéciaux)
