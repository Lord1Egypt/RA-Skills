"""
雪球帖子 V4 规则分析脚本（独立运行版）
======================================
功能：
  - 对已采集的雪球帖子做批量/单条 V4 规则分析
  - 零 token 消耗，纯规则引擎
  - 支持补分析未分析的帖子

使用方式：
  py scripts/analyze.py --db "data/xueqiu.db" --missing      # 只分析未分析的
  py scripts/analyze.py --db "data/xueqiu.db" --batch          # 全量重分析
  py scripts/analyze.py --db "data/xueqiu.db" --post-id 382580032  # 单条分析
  py scripts/analyze.py --db "data/xueqiu.db" --missing --limit 50   # 限制数量
"""

import sys
import os
import json
import re
import sqlite3
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# ── 路径 ──
_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent

# ════════════════════════════════════════
#  V4 分析引擎（从 collect.py 复用，独立可用）
# ════════════════════════════════════════

STOCK_MAP = {
    '腾讯': '00700.HK', '00700': '00700.HK', '唯品会': 'VIPS', 'VIPS': 'VIPS',
    '拼多多': 'PDD', 'PDD': 'PDD', '小赢': 'XYF', '小赢科技': 'XYF',
    '江南布衣': '03306.HK', 'JNBY': '03306.HK', '中化化肥': '00297.HK',
    '申洲国际': '02313.HK', '申洲': '02313.HK',
    '东江': '02283.HK', '东江集团': '02283.HK',
    '珩湾科技': '09609.HK', '珩湾': '09609.HK',
    '阿里': '09988.HK', '阿里巴巴': '09988.HK', 'BABA': '09988.HK',
    '美团': '03690.HK', '京东': '09618.HK', 'JD': '09618.HK',
    '百度': '09888.HK', 'BIDU': '09888.HK', '华晨中国': '01114.HK',
    '英美烟草': 'BTI', '比亚迪': '01211.HK', 'BYD': '01211.HK',
    '贵州茅台': '600519.SH', '茅台': '600519.SH',
    '招商银行': '03968.HK', '招行': '03968.HK',
    '中国平安': '02318.HK', '平安': '02318.HK',
    '网易': '09999.HK', '小米': '01810.HK', '快手': '01024.HK',
    '泡泡玛特': '09992.HK', '农夫山泉': '09633.HK',
    '格力': '000651.SZ', '宁德时代': '300750.SZ',
    '苹果': 'AAPL', 'Apple': 'AAPL', '英伟达': 'NVDA', 'NVIDIA': 'NVDA',
    '微软': 'MSFT', '特斯拉': 'TSLA',
}
CODE_TO_NAME = {}
for name, code in STOCK_MAP.items():
    if code not in CODE_TO_NAME or len(name) < len(CODE_TO_NAME[code]):
        CODE_TO_NAME[code] = name

OP_PATTERNS = {
    '买入': ['买入', '加仓', '买了', '买点', '建仓', '重仓', '补仓', '抄底', '进场'],
    '卖出': ['卖出', '减仓', '清仓', '止损', '卖了', '离场', '割肉', '止盈', '获利了结'],
    '持有': ['持仓', '继续持有', '不动', '长持', '继续拿', '躺平', '死拿', '装死'],
    '观察': ['观察', '关注', '研究', '考虑', '犹豫', '纠结', '等', '观望'],
}

POS_WORDS = ['看好','乐观','有信心','很好','不错','增长','回购','分红','上涨','涨了',
             '牛','超预期','值得','优秀','低估','便宜','机会']
NEG_WORDS = ['担心','亏损','跌了','下跌','悲观','风险','止损','不好','错了','熊',
             '大跌','暴跌','暴雷','不及预期','高位','泡沫','套牢','割肉']

TOPIC_PATTERNS = {
    '估值分析':['估值','PE','PB','DCF','市盈率','市净率','EPS','PS'],
    '财务分析':['营收','利润','财报','年报','季报','毛利率','净利率','ROE','ROA'],
    '股东回报':['回购','分红','股息','派息'], '业绩分析':['业绩','增长','下滑','收入','盈利','同比','环比'],
    '公司研究':['调研','产品','管理层','竞争对手','壁垒','商业模式','护城河','核心竞争力'],
    '行业分析':['行业','竞争','市场份额','赛道','趋势','格局','龙头'],
    '宏观经济':['经济','GDP','通胀','利率','货币','政策','美联储','央行','降息','加息'],
    '市场情绪':['情绪','恐慌','贪婪','散户','机构','换手','量能'],
    '投资理念':['价值投资','长期持有','复利','巴菲特','芒格','费雪','唐朝','烟蒂','安全边际','能力圈'],
    '操作记录':['买入','卖出','加仓','减仓','止损','清仓','建仓','调仓','仓位'],
    '港股':['港股','恒生','H股','香港'], '美股':['美股','纳斯达克','标普'],
    'A股':['A股','沪深','创业板','科创板'],
    '科技互联网':['人工智能','云计算','芯片','半导体','SaaS','自动驾驶','大模型','ChatGPT'],
    '消费':['消费','零售','品牌','服装','食品','白酒'], '金融':['银行','保险','券商'],
    '新能源':['新能源','光伏','风电','锂电','储能','电动车'], '医药':['医药','创新药','CXO','医疗器械'],
    '读书笔记':['读书','笔记','书','学习','总结'], '生活感悟':['生活','感悟','心态','随笔','日记'],
    'ETF基金':['ETF','基金','指数基金','LOF','定投'],
}


