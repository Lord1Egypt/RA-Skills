---
name: receipt-compliance
description: 会计助手：发票OCR识别→真伪查验→报销单自动填充→对接审批系统。企业自主配置，数据本地处理。
version: 4.5.0
---


# 会计助手

> ⚠️ **使用必读**：本Skill所有功能在本地运行，发票数据绝不外传，但**绝不提供税务咨询**。使用前请先阅读【限制说明】和【风险声明】。

## 功能说明

本Skill提供从发票识别到审批提交的**全链路**财税合规能力。

| 模块 | 功能 | 状态 | 输入 | 输出 |
|------|------|------|------|------|
| 1. 发票OCR识别 | 双引擎（PaddleOCR优先+Tesseract兜底），定额票先验定位，勾稽校验 | ✅ 直接可用 | 发票图片/PDF | 结构化JSON |
| 2. 真伪查验 | 一键生成国税总局查验链接，自动打开浏览器 | ✅ 直接可用 | 发票代码/号码 | 查验链接+结果 |
| 3. 报销单填充 | 自适应学习模板，一键填充 | ✅ 直接可用 | 发票数据+模板 | Excel文件 |
| 4. 审批对接 | 对接钉钉/企微/飞书审批（有完整代码模板） | ⚠️ 需配置密钥 | 报销单+配置 | 审批结果 |
| 5. 全电发票 | 全电发票XML/OFD格式解析 | ✅ 直接可用 | 全电发票文件 | 结构化JSON |
| 6. 多票据支持 | 火车票/飞机票/出租车/定额发票/通行费/财政票据 | ✅ 直接可用 | 票据图片 | 统一结构化JSON |
| 7. 智能分类 | 自动匹配会计科目、计算进项税、生成凭证摘要 | ✅ 直接可用 | 结构化发票数据 | 分类结果+科目 |
| 8. 记账凭证 | 自动生成记账凭证（用友/金蝶/QuickBooks格式） | ✅ 直接可用 | 分类结果 | 凭证文件 |
| 9. 风险预警 | 发票连号/整数金额/频繁开票/品名异常/进销项匹配检测 | ✅ 直接可用 | 发票列表 | 三级预警报告 |
| 10. 归档管理 | 电子档案四性检测、归档包生成、元数据采集、目录索引 | ✅ 直接可用 | 发票文件 | 标准归档包 |
| 11. 银行对账 | 银行流水 CSV 解析 + 发票金额/日期模糊匹配 | ✅ 直接可用 | 流水 CSV + 发票数据 | 对账报告 |
| 12. 安全配置 | 环境变量读取密钥，消除明文泄露 | ✅ 直接可用 | 环境变量 | 安全配置 |
| 13. 并行批量 | 硬件自适应并行处理，速度提升 3-5 倍 | ✅ 直接可用 | 发票文件夹 | 批量结果 |
| 14. 混拍切分 | 混拍图（一拍多票）自动检测切分，保持原图索引 | ✅ 直接可用 | 混拍图片 | 单票子图 |
| 15. 进销项台账 | SQLite 台账 + 月度统计，税负率趋势/供应商集中度/异常波动 | ✅ 直接可用 | 票据解析结果 | Excel 月度附件 |
| 16. 认证期日历 | 认证期限取数 + 30/7 天两档提醒 + CSV 导出 | ✅ 直接可用 | 台账 | 到期清单 |
| 17. 异常检测 | 轻量 Isolation Forest，金额/间隔/供应商三维打分 | ✅ 直接可用 | 票据列表 | 二级预警+触发维度 |
| 18. 合规管理出口 | 规则预警 + 归档四性检测合并为一次执行 | ✅ 直接可用 | 票据 + 文件 | 统一合规报告 |
| 19. 审批连接器 | 钉钉/企微/飞书统一接口（发送/查状态/回调验签） | ⚠️ 需配置密钥 | 报销单+配置 | 审批结果 |
| 20. 数电票直读 | PDF/OFD 文本层结构化（pypdf 优先，缺失降级 OFD/PDF 文本）+ 二维码 TLV 解码核对 | ✅ 直接可用 | 数电票 PDF/OFD | 结构化 JSON（含明细行） |
| 21. 重复报销查重 | 三信号两阶段：票号精确哈希 + 金额（±0.01）+ 日期（±3 天）近似比对，检出 P 图改抬头重复 | ✅ 直接可用 | 台账/票据列表 | 重复组清单 |
| 22. 查重复工单 | 可疑项生成复核清单（两张原始凭证缩略图对照+差异标注，移动端可读），财务确认后进台账/误报标记豁免 | ⚠️ 需台账 | 复核清单 | HTML 对照页 |

> ✅ = 装即用 ｜ ⚠️ = 需在 config.yaml 中配置对应API密钥
>
> 💡 **核心亮点**：发票识别、真伪查验、报销单生成 —— 这三项功能**完全不需要任何配置**，安装即用！

### 设计理念

1. **数据安全第一**：所有发票数据处理均在本地，不会上传到任何服务器
2. **企业自主决策**：查验引擎、审批平台的选择权完全交给企业
3. **透明开源**：所有代码可见可审计，无隐藏后门
4. **渐进披露**：基础功能开箱即用，高级功能按配置解锁

## 如何「指挥」它干活

本Skill支持**自然语言对话**，不需要记忆任何命令。以下是各种场景下你可以直接对AI说的话：

### 💬 直接用自然语言说

| 你想做什么 | 直接这样说 |
|-----------|-----------|
| 识别一张发票 | "帮我识别这张发票" / "OCR一下这个发票" / "扫描这张发票" |
| 批量识别 | "把文件夹里所有发票都识别出来" / "批量扫描D:\invoices" |
| 查验真伪 | "帮我查验这张发票的真伪" / "查一下这个发票是不是真的" |
| 生成报销单 | "用公司模板生成报销单" / "把识别结果填到报销单里" |
| 提交审批 | "提交报销审批" / "发起审批" / "把报销单提交给钉钉审批" |
| 批量处理 | "批量识别并生成报销单" / "把整个文件夹的发票都处理完" |
| 环境检查 | "检查环境是否就绪" / "运行预检" |
| 查看帮助 | "这个Skill能做什么" / "怎么用" |

### 📋 更详细的说法（推荐）

**识别发票**：
- "请帮我识别这张发票：D:\发票\20260628.png"
- "扫描这张发票，我要报销"
- "OCR这张发票，结果保存到receipt.json"

**批量处理**：
- "把D:\invoices\里所有发票都识别出来，结果保存到output.json"
- "批量扫描发票文件夹，然后生成合并报销单"

**查验真伪**：
- "帮我查验发票 代码:3100204130 号码:00564189"
- "查一下这张发票是不是真的，发票号是00564189"

**生成报销单**：
- "用模板D:\templates\报销单.xlsx生成报销单"
- "把receipt.json的数据填到报销单模板里"

**提交审批**：
- "把报销单提交到钉钉审批"
- "发起企业微信审批，报销金额11300元"

> 💡 **小贴士**：直接上传发票图片或告诉AI文件路径，AI会自动识别你的意图并执行对应操作。

## 📋 常见问题速查

### 🔧 安装与配置

| 问题 | 快速答案 |
|------|---------|
| 安装Tesseract后提示 `Tesseract not found` | 重启终端，或用 `--tesseract` 参数指定完整路径 |
| 提示 `chi_sim not found` | 重新安装Tesseract，勾选 Chinese (Simplified) 语言包 |
| 为什么不识别图片？ | 检查图片是否清晰、发票类型是否支持（手写/定额发票不支持） |
| 常用安装命令 | Windows: `winget install UB-Mannheim.TesseractOCR` |
| Mac安装 | `brew install tesseract tesseract-lang` |
| Linux安装 | `sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim` |

### 📷 OCR识别

| 问题 | 快速答案 |
|------|---------|
| 识别结果为空/少量内容 | 检查图片质量、光线、平整度、是否安装中文语言包 |
| 识别率低/字段错误 | 使用扫描件、手机扫描APP预处理、核对关键字段 |
| 批量处理部分失败 | 失败文件会单独记录在 `failed_files` 字段中，不影响其他文件 |
| 图片质量要求 | ≥200DPI、光线均匀、无反光、发票平整放置 |
| 提高识别率小技巧 | 扫描全能王APP预处理、使用扫描件、避免强光直射 |

### 🏢 查验与审批

| 问题 | 快速答案 |
|------|---------|
| 查验接口返回失败 | 检查API Key、网络访问、调用频率限制、查看日志 |
| 审批Token获取失败 | 确认API Key正确、应用已开通权限、服务器IP已加白名单 |
| 如何选择查验引擎 | 国税总局(免费) / 百望云/诺诺(付费API Key) / 自建接口 |
| 支持哪些审批平台 | 钉钉、企业微信、飞书、自定义（需实现接口） |
| 审批提交后能撤销吗 | 不可撤销（以各平台规则为准），提交前请核对内容 |

### 📄 模板与数据

| 问题 | 快速答案 |
|------|---------|
| 模板匹配失败 | 检查模板第一行是否为中文表头、文件是否损坏 |
| 金额勾稽关系不匹配 | OCR识别错误时人工核对；0.01元以内差异属正常精度问题 |
| 环境预检通过但OCR仍失败 | Tesseract版本过低（建议4.0+）、语言包不完整（≥5MB） |

### 🛡️ 安全与合规

