# Changelog

All notable changes to this project will be documented in this file.

## v12.2.0 (2026-06-08)

### 安全审计修复（192项发现全部修复）

#### Critical 修复
- SSRF防护：所有urlopen调用添加`_validate_url()`（协议白名单+私有IP阻断+域名白名单）
- API Key泄露修复：Google API Key从URL参数移至HTTP Header + 错误消息脱敏
- 提示注入防护：移除system_prompt路径 + UUID边界标记替代可伪造标记
- Spirit命令白名单：`ALLOWED_INTENTS` 限制可执行命令
- 数据外泄防护：Slack/Obsidian/收集器默认禁用

#### High 修复
- 路径遍历防护：`_validate_path()` 阻止目录遍历攻击
- 过度自主控制：5个opt-in环境变量（AUTO_PURGE/SLACK_NOTIFY/OBSIDIAN_SYNC/REACTOR_AUTO_EXECUTE/COLLECTORS_AUTO_START）
- 人格分析同意门控：`AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED` 必须显式启用
- MCP工具描述安全约束：11个工具添加SAFETY说明
- LLM注入检测：`_INJECTION_PATTERNS` 检测并记录可疑输入
- 团队共享访问控制：target_agents时visibility改为"restricted"

#### Medium 修复
- Playground IP限流：60请求/分钟
- 危险系统命令移除：network_diag.py不再执行systemctl/iptables
- SKILL.md权限声明：3必需+2可选
- Causal link类型统一：led_to→causal.led_to, contradicts→causal.contradicts
- CalendarConfig添加@dataclass装饰器
- GDPR合规检查改为功能性验证
- 传输加密不再无条件PASS
- 物理删除增加secure_delete选项

### GitHub发布准备
- LICENSE (MIT) / SECURITY.md / CODE_OF_CONDUCT.md
- Issue/PR模板 / Release工作流 / FUNDING.yml

---

## v12.1.0 (2026-06-08)

### 综合审查与修复（14轮迭代，231项改进）

#### 安全修复
- SQL注入防护：backend.py/pg_store.py/_schema.py/distill.py 添加标识符白名单校验
- 硬编码API Key替换：4处示例代码替换为`<YOUR_API_KEY>`占位符
- Playground错误信息不再泄露内部细节
- API Key比较改用hmac.compare_digest（防时序攻击）
- PII检测增强：零宽字符/RTL/HTML实体/NFKC标准化
- 暴力破解计数器持久化到SQLite
- JWT空secret校验
- Fernet密钥禁止自动生成

#### 数据安全与可靠性
- StoreCircuitBreaker：三态熔断器（CLOSED→OPEN→HALF_OPEN）+ 指数退避重试
- 启动时integrity_check + 损坏自动从备份恢复
- 降级模式：MemoryStore初始化失败时创建内存数据库
- WAL checkpoint优雅关闭（防止WAL文件膨胀）
- 软删除/恢复改用事务管理器
- 备份并发保护（_backup_lock）
- 嵌入删除失败后新增cleanup_orphaned_embeddings()

#### 性能优化
- BM25改用FTS5替代内存线性扫描（搜索延迟10x提升）
- 并行检索管道（ThreadPoolExecutor并行5路检索）
- 写入批处理队列（WriteBatcher，吞吐10x提升）
- SQLite连接池（最大20连接+健康检查）
- topics逐条INSERT改为executemany()批量
- embedding_store.list_all_ids()添加LIMIT
- distill全表扫描添加LIMIT
- 新增3个索引（last_accessed_ts/bookmarked/复合索引）
- WAL checkpoint间隔100→1000

#### 架构优化
- MemoryStore拆分为5个子管理器（VersionManager/LinkManager/StatsManager/SchemaMigrator/ConnectionManager）
- AgentMemory改为门面模式
- StorageBackend抽象接口（ABC + SQLiteBackend）
- execute_sql()网关方法（熔断器保护+缓存失效+审计）
- register_schema()统一Schema管理
- 9个文件从store.conn直接访问迁移到execute_sql()
- 26组件依赖图+严重度分级+级联影响分析
- 伪异步模块诚实文档+事务隔离警告

