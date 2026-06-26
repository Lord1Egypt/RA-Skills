# 🎯 Syléa — Coach de vie & assistant de décision

> *« L'IA qui t'aide à décider au lieu de décider à ta place. »*

Syléa est un coach de vie personnel basé sur la psychologie comportementale. Il t'aide à :

- 🧭 **Analyser tes dilemmes** avec un score de probabilité par option
- 🎯 **Planifier tes objectifs de vie** avec une formule déterministe
- 🌱 **Suivre ton bien-être** sur 5 dimensions psychologiques
- 📝 **Faire tes bilans quotidiens** pour prévenir le burn-out

**Toutes tes données restent locales** dans `~/.sylea/`. Zéro cloud, zéro tracking, zéro compte à créer.

## Installation

```bash
openclaw skills install sylea
```

## Exemples d'usage

### Analyser un dilemme
> **Toi :** *« Syléa, aide-moi à choisir entre accepter ce poste à Paris ou rester en remote dans mon rôle actuel »*
>
> **Syléa :** *[te guide à scorer chaque option sur 4 dimensions, calcule la probabilité de succès, t'affiche un tableau comparatif avec recommandation et alertes]*

### Planifier un objectif de vie
> **Toi :** *« Syléa, je veux publier mon premier roman dans 3 ans. Quelles sont mes chances ? »*
>
> **Syléa :** *[estime ta probabilité de succès (~68%), l'horizon réaliste (2.7 ans), et te liste les 2 leviers principaux à actionner]*

### Faire un bilan de journée
> **Toi :** *« Syléa, bilan rapide de ma journée »*
>
> **Syléa :** *[compare tes scores du jour avec ton baseline, flag les dimensions en alerte, suggère UNE micro-amélioration concrète pour demain]*

## Ce qui rend Syléa différent

| Feature | Syléa | Assistants IA génériques |
|---------|-------|--------------------------|
| Formule déterministe | ✅ | ❌ (réponses au feeling) |
| Profil persistant local | ✅ (`~/.sylea/`) | ❌ (oublié d'une session à l'autre) |
| Framework psycho 5 dimensions | ✅ (basé sur psychologie positive) | ❌ |
| Protège ta vie privée | ✅ (zéro réseau) | ❌ (logs cloud) |
| Français natif | ✅ | ⚠️ (traductions approximatives) |

## Gratuit vs Pro

Ce skill est la version **gratuite & locale** de Syléa. Elle te couvre à 100% pour un usage manuel personnel.

Pour aller plus loin : [**Syléa Pro**](https://sylea-ai.com) ajoute :

- ☁️ **Sync cloud multi-device** (desktop, web, mobile)
- 🤖 **Agent autonome** qui envoie tes emails, gère ton calendrier, automatise tes tâches
- 📊 **Tableau de bord** en temps réel avec graphiques
- 🧠 **ML-calibrated probabilities** (modèle entraîné sur données comportementales)

## Tester en local avant publication

Pour développeurs voulant contribuer ou tester :

```bash
# Cloner dans le dossier skills local d'OpenClaw
git clone https://github.com/Clotilde563/sylea-skill ~/.openclaw/skills/sylea

# Redémarrer le gateway
openclaw gateway restart

# Tester
openclaw skills info sylea
```

## Crédits

Créé par l'équipe Syléa — https://sylea-ai.com

**License MIT-0** (MIT No Attribution). Le code est libre, tes données sont les tiennes.

## Support

- Bug report : https://github.com/Clotilde563/sylea-skill/issues
- Questions : sylea.ai.assistance@gmail.com
