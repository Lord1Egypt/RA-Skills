# star-search v16.x / v17.x 旧版归档

> 完整 v16-v17 章节已从主 SKILL.md 移到本文件。star-search 当前版本 v20.6.0。

---

# Star Search v16.2.2 — 16 引擎 + 智能识别 (财经) + 公网 HTTPS + 前端 + 守护进程

**一个脚本替代百度搜索 API，免费、多引擎、高质量、可服务 subagent。**

> 重要：本 skill 已从 v8.3 (Camofox) 演进到 v16.2.2 (HTTP+Playwright hybrid + 智能路由 + 公网)。Camofox 路径已彻底废弃，HTTP 引擎占 11/16。GitHub: https://github.com/muchenhengxin/Star @ commit 23550b8 (v16.2.1)。**公网**：https://search.token-star.cn （HSTS+LE证书+nginx 反代 5000 端口）

---

## 🔥 v16.2.2 关键升级

| 升级 | 价值 | 触发场景 |
|------|------|----------|
| **智能识别 (smart routing)** | 财经 query 自动走 finance 引擎 (eastmoney/cls/sina_finance)，不用 mode=finance | "今天股市情况" / "上证指数" / "比亚迪股价" |
| **公网 HTTPS 部署** | `https://search.token-star.cn` 全 5 端点可调 | subagent / 外部脚本 |
| **前端文人风 (v16.2.1)** | Star-Search logo (SVG 星 + 品牌字) + 知/思/答 + 博观约取 | 浏览器直接搜索 |
| **守护进程 (脱离 systemd session)** | setsid + nohup + 父进程=init，systemd 杀不掉 | systemd user 单元被 logind SIGTERM 杀 |
| **Playwright 优雅降级** | 无 sudo 也能跑，缺 libatk 自动跳过 4 引擎 | 共享服务器/无 root |

### 智能识别 — query 自动路由（v16.2.2 关键修复）

**问题**：用户搜"今天股市情况" 走 deep mode → Bing CN 理解"今天"为"今日黄历" → 返回 8 条黄历，没一条股票。

**根因**（2026-06-03 实战发现 4 个隐藏 bug）：
1. **`MODES['stock']` 命名误导** — 实际是 `['sogou', 'baidu', 'weixin', 'bing_cn']`（news-like），不是真财经引擎
2. **真财经引擎在 `MODES['finance']`** — `['eastmoney', 'cls', 'sina_finance', 'rss_woshipm', 'rss_36kr']`
3. **`api_server.py` 没传 `force_refresh` 到 `search_async`** — 测试时缓存命中，看不到新结果，误以为修复没生效
4. **`else` 分支覆盖 `engines` 变量** — `if engine / elif mode / else` 三分支里，smart 触发的 engines 被 else 的语言感知路由覆盖

**修法**（已 ship 到 v16.2.2 search.py:921-955）：
```python
# v16.2.2: 智能识别 — query 含财经词自动用 finance 引擎 (优先于 mode)
engines = CN_ENGINES  # 默认 fallback
if not engine and not sources:
    stock_kw = ('股票','股价','股市','A股','a股','大盘','上证','深证','沪深',
                '港股','美股','纳斯达克','道琼斯','标普','基金','行情','涨停',
                '跌停','个股','板块','开盘','收盘','指数','成份股','龙虎榜',
                'ETF','etf','基金净值','今天股票','今天股市')
    if any(kw in query for kw in stock_kw):
        engines = MODES.get('finance', CN_ENGINES)
        _used_smart = True
    else:
        _used_smart = False

# 引擎确定 - 三分支都检查 _used_smart
if engine:
    engines = [engine]
elif not _used_smart and mode:
    engines = MODES.get(mode, MODES['deep'])
elif not _used_smart and not mode:
    if _has_chinese(query):
        engines = CN_ENGINES
    else:
        engines = GLOBAL_ENGINES_EN
# else: _used_smart=True, engines 已在上面设置好, 保留
```

**实测**（2026-06-03）：
| Query | 修前 | 修后 |
|-------|------|------|
| `今天股市情况` | 8 条黄历 | 5 条 RSS 财经 + 1 东方电缆增资 |
| `上证指数 今日 收盘` | 8 条黄历 | **上证指数 4057.74 (-0.27%)** 实时 |
| `比亚迪股价` | 8 条黄历 | **比亚迪 96.76 (3.32%)** 实时 |
| `Python 教程` | 正常 | 正常（未误触）|

**3 个隐藏 bug 调试方法**：加临时 `print(f'[DEBUG] engines={engines}')` → `force_refresh=True` 绕缓存 → 看 daemon log 里的 `[smart→finance]` 标记。

### 公网 HTTPS + 前端 (v16.2.1)

**架构**：
```
[Browser] → https://search.token-star.cn:443
    ↓ (nginx + LE cert)
[static /var/www/star-search/index.html]  ← 前端文人风
    ↓ (location /v1/)
[FastAPI 127.0.0.1:<api-port>]  ← api_server.py (守护进程)
    ↓
[search.py 16 引擎]
```

**前端页面**（`index.html`，12768 bytes）：
- **首页**：✦ SVG 渐变星 + "Star-Search" 品牌字 + "知你所问 · 思你所疑 · 答你所想" + 输入框 + "博观约取" 字间距印章感落款
- **结果页**：Star-Search logo + 返回 + 搜索框 + 结果列表 + 博观约取落款
- **底栏**："16 引擎 · OpenAI 兼容 · 跨源验证" 技术规格

