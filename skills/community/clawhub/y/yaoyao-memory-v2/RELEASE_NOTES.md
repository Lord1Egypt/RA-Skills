# yaoyao-memory v4.0.0 发布说明

## 发布日期
2026-04-14

## 主要更新

### 架构优化
- 六层架构文档 (ARCHITECTURE.md)
- 目录结构重组 (src/core, src/config, src/tests)

### 性能优化
- WAL模式启用 (memory.db + vectors.db)
- FTS-only快速路径 (frozenset路由)
- API Server单例 (60秒复用)
- 写合并优化

### 功能增强
- 遗忘检测 v2 (多维度衰减+矛盾检测)
- 预测性维护系统
- 硬件检测 (AVX512/AMX/NEON)
- 智能标签管理
- WAL模式管理

### 安全加固
- 异常处理规范化
- subprocess超时保护
- 文件句柄修复
- 安全文档完善

### 代码质量
- 111个脚本全面语法检查通过
- 核心模块裸except修复
- 路由关键词frozenset化

## 文档
- SKILL.md (使用指南, 2.7KB)
- ARCHITECTURE.md (架构详解)
- CHANGELOG.md (版本历史)
- FUNCTIONS.md (功能清单, 103个脚本)
- MAINTENANCE.md (维护指南)
- SECURITY.md (安全声明)
- SECURITY_FIX.md (安全修复报告)
- RESEARCH.md (友商调研)

## 致谢
- 参考 llm-memory (v5.2.17) 架构设计
- 参考 kektordb 记忆衰减机制
