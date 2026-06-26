# skill-evolve-pro — 技能进化引擎

> **版本**：Phase 1 + Phase 2  
> **框架**：基于 ReflACT 6步循环 + SkillOpt  
> **目标**：通过"失败轨迹 → 反思 → 编辑 → 验证"让 AI 技能自动进化

---

## 功能概述

- 对指定技能执行完整的 6 步进化循环
- 从失败轨迹中提取改进信号，生成原子编辑 patch
- 应用并验证编辑，最终输出进化后的技能版本
- 支持 SESSION-STATE.md 自动解析失败轨迹

---

## 安装说明

### 前提条件

- Python 3.10+
- DeepSeek API Key

### 安装步骤

1. 通过 ClawHub 安装此技能
2. 在 `scripts/config_template.py` 基础上创建 `scripts/config.py`
3. 填写你的 DeepSeek API Key 和路径配置

---

## 配置说明

### 1. 创建配置文件

```bash
# 在 scripts/ 目录下
cp config_template.py config.py
```

### 2. 填写配置（config.py）

```python
# DeepSeek API 配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
# 如果环境变量未设置，直接在下方填写（不推荐上传到公开仓库）：
# DEEPSEEK_API_KEY = "sk-your-key-here"

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

# Python 路径
PYTHON_PATH = "/usr/bin/python3"  # Linux/Mac
# PYTHON_PATH = "C:\\Users\\YourName\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"  # Windows

# 工作区路径（OpenClaw 工作区根目录）
WORKSPACE = Path.home() / ".jvs" / "workspace"

# 目标技能目录（要被进化的技能）
DEFAULT_TARGET_SKILL_DIR = WORKSPACE / "skills" / "robot-evolve"
```

### 3. 设置环境变量（推荐）

```bash
# Linux/Mac
export DEEPSEEK_API_KEY="sk-your-key-here"
export OPENCLAW_WORKSPACE="$HOME/.jvs/workspace"

# Windows (PowerShell)
$env:DEEPSEEK_API_KEY="sk-your-key-here"
$env:OPENCLAW_WORKSPACE="$HOME\.jvs\workspace"
```

---

## 使用说明

### 触发方式

在 OpenClaw 中对用户说：

| 触发话术 | 说明 |
|---------|------|
| 「进化一下 XXX skill」 | 对指定技能执行完整6步 |
| 「优化这个技能」 | 同上 |
| 「让技能自动进化」 | 同上 |
| 「执行 skill-evolve」 | 同上 |

### 手动运行

```bash
cd scripts/
python run_evolve.py
```

### 查看状态

```bash
cd scripts/
python -c "from state_manager import load_state; print(load_state('robot-evolve'))"
```

---

## 核心流程（6步循环）

```
① Rollout   → 采集轨迹
② Reflect   → 错误分析，生成编辑建议
③ Aggregate → 聚类合并，去重
④ Select    → 重要性排序，编辑预算裁剪
⑤ Update    → 应用原子编辑（append/insert_after/replace/delete）
⑥ Meta-Reflect → 验证门控，评估是否改善
⑦ Slow Update → 跨 epoch 纵向优化（保护区写入）
```

---

## 文件结构

```
skill-evolve-pro/
├── SKILL.md                  # 技能定义文档
├── README.md                 # 本文件
├── scripts/
│   ├── config_template.py    # 配置模板（上传 ClawHub）
│   ├── config.py             # 用户配置（不上传，请加入 .gitignore）
│   ├── evolve_core.py        # 核心进化引擎（Phase 1）
│   ├── rollout_result.py     # RolloutResult 数据类
│   ├── trajectory_loader.py   # 轨迹加载器（Phase 1+2）
│   ├── session_state_parser.py # SESSION-STATE.md 解析器
│   ├── skill_reflect.py      # Phase 3：反思生成
│   ├── skill_apply.py        # Phase 4：原子操作
│   ├── skill_gate.py         # Phase 5：验证门控
│   ├── skill_scheduler.py    # Phase 6：调度器
│   ├── slow_update.py        # Phase 7：跨 epoch 慢更新
│   ├── state_manager.py      # 状态管理
│   ├── run_evolve.py        # 快速启动入口
│   ├── test_phase2.py        # Phase 2 测试
│   └── test_slow_update.py   # Slow Update 测试
└── state/                    # 状态文件（自动生成）
    └── <skill_id>.json
```

---

## 保护区说明

`SKILL.md` 中的 `<!-- SLOW_UPDATE_START -->` 和 `<!-- SLOW_UPDATE_END -->` 标记的区域为**慢更新保护区**，不受常规编辑影响，仅在 Slow Update 阶段由 optimizer 改写。

---

## 故障排除

### "DEEPSEEK_API_KEY 未设置"

- 检查环境变量是否设置：`echo $DEEPSEEK_API_KEY`
- 或在 `config.py` 中直接填写 API Key

### "状态文件不存在"

- 运行一次初始化：`python -c "from state_manager import init_state; init_state('robot-evolve', '1.0.0')"`

### 进化无效果

- 确认 `temp/rollouts/` 目录下有失败轨迹文件
- 检查 SESSION-STATE.md 格式是否正确

---

*最后更新：2026-06-03*

