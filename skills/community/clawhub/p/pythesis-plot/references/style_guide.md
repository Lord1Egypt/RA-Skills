# 样式规范

本规范定义 PyThesisPlot 的科研图表样式标准，确保图表的专业性和一致性。

## 目录

- [配色方案](#配色方案)
- [字体规范](#字体规范)
- [图表尺寸](#图表尺寸)
- [线条与标记](#线条与标记)
- [导出设置](#导出设置)

---

## 配色方案

### 学术蓝 (Academic)

经典学术风格，适合正式论文。

```python
colors = ['#2E5AAC', '#5B9BD5', '#A5D6F3', '#1F4E79', '#8FB8E6']
```

### 鲜艳色 (Vibrant)

高对比度，适合数据对比和演示。

```python
colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00']
```

### 柔和色 (Pastel)

低饱和度，适合多组数据展示。

```python
colors = ['#FBB4AE', '#B3CDE3', '#CCEBC5', '#DECBE4', '#FED9A6']
```

### 期刊配色

#### Nature 风格

```python
colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F']
```

#### Science 风格

```python
colors = ['#003399', '#CC0000', '#009900', '#FFCC00', '#9900CC']
```

#### IEEE 风格

```python
colors = ['#0066CC', '#CC0000', '#009900', '#FF9900', '#9900CC']
```

### 功能配色

#### 灰度色 (Grayscale)

黑白打印友好。

```python
colors = ['#000000', '#404040', '#707070', '#A0A0A0', '#D0D0D0']
```

#### 暖色调 (Warm)

```python
colors = ['#D73027', '#F46D43', '#FDAE61', '#FEE090', '#FFFFBF']
```

#### 冷色调 (Cool)

```python
colors = ['#4575B4', '#74ADD1', '#ABD9E9', '#E0F3F8', '#FFFFBF']
```

#### 发散色 (Diverging)

适用于正负值对比。

```python
colors = ['#D73027', '#FC8D59', '#FEE090', '#91BFDB', '#4575B4']
```

### 色盲友好配色

使用 ColorBrewer 推荐的色盲友好配色：

```python
# 3 色
['#1f77b4', '#ff7f0e', '#2ca02c']

# 4 色
['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# 5 色
['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
```

### 配色使用建议

| 场景 | 推荐配色 |
|-----|---------|
| 正式论文 | academic, grayscale |
| 演示汇报 | vibrant, nature |
| 黑白打印 | grayscale |
| 多组数据 (>5) | pastel, cool |
| 对比强调 | vibrant, warm |
| 相关性热力图 | diverging |

---

## 字体规范

### 中文字体推荐

| 操作系统 | 首选字体 | 备选字体 |
|---------|---------|---------|
| Windows | SimHei (黑体) | Microsoft YaHei |
| macOS | Heiti TC (黑体-繁) | PingFang TC |
| Linux | WenQuanYi Micro Hei | Noto Sans CJK SC |

### 字体大小规范

| 元素 | 建议字号 | 说明 |
|-----|---------|-----|
| 图表标题 | 12-14 pt | 加粗 |
| 坐标轴标签 | 10-12 pt | |
| 刻度标签 | 9-10 pt | |
| 图例 | 9-10 pt | |
| 注释文字 | 8-9 pt | |

### 字体设置代码

```python
import matplotlib.pyplot as plt

# 中文字体配置
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 字体大小配置
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
```

---

## 图表尺寸

### 标准尺寸

| 使用场景 | 宽度 (英寸) | 高度 (英寸) | 对应像素 (300dpi) |
|---------|------------|------------|------------------|
| 单栏图 | 3.5 | 2.5-3.0 | 1050×750 |
| 1.5栏图 | 5.0 | 3.5-4.0 | 1500×1050 |
| 双栏图 | 7.0 | 4.5-5.5 | 2100×1350 |
| 全页图 | 7.0 | 9.0 | 2100×2700 |

### 尺寸代码

```python
# 单栏图
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# 双栏图
fig, ax = plt.subplots(figsize=(7.0, 5.0))

# 自定义尺寸
fig, ax = plt.subplots(figsize=(width_inches, height_inches))
```

### 黄金比例

推荐宽高比 1.618:1（黄金比例）或 4:3、16:9。

```python
# 黄金比例
width = 7.0
height = width / 1.618
fig, ax = plt.subplots(figsize=(width, height))
```

---

## 线条与标记

### 线条样式

```python
# 线宽
linewidth = 1.5  # 标准
linewidth = 2.0  # 强调
linewidth = 1.0  # 辅助线

# 线型
linestyle = '-'   # 实线
linestyle = '--'  # 虚线
linestyle = '-.'  # 点划线
linestyle = ':'   # 点线
```

### 标记样式

| 标记 | 代码 | 适用场景 |
|-----|-----|---------|
| 圆点 | 'o' | 一般数据点 |
| 方块 | 's' | 分类数据 |
| 三角形 | '^' | 峰值数据 |
| 菱形 | 'D' | 关键数据 |
| 星号 | '*' | 特殊标记 |
| 十字 | '+' | 误差数据 |

```python
# 标记大小
markersize = 6  # 标准
markersize = 8  # 强调

# 标记样式
ax.plot(x, y, marker='o', markersize=6, markerfacecolor='white',
        markeredgecolor='#2E5AAC', markeredgewidth=1.5)
```

### 标记间隔

避免标记过于密集：

```python
# 每 n 个点显示一个标记
markevery = 10  # 每 10 个点显示一个
ax.plot(x, y, marker='o', markevery=markevery)
```

---

## 导出设置

### 文件格式

| 格式 | 适用场景 | 优点 |
|-----|---------|-----|
| PDF | LaTeX 论文 | 矢量图，无限缩放 |
| EPS | LaTeX 论文 | 矢量图，兼容性好 |
| PNG | Word/PPT | 位图，透明背景 |
| SVG | 网页编辑 | 矢量图，可编辑 |
| TIFF | 期刊投稿 | 高质量位图 |

### 导出代码

```python
# PDF 导出（推荐用于 LaTeX）
plt.savefig('figure.pdf', bbox_inches='tight', dpi=300)

# PNG 导出（推荐用于 Word）
plt.savefig('figure.png', bbox_inches='tight', dpi=300, 
            facecolor='white', edgecolor='none')

# SVG 导出（可编辑）
plt.savefig('figure.svg', bbox_inches='tight')

# TIFF 导出（期刊投稿）
plt.savefig('figure.tiff', bbox_inches='tight', dpi=600)
```

### 导出参数

| 参数 | 说明 | 建议值 |
|-----|-----|-------|
| `bbox_inches` | 去除多余白边 | `'tight'` |
| `dpi` | 分辨率 | 300（标准）、600（高质量） |
| `pad_inches` | 边距 | 0.02 |
| `facecolor` | 背景色 | `'white'` |
| `transparent` | 透明背景 | `False` |

### 批量导出

```python
# 导出多种格式
formats = ['pdf', 'png', 'svg']
for fmt in formats:
    plt.savefig(f'figure.{fmt}', bbox_inches='tight', dpi=300)
```

---

## 样式检查清单

提交图表前检查：

- [ ] 字体清晰可读，中文正常显示
- [ ] 坐标轴标签完整（含单位）
- [ ] 图例位置合理，不遮挡数据
- [ ] 配色协调，符合论文风格
- [ ] 分辨率足够（≥300dpi）
- [ ] 无多余白边
- [ ] 线条粗细适中
- [ ] 标记清晰可辨
- [ ] 标题简洁明了
- [ ] 网格线不干扰数据阅读
