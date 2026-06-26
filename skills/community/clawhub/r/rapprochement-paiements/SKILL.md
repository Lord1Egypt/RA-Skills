---
name: rapprochement-paiements
description: Étape ⑤ du pipeline comptable. Rapproche les opérations bancaires avec les factures et notes de frais classées, et rend compte au comptable de l'état des règlements par client. À utiliser dès que le comptable veut faire le point sur les paiements : « rapprochement », « lettrage », « où en sont les paiements ? », « qui n'a pas payé ? », « rapproche les relevés avec les factures », ou après que de nouvelles pièces ont été classées par le pipeline. Pour chaque facture : réglée / partielle / impayée / en retard. Signale les opérations à justifier (facture manquante / paiement orphelin), les relevés non lisibles et les paiements en double. Écrit, par client, les deux fichiers que lit le backend : company.json (identité) et rapprochement.json (suivi, format periods[]). Lecture seule sur l'arborescence des pièces : ne classe rien (classement-document) et ne déplace aucun fichier.
license: Interne — usage privé OpenClaw
---

# Skill `rapprochement-paiements` — étape ⑤

> Action humaine : **pointer les relevés avec les factures et dire qui a payé quoi.**
> Lecture seule sur `clients/<slug>/…`. Écrit l'état du suivi, dont les deux
> fichiers que le backend Pocket-Claw lit : `company.json` + `rapprochement.json`.

Le travail est fait par `scripts/main.py`. Ce skill = quand le lancer, **la passe
vision obligatoire**, et comment en rendre compte.

---

## Comment l'utiliser

```bash
python3 scripts/main.py [<racine_clients>]      # défaut : ./clients
```

À lancer après un classement de nouvelles pièces (le pipeline le fait
automatiquement), ou quand le comptable demande un point sur les paiements. Le
script retraite tout le dossier (cache reconstructible), écrit un
`rapprochement.json` par client + un rapport consolidé, puis imprime un résumé et
un **auto-contrôle d'invariant**.

### La passe vision est OBLIGATOIRE à chaque run

Le parseur déterministe ne fait que PROPOSER ; c'est un **gate arithmétique** qui
porte la confiance. Un relevé dont `ouverture + Σ opérations ≠ clôture`, une
facture dont `HT + TVA ≠ TTC`, ou un PDF scanné sans texte sont **signalés** dans
`needs_vision.json` au lieu d'être trustés en silence. Quand le run en signale, tu
DOIS enchaîner :

```bash
python3 scripts/resolve_vision.py <racine_clients>
```

→ il prépare, pour chaque document, les **images des pages** + un squelette de
sidecar. Tu **lis les images** (outil Read), corriges le squelette (montants
SIGNÉS : crédit +, débit − ; champ illisible = `null`, jamais inventé ; pour un
relevé, vérifie ouverture + Σ = clôture), sauves dans `<pdf>.vision.json`, puis
relances `main.py`. Le sidecar fait alors **autorité** — mais repasse par le même
gate : un sidecar qui ne tombe toujours pas juste est RE-signalé (jamais masqué).

---

## Comment ça rapproche (et pourquoi c'est fiable)

Pour chaque facture (ou note de frais), on cherche l'opération qui la solde, avec
des garde-fous qui évitent les faux rapprochements :

- **Le sens compte.** Une **vente** (`out`) se solde par un **crédit**, un **achat**
  (`in`, factures fournisseurs ET notes de frais) par un **débit**. Jamais de
  comparaison en valeur absolue.
- **Jamais le montant seul.** Un rapprochement exige le bon montant **et** soit la
  référence facture, soit le nom de la contrepartie dans le libellé, soit une date
  proche. Deux factures à 100 € pile ne se confondent pas. À score égal, la date
  départage ; sinon on n'écrit rien et on signale `match_ambigu`.
- **Une transaction = une facture.** Chaque opération est consommée une seule fois
  (un paiement ne solde jamais deux factures). Les acomptes + solde d'une même
  référence sont sommés.
- **Le bruit est reconnu.** Frais bancaires, salaires/charges (URSSAF…), impôts,
  espèces, virements internes et virements de particuliers sont catégorisés
  (`excluded_bank_lines`) : jamais rapprochés, jamais signalés comme suspects.
- **Un relevé non réconcilié ne génère pas de fausses anomalies.** Ses opérations
  servent encore au matching, mais ne produisent ni orphelin ni doublon tant que la
  vision ne l'a pas corrigé (rien de flaggé n'est présenté comme fiable).

Statuts de facture : `paid`, `partial` (solde restant calculé), `unpaid`,
`overdue` (échéance dépassée → relance proposée).

---

## Ce qu'on écrit pour le backend : `rapprochement.json` (periods[])

Un objet `{"periods": [...]}`, une entrée par mois, **passée telle quelle au
front** (snake_case exact). Par période : `bank_statements_count`,
`bank_transactions_count`, `bank_matched_count`, et :

- `invoices[]` — `invoice_id, type, counterparty_name, amount, issued_date,
  due_date, status, bank_matched, amount_paid, amount_remaining, anomalies[]`.
- `unmatched_bank_lines[]` — opération sans facture en face : `type`
  (`facture_manquante` = débit sans justificatif, `paiement_orphelin` = crédit sans
  facture de vente), `label, amount` (signé), `date, invoice_ref`.
- `excluded_bank_lines[]` — opérations non facturables (avec `category`).
- `period_anomalies[]` — `doublon_paiement`, `releve_non_parseable`,
  `facture_illisible`.
- `relances[]` — `invoice_id, counterparty, amount, due_date, days_late, step, …`.

**Invariant garanti** (auto-contrôlé à chaque run, jamais KO) : pour chaque
période, `bank_matched_count + len(unmatched) + len(excluded) ==
bank_transactions_count` — toute opération du relevé est représentée exactement une
fois. `company.json` (identité) est rafraîchi en parallèle. Les mois passés
entièrement résolus sont **verrouillés** (`batch.lock.json`) et conservés tels
quels ; un fichier qui change rouvre le mois.

---

## Comment en rendre compte au comptable

Dans le ton habituel, sans jargon ni chemin technique. Structure :

1. **Les règlements** — combien de factures réglées / en attente / en retard, par client.
2. **À relire (vision)** — si des documents sont signalés, dis-le et fais la passe
   (c'est une étape du run, pas un échec).
3. **À surveiller** — les paiements en double (argent compté deux fois) et les TVA
   incohérentes, en premier.
4. **À vérifier** — les mouvements sans facture, surtout les **encaissements** (une
   vente à facturer ?) et les retards (relance à envoyer ?).

Pour un rapprochement `medium`, mentionne le doute (« réglée, sous réserve »).
Quand des relances sont dues, propose de les envoyer (niveaux J+30 / J+60 / J+90 /
escalade). Ne jamais escalader sans l'accord du comptable.

---

## Limites assumées

- Le déterminisme est MINIMAL (fast-path pour docs propres) ; toute la fiabilité
  vient du **gate + vision**. On ne patche pas le parseur banque par banque : un
  format inconnu échoue le gate → vision (robuste), jamais d'erreur silencieuse.
- Une note de frais se règle par un décaissement (type `in`) et **ne se relance
  pas** (remboursement interne au salarié).
- Ne classe pas les pièces (`classement-document`) et ne rédige pas les relances
  (workflow e-mail). Il rapproche, écrit l'état, et rend compte.
