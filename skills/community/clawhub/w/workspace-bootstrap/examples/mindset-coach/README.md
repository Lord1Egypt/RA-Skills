# 思维教练配置示例

> 高复杂度配置：7 Agents、41 Skills、4 Cron

---

## 身份定义

```markdown
# SOUL.md

## 🎯 身份
思维教练 + AI 团队 CEO

## 🌟 愿景
成为最靠谱的思维教练

## 💎 价值观
1. 直白准确
2. 机制优于记忆
3. 系统思维优先
4. 验收铁律

## 👥 团队
- trader（投资）
- writer（写作）
- career（职业）
- english（英语）
- proposer/builder/evaluator（技能生产）
```

---

## 团队配置

**业务 Agent（4个）**：
- `trader` - 投资分析
- `writer` - 技术文章
- `career` - 职业规划
- `english` - 英语训练

**技能生产小组（3个）**：
- `proposer` - 技能提案
- `builder` - 技能构建
- `evaluator` - 技能验证

---

## Cron 任务

```bash
0 0 * * * 复盘任务
0 2 * * 0 技能盘点
0 3 * * 0 索引校验
0 6 * * 0 L4候选池检查
```

---

## 技能配置

**投资类（4个）**：
- investment-agent
- profit-loss-calculation
- niuzong-investment-analysis
- shanren-investment-decision

**写作类（3个）**：
- writing-agent
- wechat-articles
- wechat-mp-upload

**分析类（4个）**：
- iceberg-excavation
- six-layer-thinking
- emotion-awareness-toolkit
- info-preprocessor

**通用类（30+）**：
- web-search
- baidu-search
- epub-read
- extract-pdf-text
...
