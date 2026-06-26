# SKILL.md

## name

张氏财报分析实战操作手册-零会计基础极速排雷

## description

将张新民教授财务分析框架落地为**可直接执行的查表、计算、定性三步法**。使用者无需深厚会计基础，只需按图索骥在指定报表提取特定科目，通过简单加减乘除即可快速完成：利润真实性验证、产业链话语权判断、财务造假与巨亏隐患排查、管理效能评估、集团管控穿透等核心分析任务，精准还原企业真实经营状况。

## instructions

### 核心原则

1. **先提取后计算**：严格按照步骤从对应报表提取指定科目，不随意增减

2. **常识优先**：任何违背基本商业逻辑的数据异常，都是最高优先级风险信号

3. **交叉验证**：单一指标异常需结合其他子技能结果综合判断，避免误判

4. **聚焦本质**：所有分析最终指向"企业是否真的靠主业赚钱，且能持续赚钱"

---

### 子技能1：测算利润含金量（防纸面富贵）

**目标**：验证账面利润是否转化为真金白银

**操作步骤**：

1. 从利润表提取：`营业收入`、`营业成本`、`税金及附加`、`销售费用`、`管理费用`、`研发费用`、`利息费用`、`其他收益`

2. 计算核心利润：`核心利润 = 营业收入 - 营业成本 - 税金及附加 - 销售费用 - 管理费用 - 研发费用 - 利息费用`

3. 从现金流量表提取：`经营活动产生的现金流量净额`

4. 计算核心利润获现率：`核心利润获现率 = 经营活动产生的现金流量净额 / (核心利润 + 其他收益)`

**判定标准**：

- ✅ 健康区(1.2~1.5)：利润含金量极高，不仅全额变现还多收了预付款

- ⚠️ 预警区(0.8~1.2)：利润部分变现，存在一定应收账款或存货积压

- ❌ 高危区(<0.8)：利润多为"白条"或库存，随时可能发生坏账，高度警惕造假

---

### 子技能2：测算"两头吃"能力（断行业地位）

**目标**：判断企业在产业链中的议价能力

**操作步骤**：

1. 从资产负债表资产方提取并相加：`应收票据 + 应收账款 + 预付款项 + 合同资产`（别人欠你的钱）

2. 从资产负债表负债方提取并相加：`应付票据 + 应付账款 + 预收款项 + 合同负债`（你欠别人的钱）

**判定标准**：

- 上游话语权：`(应付票据+应付账款) 远大于 预付款项` → 能无偿占用供应商资金

- 下游话语权：`(预收款项+合同负债) 远大于 (应收票据+应收账款)` → 产品供不应求，客户提前打款

- 综合结论："你欠别人的钱"总额远大于"别人欠你的钱" → 产业链霸主，无息负债是最好的发展动力

---

### 子技能3：极速排雷扫描（锁定造假与巨亏隐患）

**目标**：一眼识别最致命的财务风险

**操作步骤**：

1. **排雷1：存贷双高**

    - 提取：`货币资金`、`短期借款`、`长期借款`、`利息费用`

    - 判定：巨额货币资金+高额有息负债+大额利息支出 → 资金可能被挪用、冻结或造假

2. **排雷2：商誉黑洞**

    - 提取：`商誉`、`资产总额`

    - 计算：`商誉占比 = 商誉 / 资产总额`

    - 判定：商誉占比>20%且被收购标的业绩下滑 → 存在巨额减值风险，可能瞬间吞噬利润

---

### 子技能4：穿透管理效能（查验营销与存货真相）

**目标**：检验营销投入有效性和产品销售能力

**操作步骤**：

1. **营销有效性**

    - 提取连续两年：`销售费用`、`营业收入`

    - 计算两者增长率

    - 判定：销售费用大幅增长但营收增长缓慢/下降 → 营销无效，产品竞争力衰退

