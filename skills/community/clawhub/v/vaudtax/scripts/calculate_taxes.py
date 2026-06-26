#!/usr/bin/env python3
"""
calculate_taxes.py — Query the Canton Vaud official tax calculator.

Posts form data to https://www.vd.ch/.../calculer-mes-impots and parses
the HTML response. No third-party libraries required.

Usage (standalone):
    python calculate_taxes.py \\
        --periode 2025 \\
        --commune "Yverdon-les-Bains" \\
        --etat-civil single \\
        --revenu-icc 99212 \\
        --fortune-icc 337081 \\
        --revenu-ifd 102946

Usage (as module):
    from calculate_taxes import calculate_taxes
    result = calculate_taxes(
        periode=2025,
        commune="Yverdon-les-Bains",
        etat_civil="single",
        revenu_icc=99212,
        fortune_icc=337081,
        revenu_ifd=102946,
    )
    print(result["total_icc_ifd"])  # e.g. "23'450.65"
"""

import argparse
import json
import re
import sys
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

URL = "https://www.vd.ch/etat-droit-finances/impots/impots-pour-les-individus/calculer-mes-impots"

ETAT_CIVIL_MAP = {
    "single":   "1",  # Personne seule / célibataire / veuf / séparé / divorcé
    "married":  "2",  # Couple marié / Partenariat enregistré
    "parent":   "3",  # Famille monoparentale
    # also accept the French labels and numeric strings
    "1": "1", "2": "2", "3": "3",
    "personne seule": "1",
    "couple marié / partenariat enregistré": "2",
    "famille monoparentale": "3",
}


