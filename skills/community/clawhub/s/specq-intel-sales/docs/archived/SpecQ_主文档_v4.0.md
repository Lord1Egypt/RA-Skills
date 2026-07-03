# SpecQ 主文档 v4.0

> 最后更新：2026-06-09 10:30  
> 维护者：悟空 + David  
> 本文档是 SpecQ 的唯一事实来源。任何其他 SpecQ 文档以本文档为准。

---

## 目录

1. [产品定位](#1-产品定位)
2. [核心价值链](#2-核心价值链)
3. [产品架构](#3-产品架构)
4. [技术架构](#4-技术架构)
5. [当前状态](#5-当前状态)
6. [实施路径](#6-实施路径)
7. [关键决策](#7-关键决策)
8. [历史文档索引](#8-历史文档索引)

---

## 1. 产品定位

### 1.1 一句话

**电子化学品销售的客户攻单情报包生成器。**

输入：产品名 + 应用场景 + 目标客户（三字段）  
输出：八模块结构化情报包，帮助销售成交。

### 1.2 定位演变

| 时间 | 定位 | 价值标尺 |
|---|---|---|
| 2026-05（FAE Agent）| 全半导体 AI 知识引擎 | 查询准确率 |
| 2026-06-01（SpecQ v3.0.1）| 半导体产业链规格查询 + FAE 经验沉淀 | DAU |
| **2026-06-08（战略转向）** | **电子化学品攻单情报包生成器** | **成交率** |

### 1.3 价值主张

从「帮销售查资料」→「帮销售拿订单」。  
AI 生成内容终将同质化，**用户自有的销售经验数据（暗数据）是不可替代的护城河**。

---

## 2. 核心价值链

### 2.1 八模块情报包

| # | 模块 | 数据来源 | 状态 |
|---|---|---|---|
| 1 | 产品技术参数概览 | knowledge.db（爬取） | 公开数据 |
| 2 | 竞品格局分析 | knowledge.db + 行业报告 | 公开数据 |
| 3 | 应用场景适配 | knowledge.db + 工艺映射 | 公开数据 |
| 4 | **客户关注指标** | 🔒 暗数据（销售拜访沉淀） | 暗数据 |
| 5 | **切入机会（五维）** | 🔒 暗数据（竞品格局推演） | 暗数据 |
| 6 | **主要导入障碍** | 🔒 暗数据（丢单复盘） | 暗数据 |
| 7 | 推荐话术与行动建议 | LLM 生成 | AI 生成 |
| 8 | 参考来源 | knowledge.db Chunk 溯源 | 自动 |

**模块 4/5/6 是真正的护城河**，因为它们不能从公开网页爬取，只能由销售经验沉淀。

### 2.2 D→C→B 三层暗数据激励架构

| 层 | 是什么 | 解决的问题 | 状态 |
|---|---|---|---|
| **D — 工具即陷阱** | 拜访纪要（语音输入）、客户档案、丢单复盘做成销售离不开的工具 | "我为什么要用 SpecQ" | MVP 必做 |
| **C — 脱敏护盾** | 客户名→行业标签自动脱敏后才进入共享池，原文仅自己可见 | "我为什么敢共享" | MVP 后启动 |
| **B — 精准飞轮** | 基于个人沉淀数据训练私有模型，用得越久情报包越精准 | "我为什么持续用" | 数据量够后启动 |

### 2.3 双端定位

| 端 | 定位 | 核心功能 | 技术栈 |
|---|---|---|---|
| **App** | 销售沉淀工具 + 精准飞轮 | 三字段→情报包、拜访纪要（语音）、客户档案、丢单复盘、离线可用 | Flutter 3.44 |
| **小程序** | 获客入口 | 仅三字段输入→情报包生成，底部「沉淀到我的客户档案」引导下载 App | 微信原生 |

---

## 3. 产品架构

### 3.1 App 功能全景

```
SpecQ App
├── intel（情报包）
│   ├── 三字段输入（产品/应用/场景）
│   └── 八模块情报包展示
├── crm（客户关系 — D 层核心）
│   ├── customer    —— 客户档案 + 时间线
│   ├── visit       —— 拜访纪要（语音输入 + 手动输入）
│   └── loss        —— 丢单复盘
├── profile（B 层预留）
│   └── 个人精准模型
└── share（C 层预留）
    └── 脱敏共享池
```

### 3.2 MVP 功能边界

| 功能 | MVP | 备注 |
|---|---|---|
| 三字段→情报包（八模块） | ✅ P0 | 模块 4/5/6 初始为 LLM 推测版 |
| 客户档案 CRUD | ✅ P1 | 名称/行业/联系人/标签 |
| 拜访纪要（手动） | ✅ P1 | — |
| 拜访纪要（语音） | ✅ P1 | macOS/iOS/Android ✅，Windows ❌ |
| 丢单复盘 | ✅ P1 | 结构化模板 |
| 离线可用 | ✅ P1 | 读写均离线优先 |
| 跨销售数据共享（C 层） | ❌ | MVP 后 |
| 个人精准模型（B 层） | ❌ | 数据量够后 |
| 微信登录/支付 | ❌ | MVP 后 |

### 3.3 小程序 MVP

仅保留三字段输入→情报包生成，底部引导下载 App。  
服务端与 App 共享同一个 `/api/intel/generate` 端点。

---

## 4. 技术架构

### 4.1 系统全景

```
┌──────────────────┐     ┌──────────────────┐
│  SpecQ App       │     │  SpecQ 小程序     │
│  (Flutter 3.44)  │     │  (微信原生)       │
│  iOS/Android/    │     │  获客入口         │
│  macOS/Windows   │     │                  │
└────────┬─────────┘     └────────┬─────────┘
         │  Dio + Token           │  wx.request
         ▼                        ▼
┌──────────────────────────────────────────────┐
│  FastAPI 服务端 (119.91.223.127:8000)        │
│                                              │
│  auth/     — /api/auth/*       → master.db   │
│  intel/    — /api/intel/*      → knowledge.db│
│                                  + ChromaDB  │
│  crm/      — /api/customers/*  → user.db     │
│            — /api/visits/*                   │
│            — /api/loss-reviews/*             │
│  pipeline/ — 数据采集→入库管线               │
└──────────────────────────────────────────────┘
```

### 4.2 App 前端技术栈

| 层 | 选型 | 版本 |
|---|---|---|
| 框架 | Flutter | 3.44 stable |
| 语言 | Dart | >= 3.7.0 |
| 状态管理 | Riverpod（flutter_riverpod） | ^3.3.0 |
| 本地数据库 | Drift（SQLite） | ^2.33.0 |
| 网络请求 | Dio | latest |
| 代码生成 | build_runner + drift_dev | — |

**架构模式**：两层 MVVM（View → ViewModel → Repository → DataSource），不做 UseCase 层。  
**离线策略**：读先本地后远程，写先本地后同步，冲突按服务端时间戳为准。

### 4.3 服务端技术栈

| 层 | 选型 |
|---|---|
| 框架 | FastAPI（Python 3.14） |
| 数据库 | SQLite（4 层物理隔离：master / knowledge / user / ChromaDB） |
| 向量检索 | ChromaDB |
| LLM | DeepSeek API |
| 部署 | MacBook → rsync → 119.91.223.127 |

### 4.4 数据库四层隔离

| 数据库 | 内容 | 隔离级别 |
|---|---|---|
| master.db | 用户认证 | 全局 |
| knowledge.db | 化学品参数、TDS/MSDS、厂商信息 | 全局（只读） |
| ChromaDB | 文档向量索引 | 全局（只读） |
| user.db | 客户档案、拜访纪要、丢单复盘 | **Per-user 物理隔离** |

### 4.5 MacBook 本地服务端结构

```
~/SpecQ/
├── main.py                      # FastAPI 入口
├── config.py                    # 全局配置（环境变量统一入口）
├── auth/                        # 认证模块
│   ├── routes.py                # /api/auth/*
│   └── models.py
├── intel/                       # 情报包模块
│   ├── routes.py                # POST /api/intel/generate
│   ├── service.py               # 三字段→Prompt→LLM→八模块
│   └── schemas.py
├── crm/                         # 客户关系模块
│   ├── routes.py                # customers / visits / loss_reviews CRUD
│   ├── service.py               # 业务逻辑 + 数据隔离
│   └── schemas.py
├── pipeline/                    # 数据采集管线（从 ~/specq_pipeline 移入）
│   ├── pipeline.py
│   ├── parse.py / label.py / extract.py
│   ├── review.py / score.py / hardblock.py / package.py
│   └── ingest/
├── enterprise/                  # 管理后台
├── core/                        # 基础设施
│   ├── database.py              # SQLAlchemy engine + session
│   ├── deps.py                  # FastAPI Depends（get_db、get_current_user）
│   └── security.py              # JWT
├── db/                          # SQLAlchemy 模型
│   ├── auth_models.py
│   ├── intel_models.py
│   └── crm_models.py            # Customer / Visit / LossReview
├── data/                        # SPECQ_DATA_DIR
├── tests/
├── .env                         # 本地环境变量
└── deploy.sh                    # rsync 部署脚本
```

### 4.6 关键依赖版本锁定

```txt
# requirements.txt (Python)
fastapi>=0.110.0
uvicorn>=0.29.0
sqlalchemy>=2.0
chromadb>=0.5.0
python-jose[cryptography]
passlib[bcrypt]
httpx

# pubspec.yaml (Dart/Flutter)
flutter_riverpod: ^3.3.0
drift: ^2.33.0
drift_flutter: ^0.3.1-wip
path_provider: ^2.1.5
dio: latest
speech_to_text: ^7.3.0
flutter_secure_storage: latest
build_runner: ^2.15.0
drift_dev: ^2.33.0
```

---

## 5. 当前状态

### 5.1 代码资产

| 资产 | 位置 | 状态 |
|---|---|---|
| FastAPI 服务端 | 119.91.223.127 + MacBook ~/SpecQ | ✅ 运行中 |
| 数据采集管线 | MacBook ~/specq_pipeline（独立目录）| ✅ 代码完成，待合并进 ~/SpecQ |
| 小程序（获客版）| MacBook ~/miniapp | ✅ 36 文件，零依赖，待精简为获客入口 |
| SpecQ App | 未创建 | 📐 架构已定，待启动 |

### 5.2 数据资产

| 数据集 | 规模 | 状态 |
|---|---|---|
| 半导体芯片文档（FAE 遗产）| 1,446 文档 / 55,042 chunks | ✅ 在 ChromaDB，未复用 |
| 湿电子化学品数据 | 未采集 | ⏳ 策略已定（白名单 + 爬取），未执行 |
| 销售暗数据（拜访纪要等）| 无 | ⏳ App D 层是入口 |

### 5.3 API 端点状态

| 端点 | 状态 |
|---|---|
| `/api/auth/login` | ✅ 已有 |
| `/api/auth/refresh` | ✅ 已有 |
| `/api/auth/me` | ✅ 已有 |
| `GET /health` | ✅ 已有 |
| `POST /api/intel/generate` | ❌ 待新增 |
| `GET/POST/PUT /api/customers` | ❌ 待新增 |
| `GET/POST /api/visits` | ❌ 待新增 |
| `POST /api/loss-reviews` | ❌ 待新增 |

### 5.4 文档状态

| 文档 | 用途 | 状态 |
|---|---|---|
| **本文档（SpecQ 主文档 v4.0）** | **唯一事实来源** | ✅ 当前 |
| SpecQ_App_架构规格摘要.md | Flutter 前端架构细节 | ✅ 已出（参考用） |
| SpecQ_服务端架构规划_v2.0.md | 服务端架构细节 | ✅ 已出（参考用） |
| SpecQ_v3.0.1_产品规划_收口修订版_20260601.md | v3.0.1 历史产品规划 | 📦 归档 |

---

## 6. 实施路径

### 阶段 1：基础设施就绪（当前）

- [ ] 管线代码合并进 `~/SpecQ/pipeline/`
- [ ] 服务端路由重构（auth / intel / crm / core 拆分）
- [ ] 环境变量统一（config.py 作为唯一入口）
- [ ] 本地端到端验证（health + 登录）

### 阶段 2：后端 API

- [ ] `POST /api/intel/generate` — 三字段→八模块情报包
- [ ] crm_models.py — Customer / Visit / LossReview 三张表
- [ ] `GET/POST/PUT /api/customers` — 客户 CRUD
- [ ] `GET/POST /api/visits` — 拜访纪要
- [ ] `POST /api/loss-reviews` — 丢单复盘

### 阶段 3：前端 App

- [ ] Flutter 项目初始化（四平台）
- [ ] 最小可跑栈验证（Riverpod + Drift + Dio）
- [ ] intel feature — 三字段→情报包（App + 小程序共享端点）
- [ ] crm feature — 客户档案 + 拜访纪要 + 丢单复盘

### 阶段 4：数据建设

- [ ] 湿电子化学品全量爬取（按白名单厂商）
- [ ] Trust Engine 交叉验证规则 X 执行
- [ ] 10-20 条脱敏案例冷启动（确保 C 层池子非空）

### 阶段 5：暗数据闭环

- [ ] 首批种子销售使用 App D 层沉淀数据
- [ ] C 层脱敏共享池上线
- [ ] B 层个人精准模型启动

---

## 7. 关键决策

| # | 决策 | 日期 | 理由 |
|---|---|---|---|
| 1 | SpecQ 定位从「行业知识引擎」转为「攻单情报包」 | 6/8 | 价值标尺从 DAU 变为成交率 |
| 2 | 暗数据是护城河，D→C→B 三层递进激励 | 6/9 | AI 生成内容将同质化，用户数据不可替代 |
| 3 | 小程序退位为获客入口，App 承载深度体验 | 6/9 | D 层需要原生体验（语音/离线/文件管理） |
| 4 | Flutter 四平台（iOS/Android/macOS/Windows）| 6/9 | 唯一一份代码覆盖全平台的方案 |
| 5 | Riverpod + Drift + Dio，两层 MVVM | 6/9 | 匹配独立开发者维护成本 |
| 6 | 服务端复用现有 FastAPI，新增 4 路由 + 3 表 | 6/9 | 不新建后端，约 400-500 行新代码 |
| 7 | Windows 桌面端不做语音输入 | 6/9 | `speech_to_text` Windows 支持仍在 beta |
| 8 | 管线代码合并进 ~/SpecQ 统一仓库 | 6/9 | 消除双目录管理的同步成本 |
| 9 | 不引入 UseCase 层 / Repository 接口 / DI 框架 | 6/9 | 独开不需要团队协作的抽象边界 |

---

## 8. 历史文档索引

以下文档为历史记录，保留作审计用途。**所有产品/架构决策以本文档 (v4.0) 为准。**

### 产品规划

| 文档 | 日期 | 说明 |
|---|---|---|
| SpecQ_v3.0.1_产品规划_收口修订版_20260601.md | 6/1 | v3.0.1 产品规划，定位已被 6/8 转向覆盖 |
| SpecQ_v3.0_产品规划_全量设计决策汇总_20260601.md | 6/1 | v3.0 汇总，已被 v3.0.1 覆盖 |

### Experience OS 系列（5/29-6/1）

| 文档 | 内容 |
|---|---|
| SpecQ_ExperienceOS_ExecutionPlan_v1.0_20260531.md | 执行计划 |
| SpecQ_ExperienceOS_DataAcquisitionStrategy_v1.1_20260601.md | 数据采集策略（白名单 + 爬取） |
| SpecQ_ExperienceOS_TrustEngine_v1.1_20260601.md | Trust Engine 六维模型 |
| SpecQ_ExperienceOS_CaseSchema_v1.0_20260529.md | Case 数据结构 |
| SpecQ_ExperienceOS_DataOwnershipModel_v1.0_20260529.md | 数据权属模型 |
| SpecQ_ExperienceOS_FirstRevenueModel_v1.0_20260529.md | 早期商业模型 |
| SpecQ_ExperienceOS_StrategicResearch_v1.0_20260529.md | 行业战略调研 |
| SpecQ_ExperienceOS_ServiceQuote_v1.0_20260531.md | 服务报价 |
| SpecQ_ExperienceOS_CustomerShortlist_v1.0_20260531.md | 客户短名单 |

### 数据库设计

| 文档 | 说明 |
|---|---|
| SpecQ_v3.0.1_数据库设计.md | 数据库设计 v3.0.1 |
| SpecQ_v3.0.1_数据库设计_v3_MVP.md | MVP 版数据库设计 |
| SpecQ_v3.0.1_数据库设计_v4_MVP.md | MVP 版数据库设计 v4 |

### 管线

| 文档 | 说明 |
|---|---|
| SpecQ_v3.0.1_管线_OpenCode_Prompt_20260601.md | 管线 OpenCode Prompt |
| SpecQ_v3.0.1_数据入库管线管理设计文档_20260601.md | 管线设计 |
| SpecQ_数据采集执行规格_数据工程师版_20260601.md | 数据采集执行规格 |

### OpenCode Prompts（Bug 修复 / 功能开发）

| 阶段 | 文档数量 | 代表性文档 |
|---|---|---|
| Bug 修复 | ~15 份 | SpecQ_12bugs_fix_prompt.md, SpecQ_all_bugs_fix.md, SpecQ_P0_fix_prompt.md 等 |
| 功能开发 | ~10 份 | SpecQ_miniapp_OpenCode_Prompt_Part1/2.md, SpecQ_服务层升级_OpenCode_Prompt.md 等 |
| 认证/登录 | ~5 份 | SpecQ_认证系统修复_OpenCode_Prompt.md, SpecQ_login_prompt.md 等 |
| 测试 | ~4 份 | SpecQ_e2e_test_plan.md, SpecQ_final_test_report.md 等 |

### FAE Agent 历史（5/22 已闭环）

| 文档 | 说明 |
|---|---|
| FAE_issue_checklist.md | 53 项问题清单 |
| FAE_v1.0_产品手册.md | v1.0 技术规格 |
| FAE_v1.0_开发复盘.md | 58 问题全览 |
| FAE_v2.0_*.md | v2.0 设计文档 (~25 份) |
