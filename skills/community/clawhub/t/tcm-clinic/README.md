# 🏥 TCM Clinic - 中医诊所管理系统

一人中医诊所的全流程 AI 管理助手。患者建档、病历记录、中药库存、预约排班、财务收费，一句话搞定。

## ✨ 功能亮点

| 模块 | 功能 |
|------|------|
| 🏥 **患者档案** | 新增建档、模糊搜索、患者列表、过敏史/慢性病记录 |
| 📋 **病历记录** | 四诊信息（望闻问切）、辨证论治、处方记录、历史查询 |
| 🌿 **中药库存** | 入库管理、出库扣减、低库存预警、保质期监控 |
| 📅 **预约排班** | 新增预约、今日队列、状态管理（待诊/已诊/取消） |
| 💰 **财务收费** | 多类型收费（挂号/药费/针灸）、日/月/患者维度统计 |

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install openpyxl
```

### 2. 初始化诊所数据

```bash
python3 scripts/clinic_manager.py init
```

### 3. 开始使用（自然语言对话）

直接告诉 AI 助手你要做什么：

```
"帮我登记一个新患者，张三，男，45岁，电话13800138000"
"查一下李梅的历史病历"
"黄芪入库500克，进货价0.15元/克"
"看看今天有哪些预约"
"生成本月的收入统计报表"
"接诊张三，主诉头痛三日"
```

## 📁 数据存储

所有数据以 Excel 文件存储在 `clinic_data/` 目录下：

```
clinic_data/
├── patients.xlsx          # 患者信息表
├── medical_records.xlsx   # 病历记录表
├── herbs_inventory.xlsx   # 中药库存表
├── appointments.xlsx      # 预约排班表
└── finances.xlsx          # 财务记录表
```

## 🔧 脚本命令参考

也可以直接使用命令行脚本：

```bash
# 患者管理
python3 scripts/clinic_manager.py patients add --name "张三" --gender "男" --phone "13800138000"
python3 scripts/clinic_manager.py patients search --name "张"
python3 scripts/clinic_manager.py patients list

# 中药库存
python3 scripts/clinic_manager.py herbs add --name "黄芪" --quantity 500 --unit "g"
python3 scripts/clinic_manager.py herbs alerts
python3 scripts/clinic_manager.py herbs update --herb-id "H001" --quantity -50

# 财务统计
python3 scripts/clinic_manager.py finance summary --period month --month 2026-04
```

## 💊 适用场景

- 🧑‍⚕️ 个体中医诊所日常经营管理
- 📊 诊所经营数据统计与分析
- 🌿 中药房的进销存管理
- 📅 患者预约与排班管理

## 📜 兼容平台

- [x] OpenClaw
- [x] 其他支持 SKILL.md 标准的 AI Agent

## 📄 许可

MIT License

---

**🚧 需要定制化功能？**

如需以下高级功能，欢迎联系：
- 常用方剂库 / 中药材数据库预置
- 医保对接
- 多诊所/多医生支持
- 小程序/Web 前端
- 数据备份与云同步

📌 **获取完整版 / 定制开发，请联系：slamw@126.com**
