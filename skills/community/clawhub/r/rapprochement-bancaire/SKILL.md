---
name: rapprochement-bancaire
description: Moteur comptable quotidien du cabinet. Analyse les dossiers clients déjà classés par organisation-documents, rapproche les paiements avec les factures, valide la TVA, maintient followup.json / relances.json / anomalies.json. Le travail réel est fait par scripts/main.py (qui appelle scripts/extract.py). Ne traite jamais les e-mails, ne classe jamais de documents.
license: Interne — usage privé OpenClaw
---

# Skill `rapprochement-bancaire`

> Moteur d'état. Travaille uniquement sur l'arborescence `clients/<slug>/...` produite par `organisation-documents`.
> **Le travail réel est fait par `scripts/main.py`** (qui appelle `scripts/extract.py` pour toute l'extraction de texte). Ce skill = quand le lancer + comment rendre compte.

---

## ⚠️ Règle absolue — EXÉCUTION DU SCRIPT (non négociable)

**Pour chaque invocation, la SEULE action correcte est d'exécuter la commande :**

```bash
python3 scripts/main.py <racine_clients>
```

puis de lire les `followup.json` / `relances.json` / `anomalies.json` par client + le `compta_batch_report_<date>.json` consolidé, et de relayer au comptable.

### ❌ INTERDIT

- **Réimplémenter le rapprochement en Python inline / pseudo-code.** La logique (Pass 1 par référence, Pass 2 fuzzy, validation TVA, détection des anomalies, statuts overdue/partial, génération des relances) est dans `scripts/main.py`. La refaire à la main est garanti de diverger.
- **Écrire `followup.json` / `relances.json` / `anomalies.json` à la main.** C'est le script qui le fait, dans son format exact (liste d'objets avec les champs `invoice_id`, `type`, `amount`, `status`, `bank_matched`, `matched_tx`, …). Toute autre forme (dict keyé, champs `payments` / `amount_paid` ad hoc) casse les lectures ultérieures.
- **Modifier le format des fichiers de sortie.** Le format est contractuel entre ce skill et d'éventuels skills aval (`relances`, dashboards).

### ✅ OBLIGATOIRE

1. Exécuter la commande shell ci-dessus.
2. Lire les fichiers produits.
3. Relayer au comptable un tableau lisible par client (factures payées / en attente / partielles / overdue, anomalies — en mettant en avant les **bloquantes**).

### Si le script échoue

Signale l'erreur exacte (stderr). Ne rejoue PAS le batch à la main.

> Pourquoi : on a déjà eu un run où l'agent a produit un `followup.json` au mauvais format (dict avec clés `"in/N"`, champs `payments`/`amount_paid`/`amount_remaining` au lieu de `bank_matched`/`status`). Conséquence : aucun outil ni skill aval ne pouvait l'exploiter. Le script génère le bon format à tous les coups.

---

## Exécution

```bash
python3 scripts/main.py [<racine_clients>]
# racine_clients par défaut : ~/.openclaw/workspace/clients
```

À lancer :
- une fois par jour (idéalement la nuit), sur tous les clients ;
- ou immédiatement après un trigger `rapprochement-bancaire` émis par `organisation-documents`.

Le script :

1. **Parcourt** `clients/*` en ignorant les dossiers techniques `_*` (`_a-identifier`, `_incomplet`, `_non-attribue`, `_cabinet`).
2. **Périodes traitées** : mois courant + mois précédent, plus tout mois ancien non verrouillé (`batch.lock.json` absent). Un mois verrouillé n'est pas retraité.
3. **Factures** : nom de fichier conventionnel (`AAAA-MM-JJ_N°Facture_Contrepartie_MontantTTC.pdf`) → `invoice_id` + montant. Si le nom n'est pas exploitable, lecture du contenu via `extract.py`. Si toujours rien → anomalie `facture_illisible`.
4. **Relevés bancaires** : transactions extraites ligne par ligne via `extract.py` (`DATE | LIBELLÉ | MONTANT | CR/DB`), avec la référence facture si le libellé contient `REF <id>` ou `FACT <id>`. Aucune transaction extractible → anomalie `releve_non_parseable`.
5. **Rapprochement** (montant comparé en valeur absolue : une facture `out` est encaissée par un crédit, une `in` réglée par un débit) :
   - **Pass 1** — réf facture : transaction dont `invoice_ref == facture.invoice_id`. Montant exact (±1 €) → `paid` ; montant inférieur → `partial` (conserve `amount_paid`, `amount_remaining`) ; supérieur → `paid` + `overpaid_by`.
   - **Pass 2** — fuzzy : `|montant| ±1 €` ET similarité libellé / contrepartie ≥ 0.6.
   - aucun match + échéance dépassée → `overdue`.
