# Surgery-PMPH-10edition (Chirurgie)

<div align="center">

> *« Guide de l'étudiant en médecine du XXIe siècle »*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> Manuel de compétences cliniques basé sur *Chirurgie, 10e édition* (People's Medical Publishing House) — 240 compétences en chirurgie et soins critiques
<br>
<br>
<img src="https://github.com/xllgreen/Surgery-PMPH-10edition-/blob/main/assets/Surgery.png" width="260px">
<br>

Pourquoi peiner à lire tout un livre ?<br>
Posez simplement une question et obtenez la solution directement depuis le manuel.

<br>

**Autres langues / Other Languages:**

[简体中文](README.md) · [English](README_EN.md) · [日本語](README_JP.md) · [Русский](README_RU.md)

</div>

---

## À propos du projet

Ce projet intègre de manière systématique les domaines fondamentaux que sont la chirurgie clinique, la médecine d'urgence et de soins intensifs, la gestion périopératoire, le traumatisme, l'oncologie intégrative, le contrôle des infections et le diagnostic/traitement des maladies multisystémiques. Il couvre **240 compétences cliniques essentielles** organisées en **17 catégories principales**.

**Public cible** : Chirurgiens, médecins urgentistes, équipes de soins intensifs, étudiants en médecine

**Manuel de référence** : *Chirurgie*, 10e édition, People's Medical Publishing House

## Structure du projet

```
Surgery-PMPH-10edition/
├── SKILL.md              # Configuration centrale — registre des 240 compétences
├── README.md             # Ce document — présentation et guide d'utilisation
├── <skill-name>/         # Définitions détaillées de chaque compétence
│   └── SKILL.md          #   Détails de la compétence (indications, procédure, références)
├── scripts/              # Scripts utilitaires exécutables
│   ├── skill-search.sh   #   Recherche par mot-clé de compétence
│   └── skill-report.sh   #   Générateur d'inventaire des compétences
├── config/               # Fichiers de configuration
│   └── skill-config.yaml #   Classification et métadonnées des compétences
└── tests/                # Validation et tests
    └── validate-all.sh   #   Script de validation d'intégrité
```

## Aperçu des catégories de compétences

| Catégorie | Nombre | Description |
|-----------|--------|-------------|
| 🚑 Urgences & Réanimation | 14 | RCP, réanimation du choc, urgences électrolytiques |
| 🦴 Traumatologie & Fractures | 27 | Classification des fractures, réduction & fixation, lésions nerveuses |
| 🩺 Chirurgie générale & Urgences abdominales | 22 | Appendicite, occlusion intestinale, hernie, péritonite |
| 🫁 Chirurgie hépato-bilio-pancréatique & splénique | 19 | Lithiase biliaire, pancréatite, traumatisme hépatique |
| 🩻 Chirurgie gastro-intestinale | 10 | Cancer gastrique, cancer colorectal, RGO |
| 🫘 Urologie | 24 | Calculs, tumeurs, infections, lésions urétrales |
| 🩸 Chirurgie vasculaire | 7 | TVP, varices, réparation vasculaire |
| 🔥 Brûlures & Chirurgie plastique | 8 | Estimation de surface, classification de profondeur, greffe cutanée |
| 🧬 Oncologie chirurgicale & Traitement intégratif | 16 | Classification TNM, radio/chimiothérapie, chirurgie de sauvetage de membre |
| 📋 Gestion périopératoire | 18 | Optimisation préopératoire, antibiotiques, support nutritionnel |
| 💉 Anesthésiologie & Gestion de la douleur | 11 | Gestion des voies aériennes, rachianesthésie, anesthésie locale |
| ⚖️ Endocrinologie & Métabolisme | 6 | Hyperparathyroïdie, déshydratation, troubles électrolytiques |
| 🦠 Infection & Immunologie | 7 | Tuberculose, sepsis, tétanos |
| 📡 Imagerie & Radiologie interventionnelle | 10 | Imagerie de contraste, endoscopie, radiologie interventionnelle |
| 🏋️ Réadaptation & Évaluation fonctionnelle | 12 | Rééducation des fractures, évaluation neurologique |
| 🦿 Rhumatologie & Pathologies rachidiennes | 5 | Spondylarthrite ankylosante, sténose spinale |
| 🔧 Autres compétences spécialisées | 10 | SDRA, IRA, défibrillation, etc. |

