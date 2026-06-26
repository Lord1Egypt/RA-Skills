#!/usr/bin/env python3
"""
Kiểm tra đáp án đề thi bằng SymPy.
Hỗ trợ: Toán, Vật lý, Hóa học (các môn có tính toán).

Cài đặt:
    pip install sympy --break-system-packages

Cách dùng:
    python verify-answer.py --expr "solve(2*x + 5 - 11, x)"
    python verify-answer.py --equation "2*x + 5 = 11" --var x
    python verify-answer.py --calc "sqrt(3**2 + 4**2)"
    python verify-answer.py --chem "2*H2 + O2 -> 2*H2O" (cân bằng PTHH)
    python verify-answer.py --physics "F = 10 * 5" (F=ma)
"""

import sys
import argparse
import json

def check_deps():
    try:
        import sympy
    except ImportError:
        print("Cần cài: pip install sympy --break-system-packages")
        sys.exit(1)

def solve_equation(equation_str, var_name="x"):
    """Giải phương trình và trả về đáp án chính xác"""
    from sympy import symbols, solve, Eq, sympify, simplify
    from sympy.parsing.sympy_parser import parse_expr
    var = symbols(var_name)
    if "=" in equation_str:
        left, right = equation_str.split("=", 1)
        eq = Eq(parse_expr(left.strip()), parse_expr(right.strip()))
    else:
        eq = parse_expr(equation_str)
    result = solve(eq, var)
    return {"equation": equation_str, "variable": var_name, "solutions": [str(r) for r in result]}

def calc_expression(expr_str):
    """Tính biểu thức cho kết quả chính xác"""
    from sympy import sympify, simplify, nsimplify, Rational
    from sympy.parsing.sympy_parser import parse_expr
    expr = parse_expr(expr_str)
    exact = simplify(expr)
    numeric = float(exact.evalf())
    return {"expression": expr_str, "exact": str(exact), "numeric": round(numeric, 6)}

def verify_quadratic(a, b, c):
    """Giải và verify phương trình bậc 2: ax² + bx + c = 0"""
    from sympy import symbols, solve, Rational, sqrt
    x = symbols("x")
    eq = a*x**2 + b*x + c
    delta = b**2 - 4*a*c
    roots = solve(eq, x)
    return {
        "equation": f"{a}x² + {b}x + {c} = 0",
        "delta": str(delta),
        "roots": [str(r) for r in roots],
        "num_roots": len(roots)
    }

def verify_geometry(shape, **params):
    """Tính toán hình học: diện tích, chu vi, thể tích"""
    from sympy import Rational, sqrt, pi, simplify
    results = {}
    if shape == "triangle":
        a = params.get("a", 0)
        b = params.get("b", 0)
        c = params.get("c", 0)
        h = params.get("h", 0)
        base = params.get("base", a)
        if base and h:
            area = Rational(1,2) * base * h
            results["area"] = str(simplify(area))
        if a and b and c:
            s = Rational(1,2) * (a + b + c)
            area_heron = sqrt(s*(s-a)*(s-b)*(s-c))
            results["area_heron"] = str(simplify(area_heron))
            results["perimeter"] = str(a + b + c)
    elif shape == "circle":
        r = params.get("r", 0)
        results["area"] = str(simplify(pi * r**2))
        results["circumference"] = str(simplify(2 * pi * r))
    elif shape == "rectangle":
        a = params.get("a", 0)
        b = params.get("b", 0)
        results["area"] = str(simplify(a * b))
        results["perimeter"] = str(simplify(2*(a+b)))
        results["diagonal"] = str(simplify(sqrt(a**2 + b**2)))
    return {"shape": shape, "params": {k:str(v) for k,v in params.items()}, "results": results}

def verify_physics(formula, values):
    """Tính toán Vật lý"""
    from sympy import symbols, solve, Eq
    from sympy.parsing.sympy_parser import parse_expr
    result = parse_expr(formula)
    for var, val in values.items():
        result = result.subs(symbols(var), val)
    return {"formula": formula, "values": values, "result": str(result), "numeric": float(result.evalf())}