2. **存货滞销风险**

    - 提取连续两年：`存货`、`营业收入`

    - 计算两者增长率

    - 判定：存货增速远大于营收增速 → 产品大量积压，未来可能计提巨额存货跌价准备

---

### 子技能5：解剖利润结构（查验"三支柱"与"两搅局"）

**目标**：识别盈利持续性，防范利润操纵

**操作步骤**：

1. **三支柱（利润来源）**

    - 提取：核心利润（子技能1计算）、其他收益、投资收益及公允价值变动收益

    - 判定：核心利润占比<50% → 主业失能，盈利不可持续

2. **两搅局（利润操纵）**

    - 提取：`资产减值损失`、`信用减值损失`

    - 判定：换帅/业绩低迷年份出现巨额减值 → 大概率是"财务洗澡"，为未来盈利腾空间

---

### 子技能6：检验资产质量（识别不良资产与结构失衡）

**目标**：区分能赚钱的"好资产"和拖后腿的"坏资产"

**操作步骤**：

1. **结构匹配度**

    - 提取：`固定资产`、`在建工程`、`营业收入`

    - 判定：固定资产/在建工程狂增但营收停滞 → 产能严重闲置，投资失误

2. **结构性盈利能力**

    - 计算：`经营资产报酬率 = (核心利润 + 其他收益) / 平均经营资产`（经营资产=总资产-货币资金-投资资产）

    - 判定：该指标长期低于行业平均 → 主业资产大而无当，缺乏竞争力

3. **个体保值性**

    - 结合：`资产减值损失`、`信用减值损失`

    - 判定：连续针对特定资产计提巨额减值 → 该部分资产已沦为不良资产

---

### 子技能7：高阶综合评价（融合杜邦与张氏框架）

**目标**：立体诊断企业问题根源

**操作步骤**：

1. 用杜邦体系找线索：提取`净资产收益率`、`总资产周转率`、`销售净利率`，定位异动指标

2. 用张氏框架查病因：

    - 总资产周转率下降 → 排查资产结构，是否过度投资或并购拖累

    - 销售净利率下降 → 解剖利润结构，是否主业衰退或减值操纵

3. 母子报表交叉验证定前景：判断企业是"经营主导"还是"投资主导"，评估造血可持续性

---

### 子技能8：母子报表交叉验证（透视集团管控）

**目标**：识别集团资金流向、融资模式和业务关系

**操作步骤**：

1. **资金管控模式**

    - 对比：母公司与合并报表的`其他应付款`、`其他应收款`

    - 判定：母公司其他应付款>>合并 → 资金高度集权（子公司资金被集中）；母公司其他应收款>>合并 → 母公司向子公司输血

2. **融资主导权**

    - 对比：两表的`短期借款`、`长期借款`、`利息费用`

    - 判定：合并负债>>母公司 → 子公司分权融资；反之则为母公司统贷统还

3. **业务依存度**

    - 对比：两表的`营业收入`、`营业成本`

    - 判定：合并收入≈母公司收入 → 子公司是配套帮手；合并收入>>母公司收入 → 子公司是独立诸侯

---

### 子技能9：透视成本决定机制（揪出隐性浪费与治理黑洞）

**目标**：从四个维度分析成本高企的真正原因

**操作步骤**：

1. **治理层成本**：查`其他应收款`（大股东欠款）、`预计负债`（违规担保）→ 大股东掏空是致命成本

2. **决策层成本**：对比同行业`折旧摊销`、`研发费用`、`职工薪酬`→ 战略决策锁定基本成本框架

3. **管理层成本**：查`存货周转率`、行政管理费用→ 日常管理不善造成隐性浪费

4. **核算层成本**：查`会计估计变更`、`资产减值损失`→ 警惕通过会计手段人为调节成本

---

### 子技能10：商业债权穿透（揪出"团伙作案"与"内鬼"）

**目标**：识别虚构交易和利益输送

**操作步骤**：

