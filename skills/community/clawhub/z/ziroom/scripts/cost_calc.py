#!/usr/bin/env python3
"""长租公寓真实月成本计算器（零依赖，纯本地计算）。

把"标价月租"换算成含服务费、电费差的真实月成本，并与普租对比。

用法:
    python3 cost_calc.py <月租金> [选项]
选项:
    --service-rate 10    服务费占年租金百分比(默认10)
    --net 0              网费等固定月费(默认0)
    --elec-kwh 150       月用电度数(默认150,用于商电民电差)
    --commercial         房源是商电(约1.5元/度 vs 民电约0.55)
    --compare 普租月租   与普租对比(普租按月租+中介费年摊)

示例:
    python3 cost_calc.py 5000 --service-rate 10 --commercial --compare 4300
"""
import sys

CIVIL_KWH = 0.55   # 民电参考单价(元/度,各地有浮动)
COMM_KWH = 1.50    # 商电参考单价


def parse(argv):
    if not argv:
        print(__doc__)
        sys.exit(1)
    cfg = {"rent": float(argv[0]), "service_rate": 10.0, "net": 0.0,
           "kwh": 150.0, "commercial": False, "compare": None}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--service-rate":
            cfg["service_rate"] = float(argv[i + 1]); i += 2
        elif a == "--net":
            cfg["net"] = float(argv[i + 1]); i += 2
        elif a == "--elec-kwh":
            cfg["kwh"] = float(argv[i + 1]); i += 2
        elif a == "--commercial":
            cfg["commercial"] = True; i += 1
        elif a == "--compare":
            cfg["compare"] = float(argv[i + 1]); i += 2
        else:
            print(f"未知参数: {a}", file=sys.stderr); sys.exit(2)
    return cfg


def main():
    c = parse(sys.argv[1:])
    service = c["rent"] * 12 * c["service_rate"] / 100 / 12
    elec_extra = c["kwh"] * (COMM_KWH - CIVIL_KWH) if c["commercial"] else 0
    total = c["rent"] + service + c["net"] + elec_extra
    print(f"标价月租:       {c['rent']:.0f} 元")
    print(f"服务费月摊({c['service_rate']:g}%): {service:.0f} 元")
    if c["net"]:
        print(f"网费等固定费:   {c['net']:.0f} 元")
    if c["commercial"]:
        print(f"商电差价(约):   {elec_extra:.0f} 元 ({c['kwh']:g}度 × {COMM_KWH - CIVIL_KWH:.2f})")
    print(f"—— 真实月成本:  {total:.0f} 元 (比标价高 {(total/c['rent']-1)*100:.1f}%)")
    if c["compare"]:
        # 普租常见中介费=1个月租金,按12月分摊
        pu = c["compare"] * 13 / 12
        print(f"普租对比: 月租 {c['compare']:.0f} + 中介费年摊 = {pu:.0f} 元/月")
        diff = total - pu
        print(f"→ 长租公寓每月多花 {diff:+.0f} 元，一年 {diff*12:+.0f} 元"
              f"（买的是装修/维修/不随意涨租，值不值自己定）")
    print("注: 电价单价与服务费率各城市有差异，签约前以合同为准")


if __name__ == "__main__":
    main()
