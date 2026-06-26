---
name: webprinter-skill
description: >
  调用官方 WebPrinter 云打印服务（webprinter.cn），提供企业智慧文印、打印管控、共享打印、
  远程打印等全套打印管理功能，此技能的能力包含查询打印机、上传本地文件、创建漫游打印任务、
  直接打印到指定设备，以及分别更新单双面、颜色、份数和纸张等打印参数。使用前需要先安装咱丢打印服务，
  参考 [https://liqdopokb8.feishu.cn/docx/A0audnVIaoolXqxWUHPcvl1UnFd](https://liqdopokb8.feishu.cn/docx/A0audnVIaoolXqxWUHPcvYlUnFd )
  如果只是要向本地网络打印机提交打印，可使用云上驱动打印([https://github.com/zimsoft/cloud-driver-print/](https://github.com/zimsoft/cloud-driver-print/))。
env_vars:
  - WEBPRINTER_ACCESS_TOKEN
---

# 智睦云打印
当用户希望通过智睦云打印服务完成打印相关操作时，使用此技能。

本技能支持：

- 查询可用打印机
- 上传本地文件
- 创建漫游打印任务
- 直接打印到指定设备
- 更新已有打印任务的单双面设置
- 更新已有打印任务的颜色设置
- 更新已有打印任务的份数设置
- 更新已有打印任务的纸张设置

## 使用前检查
1. 运行环境需要 `Python 3.10+`
2. 首次使用前先安装依赖：
```bash
pip install -r requirements.txt
```
3. 要求用户先通过官方 OAuth 页面获取访问令牌。官方 OAuth 地址：
```text
https://any.webprinter.cn/get-ai-server-token
```
4. 令牌必须配置到环境变量 `WEBPRINTER_ACCESS_TOKEN`
5. 首次执行打印相关操作前，先运行：
```bash
python scripts/mcp_client.py check-install-progress
```

如果返回：
- `hasClient: false`：停止后续打印操作，提示用户先安装并绑定官方智睦云打印客户端（访问 `https://any.webprinter.cn` 下载）
- `hasDevice: false`：停止后续打印操作，提示用户先共享或绑定打印机

依赖文件：
- `requirements.txt`，当前依赖为 `requests>=2.31.0`

## 安全边界
直接打印和创建漫游打印任务，只接受两类输入来源：

- 用户指定的本地文件
- 用户明确提供的 `http://` 或 `https://` 文档链接，且链接内容必须能被智睦云打印服务器访问

额外限制：

- 拒绝 `localhost`、`.local` 等本地地址
- 如果 URL 指向内网地址，要提醒用户该地址必须可被打印服务访问
- 不要为了“验证链接”主动下载、抓取或打开用户给出的远程文档内容；把原始 URL 直接传给智睦云 API
- 更安全的默认路径：本地文件先上传，再使用上传结果中的 `https://any.webprinter.cn/...` 地址
- 如果用户提供的远程链接域名看起来可疑，先提醒风险，再由用户确认是否继续

## 交互动作
保留以下动作和默认决策，不要随意改变。

### 1. 创建漫游打印任务
触发条件：

- 用户说“打印这个文件/链接”
- 用户没有明确指定具体打印机

默认行为：

- 这是默认打印方式
- 不需要先查询打印机详情
- 需要根据打印机能力参数中的默认值设定初始打印参数，不要主动提示用户修改打印参数

执行步骤：
1. 如果输入是本地文件，先执行 `upload-file`
2. 然后创建漫游任务：
```bash
python scripts/mcp_client.py create-roaming-task --file-name "document.pdf" --url "https://any.webprinter.cn/files/abc123/document.pdf" --media-format PDF
```

### 2. 直接打印到指定设备
触发条件：

- 用户明确说“直接打印”
- 例如“直接打印”“用 XX 打印机打印”“直接打印到 XX”

执行步骤：
1. 先查询打印机列表：
```bash
python scripts/mcp_client.py query-printers
```
2. 如果用户指定的打印机模糊或不在打印机列表中，则列出所有可用打印机（过滤 `hidden=true` 的数据），请用户确认
3. 如果输入是本地文件，先上传
4. 当明确了打印机，并拿到文档 URL 后，再执行直接打印：
```bash
python scripts/mcp_client.py print-document --file-name "report.pdf" --url "https://any.webprinter.cn/files/abc123/report.pdf" --media-format PDF --device-name "HP LaserJet Pro" --control-sn "SERVER123456"
```

### 3. 查询打印机能力
只在用户明确提出时调用，例如：

- “查询打印机能力”
- “这台打印机支持彩色/双面/多份打印吗”

执行命令：
```bash
python scripts/mcp_client.py query-printer-detail --printer-name "HP LaserJet Pro" --share-sn "SERVER123456"
```

### 4. 更新打印参数
只在用户明确提出时调用。

修改单双面时，例如：

- “设置双面打印”
- “改单面打印”

执行命令：
```bash
python scripts/mcp_client.py update-printer-side --task-id "TASK_20240324_001" --side DUPLEX
```

支持值：

- `ONESIDE`
- `DUPLEX`
- `TUMBLE`

修改颜色时，例如：

- “改成彩色打印”
- “改成黑白打印”

执行命令：
```bash
python scripts/mcp_client.py update-printer-color --task-id "TASK_20240324_001" --color COLOR
```

支持值：

- `COLOR`
- `MONOCHROME`

修改份数时，例如：

- “打印 3 份”
- “改成 2 份”

执行命令：
```bash
python scripts/mcp_client.py update-printer-copies --task-id "TASK_20240324_001" --copies 3
```

支持值：

- `1-99`

修改纸张时，例如：

- “改成 A4”
- “纸张设成 A3”
- “设置纸张宽 210 高 297”

执行命令：
```bash
python scripts/mcp_client.py update-printer-paper --task-id "TASK_20240324_001" --paper-size A4
```

或：
```bash
python scripts/mcp_client.py update-printer-paper --task-id "TASK_20240324_001" --width 210 --height 297
```

内置纸型转换规则（单位：毫米）：

- `A3` -> `297 x 420`
- `A4` -> `210 x 297`
- `A5` -> `148 x 210`
- `B4` -> `250 x 353`
- `B5` -> `176 x 250`
- `LETTER` -> `215.9 x 279.4`
- `LEGAL` -> `215.9 x 355.6`
- `TABLOID` -> `279.4 x 431.8`

如果用户说的是纸型名称，优先自动转换成 `paper.width` 和 `paper.height` 后再调用接口。

## 核心规则
1. 用户未明确说“直接打印到指定设备”时，默认创建漫游打印任务
2. 只要是用户明确提供的可访问 HTTPS 文档链接，就直接使用原始链接，不主动下载或中转
3. 只有本地文件才需要先上传；远程链接不需要先下载再上传
4. `query-printer-detail`、`update-printer-side`、`update-printer-color`、`update-printer-copies`、`update-printer-paper` 仅在用户明确要求时调用
5. `update-printer-side` 只负责单双面；颜色和份数必须分别使用独立动作更新
6. 用户说 `A3`、`A4` 等纸型时，不要把纸型名称原样传给后端；先转换成毫米单位的 `paper.width` 和 `paper.height`
7. 在 WebPrinter 体系里，打印设备的唯一定位信息应以“打印机名称 + 服务端标识”为准；服务端标识可能表现为 `sn`、`shareSn` 或 `controlSn`，应结合接口返回字段使用

## 动作映射
| 用户表达 | 输入类型 | 调用动作 | 说明 |
| --- | --- | --- | --- |
| “上传这个文件” | 本地文件 | `upload-file` | 仅上传文件 |
| “打印这个链接：https://...” | URL 链接 | `create-roaming-task` | 默认进入漫游打印 |
| “打印这个文件”且未指定打印机 | 本地文件 | `upload-file` + `create-roaming-task` | 默认打印路径 |
| “用 XX 打印机打印” | 本地文件或 URL 链接 | `query-printers` + `upload-file`（仅本地文件）+ `print-document` | 直接打印到指定设备 |
| “查询打印机能力” | - | `query-printer-detail` | 按需调用 |
| “设置双面打印” | - | `update-printer-side` | 只更新单双面 |
| “改成彩色打印” | - | `update-printer-color` | 只更新颜色 |
| “打印 3 份” | - | `update-printer-copies` | 只更新份数 |
| “改成 A4” | - | `update-printer-paper` | 纸型先转宽高再更新 |

## 接口与命令
服务信息：

- 域名：`https://any.webprinter.cn`
- 认证方式：`Authorization: Bearer <token>`
- 环境变量：`WEBPRINTER_ACCESS_TOKEN`

### 1. 检查安装状态
- 路径：`POST /openapi/platform/checkInstallProgressMCP`
- 命令：
```bash
python scripts/mcp_client.py check-install-progress
```

### 2. 查询打印机列表
- 路径：`POST /openapi/control/queryPrinters`
- 命令：
```bash
python scripts/mcp_client.py query-printers
```

### 3. 上传本地文件
- 路径：`POST /openapi/mcpClient/uploadFileMCP`
- 命令：
```bash
python scripts/mcp_client.py upload-file --file-path "C:/path/to/document.pdf"
```

### 4. 创建漫游打印任务
- 路径：`POST /openapi/task/createRoamingTask`
- 命令：
```bash
python scripts/mcp_client.py create-roaming-task --file-name "document.pdf" --url "https://any.webprinter.cn/files/abc123/document.pdf" --media-format PDF
```

- 返回值是任务 ID 字符串，脚本会统一包装为：
```json
{
  "success": true,
  "taskId": "TASK_20240324_001"
}
```

### 5. 查询打印机能力
- 路径：`POST /openapi/control/queryPrinterDetail`
- 命令：
```bash
python scripts/mcp_client.py query-printer-detail --printer-name "HP LaserJet Pro" --share-sn "SERVER123456"
```

### 6. 更新单双面
- 路径：`POST /openapi/task/config/updatePrinterSideMCP`
- 命令：
```bash
python scripts/mcp_client.py update-printer-side --task-id "TASK_20240324_001" --side DUPLEX
```

### 7. 更新颜色
- 路径：`POST /openapi/task/config/updatePrinterColorMCP`
- 命令：
```bash
python scripts/mcp_client.py update-printer-color --task-id "TASK_20240324_001" --color COLOR
```

### 8. 更新份数
- 路径：`POST /openapi/task/config/updatePrinterCopiesMCP`
- 命令：
```bash
python scripts/mcp_client.py update-printer-copies --task-id "TASK_20240324_001" --copies 2
```

### 9. 更新纸张
- 路径：`POST /openapi/task/config/updatePrinterPaperMCP`
- 命令：
```bash
python scripts/mcp_client.py update-printer-paper --task-id "TASK_20240324_001" --paper-size A4
```

或：
```bash
python scripts/mcp_client.py update-printer-paper --task-id "TASK_20240324_001" --width 210 --height 297
```

### 10. 直接打印到指定设备
- 路径：`POST /openapi/task/directPrintDocumentMCP`
- 命令：
```bash
python scripts/mcp_client.py print-document --file-name "report.pdf" --url "https://any.webprinter.cn/files/abc123/report.pdf" --media-format PDF --device-name "HP LaserJet Pro" --control-sn "SERVER123456"
```

## 支持格式
`HTML`、`PNG`、`JPG`、`PDF`、`BMP`、`WEBP`、`WORD`、`EXCEL`、`PPT`、`TEXT`、`WPS`、`ODF`、`ODT`、`ODS`、`ODP`、`ODG`、`XPS`、`PWG`

## 错误处理
常见错误：

- `401`：令牌缺失或失效
- `403`：账户没有访问该资源的权限
- `404`：接口路径或资源不存在
- `5xx`：服务端异常

排查顺序：
1. 环境变量 `WEBPRINTER_ACCESS_TOKEN` 是否已配置
2. 链接是否是服务端可访问的有效 HTTPS URL
3. 文件路径是否真实存在且是文件
4. 打印机名称和 `control-sn` 是否来自 `query-printers` 的返回结果

## 资源
- 客户端脚本：`scripts/mcp_client.py`
