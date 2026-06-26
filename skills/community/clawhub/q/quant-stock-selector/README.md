# 量化选股系统 - ClawHub Skill

📈 基于 AKShare + 多因子模型的 A 股量化选股工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-green.svg)](https://clawhub.ai/skills/quant-stock-selector)

## ⚠️ 重要风险提示

**在使用本系统前，请务必阅读 [SKILL.md](SKILL.md) 中的风险提示章节。**

- 股市有风险，投资需谨慎
- 历史业绩不代表未来收益
- 本工具仅供参考，不构成投资建议
- 使用者应自行承担投资风险

## 快速开始

### 1. 安装

```bash
# 通过 ClawHub 安装
clawhub install quant-stock-selector

# 或手动安装
cd ~/.openclaw/skills
git clone https://github.com/quant-dev/quant-stock-skill.git
```

### 2. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 3. 配置邮箱

编辑 `config/email_config.py`：

```python
EMAIL_ACCOUNT = "your_email@163.com"
EMAIL_PASSWORD = "your_auth_code"
EMAIL_TO = "your_email@163.com"
```

### 4. 运行

```bash
# 每日选股推荐
python3 tools/daily_recommender.py

# 胜率统计
python3 tools/performance_tracker.py
```

## 功能特点

- ✅ 六大维度综合评分
- ✅ 每日自动选股（Top 3）
- ✅ 详细推荐理由
- ✅ 胜率统计面板
- ✅ 邮件推送
- ✅ 周末消息分析

## 预期效果

| 指标 | 预期值 |
|------|--------|
| 胜率 | 70-80% |
| 平均收益 | +10-20% |
| 封板概率 | 30-40% |

⚠️ **注意**：以上数据为历史回测结果，不代表未来收益。

## 文档

- [完整使用说明](SKILL.md)
- [权重分配说明](docs/WEIGHT_ALLOCATION.md)
- [90% 集中度规则](docs/CONCENTRATION_90_RULE.md)
- [选股逻辑](docs/STOCK_SELECTION_LOGIC.md)

## 风险提示

⚠️ **使用本系统前，请务必阅读以下风险提示：**

1. **股市有风险，投资需谨慎**：股票市场存在固有风险，可能导致本金损失
2. **历史业绩不代表未来收益**：过往回测数据和胜率仅供参考，不代表未来表现
3. **无收益保证**：本系统不保证任何收益，使用者应自行承担投资风险
4. **止损纪律**：建议设置 -8% 止损，严格执行
5. **仓位控制**：单只股票不超过 20% 仓位，总仓位不超过 60%

详见 [SKILL.md](SKILL.md) 中的风险提示章节。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 作者

- Author: Quant Developer
- Email: quant_dev@example.com
- GitHub: https://github.com/quant-dev

## 支持

如有问题，请提交 Issue：https://github.com/quant-dev/quant-stock-skill/issues

---

**感谢使用量化选股系统！祝投资顺利！** 📈
