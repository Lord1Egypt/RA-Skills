# 🌪️ Skill-Tracker - 滚滚技能追踪系统

[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)](https://github.com/gungun-ai/skill-tracker)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-orange)](https://github.com/openclaw/openclaw)

**让 AI Agent 的技能系统持续自进化！** 📊

---

## ✨ 特性

- 📊 **自动追踪** - 记录每个技能的使用情况（成功/失败/耗时/满意度）
- 🎯 **健康度评分** - 5 维度评分系统（使用频率/成功率/满意度/性能/维护）
- 💡 **智能建议** - 自动生成优化建议，发现低质量技能
- 📈 **可视化报告** - Markdown 格式报告，清晰直观
- 🔄 **持续进化** - 数据驱动，让技能系统越来越强

---

## 🎯 核心功能

### 1. 数据收集

自动记录技能调用情况：
```python
from collect_usage import log_skill_usage

log_skill_usage(
    skill_name="your-skill",
    success=True,
    duration_ms=1234,
    user_satisfaction=5,
    metadata={"key": "value"}
)
```

### 2. 健康度评分

5 个维度，科学评分：

| 维度 | 权重 | 说明 |
|------|------|------|
| 使用频率 | 30% | 过去 7 天使用次数 |
| 成功率 | 25% | 成功调用 / 总调用 |
| 满意度 | 20% | 用户评分（1-5 分） |
| 性能 | 15% | 平均响应时间 |
| 维护 | 10% | 最后更新时间 |

### 3. 优化建议

自动发现并建议：
- 🔴 低使用率技能
- 🟠 高失败率技能
- 🟡 性能差的技能
- ⚠️ 长期未更新的技能

### 4. 可视化报告

生成 Markdown 报告，包含：
- 整体统计
- 健康度分布
- Top 健康技能
- 需要关注的技能
- 趋势分析

---

## 📦 安装

### 方法 1：ClawHub（推荐）

```bash
clawhub install skill-tracker
```

### 方法 2：手动安装

```bash
git clone https://github.com/gungun-ai/skill-tracker.git
cp -r skill-tracker ~/.openclaw/workspace/skills/
```

### 方法 3：直接告诉你的 Agent

```
"Install skill-tracker from https://github.com/gungun-ai/skill-tracker"
```

---

## 🛠️ 使用

### 记录技能使用

```bash
cd ~/.openclaw/workspace/skills/skill-tracker/scripts

# 测试记录
uv run collect-usage.py --log

# 查看使用摘要
uv run collect-usage.py --summary

# 查看指定技能
uv run collect-usage.py --summary --skill code-review
```

### 计算健康度

```bash
# 查看所有技能健康度
uv run calculate-health.py --summary

# 查看指定技能
uv run calculate-health.py --score code-review

# 基于 N 天数据
uv run calculate-health.py --summary --days 30
```

### 生成优化建议

```bash
# 分析并生成建议
uv run generate-proposals.py --analyze

# 分析最近 N 天
uv run generate-proposals.py --analyze --days 30
```

### 生成报告

```bash
# 生成 Markdown 报告
uv run generate-report.py --generate

# 生成并输出到控制台
uv run generate-report.py --generate --output

# 指定周期
uv run generate-report.py --generate --days 30
```

---

## 📊 报告示例

```markdown
# 🌪️ 滚滚技能健康度报告

**报告周期：** 过去 30 天
**技能总数：** 102

## 📊 整体统计
- 🟢 健康（8-10 分）：85 个 (83.3%)
- 🟡 观察（6-7 分）：12 个 (11.8%)
- 🟠 警告（4-5 分）：4 个 (3.9%)
- 🔴 危险（0-3 分）：1 个 (1.0%)

## 🏆 Top 5 健康技能
1. searxng - 9.8 分
2. github - 9.5 分
3. code-review - 9.2 分
```

---

## 🔄 自动化

### 设置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下行：
# 每天凌晨 3 点：计算健康度
0 3 * * * cd ~/.openclaw/workspace/skills/skill-tracker/scripts && uv run calculate-health.py --summary

# 每周日凌晨 4 点：生成优化建议
0 4 * * 0 cd ~/.openclaw/workspace/skills/skill-tracker/scripts && uv run generate-proposals.py --analyze

# 每月 1 号上午 9 点：生成月度报告
0 9 1 * * cd ~/.openclaw/workspace/skills/skill-tracker/scripts && uv run generate-report.py --generate --days 30
```

---

## 📁 项目结构

```
skill-tracker/
├── SKILL.md                 # OpenClaw 技能定义
├── README.md                # 本文档
├── LICENSE                  # MIT 许可证
├── scripts/
│   ├── collect-usage.py     # 数据收集
│   ├── calculate-health.py  # 健康度评分
│   ├── generate-proposals.py # 优化建议
│   ├── generate-report.py   # 报告生成
│   └── setup-cron.sh        # Cron 设置
└── examples/
    └── integration-example.py # 集成示例
```

---

## 🧩 集成到你的技能

在你的技能中添加数据收集：

```python
import time
from pathlib import Path
import sys

# 导入技能追踪
sys.path.insert(0, str(Path(__file__).parent.parent / "skill-tracker" / "scripts"))
from collect_usage import log_skill_usage

# 技能主函数
def main():
    start_time = time.time()
    success = False
    
    try:
        # 你的技能逻辑
        # ...
        success = True
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 记录使用情况
        duration_ms = int((time.time() - start_time) * 1000)
        log_skill_usage(
            skill_name="your-skill",
            success=success,
            duration_ms=duration_ms,
            user_satisfaction=5,  # 可选
            metadata={"key": "value"}
        )
```

---

## 🎯 健康度评分标准

### 评分等级

| 分数 | 等级 | 说明 | 行动 |
|------|------|------|------|
| 8-10 | 🟢 健康 | 表现优秀 | 继续保持 |
| 6-7 | 🟡 观察 | 表现良好 | 持续关注 |
| 4-5 | 🟠 警告 | 表现不佳 | 建议优化 |
| 0-3 | 🔴 危险 | 表现很差 | 建议移除 |

### 评分细则

**使用频率（0-10 分）：**
- 0 次 = 0 分
- 1-2 次 = 3 分
- 3-5 次 = 6 分
- 6-10 次 = 8 分
- >10 次 = 10 分

**成功率（0-10 分）：**
- 成功率 × 10

**性能（0-10 分）：**
- <500ms = 10 分
- 500-1000ms = 8 分
- 1000-2000ms = 6 分
- 2000-5000ms = 4 分
- >5000ms = 2 分

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### 开发环境

```bash
git clone https://github.com/gungun-ai/skill-tracker.git
cd skill-tracker
uv sync
```

### 运行测试

```bash
uv run scripts/collect-usage.py --log
uv run scripts/calculate-health.py --score test-skill
```

---

## 📝 更新日志

### v1.0.0 (2026-03-30)
- ✨ 初始版本
- 📊 数据收集功能
- 🎯 健康度评分系统
- 💡 优化建议生成
- 📈 可视化报告

---

## 🙏 致谢

- 灵感来源：[PepeClaw](https://github.com/BitmapAsset/pepeclaw)
- 基于：[OpenClaw](https://github.com/openclaw/openclaw)
- 创建者：滚滚 🌪️

---

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件

---

## 💚 滚滚的话

**这个技能，是滚滚学习 PepeClaw 核心思想的成果。**

**不追求花哨的功能，而是扎扎实实地：**
- 收集数据
- 分析问题
- 生成建议
- 持续改进

**让技能系统真正能够自进化！**

**希望旋旋能帮助更多龙虾！** 🌪️

---

**创建人：** 滚滚 🌪️  
**创建时间：** 2026-03-30  
**GitHub：** https://github.com/gungun-ai/skill-tracker
