#!/usr/bin/env python3
"""
Moteur du skill `rapprochement-bancaire`.

Travaille sur l'arborescence `clients/<slug>/...` produite par `organisation-documents` (scripts/main.py).
Toute l'extraction de texte est déléguée à `extract.py` (source unique).

Pour chaque période active :
  - lit les factures (nom de fichier conventionnel, sinon contenu PDF via extract.py)
  - lit les relevés bancaires (transactions ligne par ligne via extract.py)
  - rapproche chaque facture avec son paiement (Pass 1 = réf facture, Pass 2 = fuzzy)
  - valide la TVA de chaque facture
  - détecte les anomalies (doublon, facture manquante, orphelin, TVA, retard)
  - écrit followup.json / relances.json / anomalies.json par client
  - produit un rapport consolidé

Usage :
  python3 main.py [<racine_clients>]
  <racine_clients> par défaut : ./clients
"""

import hashlib
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("clients")
# Extraction = sous-processus (pdftotext/OCR) qui relâchent le GIL → des threads
# donnent un vrai parallélisme. On sur-souscrit modérément les cœurs.
WORKERS = max(1, int(os.environ.get("RAPPRO_WORKERS", min(8, (os.cpu_count() or 2) * 2))))
# Extensions de documents réels (relevés/justificatifs). On EXCLUT les sidecars et
# artefacts (.json de cache/vision, .md/.txt laissés par d'anciennes conversions
# Docling type `<pdf>.docling.md`) qui sinon seraient lus comme de faux relevés.
DOC_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp", ".heic"}


def is_doc_file(path):
    return path.is_file() and path.suffix.lower() in DOC_EXTS
TODAY = datetime.now(timezone.utc).date()
ACTIVE_MONTHS = {
    TODAY.strftime("%Y-%m"),
    (TODAY.replace(day=1) - timedelta(days=1)).strftime("%Y-%m"),
}


# ── IO ────────────────────────────────────────────────────────────────────

def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path, data):
    # Écriture ATOMIQUE : on écrit dans un .tmp puis on renomme (rename atomique sur
    # le même FS). Un run tué en plein écriture ne laisse donc jamais un followup.json
    # / rapport tronqué → la lecture aval (serveur) ne casse pas.
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def _cache_path(pdf_path):
    return Path(str(pdf_path) + ".extract.json")


def _md_path(pdf_path):
    """Transcription texte lisible à côté du PDF (`<pdf>.md`)."""
    return Path(str(pdf_path) + ".md")


def _content_hash(path):
    """MD5 du contenu — identifie deux fichiers byte-identiques (mêmes octets)
    quel que soit leur nom. Sert à dé-dupliquer les réimports (`X.pdf` vs
    `X__Banque.pdf`) sans dépendre d'un nommage fragile."""
    h = hashlib.md5()
    try:
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 16), b""):
                h.update(chunk)
    except OSError:
        return None
    return h.hexdigest()


def _write_transcription(pdf_path, text):
    """Écrit `<pdf>.md` : la transcription texte brute du PDF (pdftotext/OCR),
    pour relecture humaine. Idempotent (n'écrase pas si déjà présent). La source
    de vérité reste le PDF — ce `.md` est une aide à la consultation."""
    md = _md_path(pdf_path)
    if md.exists():
        return
    try:
        body = text.strip() or "(aucun texte extractible — PDF scanné/photo, voir l'image source)"
        md.write_text(
            f"# Transcription — {Path(pdf_path).name}\n\n"
            f"> Texte brut extrait par `extract.pdftext()` (pdftotext `-layout` / OCR tesseract).\n"
            f"> Aide à la relecture ; la source de vérité reste le PDF.\n\n"
            f"```text\n{body}\n```\n",
            encoding="utf-8")
    except OSError:
        pass


def _file_stamp(path):
    """Signature légère du fichier (taille + mtime) pour invalider le cache dès
    que le PDF change. Évite tout hash coûteux sur des centaines de fichiers."""
    st = Path(path).stat()
    return {"size": st.st_size, "mtime": int(st.st_mtime)}


def pdf_fields(pdf_path):
    """Champs extraits d'un PDF.

    Priorité des sources :
      1. `<pdf>.vision.json`  → AUTORITÉ (correction manuelle / passe vision).
      2. `<pdf>.extract.json` → cache de l'extraction géométrique (clé taille+mtime).
         Rend le run RÉENTRANT : tué en cours, on reprend sans tout ré-extraire.
      3. extraction géométrique `extract.py` (pdftotext + templates) → mise en cache.

    Plus de fallback Docling (≈20-25 s/PDF, ingérable sur des centaines de docs) :
    un document que le moteur géométrique ne lit pas de façon fiable part en VISION
    (le modèle relit les pages rasterisées — rapide, et seul recours fiable pour
    une *photo* de ticket sans couche texte, que pdftotext ne sait pas lire)."""
    sidecar = Path(str(pdf_path) + ".vision.json")
    if sidecar.exists():
        data = load_json(sidecar, None)
        if isinstance(data, dict) and data.get("kind"):
            data["source"] = "vision"
            # transcription `.md` quand même (le sidecar court-circuite l'extraction
            # mais on veut le texte brut lisible du PDF, surtout pour ces docs durs).
            if not _md_path(pdf_path).exists():
                _write_transcription(pdf_path, extract.pdftext(pdf_path))
            # Le sidecar vision NE court-circuite PAS le gate : un relevé relu en
            # vision doit lui aussi réconcilier (ouverture + Σ = clôture). S'il ne
            # tombe toujours pas juste, les signes/montants sont encore faux → on
            # garde les opérations pour le matching mais on RESIGNALE le doc plutôt
            # que de masquer une erreur. (Une facture vision est acceptée telle quelle.)
            reasons = (extract.statement_reconcile_reasons(data)
                       if data.get("kind") == "bank-statement" else [])
            data["needs_vision"] = bool(reasons)
            if reasons:
                data["vision_reason"] = ["vision_" + r for r in reasons]
            return data

    # cache d'extraction (réentrance + reruns instantanés)
    try:
        stamp = _file_stamp(pdf_path)
        cached = load_json(_cache_path(pdf_path), None)
        if isinstance(cached, dict) and cached.get("_stamp") == stamp and cached.get("fields"):
            # garantit la transcription `.md` même sur cache hit (backfill ponctuel
            # des anciens caches sans `text` : on relit le texte une seule fois).
            if not _md_path(pdf_path).exists():
                _write_transcription(pdf_path, cached.get("text") or extract.pdftext(pdf_path))
            return cached["fields"]
    except OSError:
        stamp = None

    text = extract.pdftext(pdf_path)
    g = extract.classify_and_extract(text)
    _write_transcription(pdf_path, text)

    if stamp is not None:
        try:
            save_json(_cache_path(pdf_path), {"_stamp": stamp, "fields": g, "text": text})
        except OSError:
            pass
    return g                                    # needs_vision géré en aval (file VISION)


# ── Helpers ───────────────────────────────────────────────────────────────

