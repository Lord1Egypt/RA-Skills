# Description Quality Check — Skills-Summarize-Audit v6.4.0

> 描述质量检查规则和精炼生成规则。这是 **skills-audit 的核心特色能力**：自动将技能 description 翻译为中文触发词+简介（或反向翻译），方便跨语言用户快速了解技能功能。
> 参见 SKILL.md 步骤④-第四步。

## 核心原则

1. **触发词翻译精炼**是 skills-audit 的主要能力——不仅检查描述质量，更重要的是为中文用户生成可直接理解的中文触发词和简介
2. **语言自适应**：根据用户会话主语言决定翻译方向
3. **同义字词扩展**：翻译时自动为触发词生成同义字词，提升可发现性

## 检查项

| 检查项 | 规则 | 不合格的处理 |
|:--------|:------|:-------------|
| 语言 | 根据用户会话主语言决定翻译方向 | 自动生成目标语言版本 |
| 格式 | 必须遵循 `触发词 → 功能简介` | 自动重排为规范格式 |
| 长度 | 单侧语言 ≤40 字符 | 截断并保留核心语义 |
| 双语 | 中英双语 ` | ` 分隔，各自 ≤40 字符 | 自动补全缺失语言版本 |
| 同义字词 | 触发词扩展 2-4 个同义字词（仅中文侧） | 自动从同义词表匹配 |

## 语言自适应规则（v5.6.0 新增）

> 根据用户会话主语言自动切换翻译方向，无需手动配置 `output_language`。

| 会话特征 | 主语言 | 翻译方向 | 报告语言 |
|:---------|:------|:---------|:---------|
| 中文消息占比 >70% | zh | 英→中（将英文 description 翻译为中文触发词+简介） | zh |
| 英文消息占比 >70% | en | 中→英（将中文 description 翻译为英文触发词+简介） | en |
| 中英混合或无法判定 | auto | 双向（同时生成中英双语，主语言按最近 5 条消息判定） | 双语 |

> 判定优先级：会话历史 > `output_language` 配置 > 默认 auto。

## 语言判定规则（旧版，output_language 手动模式）

| output_language | 行为 |
|:----------------|:------|
| `auto`（默认） | 自动检测会话语言，中文环境→中文为主+英文为辅；英文环境→英文为主+中文为辅 |
| `zh` | 中文优先。纯英文→生成中文优化版，同时保留英文作为辅助 |
| `en` | 英文优先。纯中文→生成英文优化版，同时保留中文作为辅助 |

## 精炼生成步骤

| 步骤 | 规则 | 示例 |
|:------|:------|:------|
| ① 提取触发词 | 从技能 name/frontmatter 取最常用调用名。**中文用户优先提取中文调用名**，无中文则翻译 name 为中文触发词 | `summarize` → `总结`；`brainstorming` → `头脑风暴`；`skills-audit` → `技能审查` |
| ② 扩展同义字词 | 为中文触发词扩展 2-4 个同义字词（仅中文侧），提升用户用不同说法触发时的匹配率 | `技能审查` → 审计/检查/诊断；`总结` → 归纳/汇总/精炼 |
| ③ 构建简介 | `动词+宾语` 结构，2-4 个核心功能用 `·` 分隔 | `会话精炼·进度追踪·自动迭代` |
| ④ 截断 | 超 40 字符时优先级：触发词 > 核心动词 > 宾语 > 修饰词 | `DOCX 创建·编辑·分析`（完整版→截断版） |
| ⑤ 翻译 | **意译优先**，功能对等 > 字面翻译；保持目标语言 ≤40 字符。翻译时考虑中文习惯表达（如 `audit` 不译为"审计"可译为"审查/检查"） | `Use when...` → `需求澄清·创意发散·方案对比` |
| ⑥ 双语拼接 | 主语言在前，` | ` 分隔，两侧各自 ≤40 字符。中文侧可附同义字词（以 `·` 或空格分隔） | `技能审查·审计 → 画像驱动·八维评分 \| Skill Audit → profile·8dim` |

## 同义字词映射表（v5.6.0 新增）

> 翻译时自动匹配扩展，提升中文用户的可发现性。

| 英文关键词 | 中文主词 | 同义字词（扩展） |
|:-----------|:---------|:-----------------|
| audit | 审查 | 审计·检查·诊断 |
| skill/capability/tool | 技能 | 能力·工具 |
| project | 项目 | 工程·环境 |
| summarize | 总结 | 归纳·汇总·精炼 |
| search | 搜索 | 查找·检索 |
| debug | 调试 | 排错·诊断 |
| review | 审查 | 检查·审阅 |
| create/build | 创建 | 生成·构建·制作 |
| optimize | 优化 | 改进·提升 |
| deploy | 部署 | 发布·上线 |

## 翻译精炼示例（英→中）