def classify_post_type(full_content):
    """识别帖子类型"""
    if not full_content or not full_content.strip():
        return {'post_type':'empty','own_text':'','quote_text':''}
    text = full_content.strip()
    if '当前网址:' in text[:50] or '请求时间:' in text[:50]:
        return {'post_type':'error','own_text':'','quote_text':''}

    if '> **引用：**' in text:
        lines, own, quote, iq = text.split('\n'), [], [], False
        for line in lines:
            s = line.strip()
            if s == '> **引用：**': iq = True; continue
            if iq and s.startswith('> '): quote.append(s[2:]); continue
            if iq and s == '>': continue
            if iq and not s.startswith('> '): iq = False; own.append(s); continue
            if not iq: own.append(s)
        ot, qt = '\n'.join(own).strip(), '\n'.join(quote).strip()
        return {'post_type':'reply','own_text':ot,'quote_text':qt} if qt else None

    qm = re.search(r'^(.*?)//(.*?)$', text, re.DOTALL)
    if qm:
        b, a = qm.group(1).strip(), qm.group(2).strip()
        if b.startswith(':') and ':回复' in a and len(b) < 500:
            return {'post_type':'reply','own_text':_extract_reply(a),'quote_text':b[1:].strip()}

    if '\n作者\n' in text:
        lines, ai_list, own, quote, iq = text.split('\n'), [], [], [], False
        for i, l in enumerate(lines):
            if l.strip() == '作者': ai_list.append(i)
        if ai_list:
            i = 0
            while i < len(lines):
                s = lines[i].strip()
                if not s or s in {'讨论','赞','好友'}: i+=1; continue
                if s == '作者' and i+1<len(lines):
                    iq=True; qn=lines[i+1].strip(); i+=2
                    if i<len(lines) and lines[i].strip().startswith('：'):
                        qc=[]
                        while i<len(lines) and lines[i].strip().startswith('：'): qc.append(lines[i].strip()[1:]); i+=1
                        quote.append(qn+': '+' '.join(qc))
                    else: quote.append(qn)
                    continue
                if s.startswith('：') and not iq:
                    iq=True; quote.append(s[1:]); i+=1
                    while i<len(lines) and lines[i].strip().startswith('：'): quote.append(lines[i].strip()[1:]); i+=1
                    continue
                if iq: iq=False
                own.append(s); i+=1
            qt='\n'.join(quote).strip()
            if qt: return {'post_type':'reply','own_text':'\n'.join(own).strip(),'quote_text':qt}

    return {'post_type':'original','own_text':text,'quote_text':''}


def _extract_reply(rs):
    """提取对话链中用户的话"""
    lines=rs.split('\n'); own=[]; st=False
    for l in lines:
        s=l.strip()
        if s==':回复': st=True; continue
        if not st: continue
        if not s or s in{'讨论','赞','好友'}: continue
        if s.startswith('：') or s=='好友': continue
        if s.startswith(':'): own.append(s[1:])
        elif s not in{'©'}: own.append(s)
    return '\n'.join(own).strip()


