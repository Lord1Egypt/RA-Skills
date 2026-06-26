---
name: apikey
description: >
  新氧青春诊所 API Key 管理（setup）：配置/查看/替换/删除 Key、绑定主人、保存与查看主人位置。
  | Soyoung clinic apikey & owner bind
  OpenClaw setup for Soyoung (soyoung) clinic: API key lifecycle, owner binding, workspace-scoped state.
  Keywords: Soyoung, soyoung, clinic, apikey, credential, owner, medical aesthetic.

  新氧青春诊所 API Key 管理（非用户技能而是基础配置）。负责配置、查看、替换、删除当前 workspace 的新氧 API Key，
  同时绑定 API Key 主人，并保存/查看主人位置。状态目录为
  ~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/。

  安全规则：
  1. API Key 只能由主人在私聊中发送和配置，绝不能发到多人群聊中。
  2. 所有脚本调用必须透传 MessageContext 对应参数：
     --workspace-key --chat-type --chat-id --sender-open-id [--sender-name] [--mention-open-id ...]
  3. 首次配置时，当前私聊发送者会自动绑定为该 workspace 的 API Key 主人。
  4. 以下操作执行前必须先向用户发送确认消息，等待用户明确回复"确认"或"是"后才继续：
     - 查看/展示 API Key 状态（--check-key）→ 「你确定要查看 API Key 配置状态吗？回复"确认"继续」
     - 删除 API Key（--delete-key）→ 「⚠️ 确定要删除新氧 API Key 吗？删除后预约/项目功能不可用。回复"确认"继续」
     - 替换已有 API Key（--save-key，本地已存在时）→ 「⚠️ 本地已有 API Key，确定要覆盖吗？回复"确认"继续」
  5. 脚本输出 `⏸️ NEED_CONFIRM:xxx` 时，向用户发送确认消息等待回复，用户确认后加 --confirm 重新调用。
     - check_key → 查看状态  |  replace_key → 替换  |  delete_key → 删除

triggers:
  - "配置新氧 API Key"
  - "设置新氧 API Key"
  - "保存新氧 API Key"
  - "重置新氧 API Key"
  - "替换新氧 API Key"
  - "覆盖新氧 API Key"
  - "删除新氧 API Key"
  - "新氧 API Key"
  - "我的新氧 API Key 配置了吗"
  - "查看新氧 API Key"
  - "当前新氧主人是谁"
  - "谁是新氧主人"
  - "我保存的位置是什么"
  - "soyoung-clinic-api-key"
  - "新氧诊所 API Key"
  - "新氧青春诊所 API Key"
  - "新氧青春 clinic 开启调试模式"
  - "新氧青春 clinic 关闭调试模式"
  - "新氧青春 clinic 开启调式模式"
  - "新氧青春 clinic 关闭调式模式"
  - "新氧开启调试模式"
  - "新氧关闭调试模式"

metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["python3"] },
        "primaryEnv": "SOYOUNG_CLINIC_API_KEY",
        "secrets": ["soyoung-clinic-api-key"],
      },
  }
---

# Soyoung Clinic — API Key 管理 🔐

统一管理当前 workspace 的新氧 API Key、主人绑定和位置数据。

## 📋 快速索引：意图 → 操作

| 用户意图 | 脚本参数 | 需要确认 |
|---------|---------|---------|
| 配置 API Key（首次） | `--save-key "KEY"` | 否 |
| 替换/重置 API Key | `--save-key "KEY" --confirm` | ✅ 是 |
| 查看 Key 状态（脱敏）| `--check-key --confirm` | ✅ 是 |
| 删除 API Key | `--delete-key --confirm` | ✅ 是 |
| 查看主人绑定 | `--show-owner` | 否 |
| 验证 Key 格式 | `--verify-key` | 否 |
| 保存我的位置 | `--save-location --city XX` | 否 |
| 查看已保存位置 | `--get-location` | 否 |
| 开启调试模式（「新氧青春 clinic 开启调试/调式模式」）| `--debug-on` | 否 |
| 关闭调试模式（「新氧青春 clinic 关闭调试/调式模式」）| `--debug-off` | 否 |

## 🔐 首次配置引导

当用户说"配置新氧 API Key"或 Key 不存在时，引导用户：
1. 打开浏览器，访问：`https://www.soyoung.com/loginOpenClaw`
2. 登录账号，页面会显示 API Key，复制它
3. **只能在与主人私聊中**回来说：「配置新氧 API Key 为 xxx」
4. 调用脚本时必须追加消息上下文参数：
   `--workspace-key --chat-type direct --chat-id --sender-open-id [--sender-name]`

## 🛡️ 安全约束

- **API Key 仅存当前 workspace**，文件权限 600，其他 agent 不共享
- **群聊禁止发送 Key**：主人也不能在群聊里发送、替换或删除 API Key
- **主人绑定**：首次私聊配置者自动成为主人，之后只有主人能在私聊里查看/替换/删除/验证 Key
- `--check-key` 只显示前4后4位脱敏预览，不输出完整值
- **接口地址必须为 `https://`**：`--set-api-url` 不接受 `http://` 明文地址，防止 API Key 被中间人截获