def _normalize_commune(name: str) -> str:
    """Convert commune display name to the form value used by the website.

    "Yverdon-les-Bains" → "yverdonlesbains"
    "Le Mont-sur-Lausanne" → "lemontsurLausanne"  (server is inconsistent,
    so we just lowercase + strip accents + remove non-alpha chars)
    """
    nfkd = "".join(c for c in unicodedata.normalize("NFKD", name) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", nfkd.lower())


def _build_payload(
    periode: int,
    commune: str,
    etat_civil: str,
    n_enfants: int,
    n_enfants_demi: int,
    n_enfants_menage: int,
    revenu_icc: int,
    fortune_icc: int,
    revenu_ifd: int,
    calcul_icc: bool,
    calcul_ifd: bool,
) -> bytes:
    etat_civil_val = ETAT_CIVIL_MAP.get(str(etat_civil).lower())
    if etat_civil_val is None:
        raise ValueError(
            f"Unknown etat_civil {etat_civil!r}. "
            f"Use: {list(ETAT_CIVIL_MAP.keys())}"
        )
    commune_val = _normalize_commune(commune)

    fields = []
    if calcul_icc:
        fields.append(("tx_vdsqlicalculetteaci_pi1[calculICC]", "on"))
    if calcul_ifd:
        fields.append(("tx_vdsqlicalculetteaci_pi1[calculIFD]", "on"))

    fields += [
        ("tx_vdsqlicalculetteaci_pi1[periode]",              str(periode)),
        ("tx_vdsqlicalculetteaci_pi1[commune]",              commune_val),
        ("tx_vdsqlicalculetteaci_pi1[commune_reference]",    commune_val),
        ("tx_vdsqlicalculetteaci_pi1[etatCivil]",            etat_civil_val),
        ("tx_vdsqlicalculetteaci_pi1[noEnfants]",            str(n_enfants)),
        ("tx_vdsqlicalculetteaci_pi1[noEnfantsDemiQuotient]",str(n_enfants_demi)),
        ("tx_vdsqlicalculetteaci_pi1[noEnfantsMenage]",      str(n_enfants_menage)),
        ("tx_vdsqlicalculetteaci_pi1[revenuImposableICC]",   str(revenu_icc)),
        ("tx_vdsqlicalculetteaci_pi1[tauxRevenuImposableICC]","0"),
        ("tx_vdsqlicalculetteaci_pi1[fortuneImposableICC]",  str(fortune_icc)),
        ("tx_vdsqlicalculetteaci_pi1[tauxFortuneImposableICC]","0"),
        ("tx_vdsqlicalculetteaci_pi1[revenuImposableIFD]",   str(revenu_ifd)),
        ("tx_vdsqlicalculetteaci_pi1[tauxRevenuImposableIFD]","0"),
        ("tx_vdsqlicalculetteaci_pi1[afficher]",             "Afficher le résultat"),
    ]
    return urlencode(fields).encode("utf-8")


def _parse_results(html: str) -> dict:
    """Extract all res_* field values from the response HTML."""
    results = {}
    # Match: id="tx_vdsqlicalculetteaci_pi1_res_FIELD" ... value="VALUE"
    pattern = re.compile(
        r'id="tx_vdsqlicalculetteaci_pi1_res_([^"]+)"[^>]*value="([^"]*)"'
    )
    for m in pattern.finditer(html):
        key = m.group(1)
        # normalise the one known inconsistency (revenu_coeff_comm vs revenu_coef_comm)
        key = key.replace("revenu_coeff_comm", "revenu_coef_comm")
        results[key] = m.group(2)
    return results


def _parse_chf(value: str) -> float:
    """Parse a CHF string like "23'450.65" or "1'198.00" to float."""
    return float(value.replace("'", "").replace(" ", ""))


def calculate_marginal_rate(
    periode: int,
    commune: str,
    etat_civil: str = "single",
    n_enfants: int = 0,
    n_enfants_demi: int = 0,
    n_enfants_menage: int = 0,
    revenu_icc: int = 0,
    fortune_icc: int = 0,
    revenu_ifd: int = 0,
    delta: int = 1000,
    timeout: int = 15,
) -> dict:
    """Compute the marginal tax rate using the finite difference method.

    Makes two calls to the official calculator (base and base+delta) and
    returns the marginal rate as percentages for ICC, IFD, and combined.

    Parameters
    ----------
    delta : income increment in CHF used for the finite difference (default 1000)

    Returns
    -------
    dict with keys:
        marginal_icc        : ICC marginal rate in % (float)
        marginal_ifd        : IFD marginal rate in % (float)
        marginal_total      : combined marginal rate in % (float)
        base_total_icc_ifd  : base total tax (float)
        bumped_total_icc_ifd: bumped total tax (float)
    """
    base = calculate_taxes(
        periode=periode, commune=commune, etat_civil=etat_civil,
        n_enfants=n_enfants, n_enfants_demi=n_enfants_demi,
        n_enfants_menage=n_enfants_menage,
        revenu_icc=revenu_icc, fortune_icc=fortune_icc, revenu_ifd=revenu_ifd,
        calcul_icc=True, calcul_ifd=True, timeout=timeout,
    )
    bumped = calculate_taxes(
        periode=periode, commune=commune, etat_civil=etat_civil,
        n_enfants=n_enfants, n_enfants_demi=n_enfants_demi,
        n_enfants_menage=n_enfants_menage,
        revenu_icc=revenu_icc + delta, fortune_icc=fortune_icc,
        revenu_ifd=revenu_ifd + delta,
        calcul_icc=True, calcul_ifd=True, timeout=timeout,
    )

    base_icc = _parse_chf(base.get("total_icc", "0"))
    base_ifd = _parse_chf(base.get("total_ifd", "0"))
    bump_icc = _parse_chf(bumped.get("total_icc", "0"))
    bump_ifd = _parse_chf(bumped.get("total_ifd", "0"))

    marginal_icc   = (bump_icc - base_icc) / delta * 100
    marginal_ifd   = (bump_ifd - base_ifd) / delta * 100
    marginal_total = marginal_icc + marginal_ifd

    return {
        "marginal_icc":         round(marginal_icc, 2),
        "marginal_ifd":         round(marginal_ifd, 2),
        "marginal_total":       round(marginal_total, 2),
        "base_total_icc_ifd":   round(base_icc + base_ifd, 2),
        "bumped_total_icc_ifd": round(bump_icc + bump_ifd, 2),
        "delta":                delta,
    }


def calculate_taxes(
    periode: int,
    commune: str,
    etat_civil: str = "single",
    n_enfants: int = 0,
    n_enfants_demi: int = 0,
    n_enfants_menage: int = 0,
    revenu_icc: int = 0,
    fortune_icc: int = 0,
    revenu_ifd: int = 0,
    calcul_icc: bool = True,
    calcul_ifd: bool = True,
    timeout: int = 15,
) -> dict:
    """Query the Canton Vaud tax calculator and return parsed results.

    Parameters
    ----------
    periode       : fiscal year (e.g. 2025)
    commune       : display name of the Vaud commune (e.g. "Yverdon-les-Bains")
    etat_civil    : "single" | "married" | "parent" (or French labels, or "1"/"2"/"3")
    n_enfants     : number of children with full quotient
    n_enfants_demi: number of children with half quotient
    n_enfants_menage: of the above, those living in the household
    revenu_icc    : taxable income for ICC (code 800)
    fortune_icc   : taxable wealth for ICC (code 800)
    revenu_ifd    : taxable income for IFD
    calcul_icc    : include ICC simulation
    calcul_ifd    : include IFD simulation
    timeout       : HTTP timeout in seconds

    Returns
    -------
    dict with keys matching the server result fields (e.g. "total_icc", "total_ifd",
    "total_icc_ifd") plus "commune_normalized".
    Values are strings as returned by the server (e.g. "23'450.65").
    Raises RuntimeError if the server returns no results.
    """
    payload = _build_payload(
        periode, commune, etat_civil,
        n_enfants, n_enfants_demi, n_enfants_menage,
        revenu_icc, fortune_icc, revenu_ifd,
        calcul_icc, calcul_ifd,
    )
    req = Request(URL, data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "vaudtax-skill/1.0")

    try:
        with urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} from server: {e.reason}") from e
    except URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e

    results = _parse_results(html)
    if not results:
        raise RuntimeError(
            "No result fields found in server response. "
            "The form may have changed or the input was rejected."
        )

    results["commune_normalized"] = _normalize_commune(commune)
    return results


