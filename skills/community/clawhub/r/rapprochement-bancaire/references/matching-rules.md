# Référence — Règles de matching transactions ↔ factures

> Référence chargée à la demande par `rapprochement-bancaire`. Détaille la cascade, la fenêtre de date, le scoring de confiance et les cas limites.

---

## Normalisation préalable

### Côté transaction (extraite du relevé)

| Champ                | Normalisation                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| `montant`            | Décimal, signé (`+` crédit, `-` débit), arrondi 0,01 €                                                       |
| `date`               | ISO 8601 (`YYYY-MM-DD`)                                                                                       |
| `libelle`            | Trim, espaces multiples → simple espace, lowercase                                                            |
| `libelle_tokens`     | `libelle` splitté par espaces / ponctuation, tokens ≥ 3 caractères, sans stop-words bancaires (`vir`, `prlv`, `cb`, `chq`, `faveur`, `de`, `du`, `de la`) |

### Côté facture (extraite de l'index)

| Champ                | Normalisation                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------ |
| `montantTTC`         | Décimal positif (le sens vient du `categorie`: `achat` = débit, `vente` = crédit)         |
| `dateEmission`       | ISO 8601                                                                                   |
| `emetteur_normalise` | lowercase, accents retirés, suffixes juridiques retirés (`SA`, `SAS`, `SARL`, `EURL`, `Ltd`) |
| `numeroFacture`      | Conservé tel quel + variante numérique pure (`F-2026-04-1287` → aussi `20260412 87`)      |

---

## Cascade de matching (par transaction)

Pour chaque transaction, parcourir les factures du mois (et du mois précédent + suivant — cf. fenêtre date) et calculer un **score** :

```
score = match_montant × poids_montant
      + match_label × poids_label
      + match_date × poids_date
```

Poids par défaut :

- `poids_montant` : 0.5
- `poids_label` : 0.3
- `poids_date` : 0.2

### Score `match_montant`

| Condition                                                           | Score |
| ------------------------------------------------------------------- | ----- |
| `abs(montant - montantTTC) ≤ 0.01`                                  | 1.0   |
| `abs(montant - montantTTC) / montantTTC < 0.02` (escompte typique)  | 0.6   |
| Autre                                                               | 0.0   |

**Sens** : `montant > 0` → ne peut matcher qu'une facture `vente`. `montant < 0` → ne peut matcher qu'une facture `achat`. Pas de cross-match.

### Score `match_label`

Cascade — première règle qui matche :

| Condition                                                                    | Score |
| ---------------------------------------------------------------------------- | ----- |
| `libelle` contient `numeroFacture` (variante numérique pure incluse)         | 1.0   |
| `libelle_tokens` contient un token de `emetteur_normalise` (longueur ≥ 4)    | 0.8   |
| `libelle_tokens` contient un préfixe / suffixe de l'émetteur (Levenshtein ≤ 2) | 0.5   |
| Aucun                                                                        | 0.0   |

### Score `match_date`

| Condition                                            | Score |
| ---------------------------------------------------- | ----- |
| `abs(date - dateEmission) ≤ 3 j`                     | 1.0   |
| `abs(date - dateEmission) ≤ 30 j`                    | 0.7   |
| `abs(date - dateEmission) ≤ 60 j`                    | 0.3   |
| Au-delà                                              | 0.0   |

---

## Classification du score final

| Score agrégé | Confiance | Action                                                            |
| ------------ | --------- | ----------------------------------------------------------------- |
| ≥ 0.85       | `fort`    | Ligne CSV matchée + update `followup.md` (`payée <date>`)         |
| 0.65 – 0.85  | `moyen`   | Ligne CSV matchée + update `followup.md` (`payée ? <date>`, avec `?`) |
| 0.45 – 0.65  | `faible`  | Ligne CSV `match suggéré` mais **pas** d'update followup          |
| < 0.45       | aucun     | Transaction reste `unmatched`                                     |

Si une transaction a **plusieurs candidats ex-aequo** (écart < 0.10 entre top-2) → marquer `match_ambigu` dans le CSV et ne pas écrire dans followup. Lister les N candidats dans la colonne `candidats`.

