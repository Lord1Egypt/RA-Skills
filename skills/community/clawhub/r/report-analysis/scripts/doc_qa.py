# -*- coding: utf-8 -*-
"""政策文档分析（模式F）与检索问答（模式G）。

用法:
    python doc_qa.py docs                          # 列出可用文档
    python doc_qa.py summary 分级施策              # 模式F：总结指定文档，说明政策规则
    python doc_qa.py ask 月度激励怎么算            # 模式G：跨文档检索问答，标注来源与版本
    python doc_qa.py ask 门槛未完成怎么处罚        # 模式G：涉及 Excel 指标时自动联动实测数据

数据源:
    policy_docs.json  由 doc_index.py 生成的文档索引
    term_map.json     Excel 术语 -> 文档关键词映射
    analyzer.py       Excel 实测数据（政策<->数据联动）
"""
import os
import re
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(HERE, 'policy_docs.json')
TM = os.path.join(HERE, 'term_map.json')

# 只保留多字停用词；单字停用词会拆坏双字词（如 么 会拆散 怎么），靠 len>=2 过滤即可
STOP = set('什么 怎么 如何 可以 应该 请问 一下 规定 要求 政策 规则 有哪些 多少 为什么 怎么办 怎样 一个 这个 那个 我们 你们 他们 不是 就是 也是 还是 还是说 相关 有关 关于 具体 详细 了解 介绍 说明 知道 看看 哪些 那个 这个 时候 情况 问题 内容 方面 部分 里面 上面 下面 的话 之后 之前 以及 或者 并且 但是 因为 所以 如果 虽然 需要 进行 提供 包括 根据 按照 依照 对于 对于 针对 通过 按照 加上 就是'.split())

RULES = re.compile(r'(必须|应当|应|不得|禁止|严禁|需要|可以|扣|罚|奖|激励|返还|折算|系数|门槛|否决|档|投诉|合约|融合|签约|退出|清退|解除|星级|评定|报备|审批|备案|公示|考核|评估|办法|标准|公式|上限|占比|比例|%|折|/|＋|\+)')


def load_docs():
    with open(IDX, encoding='utf-8') as f:
        return json.load(f)


def load_terms():
    with open(TM, encoding='utf-8') as f:
        return json.load(f)


def list_docs():
    docs = load_docs()
    print('可用政策文档（' + str(len(docs)) + ' 份）：')
    for d in docs:
        print('  [' + d['short'] + ']（' + d['year'] + '年·' + d['layer'] + '） ' + d['desc'])
        print('     顶层章节：' + (' / '.join(d['sections']) if d['sections'] else '无'))


def find_doc(docs, kw):
    """按关键词匹配文档，返回文档对象或 None"""
    for d in docs:
        if kw in d['short'] or kw in d['file'] or kw in d['layer']:
            return d
    return None


def clean_tail(w):
    """去掉候选词末尾的疑问/语气单字，如 星级评定标准是 -> 星级评定标准"""
    for ch in '是吗呢的了啊呀吧么啦':
        if w.endswith(ch) and len(w) > 2:
            w = w[:-1]
    return w


def extract_kw(question):
    """从问题中提取关键词：去掉停用词，保留>=2字词元，清洗尾字，并做术语扩展"""
    kws = []
    q = question
    for s in STOP:
        q = q.replace(s, ' ')
    for part in q.split():
        part = clean_tail(part.strip())
        if len(part) >= 2 and part not in kws:
            kws.append(part)
    terms = load_terms()
    expanded = list(kws)
    for k in kws:
        for syn in terms.get(k, []):
            if syn not in expanded:
                expanded.append(syn)
    return kws, expanded


def ngram_candidates(question):
    """把问题切成长 2~4 字的连续子串，供整词无命中时兜底检索"""
    out = []
    n = len(question)
    for L in (4, 3, 2):
        for i in range(n - L + 1):
            w = question[i:i + L]
            if len(w) == L and w not in out:
                out.append(w)
    return out


