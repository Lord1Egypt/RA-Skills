# Sports Betting Analyzer - 开发文档

## 项目结构

```
sports-betting-analyzer/
├── SKILL.md                    # OpenClaw Skill 定义
├── README.md                   # 用户指南
├── requirements.txt            # Python 依赖
├── _meta.json                  # Skill 元数据
├── config/
│   └── sports-betting.json     # 配置文件
├── scripts/
│   ├── analyze.py              # 主分析脚本
│   ├── data_collector.py       # 数据收集模块
│   ├── prediction_model.py     # 预测模型模块
│   ├── report_generator.py     # 报告生成模块
│   └── runner.sh               # OpenClaw 集成脚本
├── data/                       # 数据存储目录（运行时生成）
│   ├── analysis_history.json   # 分析历史记录
│   └── match_*.json            # 比赛数据
└── docs/                       # 文档目录
    └── DEVELOPMENT.md          # 本开发文档
```

## 核心模块

### 1. DataCollector (data_collector.py)

**职责**:
- 收集比赛基础数据
- 提取特征
- 存储历史数据

**方法**:
- `collect_match_data()`: 收集比赛数据
- `extract_features()`: 提取预测特征
- `_collect_team_stats()`: 收集球队统计
- `_collect_head_to_head()`: 收集历史对战
- `_collect_odds()`: 收集赔率数据
- `_collect_injuries()`: 收集伤病信息

**数据来源**（当前版本）:
- 模拟数据生成
- 随机值模拟真实分布

**数据来源**（未来版本）:
- NBA官方API
- 足球官方数据源
- 免费数据API
- 赔率聚合平台

### 2. PredictionModel (prediction_model.py)

**职责**:
- 生成比赛预测
- 计算概率
- 评估置信度

**方法**:
- `predict()`: 主预测方法
- `_predict_nba()`: NBA预测
- `_predict_football()`: 足球预测
- `_sigmoid()`: Sigmoid激活函数
- `_predict_spread()`: 预测让分
- `_predict_total()`: 预测总分
- `_predict_over_under()`: 预测大小球
- `ensemble_predict()`: 集成预测
- `monte_carlo_simulation()`: 蒙特卡洛模拟

**算法**:
- 简化的逻辑回归
- 多特征加权
- Sigmoid概率转换
- 支持集成学习（可选）

### 3. ReportGenerator (report_generator.py)

**职责**:
- 生成分析报告
- 格式化输出
- 风险提示

**方法**:
- `generate_report()`: 生成完整报告
- `_generate_summary()`: 生成摘要
- `_generate_data_overview()`: 生成数据概览
- `_format_prediction()`: 格式化预测结果
- `_generate_betting_recommendation()`: 生成投注建议
- `_generate_explanation()`: 生成解释性说明
- `_analyze_factors()`: 分析各因素
- `format_as_text()`: 格式化为文本
- `save_report()`: 保存报告

### 4. SportsBettingAnalyzer (analyze.py)

**职责**:
- 主控制器
- 协调各模块
- 命令行接口

**方法**:
- `analyze_match()`: 分析比赛
- `_assess_risk()`: 评估风险
- `_is_value_bet()`: 判断价值投注
- `_calculate_bet_percentage()`: 计算投注比例
- `get_today_recommendations()`: 获取今日推荐
- `show_analysis_history()`: 显示分析历史

## 特征工程

### NBA 特征

1. **实力对比** (strength_diff)
   - 赛季胜率差异
   - 积分排名差异
   - 历史表现

2. **主客场优势** (home_advantage)
   - 主场胜率 vs 客场胜率
   - NBA主场优势约10-15%

3. **近期状态** (recent_form)
   - 最近5场比赛表现
   - 胜/负统计
   - 动态趋势

4. **历史对战** (h2h_advantage)
   - 历史交锋记录
   - 心理优势

5. **伤病影响** (injury_impact)
   - 关键球员缺阵
   - 影响系数

### 足球特征

1. **实力对比** (strength_diff)
   - 赛季胜率
   - 积分排名
   - 进球失球

