---
name: travel-expense-reimbursement
description: 自动化差旅费用报销流程，支持12306火车票、携程机票/酒店、华住会酒店、美团、吉祥航空、百望等电子发票的自动获取、解析和报销提交。支持邮件附件下载和链接下载两种发票获取方式。触发条件：用户提及差旅报销、火车票报销、12306发票、携程发票、华住会发票、酒店报销、机票报销、电子客票、美团发票、航空发票、百望发票等。
---

# 差旅费用自动报销助手

> 📊 完整流程图见 [`references/flowchart.md`](references/flowchart.md)，建议先阅读流程图了解整体流程。

## 一、能力范围

- **支持**：
  - 12306火车票电子客票
  - 携程机票电子行程单
  - 去哪网机票/酒店
  - 华住会酒店住宿发票
  - 美团发票（外卖、酒店、打车等）
- **功能**：读取邮箱、下载PDF附件/通过链接下载发票PDF、解析发票信息、生成报销数据、上传发票到FOL、提交差旅报销
- **发票获取方式**：
  - **附件下载**：邮件直接携带PDF附件，通过 himalaya/IMAP 下载
  - **链接下载**：邮件正文含发票链接，通过浏览器自动化访问并下载PDF
- **限制**：非发票类邮件会被过滤掉，但不会人为限制发票类型

## 二、依赖技能

| 技能/模块 | 用途 |
|------|------|
| **url_downloader.py** | 给定 URL，curl 优先下载 → Playwright 兜底（邮件正文中发票链接的下载） |
| **pdf-ocr** | PDF/图片OCR文字提取、发票信息解析 |
| **browser** | 浏览器自动化（仅用于 FOL 报销系统，发票上传和报销单提交） |
| **fol-invoice-upload** | FOL发票上传，通过浏览器自动化将发票PDF上传到财务系统并完成OCR识别 |
| **fol-travel-expense** | FOL报销申请，通过浏览器自动化创建国内差旅报销单并提交 |
| **himalaya** | 邮件搜索、下载附件（直接下载邮件中的 PDF/OFD 附件） |

## 三、全局执行规则

### 🚫 IMAP 严格串行规则（重要）

> **所有涉及 IMAP 连接的操作必须严格串行执行，禁止并发调用同一邮箱账号。**

- IMAP 连接是同步阻塞 IO，单连接串行操作最稳定
- 每次 `imaplib.IMAP4_SSL()` 操作完成后记得 `mail.logout()`
- 不需要在 exec 中设置特殊超时，Python imaplib 自己管理超时
- 如果 IMAP 连接超时或报错，立即切换到 himalaya CLI（最后备用）

### 🚫 OCR 严格串行规则

> **OCR 解析必须一张一张串行执行，禁止并发/并行调用多个 OCR 进程。**

RapidOCR 每进程需加载模型占用 350MB+ 内存，并行会导致内存暴涨触发 OOM Killer 杀死 gateway 进程。

## 四、执行步骤（严格按顺序执行）

### 步骤1：初始化工作目录

工作目录：`/tmp/openclaw/uploads/{session_id}/`（每次报销使用独立的动态子目录，如 `/tmp/openclaw/uploads/run-20260529-001/`）。

创建子目录：
```
/tmp/openclaw/uploads/{session_id}/
├── inbox/             # 所有发票PDF统一存放，不做分类子目录
├── processed/         # 已解析的发票数据
└── output/            # 生成的报销文件
```

> 动态目录命名规则：`run-{YYYYMMDD}-{序号}`，先检查 `/tmp/openclaw/uploads/` 下已有目录避免冲突。

### 步骤2：从邮箱搜索并下载邮件附件

**四步判断流程（严格按顺序执行）：**

#### 第一步：判断有无附件

通过 `himalaya envelope list` 获取今日邮件列表，根据发件人和主题过滤出发票邮件。
对每封邮件判断：`himalaya message read <msg_id>` 查看邮件结构，确认是否有 PDF/OFD 附件（`has_attachment: true` 的邮件）。