def parse_invoice_filename(filename):
    """
    Format conventionnel (écrit par organisation-documents/scripts/main.py) :
      AAAA-MM-JJ_N°Facture_Contrepartie_MontantTTC.pdf
    Tolère aussi un ancien format 3 parties (sans n° de facture).
    """
    m = re.match(r"(\d{4}-\d{2}-\d{2})_([^_]+)_([^_]+)_(\d+(?:\.\d+)?)\.pdf$", filename)
    if m:
        issued = m.group(1)
        return {
            "invoice_id": m.group(2),
            "issued_date": issued,
            "due_date": (datetime.strptime(issued, "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d"),
            "counterparty": m.group(3),
            "amount": float(m.group(4)),
        }
    m = re.match(r"(\d{4}-\d{2}-\d{2})_([^_]+)_(\d+(?:[._]\d+)?)\.pdf$", filename)
    if m:
        issued = m.group(1)
        amount_raw = m.group(3).replace("_", ".")
        return {
            "invoice_id": f"{issued}_{m.group(2)}_{amount_raw}",
            "issued_date": issued,
            "due_date": (datetime.strptime(issued, "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d"),
            "counterparty": m.group(2),
            "amount": float(amount_raw),
        }
    return None


def parse_expense_filename(filename):
    """Nom écrit par classement-document pour une note de frais (cf. structure-cible) :
      AAAA-MM-JJ_<Collaborateur>_<Émetteur>_<MontantTTC>.<ext>   (4 parties)
      AAAA-MM-JJ_<Émetteur>_<MontantTTC>.<ext>                   (3 parties, sans salarié)
    Une note de frais se règle par un DÉCAISSEMENT (remboursement / carte) → type "in".
    La contrepartie utile au rapprochement bancaire est l'ÉMETTEUR (le commerçant)."""
    for ext in (r"\.pdf", r"\.(?:png|jpe?g|tiff?|webp|heic)"):
        m = re.match(r"(\d{4}-\d{2}-\d{2})_([^_]+)_([^_]+)_(\d+(?:\.\d+)?)" + ext + r"$", filename, re.I)
        if m:
            issued, benef, emitter, amt = m.group(1), m.group(2), m.group(3), m.group(4)
            return {"issued_date": issued, "beneficiary": benef.replace("-", " "),
                    "emitter": emitter, "amount": float(amt),
                    "invoice_id": f"NDF-{issued}-{benef}"}
        m = re.match(r"(\d{4}-\d{2}-\d{2})_([^_]+)_(\d+(?:\.\d+)?)" + ext + r"$", filename, re.I)
        if m:
            issued, emitter, amt = m.group(1), m.group(2), m.group(3)
            return {"issued_date": issued, "beneficiary": None,
                    "emitter": emitter.replace("-", " "), "amount": float(amt),
                    "invoice_id": f"NDF-{issued}-{emitter}"}
    return None


def similarity(a, b):
    a, b = (a or "").lower().strip(), (b or "").lower().strip()
    if not a or not b:
        return 0.0
    if a == b or a in b or b in a:
        return 1.0
    # forme normalisée : hyphens/ponctuation → espace (gère noms tronqués type "Auberge-du-Vie")
    a_clean = re.sub(r"[^a-z0-9]+", " ", a).strip()
    b_clean = re.sub(r"[^a-z0-9]+", " ", b).strip()
    if a_clean and b_clean and (a_clean in b_clean or b_clean in a_clean):
        return 0.9
    base = SequenceMatcher(None, a, b).ratio()
    wa, wb = set(re.findall(r"[a-z0-9]+", a)), set(re.findall(r"[a-z0-9]+", b))
    jacc = len(wa & wb) / len(wa | wb) if (wa and wb) else 0.0
    return max(base, jacc)


def _month_hashes(month_dir):
    """Empreintes (md5) des documents d'un mois → détecter qu'un fichier a changé
    après verrouillage (alors on rouvre la période)."""
    out = {}
    for p in sorted(month_dir.rglob("*")):
        if is_doc_file(p):
            h = _content_hash(p)
            if h:
                out[str(p.relative_to(month_dir))] = h
    return out


def is_locked(month_dir):
    return (month_dir / "batch.lock.json").exists()


def should_process(month_dir):
    """Traité si : mois ACTIF (courant/précédent), OU non verrouillé, OU verrouillé
    mais dont un document a changé depuis le verrou (réouverture automatique)."""
    key = f"{month_dir.parent.name}-{month_dir.name}"
    if key in ACTIVE_MONTHS:
        return True
    lock = month_dir / "batch.lock.json"
    if not lock.exists():
        return True
    stored = (load_json(lock, {}) or {}).get("hashes") or {}
    return _month_hashes(month_dir) != stored      # un fichier a changé → on rouvre


def _month_dir_of(source_file, client_dir):
    """Le dossier <client>/AAAA/MM d'un document (d'après son chemin), ou None."""
    try:
        rel = Path(source_file).resolve().relative_to(Path(client_dir).resolve())
    except (ValueError, OSError):
        return None
    parts = rel.parts
    if len(parts) >= 2 and re.match(r"\d{4}$", parts[0]) and re.match(r"\d{2}$", parts[1]):
        return Path(client_dir) / parts[0] / parts[1]
    return None


def _month_key_of(source_file, client_dir):
    md = _month_dir_of(source_file, client_dir)
    return f"{md.parent.name}-{md.name}" if md else None


def _maybe_lock_months(client_dir, invoices, anomalies, vision_queue):
    """Clôture : verrouille un mois PASSÉ entièrement résolu (toutes factures payées,
    aucune anomalie bloquante, aucun doc à relire en vision). Conservateur et
    réversible (un fichier qui change rouvre le mois). Les factures d'un mois
    verrouillé RESTENT dans followup.json (grand livre cumulatif)."""
    inv_by_month, inv_month_of = {}, {}
    for v in invoices.values():
        k = _month_key_of(v.get("source_file"), client_dir)
        if k:
            inv_by_month.setdefault(k, []).append(v)
            inv_month_of[v["invoice_id"]] = k
    vision_months = {_month_key_of(e.get("source_file"), client_dir) for e in vision_queue}
    # On ne verrouille pas un mois qui a un problème non résolu PAR NATURE (paiement
    # compté deux fois, TVA incohérente) — indépendamment du montant. (Plus de notion
    # de « blocking » ni de seuil > 1000 : retirés du produit sur demande.)
    _LOCK_BLOCKERS = {"doublon_paiement", "tva_incorrecte"}
    block_months = set()
    for a in anomalies:
        if a.get("type") not in _LOCK_BLOCKERS:
            continue
        k = a["date"][:7] if a.get("date") else inv_month_of.get(a.get("invoice_id"))
        if k:
            block_months.add(k)
    for k, invs in inv_by_month.items():
        if k in ACTIVE_MONTHS:
            continue                                   # mois courant/précédent → jamais verrouillé
        md = client_dir / k[:4] / k[5:7]
        if is_locked(md) or k in vision_months or k in block_months:
            continue
        if any(i["status"] != "paid" for i in invs):
            continue                                   # une facture non soldée → on ne ferme pas
        save_json(md / "batch.lock.json",
                  {"locked_at": datetime.now(timezone.utc).isoformat(), "hashes": _month_hashes(md)})


def check_tva(fields):
    ht = fields.get("total_ht")
    rate = fields.get("tva_rate")
    declared = fields.get("tva_amount")
    if ht is None or rate is None or declared is None:
        return None
    if fields.get("tva_multi"):
        return None   # facture multi-taux : contrôle mono-taux (HT × taux) non fiable
    if rate == 0:
        return None
    expected = round(ht * rate, 2)
    if expected == 0:
        return None
    disc = abs(declared - expected) / expected
    if disc > 0.05:
        return {
            "type": "tva_incorrecte",
            "total_ht": ht, "tva_declared": declared, "tva_expected": expected,
            "tva_rate_pct": round(rate * 100, 1), "discrepancy_pct": round(disc * 100, 1),
        }
    return None


# ── Rapprochement : catégorisation + scoring (cf. references/matching-rules.md) ──
# Le MONTANT ne décide jamais seul. Certaines lignes ne se rapprochent pas du tout
# (frais bancaires, salaires/charges, virements internes) : les matcher ou les
# signaler « orphelines » serait du bruit.
_CAT_RULES = [
    # NARROW volontairement : on n'exclut que des libellés SANS ambiguïté (un vrai
    # paiement de facture ne doit jamais être exclu par erreur). Les frais sont de
    # toute façon des débits → jamais des « orphelins » (qui ne visent que les crédits).
    # Frais bancaires au sens large : tenue de compte, agios, commissions,
    # intérêts (créditeurs ET débiteurs), cotisation carte, frais/commissions liés
    # aux prélèvements impayés et interventions.
    ("frais_bancaires", re.compile(
        r"\b(frais\s+banc|frais\s+de\s+tenue|tenue\s+de\s+compte|agios?|"
        r"cotisation\s+(?:mensuelle\s+)?carte|cotisation\s+(?:mensuelle\s+)?\w*\s*carte|"
        r"int[ée]r[êe]ts?\s+(?:cr[ée]diteurs?|d[ée]biteurs?)|int[ée]r[êe]ts?\b|"
        r"commissions?(?:\s+d['e]\s*intervention)?|commission\s+intervention|"
        r"frais\s+pr[ée]l[èe]vement\s+impay[ée]|frais\s+(?:de\s+)?rejet|"
        r"frais\s+d['e]?\s*incident|frais\s+virement|frais\s+sepa|"
        r"frais\s+de\s+service|frais\s+carte)\b", re.I)),
    ("rh_charges", re.compile(
        # pluriels tolérés (« VIR SALAIRES … » échappait à \bsalaire\b et tombait à
        # tort en facture_manquante) ; +paie/salaire net, cotisations sociales.
        r"\b(salaires?|salaire\s+net|paies?|payes?|bulletins?\s+de\s+paie|"
        r"r[ée]mun[ée]rations?|urssaf|\bdsn\b|cipav|carsat|agirc|arrco|"
        r"madelin|mutuelles?|pr[ée]voyances?|retraites?|cotisations?\s+social|"
        r"charges?\s+social|p[ôo]le\s*emploi)\b", re.I)),
    # Organismes sociaux & prestations (non facturables) : CAF, allocations, CPAM,
    # MSA, sécurité sociale, aides.
    ("prestations_sociales", re.compile(
        r"\b(\bcaf\b|caisse\s+d['e]?\s*allocations?|allocations?\s+familiales?|"
        r"\bcpam\b|\bmsa\b|s[ée]curit[ée]\s+sociale|\bcaisse\s+primaire\b|"
        r"prestation\s+sociale|aide\s+sociale|\brsa\b|\bapl\b|\baah\b)\b", re.I)),
    # Impôts & taxes : DGFiP / DFiP / Trésor Public / impôts — non facturables.
    ("impots_taxes", re.compile(
        r"\b(dgfip|\bdfip\b|dgi\b|tr[ée]sor\s+public|impots?|imp[ôo]ts?|"
        r"\btva\b\s+(?:[àa]\s+)?(?:payer|d[ée]caisser)|tax(?:e|es)\s+fonci|"
        r"cfe\b|cvae\b|taxe\s+d['e]?habitation|amende|\bsie\b)\b", re.I)),
    # Mouvements d'espèces (retraits ET dépôts DAB/GAB) — non facturables.
    ("especes", re.compile(
        r"\b(retrait\s+(?:dab|gab|esp[èe]ces?|d['e]?\s*esp[èe]ces?)|"
        r"ret(?:rait)?\s+dab|\bdab\b|\bgab\b|retrait\s+\w*\s*card|"
        r"retrait\s+au\s+distributeur|"
        r"d[ée]p[ôo]ts?\s+(?:d['e]?\s*)?esp[èe]ces?|d[ée]p[ôo]t\s+esp\b|"
        r"versement\s+(?:d['e]?\s*)?esp[èe]ces?|remise\s+(?:d['e]?\s*)?esp[èe]ces?)\b", re.I)),
    ("transfert_interne", re.compile(
        r"virement\s+interne|vir(?:ement)?\s+entre\s+comptes?|transfert\s+interne|"
        r"de\s+compte\s+[àa]\s+compte|versement\s+sur\s+pea|vir(?:ement)?\s+pea|"
        r"vir(?:ement)?\s+livret|alimentation\s+(?:compte|livret)|"
        r"vir(?:ement)?\s+(?:de\s+)?r[ée]gularisation|changement\s+d['e]?\s*agence", re.I)),
    # Virements de/vers particuliers (personnes physiques, hors facture) — non
    # facturables : virements perso, dons, remboursements entre particuliers.
    ("virement_particulier", re.compile(
        r"\b(vir(?:ement)?\s+(?:inst\s+)?(?:de\s+|vers\s+)?(?:m\.|mr|mme|mlle|monsieur|madame)\b|"
        r"vir(?:ement)?\s+particulier|vir(?:ement)?\s+perso(?:nnel)?)", re.I)),
]

# tokens trop génériques pour servir de preuve de libellé (matching-rules.md)
_GENERIC_TOKENS = {
    "paiement", "virement", "prelevement", "prlv", "facture", "client", "achat",
    "vente", "commande", "service", "reglement", "remise", "cheque", "carte",
    "sarl", "sas", "sasu", "eurl", "societe", "monsieur", "madame", "paris"}


def tx_category(label):
    """Catégorie 'à ne pas rapprocher' (frais/salaires/virements internes) ou None."""
    for cat, rx in _CAT_RULES:
        if rx.search(label or ""):
            return cat
    return None


def _sign_ok(direction, amount):
    """Sens : une VENTE (out) est encaissée par un CRÉDIT (+) ; un ACHAT (in) réglé
    par un DÉBIT (−). Pas de cross-match (matching-rules.md)."""
    a = amount or 0.0
    return a > 0 if direction == "out" else a < 0


def _score_amount(tx_amount, inv_amount):
    if inv_amount is None or tx_amount is None:
        return 0.0
    d = abs(abs(tx_amount) - inv_amount)
    if d <= 0.01:
        return 1.0
    if inv_amount > 0 and d / inv_amount < 0.02:   # escompte typique < 2 %
        return 0.6
    return 0.0


def _score_label(label, inv_id, counterparty):
    lab = (label or "").lower()
    if inv_id and str(inv_id).lower() in lab:
        return 1.0
    digits = re.sub(r"\D", "", str(inv_id or ""))
    if len(digits) >= 4 and digits in re.sub(r"\D", "", lab):
        return 1.0
    toks = [t for t in re.findall(r"[a-zà-ÿ0-9]{4,}", (counterparty or "").lower())
            if t not in _GENERIC_TOKENS]
    if any(t in lab for t in toks):
        return 0.8
    if counterparty and similarity(lab, counterparty.lower()) >= 0.6:
        return 0.5                              # nom approché (faute/troncature)
    return 0.0


def _score_date(tx_date, inv_date):
    try:
        d = abs((datetime.strptime(tx_date, "%Y-%m-%d")
                 - datetime.strptime(inv_date, "%Y-%m-%d")).days)
    except (ValueError, TypeError):
        return 0.0
    if d <= 3:
        return 1.0
    if d <= 30:
        return 0.7
    if d <= 60:
        return 0.3
    return 0.0


def _looks_like_ref(ref):
    """Réf citée au relevé qui ressemble à un VRAI n° de facture (≥ 4 car., ≥ 1 chiffre,
    pas un n° TVA/SIREN/SIRET) → évite 'facture_manquante' sur une réf interne/SEPA."""
    if not ref or len(str(ref)) < 4 or not re.search(r"\d", str(ref)):
        return False
    return not extract._is_bad_invoice_id(str(ref))


# ── Remontée backend Pocket-Claw : company.json + rapprochement.json ────────
# Le backend lit, PAR CLIENT, exactement ces deux fichiers (les autres .json sont
# internes/ignorés). Format STRICT — voir contrat. JSON malformé → ignoré en silence,
# donc on écrit du JSON valide via save_json (atomique).

def backend_company(entry):
    """company.json depuis l'entrée clients.json (champs optionnels, fournis si dispo)."""
    entry = entry or {}
    out = {}
    name = entry.get("raisonSociale")
    if name:
        out["name"] = name
    sirens = [s for s in (entry.get("siren") or []) if s]
    if sirens:
        d = re.sub(r"\D", "", str(sirens[0]))
        out["siren"] = d[:9] if len(d) >= 9 else str(sirens[0])
    emails = [c.get("email") for c in (entry.get("contacts") or []) if c.get("email")]
    if emails:
        out["email"] = emails[0]
    m = re.search(r"\b(SASU|SARL|SAS|EURL|SELARL|SCEA|GAEC|SCM|EIRL|SCI|SNC|SCP|SA)\b",
                  name or "", re.I)
    if m:
        out["legal_form"] = m.group(1).upper()
    ibans = [i for i in (entry.get("iban") or []) if i]
    if ibans:
        out["iban"] = ibans[0]          # champ extra (conservé en "raw" côté serveur)
    return out


def _prior_period_map(prior):
    out = {}
    for p in (prior.get("periods") if isinstance(prior, dict) else []) or []:
        pk = p.get("period")
        if pk:
            out[pk] = p
    return out


def backend_rapprochement(client_dir, ledger, anomalies, relances, period_stmt, prior,
                          transactions, consumed):
    """rapprochement.json : periods[] au format STRICT du contrat backend.
    `ledger` = grand livre cumulatif (toutes périodes) ; anomalies/relances/compteurs
    = run courant (mois traités). Les périodes figées (verrouillées, non retraitées)
    sont retenues telles quelles depuis l'ancien fichier → rien ne disparaît."""
    prior_map = _prior_period_map(prior)
    P = {}

    # transactions rapprochées à une facture, comptées DANS LEUR période (au niveau
    # TRANSACTION, pas facture : robuste au cross-période facture↔paiement).
    matched_per_period = {}
    for i in consumed:
        if 0 <= i < len(transactions):
            pkt = transactions[i].get("period") or str(transactions[i].get("date") or "")[:7]
            if re.match(r"\d{4}-\d{2}$", str(pkt)):
                matched_per_period[pkt] = matched_per_period.get(pkt, 0) + 1

    def per(pk):
        if pk not in P:
            cnt = period_stmt.get(pk)
            old = prior_map.get(pk, {})
            P[pk] = {
                "period": pk,
                "locked": is_locked(client_dir / pk[:4] / pk[5:7]),
                "bank_statements_count": cnt["statements"] if cnt else old.get("bank_statements_count", 0),
                "bank_transactions_count": cnt["transactions"] if cnt else old.get("bank_transactions_count", 0),
                "bank_matched_count": matched_per_period.get(pk, old.get("bank_matched_count", 0)),
                "invoices": [], "unmatched_bank_lines": [], "excluded_bank_lines": [],
                "period_anomalies": [], "relances": [],
            }
        return P[pk]

    # anomalies rattachées à une FACTURE (par invoice_id) → injectées dans invoice.anomalies
    inv_anoms = {}
    for a in anomalies:
        iid = a.get("invoice_id")
        if iid and a.get("type") in ("invoice_overdue", "tva_incorrecte", "match_ambigu"):
            inv_anoms.setdefault(iid, []).append(
                {k: v for k, v in a.items() if k not in ("invoice_id", "source_file")})

    inv_period = {}
    for inv in ledger:
        pk = _month_key_of(inv.get("source_file"), client_dir) or str(inv.get("issued_date") or "")[:7]
        if not re.match(r"\d{4}-\d{2}$", pk):
            continue
        iid = inv.get("invoice_id")
        inv_period[iid] = pk
        status = inv.get("status")
        amt = inv.get("amount")
        if status == "paid":
            paid, remaining = inv.get("amount_paid", amt), 0
        elif status == "partial":
            paid, remaining = inv.get("amount_paid", 0), inv.get("amount_remaining", amt)
        else:                                       # unpaid / overdue
            paid, remaining = 0, amt
        obj = {
            "invoice_id": iid,
            "type": inv.get("type"),                # "out" (vente) | "in" (achat)
            "counterparty_name": inv.get("counterparty_name") or inv.get("counterparty"),
            "amount": amt,
            "issued_date": inv.get("issued_date"),
            "due_date": inv.get("due_date"),
            "status": status,
            "bank_matched": bool(inv.get("bank_matched")),
            "amount_paid": paid,
            "amount_remaining": remaining,
            "anomalies": inv_anoms.get(iid, []),
        }
        if inv.get("match_confidence"):
            obj["match_confidence"] = inv["match_confidence"]
        per(pk)["invoices"].append(obj)

    for pk in period_stmt:                          # périodes avec relevés mais sans facture
        if re.match(r"\d{4}-\d{2}$", pk):
            per(pk)

    # INVARIANT : toute transaction du relevé est représentée EXACTEMENT une fois —
    #   consommée par une facture (bank_matched_count) ;
    #   non facturable (frais/salaire/impôt/espèces/virement interne ou perso) → excluded_bank_lines ;
    #   sinon billable non rapprochée → unmatched_bank_lines (débit → facture_manquante,
    #   crédit → paiement_orphelin).
    # → bank_matched_count + unmatched + excluded == bank_transactions_count.
    for i, tx in enumerate(transactions):
        if i in consumed:
            continue                                # déjà rapprochée à une facture
        pk = tx.get("period") or str(tx.get("date") or "")[:7]
        if not re.match(r"\d{4}-\d{2}$", str(pk)):
            continue
        amt = tx.get("amount")
        cat = tx.get("category")
        line = {
            "label": tx.get("raw_label") or "Opération bancaire",
            "amount": amt,
            "date": tx.get("date"),
            "invoice_ref": tx.get("invoice_ref"),
        }
        if cat:
            # NON FACTURABLE : jamais rapprochée à une facture, jamais comptée comme
            # facture_manquante / paiement_orphelin. Listée à part (complétude).
            line["category"] = cat
            per(pk)["excluded_bank_lines"].append(line)
        else:
            is_debit = amt is not None and amt < 0
            line["type"] = "facture_manquante" if is_debit else "paiement_orphelin"
            per(pk)["unmatched_bank_lines"].append(line)

    # period_anomalies : anomalies de PÉRIODE (pas une transaction unique) — doublon de
    # paiement, relevé illisible/non parseable. (Les fm/orphelin viennent des transactions
    # ci-dessus ; invoice_overdue/tva/match_ambigu sont dans invoice.anomalies.)
    for a in anomalies:
        t = a.get("type")
        if t not in ("doublon_paiement", "releve_non_parseable", "facture_illisible"):
            continue
        pk = a["date"][:7] if a.get("date") else _month_key_of(a.get("source_file"), client_dir)
        if not pk or not re.match(r"\d{4}-\d{2}$", str(pk)):
            continue
        pa = {"type": t}
        if a.get("label"):
            pa["label"] = a["label"]
        elif a.get("source_file"):
            pa["label"] = Path(a["source_file"]).name
        if a.get("amount") is not None:
            pa["amount"] = a["amount"]
        if a.get("date"):
            pa["date"] = a["date"]
        per(pk)["period_anomalies"].append(pa)

    for r in relances:                              # relance complète (objet tel quel)
        pk = inv_period.get(r.get("invoice_id"))
        if pk and re.match(r"\d{4}-\d{2}$", str(pk)):
            per(pk)["relances"].append(dict(r))

    # Mois FIGÉ (verrouillé + inchangé, donc non retraité ce run) : l'ancien fichier
    # fait foi ENTIÈREMENT — on ÉCRASE tout rebuild partiel (les factures du grand
    # livre cumulatif appellent per() mais sans transactions → période incomplète).
    # Sinon : N repris de l'ancien mais 0 ligne → invariant KO.
    for pk, p in prior_map.items():
        if re.match(r"\d{4}-\d{2}$", str(pk)):
            md = client_dir / pk[:4] / pk[5:7]
            if md.exists() and not should_process(md):
                p["locked"] = is_locked(md)   # refléter l'état réel du verrou (auto-réparation)
                P[pk] = p

    return {"periods": [P[k] for k in sorted(P)]}


# ── Pré-extraction parallèle ──────────────────────────────────────────────

def iter_doc_paths(client_dir):
    """Tous les PDFs/relevés à extraire pour un client, en respectant les mois
    actifs/non verrouillés — même périmètre que process_client (cohérence cache)."""
    for year_dir in sorted(client_dir.iterdir()):
        if not (year_dir.is_dir() and re.match(r"\d{4}$", year_dir.name)):
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir() or not should_process(month_dir):
                continue
            for f in month_dir.rglob("invoices/**/*.pdf"):
                yield f
            for f in month_dir.rglob("notes-de-frais/**/*"):
                if is_doc_file(f):
                    yield f
            for st in month_dir.rglob("bank-statements/*"):
                if is_doc_file(st):
                    yield st


def prewarm_cache(client_dirs):
    """Extrait tous les documents EN PARALLÈLE et remplit le cache avant le
    rapprochement (séquentiel et déterministe). pdf_fields() écrit chaque résultat
    immédiatement → le run est réentrant : relancé après un kill, les PDFs déjà
    extraits sont servis depuis le cache et seuls les nouveaux sont traités."""
    paths = [p for d in client_dirs for p in iter_doc_paths(d)]
    todo = [p for p in paths if not _cache_path(p).exists()]
    if not todo:
        print(f"  · cache: {len(paths)} documents déjà extraits, rien à refaire")
        return
    print(f"  · extraction parallèle de {len(todo)}/{len(paths)} documents "
          f"({WORKERS} workers)…")
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for _ in pool.map(pdf_fields, todo):
            done += 1
            if done % 50 == 0:
                print(f"    {done}/{len(todo)} extraits")
    print(f"  · extraction terminée ({done} documents)")


# ── Cœur de rapprochement (PARTAGÉ) ────────────────────────────────────────
# Logique PURE (sans IO) : catégorisation + matching Pass 1/2 + anomalies +
# overdue/relances. Mutée en place sur invoice_list. Réutilisée par process_client
# (flux PDF/arbre) ET par le skill e-facture-rapprochement (ingestion structurée /
# tickets LLM) → un SEUL moteur, donc des sorties identiques pour des entrées
# identiques (fin de la divergence entre les deux skills). Politique CONSERVATRICE.
#   invoice_list : liste de dicts {invoice_id,type,amount,status,issued_date,
#                  due_date,counterparty,counterparty_name,bank_matched,source_file,
#                  [doc_type]} — mutés (status/bank_matched/amount_paid/…).
#   transactions : liste de dicts {date,label,raw_label,amount,invoice_ref,
#                  [reliable],[period]} — `category` posé ici.
#   anomalies    : liste pré-existante (tva/illisible/non-parseable) ENRICHIE ici.
# Renvoie (consumed:set d'indices de transactions, relances:list).

def reconcile_invoices(invoice_list, transactions, anomalies, today):
    for tx in transactions:
        tx["category"] = tx_category(tx.get("raw_label") or tx.get("label") or "")
    consumed = set()

    # Pass 1 — référence facture : SOMME des transactions de même réf et bon sens.
    for inv in invoice_list:
        hits = [i for i, tx in enumerate(transactions)
                if i not in consumed and tx.get("invoice_ref") == inv["invoice_id"]
                and _sign_ok(inv["type"], tx["amount"])]
        if not hits:
            continue
        paid = round(sum(abs(transactions[i]["amount"]) for i in hits), 2)
        consumed.update(hits)
        inv["bank_matched"] = True
        inv["matched_tx"] = " ; ".join((transactions[i].get("raw_label") or transactions[i].get("label") or "") for i in hits)
        if len(hits) > 1:
            inv["matched_tx_count"] = len(hits)
        if abs(paid - inv["amount"]) <= 1.0:
            inv["status"] = "paid"
        elif paid < inv["amount"]:
            inv["status"] = "partial"
            inv["amount_paid"] = paid
            inv["amount_remaining"] = round(inv["amount"] - paid, 2)
        else:
            inv["status"] = "paid"
            inv["amount_paid"] = paid
            inv["overpaid_by"] = round(paid - inv["amount"], 2)

    # Pass 2 — scoring montant(0.5)+libellé(0.3)+date(0.2) ; jamais le montant seul.
    for inv in invoice_list:
        if inv["bank_matched"]:
            continue
        scored = []
        for i, tx in enumerate(transactions):
            if i in consumed or tx.get("category") or not _sign_ok(inv["type"], tx["amount"]):
                continue
            sa = _score_amount(tx["amount"], inv["amount"])
            if sa == 0.0:
                continue
            lbl = tx.get("raw_label") or tx.get("label") or ""
            sl = _score_label(lbl, inv["invoice_id"], inv.get("counterparty_name"))
            sd = _score_date(tx["date"], inv.get("issued_date"))
            if sl == 0.0 and sd == 0.0:
                continue
            scored.append((round(0.5 * sa + 0.3 * sl + 0.2 * sd, 3), i))
        if not scored:
            continue
        scored.sort(key=lambda t: (t[0], _score_date(transactions[t[1]]["date"], inv.get("issued_date"))),
                    reverse=True)
        best, bi = scored[0]
        if best < 0.65:
            continue
        if len(scored) > 1 and (best - scored[1][0]) < 0.10:
            d_best = _score_date(transactions[bi]["date"], inv.get("issued_date"))
            d_next = _score_date(transactions[scored[1][1]]["date"], inv.get("issued_date"))
            if d_best <= d_next:
                inv["match_ambiguous"] = True
                anomalies.append({"type": "match_ambigu", "invoice_id": inv["invoice_id"],
                                  "amount": inv["amount"],
                                  "candidates": [(transactions[i].get("raw_label") or transactions[i].get("label") or "") for _, i in scored[:3]]})
                continue
        consumed.add(bi)
        inv["bank_matched"] = True
        inv["status"] = "paid"
        inv["matched_tx"] = transactions[bi].get("raw_label") or transactions[bi].get("label") or ""
        if best < 0.85:
            inv["match_confidence"] = "medium"

    # ── Anomalies : doublons (même date+montant+libellé) ──────────────────
    seen = {}
    for tx in transactions:
        if not tx.get("reliable", True):
            continue
        lbl = (tx.get("label") or tx.get("raw_label") or "")
        key = (tx["date"], round(abs(tx["amount"] or 0), 2), lbl.lower()[:30])
        if key in seen:
            anomalies.append({"type": "doublon_paiement", "label": tx.get("raw_label") or lbl,
                              "amount": tx["amount"], "date": tx["date"]})
        else:
            seen[key] = True

    # Réf de facture citée au relevé mais pièce absente du dossier.
    known = {inv["invoice_id"] for inv in invoice_list}
    for i, tx in enumerate(transactions):
        ref = tx.get("invoice_ref")
        if not ref or ref in known or i in consumed or tx.get("category") or not tx.get("reliable", True):
            continue
        if not _looks_like_ref(ref):
            continue
        anomalies.append({"type": "facture_manquante", "invoice_ref": ref,
                          "label": tx.get("raw_label") or tx.get("label") or "",
                          "amount": tx["amount"], "date": tx["date"]})

    # Encaissements (crédits) sans réf ni facture rapprochée, hors catégorie.
    for i, tx in enumerate(transactions):
        if (tx["amount"] is None or tx["amount"] <= 0 or i in consumed
                or tx.get("invoice_ref") or tx.get("category") or not tx.get("reliable", True)):
            continue
        anomalies.append({"type": "paiement_orphelin",
                          "label": tx.get("raw_label") or tx.get("label") or "",
                          "amount": tx["amount"], "date": tx["date"]})

    # ── Statuts overdue + relances ────────────────────────────────────────
    relances = []
    for inv in invoice_list:
        try:
            due = datetime.strptime(inv["due_date"], "%Y-%m-%d").date()
        except (ValueError, KeyError, TypeError):
            due = today + timedelta(days=30)

        if inv["status"] in ("unpaid",) and due < today:
            inv["status"] = "overdue"
            anomalies.append({"type": "invoice_overdue", "invoice_id": inv["invoice_id"],
                              "days_late": (today - due).days, "amount": inv["amount"]})

        if inv.get("doc_type") == "note-de-frais":
            continue

        if inv["status"] in ("overdue", "partial") or (inv["status"] == "unpaid" and due < today):
            days_late = max((today - due).days, 0)
            step = 1 if days_late <= 30 else 2 if days_late <= 60 else 3 if days_late <= 90 else "escalation"
            r = {"invoice_id": inv["invoice_id"], "counterparty": inv.get("counterparty", ""),
                 "amount": inv["amount"], "due_date": inv.get("due_date"), "days_late": days_late,
                 "step": step, "status": "pending",
                 "next_action_date": (today + timedelta(days=5)).strftime("%Y-%m-%d")}
            if inv["status"] == "partial":
                r["amount_remaining"] = inv.get("amount_remaining", inv["amount"])
                r["note"] = f"Solde restant dû : {r['amount_remaining']:.2f} €"
            relances.append(r)

    return consumed, relances


# ── Traitement d'un client ────────────────────────────────────────────────

def process_client(client_dir, client_entry=None):
    invoices = {}
    transactions = []
    anomalies = []
    vision_queue = []  # docs où le script n'est pas fiable → à relire en VISION
    low_conf = {}      # factures au gate douteux → vision SAUF si confirmées par la banque
    period_stmt = {}   # "AAAA-MM" -> {statements, transactions} (compteurs backend)
    # Dé-duplication par contenu : un même PDF réimporté sous plusieurs noms
    # (`X.pdf`, `X__Banque.pdf`, …) ne doit être compté qu'une fois — sinon
    # factures et opérations bancaires sont dédoublées dans followup/relances.
    seen_hashes = set()
    seen_statements = set()   # dédup SÉMANTIQUE des relevés (même banque+période+soldes)

    def is_dup(path):
        h = _content_hash(path)
        if h is None:
            return False
        if h in seen_hashes:
            return True
        seen_hashes.add(h)
        return False

    def queue_vision(path, fields):
        vision_queue.append({
            "source_file": str(path),
            "kind": fields.get("kind"),
            "reason": fields.get("vision_reason") or ["needs_vision"],
        })

    for year_dir in sorted(client_dir.iterdir()):
        if not (year_dir.is_dir() and re.match(r"\d{4}$", year_dir.name)):
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir() or not should_process(month_dir):
                continue

            # ── Factures ──────────────────────────────────────────────────
            for f in sorted(month_dir.rglob("invoices/**/*.pdf")):
                if is_dup(f):
                    continue  # réimport byte-identique d'une facture déjà vue
                direction = "out" if "/out/" in str(f).replace("\\", "/") else "in"
                parsed = parse_invoice_filename(f.name)
                fields = pdf_fields(f)

                if parsed:
                    inv_id = parsed["invoice_id"]
                    amount = parsed["amount"]
                    issued = parsed["issued_date"]
                    due = parsed["due_date"]
                    cp = parsed["counterparty"]
                elif fields.get("kind") == "invoice" and fields.get("invoice_id") and fields.get("total_ttc") is not None:
                    inv_id = fields["invoice_id"]
                    amount = fields["total_ttc"]
                    issued = fields.get("issue_date") or ""
                    due = ((datetime.strptime(issued, "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d")
                           if issued else (TODAY + timedelta(days=30)).strftime("%Y-%m-%d"))
                    cp = (fields.get("recipient") if direction == "out" else fields.get("emitter")) or client_dir.name
                else:
                    # Ni le nom de fichier ni le texte ne donnent n° + montant fiables.
                    # On ne devine pas : anomalie + mise en file VISION (le modèle
                    # lira les pages rasterisées au lieu de forcer le regex).
                    anomalies.append({"type": "facture_illisible", "source_file": str(f)})
                    queue_vision(f, fields)
                    continue

                # nom complet de la contrepartie pour le matching fuzzy ;
                # si extract.py a su lire le PDF, on récupère le numéro réel — ça permet
                # de rattraper un nom de fichier corrompu en amont (invoice_id incorrect).
                cp_name = (fields.get("recipient") if direction == "out" else fields.get("emitter")) or cp
                real_inv_id = fields.get("invoice_id") if fields.get("kind") == "invoice" else None
                if real_inv_id and real_inv_id != inv_id:
                    inv_id = real_inv_id  # le PDF a raison, le filename a tort

                # clé interne = chemin (unique) — l'invoice_id peut collisionner si l'amont
                # a mal nommé plusieurs fichiers à l'identique.
                invoices[str(f)] = {
                    "invoice_id": inv_id, "type": direction, "amount": amount,
                    "status": "unpaid", "issued_date": issued, "due_date": due,
                    "counterparty": cp, "counterparty_name": cp_name,
                    "bank_matched": False, "source_file": str(f),
                }

                if fields.get("kind") == "invoice":
                    tva_anom = check_tva(fields)
                    if tva_anom:
                        tva_anom["invoice_id"] = inv_id
                        anomalies.append(tva_anom)
                    # gate facture KO (id/TTC absent, HT+TVA≠TTC) → candidate vision,
                    # confirmée ou non par la banque (tranché APRÈS le rapprochement).
                    if fields.get("needs_vision"):
                        low_conf[str(f)] = fields

            # ── Notes de frais ────────────────────────────────────────────
            # Rattachées au client (employeur) ; se soldent par un décaissement
            # (remboursement salarié / paiement carte) → traitées comme un ACHAT
            # (type "in"). Le bénéficiaire (salarié) n'est PAS relancé : on ne
            # « relance » pas un remboursement interne (doc_type="note-de-frais").
            for f in sorted(month_dir.rglob("notes-de-frais/**/*")):
                if not is_doc_file(f) or is_dup(f):
                    continue
                parsed = parse_expense_filename(f.name)
                fields = pdf_fields(f)
                if parsed:
                    inv_id, amount = parsed["invoice_id"], parsed["amount"]
                    issued, cp = parsed["issued_date"], parsed["emitter"]
                elif fields.get("kind") == "note-de-frais" and fields.get("total_ttc") is not None:
                    issued = fields.get("issue_date") or ""
                    amount = fields["total_ttc"]
                    cp = fields.get("company") or fields.get("beneficiary") or client_dir.name
                    inv_id = f"NDF-{issued or '0000-00-00'}-{re.sub(r'[^A-Za-z0-9]+', '', cp)[:12]}"
                else:
                    anomalies.append({"type": "facture_illisible", "source_file": str(f)})
                    queue_vision(f, fields)
                    continue
                due = ((datetime.strptime(issued, "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d")
                       if issued else (TODAY + timedelta(days=30)).strftime("%Y-%m-%d"))
                invoices[str(f)] = {
                    "invoice_id": inv_id, "type": "in", "amount": amount,
                    "status": "unpaid", "issued_date": issued, "due_date": due,
                    "counterparty": cp, "counterparty_name": cp,
                    "bank_matched": False, "source_file": str(f), "doc_type": "note-de-frais",
                }
                if fields.get("kind") == "note-de-frais" and fields.get("needs_vision"):
                    low_conf[str(f)] = fields

            # ── Relevés bancaires ─────────────────────────────────────────
            for st in sorted(month_dir.rglob("bank-statements/*")):
                if not is_doc_file(st):
                    continue  # ignore sidecars (.json) et artefacts (.docling.md, .txt…)
                if is_dup(st):
                    continue  # même relevé réimporté → ne pas redoubler les opérations
                f = pdf_fields(st)
                # Dédup SÉMANTIQUE : le même relevé livré en 2 formats (PDF + tableur)
                # a des octets différents (la dédup par hash ne le voit pas) mais la même
                # identité (banque + période + soldes ouverture/clôture). On ne le compte
                # qu'une fois → pas d'opérations dédoublées. On n'applique la clé que si
                # tous ses champs sont présents (sinon on ne risque pas de fausse fusion).
                if f.get("kind") == "bank-statement":
                    skey = (f.get("bank"), f.get("period_start"), f.get("period_end"),
                            f.get("opening_balance"), f.get("closing_balance"))
                    if all(x is not None for x in skey):
                        if skey in seen_statements:
                            continue
                        seen_statements.add(skey)
                # Fiabilité : un relevé qui NE réconcilie PAS (needs_vision) a des
                # signes/montants douteux. Ses opérations servent encore au matching
                # (un vrai match reste un bonus) mais ne génèrent PAS d'anomalies
                # orphelin/manquante/doublon — sinon flot de faux positifs sur des
                # signes faux. On attend la correction vision. (Principe : rien de
                # flaggé n'est présenté comme fiable.)
                reliable = not f.get("needs_vision")
                ops = f.get("operations", []) if f.get("kind") == "bank-statement" else []
                # compteurs backend par période (relevés effectivement retenus)
                _pk = f"{year_dir.name}-{month_dir.name}"
                _sc = period_stmt.setdefault(_pk, {"statements": 0, "transactions": 0})
                _sc["statements"] += 1
                _sc["transactions"] += len(ops)
                for op in ops:
                    transactions.append({
                        "date": op.get("date"),
                        "label": (op.get("label") or "").lower(),
                        "raw_label": op.get("label") or "",
                        "amount": op.get("amount"),
                        "invoice_ref": op.get("invoice_ref"),
                        "reliable": reliable,
                        "period": _pk,          # période (dossier) → invariant backend
                    })
                if not ops:
                    anomalies.append({"type": "releve_non_parseable", "source_file": str(st)})
                    queue_vision(st, f)
                elif f.get("needs_vision"):
                    # Opérations extraites mais peu fiables (solde non réconcilié,
                    # montant douteux) : on les garde pour le matching mais on
                    # signale le relevé pour relecture VISION/correction.
                    queue_vision(st, f)

    # ── Rapprochement (cœur PARTAGÉ, cf. reconcile_invoices) ──────────────
    # Catégorisation + matching Pass 1/2 + anomalies + overdue/relances. MÊME
    # moteur que le skill e-facture-rapprochement → sorties identiques à entrées
    # identiques (politique conservatrice unique).
    consumed, relances = reconcile_invoices(list(invoices.values()), transactions, anomalies, TODAY)

    # Recoupement bancaire = CONFIRMATION : une facture au gate douteux mais dont le
    # montant tombe juste sur un paiement réel est confirmée PAR LA RÉALITÉ → inutile
    # de la relire. Sinon (non rapprochée) → vision (principe gate-centric).
    for key, fields in low_conf.items():
        if not invoices.get(key, {}).get("bank_matched"):
            queue_vision(Path(key), fields)

    # Grand livre CUMULATIF : on conserve les factures des mois FIGÉS (verrouillés et
    # non retraités ce run) telles que persistées au run précédent — elles ne
    # disparaissent jamais du followup, même une fois la période close.
    prior = load_json(client_dir / "followup.json", [])
    fresh = set(invoices.keys())
    ledger = list(invoices.values())
    for e in (prior if isinstance(prior, list) else []):
        sf = e.get("source_file")
        if not sf or sf in fresh:
            continue                       # recomputé ce run → la version fraîche prime
        md = _month_dir_of(sf, client_dir)
        if md is not None and md.exists() and not should_process(md):
            ledger.append(e)               # mois figé → on garde l'entrée d'origine
    save_json(client_dir / "followup.json", ledger)
    save_json(client_dir / "relances.json", relances)
    save_json(client_dir / "anomalies.json", anomalies)
    save_json(client_dir / "needs_vision.json", vision_queue)
    # Verrouillage AVANT l'écriture du rapprochement.json : ainsi un mois passé
    # tout juste résolu est figé ET son flag `locked` reflète la réalité dès ce run
    # (sinon le verrou était créé après → `locked:false` figé à jamais).
    _maybe_lock_months(client_dir, invoices, anomalies, vision_queue)
    # ── Remontée backend Pocket-Claw : les 2 fichiers que le serveur lit ──────
    # (les .json ci-dessus restent internes/ignorés par la sync). Format STRICT.
    save_json(client_dir / "company.json", backend_company(client_entry))
    prior_rappro = load_json(client_dir / "rapprochement.json", {})
    save_json(client_dir / "rapprochement.json",
              backend_rapprochement(client_dir, ledger, anomalies, relances, period_stmt,
                                    prior_rappro, transactions, consumed))
    return invoices, relances, anomalies, vision_queue


# ── Auto-contrôle de l'invariant backend ───────────────────────────────────

def verify_invariant(client_dirs):
    """Pour CHAQUE période, toute transaction est représentée une fois :
    rapprochées (bank_matched_count) + non rapprochées (unmatched) + non facturables
    (excluded) == bank_transactions_count. Affiche le tableau ; renvoie False si un KO."""
    print("\n  Auto-contrôle invariant (rapprochées + unmatched + exclues == nb_transactions) :")
    print(f"    {'client/période':36} {'N':>4} {'rappr':>6} {'unmat':>6} {'exclu':>6} {'somme':>6}  état")
    all_ok = True
    for d in client_dirs:
        data = load_json(d / "rapprochement.json", {})
        for p in (data.get("periods") if isinstance(data, dict) else []) or []:
            n = p.get("bank_transactions_count", 0)
            matched = p.get("bank_matched_count",
                            sum(1 for i in p.get("invoices", []) if i.get("bank_matched")))
            unm = len(p.get("unmatched_bank_lines", []))
            exc = len(p.get("excluded_bank_lines", []))
            s = matched + unm + exc
            ok = (s == n)
            all_ok = all_ok and ok
            print(f"    {d.name + '/' + p.get('period', '?'):36} {n:>4} {matched:>6} {unm:>6} {exc:>6} {s:>6}  {'OK' if ok else 'KO'}")
    print("    → " + ("✅ toutes les périodes OK" if all_ok else "❌ périodes en KO (transactions omises)"))
    return all_ok


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    if not ROOT.exists():
        print(f"✗ Racine introuvable : {ROOT}")
        sys.exit(1)

    report = {"date": TODAY.isoformat(), "clients": []}
    tot_inv = tot_paid = tot_rel = tot_anom = tot_vision = 0

    client_dirs = [d for d in sorted(ROOT.iterdir())
                   if d.is_dir() and not d.name.startswith("_")]

    # clients.json (maintenu par organisation-documents) → identité pour company.json.
    clients_by_slug = {c.get("slug"): c for c in load_json(ROOT / "clients.json", []) if c.get("slug")}

    # Pré-extraction parallèle : tout le coût PDF est payé ici, une fois, en
    # parallèle et mis en cache. Le rapprochement qui suit lit le cache (instantané).
    prewarm_cache(client_dirs)

    for client_dir in client_dirs:
        invoices, relances, anomalies, vision_queue = process_client(
            client_dir, clients_by_slug.get(client_dir.name))
        paid = sum(1 for i in invoices.values() if i["status"] == "paid")
        report["clients"].append({
            "client": client_dir.name, "invoices": len(invoices), "paid": paid,
            "matched": sum(1 for i in invoices.values() if i.get("bank_matched")),
            "relances": len(relances), "anomalies": len(anomalies),
            "needs_vision": len(vision_queue),
        })
        tot_inv += len(invoices); tot_paid += paid; tot_rel += len(relances)
        tot_anom += len(anomalies); tot_vision += len(vision_queue)

    report["totals"] = {"invoices": tot_inv, "rapprochements": tot_paid,
                        "relances": tot_rel, "anomalies": tot_anom,
                        "needs_vision": tot_vision}
    report_path = ROOT / f"compta_batch_report_{TODAY}.json"
    save_json(report_path, report)
    print(f"✓ {len(report['clients'])} clients — {tot_paid}/{tot_inv} rapprochés — "
          f"{tot_rel} relances — {tot_anom} anomalies — "
          f"{tot_vision} à relire en vision")
    for c in report["clients"]:
        extra = f", {c['needs_vision']} à relire (vision)" if c["needs_vision"] else ""
        print(f"  · {c['client']}: {c['paid']}/{c['invoices']} payées, {c['relances']} relances, {c['anomalies']} anomalies{extra}")
    if tot_vision:
        print(f"  ⚠ {tot_vision} document(s) à relire en VISION — ÉTAPE OBLIGATOIRE ce run "
              f"(c'est l'agent qui lit les pages). Enchaîne :")
        print(f"      python3 scripts/resolve_vision.py {ROOT}")
        print(f"      → ouvre les images (Read), corrige les sidecars *.vision.json, puis relance ce script.")
    print(f"  Rapport : {report_path}")
    verify_invariant(client_dirs)


if __name__ == "__main__":
    main()