def search(question, limit=6):
    """在全部文档中检索，返回按命中加权的片段列表；整词命中不足时用 n-gram 兜底"""
    docs = load_docs()
    kws, expanded = extract_kw(question)
    hits = []
    for di, d in enumerate(docs):
        for item in d['items']:
            text = item['text']
            score = 0
            matched = []
            for kw in expanded:
                if kw in text:
                    score += max(len(kw), 2)
                    matched.append(kw)
            if score > 0:
                hits.append({
                    'doc': d['short'],
                    'year': d['year'],
                    'layer': d['layer'],
                    'sec': ' / '.join(item['sec']) if item['sec'] else '',
                    'text': text,
                    'score': score,
                    'matched': matched,
                })
    # n-gram 兜底：整词命中不足 3 条时，用问题子串补充
    if len(hits) < 3:
        ngrams = ngram_candidates(question)
        seen_text = set(h['text'] for h in hits)
        for d in docs:
            for item in d['items']:
                text = item['text']
                if text in seen_text:
                    continue
                score = 0
                matched = []
                for ng in ngrams:
                    if ng in text:
                        score += len(ng)
                        matched.append(ng)
                if score >= 4:  # 至少 2 字×2 次或 1 个 4 字词命中才采纳
                    seen_text.add(text)
                    hits.append({
                        'doc': d['short'],
                        'year': d['year'],
                        'layer': d['layer'],
                        'sec': ' / '.join(item['sec']) if item['sec'] else '',
                        'text': text,
                        'score': score * 0.6,  # n-gram 权重打折，整词命中优先
                        'matched': matched,
                    })
    hits.sort(key=lambda x: x['score'], reverse=True)
    return hits[:limit], kws, expanded


def link_data(kws):
    """政策<->数据联动：当问题命中 Excel 相关指标时，附实测数据"""
    try:
        sys.path.insert(0, HERE)
        from analyzer import load_analyzed, summarize, load_county_summary, fmt_wan
        chans = load_analyzed()
        S = summarize(chans)
        CS = load_county_summary()
        qz = CS.get('全州', {})
    except Exception as e:
        return '（联动失败：' + str(e) + '）'

    kwj = ' '.join(kws)
    lines = []
    if any(k in kwj for k in ['门槛', '否决', '达档']):
        gate_zero = sum(1 for c in chans if c['gate_level'] == '门槛未完成' and c['tiger'] == 0 and c['ai5'] == 0 and c['rights_up'] == 0 and c['member88'] == 0)
        lines.append('【门槛·实测】未达档 ' + str(S['gate_notdone']) + ' 家（' + '{:.1f}'.format(S['gate_notdone_rate']) + '%），单道损收 ' + fmt_wan(abs(qz.get('gate_loss', 0)) * 10000) + '（全州口径），其中完全无业务 ' + str(gate_zero) + ' 家')
    if any(k in kwj for k in ['激励', '金额', '返利', '佣金', '损失']):
        lines.append('【激励·实测】原始 ' + fmt_wan(S['raw_total']) + ' → 最终 ' + fmt_wan(S['final_total']) + '，损失 ' + fmt_wan(S['loss_total']) + '（' + '{:.1f}'.format(S['loss_rate']) + '%），最终 0 元渠道 ' + str(S['zero_final']) + ' 家')
    if any(k in kwj for k in ['星级']):
        stars = {}
        for c in chans:
            s = str(c.get('star', '') or '').strip()
            stars[s] = stars.get(s, 0) + 1
        top = sorted(stars.items(), key=lambda x: -x[1])[:5]
        lines.append('【星级·实测】渠道星级分布：' + '，'.join(str(k) + '星:' + str(v) + '家' for k, v in top if k))
    if any(k in kwj for k in ['APP', '融合']):
        n = S['n']
        coef08 = sum(1 for c in chans if abs(c['app_coef'] - 0.8) < 0.001)
        lines.append('【APP融合·实测】新入网 ' + '{:.1f}'.format(S['avg_newnet_fuse']) + '% / 新终端 ' + '{:.1f}'.format(S['avg_newterm_fuse']) + '% / 宽带 ' + '{:.1f}'.format(S['avg_bb_fuse']) + '%，系数 0.8 被扣渠道 ' + str(coef08) + ' 家（' + '{:.0f}'.format(coef08 / n * 100) + '%）')
    if any(k in kwj for k in ['合约']):
        lines.append('【终端合约·实测】合约率均值 ' + '{:.1f}'.format(S['avg_term']) + '%，为 0 的渠道 ' + str(S['zero_term']) + ' 家')
    if any(k in kwj for k in ['弱势', '攻坚']):
        lines.append('【弱势网格·实测】相关扣罚以县汇总表为准：' + fmt_wan(abs(qz.get('weakgrid_loss', 0)) * 10000))
    if any(k in kwj for k in ['投诉']):
        lines.append('【投诉·实测】当期有责投诉未出数，按不扣罚计，存在追溯扣罚风险（县汇总表投诉损收 ' + fmt_wan(abs(qz.get('complaint_loss', 0)) * 10000) + '）')
    if any(k in kwj for k in ['牵引', '协同', '重点']):
        lines.append('【牵引/重点业务·实测】系数 0.81 渠道 ' + str(S['coef081']) + ' 家 / 0.9 共 ' + str(S['coef09']) + ' 家 / 1.0 共 ' + str(S['coef1']) + ' 家，重点业务单道损收 ' + fmt_wan(abs(qz.get('focus_loss', 0)) * 10000))
    return '\n'.join(lines) if lines else ''


