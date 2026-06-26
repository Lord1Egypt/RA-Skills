---
name: r-ggplot-quickplot
description: 上传 CSV 数据文件，自动生成 9 种常用 ggplot2 图表（散点图、柱状图、箱线图、折线图、直方图、分面图等）。零代码可视化，一键导出高质量图表。
version: 2.0.0
homepage: https://github.com/workbuddy/skills
emoji: 📊
tags:
  - visualization
  - ggplot2
  - R
  - data-science
  - charts
user-invocable: true
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["Rscript"]
      },
      "os": ["linux", "darwin", "win32"]
    }
  }
---

# r-ggplot-quickplot

**零代码 ggplot2 可视化工具** - 上传 CSV 数据，自动生成专业图表。

## 快速开始

### 1. 准备数据

上传 CSV 文件到 input 目录。支持的列：

| 列名 | 类型 | 说明 | 用途 |
|------|------|------|------|
| `x` | 数值 | X轴变量 | 散点图、折线图 |
| `y` | 数值 | Y轴变量 | 散点图、折线图 |
| `category` | 文本 | 分类变量 (A-E) | 柱状图、箱线图、分面图 |
| `value` | 数值 | 数值指标 | 柱状图、箱线图、直方图 |
| `group` | 文本 | 分组 (Control/Treatment) | 散点图、分组折线图 |
| `time` | 数值 | 时间点 | 折线图 |

### 2. 运行绘图

执行以下命令：
```bash
cd <skill-directory>
Rscript run_plot.R input/your_data.csv
```

### 3. 获取结果

图表自动保存到 `output/` 目录：

| 文件 | 图表类型 | 说明 |
|------|----------|------|
| `01_scatter_basic.png` | 散点图 | 基础散点图 |
| `02_scatter_advanced.png` | 高级散点图 | 带颜色、大小、分组 |
| `03_barplot_vertical.png` | 柱状图 | 按分类汇总的垂直柱状图 |
| `04_barplot_horizontal.png` | 水平柱状图 | 按值排序的水平柱状图 |
| `05_boxplot.png` | 箱线图 | 带数据点的箱线图 |
| `06_lineplot.png` | 折线图 | 分组时间序列折线图 |
| `07_histogram.png` | 直方图 | 数值分布直方图 |
| `08_facet.png` | 分面图 | 按分类分面的散点图 |
| `09_publication_style.png` | 出版级图表 | 300 DPI 出版风格 |

## 命令行参数

```bash
Rscript run_plot.R <input_file> [options]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<input_file>` | 输入 CSV 文件路径 | 必填 |
| `--output-dir` | 输出目录 | `output` |
| `--dpi` | 图片分辨率 | `150` |
| `--width` | 图片宽度 (英寸) | `8` |
| `--height` | 图片高度 (英寸) | `6` |

### 使用示例

```bash
# 使用默认设置
Rscript run_plot.R input/sample_data.csv

# 自定义输出设置
Rscript run_plot.R input/my_data.csv --output-dir results --dpi 300 --width 10 --height 8
```

## 输入数据格式

### 最小数据要求

只需要 `x` 和 `y` 两列即可生成散点图：

```csv
x,y
2.3,5.1
3.1,4.8
1.8,6.2
```

### 完整数据示例

```csv
x,y,category,value,group,time
2.3,5.1,A,23,Control,1
3.1,4.8,A,45,Treatment,1
1.8,6.2,B,12,Control,2
4.2,3.9,B,67,Treatment,2
```

### 注意事项

- CSV 文件必须包含表头行
- 支持中文字段名
- 缺失值用 `NA` 表示
- 日期格式建议使用 `YYYY-MM-DD`

## 图表配置 (config.yaml)

可以通过配置文件自定义图表样式：

```yaml
# 图表类型设置
charts:
  scatter: true
  barplot: true
  boxplot: true
  lineplot: true
  histogram: true
  facet: true

# 样式设置
style:
  theme: minimal    # minimal, classic, bw, light
  palette: steelblue
  font_size: 12

# 输出设置
output:
  format: [png, pdf]  # 支持 png, pdf, svg
  dpi: 150
  width: 8
  height: 6
```

## 自动检测逻辑

脚本会自动检测输入数据的列，并生成适合的图表：

| 检测到的列 | 自动生成的图表 |
|-----------|---------------|
| `x`, `y` | 散点图 |
| `category`, `value` | 柱状图、箱线图 |
| `time`, `value` | 折线图 |
| `value` (单列) | 直方图 |
| 多分类列 | 分面图 |
| `group` | 分组着色 |

## 输出示例

成功运行后会显示：

```
=== r-ggplot-quickplot 执行完成 ===
输入文件: input/sample_data.csv
输出目录: output/

生成的图表:
  ✓ 01_scatter_basic.png
  ✓ 02_scatter_advanced.png
  ✓ 03_barplot_vertical.png
  ✓ 04_barplot_horizontal.png
  ✓ 05_boxplot.png
  ✓ 06_lineplot.png
  ✓ 07_histogram.png
  ✓ 08_facet.png
  ✓ 09_publication_style.png

共生成 9 个图表文件
===============================
```

## 依赖安装

首次使用时，如缺少 R 包会自动安装：

```r
install.packages('ggplot2')
```

如需额外功能，可手动安装：

```r
install.packages('ggpubr')      # 出版级图表
install.packages('patchwork')   # 多图组合
install.packages('ggthemes')    # 主题风格
```

## 故障排除

### 错误：缺少 ggplot2

```bash
Rscript -e "install.packages('ggplot2')"
```

### 错误：输入文件不存在

```bash
# 检查文件路径
ls -la input/sample_data.csv
```

### 错误：列名不匹配

确保 CSV 文件包含所需列，或检查列名是否拼写正确。

## 技术细节

- **R 版本**: >= 4.0.0
- **ggplot2 版本**: >= 3.5.0
- **输出格式**: PNG (默认), PDF, SVG
- **编码**: UTF-8
