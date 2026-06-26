# Cloudflare Bot 保护实战 87 (2026-06-17)

## 现象

用户报告:
> "Star Search 被 Cloudflare 保护了（人机验证）, API 无法直接调用. 这个 skill 无法使用了, 是怎么回事, 人机验证不是用在 web 端吗, skill 应该可以正常使用啊"

**关键观察**:
- Web 浏览器打开 `https://search.token-star.cn/` → **正常**
- Python `requests`/`httpx`/`aiohttp`/`curl` → **403/503 弹人机验证**
- MCP server stdio (本地) → **正常** (走 127.0.0.1, 不出公网)
- MCP server SSE (公网) → **被拦**
- OpenAPI 3.0 schema (GPT Actions) → **被拦**
- Claude MCP registry → **被拦**

## 根因

Cloudflare 看到请求头:
```
User-Agent: Python-urllib/3.12
Accept-Encoding: gzip, deflate
```
+ 无 Cookie
+ 无 Referer
+ 来源 IP: 62.234.39.247 (腾讯云)

→ **Cloudflare Bot Fight Mode** 判定 bot → 触发 JS Challenge / Managed Challenge → 弹人机验证

**Web 浏览器不受影响** 是因为浏览器带 Cookie + JS 引擎 + 真实用户行为特征。

## 用户硬原则

> "方案A, 这个 skill, 是免费使用的, 这个是咱们的核心原则"

→ 必须**永久方案** (CF 后台规则), 不能用临时 hack (改 UA 一次性) — 否则用户每次升级 skill 都要操心。

## 3 选 1 修复

### A. 关 Bot Fight Mode (5 min, 推荐)

**步骤**:
1. https://dash.cloudflare.com/ 登录
2. 选 `token-star.cn` 域名
3. Security → Bots → **Bot Fight Mode** → **Off**

**优点**: 0 凭证分享, 永久解, 0 配置
**缺点**: 全域关闭 (skill/MCP 用, 但要承担风险: 别人也会爬)

### B. WAF Custom Rule 白名单 (推荐, 永久)

**步骤**:
1. dash.cloudflare.com → token-star.cn → Security → WAF → Custom Rules
2. Create rule: `ip.src eq 62.234.39.247` OR `http.user_agent contains "Star-Search-Skill"`
3. Action: **Skip**: Super Bot Fight Mode / Bot Fight Mode

**优点**: 精确白名单, 其他 IP 仍受保护
**缺点**: 要 token 权限

### C. 改 User-Agent + Headers (2 min, 不彻底)

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
```

**优点**: 0 配置, 立即生效
**缺点**: 临时方案, Cloudflare 升级检测就失效, 不能作为长期方案

## API Token 权限 (A/B 方案)

**默认 token 权限不够** (实战 87 验证):
```bash
curl "https://api.cloudflare.com/client/v4/user/tokens" \
  -H "Authorization: Bearer cfut_xxx"
```
返: `"permission_groups":[{"name":"API Tokens Write"}]`

**不够** — 必须有:
- `Zone WAF Edit` (加 Custom Rule)
- `Zone Settings Edit` (关 Bot Fight Mode)
- `Zone Bot Management Edit` (备选)

**创建 token 步骤**:
1. https://dash.cloudflare.com/profile/api-tokens
2. Create Token → Custom token
3. Permissions: 选 `Zone WAF Edit` + `Zone Settings Edit` + `Zone Bot Management Edit`
4. Zone Resources: 选 `token-star.cn` (或 All zones)
5. Continue → Create
6. **复制 token (只显示 1 次!)**

## API 调用

**Verify token**:
```bash
curl "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer cfut_xxx"
# 返: {"success":true, "status":"active", "expires_on":"2026-08-31T23:59:59Z"}
```

**List zones** (验证 token 有 zones:read):
```bash
curl "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer cfut_xxx"
# 返: {"result":[{"id":"abc123","name":"token-star.cn"}]}
```

**Zone ID 获取**:
- dash.cloudflare.com → 选 token-star.cn → 右下角 "API" 框 → Zone ID

**关 Bot Fight Mode**:
```bash
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/bot_fight_mode" \
  -H "Authorization: Bearer cfut_xxx" \
  -H "Content-Type: application/json" \
  -d '{"value":"off"}'
```

**加 WAF Custom Rule** (用 Super Bot Fight Mode Ruleset):
```bash
# 1. 找 ruleset id
curl "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets" \
  -H "Authorization: Bearer cfut_xxx"

# 2. 拿 Super Bot Fight Mode ruleset id

# 3. 加 rule
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset_id}/rules" \
  -H "Authorization: Bearer cfut_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "skip",
    "description": "Star-Search-Skill 白名单",
    "expression": "(ip.src eq 62.234.39.247) or (http.user_agent contains \"Star-Search-Skill\")",
    "action_parameters": {
      "ruleset": "current"
    }
  }'
```

## 实战 87 验证步骤

1. 拿正确权限 token
2. PATCH 关 Bot Fight Mode
3. 验证: `python3 -c "import requests; r = requests.get('https://search.token-star.cn/v1/health'); print(r.status_code)"`
   期望: `200` (不是 403/503)
4. 端到端: `curl -X POST https://search.token-star.cn/v1/search -d '{"query":"test"}'`
   期望: 返 JSON, 不是 Cloudflare challenge HTML

## 教训 (下次别的项目也用)

1. **任何公网 skill/API 服务, 上线前必须测 Cloudflare Bot 检测**
   - 用 `curl` / `requests` / `httpx` 各测一次
   - 不通过就是 CF 在保护
   
2. **CF 默认 Bot Fight Mode 是开启的** — 上线就触发
   - 主动在 CF 后台关, 不要等服务上线后再处理

3. **Token 权限 = 操作权限** — 默认 token 只能管自己
   - 管 zone 资源要 `Zone WAF Edit` / `Zone Settings Edit`
   - 管 account 资源要 `Account WAF Edit` / `Account Settings Edit`

4. **优先用 IP 白名单, 不用 UA 白名单** — IP 难伪造, UA 一行代码就改

5. **核心原则 (用户)**: "这个 skill, 是免费使用的, 这个是咱们的核心原则"
   → 用户体验 = 永久方案, 不用临时 hack
   → 修 CF 用后台规则, 不用改代码改 UA
