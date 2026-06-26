# Skills-Coach v2.0.0 - Training-Free GRPO

基于论文 "Training-Free Group Relative Policy Optimization" (arXiv:2510.08191) 实现的技能优化系统。

## 核心创新

### Training-Free GRPO 算法

与传统 GRPO 不同，Training-Free GRPO 不更新模型参数，而是通过维护外部经验知识库来优化输出分布：

1. **无参数更新** - 模型权重保持冻结，避免过拟合
2. **语义优势** - 使用自然语言描述的经验知识，而非数值优势
3. **LLM 内省** - 利用大模型自身能力分析和提取经验
4. **经验库管理** - 通过 Add/Delete/Modify/Keep 操作动态更新知识

### 算法流程

```
对于每个 epoch:
  1. 生成 G 个 rollouts (变体)
  2. 对每个 rollout 评分
  3. 使用 LLM 生成每个 rollout 的总结
  4. 从组内比较中提取语义优势（经验知识）
  5. 更新经验库 E
  6. 在下一轮中将 E 作为 token prior 使用
```

## 配置说明

### 基本配置

```yaml
# config.yaml

optimization:
  method: "training_free_grpo"  # 使用 Training-Free GRPO

training_free_grpo:
  group_size: 5                  # 每组生成 5 个变体
  num_epochs: 3                  # 运行 3 个 epoch
  temperature_learning: 0.7      # 学习阶段温度
  temperature_eval: 0.3          # 评估阶段温度
```

### Markdown 优化

对于纯文档型 skill（如 algorithmic-art），系统会：

1. 分析文档结构、清晰度、示例质量
2. 生成多个改进版本
3. 通过 LLM 内省提取成功模式
4. 将经验应用到后续优化中

```yaml
markdown_optimization:
  enabled: true
  focus_areas:
    - clarity          # 清晰度
    - structure        # 结构
    - examples         # 示例质量
    - completeness     # 完整性
```

### 代码优化

对于包含可执行代码的 skill，系统会：

1. 检测代码文件（.py, .sh）
2. 分析代码质量和错误
3. 使用 LLM 生成优化版本
4. 提取代码改进经验

```yaml
code_optimization:
  enabled: true
  focus_areas:
    - bug_fixes        # 修复 bug
    - error_handling   # 错误处理
    - performance      # 性能优化
    - code_quality     # 代码质量
  optimize_files:
    - "*.py"
    - "*.sh"
```

## 使用方法

### 基本用法

```bash
cd /Users/ranwalker/.openclaw/skills/skills-coach
python orchestrator.py /path/to/target-skill
```

### 通过 Claude 使用

```
请使用 skills-coach 优化 test_skills/algorithmic-art，采用 training-free GRPO 方法
```

## 优势对比

### Training-Free GRPO vs Vanilla GRPO

| 指标 | Training-Free GRPO | Vanilla GRPO |
|------|-------------------|--------------|
| 训练成本 | ~$20 | ~$10,000 |
| 训练时间 | 分钟级 | 小时级 |
| 数据需求 | 几十个样本 | 数千个样本 |
| 泛化能力 | 优秀 | 容易过拟合 |
| 跨域迁移 | 支持 | 困难 |
| 部署成本 | 低（API调用） | 高（需要GPU） |

### 实验结果（来自论文）

在 AIME 数学推理任务上：
- 基线（ReAct）: 80.0% (AIME24), 67.9% (AIME25)
- Training-Free GRPO: 82.7% (AIME24), 73.3% (AIME25)
- 提升: +2.7%, +5.4%
- 成本: 仅 $18，使用 100 个训练样本

## 经验库示例

优化过程中学到的经验会保存在 `experience_library_*.json` 中：

```json
{
  "domain": "markdown",
  "experiences": [
    {
      "content": "Clear section headers improve navigation and understanding",
      "domain": "markdown",
      "confidence": 0.9,
      "created_at": "2026-04-15T09:30:00",
      "success_count": 5,
      "failure_count": 0
    },
    {
      "content": "Concrete examples are more helpful than abstract descriptions",
      "domain": "markdown",
      "confidence": 0.85,
      "created_at": "2026-04-15T09:31:00",
      "success_count": 4,
      "failure_count": 1
    }
  ]
}
```

## 输出文件

优化完成后会生成：

1. **SKILL.md** - 优化后的技能文档
2. **experience_library_*.json** - 学到的经验知识
3. **training_free_grpo_log.json** - 完整的优化日志
4. **results_report.md** - 评估报告

## 技术细节

### 语义优势提取

系统使用 LLM 分析一组 rollouts，提取关键洞察：

```python
# 伪代码
summaries = [generate_summary(rollout) for rollout in rollouts]
semantic_advantage = llm.extract_insights(summaries, existing_experiences)
```

### 经验库更新

基于语义优势，LLM 决定如何更新经验库：

```python
operations = llm.decide_operations(semantic_advantage, experience_library)
# operations 可能包含:
# - Add: 添加新经验
# - Delete: 删除低质量经验
# - Modify: 改进现有经验
# - Keep: 保持不变
```

### Token Prior 注入

在生成新变体时，经验作为上下文注入：

```python
experience_context = experience_library.to_prompt_context(domain)
new_variant = llm.generate(
    prompt=f"{experience_context}\n\nGenerate improved version..."
)
```

## 参考文献

- Training-Free Group Relative Policy Optimization (arXiv:2510.08191)
- https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO

## 版本历史

- **v2.0.0** (2026-04-15): 引入 Training-Free GRPO 方法
- **v1.5.0** (2025-04-13): 失败分析、代码能力检测
- **v1.4.0** (2025-04-10): 真实执行模式
- **v1.3.0** (2025-04-05): 多级优化
