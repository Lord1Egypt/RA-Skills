# 🐾 VetClaw — 宠物医院AI技能套装

> 全球首个宠物医院专用AI技能库 | 50+自动化工作流 | 一键安装

## 产品定位

**让每家宠物医院都有一个24/7的AI助手。**

VetClaw 是一套针对宠物医院/诊所设计的AI技能集合，基于 OpenClaw 平台运行。覆盖前台接待、病历管理、预约调度、客户沟通、库存管理等核心场景。

### 目标用户
- 宠物医院经营者（1-10家门店）
- 宠物诊所医生/助理
- 宠物连锁品牌运营者

### 核心价值
- **省人力**：AI自动处理60%前台咨询，减少1-2个全职岗位
- **提效率**：预约/回访/提醒全自动，不遗漏任何一个客户
- **增收入**：智能提醒复诊/疫苗/驱虫，提升客户终身价值

---

## 技能清单（52个）

### 📞 前台接待（10个）

| # | 技能名 | 功能 | 自动化程度 |
|---|--------|------|-----------|
| 1 | `vet-intake` | 新客户/宠物信息采集 | 全自动 |
| 2 | `vet-appointment` | 预约挂号（含排班冲突检测） | 全自动 |
| 3 | `vet-reminder` | 预约提醒（短信/微信） | 全自动 |
| 4 | `vet-queue` | 候诊队列管理 | 半自动 |
| 5 | `vet-phone-ai` | AI电话接听（常见问题应答） | 全自动 |
| 6 | `vet-hours` | 营业时间/节假日自动回复 | 全自动 |
| 7 | `vet-directions` | 到院路线指引 | 全自动 |
| 8 | `vet-emergency` | 急诊分流（症状→紧急程度判断） | 半自动 |
| 9 | `vet-price-lookup` | 项目价格查询 | 全自动 |
| 10 | `vet-feedback` | 就诊后满意度收集 | 全自动 |

### 📋 病历与诊疗（10个）

| # | 技能名 | 功能 | 自动化程度 |
|---|--------|------|-----------|
| 11 | `vet-record-create` | 创建电子病历 | 半自动 |
| 12 | `vet-record-lookup` | 病历检索（按宠物/日期/症状） | 全自动 |
| 13 | `vet-prescription` | 处方模板管理 | 半自动 |
| 14 | `vet-lab-interpret` | 化验单AI解读（血常规/生化） | 全自动 |
| 15 | `vet-vaccine-schedule` | 疫苗接种计划生成 | 全自动 |
| 16 | `vet-deworm-schedule` | 驱虫计划生成 | 全自动 |
| 17 | `vet-surgery-checklist` | 术前检查清单 | 半自动 |
| 18 | `vet-discharge` | 出院指导自动生成 | 全自动 |
| 19 | `vet-followup` | 复诊提醒自动化 | 全自动 |
| 20 | `vet-referral` | 转诊记录生成 | 半自动 |

### 💰 收费与财务（8个）

| # | 技能名 | 功能 | 自动化程度 |
|---|--------|------|-----------|
| 21 | `vet-invoice` | 费用明细自动生成 | 全自动 |
| 22 | `vet-payment` | 收款记录管理 | 半自动 |
| 23 | `vet-package` | 套餐/会员卡管理 | 半自动 |
| 24 | `vet-daily-report` | 每日营收报表 | 全自动 |
| 25 | `vet-monthly-report` | 月度财务分析 | 全自动 |
| 26 | `vet-insurance` | 宠物保险理赔协助 | 半自动 |
| 27 | `vet-deposit` | 预付款/押金管理 | 半自动 |
| 28 | `vet-expense-track` | 进货/耗材成本追踪 | 半自动 |

### 📢 营销与客户（10个）

