# skill-sharpener

对现有 Agent Skill 进行全面质量评估和综合优化的 Agent Skill。

## 功能

- **自动化结构扫描**：行数统计、frontmatter 合规检查、Windows 路径检测、嵌套引用检测
- **LLM 代码审查**：由 LLM 读取 `scripts/` 下的脚本，评估错误处理、魔法数字、函数文档等代码质量
- **5 维度综合评分**：元数据质量、结构合理性、内容质量、示例与模式、脚本质量
- **结构化报告**：输出高/中优先级问题、亮点、优化后的 description 建议
- **一键应用修复**：评估后可直接应用修复或重写 description

## 文件结构

```
skill-sharpener/
├── SKILL.md                    # 主技能文件，评估流程说明
├── README.md                   # 本文件
├── references/
│   └── checklist.md            # 5 维度详细评估清单（含评分标准和示例对比）
└── scripts/
    └── audit_skill.py          # 自动化结构分析脚本
```

## 快速使用

在对话时说：

- "帮我评估一下 `~/.xxx/skills/my-skill/`"
- "审查这个 skill 的质量"
- "这个 skill 的 description 有问题吗"
- "优化一下我的 skill"

skill-sharpener 会自动触发并执行完整的评估流程。

## 单独运行分析脚本

```bash
python scripts/audit_skill.py <skill目录路径>

# 示例
python scripts/audit_skill.py ~/.cursor/skills/my-skill/
python scripts/audit_skill.py E:/project/skills/skills/pdf/
```

脚本输出文件树、行数统计、frontmatter 检查、反模式告警，适合快速诊断。

## 评估维度

| 维度 | 权重 | 主要检查项 |
|------|------|------------|
| 元数据质量 | 25% | name 格式、description 是否第三人称、WHAT/WHEN 是否完整、触发词覆盖 |
| 结构合理性 | 20% | SKILL.md ≤500 行、渐进式披露、引用一级深 |
| 内容质量 | 25% | 不过度解释 LLM 已知内容、术语一致、无时间敏感信息 |
| 示例与模式 | 15% | 有具体输入/输出示例、复杂流程有步骤清单 |
| 脚本质量 | 15% | 错误处理、路径规范、魔法数字、docstring |

## 参考文档

[技能创作最佳实践 - Claude API Docs](https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/best-practices)

[如何写好一个 Skill：从创建到迭代的最佳实践 - 文档 - TRAE CN](https://docs.trae.cn/ide/best-practice-for-how-to-write-a-good-skill)
