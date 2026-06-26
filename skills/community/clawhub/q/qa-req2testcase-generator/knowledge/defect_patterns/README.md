# L4 历史缺陷库

> 版本：1.0.0
> 创建时间：2026-04-18
> 数据来源：2025年所有项目缺陷清单.xlsx
> 状态：已完成，可用于 RAG 召回

## 用途

本目录包含公司 2025 年历史缺陷数据，内置于公司版 Skill，辅助 AI 识别高风险测试点。

主要注入 P1（功能点树）、P2（测试点草案）、P3（风险识别）步骤，帮助 AI 基于历史缺陷经验主动识别高风险场景。

## 数据概况

- 总缺陷数：3418 条
- 项目数：11 个
- 时间范围：2023~2025 年（以 2025 年为主）

## 项目清单

| 项目 | 业务域 | 缺陷数 |
|------|--------|--------|
| 优理宝移动终端 | trade（交易） | 1132 |
| 财富梦工厂 | asset_mgmt（资管） | 759 |
| 资产托管部综合管理平台 | clearing（清算） | 294 |
| 集团CRM | crm | 287 |
| 智达APP | trade（交易） | 225 |
| 数据仓库项目 | data | 195 |
| 差异化交易SMT | trade（交易） | 158 |
| 大投行业务管理系统 | investment_banking | 156 |
| 金融科技中台 | platform | 136 |
| Smart Station系统建设项目 | platform | 48 |
| 场外衍生品综合管理系统 | derivatives | 28 |

## 文件结构

```
defect_patterns/
├── project_index.json          # 项目名称索引（11个项目）
├── defects_by_domain/          # 按业务域分类
│   ├── trade.txt             # 交易域（1515条）
│   ├── asset_mgmt.txt        # 资管域（759条）
│   ├── clearing.txt          # 清算域（294条）
│   ├── crm.txt               # CRM（287条）
│   ├── data.txt              # 数据（195条）
│   ├── investment_banking.txt # 投行（156条）
│   ├── platform.txt          # 平台（184条）
│   └── derivatives.txt       # 衍生品（28条）
└── defects_by_type/            # 按缺陷类型分类
    ├── functional.txt        # 功能缺陷（3097条）
    ├── ui.txt                # UI界面（123条）
    ├── requirement.txt       # 需求问题（71条）
    ├── compatibility.txt     # 兼容性（33条）
    ├── performance.txt       # 性能（29条）
    ├── data.txt              # 数据问题（23条）
    └── ...
```

## 缺陷记录字段说明

| 字段 | 说明 |
|------|------|
| defect_id | 缺陷 ID（JIRA issue ID） |
| issue_code | JIRA issue 编号 |
| project | 所属项目 |
| module | 所属模块（父 issue 标题） |
| domain | 业务域（trade/clearing/asset_mgmt/crm/data/platform/derivatives） |
| defect_type | 缺陷类型（functional/ui/performance/security/compatibility/reliability/data/requirement/integration） |
| severity | 严重程度（P0/P1/P2/P3） |
| title | 缺陷标题 |
| description | 缺陷描述 |
| test_point_hint | 测试点提示（自动生成） |
| created_date | 创建日期 |
| archived | 是否归档（超3年标记为true） |

## 更新规则

- 每月增量更新：运行 `tools/defect_ingest.py --incremental` 追加新缺陷
- 每半年清理：超过3年的缺陷标记 archived=true，不参与召回
- 更新后在 knowledge/CHANGELOG.md 中记录
