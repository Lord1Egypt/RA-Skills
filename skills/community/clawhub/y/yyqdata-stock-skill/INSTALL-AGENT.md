# 给 Agent 装 yyqdata skill — 给最终用户看的指引

> 本指引面向**用 小龙虾(OpenClaw) / Hermes Agent / 其他兼容 Markdown skill + 自带 Bash 工具的 LLM 代理**的最终用户。
> Agent 不需要跑 shell 脚本——只需把 skill 的 markdown 文件放到 agent 的 skills 目录，再在对话中把 token 告诉 agent 即可。

---

## 一、装 skill 文件

skill 是一个 zip 包，里面只有 markdown 文档（无可执行代码）。两种装法任选其一：

### 方式 1：手动下载 + 解压（最稳）

```bash
# 在 小龙虾(OpenClaw) / Hermes 客户端机器上：
mkdir -p ~/.openclaw/skills        # 或 ~/.hermes/skills 视你的 agent 而定
curl -fsSL https://static.yyqyx.com/skill/yyqdata-stock-skill.zip -o /tmp/yyqdata.zip
unzip -oq /tmp/yyqdata.zip -d ~/.openclaw/skills/
rm /tmp/yyqdata.zip
# 解压后路径：~/.openclaw/skills/yyqdata/SKILL.md
```

**OpenClaw（小龙虾）用户**：解压到 `~/.openclaw/skills/yyqdata/` 后**不需要任何注册**——openclaw 启动时自动扫描 `~/.openclaw/skills/*/SKILL.md` 发现 skill。重启 openclaw（或 gateway）即可生效。

**Hermes Agent 用户**：注册到 `~/.hermes/agent.yaml`，在 `skills` 列表里加一项：

```yaml
skills:
  - name: yyqdata
    path: ~/.hermes/skills/yyqdata      # 改成你的实际解压路径
```

Hermes Agent 还可以加 trigger（推荐）：

```yaml
triggers:
  yyqdata:
    keywords: [看下, 走势, 估值, 财报, 龙虎榜, 板块, 资金流, 选股, 主力, 放量, 涨停, 连板]
```

重启 agent 让它加载新 skill。

### 方式 2：让 agent 自己下载

把以下话原样发给 agent（**注意把 `<TOKEN>` 替换成你的真实 token，但 token 留到第二步再给**）：

> 请帮我安装 yyqdata skill：
>
> 1. 用 curl 下载 `https://static.yyqyx.com/skill/yyqdata-stock-skill.zip` 到 `/tmp/yyqdata.zip`
> 2. 解压到 `~/.openclaw/skills/`（或你 agent 的 skills 目录），最终路径应为 `~/.openclaw/skills/yyqdata/SKILL.md`
> 3. 阅读 `SKILL.md` 顶部 frontmatter + 硬性约束章节
> 4. 阅读 `references/api-quick-reference.md`
> 5. 完成后告诉我 skill 落在哪个路径，等我给你 token
>
> 注意：本 skill 只是 markdown 文档，没有可执行代码；你只需要 `curl + unzip` 两条命令即可。**不要**尝试运行任何 shell 脚本。

---

## 二、给 token（三选一）

### 方式 A：config.json（推荐，所有 agent 通用，配一次永久生效）

在 skill 安装目录内创建 `config.json`：

```bash
# OpenClaw 用户
cat > ~/.openclaw/skills/yyqdata/config.json <<'EOF'
{ "token": "stk_live_xxx", "base_url": "http://120.220.73.199" }
EOF

# Hermes 用户
cat > ~/.hermes/skills/yyqdata/config.json <<'EOF'
{ "token": "stk_live_xxx", "base_url": "http://120.220.73.199" }
EOF
```

agent 每次启动时从 skill 目录内读取，**无需修改任何 agent / platform 配置**，OpenClaw / Hermes / Claude Code 均适用。

> ⚠️ `config.json` 含明文 token，权限设为 0600：`chmod 600 ~/.openclaw/skills/yyqdata/config.json`

### 方式 B：claw 托管实例（平台自动注入）

由 claw-server 自动开通的实例无需任何操作——token 已注入 `$YYQDATA_TOKEN`、地址已注入 `$YYQDATA_API_BASE_URL`。

### 方式 C：对话中给 token（兜底，任何 agent 通用）

skill 文件就位之后，在你的第一条业务请求里把 token 顺便给 agent：

> 我的 OpenAPI token：`stk_live_2jLvUKkeYlGxHKtnRs5B56OMNhwCIjDk`
> 服务地址：`http://120.220.73.199`（默认就这个，可省略）
>
> 帮我看下贵州茅台（600519.SH）这周的日 K 线。

Agent 会：

1. 把 token + base URL 记到当前会话的内存里（不会落盘）
2. 先调 `POST ${BASE}/openapi/v1/whoami` 看 token 套餐 / scope（会出现在 agent 后台日志里）
3. 按 `SKILL.md` 工作流：`search_stock("贵州茅台")` → `get_daily_kline(600519.SH, ...)` → 回结论

