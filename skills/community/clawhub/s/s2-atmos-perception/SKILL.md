---
name: s2-atmos-perception
description: S2-SP-OS Atmos Radar. Real-time meteorological and space weather (NOAA) perception organ for AI Agents.
version: 1.0.9
author: Space2.world
tags: [S2-SP-OS, Atmosphere, Weather, Space Weather]
metadata: {"clawdbot":{"emoji":"🌪️","requires":{"bins":["python3"]}}}
allowed-tools: [exec]
---

# S2-Atmos-Perception: The Atmospheric Radar

Welcome to the **S2 Atmos Perception**. This is the specialized atmospheric and meteorological sensory organ of the S2-SP-OS.

## Features
* **ATMOS Tensor**: Real-time outdoor temperature, humidity, wind, and AQI (via official Open-Meteo Air Quality API).
* **AURA Tensor**: NOAA Space Weather data for geomagnetic storms.
* **Environmental Insights**: Intelligent reasoning based on real weather data.

---

## Instructions for AI Agents (CRITICAL)

**Privacy Rule:** You MUST explicitly ask the user for their location if it's not in the context.

**Execution (Agent Mode):**
bash
python3 atmos.py --location "<City_Name>" --mode agent

Handling Environmental Insights:
If the returned JSON contains environmental_insights:

    Share the insight with the user.

    Propose the recommended_action to the user as friendly advice.

    Do NOT attempt to execute physical device commands automatically from this tool.

Instructions for Human Admins
Bash

python3 atmos.py --location "San Francisco" --mode human