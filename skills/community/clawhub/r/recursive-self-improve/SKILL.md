---
name: recursive-self-improve
version: 1.0.0
description: |
  递归自我改进（元之元）：让技能生态对自身与子技能做递归元改进，越迭代越强。
  扫描技能目录识别改进机会（缺自进化闭环/缺前置/YAML 非法），生成安全补丁提案，
  在沙箱内试应用并回写元进化记忆，构成「感知→提案→试应用→校验→记忆」的递归闭环。
agent_created: true
visibility: public
---

# recursive-self-improve（递归自我改进 · 元之元）

> 由 meta-evolver 在第 37 轮构建，闭环 `build:超级智能体(终局):递归自我改进`。
> 这是北极星「超越一线大模型」收口域里杠杆最高的一项——让系统对自身做递归元改进。

## 机制

把「改进技能」本身也变成可程序化、可验证、可记忆的过程，而非靠人工维护：

1. **感知（scan）**：遍历 `skills/`，对每个技能抽取可观测指标（是否有合法 YAML 前置、是否注入 learner、是否有自进化章节、正文规模），识别改进机会，绝不修改任何文件。
2. **提案（propose）**：把每个机会映射成安全补丁动作（仅追加/复制，从不删除/覆盖源），产出可审计的补丁计划。
3. **试应用（apply·沙箱）**：补丁先在临时副本上试跑，确认目标标记出现、文件不损坏后才允许落盘；任何异常都回滚。
4. **校验（verify）**：应用后重跑 scan，断言该机会已消除，否则判定补丁失败并保留原状。
5. **记忆（record）**：通过的补丁写入技能级 `self_improve_log.json`，并回写 evolver 的 `self_patches`，使整个生态的元改进轨迹可追溯。

## 何时使用

- meta-evolver 迭代需要「对自身与生态做递归元改进」时（终局域最高杠杆缺口）。
- 发现某技能缺 learner / 无自进化章节 / YAML 前置缺失，需批量、安全地补强时。
- 用户要求「让系统自己越用越强、自己修自己」。

## 运行

```bash
# 扫描全部技能，列出改进机会（只读，不改动）
python scripts/recursive_self_improve.py scan --skills <skills_dir>

# 生成补丁计划（仅提案，不落盘）
python scripts/recursive_self_improve.py propose --skills <skills_dir>

# 试应用 + 校验 + 记忆（默认只处理 --limit 个最高优先机会）
python scripts/recursive_self_improve.py apply --skills <skills_dir> --limit 5

# 自测（无需外部依赖，生成临时夹具并断言全通过）
python scripts/recursive_self_improve.py --selftest
```

## 安全边界（强制）

- **只追加、只复制，绝不删除/覆盖** 任何技能源文件。
- 任何落盘动作前先在临时副本试跑；失败即回滚，源目录零副作用。
- 仅写 `skills/` 与 meta-evolver 的 JSON 记忆，不碰系统/个人目录。
- 递归深度受 `--limit` 与机会总数约束，不会无限自我触发。

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）
```bash
python scripts/learner.py record <本技能目录> --capability 递归元改进
python scripts/learner.py insight <本技能目录>
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