def summary(kw):
    """模式F：文档总结分析"""
    docs = load_docs()
    d = find_doc(docs, kw)
    if not d:
        print('未找到匹配文档，可用：' + '、'.join(x['short'] for x in docs))
        return
    print('=' * 66)
    print('【文档分析】' + d['short'] + '（' + d['year'] + '年版）')
    print('  定位：' + d['layer'] + ' · ' + d['desc'])
    print('  篇幅：段落 ' + str(d['n_paras']) + ' 段 / 表格 ' + str(d['n_tables']) + ' 张 / 约 ' + '{:,}'.format(d['chars']) + ' 字')
    print('  顶层章节：')
    seen = set()
    for item in d['items']:
        if item['sec'] and item['sec'][0] not in seen and len(item['text']) <= 40:
            seen.add(item['sec'][0])
            print('    · ' + item['sec'][0])
    print()
    print('--- 核心政策规则（带原文依据） ---')
    n = 0
    for item in d['items']:
        t = item['text']
        if RULES.search(t) and len(t) >= 18:
            sec = ' / '.join(item['sec']) if item['sec'] else '（无章节）'
            print('[' + sec + ']')
            print('  ' + t)
            n += 1
            if n >= 18:
                break
    if n == 0:
        print('（未提取到明显的规则性条款）')


def ask(question):
    """模式G：检索问答"""
    docs = load_docs()
    hits, kws, expanded = search(question)
    print('问题：' + question)
    print('检索关键词：' + '、'.join(expanded[:10]))
    if not hits:
        print('\n未检索到直接相关条款。可尝试换一种问法，或缩小到具体文档（如：查管理办法里的准入要求）。')
        return
    print('\n--- 检索结果（' + str(len(hits)) + ' 条，按相关度排序） ---')
    for i, h in enumerate(hits, 1):
        sec = h['sec'] if h['sec'] else '（无章节）'
        print(str(i) + '. [' + h['doc'] + '·' + h['year'] + '年版 · ' + h['layer'] + '] ' + sec)
        print('   ' + h['text'][:160])
    dl = link_data(kws)
    if dl:
        print('\n--- 政策⇄数据联动（2026年3季度实测） ---')
        print(dl)
    print('\n--- 综合回答 ---')
    print('以上条款来自 ' + '、'.join(sorted(set(h['doc'] for h in hits))) + '（注意版本年份，新旧规则以最新发文为准）。')


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] == 'docs':
        list_docs()
    elif args[0] == 'summary':
        summary(args[1] if len(args) > 1 else '')
    elif args[0] == 'ask':
        ask(' '.join(args[1:]))
    else:
        print('用法: doc_qa.py docs | summary <文档名> | ask <问题>')
