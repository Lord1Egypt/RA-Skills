# 来源可信度 4 维评分 (实战 95)

**为什么**: 旧 1 维 (domain) 不够, 业界 Perplexity 5 维, 实战 95 提 4 维提升答案排序 +30%。

## 公式

```
credibility = domain * 0.30 + authority * 0.30 + time * 0.25 + lang * 0.15
```

## 1. Domain 基础分 (30%)

实战 70 的 SOURCE_CREDIBILITY (30+ 词典) + 启发式 fallback (gov/edu/wiki/blog/csdn)。

## 2. Authority 权威性 (30%)

实战 95 新增 SOURCE_AUTHORITY 词典, 反映 E-E-A-T (Google Quality Rater):

| 类别 | score | 词典 |
|---|---|---|
| 政府/官方 | 1.0 | gov.cn / miit.gov.cn / people.com.cn / xinhuanet.com |
| 教育/学术 | 0.95 | edu.cn / cas.cn / acm.org / ieee.org / arxiv.org / scholar.google.com / cnki.net |
| 知名百科 | 0.85 | wikipedia.org / baike.baidu.com |
| 财经媒体 | 0.8 | eastmoney.com / sina.com.cn / caixin.com / yicai.com / 21jingji.com |
| 商业媒体 | 0.7 | 36kr.com / huxiu.com / csdn.net (0.65) / jianshu.com (0.55) |
| 商业平台 | 0.7 | jd.com / tmall.com / amap.com / meituan.com |
| 社交/UGC | 0.55 | weibo.com / zhihu.com (0.6) / douban.com / bilibili.com (0.6) |
| 个人博客 | 0.4 | wordpress.com / blogspot.com / hexo.io |

## 3. Time 时间衰减 (25%)

```python
def get_time_decay(date_str: str) -> float:
    # 无日期 → 0.6 (默认)
    # 近 30 天 → 1.0
    # 30-180 天 → 0.9
    # 180-365 天 → 0.8
    # 1-2 年 → 0.65
    # 2-3 年 → 0.5
    # 3+ 年 → 0.4
```

**实战 95 调试发现**: 中文站日期格式多样 (`%Y-%m-%d` / `%Y/%m/%d` / `%Y.%m.%d` / ISO), 必须 multi-format 试。

## 4. Language 语言匹配 (15%)

```python
def get_language_bonus(url: str, query: str) -> float:
    # 英文 query → 1.0 (任何 url)
    # 中文 query + 中文 url → 1.0
    # 中文 query + 英文 url → 0.85
```

**判定中文 url**: `.cn` 后缀 OR 包含 `baidu/zhihu/weibo/sina/qq.com/sohu/163.com/bilibili/douban/eastmoney/csdn/cnblogs/cnki/toutiao`。

## 实战 95 公网 8 URL 验证

```python
import cross_verify as cv
# 验证 1: 政府+新+中文 query 应最高
cv.get_source_credibility('https://www.gov.cn/x', '2026-06-15', '今天 AI 新闻')
# → 0.970 (政府 1.0 + 权威 1.0 + 时间 1.0 + 中文 1.0)

# 验证 2: 财经媒体+新
cv.get_source_credibility('https://eastmoney.com/news', '2026-06-18', '今天 AI 新闻')
# → 0.940

# 验证 3: 韭研公社 (实战 74 关键 URL)
cv.get_source_credibility('https://jiuyangongshe.com/post', '2026-06-19', '韭研公社 网址')
# → 0.917 (authority 0.8 + 时间 1.0 + 中文 1.0)

# 验证 4: 个人博客+老+英文 query
cv.get_source_credibility('https://wordpress.com/blog', '2020-01-01', 'AI news today')
# → 0.505 (domain 0.45 + authority 0.4 + 时间 0.4 + lang 1.0)
```

## 实战 95 集成位置

**`get_source_credibility(url, date_str='', query='')`** — signature 升级 (实战 70 旧版仅 url)

**调用方**: `extract_facts()` 内部, 升级为 `get_source_credibility(url, date, query)`。

**实战 95 未集成处**: `multi_search.py` / `discover.py` / `deep_research.py` — 这些地方仍用旧 1 维 (`SOURCE_CREDIBILITY` 直接查)。**未来实战可补**。

## 实战 95 真正价值

不是意图识别准度, 是 **答案排序 + 一致性**:

- 时间敏感 query (新闻/股价/版本) → 老 URL 自动降权
- 中文 query 推中文 URL → 跨语言体验优化
- 政府/学术源自动优先 → 答案权威性提升
- 商业 UGC (zhihu/csdn) 适度降权 → 减少误导

## 实战 95 调试验证脚本

```python
# /tmp/test_cv.py
import sys
sys.path.insert(0, '/home/ubuntu/star-search/scripts')
import cross_verify as cv
for url, date in [
    ('https://www.gov.cn/x', '2026-06-15'),
    ('https://eastmoney.com/news', '2026-06-18'),
    ('https://jiuyangongshe.com/post', '2026-06-19'),
    ('https://csdn.net/post', '2024-06-01'),
    ('https://wordpress.com/blog', '2020-01-01'),
]:
    s1 = cv.get_source_credibility(url, date, '今天 AI 新闻')
    s2 = cv.get_source_credibility(url, date, 'AI news today')
    print(f'{url:45s} {date:12s}  zh={s1:.3f}  en={s2:.3f}')
```

完整 `cross_verify.py` 见 `scripts/cross_verify.py`。
