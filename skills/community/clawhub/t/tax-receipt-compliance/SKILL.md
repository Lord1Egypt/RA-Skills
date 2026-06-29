---

---
---
name: tax-receipt-compliance
slug: tax-receipt-compliance
displayName: 财税合规全链路助手
description: 财税合规全链路助手：发票OCR识别→真伪查验→报销单自动填充→对接审批系统。企业自主配置，数据本地处理。
version: 2.5.0
category: 财税管理
appName: 财税合规
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
---

# 财税合规全链路助手

> ⚠️ **使用必读**：本Skill所有功能在本地运行，发票数据绝不外传，但**绝不提供税务咨询**。使用前请先阅读【限制说明】和【风险声明】。

## 功能说明

本Skill提供从发票识别到审批提交的**全链路**财税合规能力。

| 模块 | 功能 | 状态 | 输入 | 输出 |
|------|------|------|------|------|
| 1. 发票OCR识别 | Tesseract本地识别增值税发票 | ✅ 直接可用 | 发票图片 | 结构化JSON |
| 2. 真伪查验 | 对接查验平台，自动获取结果 | ⚠️ 需配置密钥 | 发票代码/号码 | 查验结果 |
| 3. 报销单填充 | 自适应学习模板，一键填充 | ✅ 直接可用 | 发票数据+模板 | Excel文件 |
| 4. 审批对接 | 对接钉钉/企微/飞书审批 | ⚠️ 需配置密钥 | 报销单+配置 | 审批结果 |

> ✅ = 装即用 ｜ ⚠️ = 需在 config.yaml 中配置对应API密钥

### 设计理念

1. **数据安全第一**：所有发票数据处理均在本地，不会上传到任何服务器
2. **企业自主决策**：查验引擎、审批平台的选择权完全交给企业
3. **透明开源**：所有代码可见可审计，无隐藏后门
4. **渐进披露**：基础功能开箱即用，高级功能按配置解锁

## 触发词

| 意图 | 触发词 |
|------|--------|
| 识别发票 | "识别这张发票"、"OCR发票"、"扫描发票" |
| 查验真伪 | "查验这张发票"、"查发票真伪" |
| 生成报销单 | "用XX模板生成报销单"、"填报销单" |
| 提交审批 | "提交报销审批"、"发起审批"、"报销审批" |
| 批量处理 | "批量识别"、"批量报销" |

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

> 💡 **提示**：基础功能（发票识别、报销单生成）只需完成环境安装即可使用，无需配置API密钥。查验和审批功能才需要配置API密钥。

## 快速开始



### 第一步：环境准备（必做，5分钟完成）

**Windows用户**（一键安装）：
```powershell
# 自动下载并安装Tesseract（使用国内镜像，速度快）
.\scripts\install_tesseract.ps1
```

**Linux/macOS用户**：
```bash
bash ./scripts/install_tesseract.sh
```

**安装Python依赖**：
```bash
pip install Pillow pytesseract openpyxl pyyaml
```

> 安装完成后运行预检脚本检查环境：
> ```bash
> python scripts/check_env.py
> ```

### 第二步：配置（可选，基础功能无需配置）

```bash
# 复制配置模板
cp templates/config_template.yaml config.yaml
```

> 💡 **新手提示**：不编辑 `config.yaml` 也能使用基础功能（发票识别、报销单生成）。只有查验真伪和提交审批才需要配置对应API密钥。

### 第三步：开始使用

```bash
# 识别单张发票（直接可用，无需配置）
python scripts/ocr_engine.py --input path/to/invoice.png --output receipt.json

# 生成报销单（直接可用，无需配置）
python scripts/template_matcher.py fill --config config.yaml --receipt receipt.json --template templates/expense_basic.xlsx

# 查验发票真伪（需先配置查验引擎）
python scripts/verify_engine.py --invoice-code 3100204130 --invoice-number 00564189 --date "2026年06月28日" --amount 10000

# 提交审批（需先配置审批平台）
python scripts/approval_engine.py --config config.yaml --expense expense_output.xlsx

# 环境预检
python scripts/check_env.py
```

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

### 功能限制

| 限制项 | 具体说明 |
|--------|---------|
| OCR识别 | 仅支持增值税发票（专票/普票/电子票） |
| 暂不支持 | 手写发票、定额发票、机动车发票、二手车发票 |
| 查验功能 | 需企业自行申请API密钥，Skill不代为申请 |
| 审批功能 | 需企业管理员在对应平台开通审批API权限 |

### 技术限制

| 限制项 | 具体说明 |
|--------|---------|
| 运行环境 | Python 3.8+ |
| 必须安装 | Tesseract OCR + 中文语言包 |
| 图片格式 | PNG/JPG/TIFF/PDF（PDF需要poppler） |
| 语言 | 中文简体，其他语言准确率显著下降 |
| 并发 | 单线程处理，一次一张 |

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
| `Tesseract not found` | Tesseract未安装或未加入PATH | 运行 `install_tesseract.ps1` 并重启终端 |
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

- 问题反馈：请在SkillHub平台提交Issue
- 功能建议：欢迎提交Pull Request
- 邮箱：联系Skill开发者

## 更新日志

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

## 免责声明

本工具仅提供发票识别和报销单生成的技术支持，**不提供任何税务咨询或财务建议**。所有财务决策应由专业财务人员做出。使用者需确保符合当地法律法规。使用本工具即表示接受《风险声明》中的全部条款。