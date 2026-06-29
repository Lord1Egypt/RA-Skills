---
name: simulated-peak-plot
author: wUwproject
data_dir: ../.standardization/simulated-peak-plot/data/
license: MIT
tags: ['peak', 'plot', 'simulation', 'chromatography', 'spectroscopy', 'visualization', 'csv-export']
version: 2.13.0
description: 生成模拟峰图（高斯峰），用于色谱、光谱或任何信号可视化。支持簇峰(N子峰各独立标注)/融峰(合成单标注)/单峰、负峰(倒峰)、标注控制(annotate)、扫描速率(scan_rate)、碰撞避让标注、自定义坐标轴/单位、CSV导出及CSV导入，**负峰（倒峰）**。
external_data_dir: true
sensitive_access: false
critical_write: false
permission_weight: LOW
create_permissions_md: true
trigger: ['生成峰图', '模拟信号', '创建峰谱', '可视化保留时间', '输出 Markdown 表格', '导入 CSV 数据', '生成模拟数据']
trigger_negative: true
meta_field_sync: true
faq_unparsable: reformat
faq_quality: improve_qa
---
# Simulated Peak Plot

## 触发条件

**正向触发：**
- 说出"生成峰图"、"模拟信号"、"创建峰谱"
- 说出"可视化保留时间"、"输出 Markdown 表格"
- 说出"导入 CSV 数据"、"生成模拟数据"
- 需要色谱/光谱峰模拟、信号可视化、数据导出等场景
- **Python API 调用**（直接导入函数生成信号数据）：

**否定条件：**

除非用户明确提到生成峰图或模拟数据，否则不要主动触发。

## 快速开始

**场景：混合正负峰峰谱**
> 模拟色谱中溶剂峰倒置场景，同一谱图正峰和负峰共存
```bash
生成包含正峰和负峰的峰谱
```
  - **输入**: 时间范围 5~15 min, scan_rate=100, 正峰 (RT=7.7, height=1500, HWHM=0.08), 负峰 (RT=10.3, height=-1200, HWHM=0.12), baseline=20, noise=8
  - **输出**: 生成 PNG 峰图（正峰向上、负峰向下，Y轴自动包含负区间），打印 Markdown 数据表格

**场景：单峰生成 + CSV 导出**
> 基础用法，验证单峰生成和数据导出两个核心功能
```bash
生成一个高斯峰并导出完整数据
```
  - **输入**: 时间范围 0~10 min, scan_rate=200, 单峰 (RT=5.0, height=800, HWHM=0.1), baseline=10, noise=5, export_csv=true
  - **输出**: 生成 PNG 峰图 + CSV 文件（含全部数据点，RFC 4180 格式），打印 Markdown 采样表格

**场景：簇峰 + 融峰混合谱**
> 验证簇峰独立标注和融峰合并标注两种混合使用场景
```bash
生成包含簇峰和融峰的复杂谱图
```
  - **输入**: 时间范围 4~14 min, scan_rate=120, 单峰 (RT=5.5, height=500, HWHM=0.1), 簇峰 (3子峰: RT=7.0,8.0,9.0, height=1000,800,600, HWHM=0.15), 融峰 (2子峰: RT=11.0,12.0, height=700,500, HWHM=0.12)
  - **输出**: 生成 PNG 峰图，簇峰各子峰独立标注为 {name}-1/2/3，融峰只有单一标注在最高点
## 概述

本技能用于生成模拟峰图（高斯峰），适用于教学、测试或演示场景。支持：
- 多种峰类型，包括**复合峰**（任意数量子峰组合）
- **负峰（倒峰）**：配置 height 为负数即可产生朝下的倒峰
- 可自定义时间范围、基线和噪声
- **可自定义坐标轴标题和单位**（X/Y标签，mV/V/吸光度等）
- **CSV完整数据导出**（全部数据点）
- **可点击的 file:/// 路径**，方便直接打开图片
- Markdown 表格数据输出（在控制台打印）
- 交互式配置，带点数推荐

### ⚠️ 重要限制（使用前必读）

| 参数 | 建议范围 | 说明 |
| ------ |---------| ------ |
| 峰组数量（含子峰） | ≤ 20 组 | 过多会导致生成缓慢 |
| 扫描速率 scan_rate | 50 ~ 500 pts/min | 过低锯齿，过高文件大 |
| 总点数 | ≤ 20000 | 超过时请降 scan_rate |
| HWHM | > 0 | 半高半宽必须为正数 |
| RT | 应在 [t_start, t_end] 内 | 否则峰部分在画布外 |
| 负峰 | height 为负，**HWHM 仍为正** | 不需要改 baseline |