## Guide de démarrage rapide

### Installation

CLI :
```bash
openclaw skills install surgery-pmph-10edition
```

Invite (prompt) :
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Surgery-PMPH-10edition" (xllgreen/surgery-pmph-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/surgery-pmph-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### Utilisation après installation

Indiquez ce qui suit à l'agent :
```bash
Avant chaque réponse, veuillez consulter la compétence médicale correspondante pour confirmer.
```

### Recherche de compétences

```bash
# Recherche par mot-clé
bash scripts/skill-search.sh appendicite

# Générer l'inventaire des compétences
bash scripts/skill-report.sh
```

### Mode d'emploi

Chaque compétence se compose de quatre parties :
1. **Indications** — Quand déclencher cette compétence
2. **Procédure** — Processus opératoire standardisé
3. **Précautions** — Contre-indications et avertissements
4. **Références** — Documents complémentaires détaillés

### Stratégies d'interrogation

#### 1. **Concept**
Question :
```bash
Quel est le concept du pseudokyste pancréatique en chirurgie ?
```
Réponse :
```bash
## Pseudokyste pancréatique (Pancreatic Pseudocyst, PPC) — Concept
Un pseudokyste pancréatique est une complication **survenant après une pancréatite aiguë, un traumatisme pancréatique ou une pancréatite chronique**. Il s'agit essentiellement **d'une structure kystique formée lorsque le suc pancréatique s'écoule par un canal pancréatique nécrosé ou rompu et est encapsulé par du tissu fibreux dans l'espace péripancréatique ou le petit omentum**.
### Caractéristiques clés
| Caractéristique | Description |
|----------------|-------------|
| **Signification de « pseudo »** | La paroi kystique **n'a pas de revêtement épithélial** (contrairement aux vrais kystes) ; elle est composée de tissu conjonctif fibreux et de tissu de granulation |
| **Mécanisme de formation** | Rupture canalaire pancréatique → extravasation du suc pancréatique → réaction inflammatoire tissulaire environnante et encapsulation → maturation progressive de la paroi (nécessite **≥6 semaines**) |
| **Composition du liquide** | Riche en enzymes pancréatiques (amylase/lipase), liquide protéique |
| **Localisations fréquentes** | Petit omentum, espaces péripancréatiques |
### Histoire naturelle
- Les kystes **<4 cm** se résorbent presque toujours spontanément
- **<5 cm** — environ 50 % se résorbent spontanément
- **>6 cm ou multiples** — résorption spontanée peu probable ; évaluation d'intervention nécessaire
- La maturation de la paroi kystique prend environ **6 semaines** ; le drainage interne n'est approprié qu'après maturation
### Diagnostic différentiel avec les vrais kystes / tumeurs kystiques
> À l'imagerie, le PPC peut être confondu avec les tumeurs kystiques pancréatiques (cystadénome séreux, cystadénome mucineux, IPMN). Le PPC se distingue par trois éléments : antécédents de pancréatite aiguë/traumatisme, absence de revêtement épithélial, et amylase du liquide kystique considérablement élevée.
Souhaitez-vous que je détaille les stratégies thérapeutiques (surveillance vs drainage interne vs drainage externe vs résection) ?
```

