---
name: web-to-excel
description: |
  从网页抓取结构化数据并填写到任意 Excel 文件的通用技能。
  触发场景：
  - 用户说"帮我把网页上的参数填到 Excel"、"从网站抓数据到表格"、
    "网页参数录入 Excel"、"爬取数据并填写 Excel"、或任何类似表达
  - 用户提供网址和 Excel 文件，要求自动抓取并填写
  - 批量从多个网页抓取数据，填入 Excel 模板

  使用时用户会提供：① 目标 Excel 文件路径 ② 目标 Sheet 名称 ③ 填写范围 ④ 数据来源 URL
  本技能不硬编码任何具体网址、文件名或字段映射，全部信息由用户在使用时提供。
---

# Web → Excel 数据填充技能

## 核心工作流

```
用户发请求（含 URL + Excel 信息）
    ↓
① 询问确认   →  目标文件/Sheet/行范围/URL
② 连接浏览器  →  CDP 直连 Edge（端口 9334），复用已有标签
③ 探测字段   →  访问 URL，读取页面参数结构（处理 Lazy Loading）
④ 读取表头   →  读取 Excel 表头行，建立 {列字母: 字段名} 映射
⑤ 确认映射   →  模糊匹配 + 向用户展示字段对照表，请确认
⑥ 清空旧数据  →  若重新抓取同一范围，先清空目标行
⑦ 写入 Excel →  openpyxl 写入（只填空值，不覆盖已有）
⑧ 输出摘要   →  列出所有更新的行/列/值
```

### 关键改进点

| 步骤 | 改进内容 |
|------|---------|
| ③ 探测字段 | 新增 Lazy Loading 处理，多次滚动确保内容完整 |
| ④ 读取表头 | **新增**：每次动态读取 Excel 表头，不凭记忆映射 |
| ⑤ 确认映射 | **新增**：模糊匹配 + 双向确认，输出映射表让用户验证 |
| ⑥ 清空旧数据 | **新增**：重新抓取时先清空，避免数据叠加污染 |

## 🚀 任务启动提示（必须先执行）

**在开始任何工作前，先向用户展示以下最佳 Prompt 建议：**

---

### 📋 最佳 Prompt 模板

```
请帮我把网页数据填入 Excel，信息如下：

1. **数据来源网站**：[URL 或网站名称]
   例如：https://58moto.com/xxx/configuration.html

2. **目标 Excel 文件**：[文件路径]
   例如：~/Desktop/TVS_Motorcycle.xlsx

3. **Sheet 名称**：[Sheet名]
   例如：OEM Database V2

4. **填写位置**：[行号范围] [列范围（可选）]
   例如：第 42-83 行
   例如：第 5 行的 C-F 列

5. **特殊要求**（可选）：
   - [ ] 是否需要清空旧数据？
   - [ ] 是否需要价格换算（如 CNY→EUR）？
   - [ ] 是否有特定字段映射需求？
   - [ ] 其他说明：______
```

---

### 💡 快捷使用示例

**最小化输入**（使用默认流程）：
> "帮我把 https://58moto.com/xxx 的数据填入 ~/Desktop/data.xlsx 的 Sheet1，从第5行开始"

**完整输入**（包含特殊要求）：
> "请帮我把网页数据填入 Excel：
> - 网站：https://58moto.com/product/config.html
> - Excel：~/Desktop/TVS_Motorcycle.xlsx
> - Sheet：OEM Database V2
> - 位置：第 42-83 行
> - 特殊要求：价格需要从 CNY 换算为 EUR，清空旧数据"

---

### ⚠️ 启动检查清单

收到任务后，按以下顺序确认信息：

| # | 信息项 | 必需？ | 默认值 |
|---|--------|--------|--------|
| 1 | 数据来源 URL | ✅ 必需 | 无 |
| 2 | Excel 文件路径 | ✅ 必需 | 无 |
| 3 | Sheet 名称 | ✅ 必需 | 无 |
| 4 | 填写行范围 | ✅ 必需 | 无 |
| 5 | 填写列范围 | ❌ 可选 | 自动匹配 |
| 6 | 是否清空旧数据 | ❌ 可选 | 否 |
| 7 | 价格换算 | ❌ 可选 | 不换算 |
| 8 | 特殊字段映射 | ❌ 可选 | 自动匹配 |

**信息不完整时**：向用户询问缺失的必需项，并提供上述 Prompt 模板。

**信息完整时**：直接开始执行，无需再次确认。

---

## Step ①：询问确认

首次使用或信息不足时，向用户询问：