**nginx 关键配置**（`/etc/nginx/sites-enabled/search-token-star.conf`）：
```nginx
server {
    server_name search.token-star.cn;
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/search.token-star.cn/fullchain.pem;

    location /v1/ {
        proxy_pass http://127.0.0.1:<api-port>;
        proxy_set_header Host $host;
        proxy_read_timeout 60s;
        proxy_http_version 1.1;
    }
    location / {
        root /var/www/star-search;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

### 守护进程（脱离 systemd session）

**问题**：systemd user 单元（`stardust-svc.service`）在用户 session 闲置或 logind idle action 时**会被 SIGTERM 杀**。表现为 `systemctl --user status` 显示 active running，但 `ss -tlnp | grep 5000` 看不到端口 — 进程被 SIGTERM 还没重启完，公网 502。

**修法**（已 ship 到 v16.2.1 `/tmp/start_daemon.sh`）：
```bash
#!/bin/bash
cd /home/ubuntu/star-search/scripts
exec /usr/bin/python3 api_server.py --port 5000 \
  >> /home/ubuntu/star-search/logs/daemon.log 2>&1
```
启动方式：
```bash
nohup setsid /tmp/start_daemon.sh </dev/null >>/home/ubuntu/star-search/logs/wrap.log 2>&1 &
disown
```
- `setsid` 创建新 session
- `nohup` 忽略 SIGHUP
- `</dev/null` stdin 也脱离
- `disown` 从当前 shell job table 移除
- 父进程变成 `1` (init)，systemd 杀不掉

**验证**：`ps -ef | grep api_server` 看 PPID 列 = 1 = 永驻。

**nginx 502 定位步骤**：
1. `curl -s --max-time 3 http://127.0.0.1:<api-port>/v1/health` — 内网 200？
2. 内网 200 但公网 502 — nginx `error.log` 看 `connect() failed (111: Connection refused)` — upstream 端口没在 LISTEN
3. 原因：systemd unit 在 restart，端口空 1-2 秒，请求撞上
4. **修法**：换守护进程方式

---

## Star Search v15.0 — 10 引擎直搜 + 定时增量 + OpenAI API + 智能缓存 + 智能去重

**一个脚本替代百度搜索 API，免费、多引擎、高质量、可服务 subagent。**

> 重要：本 skill 已从 v8.3 (Camofox) 演进到 v15 (HTTP+Playwright hybrid)。Camofox 路径已彻底废弃，HTTP 引擎占 7/11。GitHub: https://github.com/muchenhengxin/Star @ commit 4cfd83f。

> 重要：本 skill 已从 v8.3 (Camofox) 演进到 v16.2.2 (HTTP+Playwright hybrid + 智能路由 + 公网)。Camofox 路径已彻底废弃，HTTP 引擎占 11/16。GitHub: https://github.com/muchenhengxin/Star @ commit 23550b8 (v16.2.1)。**公网**：https://search.token-star.cn （HSTS+LE证书+nginx 反代 5000 端口）

---

## 🔥 v16.2.2 关键升级

| 升级 | 价值 | 触发场景 |
|------|------|----------|
| **智能识别 (smart routing)** | 财经 query 自动走 finance 引擎 (eastmoney/cls/sina_finance)，不用 mode=finance | "今天股市情况" / "上证指数" / "比亚迪股价" |
| **公网 HTTPS 部署** | `https://search.token-star.cn` 全 5 端点可调 | subagent / 外部脚本 |
| **前端文人风 (v16.2.1)** | Star-Search logo (SVG 星 + 品牌字) + 知/思/答 + 博观约取 | 浏览器直接搜索 |
| **守护进程 (脱离 systemd session)** | setsid + nohup + 父进程=init，systemd 杀不掉 | systemd user 单元被 logind SIGTERM 杀 |
| **Playwright 优雅降级** | 无 sudo 也能跑，缺 libatk 自动跳过 4 引擎 | 共享服务器/无 root |

### 智能识别 — query 自动路由（v16.2.2 关键修复）

**问题**：用户搜"今天股市情况" 走 deep mode → Bing CN 理解"今天"为"今日黄历" → 返回 8 条黄历，没一条股票。

**根因**（今天实战发现 3 个隐藏 bug）：
1. **`MODES['stock']` 命名误导** — 实际是 `['sogou', 'baidu', 'weixin', 'bing_cn']`（news-like），不是真财经引擎
2. **真财经引擎在 `MODES['finance']`** — `['eastmoney', 'cls', 'sina_finance', 'rss_woshipm', 'rss_36kr']`
3. **`api_server.py` 没传 `force_refresh` 到 `search_async`** — 测试时缓存命中，看不到新结果，误以为修复没生效
4. **`else` 分支覆盖 `engines` 变量** — `if engine / elif mode / else` 三分支里，smart 触发的 engines 被 else 的语言感知路由覆盖

**修法**（已 ship 到 v16.2.2 search.py:921-955）：
```python
# v16.2.2: 智能识别 — query 含财经词自动用 finance 引擎 (优先于 mode)
engines = CN_ENGINES  # 默认 fallback
if not engine and not sources:
    stock_kw = ('股票','股价','股市','A股','a股','大盘','上证','深证','沪深',
                '港股','美股','纳斯达克','道琼斯','标普','基金','行情','涨停',
                '跌停','个股','板块','开盘','收盘','指数','成份股','龙虎榜',
                'ETF','etf','基金净值','今天股票','今天股市')
    if any(kw in query for kw in stock_kw):
        engines = MODES.get('finance', CN_ENGINES)
        _used_smart = True
    else:
        _used_smart = False

# 引擎确定 - 三分支都检查 _used_smart
if engine:
    engines = [engine]
elif not _used_smart and mode:
    engines = MODES.get(mode, MODES['deep'])
elif not _used_smart and not mode:
    if _has_chinese(query):
        engines = CN_ENGINES
    else:
        engines = GLOBAL_ENGINES_EN
# else: _used_smart=True, engines 已在上面设置好, 保留
```

**实测**：
| Query | 修前 | 修后 |
|-------|------|------|
| `今天股市情况` | 8 条黄历 | 5 条 RSS 财经 + 1 东方电缆增资 |
| `上证指数 今日 收盘` | 8 条黄历 | **上证指数 4057.74 (-0.27%)** 实时 |
| `比亚迪股价` | 8 条黄历 | **比亚迪 96.76 (3.32%)** 实时 |
| `Python 教程` | 正常 | 正常（未误触）|

