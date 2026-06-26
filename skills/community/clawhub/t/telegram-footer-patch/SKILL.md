---
name: telegram-footer-patch
description: Add a Telegram private-chat footer (`🧠 Model + 💭 Think + 📊 Context`) to OpenClaw replies, with dry-run preview, backup, syntax validation, rollback, and restart guidance.
license: MIT
spdx: MIT
---

# Telegram Footer Patch

![Footer Preview](./assets/footer-preview.jpg)

给 Telegram 私聊回复追加平台层尾注，不依赖模型记忆。

## Features

- Add a Telegram private-chat footer: `🧠 Model + 💭 Think + 📊 Context`
- Support dry-run, backup, rollback, and reapply after upgrades

## 功能

- 给 Telegram 私聊回复追加 `🧠 Model + 💭 Think + 📊 Context` 尾注
- 支持预览、备份、回滚，以及升级后重打

当前实现：优先命中并修改当前版本实际可能生效的 dist 文件（包含 `agent-runner.runtime-*.js`、`reply-*.js`、`compact-*.js`、`pi-embedded-*.js`、`delivery-*.js` 等），支持按内容 anchor 自动发现、自动备份、重复覆盖更新与回滚。**注意：这表示“尽量兼容不同 bundle 布局”，不等于已经证明跨版本都兼容；最终是否修好，以真实 Telegram 私聊回复是否出现脚注为准。**

## 版本支持 / Validation Boundary

- **已实测通过（live Telegram 私聊验收）**：OpenClaw **2026.3.22**
- **对应实际验证的 bundle 路径（2026.3.22）**：`/usr/lib/node_modules/openclaw/dist/agent-runner.runtime-BWpOtdxK.js`
- **已实测通过（live Telegram 私聊验收）**：OpenClaw **2026.4.5**
- **对应实际验证的 bundle 路径（2026.4.5）**：`/usr/lib/node_modules/openclaw/dist/agent-runner.runtime-UIIO4kss.js`
- **已实测通过（live Telegram 私聊验收）**：OpenClaw **2026.4.12**
- **对应实际验证的 bundle 路径（2026.4.12）**：`/usr/lib/node_modules/openclaw/dist/agent-runner.runtime-D6-wGQkR.js` + `/usr/lib/node_modules/openclaw/dist/delivery-iF4EZ9PY.js`
- **2026.4.12 实战结论**：只 patch runner 不够；真实 Telegram delivery/send path 也可能需要 patch，且必须在**真重启（新 PID）**后再做真实私聊验收
- **已完成的静态验证**：`--dry-run`、`--auto-discover --verify`、smoke test、`node --check`
- **未实测覆盖**：其它 OpenClaw 版本、其它 dist 命名/布局、其它未命中的真实 reply/send path
- **发布口径**：除非做过真实 Telegram 私聊验收，否则只能写“可能兼容/已做兼容处理”，不能写“已支持”

## What to consider before installing / 安装前需要考虑的事项

This skill does what it says (patches OpenClaw dist JS files to append a Telegram footer), but it **writes into your OpenClaw installation directory** and requires **Node.js + Python 3**.

Before installing/running:
1) Inspect the scripts yourself and run `--dry-run` to see which files would be touched.
2) Ensure `node` is installed and you have a plan for filesystem permissions (consider a staging instance/container).
3) Confirm backups are created (`*.bak.telegram-footer.*`) and test the revert script.
4) Only run the patch on systems you control and trust.

这项技能的功能正如其名（修改 OpenClaw 分发目录中的 JS 文件，添加 Telegram 页脚），但它会**写入 OpenClaw 安装目录**，并且需要 **Node.js + Python 3**。

安装/运行前：
1) 请自行检查脚本，并运行 `--dry-run` 先预览将会修改哪些文件。
2) 确保已安装 `node`，并规划好文件系统权限（建议先在测试环境/容器中跑）。
3) 确认已创建备份（查找 `*.bak.telegram-footer.*`）并测试还原脚本。
4) 仅在你控制且信任的系统上运行；不确定就先上 staging。