#### SDK封装
- 极简SDK：Memory类，13个方法（remember/recall/forget/update/status/echo/revert/bookmark/unbookmark/bookmarks/milestones/share_card/close）
- 品牌方法名：remember/recall/forget（save/search/delete为兼容别名）
- 零配置启动：Memory()自动创建~/.agent_memory/default.db
- 远程服务模式：Memory(server="http://...", api_key="...")
- SaveResult/DeleteResult/SearchResult结构化返回
- 记忆质量守门器（5项检查+quality_gate参数）
- 记忆收藏夹（bookmark/unbookmark/bookmarks）
- 记忆回声（echo — 时间/关联/空闲三种推荐）
- 记忆里程碑（成就自动检查+分享卡片）
- 弹性参数（4个Profile预设+细粒度覆盖）
- 统一API网关（单入口挂载/v1 + /playground + /health）

#### 产品进化
- DigitalTwin：从硬编码改为从记忆内容计算风险偏好
- CuriosityEngine：移除幻觉注入路径，改为仅返回缺口分析
- AchievementSystem：3个成就带reward（反馈加权/图谱扩展/自动脱敏）
- SkillEngine：质量调整有效使用量替代简单计数
- OrgProfile：新增主题/重要性/时效分布+健康评分+建议
- AnnualReport：数据驱动洞察替代模板化文案
- MetacognitiveLoop：策略实际被recall引擎消费
- SyncEngine：修复peer属性和时间戳bug
- KnowledgeBuilder：jieba中文分词+正确IDF计算
- PermissionMatrix：store读写层执行权限检查
- AuditLogger：批量缓冲提交+日志轮转
- AutoTagger：CJK关键字包含匹配+非CJK词边界
- FeatureFlags：remember/recall/spirit实际消费标志
- KnowledgeDistiller：按importance排序+结构化摘要

#### UX文案与信息架构
- SDK核心方法统一命名：remember/recall/forget
- 中英文混杂修复：friendly_errors/store/mcp_server/spirit/repl全部统一
- 空状态文案升级：7处添加引导+行动召唤
- 错误文案升级：Playground"系统开小差了"+SDK中文消息
- 情感基调：Spirit报告📋+Playground"记住/回忆"+SDK中文tips
- CLI分类重组：新增_recall.py+_persona.py，6个模块重新分配
- Playground按钮：写入→记住、检索→回忆

#### 可观测性
- JSON结构化日志（AGENT_MEMORY_LOG_FORMAT=json）
- Liveness/Readiness探针（/v1/health/live + /v1/health/ready）
- trace_id自动传播中间件（X-Trace-ID + X-Request-ID）
- PII检测（可选，AGENT_MEMORY_PII_CHECK_ON_WRITE=true）
- 告警通知系统（AlertManager + Webhook + 5种预定义告警 + 夜间静默）
- recall空结果率+remember成功率指标追踪

#### 合规与隐私
- GDPR自动purge（AGENT_MEMORY_AUTO_PURGE_DAYS）
- ConsentManager与API集成（写入前检查同意状态）
- CryptoStore自动加密（confidential/private级别）
- 严格加密模式（AGENT_MEMORY_STRICT_ENCRYPTION=true）

#### API防御
- 文档text长度限制（MAX_DOCUMENT_TEXT_LENGTH=500000）
- Batch端点大小限制（MAX_BATCH_SIZE=100）
- Playground top_k上限（le=100）
- Web Server速率限制（SimpleRateLimiter）
- API v2标记deprecated（DeprecationWarning + Sunset头）

#### 测试
- 新增167个测试：多租户隔离(7)+备份恢复(8)+并发访问(4)+生命周期(8)+CLI冒烟(8)+Playground API(10)+长期运行(6)
- CI覆盖率阈值60%→75%

#### 文档
- 新增SDK_QUICKSTART.md
- 新增API_REFERENCE.md
- 新增RUNBOOK.md（4个故障场景SOP）
- README.md一致性修复（4处）
- .gitignore补充（*.corrupted）

#### 实验性模块标记
- gRPC Server、CalDAV/WeChat/DingTalk收集器标记EXPERIMENTAL

---

## v12.0.0 (2026-05-25)

### 新特性
- TEMPR 五路检索融合：FTS + BM25 + 语义向量 + 实体扩展 + 因果链，RRF 融合排序
- 双时间线事实管理：valid_from/valid_until/occurrence_time/mention_time 四字段
- 实体消解引擎：规则式+LLM增强提取，别名倒排索引，三级消解（精确→别名→模糊）
- ChromaDB 向量存储回退：sqlite-vec 不可用时自动切换
- jieba 中文分词集成：FTS 写入/查询时自动分词
- 记忆衰减时间偏置（recency bias）：70天半衰期，最近访问记忆获排序加成
- 加密存储 CryptoStore：Fernet 对称加密，confidential/private 记忆自动加密
- 统一配置层 config/settings.py：聚合环境变量/JSON/默认值
- Web API 认证：X-API-Key 请求头认证
- 自动事实失效检测：LLM 驱动的新旧事实冲突检测
- BM25 稀疏检索路：FTS5 不可用时的独立稀疏检索能力
- MaintainEngine.diagnose() 统一诊断接口
- HealthChecker 委托 MaintainEngine.diagnose()
- KnowledgeDistiller 适配器化（委托核心 MemoryDistiller）

