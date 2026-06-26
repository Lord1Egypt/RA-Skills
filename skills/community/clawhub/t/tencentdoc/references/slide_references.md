# 幻灯片（Slide / PPT）参考文档

本文件包含腾讯文档 MCP 幻灯片相关工具的使用指南和注意事项。

---

## 概述

幻灯片通过 `create_slide` 工具创建，AI 自动根据用户描述和参考资料生成 PPT 内容。该接口为**异步接口**，需配合 `slide_progress` 工具轮询进度。

---

## 工具列表

| 工具名称 | 功能说明 |
|---------|---------|
| create_slide | 创建幻灯片（AI 自动生成内容，异步接口） |
| slide_progress | 查询幻灯片生成进度 |

---

## 工具详细说明

### 1. create_slide

#### 功能说明
根据用户描述和参考资料，由 AI 自动生成幻灯片内容并创建 PPT。

#### 调用示例

**示例1：根据主题生成 PPT**
```json
{
  "description": "生成一份主题为'2024年度销售总结'的PPT，要求包含业绩回顾、亮点项目、问题分析和来年规划四个章节"
}
```

**示例2：根据参考材料生成 PPT**
```json
{
  "reference_context": "第一季度销售额达到1200万，同比增长25%。主要增长来自华南区域，新客户占比40%。存在问题：北方市场渗透率不足，客单价偏低。",
  "description": "根据材料生成PPT，要求风格简洁专业，重点突出数据亮点"
}
```

#### 参数说明
- `description` (string, 必填): 用户对 PPT 的要求描述。样例1：【生成一份主题为xxx的PPT，要求xxxx】；样例2：【根据材料生成PPT，要求xxxx】
- `reference_context` (string, 可选): 生成 PPT 的参考资料，必须是 UTF-8 文本格式。**仅当用户明确指定需要根据某段内容/材料生成PPT时才传此参数，不要自由发挥填充内容**

#### 返回值说明
```json
{
  "session_id": "session_1234567890",
  "error": "",
  "trace_id": "trace_1234567890"
}
```

> ⚠️ **注意**：`create_slide` 为异步接口，返回 `session_id` 后需配合 `slide_progress` 工具轮询进度（每隔20秒轮询一次，最长等待20分钟），待状态为 `completed` 时从响应中获取 `file_url`。

### 2. slide_progress

#### 功能说明
查询幻灯片生成进度，与 `create_slide` 配合使用。调用 `create_slide` 获取 `session_id` 后，每隔 20 秒轮询一次，最长等待 20 分钟，直到状态为 `completed` 或 `failed`。

#### 状态说明
- `in_progress`：进行中，继续轮询
- `completed`：已完成，幻灯片已生成，从响应中获取 `file_url`
- `failed`：失败，停止轮询
- `canceled`：已取消，停止轮询
- `not_found`：未找到（`session_id` 不正确或已过期），停止轮询

#### 调用示例
```json
{
  "session_id": "session_1234567890"
}
```

#### 参数说明
- `session_id` (string, 必填): `create_slide` 返回的异步任务 session_id

#### 返回值说明
```json
{
  "status": "completed",
  "file_url": "https://docs.qq.com/slide/DV2h5cWJ0R1lQb0lH",
  "error": "",
  "trace_id": "trace_1234567890"
}
```

---

## 典型工作流

### 创建幻灯片

```
1. 调用 create_slide 传入 description（用户要求）和可选的 reference_context（参考资料）
2. 获取返回的 session_id
3. 使用 slide_progress 轮询进度（每隔 20 秒轮询一次，最长等待 20 分钟）
4. 待状态为 completed 时从响应中获取 file_url 并告知用户
```

### ⚠️ Agent 执行指引（重要）

#### 异步轮询任务：推荐使用 spawn 子会话

幻灯片生成通常需要 **10~15 分钟**，推荐使用 **spawn 子会话**专职轮询，主会话保持响应，避免阻塞用户交互。

#### ✅ 推荐做法：spawn 子会话轮询 + 主会话实时播报

**标准工作流：**

1. **主会话**：提交 `create_slide` 任务 → 立即告诉用户"已开始"
2. **spawn 子会话**：专职轮询
   - 每 20 秒检查一次
   - 每次检查生成状态给主会话
   - 超时自动清理，输出超时状态给主会话
3. **主会话**：接收子会话状态并格式化输出给用户
   - 进行中：`⏳ 正在生成中，第 N 次轮询，请稍候...`
   - 完成：`✅ 生成完成！PPT 链接：<file_url>`
   - 失败：`❌ 生成失败：<原因>`
   - 超时：`⚠️ 生成超时（已等待 20 分钟），请稍后重试`

#### ❌ 避免的做法

```bash
# ❌ 错误1：主会话直接 sleep 循环阻塞，用户无法交互
for i in 1..15; do
  mcporter call tencent-docs slide_progress ...
  sleep 20  # 阻塞主会话，用户体验差
done

# ❌ 错误2：后台进程静默等待，不向用户播报进度
# 用户看不到任何进度，体验如同宕机

# ❌ 错误3：子会话轮询完成后不通知主会话
# 用户在主会话中无法得知结果
```

---

## 注意事项

- `create_slide` 为异步接口，返回 `session_id` 后必须轮询
- 轮询间隔：每 20 秒一次
- 最长等待时间：20 分钟
- `reference_context` 仅在用户明确指定需要根据某段内容/材料生成 PPT 时才传
