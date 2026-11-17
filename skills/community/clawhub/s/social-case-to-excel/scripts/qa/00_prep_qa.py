# -*- coding: utf-8 -*-
"""00_prep_qa.py —— 给一次新跑批生成 QA 配置与「路径已适配」的 QA/探针脚本副本。

为什么需要它：scripts/qa/*.py 里的路径与变量名是上一轮跑批的（/tmp/cb_sel.json、
/tmp/tcb%d.py、旧 xlsx/md…），直接跑会报 FileNotFoundError，或者更糟——静默读到
上一次的数据、给出「全绿」的假结论。每次手工写一个 sed 适配脚本既慢又容易漏。

做法：把本次跑批的路径/条数写进一份 config.json，再复制 scripts/qa/ 下所有脚本到
工作目录，逐个做确定性替换。跑完打印本次该执行的命令清单。

用法：
  python3 00_prep_qa.py --tag bf --outdir /tmp/bf \
    --sel /tmp/bf/bf_sel.json \
    --raw '/tmp/bf/bf*_all.json' \
    --short /tmp/bf/bf_short.json \
    --rows '/tmp/bf/bf_rows*.py' \
    --tbf '/tmp/bf/tbf*.py' \
    --xlsx '/tmp/social-case-to-excel-example/AI黑五案例拆解库_xxx.xlsx' \
    --md   '/tmp/social-case-to-excel-example/AI黑五案例研究_35条.md' \
    --outdir /tmp

要点：
1. 入选池 JSON（sel）通常不含 text 字段（text 只存在于原始抓取记录里）。本脚本会把
   原始记录里的 text 回填进 sel，产出 <tag>_sel_qa.json —— 所有 QA 都读它。
2. qa_03 曾经把某个 tid 硬编码在脚本里，换话题就 KeyError。这里已把它改成遍历全部
   入选帖；如果以后再看到硬编码 tid，直接在 scripts/qa/ 里改掉，不要每轮 sed。
3. 替换是「确定性字面量替换」而不是正则猜测：找不到的字面量会打印 warning，
   提示你脚本可能被改过、需要人工看一眼。
4. 原始抓取不一定是 X 的结构。load_tweets() 对非 X 数据源（ClaudeBaby Reddit 返回等）做了一层
   字段归一（id→tweet_id、title+selftext→text），摊平出 0 条时会显式告警——看到告警
   说明以 raw 为输入的探针读到的是空数据，结论不可信，要先修字段映射或 --raw glob。
"""
import argparse, glob, json, os, re, shutil, sys

SKILL_QA = os.path.dirname(os.path.abspath(__file__))

# 上一轮跑批留下的字面量（QA 脚本的默认值），替换成这次的值
OLD_XLSX = '/tmp/social-case-to-excel-example/跨境电商案例拆解库_X_选品-黑五-关键词-Listing-站外-Reddit_20260916.xlsx'
OLD_MD = '/tmp/social-case-to-excel-example/跨境电商案例研究_42条_20260916.md'
OLD_SEL = '/tmp/cb_sel.json'
OLD_SHORT = '/tmp/cbx_short.json'
OLD_SHORT2 = '/tmp/cbx_short2.json'
OLD_TCB = '/tmp/tcb%d.py'
# QA 脚本里用到的完整表达式（要整段换成「读文件清单 json」，见 main() 里的说明）
OLD_TCB_EXPR = "['/tmp/tcb%d.py' % i for i in range(1, 7)]"
OLD_RAW = ['/tmp/cbx1_all.json', '/tmp/cbx2_all.json', '/tmp/cbx3_all.json', '/tmp/cbx4_all.json']


