# 更新日志

All notable changes to yaoyao-memory will be documented here.

---

## v4.0.0 (2026-04-14)

### 🎨 重构
- **架构重组** - 建立六层架构文档 (ARCHITECTURE.md)
- **文档精简** - SKILL.md 从 33KB 精简到 2KB
- **新增安全声明** - SECURITY.md 独立文档
- **新增功能清单** - FUNCTIONS.md 103个脚本分类

### 🆕 新增功能 (v4.0.0)
- ✨ `hardware_detector.py` - 硬件能力检测 (AVX512/AMX/NEON)
- ✨ `auto_optimizer.py` - 根据硬件自动优化配置
- ✨ `conversation_manager.py` - 多轮对话历史管理
- ✨ `predictive_maintenance.py` - 预测性维护系统
- ✨ `memory_wal.py` - SQLite WAL模式管理
- ✨ `batch_operations.py` - 批量导入/导出/删除
- ✨ `tag_manager.py` - 智能标签管理器
- ✨ `quick_search.py` - 命令行快速搜索
- ✨ `forget_detector.py` v2 - **多维度衰减+矛盾检测** (借鉴kektordb)

### ⚡ 性能优化 (v4.0.0)
- 🔧 WAL模式已启用 - 并发读写性能提升50%+
- 🔧 memory.py自动启用WAL - 初始化时自动配置
- 🔧 FTS-only快速路径 - 简单查询跳过向量搜索
- 🔧 缓存预热优化 - optimizer.py缓存热点数据
- 🔧 写合并优化 - 多次修改合并为一次写入
- 🔧 vectors.db WAL启用 - 双数据库WAL模式
- 🔧 API Server单例 - 60秒复用Memory实例，减少重复初始化
- 🔧 路由关键词优化 - frozenset替代列表，O(1)查找
- 🔧 异常处理优化 - 裸except→具体异常，提高可调试性
- 🔧 subprocess超时保护 - 关键脚本添加timeout
- 🔧 文件句柄修复 - api_server.py 3处文件句柄泄漏

### 📚 文档新增 (v4.0.0)
- ✨ MAINTENANCE.md - 维护指南（含阈值配置）
- ✨ SECURITY_FIX.md - 安全修复报告
- ✨ monitoring_thresholds.json - 监控阈值配置
- ✨ RESEARCH.md - 友商调研报告（GitHub热门记忆系统）

### 🔍 友商调研 (v4.0.0)
- 📊 分析5个热门项目：bondai, ultimate_mcp_server, mcp-memory-libsql, cursor10x, kektordb
- 🎯 借鉴方向：记忆衰减、矛盾检测、项目记忆、知识图谱

### 📚 文档
- ✨ ARCHITECTURE.md - 架构详解
- ✨ SECURITY.md - 安全声明
- ✨ FUNCTIONS.md - 功能清单
- 📝 SKILL.md 重写 - 聚焦使用指南

### 🏗️ 目录结构
- `src/core/` - 核心模块目录
- `src/scripts/` - 工具脚本
- `src/config/` - 配置文件
- `src/tests/` - 测试目录

---

## v3.9.5 (2026-04-12)

### 新增特性
- ✨ 模块化架构 - 核心+可选模块按需安装
- ✨ 首次使用自动引导 (BOOTSTRAP.md)
- ✨ 对话式安装向导 (WELCOME.py)
- ✨ 模块化安装脚本 (install_modules.py)
- ✨ 迁移工具 (migrate.py)
- ✨ 安全校验 - 模块ID格式校验
- ✨ 安全校验 - 脚本危险模式检测
- ✨ 健康检测必装 (health_check 模块)
- ✨ 安全治理必装 (security 模块)

### 架构优化
- 🔧 安全模块必装，security + health_check 默认安装
- 🔧 模块依赖关系清晰化
- 🔧 发布流程优化 - 添加关键文件验证
- 🔧 API server 重启稳健性提升

---

## v3.9.4 (2026-04-10 下午)

### 新增特性
- ✨ 路径自动发现模块 (paths.py) - 多用户适配
- ✨ 心理学适配器 (psychology_adapter.py) - 基于用户画像智能推荐
- ✨ FTS-only 搜索优化 - 简单查询 30x 提升
- ✨ 记忆趋势分析 (memory_trends.py)
- ✨ 智能查询推荐 (smart_query.py)
- ✨ 记忆质量评估 (memory_quality.py)
- ✨ 记忆快照管理 (memory_snapshot.py)
- ✨ 记忆洞察提取 (memory_insights.py)
- ✨ 对话摘要器 (conversation_summarizer.py)
- ✨ 查询预测器 (query_predictor.py)
- ✨ 自修复系统增强 (12 场景)
- ✨ 控制面板新增分析工具按钮

### Bug 修复
- 🐛 修复路径硬编码问题
- 🐛 修复表名/字段名映射错误

---

## v3.9.0 (2026-04-10)

### 新增特性
- ✨ 参考终极鸽子王 v2.2.2 完成六层架构对照
- ✨ 新增 Token 预算控制系统 (token_optimizer.py)
- ✨ 新增缓存TTL层级 (predictive_cache.py v2.0)
- ✨ 新增简单查询快速路径 (fast_path.py)
- ✨ 新增 L5治理层 (governance.py)
- ✨ 新增 L6基础设施层 (infrastructure.py)
- ✨ 新增层间接口规范 (docs/architecture/LAYER_INTERFACES.md)

---

## v3.4.0+ (2026-04-09)

### 新增特性
- ✨ SKILL.md 结构重组，62模块清晰分类
- ✨ Embedding配置灵活性优化（支持多Provider）
- ✨ 用户体验优化（doctor/setup命令）
- ✨ 对话交互指南（小白保护）
- ✨ 自修复系统（auto_fixer.py）

---

## v3.0.9 (2026-04-08)

### 新增特性
- ✨ ChromaDB 向量存储集成（本地持久化）

---

## v3.0.5 (2026-04-07)

### 新增特性
- ✨ 批量写入优化
- ✨ 记忆统计模块

---

_此文件记录完整版本历史_
