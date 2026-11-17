# 触发词冲突检测规则 v1.0

> 大脑加强：检测多个技能之间的触发词/描述冲突，避免误触发。
> 业界参考：搜索引警的 query disambiguation、IDE 的 command palette 唯一性约束。
> 本规则只读、只评估、只输出告警；不修改任何技能描述。

## 一、为什么需要冲突检测

**用户痛点**：当两个技能描述相近时，AI Agent（如 Claude/Codex）会"猜"该调用哪个，导致：
- 用户说"总结"→ 可能触发 summarize 或 summarize-cli 或 summary-bank
- 用户说"搜索"→ 可能触发 agent-reach 或 firecrawl 或 search-mcp
- 用户说"调试"→ 可能触发 systematic-debugging 或 debug-pro 或 debug-helper

**业界经验**：
- VS Code command palette：要求每个 command 唯一前缀
- Spotlight/Alfred：用评分模型解决歧义
- 桌面搜索引擎：编辑距离 + 关键词权重

## 二、冲突类型分类

| 类型 | 描述 | 严重度 | 示例 |
|:-:|---|:-:|---|
| **同义词冲突** | 两个技能的触发词互为同义词 | 🔴 高 | "总结" vs "归纳" |
| **包含冲突** | 一个触发词完全包含另一个 | 🟠 中 | "技能审查" 包含 "审查" |
| **范围冲突** | 描述涵盖的领域高度重叠 | 🟠 中 | 两个调研类技能都涵盖"多平台搜索" |
| **格式冲突** | 同名技能在不同平台描述不一致 | 🟡 低 | ZCode 上叫"调研"，Claude 上叫"研究" |
| **触发词过宽** | 触发词过于通用，可能误命中 | 🟡 低 | "工具"、"功能"作为触发词 |

## 三、检测算法（轻量版）

### Step 1：提取每个技能的触发词集

```python
def extract_triggers(skill_description, skill_name):
    """从描述中提取触发词候选"""
    triggers = set()
    
    # 格式 A: "主题 → ..." 中 → 之前的部分
    if '→' in skill_description:
        trigger_part = skill_description.split('→')[0].strip()
        triggers.update(split_by_separators(trigger_part, ['·', '|', '/']))
    
    # 格式 B: skill_name 本身（如 "summarize" 是英文触发词）
    triggers.add(skill_name.lower())
    
    # 格式 C: 描述开头的前 3-5 个字（中文）或前 2 个词（英文）
    first_chunk = extract_first_chunk(skill_description)
    if first_chunk:
        triggers.add(first_chunk)
    
    # 格式 D: 同义词扩展（来自 codex-ui-zh-glossary.json）
    for t in list(triggers):
        triggers.update(get_synonyms(t))
    
    return triggers
```

### Step 2：两两计算冲突分

```python
def conflict_score(triggers_a, triggers_b):
    """返回 0-1 的冲突分，1=完全冲突"""
    
    # Jaccard 相似度
    intersection = triggers_a & triggers_b
    union = triggers_a | triggers_b
    jaccard = len(intersection) / len(union) if union else 0
    
    # 编辑距离（最小距离归一化）
    min_edit = min(
        edit_distance(a, b) / max(len(a), len(b), 1)
        for a in triggers_a for b in triggers_b
    )
    edit_similarity = 1 - min_edit
    
    # 包含关系
    contains = any(a in b or b in a for a in triggers_a for b in triggers_b)
    
    # 综合
    score = max(jaccard, edit_similarity * 0.8)
    if contains:
        score = max(score, 0.6)
    
    return score
```

### Step 3：标记冲突对

```python
CONFIDENCE_THRESHOLDS = {
    'high': 0.7,    # 🔴 同义词冲突，必须处理
    'medium': 0.5,  # 🟠 包含/范围冲突，建议处理
    'low': 0.3,     # 🟡 轻度重叠，留意
}

def classify_conflict(score, skill_a, skill_b):
    if score >= CONFIDENCE_THRESHOLDS['high']:
        return ('🔴 high', '同义词冲突')
    elif score >= CONFIDENCE_THRESHOLDS['medium']:
        return ('🟠 medium', '范围重叠')
    elif score >= CONFIDENCE_THRESHOLDS['low']:
        return ('🟡 low', '轻度相似')
    return None
```

## 四、同义词表（扩展 codex-ui-zh-glossary.json）

> 这些词互为同义词，不应同时出现在不同技能的触发词中

```yaml
synonym_groups:

  - group: "总结/归纳"
    words: [总结, 归纳, 汇总, 精炼, 摘要, 概括]
    canonical: 总结
  
  - group: "审查/审计"
    words: [审查, 审计, 检查, 诊断, 评估]
    canonical: 审查
  
  - group: "搜索/调研"
    words: [搜索, 调研, 查找, 检索, 调查]
    canonical: 调研
  
  - group: "调试/排错"
    words: [调试, 排错, 诊断, 修复]
    canonical: 调试
  
  - group: "创建/生成"
    words: [创建, 生成, 构建, 制作, 新建]
    canonical: 创建
  
  - group: "优化/改进"
    words: [优化, 改进, 提升, 增强]
    canonical: 优化
  
  - group: "翻译/本地化"
    words: [翻译, 本地化, 中文化, 转换]
    canonical: 翻译
  
  - group: "分析/解析"
    words: [分析, 解析, 拆解, 剖析]
    canonical: 分析
  
  - group: "推荐/建议"
    words: [推荐, 建议, 引荐]
    canonical: 推荐
```

