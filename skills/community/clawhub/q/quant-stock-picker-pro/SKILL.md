---
name: quant-stock-picker-pro
version: 1.0.0
description: AI-powered stock screening tool for Chinese A-shares. Daily picks using multi-factor analysis (fundamentals + technical + sentiment). Use when user asks about stock screening, quantitative trading, or investment opportunities.
---

# Quant Stock Picker Pro

AI增强的A股量化选股工具，每日自动筛选优质股票。

## 功能

- **多因子分析**：基本面（60%）+ 技术面（40%）
- **AI预测**：XGBoost、LightGBM、随机森林集成
- **另类数据**：新闻情感、股吧情绪、搜索热度
- **风险控制**：动态止损、波动率目标、行业中性化
- **自动推送**：每日9:35 AM自动运行（工作日）

## 使用场景

用户询问以下问题时自动触发：
- "推荐股票"
- "今天买什么"
- "量化选股"
- "股票筛选"
- "投资机会"

## 工作流程

1. **获取数据**（9:35 AM）
   - 全市场A股实时行情（新浪API）
   - 新闻情感数据（AkShare）
   - 股吧情绪数据（东方财富）

2. **多因子打分**
   - 成长股因子（营收增长、利润增长、ROE、市值、PE）
   - 技术面因子（涨幅、量比、换手率、连续上涨）
   - 另类数据因子（新闻情感、社交媒体、搜索热度）

3. **AI预测**
   - 集成学习模型（XGBoost + LightGBM + 随机森林）
   - 交叉验证准确率：F1 0.54%
   - 置信度分级（高/中/低）

4. **风险控制**
   - 排除涨停板附近（涨幅>9.5%）
   - 排除亏损企业（PE<0）
   - 排除超高估值（PE>100）
   - 确保流动性（成交额>1000万）

5. **筛选输出**
   - TOP 10 推荐股票
   - 包含：代码、名称、得分、关键指标、买入理由、风险提示

## 输出格式

```markdown
# 量化选股报告 - YYYY-MM-DD

## TOP 10 推荐

| 排名 | 代码 | 名称 | 得分 | 涨幅 | PE | 换手率 | 买入理由 |
|------|------|------|------|------|----|----|----------|
| 1 | 600989 | 宝丰能源 | 45 | +8.32% | 17.5 | 5.2% | 低估值+温和上涨+成交活跃 |

## 风险提示

⚠️ **重要声明**：
- 本工具仅供学习参考，不构成投资建议
- 股市有风险，投资需谨慎
- 历史表现不代表未来收益
- 请根据自身风险承受能力做决策

## 系统信息

- 数据源：新浪财经（实时）
- AI模型：XGBoost + LightGBM + 随机森林
- 准确率：F1 0.54%（交叉验证）
- 运行时间：9:35 AM（工作日）
```

## 技术架构

```
quant-stock-picker-pro/
├── scripts/
│   ├── quant-stock-picker-ultimate-integrated.py  # 主脚本
│   ├── factor_engine.py                           # 因子工程
│   ├── data_collector.py                          # 数据采集
│   ├── risk_backtest.py                           # 风险管理
│   └── market_executor.py                         # 市场识别
├── references/
│   ├── factors.md                                 # 因子库文档
│   ├── strategies.md                              # 策略说明
│   └── data-sources.md                            # 数据源说明
└── SKILL.md                                       # 技能说明
```

## 安装

```bash
# 安装依赖
pip install pandas numpy scikit-learn xgboost lightgbm efinance akshare

# 设置定时任务
openclaw cron add --name "每日量化选股" --schedule "35 9 * * 1-5" --script scripts/quant-stock-picker-ultimate-integrated.py
```

## 配置

在 `scripts/config.py` 中配置：

```python
# 筛选参数
MIN_SCORE = 25          # 最低得分
MAX_PE = 100            # 最大PE
MIN_VOLUME = 10000000   # 最小成交额（元）

# AI模型参数
USE_AI = True           # 是否使用AI增强
CONFIDENCE_LEVEL = "medium"  # 置信度阈值（high/medium/low）

# 另类数据
USE_NEWS_SENTIMENT = True     # 新闻情感
USE_SOCIAL_SENTIMENT = True   # 社交媒体
USE_SEARCH_HEAT = True        # 搜索热度
```

## 定制化

可以根据需求调整：

1. **选股策略**
   - 保守型：低估值 + 回调买入
   - 进取型：成长股 + 突破买入
   - 平衡型：混合策略

2. **因子权重**
   - 基本面权重（0-100%）
   - 技术面权重（0-100%）
   - 另类数据权重（0-100%）

3. **风险偏好**
   - 低风险：严格筛选，10只股票
   - 中风险：适度筛选，20只股票
   - 高风险：宽松筛选，30只股票

## 注意事项

- ⚠️ 仅供学习参考，不构成投资建议
- ⚠️ 股市有风险，投资需谨慎
- ⚠️ 历史表现不代表未来收益
- ⚠️ 请根据自身风险承受能力做决策

## 更新日志

- **v1.0.0** (2026-03-04): 初始版本
  - 多因子分析
  - AI预测
  - 另类数据整合
  - 风险控制

---

**作者**: Sugar Daddy
**版本**: 1.0.0
**许可**: MIT