> **请提供以下信息：**
> 1. **Excel 文件路径**（如 `~/Desktop/data.xlsx`）
> 2. **Sheet 名称**（如 `Sheet1`）
> 3. **填写范围**（起始行～结束行，或具体行号，如 `第 5～10 行`）
> 4. **数据来源 URL**（参数配置页，如 `https://example.com/product/config.html`）
> 5. **列映射需求**（若与默认映射不同，或有特殊字段对应关系）
> 6. **多车型/多列**：若网页有多个产品列（如 FX 第 1 列、NX 第 2 列），告知分别对应哪一行

## Step ②：连接浏览器（CDP）

```python
import subprocess, importlib, sys, time

# 自动安装依赖
for pkg in ['websockets', 'openpyxl']:
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

sys.path.insert(0,
    '~/Library/Application Support/QClaw/openclaw/config/skills/browser-cdp/scripts')
from cdp_client import CDPClient

client = CDPClient('http://127.0.0.1:9334')  # Edge CDP 端口（Mac 默认 9334）
client.connect()
tabs = client.list_tabs()

# 查找已打开的匹配标签
target_tab = None
for t in tabs:
    if url[:40] in t['url']:
        target_tab = t
        print(f'  → 复用已有标签: {t["id"]} | {t["url"]}')
        break

if not target_tab:
    client.create_tab(url)
    time.sleep(3)
    tabs = client.list_tabs()
    for t in tabs:
        if url[:40] in t['url']:
            target_tab = t
            break

client.attach(target_tab['id'])
time.sleep(2)
```

## Step ③：探测字段

访问目标页面，抓取参数配置区域文本：

```python
# 方法1：从"参考价"关键词位置往后截取（适合摩托范等汽车参数站）
result = client.send("Runtime.evaluate", {
    "expression": "(function(){"
        "var t=document.body.innerText;"
        "var i=t.indexOf('参考价');"
        "return i>=0 ? t.substring(i, i+25000) : 'NO_DATA';"
    "})()"
})
text = result['result']['value']

# 方法2：截取包含参数的完整区域（通用）
result2 = client.send("Runtime.evaluate", {
    "expression": "(function(){"
        "var t=document.body.innerText;"
        "return t.length > 50000 ? t.substring(0, 50000) : t;"
    "})()"
})
text = result2['result']['value']
```

解析为结构化字典：

```python
def parse_params(text):
    """
    将网页参数文本（制表符分隔）解析为：
    - field_data: {字段名: [值列表]}   # 同一字段多列的值
    - column_names: [第1列车型名, 第2列车型名, ...]
    """
    lines = [l for l in text.strip().split('\n')
             if l.strip() and '\t' in l]
    if not lines:
        return {}, []
    header = lines[0].split('\t')          # [字段名, col1名, col2名, ...]
    column_names = header[1:]               # 跳过第一列（字段名列）
    field_data = {}
    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) < 2:
            continue
        field = parts[0].strip()
        values = parts[1:]
        if field not in field_data:
            field_data[field] = values
    return field_data, column_names

field_data, column_names = parse_params(text)
print(f'网页列头: {column_names}')
print(f'字段数量: {len(field_data)} 个')
```

## Step ④：确认字段映射

向用户展示映射表：

```
| Excel 列 | Excel 字段名    | 网页字段名          | 操作 |
|----------|---------------|-------------------|------|
| AI       | 最大功率(kW)   | 电机最大功率       | ← 请确认 |
| AJ       | 额定功率(kW)   | 电机额定功率       | ← 请确认 |
...
```

**标准中文→列映射**（适合摩托范等汽车参数站）：

| Excel 列 | 中文表头关键词 | 网页字段名（常见） |
|----------|-------------|----------------|
| AI | 最大功率 | `电机最大功率`、`最大功率` |
| AJ | 额定功率 | `电机额定功率`、`额定持续功率` |
| AK | 电压 | `额定电压(V)`、`电压` |
| AL | 电池kWh | `电池能量(kWh)`、`电池容量` |
| AN | 扭矩 | `电机最大扭矩(N·m)` |
| AP | 续航 | `官方续航里程(km)` |
| AZ | 前制动 | `前制动系统`、`前制动` |
| BA | 后制动 | `后制动系统`、`后制动` |
| BE | 前轮胎 | `前轮规格`、`前轮胎` |
| BF | 后轮胎 | `后轮规格`、`后轮胎` |
| BB | 轴距 | `轴距(mm)` |
| BI | 整备质量 | `整备质量(kg)` |
| BJ | 最大允许总质量 | `最大允许总质量`（通常 = 整备质量 + 载荷）|
| BK | 最高车速 | `最高车速(km/h)` |
| BM | 载荷 | `最大有效载荷(kg)` |
| BO | 价格 | `参考价` |
| AV | 前悬挂 | `前悬挂系统` |
| AW | 后悬挂 | `后悬挂系统` |
| AT | 车架结构 | `车架型式` |
| AS | 传动方式 | `传动方式`、`驱动形式` |

