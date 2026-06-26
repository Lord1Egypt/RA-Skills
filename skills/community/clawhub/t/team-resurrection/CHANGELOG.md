# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-04-22

### Added
- 分身复活核心功能：`clone.py` 扫描子代理session找接续点，创建新agent继承记忆继续工作
- `SKILL.md` — 完整使用说明与操作步骤
- `clone.py` — 核心克隆脚本，支持scan/simulate/show三种模式
- `pack.py` — 打包脚本

### 适用场景
- Main agent失联（gateway崩溃、网络中断）
- 任务执行到一半agent无响应
- 需要在多台机器上恢复同一个agent状态
