# REA-CN 常见错误 → 中文含义与处理

> 引擎错误信息均为英文。本表把高频错误/状态翻译成中文，便于中文 LLM 与用户快速定位。
> 实际信息以引擎实时返回为准；本表为经验性参考。

## 1. 工具/调用类

| 英文现象 | 中文含义 | 处理 |
|---|---|---|
| `Missing tool contract: <name>` | 工具契约缺失（名字不认识） | 工具名写错/被翻译。查 `tool-manifest.json` 用精确英文名 |
| `tool <x> not found` / 工具不存在 | 客户端未注册该工具 | 确认 MCP 服务器已加载且版本一致；参考 `SKILL.en.md` |
| `resource_constraint` + `resource: "transport"` | 单次返回过大，被传输层截断 | 用 `inspect_analysis_view` 取摘要/分页，或 `export_evidence_bundle` 落盘 |
| `client approval required` | 客户端要求人工审批 | 按客户端策略授权后重试 |
| `blocked by client` | 客户端拦截了调用 | 检查客户端 MCP 权限/网络策略 |

## 2. 目标/会话类

| 英文现象 | 中文含义 | 处理 |
|---|---|---|
| `target not open` / `no active target` | 尚未打开目标 | 先 `open_binary` 或对应打开类工具 |
| `already open` (JEB) | 已有工程打开，不能重复开 | 先关闭当前工程再开 |
| `unsupported provider` | 当前 provider 不支持该能力 | 换 provider（`provider_id`）或换工具；用 `binary_session` 看可用性 |
| `Windows P0 unsupported` | Windows P0 层级不被支持 | 该能力在 Windows P0 不可用，换平台或跳过 |
| `format detection failed` | 格式识别失败 | 显式传 `format=` 或确认文件完整 |
| `immutable snapshot save refused` | 有未提交元数据编辑，拒绝存快照 | 先 `close_binary` 或 `export_evidence_bundle` 再存 |

## 3. 文件/路径类（常因中文路径/编码）

| 英文现象 | 中文含义 | 处理 |
|---|---|---|
| `ENOENT` / `no such file` | 文件不存在 | 检查路径；优先 ASCII 路径（见 `locale-encoding.md`） |
| `path traversal rejected` | 路径穿越被拒 | 不要传 `../` 越界路径 |
| `overwrite required` | 目标文件已存在，需显式覆盖 | 传入 `overwrite: true`（如 `export_evidence_bundle`） |
| `GBK`/乱码相关 | 控制台编码非 UTF-8 | `chcp 65001` 或重定向到 UTF-8 文件 |

## 4. 设备/ADB 类

| 英文现象 | 中文含义 | 处理 |
|---|---|---|
| `device not found` | 未连接设备 | `list_adb_devices` 确认；检查 USB/网络/模拟器 |
| `adb server not started` | adb 服务未起 | 首次使用会自动尝试启动；或手动 `adb start-server` |
| `permission denied` | 权限不足 | 设备需授权调试；部分操作需 root |
| `install failed` / `uninstall failed` | 安装/卸载失败 | 看设备返回的具体原因（保留原样） |

## 5. 通用建议

- **不要把英文错误"翻译"成工具名去调用**——错误文本不是工具。
- 遇到不确定错误，先 `binary_session`（入参 `{}`）查看 `tool_availability` 与服务器身份。
- 把错误原文保留，连同中文解释一并呈现给用户，便于排错。
