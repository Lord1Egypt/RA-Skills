import argparse
import json
import sys

def get_comprehensive_tax(taxable_income):
    if taxable_income <= 0:
        return 0.0, 0.0, 0.0
    brackets = [
        (36000.0, 0.03, 0.0),
        (144000.0, 0.10, 2520.0),
        (300000.0, 0.20, 16920.0),
        (420000.0, 0.25, 31920.0),
        (660000.0, 0.30, 52920.0),
        (960000.0, 0.35, 85920.0),
        (float('inf'), 0.45, 181920.0)
    ]
    for limit, rate, deduction in brackets:
        if taxable_income <= limit:
            return taxable_income * rate - deduction, rate, deduction

def get_bonus_tax(bonus):
    if bonus <= 0:
        return 0.0, 0.0, 0.0
    monthly_bonus = bonus / 12.0
    brackets = [
        (3000.0, 0.03, 0.0),
        (12000.0, 0.10, 210.0),
        (25000.0, 0.20, 1410.0),
        (35000.0, 0.25, 2660.0),
        (55000.0, 0.30, 4410.0),
        (80000.0, 0.35, 7160.0),
        (float('inf'), 0.45, 15160.0)
    ]
    for limit, rate, deduction in brackets:
        if monthly_bonus <= limit:
            return bonus * rate - deduction, rate, deduction

