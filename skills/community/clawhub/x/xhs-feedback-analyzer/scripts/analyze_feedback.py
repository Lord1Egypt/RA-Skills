#!/usr/bin/env python3
"""
小红书跑腿舆情分析脚本 v2
输出：结构清晰的 Markdown 报告（结论先行 + 金字塔结构）
"""
import json, sys, os, argparse
from collections import Counter
from datetime import datetime

# 情感分类关键词
NEG_WORDS = ['投诉','骗','差','慢','超时','取消','丢失','损坏','不满','差评','垃圾','坑','黑','欺骗',
             '强制','退款','赔偿','客服不','无法联系','等了','迟到','没来','扣费','乱扣','有病','有问题']
POS_WORDS = ['好评','满意','棒','赞','推荐','感谢','帮我','快速','准时','专业','贴心','放心','惊喜',
             '好用','方便','省心','救场','解决了']

SERVICE_KEYWORDS = {
    '帮办/跑腿': ['跑腿','代办','帮办','急送','一对一'],
    '帮买/代购': ['帮买','代购','代买','代下单','帮你买'],
    '帮送/配送': ['帮送','配送','快送','即时','超市','众包','骑手'],
}

FEEDBACK_KEYWORDS = {
    '配送速度/超时': ['超时','慢','等','迟到','半小时','一小时','快速','准时'],
    '骑手服务态度': ['骑手','小哥','态度','服务','礼貌'],
    '客服/投诉处理': ['客服','投诉','反馈','申诉','处理','赔'],
    '价格/费用问题': ['价格','费用','收费','贵','便宜','优惠','跑腿费','运费'],
    '丢失/损坏': ['丢','损','破','坏','没收到','丢失'],
    'App体验/功能': ['app','软件','功能','界面','下单','入口','操作'],
    '好评/正面体验': ['感谢','救场','帮我','方便','放心','好评'],
    '使用攻略/教程': ['教程','攻略','怎么用','步骤','流程','如何'],
    '比较/测评': ['对比','测评','推荐','哪个好','比较'],
    '其他/通用分享': [],
}

def classify_sentiment(title, body):
    text = (title or '') + ' ' + (body or '')
    neg = sum(1 for w in NEG_WORDS if w in text)
    pos = sum(1 for w in POS_WORDS if w in text)
    # 正面信号：攻略/分享/体验类，即使提到负面词也以整体情绪为准
    ATT_WORDS = ['攻略','分享','体验','新手','教程','邀请','入门','探索','感受','有趣','圆满','流程','步骤']
    att = sum(1 for w in ATT_WORDS if w in text)
    # 攻略/体验分享帖：att>=3 时强制正面（即使有少量负面词）
    if att >= 3: return '正面'
    if att >= 2 and neg <= 1: return '正面'
    if neg >= 2 or (neg >= 1 and pos == 0 and att == 0): return '负面'
    if pos >= 2 or att >= 1: return '正面'   # 正面：需命中2个及以上正面关键词（或1个攻略词）
    if pos == 1 and neg == 0: return '中立'  # 只有1个正面词，降为中立
    return '中立'

def classify_service(title, body):
    text = (title or '') + ' ' + (body or '')
    for stype, kws in SERVICE_KEYWORDS.items():
        if any(w in text for w in kws):
            return stype
    return '帮办/跑腿'

def classify_feedback(title, body):
    text = (title or '') + ' ' + (body or '')
    matched = []
    for ftype, kws in FEEDBACK_KEYWORDS.items():
        if kws and any(w in text for w in kws):
            matched.append(ftype)
    return matched or ['其他/通用分享']

EMOJI = {'正面': '😊', '中立': '😐', '负面': '😞'}


# 官方账号标识（排除）
OFFICIAL_ACCOUNTS = ['美团跑腿']  # 官方账号在帖子 tag 中会有 #美团跑腿 作为唯一 tag，同时 likes 极低
OFFICIAL_TITLE_SIGNALS = ['用户故事✨', '官方征集', '优秀投稿']  # 官方帖常见标题前缀

def is_official_account(note):
    """判断是否为官方账号发帖（过滤掉）"""
    title = note.get('title', '') or ''
    body = note.get('body', '') or ''
    # 官方帖特征：标题含官方信号词 + body 含"征集"/"入选"/"专属惊喜"等运营词
    official_signals = ['征集活动', '优秀投稿', '入选', '专属惊喜', '官方', '我们发起']
    title_match = any(s in title for s in OFFICIAL_TITLE_SIGNALS)
    body_match = sum(1 for s in official_signals if s in body)
    return title_match or body_match >= 2

