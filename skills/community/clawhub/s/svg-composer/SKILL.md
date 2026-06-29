# SVG 拼接工具 (svg-composer)

> 将 SVG 符号进行横向/纵向拼接，支持内置字符集和四种拼接模式。

## 技能概述

本技能封装了 SVG 布局拼接核心功能，支持两种使用方式：

1. **内置字符集**（零依赖）：直接拼接 `0-9`、`A-Z` 等字符
2. **自定义符号**：从外部 SVG 文件加载符号进行拼接

**适用场景**：
- 图标/符号批量拼接（如数字、字母组合）
- 复合图标制作（多符号排列）
- Logo/徽章设计（多元素组合）
- 密码本/验证码生成（全排列组合）

## 内置字符集

### Font Awesome Free（默认）

**来源**：`@fortawesome/fontawesome-free` v7.2.0
**许可**：CC BY 4.0 + SIL OFL 1.1 + MIT
**支持字符**：`0-9`、`A-Z`（共36个）
**输入处理**：小写字母自动转为大写

**特性**：
- viewBox 高度统一为 512，宽度各异（256/320/384/448/576）
- 每个字符有独立的 advance_ratio，间距计算精确
- Y=0 在顶部（标准 SVG 坐标系）

**许可证说明**：
所有生成的 SVG 文件内部包含归属声明注释：
```xml
<!-- Icons provided by Font Awesome Free (CC BY 4.0) https://fontawesome.com/license/free -->
```
查看 SVG 源码即可看到完整许可证信息。

## 颜色支持

**仅支持两种颜色**：

| 颜色名 | 十六进制 | 说明 |
|--------|----------|------|
| `black` | `#000000` | 黑色（默认） |
| `white` | `#FFFFFF` | 白色 |

输入 `fill` 参数时接受：
- 颜色名称：`"black"` 或 `"white"`
- 十六进制：`"#000000"` 或 `"#FFFFFF"`

---

## 核心函数

### 1. compose_text - 基础拼接（推荐）

直接拼接文本字符串，无需外部 SVG 文件。

**参数说明**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str | — | 要拼接的文本，如 `"ABC123"` |
| `direction` | str | `'horizontal'` | 拼接方向：`'horizontal'` / `'vertical'` |
| `canvas_size` | tuple | `(640, 640)` | 画布尺寸 |
| `margin` | float/int | `0` | 字符间距（像素） |
| `align` | str | `'center'` | 对齐方式：`'center'` / `'start'` / `'end'` |
| `fill` | str | `'black'` | 填充颜色：`'black'` 或 `'white'` |
| `font_height_ratio` | float | `0.8` | 字体高度占画布比例 |
| `charset` | str | `'fa'` | 字符集：`'fa'`（默认） |

**返回值**：SVG 字符串

### 2. compose_sequence - 模式1：仅顺序

拼接输入顺序的文字，不做任何排列组合。

**示例**：
```python
# 输入 "ABC" -> 输出 SVG("ABC")
svg = compose_sequence("ABC", fill="black")
```

### 3. compose_permutations - 模式2：全排列

输入字符的全排列（不重复组合）。

**示例**：
```python
# 输入 "ABC" -> 输出 6 个 SVG: "ABC", "ACB", "BAC", "BCA", "CAB", "CBA"
svg_list = compose_permutations("ABC", fill="black")
# svg_list = [svg_abc, svg_acb, svg_bac, svg_bca, svg_cab, svg_cba]
```

### 4. compose_combinations - 模式3：笛卡尔积

可重复组合（密码本模式），生成所有可能的重复排列。

**示例**：
```python
# 输入 "ABC", length=3 -> 输出 27 个: AAA, AAB, AAC, ABA, ABB, ABC... CCC
svg_list = compose_combinations("ABC", length=3, fill="black")
```

### 5. compose_limited - 模式4：限制长度

限制每个组合的长度，生成所有长度的全排列。

**示例**：
```python
# 输入 "ABC", limit=2 -> 输出 12 个: A, B, C, AB, AC, BA, BC, CA, CB
svg_list = compose_limited("ABC", limit=2, fill="black")
```

### 6. layout_elements - 布局拼接

将多个 SVG 符号横向或纵向拼接成一个 SVG。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `elements` | list | — | 元素列表 `{'d': path_d, 'bbox': (...) }` |
| `direction` | str | `'horizontal'` | `'horizontal'` / `'vertical'` |
| `canvas_size` | tuple | `(640, 640)` | 画布尺寸 |
| `margin` | float/int | `0` | 元素间距 |
| `align` | str | `'center'` | `'center'` / `'start'` / `'end'` |
| `fill` | str | `'black'` | `'black'` 或 `'white'` |

### 7. load_symbols - 加载自定义符号

从文件夹批量加载 SVG 符号。

**参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `symbol_dir` | str | 符号文件夹路径（包含 .svg 文件） |

**返回值**：字典 `{symbol_name: {'d': path_d, 'bbox': (xmin,xmax,ymin,ymax)}}`

### 8. compose_number - 外部符号拼接（兼容）

使用外部 SVG 符号文件组合字符串（来自用户提供代码）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `target` | str | 目标字符串，如 `"A10"` |
| `symbol_files` | dict | `{字符: SVG文件路径}` |
| `fill` | str | `'black'` 或 `'white'` |
| `margin` | int | 符号间距（像素），默认 0 |

---

## 使用示例

### 示例 1：基础拼接（黑色）

```python
from svg_composer import compose_text

svg = compose_text("HELLO2026", fill="black", font_height_ratio=0.85)

with open('hello2026_black.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
```

### 示例 2：白色文字

```python
svg = compose_text("HELLO2026", fill="white", font_height_ratio=0.85)

with open('hello2026_white.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
```