def balance_chemical(equation_str):
    """Cân bằng phương trình hóa học — SGK THCS + THPT"""
    common = {
        # SGK Hóa 8-9
        "H2+O2->H2O": "2H2 + O2 -> 2H2O",
        "Fe+O2->Fe3O4": "3Fe + 2O2 -> Fe3O4",
        "Fe+O2->Fe2O3": "4Fe + 3O2 -> 2Fe2O3",
        "Fe+HCl->FeCl2+H2": "Fe + 2HCl -> FeCl2 + H2",
        "Fe+H2SO4->FeSO4+H2": "Fe + H2SO4 -> FeSO4 + H2",
        "NaOH+HCl->NaCl+H2O": "NaOH + HCl -> NaCl + H2O",
        "CaCO3->CaO+CO2": "CaCO3 -> CaO + CO2",
        "Al+O2->Al2O3": "4Al + 3O2 -> 2Al2O3",
        "Zn+HCl->ZnCl2+H2": "Zn + 2HCl -> ZnCl2 + H2",
        "Na+H2O->NaOH+H2": "2Na + 2H2O -> 2NaOH + H2",
        "Mg+O2->MgO": "2Mg + O2 -> 2MgO",
        "Mg+HCl->MgCl2+H2": "Mg + 2HCl -> MgCl2 + H2",
        "Cu+AgNO3->Cu(NO3)2+Ag": "Cu + 2AgNO3 -> Cu(NO3)2 + 2Ag",
        "BaCl2+Na2SO4->BaSO4+NaCl": "BaCl2 + Na2SO4 -> BaSO4 + 2NaCl",
        "P+O2->P2O5": "4P + 5O2 -> 2P2O5",
        "KMnO4->K2MnO4+MnO2+O2": "2KMnO4 -> K2MnO4 + MnO2 + O2",
        "KClO3->KCl+O2": "2KClO3 -> 2KCl + 3O2",
        "CO2+NaOH->Na2CO3+H2O": "CO2 + 2NaOH -> Na2CO3 + H2O",
        "CO2+Ca(OH)2->CaCO3+H2O": "CO2 + Ca(OH)2 -> CaCO3 + H2O",
        # SGK Hóa 10-12
        "N2+H2->NH3": "N2 + 3H2 -> 2NH3",
        "NH3+O2->NO+H2O": "4NH3 + 5O2 -> 4NO + 6H2O",
        "SO2+O2->SO3": "2SO2 + O2 -> 2SO3",
        "FeS2+O2->Fe2O3+SO2": "4FeS2 + 11O2 -> 2Fe2O3 + 8SO2",
        "C2H5OH+O2->CO2+H2O": "C2H5OH + 3O2 -> 2CO2 + 3H2O",
        "CH4+O2->CO2+H2O": "CH4 + 2O2 -> CO2 + 2H2O",
        "C2H4+O2->CO2+H2O": "C2H4 + 3O2 -> 2CO2 + 2H2O",
        "C6H12O6->C2H5OH+CO2": "C6H12O6 -> 2C2H5OH + 2CO2",
        "Fe2O3+HCl->FeCl3+H2O": "Fe2O3 + 6HCl -> 2FeCl3 + 3H2O",
        "Fe2O3+H2SO4->Fe2(SO4)3+H2O": "Fe2O3 + 3H2SO4 -> Fe2(SO4)3 + 3H2O",
        "Al+NaOH+H2O->NaAlO2+H2": "2Al + 2NaOH + 2H2O -> 2NaAlO2 + 3H2",
        "Cu+HNO3->Cu(NO3)2+NO+H2O": "3Cu + 8HNO3 -> 3Cu(NO3)2 + 2NO + 4H2O",
    }
    key = equation_str.replace(" ", "")
    if key in common:
        return {"input": equation_str, "balanced": common[key], "method": "lookup"}
    return {"input": equation_str, "balanced": None, "method": "not_found",
            "note": "PTHH nay chua co trong lookup table. Dung web search de verify."}

def calc_mol(formula_type, **kwargs):
    """Tính toán mol, nồng độ, thể tích (Hóa học)"""
    from sympy import Rational
    results = {}
    if formula_type == "mol_mass":
        m = kwargs.get("m", 0)
        M = kwargs.get("M", 0)
        if m and M:
            results["n"] = str(Rational(m, M)) + " mol"
            results["numeric"] = round(m / M, 4)
    elif formula_type == "concentration":
        n = kwargs.get("n", 0)
        V = kwargs.get("V", 0)
        if n and V:
            results["CM"] = str(Rational(n * 1000, int(V * 1000))) + " mol/L"
            results["numeric"] = round(n / V, 4)
    elif formula_type == "gas_volume":
        n = kwargs.get("n", 0)
        results["V_dktc"] = str(n * 22.4) + " L"
    return {"type": formula_type, "params": kwargs, "results": results}

def main():
    ap = argparse.ArgumentParser(description="Verify dap an de thi bang SymPy")
    ap.add_argument("--equation", help="Giai phuong trinh (VD: '2*x+5=11')")
    ap.add_argument("--var", default="x", help="Bien (mac dinh: x)")
    ap.add_argument("--calc", help="Tinh bieu thuc (VD: 'sqrt(3**2+4**2)')")
    ap.add_argument("--quadratic", nargs=3, type=float, metavar=("A","B","C"),
                    help="Giai PT bac 2: ax^2+bx+c=0")
    ap.add_argument("--geometry", help="Hinh hoc: triangle/circle/rectangle")
    ap.add_argument("--params", help="Tham so hinh hoc (JSON)")
    ap.add_argument("--chem", help="Can bang PTHH")
    ap.add_argument("--json", action="store_true", help="Xuat JSON")
    args = ap.parse_args()

    check_deps()
    result = None

    if args.equation:
        result = solve_equation(args.equation, args.var)
    elif args.calc:
        result = calc_expression(args.calc)
    elif args.quadratic:
        a, b, c = args.quadratic
        result = verify_quadratic(a, b, c)
    elif args.geometry:
        params = json.loads(args.params) if args.params else {}
        result = verify_geometry(args.geometry, **{k:float(v) for k,v in params.items()})
    elif args.chem:
        result = balance_chemical(args.chem)
    else:
        ap.print_help()
        return

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print("  KET QUA VERIFY")
        print("=" * 50)
        for k, v in result.items():
            print(f"  {k}: {v}")
        print("=" * 50)

if __name__ == "__main__":
    main()