def main():
    parser = argparse.ArgumentParser(description="Calculate tax settlement options (Decision Support System)")
    parser.add_argument("--salary", type=float, default=0.0, help="工资薪金税前总额")
    parser.add_argument("--labor", type=float, default=0.0, help="劳务报酬税前总额")
    parser.add_argument("--manuscript", type=float, default=0.0, help="稿酬税前总额")
    parser.add_argument("--royalty", type=float, default=0.0, help="特许权使用费税前总额")
    parser.add_argument("--bonus", type=float, default=0.0, help="全年一次性奖金")
    parser.add_argument("--options", type=float, default=0.0, help="期权/股权激励所得")
    parser.add_argument("--deductions", type=float, default=0.0, help="专项扣除+专项附加扣除等扣除合计 (不含基本减除60k)")
    parser.add_argument("--paid_salary_tax", type=float, default=0.0, help="已预缴工资个税")
    parser.add_argument("--paid_labor_tax", type=float, default=0.0, help="已预缴劳务/稿酬/特许权个税")
    parser.add_argument("--paid_bonus_tax", type=float, default=0.0, help="已预缴年终奖个税")
    parser.add_argument("--paid_options_tax", type=float, default=0.0, help="已预缴期权个税")
    parser.add_argument("--duplicated_exemption", type=float, default=0.0, help="重复享受的起征点免税额")
    args = parser.parse_args()

    # Calculate statutory income amounts (收入额)
    salary_inc = args.salary
    labor_inc = args.labor * 0.8
    manuscript_inc = args.manuscript * 0.56
    royalty_inc = args.royalty * 0.8
    comp_income = salary_inc + labor_inc + manuscript_inc + royalty_inc

    # Scenario A: Bonus Separate, Options Separate
    taxable_a = max(0.0, comp_income - 60000.0 - args.deductions)
    tax_comp_a, rate_comp_a, qd_comp_a = get_comprehensive_tax(taxable_a)
    tax_bonus_a, rate_bonus_a, _ = get_bonus_tax(args.bonus)
    tax_options_a, rate_options_a, _ = get_comprehensive_tax(args.options)
    total_tax_a = tax_comp_a + tax_bonus_a + tax_options_a

    # Scenario B: Bonus Merged, Options Separate
    taxable_b = max(0.0, comp_income + args.bonus - 60000.0 - args.deductions)
    tax_comp_b, rate_comp_b, qd_comp_b = get_comprehensive_tax(taxable_b)
    tax_options_b, rate_options_b, _ = get_comprehensive_tax(args.options)
    total_tax_b = tax_comp_b + tax_options_b

    # Scenario C: Bonus Separate, Options Merged
    taxable_c = max(0.0, comp_income + args.options - 60000.0 - args.deductions)
    tax_comp_c, rate_comp_c, qd_comp_c = get_comprehensive_tax(taxable_c)
    tax_bonus_c, rate_bonus_c, _ = get_bonus_tax(args.bonus)
    total_tax_c = tax_comp_c + tax_bonus_c

    # Scenario D: Bonus Merged, Options Merged
    taxable_d = max(0.0, comp_income + args.bonus + args.options - 60000.0 - args.deductions)
    tax_comp_d, rate_comp_d, qd_comp_d = get_comprehensive_tax(taxable_d)
    total_tax_d = tax_comp_d

    # Find the best scenario
    scenarios = {
        "A": {
            "name": "年终奖单独计税 + 期权单独计税",
            "comp_tax": tax_comp_a, "comp_rate": rate_comp_a, "comp_taxable": taxable_a,
            "bonus_tax": tax_bonus_a, "bonus_rate": rate_bonus_a,
            "options_tax": tax_options_a, "options_rate": rate_options_a,
            "total_tax": total_tax_a
        },
        "B": {
            "name": "年终奖并入综合所得 + 期权单独计税",
            "comp_tax": tax_comp_b, "comp_rate": rate_comp_b, "comp_taxable": taxable_b,
            "bonus_tax": 0.0, "bonus_rate": 0.0,
            "options_tax": tax_options_b, "options_rate": rate_options_b,
            "total_tax": total_tax_b
        },
        "C": {
            "name": "年终奖单独计税 + 期权并入综合所得",
            "comp_tax": tax_comp_c, "comp_rate": rate_comp_c, "comp_taxable": taxable_c,
            "bonus_tax": tax_bonus_c, "bonus_rate": rate_bonus_c,
            "options_tax": 0.0, "options_rate": 0.0,
            "total_tax": total_tax_c
        },
        "D": {
            "name": "年终奖并入综合所得 + 期权并入综合所得",
            "comp_tax": tax_comp_d, "comp_rate": rate_comp_d, "comp_taxable": taxable_d,
            "bonus_tax": 0.0, "bonus_rate": 0.0,
            "options_tax": 0.0, "options_rate": 0.0,
            "total_tax": total_tax_d
        }
    }

    best_key = min(scenarios, key=lambda k: scenarios[k]["total_tax"])
    best = scenarios[best_key]

    # Prepaid summary
    total_prepaid = args.paid_salary_tax + args.paid_labor_tax + args.paid_bonus_tax + args.paid_options_tax
    settlement_amount = best["total_tax"] - total_prepaid

    # Analysis of tax-saving due to deductions
    deduction_saving = 0.0
    bracket_drop = False
    rate_before = 0.0
    rate_after = 0.0
    if args.deductions > 0:
        # What would tax be without deductions under the same best scenario strategy?
        comp_taxable_no_ded = max(0.0, comp_income - 60000.0)
        tax_comp_no_ded, rate_comp_no_ded, _ = get_comprehensive_tax(comp_taxable_no_ded)
        
        if best_key == "A":
            total_tax_no_ded = tax_comp_no_ded + tax_bonus_a + tax_options_a
            rate_after = rate_comp_a
        elif best_key == "B":
            comp_taxable_no_ded_b = max(0.0, comp_income + args.bonus - 60000.0)
            tax_comp_no_ded_b, rate_comp_no_ded_b, _ = get_comprehensive_tax(comp_taxable_no_ded_b)
            total_tax_no_ded = tax_comp_no_ded_b + tax_options_b
            rate_comp_no_ded = rate_comp_no_ded_b
            rate_after = rate_comp_b
        elif best_key == "C":
            comp_taxable_no_ded_c = max(0.0, comp_income + args.options - 60000.0)
            tax_comp_no_ded_c, rate_comp_no_ded_c, _ = get_comprehensive_tax(comp_taxable_no_ded_c)
            total_tax_no_ded = tax_comp_no_ded_c + tax_bonus_c
            rate_comp_no_ded = rate_comp_no_ded_c
            rate_after = rate_comp_c
        else:
            comp_taxable_no_ded_d = max(0.0, comp_income + args.bonus + args.options - 60000.0)
            tax_comp_no_ded_d, rate_comp_no_ded_d, _ = get_comprehensive_tax(comp_taxable_no_ded_d)
            total_tax_no_ded = tax_comp_no_ded_d
            rate_comp_no_ded = rate_comp_no_ded_d
            rate_after = rate_comp_d
            
        deduction_saving = total_tax_no_ded - best["total_tax"]
        rate_before = rate_comp_no_ded
        if rate_before > rate_after:
            bracket_drop = True

    # Why tax is owed/refunded diagnostics
    diagnostics = []
    if settlement_amount > 0:
        if args.duplicated_exemption > 0:
            extra_tax_due_to_dup = args.duplicated_exemption * best["comp_rate"]
            diagnostics.append(f"基本减除费用（起征点）重复扣除：平时多处扣税重复抵扣了 {args.duplicated_exemption:.2f} 元免税额度，汇算收回导致补税约 {extra_tax_due_to_dup:.2f} 元。")
        if best["comp_rate"] > 0.10:
            diagnostics.append(f"合并计税税率级距跳升：多处收入合并后，年度综合应纳税所得额达 {best['comp_taxable']:.2f} 元，适用税率达 {best['comp_rate']*100:.0f}% 档，高于平时分开扣缴时的税率。")
    elif settlement_amount < 0:
        diagnostics.append("您的各项扣除额（专项附加扣除等）未在平时完全扣除，或平时预扣税率偏高，汇算后产生退税。")

    output = {
        "Inputs": {
            "Comprehensive_Income_Total": comp_income,
            "Salary_Pretax": args.salary,
            "Labor_Pretax": args.labor,
            "Manuscript_Pretax": args.manuscript,
            "Royalty_Pretax": args.royalty,
            "Bonus": args.bonus,
            "Options": args.options,
            "Deductions_Excluding_Basic": args.deductions,
            "Total_Prepaid_Tax": total_prepaid
        },
        "Filing_Scenarios": {
            "A_Both_Separate": {
                "Description": "年终奖与期权均单独计税",
                "Total_Tax": total_tax_a,
                "Comprehensive_Tax": tax_comp_a,
                "Comprehensive_Rate": f"{rate_comp_a*100:.0f}%",
                "Bonus_Tax": tax_bonus_a,
                "Bonus_Rate": f"{rate_bonus_a*100:.0f}%",
                "Options_Tax": tax_options_a,
                "Options_Rate": f"{rate_options_a*100:.0f}%"
            },
            "B_Bonus_Merged_Options_Separate": {
                "Description": "仅期权单独计税，年终奖并入综合所得",
                "Total_Tax": total_tax_b,
                "Comprehensive_Tax": tax_comp_b,
                "Comprehensive_Rate": f"{rate_comp_b*100:.0f}%",
                "Options_Tax": tax_options_b,
                "Options_Rate": f"{rate_options_b*100:.0f}%"
            },
            "C_Bonus_Separate_Options_Merged": {
                "Description": "仅年终奖单独计税，期权并入综合所得",
                "Total_Tax": total_tax_c,
                "Comprehensive_Tax": tax_comp_c,
                "Comprehensive_Rate": f"{rate_comp_c*100:.0f}%",
                "Bonus_Tax": tax_bonus_c,
                "Bonus_Rate": f"{rate_bonus_c*100:.0f}%"
            },
            "D_Both_Merged": {
                "Description": "年终奖与期权均并入综合所得",
                "Total_Tax": total_tax_d,
                "Comprehensive_Tax": tax_comp_d,
                "Comprehensive_Rate": f"{rate_comp_d*100:.0f}%"
            }
        },
        "Optimized_Result": {
            "Best_Scenario": best_key,
            "Best_Scenario_Name": best["name"],
            "Best_Total_Tax": best["total_tax"],
            "Tax_Saved_Vs_Worst": max(total_tax_a, total_tax_b, total_tax_c, total_tax_d) - best["total_tax"],
            "Paid_Tax": total_prepaid,
            "Filing_Refund_Or_Pay": abs(settlement_amount),
            "Action": "应退税" if settlement_amount < 0 else "应补税"
        },
        "Deduction_Benefit": {
            "Deductions_Amount": args.deductions,
            "Deductions_Saved_Tax": deduction_saving,
            "Bracket_Drop": bracket_drop,
            "Rate_Before_Deductions": f"{rate_before*100:.0f}%" if rate_before > 0 else "N/A",
            "Rate_After_Deductions": f"{rate_after*100:.0f}%"
        },
        "Diagnostics": diagnostics
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
