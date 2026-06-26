# Skills Monitor

> AI Skills 一站式监控评估平台

## 快速安装

```bash
# 通过 SkillsHUB 安装
skills install skills-monitor

# 或手动安装
pip install -r requirements.txt
```

## 使用方式

### 作为 Skill 调用

```python
from main import run

# 初始化
result = run("init")

# 查看状态
result = run("status")

# 7因子评估
result = run("evaluate", skill_slug="your-skill")

# 智能推荐
result = run("recommend", top_n=5)

# 诊断报告
result = run("diagnose", send=True)
```

### 命令行使用

```bash
python main.py init
python main.py status
python main.py evaluate --skill your-skill
python main.py recommend
python main.py diagnose --send
```

## 完整文档

参见 [SKILL.md](./SKILL.md)

## 许可证

GPL-3.0
