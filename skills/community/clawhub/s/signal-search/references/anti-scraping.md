# 反爬 + 抖动 + 验证绕过 方法论（Signal-Search）

> 本文档是 `scrape.py`（§5.4 / §6.3c）与 `search.py`（§5.3）的实现依据，也是 §13 **M13–M18 / M55** 验收对照源。蓝图 §5.4 引用本文件。
> 核心定位："爬得到"是一等能力，但**只抓公开数据、尊重 robots.txt、不绕过登录鉴权取私有内容、不做高并发压测式请求**（伦理护栏写进代码注释与 SKILL.md）。

---

## 1. 核心心法

反爬对抗不是"硬刚 WAF"，而是**让请求看起来像最守规矩的访客、并尽量绕开 WAF 的存在**。最高效的一招是**直接命中站点自己的 JSON 数据接口（XHR/Ajax 端点）**——现代网站（尤其金融站）页面数据多为 JS 异步注入，真正结构化数据走一个返回干净 JSON 的内部接口，通常**无浏览器挑战**，命中即彻底绕开重反爬。这就是把"探隐藏 JSON API"定为抓取第一优先级的缘故（§5.5 / D9）。

---

## 2. 现代反爬四层（缺一层就过不去）

| 层 | 机制 | 应对 |
|----|------|------|
| 协议层 TLS/JA3/JA4 | python-requests 默认指纹与任何浏览器不同，WAF 在返回 HTML 前 RST | 系统 `curl` 子进程 / `curl_cffi`(impersonate) 对齐；UA 须与模拟浏览器一致 |
| IP 信誉层 | 每 IP 实时信誉（窗口频率/C段/时间规律性），**占拦截权重 60%+** | 住宅/移动代理 >> 数据中心；智能轮换、失败即换 IP |
| 设备指纹+行为层 | Canvas/WebGL/Audio、`navigator.webdriver`、鼠标轨迹/滚动/停留 | Headless 打 stealth 补丁；各维度**互相一致**（矛盾即暴露） |
| 验证码层 | 高风险弹 Turnstile/reCAPTCHA/hCaptcha | 先提真人度免挑战；stealth 渲染过非交互挑战；solver 默认关 |

---

## 3. scrape.py 九能力详版（必实现，对应 M13–M18）

1. **抖动延时**：`time.sleep(random.uniform(t_min, t_max))`，间隔**随机**非固定（固定 1.0s 是 bot 信号）。默认按档位/域名配置（如 1.2–3.5s）。
2. **完整且自洽请求头**：UA/Accept/Accept-Language/Accept-Encoding/Sec-Fetch-*/Referer 整套内部一致（声明 Windows UA 不能配 macOS 字体列表）；UA 池取近期真实版本。
3. **TLS 指纹模拟 + 回落链**：系统 `curl` 子进程 → `curl_cffi(impersonate="chrome120")` → Playwright stealth。UA 与模拟浏览器配置一致。无 curl_cffi 退化为带完整头 `requests` + 日志告警不崩（M14）。
4. **代理轮换（可选，默认关）**：config `proxies` 存在时智能分配；失败/403/429 即丢该 IP 换新，不原地重锤；支持 sticky 会话。
5. **指数退避 + 抖动重试**：429/503 时 `backoff=base*2**n+random_jitter`，最多 3 次；每次换新代理（若有）。3 次失败返 `(None, blocked=True)`（M17）。
6. **挑战页检测与回退**：响应含 `cf-chl`/`challenges.cloudflare.com`/`cf-turnstile`/文案"checking your browser" → 回退 Playwright+stealth 渲染；仍失败标 `blocked=True` 由上层换源（M15）。
7. **蜜罐不跟**：CSS `display:none`/`visibility:hidden`/极小尺寸 `<a>` 视为蜜罐，**绝不请求**（单测注入蜜罐断言无请求，M16）。
8. **会话热身（强反爬站点）**：config 标 `warmup:true` 的域名，先首页→分类页→接受 cookie→随机延时→再进目标页。
9. **Cookies 持久化**：成功后 cookie 落本地缓存（相对路径），复用 `cf_clearance` 跳挑战；成功率掉则重做热身。

---

## 4. 分级升级路径（scrape.py 据此自动降级，成本从低到高）

- **Tier 0｜直击 JSON 数据接口**（首选）：devtools/network 抓 XHR 或逆向令牌；结构化、零挑战、token 最省。东财 push2 即此档。
- **Tier 1｜轻量 HTML（仅 TLS+IP 频率）**：curl_cffi / 系统 curl + 随机 UA/头 + 抖动 + 蜜罐不跟。覆盖东财/新浪/雪球等多数中文站。
- **Tier 2｜重 WAF（Cloudflare/Akamai/DataDome）**：stealth 渲染过 Turnstile（真实浏览器引擎天然过，无需付费 solver）。
- **Tier 3｜兜底**：缓存/归档（Wayback CDX API、Common Crawl）取快照；或标 `blocked=True` 换源/放弃。

---

## 5. TLS 工具矛盾与处理（重要，避免踩坑）

本地 `eastmoney-fundflow-scraper` 实测："**Python requests / curl_cffi 被东财 TLS 封禁，必须用系统 `curl` 子进程**"；外网部分教程称"`curl_cffi impersonate` 可过"。**两者可能都成立**（差异来自版本/网络/具体接口）。本 skill 处理：scrape.py 实现**回落链** `系统 curl → curl_cffi → Playwright stealth`，按响应是否 RST/403 自动升级；并把"东财接口 TLS 工具可用性"列为首版实测验收项（M18，用 `rc==0` 真数据验证），不在规范武断定死某一种。

> 来源质量提示：CSDN 带随机数字 ID 文章多为 AI 内容农场，仅作思路导航；东财结论以本地实战 skill 为准。

---

## 6. 合规护栏（M55，默认开 `compliance.enabled=true`）

抓取层合规与风险控制，对应 §5.23 M55：

1. **robots.txt 尊重**：默认解析并遵守 `Disallow`（config `compliance.respect_robots=true`）；仅抓公开数据。
2. **PII 检测 + 脱敏/不落库原文**：抓取内容做 PII 扫描（手机号/身份证/邮箱/住址），命中则**不落库原文**，仅存脱敏引用元信息（如"某用户 138****1234 提及…"）；`compliance.pii_redact=true`（A27.2）。
3. **rate-limit**：默认 `rate_limit_per_sec≈0.07`（即 1 req/~14s），与 §3 抖动协同，避免高并发压测式请求。
4. **ToS / CFAA 风险标注**：登录墙（`/login`、需鉴权态）、付费墙源标**高风险默认跳过**（`compliance.skip_loginwall_paywall=true`，A27.1）；公开数据可抓。
5. **伦理边界**：不绕过登录鉴权取私有内容；不爬取明确禁止的敏感系统。

> 合规护栏误杀率高时可临时关 `compliance.enabled`，但不默认关（M55 在 §13 交付模式为 ON）。

---

## 7. 验证绕过边界（成本从低到高，与 D12 一致）

1. 探 JSON API（最优，Tier 0）。
2. 提升真人度让挑战不出现（干净指纹 + 住宅 IP + 随机行为）。
3. stealth 渲染过非交互挑战（Turnstile 等，免费手段够）。
4. **solver 服务默认关闭**：仅全失效且用户显式启用并自备 Key 才用（不在首版）。
