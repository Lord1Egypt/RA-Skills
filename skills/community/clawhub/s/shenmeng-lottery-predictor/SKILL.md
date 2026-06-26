---
name: lottery-predictor
description: 中国体育彩票/福利彩票预测分析工具 - 支持排列三、排列五、大乐透、双色球、七星彩、足彩14场的历史数据分析、号码统计、遗漏值分析及智能推荐
---

# 彩票预测分析工具 Lottery Predictor

> ⚠️ **免责声明**
> 
> 本工具仅供娱乐和学习数据分析使用，**不构成任何投注建议**。
> 
> 彩票开奖是独立随机事件，历史数据不具备预测未来开奖结果的能力。
> 请理性购彩，量力而行，切勿沉迷。

---

## 功能概述

本 Skill 提供中国主流彩票玩法的数据分析和号码推荐功能：

| 彩票类型 | 玩法说明 | 预测方法 |
|---------|---------|----------|
| 排列三 | 3位数字(0-9) | 冷热号分析、遗漏值、和值分析 |
| 排列五 | 5位数字(0-9) | 冷热号分析、位置统计、跨度分析 |
| 大乐透 | 5+2 (前区1-35, 后区1-12) | 区间分析、奇偶比、连号分析 |
| 双色球 | 6+1 (红球1-33, 蓝球1-16) | 热号追踪、AC值、三区比 |
| 七星彩 | 7位数字(0-9) | 定位分析、重号统计、和值走势 |
| 足彩14场 | 14场比赛胜平负 | 赔率分析、历史战绩、盘口数据 |

---

## 核心分析方法

### 1. 冷热号分析
统计历史开奖号码的出现频率，识别热号(近期频繁出现)和冷号(长期未出现)。

```
热号：近30期出现次数 > 理论平均值 × 1.5
冷号：近30期出现次数 < 理论平均值 × 0.5
温号：介于两者之间
```

### 2. 遗漏值分析
统计每个号码自上次开出以来的遗漏期数，识别即将开出的冷号回补。

```
理论遗漏 = 总期数 / 该号码出现次数
当前遗漏 / 理论遗漏 > 2.0 为超冷号
```

### 3. 走势分析
- **和值走势**：号码之和的近期趋势
- **奇偶比**：奇数与偶数的比例
- **大小比**：大号(≥5)与小号(<5)的比例
- **连号分析**：连续号码出现的概率

### 4. 足彩14场专项分析
- **赔率分析**：胜平负赔率与概率转换
- **历史战绩**：近期交锋记录
- **盘口分析**：让球盘、大小球趋势
- **冷门识别**：赔率异常、热门过度集中

---

## 自动进化系统 (v1.1.0+)

本工具内置**自动进化系统**，能够根据实际开奖结果持续优化预测模型参数。

### 进化原理

系统记录每次预测和实际开奖结果，自动计算：
1. **命中情况** - 直选命中、组选命中、位数命中
2. **策略效果** - 热号策略vs冷号策略的表现
3. **参数调整** - 动态调整各项权重

### 进化策略

```python
# 如果热号策略效果好 → 增加热号权重
if 近期命中率 > 整体命中率 + 阈值:
    hot_weight += 0.05
    cold_weight -= 0.025

# 如果热号策略效果差 → 增加冷号权重（博冷）
elif 近期命中率 < 整体命中率 - 阈值:
    cold_weight += 0.05
    hot_weight -= 0.025
```

### 使用方法

```bash
# 生成进化报告
python3 lottery_evolution.py --report

# 指定彩票类型的报告
python3 lottery_evolution.py --report --type pl3

# 记录预测和实际开奖（自动触发进化）
python3 lottery_evolution.py --record --type pl3 \
    --prediction '[4,5,6]' --actual '[4,5,9]'
```

### 查看进化效果

```bash
$ python3 lottery_evolution.py --report --type pl3

============================================================
🧬 彩票预测模型自动进化报告
============================================================
📊 排列三
----------------------------------------
🎚️  当前优化权重:
   热号权重: 0.65
   冷号权重: 0.08
   温号权重: 0.27

📈 性能统计:
   总预测次数: 50
   直选命中: 1 次 (2.00%)
   组选命中: 3 次 (6.00%)
   平均位数命中: 0.85

⚠️  注意: 以上数据仅反映历史表现，不能预测未来结果
```

### 进化配置存储

- 配置文件: `data/evolution_config.json`
- 历史记录: `data/prediction_history.json`
- 保留最近200条预测记录

---

## 使用方式

### 命令行工具

