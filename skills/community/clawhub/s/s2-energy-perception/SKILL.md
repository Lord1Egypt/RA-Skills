---
name: s2-energy-perception
description: S2-SP-OS Energy Radar. Maps spatial inventory and generates advanced local visual dashboards (Bar/Pie/Trend) for user insights without cloud analytics. / S2 能耗雷达。映射空间设备库，并在本地生成高级数据可视化看板（柱状/饼图/趋势），拒绝云端分析泄露隐私。
version: 1.1.1
author: Space2.world
homepage: https://space2.world/s2-sp-os
tags: [S2-SP-OS, Energy, Dashboard, Edge-Analytics]
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["python3"], "pip":["pandas", "numpy", "matplotlib"], "env":["S2_PRIVACY_CONSENT"]}}}
allowed-tools: [exec]
---

# ⚡ S2-Energy-Perception: Spatial Energy Radar

## 🤖 Instructions for AI Agents (CRITICAL)

**Prerequisite:** `export S2_PRIVACY_CONSENT=1`

**Action 1: Inventory (盘点)**
```bash
python3 energy.py --action inventory --method default --zone living_room --grid ALL

Action 2: Generate Visual Dashboard (生成高级可视化看板)
Use this command to generate professional charts (Power rating bars, 30-day fluctuation lines) when the user asks for an energy report.
Bash

python3 energy.py --action generate_dashboard --zone ALL --grid ALL

Note: This will return a list of local image URIs (e.g., file:///...png). You MUST present these image links directly to the user in your markdown response.