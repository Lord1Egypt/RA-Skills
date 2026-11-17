# Pre-Gate & Entry Routing Reference

Complete methodology for Phase -1 (pre-gate) and Phase 0 entry routing in skill-forge v5.0.

**When to read**: When entering Phase -1 (pre-gate check) or Phase 0 (entry routing). Read this file in full before starting.

---

## Part 1: Pre-Gate (前置闸门)

**Purpose**: Before investing time in interview + creation, judge whether this idea is worth making into a Skill at all.

### Three Checks

| Check | Question | Pass | Fail (劝退) |
|-------|----------|------|-------------|
| **Worth doing?** | 最近一周做了3次以上？做法基本固定？输出格式可预期？ | ≥2个Yes → proceed | 一次性任务 → "直接问AI更快，不用做Skill" |
| **Already exists?** | SkillHub上有没有现成的高质量同类？ | 没有 or 有但有明显差距 → proceed | 有且很好 → "建议直接安装: `skillhub install <slug>`" |
| **Too big?** | 这个想法是不是其实是好几个Skill？ | 单一场景 → proceed | 多场景 → "这其实是N个Skill，建议拆开。先做哪个？" |

###劝退原则

一个会劝你别做的 Skill creator，因为它知道 AI 的边界在哪里。

- 你这事要是只干一次 → 直接问AI更快
- Claude张口就能办 → 不值得做成Skill
- 更该做成别的形态（脚本/模板/配置）→ 建议替代方案
- 想法太大（"帮我做所有的数据分析"）→ 提示拆分，先聚焦一个

**省得你忙活半天，做出个没人用的摆设。**

---

## Part 2: Five Entry Routes (五类入口路由)

After pre-gate passes, detect which entry route the user is coming from:

| Route | Signal | Strategy |
|-------|--------|----------|
| **R1: 从零想法** | "我想做个帮我做X的skill" | 进入自适应访谈（Phase 0.2） |
| **R2: 从对话提取** | "把刚才对话变成skill" / "把咱们刚才做的存成skill" | 扫描上下文对话→提取步骤/工具/纠正→生成四要素草稿→确认门 |
| **R3: 从现成材料** | 用户给文档/SOP/流程规范 | 分析材料→反推四要素→补缺→确认门 |
| **R4: 从草稿完善** | 用户给半成品SKILL.md | 检查缺失模块→补全→验证 |
| **R5: 改进已有skill** | "我的skill不触发" / "跑偏了" / "太啰嗦" | 进入诊断模式（Part 3） |

### Route Detection

Scan user's first message for signals:

- Contains "做个skill" + no context → R1
- Contains "刚才/刚刚/存成/变成" → R2
- Contains attachment / "照这个文档" / "这是我们的SOP" → R3
- Contains existing SKILL.md content / "帮我补全" → R4
- Contains "不触发/不工作/跑偏/太啰嗦/改进" → R5
- Ambiguous → Ask: "你是从头开始做，还是有现成的材料或对话想固化？" (3 options + Other)

### R2: Dialog Extraction Method

When user says "把刚才对话变成skill":

1. Scan all conversation context
2. Extract: steps taken, tools used, user corrections, output format
3. Generate draft four-elements:
   - 做什么: based on what was actually done
   - 何时触发: based on what user said to start
   - 输入输出: based on actual input/output
   - 边界: based on what user rejected or corrected
4. Present summary → 确认门 → **Step 0.4 同类预检**（不可跳过）

### R3: Material Analysis Method

When user provides a document/SOP:

1. Read the material thoroughly
2. Extract four-elements by reverse-engineering:
   - 做什么: what does this material guide?
   - 何时触发: when would someone need this?
   - 输入输出: what goes in, what comes out?
   - 边界: what's explicitly excluded?
3. Fill gaps with targeted questions (max 3)
4. Present summary → 确认门 → **Step 0.4 同类预检**（不可跳过）

### R4: Draft Completion Method

When user has a half-finished SKILL.md:

1. Check which modules are present: name? description? 任务? 输出格式? 规则? 示例?
2. **反推四要素**：从半成品草稿反推 做什么/何时触发/输入输出/边界（即使用户带着成熟草稿，也必须收敛递归转写为 plan）
3. Present summary → 确认门 → **Step 0.4 同类预检**（不可跳过，避免重复造轮子）
4. 同类预检通过后（无更好同类 or 有差距需新建），补全缺失模块
5. Run full validation (Step 4)

> **关键约束**：R4 入口即使用户给的是完整草稿，也不能直接跳到 Step 4 验证。必须先走"反推四要素 → 确认门 → 同类预检"流程，确保 SkillHub 同类搜索比对不被遗漏。

---

## Part 3: Skill Improvement Diagnosis (改进诊断)

When user says "my skill doesn't work / runs off / too verbose":

### Diagnosis Script: Symptom → Check Point → Action

| Symptom | Check Point | Action |
|---------|------------|--------|
| **不被触发** | description里有没有触发关键词？关键词在前200字符吗？ | 重写description，关键词前置 |
| **触发太频繁** | description太宽泛？Do NOT范围太窄？ | 收窄description，扩大Do NOT |
| **输出跑偏** | 任务定义模糊？输出格式不具体？ | 锁定任务边界，固定输出格式 |
| **输出太啰嗦** | 规则太多？示例太长？ | 精简到3-5条规则，示例只保留1组 |
| **边界情况崩** | 示例没覆盖边界？规则有漏洞？ | 补充边界示例，修复规则漏洞 |
| **格式不一致** | 输出格式字段模糊？ | 每个字段固定具体格式 |
| **安全风险** | 有curl/wget/凭证读取？ | 立即移除，走安全红线检查 |

### Improvement Flow

```
用户描述症状
  ↓
诊断脚本匹配症状 → 检查点 → 动作
  ↓
执行修复
  ↓
触发测试验证（5条真实用户说法）
  ↓
确认修复有效 → 迭代或交付
```

### Level-Adaptive Diagnosis

- 小白：直接告诉用户哪里有问题、怎么改，用户只需确认
- 老手：指出问题点和优化方向，让用户自己决定改不改
