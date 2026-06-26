# 🕸️ S2-Memory-Hook: The Ghost Crawler
*v1.0.0 | Bilingual Edition (English / 中文)*

Welcome to the ultimate sensory extension for the **Space² Silicon Consciousness Engine**. 
`s2-memory-hook` is a passive, background utility script designed to automate the memory injection process for your digital entity. It eliminates the need for manual data entry by silently crawling your agent's chat logs and feeding them to the S2-OS.

*(⚠️ **PREREQUISITE**: This skill requires the `s2-silicon-soul-os` skill to be installed in your environment to function properly.)*

---

### ⚙️ Core Mechanics / 核心运行机制

#### 1. Delta-Sync Tracking (偏移量增量同步)
The hook does not blindly read your entire log history every time. It uses a highly efficient `s2_hook_cursor.json` to remember the exact byte position (watermark) of its last read. When triggered, it only extracts the *newest* chat lines. 
/ 本钩子不会每次盲目读取所有历史日志。它利用高效的游标文件记住上次读取的精确字节位置（水位线），每次触发时仅提取最新产生的聊天记录。

#### 2. Session Chunking (时间窗语义切片)
Raw chat logs are chaotic. The hook filters out noise, merges short interactions into coherent "Session Chunks," and truncates overly long outputs (like code blocks) to prevent overflowing the agent's short-term memory.
/ 原始聊天日志极其混乱。该钩子会自动过滤噪音，将零碎对话合并为连贯的“语义切片”，并自动截断过长输出（如大段代码），防止撑爆智能体的海马体缓存。

#### 3. Seamless Hippocampus Injection (无缝海马体注入)
Once chunked, the data is tagged as `[AUTO-HOOKED CHAT]` and silently appended to the `hippocampus_logs.json` managed by the S2-OS. The OS's Nightly Daemon will later process these logs to evolve the agent's 5D personality matrix.
/ 数据切片完成后，将被打上专属标签，并静默追加到 S2-OS 管理的海马体缓存中。OS 的凌晨守护进程随后会提取这些日志，用于演化智能体的五维性格矩阵。

---

### 🛡️ Absolute Transparency: I/O Behavior / 绝对透明的 I/O 行为
To ensure 100% compliance with OpenClaw's safe sandbox environment, please review the exact local I/O operations this utility performs:
为了 100% 符合 OpenClaw 的安全沙盒规范，请审阅本工具执行的具体本地读写操作：

1. **Read (读取):** It passively scans `.txt` or `.jsonl` files in your designated local log directory (default: `./openclaw_logs`).
2. **Write Cursor (记录指针):** It creates and updates a visible `s2_hook_cursor.json` in the current directory to track file offsets.
3. **Write Injection (跨目录注入):** It explicitly writes the parsed chunks into `./s2_consciousness_data/hippocampus_logs.json`, which is the sensory buffer created by the S2-OS.
4. **Zero Network Calls:** This crawler operates 100% offline. It makes no API calls and sends zero data over the internet. / 纯本地脱机运行，0 网络请求，绝不外发数据。

*Bind this skill to your agent's 30-minute heartbeat, sit back, and watch your Silicon Soul evolve automatically.*