2. **主客场优势** (home_advantage)
   - 足球主场优势约8-10%
   - 欧洲联赛主场明显

3. **近期状态** (recent_form)
   - 最近5场表现
   - 胜/平/负统计

4. **历史对战** (h2h_advantage)
   - 历史交锋
   - 风格克制

5. **伤病影响** (injury_impact)
   - 核心球员状态

## 预测模型

### 基础模型

```
score = w1*strength_diff + w2*home_advantage +
        w3*recent_form + w4*h2h + w5*injury_impact

probability = sigmoid(score)
```

### 权重配置

**NBA**:
- strength: 0.3
- home_advantage: 0.2
- recent_form: 0.15
- h2h: 0.15
- injuries: -0.1

**足球**:
- strength: 0.25
- home_advantage: 0.2
- recent_form: 0.15
- h2h: 0.15
- injuries: -0.1

### 概率转换

使用 Sigmoid 函数将得分转换为概率:

```
sigmoid(x) = 1 / (1 + e^(-x))
```

### 三分式概率（足球）

足球需要考虑平局:

```
P(team1) = sigmoid(score + offset)
P(team2) = sigmoid(-score + offset)
P(draw) = 1 - P(team1) - P(team2)
```

## 风险评估

### 置信度分级

- **高置信度** (> 0.75): 低风险
- **中置信度** (0.65 - 0.75): 中风险
- **低置信度** (< 0.65): 高风险

### 价值投注判断

比较模型概率与市场赔率隐含概率:

```
if model_prob > market_prob + threshold:
    value_bet = True
```

### 投注比例计算

根据置信度和风险等级动态调整:

```
base_percentage = config.default_bet_percentage

if confidence > 0.8:
    bet_percentage = base * 1.5
elif confidence > 0.7:
    bet_percentage = base
else:
    bet_percentage = base * 0.5
```

## 配置说明

### config/sports-betting.json

```json
{
  "risk_level": "moderate",        // 风险偏好
  "default_bet_percentage": 2,     // 默认投注比例(%)
  "preferred_leagues": [...],      // 优先联赛
  "min_confidence": 0.6,          // 最低置信度
  "max_daily_bets": 3,             // 每日最大投注数
  "model_settings": {
    "use_ensemble": false,         // 集成模型
    "num_ensemble_models": 3,
    "use_monte_carlo": false       // 蒙特卡洛模拟
  }
}
```

## 扩展方向

### 短期

1. **真实数据源接入**
   - NBA Stats API
   - Football-Data.org
   - TheSportsDB

2. **模型优化**
   - 调整权重参数
   - 添加更多特征
   - 历史数据回测

3. **功能增强**
   - 实时赔率监控
   - 历史准确率追踪
   - 自动推送推荐

### 长期

1. **高级模型**
   - 深度学习
   - 随机森林
   - XGBoost

2. **实时功能**
   - 比赛直播分析
   - 盘口变动跟踪
   - 套利机会检测

3. **社区功能**
   - 分享分析结果
   - 用户评论
   - 排行榜

## 测试

### 单元测试

```bash
python3 -m pytest tests/
```

### 集成测试

```bash
# 测试NBA分析
./scripts/runner.sh NBA 湖人 勇士

# 测试足球分析
./scripts/runner.sh football 巴萨 皇马

# 测试今日推荐
./scripts/runner.sh today NBA
```

### 性能测试

```bash
time ./scripts/runner.sh NBA 测试队1 测试队2
```

## 已知限制

1. **数据准确性**: 当前使用模拟数据
2. **模型简单**: 仅使用简化逻辑回归
3. **无实时性**: 不支持实时数据更新
4. **覆盖率**: 仅支持NBA和部分足球联赛
5. **准确率**: 未经过历史数据验证

## 免责声明

本工具仅供学习和娱乐使用，不构成任何投资或投注建议。

使用本工具产生的任何后果，开发者不承担责任。

请理性对待体育博彩，遵守当地法律法规。

---

**开发者**: 黄杨
**版本**: 1.0.0
**最后更新**: 2026-04-02