### Store 重构
- `store.py` 拆分为 `store/` 包，包含 5 个子模块：
  - `_core.py` — MemoryStore 核心 CRUD 操作
  - `_schema.py` — SchemaMigrator 数据库 Schema 创建与迁移
  - `_tasks.py` — TaskManager 记忆相关 TODO 与提醒
  - `_maintenance.py` — MaintenanceManager 数据库优化、VACUUM、完整性检查
  - `_file_lock.py` — _FileLock 跨进程文件锁

### Recall Pipeline
- 7 步后处理管道：_RankingStep → _TemporalFilterStep → _FeedbackStep → _EmotionStep → _RerankStep → _MMRStep → _EnrichmentStep
- 多维质量排序、双时间线过滤、反馈权重调整、情感共鸣加成、交叉编码器精排、MMR 多样性、结果富化

### Resilience 模块
- CircuitBreaker 断路器：CLOSED → OPEN → HALF_OPEN 三态，可配置失败阈值与恢复超时
- timeout_call 超时包装：线程级超时控制，防止慢查询阻塞
- CircuitOpenError / TimeoutError 异常类型

### 成本优化（FinOps）
- LLM 日调用限制（AGENT_MEMORY_COST_LLM_DAILY_CALL_LIMIT）
- LLM 日费用限制（AGENT_MEMORY_COST_LLM_DAILY_COST_LIMIT_USD）
- 压缩 LLM 预算控制（AGENT_MEMORY_COST_COMPRESS_LLM_BUDGET）
- 因果分析间隔控制（AGENT_MEMORY_COST_CAUSAL_ANALYSIS_INTERVAL）
- VACUUM 时间窗口限制（AGENT_MEMORY_COST_VACUUM_ALLOWED_HOURS）

### 安全修复
- 修复 TEMPR 检索返回0条的 bug（中文查询关键词提取+LIKE回退）
- 修复 FTS5 tokenizer 自动回退（trigram→unicode61）
- 修复 pipeline.py 独立 SQLite 连接缺少 PRAGMA 配置
- 修复 recall_mixin Fallback 路径缺少 keyword 参数
- 修复 TopicRegistry 缺少 get_all_topic_codes 方法
- 修复 engines/ 目录裸包名导入（recall_engine/ingest/cognition）
- 修复 memory_mixin media_processor 裸导入
- 修复 pipeline enterprise 裸导入
- 修复 MCP tool_correct 参数签名错误
- 修复 web_server.py 无认证
- 修复 CryptoStore 失败返回明文
- 修复 JWT 默认密钥硬编码
- 修复 entity.py 全表扫描性能问题（别名倒排索引+模糊匹配缓存）
- 修复 jieba 懒加载非线程安全
- 修复 HealthChecker 5次重复全量查询

### UX 改进
- health_check() 返回结构化结果：status/healthy/total/available/degraded/components
- recall() 返回 dict（primary/total/search_mode/status），不再返回裸列表
- CLI 新增约 60 个子命令，覆盖核心操作/知识管理/时间旅行/自我认知/Spirit 管家/增长/分布式

### 变更
- 版本号统一为 12.0.0（pyproject.toml + __init__.py + VERSION + MCP）
- 13个废弃模块归档到 _archive/
- store.py 重构为 store/ 包（_core/_schema/_tasks/_maintenance/_file_lock）
- pipeline.py 复用 store 连接（统一 PRAGMA 配置）
- PII 模式统一到 privacy/patterns.py
- recall_mixin 文档更新为"五路并行检索"
- mcp_server 文档更新为"11 MCP tools"
- 新增 resilience/ 包（CircuitBreaker + timeout_call）

---

## v11.0.0 (2026-05-25) — 个人记忆操作系统

### 🏗️ 架构升级：从记忆系统到记忆操作系统

V11 核心范式转换：所有 Agent 产生记忆 → 管家统一管理 → 任何 Agent 按需获取。