## 使用

### 1) 预览

```bash
python3 scripts/patch_reply_footer.py --dry-run --list-targets
```

### 2) 应用

```bash
python3 scripts/patch_reply_footer.py --auto-discover
python3 scripts/patch_reply_footer.py --auto-discover --verify
```

### 2.5) 跑 smoke test / verify（推荐）

```bash
bash scripts/smoke_test_footer_patch.sh
# 或指定 dist
bash scripts/smoke_test_footer_patch.sh /usr/lib/node_modules/openclaw/dist
```

这个流程会依次执行：
- target discovery
- dry-run auto-discover
- apply auto-discover patch
- marker verification
- 对已打 marker 的文件逐个 `node --check`
- 额外检查 patched file 中没有残留 `formatTokens(`

**边界说明：** 这一步只证明“当前 dist 样本里的候选 bundle 已被 patch 且语法正常”，**不等于**真实回复链路一定已经生效，也不等于跨版本兼容已经被证明。

### 3) 真重启网关（**必须**，才能生效）

> 说明：补丁改的是 OpenClaw 的 dist bundle；Gateway 不重启就不会重新加载，Telegram 私聊脚注不会生效。**仅热刷新 / SIGUSR1 不应直接当作验收通过。**如果环境允许，最好确认出现了**新 PID**。

```bash
openclaw gateway restart
```

### 3.5) 真实验收（**必须**）

重启后，必须做一次**真实 Telegram 私聊回复验收**：
1. 给机器人发一条普通私聊消息；
2. 看实际收到的回复末尾是否出现：
   - `🧠 ...`
   - `💭 Think: ...`
   - `📊 .../...`
3. 若实际消息里**没有脚注**，则结论应是：**还没修好**。

推荐验收标准：
- `--dry-run` / smoke test 通过 → 只能说明 patch 写进了候选 bundle；
- **真实 Telegram 私聊回复带脚注** → 才算当前 live path 修好。

### 4) 回滚

```bash
python3 scripts/revert_reply_footer.py
openclaw gateway restart
```

## 现在包含的保护

- patch 后自动执行 `node --check`
- 尾注片段自包含，不依赖目标 bundle 内部是否存在 `formatTokens` 等局部 helper
- 语法校验失败时自动恢复刚写入前的备份
- 支持 `--list-targets` / `--verify`，先看命中文件，再确认 marker 是否真的打进实际 bundle
- 附带 `scripts/smoke_test_footer_patch.sh`，把 patch + verify + syntax + helper-sanity 串成一套固定回归流程
- smoke test 只是静态/候选级验证；最终仍以**真实 Telegram 私聊回复是否带脚注**为验收标准
- 若 marker 丢失但已有历史备份，会提示“可能被升级覆盖，正在重打”
- 若 insertion needle 在候选 reply bundle 中失效，会明确报错，不再静默跳过
- 会清理已知旧版 Telegram 尾注块，避免双尾注叠加

## 说明

- 当前优先候选包含：`dist/agent-runner.runtime-*.js`、`dist/reply-*.js`、`dist/compact-*.js`、`dist/pi-embedded-*.js`、`dist/plugin-sdk/thread-bindings-*.js`、`dist/model-selection-*.js`、`dist/auth-profiles-*.js`、`dist/delivery-*.js`
- `--auto-discover` 会按内容 needle 追加扫描 `dist/**/*.js`，适合升级后重新定位实际生效 bundle
- 已打过补丁时，会按 marker 直接覆盖更新，不会重复注入
- 每次写入前会自动生成 `.bak.telegram-footer.*` 备份
- OpenClaw 升级后若补丁被覆盖，先跑 `--dry-run --list-targets`，再用 `--auto-discover --verify` 确认命中实际 bundle
- 如果文档、smoke test、marker 都看起来正常，但真实 Telegram 回复仍无脚注，说明**当前真实发送链路未命中**，应继续沿 live path 排查，而不是宣布修复完成