def analyze_post(title, full_content, category):
    """V4 完整规则分析"""
    content=(full_content or '').strip()
    ti=classify_post_type(content)
    pt, own_text=ti['post_type'], ti['own_text']
    at=own_text if (pt=='reply' and own_text) else content
    text=at+' '+(title or '')

    stocks, ss=[], set()
    for name, code in STOCK_MAP.items():
        if name in text and code not in ss: ss.add(code); stocks.append({'code':code,'name':CODE_TO_NAME.get(code,code)})

    ops=[]
    for op,kws in OP_PATTERNS.items():
        if any(kw in text for kw in kws): ops.append(op)

    pc=sum(1 for w in POS_WORDS if w in text); nc=sum(1 for w in NEG_WORDS if w in text)
    sentiment='看多' if pc>nc+1 else ('看空' if nc>pc+1 else '中性')

    topics, ts=[], set()
    for tp, kws in TOPIC_PATTERNS.items():
        if tp not in ts and any(kw in text for kw in kws): topics.append(tp); ts.add(tp)

    cl=len(at)
    if cl<10: ct='空内容'
    elif re.search(r'(买入|卖出|加仓|减仓).{0,20}(元|股|手|均价)', text): ct='交易记录'
    elif re.search(r'\d+\.?\d*\s*(亿|万|%)', text) and len(re.findall(r'\d+\.?\d*\s*(亿|万|%)', text))>=3: ct='数据分析'
    elif re.search(r'(觉得|认为|看法)', text): ct='讨论交流'
    elif category in('读书笔记',) or re.search(r'(读书|笔记|读后)', text): ct='读书笔记'
    elif cl<80: ct='短评'
    elif cl>500: ct='深度分析'
    else: ct='一般讨论'

    ti_op=ops[0] if ops else '无'
    if cl<5: ir='none'
    elif stocks and ti_op!='无' and cl>100: ir='high'
    elif stocks and ct in('深度分析','数据分析','交易记录') and cl>100: ir='high'
    elif len(stocks)>=2 and cl>100: ir='high'
    elif stocks and cl>200 and category not in('读书笔记','生活随笔'): ir='high'
    elif stocks and cl>50: ir='medium'
    elif stocks and cl>10: ir='low'
    elif stocks: ir='low'
    elif category not in('其他',) and category not in('读书笔记','生活随笔'): ir='medium'
    elif ct in('交易记录','数据分析','深度分析'): ir='medium'
    elif ti_op!='无': ir='low'
    elif category in('读书笔记','生活随笔'): ir='none'
    else: ir='none'

    depth='短评' if cl<80 else ('中篇' if cl<300 else ('长文' if cl<800 else '深度长文'))
    if pt in('error','empty') or cl<10: qs=0
    elif ir=='none': qs=1
    else:
        qs=2
        if stocks: qs+=1
        if depth in('长文','深度长文'): qs+=1
        if ops: qs+=1
        if ct in('深度分析','数据分析','交易记录'): qs+=1
        if ir=='high': qs+=1
        qs=min(qs,5)

    summary=re.sub(r'//\s*@[^\n]+','',at)
    summary=re.sub(r'@\w+\s*[:：]?\s*','',summary)
    summary=re.sub(r'https?://[^\s]+','',summary)
    for pat in [r'修改于',r'发布于',r'来自\w+',r'讨论\s*\d+',r'赞\s*\d+']:
        summary=re.sub(pat,'',summary)
    summary=re.sub(r'\n{3,}','\n\n',summary).strip()[:300]

    sn=[s['name'] for s in stocks]
    return {
        'post_type':pt,'own_text':own_text or None,'quote_text':ti.get('quote_text') or None,
        'tags':json.dumps(sn,ensure_ascii=False) if sn else None,
        'sentiment':sentiment,'trade_intent':ti_op,'content_type':ct,
        'quality_score':qs,'investment_relevance':ir,'word_count':cl,
        'summary':summary or None,'content_depth':depth,
        'topics':json.dumps(topics,ensure_ascii=False) if topics else None,
    }


# ════════════════════════════════════════
#  数据库操作
# ════════════════════════════════════════

def init_db(db_path):
    conn=sqlite3.connect(db_path)
    conn.execute("""CREATE TABLE IF NOT EXISTS xueqiu_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT, post_id TEXT UNIQUE NOT NULL,
        stock_code TEXT, source TEXT DEFAULT 'xueqiu', title TEXT, content TEXT,
        full_content TEXT, author TEXT, author_id TEXT, url TEXT, published_at TEXT,
        crawled_at TEXT, category TEXT, like_count INTEGER DEFAULT 0,
        comment_count INTEGER DEFAULT 0, repost_count INTEGER DEFAULT 0,
        read_count TEXT, image_ocr_text TEXT, post_type TEXT DEFAULT 'original',
        own_text TEXT, quote_text TEXT, investment_relevance TEXT,
        sentiment TEXT, trade_intent TEXT, content_type TEXT,
        quality_score INTEGER DEFAULT 0, word_count INTEGER DEFAULT 0,
        summary TEXT, content_depth TEXT, topics TEXT, tags TEXT,
        reply_to_post_id TEXT
    )""")
    conn.commit()
    # 确保所有分析字段存在
    cols={r[1] for r in conn.execute("PRAGMA table_info(xueqiu_posts)").fetchall()}
    for col,dtype in {'summary':'TEXT','content_depth':'TEXT','topics':'TEXT',
                      'post_type':'TEXT DEFAULT original','own_text':'TEXT',
                      'quote_text':'TEXT','investment_relevance':'TEXT',
                      'sentiment':'TEXT','trade_intent':'TEXT','content_type':'TEXT',
                      'quality_score':'INTEGER DEFAULT 0','word_count':'INTEGER DEFAULT 0',
                      'tags':'TEXT','reply_to_post_id':'TEXT'}.items():
        if col not in cols:
            conn.execute(f"ALTER TABLE xueqiu_posts ADD COLUMN {col} {dtype}")
    conn.commit()
    return conn


