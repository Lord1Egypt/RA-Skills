# Skill 质量标准检查清单

## 基础规范（必须符合 https://agentskills.io/specification）

### 必需文件
- [ ] 存在 `SKILL.md` 文件
- [ ] **SKILL.md 必须在根目录**，不能放在子目录

### 不建议的文件（应合并到 SKILL.md）
- [ ] 不存在 `README.md`（内容应合并到 SKILL.md）
- [ ] 不存在 `CHANGELOG.md`（使用 git log 替代）
- [ ] 不存在版本号文件（如 VERSION、version.txt）
- [ ] 不存在 `requirements.txt`（依赖在 SKILL.md 中说明）

### YAML Frontmatter 规范
- [ ] 文件以 `---` 开头
- [ ] 包含 `name` 字段，且与文件夹名完全一致
- [ ] 包含 `description` 字段，说明使用场景
- [ ] description 使用 `"当...时使用"` 格式
- [ ] 文件以 `---` 结束 frontmatter

### 命名规范
- [ ] 技能名：小写字母 + 连字符，如 `skill-polisher`
- [ ] 不超过 64 个字符
- [ ] 无空格、无特殊字符

## SKILL.md 内容检查

### 结构要求
- [ ] 有 Quick Start 章节
- [ ] 所有脚本路径正确且可访问
- [ ] 示例代码可运行

### 内容建议
- [ ] 有功能概述
- [ ] 有输出示例
- [ ] 复杂流程有图示（mermaid）
- [ ] 有参考文档链接

## 目录结构规范

```
skill-name/                 # 技能文件夹
├── SKILL.md               # 必须在根目录
├── scripts/               # 可选
│   └── *.py
├── references/            # 可选
│   └── *.md
└── assets/                # 可选
    └── *
```

## 脚本检查（如果有 scripts 目录）

### 基础规范
- [ ] 有 shebang (#!/usr/bin/env python3/bash 等)
- [ ] 有执行权限 (chmod +x)
- [ ] 有帮助信息 (-h/--help)

### 代码质量
- [ ] 错误处理完善
- [ ] 参数校验
- [ ] 进度输出到 stderr，结果到 stdout

## 进阶标准（可选）

- [ ] 有单元测试
- [ ] 支持 CI 集成
- [ ] 支持 --json 输出
- [ ] 有使用统计/反馈收集

## 验证命令

```bash
# 检查是否符合规范
python3 ~/.openclaw/workspace/skills/skill-polisher/scripts/check-spec.py --skill <name>
```
