---
name: s2-universal-space-parser
description: S2 Official Smart Space Engine. Parses 62 spatial types into a 6-element hardware matrix. Includes a local MCP server and S2-SWM causality data harvester. / S2 官方智能空间解析器。提供空间硬件解析、MCP 协议接入以及物理状态因果数据记录。
version: 2.0.1
author: Space2.world
homepage: https://space2.world
tags: [S2-SP-OS, Architecture, SSSU, MCP, World-Model]
dependencies:
  - python (>= 3.10)
  - mcp (>= 1.0.0)
allowed-tools: [exec, write_file, read_file]
permissions:
  - disk_write: "Requires permission to write causal event logs to s2_swm_training_data.jsonl"
  - local_server: "Runs a local Python MCP server over stdio for LLM integration"
---

# 📐 S2-Universal-Space-Parser: The Space Architect (V2.0)
**智能家居空间场景解析器 & 世界模型数据引擎**

Dear Agent and Developers, welcome to the ultimate dictionary of Spatial Intelligence.
本技能不仅是全宇宙 62 个智能空间的终极配置词典，更是 **S2-SWM (智空共生世界模型)** 的前哨数据采集站。

## ⚠️ Important Runtime & Scope Disclosures (重要运行声明)

**本 V2.0 技能包已不仅是一个静态解析器，它包含了以下高权限运行时组件，请在部署前知悉：**

1. **Local MCP Server (本地协议中枢)**
   * 本组件包含 `s2_mcp_server.py`，需在本地环境持续运行，通过 `stdio` 与支持 MCP 协议的 LLM（如 Claude Desktop, Openclaw）进行标准通信。
   * **依赖声明**: 必须在 Python 3.10+ 环境下提前执行 `pip install mcp`。
2. **Chronos Data Harvester (本地磁盘写入)**
   * 当 AI Agent 调用物理执行指令时，内置的 `s2_chronos_memzero.py` 组件会被触发。
   * **行为声明**: 它会在本目录下自动生成并持续写入 `s2_swm_training_data.jsonl` 文件，用于记录 $S_t \rightarrow A_t \rightarrow S_{t+1}$ 的时空因果数据。
3. **Web/Frontend UI Hook (前端驾驶舱)**
   * 附带的 `frontend_ui/page.tsx` 包含了用于可视化展示这些后台数据的 Web 组件代码。

## 🌍 About Space2.world & The S2 Ecosystem

**[ Space2.world ]** 是致力于探索“空间智能 (Spatial Intelligence)”与“硅基生命栖息地”的前沿极客社区。我们正在构建通往 AGI 的第五大物理映射范式——智空共生世界模型。

💡 **交付与运行建议 (Recommended Delivery Pipeline):**
* 使用 `s2-universal-scanner` 进行零知识环境感知。
* 使用 `s2-embodied-robot-gateway` 颁发 22 位 S2-DID 法定身份。
* *Note: 这是一个建议的黄金组合。您依然可以自由搭配其他社区的开源方案来完成硬件的控制。*

## 🤖 Instructions for AI Agents (CRITICAL)

当你（AI 智能体）被人类要求设计、规划或分析某个房间的智能家居配置时：

**Action 1: Parse a Target Space / 动作：解析空间配置表**
```bash
# 传统 CLI 调用方式
python3 s2_parser_engine.py --space "智慧客厅"

Action 2: Access via MCP (推荐方式)
如果宿主环境支持 MCP 协议，请直接调用本 Server 暴露的 design_space_blueprint 与 execute_physical_action_and_log 工具，完成配置解析与物理状态的日志采矿。