## 五、输出格式

```text
⚠️ 触发词冲突检测

🔴 高冲突（建议立即处理）
| 技能 A | 技能 B | 冲突类型 | 冲突分 | 共同触发词 | 建议 |
|---|---|---|:-:|---|---|
| summarize | summarize-cli | 同义词 | 0.85 | 总结, 摘要, 归纳 | 改名其中一个（如 summarize → 会话总结） |
| agent-reach | firecrawl-search | 范围重叠 | 0.72 | 搜索, 调研 | 用作用域隔离（reach=社交，firecrawl=深度） |

🟠 中冲突（建议留意）
| 技能 A | 技能 B | 冲突类型 | 冲突分 | 备注 |
|---|---|---|:-:|---|
| skills-audit | skills-summarize-audit | 包含 | 0.65 | 前者已归档，应清理 |

🟡 低冲突（记录观察）
| 技能 A | 技能 B | 冲突分 |
|---|---|:-:|
| learn | cangjie-skill | 0.35 |

🛡 已豁免（用户/系统标记为有意共存）
| 技能对 | 豁免理由 | 豁免时间 |
|---|---|---|
| docx | pdf | 同属 document-skills 包 | 2026-07-19 |
```

## 六、处理建议模板

> Audit 不直接修改，只给出"用户应让 agent 做什么"的指导

### 模板 A：重命名建议

```
[对 agent 说]

我接受了 Audit 的冲突报告，请按以下步骤重命名 "summarize-cli"：

1. 备份现有 SKILL.md
2. 将 frontmatter 的 name: summarize-cli 改为 content-summary-cli
3. 将 description 的触发词从 "总结" 改为 "内容总结"
4. 同步更新以下引用（如果有）：
   - skill-registry.yaml 中的对应条目
   - README.md 中的引用
5. 让我刷新 Codex/Claude 验证触发不再冲突
```

### 模板 B：作用域隔离建议

```
[对 agent 说]

"agent-reach" 与 "firecrawl-search" 触发词冲突，但功能互补。
请帮我配置"上下文感知"避免误触发：

1. 在 ~/.agents/AGENTS.md 中追加：
   "用户说'调研/搜索'时，默认调用 agent-reach；
    用户明确说'抓取/爬取/JS 渲染'时，调用 firecrawl。"
2. 在两个 SKILL.md 的 description 中追加"场景限定"：
   - agent-reach: "互联网调研 → 多平台·社交"（强调多平台）
   - firecrawl: "深度抓取 → JS 渲染·反反爬"（强调深度）
```

### 模板 C：归档建议

```
[对 agent 说]

"skills-audit" 与 "skills-summarize-audit" 冲突，前者已废弃。
请帮我：

1. mv ~/.agents/skills/skills-audit ~/.agents/skills/archived/skills-audit-2026-07-19
2. 更新 ~/.agents/skills/archived/README.md，记录归档原因
3. 检查 ~/.zcode/cli/config.json 是否还引用 skills-audit，如有则移除
```

## 七、豁免机制

> 有些"冲突"是用户有意的（如官方 docx + pdf 同包），需要豁免

```yaml
# .data/conflict-exemptions.json
exemptions:
  - pair: ["docx", "pdf"]
    reason: "同属 document-skills 官方包"
    expires: null  # 永久豁免
    added_at: "2026-07-19"
  
  - pair: ["summarize", "summarize-cli"]
    reason: "前者=会话总结，后者=内容总结，已重命名触发词"
    expires: "2026-10-19"  # 临时豁免，3 个月后复核
    added_at: "2026-07-19"
```

### 豁免添加流程

```
1. Audit 输出冲突报告
2. 用户说："docx 和 pdf 是有意共存，豁免"
3. Audit 验证：豁免是否合理（同包/互补/明确分工）
4. 输出指令：建议 agent 追加到 .data/conflict-exemptions.json
5. 下次扫描跳过此对
```

## 八、增量检测

> 全量扫描成本高，支持增量

```python
def incremental_detection(new_skill, all_skills):
    """只检测新增技能与现有的冲突"""
    new_triggers = extract_triggers(new_skill)
    conflicts = []
    for existing in all_skills:
        if existing.name == new_skill.name:
            continue
        existing_triggers = extract_triggers(existing)
        score = conflict_score(new_triggers, existing_triggers)
        if score >= 0.3:
            conflicts.append((existing, score))
    return sorted(conflicts, key=lambda x: -x[1])
```

### 触发场景

- 用户安装新技能后 → 自动增量检测
- 用户编辑 description 后 → 增量检测受影响技能
- 全量审计（"技能审查"）→ 全量两两检测

## 九、与 v7.1.0 的集成

### 新增 Phase：在 ⑥ 报告后追加

```yaml
# 注：references/flow/ 已于 v8.2.1 归档至 references/.archived/flow-v7/，此过时 TODO 不再适用
phase: "⑥-f 冲突检测"
trigger:
  - 全量审计时
  - 新增技能时
  - description 修改后
input:
  - 所有可见技能的 name + description
output:
  - 冲突报告（按本文件第五节格式）
  - 处理建议（按本文件第六节模板）
skip_when:
  - 单技能精炼模式
  - CI 模式且 token 预算 < 2000
```

## 十、维护

- 同义词表新增：第四节 synonym_groups
- 阈值调整：第三节 CONFIDENCE_THRESHOLDS
- 新增冲突类型：第二节分类
- 豁免清单：`.data/conflict-exemptions.json`（运行时）
