# REA-CN 配置键对照（Environment / Config Keys）

> REA 通过环境变量与配置选择 provider 与运行时行为。本表列出中文环境下最常用、且与本技能脚本相关的键。
> 完整键以引擎源码/官方文档为准；下表为适配层重点摘选。

## 1. Provider 选择 / 路径类（最常配）

| 配置键 | 作用 | 说明 |
|---|---|---|
| `REA_ADB_PATH` | adb 可执行文件路径 | 指向绝对路径的 `adb`；不设则用 PATH 中 `adb`。Android 类工具需要 |
| `REA_APKTOOL_COMMAND` | apktool 启动器 | 绝对路径或 PATH 中的 `apktool`；资源解码需要（Java 自备） |
| `REA_JEB_MCP_URL` | JEB MCP 端点 | 默认 `http://127.0.0.1:8425/mcp`；需你先启动 JEB 客户端 |
| `REA_BROWSER_EXECUTABLE` | 浏览器可执行文件 | 绝对路径；Web 模块导入/原生导入需要（Chromium 系） |
| `REA_PROCESS_RUN_ID` | 进程运行归属标识 | 保留键，脚本/捕获场景内部使用，勿手动设置 |

## 2. 引擎/安装类（本技能脚本读取）

| 配置键 / 文件 | 作用 | 说明 |
|---|---|---|
| `config/cn-config.json` → `engineVersion` | 默认引擎版本 | `cn-installer.mjs` / `rea-selfupdate.mjs` 读取 |
| `config/cn-config.json` → `npmRegistry` | 国内镜像源 | 默认 `https://registry.npmmirror.com` |
| `REA_INSTALL_DIR` | 安装目录覆盖 | 不设则用技能根目录 |
| `engine/` | 离线引擎基线 | 自更新器同步目标；与本地化文件并列 |

## 3. provider_id（open_binary 入参）

`open_binary` 的 `provider_id` 用于显式选择后端：

| 值 | 含义 |
|---|---|
| （省略） | 确定性自动选择 |
| `"ghidra"` | Ghidra（headless 分析） |
| `"hopper"` | Hopper（macOS GUI 桥） |
| `"ida"` | IDA（需已配置 IDA MCP） |
| 其他原生/专项 | 由引擎与已安装 provider 决定 |

## 4. 设置方式示例（Windows PowerShell）

```powershell
$env:REA_ADB_PATH = "C:/Android/platform-tools/adb.exe"
$env:REA_APKTOOL_COMMAND = "C:/tools/apktool.bat"
$env:REA_JEB_MCP_URL = "http://127.0.0.1:8425/mcp"
```

Linux / macOS（bash）：
```bash
export REA_ADB_PATH=/opt/android-sdk/platform-tools/adb
export REA_APKTOOL_COMMAND=/usr/local/bin/apktool
```

## 5. 自查

- [ ] 需要的 provider 是否已安装且在 PATH / 绝对路径中？
- [ ] 相关环境变量是否已 `export` / `$env:` 到运行 REA 的同一进程？
- [ ] 用 `binary_session`（入参 `{}`）确认 `tool_availability` 显示该 provider 可用？
