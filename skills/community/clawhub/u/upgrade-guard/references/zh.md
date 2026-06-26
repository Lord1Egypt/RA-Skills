# Upgrade Guard 中文说明

安全升级 OpenClaw：升级前备份，重启前验证，失败后回滚。

## 为什么需要

OpenClaw 对配置文件**严格验证**——新版本的 schema 不认识旧字段，Gateway 直接拒绝启动。`openclaw update` 升级完才检查配置，如果出问题你就卡在半中间。

Upgrade Guard 补了这个缺口：**先备份 → 再升级 → 验证通过才重启 → 失败自动回滚**。

## 三种模式

| 模式 | 流程 | 适合谁 |
|------|------|--------|
| **cautious**（默认） | 安装包 → 修配置 → 验证 → 重启 | 大版本升级、自定义配置 |
| **openclaw-update** | openclaw update → 验证健康 → 需要时回滚 | 日常小版本升级 |
| **manual** | 只备份+预检 | 自己完全控制升级过程 |

## 升级前预检

升级前检查以下项目：

1. **配置语法**：`openclaw config get agents.defaults.workspace` — 失败说明配置已经坏了
2. **遗留 key**：`openclaw doctor --non-interactive` — 扫出即将被迁移的废弃字段
3. **Gateway 健康**：`openclaw health` — 确认当前状态正常
4. **版本信息**：`openclaw --version` + `node --version`
5. **更新检查**：`openclaw update status --json`

## 备份

升级前必须备份配置文件：

```bash
mkdir -p ~/.openclaw/upgrade-guard
ts=$(date +%Y%m%d-%H%M%S)
ver=$(openclaw --version 2>/dev/null | tr ' ' '_')
mkdir -p "$HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}"
cp ~/.openclaw/openclaw.json "$HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}/"
ln -sfn "$HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}" "$HOME/.openclaw/upgrade-guard/latest"
```

备份位置：`~/.openclaw/upgrade-guard/`

保留最近 10 个，自动清理旧的：
```bash
cd ~/.openclaw/upgrade-guard && ls -1d pre-* 2>/dev/null | sort | head -n -10 | xargs rm -rf 2>/dev/null
```

## Cautious 模式（推荐）

### 第一步：安装包（不重启）
```bash
npm install --global openclaw@latest
```

### 第二步：修复配置
```bash
openclaw doctor --fix --non-interactive
```
这一步用新版本的 doctor，它知道新 schema 和迁移规则。

### 第三步：验证配置能加载
```bash
openclaw config get agents.defaults.workspace
```
**如果失败，不要重启！** 先恢复备份：
```bash
cp ~/.openclaw/upgrade-guard/latest/openclaw.json ~/.openclaw/openclaw.json
```

### 第四步：重启 Gateway
```bash
openclaw gateway restart
```

### 第五步：健康检查
```bash
openclaw health
```
每 5 秒检查一次，最多 12 次（60 秒）。如果 Gateway 起不来，恢复备份配置。

## OpenClaw-Update 模式

1. 备份配置（见上方）
2. `openclaw update --yes`
3. 升级完成后验证：`openclaw health`
4. 如果不健康 → 恢复备份配置 → 手动重启

## Manual 模式

只做备份和预检，升级过程你自己来。

## 回滚

```bash
# 恢复最新备份的配置
cp ~/.openclaw/upgrade-guard/latest/openclaw.json ~/.openclaw/openclaw.json
openclaw gateway restart
```

```bash
# 回滚到指定版本
npm install --global openclaw@2026.4.1
openclaw doctor --fix --non-interactive
openclaw gateway restart
```

## 常见配置迁移

升级时 `doctor --fix` 自动处理的变更：

| 旧字段 | 新字段 |
|---|---|
| `routing.*` | `channels.*` / `messages.*` / `bindings` |
| `agent.*` | `agents.defaults.*` / `tools.*` |
| `messages.tts.openai` | `messages.tts.providers.openai` |
| `talk.voiceId` 等 | `talk.provider` + `talk.providers.*` |
| `identity`（根级） | `agents.list[].identity` |
| `browser.driver: "extension"` | `browser.driver: "existing-session"` |

## 配置热重载

大部分配置变更不需要重启：
- **热生效**：channels、agents、models、hooks、cron、sessions、tools、skills
- **需要重启**：gateway.*（端口、绑定、认证）、discovery、plugins

## 适用场景

| 场景 | 推荐 | 原因 |
|---|---|---|
| npm 全局安装 | ✅ | 直接支持 |
| pnpm/bun 全局安装 | ✅ | 把 npm 换成 pnpm/bun 即可 |
| 很久没升级的 | ✅ 最需要 | 版本跨度大 = 踩坑概率高 |
| 自定义配置多的 | ✅ 最需要 | 改得多 = 更容易不兼容 |
| Docker 部署 | ❌ | 升级是换镜像，流程不同 |
| Git 源码安装 | ❌ | dev 用户走 git pull + pnpm build |
| 多实例生产环境 | ❌ | 需要协调升级，skill 不处理 |

## 安装

```bash
clawhub install upgrade-guard
```
