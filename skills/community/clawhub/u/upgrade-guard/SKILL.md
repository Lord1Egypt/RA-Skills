---
name: upgrade-guard
description: >
  Safe OpenClaw upgrade workflow with pre-flight config check, automatic backup,
  post-upgrade migration, and rollback. Three modes: cautious (install first,
  verify config before restart), openclaw-update (built-in flow with backup
  safety net), manual (backup only). Use when: upgrading OpenClaw, "gateway
  won't start after update", config backup before version jumps, config
  rollback. Triggers on: upgrade openclaw, update openclaw, 升级openclaw,
  gateway won't start, config broke, config migration, 版本升级.
---

# Upgrade Guard

Safe OpenClaw upgrade: backup before touching anything, verify before restarting, rollback if broken.

## Why

OpenClaw strictly validates config. If a new version renames or removes a key, Gateway refuses to start. `openclaw update` installs the new version before checking config compatibility — if something breaks, you're stuck mid-migration. This adds the safety net that's missing: **backup first, verify before restart, rollback if broken**.

## Three Modes

| Mode | Flow | Best for |
|------|------|----------|
| **cautious** | install package → fix config → verify → restart | large version jumps, custom configs |
| **openclaw-update** | openclaw update → verify health → rollback if needed | routine updates |
| **manual** | backup + pre-check only | you handle the upgrade yourself |

Default: `cautious`

## Pre-flight (all modes)

Before any upgrade, check:

1. **Config syntax**: `openclaw config get agents.defaults.workspace` — if this fails, config is broken already
2. **Legacy keys**: `openclaw doctor --non-interactive` — scan for deprecated keys that will be migrated
3. **Gateway health**: `openclaw health` — confirm current state is good before changing anything
4. **Version info**: `openclaw --version` + `node --version`
5. **Update check**: `openclaw update status --json`

## Backup

Always backup config before upgrading:

```bash
# Create timestamped backup
mkdir -p ~/.openclaw/upgrade-guard
ts=$(date +%Y%m%d-%H%M%S)
ver=$(openclaw --version 2>/dev/null | tr ' ' '_')
mkdir -p "$HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}"
cp ~/.openclaw/openclaw.json "$HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}/"
ln -sfn "$HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}" "$HOME/.openclaw/upgrade-guard/latest"
echo "Backup: $HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}"
```

Keep max 10 backups:
```bash
# Prune old backups (keep newest 10)
cd ~/.openclaw/upgrade-guard && ls -1d pre-* 2>/dev/null | sort | head -n -10 | xargs rm -rf 2>/dev/null; cd -
```

## Upgrade: Cautious Mode

Step-by-step, verifying at each stage:

### Step 1: Install new package only (no restart)
```bash
npm install --global openclaw@latest
```
Or for a specific version: `npm install --global openclaw@2026.4.1`

### Step 2: Fix config with new version's doctor
```bash
openclaw doctor --fix --non-interactive
```
This runs the new version's doctor, which knows the new schema and migration rules.

### Step 3: Verify config loads
```bash
openclaw config get agents.defaults.workspace
```
If this fails, **do not restart**. Restore backup instead:
```bash
cp ~/.openclaw/upgrade-guard/latest/openclaw.json ~/.openclaw/openclaw.json
```

### Step 4: Restart Gateway
```bash
openclaw gateway restart
```

### Step 5: Health check
```bash
openclaw health
```
Repeat every 5 seconds, up to 12 times (60s total). If Gateway doesn't become healthy, restore backup.

## Upgrade: OpenClaw-Update Mode

Use the built-in flow with backup safety net:

1. Backup config (see above)
2. `openclaw update --yes`
3. After update completes, verify: `openclaw health`
4. If Gateway unhealthy → restore backup config and restart manually

## Upgrade: Manual Mode

Just backup and pre-check. Print instructions, user handles the rest.

## Rollback

```bash
# Restore config from latest backup
cp ~/.openclaw/upgrade-guard/latest/openclaw.json ~/.openclaw/openclaw.json
openclaw gateway restart
```

```bash
# Rollback to specific version
npm install --global openclaw@2026.4.1
openclaw doctor --fix --non-interactive
openclaw gateway restart
```

## Known Config Migrations

Common breaking changes (all handled by `doctor --fix`):

| Legacy | New |
|---|---|
| `routing.*` | `channels.*` / `messages.*` / `bindings` |
| `agent.*` | `agents.defaults.*` / `tools.*` |
| `messages.tts.openai` | `messages.tts.providers.openai` |
| `talk.voiceId` etc | `talk.provider` + `talk.providers.*` |
| `identity` (root) | `agents.list[].identity` |
| `browser.driver: "extension"` | `browser.driver: "existing-session"` |

## Config Hot Reload

Most config changes apply without restart:
- **Hot**: channels, agents, models, hooks, cron, sessions, tools, skills
- **Needs restart**: gateway.* (port, bind, auth), discovery, plugins

After upgrade, gateway auto-restarts for critical changes (hybrid mode is default).

---

# 中文版

## 为什么需要

OpenClaw 对配置**严格验证**——新版本 schema 不认识旧字段，Gateway 直接拒绝启动。`openclaw update` 先升级再检查配置，出问题了你就卡在半中间。

Upgrade Guard 补了这个缺口：**先备份 → 再升级 → 验证通过才重启 → 失败回滚**。

## 三种模式

| 模式 | 流程 | 适合谁 |
|------|------|--------|
| **cautious**（默认） | 安装包 → 修配置 → 验证 → 重启 | 大版本升级、自定义配置 |
| **openclaw-update** | openclaw update → 验证健康 → 需要时回滚 | 日常小版本升级 |
| **manual** | 只备份+预检 | 自己完全控制升级过程 |

## 升级流程（Cautious 模式）

### 1. 备份
```bash
mkdir -p ~/.openclaw/upgrade-guard
ts=$(date +%Y%m%d-%H%M%S)
ver=$(openclaw --version 2>/dev/null | tr ' ' '_')
mkdir -p "$HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}"
cp ~/.openclaw/openclaw.json "$HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}/"
ln -sfn "$HOME/.openclaw/upgrade-guard/pre-${ts}-${ver}" "$HOME/.openclaw/upgrade-guard/latest"
```

### 2. 预检
```bash
openclaw config get agents.defaults.workspace  # 配置语法
openclaw doctor --non-interactive              # 遗留 key 扫描
openclaw health                                # Gateway 健康
```

### 3. 安装包（不重启）
```bash
npm install --global openclaw@latest
```

### 4. 修配置 + 验证
```bash
openclaw doctor --fix --non-interactive
openclaw config get agents.defaults.workspace   # 失败就恢复备份
```

### 5. 重启 + 健康检查
```bash
openclaw gateway restart
openclaw health   # 最多等 60 秒
```

## 回滚
```bash
cp ~/.openclaw/upgrade-guard/latest/openclaw.json ~/.openclaw/openclaw.json
openclaw gateway restart
```

## 常见配置迁移

| 旧字段 | 新字段 |
|---|---|
| `routing.*` | `channels.*` / `messages.*` |
| `agent.*` | `agents.defaults.*` / `tools.*` |
| `talk.voiceId` 等 | `talk.provider` + `talk.providers.*` |
| `identity`（根级） | `agents.list[].identity` |

## 适用场景

- ✅ npm/pnpm/bun 全局安装
- ✅ 很久没升级的、自定义配置多的
- ❌ Docker 部署（升级是换镜像）
- ❌ Git 源码安装（dev 用户走不同流程）
