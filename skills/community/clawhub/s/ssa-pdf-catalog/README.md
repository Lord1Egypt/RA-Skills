# PDF 产品目录提取 Skill - 快速开始

## 🚀 5 分钟上手

### 1. 安装依赖

```bash
# 系统依赖
brew install poppler

# Python 依赖
pip3 install docling openpyxl
```

### 2. 运行提取

```bash
cd /Users/wilson/.openclaw/workspace

python3 skills/pdf-product-catalog/scripts/extract.py \
  --pdf-dir "/Users/wilson/Library/CloudStorage/GoogleDrive-cjboy0756@gmail.com/我的云端硬盘/Job/产品资料/599" \
  --output-dir "./knowledge-base/客户/599" \
  --verbose
```

### 3. 查看结果

```bash
# 查看产品索引
cat knowledge-base/客户/599/产品索引.md

# 查看产品词条
ls knowledge-base/客户/599/类目词条/

# 查看 JSON 数据
cat knowledge-base/客户/599/产品详细数据.json | python3 -m json.tool
```

---

## 📋 输出文件

| 文件 | 说明 |
|------|------|
| `产品索引.md` | 58 个产品总表 |
| `类目词条/*.md` | 每个产品一个词条 |
| `产品详细数据.json` | 完整 JSON 数据 |

---

## ⚠️ 常见错误排除

### 错误 1: BJ0599-XXXX 被误认为模具号

**现象：** 模具号显示为 BJ0599-0001

**原因：** BJ0599-XXXX 是包装规范

**解决：** 脚本已自动排除，如仍有问题检查 `extract_model_no()` 函数

### 错误 2: 模具号与客户品名相同

**现象：** 模具号 = GCHDMIFF（客户品名）

**原因：** PDF 的 MODEL NO. 在图片中

**解决：** 确保 docling 已安装，会自动启用 OCR

### 错误 3: OCR 失败

**现象：** 提示 "docling 未安装"

**解决：** 
```bash
pip3 install docling
```

---

## 🔧 自定义配置

### 添加已知映射

编辑 `scripts/extract.py` 中的 `KNOWN_MAPPINGS` 字典：

```python
KNOWN_MAPPINGS = {
    '599-001': {'model': 'GCHDMIFF', 'pkg': 'BJ0599-0001', 'items': ['GCHDMIFF'], 'lengths': []},
    # 添加你的映射...
}
```

### 调整 OCR 阈值

```bash
python3 scripts/extract.py \
  --pdf-dir "/path/to/pdfs" \
  --output-dir "./output" \
  --ocr-threshold 500  # 文本少于 500 字符时启用 OCR
```

---

## 📊 性能参考

| PDF 数量 | 处理方式 | 耗时 |
|---------|---------|------|
| 58 | pdftotext | ~10 秒 |
| 58 | OCR (全部) | ~5-10 分钟 |
| 58 | 混合（推荐） | ~30 秒 |

---

## 📚 更多信息

- 完整文档：`SKILL.md`
- 示例数据：`examples/`
- 输出目录：`output/`