| 原始 description（英文） | 精炼后（中文为主 + 英文辅助） |
|:------------------------|:---------------------------|
| `Use when brainstorming ideas, generating creative solutions, or comparing different approaches` | `头脑风暴 → 创意发散·方案对比 \| Brainstorm → ideas·solutions` |
| `Systematic debugging methodology for complex issues across multiple layers` | `系统调试 → 多层排错·根因分析 \| Debug → systematic·root cause` |
| `Automates browser interactions for web testing, form filling, screenshots` | `浏览器自动化 → 测试·填表·截图 \| Browser → test·form·screenshot` |
| `Create, read, edit, and manipulate Word documents (.docx)` | `Word文档 → 创建·编辑·分析 \| DOCX → create·edit·analyze` |

## 翻译精炼示例（中→英）

| 原始 description（中文） | 精炼后（英文为主 + 中文辅助） |
|:------------------------|:---------------------------|
| `为AI编程助手提供游戏开发相关的专业技能支持` | `Game Dev → engine·design·assets \| 游戏开发 → 引擎·设计·资源` |
| `多平台互联网调研工具，支持13个渠道的信息获取` | `Web Research → 13 channels·multi-platform \| 互联网调研 → 13渠道·多平台` |

> 系统/插件技能（editable=false）只标注问题，不自动修改。
> 审计完成后必须回头检查 skills-summarize-audit 自身的 description 是否符合以上规范；不合格时输出修正候选，获得明确确认后才修改（解决自指盲区）。

---

## 质量门禁（v6.2.0 新增 — 联动 Forma 维度）

> 将 description-quality.md 从"翻译参考"升级为 **质量门禁**，在 ⑥-c output-check 阶段输出可执行的修复清单。

### 触发条件

| 条件 | Forma 扣分 |
|:-----|:----------:|
| description-quality.md 检测发现任一检查项不合格 | -1 档（如 A→B） |
| 多个检查项不合格 | -2 档（如 A→C） |
| 自身 description 违规 | -1 档（自检双重扣分） |

### 输出格式（在报告尾部新增 "📋 描述格式优化建议" 区块）

```
📋 描述格式优化建议（Forma 分 3.5/10 ⚠️）

| 技能 | 问题 | 建议 |
|:----|:-----|:-----|
| diagnose-commands | 整段英文 >200 字符 | 命令诊断 → 定位·修复斜杠命令配置 |
| learn | 含"(1次调用)"冗余词 | 学习+链接 → 自动提取·AI分析·闪卡·导入 |

🛠️ 格式优化参考：
  1. 统一使用 `主题 → 功能1·功能2·功能3` 箭头格式
  2. 全中文描述（标准缩写 MCP/TDD/PR 除外）
  3. 单侧 ≤40 字符
  4. 去除使用说明/触发条件等正文内容
```

### 自检规则（v6.2.0 严格执行）

每次审计必须检查 skills-summarize-audit 自身的 description：
1. 读取 `SKILL.md` 的 `description:` 字段
2. 用 Forma 4 项规则评分
3. 不合格时在报告中输出"⚠️ 自检：审计技能自身描述不合格 → 建议修正" 
4. 自动生成修正候选，不得绕过 description 写入确认门禁

---

## Forma 格式分规则（v8.2.2 合并自 description-refinement.md）

> 以下来自已删除的 `references/description-refinement.md`（v7 时代 Forma 格式分规则，原仅被已归档的 `.archived/flow-v7/06-d` 引用），其独特内容（Forma 维度、权重、阈值）合并于此，作为 Forma 维度的唯一事实源。

### Forma 四项检查规则

| 检查项 | 合格标准 | 不合格示例 |
|:-------|:---------|:-----------|
| **格式规范** | `主题 → 功能1·功能2·功能3` 箭头短语 | 完整句子、纯段落 |
| **语言一致性** | 全中文（标准缩写除外） | 中英混搭、整段英文 |
| **长度合规** | 单侧 ≤40 字符 | 超长描述含使用说明 |
| **信息密度** | 纯功能短语，无杂质 | 含触发条件、使用说明、版本号 |

### 标准缩写白名单

```
MCP  TDD  PR  TS  Python  API  Git  JSON  CLI  IDE
ACP  DOCX  iOS  AI  URL  SSH  HTTP  SSL  SQL
```

### Forma 权重与阈值

- 权重（唯一权威：`config.yaml` 的 `forma_check.weights`）：format_style 0.40 / language_consistency 0.30 / length_limit 0.20 / info_density 0.10。
- 报告阈值：Forma < 6.0 → 在报告中标记为"需优化"（`config.yaml` 的 `forma_check.threshold`）。

### Forma 评分等级

| Forma 分 | 等级 | 处理方式 |
|:---------|:-----|:---------|
| 10/10 | ✅ 合格 | 跳过 |
| 6-9/10 | ⚠️ 微调 | 自动精炼 |
| 0-5/10 | 🔴 需重写 | 按标准重写 |