**3 个隐藏 bug 调试方法**：加临时 `print(f'[DEBUG] engines={engines}')` → `force_refresh=True` 绕缓存 → 看 daemon log 里的 `[smart→finance]` 标记。

### 公网 HTTPS + 前端 (v16.2.1)

**架构**：
```
[Browser] → https://search.token-star.cn:443
    ↓ (nginx + LE cert)
[static /var/www/star-search/index.html]  ← 前端文人风
    ↓ (location /v1/)
[FastAPI 127.0.0.1:<api-port>]  ← api_server.py (守护进程)
    ↓
[search.py 16 引擎]
```

**前端页面**（`index.html`，12768 bytes）：
- **首页**：✦ SVG 渐变星 + "Star-Search" 品牌字 + "知你所问 · 思你所疑 · 答你所想" + 输入框 + "博观约取" 字间距印章感落款
- **结果页**：Star-Search logo + 返回 + 搜索框 + 结果列表 + 博观约取落款
- **底栏**："16 引擎 · OpenAI 兼容 · 跨源验证" 技术规格

**nginx 关键配置**（`/etc/nginx/sites-enabled/search-token-star.conf`）：
```nginx
server {
    server_name search.token-star.cn;
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/search.token-star.cn/fullchain.pem;

    location /v1/ {
        proxy_pass http://127.0.0.1:<api-port>;
        proxy_set_header Host $host;
        proxy_read_timeout 60s;
        proxy_http_version 1.1;
    }
    location / {
        root /var/www/star-search;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

### 守护进程（脱离 systemd session）

**问题**：systemd user 单元（`stardust-svc.service`）在用户 session 闲置或 logind idle action 时**会被 SIGTERM 杀**。表现为 `systemctl --user status` 显示 active running，但 `ss -tlnp | grep 5000` 看不到端口 — 进程被 SIGTERM 还没重启完，公网 502。

**修法**（已 ship 到 v16.2.1 `/tmp/start_daemon.sh`）：
```bash
#!/bin/bash
cd /home/ubuntu/star-search/scripts
exec /usr/bin/python3 api_server.py --port 5000 \
  >> /home/ubuntu/star-search/logs/daemon.log 2>&1
```
启动方式：
```bash
nohup setsid /tmp/start_daemon.sh </dev/null >>/home/ubuntu/star-search/logs/wrap.log 2>&1 &
disown
```
- `setsid` 创建新 session
- `nohup` 忽略 SIGHUP
- `</dev/null` stdin 也脱离
- `disown` 从当前 shell job table 移除
- 父进程变成 `1` (init)，systemd 杀不掉

**验证**：`ps -ef | grep api_server` 看 PPID 列 = 1 = 永驻。

**nginx 502 定位步骤**：
1. `curl -s --max-time 3 http://127.0.0.1:<api-port>/v1/health` — 内网 200？
2. 内网 200 但公网 502 — nginx `error.log` 看 `connect() failed (111: Connection refused)` — upstream 端口没在 LISTEN
3. 原因：systemd unit 在 restart，端口空 1-2 秒，请求撞上
4. **修法**：换守护进程方式

---

## 🔥 核心能力（v16 旗舰版）

### 5 维指标 vs 百度搜索 API

| 维度 | v16.2.2 表现 | 与百度搜索工具对比 |
|:----|:---------|:----------------|
| **全面性** | 20-40条/次（16 引擎聚合） | ✅ 超过（百度 20条/次） |
| **准确性** | 100% 摘要（平均 90字） | ✅ 超过（百度 50字） |
| **时效性** | 60-100% 有日期 📅 | ✅ 超过 |
| **稳定性** | 16 引擎互为 fallback | ✅ 超过（单点） |
| **速度** | quick 0.5-1s / deep 2-5s / API 1-6s | ✅ 持平/略胜 |
| **成本** | **完全免费** | ✅ 替代 |
| **真实 URL** | Bing CN / 头条 / 知乎 / GitHub 直链 100% | ✅ 超过（跳转链 90%） |
| **智能识别** | 财经 query 自动转 finance | ✅ 独有 |
| **API 暴露** | OpenAI-compatible + 公网 HTTPS + cron 客户端 | ✅ 独有 |
| **智能缓存** | 分桶 TTL + query 归一化 + 桶复用 | ✅ 独有 |

### 16 引擎清单

| 引擎 | 类型 | 权重 | URL 类型 | 备注 |
|------|------|------|----------|------|
| **Bing CN** | HTTP (aiohttp) | 85 | 真实直链 | 中文搜索主力，新华网/知乎/东方财富 |
| **GitHub Issues** | HTTP (aiohttp) | 80 | 真实直链 | 开发者向，issue 级讨论，过滤 bot/PR |
| **toutiao** | HTTP (site:bing) | 75 | 真实直链 | v15 头条，100% toutiao.com |
| **zhihu** | HTTP (site:bing) | 75 | 真实直链 | v15 知乎，100% zhihu.com |
| **weixin_bing** | HTTP (site:bing) | 85 | 跳转链接 | v15 微信公众号 |
| **csdn** | HTTP (site:bing) | 70 | 跳转链接 | v15.1 CSDN 技术博客 |
| **cnblogs** | HTTP (site:bing) | 70 | 跳转链接 | v15.1 博客园 |
| **eastmoney** | HTTP (site:bing) | 90 | 真实直链 | **v15.1 东方财富（财经专用）** |
| **cls** | HTTP (site:bing) | 90 | 真实直链 | **v15.1 财联社（财经快讯）** |
| **sina_finance** | HTTP (site:bing) | 90 | 真实直链 | **v15.1 新浪财经** |
| **sohu / tencent_cloud** | HTTP (site:bing) | 60/80 | 跳转链接 | v15.1 综合/腾讯云 |
| **5 RSS 引擎** | HTTP (RSS) | 70 | 真实直链 | **v16.1** rss_ithome/rss_36kr/rss_sspai/rss_oschina/rss_woshipm |
| **搜狗 HTTP** | HTTP (aiohttp) | 95 | 跳转链接 | <1秒 |
| 搜狗 (Playwright) | Playwright | 100 | 跳转链接 | v16.2 graceful skip (无 sudo) |
| 百度 | Playwright | 80 | 跳转链接 | v16.2 graceful skip |
| 360 | Playwright | 60 | 跳转链接 | v16.2 graceful skip |
| weixin_pw | Playwright | 85 | 跳转链接 | v16.2 graceful skip |
| Bing HTTP | HTTP (aiohttp) | 70 | 真实直链 | 国际版（global 模式） |

