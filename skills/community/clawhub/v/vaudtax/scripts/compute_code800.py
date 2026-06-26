#!/usr/bin/env python3
"""
compute_code800.py — Estimate revenu imposable ICC (code 800), IFD, and fortune
from a .vaudtax file, applying the official deduction rules.

Outputs the three values ready to pass to calculate_taxes.py.

Usage:
    python compute_code800.py <file.vaudtax>
    python compute_code800.py <file.vaudtax> --json

Deduction rules: Canton Vaud — see DEDUCTIONS.md and TAX_COMPUTATION.md.
"""

import argparse
import json
import warnings

from parse_vaudtax import open_vaudtax, summarize

# ---------------------------------------------------------------------------
# Year-varying constants
# ---------------------------------------------------------------------------

# LPP upper salary limit (LPP art. 8 al. 1) by fiscal year.
# Set by the Federal Council, indexed to AVS maximum annual pension (×3).
# Pillar 3a limits are derived from this via OPP 3 art. 7:
#   max_with_2nd_pillar    = LPP_upper_limit × 8%
#   max_without_2nd_pillar = LPP_upper_limit × 40%
_LPP_UPPER_LIMIT_BY_YEAR = {
    2022: 86_040,
    2023: 88_200,
    2024: 88_200,
    2025: 90_720,
    2026: 90_720,
}


def _pillar3a_limits(fiscal_year: int) -> tuple:
    """Return (max_with_lpp, max_without_lpp) per OPP 3 art. 7.

    max_with_lpp    = LPP_upper_limit × 8%   (for employees enrolled in a pension fund)
    max_without_lpp = LPP_upper_limit × 40%  (for self-employed with no 2nd pillar)
    """
    lim = _LPP_UPPER_LIMIT_BY_YEAR.get(fiscal_year)
    if lim is None:
        known = max(_LPP_UPPER_LIMIT_BY_YEAR)
        warnings.warn(
            f"Fiscal year {fiscal_year} not in _LPP_UPPER_LIMIT_BY_YEAR; "
            f"falling back to {known}. Update _LPP_UPPER_LIMIT_BY_YEAR when "
            f"the Federal Council publishes new LPP limits."
        )
        lim = _LPP_UPPER_LIMIT_BY_YEAR[known]
    return round(lim * 0.08), round(lim * 0.40)


# ---------------------------------------------------------------------------
# Deduction constants — verify against official instructions each fiscal year
# Source: Canton Vaud instructions générales (21001), published annually at vd.ch
# ---------------------------------------------------------------------------

# Transport ICC forfait: one-way km → annual deduction CHF
_ICC_TRANSPORT_FORFAIT = [
    (20, 3001), (25, 3136), (30, 3288), (31, 3320), (35, 3448),
    (40, 3608), (45, 3768), (51, 4080),
]
_IFD_TRANSPORT_MAX     = 3300   # IFD cap
_MEAL_PER_DAY          = 15     # CHF / jour, repas hors domicile
_MEAL_MAX              = 3200   # annual cap, regular lunch away from home
_MEAL_CANTINE_PER_DAY  = 7.5    # CHF / jour, cantine subventionnée
_MEAL_CANTINE_MAX      = 1600   # annual cap, cantine subventionnée
_ICC_INS_SINGLE        = 5000   # insurance premiums ICC cap, single
_ICC_INS_MARRIED       = 9900   # insurance premiums ICC cap, married
_IFD_INS_SINGLE        = 1800   # IFD cap combined with savings interest
_IFD_INS_MARRIED       = 3700   # IFD cap combined with savings interest
_ICC_EPARGNE_SINGLE    = 1600   # savings interest deduction ICC, single
_ICC_EPARGNE_MARRIED   = 3300   # savings interest deduction ICC, married
_ICC_LOGEMENT_PLAFOND_SINGLE  = 11100  # max rent for housing deduction, single
_ICC_LOGEMENT_PLAFOND_MARRIED = 13700  # max rent for housing deduction, married
_ICC_LOGEMENT_PLAFOND_PER_CHILD = 3700 # additional plafond per dependant child
_ICC_LOGEMENT_MAX_DEDUCTION   = 6800   # absolute max deduction regardless of family
_ADMIN_TITRES_PERMILLE = 1.5    # 1.5‰ of portfolio fiscal value (code 490)


