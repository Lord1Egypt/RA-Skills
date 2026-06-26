---
name: tri-courrier-entrant
description: Étape ① du pipeline comptable. Trie un mail entrant comme le ferait une assistante qui ouvre son courrier : décide s'il concerne la comptabilité, en sort les pièces à traiter et les informations d'en-tête (expéditeur, domaine, objet) utiles pour reconnaître le client ensuite. À utiliser dès qu'un mail arrive et qu'il faut décider quoi en faire : « ce mail me concerne ? », « y a-t-il une facture là-dedans ? », tri d'un courrier reçu, première étape avant d'analyser une pièce. Ne lit pas le contenu des pièces (c'est analyse-piece-comptable) et ne range rien (c'est classement-document). Décision + normalisation, rien d'autre.
license: Interne — usage privé OpenClaw
---

# Skill `tri-courrier-entrant` — étape ①

> Action humaine : **ouvrir un mail et décider en un coup d'œil s'il mérite d'être traité.**
> Sort les pièces + l'en-tête utile. N'analyse pas les pièces, ne range rien.

C'est la porte d'entrée du pipeline. Son seul rôle : éviter qu'on analyse et range
du courrier qui n'a rien de comptable, et préparer un « dossier » propre pour la suite.

---

## Comment l'utiliser

```bash
echo '<mail.json>' | python3 scripts/tri.py
```

Entrée : le mail (expéditeur, objet, corps, date, identifiant, pièces jointes).
Sortie : un **dossier initial** que les étapes suivantes enrichiront.

```jsonc
{
  "relevant": true,
  "reason": "pièce jointe + mot-clé « facture »",
  "email": { "from", "domain", "subject", "date", "messageId" },
  "pieces":  [ { "filename", "path", "mimeType" } ],
  "ignored_attachments": [ { "filename", "reason" } ]
}
```

### Règle de pertinence

Un mail est retenu s'il porte **une pièce exploitable** (PDF, image, .eml, XML,
CSV/OFX) **ou** un **mot-clé comptable** (facture, paiement, TVA, relevé, avoir…).
Sinon il est écarté — on ne perd pas de temps dessus.

Les images (PNG/JPG) sont **gardées** : une facture peut être scannée ou
photographiée. C'est l'étape ② qui dira si l'image porte vraiment un document ;
un simple logo de signature finira naturellement en « non comptable » plus loin.

---

## Comment en rendre compte au comptable

En une phrase, dans le ton habituel, sans jargon : « Ce mail de … contient une
facture à traiter » ou « Ce mail ne concerne pas la comptabilité, je le laisse de
côté ». Ne mentionne jamais le script ni le JSON.

Quand le mail est pertinent, la suite logique est l'analyse de chaque pièce
(étape ②). En usage courant, c'est l'orchestrateur `pipeline-comptable` qui
enchaîne tout seul.

---

## Limites assumées

- Ne lit pas l'intérieur des pièces — il décide seulement si ça vaut le coup.
- Ne range rien, n'écrit aucun fichier.
- Un mail sans pièce mais avec un mot-clé est signalé « corps à lire » : c'est au
  comptable (ou à un skill dédié) de décider quoi en faire.