### 11 模式清单

| 模式 | 引擎 | 适用 |
|------|------|------|
| **deep**（默认） | CN_ENGINES = 搜狗HTTP+百度+360+搜狗PW+微信PW+Bing CN | 综合研究 |
| **quick** | 搜狗HTTP | 快速验证 |
| **news** | 搜狗+百度+微信+bing_cn | 新闻追踪 |
| **policy** | 百度+搜狗+bing_cn | 政策研究 |
| **stock** | 搜狗+百度+微信+bing_cn（**注意：实际是 news-like，不是财经**） | (留作兼容) |
| **dev** | 搜狗+百度+github+bing_cn | 开发者向 |
| **global** | 中文→bing_cn+bing_http；英文→bing_http | 英文/国际 |
| **finance** | **eastmoney+cls+sina_finance+rss_woshipm+rss_36kr** | 财经/股票（真财经） |
| **dev_rss** | dev+5 RSS | 开发者向完整 |
| **tech_news** | cnblogs+csdn+5 RSS | 技术新闻 |
| **weixin_agg** | 微信(双源)+搜狗+cls+woshipm | 微信公众号聚合 |
| **auto** | 智能识别：财经→finance；中文→deep；英文→global | v16.2.2 默认 |

### 关键升级时间线

| 版本 | 升级 | 价值 |
|------|------|------|
| **v16.2.2** | 智能识别 (财经 query→finance) | 修"今天股市情况"返回黄历 bug |
| **v16.2.1** | 公网 HTTPS + 前端 + 守护进程 | 给 LLM agent 当事实层 |
| **v16.2** | Playwright 优雅降级 (search.py 953-988) | 无 sudo 服务器也能跑 |
| **v16.1** | 5 RSS 引擎 + global 中英双源 + finance 模式 | 时效新闻 + 真财经 |
| **v16** | sogou KeyError 修复 + 质量标识 🌟🌟🌟 + --explain | 可解释性 |
| **v15.1** | +7 引擎 (csdn/cnblogs/eastmoney/cls/tencent_cloud/sina_finance/sohu) | 垂类覆盖 |
| **v15** | 3 site:bing 直搜 (toutiao/zhihu/weixin) | 免反爬 <1秒 |
| **v14** | OpenAI API + 增量追加 | subagent 友好 |
| **v13** | 智能缓存 (分桶 TTL) | 节省 78% 时间 |
| **v12.2** | 智能去重 + ⭐ 跨源标记 | 合并转载 |

---

## 🚀 快速使用

### CLI 模式

```bash
python3 search.py "AI大模型"                                # 中文→deep
python3 search.py "asyncio vs threading"                     # 英文→global
python3 search.py "FastAPI 异常处理" --mode dev             # 开发者向（GitHub Issues）
python3 search.py "华为鸿蒙" --engine toutiao                # v15: 头条
python3 search.py "Python asyncio" --engine zhihu            # v15: 知乎
python3 search.py "DeepSeek V4" --engine weixin              # v15: 微信公众号
python3 search.py "今天股市情况"                              # v16.2.2: 智能识别自动走 finance
python3 search.py "上证指数" --mode finance --recency=day    # 显式 finance 模式
python3 search.py "华为鸿蒙" --mode deep --recency=week      # deep + 时效
python3 search.py "Python教程" --exact                       # 精确匹配
python3 search.py "阿里巴巴" --sources="weixin,baidu"
python3 search.py --list                                    # 列引擎/模式
```

### API 模式（公网 + 本地）

```bash
# 公网 (推荐 subagent)
curl -X POST https://search.token-star.cn/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"比亚迪股价","top":5}'

# 本地 (开发/调试)
python3 scripts/api_server.py --port 9800
curl -X POST http://127.0.0.1:9800/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"FastAPI 异常处理","mode":"dev","top":5}'

# 增量追加 (1.2s)
curl -X POST https://search.token-star.cn/v1/search/refresh \
  -H "Content-Type: application/json" \
  -d '{"query":"FastAPI 异常处理","force_refresh":true}'

# Python 客户端
import httpx
r = httpx.post('https://search.token-star.cn/v1/search', json={
    'query': '华为鸿蒙', 'mode': 'dev', 'top': 5
}).json()
for item in r['results']:
    print(f"{item['score']:5.1f}  {item['title']}")
```

### 5 端点参考

| 端点 | 用途 | 耗时 |
|------|------|------|
| `POST /v1/search` | 主搜索（带缓存） | 0.1-5.5s |
| `POST /v1/search/refresh` | 增量追加（强制刷新+合并） | 1-2s |
| `GET /v1/health` | 健康检查 | <10ms |
| `GET /v1/modes` | 列出模式 | <10ms |
| `GET /v1/engines` | 列出引擎 | <10ms |

---

## ⚙️ 关键参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--mode` | auto | 搜索模式（v16.2.2: 财经 query 自动转 finance） |
| `--engine` | 自动 | 单引擎指定 |
| `--top` | 10 | 输出数量（最大 30） |
| `--recency` | 无 | day/week/month/year |
| `--exact` | False | 精确匹配 |
| `--sources` | 无 | 限定来源（weixin,baidu,...） |
| `--json` | False | JSON 输出（管道用） |
| `--list` | False | 列引擎/模式 |
| `--force-refresh` | False | API 强制刷新（绕缓存） |

### 5+ API 字段（result 字典）

