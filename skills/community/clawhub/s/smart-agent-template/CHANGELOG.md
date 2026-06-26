# 更新日志

## v1.2.0 (2026-03-27)

### 新增（P0 完整版）
- ✅ 多 Agent 协作机制
  - `docs/MULTI_AGENT_COLLABORATION.md` — 协作架构、通信协议、冲突避免
  - `scripts/safe_write.sh` — 文件锁机制
- ✅ 性能监控机制
  - `docs/PERFORMANCE_MONITORING.md` — 监控指标、数据分析、可视化
  - `scripts/log_metrics.sh` — 记录性能数据
  - `scripts/generate_report.sh` — 生成周报
  - `reports/` 目录 — 存放性能报告

### 改进
- 更新 README，增加性能监控使用说明
- 完善文件结构说明

---

## v1.1.0 (2026-03-27)

### 新增
- ✅ 自动化脚本
  - `scripts/compress_hot.sh` — 自动压缩 hot.md
  - `scripts/archive_logs.sh` — 自动归档旧日志
  - `scripts/health_check.sh` — 健康检查
- ✅ 记忆压缩规则文档 `docs/MEMORY_COMPRESSION.md`
- ✅ 真实案例 `examples/case-01-ios-dev/`（30天演化过程）
- ✅ 补充缺失目录结构

### 改进
- 更新 README，增加自动化工具使用说明
- 完善文件结构说明

---

## v1.0.0 (2026-03-26)

### 初始版本
- 基础模板结构
- 分层记忆机制
- WBS 任务拆分
- 3高原则 + 第一性原理
