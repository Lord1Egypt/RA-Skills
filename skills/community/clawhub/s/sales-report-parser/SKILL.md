# sales-report-parser

销售报表图片 OCR 识别与大模型解析工具集

## 功能

从销售报表图片中提取数据，支持：
- 图片 OCR 文字识别（使用 cnocr）
- 大模型 JSON 解析（支持 MiniMax API）
- JSON 转 Excel 表格

## 工具

### 1. OCR 识别

```bash
cd /data/sales-report-parser/skills/sales-report-parser/scripts
pip install -r requirements.txt

# 识别图片中的文字
python ocr_images.py --image /path/to/image.jpg
```

### 2. 大模型 JSON 生成

```bash
python llm_json.py \
  --content "OCR识别结果文本" \
  --prompt "你的提示词" \
  --api_key "你的API密钥" \
  --output result.json
```

### 3. JSON 转 Excel

```bash
python json_to_excel.py --input result.json --output result.xlsx
```

### 4. 批量提取（推荐）

```bash
python batch_extract.py \
  --api_key "你的API密钥" \
  --image /path/to/images/ \
  --output my_output
```

## 参数说明

### ocr_images.py
- `--image/-i`: 图片路径（必需）

### llm_json.py
- `--content/-c`: 要处理的内容（必需）
- `--prompt/-p`: 提示词（必需）
- `--api_key/-k`: API 密钥（必需）
- `--output/-o`: 输出 JSON 路径（必需）
- `--base_url`: API 地址（默认 https://api.minimaxi.com/v1）
- `--model`: 模型名（默认 MiniMax-M2.5）
- `--temperature`: 温度（默认 1.0）

### json_to_excel.py
- `--input/-i`: 输入 JSON 文件（必需）
- `--output/-o`: 输出 Excel 文件（必需）
- `--sheet/-s`: 工作表名（默认 Sheet1）
- `--no-transpose`: 不转置表格
- `--no-sort`: 不按日期排序

### batch_extract.py
- `--api_key/-k`: API 密钥（必需）
- `--image/-i`: 图片或目录（必需）
- `--output/-o`: 输出文件名（默认 output）
- `--base_url`: API 地址
- `--retries`: 重试次数（默认 3）

## 销售报表字段

```
日期, 总销售, 产品净销售, 现烤面包, 袋装面包, 软点, 西点, 中点, 蛋糕个数, 蛋糕金额, 卡劵, 交易次数
```

## 示例

```bash
# 完整流程示例
cd /data/sales-report-parser/skills/sales-report-parser/scripts

# 方式一：一步到位批量处理
python batch_extract.py \
  --api_key "your-api-key" \
  --image ../ \
  --output sales_data

# 方式二：分步骤处理
# 1. OCR 识别
python ocr_images.py --image 1,8.png

# 2. 大模型解析（将 OCR 结果粘贴到 content）
python llm_json.py \
  --content "OCR识别结果" \
  --prompt "提取销售数据..." \
  --api_key "your-api-key" \
  --output data.json

# 3. 转 Excel
python json_to_excel.py --input data.json --output data.xlsx
```

## 依赖

```
cnocr
langchain-openai
langchain-core
pandas
openpyxl
pillow
pydantic
```
