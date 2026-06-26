# r-ggplot-quickplot Skill (ClawPro 版本)

快速创建常见 ggplot2 图表（散点图、柱状图、箱线图、折线图、直方图、分面图）的 ClawPro Skill。

**主要特性**:
- 上传 CSV 数据文件，自动分析数据列
- 零代码可视化，一键生成 9 种专业图表
- 支持命令行参数自定义输出
- 自动检测数据列类型，生成最适合的图表

## 目录结构

```
r-ggplot-quickplot/
├── SKILL.md              # Skill 定义 (ClawPro 格式)
├── run_plot.R            # 主执行脚本
├── config.yaml           # 配置文件
├── README.md             # 本文件
├── input/                # 示例输入数据
│   └── sample_data.csv   # 模拟数据
├── examples/             # 示例代码
│   ├── scatter_example.R
│   ├── barplot_example.R
│   └── complete_demo.R
└── output/               # 输出目录 (运行后生成)
```

## 快速开始

### 1. 上传数据

将您的 CSV 文件放入 `input/` 目录。

### 2. 运行绘图

```bash
Rscript run_plot.R input/sample_data.csv
```

### 3. 查看结果

图表自动保存到 `output/` 目录。

## 输入数据格式

### 最小数据要求

只需 `x` 和 `y` 两列即可生成散点图：

```csv
x,y
2.3,5.1
3.1,4.8
1.8,6.2
```

### 完整数据格式

```csv
x,y,category,value,group,time
2.3,5.1,A,23,Control,1
3.1,4.8,A,45,Treatment,1
1.8,6.2,B,12,Control,2
4.2,3.9,B,67,Treatment,2
```

### 列说明

| 列名 | 类型 | 说明 | 用途 |
|------|------|------|------|
| `x` | 数值 | X轴变量 | 散点图、折线图 |
| `y` | 数值 | Y轴变量 | 散点图、折线图 |
| `category` | 文本 | 分类变量 (A-E) | 柱状图、箱线图、分面图 |
| `value` | 数值 | 数值指标 | 柱状图、箱线图、直方图 |
| `group` | 文本 | 分组 (Control/Treatment) | 散点图、分组折线图 |
| `time` | 数值 | 时间点 | 折线图 |

## 命令行参数

```bash
Rscript run_plot.R <input_file> [options]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--output-dir` | 输出目录 | `output` |
| `--dpi` | 图片分辨率 | `150` |
| `--width` | 图片宽度 (英寸) | `8` |
| `--height` | 图片高度 (英寸) | `6` |
| `--theme` | 图表主题 | `minimal` |

### 示例

```bash
# 使用默认设置
Rscript run_plot.R input/sample_data.csv

# 自定义设置
Rscript run_plot.R input/my_data.csv --output-dir results --dpi 300
```

## 输出文件

| 文件 | 描述 |
|------|------|
| `01_scatter_basic.png` | 基础散点图 |
| `02_scatter_advanced.png` | 带颜色和大小的散点图 |
| `03_barplot_vertical.png` | 垂直柱状图 |
| `04_barplot_horizontal.png` | 水平排序柱状图 |
| `05_boxplot.png` | 带数据点的箱线图 |
| `06_lineplot.png` | 分组折线图 |
| `07_histogram.png` | 直方图 |
| `08_facet.png` | 分面散点图 |
| `09_publication_style.png` | 出版风格图表 (300 DPI) |

## 依赖

```r
install.packages('ggplot2')
```

## 故障排除

### 错误: 找不到 ggplot2

```r
Rscript -e "install.packages('ggplot2')"
```

### 错误: 文件不存在

检查文件路径是否正确：
```bash
ls -la input/sample_data.csv
```

## 技能元数据

- **名称**: r-ggplot-quickplot
- **类型**: R
- **主要工具**: ggplot2
- **版本**: 2.0.0 (ClawPro)
- **兼容性**: OpenClaw / ClawPro
