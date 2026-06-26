# 📋 报价单工作流 - 实施进度

**创建时间：** 2026-03-14  
**状态：** Phase 1 核心功能已完成 ✅

---

## ✅ 已完成功能

### 1. Excel 报价单生成
**脚本位置：** `/Users/wilson/.openclaw/workspace/skills/excel-xlsx/scripts/generate_quotation.py`

```bash
# 创建空白模板
python3 generate_quotation.py --template /path/to/template.xlsx

# 使用测试数据生成
python3 generate_quotation.py --output /path/to/QT-20260314-001.xlsx --quick-test

# 从 JSON 数据生成
python3 generate_quotation.py --data quotation_data.json --output /path/to/QT-20260314-001.xlsx
```

**功能特性：**
- ✅ 标准报价单格式（公司 Logo/联系信息）
- ✅ 客户信息区域
- ✅ 产品列表表格（支持公式自动计算）
- ✅ 汇总区域（小计/运费/税费/总计）
- ✅ 备注和条款
- ✅ 签名区域
- ✅ 货币格式（#,##0.00）
- ✅ 日期处理（Excel 序列号转换）

### 2. Excel 读取功能
**脚本位置：** `/Users/wilson/.openclaw/workspace/skills/excel-xlsx/scripts/read_excel.py`

```bash
# 读取 Excel 文件
python3 read_excel.py "path/to/file.xlsx"

# 指定 Sheet
python3 read_excel.py "file.xlsx" --sheet "产品列表"

# 表格格式输出
python3 read_excel.py "file.xlsx" --format table -v

# JSON 格式输出（默认）
python3 read_excel.py "file.xlsx" --format json
```

**功能特性：**
- ✅ 支持通配符批量读取
- ✅ 多 Sheet 支持
- ✅ 智能类型转换（日期/数字/文本）
- ✅ 公式识别
- ✅ 1900/1904 日期系统处理
- ✅ 中文文件名编码兼容

### 3. Word 报价单生成
**脚本位置：** `/Users/wilson/.openclaw/workspace/skills/word-docx/scripts/generate_quotation_docx.py`

```bash
# 创建空白模板
python3 generate_quotation_docx.py --template /path/to/template.docx

# 使用测试数据生成
python3 generate_quotation_docx.py --output /path/to/QT-20260314-001.docx --quick-test

# 从 JSON 数据生成
python3 generate_quotation_docx.py --data quotation_data.json --output /path/to/QT-20260314-001.docx
```

**功能特性：**
- ✅ 专业格式排版
- ✅ 表格布局（客户信息/产品列表/汇总）
- ✅ 样式定义（字体/颜色/对齐）
- ✅ 自动金额计算
- ✅ 签名区域

### 4. Word 读取功能
**脚本位置：** `/Users/wilson/.openclaw/workspace/skills/read-docx/read-docx.py`

```bash
# 读取 DOCX 文件（支持通配符）
python3 read-docx.py "path/*.docx"

# 详细模式
python3 read-docx.py "exams/HDMI*.docx" -v
```

---

## ✅ 已完成功能（续）

### 5. PDF 导出 ✅（2026-03-14 新增）
**LibreOffice 已安装** 🍺

```bash
# 单个文件转换
soffice --headless --convert-to pdf QT-20260314-001.xlsx --outdir ./output/
soffice --headless --convert-to pdf QT-20260314-001.docx --outdir ./output/

# 批量转换（使用脚本）
/Users/wilson/.openclaw/workspace/skills/quotation-workflow/scripts/convert-to-pdf.sh *.xlsx *.docx

# 指定输出目录
OUTPUT_DIR=/path/to/output ./convert-to-pdf.sh QT-20260314-001.xlsx
```

### 2. OKKI CRM 集成 ⏳ Phase 2
- [ ] 从 OKKI 读取客户信息
- [ ] 从 OKKI 读取产品库
- [ ] 报价单关联客户 ID
- [ ] 自动创建跟进记录

### 3. 价格计算引擎 ⏳ Phase 2
- [ ] 价格阶梯逻辑（MOQ 折扣）
- [ ] 运费估算（按地区/重量）
- [ ] 税费计算（不同国家税率）
- [ ] 货币转换（USD/EUR/CNY）

