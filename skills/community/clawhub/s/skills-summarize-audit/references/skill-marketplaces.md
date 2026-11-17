# 技能市场目录与发现框架 v1.0

> 大脑加强：本技能不直接抓取市场数据，提供"市场目录 + 评估维度 + 决策框架"。
> 用户 Agent 按本表提供的 URL 自行抓取，Audit 给出推荐结论。

## 一、主流技能市场对比（2026-07 实测可用）

| 市场 | 主 URL | 规模 | 平台 | 特色 | 推荐场景 |
|---|---|---|:-:|---|---|
| **Anthropic Skills** | https://claude.com/skills | 官方 | Claude | 内置技能 + 组织技能 | 权威背书 |
| **Skills Directory** | https://www.skillsdirectory.com/ | 500+ | Claude | **50+ 安全规则扫描 + A/B/C 评级** | **安全首选** |
| **SkillRegistry.io** | https://skillregistry.io/ | 300+ | 多平台 | `.md` 文件直传 | 跨平台 |
| **csreg.nexus** | https://www.csreg.nexus/ | 200+ | Claude Code | 版本化 + 团队共享 | 企业团队 |
| **Skill CLI** | https://skillsdir.dev/docs/cli | - | 多平台 | 包管理 CLI | 类 npm 体验 |
| **claude-plugins.dev** | https://claude-plugins.dev/skills | - | Claude | agentskills spec | 标准化 |
| **OpenAI Codex Skills** | https://github.com/openai/codex (内置) | - | Codex | 官方内置 | Codex 用户 |

### 各市场 API（用户授权后由 agent 调用）

```
# Skills Directory（含安全评级，推荐主源）
https://www.skillsdirectory.com/api/registry
https://www.skillsdirectory.com/api/registry/{skill-name}
https://www.skillsdirectory.com/api/registry?q={query}&category={cat}

# SkillRegistry.io
https://skillregistry.io/api/skills
https://skillregistry.io/api/skills/{slug}

# csreg.nexus
https://www.csreg.nexus/api/skills
https://www.csreg.nexus/api/skills/{name}/versions
```

## 二、技能健康度七维评估（参考 OpenSSF + Skills Directory 安全规则）

| 维度 | 权重 | 评估指标 | 取数方式 | 阈值（10 分制） |
|:-:|:-:|---|---|---|
| **安全合规** | 25% | Skills Directory grade / 自身 SEC 规则 | SD API / security-rules.yaml | A=10 · B=7 · C=3 · 无=0 |
| **维护活跃度** | 20% | 最近 commit / release 距今天数 | GitHub API | <30d=10 · <90d=7 · <180d=4 · ≥180d=1 |
| **社区热度** | 15% | stars / 安装数 / issues 响应 | GitHub / SD API | ⭐≥1k=10 · ≥100=7 · ≥10=4 · <10=1 |
| **文档完整度** | 15% | SKILL.md 字数 / examples / references | fetch SKILL.md | 完整=10 · 基础=6 · 缺=2 |
| **依赖深度** | 10% | 引用文件数 / 是否含 MCP / 是否需 API Key | 解析 SKILL.md | 无依赖=10 · 1-3=7 · 4+=3 |
| **触发词质量** | 10% | TQI 分（见 translation-quality.md） | 本技能自评 | ≥8=10 · 6-7=7 · <6=3 |
| **测试与示例** | 5% | 有无 tests/ / fixtures / 示例输出 | 检查目录 | 全有=10 · 部分=5 · 无=0 |

### 综合分公式

```
SkillHealth = 安全×0.25 + 维护×0.20 + 社区×0.15 + 文档×0.15 + 依赖×0.10 + 触发词×0.10 + 测试×0.05
```

**判定阈值**：
- ≥8.0 → 🟢 **保留**（核心工具）
- 6.0–7.9 → 🟡 **观察**（次级工具）
- 4.0–5.9 → 🟠 **评估**（建议升级或替换）
- <4.0 → 🔴 **归档候选**

## 三、推荐技能候选库（精选 T0/T1，按场景分类）

### 🛠️ 技能开发类

| 技能 | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **skill-creator** (官方) | 创建/编辑 SKILL.md | 9 | anthropic skills repo |
| **skill-installer** (官方) | 从仓库安装 | 8 | anthropic skills repo |
| **plugin-creator** (官方) | 插件脚手架 | 8 | anthropic skills repo |

### 📝 写作与文档类

| 技能 | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **document-skills/docx** | DOCX 创建/编辑 | 9 | 官方 zcode-plugins |
| **document-skills/pdf** | PDF 生成/解析 | 9 | 官方 zcode-plugins |
| **humanizer** | 去 AI 味 | 7 | skillsdirectory.com |

### 🔬 调研分析类

| 技能 | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **agent-reach** | 多平台调研（13 渠道） | 9 | https://github.com/Panniantong/Agent-Reach |
| **last30days** | 30 天趋势 | 8 | 本地 |
| **scrapling** | 反反爬抓取 | 8 | https://github.com/D4Vinci/Scrapling |

### 🎨 设计与创意类

| 技能 | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **gpt-taste** | AIDA 页面 + GSAP | 8 | 本地 |
| **hatch-pet** | 像素宠物生成 | 7 | 本地 |

### 🧠 思维与方法论类

| 技能 | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **brainstorming** (官方) | 结构化头脑风暴 | 8 | anthropic |
| **systematic-debugging** (官方) | 多层根因分析 | 9 | anthropic |
| **sequential-thinking** | 链式推理（MCP） | 9 | 官方 servers |

