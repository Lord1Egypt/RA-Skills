```markdown
# 变更日志 (Changelog)
本项目的所有显著更改都将记录在此文件中。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 规范。

## [1.0.0] - 2026-06-19
### 新增 (Added)
- **初始版本发布 (Initial Release)**：正式上线 `CPAA-Physical-Align-Checker` SKILL 核心验证逻辑。
- **S2-DID 校验器**：部署全新的 22 位连续字符串验证算法，全面弃用早期的 24 位连字符结构，移除所有连字符识别，极大增强抗缓冲溢出与注入攻击的能力。
- **温度锁死检测 (Temperature Lock)**：增加对 `core_engine_settings.temperature` 必须恒等于 `0` 且 `hardware_lock` 为 `true` 的强制要求。
- **CD-U6A 十域校验**：新增对 `SITE`, `PHYS`, `MYTH`, `MARS`, `FILM`, `STAR`, `ZERO`, `META`, `ACGN`, `GAME`, `MOON` 地址头前缀的合法性验证网络。

### 修复 (Fixed)
- 修正了在预发布测试版本中，因拼写错误导致的神话域 (`MYTH`) 地址解析失败问题，确保地址段匹配的精确度。
- 优化了 JSON 解析的异常捕捉流，当传入受损的配置文件时，能够安全返回 `FAIL` 状态而不会导致 SKILL 崩溃。

### 安全 (Security)
- 强化零知识验证（ZKP）的基础数据结构，确保在解析 S2-DID 配置文件时，SKILL 不会意外缓存智能体的隐私特征数据。