6. **Validation TVA** de chaque facture : si `|TVA déclarée − TVA attendue| / TVA attendue > 5 %` (TVA attendue = `TOTAL HT × taux`) → anomalie `tva_incorrecte` (TVA 0 % / exonération ignorée).
7. **Anomalies** : voir tableau ci-dessous.
8. **Relances** : `overdue` / `partial` / `unpaid` hors délai → step selon ancienneté.
9. Écrit `clients/<slug>/followup.json`, `relances.json`, `anomalies.json`, et un rapport consolidé `compta_batch_report_<date>.json`.

**Après l'exécution**, lire le rapport et relayer au comptable un tableau lisible par client (factures payées / en attente, relances, anomalies — en mettant en avant les anomalies **bloquantes**). Jamais de chemins techniques.

---

## Statuts de facture (`followup.json`)

| Statut | Sens |
|--------|------|
| `unpaid` | non échue, aucun paiement |
| `paid` | paiement confirmé (rapprochement réussi) |
| `partial` | paiement partiel — `amount_paid` + `amount_remaining` conservés |
| `overdue` | échéance dépassée, aucun paiement |

---

## Anomalies (`anomalies.json`)

**Bloquantes** (empêchent la clôture de la période) :

| Type | Condition |
|------|-----------|
| `doublon_paiement` | même date + montant + libellé |
| `tva_incorrecte` | écart TVA calculée / déclarée > 5 % |
| `facture_manquante` | une ligne du relevé cite un n° de facture (`REF`/`FACT`) absent du dossier, montant > 1 000 € |
| `paiement_orphelin` | crédit > 1 000 € sans aucune référence ni facture |

**Non bloquantes** (signalées, clôture possible) :

| Type | Condition |
|------|-----------|
| `facture_manquante` | n° de facture cité au relevé mais absent, montant ≤ 1 000 € |
| `paiement_orphelin` | crédit ≤ 1 000 € sans référence |
| `releve_non_parseable` | aucune transaction extractible d'un relevé |
| `facture_illisible` | facture dont ni le nom ni le contenu ne donnent n° + montant |
| `invoice_overdue` | facture non payée, échéance dépassée |

> `facture_manquante` ≠ `paiement_orphelin` : le premier = paiement qui **cite** un n° de facture qu'on n'a pas reçu (le client a oublié de transmettre la pièce) ; le second = encaissement sans aucune référence.

---

## Relances (`relances.json`)

| Ancienneté du retard | Step |
|----------------------|------|
| ≤ 30 j | 1 |
| ≤ 60 j | 2 |
| ≤ 90 j | 3 |
| > 90 j | escalation |

Pour `partial` : mention explicite `"Solde restant dû : X,XX €"`.

---

## Clôture de période

Le script crée `clients/<slug>/<AAAA>/<MM>/batch.lock.json` quand : aucune anomalie **bloquante** sur la période, hash des fichiers stable depuis 7 jours, aucun statut `unpaid`/`overdue` non justifié. Les périodes verrouillées ne sont jamais retraitées sauf changement de hash.

---

## Règles critiques

- Ne jamais supprimer de données. Ne jamais retraiter un mois verrouillé.
- `followup.json` est un **cache reconstructible** : les PDFs classés restent la vérité. Le batch peut tout recalculer depuis zéro.
- `clients.json` est lu seulement (maintenu par `organisation-documents`), jamais écrit ici.
- Toute l'extraction de texte passe par `scripts/extract.py` — source unique, pas de logique de parsing dupliquée ici.

---

## Philosophie

```
organisation-documents  →  classe les pièces, déduit clients.json
rapprochement-bancaire            →  rapproche, valide, reconstruit l'état comptable  (scripts/main.py)
relances                →  décision différée
```

Le système doit pouvoir être recalculé intégralement à partir des documents classés.
