# DESIGN.md - OpenClaw Workspace Auditor（工作区体检）

> 五件套之一：家（initializer）→ 内容（memory-distill）→ 状态（tracker）→ 知识（kb-retriever）→ **健康（workspace-auditor）**
> 定位：工作区「质检员」——只读体检，只报不修，分级报告 + 修复建议

## 核心原则

1. **只读不修**：脚本只扫描报告，永不删除/移动/修改文件（红线：破坏性操作必须指挥官决策）
2. **渐进式依赖**：检查项按依赖件套分组，缺依赖自动降级跳过 + 提示，不报假阳性
3. **零依赖**：Python 标准库，无第三方包
4. **确定性**：所有检查逻辑收敛到 `scripts/scan_workspace.py`，SKILL.md 只做触发/解读/引导

## 检查项设计（5 类）

### 1. 目录合规（依赖 initializer）
| 检查 | 规则 | 级别 |
|---|---|---|
| 标准目录齐全 | projects/tasks/outputs/knowledge/scripts/memory/tmp 存在 | 🟡 缺失 |
| 根目录纯净 | 根目录只允许 *.md 配置文件（排除系统目录/隐藏文件） | 🟡 |
| 命名规范 | 目录 kebab-case `^[a-z0-9]+(-[a-z0-9]+)*$`；md kebab-case；py snake_case；js/ts camelCase | 🟡 |
| 命名豁免 | 含 CJK 字符的目录/文件名、系统文件（README/data_structure 等）不查 | - |

### 2. 任务健康（依赖 tracker v2）
| 检查 | 规则 | 级别 |
|---|---|---|
| PROGRESS.md 存在 | tasks/ 与 projects/ 下每个目录必须有（目录即容器） | 🟡 孤儿目录 |
| frontmatter 状态合法 | status 字段 ∈ {active, done, archived, paused}（缺失也算 🟡） | 🟡 |
| 超龄未完结 | PROGRESS.md mtime > 30 天 且 status ≠ done/archived | 🟡 |

### 3. 记忆健康（通用约定）
| 检查 | 规则 | 级别 |
|---|---|---|
| memory/ 日志空窗 | 最近日志日期距今 > 7 天 | 🟡 |
| MEMORY.md | 存在且非空 | 🟡 缺失 |

### 4. 知识库健康（依赖 kb-retriever）
| 检查 | 规则 | 级别 |
|---|---|---|
| data_structure.md 索引 | knowledge/ 下存在（缺失 → 提示可装 kb-retriever 建索引，其余降级） | 🟡 |
| 索引同步（索引孤儿） | 文件相对路径未出现在索引文本中（目录级覆盖算命中，宽松匹配） | 🟡 |
| 支持类型 | 仅 md/pdf/xlsx 受支持，其他类型（docx/pptx/图片等）提示 | 🟡 |
| 超大文件 | > 20MB（PDF 提取慢） | 🟡 |
| 根目录散文件 | knowledge/ 根目录直接散落的文件（未按主题归档） | 🟡 |
| 命名规范 | 同第 1 类（中文豁免） | 🟡 |

### 5. 垃圾/临时文件（通用，无依赖）
| 检查 | 规则 | 级别 |
|---|---|---|
| tmp/ 超龄 | tmp/ 下文件 mtime > 30 天 | 🟡 |
| 大文件定位 | 全工作区 > 50MB | 🟡 |

## 输出格式

- **JSON**（`--json`）：结构化 findings，供程序消费
  ```json
  {
    "workspace": "/path",
    "scanned_at": "2026-08-28T16:00:00+08:00",
    "summary": {"red": 0, "yellow": 5, "green": 3, "skipped": 1},
    "findings": [
      {"id": "kb-index-orphan", "severity": "yellow", "category": "knowledge",
       "path": "knowledge/foo/bar.md", "message": "...", "fix": "..."}
    ]
  }
  ```
- **Markdown 报告**（`--report` 或默认）：分级区块 + 修复建议 + 总结

## 依赖降级矩阵

| 缺失产物 | 影响 |
|---|---|
| 标准目录（无 initializer） | 第 1 类跳过 + 提示 |
| PROGRESS.md 体系（无 tracker） | 第 2 类跳过 + 提示 |
| memory/（无约定落地） | 第 3 类跳过 |
| knowledge/data_structure.md（无 kb-retriever） | 第 4 类降级：只查命名/散文件/类型 + 提示建索引 |
| 无 | 第 5 类永远可用 |

## 脚本 CLI

```
python scan_workspace.py [--root PATH] [--json] [--report] [--days N] [--max-file MB]
```
- `--root`：工作区根（默认：脚本定位——优先参数，其次 cwd 向上找 WORKSPACE.md）
- `--json`：输出 JSON；`--report`：输出 Markdown（默认）
- `--days`：超龄阈值（默认 30）；`--max-file`：大文件阈值（默认 50）

## 发布计划（走 4 项目血泪 SOP）

1. GitHub：dtsola/xiaoyaoclaw-workspace-auditor（public/main/MIT/topics）
2. README 结构对齐姊妹项目（中英双语 + hero + 五件套互链）
3. SKILL.md：frontmatter description 块标量 `>`、英文在前中文在后、开头格式对齐
4. ClawHub publish（--source-repo + --source-commit 成对，dry-run 预览）
5. 全局技能同步（精简版：SKILL.md + scripts + templates，清理 .git）
6. 五件套 README 互链 + push
