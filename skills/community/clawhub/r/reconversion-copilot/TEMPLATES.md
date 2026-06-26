# Templates Reconversion Copilot

## DIAGNOSTIC

Remplir CHAQUE cellule. Ne pas laisser de placeholder.

```
DIAGNOSTIC EXPRESS - CARTE DE COMPETENCES

PROFIL
- Poste actuel : [POSTE]
- Secteur : [SECTEUR]
- Experience totale : [X] ans
- Management : [Oui/Non - details]

HARD SKILLS
| Competence | Niveau | Transferable data ? |
|-----------|--------|---------------------|
| [skill] | [debutant/intermediaire/avance] | [Oui direct / Avec adaptation / Non] |

SOFT SKILLS
| Competence | Contexte | Valeur data |
|-----------|---------|-------------|
| [skill] | [contexte] | [Elevee/Moyenne/Faible] |

PROXIMITE DATA
- Reporting : [outils et frequence]
- Donnees manipulees : [type et volume]
- SQL/BI : [niveau]
- Contact equipes tech/data : [description]

SCORES DE COMPATIBILITE
| Role | Score /10 | Justification |
|------|-----------|---------------|
| Data Analyst | [X] | [pourquoi] |
| AMOA Data | [X] | [pourquoi] |
| PO Data | [X] | [pourquoi] |
| BI Lead | [X] | [pourquoi] |

Scoring : +1 management, +1 SIRH/ERP, +1 manipule donnees. -2 si < 5 ans exp. -1 si zero proximite data.
7-10 = realiste. 4-6 = possible avec effort. 1-3 = difficile.

VERDICT
[3-4 phrases honnetes : forces, faiblesses, recommandation role principal, timeline estimee]
```

## FICHE METIER

Une fiche par role. Remplir chaque section.

```
FICHE METIER : [ROLE]

DESCRIPTION
[2-3 phrases : ce que fait ce pro au quotidien]

COMPETENCES REQUISES
| Competence | Requis | Niveau actuel du candidat | Gap |
|-----------|--------|--------------------------|-----|
| [comp] | [niveau] | [niveau] | [a combler / OK] |

SALAIRE FRANCE (2025-2026)
- Paris : [fourchette]
- Province : [fourchette]
- En reconversion 10+ ans exp : [fourchette realiste]

MARCHE
- Tendance : [croissante/stable]
- Secteurs : [liste]
- Code ROME : [code]

REALISME POUR CE PROFIL
[Analyse honnete en 2-3 phrases]
```

Donnees de reference :
- Data Analyst : ROME M1403/M1805. Paris 38-70k. Province 32-60k.
- AMOA Data : ROME M1802. Paris 42-80k.
- PO Data : ROME M1805. Paris 45-90k.
- BI Lead : ROME M1805/M1802. Paris 50-80k.

## PLAN

Roadmap avec actions concretes par mois. Pas de vague "Phase 1 : 3 mois".

```
PLAN DE TRANSITION

OBJECTIF : [Role cible] en [X mois]
SITUATION : [en poste / recherche / conge]

MOIS 1-2 : FONDATIONS
- [ ] [Action concrete 1 avec ressource precise]
- [ ] [Action concrete 2]
- [ ] [Action concrete 3]
Temps : [X]h/semaine

MOIS 3-4 : MONTEE EN COMPETENCE
- [ ] [Actions specifiques]
- [ ] [Projet portfolio : nom + description + dataset]
- [ ] [Networking : evenement ou communaute precise]

MOIS 5-6 : POSITIONNEMENT
- [ ] CV repositionne (voir template CV)
- [ ] LinkedIn optimise
- [ ] [X] candidatures/semaine
- [ ] Preparation entretiens

FORMATIONS
| Formation | Organisme | Duree | Cout | CPF |
|----------|-----------|-------|------|-----|
| [nom] | [organisme] | [duree] | [prix] | [Oui/Non] |

CERTIFICATIONS
| Certification | Organisme | CPF |
|-------------|-----------|-----|
| Google Data Analytics | Coursera | Non |
| Power BI PL-300 | Microsoft | Oui |

PROJETS PORTFOLIO
1. [Nom] : [description, dataset, competences demontrees]
2. [Nom] : [description, dataset, competences demontrees]

FINANCEMENT
- CPF : moncompteformation.gouv.fr
- Transitions Pro (ex-CIF)
- France Travail : AIF, AFPR, POEI
- Employeur : plan de dev des competences
```

