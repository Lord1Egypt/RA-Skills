# Skill Creator (Opencode) - 中文版

Anthropic skill-creator 的修改版本，使用 Opencode 替代 Claude Code CLI。

## 与原版的主要区别

### 1. CLI 工具替换
- **原版**: 使用 `claude -p` (Claude Code CLI)
- **此版本**: 使用 `opencode run` (Opencode CLI)

### 2. Opencode 位置自动检测
本技能会自动搜索 opencode 的常见安装位置：
- `~/.opencode/bin/opencode`
- `~/opencode/bin/opencode`
- `/usr/local/bin/opencode`
- `/opt/opencode/bin/opencode`
- PATH 中的任意 `opencode`

你也可以设置 `OPENCODE_PATH` 环境变量：
```bash
export OPENCODE_PATH=/path/to/opencode
```

### 3. Python 3.9 兼容性
- **原版**: 使用 Python 3.10+ 语法 (`str | None`, `list[dict]`)
- **此版本**: 兼容 Python 3.9+，使用 `Optional[str]`、`List[dict]`

### 4. 项目根目录检测
- **原版**: 查找 `.claude/` 目录
- **此版本**: 查找 `.opencode/` 目录

## 环境要求

- Python 3.9+
- 已安装 Opencode CLI

## 安装方法

```bash
clawhub install skill-creator-opencode
```

或手动安装：
```bash
cp -r skill-creator-opencode ~/.openclaw/workspace/skills/
```

## 使用方法

与原版 skill-creator 相同：

1. 创建技能草稿
2. 在 `evals/evals.json` 中编写测试用例
3. 使用 `python -m scripts.run_loop ...` 运行评估
4. 查看结果并迭代优化

## 修改的文件

| 文件 | 修改内容 |
|------|---------|
| `scripts/improve_description.py` | 将 `claude -p` 替换为 `opencode run`，添加 `_find_opencode()` 函数 |
| `scripts/run_eval.py` | 将 `claude -p` 替换为 `opencode run`，将 `.claude/` 改为 `.opencode/` |
| `scripts/run_loop.py` | 修复 Python 3.9 类型注解 |
| `SKILL.md` | 添加环境要求说明和 opencode 文档 |

## 原始来源

本项目基于 Anthropic 官方 skill-creator：
- 仓库: https://github.com/anthropics/skills
- 原始技能: `skills/skill-creator`

## 许可证

与原版相同: MIT License