| 字段 | 说明 |
|------|------|
| `score` | 综合评分（含引擎权重、cross_verified 加成） |
| `cross_verified` | 被几个引擎收录（≥2 时显示 ⭐） |
| `cluster_size` | 同事件合并数 |
| `topic_key` | 主题词 key（停用词过滤后前 10 字符） |
| `source_count` | 跨源数 |
| `source_engines` | 跨源引擎列表 |
| `cluster_id` | 同事件 ID |
| `refresh` | 是否为 force_refresh 拉取的新结果 |
| `category` | 自动分类（📰新闻/💬问答/💻代码/📖百科/🔗网页/✍️博客） |

---

## 🔌 依赖

```bash
pip install aiohttp beautifulsoup4 lxml playwright fastapi uvicorn 'pydantic>=2' httpx
playwright install chromium
```

**无需 API Key、无需登录、无需付费。**

---

## ⚠️ 已知限制与陷阱

1. **site:bing 代理**：Bing site: 实际返回是 Bing 索引结果，**不一定是 100% 目标站最新文章**——必须在解析后过滤 `if target_site in r['url']`，否则 engine 标签会撒谎
2. **GitHub Issues bot 过滤**：必须用 `language:zh + archived:false`，否则 Renovate/Dependabot 占结果 80%+
3. **Playwright 引擎并发**：单次 `_search_pw` 内部 new_page() 偶发 context 关闭，**v14 fix**: `try/except` 包 new_page，context 必须 cleanup
4. **query 归一化 key**：用 `re.sub(r'[^\w\s]', '', query.lower().strip())`，**不要做全角半角转换**（反而破坏中文语义）
5. **分桶 TTL**：news/policy/stock 5分钟（时效敏感），dev/global 1小时（结果稳定）
6. **桶复用**：缓存永远存 `max(请求num, 20)` 条，num=5 调完 num=10 直接切片返回
7. **force_refresh 合并**：新结果标 `refresh=true`，历史（不在新结果里）标 `refresh=false`，按 URL 去重
8. **【v16.2 关键】Playwright 浏览器启动失败必须 try/except**（无 sudo 服务器，缺 libatk 必然触发）— 详见 `devops/playwright-server-deployment` skill 第 3.1 节。**3 个易错点**：(1) `browser = None; ctx = None` 必须在 try 块前初始化；(2) `if pw_engines and ctx is not None:` 而非 `if pw_engines:`；(3) `pw_engines = []` 在 except 内。
9. **【v16.2.1 关键】systemd user 单元会被 logind SIGTERM 杀** — 用 `nohup setsid` + `disown` 让父进程=init 才稳。
10. **【v16.2.2 关键】命名误导 `MODES['stock']` 实际是 news-like** — 财经 query 必须用 `MODES['finance']`（eastmoney/cls/sina_finance）。不要看名字想当然。

---

## 📁 文件结构

```
star-search/
├── search.py                    # 主程序（v16.2.2，~1100 行）
├── SKILL.md                     # 本文件
├── index.html                   # v16.2.1 前端文人风
├── README.md                    # GitHub 仓库 README
├── scripts/
│   ├── api_server.py            # v14 FastAPI 5 endpoints
│   ├── cron_refresh.py          # v15 定时增量客户端
│   ├── stealth.js               # Playwright 反检测
│   └── deploy_web.sh            # v16.2.1 nginx 部署
├── /tmp/start_daemon.sh         # v16.2.1 守护进程启动器
├── /var/www/star-search/        # v16.2.1 nginx 静态目录
└── references/
    ├── site-bing-proxy-pattern.md       # v15 site:bing 代理模式
    ├── incremental-cache-pattern.md     # v13 智能缓存+增量模式
    ├── v16-finance-mode-and-smart-routing.md    # v16.2.2 新
    └── v16-public-deployment-and-daemon.md      # v16.2.1 新
```

---

## 🔄 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| **16.2.2** | 2026-06-03 | **智能识别**：财经 query 自动转 finance mode；修 api_server 没传 force_refresh + else 分支覆盖 engines 3 个隐藏 bug |
| **16.2.1** | 2026-06-03 | **公网 HTTPS (search.token-star.cn) + 前端文人风 + 守护进程** (脱离 systemd session) |
| **16.2** | 2026-06-03 | **Playwright 优雅降级** (无 sudo 也能跑)：libatk 缺自动 skip 4 引擎 |
| **16.1** | 2026-06-02 | **+5 RSS 引擎** (ithome/36kr/sspai/oschina/woshipm) + global mode 中英双源 + finance mode |
| **16.0** | 2026-06-02 | sogou KeyError 修复 + 质量标识 🌟🌟🌟 + --explain 评分透明 |
| **15.1** | 2026-06-01 | +7 site:bing 代理引擎 (csdn/cnblogs/eastmoney/cls/tencent_cloud/sina_finance/sohu) |
| **15.0** | 2026-06-01 | 10 引擎直搜 + 定时增量：toutiao/zhihu/weixin 3 个 site:bing 代理 + cron_refresh.py 客户端 |
| **14.0** | 2026-06-01 | OpenAI API + 增量追加：FastAPI 5 endpoints + force_refresh |
| **13.0** | 2026-06-01 | 智能缓存层：分桶 TTL + query 归一化 + 桶复用 |
| **12.2** | 2026-06-01 | 智能去重 + 跨源聚合：主题词 key + Jaccard 双策略，⭐ 标记 |
| **12.1** | 2026-06-01 | GitHub Issues 引擎 + dev 模式 |
| 11.2 | 2026-05-28 | 搜狗 HTTP 模式（aiohttp，<1秒） |
| 11.1 | 2026-05-25 | Bing CN HTTP 引擎（真实直链） |
| 10.x | 2026-05-15 | Playwright + 搜狗/百度/360 多引擎 |
| 8.3 | 2026-05-10 | 旗舰版（Camofox 时代，已废弃） |

---

## 📝 使用建议

