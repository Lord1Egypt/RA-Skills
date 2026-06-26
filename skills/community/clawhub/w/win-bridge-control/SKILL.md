---
name: win_bridge_control
description: "Bridge: Cross-OS UI automation for Windows Host"
metadata:
  openclaw:
    os: ["linux"]
    requires:
      bins: ["/mnt/c/Windows/System32/cmd.exe", "node"]
    security_scope: "restricted_environment"
---

# Windows Host Bridge Control

此技能专门用于在 WSL2 环境中穿透控制 Windows 宿主机上的仪器。

## 🛡️ 安全合规协议 (Security Protocol)
1. **已知工具**：本技能显式调用宿主机 `cmd.exe` 和 `npx`，用于合规自动化。
2. **输入清洗**：Agent 在构造指令前，必须移除 `action_prompt` 中的非法字符（如 `;`, `&`, `|`, `$`, `>`），防止命令注入。
3. **隔离执行**：本技能仅限于 UI 视觉操作，不涉及敏感文件读取。

## ⚙️ 执行逻辑 (Execution Logic)
当需要操作 Windows 界面时，必须严格遵守以下参数构造：

- **宿主机 Shell**: `/mnt/c/Windows/System32/cmd.exe /C`
- **Node 路径**: `C:\PROGRA~1\nodejs\npx.cmd` (强制使用 8.3 短路径以规避空格解析错误)
- **核心组件**: `@midscene/computer@1`

### 标准指令模板：
使用系统 `exec` 工具运行以下原子化命令：
`/mnt/c/Windows/System32/cmd.exe /C "C:\PROGRA~1\nodejs\npx.cmd @midscene/computer@1 act --prompt \"{{action_prompt}}\""`

## 场景示例 (Scenarios)
- **读取数据**: "Click the 'Read' button in software and wait for completion."
- **环境检查**: "Take a screenshot of the main display and identify the active window."
- **坐标操作**: "Move the mouse cursor to the center of the screen."

## ⚠️ 故障排除
- 如果报错 "C:\Program is not recognized"，请检查是否严格使用了 `PROGRA~1` 路径。
- 如果出现 "Permission Denied"，请确保 Windows 侧已开启开发者模式并允许外部调用。