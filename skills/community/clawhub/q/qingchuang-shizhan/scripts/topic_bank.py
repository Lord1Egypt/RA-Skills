# -*- coding: utf-8 -*-
"""
qingchuang-shizhan 自动化脚本：选题库 + 内容日历一键生成
用法：
  python topic_bank.py --positioning "帮中小企业主做IP操盘" --audience "中小企业主" --format 短视频
  python topic_bank.py --positioning "中医养生内容" --audience "30+女性" --count 50 --calendar
规则：5 类选题 × 每类 10 条 = 50 条；--calendar 额外输出 4 周排期（每周 3-5 更）。
"""
import argparse
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PAIN_HOOKS = ["没方向", "没流量", "不敢报价", "坚持不下去", "被割韭菜", "不知道发什么", "做了没反馈", "做不出差异化"]
OUTCOME_HOOKS = ["从0到1跑通变现", "做出第一个付费产品", "稳定涨粉", "收到第一笔钱", "跑通内容获客"]
PITFALL_HOOKS = ["定位贪大", "更新断更", "只学不做", "搬运洗稿", "变现太急", "乱追热点", "承诺收益", "现金流失衡"]

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memory")
LOG_FILE = os.path.join(LOG_DIR, "learning-log.md")
LOG_HEADER = """# 学习日志（自迭代用）

每次使用后把新经验记一行；每周复盘，把出现 2 次以上的经验固化到 SKILL.md 或词库。

| 日期 | 任务类型 | 经验/记录 |
|---|---|---|
"""


def log_learn(note):
    """把一条选题经验追加到学习日志（如哪类选题反馈好）。"""
    if not note:
        return
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(LOG_HEADER)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"| 今日 | 选题记录 | {note.replace('|', '／')} |\n")
    print(f"[学习] 已记录到学习日志：{LOG_FILE}")