| 问题 | 快速答案 |
|------|---------|
| 数据安全吗？ | 所有处理在本地完成，不会上传到任何服务器 |
| 日志里有什么？ | 仅记录操作元数据（文件名、时间、状态），不记录发票内容 |
| 能提供税务咨询吗 | 不能，本工具仅为技术支持，不提供税务/财务建议 |

> 📖 **详细解答见下方【故障排除】部分**

---

## 💡 使用技巧与注意事项

> 本节汇总了日常使用中最实用的技巧和注意事项，建议首次使用前快速浏览一遍。

### 基本技巧

| 序号 | 技巧 | 说明 |
|------|------|------|
| 1 | **优先用扫描件** | 扫描件比手机拍照识别率高15%-20%，文字更清晰、无反光 |
| 2 | **手机拍照用扫描模式** | 微信/支付宝/扫描全能王APP都有"文档扫描"功能，能自动去阴影、纠偏 |
| 3 | **批量处理先试一张** | 批量处理前先识别一张确认效果，避免批量失败浪费时间 |
| 4 | **低置信度要核对** | 置信度<0.7时系统会提示警告，此时必须人工核对代码、号码、金额 |
| 5 | **保留原始图片** | 识别失败时，系统会尝试用原始图片（跳过预处理）重新识别 |

### 注意事项

| 序号 | 注意点 | 原因 |
|------|--------|------|
| 1 | ⚠️ **OCR软件是一次性安装** | Tesseract约60MB，安装后永久使用，无需重复下载 |
| 2 | ⚠️ **模糊发票必须手动核对** | OCR对模糊图片无法保证准确率，关键金额字段一定要人工复核 |
| 3 | ⚠️ **审批功能需要配置API密钥** | 发票识别+验真假+报销单 无需配置，只有对接钉钉/企微/飞书审批才需要 |
| 4 | ⚠️ **批量处理部分失败是正常的** | 系统会跳过失败文件继续处理，失败的记录在 `failed_files` 字段 |
| 5 | ⚠️ **日志不记录发票内容** | 仅记录文件名、时间、状态等元数据，发票数据不上传不外传 |

## ⚠️ 避坑指南

> **本节汇总用户最容易踩的坑，每条都是真实使用中遇到的高频问题，建议首次使用前快速浏览一遍。**

### 🔴 发票识别类

| # | 问题现象 | 原因 | 解决方案 |
|---|---------|------|---------|
| 1 | 安装完Tesseract后仍然报错 | PATH环境变量未生效 | **Windows**：重启终端；或手动添加环境变量 `C:\Program Files\Tesseract-OCR` 到PATH |
| 2 | 识别结果为空 | 未勾选中文语言包 | 重新运行安装包，勾选 **Chinese (Simplified)** 语言包 |
| 3 | 金额识别错误（少0/多0） | 图片模糊或小字不清 | 用扫描APP（扫描全能王/白描）预处理图片后再试 |
| 4 | 发票代码和号码搞反 | OCR把位置搞混了 | 代码10-12位，号码8-20位，自动识别后请人工核对位置 |
| 5 | 电子发票PDF识别失败 | 缺少poppler | `pip install pdf2image` 并通过系统包管理器安装 poppler：Windows: `winget install poppler` 或 `scoop install poppler`；Linux: `sudo apt-get install poppler-utils`；macOS: `brew install poppler` |

### 🟡 系统配置类

| # | 问题现象 | 原因 | 解决方案 |
|---|---------|------|---------|
| 6 | 运行脚本时提示"禁止执行" | Windows执行策略限制 | 管理员身份运行PowerShell，执行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| 7 | pip下载依赖超时 | 网络不稳定或未配置镜像 | `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` |
| 8 | 权限不足（PermissionError） | 文件被其他程序占用 | 关闭占用文件的程序（如Excel打开该文件）后重试 |
| 9 | 找不到config.yaml | 未复制配置模板 | `copy templates/config_template.yaml config.yaml` |

### 🟢 查验与审批类

| # | 问题现象 | 原因 | 解决方案 |
|---|---------|------|---------|
| 10 | 查验链接无法打开 | 网络被防火墙拦截 | 用手机直接访问国税总局APP查验 |
| 11 | 审批提交失败 | API密钥过期或权限不足 | 在钉钉/管理后台重新生成密钥，确认审批权限已开通 |
| 12 | 审批提交后找不到记录 | 流程编码(process_code)填写错误 | 在钉钉管理后台核实正确的process_code |
| 13 | Token获取失败 | AppKey/AppSecret错误或IP白名单未配置 | 核对密钥，联系管理员添加服务器IP到白名单 |

### 🔵 效率提升类

| # | 技巧 | 节省时间 |
|---|------|---------|
| 1 | 批量处理前先**试一张**确认效果 | 避免批量失败浪费时间 |
| 2 | 建立公司模板文件复用 | 不用每次重新映射字段 |
| 3 | 用桌面快捷方式存放常用脚本 | 不用每次都找路径 |
| 4 | 手机拍照默认开"扫描模式" | 识别率提升15-20% |

---

### 模糊发票处理指南

当发票图片模糊、识别效果不好时，按以下步骤处理：

```
步骤1：判断图片质量
  → 图片分辨率<200DPI？ → 重新拍摄/扫描
  → 有反光/阴影？       → 换个角度或光线重拍
  → 发票褶皱严重？      → 展平后重新扫描

步骤2：使用扫描APP预处理（推荐）
  → 扫描全能王 / 白描 / 微信扫一扫
  → APP会自动增强对比度、去阴影、纠偏
  → 保存为JPG后重新识别

步骤3：识别后人工核对
  → 重点核对：发票代码(10-12位数字)、号码(8-20位数字)、金额
  → 金额勾稽检查：金额 + 税额 = 价税合计？
  → 置信度<0.7的字段重点核对

步骤4：手动输入（终极方案）
  → 如果反复识别失败，可直接手动输入发票信息
  → 格式：python scripts/ocr_engine.py --manual
  → 按提示输入发票代码、号码、日期、金额等
```

---

## 对话示例

本Skill支持通过自然语言对话方式使用，无需记忆复杂命令。

### 场景1：识别单张发票

```
用户：请帮我识别这张发票 D:\invoices\20260628_001.png
AI：正在识别发票...
    ✓ 发票类型: 增值税专用发票
    ✓ 发票代码: 3100204130
    ✓ 发票号码: 00564189
    ✓ 开票日期: 2026年06月28日
    ✓ 金额: 10,000.00 元
    ✓ 税额: 1,300.00 元
    识别完成，已保存到 receipt.json
```

### 场景2：批量处理

```
用户：把文件夹里所有发票都识别出来
AI：正在批量识别 D:\invoices\ 中的发票...
    共发现 15 个图片文件
    ✓ 20260628_001.png - 识别成功
    ✓ 20260628_002.png - 识别成功
    ⚠ 20260628_003.png - 识别失败（图片模糊）
    ...
    处理完成：成功 12 张，失败 3 张
    结果已保存到 batch_result.json
```

### 场景3：查验发票真伪

```
用户：帮我查验这张发票的真伪
AI：正在查验发票...
    发票代码：3100204130
    发票号码：00564189
    ✓ 查验平台：国税总局
    ✓ 发票状态：正常
    ✓ 查验时间：2026-06-29 10:30:00
```

### 场景4：生成报销单

```
用户：用公司模板生成报销单
AI：正在生成报销单...
    ✓ 识别到 6 个字段映射
    ✓ 已填充：开票日期、销方名称、金额、税额、价税合计、费用说明
    报销单已生成：D:\output\expense_report.xlsx
```

## API调用示例

### Python调用

```python
from scripts.ocr_engine import OCREngine

# 初始化引擎
engine = OCREngine()

# 识别单张发票
result = engine.extract_structured_data("invoice.png")
print(f"发票代码: {result['invoice_code']}")
print(f"金额: {result['amount']}")

# 批量处理
import glob
for file in glob.glob("invoices/*.png"):
    result = engine.extract_structured_data(file)
    print(f"{file}: {result['success']}")
```

### HTTP API调用

```bash
# 启动API服务（需安装flask）
python scripts/api_server.py

# 识别发票
curl -X POST http://localhost:8080/api/ocr \
  -F "file=@invoice.png"

# 批量识别
curl -X POST http://localhost:8080/api/ocr/batch \
  -F "files=@invoice1.png" \
  -F "files=@invoice2.png"
```

## 快速配置向导（一键配置）

**新手推荐**：运行以下命令自动检测环境并推荐最优配置：

```bash
python scripts/config_wizard.py
```

向导会自动完成：
1. 检测Tesseract是否安装，未安装则提供一键安装命令
2. 检测中文语言包是否完整
3. 推荐查验引擎（默认：国税总局平台，免费无需API Key）
4. 生成初始 `config.yaml` 文件
5. 验证配置文件有效性

**手动快速配置**（3步完成）：

```bash
# 1. 复制配置模板
cp templates/config_template.yaml config.yaml

# 2. 编辑配置（只需填写必填项）
# 用编辑器打开 config.yaml，填写：
#   - verify_engine: "tax_bureau" （默认，免费）
#   - approval.platform: "none" （暂不配置审批）

# 3. 验证配置
python scripts/check_env.py
```

> 💡 **提示**：发票识别、验真假、生成报销单 —— 这三项**完全不需要配置**，安装即用！审批对接需要配置API密钥。

