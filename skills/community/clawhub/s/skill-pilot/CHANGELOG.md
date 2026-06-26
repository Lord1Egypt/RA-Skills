# SkillPilot 更新日志

## v0.4.6 (2026-03-24) - 安全声明完善版

### 🔒 安全声明改进 (ClawHub 扫描修复)

**修复内容**:
- `SKILL.md`: 完善 manifest 安全声明
  - 添加 `required_env`: 声明可能使用的环境变量
  - 添加 `optional_env`: 声明可选环境变量
  - 添加 `security_notes`: 透明化权限范围

**声明内容**:
- **读取范围**: ~/.openclaw/workspace/skills/* (技能配置)
- **写入范围**: ~/.openclaw/workspace/skills/skill-pilot/ (config/cache/history)
- **网络探测**: DNS 延迟、代理检测、区域判断 (仅用于环境优化)
- **技能调用**: 通过输入验证 + 超时保护执行其他技能脚本
- **环境变量**: 仅传递给子进程，不主动外泄

**扫描状态**:
- ✅ PURPOSE & CAPABILITY: 通过
- ✅ INSTALL MECHANISM: 通过
- ✅ INSTRUCTION SCOPE: 已修复 (完善声明)
- ✅ CREDENTIALS: 已修复 (声明环境变量)
- ✅ PERSISTENCE & PRIVILEGE: 已修复 (声明写入范围)

---

## v0.4.5 (2026-03-20) - 安全修复 + 纯调度器重构

### 🔒 安全修复 (Critical)

**问题**: Shell 注入漏洞 (ClawHub 安全扫描报告)

**修复内容**:
- `run_search.py`: 移除 `shell=True`，添加输入验证和清理
- `scripts/engine.py`: 
  - `SkillExecutor._validate_args()`: 参数安全验证
  - `SkillExecutor._run_script()`: 继承环境变量 (`TAVILY_API_KEY`)
  - `OpenClawCaller._sanitize_query()`: 查询字符串清理

**测试验证**:
- ✅ 正常查询：正常工作
- ✅ 注入攻击 (`;`, `|`, `$()`, `` ` ``): 全部被拒绝

### 🏗️ 架构重构

**核心原则**: SkillPilot 只做调度和评测，不自己实现调用逻辑

**变更内容**:
- `ExecutionEngine`: 简化为纯调度器
- `SkillExecutor`: 仅执行有脚本文件的技能
- `OpenClawCaller`: 通过 OpenClaw 工具调用无脚本技能

**设计优势**:
- ✅ 职责清晰：调度 vs 执行分离
- ✅ 易于维护：不重复实现调用逻辑
- ✅ 借用现有：使用 OpenClaw 工具链

### 📊 功能优化

**全量模式**:
- 调用多个技能 → 收集结果 → 对比质量 → 选出最优
- 自动更新默认工具（如果新工具更优）

**质量评估**:
- 内容长度评分
- 中文内容识别
- 信息密度评估

### 🐛 Bug 修复

- 修复 `tavily-search` 环境变量传递问题
- 修复 `subprocess.run()` 不继承环境变量问题
- 修复质量评估逻辑问题

### 📈 性能改进

- 技能缓存机制
- 并行执行优化
- 超时控制增强

---

## v0.3.0 (2026-03-17) - 双模式支持

### ✨ 新增功能

**双模式**:
- `default` 模式：快速执行，使用默认工具
- `full` 模式：对比优化，自动选择最优

**自动优化**:
- 根据执行表现自动选择最优工具
- 更新默认工具配置

### 📊 可观测性

- 执行日志记录
- 性能指标收集
- 学习模式分析

---

## v0.2.0 (2026-03-17) - 自适应优化版

- ✅ 新增环境探测模块
- ✅ 新增用户偏好模块
- ✅ 新增历史学习模块
- ✅ 新增可观测性模块
- ✅ 新增调度策略模板
- ✅ 新增配置管理

---

## v0.1.0 (2026-03-17) - 基础版

- ✅ 核心框架实现
- ✅ 技能注册中心
- ✅ 路由决策器
- ✅ 降级处理器
- ✅ 执行引擎
- ✅ 基础指标收集
