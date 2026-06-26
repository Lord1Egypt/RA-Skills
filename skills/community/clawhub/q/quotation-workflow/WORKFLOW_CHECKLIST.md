# 报价单生成工作流检查清单 ⭐

**位置：** `/Users/wilson/.openclaw/workspace/monorepo/super-sales-agent/skills/quotation-workflow/`

**版本：** v2.0 (2026-03-27) - 集成自动化验证

---

## 🔴 P0 改进措施（2026-03-27 已完成）

### 新增功能

1. **quotation_schema.py** - 完整数据验证模块
   - 客户信息验证（公司名称/邮箱/地址/电话）
   - 报价单号格式验证（QT-YYYYMMDD-XXX）
   - 产品数据验证（名称/数量/价格）
   - 贸易条款验证（Incoterms/货币/交期）
   - 日期验证（格式/逻辑）

2. **pre_send_checklist.py** - 发送前强制检查清单
   - 客户来源检查（OKKI 关联）
   - 邮箱域名检查
   - 产品列表检查
   - 总金额计算检查
   - 附件就绪检查

3. **generate-all.sh 集成验证**
   - 生成前自动运行数据验证
   - 验证失败立即终止流程
   - 无交互确认（强制失败）

### 验证规则

| 检查项 | 规则 | 失败处理 |
|--------|------|----------|
| 公司名称 | 不能包含 example/test/sample/xxx 等关键词 | ❌ 终止 |
| 邮箱域名 | 不能是 example.com/test.com/公共邮箱 | ❌ 终止 |
| 地址 | 不能是占位符（123 xxx street） | ❌ 终止 |
| 电话 | 不能是 123456789/000000000 等占位符 | ❌ 终止 |
| 报价单号 | 必须是 QT-YYYYMMDD-XXX 格式 | ❌ 终止 |
| 产品列表 | 不能为空，名称不能是占位符 | ❌ 终止 |
| 价格 | 必须是有效数值，>0 且 <100 万 | ❌ 终止 |
| 总金额 | 必须与计算结果匹配 | ❌ 终止 |

---

## ⚠️ 历史错误记录

### 2026-03-15 严重错误

**错误 1：使用示例报价单而非客户专属报价单**
- ❌ 给 SPECIALIZED COMPUTER PRODUCTS USA 发送了 `QT-TEST-001-Final.pdf`（示例文件）
- ❌ 没有为客户生成专属报价单

**错误 2：模板字段名不匹配**
- ❌ `customer.company_name` vs `customer.name`
- ❌ `product.unit_price` vs `product.unitPrice`
- ❌ `terms` 字典格式 vs 列表格式
- **结果：** 生成的报价单客户名/价格/条款全部空白

**错误 3：直接照抄模板内容（最严重）**
- ❌ 开发信模板包含 "Paul and QUADNET Team"（澳洲客户）
- ❌ 内容提到 "West Gladstone, Queensland"
- ❌ 收件人是意大利客户 LABEL ITALY
- **根本原因：** 没有根据客户信息定制内容，直接发送模板

---

## ✅ 正确工作流程

### Step 1: 收集客户信息

**必须收集的信息：**
```json
{
  "company_name": "客户公司全称",
  "contact": "联系人姓名",
  "country": "客户国家",
  "email": "客户邮箱",
  "industry": "客户行业（可选）"
}
```

**信息来源：**
- OKKI CRM 客户详情
- 往来邮件签名
- 客户网站
- 名片/展会资料

---

### Step 2: 创建报价单数据文件

**使用标准模板：** `template-standard.json`

```bash
cd /Users/wilson/.openclaw/workspace/monorepo/super-sales-agent/skills/quotation-workflow

# 复制模板
cp template-standard.json examples/QT-20260327-001-CUSTOMER.json

# 编辑文件，填入真实客户信息
# ⚠️ 必须修改的字段：
# - customer.company_name
# - customer.contact
# - customer.country
# - quotation.quotation_no
# - products[] (根据客户需求定制)
```

**字段兼容性说明：**

脚本支持以下多种字段名格式（自动兼容）：

| 字段 | 支持格式 1 | 支持格式 2 |
|------|-----------|-----------|
| 客户名称 | `customer.company_name` | `customer.name` |
| 联系人 | `customer.contact` | `customer.contact_name` |
| 单价 | `product.unit_price` | `product.unitPrice` |
| 报价单号 | `quotation.quotation_no` | `quotationNo` |
| 贸易条款 | `trade_terms.incoterms` | `terms.incoterms` |
| 交期 | `trade_terms.delivery` | `terms.delivery` / `lead_time` |

---

### Step 3: 生成报价单

```bash
# 生成所有格式（Excel + Word + HTML + PDF）
bash scripts/generate-all.sh examples/QT-20260327-001-CUSTOMER.json QT-20260327-001

# 只生成 HTML（快速测试）
bash scripts/generate-all.sh examples/QT-20260327-001-CUSTOMER.json QT-20260327-001 --html-only
```

**输出文件：**
- `QT-20260327-001.xlsx` - Excel 版本
- `QT-20260327-001.docx` - Word 版本
- `QT-20260327-001.html` - HTML 版本（推荐用于 PDF 导出）
- `QT-20260327-001-HTML.pdf` - 从 HTML 导出的 PDF（质量最佳）
- `QT-20260327-001-Excel.pdf` - 从 Excel 导出的 PDF

---

### Step 4: 验证报价单内容 ⭐⭐⭐（关键步骤！）