#### 第二步：有附件则下载附件

对有附件的邮件，执行：
```bash
himalaya attachment download <message_id> -d /tmp/openclaw/uploads/{session_id}/inbox/
```
附件直接落入 `inbox/`，标记该邮件处理完毕，跳过第三、四步。

#### 第三步：无附件则提取下载地址

对无附件的邮件，读取正文（`himalaya message read <msg_id>`），按以下优先级提取下载 URL：

1. **正则提取**：`re.findall(r'https?://[^\s"'\'<>]+', text)` 从 HTML 正文直接匹配 `http` 链接
2. **解析 MIME 结构**：用 Python `email` 模块解析原始邮件，对每个 part 的 `text/html` 或 `text/plain` 内容深度扫描 URL
3. **按钮文字识别**：若正文仅含"下载PDF文件"等按钮文字而无真实链接，标记为**链接不可提取**，进入第四步

常见发件人 URL 特征：
- 百望：`pis.baiwang.com/smkp-vue/previewInvoiceAllEle?param=`
- 吉祥航空：`einvoice@juneyaoair.com` / `www.juneyaoair.com/eflight/invoice`
- 深圳航空：百望链接（同百望逻辑）

#### 第四步：下载无附件情况的发票 PDF

调用 `url_downloader.py` 下载：
```python
import sys
sys.path.insert(0, '/app/skills/travel-expense-reimbursement/references')
from url_downloader import download_file

filepath = download_file(
    url='<提取到的URL>',
    save_dir='/tmp/openclaw/uploads/{session_id}/inbox/',
    filename_hint='invoice.pdf',
)
```

**下载策略（curl 优先，Playwright 兜底）：**
```
curl 直接下载
  ↓ 失败（超时/非PDF响应）
Playwright 访问页面
  → 页面直接触发 PDF 下载？拦截保存
  → 未触发？查找并点击下载按钮
  → 找到 PDF 直链？curl 下载
  → 全部失败 → 截图备用，告知用户手动下载
```

**扩展新的发票下载类型**（在 `url_downloader.py` 中添加 handler）：
```python
def download_myinvoice(page_url: str, save_dir: str) -> Optional[str]:
    return download_file(page_url, save_dir)

URL_PATTERN_HANDLERS.append((
    'https://myinvoice.example.com/',
    download_myinvoice,
))
```

> ⚠️ **吉祥航空特别说明**：部分吉祥航空邮件正文中的"下载PDF文件"仅为文字按钮，非真实超链接。若第二步和第三步均无法获取真实下载地址，应告知用户手动从吉祥航空App或官网下载发票附件后发送至邮箱。

### 步骤4：OCR解析发票

**批量解析：所有 PDF 一次性完成，不逐张调用。**

```python
import sys
import os
import glob
sys.path.insert(0, '/app/skills/pdf-ocr-skill/scripts')
from pdf_ocr_processor import PDFOCRProcessor

inbox_dir = '/tmp/openclaw/uploads/{session_id}/inbox/'
pdf_files = sorted(glob.glob(os.path.join(inbox_dir, '*.pdf')))

processor = PDFOCRProcessor(engine='rapid')
results = []
for pdf_path in pdf_files:
    result = processor.ocr_pdf(pdf_path)
    results.append({
        'pdf_path': pdf_path,
        'filename': os.path.basename(pdf_path),
        'text': result['text'],
        'page_count': result['page_count']
    })
    print(f"[OK] {os.path.basename(pdf_path)} ({result['page_count']}页)")

# 输出汇总供后续步骤使用
import json
print('\n=== OCR_RESULTS_JSON ===')
print(json.dumps(results, ensure_ascii=False))
```

- 批量解析完成后，所有发票的 OCR 文本在 `results` 列表中，进入步骤5汇总
- 不再逐张调用 pdf-ocr，所有 PDF 在**一条 exec 命令**内全部完成

### 步骤5：发票信息汇总

