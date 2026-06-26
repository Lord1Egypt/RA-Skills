# tob-win-loss-review — 丢单复盘助手

> 输入行业/规模/阶段/竞品/关键事件，基于李宁原创 ToB 销售经验规则输出根因分析、风险信号和改进建议。

本技能从 v2.0.0 起改为**纯规则引擎**：不打包任何客户商业资产，默认可离线运行。

## 快速开始

```bash
# 交互模式
python3 scripts/tob_win_loss_review.py

# 快速模式
python3 scripts/tob_win_loss_review.py --industry 零售 --size 大型 \
  --duration 4个月 --stage 报价谈判 --competitor 略 \
  --event "客户说我们价格比竞品高30%"
```

## 输出结构

```
项目画像 → 根因分析(规则依据) → 风险信号 → 改进建议
```

根因分析中的「规则依据」来自行业 + 阶段 + 事件三因素交叉匹配，例如：

```
规则依据：行业[零售]+阶段[报价谈判]+事件[价格/预算触发] → 价格竞争力风险
```

## 技术栈

- Python 3 标准库
- 纯规则引擎：行业 / 阶段 / 事件三因素经验模型
- 概率排序：核心原因 / 辅助原因 / 潜在风险

## 安装

```bash
clawhub install tob-win-loss-review
# 或
openclaw skills install tob-win-loss-review
```

## 版权

规则经验来自李宁原创 ToB 销售与解决方案实践。

## 链接

- GitHub: https://github.com/william202404/tob-skills
- ClawHub: `clawhub search tob-win-loss-review`
- SkillHub: `skillhub search tob-win-loss-review`

## License

MIT-0 (No Attribution Required)
