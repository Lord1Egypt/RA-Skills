---
name: 实验设计技能
slug: doe-experiment-design
displayName: 实验设计技能
description: 生成全因子与部分因子实验方案；支持自定义因子/水平数、分辨率设置及CSV导出，用于实验设计与数据分析；覆盖DOE、正交实验、田口方法等常见设计
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# DOE实验设计工具

## 任务目标
- 本Skill用于:根据因子和水平配置生成标准DOE实验方案
- 能力包含:全因子设计(完整组合)、部分因子设计(2^(k-p)分辨率)、CSV导出
- 触发条件:用户需要"设计实验方案"、"DOE"、"正交实验"、"因子实验"

## 前置准备
- 依赖:pandas>=1.5.0
- 无需准备额外文件

## 操作步骤

### 1. 全因子实验设计
当用户需要生成所有因子所有水平的完整组合时：

```bash
python scripts/doe_generator.py full --factors 3 --levels 2 --output full_factorial.csv
```

参数说明:
- `--factors`: 因子数量(正整数)
- `--levels`: 每个因子的水平数(正整数)
- `--output`: 输出CSV文件路径

### 2. 部分因子实验设计(2^(k-p))
当实验次数受限，需要使用分辨率更高的部分因子设计：

```bash
python scripts/doe_generator.py fractional --base-levels 2 --num-factors 4 --resolution 3 --output fractional_4f8run.csv
```

参数说明:
- `--base-levels`: 基础水平数(默认2，适用于2水平设计)
- `--num-factors`: 因子总数(正整数)
- `--resolution`: 设计分辨率(3=分辨率III, 4=分辨率IV, 5=分辨率V)
- `--output`: 输出CSV文件路径

### 3. 查看生成的方案
脚本输出JSON格式的摘要:
```json
{
  "design_type": "full_factorial",
  "num_factors": 3,
  "num_levels": 2,
  "num_runs": 8,
  "output_file": "full_factorial.csv",
  "factors": ["Factor_A", "Factor_B", "Factor_C"]
}
```

### 4. 导出与使用
- CSV文件包含列:Run, Factor_A, Factor_B, ... (各水平用数值编码:0,1,2...)
- 可直接用于实验执行或导入分析软件

## 使用示例

### 示例1: 3因子2水平全因子设计
- 场景: 温度、压力、浓度3个因子，各2水平
- 输入: `python scripts/doe_generator.py full --factors 3 --levels 2 --output doe_3f2l.csv`
- 产出: 8次实验的完整方案
- 要点: 全因子=因子数^水平数，3因子2水平=8次实验

### 示例2: 6因子2水平部分因子设计(分辨率IV)
- 场景: 因子较多，全因子32次太多，需要减少实验
- 输入: `python scripts/doe_generator.py fractional --base-levels 2 --num-factors 6 --resolution 4 --output doe_6f16run.csv`
- 产出: 16次实验的部分因子方案
- 要点: 2^(6-1)=32→16次，分辨率IV可估计主效应

### 示例3: 自定义因子名称
- 场景: 需要明确标识每个因子的含义
- 输入: 编辑CSV文件或在后续分析中指定因子名
- 要点: 因子默认命名为Factor_A, Factor_B...，可在导出的CSV中修改

## 资源索引
- 脚本:见 [scripts/doe_generator.py](scripts/doe_generator.py)(用途:生成DOE方案并导出CSV)
- 参考:见 [references/doe_guide.md](references/doe_guide.md)(何时读取:需要了解设计原理或选择合适分辨率)

## 注意事项
- 部分因子设计目前仅支持2水平(2^(k-p)设计)
- 导出路径为相对路径，保存于当前工作目录
- 分辨率III设计仅能估计部分主效应，选择时需谨慎

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