### 示例 3：纵向排列

```python
svg = compose_text(
    "ABC",
    direction='vertical',
    canvas_size=(400, 600),
    margin=20,
    fill='white',
    font_height_ratio=0.7
)

with open('abc_vertical.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
```

### 示例 4：模式1 - 仅顺序

```python
from svg_composer import compose_sequence

svg = compose_sequence("ABC", fill="black")
# 输出: SVG("ABC")
```

### 示例 5：模式2 - 全排列

```python
from svg_composer import compose_permutations

svg_list = compose_permutations("ABC", fill="black")
# 输出: [SVG("ABC"), SVG("ACB"), SVG("BAC"), SVG("BCA"), SVG("CAB"), SVG("CBA")]

for i, svg in enumerate(svg_list):
    with open(f'perm_{i+1}.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
```

### 示例 6：模式3 - 笛卡尔积

```python
from svg_composer import compose_combinations

# 生成 3 位数字密码本 (0-9)
svg_list = compose_combinations("0123456789", length=3, fill="black")
# 输出: 1000 个 SVG (000, 001, 002, ... 999)

for i, svg in enumerate(svg_list):
    with open(f'code_{i:04d}.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
```

### 示例 7：模式4 - 限制长度

```python
from svg_composer import compose_limited

# 生成 1-2 位组合
svg_list = compose_limited("ABC", limit=2, fill="black")
# 输出: A, B, C, AB, AC, BA, BC, CA, CB (9个)

for i, svg in enumerate(svg_list):
    with open(f'combo_{i+1}.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
```

### 示例 8：使用外部 SVG 文件

```python
from svg_composer import compose_number

symbol_files = {
    'A': r"D:\symbols\A.svg",
    '1': r"D:\symbols\1.svg",
    '0': r"D:\symbols\0.svg",
}

svg = compose_number("A10", symbol_files, fill="black", margin=0)

with open('a10.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
```

### 示例 9：使用 load_symbols + layout_elements

```python
from svg_composer import load_symbols, layout_elements

# 加载外部符号文件夹
symbols = load_symbols(r"D:\PycharmProjects\icons")

# 横向拼接自定义符号
svg = layout_elements(
    elements=[symbols['A'], symbols['1'], symbols['0']],
    direction='horizontal',
    canvas_size=(640, 640),
    margin=10,
    fill='white'
)

with open('custom_icons.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
```

### 示例 10：批量模式生成 + 预览 HTML

```python
from svg_composer import batch_mode_compose_with_preview

svg_list, preview_path = batch_mode_compose_with_preview(
    output_dir="output",
    text="ABC",
    mode='permutations',  # 全排列
    fill='black',
    generate_preview=True  # 自动生成预览 HTML
)
print(f"预览页面: {preview_path}")
```

### 示例 11：生成预览 HTML（横向+纵向）

```python
from svg_composer import compose_text, generate_preview_html

output_dir = "output"
text = "HELLO"

# 生成预览 HTML（包含横向和纵向两个 SVG）
html_path = generate_preview_html(
    output_dir=output_dir,
    text=text,
    direction='horizontal',
    fill='black',
    font_height_ratio=0.8
)

print(f"预览页面已生成: {html_path}")
# 预览页面包含：
# 1. 下载链接（可点击下载 SVG 文件）
# 2. 文件夹路径链接（file:/// 协议可直接打开）
# 3. SVG 预览图（棋盘格背景）
```

---

## 四种拼接模式对比

| 模式 | 函数 | 输入 "ABC" 示例 | 数量 |
|------|------|-----------------|------|
| 模式1 | `compose_sequence` | ABC | 1 |
| 模式2 | `compose_permutations` | ABC, ACB, BAC, BCA, CAB, CBA | 6 |
| 模式3 | `compose_combinations` | AAA, AAB, AAC... CCC (27个) | 27 |
| 模式4 | `compose_limited` | A, B, C, AB, AC, BA, BC, CA, CB | 9 |

---

## 字符集对比

| 字符集 | 0-9 | A-Z | a-z | 来源 |
|--------|-----|-----|-----|------|
| **FA Free（默认）** | ✅ | ✅ | ✅（自动转大写） | @fortawesome/fontawesome-free |

---

## 注意事项

1. **字符集**：使用 Font Awesome Free（`'fa'`），支持 `0-9`、`A-Z`
2. **颜色**：仅支持 `black`（#000000）和 `white`（#FFFFFF）
3. **小写处理**：小写字母自动转为大写
4. **尺寸溢出**：当总拼接长度超过画布时，自动整体等比缩放
5. **组合数量**：模式3（笛卡尔积）可能产生大量组合，注意性能

---

## 依赖

- Python 3.7+
- svgpathtools (`pip install svgpathtools`)

---

## 更新日志

- **v3.2**：
  - 新增 `generate_preview_html()` 函数：生成带超链接的预览 HTML
  - 新增 `batch_mode_compose_with_preview()` 函数：批量生成 + 自动生成预览
  - 预览页面包含：下载链接、文件夹路径链接（file:///）、SVG 预览图
- **v3.1**：
  - SVG 输出添加 Font Awesome 许可证注释（CC BY 4.0）
- **v3.0**：
  - 明确仅支持 `0-9`、`A-Z` 字符集
  - 添加黑白双色支持（仅 `black` / `white`）
  - 添加四种拼接模式：`compose_sequence`、`compose_permutations`、`compose_combinations`、`compose_limited`
  - 自动小写转大写处理
  - 移除 `currentColor` 支持
- **v2.0**：默认字符集从 @tscircuit/alphabet 改为 @fortawesome/fontawesome-free
- **v1.0**：初始版本，支持横向/纵向拼接
