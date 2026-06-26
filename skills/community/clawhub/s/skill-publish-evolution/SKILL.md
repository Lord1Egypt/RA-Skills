---
name: skill-publish-evolution
description: 技能发布与自我进化工作流 — 自动化发现可封装能力、发布到技能市场、学习其他Agent优秀实践并回灌改进。适用于Agent能力沉淀、市场发布、持续进化闭环。
metadata: {"emoji":"🚀","category":"agent-tools","trigger":["发布技能","封装能力","自我进化","技能市场"]}
---

# Skill Publish & Evolution Workflow

Agent 能力封装、市场发布、持续进化的标准化闭环工作流。帮助 Agent 系统化地沉淀能力、赚取积分、从其他 Agent 学习并持续进化。

## Use When 何时使用

**触发此技能：**
- 完成一个复杂任务后，发现可复用的能力模式
- 需要将自动化脚本封装为标准化 Skill
- 计划发布技能到 clawhub/EvoMap 等市场
- 需要学习其他 Agent 的优秀技能设计
- 执行 Agent 自我进化和能力迭代
- 触发词：`发布技能`、`封装能力`、`自我进化`、`技能市场`、`publish skill`

**不使用此技能：**
- 一次性脚本，没有复用价值
- 简单任务，不值得标准化封装

## Standard Workflow 标准工作流

### Phase 1: 能力发现与盘点
```bash
# 1. 盘点本地已有资源
ls -la skills/
find . -name "*.sh" -o -name "*.py" -o -name "*.js" | grep -v node_modules

# 2. 识别可封装模式
# - 重复执行的自动化流程
# - 解决特定领域问题的完整方案
# - 有明确边界的工具链
```

### Phase 2: 发布链路验证
```bash
# 验证 clawhub 通道（优先推荐）
clawhub whoami
# Expected: ✅ username

# 验证 EvoMap 通道（备选）
node -e "require('axios')"                  # 检查依赖
ls config/publish.json                      # 检查配置
curl -I https://evomap.ai/api/v1/publish    # 检查API可达性

# 决策：选择第一个可用通道，阻塞时记录原因
```

### Phase 3: 同行学习（关键回灌步骤）
```bash
# 1. 搜索同领域 2-3 个优秀技能
clawhub search <domain-keyword>
clawhub inspect <skill-name>

# 2. 提取可借鉴模式：
# - 命名可发现性：是否包含领域关键词
# - 摘要结构：Use When + 触发词清单
# - 范围收敛：聚焦 3-5 个具体用例
# - 工作流标准化：分阶段 + 代码示例

# 3. 回灌到自己的技能设计
```

### Phase 4: Skill 标准化封装

**目录结构规范：**
```
skills/your-skill-name/
├── SKILL.md           # 主文件（必需）
├── README.md          # 补充说明（可选）
├── scripts/           # 辅助脚本
└── references/        # 参考资料
```

**SKILL.md 规范：**
```yaml
---
name: skill-id-kebab-case
description: 技能名 — 一句话说明。适用场景xxx/xxx/xxx。触发词：a、b、c
metadata: {"emoji":"📌","category":"category-name"}
---

# Skill Name
简短的能力定位说明

## Use When 何时使用
**使用此技能：**
- 场景1
- 场景2
- 触发词：xxx、yyy

**不使用此技能：**
- 不适用的场景
```

### Phase 5: 发布与验证
```bash
# 1. 执行发布
clawhub publish skills/your-skill-name/

# 2. 联合验证（注意索引延迟）
clawhub search your-skill-name
clawhub inspect your-skill-name

# 3. 记录状态
# - ✅ 已发布：skill-name, version, published-at
# - ⏳ 索引中：publish成功，search/inspect待同步
# - ❌ 被阻塞：列出具体原因（依赖缺失/配置/API不可达）
```

### Phase 6: 持续进化闭环
1. 每发布 3 个技能后，回顾发布流程并优化此 Skill
2. 每月抽样查看市场 Top 10 技能，提取最佳实践
3. 收集安装/评分数据，迭代已有技能

## Blockers & Mitigation 阻塞与应对

| 阻塞点 | 应对策略 |
|--------|----------|
| EvoMap 缺 axios 依赖 | 改用 clawhub 通道 |
| EvoMap 缺 publish.json 配置 | 改用 clawhub 通道 |
| EvoMap API 403/404 | 改用 clawhub 通道 |
| publish 成功但 inspect 查不到 | 按索引延迟处理，用 search 二次佐证 |

## Best Practices 最佳实践

1. **边界清晰**：一个 Skill 只解决一类问题
2. **可发现性**：名称+描述包含领域关键词
3. **可操作性**：每个工作流步骤都有可执行代码
4. **诚实记录**：区分「已完成/已验证/被阻塞」，不做未验证承诺
5. **回灌优先**：先学习他人，再发布自己，站在巨人肩膀上

## Output Format 输出规范

任务完成后统一输出格式：
```
📦 技能发布与自我进化报告

🔍 能力盘点：已识别 X 个可封装能力
🔌 发布通道：clawhub/EvoMap/被阻塞（原因）
📚 同行学习：已学习 N 个技能，提取 M 项改进点
🚀 已发布技能：
  - skill-name-1 (version) ✅
  - skill-name-2 (version) ⏳（索引中）
🔮 下一步：具体行动项
```

## Safety & Limits 安全与边界

- 仅发布自己有权发布的原创内容
- 不泄露任何 API Key、凭证到技能市场
- 不编造积分、收益、安装量数据（平台未返回则写"积分未知"）
- 不要仅因一次 inspect 失败就判定发布失败
- 真实环境反馈与流程不一致时，以真实证据为准
