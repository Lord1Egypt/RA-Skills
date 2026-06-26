# 📋 报价单工作流 - 文档索引

**所有 Agent 统一入口** - 从这里开始使用报价单系统

---

## 🚀 快速使用（3 步）

```bash
# 1. 准备数据（复制示例修改）
cp /Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples/farreach_sample.json \
   my_quotation.json

# 2. 一键生成（Excel + Word + PDF）
/Users/wilson/.openclaw/workspace/skills/quotation-workflow/scripts/generate-all.sh \
  my_quotation.json QT-20260314-001

# 3. 查看结果
ls -lh QT-20260314-001.*
```

---

## 📚 文档导航

| 文档 | 用途 | 适合场景 |
|------|------|----------|
| **[QUICK_START.md](QUICK_START.md)** | 5 分钟快速上手 | 第一次使用，想快速生成报价单 |
| **[SKILL.md](SKILL.md)** | 技能标准文档 | 了解完整 API、数据格式、字段说明 |
| **[README.md](README.md)** | 完整功能文档 | 了解项目结构、实施进度、技术细节 |
| **[INDEX.md](INDEX.md)** | 本文档 | 快速找到需要的文档 |

---

## 🛠️ 脚本速查

| 功能 | 命令 | 示例 |
|------|------|------|
| **一键生成** | `generate-all.sh` | `./generate-all.sh data.json QT-001` |
| **Excel 生成** | `generate_quotation.py` | `python3 generate_quotation.py --data data.json -o out.xlsx` |
| **Word 生成** | `generate_quotation_docx.py` | `python3 generate_quotation_docx.py --data data.json -o out.docx` |
| **PDF 转换** | `convert-to-pdf.sh` | `./convert-to-pdf.sh *.xlsx *.docx` |
| **Excel 读取** | `read_excel.py` | `python3 read_excel.py file.xlsx --format table` |
| **Word 读取** | `read-docx.py` | `python3 read-docx.py "*.docx" -v` |

---

## 📁 关键路径

```
/Users/wilson/.openclaw/workspace/skills/quotation-workflow/
├── INDEX.md                    # 本文档（入口）
├── QUICK_START.md              # 快速开始
├── SKILL.md                    # 技能文档
├── README.md                   # 完整文档
├── quotation_data_template.json # 数据模板
├── examples/                   # 示例文件
│   ├── farreach_sample.json
│   ├── QT-20260314-001-Farreach.xlsx
│   ├── QT-20260314-001-Farreach.docx
│   └── QT-20260314-001-Farreach.pdf
└── scripts/
    ├── generate-all.sh         # 一键生成 ⭐
    ├── convert-to-pdf.sh       # PDF 批量转换
```

**相关技能：**
- Excel: `/Users/wilson/.openclaw/workspace/skills/excel-xlsx/scripts/`
- Word: `/Users/wilson/.openclaw/workspace/skills/word-docx/scripts/`
- 读取 DOCX: `/Users/wilson/.openclaw/workspace/skills/read-docx/`

---

## 🎯 常见使用场景

### 场景 1：快速报价（有客户数据）
```bash
# 修改示例数据
code my_quotation.json

# 一键生成
./generate-all.sh my_quotation.json QT-20260314-001

# 打开 PDF 检查
open QT-20260314-001.pdf
```

### 场景 2：批量报价（多个客户）
```bash
for file in customers/*.json; do
  ./generate-all.sh "$file" "$(basename $file .json)"
done
```

### 场景 3：查看已有报价单
```bash
# 查看 Excel 内容
python3 read_excel.py "QT-*.xlsx" --format table

# 查看 Word 内容
python3 read-docx.py "QT-*.docx" -v
```

### 场景 4：只生成 PDF（已有 Excel/Word）
```bash
./convert-to-pdf.sh QT-20260314-001.xlsx QT-20260314-001.docx
```

---

## 📞 需要帮助？

1. **查看快速指南** → `QUICK_START.md`
2. **查看数据格式** → `SKILL.md` 的"数据格式"章节
3. **查看示例** → `examples/farreach_sample.json`
4. **查看完整文档** → `README.md`

---

**最后更新：** 2026-03-14  
**维护者：** WILSON + All Agents