**必须检查的内容：**

```markdown
## 报价单验证清单

### 客户信息
- [ ] 客户公司名称正确（不是 "Example Customer Corp"）
- [ ] 联系人姓名正确（不是 "John Doe"）
- [ ] 客户地址正确（不是 "123 Business St"）
- [ ] 客户国家正确

### 产品信息
- [ ] 产品列表符合客户需求
- [ ] 数量正确
- [ ] 单价正确（不是 0 或空白）
- [ ] 总金额计算正确

### 贸易条款
- [ ] 报价单号正确（不是 "QT-TEST-001"）
- [ ] 日期正确
- [ ] 有效期正确
- [ ] 贸易条款（FOB/CIF 等）正确
- [ ] 货币单位正确（USD/EUR 等）
- [ ] 交期正确

### PDF 质量
- [ ] 背景色正常打印（Tailwind 背景色）
- [ ] 表格没有分页断裂
- [ ] 所有文字清晰可见
- [ ] 没有乱码或空白字段
```

**验证命令：**

```bash
# 在浏览器打开 HTML 预览
open examples/QT-20260327-001.html

# 或在 Finder 打开 PDF
open examples/QT-20260327-001-HTML.pdf
```

---

### Step 5: 发送邮件

**发送前最终检查：**

```markdown
1. [ ] 邮件正文已根据客户信息定制（不是模板原文）
2. [ ] 产品目录附件存在（`02-产品目录/SKW 2026 catalogue-15M.pdf`）
3. [ ] 报价单 PDF 附件存在且内容正确
4. [ ] 收件人邮箱正确
5. [ ] 抄送人邮箱正确（如有需要）
6. [ ] 邮件主题包含客户公司名或报价单号
```

**发送命令：**

```bash
cd /Users/wilson/.openclaw/workspace/skills/imap-smtp-email

node scripts/smtp.js send \
  --to "customer@example.com" \
  --subject "Quotation QT-20260327-001 - [Customer Name]" \
  --body-file "/path/to/customized-email.html" \
  --attach "/Users/wilson/.openclaw/workspace/monorepo/super-sales-agent/skills/quotation-workflow/examples/QT-20260327-001-HTML.pdf,/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf"
```

---

### Step 6: OKKI 同步（自动）

`generate-all.sh` 会自动调用 `okki-sync.js` 创建报价单跟进记录（trail_type=101）。

**手动同步（如需要）：**

```bash
cd /Users/wilson/.openclaw/workspace/skills/imap-smtp-email

node okki-sync.js quotation '{"dataFile":"/path/to/data.json","quotationNo":"QT-20260327-001"}'
```

---

## 🚫 禁止行为

### ❌ 绝对不要做的事情：

1. **禁止使用示例文件作为正式报价单**
   - ❌ `QT-TEST-001-Final.pdf`
   - ❌ `farreach_sample.json` 直接生成
   - ❌ `quadnet_quotation.json` 用于其他客户

2. **禁止直接发送模板内容**
   - ❌ 开发信模板中的 "Paul and QUADNET Team"
   - ❌ 模板中的 "West Gladstone, Queensland"
   - ❌ 模板中的 "Example Customer Corp"

3. **禁止不验证就发送**
   - ❌ 不检查 PDF 内容（客户名/价格/条款）
   - ❌ 不检查附件路径
   - ❌ 不检查收件人信息

4. **禁止重复使用报价单**
   - ❌ 给不同客户发送同一份报价单
   - ❌ 给同一客户发送过期的报价单

---

## 📋 快速参考

### 文件结构

```
quotation-workflow/
├── scripts/
│   ├── generate-all.sh              # 一键生成脚本
│   ├── generate_quotation_html.py   # HTML 生成
│   └── ...
├── examples/
│   ├── template-standard.json       # ⭐ 标准模板（复制使用）
│   ├── farreach_sample.json         # 示例数据（仅参考）
│   └── QT-20260327-001-CUSTOMER.json # 客户专属数据
├── output/
│   └── (生成的文件)
└── WORKFLOW_CHECKLIST.md            # 本文件
```

### 常用命令

```bash
# 快速生成（HTML only）
bash scripts/generate-all.sh examples/data.json OUTPUT --html-only

# 完整生成（所有格式 + OKKI 同步）
bash scripts/generate-all.sh examples/data.json OUTPUT

# 验证 JSON 格式
python3 -m json.tool examples/data.json > /dev/null && echo "✅ JSON 格式正确"
```

### 字段速查

```json
{
  "customer": {
    "company_name": "必填 - 客户公司名",
    "contact": "必填 - 联系人",
    "country": "必填 - 国家"
  },
  "quotation": {
    "quotation_no": "必填 - QT-YYYYMMDD-XXX"
  },
  "products": [
    {
      "description": "必填 - 产品描述",
      "quantity": "必填 - 数量",
      "unit_price": "必填 - 单价"
    }
  ]
}
```

---

## 📝 更新日志

| 日期 | 更新内容 | 原因 |
|------|----------|------|
| 2026-03-27 | 创建完整工作流检查清单 | 防止历史错误重演 |
| 2026-03-15 | 修复字段名兼容性问题 | `unitPrice` vs `unit_price` 不匹配 |
| 2026-03-15 | 添加模板内容定制原则 | 禁止照抄模板 |

---

**最后更新：** 2026-03-27  
**维护者：** WILSON  
**状态：** ✅ 已验证
