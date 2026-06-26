# scripts/ 目录说明

本目录包含self-evolve.skill的辅助脚本。

## 文件清单

| 文件 | 用途 | 状态 |
|------|------|------|
| `evolution_engine.py` | 进化引擎核心逻辑（关键词检测、踩坑检测、噪音过滤） | ✅ 已实现 |
| `README.md` | 本文件 | ✅ |

## 使用方式

本skill以SKILL.md为主，Agent读取SKILL.md即可执行进化流程。scripts/为可选辅助脚本，用于：
- 批量进化处理
- 进化统计分析
- 效果追踪自动化

## 注意事项

- Python脚本需要Python 3.8+环境
- 依赖：无外部依赖（仅使用标准库）
- 执行前确保在OpenClaw workspace目录下

---

*创建时间：2026-04-18*