注意：

- ⚠ token 是私密的，agent 不会回显完整值（最多 `stk_live_xxx...` 脱敏）
- ⚠ 同一会话期内不必重复给 token；新开会话需要重新提供
- ⚠ 如果 agent 让你再次提供 token，说明它丢失了上下文（context 被压缩 / 长会话清理），重发即可

---

## 三、自动更新（推荐）

yyqdata 自带 `update.sh`，可一键检查 + 升级到最新版。

### 3.1 用户视角：一行命令

```bash
# 最常用：检查 + 有新版自动装（自动备份旧版到 yyqdata.bak-时间戳/）
bash ~/.openclaw/skills/yyqdata/update.sh

# 只检查不安装（exit 0=最新 / 10=有新版 / 1=网络错误）
bash ~/.openclaw/skills/yyqdata/update.sh --check

# 强制重装（不论本地版本）
bash ~/.openclaw/skills/yyqdata/update.sh --apply
```

环境变量（可选）：

| 变量 | 默认 | 说明 |
|---|---|---|
| `SKILL_UPDATE_URL` | `https://static.yyqyx.com/skill/yyqdata-stock-skill.zip` | zip 下载 URL |
| `SKILL_MANIFEST_URL` | `https://static.yyqyx.com/skill/yyqdata.manifest.json` | 版本元数据 URL |
| `SKILL_INSTALL_DIR` | 自动探测（`~/.openclaw/skills` → `~/.hermes/skills` → `~/.claude/skills`）| skill 安装父目录 |

### 3.2 Agent 视角：每天自动检查

SKILL.md 的「skill 自动更新」章节告诉 agent **每天第一轮**异步拉一次
`https://static.yyqyx.com/skill/yyqdata.manifest.json` 看 version。发现新版时**只在回复末尾追加一行温和提示**，不打扰当前任务，由用户决定要不要升级。

manifest 长这样：

```json
{
  "name": "yyqdata",
  "version": "1.1.0",
  "build_date": "2026-05-22T21:54:33+08:00",
  "zip_url": "https://static.yyqyx.com/skill/yyqdata-stock-skill.zip",
  "size_bytes": 131870,
  "sha256": "<64 字符 hex>",
  "changelog_summary": "v1.1.0：13→19 scope，新增港股/美股/研报/国际宏观/外汇/TMT"
}
```

### 3.3 失败回退（手动重装）

如 update.sh 失败（网络 / 安装目录权限），仍可走原始装法：

```bash
curl -fsSL https://static.yyqyx.com/skill/yyqdata-stock-skill.zip -o /tmp/yyqdata.zip
unzip -oq /tmp/yyqdata.zip -d ~/.openclaw/skills/
rm /tmp/yyqdata.zip
```

### 3.4 后端开发视角：发布新版

后端（`stock/`）有新 endpoint 时：

```bash
cd stock/

# 一键打包 + scp（推荐）
./skill/pack-skill.sh --push

# 或分步：先打包，再人工 scp（适合 review）
./skill/pack-skill.sh
scp dist/yyqdata.zip      root@120.220.73.199:/var/www/html/
scp dist/yyqdata.manifest.json root@120.220.73.199:/var/www/html/
```

`pack-skill.sh --push` 会：

1. 在 `controller/` 模块跑 `mvn -Dfile.encoding=UTF-8 smart-doc:markdown` 重生 API 文档
2. 拷 `stock/doc/AllInOne.md` 进 zip 作 `references/api-full-spec.md`
3. 打 zip 到 `dist/yyqdata.zip` + 版本化 `skill-yyqdata-vX.Y.Z-YYYYMMDD.zip`
4. 生成 `dist/yyqdata.manifest.json`（含 version / sha256 / size / changelog）
5. scp zip + manifest 到服务器 `/var/www/html/`

客户端用户**不需要**手动重装——下次会话 agent 检查 manifest 即可发现并提示。

---

## 四、Token 拿不到 / 套餐不够时

- **没 token**：联系 stock 后端管理员，调 `POST /stock/user/admin/openapi/token/create` 签发一个绑定你出口 IP 的 token（`allowedIps` 必填）
- **来源 IP 不在白名单（401/403）**：claw 发的 token 默认 **自动登记（TOFU）** —— agent **第一次连上**时自动把它的出口 IP 绑进白名单，**最多 2 个**（够在两处用：家里 + 公司 / 两台机器），学满即锁。换到第 3 个网络会被拒；要更换请在 claw_client『我的-数据权益』解绑，或联系管理员把白名单重置回 `auto`。（管理员手签的固定 IP token 则走 `POST .../token/ip/add` 手动改，封顶 2 个；大段地址用 CIDR）
- **403 scope 不足**：当前套餐不含某个数据维度（例如 stock.financial 需要 Plus 套餐及以上），让管理员升级或换 token
- **429 频率超限**：等下一分钟，或申请更高频率档

随时可以让 agent 调一次 `POST ${BASE}/openapi/v1/whoami` 自查当前 token 的套餐 / scope / 频率上限。