```bash
# 排列三分析和推荐
python3 lottery_cli.py pl3 --analyze --recommend

# 排列五分析
python3 lottery_cli.py pl5 --analyze --recommend

# 大乐透分析
python3 lottery_cli.py dlt --analyze --recommend

# 双色球分析
python3 lottery_cli.py ssq --analyze --recommend

# 七星彩分析
python3 lottery_cli.py qxc --analyze --recommend

# 足彩14场分析
python3 lottery_cli.py zc14 --matches "英超,西甲,意甲,德甲..." --recommend
```

### Python API

```python
from lottery_predictor import LotteryPredictor

# 创建预测器
predictor = LotteryPredictor()

# 排列三分析
pl3_result = predictor.analyze_pl3()
print(f"热号: {pl3_result['hot_numbers']}")
print(f"冷号: {pl3_result['cold_numbers']}")
print(f"推荐: {pl3_result['recommendation']}")

# 双色球分析
ssq_result = predictor.analyze_ssq()
print(f"红球热号: {ssq_result['red_hot']}")
print(f"蓝球热号: {ssq_result['blue_hot']}")
print(f"推荐号码: {ssq_result['recommendation']}")
```

---

## 数据源

本工具依赖以下公开数据源：

1. **中国体彩网** - 排列三、排列五、大乐透、七星彩
2. **中彩网** - 双色球历史数据
3. **500彩票网/澳客网** - 足彩14场对阵和赔率
4. **Football-Data.co.uk** - 国际足球比赛数据

⚠️ 数据仅供参考，请以官方开奖结果为准。

---

## 免责声明（重要）

**再次强调：**

1. 彩票开奖是完全独立的随机事件
2. 历史数据分析不能预测未来结果
3. 本工具的推荐号码仅为基于统计的随机选择
4. 购彩有风险，投注需谨慎
5. 未成年人禁止购彩

**使用本工具即表示您理解并接受以上声明。**

---

## 技术实现

### 核心算法

```python
# 1. 冷热号统计
def calc_hot_cold(numbers_history, window=30):
    """计算冷热号"""
    frequency = Counter(flatten(numbers_history[-window:]))
    avg_freq = sum(frequency.values()) / len(frequency)
    
    hot = [n for n, f in frequency.items() if f > avg_freq * 1.5]
    cold = [n for n, f in frequency.items() if f < avg_freq * 0.5]
    
    return {'hot': hot, 'cold': cold, 'warm': others}

# 2. 遗漏值计算
def calc_missing(numbers_history, max_num=9):
    """计算各号码遗漏值"""
    missing = {}
    for num in range(max_num + 1):
        # 从最近一期往前找
        for i, draw in enumerate(reversed(numbers_history)):
            if num in draw:
                missing[num] = i
                break
        else:
            missing[num] = len(numbers_history)
    
    return missing

# 3. 智能推荐算法
def generate_recommendation(analysis, count=5):
    """基于分析生成推荐号码"""
    candidates = []
    
    # 70%概率从热号中选
    if random.random() < 0.7:
        candidates.extend(analysis['hot'])
    
    # 20%概率从温号中选
    if random.random() < 0.2:
        candidates.extend(analysis['warm'])
    
    # 10%概率从冷号中选(博冷)
    if random.random() < 0.1:
        candidates.extend(analysis['cold'])
    
    # 遗漏值权重调整
    for num, miss in analysis['missing'].items():
        if miss > analysis['avg_missing'] * 2:
            candidates.append(num)  # 超冷号增加权重
    
    return random.sample(candidates, min(count, len(candidates)))
```

---

## 文件结构

```
lottery-predictor/
├── SKILL.md                 # 本文件
├── _meta.json              # Skill元数据
├── payment.py              # SkillPay支付模块
├── lottery_predictor.py    # 核心预测模块
├── lottery_cli.py          # 命令行工具
├── data/                   # 数据缓存目录
│   ├── pl3_history.json
│   ├── pl5_history.json
│   ├── dlt_history.json
│   ├── ssq_history.json
│   ├── qxc_history.json
│   └── zc14_fixtures.json
└── README.md
```

---

## 更新日志

### v1.1.0 (2026-04-02)
- 新增自动进化系统 `lottery_evolution.py`
- 支持根据实际开奖结果自动调整模型权重
- 生成进化报告查看优化效果

### v1.0.0 (2026-04-02)
- 初始版本发布
- 支持排列三、排列五、大乐透、双色球、七星彩
- 支持足彩14场赔率分析
- 集成冷热号、遗漏值、走势分析