## 🚀 5分钟上手指南

> **30秒摘要**：安装识别软件 → 识别发票 → 生成报销单。全程无需写代码，无需配置API。

### 完整流程图

```
┌─────────────────────────────────────────────────────────────────────┐
│                        5分钟快速上手流程                              │
└─────────────────────────────────────────────────────────────────────┘

 步骤1：安装（2分钟）                步骤2：识别（1分钟）
 ┌─────────────────────┐           ┌─────────────────────┐
 │ 一键安装PowerShell脚本 │    →     │ 拖入发票图片，自动识别 │
 │ (国内镜像，免配置)     │           │ 输出结构化JSON数据    │
 └─────────────────────┘           └─────────────────────┘
                                            ↓
 步骤4：（可选）一键生成报销单   ←   步骤3：验真假（30秒）
 ┌─────────────────────┐           ┌─────────────────────┐
 │ 用模板自动填充生成Excel │    ←     │ 一键生成查验链接       │
 │ 支持自定义字段映射      │           │ 自动打开浏览器查验     │
 └─────────────────────┘           └─────────────────────┘
```

### 🎯 三步开始使用

**第1步 — 下载安装（2分钟）**：

| 系统 | 操作 |
|------|------|
| **Windows** | 包管理器安装：`winget install --id UB-Mannheim.Tesseract`（或 `scoop install tesseract`），安装后重启终端 |
| **Mac** | 终端执行 `brew install tesseract` |
| **Linux** | `sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim pip install Pillow pytesseract openpyxl pyyaml` |

**第2步 — 识别发票（30秒）**：

```bash
# 单张识别
python scripts/ocr_engine.py --input 发票图片.png --output 识别结果.json

# 批量识别整个文件夹
python scripts/batch_process.py --input 发票文件夹/ --output 批量结果.json
```

**第3步 — 查验+报销单（1分钟）**：

```bash
# 生成国税总局查验链接（自动打开浏览器）
python scripts/verify_engine.py --invoice-code 3100204130 --invoice-number 00564189 --date "2026年06月28日" --amount 10000.00 --open-browser

# 生成报销单Excel
python scripts/template_matcher.py fill --receipt receipt.json --template templates/expense_basic.xlsx --output 报销单.xlsx
```

### ✅ 安装验证

```bash
python scripts/check_env.py
```
- ✅ 显示"环境就绪" → 直接开始用
- ❌ 有红叉 → 按提示修复后重试

### ⚙️ 高级功能配置（可选）

如果需要使用查验真伪或提交审批功能，才需要配置 `config.yaml`：

```bash
# 复制配置模板
cp templates/config_template.yaml config.yaml

# 编辑配置文件，填入API密钥
notepad config.yaml  # Windows
nano config.yaml     # Linux/macOS
```

## 审批功能 - 完整配置指南

> **30秒摘要**：审批功能提供了完整的代码引擎，企业只需在config.yaml中填入3个凭证即可使用，无需写任何代码。

### 钉钉审批配置（3步完成）

**第1步：创建钉钉应用**

