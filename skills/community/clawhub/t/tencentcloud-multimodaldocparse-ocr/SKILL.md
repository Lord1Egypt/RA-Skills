---
name: tencentcloud-ocr-multimodaldocparse
description: 腾讯云多模态解析（文档版）(MultimodalDocParse) 技能包。当用户提供文档 URL 地址时，应自动调用多模态解析（文档版）接口提取文档内容信息。支持 PDF、Word、PPT、Excel、Markdown、TXT、图片、WPS 等多格式文档解析；可配置页码范围、子图解析、任务类型、输出格式等可选参数；接口返回 ZIP 格式结果包下载地址，包内含结构化解析结果（*.md / *.xml / *_ocr_page{N}.json）及文档内提取的图片素材（images/）。结果包的真实结构与字段说明详见 references/result-package-structure.md。
---

# 腾讯云多模态解析（文档版）(MultimodalDocParse)

## 用途

调用腾讯云多模态解析（文档版）接口，对多种类型的文档文件进行智能解析，返回结构化结果。

核心能力：
- **多格式文档解析**：支持 PDF、Word、PPT、Excel、Markdown、TXT、图片、WPS 等 8 种文档类型
- **可配置解析范围**：支持页码范围（PageRange）裁剪，单次最多 300 页
- **多任务类型**：文档解析 / 图片 OCR / 切片文字识别 / 切片表格识别 / 切片代码识别
- **多输出格式**：json / markdown / xml / 三合一
- **子图解析**：可选开启子图识别（EnableSubImg）
- **ZIP 结果包**：接口返回 ZIP 临时下载地址，脚本支持自动下载落盘

官方文档：https://cloud.tencent.com/document/product/866/133224

## 📚 可用资源

### References（场景化指引）
- `references/result-package-structure.md` - **结果包 ZIP 的真实结构与字段说明**（实测，非文档转述）。需要解析 ZIP 内容、取元素坐标、做页码对齐时**必读**

### Scripts（脚本入口）
- `scripts/main.py` - 核心：CLI 封装（参数校验、SDK 调用、ZIP 下载、错误码建议）

## 使用时机

当用户提出以下需求时触发此技能：
- **用户提供了文档 URL**（如 `https://xxx.com/report.pdf`、`https://xxx.cos.xxx/合同.docx` 等），需要解析其中的内容
- 用户说"解析这个文档"、"提取文档内容"、"文档转 markdown"、"多模态解析"、"文档智能解析"等表达
- 需要从 PDF、Word、PPT、Excel、Markdown、TXT、图片、WPS 等多格式文档中提取结构化内容
- 涉及合同/发票/研报/论文/简历等多格式文档智能解析的任何场景
- 需要将文档转换为 markdown/json 进行二次加工
- 需要批量提取文档内嵌图片素材

### 🤖 自动触发指引（面向大模型）

当检测到以下信号时，应**自动调用**此技能，无需用户显式要求"多模态解析"：

1. **用户消息中包含文档URL**：检测到 `http(s)://` 开头且以文档扩展名（`.pdf`、`.doc`、`.docx`、`.ppt`、`.pptx`、`.xls`、`.xlsx`、`.md`、`.txt`、`.wps`、图片类 `.png/.jpg/.jpeg` 等）结尾的URL
2. **用户上传/粘贴了文档文件**：对话中出现了 PDF/Word/PPT/Excel 等文档附件
3. **用户意图关键词**：消息中包含"解析文档"、"提取内容"、"文档转结构化"、"多模态解析"、"文档版OCR"等与文档智能解析相关的表达

**调用方式**：
- 用户提供的是 URL，直接使用 `--file-url` 参数传入
- 用户上传的是本地文件，需先上传到可访问的存储（如腾讯云 COS）拿到 URL 后再传入

### 🎯 识别类型选择（调用前必读）

先按用户请求提取识别意图，再决定是否传 `--task-type` / `--result-type` 等参数：

1. **意图 → 参数映射**（命中即带参调用）：
   - "转 markdown / 要全文 / 文档转 md" → `--result-type 2`
   - "识别里面的表格 / 表格数据化" → `--task-type 3`
   - "提取文字 / OCR 这张图 / 扫描件文字" → `--task-type 1`（图片场景）
   - "只要结构化 JSON" → `--result-type 1`
   - 明确只要某几页 → `--page-range 开始页-结束页`（如 `1-10`）
