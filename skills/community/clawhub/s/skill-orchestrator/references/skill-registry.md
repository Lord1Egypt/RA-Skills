# Skill Registry — 技能注册表格式规范 v2.0

## 概述

Skill Registry 是 skill-orchestrator 的"眼睛"——它感知当前环境中哪些 Skill 可用，并按需检索最匹配的那个。

**核心原则：平台无关。用户用任何 AI 工具/平台安装本 Skill，编排器都能正常跑起来。**

## 多源发现架构

```
用户请求编排
    │
    ├── Source 1: 本地文件系统
    │   ├── ~/.workbuddy/skills/          （WorkBuddy 用户级）
    │   └── {project}/.workbuddy/skills/ （WorkBuddy 项目级）
    │
    ├── Source 2: ClawHub Marketplace
    │   └── {已安装列表 + 热门 Skill 缓存}
    │
    ├── Source 3: 用户自定义路径
    │   └── 环境变量 SKILL_PATH（逗号分隔多个路径）
    │
    └── Source 4: 内置兜底矩阵
        └── 始终可用，保证零依赖
```

**发现优先级：**
```
Source 1 > Source 2 > Source 3 > Source 4
（优先用本地精确匹配，降级到市场查询，再降级到自定义路径，最后兜底）
```

## Source 1：本地文件系统扫描

**扫描路径（按顺序尝试）：**

| 平台 | 路径 | 说明 |
|---|---|---|
| WorkBuddy 用户级 | `~/.workbuddy/skills/` | 用户自己安装的 Skill |
| WorkBuddy 项目级 | `./.workbuddy/skills/` | 当前项目的共享 Skill |
| Claw 本地 | `~/.claw/skills/` | Claw 用户级（兼容） |
| 自定义 | `SKILL_PATH` 环境变量 | 用户自定目录 |

**扫描规则：**
1. 遍历所有目标目录的子目录
2. 每个子目录若含 `SKILL.md`，则视为一个有效 Skill
3. 读取 frontmatter 的 `name`、`description`、`location` 字段
4. 注册到内存索引

**Registry Entry 格式：**

```yaml
- name: "pdf"
  description: "处理 PDF 文件的读写、合并、分割等操作"
  location: "plugin"              # user | plugin | manager | claw | custom
  source: "local"                 # local | marketplace | builtin
  capabilities:
    - read_pdf
    - merge_pdf
    - split_pdf
  tags: ["document", "pdf", "office"]
  installed: true
  install_path: "~/.workbuddy/skills/pdf"

- name: "skill-orchestrator"
  description: "技能编排器 - 理解复杂需求，自动拆解并调度多个专家Skill协作"
  location: "user"
  source: "local"
  risk_tier: "low"
  capabilities:
    - orchestrate
    - dispatch
    - merge_results
  consumes: ["user_goal"]
  produces: ["markdown_report", "optional_json_bundle"]
  tags: ["orchestration", "multi-skill"]
  installed: true
  install_path: "~/.workbuddy/skills/skill-orchestrator"
```

## 建议扩展字段（可选，利于匹配与安全门禁）

各 Skill 可在 `SKILL.md` frontmatter 或侧车 YAML 中声明（与 OpenClaw `metadata.openclaw` 兼容时最佳）：

| 字段 | 说明 |
|------|------|
| `risk_tier` | `low` / `medium` / `high`，供编排器与 Checkpoint 规则引用 |
| `capabilities` | 短标签数组，如 `read_pdf`、`orchestrate` |
| `consumes` | 期望的上游输入类型，如 `user_brief`、`upstream_markdown` |
| `produces` | 输出类型，如 `markdown_report`、`json_metrics` |

**skill-orchestrator 自描述示例**：`risk_tier: low`；`capabilities: [orchestrate, dispatch, merge_results]`；`consumes: [user_goal]`；`produces: [markdown_report, optional_json_bundle]`。

## Source 2：ClawHub Marketplace 查询

**当本地扫描结果不足（< 2 个匹配）时，查询 ClawHub API：**

```
搜索策略：
1. 用需求关键词搜索 ClawHub 热门 Skill
2. 获取 Top-5 结果的 name、description、tags
3. 标记为 "marketplace" 来源，供用户决定是否安装
4. 不自动安装（需要用户同意）
```

**输出格式：**