def load_tweets(paths):
    """把若干原始抓取 JSON 里的 tweet 全部摊平成一个 tid -> tweet 字典。
    结构兼容 {label: {keyword, tweets:[...]}} 与本文件里直接是 list/dict 的情况。

    非 X/Twitter 数据源（例如 ClaudeBaby 返回的 Reddit 记录）的字段名不一样，这里做一层归一：
      tid  ← tweet_id | id | name(t3_xxx 形式去掉前缀)
      text ← text | selftext（Reddit 正文，标题另拼在前面）| body
    否则摊平结果会是 0 条，probe_*_raw_records_sanity 这类以 raw 为输入的探针会
    静默读到空数据、给出「全绿但没意义」的结论。所以下面还会对「摊平 0 条」显式告警。
    """
    recs = {}

    def norm(obj):
        """把一条非 X 结构记录补成 {tweet_id, text} 形状；补不出来就返回 None。"""
        tid = obj.get('tweet_id') or obj.get('id') or ''
        if isinstance(tid, str) and tid.startswith('t3_'):
            tid = tid[3:]
        text = obj.get('text')
        if text is None:
            body = obj.get('selftext') or obj.get('body') or ''
            title = obj.get('title') or ''
            if body or title:
                text = (title + '\n\n' + body).strip()
        if tid and text is not None:
            d = dict(obj)
            d['tweet_id'] = str(tid)
            d['text'] = text
            return d
        return None

    def eat(obj):
        if isinstance(obj, dict):
            got = norm(obj)
            if got:
                recs.setdefault(got['tweet_id'], got)
                return
            for v in obj.values():
                eat(v)
        elif isinstance(obj, list):
            for v in obj:
                eat(v)

    for p in paths:
        eat(json.load(open(p, encoding='utf-8')))
    if not recs:
        print('!! 警告：--raw 摊平出 0 条记录 —— 原始结构既不是 X 的 {label:{tweets:[]}}，'
              '也没有可识别的 id/selftext/body 字段。\n'
              '   以 raw 为输入的探针（probe_03_raw_records_sanity 等）会读到空数据、'
              '给出一看就通过但无意义的结论。\n'
              '   请检查 --raw glob 是否指到了真正的抓取文件，或在此函数里补字段映射。')
    return recs