2. **意图不明时先问，不要默认跑**：用户请求与以上意图都不匹配，或结果格式会影响后续用途（如"我要拿来对比数字"与"我要全文阅读"输出不同）时，先抛选择题问清**识别方式**（文档解析/图片OCR/切片表格/切片代码）与**输出格式**（json/md/xml/全要），等用户回答后再调用。
3. **用户已明确则直接执行**：用户明确说了"转成 md"、"识别表格"等指令时不要反问，直接带对应参数调用；用户只说"解析这个文档"且无更多要求时，按默认（文档解析 + 三合一）执行。

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成文档解析。脚本使用 SDK 高层接口 `client.MultimodalDocParse(req)` 进行调用，具有类型安全和自动反序列化的优势。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| FileUrl | str | 是 | 待解析文档的 URL 地址，支持 HTTP/HTTPS；文件下载时间不超过3秒，**建议文件存储于腾讯云 COS/CDN 以保障下载速度和稳定性** |
| FileType | int | 否(推荐) | 文件类型。0=未知 1=PDF 2=Word 3=PPT 4=Excel 5=Markdown 6=TXT 7=图片 8=WPS；**不传时脚本会按 URL 扩展名自动推断；API 服务端默认 1=PDF** |
| ResultType | int | 否 | 输出格式。1=json 2=markdown 3=xml 9=json+markdown+xml（三合一）；API 默认 9 |
| EnableSubImg | bool | 否 | 是否开启子图解析，默认 false |
| PageRange | str | 否 | 页码范围，格式 `开始页-结束页`，单次调用最多 300 页；仅对 PDF/Word/PPT 有效，例如 `1-10` |
| TaskType | int | 否 | 任务类型。0=文档解析 1=图片OCR识别 2=切片文字识别 3=切片表格识别 4=切片代码识别；默认 0 |
| **UserAgent** | **str** | **否** | **请求来源标识(可选)，用于追踪调用来源，统一固定为`Skills`** |

### ⚠️ UserAgent参数使用指南

**`--user-agent`参数是可选参数**，统一固定为`Skills`，无需手动传递。用于标识API调用来源，便于追踪和统计：

| 调用框架 | --user-agent 参数值 | 说明 |
|---------|--------------|------|
| 所有框架 | `Skills` | 统一固定值，不传递时也默认为此值 |

**实现说明**：
- 通过`--user-agent`命令行参数传递，SDK 会将其拼接为 `SDK_PYTHON_x.x.x; Skills` 注入到请求中
- 统一固定为`Skills`，未传递时也默认为此值
- 该标识会记录在ES日志的 `ReqBody.RequestClient` 字段中，可用于追踪来源

### ⚠️ 参数使用要点

**1. FileType 建议显式传入**

FileType 在 API 文档中标为"否"，但 **API 默认值 = 1（PDF）**。传 Word/PPT 等非 PDF 文件却不显式传 FileType，会被错误地按 PDF 处理。

脚本策略：显式传 `--file-type` 时透传；未传时按 URL 扩展名自动推断（`.pdf→1, .doc/.docx→2, .ppt/.pptx→3, .xls/.xlsx→4, .md→5, .txt→6, 图片→7, .wps→8`）；推断不出则**不传递**该参数并打印警告，此时请显式传参。

**2. PageRange 的入参与输出页码基准差 1**

| 方向 | 基准 | 说明 |
|------|------|------|
| `PageRange` 入参 | **1-based** | `2-3` 表示人眼看到的「第 2 页到第 3 页」 |
| 结果包 `page-number` / `ocr_pageN.json` | **0-based** | 第 2 页 → `page-number=1`、`ocr_page1.json` |

即 **输出索引 = 输入页码 − 1**。格式必须为 `开始页-结束页`（不支持 `1,3,5` 这类离散页码），单次最多 300 页，仅对 PDF/Word/PPT 有效。

**3. 接口是同步阻塞的，约 30 秒硬超时**

超时返回 `FailedOperation.EngineRecognizeTimeout`，**无异步任务 ID 可轮询**，超时即本次调用作废（仍会计费）。大文档务必配合 `--page-range` 分批（建议每批 ≤ 10 页），并谨慎开启 `--enable-sub-img`（子图解析会显著拉长耗时）。

### 输出格式

调用成功且未启用下载时返回 JSON：

```json
{
  "ResultUrl": "https://example.com/result.zip",
  "RequestId": "xxx",
  "ExpiresIn": "30分钟"
}
```

启用 `--download` 时返回：

```json
{
  "ResultUrl": "https://example.com/result.zip",
  "RequestId": "xxx",
  "ExpiresIn": "30分钟",
  "downloaded_to": "/path/to/multimodal_results/result.zip"
}
```

**ZIP 包内容（实测确认）**

包内文件名统一以 `{任务哈希}` 为前缀（同一批结果共享同一前缀）：

| 文件 | 产生条件 | 说明 |
|------|---------|------|
| `{hash}_md_full.md` | `--result-type` 含 md（2/9） | Markdown 全文，按页用 `<!-- "type": "page-number", "value": N -->` 分隔 |
| `{hash}_xml_full.xml` | `--result-type` 含 xml（3/9） | XML 全文，节点带 `page-numbers` 属性 |
| `{hash}_ocr_page{N}.json` | `--result-type` 含 json（1/9） | **每页一个文件**，`N` 从 0 开始 |
| `images/imgParseSvr_img_{id}_{i}.png` | 文档内含图片时 | 抽出的图片素材 |

⚠️ 注意两点实测结论：

1. **`--result-type` 是"选择"而非"累加"**——它直接决定产出哪些文件，不是叠加输出。`2`（仅 md）就只出 `_md_full.md`，不会附带 json/xml。
2. **即使 `--enable-sub-img false`，文档里的图片仍会被抽出**并保存进 `images/`，且图片内的文字会被识别、内联进 md 的 `<image>` 标签中。

