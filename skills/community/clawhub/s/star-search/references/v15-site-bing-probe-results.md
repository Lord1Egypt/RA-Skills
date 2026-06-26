# v15.1 site:bing 代理引擎 — 27 域实测数据

**测试时间**: 2026-06-01
**解析器**: v15 `_parse_bing_cn`（bs4 select `li.b_algo > h2 a`）
**判定**: target ≥ 1 条 = 有效

## 有效引擎（10 个 site: 代理全部采纳）

| alias | site | 测试 query | 目标域 hits | 备注 |
|-------|------|-----------|-----------|------|
| toutiao | toutiao.com | 华为鸿蒙 PC | 2+ | v15 |
| zhihu | zhihu.com | Python asyncio 教程 | 1+ | v15 |
| weixin | mp.weixin.qq.com | DeepSeek V4 | 3+ | v15，URL 走 weixin.sogou.com |
| csdn | csdn.net | asyncio 教程 | 1 | v15.1 |
| cnblogs | cnblogs.com | asyncio 教程 | 1 | v15.1 |
| eastmoney | eastmoney.com | A股 政策 | 1 | v15.1 |
| cls | cls.cn | 财经早知道 | 1 | v15.1（query 要"财经"才命中） |
| tencent_cloud | cloud.tencent.com | asyncio 教程 | 1 | v15.1 |
| sina_finance | finance.sina.com.cn | A股 政策 | 1 | v15.1 |
| sohu | sohu.com | 鸿蒙 PC | 1 | v15.1 |

## 无效引擎（20 个，不予采纳）

juejin / ithome / 36kr / sspai / infoq / oschina / huxiu / smzdm / zol / xueqiu / wallstreetcn / douban / jianshu / segmentfault / netease / qq / ifeng / chinanews / people / xinhuanet — 全部 raw=10 但 target=0。

## 关键发现

1. **Bing 索引对中文站点覆盖率极不均匀** — 27 域中仅 10 域能拿到目标域真实结果
2. **官方/央媒（人民网/新华网/中新网）竟然索引不到** — news/policy 模式建议继续用搜狗/微信/百度 Playwright 引擎兜底
3. **反爬严的站（雪球/华尔街见闻/36kr/虎嗅）一致 0 命中** — site:bing 无法绕过反爬
4. **cls query 关键词敏感** — "央行 降息" 0 命中但 "财经早知道" 1 命中
5. **zhihu 实测有效**（"一份详细的asyncio入门教程" zhuanlan.zhihu.com）

## 探测脚本（re-runnable）

```python
import urllib.request, urllib.parse, ssl, re
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0'

def hits_count(q, site):
    url = f"https://cn.bing.com/search?q=site%3A{site}+{urllib.parse.quote(q)}&count=15&setlang=zh-cn"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://cn.bing.com/"})
    body = urllib.request.urlopen(req, timeout=8, context=ctx).read().decode('utf-8', errors='ignore')
    count = 0
    for m in re.finditer(r'<li class="b_algo[^"]*">(.*?)</li>', body, re.DOTALL):
        a = re.search(r'<a[^>]+href="(https?://[^"]+)"', m.group(1))
        if a and site in a.group(1): count += 1
    return count
```

## 后续建议

- **新引擎发现流程**：用本脚本批量测 → 只采纳 target ≥ 1
- **不要相信直觉**："人民网应该能搜到吧" — 实测 0 命中。用数据说话
- **每域用 2-3 个 query 验证稳定性**
- **可以每季度重新探测**（Bing 索引会变）