1. 按时间排序，生成 `/tmp/openclaw/uploads/{session_id}/processed/invoice-list.json`
2. 向用户展示发票汇总表（表格形式）：类型、发票号码、行程/内容、日期、金额、姓名
3. 标注总金额
4. 明确说明过滤掉的非目标人员发票

### 步骤6：行程分析

依据 `references/行程分析指南.md` 分析行程，先自行分析整理，遇到不确定的再问用户。

### 步骤7：确认报销参数（记忆 + 交互式）

以下参数从发票自动推断，不需要问用户：
- 出发/出差城市、交通方式、住宿天数、附件路径等

**只需要确认两个参数**：报销事由和项目名称。

#### 7.1 读取记忆

通过 `memory_search` 搜索历史报销记忆，关键词：`报销 项目名称`、`差旅报销 事由`

#### 7.2 确认参数

向用户一次性确认：
```
请确认：
- 报销事由：出差（记忆中最常用）/ 或用户输入
- 项目名称：????（历史曾用：A、B、C）/ 或用户输入新项目
```

其余参数不询问，从发票自动填充。

#### 7.3 写入记忆

用户确认后，只将**事由和项目名称**写入 `memory/YYYY-MM-DD.md`：
```markdown
## 差旅报销 (当日日期)

- 事由: XXX
- 项目名称: XXX
```

### 步骤8：上传发票到FOL

调用 `fol-invoice-upload` 技能，**一次性批量上传所有发票PDF**（不要逐张上传）。

收集所有待上传发票的文件路径列表，一次性传递给上传流程（如果上传流程支持批量），或尽可能连续快速上传减少等待。

发票文件路径使用 `/tmp/openclaw/uploads/{session_id}/inbox/` 下的文件。

### 步骤9：提交报销

调用 `fol-travel-expense` 技能，按行程分段提交报销单。

### 步骤10：输出结果

向用户展示：处理发票数、总金额、行程汇总、提交状态。

## 五、错误处理

| 错误 | 处理 |
|------|------|
| **第一步**判断失误/邮件获取失败 | 降级到 Python imaplib 直连获取 |
| **第二步** himalaya 下载附件失败 | 降级到 Python imaplib 直连 |
| **第三步** 无法提取下载地址（按钮文字非链接） | 告知用户手动从发件方官网/App下载，询问是否上传PDF |
| **第三步** 正则提取 URL 失败 | 尝试 Python `email` 模块深度解析 MIME 结构 |
| **第四步** url_downloader curl 失败 | 自动切换 Playwright 浏览器方案 |
| **第四步** Playwright 仍失败（超时/需登录/验证码） | 截图备用，告知用户该链接无法自动下载，询问是否手动上传PDF |
| PDF解析失败 | 保留文件，继续处理其他的 |
| 发票类型无法识别 | 记录到待处理，提示用户 |
| fol-invoice-upload 失败 | 记录失败发票，提示手动上传 |
| fol-travel-expense 失败 | 保存数据，提示手动提交 |

## 六、支持的邮箱发件人

| 发票类型 | 搜索关键词（from） | 主题特征 | 发票获取方式 |
|---------|-------------------|---------|------------|
| 12306火车票 | 12306 | "电子发票通知" | 邮件附件 |
| 携程机票/酒店 | trip | "机票"/"行程单"/"航班"/"酒店"/"住宿" | 邮件附件 |
| 去哪网机票/酒店 | qunar | "机票"/"行程单"/"航班"/"酒店"/"住宿" | 邮件附件 |
| 华住会酒店 | huazhuhotel | "发票"/"电子发票" | 邮件附件 |
| 美团发票 | meituan | "发票"/"电子发票" | 邮件附件 |
| 吉祥航空机票 | juneyaoair | 航空/行程单/发票 | url_downloader.py（curl 直链，失败切 Playwright） |
| 百望发票 | baiwang | 发票/电子发票 | url_downloader.py（GreenPaper 跨域 iframe，截图备用；建议手动下载 PDF 上传） |
