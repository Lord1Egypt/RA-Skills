#!/usr/bin/env python3
"""
半导体工程计算工具集
Semiconductor Engineering Calculator

支持: 本征载流子浓度、电阻率、阈值电压、耗尽层宽度、
      击穿电压、良率模型、迁移率等计算。
用法:
  python semiconductor_calc.py <command> [options]
  python semiconductor_calc.py list  # 列出所有可用命令
"""

import math
import argparse
import sys

# ============================================================
# 物理常数
# ============================================================
Q = 1.602176634e-19       # 电子电荷 (C)
K = 1.380649e-23           # 玻尔兹曼常数 (J/K)
EPS0 = 8.854187817e-14     # 真空介电常数 (F/cm)
T300 = 300.0               # 室温 (K)
kT_q_300 = K * T300 / Q    # 热电压 0.02585 V

# Si params
SI_EG0 = 1.17              # Si E_g(0K) eV
SI_ALPHA = 4.73e-4         # Varshni alpha
SI_BETA = 636              # Varshni beta
SI_EPS = 11.7              # Si relative permittivity
SI_NC = 2.8e19             # Si N_c 300K
SI_NV = 1.04e19            # Si N_v 300K

# SiO2 params
SIO2_EPS = 3.9             # SiO2 relative permittivity


def si_bandgap(T=T300):
    """计算硅的禁带宽度 (Varshni公式)"""
    return SI_EG0 - SI_ALPHA * T**2 / (T + SI_BETA)


def intrinsic_carrier(T=T300, material="Si"):
    """计算本征载流子浓度 n_i"""
    if material == "Si":
        eg = si_bandgap(T)
        nc = SI_NC * (T / T300) ** 1.5
        nv = SI_NV * (T / T300) ** 1.5
    elif material == "GaAs":
        eg = 1.52 - 5.41e-4 * T**2 / (T + 204)
        nc = 4.7e17 * (T / T300) ** 1.5
        nv = 7.0e18 * (T / T300) ** 1.5
    else:
        raise ValueError(f"Unsupported material: {material}")
    kt_q = K * T / Q
    ni = math.sqrt(nc * nv) * math.exp(-eg / (2 * kt_q))
    return ni


def resistivity(doping_type, concentration, material="Si", T=T300):
    """计算电阻率 ρ (Ω·cm)"""
    if material == "Si":
        if doping_type.lower() in ("n", "n-type"):
            # 硅电子迁移率模型 (Caughey-Thomas)
            mu_max, mu_min, nref, alpha = 1360, 92, 1.3e17, 0.91
        else:
            mu_max, mu_min, nref, alpha = 495, 48, 6.3e16, 0.76
        mu = mu_min + (mu_max - mu_min) / (1 + (concentration / nref) ** alpha)
    else:
        raise ValueError(f"Unsupported material: {material}")
    rho = 1.0 / (Q * concentration * mu)
    return rho, mu


def threshold_voltage(tox_nm, nsub, vfb=0.0, material="Si", T=T300):
    """计算MOSFET阈值电压 V_th (V)
    
    Args:
        tox_nm: 栅氧厚度 (nm)
        nsub: 衬底掺杂浓度 (cm^-3)
        vfb: 平带电压 (V)
        material: 衬底材料
        T: 温度 (K)
    """
    ni = intrinsic_carrier(T, material)
    eps_si = SI_EPS * EPS0
    eps_ox = SIO2_EPS * EPS0
    
    tox_cm = tox_nm * 1e-7
    cox = eps_ox / tox_cm
    
    phi_f = (K * T / Q) * math.log(nsub / ni)
    vth = vfb + 2 * phi_f + math.sqrt(2 * eps_si * Q * nsub * abs(2 * phi_f)) / cox
    return vth, cox, phi_f


def depletion_width(na, nd, va=0.0, material="Si", T=T300):
    """计算pn结耗尽层宽度 (μm)
    
    Args:
        na: p区掺杂浓度 (cm^-3)
        nd: n区掺杂浓度 (cm^-3)
        va: 外加偏压 (V)，正偏为正
    """
    ni = intrinsic_carrier(T, material)
    eps_si = SI_EPS * EPS0
    vbi = (K * T / Q) * math.log(na * nd / ni**2)
    w = math.sqrt(2 * eps_si * (vbi - va) * (1/na + 1/nd) / Q)
    return w * 1e4, vbi  # cm -> μm


def breakdown_voltage(nb, material="Si", junction_type="abrupt"):
    """估算pn结击穿电压 V_BD (V)
    
    Args:
        nb: 轻掺杂侧浓度 (cm^-3)
        material: 材料
        junction_type: "abrupt"(突变结) or "linear"(线性缓变结)
    """
    if material == "Si":
        if junction_type == "abrupt":
            vbd = 60.0 * (nb / 1e16) ** (-0.75)
        else:
            vbd = 60.0 * (nb / 1e16) ** (-0.5)
    elif material == "4H-SiC":
        vbd = 3000.0 * (nb / 1e16) ** (-0.75)
    elif material == "GaN":
        vbd = 2500.0 * (nb / 1e16) ** (-0.75)
    else:
        raise ValueError(f"Unsupported material: {material}")
    return vbd


