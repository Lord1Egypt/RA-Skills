# QC手法操作指南

## 目录
1. [柏拉图(Pareto Chart)](#1-柏拉图pareto-chart)
2. [鱼骨图(Ishikawa Diagram)](#2-鱼骨图ishikawa-diagram)
3. [直方图(Histogram)](#3-直方图histogram)
4. [控制图(Control Chart)](#4-控制图control-chart)
5. [散布图(Scatter Diagram)](#5-散布图scatter-diagram)

---

## 1. 柏拉图(Pareto Chart)

### 1.1 概述
柏拉图基于"80/20法则"，即80%的问题往往由20%的原因造成。通过柏拉图可以识别关键少数，将改善资源集中在最重要的问题上。

### 1.2 适用场景
- 质量问题排序与优先级确定
- 识别需要优先解决的关键问题
- 改善效果验证（改善前后对比）
- 客户投诉分析

### 1.3 数据格式
```json
[
  {"category": "缺陷类型1", "value": 数量1},
  {"category": "缺陷类型2", "value": 数量2}
]
```

### 1.4 操作步骤
1. **收集数据**:统计各类问题或缺陷的数量
2. **排序**:按数量降序排列
3. **计算累计占比**:逐一计算累计百分比
4. **绘制图表**:柱状图表示数量，折线图表示累计占比
5. **识别关键区域**:累计占比80%以内的项目为关键少数

### 1.5 结果解读
| 关键发现 | 含义 |
|---------|------|
| 前1-2项占比>60% | 单一问题主导，应优先解决 |
| 前3-5项累计>80% | 存在明显关键少数 |
| 各项目分布均匀 | 无突出重点，需多角度分析 |

### 1.6 使用示例
```bash
python scripts/qc_chart_generator.py -t pareto \
  -d '[{"category":"外观缺陷","value":45},{"category":"尺寸偏差","value":32},{"category":"装配不良","value":28}]' \
  -o output/pareto.png --title "产品缺陷柏拉图"
```

---

## 2. 鱼骨图(Ishikawa Diagram)

### 2.1 概述
鱼骨图，又称因果图或石川图，将问题与可能原因以鱼骨状结构组织，帮助系统性思考问题根因。

### 2.2 适用场景
- 问题根因分析
- 新员工培训和问题讲解
- 团队头脑风暴
- 制定改善对策

### 2.3 常用分类维度
| 维度 | 说明 | 典型原因示例 |
|------|------|-------------|
| 人(Man) | 作业人员相关 | 技能不足、粗心大意、培训不够 |
| 机(Machine) | 设备工装相关 | 设备老化、模具磨损、维护不当 |
| 料(Material) | 原材料相关 | 批次差异、来料不良、存储问题 |
| 方法(Method) | 工艺作业方法 | 参数不当、方法复杂、标准不清 |
| 环境(Environment) | 作业环境相关 | 温湿度、噪音、光照、5S |
| 测量(Measurement) | 测量系统相关 | 量具精度、测量方法、人员差异 |

### 2.4 数据格式
```json
{
  "problem": "质量问题描述",
  "causes": {
    "人": ["原因1", "原因2"],
    "机": ["原因1", "原因2"],
    "料": [],
    "法": [],
    "环": [],
    "测": []
  }
}
```

### 2.5 操作步骤
1. **明确问题**:在鱼头位置填写要分析的问题
2. **确定主骨**:识别主要分类维度（人机料法环测）
3. **头脑风暴**:针对每个维度列举可能原因
4. **层层展开**:对主要原因进一步细分
5. **识别关键**:通过数据验证确定真正根因（可结合其他QC手法）

### 2.6 使用示例
```bash
python scripts/qc_chart_generator.py -t fishbone \
  -d '{"problem":"产品不良率高","causes":{"人":["操作失误"],"机":["模具磨损"],"料":["来料不良"]}}' \
  -o output/fishbone.png --title "不良率分析鱼骨图"
```

---

## 3. 直方图(Histogram)

### 3.1 概述
直方图用于展示数据分布形态，通过观察分布是否正态、是否在规格限内，判断过程能力和稳定性。

### 3.2 适用场景
- 过程能力分析
- 数据分布查看
- 规格界限对比
- 改善前后对比

### 3.3 数据格式
```json
{
  "values": [数据点列表],
  "spec_limits": {
    "USL": 上规格限,
    "LSL": 下规格限
  }
}
```

### 3.4 分布形态判断
| 形态 | 特征 | 可能原因 |
|------|------|---------|
| 标准型 | 中间高、两边低、近似对称 | 正常分布 |
| 孤岛型 | 远离主体有孤立峰 | 测量错误/异常工序 |
| 偏心型 | 峰值偏向一侧 | 设备调整不当/刀具磨损 |
| 双峰型 | 两个峰值 | 两台设备/两类产品混合 |
| 陡壁型 | 一侧陡峭下降 | 过程已截断/全数检验 |
| 平顶型 | 顶部平缓 | 多种分布混合 |

### 3.5 过程能力指数
- **Cp(过程能力指数)**:(USL-LSL)/(6σ)，衡量过程满足规格的能力
- **Cpk(过程能力指数修正值)**:考虑分布中心偏移
- **评价标准**:
  - Cpk < 1.0: 能力不足
  - 1.0 ≤ Cpk < 1.33: 勉强合格
  - 1.33 ≤ Cpk < 1.67: 能力充足
  - Cpk ≥ 1.67: 能力充裕

### 3.6 使用示例
```bash
python scripts/qc_chart_generator.py -t histogram \
  -d '{"values":[50.2,50.5,49.8,50.3,50.1,50.6,49.9,50.4],"spec_limits":{"USL":51,"LSL":49}}' \
  -o output/histogram.png --title "产品重量分布"
```

---

## 4. 控制图(Control Chart)

### 4.1 概述
控制图用于监控过程稳定性，区分普通原因变异和特殊原因变异，是统计过程控制(SPC)的核心工具。

### 4.2 适用场景
- 过程监控与预警
- 异常原因查找
- 改善效果验证
- 供应商评估

### 4.3 常用控制图类型
| 类型 | 适用场景 | 子组大小 |
|------|---------|---------|
| X̄-R图 | 计量型数据，样本量2-10 | n ≤ 10 |
| X̄-S图 | 计量型数据，样本量>10 | n > 10 |
| I-MR图 | 单个测量值，无法分组 | n = 1 |
| p图 | 不良率/不合格率 | 变长 |
| np图 | 不良数（子组大小固定） | 固定 |
| c图 | 缺陷数 | 固定单位 |
| u图 | 单位缺陷数 | 变长 |

### 4.4 数据格式
```json
{
  "subgroups": [[子组1数据], [子组2数据], ...],
  "subgroup_size": 子组大小,
  "chart_type": "xbar_r" 或 "xbar_s" 或 "imr"
}
```

### 4.5 判异规则
满足以下任一条件，判断过程异常：
1. **规则1**:1个点超出UCL或LCL
2. **规则2**:连续9点落在中心线同一侧
3. **规则3**:连续6点递增或递减
4. **规则4**:连续14点交替上下
5. **规则5**:连续3点中有2点落在2σ区域外
6. **规则6**:连续5点中有4点落在1σ区域外
7. **规则7**:连续15点落在1σ区域内
8. **规则8**:连续8点落在1σ区域外

### 4.6 使用示例
```bash
python scripts/qc_chart_generator.py -t control \
  -d '{"subgroups":[[10.2,10.1,9.9,10.3,10.0],[10.1,10.2,10.0,9.8,10.1]],"subgroup_size":5,"chart_type":"xbar_r"}' \
  -o output/control_chart.png --title "尺寸控制图"
```

---

## 5. 散布图(Scatter Diagram)

### 5.1 概述
散布图用于分析两个变量之间的相关关系，帮助判断是否存在相关性、相关方向和强度。

### 5.2 适用场景
- 两变量相关性分析
- 原因与结果关系验证
- 最佳参数范围确定
- 回归分析前期探索

### 5.3 数据格式
```json
{
  "x": [X轴数据列表],
  "y": [Y轴数据列表],
  "x_label": "X轴标签名",
  "y_label": "Y轴标签名"
}
```

### 5.4 相关性判断
| 相关系数范围 | 相关强度 | 判断 |
|-------------|---------|------|
| |r| < 0.2 | 几乎无相关 | 需寻找其他因素 |
| 0.2 ≤ |r| < 0.4 | 弱相关 | 可能有关系 |
| 0.4 ≤ |r| < 0.6 | 中等相关 | 确实存在关联 |
| 0.6 ≤ |r| < 0.8 | 强相关 | 高度关联 |
| |r| ≥ 0.8 | 非常强相关 | 显著关联 |

### 5.5 相关方向
| 方向 | 特征 | 说明 |
|------|------|------|
| 正相关 | x↑时y↑ | x增加会导致y增加 |
| 负相关 | x↑时y↓ | x增加会导致y减少 |
| 无相关 | 散点无规律 | 两变量相互独立 |

### 5.6 注意事项
- 相关不等于因果，需结合专业知识判断
- 关注异常点，可能是分析的关键线索
- 需确认测量系统准确性
- 非线性关系需使用其他分析方法

### 5.7 使用示例
```bash
python scripts/qc_chart_generator.py -t scatter \
  -d '{"x":[20,25,30,35,40,45,50],"y":[42,48,55,62,70,78,85],"x_label":"温度","y_label":"产量"}' \
  -o output/scatter.png --title "温度与产量关系"
```

---

## 模板索引

| 模板名称 | 路径 | 用途 |
|---------|------|------|
| pareto_defects | [assets/templates/pareto_defects.json](assets/templates/pareto_defects.json) | 产品缺陷分类统计示例 |
| histogram_weight | [assets/templates/histogram_weight.json](assets/templates/histogram_weight.json) | 产品重量分布示例 |
| control_xbar_r | [assets/templates/control_xbar_r.json](assets/templates/control_xbar_r.json) | X-bar R图数据模板 |
| scatter_temp_output | [assets/templates/scatter_temp_output.json](assets/templates/scatter_temp_output.json) | 温度产量相关性示例 |
| fishbone_defect | [assets/templates/fishbone_defect.json](assets/templates/fishbone_defect.json) | 不良率根因分析模板 |

---

## 工具调用方式

### 使用JSON数据
```bash
python scripts/qc_chart_generator.py -t <chart_type> -d '<json_data>' -o <output_path>
```

### 使用模板
```bash
python scripts/qc_chart_generator.py -t <chart_type> --template -d <template_name> -o <output_path>
```

### 导出分析结果
```bash
python scripts/qc_chart_generator.py -t <chart_type> -d '<json_data>' -o <output.png> -e
```