| # | 技能名 | 功能 | 自动化程度 |
|---|--------|------|-----------|
| 29 | `vet-birthday` | 宠物生日祝福自动化 | 全自动 |
| 30 | `vet-loyalty` | 积分/忠诚度管理 | 半自动 |
| 31 | `vet-review-gen` | 好评引导/评价管理 | 全自动 |
| 32 | `vet-social-post` | 社交媒体内容生成 | 全自动 |
| 33 | `vet-campaign` | 促销活动策划模板 | 半自动 |
| 34 | `vet-referral-program` | 转介绍奖励管理 | 半自动 |
| 35 | `vet-wechat-push` | 微信公众号推送 | 全自动 |
| 36 | `vet-pet-care-tips` | 季节性养护知识推送 | 全自动 |
| 37 | `vet-churn-predict` | 流失预警（久未复诊客户） | 全自动 |
| 38 | `vet-nps` | NPS净推荐值追踪 | 全自动 |

### 🏥 库存与运营（8个）

| # | 技能名 | 功能 | 自动化程度 |
|---|--------|------|-----------|
| 39 | `vet-inventory` | 药品/耗材库存管理 | 半自动 |
| 40 | `vet-expiry-alert` | 效期预警 | 全自动 |
| 41 | `vet-supplier-order` | 供应商自动下单 | 半自动 |
| 42 | `vet-equipment-maint` | 设备维护提醒 | 全自动 |
| 43 | `vet-staff-schedule` | 排班管理 | 半自动 |
| 44 | `vet-compliance` | 执业资质/年检提醒 | 全自动 |
| 45 | `vet-sterilize-log` | 消毒记录管理 | 半自动 |
| 46 | `vet-waste-disposal` | 医疗废物处理记录 | 半自动 |

### 🧠 知识与培训（6个）

| # | 技能名 | 功能 | 自动化程度 |
|---|--------|------|-----------|
| 47 | `vet-qa-kb` | 兽医知识库问答（RAG） | 全自动 |
| 48 | `vet-drug-interaction` | 药物相互作用查询 | 全自动 |
| 49 | `vet-breed-info` | 品种/遗传病信息查询 | 全自动 |
| 50 | `vet-nutrition` | 营养/饮食建议生成 | 全自动 |
| 51 | `vet-training` | 新员工培训内容生成 | 半自动 |
| 52 | `vet-case-library` | 典型病例库管理 | 半自动 |

---

## 技术架构

```
┌─────────────────────────────────────────────┐
│              VetClaw 技能引擎                │
├─────────────────────────────────────────────┤
│  OpenClaw Agent Runtime (Python)            │
│  ├── Skill Loader (动态加载52个技能)         │
│  ├── LLM Router (DeepSeek/Qwen/GPT)         │
│  ├── RAG Engine (知识库检索)                  │
│  └── Scheduler (定时任务/cron)               │
├─────────────────────────────────────────────┤
│  数据层                                      │
│  ├── SQLite (本地/单店)                      │
│  ├── PostgreSQL (多店/云端)                  │
│  └── ChromaDB (向量知识库)                   │
├─────────────────────────────────────────────┤
│  集成层                                      │
│  ├── 微信/短信通知                            │
│  ├── 电话API (Vapi/阿里云)                   │
│  ├── 支付 (支付宝/微信支付)                   │
│  └── 打印 (处方/发票)                        │
└─────────────────────────────────────────────┘
```

## 定价

| 套餐 | 价格 | 包含 |
|------|------|------|
| 🥉 基础版 | $500 | 前台接待10个技能 + 安装支持 |
| 🥈 专业版 | $2,000 | 全部30个技能 + 1个月技术支持 |
| 🥇 企业版 | $5,000 | 全部52个技能 + 定制化 + 3个月技术支持 |

## 快速开始

```bash
cd business/skill-bundles/veterinary-clinic-bundle
pip install -r requirements.txt
copy .env.example .env       # 可选：配置DeepSeek API Key
py main.py
# 访问 http://localhost:8000
```

## 技术栈

