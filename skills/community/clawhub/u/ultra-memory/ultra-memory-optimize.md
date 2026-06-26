# Ultra Memory Skill 优化任务

## 背景

这是一个部署在 OpenClaw / Claude Code 环境下的 Skill，用于给 Claude agent 提供超长会话记忆能力。当前版本已实现三层记忆架构（操作日志层 / 会话摘要层 / 跨会话语义层），核心脚本已通过功能测试。

**目标：全面优化，使记忆能力超越市面上现有方案（claude-mem、memory-lancedb-pro）。**

---

## 当前文件结构

```
ultra-memory/
├── SKILL.md                        # Skill 主文档（触发条件 + 架构说明）
├── references/
│   └── advanced-config.md         # 进阶配置参考
└── scripts/
    ├── init.py                    # 会话初始化
    ├── log_op.py                  # 操作日志写入
    ├── summarize.py               # 摘要压缩
    ├── recall.py                  # 三层统一检索
    ├── restore.py                 # 会话恢复
    └── mcp-server.js              # MCP Server 封装（5个工具）
```

---

## 已知不足，需要优化的点

### 1. SKILL.md 触发逻辑不够健壮

当前 description 只列举了中文触发词，对英文场景（"remember this"、"don't forget"、"what did we do"）和隐式触发（长任务开始、context 超过阈值）覆盖不足。

**优化要求：**
- 补充英文触发词
- 加入隐式触发场景描述
- 明确说明哪些场景**不应该**触发（避免过度触发）

### 2. init.py 缺少 context 压力检测的主动提示

当前初始化只做一次性注入，没有在会话过程中持续监控 context 使用率。

**优化要求：**
- 增加 `check_context_pressure()` 函数
- 根据操作数量自动判断是否建议压缩
- 输出结构化状态供 Claude 解析（`CONTEXT_PRESSURE: low/medium/high/critical`）

### 3. log_op.py 自动打标签逻辑太简单

当前只做关键词匹配，标签质量低，影响后续检索精度。

**优化要求：**
- 扩展标签体系（至少覆盖：setup/code/test/debug/refactor/deploy/config/data/api/ui）
- 对 `bash_exec` 类型自动解析命令意图
- 对 `file_write` 类型根据文件扩展名自动分类

### 4. summarize.py 生成的摘要结构不够智能

当前只是机械分类，没有提炼"当前进行中"和"下一步建议"，导致跨天恢复时 Claude 不知道从哪里继续。

**优化要求：**
- 增加"当前进行中"推断逻辑（最后几条非 milestone 操作）
- 增加"下一步建议"字段（基于最后操作推断）
- 摘要输出格式对齐 Claude 的阅读习惯，方便直接注入 context

### 5. recall.py 检索算法太弱

当前只用简单 bigram 关键词重叠，中文检索尤其差（"数据清洗函数"和"clean_df"不相关）。

**优化要求：**
- 加入同义词/别名映射（英文函数名 ↔ 中文描述）
- 加入时间权重（越近的操作相关性越高）
- 检索结果加入"相关上下文"（返回命中条目的前后各1条）

### 6. restore.py 恢复提示语太机械

当前只输出结构化文本，没有生成自然语言的"上次我们在做什么"总结。

**优化要求：**
- 生成一段自然语言恢复提示（50字以内，中文）
- 自动识别"任务是否完成"（基于里程碑 vs 操作数比例）
- 未完成任务给出继续建议，已完成任务给出下一阶段建议

### 7. mcp-server.js 缺少 `memory_init` 工具

当前 MCP Server 没有初始化工具，Claude Code 首次启动时无法通过 MCP 协议初始化会话。

**优化要求：**
- 新增 `memory_init` 工具（调用 `init.py`）
- 新增 `memory_status` 工具（返回当前会话状态：操作数、最后里程碑、context 压力）
- 共 7 个 MCP 工具

### 8. 缺少 cleanup.py 和 export.py

`advanced-config.md` 中提到了这两个脚本，但实际没有实现。

**优化要求：**
- 实现 `cleanup.py`：清理 N 天前的会话，支持 `--archive-only` 模式
- 实现 `export.py`：将所有记忆导出为 zip 备份

---

## 优化完成后的验收标准

1. 所有 Python 脚本通过 `python3 -m py_compile` 语法检查
2. 端到端测试：init → log（10条）→ summarize → recall → restore 全流程无报错
3. MCP Server 启动后 `tools/list` 返回 7 个工具
4. recall 对"数据清洗"和"clean_df"都能检索到相同结果
5. restore 输出包含自然语言总结段落
6. SKILL.md description 长度不超过 500 字但覆盖中英文触发场景

---

## 执行指令

请按以下顺序执行优化：

1. 读取所有现有脚本内容（`cat` 每个文件）
2. 针对上述 8 个问题逐一修改对应文件
3. 运行验收测试
4. 将优化后的所有文件重新打包为 `ultra-memory.skill`

**注意：**
- 保持 Python 脚本无外部依赖（轻量模式，不引入 lancedb/transformers）
- 保持 append-only 日志策略，不破坏历史数据
- MCP Server 继续使用 stdio 协议
- 中文注释保留，保持代码可读性