def mos_capacitance(tox_nm, area_um2=1.0, material="SiO2"):
    """计算MOS电容值 (fF)
    
    Args:
        tox_nm: 氧化层厚度 (nm)
        area_um2: 面积 (μm²)
        material: 介电材料
    """
    eps_dict = {"SiO2": SIO2_EPS}
    eps_r = eps_dict.get(material, SIO2_EPS)
    tox_cm = tox_nm * 1e-7
    area_cm2 = area_um2 * 1e-8
    c = eps_r * EPS0 * area_cm2 / tox_cm
    return c * 1e15  # F -> fF


def yield_model(d0, area_cm2, model="negative_binomial", alpha=2.0):
    """良率模型计算
    
    Args:
        d0: 缺陷密度 (cm^-2)
        area_cm2: 芯片面积 (cm²)
        model: "poisson", "murphy", "seeds", "negative_binomial"
        alpha: 负二项模型的聚类因子
    """
    ad = d0 * area_cm2
    if model == "poisson":
        y = math.exp(-ad)
    elif model == "murphy":
        if ad < 1e-10:
            y = 1.0
        else:
            y = ((1 - math.exp(-ad)) / ad) ** 2
    elif model == "seeds":
        y = 1.0 / (1 + ad)
    elif model == "negative_binomial":
        y = (1 + ad / alpha) ** (-alpha)
    else:
        raise ValueError(f"Unknown model: {model}")
    return y * 100  # 百分比


def electromigration_mttf(j_a_cm2, T_C, material="Cu"):
    """电迁移MTTF估算 (小时)
    
    Args:
        j_a_cm2: 电流密度 (A/cm²)
        T_C: 温度 (°C)
        material: 金属材料
    """
    params = {"Cu": (1.1, 1.0), "Al": (0.6, 0.5)}
    ea, n = params.get(material, (1.1, 1.0))
    T_K = T_C + 273.15
    a = 1e7  # 比例常数 (归一化)
    mttf = a * j_a_cm2 ** (-n) * math.exp(ea * Q / (K * T_K))
    return mttf


def mobility(doping_type, concentration, T=T300, material="Si"):
    """计算载流子迁移率 (cm²/V·s)"""
    _, mu = resistivity(doping_type, concentration, material, T)
    return mu