1. 查报表附注："按欠款方归集的期末余额前五名的应收账款/其他应收款"

2. 判定：债务人名称高度相似/注册地集中 → 可能是"团伙作案"配合虚构收入

3. 判定：刚发生的巨额债权直接计提100%坏账 → 本质是恶意资产掏空

4. 追溯业务经手人：特定人员频繁产生坏账 → 存在内外勾结利益输送

---

### 子技能11：拆解预算管理（透视内部利益博弈）

**目标**：通过资源倾斜判断管理层战略偏好和内部管控水平

**操作步骤**：

1. **一把手战略偏好**：资源向研发倾斜→技术驱动；向销售倾斜→营销驱动；向薪酬倾斜→人才驱动

2. **母子预算博弈**：子公司频繁借款且费用率失控 → 母公司预算管控失效

3. **预算心理弹性**：薪酬差旅适度增长且带动核心利润增长 → 预算管理健康有效

## input_schema

```JSON

{
  "type": "object",
  "properties": {
    "company_name": {
      "type": "string",
      "description": "上市公司全称或股票代码"
    },
    "analysis_year": {
      "type": "string",
      "description": "分析年度，如'2025年'或'2023-2025年'"
    },
    "financial_data": {
      "type": "object",
      "description": "可选，用户提供的具体财报数据，未提供则自动获取公开数据",
      "properties": {
        "income_statement": {"type": "object", "description": "利润表数据"},
        "balance_sheet": {"type": "object", "description": "资产负债表数据"},
        "cash_flow_statement": {"type": "object", "description": "现金流量表数据"},
        "notes": {"type": "object", "description": "报表附注关键数据"}
      }
    },
    "focus_skills": {
      "type": "array",
      "description": "可选，指定要执行的子技能编号，如[1,3,5]，默认执行全部11项",
      "items": {"type": "integer", "minimum": 1, "maximum": 11}
    }
  },
  "required": ["company_name", "analysis_year"]
}
```

## output_schema

```JSON

{
  "type": "object",
  "properties": {
    "core_conclusion": {
      "type": "string",
      "description": "一句话核心结论，明确企业整体财务状况和最大风险点"
    },
    "sub_skill_results": {
      "type": "object",
      "description": "各子技能执行结果，仅包含指定执行的子技能",
      "properties": {
        "profit_quality": {
          "type": "object",
          "description": "子技能1结果",
          "properties": {
            "core_profit": {"type": "number", "description": "核心利润（万元）"},
            "core_profit_cash_conversion": {"type": "number", "description": "核心利润获现率"},
            "assessment": {"type": "string", "description": "利润含金量评价"}
          }
        },
        "industry_position": {
          "type": "object",
          "description": "子技能2结果",
          "properties": {
            "receivables_total": {"type": "number", "description": "别人欠你的钱总额（万元）"},
            "payables_total": {"type": "number", "description": "你欠别人的钱总额（万元）"},
            "upstream_power": {"type": "string", "description": "上游话语权评价"},
            "downstream_power": {"type": "string", "description": "下游话语权评价"},
            "overall_position": {"type": "string", "description": "综合产业链地位评价"}
          }
        },
        "quick_risk_scan": {
          "type": "object",
          "description": "子技能3结果",
          "properties": {
            "deposit_loan_dual_high": {
              "type": "object",
              "properties": {
                "cash_balance": {"type": "number", "description": "货币资金（万元）"},
                "interest_bearing_debt": {"type": "number", "description": "有息负债总额（万元）"},
                "interest_expense": {"type": "number", "description": "利息费用（万元）"},
                "risk_level": {"type": "string", "description": "风险等级：无/低/中/高/极高"}
              }
            },
            "goodwill_risk": {
              "type": "object",
              "properties": {
                "goodwill_balance": {"type": "number", "description": "商誉余额（万元）"},
                "goodwill_ratio": {"type": "number", "description": "商誉占总资产比例"},
                "risk_level": {"type": "string", "description": "风险等级：无/低/中/高/极高"}
              }
            }
          }
        },
        "management_efficiency": {"type": "object", "description": "子技能4结果"},
        "profit_structure": {"type": "object", "description": "子技能5结果"},
        "asset_quality": {"type": "object", "description": "子技能6结果"},
        "comprehensive_diagnosis": {"type": "object", "description": "子技能7结果"},
        "group_control": {"type": "object", "description": "子技能8结果"},
        "cost_analysis": {"type": "object", "description": "子技能9结果"},
        "receivables_risk": {"type": "object", "description": "子技能10结果"},
        "budget_management": {"type": "object", "description": "子技能11结果"}
      }
    },
    "comprehensive_risk_assessment": {
      "type": "array",
      "description": "综合风险评估，按风险等级排序",
      "items": {
        "type": "object",
        "properties": {
          "risk_level": {"type": "string", "description": "风险等级：低/中/高/极高"},
          "risk_description": {"type": "string", "description": "风险点描述"},
          "evidence": {"type": "string", "description": "数据证据"},
          "potential_impact": {"type": "string", "description": "潜在影响"}
        }
      }
    },
    "final_suggestion": {
      "type": "string",
      "description": "最终风险提示与行动建议"
    }
  },
  "required": ["core_conclusion", "sub_skill_results", "comprehensive_risk_assessment", "final_suggestion"]
}
```

