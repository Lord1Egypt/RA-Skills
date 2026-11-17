# 运行、本地加载与打包

## 1. 依赖

| 依赖 | 版本要求 | 检查命令 |
|---|---|---|
| `node` | ≥ 18（脚本零第三方依赖，不需要 `npm install`） | `node --version` |
| `alipay-bot` | 官方 `@alipay/agent-payment` | `alipay-bot --version` |

本 Skill 与官方买家支付能力使用**同一套 Node 运行时**，不需要 Python、pip 或其他语言环境。
缺少 `alipay-bot` 时按 alipay-payment-skill 的 `references/command-recovery.md` 先校验 `dist.integrity` 再安装，未经用户同意不得安装。

## 2. 运行

```bash
# 只组装请求体（不发请求）
node "$SKILL_DIR/scripts/travel_aipay.mjs" body --query '杭州三日亲子游，2 大 1 小' --email buyer@example.com

# 取 402 账单
node "$SKILL_DIR/scripts/travel_aipay.mjs" probe --query '...' --email '...' --country-code CN

# 用户明确同意付款后
node "$SKILL_DIR/scripts/travel_aipay.mjs" pay --confirm --session-id '<当前会话标识>'

# 付款后取货（复用同一订单）
node "$SKILL_DIR/scripts/travel_aipay.mjs" complete --out-shake-no '<官方查询单号>'

# 渲染已保存的响应
node "$SKILL_DIR/scripts/travel_aipay.mjs" render --response ~/.xianzong-travel-aipay/delivery.json
```

通用选项：

| 选项 | 说明 |
|---|---|
| `--state-dir DIR` | 本地状态目录，默认 `~/.xianzong-travel-aipay` |
| `--timeout-ms N` | HTTP 超时毫秒，默认 `600000`（生成含 PDF 可能数分钟） |
| `--resource-url URL` | 覆盖资源地址（一般无需改动） |
| `--dry-run` | `probe` / `complete` 支持，只打印将发送的请求，不发送 |

退出码含义见 `SKILL.md` 的状态矩阵。

## 3. 本地加载（让 Agent 发现本 Skill）

| 宿主 | 放置路径 |
|---|---|
| 本仓库（产品目录，可提交） | `skills/xianzong-travel-aipay/` |
| VS Code / Copilot（默认目录，无需设置） | `.github/skills/xianzong-travel-aipay/`、`.claude/skills/`、`.agents/skills/` |
| VS Code / Copilot（用户级） | `{{VSCODE_USER_PROMPTS_FOLDER}}/../skills/xianzong-travel-aipay/`、`~/.copilot/skills/`、`~/.claude/skills/`、`~/.agents/skills/` |
| Claude Code | `~/.claude/skills/xianzong-travel-aipay/` |

加载后校验：

1. `SKILL.md` 的 frontmatter `name` 必须与目录名 `xianzong-travel-aipay` 完全一致。
2. `description` 里必须含触发词（旅行方案 / 行程规划 / 仙踪问道 / 旅行咨询 PDF）。
3. 用户说"帮我做个杭州三日亲子游方案"应能命中本 Skill；说"我要付款"应交由 alipay-payment-skill。

### 仓库根 `skills/` 必须登记才能生效

VS Code / Copilot 只会扫描**固定的默认目录**（源码 `chat.agentSkillsLocations` 默认值）：

```
.agents/skills        .github/skills        .claude/skills
~/.agents/skills      ~/.copilot/skills     ~/.claude/skills
```

仓库根的 `skills/` **不在**默认清单里，不登记就**不会自动发现**（也不会有 `/` 斜杠命令），只能靠用户明确说"读取 `skills/xianzong-travel-aipay/SKILL.md`"手动加载。

本仓库已在 `.vscode/settings.json` 里登记：

```jsonc
{
  "chat.useAgentSkills": true,
  "chat.agentSkillsLocations": {
    ".agents/skills": true,
    ".github/skills": true,
    ".claude/skills": true,
    "skills": true          // 相对仓库根的产品 Skill 目录
  }
}
```

注意事项：

- 必须是**子目录 + SKILL.md** 的形态（`skills/xianzong-travel-aipay/SKILL.md`），不能直接把 `SKILL.md` 放在 `skills/` 下。
- `.vscode/` 在本仓库被 gitignore，所以这份登记**只对本机生效**；新环境 clone 后需在设置里再加一改才能自动触发。
- 不要用软链指向别处（发现逻辑会做 realpath 包含性校验）。
- 改完设置后需重载窗口（Reload Window）才会重新扫描目录。

## 4. 离线测试（不花钱、不联网）

```bash
node "$SKILL_DIR/tests/run_offline_tests.mjs"
```

覆盖：402 取账单、参数校验拦截、付款前拦截（无 `--confirm` 不得付款）、成功交付、同订单重试（不新建账单）、409 生成中、402 凭证失效、500、业务失败、dry-run、render、参数越界、缺单号拦截。

## 5. 打包

```bash
# 在 skills 目录下打包（排除工作目录、凭证、缓存）
cd skills
zip -r xianzong-travel-aipay.zip xianzong-travel-aipay \
  -x 'xianzong-travel-aipay/.xianzong-travel-aipay/*' \
  -x '*/node_modules/*' \
  -x '*.pyc' \
  -x '*/__pycache__/*' \
  -x '*/.env' \
  -x '*/payment-needed.txt' \
  -x '*/body.json' \
  -x '*/state.json' \
  -x '*/delivery.json'
```

打包后自检：

```bash
unzip -l xianzong-travel-aipay.zip
```

必须**没有** `.xianzong-travel-aipay/`、`node_modules/`、`.env`、任何凭证/状态文件。

若用官方安装器分发：

```bash
alipay-bot skill-install --package xianzong-travel-aipay.zip --skills-root ~/.agents/skills
```

## 6. 尚未提供的配置

本 Skill 无需填写任何密钥或服务端配置：账单签名、验付、履约确认全部在服务端完成。以下为需与支付宝服务市场登记保持一致的对外信息，已固化在 `SKILL.md`：

| 项 | 当前值 |
|---|---|
| 资源地址 | `https://api.riyuexinzhu.com/aipay/travel_consultant` |
| 单次价格 | `0.99` 元/次 |
| 商品名 | `仙踪问道_旅行咨询` |
| 服务标识 | `API_7D36D49749854F1F` |

如服务市场登记地址、单价或商品名发生变更，需同步更新 `scripts/travel_aipay.mjs` 顶部的 `RESOURCE_URL` / `PRICE_CNY` / `GOODS_NAME` 与本文件。
