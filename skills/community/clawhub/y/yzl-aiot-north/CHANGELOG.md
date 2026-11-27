# 更新日志

## v2.0.0 (2026-11-27) — 自带接口库

- 🧰 新增 `lib/north_client.py`（标准库）与 `lib/north_client.mjs`（原生 fetch），覆盖全部北向 REST 接口
- 🖥️ `tool.py` 改为调用自带库，移除对外部 SDK 的依赖
- 🧪 新增 `tests/`：本地 mock + 25 项 Python / 12 项 JS 离线自测
- 📄 新增 `lib/README.md`：接口 ↔ 方法 ↔ CLI 对照

## v1.3.0 (2026-11-27) — 增加 Python / Node.js 示例

- 📁 新增 `examples/python`（quickstart、bridge_webhook）与 `examples/js`（quickstart、bridge_webhook）
- 📝 SKILL.md、README.md 增加示例入口与运行说明
- ⚠️ 接口与 SDK 行为不变

## v1.2.0 (2026-11-27) — 文档重写 + 命令行工具

- 📝 **SKILL.md 重写**：按 `yzl-open-api` 的结构统一（平台边界、运行时要求、限频、快速使用、接口表、常见坑、验证、安全、版本历史）。
- 🧰 **新增 `tool.py`**：包装 `aiot_north` SDK CLI，提供 `devices` / `telemetry` / `history` / `command` / `bridge` 等命令，以及本地 `help` / `version` / `check-update`。
- 📄 **补齐包结构**：`README.md`、`CHANGELOG.md`、`skill-card.md`、`_meta.json`、`sync.sh`。
- 📏 **限频口径**：北向 REST 用户配额（基础 + 设备数 × 每台追加，按秒计；写接口 3 倍），与开放平台按接口限速分开。
- ⚠️ 行为无变化：接口、鉴权与 SDK 逻辑不变。

## v1.1.0 (2026-11-24) — 补单设施属性修改

- 🧩 新增 `PATCH /open/product/{id}/metric/{key}` 用法与 `before` / `after` 快照说明。
- 🕳️ 补充实测坑：单型号 GET 404、`autoAdd`、`access=rw` 的真实含义。
- 🔧 平台 2026-11-21 更新：支持按测点单点修改（不再必须 `PUT` 整表覆盖）。

## v1.0.0 — 北向首版

- 🐍🟨 Python / Node 客户端、CLI、Bridge / Webhook、北向 MQTT。
- 🔑 三级认证（JWT → 账号密码 → API Key）。