| 场景 | 推荐方式 |
|------|----------|
| 日常信息收集 | `--mode deep`（默认） |
| 验证事实 | `--mode quick` |
| 政策/法规 | `--mode policy --recency=month` |
| 最新动态 | `--mode news` |
| **股票/财经** | 不需要 mode！直接搜 "今天股市情况" / "比亚迪股价"，v16.2.2 自动走 finance |
| 财经显式模式 | `--mode finance`（eastmoney+cls+sina_finance+rss_woshipm+rss_36kr）|
| 开发者向 | `--mode dev`（自动含 GitHub Issues） |
| 子代理调用 | API 模式 + `/v1/search/refresh` 增量 |
| subagent 监控 | `cron_refresh.py --loop 1800` + cron job |
| 头条/知乎/微信 | `--engine toutiao/zhihu/weixin` |
| 浏览器直接搜索 | https://search.token-star.cn (前端) |

---

## ⚠️ 重要：本地部署注意

**本 skill 在 `~/.hermes/skills/research/star-search/` 是源码位置**（v16.2.2 实际工程），而 `~/.hermes/skills/openclaw-imports/star-search/SKILL.md` 是元数据/入口。如果源目录消失（如意外清理），从 GitHub clone 重建：
```bash
cd /tmp && git clone https://github.com/muchenhengxin/Star.git
cp -r Star/* ~/.hermes/skills/research/star-search/
```

> **下一步**：发布到 ClawHub v16.2.2；继续优化智能识别（垂类 mode chip 前端入口）。

---

# 🔥 v17.0.0 — MCP 化 (Model Context Protocol)

**重磅升级**: star-search 现在是一个 **标准 MCP server** —— 任何 LLM agent (Claude Desktop / Cursor / Cline / Continue / Hermes) 都能直接 `web_search` / `web_search_news` / `web_search_finance` 当作工具调用。

**目标**：**免费中文版 Tavily**（Tavily 收费，star-search 免费 + 中文特化）。

## 4 个 MCP Tools

| Tool | 用途 | 引擎 |
|------|------|------|
| `web_search` | 通用搜索 (智能识别) | 默认 deep mode + 财经 query 自动 finance |
| `web_search_news` | 科技/AI/产品新闻 | csdn/cnblogs + 5 RSS (ithome/36kr/sspai/oschina/woshipm) |
| `web_search_finance` | 财经/股票/A股专属 | eastmoney/cls/sina_finance/sohu/baidu/weixin/bing_cn |
| `get_engines` | 列 16 引擎 + 5 模式 | 工具决策用 |

## 部署方式

### A. stdio (本地) — Claude Desktop / Hermes

`~/.config/claude_desktop_config.json` (macOS) 或 `%APPDATA%/Claude/claude_desktop_config.json` (Windows)：

```json
{
  "mcpServers": {
    "star-search": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "STAR_SEARCH_API": "http://127.0.0.1:<api-port>/v1/search"
      }
    }
  }
}
```

### B. HTTP/SSE (远程) — 任何 HTTP MCP client

公网 endpoint：
- **SSE**: `https://search.token-star.cn/mcp/sse`
- **POST**: `https://search.token-star.cn/mcp/messages?session_id=<从 SSE 推的 endpoint URL 拿>`
- **Health**: `https://search.token-star.cn/mcp/health`

```python
import aiohttp, json

# 1. SSE 握手
async with aiohttp.ClientSession() as s:
    async with s.get("https://search.token-star.cn/mcp/sse") as r:
        line = await r.content.readline()  # event: endpoint
        line = await r.content.readline()  # data: <URL>
        endpoint = line.decode().replace("data: ", "").strip()

    # 2. initialize
    req = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
           "params": {"protocolVersion": "2025-06-18"}}
    await s.post(endpoint.replace("http://", "https://").replace(":80", ""),
                 json=req)
    # ... 读 SSE 响应, 拿 session_id
    # 3. tools/call
    req = {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
           "params": {"name": "web_search",
                      "arguments": {"query": "比亚迪股价"}}}
    await s.post(messages_url, json=req)
```

## 启动服务器

```bash
# stdio (本地)
python3 mcp_server.py

# HTTP/SSE (公网, 端口 8765)
python3 mcp_server.py --transport http --port 8765
```

## 实测结果

| Tool | query | 耗时 | 结果 |
|------|-------|------|------|
| `web_search` | "比亚迪股价" | 0.85s | 7 条 0.85s（东方财富/新浪/雪球/同花顺/知乎）|
| `web_search_finance` | "上证指数今日收盘" | 0.87s | 8 条 0.87s（4074.74）|
| `web_search_news` | "AI 创业" | 0.28s | 8 条 IT之家科技新闻 |
| `get_engines` | - | 0s | 16 引擎清单 |

## 协议细节

- **JSON-RPC 2.0** over stdio (一行一个 JSON) 或 HTTP/SSE
- **protocolVersion**: 2025-06-18
- **零依赖**: 纯 stdlib + aiohttp (服务器已装)
- **HTTP 端点**: `/sse` (GET, 推送 endpoint) + `/messages?session_id=X` (POST) + `/health` (GET)
- **结果格式**: `{type: "text", text: "🔍 找到 8 条..."}` 友好格式化
- **错误处理**: HTTP 5xx / Timeout / Parse error 全部捕获, 返回 `{isError: true}` text

---

# 🚀 v17.2.0 — LLM 答案层 (Perplexity Mode)

**重磅升级**: star-search 不只返 8 条蓝链，**直接给 1 段 AI 总结答案 + 来源**（Perplexity AI 风格）。

## 核心特性

- **诚实答案** > 编造答案: LLM 看到 8 条搜索结果，**有具体数字才写**，**没数据就告诉用户查行情网站/官方源**
- **DeepSeek-V4-Flash** 总结（免费 via new-api <服务器IP>:<内部端口>）
- **2-3s** 生成答案
- **4-5 源** 末尾标出

## 3 种用法

### 1. 搜索接口加 `answer=true`

```bash
curl -X POST https://search.token-star.cn/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "比亚迪股价", "top": 8, "answer": true}'
```

