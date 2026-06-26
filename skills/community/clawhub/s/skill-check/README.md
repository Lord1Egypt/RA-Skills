# Skill Check - 技能审查器

分析技能目录结构，识别改进点，输出优化建议和执行方案。

## 功能特点

- 🔍 结构性审查（渐进式披露、脚本沉淀、资源归位）
- 🧠 逻辑性审查（漏洞、重复、冲突、断层）
- 🤖 Agent 兼容性审查（工具绑定、API 依赖、路径耦合）
- 📊 自动分析报告（结构化输出问题清单）
- 🔁 循环审查修复（review-loop.py 自动迭代）

## 使用场景

触发词："优化技能"、"审查技能"、"检查技能规范"

## 工作流程

结构分析 → 问题识别 → 逻辑审查 → 输出报告

## 执行命令

```bash
# 单次审查
python3 scripts/analyze.py <skill-dir>

# 循环审查-修复
python3 scripts/review-loop.py <skill-dir>
```

## 目录结构

```
skill-check/
├── SKILL.md                          # 核心工作流
├── manifest.json                     # 技能元数据
├── README.md                         # 本文件
├── scripts/
│   ├── analyze.py                   # 结构分析脚本
│   ├── fix.py                       # 自动修复脚本
│   └── review-loop.py               # 循环审查脚本
└── references/
    └── structure-patterns.md        # 结构优化模式
```

## 审查维度

### 结构性（脚本检测）
- SKILL.md < 500 行
- 固定行为脚本化
- 资源文件归位
- 参考文档分离

### 逻辑性（LLM 分析）
- 逻辑漏洞、重复、冲突、断层
- 执行可行性、确定性
- 工作流完整性

### Agent 兼容性
- 无工具名硬编码
- 无特定 API 依赖
- 无路径耦合

## 问题优先级

| 优先级 | 定义 | 示例 |
|--------|------|------|
| P0 | 阻塞性问题 | 缺少 frontmatter、脚本无法执行 |
| P1 | 结构问题 | SKILL.md 过长、资源位置错误 |
| P2 | 优化建议 | 缺少错误处理、命名不规范 |

## 参考资料

- 结构优化模式 → [references/structure-patterns.md](references/structure-patterns.md)