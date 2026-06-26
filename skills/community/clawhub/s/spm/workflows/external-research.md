# External Research — 外部资源分析

> Phase 1 可选子流程。当项目需要分析外部代码库、参考技能、技术方案对比时使用。

## When to Activate

- 用户说"参考一下 XXX 的做法"、"对比 A 和 B 两个方案"
- 需要从 GitHub 仓库、开源项目中提取设计模式
- 技能/工具选型：分析多个候选方案，逐项对比

## Workflow

### Step 1: 明确分析目标

在开始获取外部资源前，先和用户对齐：

```
分析目标：我们要从 [外部资源] 中提取什么？
  - 整体架构对比？
  - 某个具体功能的实现方案？
  - 可复用的设计模式？
  - 性能/安全/测试策略？
```

### Step 2: 获取资源

```
1. GitHub 仓库 → curl API / git clone
   curl -s "https://api.github.com/repos/<owner>/<repo>/contents/<path>"
   curl -s "https://raw.githubusercontent.com/<owner>/<repo>/main/<path>"

2. 文档/博客 → web_fetch
3. 本地代码库 → exec ls / read
```

**铁律：先列文件清单再决定读哪些，不要盲目全量下载。**

### Step 3: 结构化分析

对每个候选方案，按统一维度分析：

```markdown
| 维度 | 方案A | 方案B | 方案C |
|------|-------|-------|-------|
| 核心思路 | | | |
| 适用场景 | | | |
| 优势 (比 SPM 强在哪) | | | |
| 劣势 (不如 SPM 的地方) | | | |
| 可采纳的具体点 | | | |
| 采纳风险/代价 | | | |
```

### Step 4: 输出采纳清单

```markdown
## 采纳决策

### P0 — 必须采纳 (显著优于 SPM)
1. [特性名] — 来自 [来源] — 改 [SPM 文件]
   - 理由: [一句话]
   - 改动范围: [文件列表]

### P1 — 值得采纳
1. ...

### ❌ 不采纳
1. [特性名] — 理由: [一句话]
```

### Step 5: 过渡到 Planning

将采纳清单中的每个项目转为 WBS 任务。优先级：P0 先。

## 输出

- `docs/spm/research/YYYY-MM-DD-xxx-analysis.md` — 结构化分析报告
- 采纳清单 → Phase 2 的 WBS 输入

## 注意事项

- 外部资源的许可协议是否允许借鉴？（MIT/Apache 安全，AGPL 需谨慎）
- 不要整段复制代码——提取设计模式，用自己的方式实现
- 分析完成后删除下载的临时文件