## examples

### 输入示例

```JSON

{
  "company_name": "XX科技",
  "analysis_year": "2025年",
  "focus_skills": [1, 2, 3, 5]
}
```

### 输出示例

```JSON

{
  "core_conclusion": "XX科技2025年主业盈利能力严重下滑，利润含金量极低，存在明显的商誉减值风险，最大隐患是盈利不可持续且现金流持续恶化",
  "sub_skill_results": {
    "profit_quality": {
      "core_profit": 5200,
      "core_profit_cash_conversion": 0.32,
      "assessment": "利润含金量极差，近70%的利润未转化为现金，主要体现为应收账款增加"
    },
    "industry_position": {
      "receivables_total": 85000,
      "payables_total": 32000,
      "upstream_power": "较弱，对供应商议价能力不足",
      "downstream_power": "极弱，大量采用赊销模式",
      "overall_position": "产业链弱势地位，被上下游双向挤压"
    },
    "quick_risk_scan": {
      "deposit_loan_dual_high": {
        "cash_balance": 12000,
        "interest_bearing_debt": 68000,
        "interest_expense": 4200,
        "risk_level": "中"
      },
      "goodwill_risk": {
        "goodwill_balance": 95000,
        "goodwill_ratio": 0.28,
        "risk_level": "高"
      }
    },
    "profit_structure": {
      "core_profit_ratio": 0.35,
      "other_income_ratio": 0.42,
      "investment_income_ratio": 0.23,
      "assessment": "利润主要依赖政府补贴，主业已失去核心竞争力，盈利不可持续",
      "earnings_manipulation_risk": "低，未发现明显的财务洗澡迹象"
    }
  },
  "comprehensive_risk_assessment": [
    {
      "risk_level": "高",
      "risk_description": "商誉减值风险",
      "evidence": "商誉占总资产比例28%，2025年被收购子公司业绩未达承诺的60%",
      "potential_impact": "若全额计提商誉减值，将导致公司当年亏损约9.5亿元"
    },
    {
      "risk_level": "高",
      "risk_description": "现金流断裂风险",
      "evidence": "核心利润获现率仅0.32，经营活动现金流连续两年为负",
      "potential_impact": "若无法获得外部融资，公司将面临资金链断裂风险"
    }
  ],
  "final_suggestion": "建议规避该公司股票，密切关注其商誉减值计提情况和现金流改善迹象，待主业盈利能力恢复后再重新评估"
}
```