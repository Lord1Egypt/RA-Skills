# TqSdk 量化交易策略集

> 基于 [天勤量化 TqSdk](https://github.com/shinnytech/tqsdk-python) 实现的期货量化交易策略示例集合，每个策略附有完整中文注释和详细策略思路讲解。

---

## 关于 TqSdk

**TqSdk（天勤量化开发包）** 是由 [信易科技](https://www.shinnytech.com/) 发起并开源的 Python 量化交易框架，专为国内期货市场设计。

### 核心特性

- 极简代码：几十行代码即可构建完整的量化交易策略。
- 全品种数据：覆盖期货、期权、股票，提供全历史 Tick 与 K 线数据。
- 实时行情：毫秒级行情推送，数据全在内存，零访问延迟。
- 全流程支持：历史数据 → 开发调试 → 策略回测 → 模拟交易 → 实盘交易。
- 广泛兼容：支持市场上 90% 以上的期货公司实盘交易。
- Pandas 友好：数据直接以 `pandas.DataFrame` 返回，无缝对接数据分析。

---

## 官方资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://doc.shinnytech.com/tqsdk/latest/ |
| 快速入门 | https://doc.shinnytech.com/tqsdk/latest/quickstart.html |
| API 参考 | https://doc.shinnytech.com/tqsdk/latest/reference/index.html |
| TqSdk GitHub | https://github.com/shinnytech/tqsdk-python |
| 信易科技官网 | https://www.shinnytech.com/ |
| 快期账户注册 | https://account.shinnytech.com/ |

---

## 安装与配置

### 1. 安装环境
要求：Python >= 3.8（推荐 3.10+）
```bash
pip install tqsdk -U
2. 快速上手
在任一策略文件中替换 YOUR_ACCOUNT 和 YOUR_PASSWORD 为你的快期账户信息，然后运行：

bash
python strategies/01_double_ma.py
策略库概览（61 个实战模型）
存储路径：/strategies/。每个文件均包含 500 字以上的逻辑说明及核心代码注释。

趋势与突破类（01–45）
[01] 双均线趋势：MA5/MA20 金叉死叉基础模型。

[05] 海龟交易：经典唐奇安通道突破 + ATR 仓位管理。

[30] SuperTrend：基于 ATR 动态轨道的自适应趋势跟踪。

[44] 顾比均线：短期与长期均线组发散/聚拢识别趋势强度。

[45] 趋势过滤 RSI：大周期均线定性，小周期 RSI 捕捉回调机会。

多因子、对冲与机构模型（46–55）
[46] 多因子选股：动量、趋势、波动率、成交量四因子综合评分。

[47] 跨市场对冲：基于 Z-Score 的相关品种（如 RB vs HC）价差对冲。

[49] 均值方差组合：基于 Markowitz 框架的夏普比率最优权重配置。

[51] 期限结构回归：利用近远月合约基差（Contango/Back）进行回归交易。

高级专题与 AI 预测（56–61）
[56] 黑色系截面轮动：多品种动量与 Ranking 排名轮动。

[57] 自适应波动率：基于波动率锥（Volatility Cone）的动态头寸管理。

[60] 机器学习排名：利用回归/分类模型辅助截面因子打分。

[61] 统计套利：包含协整检验（Cointegration）的专业对冲逻辑。

风险提示
本仓库所有策略仅供学习和研究使用，不构成任何投资建议。量化交易存在亏损风险，实盘前请务必使用 TqSim 模拟账户进行充分测试。历史回测结果不代表未来实盘表现。

许可证
本项目基于 MIT License 开源。TqSdk 本身基于 Apache-2.0 License。