返回:
```json
{
  "query": "比亚迪股价",
  "count": 8,
  "results": [...8 条蓝链...],
  "answer": {
    "answer": "比亚迪近期股价走势受多重消息影响...实时报价请查询东方财富...",
    "model": "DeepSeek-V4-Flash",
    "elapsed_ms": 2600,
    "tokens": 678,
    "sources": ["data.eastmoney.com", "tags.news.sina.com.cn", ...]
  }
}
```

### 2. 独立答案端点 `/v1/answer`

```bash
curl -X POST https://search.token-star.cn/v1/answer \
  -H "Content-Type: application/json" \
  -d '{"query": "今天有什么科技新闻", "results": [...8条结果...], "mode": "tech_news"}'
```

### 3. MCP tool 加 `answer: true`

```python
# Claude Desktop / Hermes agent
await mcp.call("web_search", query="比亚迪股价", answer=True)
```

## 答案风格

| Query 类型 | 答案行为 |
|---|---|
| 股价/财经 (有数据) | 直接报数字 + 来源 |
| 股价/财经 (无数据) | 告诉用户查东方财富/新浪财经/同花顺，**不编** |
| 指数/基金 | 找具体点位，没有就报"实时指数请查..." |
| 科技/产品 | 突出事实要点 + 数字 (参数/价格/发布日期) |
| 新闻/事件 | 谁/什么/什么时候 |
| 旧数据 | 标注"截至 YYYY-MM-DD"或"近期"，不冒充今日 |

## Prompt 核心（避免幻觉）

- ⚠️ 数字必须从源文 snippet 中能直接找到, 否则不写
- ⚠️ 如果搜索结果是新闻/资讯/公告, 不能编出具体价格数字
- ⚠️ 多个来源矛盾 → 列出分歧, 不强行统一
- ⚠️ 来源不够时建议查更权威的源 (官方/行情网站)

## 实测结果

| Query | 答案行为 | LLM 耗时 |
|---|---|---|
| "比亚迪股价" | "实时股价请查询东方财富/新浪财经..." | 2.6s |
| "比亚迪 5月汽车销量" | "未找到...建议查产销快报..." | 2.9s |
| "GPT-5 发布时间" | "OpenAI 尚未公布...以官方为准" | - |
| "上证指数今日收盘" | 数字 + 来源 (有数据时) | 2.0s |

## 下一步 (v17.3+)

- 答案模式 UI: 大段文字 + 来源小字
- 答案长度自适应: query 复杂 → 长答案, 简单 → 短答案
- 答案来源点击直达
- 多轮 query (答案 + 反问 "你想知道更多关于...?")

---

# 🚀 v17.3.0 — 前端 AI 答案卡片 (Perplexity Mode UI)

**前端 UI 完整**: 浏览器也能直接看 AI 答案, 不只 API/MCP 用户.

## 状态栏右上 "✦ AI 答案" 开关

- 默认开启 (Perplexity Mode)
- 点击切换 ON/OFF
- 关闭后只返 8 条蓝链 (省 2-3s LLM 耗时)

## 答案卡片 (玻璃态)

```
┌────────────────────────────────────────┐
│ ✦ AI 答案  DeepSeek-V4-Flash  2100ms   │  ← badge + 模型 + 耗时
│                                          │
│ 比亚迪实时股价未在搜索结果中...         │  ← 大段答案 (200-400 字)
│ ...多方认为销量拐点确立...              │
│                                          │
│ ─────────────────────────────────────   │
│ 来源                                     │
│ [quote.eastmoney.com] [sina.com.cn]    │  ← 来源 chips (蓝色, 可点)
│                                          │
│ ▼ 查看下方原始来源 (8 条)               │  ← 滚到蓝链
└────────────────────────────────────────┘
```

## 加载动画

- shimmer 1.4s 渐变循环 (4 行占位)
- 答案生成中, 卡片已显示, 不空等

## 实测

| 模式 | 耗时 | 行为 |
|---|---|---|
| AI 答案 ON (默认) | 3.4s | 答案卡 + 5 个来源 chips + 8 条蓝链 |
| AI 答案 OFF | 0s (缓存) | 只 8 条蓝链 |

---

# 🚀 v17.4.0 — 相关问题 (Follow-up)

**答案卡底部加 3 个紫色 chips**: 用户能一键深挖, 不用重新输入.

## 行为

```
[来源 chips: 蓝色]
[相关问题: 紫色]
[→ 比亚迪 5月销量详情]  [→ 比亚迪 股价历史走势]  [→ 比亚迪 新能源车市占率]
```

- **点击 chip** → 自动 doSearch(那个 query) → 加载新答案
- **生成方式**: LLM 单独调一次 (max_tokens=120, 30-50 tokens, +1-2s)
- **失败降级**: 启发式模板 (`{query} 财务报表` 等)

## 实现

- `_generate_followups(query, answer, domains, category)` in `scripts/answer.py`
- answer dict 加 `followups: [str, str, str]`
- 失败 → 4 类别模板 (finance/tech/news/general)

## 端到端测试

```
query: "比亚迪股价"
answer: "..." (诚实: 实时股价请查行情网站)
followups: ["比亚迪 5月销量详情", "比亚迪 股价历史走势", "比亚迪 新能源车市占率"]
→ 3 个问题都相关且角度不同 (事实深挖 / 技术面 / 行业对比)
```

---

# 🚀 v17.5.0 — 4 类 Prompt 模板 (答案质量分层)

**核心问题**: 之前 1 个通用 prompt 答所有 query, 财经/科技/新闻/通用不分.

**v17.5 解决**: query 分类, 4 个专用 prompt 模板, 答案风格差异化.

## Query 分类 (`_classify_query`)

| 类别 | 触发关键词 | Prompt 风格 |
|---|---|---|
| **finance** | 股票/股价/A股/上证/深证/基金/财报/纳斯达克... | 彭博/华尔街见闻 - **数字粗体 + 严禁编造** |
| **tech** | GPT/AI/LLM/芯片/GPU/Python/CUDA/开源... | 36kr/极客公园 - **版本号精确 + 参数** |
| **news** | 新闻/今天/最新/官方/宣布/突发/媒体... | 澎湃/财新 - **时间敏感 + 多角度** |
| **general** | 其余 | Perplexity - **通用简洁** |