各格式的完整字段结构、坐标系缩放规则见 `references/result-package-structure.md`。

> ⚠️ ResultUrl 是**一次性临时链接**（官方标注 30 分钟有效），接口无任务 ID、丢失后无法二次查询，务必用 `--download` 立即落盘。

### 调用示例

```bash
# 1. 基础调用：解析 PDF 文档（自动从 .pdf 扩展名推断 FileType=1）
python scripts/main.py --file-url "https://example.com/document.pdf"

# 2. 解析 Word 文档（按 .docx 扩展名自动推断 FileType=2）
python scripts/main.py --file-url "https://example.com/report.docx"

# 3. 显式指定 FileType，规避扩展名推断不到的情况
python scripts/main.py --file-url "https://example.com/contract" --file-type 2

# 4. 多页 PDF 仅解析第 1-10 页
python scripts/main.py --file-url "https://example.com/long.pdf" --page-range 1-10

# 5. 输出 markdown 格式 + 自动下载结果包
python scripts/main.py --file-url "https://example.com/paper.pdf" \
  --result-type 2 --download --output-dir ./results

# 6. 任务类型：图片OCR识别（适用于扫描件）
python scripts/main.py --file-url "https://example.com/scan.png" \
  --file-type 7 --task-type 1

# 7. 任务类型：切片表格识别（适用于财务报表）
python scripts/main.py --file-url "https://example.com/finance-report.pdf" \
  --task-type 3

# 8. json+markdown+xml 三合一输出
python scripts/main.py --file-url "https://example.com/full.pdf" --result-type 9
```

## 密钥配置（新用户从零到跑通）

> ⚠️ 脚本**只认两个环境变量** `TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY`（见 `scripts/main.py` 的 `validate_env`），读不到就退出、无任何配置文件兜底。首次运行报 `错误: 请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY` 时，按下面 ①→④ 走一遍即可。

### ① 申请 API 密钥（CAM 控制台）

1. 打开 🔗 **[腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)**（需主账号或有 CAM 权限的子账号）。
2. 点「新建密钥」，生成一对 `SecretId`（AKID 开头）+ `SecretKey`。
3. ⚠️ 子账号若报权限不足，需主账号在 CAM 里给其授权 `QcloudOCRFullAccess`。

### ② 开通服务（不开通会报 `FailedOperation.UnOpenError`）

打开 🔗 **[腾讯云文字识别 OCR 购买页](https://buy.cloud.tencent.com/iai_ocr)**，按以下导航选到目标产品：

| 步骤 | 选择项 |
|------|--------|
| 产品大类 | **文字识别**（默认页） |
| 服务类别 tab | **文档智能**（共 8 个 tab，注意不要选错） |
| 接口名称 | **多模态解析（文档版）**（蓝色高亮即选中，描述里带「PDF/Word/PPT/Excel/图片」多格式） |

⚠️ 关键：OCR 是个产品族，**通用 OCR 开通不算**。本页最容易踩的坑是在「通用文字识别」下选完即关页面——`多模态解析（文档版）` 是「文档智能」类目下的独立 SKU，必须在此处单独点选并完成购买。

计费方式选「资源包」或「并发买断包」按需即可（按量付费默认包内）。

### ③ 配置密钥（三选一，按安全度排序）

**方式 A：临时注入（最安全，用完即消，仅当前终端生效）**
```bash
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
```

**方式 B：600 权限文件 + source（推荐，防命令行留痕）**
```bash
printf 'export TENCENTCLOUD_SECRET_ID="你的SecretId"\nexport TENCENTCLOUD_SECRET_KEY="你的SecretKey"\n' > ~/.tc_ocr_cred
chmod 600 ~/.tc_ocr_cred
source ~/.tc_ocr_cred        # 每次新开终端需重新 source
```

**方式 C：写进 shell 配置（一劳永逸，但密钥明文落盘，谨慎使用）**
```bash
echo 'export TENCENTCLOUD_SECRET_ID="你的SecretId"' >> ~/.bashrc
echo 'export TENCENTCLOUD_SECRET_KEY="你的SecretKey"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell)：**
```powershell
$env:TENCENTCLOUD_SECRET_ID = "你的SecretId"
$env:TENCENTCLOUD_SECRET_KEY = "你的SecretKey"
```

### ④ 验证跑通

拿到真实密钥后，先用最小验证确认链路通：

```bash
python scripts/main.py --file-url "<一个可公开访问的小PDF的URL>" --download
```

成功返回含 `ResultUrl` / `RequestId` / `ExpiresIn` 的 JSON 即链路通。

⚠️ **不要**把密钥直接敲在命令行历史里，请用方式 A 或 B；临时文件用完删除。

### 🤖 面向大模型的引导

当脚本因缺密钥退出（stderr 含「请设置环境变量 TENCENTCLOUD_SECRET_ID」）时，**不要只转发报错**：应把本节「① 申请 → ② 开通 → ③ 配置 → ④ 验证」完整路径主动贴给用户，引导其完成配置后重跑；若用户已有密钥（如存在某台机器或内部文档里），可直接询问位置，不要让其重新申请。
