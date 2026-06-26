# Examples Reference

## 示例 1: 路径分叉 — 配色选择

**上下文**: A版文章当前是珊瑚色，与B版暗红色视觉雷同。可以选择换淡雅绿、换暖金、或保持珊瑚色微调。

```yaml
# 输入
stage_goal: "A版排版配色与B版形成视觉区分"
current_gap: "珊瑚色与暗红色在手机屏幕上对比度不足"
available_actions: anchor, search, synthesize, degrade_continue
```

```yaml
# 输出
next_action: degrade_continue
reason: "换淡雅绿方案可行且区分度高，直接执行"
```

---

## 示例 2: 高代价动作前 — 发布前校验

**上下文**: 准备发布到微信公众号，发现标题显示为文件名而非文章标题。

```yaml
# 输入
stage_goal: "A版文章完整发布到草稿箱"
current_gap: "publisher不识别HTML标题，会用文件名作为标题"
available_actions: anchor, clean, degrade_continue
```

```yaml
# 输出
next_action: degrade_continue
reason: "发布后用户可在草稿箱手动改标题，不阻塞发布"
```

---

## 示例 3: 连续无增益 — 排版修改循环

**上下文**: 已换了两版配色（森林绿→珊瑚色），用户仍反馈雷同。

```yaml
# 输入
stage_goal: "排版配色用户确认通过"
current_gap: "两版修改后用户仍不满意，已消耗3次迭代"
available_actions: anchor, time_bind, clean, synthesize, degrade_continue
```

```yaml
# 输出
next_action: time_bind
reason: "迭代已3次未通过，绑定上限再2轮"
```

---

## 示例 4: 信息缺失 — 搜索决策

**上下文**: 要写AI行业分析，但缺少2025年Q4的模型发布数据。

```yaml
# 输入
stage_goal: "完成AI行业分析的数据支撑"
current_gap: "缺少2025年Q4前沿模型发布数量和间隔数据"
available_actions: search, synthesize, degrade_continue
```

```yaml
# 输出
next_action: search
reason: "关键数据点缺失，定向搜索一次"
```

> **注意**: 如果下一轮裁决时搜索结果仍不足以填补缺口，必须选 `degrade_continue` 而非再次 `search`。

---

## 反面示例 — 不应触发的场景

**场景**: 按SOP顺序执行 02→04→03→05 调度链路。

```
# 这是既定流程，不是分叉、不是高代价、不是停滞
# → 不触发 self-governor，直接执行
```

**场景**: 用户说"发布"。

```
# 这是明确的单一路径指令
# → 不触发（除非发布前检测到异常）
```