### 4. 审批流程 ⏳ Phase 3
- [ ] 审批规则配置
- [ ] 多级审批工作流
- [ ] Discord/邮件通知
- [ ] 审批记录归档

### 5. 邮件发送集成 ⏳ Phase 3
- [ ] 邮件模板
- [ ] 附件自动附加
- [ ] 客户邮箱自动填充
- [ ] 发送记录归档

### 6. 归档与管理 ⏳ Phase 3
- [ ] 文件归档（按客户/日期分类）
- [ ] 版本控制
- [ ] 快速检索
- [ ] 有效期管理

---

## 📁 文件结构

```
quotation-workflow/
├── README.md                          # 本文档
├── quotation_data_template.json       # 数据模板（待创建）
└── examples/                          # 示例文件
    ├── QT-20260314-001.xlsx          # Excel 示例
    └── QT-20260314-001.docx          # Word 示例

skills/excel-xlsx/scripts/
├── read_excel.py                      # Excel 读取
└── generate_quotation.py              # Excel 报价单生成

skills/word-docx/scripts/
└── generate_quotation_docx.py         # Word 报价单生成

skills/read-docx/
└── read-docx.py                       # Word 读取（已有）
```

---

## 🧪 测试数据格式

```json
{
  "customer": {
    "company_name": "Test Customer Inc.",
    "contact": "John Doe",
    "email": "john@test.com",
    "phone": "+1-234-567-8900",
    "address": "123 Main St, City, Country"
  },
  "quotation": {
    "quotation_no": "QT-20260314-001",
    "date": "2026-03-14",
    "valid_until": "2026-04-13"
  },
  "products": [
    {
      "description": "HDMI 2.1 Ultra High Speed Cable",
      "specification": "8K@60Hz, 48Gbps, 2m",
      "quantity": 500,
      "unit_price": 8.50
    },
    {
      "description": "USB-C to USB-C Cable",
      "specification": "USB 4.0, 80Gbps, 100W PD, 1m",
      "quantity": 1000,
      "unit_price": 12.00
    }
  ],
  "currency": "USD",
  "payment_terms": "T/T 30% deposit, 70% before shipment",
  "lead_time": "15-20 days after deposit",
  "freight": 150.00,
  "tax": 0,
  "notes": "1. 以上价格基于当前原材料成本\n2. 最终价格以确认为准"
}
```

---

## 🚀 下一步

### 立即可用 ✅
1. ✅ Excel 报价单生成和读取
2. ✅ Word 报价单生成和读取
3. ✅ PDF 导出（LibreOffice 已安装）

### Phase 2 - OKKI 集成（下周）
1. ⏳ 连接 OKKI 产品库
2. ⏳ 实现价格计算引擎
3. ⏳ 客户信息自动填充

### Phase 3 - 审批与邮件（下下周）
1. 审批流程
2. 邮件发送
3. 归档管理

---

## 📝 使用说明

### 快速测试
```bash
cd /Users/wilson/.openclaw/workspace/skills/excel-xlsx/scripts

# 生成 Excel 报价单
python3 generate_quotation.py --output /tmp/test.xlsx --quick-test

# 查看内容
python3 read_excel.py /tmp/test.xlsx --format table
```

### 自定义数据
```bash
# 1. 创建 JSON 数据文件
cat > my_quotation.json << 'EOF'
{
  "customer": {
    "company_name": "Your Customer",
    "contact": "Contact Name",
    "email": "customer@example.com"
  },
  "quotation": {
    "quotation_no": "QT-20260314-002",
    "date": "2026-03-14",
    "valid_until": "2026-04-13"
  },
  "products": [
    {
      "description": "Product Name",
      "specification": "Spec details",
      "quantity": 100,
      "unit_price": 10.00
    }
  ],
  "currency": "USD",
  "payment_terms": "T/T",
  "lead_time": "15 days",
  "freight": 0,
  "tax": 0
}
EOF

# 2. 生成报价单
python3 generate_quotation.py --data my_quotation.json --output QT-20260314-002.xlsx
```

---

**最后更新：** 2026-03-14  
**维护者：** WILSON