### 📊 总结与记忆类

| 技能 | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **summarize** | 会话精炼 + 错误收割 | 9 | https://github.com/gtbwpkwjnb-alt/summarize-skill |
| **memory-bank** | 跨会话记忆 | 8 | skillsdirectory |

### 🎓 学习与教学类

| 技能 | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **learn** | 视频/音频转知识 | 8 | 本地 |
| **cangjie-skill** | 知识蒸馏 | 7 | 本地 |

## 四、用户 Agent 抓取指引（指导"如何指导 agent"）

### 模板：让 agent 评估某个新技能

```
[用户对 agent 说]

我要评估是否引入技能 "X"，请按以下步骤：

1. 调用 WebFetch 获取：
   - https://www.skillsdirectory.com/skills/X （安全评级）
   - https://skillregistry.io/skills/X       （跨平台可用性）
   - 技能 GitHub repo README（活跃度）

2. 按七维评估：
   | 维度 | 权重 | 评分依据 | 备注 |
   |---|---|---|---|
   | 安全合规 | 25% | SD grade | ? |
   | 维护活跃度 | 20% | 最近 commit | ? |
   | 社区热度 | 15% | stars | ? |
   | 文档完整度 | 15% | SKILL.md 字数 | ? |
   | 依赖深度 | 10% | 是否需 MCP/Key | ? |
   | 触发词质量 | 10% | 描述规范度 | ? |
   | 测试与示例 | 5% | tests/ | ? |

3. 给出 🟢/🟡/🟠/🔴 判定 + scope 建议（project/global）
4. 列出"安装前必须确认的 3 件事"（许可证/兼容性/作用域）
```

### 模板：发现某类需求的最优技能

```
[用户对 agent 说]

我需要"视频转文字 + 知识入库"的技能。请：

1. 在以下市场搜索关键词 ["video transcript", "subtitle extract", "knowledge import"]：
   - skillsdirectory.com
   - skillregistry.io
   - github.com（搜索 SKILL.md 包含相关词）

2. 横向对比前 5 个候选，输出对比表
3. 如已安装 "learn" 技能，判断是替代/互补/无关
4. 推荐 top-1，给出安装命令和确认清单
```

## 五、跨平台一致性检查

> 同名技能在不同平台的版本/description 可能不一致

### 检查规则

```yaml
# 假设已扫描到多平台技能路径
for skill_name in all_skill_names:
  occurrences = [
    {platform: "zcode", path: "~/.zcode/skills/X", version: "1.2"},
    {platform: "claude", path: "~/.claude/skills/X", version: "1.0"},
    {platform: "codex", path: "~/.codex/skills/X", version: "1.2"},
  ]
  
  # 一致性检查
  versions = unique(occurrences.version)
  descriptions = unique(occurrences.description)
  
  if len(versions) > 1:
    warning: "版本不一致，建议同步到最新"
  if len(descriptions) > 1:
    warning: "description 不一致，可能触发不一致行为"
  
  # 推荐同步目标
  latest_version = max(versions)
  target_platforms = [p for p in occurrences if p.version != latest_version]
```

### 输出格式

```
🔄 跨平台一致性检查

| 技能 | ZCode | Claude | Codex | 一致性 | 建议 |
|---|---|---|---|:-:|---|
| summarize | 6.8.0 | 6.8.0 | 6.5.0 | ⚠️ 版本 | 升级 Codex 到 6.8.0 |
| learn | 4.1.0 | - | - | ✅ 单平台 | 考虑同步到 Claude |
```

## 六、官方/可信来源白名单

> 这些来源的技能默认信任度更高，可降低安全审查强度

```yaml
trusted_sources:
  - name: "Anthropic 官方"
    repos: ["anthropics/skills", "anthropics/claude-code-skills"]
    grade: A
    note: "Anthropic 官方维护"

  - name: "OpenAI 官方"
    repos: ["openai/codex"]
    grade: A
    note: "Codex 内置技能"

  - name: "ZCode 官方插件"
    repos: ["zcode-plugins-official"]
    grade: A
    note: "本地已安装的官方插件包"

  - name: "Microsoft 官方"
    repos: ["microsoft/*"]
    grade: A-
    note: "微软系 MCP/skills"
```

## 七、给推荐引擎的输入契约

```
skill_candidates:
  - name: "scrapling"
    source_market: "github"
    source_url: "https://github.com/D4Vinci/Scrapling"
    health_score: 7.5
    confidence: "observed"
    capability_match:
      - dimension: web-scrape
        score: 9
        evidence: "topics: web-scraping, anti-bot"
    relationship_to_existing: "complement"  # 与 agent-reach 互补
    scope_suggestion: "project"
    install_complexity: "low"
    license: "MIT"
    security_grade: "B"
```

## 八、安全边界

- 默认不抓市场；触发词"推荐"/"建议"且用户授权后由 agent 抓取
- Skills Directory grade < B 的技能标记 🔴 不建议
- 来源不明的 GitHub repo（< 10 stars + < 30 天）标记 🟠 高风险
- 涉及凭证/网络的技能必须显式列出风险点

## 九、维护

- 市场规模/URL 变动时更新本表
- 新增高分技能时追加到第三节"候选库"
- 评估维度变更时同步 `references/recommendation-framework.md`
- 安全规则更新时同步 `references/security-rules.yaml`