def _transport_icc_forfait(km: int) -> int:
    for threshold, amount in _ICC_TRANSPORT_FORFAIT:
        if km <= threshold:
            return amount
    return _ICC_TRANSPORT_FORFAIT[-1][1]


def compute(data: dict) -> dict:
    """Estimate revenu_icc, revenu_ifd, fortune_icc from summarize() output.

    Returns a dict with keys:
        revenu_icc    — estimated ICC taxable income (code 800)
        revenu_ifd    — estimated IFD taxable income
        fortune_icc   — total declared assets
        breakdown     — itemised amounts used in the computation
    """
    fiscal_year = int(data.get("fiscal_year") or 0)
    pillar3a_max_lpp, _pillar3a_max_no_lpp = _pillar3a_limits(fiscal_year)

    marital = (data.get("taxpayer") or {}).get("marital_status", "CELIBATAIRE")
    is_married = marital in ("MARIE", "PARTENARIAT_ENREGISTRE")

    # ── Income ────────────────────────────────────────────────────────────
    salary = sum(
        int(e["net_salary_chf"])
        for e in data.get("income", [])
        if e.get("net_salary_chf")
    )
    pensions = sum(
        int(e["amount_chf"])
        for e in data.get("pension_income", [])
        if e.get("amount_chf")
    )
    self_emp = sum(
        int(e["net_revenue_chf"])
        for e in data.get("self_employment_income", [])
        if e.get("net_revenue_chf")
    )
    savings_interest = 0.0
    investment_income = 0.0
    for a in data.get("assets", []):
        if a.get("yield_amount"):
            try:
                amt = float(a["yield_amount"])
                if a.get("type") == "compte":
                    savings_interest += amt
                investment_income += amt
            except (ValueError, TypeError):
                pass
        if a.get("revenus_bruts_chf"):
            try:
                investment_income += float(a["revenus_bruts_chf"])
            except (ValueError, TypeError):
                pass
    gross_income = salary + pensions + self_emp + investment_income

    # ── Code 140 — transport ──────────────────────────────────────────────
    transport_icc = transport_ifd = 0
    for t in data.get("transport_costs", []):
        km = int(t.get("km") or 0)
        mean = t.get("mean") or ""
        is_flat_rate = t.get("is_flat_rate") or False
        # Apply forfait table when:
        #   - public transport declared, OR
        #   - car declared with isForfait=true (car used but deduction taken
        #     at TP forfait rate, e.g. when taxpayer must transport equipment)
        if "PUBLIC" in mean or is_flat_rate:
            icc_amount = _transport_icc_forfait(km)
            transport_icc += icc_amount
            transport_ifd += min(icc_amount, _IFD_TRANSPORT_MAX)
        # VEHICULE_PRIVE without forfait: km × rate × days — not implemented

    # ── Code 150 — meals (per-day forfait, capped annually) ───────────────
    meals = 0
    for m in data.get("meal_costs", []):
        t = m.get("type") or ""
        days = int(m.get("days") or 0)
        if "CANTINE" in t or "EMPLOYEUR" in t:
            meals += min(round(days * _MEAL_CANTINE_PER_DAY), _MEAL_CANTINE_MAX)
        else:
            meals += min(days * _MEAL_PER_DAY, _MEAL_MAX)

    # ── Code 160 — autres frais professionnels ────────────────────────────
    opex = data.get("other_professional_expenses") or {}
    autres_frais = (int(opex.get("ctb1_forfait_chf") or 0)
                    + int(opex.get("ctb2_forfait_chf") or 0))
    if not autres_frais:
        autres_frais = max(2000, min(4000, round(salary * 0.03)))

    # ── Code 300 — assurances ─────────────────────────────────────────────
    ins = data.get("insurance_premiums") or {}
    ins_net = int(ins.get("gross_premiums_chf") or 0) - int(ins.get("subsidies_chf") or 0)
    assurances_icc = min(ins_net, _ICC_INS_MARRIED if is_married else _ICC_INS_SINGLE)
    # IFD: assurances + savings interest share a single cap
    assurances_ifd = min(ins_net + savings_interest,
                         _IFD_INS_MARRIED if is_married else _IFD_INS_SINGLE)

    # ── Code 310 — pilier 3a ──────────────────────────────────────────────
    pilier3a = (min(int(ins.get("third_pillar_a_chf") or 0), pillar3a_max_lpp)
                + min(int(ins.get("third_pillar_a_ctb2_chf") or 0), pillar3a_max_lpp))

    # ── Code 480 — intérêts capitaux d'épargne (ICC only) ─────────────────
    cap_480 = _ICC_EPARGNE_MARRIED if is_married else _ICC_EPARGNE_SINGLE
    interets_epargne = min(savings_interest, cap_480)

    # ── Code 520 — intérêts de dettes ────────────────────────────────────
    # Debt interest is fully deductible (no cap) for both ICC and IFD.
    dettes = data.get("debt_interest") or {}
    interets_dettes = (int(dettes.get("ctb1_amount_chf") or 0)
                       + int(dettes.get("ctb2_amount_chf") or 0))

    # ── Code 490 — frais administration titres ────────────────────────────
    portfolio_value = sum(
        float(a.get("valeur_fiscale_chf") or 0)
        for a in data.get("assets", [])
        if a.get("type") == "portefeuille"
    )
    admin_titres = round(portfolio_value * _ADMIN_TITRES_PERMILLE / 1000)

    # ── Code 700 (before logement and medical) ────────────────────────────
    code_700_pre = round(gross_income
                         - transport_icc - meals - autres_frais
                         - assurances_icc - pilier3a - interets_epargne - admin_titres
                         - interets_dettes)

    # ── Code 660 — déduction logement (ICC only) ──────────────────────────
    rent = data.get("rent_deduction") or {}
    loyer = int(rent.get("annual_rent_chf") or 0)
    n_children = int(data.get("n_children") or 0)
    plafond_base = _ICC_LOGEMENT_PLAFOND_MARRIED if is_married else _ICC_LOGEMENT_PLAFOND_SINGLE
    plafond = plafond_base + n_children * _ICC_LOGEMENT_PLAFOND_PER_CHILD
    logement_icc = max(0, min(min(loyer, plafond) - round(0.20 * code_700_pre),
                              _ICC_LOGEMENT_MAX_DEDUCTION))
    code_700 = code_700_pre - logement_icc

    # ── Code 710 — frais médicaux ─────────────────────────────────────────
    medical_net = sum(int(m.get("net_amount_chf") or 0)
                      for m in data.get("medical_costs", []))
    medical_icc = max(0, medical_net - round(code_700 * 0.05))

    # ── Code 800 ICC ──────────────────────────────────────────────────────
    # No social deductions for single/no children in Vaud 2025
    revenu_icc = code_700 - medical_icc

    # ── IFD ───────────────────────────────────────────────────────────────
    revenu_interm = round(gross_income
                          - transport_ifd - meals - autres_frais
                          - assurances_ifd - pilier3a - admin_titres
                          - interets_dettes)
    medical_ifd = min(max(0, medical_net - round(revenu_interm * 5 / 95)), medical_net)
    ifd_social = 2800 if is_married else 0
    revenu_ifd = revenu_interm - medical_ifd - ifd_social

    # ── Fortune ICC ───────────────────────────────────────────────────────
    fortune = sum(
        float(a.get(field) or 0)
        for a in data.get("assets", [])
        for field in ("balance_chf", "valeur_fiscale_chf", "valeur_imposable_chf", "valeur_chf")
        if a.get(field)
    )
    fortune += sum(
        float(r.get("fiscal_value_chf") or 0)
        for r in data.get("real_estate", [])
    )
    fortune += sum(
        float(v.get("value_chf") or 0)
        for v in data.get("vehicles", [])
    )
    fortune_icc = round(fortune)

    return {
        "revenu_icc":  revenu_icc,
        "revenu_ifd":  revenu_ifd,
        "fortune_icc": fortune_icc,
        "breakdown": {
            "gross_income":     round(gross_income),
            "transport_icc":    transport_icc,
            "transport_ifd":    transport_ifd,
            "meals":            meals,
            "autres_frais":     autres_frais,
            "assurances_icc":   assurances_icc,
            "assurances_ifd":   round(assurances_ifd),
            "pilier3a":         pilier3a,
            "interets_epargne": round(interets_epargne),
            "interets_dettes":  interets_dettes,
            "admin_titres":     admin_titres,
            "logement_icc":     logement_icc,
            "code_700":         code_700,
            "medical_icc":      medical_icc,
            "medical_ifd":      medical_ifd,
        },
    }