> 更多反模式与避坑指南 → 渐进式文件索引表
> 常见问题解答 → 渐进式文件索引表

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
| -------- |------| ---------- |----------|
| `references/LICENSE.md` | 许可协议 | 开源许可证声明（MIT）。包含：MIT 许可证完整文本。 | R-26 |
| `references/antipatterns.md` | 规范指南 | skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。 | R-18 |
| `references/changelog.md` | 版本管理 | 版本更新日志。包含：版本号、更新类型、修复项、升级说明。 | R-24 |
| `references/faq.md` | 常见问题 | 常见疑问与解答。包含：问题分类、原因分析、解决方案。 | R-19, R-25 C-19 |
| `references/features.md` | 参考文档 | 将 height 设为负数即可生成倒峰。Y轴自动缩放包含负区间，标注自动反向指向下方。 | 无 |
| `references/parameters.md` | 参考文档 | 本文档提供模拟峰图生成中所有参数的详细信息。 | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。 | R-15, R-16 |
| `references/test-report.md` | 测试报告 | 技能功能测试与场景测试结论报告。包含：测试结果、修复项、测试覆盖说明。 | 无 |

### 文件目录结构

```text
├── SKILL.md
├── _meta.json
├── scripts/
│   └── generate_peak.py
└── references/
    ├── antipatterns.md
    ├── changelog.md
    ├── faq.md
    ├── features.md
    ├── LICENSE.md
    ├── parameters.md
    ├── permissions.md
    └── test-report.md
```

## 工作流程

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

### 1. 环境检查

**始终从检查环境开始：**

```bash
# 检查 Python 可用性
python --version

# 检查必需包
python -c "import numpy; import matplotlib; print('所有包可用')"
```

如果缺少包，指导用户安装：
```bash
pip install numpy matplotlib
```

### 2. 参数配置

通过对话配置。先显示点数推荐表，再询问峰参数、基线/噪声、输出选项。
默认: 起始5min/结束15min/scan_rate=100, 空白峰+3子峰复合峰, baseline=20, noise=8。

### 3. 点数推荐

总点数 = duration × scan_rate。scan_rate 默认 100 pts/min。
推荐: 短时(5-10min)用80-120 pts/min, 长时(30+)用50-70 pts/min。

### 4. 生成图表

```bash
python {SKILL_DIR}/scripts/generate_peak.py --interactive
```

### 5. 输出

PNG + Markdown 表格 + CSV(data_dir)。输出路径：`file:///...` 可直接点击。

## 新功能

支持：负峰(倒峰) / 簇峰(各子峰独立标注) / 融峰(合成信号单标注) / 扫描速率(pts/min) / 碰撞避让标注布局。

## 簇峰 / 融峰

- **簇峰 (cluster)**: 各子峰独立标注为 {name}-N，type: "cluster"（兼容旧 "composite"）
- **融峰 (merged)**: 多子峰合成信号，单一标注在真实最高点

## 文件引用

- **脚本**: 主生成脚本
- **参数参考**: 详细参数文档

```bash
{SKILL_DIR}/scripts/generate_peak.py
{SKILL_DIR}/references/parameters.md
{SKILL_DIR}/references/features.md
```

## 使用示例

**用户请求**: "生成包含5个峰（含1个3子峰簇峰）的峰谱，输出数据为表格"

**响应工作流**:
1. 检查环境
2. 显示点数推荐表
3. 询问峰参数
4. 生成带 Markdown 表格输出的光谱
5. 保存PNG文件并在控制台打印表格

## 自定义选项

用户可以更新:
- 峰数量（包括簇峰/融峰的多子峰组合）
- 峰参数（RT、高度、HWHM）— **height 设为负数即为负峰**
- 峰类型: **单峰** / **簇峰** (cluster) / **融峰** (merged)
- 扫描速率 (scan_rate, pts/min)
- 噪声和基线水平
- 坐标轴标题和单位
- CSV导出 / 网格线 / 标注控制(annotate: false)

## JSON 配置示例

> 簇峰的每个子峰会独立标注; 融峰只在最高子峰处标注为单一名称。

### CSV 输出格式（RFC 4180 标准）
```csv
Time_min,Signal_mV
2.000000,49.782199
2.020040,46.140969
...
```


## 触发场景
**正向触发（满足以下任意一条）：**
- 用户需要模拟峰图生成器 (Simulated Peak Plot Generator)
- 用户需要生成可定制的高斯峰图，支持复合峰（N个子峰组合）和 Markdown 表格输出。
- 用户需要复合峰可形成多种形状：M形、馒头形、泊松分布形等。
- 用户需要优雅处理 Ctrl+C 中断信号

**否定条件（满足以下任意一条，不触发）：**
- 简单问答、闲聊、问候（不需要本技能）
- 单步任务（不需要结构化执行）
