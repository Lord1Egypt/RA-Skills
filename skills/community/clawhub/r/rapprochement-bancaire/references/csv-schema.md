# Référence — Schéma CSV de rapprochement & état persisté

> Référence chargée à la demande par `rapprochement-bancaire`. Format du CSV, enum `anomalie`, schéma de `rapprochement-state.json`.

---

## Localisation du CSV

```
clients/<slug>/<AAAA>/<MM>/rapprochement.csv
```

Un fichier par (client, mois). Réécrit en entier à chaque run du mois concerné (idempotent). Pas d'append.

---

## Encodage et locale

- **Encoding** : UTF-8 avec BOM (`﻿` en tête) — pour Excel français qui sinon mojibake.
- **Séparateur** : `;` (semicolon) — convention française, évite la confusion avec décimales `,`.
- **Décimal** : `,` (virgule).
- **Date** : `AAAA-MM-JJ` (ISO 8601, lisible par tout tableur).
- **Saut de ligne** : `\r\n` (CRLF) — compatibilité Windows / Excel.
- **Quotes** : `"` autour des champs qui contiennent `;`, `"`, ou `\r\n`. Doubler les `"` internes (`""`).

---

## Colonnes du CSV

| #  | Colonne                | Type          | Description                                                                                  |
| -- | ---------------------- | ------------- | -------------------------------------------------------------------------------------------- |
| 1  | `ligne`                | int           | Numéro de ligne séquentiel (1, 2, 3, …) — facilite la référence dans les conversations       |
| 2  | `source`               | enum          | `transaction` (ligne de relevé), `facture_non_payee` (facture sans transaction)              |
| 3  | `compte`               | string        | Banque ou compte (ex : `BNP-courant`, `Qonto-pro`) — vide si `source=facture_non_payee`      |
| 4  | `date`                 | date          | Date transaction OU date d'émission de la facture                                            |
| 5  | `libelle`              | string        | Libellé brut du relevé ou raison sociale + n° facture                                       |
| 6  | `montant`              | decimal       | Signé (`+` crédit, `-` débit)                                                                |
| 7  | `categorie_auto`       | enum          | `match` / `frais_bancaires` / `rh_charges` / `transfert_interne` / `non_categorise`         |
| 8  | `match_facture`        | string        | Numéro de facture matchée — vide si non-match                                                |
| 9  | `match_emetteur`       | string        | Raison sociale de la facture matchée                                                         |
| 10 | `match_mois_origine`   | string        | `AAAA-MM` du mois d'origine de la facture si différent du mois courant — vide sinon          |
| 11 | `confidence`           | enum          | `fort` / `moyen` / `faible` / `aucun`                                                        |
| 12 | `anomalie`             | enum          | cf. table ci-dessous — vide si aucune                                                        |
| 13 | `montant_attendu`      | decimal       | Montant TTC de la facture matchée — vide si non-match                                        |
| 14 | `ecart`                | decimal       | `montant - montant_attendu` — vide si non-match                                              |
| 15 | `candidats`            | string        | Liste de numéros de facture séparés par `|` si `anomalie=match_ambigu`                       |
| 16 | `commentaire`          | string        | Champ libre, éditable par le comptable. Préservé entre runs                                  |

---

## Enum `anomalie`

| Valeur                      | Sens                                                                                                |
| --------------------------- | --------------------------------------------------------------------------------------------------- |
| (vide)                      | Aucune anomalie                                                                                     |
| `paiement_orphelin`         | Transaction débit sans facture in correspondante                                                    |
| `encaissement_sans_facture` | Transaction crédit sans facture out correspondante                                                  |
| `facture_non_payee`         | Facture out avec échéance dépassée et pas de paiement détecté                                       |
| `montant_incoherent`        | Match trouvé mais `abs(ecart) > tolerance` (typiquement escompte ou frais)                          |
| `doublon_paiement`          | Plusieurs transactions matchent la même facture avec somme > `montantTTC`                           |
| `paiement_partiel`          | Transaction crédit < `montantTTC` de la facture matchée                                             |
| `match_ambigu`              | Plusieurs candidats avec scores proches (écart < 0.10) — non choisi automatiquement                 |
| `facture_double_classement` | La facture matchée est référencée dans 2 mois différents de `index.json` — inconsistance à corriger |
| `libelle_suspect`           | Mots-clés louches (URL raccourcie, IBAN inconnu) — flag manuel, pas bloquant                        |

---

## Tri des lignes

1. `date` croissante.
2. À date égale, `source=transaction` avant `source=facture_non_payee`.
3. À source égale, `compte` alphabétique puis `ligne` (ordre du relevé).

Permet une lecture chronologique pour le comptable.

---

## Préservation du `commentaire`

La colonne `commentaire` est la **seule** qui survit entre les runs. À chaque réécriture :

1. Lire le CSV existant en mémoire.
2. Indexer les commentaires par `(date, montant, libelle_hash)`.
3. Après le matching, restaurer les commentaires sur les lignes qui correspondent.
4. Les lignes nouvelles ont `commentaire` vide.

Si le comptable édite manuellement d'autres colonnes → écrasées au prochain run. Une bannière en tête du fichier le rappelle :

```
# rapprochement.csv — ACME SA — 2026/04
# Généré par rapprochement-bancaire — réécrit à chaque run.
# SEULE la colonne 'commentaire' est préservée entre runs. Autres modifs perdues.
```

---

## Exemple de CSV

```csv
ligne;source;compte;date;libelle;montant;categorie_auto;match_facture;match_emetteur;match_mois_origine;confidence;anomalie;montant_attendu;ecart;candidats;commentaire
1;transaction;BNP-courant;2026-04-03;"VIR FAVEUR TRENDEX TECH F-2026-03-007";5800,00;match;F-2026-03-007;Trendex Tech;2026-03;fort;;5800,00;0,00;;
2;transaction;BNP-courant;2026-04-05;"PRLV ORANGE PRO F-2026-04-1287";-348,50;match;F-2026-04-1287;Orange Pro;;fort;;-348,50;0,00;;
3;transaction;BNP-courant;2026-04-12;"VIR FAVEUR FOO SAS";1248,00;match;F-2026-03-008;Foo SAS;2026-03;moyen;;1248,00;0,00;;
4;transaction;BNP-courant;2026-04-15;"CB SNCF PARIS-LYON";-84,50;match;;SNCF;;faible;;;;;
5;transaction;BNP-courant;2026-04-22;"PRLV URSSAF";-1870,00;rh_charges;;;;aucun;;;;;
6;transaction;BNP-courant;2026-04-28;"CHQ N° 4521 - FOURN MAT";-720,00;non_categorise;;;;aucun;paiement_orphelin;;;;à investiguer
7;facture_non_payee;;2026-04-15;"F-2026-04-013 - ACME Corp";5800,00;;F-2026-04-013;ACME Corp;;aucun;facture_non_payee;5800,00;;;
```