**用户可自定义映射**：告知用户可直接在对话中告诉我"网页的 `XX` 字段对应 Excel 的 `YY` 列"，我会添加到映射中。

## Step ⑤：写入 Excel

```python
from openpyxl import load_workbook

wb = load_workbook(excel_path)
sheet = wb[sheet_name]

def col_to_num(letter):
    """列字母 → 列号（A=1, Z=26, AA=27...）"""
    num = 0
    for c in letter.upper():
        num = num * 26 + (ord(c) - ord('A') + 1)
    return num

def clean_val(v):
    """清洗值：去除¥符号、逗号、空格，暂无报价→跳过"""
    if v is None: return None
    s = str(v).strip().replace('¥','').replace(',','').replace(' ','')
    if s in ('-','暂无报价','','None','—'): return None
    try: return float(s)
    except: return s.strip()

def write_row(sheet, row_num, field_data, col_idx, field_map):
    """向指定行写入，col_idx=网页列索引（0=第1列车型）"""
    updates = []
    for web_field, excel_col in field_map.items():
        if web_field not in field_data:
            continue
        vals = field_data[web_field]
        if col_idx >= len(vals):
            continue
        raw = vals[col_idx]
        val = clean_val(raw)
        if val is None:
            continue
        col_num = col_to_num(excel_col)
        old = sheet.cell(row_num, col_num).value
        if old is None:                      # 只填空值，不覆盖已有
            sheet.cell(row_num, col_num).value = val
            updates.append((row_num, excel_col, col_num, field_data.get('参考价', ['']*99)[col_idx], None, val))
    return updates

# 执行写入
all_updates = []
for row_num in range(start_row, end_row + 1):
    name = sheet.cell(row_num, 10).value    # J列=车型/产品名
    col_idx = user_specified_index         # 0=第1列, 1=第2列...
    ups = write_row(sheet, row_num, field_data, col_idx, field_map)
    all_updates.extend(ups)
    if ups:
        print(f'  ✅ 行{row_num} {str(name):<30} 更新了 {len(ups)} 个字段')

wb.save(excel_path)
print(f'\n✅ 已保存: {excel_path}')
```

## Step ⑥：输出变更摘要

```python
def make_report(excel_path, sheet_name, start_row, end_row, updates):
    lines = [
        f'📊 数据填充完成报告',
        f'文件 : {excel_path}',
        f'Sheet: {sheet_name}',
        f'填写范围: 第 {start_row}～{end_row} 行',
        '',
    ]
    if updates:
        lines.append(f'{"行":<5} {"列":<6} {"新值"}')
        lines.append('-' * 50)
        for row, col, col_num, name_or_price, old, new in updates:
            lines.append(f'  行{row:<3} {col:<6} {new}')
    else:
        lines.append('⚠️ 无更新（目标单元格可能已有数据）')
    return '\n'.join(lines)

print(make_report(excel_path, sheet_name, start_row, end_row, all_updates))
```

## 多 URL 批量处理

若用户提供多个 URL（每个产品一页）：

```python
urls_and_rows = [
    (row33, 'https://.../FX/configuration.html'),
    (row34, 'https://.../NX/configuration.html'),
    (row35, 'https://.../NS/configuration.html'),
]
for row_num, url in urls_and_rows:
    # 对每个 URL：连接浏览器 → 抓取 → 解析 → 写入 → 记录
    pass
```

## 注意事项

- **只填空值**：写入前检查 `sheet.cell(row, col).value is None`，不覆盖已有数据
- **价格清洗**：`¥12,999` → `12999`，`暂无报价` → 跳过
- **多 tab 复用**：已有目标 URL 的 tab 时，直接 `attach` 复用，不重复创建
- **参数页结构**：参数内容通常在 `configuration.html` 子页面
- **网页字段探测**：若第一行非参数表，先 `accessibility_tree()` 查看页面结构
- **用户自定义**：任何字段映射都可在对话中实时告知，无需修改代码

---

## ⚠️ 通用最佳实践（必须遵循）