def build(positioning, audience, fmt):
    p = positioning or "这个领域"
    a = audience or "目标人群"
    bank = []
    bank.append(("痛点共鸣", [
        f"给{a}的【{PAIN_HOOKS[0]}】：为什么你总觉得做{p}很难",
        f"不是你不会做{p}，是你一直在用错误的方式",
        f"{a}最怕的事：投入半年，{p}一点水花没有",
        f"做{p}最煎熬的阶段，不是没方法，是没人告诉你正常",
        f"如果你也是{a}，这条一定要看：{p}的真实门槛",
        f"为什么{p}做到一半就放弃的人，几乎都栽在这3件事上",
        f"{a}的{p}困境，根源不在能力，在判断",
        f"你的{p}做不起来，可能只是缺一个具体到能执行的口子",
        f"别急着学{p}的新玩法，先把这1个基本功补上",
        f"{p}做了3个月没结果？先回答自己这3个问题",
    ]))
    bank.append(("方法干货", [
        f"{p}第一步：锁定1个最小可卖的服务，先收第一笔钱",
        f"{p}从0到1的完整动作清单：本周只做这3件事",
        f"给{a}的{p}实操框架：内容→信任→咨询→付费",
        f"做{p}的50条选题怎么建？一条公式搞定",
        f"{p}怎么定节奏：宁可少而稳，不要多而断",
        f"把{p}的卖点讲清楚：一句话定位公式",
        f"{p}获客的3个渠道测试法：两周无反馈就砍",
        f"内容创业第一步：先定{fmt}主形式，再谈其他",
        f"{p}的交付标准化：怎么让流程可以被复制",
        f"每周30分钟的{p}复盘法：数据、动作、问题",
    ]))
    bank.append(("案例拆解", [
        f"拆解一个{a}的{p}案例：他是怎么{OUTCOME_HOOKS[0]}的",
        f"一个没背景的普通人做{p}，90天做了什么",
        f"{a}做{p}，最值钱的动作不是发内容，是这个",
        f"从0粉丝到第一单：{p}最小闭环复盘",
        f"案例：{a}靠{p}跑通{OUTCOME_HOOKS[3]}的完整路径",
        f"同样是{p}，为什么别人能{OUTCOME_HOOKS[2]}而你不行",
        f"一个{p}失败案例的3个教训：避坑比方法论重要",
        f"{a}做{p}的翻车经历：这5个坑他全踩了",
        f"案例拆解：{p}怎么把普通内容变成付费产品",
        f"从{OUTCOME_HOOKS[1]}到复购：{a}的{p}进阶路径",
    ]))
    bank.append(("避坑提醒", [
        f"做{p}最容易踩的坑：{PITFALL_HOOKS[0]}",
        f"{a}做{p}，第1个要避的坑是{PITFALL_HOOKS[1]}",
        f"做{p}别碰这3件事：{PITFALL_HOOKS[2]}、搬运、承诺收益",
        f"{p}变现太急的后果：为什么先跑通信任再说",
        f"{a}注意：做{p}前先留6个月生活费",
        f"做{p}被割韭菜的3个信号：及时止损",
        f"{p}的合规红线：不虚假宣传、不承诺收益",
        f"做{p}最隐蔽的坑：{PITFALL_HOOKS[6]}",
        f"{a}做{p}，别同时开3个以上项目",
        f"做{p}两周没反馈怎么办：砍掉，换渠道，别死磕",
    ]))
    bank.append(("观点态度", [
        f"别再把{p}当爱好，它是门生意",
        f"{p}真正值钱的不是方法，是你的判断",
        f"做{p}，先接受自己会很慢",
        f"{a}做{p}，最该戒掉的是完美主义",
        f"为什么{p}的尽头是私域",
        f"做{p}不需要天赋，需要的是被盯着把动作做完",
        f"{p}做得好的，都不是最聪明的人，是最能坚持的人",
        f"别被{p}的噪音带偏：只聚焦1个主增长引擎",
        f"{a}的{p}路线：先活下来，再谈规模",
        f"做{p}到100万，靠的是把交付标准化",
    ]))
    return bank


def render_bank(bank, count=50):
    out = []
    total = sum(len(items) for _, items in bank)
    out.append(f"===== 选题库（共 {total} 条，覆盖 5 类）=====\n")
    n = 0
    for cat, items in bank:
        out.append(f"【{cat}】")
        for it in items:
            n += 1
            if n > count:
                break
            out.append(f"{n}. {it}")
        out.append("")
    return "\n".join(out)


def render_calendar(bank):
    flat = [it for _, items in bank for it in items]
    weeks = [[flat[i * 3 + j] for j in range(3) if i * 3 + j < len(flat)] for i in range(4)]
    out = ["===== 内容日历（4 周，每周 3 更）=====\n"]
    for i, wk in enumerate(weeks, 1):
        out.append(f"第{i}周：")
        for j, t in enumerate(wk, 1):
            out.append(f"  周{['一', '三', '五'][j - 1]} {t}")
        out.append("")
    out.append("节奏原则：宁可少而稳，不要多而断；每周复盘数据，砍掉两周无反馈的动作。")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="qingchuang-shizhan 选题库自动化")
    ap.add_argument("--positioning", default="", help="一句话定位")
    ap.add_argument("--audience", default="", help="目标人群")
    ap.add_argument("--format", default="图文", help="内容形式：图文/短视频/音频")
    ap.add_argument("--count", type=int, default=50, help="选题数量（默认50）")
    ap.add_argument("--calendar", action="store_true", help="额外输出4周内容日历")
    ap.add_argument("--note", help="把一条选题经验追加到学习日志（如哪类选题反馈好）")
    args = ap.parse_args()
    bank = build(args.positioning, args.audience, args.format)
    print(render_bank(bank, args.count))
    if args.calendar:
        print(render_calendar(bank))
    log_learn(args.note)


if __name__ == "__main__":
    main()
