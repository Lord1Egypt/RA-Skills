# universal-intelligence-agent v1.0.0

> **状态: 稳定版** — 生产就绪

## 架构

| 维度 | 实现 |
|------|:---:|
| 编排器 | 纯调度协调器 (pipeline_coordinator.py) |
| 数据校验 | Pydantic v2 强制契约 + ACL 防腐层 |
| 熔断 | 三级: 引擎/阶段/全局 |
| 事务 | 两阶段提交 (2PC) |
| 副作用 | SideEffectLogger 完整审计 |
| 输入净化 | InputSanitizer + Anti-Corruption |
| 测试 | Contract Tests + Fuzzing + 集成测试 |
| 搜索容错 | 重试+指数退避 |
| 全局超时 | Unix signal / Windows 轮询 |
| 会话恢复 | WAL 快照 + resume_session |

## 项目结构

```
universal-intelligence-agent/
├── __init__.py                     # 包入口
├── run.py                          # CLI 入口
├── pyproject.toml                  # 工程配置
├── requirements.txt                # 依赖
├── SKILL.md                        # 技能定义
├── README.md                       # 本文件
│
├── contracts/                      # 数据契约 (Pydantic v2)
│   ├── search_schema.py            # 搜索请求/结果
│   ├── crawl_schema.py             # 爬取请求/结果
│   ├── analysis_schema.py          # 分析结果
│   ├── llm_schema.py               # LLM分析
│   ├── nlp_schema.py               # NLP结果
│   ├── state_schema.py             # 状态机/事务
│   ├── report_schema.py            # 报告输出
│   ├── alert_schema.py             # 预警监控
│   └── context_schema.py           # 上下文总线
│
├── layers/                         # 执行层
│   ├── input_adapter.py            # 输入适配层
│   ├── output_adapter.py           # 输出适配层
│   ├── pipeline_coordinator.py     # 纯调度协调器
│   ├── acl.py                      # 防腐层
│   ├── field_mapper.py             # 字段映射
│   ├── degraded_handler.py         # 降级处理
│   ├── rollback_coordinator.py     # 回滚协调
│   ├── preflight.py                # 环境预检
│   ├── search_engine.py            # 16引擎搜索
│   ├── scraper.py                  # 智能爬取
│   ├── analyzer.py                 # 分析引擎
│   ├── credibility_engine.py       # 可信度评分
│   ├── nlp_engine.py               # NLP分析
│   ├── llm_hub.py                  # 免费LLM池
│   └── engine_health.py            # 引擎健康度
│
├── middlewares/                    # 横切层
│   ├── circuit_breaker.py          # 三级熔断器
│   ├── transaction.py              # 两阶段事务
│   ├── anti_corruption.py          # 输入净化
│   ├── side_effect_log.py          # 副作用日志
│   └── metrics.py                  # 监控指标
│
├── templates/                      # 报告模板
│   ├── brief_report.md
│   └── analysis_report.md
│
└── tests/                          # 测试 (112 通过)
    ├── conftest.py
    ├── contracts/
    ├── fuzz/
    └── integration/
```

## 快速开始

```bash
# 安装
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# CLI 使用
python run.py search "AI趋势"
python run.py deep "区块链技术"
python run.py compare "Python" "Rust"
python run.py verify "某个断言"
python run.py health
python run.py status
```

## 核心特性

1. **PipelineBus 单轨制**: 阶段间数据通过强类型上下文总线传递，消除类型黑洞
2. **ACL 防腐层**: 每个阶段间强制数据校验，杜绝 None/空列表/脏数据向下游传播
3. **三级熔断**: 引擎级/阶段级/全局级，单引擎失败不拖垮整组
4. **两阶段提交**: 所有副作用先缓冲，统一提交或逆序回滚
5. **搜索重试+退避**: 单引擎最多重试 2 次，指数退避 2s→4s
6. **全局超时**: Unix signal.alarm / Windows 轮询标志位
7. **声明式字段映射**: FieldMapper 映射表，零类型猜测
8. **版本号幂等**: 同名文件追加 _v1/_v2，不覆盖
9. **WAL 快照恢复**: 每个阶段完成后序列化 PipelineBus，支持跨会话恢复
10. **统一降级路径**: DegradedHandler 确保降级输出与正常输出格式一致

## 功能完整性

- ✅ 16引擎搜索 — 含重试+退避
- ✅ 智能反爬+指纹伪装
- ✅ 跨源去重+内容去重
- ✅ 来源可信度评分
- ✅ 免费LLM池
- ✅ 中文NLP
- ✅ 决策框架
- ✅ WAL协议 — 两阶段提交
- ✅ 多格式报告 — 简报/深度/对比/JSON
- ✅ 跨会话恢复 — resume_session
- ✅ 全局超时 + 熔断保护
- ✅ 副作用审计 + 原子回滚