def format_result(title, values, units):
    """格式化输出结果"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    for name, val in values.items():
        if isinstance(val, float):
            print(f"  {name:20s}: {val:.4e} {units.get(name, '')}")
        else:
            print(f"  {name:20s}: {val}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Semiconductor Engineering Calculator")
    subparsers = parser.add_subparsers(dest="command", help="Calculation type")

    # ni
    p_ni = subparsers.add_parser("ni", help="Intrinsic carrier concentration")
    p_ni.add_argument("--T", type=float, default=300, help="Temperature (K)")
    p_ni.add_argument("--material", default="Si", help="Material (Si/GaAs)")

    # resistivity
    p_res = subparsers.add_parser("resistivity", help="Resistivity calculation")
    p_res.add_argument("--type", required=True, choices=["n", "p"], help="Doping type")
    p_res.add_argument("--concentration", type=float, required=True, help="Doping conc (cm^-3)")
    p_res.add_argument("--material", default="Si", help="Material")
    p_res.add_argument("--T", type=float, default=300, help="Temperature (K)")

    # threshold voltage
    p_vth = subparsers.add_parser("vth", help="MOSFET threshold voltage")
    p_vth.add_argument("--tox", type=float, required=True, help="Gate oxide thickness (nm)")
    p_vth.add_argument("--nsub", type=float, required=True, help="Substrate doping (cm^-3)")
    p_vth.add_argument("--vfb", type=float, default=0.0, help="Flat-band voltage (V)")
    p_vth.add_argument("--T", type=float, default=300, help="Temperature (K)")

    # depletion width
    p_dep = subparsers.add_parser("depletion", help="Depletion width")
    p_dep.add_argument("--na", type=float, required=True, help="p-region doping (cm^-3)")
    p_dep.add_argument("--nd", type=float, required=True, help="n-region doping (cm^-3)")
    p_dep.add_argument("--va", type=float, default=0.0, help="Bias voltage (V)")

    # breakdown voltage
    p_bv = subparsers.add_parser("breakdown", help="Breakdown voltage estimation")
    p_bv.add_argument("--nb", type=float, required=True, help="Light-side doping (cm^-3)")
    p_bv.add_argument("--material", default="Si", help="Material (Si/4H-SiC/GaN)")
    p_bv.add_argument("--junction", default="abrupt", choices=["abrupt", "linear"])

    # MOS capacitance
    p_cc = subparsers.add_parser("cox", help="MOS capacitance calculation")
    p_cc.add_argument("--tox", type=float, required=True, help="Oxide thickness (nm)")
    p_cc.add_argument("--area", type=float, default=1.0, help="Area (um^2)")

    # yield
    p_yield = subparsers.add_parser("yield", help="Yield model")
    p_yield.add_argument("--d0", type=float, required=True, help="Defect density (cm^-2)")
    p_yield.add_argument("--area", type=float, required=True, help="Chip area (cm^2)")
    p_yield.add_argument("--model", default="negative_binomial",
                         choices=["poisson", "murphy", "seeds", "negative_binomial"])
    p_yield.add_argument("--alpha", type=float, default=2.0, help="Clustering factor")

    # mobility
    p_mob = subparsers.add_parser("mobility", help="Carrier mobility")
    p_mob.add_argument("--type", required=True, choices=["n", "p"], help="Carrier type")
    p_mob.add_argument("--concentration", type=float, required=True, help="Doping conc (cm^-3)")
    p_mob.add_argument("--T", type=float, default=300, help="Temperature (K)")

    # list
    subparsers.add_parser("list", help="List all commands")

    args = parser.parse_args()

    if args.command == "ni":
        ni = intrinsic_carrier(args.T, args.material)
        format_result("Intrinsic Carrier Concentration", {
            "Temperature": f"{args.T} K",
            "Material": args.material,
            "n_i": ni,
        }, {"n_i": "cm^-3"})

    elif args.command == "resistivity":
        rho, mu = resistivity(args.type, args.concentration, args.material, args.T)
        format_result("Resistivity Calculation", {
            "Doping type": f"{args.type}-type",
            "Concentration": args.concentration,
            "Mobility mu": mu,
            "Resistivity rho": rho,
        }, {"Concentration": "cm^-3", "Mobility mu": "cm^2/Vs", "Resistivity rho": "ohm-cm"})

    elif args.command == "vth":
        vth, cox, phi_f = threshold_voltage(args.tox, args.nsub, args.vfb, T=args.T)
        format_result("MOSFET Threshold Voltage", {
            "t_ox": f"{args.tox} nm",
            "N_sub": args.nsub,
            "V_FB": f"{args.vfb} V",
            "phi_F": phi_f,
            "C_ox": cox,
            "V_th": vth,
        }, {"N_sub": "cm^-3", "phi_F": "V", "C_ox": "F/cm^2", "V_th": "V"})

    elif args.command == "depletion":
        w, vbi = depletion_width(args.na, args.nd, args.va)
        format_result("Depletion Width", {
            "N_a (p-region)": args.na,
            "N_d (n-region)": args.nd,
            "Bias V_a": f"{args.va} V",
            "Built-in V_bi": vbi,
            "Width W": w,
        }, {"N_a (p-region)": "cm^-3", "N_d (n-region)": "cm^-3", "Built-in V_bi": "V", "Width W": "um"})

    elif args.command == "breakdown":
        vbd = breakdown_voltage(args.nb, args.material, args.junction)
        format_result("Breakdown Voltage", {
            "Material": args.material,
            "Junction": args.junction,
            "N_B (light side)": args.nb,
            "V_BD": vbd,
        }, {"N_B (light side)": "cm^-3", "V_BD": "V"})

    elif args.command == "cox":
        c = mos_capacitance(args.tox, args.area)
        format_result("MOS Capacitance", {
            "t_ox": f"{args.tox} nm",
            "Area": f"{args.area} um^2",
            "C_ox": c,
        }, {"C_ox": "fF"})

    elif args.command == "yield":
        y = yield_model(args.d0, args.area, args.model, args.alpha)
        format_result("Yield Model", {
            "Defect density D0": args.d0,
            "Chip area": f"{args.area} cm^2",
            "Model": args.model,
            "Yield Y": y,
        }, {"Defect density D0": "cm^-2", "Yield Y": "%"})

    elif args.command == "mobility":
        mu = mobility(args.type, args.concentration, args.T)
        format_result("Carrier Mobility", {
            "Type": args.type,
            "Concentration": args.concentration,
            "Temperature": f"{args.T} K",
            "Mobility mu": mu,
        }, {"Concentration": "cm^-3", "Mobility mu": "cm^2/Vs"})

    elif args.command == "list":
        print("""
Available commands:
  ni           - Intrinsic carrier concentration n_i
  resistivity  - Resistivity / mobility calculation
  vth          - MOSFET threshold voltage
  depletion    - pn junction depletion width
  breakdown    - Breakdown voltage estimation
  cox          - MOS capacitance calculation
  yield        - Yield model
  mobility     - Carrier mobility

Examples:
  python semiconductor_calc.py ni --T 400
  python semiconductor_calc.py resistivity --type n --concentration 1e17
  python semiconductor_calc.py vth --tox 2.5 --nsub 5e17
  python semiconductor_calc.py depletion --na 1e16 --nd 1e18 --va -2
  python semiconductor_calc.py breakdown --nb 1e15 --material 4H-SiC
  python semiconductor_calc.py cox --tox 2.0 --area 0.01
  python semiconductor_calc.py yield --d0 0.5 --area 1.0 --model negative_binomial
  python semiconductor_calc.py mobility --type n --concentration 1e17
""")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