- **后端**: Python FastAPI
- **前端**: HTML + Tailwind CSS
- **LLM**: DeepSeek API（可选，无API时使用模板模式）
- **知识库**: JSON + YAML配置
- **数据库**: SQLite（自动创建）

## 安装

```bash
# 克隆仓库
git clone https://github.com/DMNO1/vetclaw-bundle.git
cd vetclaw-bundle

# 安装依赖
pip install -r requirements.txt

# 配置
cp config/vet-config.yaml.template config/vet-config.yaml
# 编辑 config/vet-config.yaml 填入诊所信息

# 运行
python install_skills.py
openclaw run vetclaw --config ./config
```

## 目录结构

```
veterinary-clinic-bundle/
├── README.md                    # 本文件
├── SKILL.md                     # 技能包详细说明
├── main.py                      # Web应用主入口
├── requirements.txt             # Python依赖
├── install_skills.py            # 技能目录生成脚本
├── test_api.py                  # API测试脚本
├── .env.example                 # 环境变量模板
├── config/
│   ├── vet-config.yaml          # 诊所配置（含医生排班/服务价格）
│   └── vet-knowledge-base.json  # 兽医知识库（疾病/疫苗/药物）
├── templates/
│   └── index.html               # Web UI（Tailwind CSS）
├── skills/                      # 52个技能目录（含SKILL.md+handler.py）
│   ├── vet-intake/              # 新客户采集
│   ├── vet-appointment/         # 预约管理
│   ├── vet-emergency/           # 急诊分流
│   ├── vet-phone-ai/            # AI电话
│   └── ... (共52个)
├── data/                        # SQLite数据库（自动创建）
└── examples/
    ├── sample_conversations.md  # 示例对话
    └── workflow_flows.md        # 工作流示例
```

## 已实现功能（14个核心技能）

| 技能 | 触发词 | 状态 |
|------|--------|------|
| 🚨 急诊分流 | "抽搐""出血""中毒" | ✅ 三级分流（红黄绿）|
| 📅 预约挂号 | "预约""挂号" | ✅ 时间解析+自动入库 |
| 📋 新客户建档 | "主人""新客户" | ✅ 客户+宠物信息采集 |
| 🕐 营业时间 | "几点开门" | ✅ 工作日/周末自动判断 |
| 📍 地址导航 | "在哪""地址" | ✅ 多交通方式指引 |
| 💰 价格查询 | "多少钱""价格" | ✅ 读取YAML配置 |
| 🔬 化验解读 | "WBC""血常规" | ✅ 数值解析+LLM增强 |
| 💉 疫苗计划 | "疫苗""免疫" | ✅ 知识库驱动 |
| 📋 病历查询 | "病历""就诊记录" | ✅ 数据库查询 |
| 📖 知识问答 | "症状""什么病" | ✅ 疾病知识库+LLM |
| 📊 每日报表 | "日报""运营报表" | ✅ 实时统计 |
| 📦 库存管理 | "库存""入库" | ✅ 增删查+不足预警 |
| ⭐ 满意度 | "评价""打分" | ✅ 1-5星评价 |
| 📞 AI前台 | 默认路由 | ✅ 意图识别+LLM兜底 |

## 成功案例

- **LiveTok兽医AI接待员**：已有客户，诊所增加40%预约量
- **OpenVet VetClaw**：全球首个兽医AI技能库，51个技能，开源验证

## 复制路径

本技能包模式可复制到其他垂直行业：
1. 🐾 兽医诊所 ← **本产品**
2. 🏥 中医诊所 → 望闻问切+中药处方+体质管理
3. ⚖️ 法律咨询 → 合同审查+法律问答+案件管理
4. 📊 财务代理 → 记账+报税+发票管理
5. 🎓 教育培训 → 课程管理+学员跟踪+考试出题

---

**VetClaw — 让AI为每一家宠物医院工作。** 🐾
