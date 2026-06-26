# Triple-Layer Memory System

三层记忆系统 - 解决 AI Agent 长对话记忆丢失和上下文管理问题

## 特性

- ✅ **Session 自动压缩 + 自动切换**（150k 或 80% 上下文触发）
- ✅ **Session 交接机制**（防止记忆断层）
- ✅ **质量门控**（每条输出都打分，< 7 分拦截）
- ✅ **记忆写入时机优化**（关键时机立即写入）
- ✅ **跨 Session 记忆连续性**（智能加载）
- ✅ **记忆遗忘机制**（语义去重、高频升权、低权归档）
- ✅ **频道级记忆隔离**（Mem0 命名空间）

## 核心解决的问题

### 1. Session 切换时的记忆断层
**问题：** 旧 session 要满了，手动切换新 session，但旧 session 还没压缩，新 session 读不到旧 session 的内容。

**解决方案（四层防护）：**
- ① 主动压缩：检测到 `[NEW_SESSION]` 标记时，立即触发压缩
- ② 交接上下文：压缩后生成交接摘要，保存到 `memory/session_handoff.md`
- ③ 新 session 启动：优先读取交接上下文，获取旧 session 的关键信息
- ④ 实时记忆写入：完成关键任务时立即写入，不等 session 结束

### 2. 低质量输出污染记忆
**问题：** Agent 输出质量参差不齐，错误信息、无意义回复会污染记忆系统。

**解决方案：质量门控机制**
- 每条输出都经过质量评分（准确性、完整性、可读性、安全性）
- 分数 < 7：直接拦截，不输出
- 分数 7-8：输出但标记警告
- 分数 > 8：正常输出
- **宁可不做，也不做烂**

## 架构

```
Layer 3: Session 管理层（自动压缩、智能加载、交接机制）
    ↓
Layer 2: 文件层（索引/项目/经验/日志）
    ↓
Layer 1: Mem0（向量检索）
```

## 快速开始

### 安装

```bash
# 使用 clawhub 安装
clawhub install triple-layer-memory

# 或手动安装
cd ~/Desktop/openclaw-workspace/skills
git clone https://github.com/0range-x/triple-layer-memory.git
```

### 初始化

```bash
cd ~/Desktop/openclaw-workspace
bash skills/triple-layer-memory/scripts/init.sh
```

### 配置

1. 更新 `AGENTS.md` 添加 Session 启动流程
2. 更新 `HEARTBEAT.md` 添加 token 检查逻辑
3. 如果使用 Mem0，配置频道级命名空间隔离

详细文档：[SKILL.md](SKILL.md)

## 性能指标

- Session 寿命：~100k → ~150k tokens
- 记忆丢失率：~30% → ~5%
- 新 session 启动时间：~10s → ~3s
- 记忆检索准确率：~60% → ~85%

## 文件结构

```
workspace/
├── MEMORY.md                    # 核心索引
├── MEMORY_ARCHITECTURE.md       # 架构文档
├── memory/
│   ├── projects.md              # 项目状态追踪
│   ├── lessons.md               # 经验教训库
│   ├── YYYY-MM-DD.md           # 日志文件
│   ├── session_handoff.md      # Session 交接上下文
│   └── .archive/               # 归档目录
└── scripts/
    ├── session_compress.py      # Session 自动压缩
    ├── session_rotate.py        # 80%上下文触发会话轮换
    ├── session_handoff.py       # Session 交接脚本
    ├── quality_gate.py          # 质量门控脚本
    ├── auto_memory_write.py     # 自动记忆写入
    ├── memory_decay.py          # 记忆衰减和归档
    └── ...
```

## 新增功能（v2.0）

### Session 交接机制
防止 session 切换时的记忆断层：
```bash
# 压缩当前 session
python scripts/session_handoff.py compress

# 生成交接上下文
python scripts/session_handoff.py handoff [channel]
```

### 质量门控
评估输出质量，拦截低质量内容：
```python
from scripts.quality_gate import evaluate_output, should_block

score = evaluate_output(output_text)
if should_block(score, threshold=7.0):
    return "质量不达标，已拦截。"
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 作者

 ([小橘](https://x.com/maru_49940))

## 致谢

- [Mem0](https://github.com/mem0ai/mem0) - 向量检索框架
- [OpenClaw](https://openclaw.ai) - AI Agent 框架