def pick_rows(sel):
    """从 sel 文件里取出「入选行」列表，兼容三种历史写法。

    06_select.py 写的是 {'picked': [...]}（可能还有 'miss'），更早的跑批写成裸 list
    或 {'rows': [...]}。以前只认 list / 'rows'，遇到 {'picked': ...} 会把整个 dict 当成
    行列表去迭代，报 `TypeError: string indices must be integers` —— 这里的兜底是：
    按已知键名找，找不到就取 dict 里第一个「元素是 dict 且带 tid」的列表值。
    """
    if isinstance(sel, list):
        return sel
    for k in ('picked', 'rows', 'cases', 'sel'):
        v = sel.get(k)
        if isinstance(v, list):
            return v
    for v in sel.values():
        if isinstance(v, list) and v and isinstance(v[0], dict) and 'tid' in v[0]:
            return v
    sys.exit('sel 文件里找不到入选行列表（期望 list 或 {picked: [...]}），请检查 %s' % sel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', required=True, help='本次跑批前缀，例如 bf')
    ap.add_argument('--sel', required=True, help='入选池 JSON（含 tid）')
    ap.add_argument('--raw', required=True, help='原始抓取 JSON 的 glob，例如 "/tmp/bf/bf*_all.json"')
    ap.add_argument('--outdir', default='/tmp')
    ap.add_argument('--xlsx', default='')
    ap.add_argument('--md', default='')
    ap.add_argument('--short', default='')
    ap.add_argument('--cases', default='')
    ap.add_argument('--rows', default='')
    ap.add_argument('--tbf', default='')
    ap.add_argument('--extra', default='{}', help='附加配置（JSON 字串），写进 config 供人工查阅')
    a = ap.parse_args()

    workdir = a.outdir.rstrip('/')
    os.makedirs(workdir, exist_ok=True)   # 输出目录不存在时以前会跑到写文件那一步才报错
    raw_paths = sorted(glob.glob(a.raw))
    if not raw_paths:
        sys.exit('原始抓取文件没匹配到：%s' % a.raw)
    recs = load_tweets(raw_paths)

    sel = json.load(open(a.sel, encoding='utf-8'))
    rows = pick_rows(sel)
    miss = []
    for r in rows:
        t = recs.get(str(r.get('tid', '')))
        if t and t.get('text'):
            r['text'] = t['text']
        elif not r.get('text'):
            miss.append(r.get('tid'))
    sel_qa = os.path.join(workdir, '%s_sel_qa.json' % a.tag)
    json.dump(rows, open(sel_qa, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    tbf = sorted(glob.glob(a.tbf)) if a.tbf else []
    if not tbf:
        # 没传 --tbf 时先就地找一找，别让 qa_01/02/04/probe_06 静默读到 0 条译文
        tbf = sorted(set(glob.glob(os.path.join(workdir, '%s_tcb*.py' % a.tag))
                         + glob.glob(os.path.join(workdir, '%s_t*.py' % a.tag))))
    n_tbf = len(tbf) or 6
    # 译文/推文文件清单**不能靠「把文件名末尾的数字换成 %d」来猜**：文件名可能是
    # tcb0_cn.py（数字不在 .py 紧邻处）、tcb_a.py（根本没有数字）、甚至有多个数字段，
    # 正则猜不中时 pattern 会退化成字面量原路径，注入 qa_01/02/04/probe_06 后
    # 变成 `'/tmp/x/tcb0_cn.py' % i` → TypeError: not all arguments converted
    # during string formatting（本批为此丢过一轮）。
    # 做法：把匹配到的真实文件清单写成 json，生成脚本改成读这个 json ——
    # 这四个脚本都已经 import json，不需要额外注入 import。
    if tbf:
        tbf_list = os.path.join(workdir, '%s_tbf_list.json' % a.tag)
        json.dump(tbf, open(tbf_list, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        tcb_expr = "json.load(open('%s', encoding='utf-8'))" % tbf_list
        print('tbf files : %d → %s' % (len(tbf), tbf_list))
    else:
        tbf_list = ''
        tcb_expr = None
        print('!! 没传 --tbf 且 %s 下没找到 <tag>_tcb*.py / <tag>_t*.py：'
              'qa_01/qa_02/qa_04/probe_06 的译文覆盖检查会读到 0 条（看着像通过）。'
              '下次把 --tbf \"/tmp/<tag>/<写作文>*.py\" 显式传进来。' % workdir)

    cfg = {
        'tag': a.tag, 'workdir': workdir, 'raw': raw_paths, 'raw_tweets': len(recs),
        'sel': a.sel, 'sel_qa': sel_qa, 'sel_rows': len(rows), 'sel_missing_text': miss,
        'cases': a.cases, 'short': a.short, 'rows_glob': a.rows, 'tbf': tbf, 'tbf_count': n_tbf,
        'xlsx': a.xlsx, 'md': a.md,
    }
    try:
        cfg['extra'] = json.loads(a.extra)
    except Exception:
        cfg['extra'] = a.extra
    cfg_path = os.path.join(workdir, '%s_qa_config.json' % a.tag)
    json.dump(cfg, open(cfg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # 人工闸门要一个「构建产出的中间文件」作为入参：优先用 --cases，其次按 tag 猜
    cases_hint = a.cases if (a.cases and a.cases.endswith('.json')) else os.path.join(workdir, '%s_cases_final.json' % a.tag)

    subs = [
        (OLD_XLSX, a.xlsx or OLD_XLSX),
        (OLD_MD, a.md or OLD_MD),
        (OLD_SEL, sel_qa),
        (OLD_SHORT2, a.short or OLD_SHORT2),
        (OLD_SHORT, a.short or OLD_SHORT),
        (OLD_TCB, os.path.join(workdir, '%s_tcb%%d.py' % a.tag)),
        # 探针脚本的默认 glob（多轮抓取时逐元素替换会坏掉，改成替换 glob 本身）
        ('/tmp/cb*_all.json', a.raw),
    ]
    for p in OLD_RAW:
        subs.append((p, a.raw))

    scripts = sorted(f for f in os.listdir(SKILL_QA)
                     if f.endswith('.py') and not f.startswith('00_') and not f.startswith('_'))
    made = []
    warn = []
    for f in scripts:
        src = open(os.path.join(SKILL_QA, f), encoding='utf-8').read()
        out = src
        touched = False
        # 整段替换译文/推文文件清单的表达式（必须早于 subs，否则 '/tmp/tcb%d.py'
        # 这个子串会先被 subs 换成新 pattern，表达式就再也匹配不上了）
        if tcb_expr and OLD_TCB_EXPR in out:
            out = out.replace(OLD_TCB_EXPR, tcb_expr)
            touched = True
        for old, new in subs:
            if old and old in out:
                out = out.replace(old, new)
                touched = True
        # 老脚本里一定有 /tmp/cb_sel.json 这类字面量；一个都没替换到说明脚本被改过
        if '/tmp/cb' in out:
            out = re.sub(r"/tmp/cb(?=[A-Za-z0-9_]*\.(?:json|txt|py))",
                         os.path.join(workdir, a.tag), out)
            touched = True
        # 只改「与译文/推文文件相关」的 range(1, 7)：qa_04 打印 sheet6 列用的也是
        # range(1, 7)，被无差别替换会少印/多印列（这类"看着正常"的错更难发现）
        if 'range(1, 7)' in out:
            lines = []
            for ln in out.split('\n'):
                if 'range(1, 7)' in ln and ('tcb' in ln or 'tbf' in ln or '译文' in ln):
                    ln = ln.replace('range(1, 7)', 'range(1, %d)' % (n_tbf + 1))
                    touched = True
                lines.append(ln)
            out = '\n'.join(lines)
        if not touched:
            warn.append(f)
        dst = os.path.join(workdir, '%s_%s' % (a.tag, f))
        open(dst, 'w', encoding='utf-8').write(out)
        made.append(dst)

    # 生成完自检：还留着上一轮 tbf 表达式的脚本会 TypeError / 静默读 0 条译文
    # （只认「读 /tmp/tcb%d.py」这种真残留；range(1, 7) 也可能是列循环，不能当信号）
    stale = []
    for p in made:
        s = open(p, encoding='utf-8').read()
        if "['/tmp/tcb%d.py'" in s or "tcb%d.py' % i" in s:
            stale.append(os.path.basename(p))
    if stale:
        print('!! 这些生成脚本仍带着上一轮的译文/推文文件表达式（会 TypeError 或读不到文件）：%s' % stale)
        print('   检查 --tbf 是否为该 glob 或对应文件是否存在，必要时手工改成读 <workdir>/<tag>_tbf_list.json。')
    else:
        print('tbf check : 译文/推文文件表达式已全部改写（无残留）')

    if warn:
        print('!! 这些脚本没有任何可替换的路径字面量（gate_* / qa_11 / 接受 argv 的脚本属正常）：%s' % warn)
        print('   ↑ 这几关**必须显式传参**才会真的检查（gate_01/gate_02 吃构建产出的中间 json，qa_11 吃 xlsx/path）。'
              '直接跑 run_all_qa.sh 会替你传，别只跑 qa_0* 就以为全过了。')

    print('raw files : %d（摊平 %d 条推文）' % (len(raw_paths), len(recs)))
    print('sel rows  : %d → %s' % (len(rows), sel_qa))
    if miss:
        print('!! 这些 tid 在原始记录里找不到 text，QA 会拿不到原文：%s' % miss)
    print('config    : %s' % cfg_path)
    print('adapted   : %d 个脚本' % len(made))
    print()
    print('下一步（在 %s 下执行）：' % workdir)
    print('  # 推荐：一条命令跑完十条 QA + probe + 两道人工闸门 + 脱敏，日志落盘（PTY 回显会截断，别逐条翻屏）')
    print('  bash %s/run_all_qa.sh --tag %s --outdir %s --cases %s \\' % (SKILL_QA, a.tag, workdir, cases_hint))
    print("       --xlsx '%s' --md '%s'" % (a.xlsx or '<xlsx>', a.md or '<md>'))
    print('  # 或者手工逐条跑（注意最后三行必须显式传参，它们没有默认路径）：')
    print('  for f in %s/%s_qa_0*.py; do echo "## $f"; python3 "$f"; done' % (workdir, a.tag))
    print('  for f in %s/%s_probe_0*.py; do echo "## $f"; python3 "$f"; done' % (workdir, a.tag))
    print('  python3 %s/%s_gate_01_no_english_leftover.py %s' % (workdir, a.tag, cases_hint))
    print('  python3 %s/%s_gate_02_second_person.py %s' % (workdir, a.tag, cases_hint))
    print('  python3 %s/%s_qa_11_no_vendor_leak.py %s %s' % (workdir, a.tag, a.xlsx or "'<xlsx>'", a.md or "'<md>'"))


if __name__ == '__main__':
    main()