## CV/LINKEDIN

Produire le document FINAL, pas des conseils. Traduction de competences.
Verbes data : analyser, piloter, structurer, modeliser, automatiser, extraire, croiser, restituer, monitorer.

```
[PRENOM NOM]
[Role cible]
[Ville] | [Email] | [LinkedIn]

[Accroche 2-3 lignes positionnant l'experience comme atout data]

EXPERIENCE PROFESSIONNELLE

[Poste] | [Entreprise] | [Dates]
- [Chaque bullet TRADUIT en langage data avec chiffres]

Exemples de traduction :
AVANT : "Gestion du SIRH pour 2000 collaborateurs"
APRES : "Pilotage du referentiel de donnees RH (2000 collaborateurs) : qualite, coherence, RGPD"

AVANT : "Tableaux de bord RH"
APRES : "Conception dashboards RH (Power BI) : KPIs absenteisme, turnover — reduction reporting 40%"

AVANT : "Coordination equipe IT"
APRES : "Interface metier-IT migration SIRH : expression de besoin, recette, conduite du changement (150 users)"
```

LinkedIn :
```
TITRE : [Role cible] | [Expertise metier] | [Differentiant]
Ex : "AMOA Data | Ex-Responsable SIRH | Traduction metier-data"

RESUME :
1. Accroche percutante (1 phrase)
2. Parcours (2-3 phrases)
3. Pourquoi la data (2 phrases)
4. 3 bullet points differenciants
5. Ce que je cherche
```

Lettre de motivation :
```
Objet : Candidature [POSTE] - [ENTREPRISE]

[P1 : pourquoi cette entreprise - recherche faite, pas generique]
[P2 : 2-3 experiences traduites data avec chiffres]
[P3 : pourquoi la transition est logique + avantage vs profil data pur]
[P4 : ce que j'apporte concretement]
[Conclusion : dispo + CTA]
```

Pitch :
```
30 SEC : "Je suis [PRENOM], [role] depuis [X] ans en [secteur]. J'ai [realisation data]. J'evolue vers [cible] parce que [raison]. Mon avantage : [differentiant]."

2 MIN : Meme structure etendue avec exemple concret chiffre + actions de transition + valeur unique.
```

## ENTRETIENS

Generer les REPONSES REDIGEES, pas des conseils.

Questions transition :
Q: "Pourquoi cette reconversion ?"
R (STAR) : Situation → Task → Action → Result. Redigee avec les vraies experiences du candidat.
NE PAS dire : "j'en avais marre", "la data c'est l'avenir", "je veux gagner plus"

Q: "Pas d'experience technique data ?"
R : Retourner en avantage : expertise metier + comprehension donnees + maturite.

Q: "Pourquoi vous vs un junior data ?"
R : Autonomie, connaissance sectorielle, gestion projet, communication stakeholders.

Questions techniques par role :
- Data Analyst : SQL joins, valeurs manquantes, processus dashboard
- AMOA Data : cahier des charges data, interface metier-tech, priorisation
- PO Data : backlog data, user stories, mesure succes
- BI Lead : choix outil BI, gouvernance donnees, projet pilote

Negociation salariale :
- Ne pas partir de zero. L'experience metier a de la valeur.
- Viser au-dessus du junior : "Mon experience de [X] ans me positionne a [fourchette]."

## SUIVI

```
POINT HEBDOMADAIRE

1. Qu'as-tu fait cette semaine ?
2. Qu'est-ce qui a bloque ?
3. Objectif semaine prochaine ?

PROGRESSION
| Semaine | Objectif | Statut |
|---------|----------|--------|
| S1 | [objectif] | [fait/en cours/bloque] |
```

Rejet : "C'est normal. As-tu eu du feedback ? Un refus = signal sur le positionnement, pas un verdict."
Blocage > 2 mois : revoir objectif, role, plan. "C'est toujours ce que tu veux ?"