def _print_results(result: dict) -> None:
    b = result["breakdown"]
    periode = result.get("periode", "?")

    print()
    print("=" * 52)
    print(f"  Revenus imposables estimés — {periode}")
    print("=" * 52)
    print(f"\n  Revenu brut                    CHF {b['gross_income']:>10,}")
    print("\n  Déductions ICC")
    print(f"  {'─' * 48}")
    print(f"  Transport (code 140)           CHF {b['transport_icc']:>10,}")
    print(f"  Repas (code 150)               CHF {b['meals']:>10,}")
    print(f"  Autres frais prof. (code 160)  CHF {b['autres_frais']:>10,}")
    print(f"  Assurances (code 300)          CHF {b['assurances_icc']:>10,}")
    print(f"  Pilier 3a (code 310)           CHF {b['pilier3a']:>10,}")
    print(f"  Intérêts épargne (code 480)    CHF {b['interets_epargne']:>10,}")
    print(f"  Admin. titres (code 490)       CHF {b['admin_titres']:>10,}")
    print(f"  Intérêts dettes (code 520)     CHF {b['interets_dettes']:>10,}")
    print(f"  Logement (code 660)            CHF {b['logement_icc']:>10,}")
    print(f"  Frais médicaux (code 710)      CHF {b['medical_icc']:>10,}")
    print(f"\n  Code 700                       CHF {b['code_700']:>10,}")
    print(f"\n  ► REVENU IMPOSABLE ICC (800)   CHF {result['revenu_icc']:>10,}")
    print()
    print("  Déductions IFD")
    print(f"  {'─' * 48}")
    print(f"  Transport (code 140)           CHF {b['transport_ifd']:>10,}")
    print(f"  Assurances+épargne (code 300)  CHF {b['assurances_ifd']:>10,}")
    print(f"  Frais médicaux (code 710)      CHF {b['medical_ifd']:>10,}")
    print(f"\n  ► REVENU IMPOSABLE IFD         CHF {result['revenu_ifd']:>10,}")
    print()
    print(f"  ► FORTUNE IMPOSABLE ICC        CHF {result['fortune_icc']:>10,}")
    print()
    print("  Ready for calculate_taxes.py:")
    print(f"    --revenu-icc {result['revenu_icc']} --fortune-icc {result['fortune_icc']}"
          f" --revenu-ifd {result['revenu_ifd']}")
    print("=" * 52)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Estimate ICC/IFD taxable income (code 800) from a .vaudtax file."
    )
    parser.add_argument("file", help="Path to the .vaudtax file")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    root, _ = open_vaudtax(args.file)
    data = summarize(root)
    result = compute(data)

    result["periode"] = data.get("fiscal_year", "?")
    # commune lives under identification; marital_status under taxpayer.
    result["commune"] = (data.get("identification") or {}).get("commune")
    result["marital_status"] = (data.get("taxpayer") or {}).get("marital_status")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_results(result)


if __name__ == "__main__":
    main()
