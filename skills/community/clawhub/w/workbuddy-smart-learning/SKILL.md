# WorkBuddy 智能学习系统 (Smart Learning System)

## 概述

WorkBuddy 的自我进化引擎，基于「感知-学习-行动」SEA 循环实现持续优化。整合六大模块，形成完整的反馈闭环。

---

## 系统架构

```
反馈收集 ←→ 隐式信号 ←→ 任务画像
     ↓              ↓           ↓
  知识蒸馏 ←→ 自适应阈值 ←→ 模式识别
                  ↓
            实时警报（触发→固化）
                  ↓
            模板执行（命中→执行→对比）
```

### 模块说明

| 模块 | 文件 | 核心功能 |
|------|------|---------|
| 反馈收集 | `feedback.py` | 显式反馈（👍/👎/✏️）+ 自动归类 |
| 隐式信号 | `signal_collector.py` | 5类行为信号无感采集 |
| 任务画像 | `task_profiler.py` | 执行轨迹追踪 + 复杂度分析 |
| 模式识别 | `pattern_recognizer.py` | 高频模式扫描 + 自适应警报 |
| 知识蒸馏 | `knowledge_distiller.py` | 自适应阈值 + 模板匹配 + 避坑规则 |
| 主入口 | `learn.py` | 整合六大模块，CLI 命令行 |

### 数据存储

```
.workbuddy/memory/
├── feedback/           # 反馈记录 (JSON)
├── signals/           # 隐式信号数据 (JSON)
├── task_profiles/     # 任务执行轨迹 (JSON)
├── patterns/          # 模式识别结果 + 阈值状态
│   └── threshold_state.json  # 自适应阈值状态
└── templates/         # 蒸馏模板 + 避坑规则
    └── failed_patterns/avoid_*.yaml
```

---

## 核心模块详解

### 1. 反馈收集 (feedback.py)

**FeedbackCollector**：
- `record_feedback(task_id, rating, tags, note)` - 记录单条反馈
- `get_recent_feedback(days)` - 获取近期反馈
- `generate_feedback_prompt()` - 生成反馈询问文本

**反馈类型**：good / bad / neutral
**标签**：用户自定义，如 `文件整理`、`数据分析`、`报告生成`

### 2. 隐式信号采集 (signal_collector.py)

**SignalCollector** - 5类信号无感采集：

| 信号 | 计算方式 | 学习意义 |
|------|---------|---------|
| 反馈填写率 | 有反馈任务/总任务 | 参与度代理 |
| 任务取消率 | 主动中断/总任务 | 方案不适配 |
| 平均任务时长 | 所有任务耗时均值 | 执行效率 |
| 工具成功率 | 成功调用/总调用 | 工具质量 |
| 重复修正率 | 重复执行/总任务 | 模式固化价值 |

**健康评分**（0-100）：基于5类信号综合计算

### 3. 任务画像 (task_profiler.py)

**TaskProfile** - 单任务轨迹：
- `start_task(task_id, summary)` - 开始
- `use_template(template_id, name)` - 标记使用模板
- `record_tool_call(tool, success, duration)` - 记录工具调用
- `end_task(outcome, success)` - 结束

**TaskProfilerAnalyzer** - 分析器：
- `get_complexity_distribution(days)` - 简单/中等/复杂 分布
- `compare_template_vs_free(days)` - 有模板 vs 自由执行 对比
- `get_tool_usage_stats(days)` - Top10 高频工具

### 4. 模式识别 + 警报 (pattern_recognizer.py)

**评分公式**：
```
score = (freq/max_freq) * 50 + (recency/max_recency) * 20 + stability * 30
```
≥60分 = 高价值模式，建议沉淀

**自适应阈值引擎 (AdaptiveThresholds)**：
- 基于历史警报准确率自动调节阈值
- 准确率 > 70% → 敏感模式（降阈值 15%）
- 准确率 < 40% → 保守模式（升阈值 30%）
- 状态持久化：`threshold_state.json`

**三级警报**：

| 等级 | 类型 | 条件 | 响应 |
|------|------|------|------|
| URGENT | 突发 | ≥ urgent阈值（默认75） | 立即通知 |
| TREND | 趋势 | 环比增长 > 150% 且 ≥ trend阈值 | 本周关注 |
| STABLE | 稳定 | 长期高频且 ≥ high阈值 | 建议模板化 |

### 5. 知识蒸馏 (knowledge_distiller.py)

**自适应蒸馏阈值**：
```
effective_threshold = base / feedback_rate
```
填写率高 → 低阈值（频繁蒸馏）；填写率低 → 高阈值（避免误触发）

**模板匹配**：
- `match_template(user_request)` - Jaccard 相似度关键词匹配
- `generate_match_suggestion(user_request)` - 生成推荐文本
- 置信度 ≥ 50% → 直接推荐；≥ 20% → 参考提示

**避坑规则**：
- 负面反馈 → `avoid_*.yaml` 避坑规则
- 自动推断应避免的操作 + 修复建议

---

## 命令行使用

```bash
cd .workbuddy/skills/workbuddy-smart-learning

python learn.py full        # 完整学习周期（6阶段综合报告）
python learn.py patterns     # 模式识别
python learn.py feedback    # 记录反馈
python learn.py distill     # 知识蒸馏
python learn.py signals     # 隐式信号报告
python learn.py alerts      # 实时警报检查
python learn.py profiler    # 任务画像分析
python learn.py match "关键词"  # 模板关键词匹配
```

### full 命令输出结构

```
## 1. 反馈摘要     - 近7天反馈数、填写率
## 2. 模式识别     - 近30天高价值模式、Top3高频任务
## 3. 实时警报     - URGENT/TREND/STABLE 三级警报
## 4. 知识蒸馏     - 自适应阈值状态、自动蒸馏触发结果
## 5. 模板对比     - 有模板 vs 自由执行 成功率/耗时对比
```

---

## 与主对话流程集成

### 任务完成后 → 反馈询问
```
反馈：[👍/👎/✏️]
标签：任务类型（可选）
备注：改进建议（可选）
```
调用 `python learn.py feedback` 记录

### 新会话启动时 → 模式检查
检测到涉及历史上下文时：
1. 读取 MEMORY.md + 近期每日记忆
2. 检查 ≥60分的高频模式
3. 主动提示用户是否需要优化

### 警报处理 → 阈值学习
- 用户确认警报有效 → `record_alert_confirmed(task)`
- 用户判定为误报 → `record_alert_rejected(task)`

---

## 阈值配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 模式评分阈值 | 60 | ≥60分触发沉淀建议 |
| 蒸馏基础阈值 | 5 | 正面反馈达到此数触发蒸馏 |
| 警报-突发 | 75 | 立即通知 |
| 警报-关注 | 70 | 本周关注 |
| 警报-趋势 | 60 | 周报标记 |
| 趋势增幅 | 150% | 环比超过此值触发趋势警报 |

---

## 版本历史

- **2026-04-14**：基础版 - 反馈收集 + 模式识别 + 知识蒸馏
- **2026-04-17 v1**：第一轮 - 隐式信号 + 自动蒸馏触发 + 实时警报
- **2026-04-17 v2**：第二轮 - 任务画像 + 模板匹配 + 自适应阈值引擎
