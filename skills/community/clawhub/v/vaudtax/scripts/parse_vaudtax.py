#!/usr/bin/env python3
"""
Analyse un fichier .vaudtax et affiche un résumé lisible.

Usage :
    python parse_vaudtax.py <fichier.vaudtax>
    python parse_vaudtax.py <fichier.vaudtax> --full
    python parse_vaudtax.py <fichier.vaudtax> --extract all [--outdir DIR]
    python parse_vaudtax.py <fichier.vaudtax> --extract doc17700000000000 ...

Les identifiants directs (NAVS13, IBAN, téléphone, e-mail) sont masqués par
défaut dans le résumé ; --full les affiche en clair.
"""

import argparse
import zipfile
import xml.etree.ElementTree as ET
import itertools
import tempfile
from pathlib import Path

NS = "http://www.vd.ch/fiscalite/vaudtax"

# Top-level XML sections that this script knows about (parsed, acknowledged, or intentionally skipped).
# Any section found in the file that is not in this set is reported as unhandled.
KNOWN_SECTIONS = {
    # Metadata
    "fiscalPeriod", "lastGesdemReference",
    # Taxpayer identity
    "identification", "taxpayerPersonalData1", "taxpayerPersonalData2", "representative",
    # Income
    "activiteSalarieeRevenus", "complementRentePension", "activitesIndependantes",
    "autresRevenusExoneresImposesSource", "revenuImposeAutreEtat",
    # Deductions
    "autresFraisEtFraisActiviteSalarialeAccessoire", "fraisTransport", "fraisRepas",
    "primesEtCotisationsAssurance", "deductionSocialeLogement",
    "fraisMedicauxDentaires", "fraisMedicaux",
    "interetsDettes", "fraisFormation", "donationsAvancesHoiries", "successionHoirieDonation",
    # Assets
    "etatTitres", "relevesFiscauxBancaires", "numerairesList", "objetsMobiliers",
    "biensImmobiliers", "immeubles", "autoMoto", "fraisAdministrationTitres",
    # Documents & tax subject info
    "piecesJustificativesObligatoires", "piecesJustificativesFacultatives",
    "infosComplementairesIes", "prestationsEnCapital",
    # UI / navigation state (intentionally skipped)
    "guidedNav", "userProfil", "piecesJustificativesSubFormInitialized",
}


def ns(tag):
    return f"{{{NS}}}{tag}"


def text(el, tag):
    child = el.find(ns(tag))
    return child.text if child is not None else None


def bool_text(el, tag):
    """Return True/False for XML boolean text, or None if the element is absent."""
    val = text(el, tag)
    if val is None:
        return None
    return val.lower() == "true"


def ctb_label(el):
    """Return 'CTB1' or 'CTB2' based on the isContribuable1 element."""
    return "CTB1" if text(el, "isContribuable1") == "true" else "CTB2"


def format_navs13(raw):
    """Format a 13-digit NAVS13 number as XXX.XXXX.XXXX.XX"""
    if raw and len(raw) == 13 and raw.isdigit():
        return f"{raw[0:3]}.{raw[3:7]}.{raw[7:11]}.{raw[11:13]}"
    return raw


def mask_navs13(formatted):
    """Mask a formatted NAVS13 (XXX.XXXX.XXXX.XX), keeping prefix and last group."""
    if formatted and len(formatted) == 16:
        return f"{formatted[:3]}.****.****.{formatted[-2:]}"
    return formatted and "***"


def mask_iban(iban):
    """Mask an IBAN, keeping the country+check digits and the last 4 characters."""
    if not iban:
        return iban
    compact = iban.replace(" ", "")
    if len(compact) <= 8:
        return "****"
    return f"{compact[:4]}…{compact[-4:]}"


