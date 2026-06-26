# 🗄️ S2-Chronos-Memzero: The Holographic Memory Matrix
# 时空全息记忆阵列 (S2 记忆零节点)
*v1.0.1 | Bilingual Edition (English / 中文)*

Welcome to Phase 5 of the **S2-Spatial-Primitive OS**. A true intelligent system needs more than just reactive capabilities; it needs **Causality Memory (因果记忆)**. 
欢迎来到 S2 操作系统的第五阶段。一个真正的智能系统需要的不仅是响应能力，更需要**因果记忆**。

---

### 🛡️ Core Principle 1: The 1-Minute Life-Safety Baseline (1分钟生命安全底线)
We discard the industry standard of logging meaningless sensor noise every millisecond. S2 anchors its timeline granularity precisely at **1 Minute**. 
我们抛弃了行业内每毫秒记录无意义传感器噪音的做法。S2 将时间线颗粒度精确锚定为**1 分钟**。
* **The Rationale**: Extensively modeled against edge-case critical failures (e.g., HVAC failure in extreme heat, oxygen supply malfunction). A 1-minute blind spot does not result in irreversible biological trauma to human occupants. / 经过极端故障模型推演（如制冷或维生供氧失效），1 分钟的监控盲区不会对碳基生物造成不可逆的致命伤害。
* This filters out massive data noise while guaranteeing we capture every critical timeline turning point. 

### 🗜️ Core Principle 2: Backward-Persistence & Delta Compression (逆向持存与差值压缩)
Respecting the homogeneity of our 4m² Da Xiang Standard Units, S2 storage acts as an ultra-efficient Time-Series Database (TSDB):
尊重 4㎡ 标准空间的均一性，S2 存储系统作为极高效率的时序数据库运行：
* **Backward Persistence (逆向持存)**: A state recorded at `15:02:18` signifies that the space maintained this exact, homogeneous state spanning backwards from `15:01:19` to `15:02:18`.
* **Delta-State Compression (差值折叠压缩)**: If a room remains unchanged for 8 hours while you sleep, the system **WILL NOT** log redundant data every minute. The DB engine detects zero-variance and triggers a fold, logging *only* the timestamps and values of actual state changes (deltas).

---

### 📊 The 4-Dimensional Causality Schema / 四维因果数据表
This SKILL automatically builds an `s2_chronos.db` containing four perfectly aligned tables based on Project/Object/Time:
本技能自动构建四张数据表，在项目、对象、时间上实现严格对齐：
1. **Environment Timeline**: 1-minute delta-compressed physical reality (Light, HVAC, Sound, Energy).
2. **Agent Decisions**: The exact execution log and the *semantic LLM rationale* of the Core Agent.
3. **Avatar Mandates**: The translated legal strategy authorized by your Embodied Digital Avatar.
4. **External Pointers**: **S2 DOES NOT STORE RAW VIDEO.** It creates timestamped "pointers" (e.g., `EZVIZ_CAM_REF`) to query 3rd-party cameras securely, protecting the 4m² privacy boundary.

### 🚀 Execution Simulation
Run this script to witness the TSDB Delta Compression in real-time. The console will demonstrate how redundant states are folded, and how causal events break the compression loop!
运行本脚本，实时见证时序差值压缩。控制台将向您展示冗余状态是如何被折叠的，以及因果律事件是如何打破压缩循环并精准记录的！