def _print_results(results: dict) -> None:
    print()
    print("=" * 52)
    print("  Estimation impôts Canton de Vaud")
    print("=" * 52)

    sections = [
        ("ICC — Revenu", [
            ("revenu_montant_imp", "Revenu imposable"),
            ("revenu_impot_base",  "Impôt de base"),
            ("revenu_coef_cant",   "Coeff. cantonal (%)"),
            ("revenu_cf_cant",     "Impôt cantonal revenu"),
            ("revenu_coef_comm",   "Coeff. communal (%)"),
            ("revenu_cf_comm",     "Impôt communal revenu"),
        ]),
        ("ICC — Fortune", [
            ("fortune_montant_imp","Fortune imposable"),
            ("fortune_impot_base", "Impôt de base"),
            ("fortune_cf_cant",    "Impôt cantonal fortune"),
            ("fortune_cf_comm",    "Impôt communal fortune"),
        ]),
        ("IFD", [
            ("revenu_ifd",         "Revenu imposable IFD"),
            ("revenu_base_ifd",    "Impôt de base IFD"),
            ("rabais_ifd",         "Rabais IFD"),
            ("total_ifd",          "Total IFD"),
        ]),
        ("Totaux", [
            ("total_icc",          "Total ICC"),
            ("total_ifd",          "Total IFD"),
            ("total_icc_ifd",      "TOTAL DÛ (ICC + IFD)"),
        ]),
    ]

    for section_title, fields in sections:
        print(f"\n  {section_title}")
        print("  " + "-" * 48)
        for key, label in fields:
            val = results.get(key, "—")
            print(f"  {label:<32} CHF {val:>12}")

    print()
    print(f"  Part familiale : {results.get('part_familiale', '—')}")
    print(f"  Revenu déterminant pour le taux : {results.get('revenu_taux', '—')}")
    print("=" * 52)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Query the Canton Vaud official tax calculator via HTTP POST."
    )
    parser.add_argument("--periode",     type=int,   required=True,  help="Fiscal year, e.g. 2025")
    parser.add_argument("--commune",     type=str,   required=True,  help='Commune name, e.g. "Yverdon-les-Bains"')
    parser.add_argument("--etat-civil",  type=str,   default="single",
                        help='Marital status: single | married | parent (default: single)')
    parser.add_argument("--enfants",     type=int,   default=0,      help="Children with full quotient (default: 0)")
    parser.add_argument("--enfants-demi",type=int,   default=0,      help="Children with half quotient (default: 0)")
    parser.add_argument("--enfants-menage",type=int, default=0,      help="Children in household (default: 0)")
    parser.add_argument("--revenu-icc",  type=int,   default=0,      help="Taxable income ICC (code 800)")
    parser.add_argument("--fortune-icc", type=int,   default=0,      help="Taxable wealth ICC (code 800)")
    parser.add_argument("--revenu-ifd",  type=int,   default=0,      help="Taxable income IFD")
    parser.add_argument("--no-icc",        action="store_true",      help="Skip ICC simulation")
    parser.add_argument("--no-ifd",        action="store_true",      help="Skip IFD simulation")
    parser.add_argument("--marginal-rate", action="store_true",      help="Compute taux marginal d'imposition (2 HTTP calls)")
    parser.add_argument("--json",          action="store_true",      help="Output raw JSON instead of formatted table")
    args = parser.parse_args()

    if args.marginal_rate:
        try:
            mr = calculate_marginal_rate(
                periode=args.periode,
                commune=args.commune,
                etat_civil=args.etat_civil,
                n_enfants=args.enfants,
                n_enfants_demi=args.enfants_demi,
                n_enfants_menage=args.enfants_menage,
                revenu_icc=args.revenu_icc,
                fortune_icc=args.fortune_icc,
                revenu_ifd=args.revenu_ifd,
            )
        except (RuntimeError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        if args.json:
            print(json.dumps(mr, ensure_ascii=False, indent=2))
        else:
            print()
            print("=" * 52)
            print("  Taux marginal d'imposition")
            print("=" * 52)
            print(f"  ICC (cantonal + communal)  {mr['marginal_icc']:>10.2f} %")
            print(f"  IFD (fédéral direct)       {mr['marginal_ifd']:>10.2f} %")
            print(f"  {'─' * 38}")
            print(f"  TOTAL                      {mr['marginal_total']:>10.2f} %")
            print()
            print(f"  (méthode: Δtax / Δrevenu, Δ = CHF {mr['delta']})")
            print("=" * 52)
            print()
        return

    try:
        results = calculate_taxes(
            periode=args.periode,
            commune=args.commune,
            etat_civil=args.etat_civil,
            n_enfants=args.enfants,
            n_enfants_demi=args.enfants_demi,
            n_enfants_menage=args.enfants_menage,
            revenu_icc=args.revenu_icc,
            fortune_icc=args.fortune_icc,
            revenu_ifd=args.revenu_ifd,
            calcul_icc=not args.no_icc,
            calcul_ifd=not args.no_ifd,
        )
    except (RuntimeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        _print_results(results)


if __name__ == "__main__":
    main()