def redact_identifiers(data):
    """Mask direct identifiers in a summarize() dict, in place.

    Masks NAVS13 and IBANs, removes phone and e-mail. Amounts are untouched —
    they are the point of the analysis; the identifiers are not.
    """
    ident = data.get("identification")
    if ident:
        ident["email"] = None
        ident["phone"] = None
        ident["iban"] = mask_iban(ident.get("iban"))
    for tp_key in ("taxpayer", "taxpayer2"):
        tp = data.get(tp_key)
        if tp:
            tp["navs13"] = mask_navs13(tp.get("navs13"))
    ies = data.get("tax_subject_info")
    if ies:
        ies["refund_account_iban"] = mask_iban(ies.get("refund_account_iban"))
    for a in data.get("assets", []):
        if a.get("iban"):
            a["iban"] = mask_iban(a["iban"])
    return data


def open_vaudtax(path):
    """Open a .vaudtax file and return (root_element, list_of_pdf_names)."""
    with zipfile.ZipFile(path) as z:
        xml_name = next(n for n in z.namelist() if n.endswith(".xml"))
        with z.open(xml_name) as f:
            tree = ET.parse(f)
        pdfs = [n for n in z.namelist() if not n.endswith(".xml")]
    return tree.getroot(), pdfs


def extract_attachments(vaudtax_path, keys, outdir=None):
    """Extract attachments by ZIP key (e.g. 'doc17700000000000') and return their paths.

    keys: list of ZIP keys, or ["all"] for every attachment.
    Files persist until the caller deletes them; each is named
    <key>_<original filename> so the name stays unique and readable.
    Works for PDFs, JPEG images, and PNG images.
    """
    root, _ = open_vaudtax(vaudtax_path)
    index = {}
    for doc in root.findall(f".//{ns('documents')}"):
        key = text(doc, "key")
        if key:
            index[key] = text(doc, "filename") or key
    if keys == ["all"]:
        keys = list(index)
    outdir = Path(outdir) if outdir else Path(tempfile.mkdtemp(prefix="vaudtax_"))
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    with zipfile.ZipFile(vaudtax_path) as z:
        for key in keys:
            target = outdir / f"{key}_{index.get(key, key)}"
            with z.open(key) as src:
                target.write_bytes(src.read())
            paths.append(target.resolve())
    return paths


