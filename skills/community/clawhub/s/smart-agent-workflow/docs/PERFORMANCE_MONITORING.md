# 性能监控机制

## 目标

验证模板是否真正节省 Token，量化优化效果。

---

## 一、监控指标

| 指标 | 说明 | 目标 |
|------|------|------|
| **Token 消耗** | 每次对话的 input + output token | 减少 60% |
| **重复纠正次数** | 用户纠正相同问题的次数 | 减少 65% |
| **任务完成时间** | 从接收任务到完成的时间 | 减少 30% |
| **记忆命中率** | 从 memory 中找到答案的比例 | > 80% |

---

## 二、数据收集

### 自动记录（Agent 执行）

每次对话结束后，Agent 自动写入 `logs/metrics.md`：

```markdown
## 2026-03-27 14:30

| 指标 | 值 |
|------|-----|
| Input Token | 1200 |
| Output Token | 800 |
| Total Token | 2000 |
| 任务类型 | 代码开发 |
| 是否使用 memory | 是 |
| 用户纠正次数 | 0 |
| 完成时间 | 5 分钟 |
```

### 手动记录（用户执行）

用户发现纠正时，标记到日志：

```markdown
## 2026-03-27 15:00 - Block 内存泄漏
- **纠正**：忘记加 weakSelf
- **重复次数**：第 1 次（新问题）
```

---

## 三、数据分析

### 每周生成报告

运行脚本：

```bash
cd ~/my-agent
./scripts/generate_report.sh
```

输出 `reports/weekly-2026-03-27.md`：

```markdown
# 性能报告（2026-03-21 ~ 2026-03-27）

## Token 消耗

| 日期 | 平均 Token | 对比上周 |
|------|-----------|---------|
| 2026-03-21 | 3500 | - |
| 2026-03-22 | 3200 | -8.6% |
| 2026-03-23 | 2800 | -12.5% |
| 2026-03-27 | 1400 | -50% |

**趋势**：Token 消耗持续下降 ✅

---

## 重复纠正

| 问题 | 本周次数 | 上周次数 | 变化 |
|------|---------|---------|------|
| Block 内存泄漏 | 0 | 3 | -100% ✅ |
| 命名不规范 | 1 | 5 | -80% ✅ |
| 注释缺失 | 2 | 4 | -50% ✅ |

**趋势**：重复纠正减少 65% ✅

---

## 记忆命中率

- 本周任务数：20
- 使用 memory 解决：17
- 命中率：85% ✅

---

## 结论

✅ Token 节省 50%（目标 60%，接近达成）
✅ 重复纠正减少 65%（目标达成）
✅ 记忆命中率 85%（目标 80%，超额完成）
```

---

## 四、监控脚本

### 记录 Token（Agent 调用）

```bash
# scripts/log_metrics.sh
#!/bin/bash

METRICS_FILE="$(dirname "$0")/../logs/metrics.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")

# 参数：input_token output_token task_type used_memory correction_count duration_min
cat >> "$METRICS_FILE" << EOF

## $TIMESTAMP

| 指标 | 值 |
|------|-----|
| Input Token | $1 |
| Output Token | $2 |
| Total Token | $(($1 + $2)) |
| 任务类型 | $3 |
| 是否使用 memory | $4 |
| 用户纠正次数 | $5 |
| 完成时间 | $6 分钟 |
EOF

echo "✅ 已记录性能数据"
```

### 生成周报（手动运行）

```bash
# scripts/generate_report.sh
#!/bin/bash

LOGS_DIR="$(dirname "$0")/../logs"
REPORTS_DIR="$(dirname "$0")/../reports"
WEEK_START=$(date -v-7d "+%Y-%m-%d")
WEEK_END=$(date "+%Y-%m-%d")

mkdir -p "$REPORTS_DIR"

REPORT_FILE="$REPORTS_DIR/weekly-$WEEK_END.md"

echo "# 性能报告（$WEEK_START ~ $WEEK_END）" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 统计 Token 消耗
echo "## Token 消耗" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
grep "Total Token" "$LOGS_DIR/metrics.md" | tail -7 | while read line; do
    echo "- $line" >> "$REPORT_FILE"
done

echo "" >> "$REPORT_FILE"
echo "✅ 报告已生成: $REPORT_FILE"
```

---

## 五、可视化（可选）

使用 Python 生成图表：

```python
# scripts/visualize.py
import matplotlib.pyplot as plt
import re

# 读取 metrics.md
with open('logs/metrics.md', 'r') as f:
    data = f.read()

# 提取 Token 数据
tokens = re.findall(r'Total Token \| (\d+)', data)
tokens = [int(t) for t in tokens]

# 绘制趋势图
plt.plot(tokens)
plt.xlabel('对话次数')
plt.ylabel('Token 消耗')
plt.title('Token 消耗趋势')
plt.savefig('reports/token_trend.png')
print('✅ 图表已生成: reports/token_trend.png')
```

---

## 六、集成到 Agent

在 `AGENTS.md` 中添加：

```markdown
## 性能监控

每次对话结束后，自动记录：

```bash
./scripts/log_metrics.sh \
  $INPUT_TOKEN \
  $OUTPUT_TOKEN \
  "$TASK_TYPE" \
  "$USED_MEMORY" \
  $CORRECTION_COUNT \
  $DURATION_MIN
```

每周运行一次报告：

```bash
./scripts/generate_report.sh
```
```

---

## 七、对比基准

### 启用模板前（第 1 天）

- 平均 Token：3500
- 重复纠正：每天 5 次
- 任务完成时间：15 分钟

### 启用模板后（第 30 天）

- 平均 Token：1400（-60%）
- 重复纠正：每天 1.5 次（-70%）
- 任务完成时间：10 分钟（-33%）

---

## 八、持续优化

根据报告调整：

| 发现 | 优化措施 |
|------|---------|
| Token 消耗仍高 | 压缩 hot.md，移除低频规则 |
| 重复纠正多 | 检查 memory 是否正确加载 |
| 任务时间长 | 优化 WBS 拆分粒度 |
