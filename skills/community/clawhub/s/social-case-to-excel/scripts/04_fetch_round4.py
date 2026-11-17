# -*- coding: utf-8 -*-
"""社媒案例库 Round4：重跑 Round3 失败的组合 + 补捞长尾。

**为什么单独有一轮"重跑"**：本通道约 30s 代理硬超时且是**静默失败**（HTTP 200 + 空 body
或 `upstream_unavailable`），首轮冷启经常挂掉几个组合。这类失败**不是"该社区没内容"**，
必须原样重发同一参数（吃服务端缓存，通常 1–2s 返回）；**改参数是大忌**——新参数 = 新
cache key，会重新冷跑再超时。

`harvest_round()` 已经对每个组合做了一次原样重试，并把仍失败的写进
`/tmp/cbx3_errors.json`；本脚本读那个文件，把失败组合**原封不动**再跑一遍，
外加几条首轮没覆盖的补捞词。
"""
import json, os
import cb_mcp

LIMIT = 300
DAYS = 1095
OUT = '/tmp/cbx4_all.json'
ERR = '/tmp/cbx3_errors.json'

# 补捞：首轮没覆盖的长尾社区/词
EXTRA = [
    ('h1_ecom_launch',  'ecommerce',   '"i launched" OR "we launched" results OR sales', DAYS),
    ('h2_fba_q4',       'AmazonFBA',   'Q4 OR "holiday" results OR sales', DAYS),
    ('h3_shop_scale',   'shopify',     '"we scaled" OR scaled OR "grew to" revenue', DAYS),
    ('h4_email_life',   'EmailMarketing', 'lifecycle OR retention OR "repeat purchase"', DAYS),
    ('h5_reddit_cust',  'smallbusiness', '"reddit" customers OR leads OR sales', DAYS),
]


def specs():
    out = list(EXTRA)
    if os.path.exists(ERR):
        try:
            errs = json.load(open(ERR, encoding='utf-8'))
        except Exception:
            errs = []
        for e in errs:
            label, sub, q, d = e.get('label'), e.get('subreddit'), e.get('query'), e.get('days')
            if label and sub and q:
                out.append((label, sub, q, int(d or DAYS)))
        print('从 %s 恢复 %d 个失败组合' % (ERR, len(out) - len(EXTRA)))
    else:
        print('（没有 %s：Round3 无失败组合，本脚本只跑补捞词）' % ERR)
    return out


if __name__ == '__main__':
    cb_mcp.harvest_round(specs(), OUT, limit=LIMIT, sleep=2.0,
                         per_label_files='/tmp/cbx4_%s.json')