### 1. 每次动态读取 Excel 表头，不凭记忆映射

```python
def build_excel_header_map(sheet, header_row=16):
    """读取 Excel 表头行，建立 {列字母: 字段名} 映射"""
    import openpyxl.utils
    header_map = {}
    for col in range(1, 200):
        val = sheet.cell(header_row, col).value
        if val:
            letter = openpyxl.utils.get_column_letter(col)
            header_map[letter] = str(val).strip()
    return header_map

# 使用示例
header_map = build_excel_header_map(sheet, header_row=16)
print(f"Excel 表头: {header_map}")
```

### 2. 字段映射双向确认

```python
def confirm_field_mapping(field_data, header_map, field_keywords):
    """
    建立网页字段 → Excel列 的映射，并向用户展示确认
    
    field_keywords: {Excel列: [可能的关键词列表]}
    例如: {'BM': ['载荷', '有效载荷', 'payload', '载重'],
           'BI': ['整备质量', '重量', 'weight', 'kg']}
    """
    mapping = {}
    print("📋 字段映射确认：")
    print(f"{'Excel列':<8} {'Excel字段名':<25} {'网页字段名':<20} {'状态'}")
    print("-" * 70)
    
    for excel_col, keywords in field_keywords.items():
        excel_field = header_map.get(excel_col, '未知')
        matched = None
        for web_field in field_data.keys():
            if any(kw in web_field for kw in keywords):
                matched = web_field
                break
        if matched:
            mapping[matched] = excel_col
            print(f"{excel_col:<8} {excel_field:<25} {matched:<20} ✅ 匹配")
        else:
            print(f"{excel_col:<8} {excel_field:<25} {'--':<20} ⚠️ 未匹配")
    
    return mapping

# 向用户展示映射表，等待确认后再写入
```

### 3. 写入前清空旧数据（重新抓取时）

```python
def clear_range(sheet, start_row, end_row, cols_to_clear):
    """清空指定范围的单元格（重新抓取同一范围时使用）"""
    for row in range(start_row, end_row + 1):
        for col in cols_to_clear:
            sheet.cell(row, col).value = None
    print(f'已清空行 {start_row}-{end_row} 的 {len(cols_to_clear)} 列')

# 使用前询问用户
# user_confirm = input("是否清空目标行的旧数据？(y/n): ")
# if user_confirm.lower() == 'y':
#     clear_range(sheet, start_row, end_row, list(field_map.values()))
```

### 4. 变体数量验证

```python
def validate_variant_count(field_data, column_names, expected_count=None):
    """
    验证网页列数与预期变体数是否匹配
    expected_count=None 时不验证，仅输出信息
    """
    web_columns = len(column_names)
    print(f"📊 网页列数: {web_columns}")
    print(f"   列名: {column_names[:5]}{'...' if len(column_names) > 5 else ''}")
    
    if expected_count is not None and web_columns != expected_count:
        print(f'⚠️ 警告：网页有 {web_columns} 列，但预期 {expected_count} 个变体')
        print('   可能存在数据丢失或多余列，请检查！')
        return False
    return True
```

### 5. Lazy Loading 处理

```python
def handle_lazy_loading(client, min_chars=10000, max_scrolls=5):
    """
    处理页面懒加载，确保内容完整抓取
    """
    for i in range(max_scrolls):
        # 获取当前页面文本
        result = client.send("Runtime.evaluate", {
            "expression": "document.body.innerText.length"
        })
        current_len = result['result']['value']
        
        if current_len >= min_chars:
            print(f"✅ 页面内容完整 ({current_len} 字符)")
            break
        
        # 滚动到底部
        client.send("Runtime.evaluate", {
            "expression": "window.scrollTo(0, document.body.scrollHeight)"
        })
        time.sleep(1.5)
        print(f"  滚动 {i+1}/{max_scrolls}，当前 {current_len} 字符")
    else:
        print(f"⚠️ 滚动 {max_scrolls} 次后仍未达到预期长度")
```

---

## 🚫 常见错误警示

| 错误做法 | 正确做法 |
|---------|---------|
| 凭上次任务的映射直接套用 | 每次重新读取 Excel 表头，动态建立映射 |
| 假设某列固定对应某字段 | 通过关键词匹配 + 用户确认建立映射 |
| 重新抓取时不清空旧数据 | 先清空目标行，再写入新数据 |
| 忽略变体数量不匹配 | 验证网页列数 = 预期变体数，不等则报警 |
| 页面内容截断就写入 | 多次滚动触发懒加载，确认内容完整