#### 2. **Analyse de cas clinique**
Question :
```bash
Femme de 28 ans, infertilité depuis 3 ans de mariage. Présente une aménorrhée et une galactorrhée depuis 6 mois. Examen physique : apparence normale, galactorrhée présente, fond d'œil et champs visuels normaux. Prolactine sérique à 250 ng/mL. L'IRM révèle une zone hyposignal de 4mm×4mm dans la selle turcique, à 5mm du nerf optique. Quel est le diagnostic et le plan de traitement ?
```
Réponse :
```bash
## Analyse du cas
**Indices clés :**
| Élément | Résultat |
|---------|----------|
| Patient | Femme de 28 ans |
| Plainte principale | **Aménorrhée + galactorrhée + infertilité** (triade classique) |
| PRL sérique | **250 ng/mL** (normale < 25, nettement élevée) |
| IRM | **Zone hyposignal de 4mm × 4mm** dans la selle (microadénome < 10mm) |
| Champs visuels/acuité | **Normaux**, à 5mm du nerf optique (pas de compression) |
### Diagnostic : Microadénome hypophysaire à prolactine
**Arguments :**
- PRL élevée → inhibe la GnRH → **syndrome aménorrhée-galactorrhée-infertilité**
- Tumeur de 4mm = microadénome
- Pas de déficit du champ visuel = pas de compression du chiasma optique
### Traitement : Traitement médical en première intention, pas d'indication chirurgicale
**Première ligne : Agonistes des récepteurs dopaminergiques**
| Médicament | Posologie | Avantage |
|------------|-----------|----------|
| **Cabergoline** | 0,25–0,5 mg, 1–2 fois/semaine | Premier choix, effets secondaires moindres, prise facile |
| Bromocriptine | 1,25–5 mg, 2–3 fois/jour | Alternative, mais nausées/vertiges plus fréquents |
**Résultats attendus :**
- **En quelques semaines** → normalisation de la PRL → reprise des menstruations ovulatoires, disparition de la galactorrhée
- **En quelques mois à un an** → réduction tumorale significative (~80–90 % d'efficacité)
**Pourquoi pas de chirurgie ?**
- Les microadénomes sont traités médicalement en première intention — haute efficacité, traumatisme minime
- La chirurgie transsphénoïdale est indiquée pour : résistance/intolérance médicamenteuse, symptômes de compression du nerf optique, ou suspicion de tumeur non à prolactine (ex. adénome non fonctionnel)
- Ce cas : à 5mm du nerf optique, champs visuels normaux — **pas d'indication chirurgicale**
### Suivi
- Contrôle de la PRL tous les 3 à 6 mois après traitement
- IRM annuelle après réduction tumorale
- Une fois la PRL normalisée, une grossesse est envisageable ; nécessite une gestion conjointe obstétrico-endocrinienne
```

#### 3. **Questions d'examen**
Question :
```bash
La complication la plus grave de la thrombose veineuse profonde des membres inférieurs est :
A. Varices superficielles des membres inférieurs
B. Embolie pulmonaire
C. Spasme artériel associé avec ischémie du membre
D. Ulcère du membre inférieur
E. Obstruction de la veine cave
```
Réponse :
```bash
La réponse est **B. Embolie pulmonaire**
La complication la plus grave de la thrombose veineuse profonde (TVP) des membres inférieurs est **l'embolie pulmonaire (EP)** — le thrombus se détache et chemine par la veine cave inférieure → oreillette droite → ventricule droit → artère pulmonaire, pouvant entraîner un infarctus pulmonaire massif et une mort subite.
- **A** Varices superficielles → manifestation de la circulation collatérale en phase chronique de la TVP, pas une complication grave
- **C** Spasme artériel avec ischémie du membre → observé dans la TVP de type phlegmatia cerulea dolens ; grave mais incidence bien inférieure à l'EP
- **D** Ulcère du membre inférieur → séquelle de phase chronique, pas la plus grave
- **E** Obstruction de la veine cave → rare, généralement le résultat de l'extension proximale de la TVP
La menace la plus mortelle pour les patients atteints de TVP est **le détachement du thrombus menant à l'embolie pulmonaire**, ce qui explique pourquoi la TVP aiguë nécessite une anticoagulation immédiate et, en cas de contre-indication, la pose d'un filtre de veine cave inférieure.
```

## À propos de l'auteur

**Xiao Lv Lv (xllgreen)** — [xllgreen.github.io](https://xllgreen.github.io) — Étudiant en médecine au Jiujiang University College of Clinical Medicine · Geek technophile

## Support technique

<br>
Projet PDF2App : https://pdf2app.cn
<br>
Microsoft Visual Studio Code : https://code.visualstudio.com/
<br>
Claude Code pour VS Code : https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>API DeepSeek : https://platform.deepseek.com/
© 2026 Hangzhou DeepSeek Artificial Intelligence Basic Technology Research Co., Ltd. Tous droits réservés
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>API Xiaomi Mimo : https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## Licence

Le contenu de ce projet est compilé à partir de *Chirurgie*, 10e édition (People's Medical Publishing House) et est fourni à des fins d'étude et de référence uniquement.

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FSurgery-PMPH-10edition-&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&legend=top-left" />
 </picture>
</a>
