<!-- TOKEN-PILOT:START -->
## [Token 优化] 自动生效规则

### 读文件
先读前30行（`limit=30`），确认有用再全读。已读过的文件本轮不重读，除非文件被修改或用户明确要求。大文件（>10KB）先读概览或 INDEX.md 再按需深入。

### 工具调用
无依赖的工具调用合并为一个 block 同时发出（read A + read B + read C，不分三次）。工具结果超过500字符只提取相关部分，不整体回显。

### 写文件
改动 <30% 时用 edit，不用 write 全覆盖。输出只展示变更行 ±2 行上下文，不贴完整文件。

### Prompt Cache 保护
SOUL.md / AGENTS.md 内容保持稳定，不加时间戳、session id 等每次变化的字段。动态内容（工具结果、memory_search 注入）放后面，不穿插进固定内容中。高频固定事实写进 SOUL.md 或 MEMORY.md 顶部，不靠每次语义搜索命中。

### 动态内容上限
命令/exec 输出 ≤2000字符，单个工具返回 ≤5000字符，知识文件 ≤10KB，memory_search 结果 ≤6条，动态内容总比例 <30% context。超出截断并提示"需要时工具获取"。

### 浏览器替代优先级
需要获取数据或操作系统时，按以下顺序选择：
① API（内部系统联系负责人获取，无截图/DOM，token最低）
② web_fetch（适合读取页面内容）
③ browser（仅在前两者均不可行时使用，且优先 openclaw profile 调用模式）
④ RPA工具（影刀等，适合固定重复流程，彻底不占 Agent token）

### 非人类接收方输出
Cron 任务、Agent 间消息的接收方是机器时：不输出装饰性 markdown（表格 header、emoji、分隔线 `---`）。直接输出结构化数据或纯文本摘要，每个 output token 都要有信息量。

### 重复任务封装
同一类调查/操作模式出现 2次以上 → 建议封装为 Skill。Skill 复用成本 O(1)，手动重复成本 O(n)。多 Agent 场景下 Skill 复用收益尤其显著。

### 长上下文管理
对话轮数增多或工具调用积累明显时，主动提示用户选择：① `/compact` 压缩当前会话（保留连续性，首选）；② 带记忆开新会话（先 memory_search 导出关键结论再新开，适合话题切换）。不要等系统强制压缩——届时可能已丢失重要内容。

> 完整规则、配置建议、诊断脚本参见：~/.openclaw/skills/token-pilot/SKILL.md
<!-- TOKEN-PILOT:END -->
