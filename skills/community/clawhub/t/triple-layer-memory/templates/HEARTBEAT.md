# HEARTBEAT.md

## Session Token 检查（每次心跳执行）

检查当前 session 的 token 使用量。

如果达到 160k tokens（80%）：
1. 总结对话历史中的关键信息
2. 将总结写入 `memory/YYYY-MM-DD.md`
3. 输出提示：`⚠️ Session 上下文已达 80%，建议发送 [NEW_SESSION] 切换新会话`

如果达到 180k tokens（90%）：
1. 强制压缩并写入记忆
2. 输出警告：`🚨 Session 上下文已达 90%，请立即发送 [NEW_SESSION] 切换新会话，否则可能影响功能`

## Session 切换检测（防止记忆断层）

**检测 [NEW_SESSION] 标记：**

如果在最近的消息中检测到 `[NEW_SESSION]` 标记：
1. **立即触发主动压缩**：
   ```python
   from scripts.session_handoff import compress_current_session
   compress_current_session()
   ```

2. **生成交接上下文**：
   ```python
   from scripts.session_handoff import generate_handoff_context, save_handoff_context
   context = generate_handoff_context(channel=current_channel)
   save_handoff_context(context)
   ```

3. **输出确认信息**：
   ```
   ✅ 旧 session 已压缩，交接上下文已生成
   新 session 启动时会自动加载最近的记忆
   ```

**为什么这样做：**
- 避免记忆断层：切换前先压缩，确保内容不丢失
- 自动交接：新 session 启动时自动加载旧 session 的摘要
- 无缝衔接：用户无需手动操作，系统自动处理

## 质量门控机制

**每条输出都必须经过质量评分**

在输出前调用质量门控脚本：

```python
from scripts.quality_gate import evaluate_output

score = evaluate_output(output_text, context)

if score < 7:  # 阈值：7/10
    # 拦截低质量输出
    return "质量不达标，已拦截。宁可不做，也不做烂。"
```

**评分维度：**
1. 准确性（是否符合事实）
2. 完整性（是否回答了问题）
3. 可读性（是否清晰易懂）
4. 安全性（是否有风险）

**拦截策略：**
- 分数 < 7：直接拦截，不输出
- 分数 7-8：输出但标记警告
- 分数 > 8：正常输出