| 维度 | V10 | V11 |
|------|-----|-----|
| 记忆归属 | Agent 的附属 | **用户的资产** |
| 管家角色 | 记忆库管理员 | **用户数字身份的守门人** |
| 连接模式 | 单 Agent 直连 | **多 Agent 共享网络** |
| 技能传播 | 无 | **Agent 间技能学习与分发** |

### ✨ 新特性

- **MCP Server** — 11 个标准 MCP 工具（remember/recall/spirit_check/get_profile/report/share_skill/learn_skill/context_for/correct/delete/significance），任意 MCP 客户端零代码接入
- **Spirit 管家克制规则** — 防止过度打扰，按频率/时段智能控制巡检与通知
- **多源收集器框架** — 钉钉 / 企业微信 / 邮件 / 日历 / 文件，5 种收集器 + 调度器 + 归一化器（部分为占位标注，待接入实际 API）
- **跨 Agent 技能分发** — 技能包打包、分享、评分、学习
- **隐私守门** — PrivacyGuard（基于 visibility 的访问控制）+ PrivacyRuleSet（规则引擎）+ SensitivityAnalyzer（PII/金融/健康/凭证检测）+ ConsentManager（授权管理）
- **企业级模块** — 权限矩阵 + 审计日志 + 合规检测（ComplianceGuard）+ 知识蒸馏 + 离职交接 + 组织画像 + 技能市场
- **Graceful Degradation** — 可选依赖缺失时核心功能不受影响，`check_optional_deps()` 返回依赖状态
- **Docker 支持** — Dockerfile + docker-compose.yml

### 🐛 修复

- **embedding_store 弱引用错误** — 修复 `_initialized_conns` 在弱引用场景下的连接丢失问题
- **FTS5 降级** — SQLite 不支持 trigram tokenizer 时自动降级为基础 tokenizer，不再崩溃
- **sqlite-vec 降级** — sqlite-vec 不可用时自动降级为 SimHash，核心功能不受影响
- **recall 缓存问题** — 修复 recall_mixin 缓存键哈希化，防止缓存键过长导致的问题
- **密钥 URL 明文传递** — API 密钥不再出现在 URL 参数中，改用 Header 传递
- **PermissionError 覆盖内置异常** — 修复自定义 PermissionError 遮蔽 Python 内置 PermissionError 的问题
- **should_merge / is_retracted 逻辑** — 修复记忆合并与撤回判断的边界条件

### ⚡ 优化

- **HfApi 镜像降级** — huggingface_hub 1.16+ 的 `hf_hub_download` 不读 `HF_ENDPOINT` 时，自动用 `HfApi(endpoint=...)` 从镜像下载
- **本地模型路径支持** — `AGENT_MEMORY_EMBEDDING_MODEL` 支持本地路径，离线/内网部署无需网络
- **ComplianceGuard 集成** — 合规检测集成到写入管道，自动标记敏感内容
- **收集器占位标注** — 钉钉/企业微信/邮件/日历收集器标注为占位实现，待接入实际 API

### 🔒 安全

- **审计 Round 4** — SQL 注入防护（query_raw 白名单）、租户隔离验证、CORS 强化、Prompt 注入防护
- **审计 Round 5** — 版本号一致性校验、裸 except 清理、存储工厂安全

### 📦 依赖

- **sentence-transformers 移至可选依赖** — 从核心依赖移至 `[semantic]` 可选组，基础安装不再包含
- **requirements.txt 与 pyproject.toml 同步** — requirements.txt 仅包含核心依赖（typing_extensions, sqlite-vec），可选依赖通过 pyproject.toml 管理
- **pyproject.toml 版本更新至 11.0.0**

### 🧪 测试

- 新增 test_v11_phase1.py — MCP Server + PrivacyGuard + SensitivityAnalyzer + ConsentManager + Schema 迁移
- 新增 test_v11_full.py — Privacy Rules + Collectors + Skill Distribution + Spirit 增强 + Enterprise 模块
- 新增 test_v11_integration.py — AgentManager V11 + Schema 验证 + Bug 修复验证
- 新增 test_v11_productization.py — Demo + CLI + Docker + Graceful Degradation
- 新增 test_audit_round4.py — SQL 注入 + 租户隔离 + CORS
- 新增 test_audit_round5.py — 版本一致性 + 裸 except + 存储工厂

---

## v10.0.0 (2026-05-20) — 四引擎架构 + 器灵管家 + 双 LLM 安全协议