```
═══════════════════════════════════════════════
🌐 ClawHub 市场发现
═══════════════════════════════════════════════

本地未找到足够匹配，探索市场中...

[M] CLAUDE-CODE-COACH  (热门 #12)
    描述：AI 编程教练，优化代码风格与架构
    评分：4.8 ⭐ | 安装量：8.2k
    标签：coding, coaching, architecture

[M] FIGMA-TO-CODE      (热门 #34)
    描述：Figma 设计稿转前端代码
    评分：4.6 ⭐ | 安装量：5.1k
    标签：design, frontend, figma

[?] 安装任一？回复 "安装 {名称}" 即可
═══════════════════════════════════════════════
```

## Source 3：用户自定义路径

**通过环境变量配置：**

```bash
#  ~/.zshrc 或 ~/.bashrc
export SKILL_PATH="~/my-skills,~/corp-skills,/opt/shared-skills"
```

编排器启动时读取 `SKILL_PATH`，扫描所有路径，合并到 Registry。

## Source 4：内置兜底矩阵

**始终可用，不依赖任何外部环境。**

| 需求关键词 | Fallback Skill（内置模拟） |
|---|---|
| pdf, 文档, 合并, 分割 | 内置 PDF 处理逻辑（文字提取/合并/分割） |
| excel, 表格, xlsx, 数据 | 内置数据处理逻辑（计算/格式化） |
| ppt, 演示, 幻灯片 | 内置 PPT 结构逻辑（大纲生成） |
| word, docx, 合同 | 内置文档逻辑（结构生成） |
| 搜索, research, 调研 | 内置搜索逻辑（多源检索 + 综合） |
| 浏览器, 网页, 截图 | 内置浏览器操作逻辑（DOM 操作模拟） |
| 编程, 代码, debug | 内置代码审查逻辑（风格检查 + 优化建议） |
| 视频, 生成, 剪辑 | 内置视频处理逻辑（脚本生成 + 分镜） |

**Fallback 调用示例：**

```
[step-2a] 产品规划分析
  Skill：产品总监（内置模拟）
  模式：acceptEdits
  来源：builtin
  依赖：无

→ 不需要外部 Skill，编排器直接以内置角色输出结果
```

## 检索算法

```
输入：用户需求文本
输出：排序后的 Skill 候选列表

Step 1: 关键词精确匹配（权重 ×10）
  - 提取需求中的名词/动词
  - 匹配 Skill name、description 中的关键词

Step 2: Tag 语义扩展（权重 ×5）
  - 将需求映射到标准 Tag 集
  - 匹配相同 Tag 的 Skill

Step 3: 来源加成
  - 本地已安装：+3
  - Marketplace 有：+1（可降级安装）

Step 4: 综合评分
  score = exact_match×10 + tag_match×5 + desc_sim×2 + source_bonus

Step 5: 过滤
  - 优先本地 > 市场 > 内置
  - 返回 Top-3 候选
  - 低于阈值（< 5分）→ 直接用内置兜底
```

## 错误处理

| 场景 | 处理策略 |
|---|---|
| 所有 Source 均无结果 | 使用内置兜底，保证编排不中断 |
| 环境变量路径不存在 | 跳过该路径，不报错 |
| SKILL.md 解析失败 | 跳过该 Skill，继续扫描其他 |
| ClawHub API 不可用 | 降级到本地 + 内置，不阻塞编排 |
| 磁盘 I/O 超时（> 2s） | 跳过该目录，用其他 Source |

## 调用接口

```javascript
// 编排器内部调用流程
async function discoverSkills(query) {
  const results = [];

  // Source 1: 本地扫描
  const local = await scanLocalPaths(LOCAL_PATHS);
  results.push(...local.map(s => ({ ...s, source: 'local' })));

  // Source 2: ClawHub（仅当本地不足时）
  if (results.length < 2) {
    const marketplace = await queryClawHub(query);
    results.push(...marketplace.map(s => ({ ...s, source: 'marketplace' })));
  }

  // Source 3: 自定义路径
  const customPaths = (process.env.SKILL_PATH || '').split(',').filter(Boolean);
  if (customPaths.length) {
    const custom = await scanLocalPaths(customPaths);
    results.push(...custom.map(s => ({ ...s, source: 'custom' })));
  }

  // Source 4: 内置兜底（始终可用）
  const builtin = getBuiltinFallback(query);
  results.push(...builtin.map(s => ({ ...s, source: 'builtin' })));

  // 评分排序
  const scored = results.map(s => ({
    skill: s,
    score: calculateScore(query, s)
  }));

  return scored.sort((a, b) => b.score - a.score);
}
```