def batch_analyze(conn, only_missing=False, limit=None):
    """批量分析"""
    where=" AND (post_type IS NULL OR post_type='' OR summary IS NULL)" if only_missing else ""
    query=f"""SELECT post_id,title,full_content,category FROM xueqiu_posts
             WHERE full_content IS NOT NULL AND full_content!=''{where} ORDER BY id"""
    if limit: query+=f" LIMIT {limit}"
    rows=conn.execute(query).fetchall()
    processed=skipped=0
    for row in rows:
        pid,title,fc,cat=row
        if len(fc or '')<10: skipped+=1; continue
        result=analyze_post(title,fc,cat)
        conn.execute(
            """UPDATE xueqiu_posts SET post_type=?,own_text=?,quote_text=?,
               tags=?,sentiment=?,trade_intent=?,content_type=?,quality_score=?,
               investment_relevance=?,word_count=?,summary=?,content_depth=?,topics=?
               WHERE post_id=?""",
            (result['post_type'],result.get('own_text'),result.get('quote_text'),
             result['tags'],result['sentiment'],result['trade_intent'],
             result['content_type'],result['quality_score'],result['investment_relevance'],
             result['word_count'],result['summary'],result['content_depth'],
             result['topics'], pid))
        processed+=1
    conn.commit()
    return processed,skipped


def show_single(conn, post_id):
    """显示单条分析结果"""
    row=conn.execute("SELECT * FROM xueqiu_posts WHERE post_id=?", (post_id,)).fetchone()
    if not row:
        print(f'未找到 post_id={post_id}')
        return
    cols=[d[1] for d in conn.execute(f"SELECT * FROM xueqiu_posts LIMIT 0").description]
    post=dict(zip(cols,row))
    print(f"\n{'─'*50}")
    print(f"  帖子 #{post_id} 分析结果")
    print(f"{'─'*50}")
    print(f"  标题     ：{post.get('title','-')}")
    print(f"  类型     ：{post.get('post_type','-')}")
    print(f"  相关性   ：{post.get('investment_relevance','-')}")
    print(f"  情感     ：{post.get('sentiment','-')}")
    print(f"  操作意图 ：{post.get('trade_intent','-')}")
    print(f"  内容类型 ：{post.get('content_type','-')}")
    print(f"  质量     ：{post.get('quality_score',0)}分")
    print(f"  字数     ：{post.get('word_count',0)}")
    print(f"  深度     ：{post.get('content_depth','-')}")
    print(f"  主题     ：{post.get('topics','-')}")
    print(f"  提及股票 ：{post.get('tags','-')}")
    print(f"  摘要     ：{(post.get('summary') or '-')[:150]}")
    print(f"  分类     ：{post.get('category','-')}")


# ════════════════════════════════════════
#  主流程
# ════════════════════════════════════════

def main():
    p=argparse.ArgumentParser(description="雪球帖子 V4 规则分析")
    p.add_argument('--db',default=None,help='数据库路径')
    p.add_argument('--batch',action='store_true',help='全量重分析')
    p.add_argument('--missing',action='store_true',help='只分析未分析的')
    p.add_argument('--post-id',type=str,default=None,help='指定 post_id')
    p.add_argument('--limit',type=int,default=None,help='限制数量')
    args=p.parse_args()

    db_path=args.db or str(_SKILL_ROOT/'data'/'xueqiu.db')
    conn=init_db(db_path)
    total=conn.execute("SELECT COUNT(*) FROM xueqiu_posts WHERE full_content IS NOT NULL AND full_content!=''").fetchone()[0]

    if args.post_id:
        show_single(conn, args.post_id)
    elif args.batch or args.missing:
        only_missing=args.missing and not args.batch
        proc,skip=batch_analyze(conn,only_missing=only_missing,limit=args.limit)
        print(f'\n✅ 分析完成：处理 {proc} 条，跳过 {skip} 条（总有效 {total} 条）')
        # 统计
        stats=conn.execute("""SELECT post_type,investment_relevance,COUNT(*)
            FROM xueqiu_posts WHERE full_content IS NOT NULL AND full_content!=''
            GROUP BY post_type,investment_relevance ORDER BY COUNT(*) DESC""").fetchall()
        print(f'\n  {"类型":<10s}{"相关性":<8s}{"数量":>6s}\n  {"-"*26}')
        for pt,ir,cnt in stats: print(f'  {pt:<10s}{ir:<8s}{cnt:>6d}')
    else:
        p.print_help()

    conn.close()


if __name__=="__main__":
    main()
