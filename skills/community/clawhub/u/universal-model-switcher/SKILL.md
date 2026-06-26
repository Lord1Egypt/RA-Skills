---
name: universal-model-switcher
description: Universal Model Switcher V7.1.0 - Only switch within your existing models.
version: 7.1.1
author: davidme6
---

# Universal Model Switcher V7.1.1

## Core Principle

Only switch within models you already have. No cost concerns.

## Switch Rules

### 1. Multimodal First
- Image/Video/Audio -> qwen3.5-plus

### 2. Task-based Switch
- Code -> glm-5
- Reasoning -> qwen3-max  
- Chat -> qwen3.5-plus (best all-rounder)
- Long Doc -> qwen3.5-plus (256K)
- Office -> MiniMax-M2.5

### 3. Subagent Keep Professional
- Tech Expert -> glm-5
- Reasoning Expert -> qwq-plus
- Market Hunter -> qwen3-max

## Your Model Pool

| Task | Best | Backup |
|------|------|--------|
| Code | glm-5 | qwen3-coder-plus |
| Reasoning | qwen3-max | qwen3.5-397b-a17b |
| Multimodal | qwen3.5-plus | - |
| Chat | qwen3.5-plus | - |
| Office | MiniMax-M2.5 | - |

Version: 7.1.0