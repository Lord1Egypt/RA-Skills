# QA Reviewer - 质量保证技能

## 简介

基于 SRM 项目 24 小时实战经验，提供完整的质量保证能力。

## 核心经验

1. **清晰的角色分工** - 开发不测试，测试不开发
2. **快速反馈循环** - 发现问题→报告→修复→验证 < 1 小时

## 目录结构

```
qa-reviewer/
├── SKILL.md              # 技能说明
├── README.md             # 本文件
├── templates/            # 报告模板
│   ├── test_report.md
│   ├── code_review.md
│   └── todo_tracker.md
├── scripts/              # 自动化脚本
│   ├── run_tests.sh
│   ├── code_review.sh
│   └── generate_report.sh
├── examples/             # 使用示例
│   └── test_case_example.cpp
└── docs/                 # 详细文档
    ├── workflow.md
    ├── checklist.md
    └── best_practices.md
```

## 快速开始

```bash
# 克隆项目
cd /path/to/project

# 运行代码审查
~/.openclaw/extensions/qa-reviewer/scripts/code_review.sh

# 生成测试报告
cp ~/.openclaw/extensions/qa-reviewer/templates/test_report.md ./
vim ./TEST_REPORT.md
```

## 使用示例

详见 `examples/` 目录

## 更多文档

- [技能说明](SKILL.md)
- [工作流程](docs/workflow.md)
- [检查清单](docs/checklist.md)
- [最佳实践](docs/best_practices.md)

---

*创建时间：2026-03-04*  
*版本：1.0.0*
