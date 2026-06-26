# Changelog: S2-Universal-Space-Parser & SWM Engine

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), 
and this project adheres to Semantic Versioning.

## [2.0.1] - 2026-03-30 "The Symbiotic Awakening"

### 🚀 Major Pivot (核心战略升维)
* **S2-SWM (Space² Symbiotic World Model)**: 项目定位正式从“智能家居硬件BOM解析器”升维至“物理世界模型的数据收割引擎与交互沙盒”。标志着 S2 正式迈入通用人工智能 (AGI) 与具身智能的底层物理映射领域。

### ✨ Added (新增功能与架构)
* **MCP Server Integration (`s2_mcp_server.py`)**: 新增符合 Model Context Protocol (MCP) 规范的本地服务器。允许云端或本地大模型（如 Claude, Openclaw 等）直接作为 Agent 接入 S2 系统，执行物理动作并读取空间张量。
* **Chronos Memzero Harvester (`s2_chronos_memzero.py`)**: 新增世界模型专属的“时空全息记忆阵列”。可在 AI 触发物理执行时，自动截获并记录 $S_t \rightarrow A_t \rightarrow S_{t+1}$ 的因果状态流，并以 `.jsonl` 格式落盘，为 S2-SWM 提供第一性原理的训练语料。
* **Cyberpunk Frontend UI V2.0 (`frontend_ui/page.tsx`)**: 全新构建基于 Next.js/React 的赛博朋克风全息驾驶舱。新增 Chronos 数据流实时滚动的终端监视器面板，实现“数据炼金”过程的完全可视化。
* **Strategic Whitepaper (`S2-UHSP-Whitepaper-V1.0.md`)**: 发布《S2-SWM 智空共生世界模型白皮书 (V1.0)》，确立非视觉、反像素诅咒的第五大世界模型派系理论。
* **Sales & Design Manual (`S2_SPACE_ARCHITECT_MANUAL.md`)**: 新增面向空间设计师与技术型销售的实战话术与“满配穷举、做减法”的落地方案指南。
* **Agent Skill Registry (`skill.md`)**: 新增 Openclaw/Agent 标准技能注册卡片，明确 S2 生态的调用指令与规范。

### 🔄 Changed (重构与优化)
* **Unified Parser Engine (`s2_parser_engine.py`)**: 将分散的 5 大空间群组字典（共 62 个标准空间）彻底打通，主引擎现已支持对全量物理空间的六要素（光、气、声、电磁、能、视）张量解析。
* **Python Environment Standard**: 将底层运行环境基准要求提升至 Python 3.10+ (推荐 3.12+)，以完美适配本地边缘计算与高并发的异步 MCP 协议交互。

### 🛠️ Fixed (修复)
* 修复了前期模块解耦测试中，因跨目录调用导致的 `ModuleNotFoundError` 幽灵寻址报错，现已确立扁平化且标准化的项目根目录沙盒机制 (`.venv`)。

---

## [1.0.0] - 2026-03-xx "The SSSU Genesis"

### ✨ Added
* 初代 SSSU 空间标准单元法则落地，发布 `dict_01` 至 `dict_05` 系列硬件解析字典。
* 实现从“自然语义”向“无品牌绑定的底层物理逻辑”的降维解析功能。