---

## Fenêtre de date et débordement de mois

Une facture émise le 28/03 peut être payée le 02/04. Donc :

- Charger les factures des **3 mois** : précédent, courant, suivant, autour du mois de la transaction.
- Si match avec une facture d'un autre mois → l'écrire dans le CSV du mois de la **transaction**, mais annoter `facture_mois_origine` = mois de la facture.
- Mettre à jour le `followup.md` du **mois de la facture** (pas celui de la transaction).

---

## Cas limites

### Frais bancaires / commissions

Transaction avec `libelle` contenant un mot-clé d'agios :

- `frais`, `commission`, `cotisation`, `agios`, `interets`, `tenue de compte`

→ Pas de matching tenté. Annoter `categorie_auto: frais_bancaires` dans le CSV. Ne pas alerter (comportement normal).

### Salaires / charges sociales

Mots-clés : `salaire`, `urssaf`, `dsn`, `cipav`, `madelin`, `mutuelle`, `prevoyance`.

→ Pas de matching. Annoter `categorie_auto: rh_charges`. Pas d'alerte par défaut, mais flag possible si montant aberrant vs historique (v0.3+).

### Virements internes

Mots-clés : `virement interne`, `vir entre comptes`, `transfert`.

→ Pas de matching. Annoter `categorie_auto: transfert_interne`. Pas d'alerte.

### Encaissements partiels

Si `montant < montantTTC` ET `montant > 0` ET match label + date OK :

- Annoter `paiement_partiel` dans le CSV.
- Calculer pourcentage : `(montant / montantTTC) × 100`.
- Update `followup.md` : `partielle (X%)`.
- Au prochain run, chercher les transactions complémentaires pour atteindre 100 %.

### Multi-paiements pour une facture

Une facture peut être payée en plusieurs fois (acompte + solde). Si plusieurs transactions matchent la même facture avec sens cohérent et somme = `montantTTC` → OK, listées comme un groupe dans le CSV avec un identifiant `match_group`.

Si somme > `montantTTC` → anomalie `doublon_paiement`.

### Devise étrangère

Hors scope v0.1. Si une facture USD et un encaissement EUR matchent par hasard sur le montant → faux positif. Mitigation v0.2 : taux de change + tolérance plus large.

### Relevés multi-comptes

Un client peut avoir plusieurs comptes (cf. `bank-statements/2026-04_BNP-courant.pdf` et `bank-statements/2026-04_Qonto-pro.pdf`). Toutes les transactions de tous les comptes du mois sont mises en pool commun pour le matching. Le CSV indique la source dans une colonne `compte`.

### Reclassement d'une facture après matching

Si une facture est reclassée par `organisation-documents` (mauvais client, mauvaise catégorie) APRÈS un matching :

- Le `rapprochement-state.json` détecte le changement de chemin et marque le mois `dirty: true`.
- Au prochain run, le matching est recalculé pour ce mois → le CSV est régénéré, `followup.md` mis à jour.
- L'ancien match est purgé de l'état précédent.

---

## Anti-faux-positifs

Sources connues de faux positifs et garde-fous :

| Source                                                          | Garde-fou                                                                                  |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 2 fournisseurs facturent le même montant rond (`100,00 €`)      | Required : label OU date proche, jamais montant seul                                       |
| Abonnement mensuel identique → faux match sur le mauvais mois   | Fenêtre date prioritaire si plusieurs candidats même montant                               |
| Émetteur générique (`Amazon`) qui matche partout                | Liste noire de tokens trop génériques : `paiement`, `achat`, `commande`, `service`, `web` |
| Transaction de l'année précédente reposté (relevé re-généré)    | Si date < `mois - 90 j` → ignorée                                                          |

**Règle absolue** : un match `fort` ne doit jamais écraser une donnée déjà éditée par le comptable dans `followup.md` (statut paiement, prochaine relance). En cas de conflit, garder la valeur humaine et lister le conflit dans le CSV avec `anomalie=libelle_suspect` + commentaire automatique « override manuel respecté ».