### 🏗️ 架构重构：碎片化模块 → 4 引擎统一架构

```
┌─────────────────────────────────────────┐
│           接入层 (Gateway)               │
│  CLI · HTTP API · gRPC · MCP Server     │
├─────────────────────────────────────────┤
│           管家层 (Spirit)               │
│  主动巡检 · 隐私守门 · 精准分发          │
├─────────────────────────────────────────┤
│           引擎层 (Engines)              │
│  Ingest · Recall · Maintain · Cognition │
├─────────────────────────────────────────┤
│           存储层 (Storage)              │
│  SQLite + sqlite-vec + FTS5             │
└─────────────────────────────────────────┘
```

### ✨ 新特性

- **四引擎架构** — IngestEngine / RecallEngine / MaintainEngine / CognitionEngine，统一接口
- **Spirit 记忆管家** — 主动巡检 + 健康检查 + 冲突解决 + 每日/每周报告 + 命令系统
- **双 LLM 安全协议** — 12 个 Bug 场景与对策，Agent LLM 永远不接触原始记忆数据
- **认知引擎** — 数字孪生 + 偏好记忆 + 元认知 + 好奇心驱动
- **Spirit 增强模块** — preference_sync（偏好同步）+ proactive_delivery（精准分发）+ memory_partition（记忆分区）+ cross_agent_dedup（跨 Agent 去重）
- **引擎层扩展** — DecayPolicy / RecallAssessor / KnowledgeBuilder / FeedbackLearner / FederationEngine / SyncEngine / CuriosityEngine / KnowledgeValidator / SkillEngine / MetacognitiveLoop / CognitiveProfile

### 🔒 安全

- **Dual-LLM 安全协议** — [MEMORY_REPORT] 标记 + [META] 元信息 + [UNVERIFIED] 标记 + 写入冷却期
- **IngestEngine filter** — 检测并剥离 Agent 推理性语言，防止写入劫持
- **Spirit LLM Layer** — 三层降级（LLM → Embedding → 模板），每层输出格式一致

### 🧪 测试

- 新增 test_v10_engines.py — 4 引擎核心功能测试
- 新增 test_v10_core.py — 综合功能测试（无外部依赖）

---

## v9.3.1 (2026-05-17) — 系统审计·安全加固·性能优化

### 🔒 安全加固
- **JWT Insecure Mode 加固**: 不安全模式下 Token 签发仅允许 localhost 请求; 响应头注入 X-Insecure-Mode 标识
- **SQL 注入防护**: chat_parser.py 表名严格正则校验，防止恶意 SQLite 数据库注入
- **MD5 → SHA-256**: chat_parser.py 和 personality_memory.py 的 ID 生成从 MD5 升级为 SHA-256
- **文件上传大小限制**: API 文档上传端点添加 50MB 限制，防止 OOM 攻击
- **SSE 连接数限制**: 最大 100 并发 SSE 连接，防止资源耗尽

### 🏗️ 架构修复
- **TenantContext 统一**: 合并 auth_middleware.py 和 tenant.py 中重复的 TenantContext 类，统一使用 tenant.py 版本（含 can_read/can_write/can_admin 方法）
- **pyproject.toml build-backend**: 修正为标准值 setuptools.build_meta

### ⚡ 性能优化
- **get_memory() N+1 修复**: 5 次查询 → 委托 get_memories() 批量查询
- **get_linked() N+1 修复**: 递归 DFS → 两阶段 BFS 批量获取，5N 次查询 → ~4+N 次
- **check_overdue() N+1 修复**: 逐条 UPDATE/SELECT → 批量操作
- **缓存 LRU 淘汰**: 简单字典 → OrderedDict 实现 LRU 策略
- **新增 _batch_get_links()**: 与 _batch_get_topics/tools/knowledge 一致的批量查询

### 🧹 代码质量
- **emotion.py**: 移除 9 处字典重复键
- **chat_parser.py**: datetime 导入提升至文件顶部
- **permission_manager.py**: time 导入提升至文件顶部
- **personality_analyzer.py**: 修复 ChatSession/ChatMessage dataclass 兼容性（_get() 辅助函数）

### 🧪 测试
- 新增 test_permission_manager.py (64 tests)
- 新增 personality_memory SQLite 集成测试 (4 tests)
- 新增 chat_parser CSV 解析和表名校验测试 (2 tests)

---

更早的版本记录请参见 [agent_memory/CHANGELOG.md](agent_memory/CHANGELOG.md)。
