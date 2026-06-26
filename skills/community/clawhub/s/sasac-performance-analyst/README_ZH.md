# 国资委企业绩效评价智能分析SKILL v2.0

> 🇨🇳 基于国务院国资委《企业绩效评价标准值（2025）》的企业绩效对标评价智能分析系统

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-已发布-green.svg)](https://clawhub.ai/yjkj999999/sasac-performance-analyst)
[![Version](https://img.shields.io/badge/版本-2.0.0-orange.svg)](https://github.com/yjkj999999/sasac-performance-analyst)

## 🌟 概述

**国资委绩效分析师（SASAC Performance Analyst）** 是一款专业的企业绩效对标评价AI技能，基于国务院国资委考核分配局发布的权威数据《企业绩效评价标准值（2025年版）》构建。

## ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 🔍 **精准对标** | 输入指标数值，自动判定优秀/良好/中等/较低/较差五档位 |
| 📊 **四维诊断** | 盈利回报、资产运营、风险防控、持续发展四维雷达图分析 |
| 📈 **评分引擎** | 五档线性插值评分，权重可配置 |
| 📋 **报告生成** | 综合评价报告（HTML/PDF/腾讯文档） |
| 🌍 **国际对标** | 19个行业国际标准值（2024）对标 |
| 📄 **招股书解析** | 港交所IPO招股书财务数据自动提取 |
| 🔗 **跨境上市评估** | 国企港股上市可行性评估 |

## 📊 数据覆盖

- **332个标准值表**（国内314 + 国际18）
- **10大行业门类**、48个行业中类、107个行业小类
- **24项评价指标**（16项核心 + 8项补充）
- **5个评价等级**：优秀、良好、中等、较低、较差
- **4种规模分类**：全行业、大型、中型、小型

## 🚀 快速开始

### 安装

```bash
# 通过 SkillHub 安装（推荐）
skillon install sasac-performance-analyst

# 通过 ClawHub 安装
openclaw skills install sasac-performance-analyst

# 手动安装
git clone https://github.com/yjkj999999/sasac-performance-analyst.git ~/.qclaw/skills/sasac-performance-analyst/
```

### 使用示例

```
用户：我是一家大型医药工业企业，净资产收益率15%，研发经费投入强度4%。

AI助手：
📊 【对标结果】
  净资产收益率(15%)：【良好值】区间（优秀17.1%，差距12%）
  研发经费投入强度(4%)：【中等值】区间（优秀7.9%，差距49%）

💡 【诊断结论】
  盈利能力良好，但研发投入不足，存在"重当期利润、轻长远发展"风险。

📋 【改进建议】
  1. 将研发投入提升至≥7.9%（优秀值）
  2. 建立研发投入考核机制
  3. 参考中国中车创新绩效评价案例
```

## 📊 评价维度与权重

| 维度 | 权重 | 核心指标 |
|------|------|---------|
| 💰 盈利回报 | 30% | 净资产收益率、营业收入利润率、总资产报酬率、盈余现金保障倍数 |
| ⚙️ 资产运营 | 20% | 总资产周转率、应收账款周转率、流动资产周转率、两金占比 |
| 🛡️ 风险防控 | 25% | 资产负债率、现金流动负债比率、带息负债比率、已获利息倍数 |
| 🌱 持续发展 | 25% | 研发经费投入强度、全员劳动生产率、经济增加值率、国有资本保值增值率 |

## 🏗️ 架构设计

```
数据采集 → 指标计算 → 标杆评价 → 报告生成
  ├─ 巨潮网API     ├─ 24项公式      ├─ 行业匹配       ├─ HTML报告
  ├─ 港交所招股书   ├─ IFRS↔CAS调整  ├─ 规模判定       ├─ 雷达图
  └─ 手动输入       └─ 自动计算      └─ 五档线性插值    └─ CSV导出
```

## 📁 文件结构

```
sasac-performance-analyst/
├── SKILL.md                          # 技能定义
├── README.md                         # 英文说明
├── README_ZH.md                     # 本文件（中文说明）
├── package.json                     # 元数据
├── system_prompt.md                  # 系统提示词
├── data/
│   ├── sasac_2025_standards.json   # 国内标准值（314表）
│   ├── international_standards.json # 国际标准值（18表）
│   ├── industry_mapping.json        # 行业分类映射
│   ├── case_studies.json           # 最佳实践案例（5家）
│   ├── hk_ipo_db.json              # 港股IPO数据库
│   └── cross_listing_db.json       # 跨境上市评估库
├── tools/
│   ├── performance_calculator.py    # 绩效计算引擎
│   ├── visualization.py             # 可视化工具
│   ├── financial_data_extractor.py # 财务数据提取
│   ├── hk_ipo_integration.py       # 港股集成
│   └── report_generator.py         # 报告生成
├── templates/
│   └── report_template.html        # 报告模板
└── html/
    └── sasac_performance_query_2025.html  # 交互式查询系统
```

## 📜 许可证

MIT License — 详见 [LICENSE](LICENSE)

## 👤 作者

**王东杰 (Wang Dongjie)**
- 职务：CFO首席财务官 | 资深复合型战略财务专家 | CGMA持证人
- 邮箱：Wdj_@163.com
- GitHub: [@yjkj999999](https://github.com/yjkj999999)

## 🙏 致谢

- 国务院国资委考核分配局（数据来源）
- 经济科学出版社（出版单位）
- AICPA & CIMA（CGMA知识体系）
- 香港交易所（IPO数据）