def generate_report(data):
    raw_notes = data.get('notes', [])
    trending = data.get('trending', [])
    target_dates = data.get('target_dates', [])
    keyword_list = data.get('keyword_list', [])
    run_date = datetime.now().strftime('%Y-%m-%d')

    # 过滤官方账号帖子
    official_filtered = [n for n in raw_notes if is_official_account(n)]
    notes = [n for n in raw_notes if not is_official_account(n)]

    # 分类
    for n in notes:
        n['sentiment'] = classify_sentiment(n.get('title',''), n.get('body',''))
        n['service'] = classify_service(n.get('title',''), n.get('body',''))
        n['feedback'] = classify_feedback(n.get('title',''), n.get('body',''))

    total = len(notes)
    if total == 0:
        return "（本期无有效帖子）"

    sent_counts = Counter(n['sentiment'] for n in notes)
    service_counts = Counter(n['service'] for n in notes)
    feedback_counts = Counter(fb for n in notes for fb in n['feedback'])

    neg_pct = round(sent_counts['负面'] / total * 100)
    pos_pct = round(sent_counts['正面'] / total * 100)
    neu_pct = 100 - neg_pct - pos_pct
    top_issues = [k for k, _ in feedback_counts.most_common(3)]
    top_service = service_counts.most_common(1)[0][0] if service_counts else '—'

    # 日期范围
    dates_sorted = sorted(target_dates, reverse=True)
    date_range = f"{dates_sorted[-1]} ~ {dates_sorted[0]}" if len(dates_sorted) > 1 else dates_sorted[0]

    # 负面帖（精选）
    neg_notes = [n for n in notes if n['sentiment'] == '负面'][:3]
    pos_notes = [n for n in notes if n['sentiment'] == '正面'][:2]

    # 主要结论
    if neg_pct >= 30:
        main_conclusion = f"本期负面声音偏多（{neg_pct}%），重点集中在 **{'** 和 **'.join(top_issues[:2])}**，需关注。"
    elif pos_pct >= 30:
        main_conclusion = f"本期口碑整体向好（正面 {pos_pct}%），主要场景 **{top_service}** 获得较多认可。"
    else:
        main_conclusion = f"本期口碑以中立为主（{neu_pct}%），负面占 {neg_pct}%，主要集中在 **{'** 和 **'.join(top_issues[:2])}**。"

    # 开始构建报告
    kw_str = ' / '.join(f'`{k}`' for k in keyword_list) if keyword_list else '—'
    official_note = f"（已过滤官方账号帖子 {len(official_filtered)} 篇）" if official_filtered else ""
    md = f"""## 小红书跑腿舆情监控 · {run_date}

> 📅 {date_range} &nbsp;|&nbsp; 📊 有效帖子 **{total}** 篇 {official_note}&nbsp;|&nbsp; 🔍 关键词：{kw_str}

---

### 核心结论

> {main_conclusion}

---

### 一、舆情概览

| 维度 | 数值 |
|------|------|
| 有效帖子 | {total} 篇 |
| 😊 正面 | {sent_counts['正面']} 篇（{pos_pct}%） |
| 😐 中立 | {sent_counts['中立']} 篇（{neu_pct}%） |
| 😞 负面 | {sent_counts['负面']} 篇（{neg_pct}%） |

**服务场景分布**

| 场景 | 帖子数 | 占比 |
|------|--------|------|
"""
    for stype, cnt in service_counts.most_common():
        pct = round(cnt/total*100)
        md += f"| {stype} | {cnt} | {pct}% |\n"

    md += "\n---\n\n### 二、主要负面问题\n\n"
    if neg_notes:
        for i, n in enumerate(neg_notes, 1):
            short_body = (n.get('body','') or '')[:120].replace('\n',' ').strip()
            if short_body: short_body = f'> "{short_body}…"'
            md += f"**{i}. {n.get('title','（无标题）')}**  \n"
            md += f"日期：{n.get('date','')} | 反馈类型：{'、'.join(n['feedback'])}  \n"
            if short_body: md += f"{short_body}  \n"
            md += f"🔗 [查看原帖]({n.get('url','')})  \n\n"
    else:
        md += "_本期无负面帖子_\n\n"

    md += "---\n\n### 三、正面案例\n\n"
    if pos_notes:
        for n in pos_notes:
            short_body = (n.get('body','') or '')[:120].replace('\n',' ').strip()
            if short_body: short_body = f'> "{short_body}…"'
            md += f"**{n.get('title','（无标题）')}**  \n"
            md += f"日期：{n.get('date','')}  \n"
            if short_body: md += f"{short_body}  \n"
            md += f"🔗 [查看原帖]({n.get('url','')})  \n\n"
    else:
        md += "_本期无正面帖子_\n\n"

    # 大家都在搜
    if trending:
        md += "---\n\n### 四、「大家都在搜」用户认知热词\n\n"
        md += "| # | 热词 |\n|---|------|\n"
        for i, word in enumerate(trending, 1):
            md += f"| {i} | {word} |\n"
        md += "\n> 💡 **洞察**：用户对基础使用的困惑（如何下单/入口在哪）高于对服务本身的投诉，产品引导链路有优化空间。\n\n"
        section_num = 5
    else:
        section_num = 4

    # 全部帖子明细
    md += f"---\n\n### {section_num}、全部帖子明细\n\n"
    md += "| 日期 | 标题 | 情感 | 反馈类型 | 链接 |\n"
    md += "|------|------|------|----------|------|\n"
    for n in sorted(notes, key=lambda x: x.get('date',''), reverse=True):
        title = (n.get('title','') or '（无标题）')[:25]
        emoji = EMOJI.get(n['sentiment'], '')
        fb = '、'.join(n['feedback'])[:15]
        url = n.get('url','')
        date = (n.get('date','') or '')[-5:]  # MM-DD
        md += f"| {date} | {title} | {emoji} {n['sentiment']} | {fb} | [→]({url}) |\n"

    md += "\n---\n\n"
    return md

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file')
    parser.add_argument('--out', default='./output')
    args = parser.parse_args()

    with open(args.json_file, encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(args.out, exist_ok=True)
    run_date = datetime.now().strftime('%Y-%m-%d')
    report = generate_report(data)

    # 输出到文件
    out_path = os.path.join(args.out, f"report_{run_date}.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ 报告已生成: {out_path}")
    print(f"   共分析 {len(data.get('notes',[]))} 篇帖子")
    print("\n" + "="*60)
    print(report[:800])

if __name__ == '__main__':
    main()