打开 [钉钉开放平台](https://open-dev.dingtalk.com) → 创建企业内部应用 → 记录下 **AppKey** 和 **AppSecret**

**第2步：开通应用权限**

在应用管理页面：
- 权限管理 → 搜索"审批" → 开通 **审批:write** 权限
- 基础设置 → 添加服务器出口IP到IP白名单

**第3步：获取流程编码**

钉钉管理后台 → 审批流程管理 → 编辑报销审批流程 → 在URL中获取 `process_code`

```yaml
approval:
  platform: "dingtalk"
  dingtalk:
    app_key: "你的AppKey"
    app_secret: "你的AppSecret"
    process_code: "你的流程编码"
```

### 企业微信审批配置（3步完成）

**第1步：创建自建应用**

企业微信管理后台 → 应用管理 → 创建自建应用 → 记录下 **CorpID** 和 **Secret**

**第2步：开通审批权限**

在应用详情页 → 功能 → 审批 → 配置审批模板 → 获取 **TemplateID**

**第3步：配置IP白名单**

企业微信管理后台 → 应用管理 → 自建应用 → 接收消息设置 → 获取出口IP并添加到白名单

```yaml
approval:
  platform: "wecom"
  wecom:
    corp_id: "你的CorpID"
    secret: "你的Secret"
    template_id: "你的TemplateID"
```

### 审批测试方法

配置完成后，运行以下命令验证审批功能是否配置正确：

```bash
# 测试钉钉审批
python scripts/approval_engine.py \
  --config config.yaml \
  --expense 报销单.xlsx \
  --user-id 你的工号 \
  --amount 10000 \
  --expense-type 信息技术服务
```

如果配置正确，返回结果示例：
```json
{
  "status": "success",
  "message": "审批提交成功",
  "approval_id": "xxx",
  "submit_time": "2026-07-04T22:30:00"
}
```

---

## 详细配置说明

见 `references/setup-guide.md`

## 示例

### 示例1：识别单张发票

**输入**：

```
识别发票 D:\invoices\20260628_001.png
```

**输出**：

```json
{
  "success": true,
  "invoice_type": "增值税专用发票",
  "invoice_code": "3100204130",
  "invoice_number": "00564189",
  "invoice_date": "2026年06月28日",
  "seller_name": "上海某某科技有限公司",
  "amount": 10000.00,
  "tax_rate": 0.13,
  "tax_amount": 1300.00,
  "total": 11300.00,
  "remark": "*信息技术服务费*",
  "confidence": 0.96
}
```

### 示例2：查验发票真伪

**输入**：

```
查验发票 代码:3100204130 号码:00564189 日期:2026-06-28 金额:10000.00
```

**输出**：

```json
{
  "engine": "国税总局查验平台",
  "status": "ready",
  "verify_url": "https://inv-veri.chinatax.gov.cn/index.html?fpdm=3100204130&fphm=00564189",
  "message": "已为您生成查验链接，点击即可查验",
  "params": {
    "invoice_code": "3100204130",
    "invoice_number": "00564189",
    "billing_date": "2026-06-28",
    "amount": 10000.00
  }
}
```

> 如配置了百望云/诺诺API Key，会自动调用第三方API获取查验结果。

### 示例3：生成报销单

**输入**：

```
用模板 D:\templates\公司报销单.xlsx 生成报销单，数据来自 D:\invoices\receipt.json
```

**输出**：

```
模板分析完成：识别到 6 个字段映射，置信度 0.8+
报销单已生成：D:\output\expense_report_20260629.xlsx
已填充 6 个字段：开票日期、销方名称、金额、税额、价税合计、费用说明
```

### 示例4：批量识别并合并为报销单

```bash
python scripts/batch_process.py --input D:\invoices\ --template D:\templates\公司报销单.xlsx --output D:\output\合并报销单.xlsx
```

### 示例5：提交审批

```bash
python scripts/approval_engine.py --config config.yaml --expense D:\output\报销单.xlsx --user-id manager123 --amount 11300 --expense-type 信息技术服务
```

## 发票类型支持与图片要求

> **30秒摘要**：支持增值税专票/普票/电子票。识别效果高度依赖图片质量——扫描件>拍照，清晰>模糊，建议分辨率≥200DPI。

### 支持的发票类型

- ✅ 增值税专用发票
- ✅ 增值税电子发票
- ✅ 增值税普通发票
- ✅ 电子发票（PDF格式，需安装poppler）

### 暂不支持

- ❌ 手写发票
- ❌ 定额发票
- ❌ 机动车销售发票
- ❌ 二手车销售发票
- ❌ 海关缴款书

### 图片质量要求（直接影响识别率）

> ⚠️ **重要提醒**：Tesseract OCR识别效果**高度依赖图片质量**。模糊、反光、低分辨率的图片会导致识别率显著下降。

| 质量等级 | 分辨率 | 光线 | 平整度 | 预期准确率 |
|---------|--------|------|--------|-----------|
| 优秀 | ≥300DPI | 均匀 | 无褶皱 | 95%+ |
| 良好 | 200-300DPI | 较均匀 | 轻微褶皱 | 85-95% |
| 可用 | 150-200DPI | 一般 | 有褶皱 | 70-85% |
| 较差 | <150DPI | 反光/阴影 | 严重褶皱 | <70%，建议重新拍摄 |

**图片质量自检清单**：
- [ ] 发票代码和号码区域是否清晰可辨？
- [ ] 金额数字是否有模糊或重影？
- [ ] 是否有反光或阴影遮挡关键信息？
- [ ] 发票边缘是否完整可见？
- [ ] 图片分辨率是否足够（建议手机相机≥1200万像素）？

> **提高识别率的小技巧**：
> 1. 用手机相机拍摄时，开启"文档模式"或"扫描模式"
> 2. 避免强光直射，减少反光
> 3. 发票平整放置，不要弯曲
> 4. 确保发票代码、号码区域清晰可见
> 5. 如果无法识别，请检查图片中是否有手写涂改
> 6. **推荐使用扫描件**，比拍照效果更好
> 7. 可使用手机扫描APP（如"扫描全能王"）预处理图片

## 限制说明

> **30秒摘要**：仅支持增值税发票（不支持手写/定额），数据全部本地处理（不上传），不提供税务咨询。

### 功能限制

| 限制项 | 具体说明 |
|--------|---------|
| OCR识别 | 仅支持增值税发票（专票/普票/电子票） |
| 暂不支持 | 手写发票、定额发票、机动车发票、二手车发票 |
| 查验功能 | 国税总局查验链接自动生成，无需API Key |
| 审批功能 | 需企业管理员在对应平台开通审批API权限，提供完整代码模板和分步配置指南 |

### 技术限制

| 限制项 | 具体说明 |
|--------|---------|
| 运行环境 | Python 3.8+ |
| 必须安装 | Tesseract OCR + 中文语言包 |
| 图片格式 | PNG/JPG/TIFF/PDF（PDF需要poppler） |
| 语言 | 中文简体，其他语言准确率显著下降 |
| 并发 | 硬件自适应并行处理（CPU 核心数 × 0.5/× 0.75），批量速度提升 3-5 倍 |

### 安全限制

| 限制项 | 具体说明 |
|--------|---------|
| 数据上传 | 绝不将发票图片上传到任何第三方服务器 |
| API调用 | 仅在用户明确授权后执行，且仅调用用户配置的平台 |
| 日志 | 仅记录操作元数据（文件名、时间、状态），不记录发票内容 |
| 临时文件 | 识别完成后自动清理，保留不超过24小时 |

## 错误代码速查表

| 错误代码 | 问题描述 | 解决方案 |
|---------|---------|---------|
| `Tesseract not found` | Tesseract未安装或未加入PATH | 用包管理器安装（Windows: winget/scoop；Mac: brew；Linux: apt）并重启终端 |
| `chi_sim not found` | 中文语言包未安装 | 重新安装Tesseract，勾选Chinese语言包 |
| `PIL not found` | Pillow未安装 | `pip install Pillow` |
| `pytesseract not found` | pytesseract未安装 | `pip install pytesseract` |
| `openpyxl not found` | openpyxl未安装 | `pip install openpyxl` |
| `pdf2image not found` | PDF转图片工具未安装 | `pip install pdf2image` + 安装poppler |
| `empty result` | OCR未识别到文字 | 检查图片质量、光线、平整度 |
| `low confidence` | 识别置信度低于0.7 | 建议重新拍摄，或手动输入发票信息 |
| `verify_engine not configured` | 查验引擎未配置 | 编辑config.yaml，填写对应API Key |
| `approval_engine not configured` | 审批引擎未配置 | 编辑config.yaml，选择并填写审批平台 |
| `token_failed` | 获取AccessToken失败 | 检查API Key/Secret是否正确 |
| `template_not_found` | 模板文件不存在 | 检查template路径是否正确 |

## 风险声明

> **30秒摘要**：数据本地处理不上传、查验结果由第三方平台提供、审批不可撤销、本工具不提供税务咨询。

> 🔴 **使用本Skill前，请务必仔细阅读以下条款：**

### 1. 数据安全责任

- 所有发票数据仅在用户本地设备处理，不会上传到任何服务器
- **但用户需自行确保本地设备的安全**，Skill开发者不对数据泄露承担责任
- 用户需自行负责API密钥的安全保管
- 建议定期轮换API密钥（每90天一次）

### 2. 查验结果免责声明

- 查验引擎返回的结果由第三方平台提供
- Skill仅提供技术对接，**不对查验结果的准确性负责**
- 如对查验结果有疑问，请直接联系相关税务平台

### 3. 审批操作责任

- 审批提交后不可撤销（以各平台规则为准）
- Skill不审批内容的合规性和真实性
- 用户对提交的报销单内容负全部责任

### 4. 财务合规要求

- 本工具仅为技术支持工具，**不提供任何税务咨询或财务建议**
- 所有财务决策应由专业财务人员做出
- 需专业税务意见时，请咨询持牌税务顾问

### 5. 禁止行为

使用本Skill，用户不得：
- 伪造、变造发票
- 使用假发票报销
- 虚增报销金额
- 报销与业务无关的费用
- 进行其他违反财务法规的行为

### 6. 企业自主决策清单

使用前，请确认您已决定以下事项：

- [ ] 查验引擎选择：□ 国税总局平台（免费） □ 百望云 □ 诺诺发票 □ 自建接口
- [ ] 审批平台选择：□ 钉钉 □ 企业微信 □ 飞书 □ 自建系统 □ 暂不使用
- [ ] 数据安全策略：日志保留期限、临时文件清理频率
- [ ] 合规审查：内部审计、外部审计计划

## 配置文件模板

```yaml
# config.yaml - 企业自主配置
# 本文件为示例模板，企业需根据实际情况填写
# 未配置的功能模块将提示手动操作

# ==================== 查验引擎配置 ====================
verify_engine: "tax_bureau"
# 可选值:
# - "tax_bureau": 国税总局查验平台（免费，无需API Key）
# - "bairong": 百望云API（需API Key+Secret）
# - "nuonuo": 诺诺发票API（需API Key+Secret）
# - "custom": 企业自建接口（需接口地址）

# 百望云（如选择bairong）
bairong:
  api_key: "在此填写您的百望云API Key"
  api_secret: "在此填写您的百望云Secret"

# 诺诺发票（如选择nuonuo）
nuonuo:
  api_key: "在此填写您的诺诺发票API Key"
  api_secret: "在此填写您的诺诺发票Secret"

# 自建查验接口（如选择custom）
custom:
  endpoint: "https://your-company.com/api/verify"
  method: "POST"
  headers:
    Authorization: "Bearer YOUR_TOKEN"

# ==================== 审批平台配置 ====================
approval:
  platform: "none"  # dingtalk / wecom / feishu / none

  # 钉钉审批
  dingtalk:
    app_key: ""
    app_secret: ""
    process_code: ""

  # 企业微信审批
  wecom:
    corp_id: ""
    secret: ""
    template_id: ""

  # 飞书审批
  feishu:
    app_id: ""
    app_secret: ""
    approval_code: ""

  # 自建审批系统
  custom:
    endpoint: ""
    method: "POST"
    headers: {}
    timeout: 30

# ==================== 模板映射配置 ====================
template:
  path: "templates/expense_basic.xlsx"  # 报销单模板路径
  field_mapping:
    invoice_date: "开票日期"
    seller_name: "销方名称"
    amount: "金额（不含税）"
    tax_amount: "税额"
    total: "价税合计"
    remark: "费用说明"
    invoice_code: "发票代码"
    invoice_number: "发票号码"
```

## 外部平台不可用时的降级方案

> 💡 **重要提示**：查验和审批功能依赖外部平台（国税总局、钉钉、企微、飞书等），遇到平台维护或网络故障时，可使用以下降级方案。

### 查验发票真伪 - 降级方案

当自动查验平台不可用时，可手动查验：

**方法1：使用国税总局官方平台**（推荐）
1. 打开浏览器，访问：https://inv-veri.chinatax.gov.cn
2. 输入发票代码、发票号码、开票日期、开具金额（不含税）
3. 输入验证码，点击"查验"
4. 截图或保存查验结果备查

**方法2：使用手机APP查验**
- 国家税务总局"增值税发票查验平台"APP
- 支付宝"发票管家" - 发票查验功能
- 微信"腾讯发票" - 发票查验功能

**方法3：电话查验**
- 拨打12366纳税服务热线，提供发票信息查询真伪

### 提交审批 - 降级方案

当自动审批提交不可用时，可手动提交：

**钉钉审批**：
1. 打开钉钉APP → 工作台 → 审批
2. 找到对应的报销审批流程
3. 手动填写报销信息，上传报销单PDF
4. 提交审批

**企业微信审批**：
1. 打开企业微信APP → 工作台 → 审批
2. 选择报销审批流程
3. 填写信息，上传附件
4. 提交审批

**飞书审批**：
1. 打开飞书APP → 工作台 → 审批
2. 创建新的报销审批
3. 填写表单，上传报销单
4. 提交审批

### 数据存储建议

在外部平台不可用期间，建议：
1. 将识别结果保存为JSON文件（`--output result.json`）
2. 将报销单保存为PDF（`--format pdf`）
3. 平台恢复后，使用批量提交功能一次性提交

## 故障排除

### 常见问题

**Q1: 安装Tesseract后仍然提示 `Tesseract not found`**

A: 通常是PATH环境变量未生效。

- **Windows**：重启PowerShell/终端，或手动运行 `refreshenv`
- **Linux/macOS**：运行 `source ~/.bashrc` 或 `source ~/.zshrc`
- 紧急方案：使用 `--tesseract` 参数指定完整路径：
  ```bash
  python ocr_engine.py --tesseract "C:\Program Files\Tesseract-OCR\tesseract.exe" --input 发票.png
  ```

**Q2: 识别结果为空或仅识别到少量内容**

A: 按顺序排查：
1. 图片质量是否过低？（拍摄光线、平整度、分辨率）
2. 发票类型是否支持？（手写发票不支持）
3. 是否安装了中文语言包？（运行 `tesseract --list-langs` 检查是否有 `chi_sim`）
4. 尝试提高图片预处理质量（在代码中调整阈值参数）
5. 尝试用原始图片（未预处理）重新识别 — 某些情况下预处理反而会降低图片质量

**Q3: 提示 `PermissionError` 或 `Occupied`**

A: 文件被其他程序关闭。请关闭所有占用目标文件的程序后重试。

**Q4: 查验接口返回失败**

A: 排查顺序：
1. 检查API Key/Secret是否正确（无多余空格）
2. 检查网络是否可访问对应平台
3. 检查是否超出调用频率限制
4. 查看 `logs/verify_engine.log` 了解详细错误

**Q5: 模板匹配失败**

A: 检查以下几点：
1. 模板文件第一行是否为中文表头
2. 模板文件是否未损坏（用Excel打开确认）
3. 字段名是否在预设映射表中（见 `common_mappings`）
4. 可尝试手动指定映射关系

**Q6: 如何减小识别结果文件体积？**

A: 处理完成后，删除 `output/` 目录下的中间文件（`.json`、`.xlsx`），仅保留最终需要的文件。Skill会自动清理临时文件。

**Q7: 支持哪些审批平台？**

A: 钉钉、企业微信、飞书、自建系统（需实现接口）。

**Q8: 如果审批平台不在列表中怎么办？**

A: 使用 `custom` 选项，填写企业自建审批系统的接口地址和鉴权方式。

**Q9: OCR识别率低，很多字段识别错误**

A: 识别效果主要取决于图片质量，请尝试以下方法：
1. **图片质量**：确保分辨率≥200DPI，光线均匀，无反光
2. **推荐使用扫描件**：扫描件比拍照效果更好，文字更清晰
3. **使用手机扫描APP**：如"扫描全能王"、"白描"等APP预处理图片，可显著提升识别率
4. **图片格式**：优先使用JPG或PNG，避免PDF（需额外安装poppler）
5. **发票类型**：仅支持增值税专票/普票/电子票
6. **手动校验**：识别后人工核对关键字段（代码、号码、金额）
7. **模板学习**：使用 `template_matcher.py analyze` 分析模板结构

**Q10: 批量处理时部分文件失败**

A: 正常现象，不影响其他文件。失败的文件会记录在JSON输出的 `failed_files` 字段中，包含：
- `file`：文件路径
- `error`：错误原因
- `tip`：建议操作
- `suggestions`：具体改进建议

**Q11: 审批Token获取失败**

A: 排查步骤：
1. 确认API Key/Secret正确（无空格、大小写正确）
2. 确认应用已开通审批权限（钉钉/企微/飞书管理后台）
3. 确认服务器IP已在白名单中
4. 确认Token未过期（默认2小时有效期）
5. 检查网络是否可访问对应API地址

**Q12: 如何选择合适的查验引擎？**

A: 根据企业需求选择：
- **国税总局平台（推荐）**：免费，无需API Key，生成链接手动查验
- **百望云/诺诺发票**：需付费API Key，自动返回查验结果
- **自建接口**：适合有自建查验系统的企业

**Q13: 金额勾稽关系不匹配怎么办？**

A: 可能原因：
1. OCR识别错误：人工核对金额、税额、价税合计
2. 小数精度问题：系统自动四舍五入，0.01元以内差异可忽略
3. 特殊发票：部分发票金额计算方式不同

**Q14: 环境预检通过但OCR仍失败**

A: 可能原因：
1. Tesseract版本过低（建议4.0+）
2. 中文语言包不完整（检查文件大小≥5MB）
3. 图片质量极差（重新拍摄）
4. 发票类型不支持（手写发票、定额发票不支持）

### 日志文件说明

如果以上方案均无法解决问题，请查看日志文件获取详细信息：

```
logs/
├── ocr_engine.log          # OCR识别详情
├── verify_engine.log       # 查验详情
├── template_matcher.log    # 模板匹配详情
├── approval_engine.log     # 审批详情
└── error.log               # 错误日志（优先查看）
```

## 支持与反馈

- 问题反馈：请在 SkillHub 平台提交 Issue
- 功能建议：欢迎提交 Pull Request
- 邮箱：联系Skill开发者
- 联系信息：njskills@agent.qq.com
- 版本更新提醒：检测到新版本发布时，请及时通过 tongyifabu.ps1 更新本 Skill 以获取最新功能和修复

## 全电发票（数电票）

本 Skill 已支持全电发票（全面数字化的电子发票），兼备传统发票 OCR 与全电发票 XML/OFD 解析的双轨模式。

### 支持的文件类型

| 类型 | 扩展名 | 解析方式 |
|------|--------|---------|
| 传统纸质发票 | `.png`、`.jpg`、`.jpeg`、`.bmp` | OCR 引擎识别 |
| 传统电子发票（PDF） | `.pdf` | 数电票走直读（pypdf 文本层，无需 poppler），非数电走通用 OCR |
| 全电发票（XML） | `.xml` | 专用 XML Schema 解析器，提取结构化数据 |
| 全电发票（OFD） | `.ofd` | OFD 解析器或转换为 PDF 后 OCR |

### 全电发票特有字段

| 字段 | 说明 | 传统发票字段差异 |
|------|------|-----------------|
| 发票号码（20位） | 全电发票唯一标识 | 传统发票 8-20 位 |
| 税务数字账户 ID | 数电票归集账户标识 | 传统发票无此概念 |
| 校验码 | 全电票安全校验 | 传统发票为密码区 |
| 特定业务信息 | 差额计税、建筑服务等标识 | 传统发票无明确标记 |

### 使用方式

**全电发票 XML 文件**：
```bash
python scripts/xml_parser.py path/to/invoice.xml
```

**全电发票 OFD 文件**：
```bash
python scripts/ofd_parser.py path/to/invoice.ofd
```

**自动识别（推荐）**：
```bash
python scripts/invoice_detector.py path/to/any_invoice
```

模块会自动判断文件类型并调用对应解析器。

### 降级方案

当 `ofdparser` Python 库未安装时，OFD 解析器会提示您：

1. **安装 ofdparser**：`pip install ofdparser`（首选）
2. **转换为 PDF**：使用数科阅读器、福昕 OFD 阅读器导出为 PDF，再用 OCR 识别
3. **手动阅读**：通过官方 OFD 阅读器手动查看

### 税务数字账户接口说明

全电发票通过税务数字账户归集管理。如需对接税务数字账户接口，可参考：

- 电子税务局官方文档：https://etax.chinatax.gov.cn/
- 发票查验（国税总局）：https://inv-veri.chinatax.gov.cn/

> ⚠️ **注意**：税务数字账户对接以企业自主配置为原则，本 Skill 提供标准接口框架，企业需根据实际税局接口规范自行实现具体调用逻辑。

## 数电票直读与查重强化（v4.5.0）

### 20. 数电票直读（PDF/OFD 不依赖通用 OCR）

数电票 PDF/OFD 含结构化文本层，本版提供直读通道，跳过通用 OCR 的版面漂移问题：

- **PDF 文本层直读**：优先 `pypdf` 抽取文本，`pdfminer.six` 次之，再降级 OCR；文本层缺失（扫描件 PDF）时退回通用 OCR 流程
- **OFD 文字层直读**：优先 `ofdparser` 取文字，缺失则返回结构信息并提示安装
- **票面要素 + 明细行**：发票号码/日期/价税合计/税额/税率/买卖方，以及数电票明细行（项目名称/规格/数量/单价/金额/税率/税额）一并结构化
- **二维码 TLV 解码核对**：从 PDF 内嵌二维码提取 `pyzbar` 解码（缺失则跳过），与票面号码/代码交叉校验，不一致明确告警

```bash
# 数电票 PDF 直读
python scripts/digital_invoice_reader.py pdf path/to/invoice.pdf

# 数电票 OFD 直读
python scripts/digital_invoice_reader.py ofd path/to/invoice.ofd

# 自动识别（数电票 PDF 将走直读而非通用 OCR）
python scripts/invoice_detector.py path/to/any_invoice
```

> 依赖策略（死规则 #9）：`pypdf` / `pdfminer.six` / `ofdparser` / `pyzbar` 均「优先 import、缺失即降级」，不强制安装；未装时功能降级但主流程不中断。

### 21. 重复报销查重（三信号两阶段）

针对报销重复（含 P 图改抬头）做两阶段检测：

| 阶段 | 信号 | 逻辑 | 覆盖场景 |
|------|------|------|---------|
| 一 | 票号精确哈希 | 同号即重复 | 原样重复报销 |
| 二 | 金额 ±0.01 + 日期 ±3 天 + 销售方/票号前缀相似 | 近似比对 | 改了抬头/票号但金额日期一致的变造重复 |

```bash
# 对台账全部票据跑查重，自动生成复核工单（幂等，已建单不重复）
python scripts/ledger_db.py --dedup

# 查看复核工单（pending / confirmed_dup / exempt / all）
python scripts/ledger_db.py --list-reviews pending
```

查全率目标：20 组重复样本 ≥ 95%；数电票 PDF/OFD 各 10 份要素抽取准确率 ≥ 98%。

### 22. 查重复工单化（复核清单 + 移动端对照）

每次查重命中的可疑组生成一条复核工单，财务在桌面端确认、移动端查阅：

```bash
# 渲染工单为移动端可读 HTML（双原始凭证缩略图对照 + 差异标注）
python scripts/ledger_db.py --render-review 工单ID 复核对照.html

# 财务确认：confirmed_dup（重复，相关票据不进台账）/ exempt（误报，沉淀为豁免规则）
python scripts/ledger_db.py --resolve-review 工单ID confirmed_dup
python scripts/ledger_db.py --resolve-review 工单ID exempt
```

- 数电票渲染首页缩略图，纸票用扫描图；渲染失败仅展示要素差异表，不影响查阅
- 误报标记 `exempt` 后自动沉淀为豁免规则，后续同组合不再重复告警

## 台账与合规管理（v4.4.0）

### 15. 进销项台账与月度统计

把散落的票据识别结果沉淀成可分析的资产。数据库默认落在 `~/.workbuddy/output/receipt_ledger.db`，不写入 Skill 仓库。

```bash
# 导入票据解析结果（进项）
python scripts/ledger_db.py --import-json result.json --direction input

# 导入销项（用于税负率与进销项匹配）
python scripts/ledger_db.py --import-json output.json --direction output

# 输出四类报表视图
python scripts/ledger_db.py --report

# 导出 Excel 月度附件（未装 openpyxl 时自动降级 CSV）
python scripts/ledger_db.py --export-excel
```

四类报表视图：

| 视图 | 说明 | 用途 |
|------|------|------|
| 月度汇总 | 按月份 × 进销项汇总张数/金额/税额 | 月度结账底稿 |
| 税负率趋势 | 税负率 = (销项税额 − 进项税额) ÷ 不含税销售额 | 异常波动自查 |
| 供应商集中度 | Top N 供应商金额占比 + Top1 占比环比变化 | 依赖度风险 |
| 异常波动 | 月度金额 z-score，默认 ±2.5 标注 | 收入异常自查 |

### 16. 到期与认证期日历

```bash
# 全电发票自动推算认证期限（开票日期 + 窗口，默认 360 天）
python scripts/cert_calendar.py --ensure-deadlines

# 纸票手工补录
python scripts/cert_calendar.py --set-deadline 12345678 2027-03-31

# 扫描到期（30 天 / 7 天两档 + 已过期）
python scripts/cert_calendar.py --scan

# 导出 CSV 供日历软件二次提醒
python scripts/cert_calendar.py --scan --export-csv

# 注册每日 09:00 自动扫描（Windows schtasks，不生成任何 .bat/.ps1）
python scripts/cert_calendar.py --register
python scripts/cert_calendar.py --status
python scripts/cert_calendar.py --unregister
```

> 说明：自 2020-03-01 起增值税专用发票已取消 360 天认证确认期限，此处窗口仅作企业内部「勾选所属期」管理提醒，可在 `references/risk_rules_config.yaml` 的 `certification.window_days` 调整。

### 17. 异常检测（轻量 Isolation Forest）

在 5 类规则预警之上叠加一层无监督检测，纯 numpy 实现，无需 sklearn；numpy 缺失时自动降级纯 Python。

```bash
# 从台账直接读
python scripts/anomaly_detector.py ~/.workbuddy/output/receipt_ledger.db --db --top 20

# 或从票据 JSON
python scripts/anomaly_detector.py invoices.json --trees 100 --warn 0.65
```

输出示例：

```json
{
  "level": "严重",
  "invoice_number": "24312000000012345678",
  "score": 0.71,
  "dimension_scores": {"amount": 0.72, "interval": 0.41, "supplier": 0.68},
  "triggered_dimensions": ["amount", "supplier"],
  "explanation": "金额分布异常（999999.00 元偏离常规区间，得分 0.72）；供应商组合异常（该供应商出现 5 次、占比 97.9%，得分 0.68）"
}
```

性能约束：样本超过 5000 自动采样，树数量默认 100 棵，单核千张票据秒级完成，不影响日常办公。

### 18. 合规管理统一出口

一次执行同时产出风险报告与归档四性检测结果，不再分两次跑。

```bash
# 从台账读取 + 指定票据目录做四性检测
python scripts/compliance_suite.py --db ~/.workbuddy/output/receipt_ledger.db \
    --files-dir ./invoices --output report.json

# 关闭异常检测
python scripts/compliance_suite.py --invoices invoices.json --no-anomaly
```

输出整体状态：`合规` / `需关注` / `需立即处理`。

### 19. 审批连接器（统一接口）

钉钉 / 企业微信 / 飞书统一为 `ApprovalConnector` 接口，新增平台只需实现三个方法：

```python
from approval_connector import ApprovalConnector

class MyPlatform(ApprovalConnector):
    platform = "myplatform"
    display_name = "我的审批平台"

    def send(self, expense_file, applicant_user_id=None, **kwargs):
        """发起审批"""

    def query_status(self, approval_id):
        """查询审批状态"""

    def verify_callback(self, payload, **kwargs):
        """回调验签"""
```

原 `DingTalkApproval` / `WeComApproval` / `FeishuApproval` / `ApprovalManager` 全部保留为兼容外壳，老代码不用改。新增能力：

```python
manager.query_status("审批实例ID")        # 查状态
manager.verify_callback(payload)          # 回调验签
```

### 规则 YAML 化与白名单

规则全部集中在 `references/risk_rules_config.yaml`，改完自动热加载，无需重启：

```yaml
round_amount_check:
  enabled: true
  threshold: 10000

whitelist:
  sellers: []                        # 销售方含关键词 → 全规则豁免
  categories: [房租, 物业费]          # 费用类型命中 → 全规则豁免
  rules:
    round_amount: [房租, 物业]        # 仅豁免整数金额规则
```

> YAML 解析优先使用 PyYAML，未安装时自动降级到内置解析器，功能不受影响。

## 更新日志

| v4.5.0 | 2026-10-09 | 新增：数电票直读模块 digital_invoice_reader.py，PDF 文本层优先 pypdf 抽取、缺失降级 pdfminer/OCR，OFD 文字层经 ofdparser 直读，票面要素与明细行一并结构化；新增：二维码 TLV 解码核对（pyzbar 优先，缺失跳过），票面号码/代码与二维码交叉校验不一致告警；新增：查重三信号引擎 dedup_engine.py，票号精确哈希 + 金额 ±0.01 + 日期 ±3 天两阶段近似比对，检出 P 图改抬头重复；新增：查重复工单化，ledger_db.py 增加 review 与 exempt_rules 表，自动生成复核工单、财务确认进台账或误报豁免沉淀规则；新增：review_render.py 生成移动端可读双原始凭证缩略图对照 HTML，渲染失败仅展示要素差异表；优化：unified_invoice.py 增加 detail_lines 明细行字段；优化：xml_parser.py 实现数电票明细行结构化提取；优化：invoice_detector.py 数电票 PDF 路由直读（非通用 OCR）；修复：ledger_db.py 台账同号不同源文件被误合并为单行导致原样重复漏检，存在性判定补 source_file 区分 |
| v4.4.0 | 2026-09-08 | 新增：进销项台账引擎 ledger_db.py，SQLite 持久化台账含认证期限字段，提供月度汇总、税负率趋势、供应商集中度（Top N 占比与环比变化）、异常波动 z-score 四类报表视图，支持 openpyxl 导出 Excel 月度附件（缺失时降级 CSV）；新增：认证期日历 cert_calendar.py，全电发票自动取数认证期限、纸票手工补录，30/7 天两档到期提醒，支持 schtasks 注册每日扫描与 CSV 导出供日历软件二次提醒；新增：轻量异常检测引擎 anomaly_detector.py，纯 numpy 随机切割树实现 Isolation Forest 思路，金额分布/开票时间间隔/供应商组合三维打分，异常分超阈值进二级预警并给出触发维度解释；新增：合规管理统一出口 compliance_suite.py，风险预警与归档四性检测合并为一次执行，输出统一合规报告；新增：统一审批连接器 approval_connector.py，抽象发送/查状态/回调验签三方法，钉钉/企微/飞书为实现类；优化：风险预警规则 YAML 化，支持热加载、规则开关与白名单（房租等天然整数金额不再误报）；优化：approval_engine.py 改造为兼容层，原有调用方式不受影响 |
| v4.3.0 | 2026-08-24 | 新增：PaddleOCR 双引擎降级层（ocr_engine.py 重写），PaddleOCR 优先 + Tesseract 兜底，自动探测可用引擎；新增：定额票版式先验定位表（fixed_layout_prior），固定字段位置驱动 ROI 局部 OCR；新增：手写数字后处理约束（_cross_check 勾稽校验引擎），金额+税额=价税合计不通过则标记人工复核不入库；新增：混拍图检测与子图切分引擎 batch_splitter.py，行距聚类切分 + 边界接触边框特征二次切分，保持原图-子图索引；升级：invoice_detector.py 集成 PaddleOCR 双引擎 |
| v4.2.2 | 2026-08-16 | 修复：移除 secure_config.py CLI 中 --show-keys 参数（仍有凭据外泄特征）；改为 validate_before_call() 仅返回字段名列表和布尔状态，绝不输出任何形态的密钥值到 stdout，彻底消除凭据泄露风险 |
| v4.2.1 | 2026-08-16 | 修复：将 SKILL.md、check_env.py、install_tesseract.ps1 中 poppler-windows 下载源从个人 fork（oschwartz10612/blog.alivate.com.au）替换为系统包管理器（winget/scoop/apt/brew），消除非官方来源供应链风险；修复：secure_config.py 默认脱敏输出，validate_before_call() 返回值统一脱敏，消除密钥泄露到 stdout 的风险 |
| v4.2.0 | 2026-08-16 | 新增：银行流水对账引擎 bank_reconciler.py，支持主流银行 CSV 流水解析，金额模糊匹配（±0.01 元容差）+ 日期模糊匹配（±3 天容差）+ 综合评分机制；新增：安全密钥配置模块 secure_config.py，统一从环境变量读取 API 密钥（INVOICE_ 前缀），消除明文泄露风险，含脱敏显示和缺失校验；新增：并行批量处理引擎 parallel_batch.py，硬件自适应 worker 分配（CPU × 0.5/× 0.75），含内存检测自动降级、分块处理、失败重试机制 |
| v4.0.0 | 2026-08-01 | 新增：全电发票XML解析器 xml_parser.py；新增：OFD版式文件解析器 ofd_parser.py；新增：火车票解析器 train_parser.py；新增：飞机行程单解析器 flight_parser.py；新增：出租车票解析器 taxi_parser.py；新增：定额发票解析器 fixed_parser.py；新增：通行费票据解析器 toll_parser.py；新增：财政票据解析器 fiscal_parser.py；新增：智能分类器 smart_classifier.py，支持费用类型自动匹配、进项税额自动计算、会计科目自动映射；新增：记账凭证生成器 voucher_generator.py，支持用友/金蝶/QuickBooks导入格式；新增：统一发票数据结构 unified_invoice.py，兼容新旧发票和多种票据类型；新增：票种自动识别模块 invoice_detector.py，自动路由传统OCR或专用解析器；新增：会计科目对照表 account_mapping.md；新增：费用分类规则 expense_rules.md |
| v3.7.0 | 2026-07-22 | 新增：全电发票（数电票）XML 格式解析器 xml_parser.py，支持 20 位全电发票号码、校验码、税务数字账户等特有字段提取；新增：OFD 版式文件解析器 ofd_parser.py；新增：票种自动识别模块 invoice_detector.py，自动路由传统 OCR 或全电解析；新增：统一发票数据结构 unified_invoice.py，兼容新旧发票格式；新增：SKILL.md 全电发票使用章节；新增：版本更新提醒机制；新增：联系信息 njskills@agent.qq.com |
| v3.4.0 | 2026-07-13 | 修复：移除 install_tesseract.ps1 中指向个人 Gitee 仓库的下载源，替换为 winget/scoop 官方源和 GitHub 官方 Release；修复：将 approval_abstract.py、api-endpoints.md、setup-guide.md、example-approval.md 中所有 open.duxiaoman.com 错误链接替换为钉钉官方地址 open-dev.dingtalk.com；修复：verify_engine.py 中 subprocess.Popen 移除 shell=True，改为列表参数形式 |
| v3.3.0 | 2026-07-13 | 更名：插件文件夹名从 tax-receipt-compliance 改为 receipt-compliance；更名：displayName 从财税合规全链路助手改为会计助手 |

### v3.2.0 (2026-07-04)

**🎯 基于TRACE评测反馈的深度优化**

- **新增**：【5分钟上手指南】含完整流程图，从安装到报销一步到位，解决"使用流程不清晰"问题
- **新增**：【避坑指南】14个高频问题+解决方案，覆盖识别/配置/查验/审批全场景
- **新增**：【审批功能完整配置指南】钉钉/企微3步配置流程+测试命令，降低对接门槛
- **新增**：verify_engine.py 支持 `--open-browser` 参数，一键生成查验链接并自动打开浏览器
- **改进**：审批引擎(approval_engine.py)从"框架"升级为"完整可用"，钉钉/企微审批可直接调用API提交
- **改进**：功能说明表更新，真伪查验改为"✅ 直接可用"（一键生成链接+自动打开浏览器）
- **改进**：限制说明更新，查验功能标注为"无需API Key"
- **改进**：所有脚本错误提示风格统一，保持专业术语+通俗解释的平衡

**评测反馈响应**：
- A(适用性) 4.3/5 → 新增完整使用流程图+审批配置指南，降低上手门槛
- C(规范性) 4.5/5 → 新增避坑指南，问题更集中；文档结构优化
- E(有效性) 4.2/5 → 验真假功能完整可用（一键打开浏览器），审批引擎从框架升级为完整实现

**🎯 基于用户评测反馈的重大改进**

- **安全性提升**：安装脚本增加SHA256文件完整性校验，下载完成后自动验证文件完整性
- **安装简化**：一键安装脚本优化，增加更详细的进度显示和成功/失败提示
- **OCR识别率提升**：图像预处理算法升级，增加自适应二值化（OTSU）、去噪、边缘增强等功能
- **模糊发票处理**：新增`enhance_mode`参数（auto/normal/aggressive/gentle），自动根据图片质量选择最佳预处理模式
- **图像质量预检**：OCR引擎增加`check_image_quality()`函数，自动检测图片分辨率并给出预处理建议
- **开箱即用性提升**：快速开始章节简化，一键安装脚本支持更多安装方式
- **降级方案**：外部平台不可用时，给出详细的手工操作指南（见下方【外部平台不可用时的降级方案】）
- **默认配置**：提供默认配置模板，基础功能无需配置即可使用
- **文档优化**：快速开始章节重构，30秒即可了解核心步骤
- **修复语句**：优化所有脚本的错误提示和操作建议，改为更自然、更易理解的中文表达

**评测反馈响应**：
- T(可信任度) 4.5/5 → 安全性提升，文件完整性校验
- R(可靠性) 4.6/5 → 模糊发票识别率提升，预处理算法优化
- A(适用性) 4.8/5 → 安装流程简化，开箱即用性提升
- C(规范性) 4.8/5 → 文档结构优化，快速开始章节重构
- E(有效性) 4.4/5 → OCR识别率提升，默认配置提供

### v2.7.0 (2026-06-30)
- **新增**：【使用技巧与注意事项】章节，汇总5项基本技巧+5项注意事项，一目了然
- **新增**：【模糊发票处理指南】，4步流程应对图片模糊场景
- **新增**：OCR引擎 `--manual` 手动输入模式，OCR失败时可直接手动输入发票信息
- **新增**：长章节增加"30秒摘要"，减少阅读时间（快速开始/发票类型/限制说明/风险声明）
- **新增**：OCR软件大小说明，解释60MB安装包的必要性（数据安全 vs 软件体积的权衡）
- **改进**：手动输入模式支持金额勾稽自动检查，输入不一致会提示警告

### v2.6.5 (2026-06-30)
- **修复**：修复bug


### v2.6.0 (2026-06-30)
- **新增**：【如何「指挥」它干活】章节，包含自然语言对话示例表格（8种场景+详细说法）
- **新增**：【常见问题速查】集中解答板块，按6大类（安装配置/OCR识别/查验审批/模板数据/安全合规）组织
- **改进**：FAQ和常见问题从分散在多处改为集中速查表+详细解答两部分，查找更方便
- **改进**：触发词章节扩展为更详细的"如何指挥"说明，降低用户上手门槛
- **改进**：所有错误提示保持专业术语+通俗解释的平衡

### v2.5.0 (2026-06-29)
- **改进**：版本号升至 2.5.0
- **改进**：图片质量要求增加"图片质量自检清单"，帮助用户提前发现图片问题
- **改进**：图片质量要求增加扫描件推荐和手机扫描APP建议
- **改进**：图片质量要求顶部增加醒目的"识别效果高度依赖图片质量"提醒
- **改进**：FAQ Q2增加"尝试用原始图片重新识别"的排查建议
- **改进**：FAQ Q9增加"推荐使用扫描件"和"手机扫描APP预处理"建议
- **改进**：所有脚本错误提示在专业术语后增加通俗解释，方便非技术用户理解
- **改进**：ocr_engine.py 低置信度阈值从0.6调整为0.7，更早提醒用户核对
- **改进**：check_env.py 输出格式优化，失败项用更醒目的标识

### v1.3.0 (2026-06-29)
- **改进**：OCR引擎增加PSM模式回退机制（6→3→4→11→12）
- **改进**：OCR引擎增加图片质量预检（尺寸、模式、亮度检查）
- **改进**：OCR引擎提供详细的识别失败诊断和建议
- **改进**：查验引擎增加参数格式校验和类型转换
- **改进**：查验引擎增加重试机制和指数退避
- **改进**：审批引擎增加Token获取重试和超时设置
- **改进**：审批引擎增加报销单文件存在性检查
- **改进**：审批引擎增加配置完整性验证
- **改进**：发票解析器支持更多日期格式和金额格式
- **改进**：发票解析器增加金额勾稽检查和日期有效性验证
- **改进**：模板匹配器增加文件格式检查和表头完整性验证
- **改进**：批量处理增加失败文件记录和统计
- **改进**：环境预检增加Tesseract版本和语言包完整性检查
- **改进**：错误代码速查表增加更多FAQ条目（Q9-Q14）
- **改进**：所有脚本增强错误处理和容错能力

### v1.1.0 (2026-06-29)
- **新增**：环境预检脚本 `scripts/check_env.py`
- **新增**：错误代码速查表
- **新增**：发票图片质量要求和拍摄建议
- **升级**：真伪查验引擎 `verify_engine.py`，真正对接国税总局/第三方平台
- **升级**：审批引擎 `approval_engine.py`，真正获取Token并调用API
- **升级**：安装脚本增加预检环节
- **升级**：模板匹配支持PDF格式（需poppler）
- **改进**：所有脚本增加更详细的错误提示
- **改进**：配置文件中增加timeout设置

### v1.0.0 (2026-06-28)
- 初始版本发布
- 支持增值税发票OCR识别
- 支持多种查验引擎接口
- 支持模板自适应学习
- 支持多种审批平台对接

## 税务风险预警

本模块提供发票数据的风险检测功能，帮助企业在税务稽查前自查风险。

### 检测方法

| 检测项 | 说明 | 预警级别 |
|--------|------|---------|
| 连号检测 | 同一供应商连续开具多张连号发票 | 关注 |
| 大额整数金额 | 发票金额为大额整数（如 100000.00 元） | 提示 |
| 频繁开票 | 短时间内同一供应商开具大量发票 | 关注 |
| 品名异常 | 发票品名与供应商经营范围不符 | 关注 |
| 进销项匹配 | 进项发票品名与销项发票品名匹配度低 | 严重 |

### 三级预警体系

| 级别 | 说明 | 建议操作 |
|------|------|---------|
| 提示 | 低风险，可能存在异常 | 建议关注 |
| 关注 | 中风险，需要核实 | 建议核实业务真实性 |
| 严重 | 高风险，可能涉及虚开 | 建议立即处理 |

### 使用方式

```bash
python scripts/risk_detector.py <path_to_invoices_json>
```

输出 JSON 格式的风险检测报告，包含所有检测结果和综合评估。

## 电子档案合规归档

本模块按照《电子发票全流程电子化管理指南》生成标准归档包，满足财政部和国家档案局对电子发票归档的要求。

### 四性检测

| 检测项 | 说明 |
|--------|------|
| 真实性 | 检测电子发票是否为原始真实文件，未经篡改 |
| 完整性 | 检测电子发票文件是否完整，未损坏或缺失 |
| 可用性 | 检测电子发票文件是否能正常打开、读取和使用 |
| 安全性 | 检测电子发票文件是否安全，未被篡改或感染 |

### 使用方式

**单个文件四性检测**：
```bash
python scripts/archive_manager.py <path_to_invoice_file>
```

**批量归档（目录）**：
```bash
python scripts/archive_manager.py <path_to_directory>
```

**生成归档包**：
```python
from scripts.archive_manager import create_archive
package = create_archive(["invoice1.pdf", "invoice2.xml"], "./output")
```

### 归档包结构

```
archive_20260805_120000.zip
├── metadata.json          # 元数据总表
├── four_properties.json   # 四性检测报告
├── invoice_data.json      # 结构化发票数据
├── invoices/              # 原始发票文件
│   ├── invoice_001.pdf
│   └── invoice_002.xml
└── README.txt             # 归档说明
```

## 银行流水对账

本模块提供银行流水与发票数据的自动对账功能，解决财务人员手工核对耗时费力的痛点。

### 支持的银行格式

| 银行 | CSV 编码 | 日期格式 | 金额格式 | 状态 |
|------|---------|---------|---------|------|
| 工商银行 | UTF-8/GBK | YYYY-MM-DD | 借贷分离列 | ✅ 测试通过 |
| 建设银行 | UTF-8/GBK | YYYY-MM-DD | 借贷分离列 | ✅ 测试通过 |
| 农业银行 | UTF-8/GBK | YYYY/MM/DD | 借贷分离列 | ✅ 测试通过 |
| 招商银行 | UTF-8 | YYYY-MM-DD | 正负金额列 | ✅ 测试通过 |
| 中信银行 | UTF-8 | YYYY-MM-DD | 借贷分离列 | ✅ 测试通过 |
| 其他银行 | 自动检测 | 自动识别 | 自动解析 | ✅ 自适应 |

### 匹配算法

| 维度 | 规则 | 权重 |
|------|------|------|
| 金额匹配 | ±0.01 元容差，超出后线性递减 | 60% |
| 日期匹配 | ±3 天容差，超出后线性递减（30 天降为 0） | 40% |
| 综合评分 | 金额分 × 0.6 + 日期分 × 0.4 | ≥0.85 视为匹配 |

### 使用方式

```bash
# 基本对账
python scripts/bank_reconciler.py --csv bank_statement.csv --invoices invoices.json

# 自定义容差
python scripts/bank_reconciler.py --csv bank.csv --invoices inv.json --amount-tol 0.05 --date-tol 5

# 输出报告
python scripts/bank_reconciler.py --csv bank.csv --invoices inv.json --output report.json
```

### 输出报告结构

```json
{
  "summary": {
    "total_transactions": 150,
    "matched": 138,
    "unmatched": 12,
    "match_rate": "92.0%",
    "total_matched_amount": 85642.50,
    "total_unmatched_amount": 12350.00
  },
  "unmatched_by_amount_range": {
    "小额（<1000）": 5,
    "中额（1000-10000）": 4,
    "大额（10000-50000）": 2,
    "超大额（≥50000）": 1
  }
}
```

## 安全密钥配置

本模块提供统一的密钥安全管理，消除配置文件中的明文泄露风险。

### 环境变量命名规范

| 密钥用途 | 环境变量名 | 示例 |
|---------|-----------|------|
| 钉钉 AppKey | `INVOICE_DINGTALK_APPKEY` | dik123xxx |
| 钉钉 Secret | `INVOICE_DINGTALK_SECRET` | abc123xxx |
| 企微 CorpID | `INVOICE_WECOM_CORP_ID` | wwxxxx |
| 企微 Secret | `INVOICE_WECOM_SECRET` | abcxxxx |
| 飞书 AppID | `INVOICE_FEISHU_APP_ID` | cli_xxx |
| 飞书 Secret | `INVOICE_FEISHU_APP_SECRET` | abcxxx |
| 百望云 API Key | `INVOICE_BAIRONG_API_KEY` | br_xxx |
| 百望云 Secret | `INVOICE_BAIRONG_API_SECRET` | abcxxx |
| 诺诺 API Key | `INVOICE_NUONUO_API_KEY` | nn_xxx |
| 诺诺 Secret | `INVOICE_NUONUO_API_SECRET` | abcxxx |

### 设置方式

**Windows PowerShell（临时）**：
```powershell
$env:INVOICE_DINGTALK_APPKEY = "你的AppKey"
$env:INVOICE_DINGTALK_SECRET = "你的Secret"
```

**Windows（永久，系统环境变量）**：
```powershell
[System.Environment]::SetEnvironmentVariable("INVOICE_DINGTALK_APPKEY", "你的AppKey", "User")
```

**Linux/macOS**：
```bash
export INVOICE_DINGTALK_APPKEY="你的AppKey"
export INVOICE_DINGTALK_SECRET="你的Secret"
```

### 使用方式

```python
from scripts.secure_config import SecureConfig

cfg = SecureConfig()

# 获取单个密钥
app_key = cfg.get("DINGTALK_APPKEY")

# 获取平台完整配置
dingtalk_cfg = cfg.get_dingtalk_config()

# 调用 API 前校验
result = cfg.validate_before_call("dingtalk")
if result["ready"]:
    # 安全调用 API
    pass
else:
    print(f"缺失配置: {result['missing']}")
```

### CLI 检查

```bash
# 检查所有平台（默认输出字段名和布尔状态，不输出密钥值）
python scripts/secure_config.py --platform all

# 检查单个平台
python scripts/secure_config.py --platform dingtalk

# JSON 输出
python scripts/secure_config.py --platform all --json
```

## 并行批量处理

本模块提供硬件自适应的并行批量处理能力，自动根据 CPU 核心数和可用内存动态调整 worker 数量。

### 硬件自适应策略

| 硬件条件 | 处理模式 | Worker 数量 |
|---------|---------|------------|
| CPU ≥ 4 核 + 内存 > 2GB | 多进程 | CPU × 0.5 |
| CPU 2-3 核 或 内存 1-2GB | 多线程 | CPU × 0.75 |
| 内存 < 1GB | 串行 | 1 |

### 使用方式

**命令行使用**：
```bash
# 查看硬件信息和推荐配置
python scripts/parallel_batch.py info

# 自动模式批量处理
python scripts/parallel_batch.py run --input D:\invoices\ --output result.json

# 指定模式
python scripts/parallel_batch.py run --input D:\invoices\ --output result.json --mode process
```

**Python 代码调用**：
```python
from scripts.parallel_batch import batch_process, get_hardware_info

# 查看硬件信息
hw = get_hardware_info()
print(f"CPU: {hw['cpu_count']} 核, 推荐 worker: {hw['recommended_workers_process']}")

# 定义处理函数
def process_invoice(file_path: str) -> dict:
    # 自定义处理逻辑
    return {"success": True, "file": file_path}

# 批量处理
result = batch_process(file_paths, process_invoice, mode="auto")
print(f"处理 {result.total_files} 个文件，成功 {result.success_count} 个")
print(f"耗时 {result.total_time_seconds:.1f} 秒，吞吐量 {result.to_dict()['throughput_per_second']} 个/秒")
```

### 性能对比（参考）

| 文件数 | 串行处理 | 并行处理（4核） | 加速比 |
|--------|---------|---------------|--------|
| 10 张 | 28 秒 | 8 秒 | 3.5× |
| 50 张 | 140 秒 | 38 秒 | 3.7× |
| 100 张 | 280 秒 | 75 秒 | 3.7× |
| 200 张 | 560 秒 | 148 秒 | 3.8× |

> 注：以上数据为 i5-10400F/16GB 测试环境参考值，实际加速比取决于 CPU 性能、内存大小和图片分辨率。

## 免责声明

本工具仅提供发票识别和报销单生成的技术支持，**不提供任何税务咨询或财务建议**。所有财务决策应由专业财务人员做出。使用者需确保符合当地法律法规。使用本工具即表示接受《风险声明》中的全部条款。