---
name: QQBot Installer
description: OpenClaw QQ 机器人插件安装与升级助手。当用户说「安装 qqbot」「升级 qqbot 插件」「更新 openclaw-qqbot」「qqbot 插件怎么装」「帮我安装/升级 qqbot」等相关语句时激活。支持全新安装和版本升级，含文件验证、自动回滚、重启。
---

# OpenClaw QQ 机器人插件安装 & 升级

通过 `scripts/upgrade-plugin.sh` 在 agent 内直接完成插件的安装或升级，无需用户在终端手动操作。

## 核心脚本

`scripts/upgrade-plugin.sh` — 通用插件安装/升级脚本。

```
用法: upgrade-plugin.sh <npm-pkg-name> <plugin-id> [选项]

必填：
  <npm-pkg-name>           npm 包名，如 openclaw-qqbot
  <plugin-id>              插件目录名，如 openclaw-qqbot

选项：
  --version <ver>          指定版本（跳过 update，走 reinstall）
  --no-restart             不重启 gateway（热更新场景）
  --verify-files <files>   逗号分隔的相对路径，验证这些文件存在
  --legacy-dirs <dirs>     逗号分隔的旧目录名，安装前清理
```

## 执行逻辑

1. **策略判断**：有安装记录 + 有目录 + 未指定版本 → `plugins update`（升级）；否则 → backup + `plugins install --pin`（全新安装）
2. **文件验证**：读取 `package.json` 版本号，检查 `--verify-files` 指定的关键文件
3. **postinstall**：若存在 `scripts/postinstall-link-sdk.js` 自动执行
4. **重启**：执行 `gateway restart` 使插件生效（`--no-restart` 跳过）

## QQ 机器人插件（openclaw-qqbot）

**安装或升级到最新版：**
```bash
bash <skill_dir>/scripts/upgrade-plugin.sh \
  "openclaw-qqbot" \
  "openclaw-qqbot" \
  --verify-files "dist/index.js,dist/src/gateway.js,dist/src/api.js,dist/src/admin-resolver.js" \
  --legacy-dirs "qqbot,openclaw-qq"
```

**安装或升级到指定版本：**
```bash
bash <skill_dir>/scripts/upgrade-plugin.sh \
  "openclaw-qqbot" \
  "openclaw-qqbot" \
  --version "1.2.3" \
  --verify-files "dist/index.js,dist/src/gateway.js,dist/src/api.js,dist/src/admin-resolver.js" \
  --legacy-dirs "qqbot,openclaw-qq"
```

> `<skill_dir>` = 本 skill 文件所在目录，即 `SKILL.md` 的 dirname。
> 执行前需用 `exec` 运行脚本，并将输出展示给用户。

## 执行后处理

脚本输出包含结构化行：
- `PLUGIN_NEW_VERSION=1.2.3` → 新版本号
- `PLUGIN_REPORT=✅ ...` → 结果摘要（直接转发给用户）

若脚本退出码非 0，告知用户操作失败并粘贴输出，建议检查网络和 npm registry。

## 通用插件（非 qqbot）

```bash
bash <skill_dir>/scripts/upgrade-plugin.sh \
  "my-org/my-openclaw-plugin" \
  "my-plugin-id"
```
