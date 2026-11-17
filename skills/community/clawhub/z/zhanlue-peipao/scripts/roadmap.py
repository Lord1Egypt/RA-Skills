# -*- coding: utf-8 -*-
"""
zhanlue-peipao 自动化脚本：战略路线图一键生成（现状卡 + 定档判定 + 目标拆解 + 90天里程碑）
用法：
  python roadmap.py --income 50000 --hours 10 --target 100 --months 12
规则：按 references/sanji-luxian.md 的三档数据生成；收入均为目标量级参考，不承诺结果。
"""
import argparse
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TIERS = {
    10: {
        "名称": "10万档（生存起步）",
        "定位": "跑通「一个产品 × 一个渠道 × 一个收入闭环」",
        "月均": 8300, "日均": 280,
        "拆法": "年10万 = 月均8300 = 日均约280元；成交公式：客单价 × 成交数 = 日收入（例：客单280 × 日1单，或客单28 × 日10单）",
        "动作": [
            "选定1个细分人群 + 1个真实需求（禁止空泛定位）",
            "做出1个最小可卖产品/服务（能收第一笔钱即可）",
            "每天固定做增量动作：发内容 / 获客 / 跟进成交",
            "每周复盘数据，砍掉两周无反馈的动作",
            "跑通「内容→信任→咨询→付费」链路",
        ],
        "里程碑90": ["首笔收入产生", "连续30天有出单记录", "明确1个有效获客渠道"],
        "坑": ["定位贪大（'做自媒体'不叫定位）", "同时做3个以上项目精力分散", "只学不做、以收藏教程代替执行"],
        "升档": "单一渠道月稳定出单且产能饱和；交付占用时间超60%；复购/转介绍占比上升",
    },
    100: {
        "名称": "100万档（稳定规模化）",
        "定位": "把个人能力变成可复制的系统：标准化、团队化、多渠道、私域复购",
        "月均": 83000, "日均": 2700,
        "拆法": "年100万 = 月均8.3万 = 日均约2700元；拆法：产品数 × 客单价 × 客户数，或渠道数 × 单渠道产出（例：3渠道 × 月3万/渠道）",
        "动作": [
            "把主产品标准化：SOP、定价体系、交付流程（让别人能接手）",
            "组建2-5人小团队：内容/销售/交付分工",
            "扩到2-3个获客渠道（主渠道深做 + 新渠道试跑）",
            "建私域与复购体系：客户分层、会员/订阅/长尾产品",
            "建立简单财务制度：收支表、成本核算、利润优先",
        ],
        "里程碑90": ["主产品SOP完成并跑通1个代执行流程", "第二渠道开始出单", "团队分工文档化"],
        "坑": ["老板继续干一线全部活", "盲目扩品类稀释主业务", "只看销售额不看净利润与现金流"],
        "升档": "团队化运营稳定、创始人脱离一线仍能运转；渠道与产品矩阵成型；需要组织制度财务资本升级",
    },
    1000: {
        "名称": "1000万档（组织化平台化）",
        "定位": "靠系统、组织和资产赚钱：制度、品牌、渠道网络、多业务线、财务合规体系",
        "月均": 830000, "日均": 27000,
        "拆法": "年1000万 = 月均83万 = 日均约2.7万；拆法：多业务线 × 单线产出，或直营 × 加盟/渠道网络 × 单网点产出",
        "动作": [
            "建设制度：流程、授权、考核、分钱机制",
            "打造可复制的扩张模式：加盟/代理/渠道网络/产品线复制",
            "品牌化：市场定位、内容资产、私域品牌沉淀",
            "财务与合规体系：核算、税务、法务、内控",
            "数据驱动：建数据看板，用数据决策砍线/加码",
        ],
        "里程碑90": ["确定1个可复制扩张模式并试点跑通", "制度文档化（岗位、流程、考核）", "现金流警戒线明确（<3个月运营即触发）"],
        "坑": ["盘子铺太大现金流断裂", "创始人成为唯一瓶颈", "财务混乱、税务风险累积"],
        "升档": "组织稳定后考虑平台化/资本化/行业整合；1000万档之后超出本技能范围，建议专业咨询",
    },
}


LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memory")
LOG_FILE = os.path.join(LOG_DIR, "learning-log.md")
LOG_HEADER = """# 学习日志（自迭代用）

每次使用后把新经验记一行；每周复盘，把出现 2 次以上的经验固化到 SKILL.md 或词库。

| 日期 | 任务类型 | 经验/记录 |
|---|---|---|
"""


def log_learn(note):
    """把一条战略经验追加到学习日志（如里程碑完成情况、跳档教训）。"""
    if not note:
        return
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(LOG_HEADER)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"| 今日 | 战略记录 | {note.replace('|', '／')} |\n")
    print(f"[学习] 已记录到学习日志：{LOG_FILE}")


def current_tier(income):
    if income < 100000:
        return 0, "起步期（未达10万档）"
    if income < 1000000:
        return 1, "当前处于10万档区间"
    if income < 10000000:
        return 2, "当前处于100万档区间"
    return 3, "当前处于1000万档区间"


def main():
    ap = argparse.ArgumentParser(description="zhanlue-peipao 战略路线图自动化")
    ap.add_argument("--income", type=float, required=True, help="当前年收入（元）")
    ap.add_argument("--hours", type=float, required=True, help="每周可投入小时数")
    ap.add_argument("--target", type=int, choices=[10, 100, 1000], required=True, help="目标档位（万元）")
    ap.add_argument("--months", type=int, default=12, help="目标时限（月，默认12）")
    ap.add_argument("--note", help="把一条战略经验追加到学习日志（如里程碑完成情况）")
    args = ap.parse_args()

    t = TIERS[args.target]
    cur_idx, cur_desc = current_tier(args.income)
    tgt_idx = {10: 1, 100: 2, 1000: 3}[args.target]

    out = []
    out.append("===== 战略路线图（自动生成）=====\n")
    out.append("## 现状卡")
    out.append(f"- 起点：当前年收入约 {args.income:,.0f} 元")
    out.append(f"- 资源：每周可投入约 {args.hours:g} 小时")
    out.append(f"- 目标档位：{args.target} 万元档，时限 {args.months} 个月")
    out.append(f"- 判定：{cur_desc}")
    if tgt_idx - cur_idx > 1:
        out.append("- 警告：目标档位与现状相差超过 1 档（跳档越级是主要失败原因）。建议先定中间档，跑通再升档。")
    out.append("")
    out.append(f"## 目标拆解（{t['名称']}）")
    out.append(f"- 定位：{t['定位']}")
    out.append(f"- 收入拆解：{t['拆法']}")
    if args.hours > 0:
        daily_need = t["日均"] / max(args.hours / 7, 1)
        out.append(f"- 按每周 {args.hours:g} 小时折算：每小时需创造约 {daily_need:,.0f} 元收入（量级参考）")
    out.append("")
    out.append("## 核心动作（按优先级）")
    for i, a in enumerate(t["动作"], 1):
        out.append(f"{i}. {a}")
    out.append("")
    out.append("## 90 天里程碑（可验证）")
    for m in t["里程碑90"]:
        out.append(f"- {m}")
    out.append("")
    out.append("## 每周执行清单（陪跑节奏）")
    out.append("- 本周 3 件事：1 件最重要增长动作 + 1 件现金流动作 + 1 件能力积累动作")
    out.append("- 看 2 个数据指标：触达量、成交数/客单价（100万档以上看毛利/复购）")
    out.append("- 复盘 1 个问题：本周哪个动作有反馈、哪个该砍")
    out.append("")
    out.append("## 常见坑（先避）")
    for p in t["坑"]:
        out.append(f"- {p}")
    out.append("")
    out.append(f"## 升档信号（进入下一档筹备）")
    out.append(f"- {t['升档']}")
    out.append("")
    out.append("提示：所有收入均为目标设定与量级参考，不承诺结果；先保现金流（留6个月生活费），"
               "账上现金低于3个月运营即触发警戒。")
    print("\n".join(out))
    log_learn(args.note)


if __name__ == "__main__":
    main()
