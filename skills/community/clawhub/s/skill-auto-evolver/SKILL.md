---
name: auto-evolver
description: 自动分析和优化 Agent Skill 的工具 - 监控使用情况、评估健康度、生成改进建议
version: 0.1.0
author: OpenClaw
license: MIT
tags:
  - analysis
  - monitoring
  - optimization
  - cli
  - python
---

# Skill Evolver

自动分析和优化 OpenClaw Agent Skills 的 Python CLI 工具。

## 功能特性

- 📊 **使用监控**: 记录技能调用次数、成功率、响应时间
- 🏥 **健康度评估**: 基于可靠性、性能、代码质量、用户满意度的综合评分
- 🔍 **代码分析**: 检查 SKILL.md 完整性、Python 语法、代码质量问题
- 💡 **改进建议**: 基于规则自动生成优化建议
- 📈 **报告生成**: 支持 JSON、Markdown、HTML 格式导出

## 安装

```bash
# 使用 clawhub 安装
clawhub install skill-evolver

# 或手动安装
cd ~/.openclaw/skills/skill-evolver
pip install -r requirements.txt
```

## 依赖

- Python 3.8+
- SQLite3 (内置)
- PyYAML
- GitPython (可选，用于 Git 操作)

## 使用方法

### CLI 命令

```bash
# 初始化数据库
skill-evolver init

# 分析单个技能
skill-evolver analyze <skill-name>

# 分析所有技能
skill-evolver analyze --all

# 查看详细分析
skill-evolver analyze <skill-name> --verbose

# 生成健康度报告
skill-evolver report <skill-name>

# 生成所有技能报告
skill-evolver report --all

# 导出报告
skill-evolver report <skill-name> -o report.json -f json
skill-evolver report <skill-name> -o report.md -f markdown
skill-evolver report <skill-name> -o report.html -f html

# 查看健康度评分
skill-evolver health <skill-name>
skill-evolver health --all

# 记录技能使用
skill-evolver log <skill-name> <action> --status success --duration 100

# 添加用户反馈
skill-evolver feedback <skill-name> 5 --comment "很好用"

# 清理旧数据
skill-evolver clear --days 90

# 列出已记录的技能
skill-evolver log --list
```

### Python API

```python
from skill_evolver import SkillMonitor, SkillAnalyzer, SkillReporter

# 监控技能使用
monitor = SkillMonitor()

# 方式 1: 手动记录
monitor.log_usage(
    skill_name="my-skill",
    action="process",
    status="success",
    duration_ms=150
)

# 方式 2: 使用上下文管理器
with monitor.track("my-skill", "process") as tracker:
    result = do_something()
    tracker.set_context({"input_size": len(data)})

# 方式 3: 使用装饰器
@monitor.track_decorator("my-skill")
def my_function():
    pass

# 分析技能代码
analyzer = SkillAnalyzer()
result = analyzer.analyze_skill("my-skill")
print(f"评分：{result.score}/100")
print(f"问题：{len(result.issues)} 个")

# 生成报告
reporter = SkillReporter()
report = reporter.generate_health_report("my-skill")
print(f"健康度：{report['overall_score']}/100")
print(f"状态：{report['status']}")

# 导出报告
reporter.export_report(report, "report.html", format="html")
```

### 在 Skill 中集成

在你的 Skill 代码中集成监控：

```python
from skill_evolver.monitor import get_monitor

monitor = get_monitor()

def execute_skill_action(action, **kwargs):
    with monitor.track("my-skill", action) as tracker:
        tracker.set_context({"params": list(kwargs.keys())})
        # 执行实际逻辑
        result = do_work(**kwargs)
        return result
```

## 健康度评分说明

综合评分由以下维度加权计算：

| 维度 | 权重 | 说明 |
|------|------|------|
| 可靠性 | 30% | 基于成功率计算 |
| 性能 | 20% | 基于平均响应时间 |
| 代码质量 | 30% | 基于代码分析评分 |
| 用户满意度 | 20% | 基于用户反馈评分 |

### 状态等级

- 🟢 **healthy** (≥80): 技能运行良好
- 🟡 **warning** (60-79): 需要关注和改进
- 🔴 **critical** (<60): 存在严重问题

## 代码检查规则

### 严重问题 (Critical)

- 缺少 SKILL.md 文件
- SKILL.md YAML 格式错误
- Python 语法错误
- package.json JSON 格式错误

### 警告 (Warning)

- SKILL.md 缺少必需字段
- package.json 缺少必需字段
- 使用了 bare except
- 版本格式不正确

### 提示 (Info)

- 缺少代码示例
- 缺少测试目录
- 缺少 README
- 行过长 (>120 字符)
- 存在 TODO/FIXME 注释
- 使用了 print 语句

## 数据库结构

数据存储在 `~/.openclaw/skill-evolver/skill_evolver.db`

### 表结构

- `skill_usage`: 技能使用日志
- `health_score`: 健康度评分
- `feedback`: 用户反馈

## 输出示例

### 分析输出

```
✅ my-skill
   评分：85/100
   路径：~/.openclaw/skills/my-skill
   问题：2 个
      ℹ️ [content] SKILL.md 缺少代码示例
      ℹ️ [structure] 未找到测试目录
   建议：
      • 添加使用示例代码块
      • 创建 tests/ 目录并添加单元测试
```

### 健康度报告

```
🟢 my-skill 健康度报告
   总体评分：85/100
   状态：healthy

   详细评分:
      可靠性：90/100
      性能：80/100
      代码质量：85/100
      用户满意度：85/100

   使用情况 (过去 30 天):
      总调用：150
      成功率：92.0%
      平均耗时：120ms

   改进建议:
      1. 添加使用示例代码块
      2. 创建 tests/ 目录
```

## 开发

### 运行测试

```bash
cd ~/.openclaw/skills/skill-evolver
python -m pytest tests/ -v
```

### 目录结构

```
skill-evolver/
├── SKILL.md              # 技能说明
├── package.json          # 包元数据
├── README.md             # 项目说明
├── skill_evolver/        # 主模块
│   ├── __init__.py
│   ├── monitor.py        # 使用监控
│   ├── analyzer.py       # 代码分析
│   ├── reporter.py       # 报告生成
│   └── cli.py            # CLI 入口
├── database/
│   ├── __init__.py
│   └── models.py         # 数据模型
└── tests/
    ├── __init__.py
    ├── test_database.py
    ├── test_analyzer.py
    ├── test_reporter.py
    └── test_cli.py
```

## 常见问题

### Q: 如何查看某个技能的详细使用情况？

```bash
skill-evolver analyze my-skill --verbose
```

### Q: 如何导出所有技能的对比报告？

```bash
skill-evolver report --all -o all-skills.json
```

### Q: 如何清理历史数据？

```bash
skill-evolver clear --days 30  # 保留最近 30 天
```

### Q: 数据存储在何处？

默认存储在 `~/.openclaw/skill-evolver/skill_evolver.db`

## 许可证

MIT License
