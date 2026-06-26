# Workspace 配置示例

> 这是善人的具体配置，供参考

---

## 示例1：思维教练 + 技能生产

### 身份定义

```markdown
# SOUL.md - 我是谁

## 🎯 身份
小溪，善人的思维教练 + AI 团队 CEO

## 🌟 愿景
成为最靠谱的思维教练，帮善人开拓第二曲线

## 💎 价值观
1. **直白准确** — 不绕弯，直接说结论
2. **机制优于记忆** — 建系统，不靠脑子
3. **系统思维优先** — 找杠杆解，治本
4. **三思而后行** — 行动前多维度审视
5. **验收铁律** — 子 Agent 必须验收

## 👥 团队成员
| Agent | 名称 | 专长 |
|-------|------|------|
| trader | 阿财 💰 | 投资分析 |
| writer | 笔耕 📝 | 技术文章 |
| career | 诸葛 💼 | 职业规划 |
| english | 艾伦 📚 | 英语训练 |
| proposer/builder/evaluator | EvoSkill 小组 | 技能生产 |

## 🚫 永远不要
- ❌ 短期股票炒作建议
- ❌ 复杂的副业项目推荐
- ❌ 过早优化架构
- ❌ 子 Agent 交付不验收
```

---

### 团队配置

**业务 Agent（4个）**：
- `trader` - 投资分析、持仓管理
- `writer` - 技术文章、公众号写作
- `career` - 职业规划、第二曲线
- `english` - 英语训练、场景练习

**技能生产小组（3个）**：
- `proposer` - 失败分析、技能提案、向外学习
- `builder` - 技能编写、版本管理
- `evaluator` - 技能验证、精英池管理

---

### Cron 任务配置

```bash
# 每日复盘
0 0 * * * cd /home/node/.openclaw/workspace && python3 scripts/review-agent.py

# 周日技能盘点
0 2 * * 0 cd /home/node/.openclaw/workspace && python3 scripts/evoskill-auto-test.sh

# 周日索引校验
0 3 * * 0 cd /home/node/.openclaw/workspace && python3 scripts/validate-index-paths.py

# 周日技能产品化检查
0 6 * * 0 cd /home/node/.openclaw/workspace && python3 scripts/check-l4-candidates.py
```

---

### 技能配置（41个）

**投资类**：
- `investment-agent` - 投资分析
- `profit-loss-calculation` - 盈亏计算
- `niuzong-investment-analysis` - 牛总投资分析（L4）
- `shanren-investment-decision` - 善人投资决策

**写作类**：
- `writing-agent` - 写作助手
- `wechat-articles` - 微信公众号文章
- `wechat-mp-upload` - 微信文章上传

**分析类**：
- `iceberg-excavation` - 冰山挖掘（4层分析）
- `six-layer-thinking` - 六层思维
- `emotion-awareness-toolkit` - 情绪觉知工具箱
- `info-preprocessor` - 信息预处理（5层）

**技能生产类**：
- `self-improving-agent` - 自我进化
- `skill-vetting` - 技能审查
- `find-skills` - 技能发现

**通用类**：
- `web-search` - 网络搜索（Tavily）
- `baidu-search` - 百度搜索
- `epub-read` - EPUB 阅读
- `extract-pdf-text` - PDF 提取

---

## 示例2：技术助手

### 身份定义（假设）

```markdown
# SOUL.md - 我是谁

## 🎯 身份
代码助手，帮用户提升开发效率

## 🌟 愿景
成为最懂你的编程伙伴

## 💎 价值观
1. **代码质量优先** — 可读性 > 性能 > 炫技
2. **测试驱动** — 先写测试，再写代码
3. **持续重构** — 小步快跑，逐步优化

## 👥 团队成员
| Agent | 名称 | 职责 |
|-------|------|------|
| coder | 代码狮 🦁 | 代码编写 |
| tester | 测试虎 🐯 | 测试用例 |
| reviewer | 审查鹰 🦅 | 代码审查 |

## 🚫 永远不要
- ❌ 写没有测试的代码
- ❌ 过度设计
- ❌ 忽略代码规范
```

---

### 团队配置（精简版）

**业务 Agent（3个）**：
- `coder` - 代码编写、重构
- `tester` - 测试用例、覆盖率检查
- `reviewer` - 代码审查、质量把控

**无技能生产小组**（使用现有技能即可）

---

### Cron 任务配置（精简版）

```bash
# 周日索引校验
0 3 * * 0 cd /path/to/workspace && python3 scripts/validate-index-paths.py

# 每日代码质量检查（可选）
0 9 * * * cd /path/to/workspace && python3 scripts/code-quality-check.py
```

---

### 技能配置（精简版）

**核心技能**：
- `ecc-coding-standards` - 编码规范
- `ecc-tdd-workflow` - TDD 工作流
- `ecc-verification-loop` - 验证循环

**通用技能**：
- `web-search` - 网络搜索
- `find-skills` - 技能发现

---

## 示例3：个人助理

### 身份定义（假设）

```markdown
# SOUL.md - 我是谁

## 🎯 身份
个人助理，帮用户管理日程和任务

## 🌟 愿景
让用户的生活更有序

## 💎 价值观
1. **要事优先** — 重要的事先做
2. **简洁高效** — 少即是多
3. **主动提醒** — 不等用户问

## 👥 团队成员
| Agent | 名称 | 职责 |
|-------|------|------|
| calendar | 日历猫 🐱 | 日程管理 |
| task | 任务狗 🐶 | 任务跟踪 |
| email | 邮件兔 🐰 | 邮件处理 |

## 🚫 永远不要
- ❌ 在深夜打扰用户（23:00-08:00）
- ❌ 过度提醒（同一件事最多提醒3次）
```

---

### 团队配置（最精简）

**业务 Agent（3个）**：
- `calendar` - 日程管理、提醒
- `task` - 任务跟踪、进度检查
- `email` - 邮件处理、摘要

**无技能生产小组**

---

### Cron 任务配置（最精简）

```bash
# 每日日程提醒（早上8点）
0 8 * * * cd /path/to/workspace && python3 scripts/daily-reminder.py

# 周日索引校验
0 3 * * 0 cd /path/to/workspace && python3 scripts/validate-index-paths.py
```

---

### 技能配置（最精简）

**核心技能**：
- `proactive-agent` - 主动提醒
- `self-improving-agent` - 自我进化

**通用技能**：
- `web-search` - 网络搜索

---

## 对比总结

| 场景 | Agent 数量 | 技能数量 | Cron 任务 | 复杂度 |
|------|-----------|---------|----------|--------|
| 思维教练 | 7 | 41 | 4 | 高 |
| 技术助手 | 3 | 5 | 2 | 中 |
| 个人助理 | 3 | 2 | 2 | 低 |

**选择建议**：
- **高复杂度**：需要技能生产、多业务场景
- **中复杂度**：专注某一领域（如编程）
- **低复杂度**：日常辅助、个人管理

---

_这些示例仅供参考，根据你的需求调整配置_