## 关键差异

| 维度 | 财经 | 科技 | 新闻 | 通用 |
|---|---|---|---|---|
| **数字处理** | **粗体**强制 | **版本号/参数** | **数据出处** | 突出即可 |
| **诚实原则** | 严禁编造价格 | 区分官方/媒体 | 区分事实/评论 | 通用诚实 |
| **结构** | 多空观点 | 核心+参数+影响 | 5W1H+多角度 | 自由 |
| **来源偏好** | 东财/新浪 > 雪球 | 官方/知名媒体 | 主流官方媒体 | 不限 |

## 实测对比

```
=== 比亚迪股价 (finance) ===
"**5月**销量结束**8个月**下滑...
多方认为销量拐点确立; 空方担忧行业价格战...
来源: data.eastmoney.com / finance.sina.com.cn"

=== Python 3.13 (tech) ===
"Python **3.13** 于 **2024年10月** 发布...
**JIT 编译器** + **自由线程**模式 (无需 GIL)...
类型系统新增 `TypeAlias` 注解..."

=== 特朗普推文 (news) ===
"当地时间**2025-04-04**晚...连发数十条推文...
支持者认为反映基层不满; 批评者指出数据存出入 (3.9% 失业率)..."

=== 如何煮咖啡 (general) ===
"抱歉, 提供的搜索结果不相关...请换关键词..."
```

## 端到端

- 4 类 query 全部识别正确
- 答案风格差异化
- 端到端 ~4s (search 1s + LLM 3s)
- LLM 选型不变: DeepSeek-V4-Flash (新-API 免费)

---

# ⚡ v17.6.0 — 答案缓存 (LLM Token 成本杀手)

**核心**: 相同 query 30min 缓存 LLM 答案, 不调 LLM, 省 token + 加速.

## 实测加速比

| 维度 | 数字 |
|---|---|
| 第 1 次 | 12.5s (search 6.6s + LLM 5.9s) |
| 第 2 次 (cache 命中) | **53ms** (236x speedup) |
| 第 3 次 (新 query) | 6.9s (重新调 LLM) |

## 缓存策略

- **cache key**: `md5(query_normalized + category + results_bucket)`
  - query 归一化: 小写 + 去首尾空格
  - bucket: 0 / 1-3 / 4-6 / 7+ (避免 8 vs 9 命中不同 cache)
- **TTL**: 30min (短, 因为新闻 query 易过期)
- **存储**: `~/.star-search-cache/answers/<key>.json` (磁盘, 不占内存)
- **降级**: cache 写失败/读失败 → 不影响主流程, 当作 cache miss

## answer dict 新字段

```json
{
  "answer": "...",
  "elapsed_ms": 53,           // cache 命中时是历史 elapsed
  "tokens": 0,                // 0 (没调 LLM)
  "cached": true,             // 标志
  "category": "finance",
  "followups": [...],
  "citations": {...}
}
```

## 配置

```bash
ANSWER_CACHE_TTL=1800   # 30min (默认), 可调到 3600 (1h) 或 300 (5min)
```

## 实战价值

- **降本**: 重复 query 直接 0 LLM token, 月省 50%+
- **加速**: 53ms 体验 vs 12.5s, 用户感知极快
- **并发友好**: 高 QPS 不打爆 new-api (DeepSeek-V4-Flash 限速)

---

# 🎯 v17.7.0 — 内联引用 (Perplexity Mode 完整体验)

**核心**: 答案里 `**比亚迪销量**[2]` → 青绿色 chip, hover 显示来源标题, 点击直达源.

## 端到端示例

```
query: "v17.6 cache 测试 今日新闻"
LLM 输出: "今日未检索到关于 'v17.6 cache 测试' 的直接新闻...
   搜索结果主要指向 'V17' 相关技术教程与娱乐内容:
   西门子博途 TIA Portal v17 安装教程[1][2] 与
   萌娘百科 V17 条目[3]..."
citations: {
  1: {title: "TIA Portal v17 安装教程附安装包 - 知乎", url: "..."},
  2: {title: "西门子博图 V17 - CSDN 博客", url: "..."},
  3: {title: "V17 - 萌娘百科", url: "..."}
}
```

## 渲染方式

1. **LLM prompt 改 4 类**: 都要求"重要事实标 [N], N 对应源序号"
2. **_format_results_for_llm**: 加 `[N]` 序号 (`[1] 标题` / `[2] 标题`)
3. **_extract_citations**: regex `\[(\d+)\]` 解析 → dict
4. **前端 renderAnswerTextWithCitations**: `[N]` 替换成 `<a class="answer-citation-chip">[N]</a>`
5. **CSS 青绿色 chip**: `vertical-align: super` (上标), hover 抬升

## 颜色编码 (避免混淆)

| 类型 | 颜色 | 用途 |
|---|---|---|
| **答案 chip (citation)** | 青绿 #86efac | 答案内 `[N]` 内联引用 |
| **来源 chip (sources)** | 蓝色 #60a5fa | 答案卡底部 5 个域名 |
| **Followup chip** | 紫色 #c4b5fd | 答案卡底部 3 个相关问题 |

## 用户体验

- 一眼看到答案 + 引用, 不需要滚动到来源列表
- 点击 chip 跳转到具体源页面 (不是首页)
- hover 显示来源标题 (如 "TIA Portal v17 安装教程 - 知乎")
- 信任度大幅提升 (可追溯)

## 引用准确性

LLM 用 DeepSeek-V4-Flash 训练得很准, 几乎不编造 [N] 序号:
- 1 次只引用真实存在的 [N]
- 不混淆源 (东方财富说的不会标成新浪)
- 多源说同一事 → 引用最权威的 [N]


---

# v20 实战 35-46 总结 (2026-06-12 至 06-15)