def summarize(root):
    """Return a dict with the key data sections."""
    out = {}

    out["fiscal_year"] = text(root, "fiscalPeriod")
    out["reference"] = text(root, "lastGesdemReference")

    # Identification
    ident = root.find(ns("identification"))
    if ident is not None:
        addr = ident.find(ns("address"))
        locality = addr.find(ns("locality")) if addr is not None else None
        commune = ident.find(ns("communeFiscale"))
        out["identification"] = {
            "email": text(ident, "email"),
            "phone": text(ident, "phone1"),
            "iban": text(ident, "iban"),
            "street": text(addr.find(ns("street")), "longName") if addr is not None else None,
            "house_number": text(addr, "houseNumber") if addr is not None else None,
            "zip": text(locality, "zipCode") if locality is not None else None,
            "locality": text(locality, "longName") if locality is not None else None,
            "commune": text(commune, "nomOfficiel") if commune is not None else None,
        }

    # Taxpayer 1
    ctb1 = root.find(ns("taxpayerPersonalData1"))
    if ctb1 is not None:
        out["taxpayer"] = {
            "first_name": text(ctb1, "firstName"),
            "last_name": text(ctb1, "lastName"),
            "birthdate": text(ctb1, "birthdate"),
            "navs13": format_navs13(text(ctb1, "navs13")),
            "profession": text(ctb1, "profession"),
            "working_location": text(ctb1, "workingLocation"),
            "working_situation": [el.text for el in ctb1.findall(ns("workingSituations"))],
            "marital_status": text(root.find(ns("identification")), "maritalStatus"),
        }

    # Income (employed activity)
    income_entries = []
    for el in root.findall(ns("activiteSalarieeRevenus")):
        income_entries.append({
            "employer": text(el, "employeur"),
            "type": text(el, "type"),
            "activity_rate_pct": text(el, "tauxActivite"),
            "date_start": text(el, "dateDebut"),
            "date_end": text(el, "dateFin"),
            "net_salary_chf": text(el, "salaireNet"),
            "pension_contribution_chf": text(el, "cotisationOrdinaire"),
            "other_contractual_contribution_chf": text(el, "autreCotiContractuelle"),
            "taxpayer": ctb_label(el),
        })
    out["income"] = income_entries

    # Transport costs
    transport = []
    for el in root.findall(ns("fraisTransport")):
        transport.append({
            "mean": text(el, "moyenTransport"),
            "from": text(el, "domicile"),
            "to": text(el, "lieuTravail"),
            "date_start": text(el, "dateDebut"),
            "date_end": text(el, "dateFin"),
            "days": text(el, "nbJours"),
            "km": text(el, "nbKilometres"),
            "is_flat_rate": bool_text(el, "isForfait"),
            "justification": text(el, "justification"),
            "taxpayer": ctb_label(el),
        })
    out["transport_costs"] = transport

    # Meal costs
    meals = []
    for el in root.findall(ns("fraisRepas")):
        meals.append({
            "type": text(el, "fraisRepasType"),
            "days": text(el, "nbJours"),
            "date_start": text(el, "dateDebut"),
            "date_end": text(el, "dateFin"),
            "from": text(el, "domicile"),
            "to": text(el, "lieuTravail"),
            "taxpayer": ctb_label(el),
        })
    out["meal_costs"] = meals

    # Insurance / 3rd pillar
    ins = root.find(ns("primesEtCotisationsAssurance"))
    if ins is not None:
        out["insurance_premiums"] = {
            "gross_premiums_chf": text(ins, "montantPrimesBrutes"),
            "subsidies_chf": text(ins, "montantSubsides"),
            "third_pillar_a_chf": text(ins, "formesReconnuesPrevoyanceIndividuelleContribuable1"),
            "third_pillar_a_ctb2_chf": text(ins, "formesReconnuesPrevoyanceIndividuelleContribuable2"),
        }

    # Rent deduction (skip when not initialized)
    rent = root.find(ns("deductionSocialeLogement"))
    if rent is not None and bool_text(rent, "isInitialized") is not False:
        loyer = text(rent, "loyerAnnuelNetPayeSansCharge")
        if loyer:
            out["rent_deduction"] = {"annual_rent_chf": loyer}

    # Management fees for securities (fraisAdministrationTitres)
    frat = root.find(ns("fraisAdministrationTitres"))
    if frat is not None:
        out["management_fees_securities"] = {
            "is_initialized": bool_text(frat, "isInitialized"),
            "is_private": bool_text(frat, "isPrivate"),
            # Amount is typically calculated as 1.5‰ of total securities value (CODE 490)
        }

    # Medical / dental costs (fraisMedicauxDentaires in 2025+, fraisMedicaux in older years)
    medical = []
    for el in itertools.chain(root.findall(ns("fraisMedicauxDentaires")), root.findall(ns("fraisMedicaux"))):
        montant = text(el, "montantBrut")
        if montant:
            net = text(el, "montantFrais") or text(el, "montantACharge")
            medical.append({
                "insurer": text(el, "etabliPar"),
                "type": text(el, "type"),
                "gross_amount_chf": montant,
                "net_amount_chf": net,
                "date_payment": text(el, "datePaiement"),
                "taxpayer": text(el, "concerne"),
            })
    out["medical_costs"] = medical

    # Other professional expenses / misc deduction (autresFraisEtFraisActiviteSalarialeAccessoire)
    autres_frais = root.find(ns("autresFraisEtFraisActiviteSalarialeAccessoire"))
    if autres_frais is not None:
        ctb1_frais = autres_frais.find(ns("contribuable1"))
        ctb2_frais = autres_frais.find(ns("contribuable2"))
        out["other_professional_expenses"] = {
            "ctb1_type": text(ctb1_frais, "autresFraisDeductionType") if ctb1_frais is not None else None,
            "ctb1_forfait_chf": text(ctb1_frais, "autresFraisFraisForfaitaires") if ctb1_frais is not None else None,
            "ctb1_effectif_chf": text(ctb1_frais, "autresFraisFraisEffectifs") if ctb1_frais is not None else None,
            "ctb2_type": text(ctb2_frais, "autresFraisDeductionType") if ctb2_frais is not None else None,
            "ctb2_forfait_chf": text(ctb2_frais, "autresFraisFraisForfaitaires") if ctb2_frais is not None else None,
            "ctb2_effectif_chf": text(ctb2_frais, "autresFraisFraisEffectifs") if ctb2_frais is not None else None,
        }

    # Taxpayer 2 (spouse/partner)
    ctb2_el = root.find(ns("taxpayerPersonalData2"))
    if ctb2_el is not None:
        out["taxpayer2"] = {
            "first_name": text(ctb2_el, "firstName"),
            "last_name": text(ctb2_el, "lastName"),
            "birthdate": text(ctb2_el, "birthdate"),
            "navs13": format_navs13(text(ctb2_el, "navs13")),
            "profession": text(ctb2_el, "profession"),
            "working_location": text(ctb2_el, "workingLocation"),
            "working_situation": [el.text for el in ctb2_el.findall(ns("workingSituations"))],
        }

    # Pension / rentes income (complementRentePension)
    # The section is always present in the XML; skip if isInitialized=false.
    pensions = []
    for el in root.findall(ns("complementRentePension")):
        if text(el, "isInitialized") == "false":
            continue
        pensions.append({
            "type": text(el, "type"),
            "amount_chf": text(el, "montant") or text(el, "montantRente"),
            "taxpayer": ctb_label(el),
        })
    out["pension_income"] = pensions

    # Self-employment income (activitesIndependantes)
    # The section is always present; contains sub-elements per contributor.
    # Skip if isInitialized=false.
    self_emp = []
    for el in root.findall(ns("activitesIndependantes")):
        if text(el, "isInitialized") == "false":
            continue
        for ctb_tag, ctb_code in (("activitesIndependantesCtb1", "CTB1"),
                                   ("activitesIndependantesCtb2", "CTB2")):
            ctb_el = el.find(ns(ctb_tag))
            if ctb_el is None:
                continue
            net = text(ctb_el, "revenuNet") or text(ctb_el, "resultatNet")
            if net:
                self_emp.append({
                    "activity": text(ctb_el, "activite") or text(ctb_el, "designation"),
                    "net_revenue_chf": net,
                    "taxpayer": ctb_code,
                })
    out["self_employment_income"] = self_emp

    # Debt interest deductions (interetsDettes, code 520)
    dettes = root.find(ns("interetsDettes"))
    if dettes is not None:
        ctb1_d = dettes.find(ns("contribuable1"))
        ctb2_d = dettes.find(ns("contribuable2"))
        if ctb1_d is not None or ctb2_d is not None:
            out["debt_interest"] = {
                "ctb1_amount_chf": text(ctb1_d, "montantInteretsDettes") if ctb1_d is not None else None,
                "ctb2_amount_chf": text(ctb2_d, "montantInteretsDettes") if ctb2_d is not None else None,
            }
        else:
            out["debt_interest"] = {
                "ctb1_amount_chf": text(dettes, "montantInteretsDettes") or text(dettes, "montant"),
                "ctb2_amount_chf": None,
            }

    # Education / training costs (fraisFormation)
    education = []
    for el in root.findall(ns("fraisFormation")):
        education.append({
            "amount_chf": text(el, "montant") or text(el, "montantFrais"),
            "taxpayer": ctb_label(el),
        })
    out["education_costs"] = education

    # Real estate — current XML uses biensImmobiliers; older years used immeubles
    real_estate = []
    for el in itertools.chain(root.findall(ns("biensImmobiliers")),
                              root.findall(ns("immeubles"))):
        if text(el, "isInitialized") == "false":
            continue
        addr = el.find(ns("address"))
        commune = el.find(ns("communeFiscale"))
        street = None
        locality = None
        if addr is not None:
            street_el = addr.find(ns("street"))
            loc_el = addr.find(ns("locality"))
            if street_el is not None:
                street = text(street_el, "longName")
            if loc_el is not None:
                locality = text(loc_el, "longName")
        real_estate.append({
            "designation": text(el, "designation") or street,
            "address": street,
            "locality": locality,
            "commune": text(commune, "nomOfficiel") if commune is not None else None,
            "parcel_number": text(el, "numParcelle"),
            "is_built": bool_text(el, "batimentExiste"),
            "fiscal_value_chf": (text(el, "estimationFiscale")
                                 or text(el, "valeurFiscale")
                                 or text(el, "valeurVenale")),
            "rental_income_chf": text(el, "revenuLocatif") or text(el, "loyerBrut"),
            "is_main_residence": bool_text(el, "typeLogementPrincipal"),
            "is_rented_to_third_party": bool_text(el, "isLocationTiers"),
            "date_acquisition": text(el, "dateAcquisition"),
            "ownership_share": (f"{text(el, 'partProprieteNum')}/{text(el, 'partProprieteDenom')}"
                                if text(el, "partProprieteNum") else None),
            "taxpayer": text(el, "contribuable") or ctb_label(el),
        })
    out["real_estate"] = real_estate

    # Donations / advances on inheritance — given or received during the year.
    # Not income (donations are exempt for direct descendants in VD), but
    # mandatory to declare. Affects fortune for the recipient.
    donations = []
    for el in root.findall(ns("donationsAvancesHoiries")):
        if text(el, "isInitialized") == "false":
            continue
        op_type = text(el, "typeOperation") or ""
        donations.append({
            "operation": op_type,
            "direction": ("RECUE" if "RECUE" in op_type
                          else "VERSEE" if "VERSEE" in op_type else None),
            "kinship": text(el, "lienParente"),
            "date": text(el, "dateDonation"),
            "amount_chf": text(el, "montantDonation"),
            "counterparty_first_name": text(el, "prenom"),
            "counterparty_last_name": text(el, "nom"),
            "taxpayer": text(el, "contribuable") or ctb_label(el),
        })
    out["donations"] = donations

    # Vehicles (autoMoto)
    # The section is always present; skip if isInitialized=false.
    vehicles = []
    for el in root.findall(ns("autoMoto")):
        if text(el, "isInitialized") == "false":
            continue
        vehicles.append({
            "designation": text(el, "designation") or text(el, "marque"),
            "value_chf": text(el, "valeurVenale") or text(el, "valeur"),
            "taxpayer": text(el, "contribuable") or ctb_label(el),
        })
    out["vehicles"] = vehicles

    # Tax subject info (infosComplementairesIes)
    ies = root.find(ns("infosComplementairesIes"))
    if ies is not None:
        out["tax_subject_info"] = {
            "assujetti_ifd": bool_text(ies, "assujettiIFD"),
            "assujetti_icc": bool_text(ies, "assujettiICC"),
            "refund_account_iban": text(ies, "numeroComptePostal"),
        }

    # Assets: bank accounts / securities (etatTitres)
    assets = []
    for el in root.findall(ns("etatTitres")):
        country = el.find(ns("country"))
        devise = el.find(ns("devise"))
        assets.append({
            "type": "compte",
            "institution": text(el, "etablissement"),
            "iban": text(el, "iban"),
            "country": text(country, "iso2Id") if country is not None else None,
            "currency": text(devise, "label") if devise is not None else None,
            "balance_chf": text(el, "soldeCompteCHF"),
            "yield_type": text(el, "rendementType"),
            "yield_amount": text(el, "rendementSoumisIA"),
            "yield_amount_non_ia": text(el, "rendementNonSoumisIA"),
            "date_opened": text(el, "dateOuverture"),
            "date_closed": text(el, "dateCloture"),
            "taxpayer": text(el, "contribuable"),
        })

    # Investment portfolios / fiscal bank statements (relevesFiscauxBancaires)
    # This covers brokerage accounts like IBKR: total portfolio value + income
    for el in root.findall(ns("relevesFiscauxBancaires")):
        country = el.find(ns("country"))
        assets.append({
            "type": "portefeuille",
            "institution": text(el, "designation"),
            "account_number": text(el, "numeroCompte"),
            "country": text(country, "iso2Id") if country is not None else None,
            "valeur_fiscale_chf": text(el, "valeurFiscaleFinaleSoumisIES"),
            "revenus_bruts_chf": text(el, "revenusBrutsSoumisIES"),
            "montant_ies_chf": text(el, "montantIES"),
            "taxpayer": text(el, "contribuable"),
        })

    # Cash / numeraire balances (numerairesList)
    for el in root.findall(ns("numerairesList")):
        assets.append({
            "type": "numeraire",
            "valeur_imposable_chf": text(el, "valeurImposable"),
            "taxpayer": text(el, "contribuable"),
        })

    # Movable assets / crypto (objetsMobiliers items, if any)
    for el in root.findall(f".//{ns('objetsMobiliers')}/{ns('item')}"):
        assets.append({
            "type": "objet_mobilier",
            "designation": text(el, "designation"),
            "valeur_chf": text(el, "valeurVenale"),
            "taxpayer": text(el, "contribuable"),
        })

    out["assets"] = assets

    # Unknown sections — any top-level element not in KNOWN_SECTIONS that has actual data.
    # Sections where every occurrence has isInitialized=false are silently skipped:
    # they're empty form placeholders, not gaps in coverage.
    seen_tags = {child.tag.split("}")[1] for child in root}
    unknown = []
    for tag in sorted(seen_tags - KNOWN_SECTIONS):
        for el in root.findall(ns(tag)):
            # Skip if explicitly uninitialized or entirely empty (no children, no text)
            if text(el, "isInitialized") == "false":
                continue
            if len(el) == 0 and not (el.text or "").strip():
                continue
            unknown.append(tag)
            break
    if unknown:
        out["unknown_sections"] = unknown

    # Attached documents
    # Each <documents> element has: <key> = ZIP entry name, <reference> = UUID,
    # <filename> = original name, <mimeType> = application/pdf | image/jpeg | image/png,
    # <fileSize> = bytes, <label> = human-readable description.
    #
    # Documents have no explicit taxpayer field in the XML. For single filers all
    # documents are CTB1. For joint filers, taxpayer is None here and must be
    # determined from document content (NAVS13, birthdate, or name).
    has_ctb2 = root.find(ns("taxpayerPersonalData2")) is not None
    docs = []
    for doc in root.findall(f".//{ns('documents')}"):
        key = text(doc, "key")
        if key:
            docs.append({
                "zip_key": key,
                "filename": text(doc, "filename"),
                "size_bytes": text(doc, "fileSize"),
                "mime": text(doc, "mimeType"),
                "label": text(doc, "label"),
                "taxpayer": None if has_ctb2 else "CTB1",
            })
    out["attachments"] = docs
    out["has_ctb2"] = has_ctb2

    return out


def print_summary(data):
    print("=== Déclaration VaudTax ===")
    print(f"Année fiscale : {data.get('fiscal_year')}")
    print(f"Référence     : {data.get('reference')}")

    ident = data.get("identification", {})
    print("\n--- Identification ---")
    print(f"Adresse : {ident.get('street')} {ident.get('house_number')}, {ident.get('zip')} {ident.get('locality')}")
    print(f"Commune : {ident.get('commune')}")
    if ident.get("email"):
        print(f"E-mail  : {ident.get('email')}")
    if ident.get("phone"):
        print(f"Tél.    : {ident.get('phone')}")
    print(f"IBAN    : {ident.get('iban')}")

    tp = data.get("taxpayer", {})
    print("\n--- Contribuable ---")
    print(f"Nom           : {tp.get('first_name')} {tp.get('last_name')}")
    print(f"Date naissance: {tp.get('birthdate')}")
    print(f"NAVS13        : {tp.get('navs13')}")
    print(f"Profession    : {tp.get('profession')} à {tp.get('working_location')}")
    print(f"Situation     : {tp.get('working_situation')} / {tp.get('marital_status')}")

    tp2 = data.get("taxpayer2")
    if tp2:
        print("\n--- Contribuable 2 ---")
        print(f"Nom           : {tp2.get('first_name')} {tp2.get('last_name')}")
        print(f"Date naissance: {tp2.get('birthdate')}")
        print(f"NAVS13        : {tp2.get('navs13')}")
        print(f"Profession    : {tp2.get('profession')} à {tp2.get('working_location')}")
        print(f"Situation     : {tp2.get('working_situation')}")

    print("\n--- Revenus ---")
    for e in data.get("income", []):
        lpp = f", LPP CHF {e['pension_contribution_chf']}" if e.get("pension_contribution_chf") else ""
        autre_coti = f" + CHF {e['other_contractual_contribution_chf']}" if e.get("other_contractual_contribution_chf") else ""
        print(f"  {e['employer']} ({e['type']}, {e['activity_rate_pct']}%) : CHF {e['net_salary_chf']} net"
              f"{lpp}{autre_coti} [{e['date_start']} – {e['date_end']}]")
    for e in data.get("pension_income", []):
        print(f"  Rente/pension ({e.get('type')}) [{e['taxpayer']}] : CHF {e.get('amount_chf')}")
    for e in data.get("self_employment_income", []):
        print(f"  Indépendant : {e.get('activity')} [{e['taxpayer']}] : CHF {e.get('net_revenue_chf')} net")

    print("\n--- Déductions ---")
    for t in data.get("transport_costs", []):
        print(f"  Transport : {t['mean']} de {t['from']} à {t['to']}, {t['days']} jours, {t['km']} km")
    for m in data.get("meal_costs", []):
        print(f"  Repas : {m['type']}, {m['days']} jours")
    ins = data.get("insurance_premiums", {})
    if ins:
        print(f"  Primes d'assurance : CHF {ins.get('gross_premiums_chf')} (subsides : CHF {ins.get('subsidies_chf')})")
        print(f"  Pilier 3a CTB1 : CHF {ins.get('third_pillar_a_chf')}")
        if ins.get("third_pillar_a_ctb2_chf"):
            print(f"  Pilier 3a CTB2 : CHF {ins.get('third_pillar_a_ctb2_chf')}")
    rent = data.get("rent_deduction", {})
    if rent:
        print(f"  Loyer annuel : CHF {rent.get('annual_rent_chf')}")
    mgmt = data.get("management_fees_securities", {})
    if mgmt and mgmt.get("is_initialized"):
        print("  Frais administration titres : déclaré (CODE 490)")
    for med in data.get("medical_costs", []):
        print(f"  Frais médicaux ({med.get('insurer')}) : CHF {med.get('gross_amount_chf')} brut / CHF {med.get('net_amount_chf')} net")
    autres = data.get("other_professional_expenses", {})
    if autres and autres.get("ctb1_forfait_chf"):
        print(f"  Autres frais prof. CTB1 : CHF {autres['ctb1_forfait_chf']} ({autres['ctb1_type']})")
    if autres and autres.get("ctb2_forfait_chf"):
        print(f"  Autres frais prof. CTB2 : CHF {autres['ctb2_forfait_chf']} ({autres['ctb2_type']})")
    dettes = data.get("debt_interest", {})
    if dettes:
        if dettes.get("ctb1_amount_chf"):
            print(f"  Intérêts de dettes CTB1 (code 520) : CHF {dettes['ctb1_amount_chf']}")
        if dettes.get("ctb2_amount_chf"):
            print(f"  Intérêts de dettes CTB2 (code 520) : CHF {dettes['ctb2_amount_chf']}")
    for e in data.get("education_costs", []):
        print(f"  Frais de formation [{e['taxpayer']}] : CHF {e.get('amount_chf')}")

    ies = data.get("tax_subject_info", {})
    if ies:
        subj = []
        if ies.get("assujetti_ifd"):
            subj.append("IFD")
        if ies.get("assujetti_icc"):
            subj.append("ICC")
        if subj:
            print(f"  Assujetti : {', '.join(subj)}")
        if ies.get("refund_account_iban"):
            print(f"  IBAN remboursement : {ies['refund_account_iban']}")

    print("\n--- Fortune ---")
    for a in data.get("assets", []):
        t = a.get("type")
        if t == "compte":
            balance = f"CHF {a['balance_chf']}" if a.get("balance_chf") else "(clôturé)"
            yield_info = f", rendement : {a['yield_amount']}" if a.get("yield_amount") else ""
            print(f"  [compte]      {a['institution']} ({a['iban']}) : {balance}{yield_info}")
        elif t == "portefeuille":
            print(f"  [portefeuille] {a['institution']} ({a.get('account_number')}) : "
                  f"valeur fiscale CHF {a.get('valeur_fiscale_chf')}, "
                  f"revenus CHF {a.get('revenus_bruts_chf')}")
        elif t == "numeraire":
            print(f"  [numéraire]   valeur imposable CHF {a.get('valeur_imposable_chf')}")
        elif t == "objet_mobilier":
            print(f"  [objet mob.]  {a.get('designation')} : CHF {a.get('valeur_chf')}")
    for r in data.get("real_estate", []):
        loyer = f", loyer CHF {r['rental_income_chf']}" if r.get("rental_income_chf") else ""
        parc = f" parcelle {r['parcel_number']}" if r.get("parcel_number") else ""
        commune = f" ({r['commune']})" if r.get("commune") else ""
        bati = "" if r.get("is_built") else " [non bâti]"
        share = f" part {r['ownership_share']}" if r.get("ownership_share") and r["ownership_share"] != "1/1" else ""
        designation = r.get("designation") or r.get("address") or "—"
        print(f"  [immeuble]    {designation}{commune}{parc}{bati}{share} : CHF {r.get('fiscal_value_chf')}{loyer}")
    for v in data.get("vehicles", []):
        print(f"  [véhicule]    {v.get('designation')} : CHF {v.get('value_chf')}")

    donations = data.get("donations", [])
    if donations:
        print("\n--- Donations / avances d'hoirie ---")
        for d in donations:
            who = f"{d.get('counterparty_first_name') or ''} {d.get('counterparty_last_name') or ''}".strip()
            kin = f" ({d['kinship']})" if d.get("kinship") else ""
            sign = "←" if d.get("direction") == "RECUE" else "→" if d.get("direction") == "VERSEE" else ""
            print(f"  {sign} CHF {d.get('amount_chf')} {who}{kin} le {d.get('date')} [{d['taxpayer']}]")

    print("\n--- Pièces justificatives ---")
    has_ctb2 = data.get("has_ctb2", False)
    for d in data.get("attachments", []):
        size = f"{int(d['size_bytes']):,} octets" if d.get("size_bytes") else ""
        label = f" — {d['label']}" if d.get("label") else ""
        ctb = f" [{d['taxpayer'] or '?'}]" if has_ctb2 else ""
        print(f"  [{d['zip_key']}] {d['filename']} ({d['mime']}) {size}{label}{ctb}")

    unknown = data.get("unknown_sections")
    if unknown:
        print("\n--- Sections non reconnues ---")
        for s in unknown:
            print(f"  {s}")
        print("  → Ces sections ne sont pas encore gérées par le skill vaudtax.")
        print("  → Pour signaler le problème : https://github.com/fredj/ai-stuff/issues")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Analyse un fichier .vaudtax")
    ap.add_argument("file", help="fichier .vaudtax")
    ap.add_argument("--extract", nargs="+", metavar="KEY",
                    help="extrait les pièces jointes par clé ZIP ('all' pour toutes) "
                         "et affiche un chemin par ligne au lieu du résumé")
    ap.add_argument("--outdir", help="répertoire de sortie (défaut : répertoire temporaire)")
    ap.add_argument("--full", action="store_true",
                    help="affiche les identifiants en clair (NAVS13, IBAN, téléphone, e-mail) ; "
                         "masqués par défaut")
    args = ap.parse_args()
    if args.extract:
        for p in extract_attachments(args.file, args.extract, args.outdir):
            print(p)
    else:
        root, pdfs = open_vaudtax(args.file)
        data = summarize(root)
        if not args.full:
            redact_identifiers(data)
        print_summary(data)
