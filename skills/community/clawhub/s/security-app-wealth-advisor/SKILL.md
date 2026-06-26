---
name: Bank APP Wealth Advisor Assistant
slug: bank-app-wealth-advisor
description: AI-powered bank APP wealth advisory assistant — covers product recommendation, investment consultation, financial planning, and compliance-compliant customer interaction for bank mobile applications. Built for China commercial bank digital banking teams and wealth management advisors. Keywords: bank APP, wealth advisor, digital banking, mobile banking, AI advisor, product recommendation, China banking digital, 银行APP, 财富顾问, 智能投顾, 手机银行, 数字银行, 产品推荐, 理财推荐, 基金销售, 资产配置.
version: "3.0.1"

capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - no-executable-code
---

# Bank APP Wealth Advisor Assistant / 银行APP财富顾问助手
> **⚠️ SECURITY NOTICE**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries included**
> - **No persistent storage, network calls, or background execution**
> - **No credential collection, PII processing, or system access**
> - **All outputs require human review before real-world application**
> - **NOT financial, legal, or insurance advice**




### 银行监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 银行监管 | 2026年Q1理财信息披露'三清'推进，财富管理话术需更新 | 投顾话术和策略模板需适配市场新环境 |
| 银行监管 | 净息差压力下，银行理财产品收益率下行，投顾建议需调整 | 投顾话术和策略模板需适配市场新环境 |
| 银行监管 | 2026年A股量化资金占比30%-40%，财富管理策略需关注量化冲击 | 投顾话术和策略模板需适配市场新环境 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

> **English:** AI-powered wealth advisory assistant for bank mobile applications — provides product recommendations, investment consultation, and compliance-compliant customer interaction. Built for digital banking teams.
>
> **中文:** 银行APP财富顾问助手——为手机银行提供产品推荐、投资咨询、合规客户交互。适用：数字银行团队、财富管理师。

---

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **APP用户粘性低** | 用户用完即走，无深度服务 | AI投顾提升个性化体验 |
| **产品匹配效率低** | 人工推荐成本高 | 智能产品匹配引擎 |
| **合规要求严** | 监管禁止虚假宣传 | 合规话术自动检查 |
| **服务覆盖有限** | 人工客服无法7x24 | AI24小时在线解答 |
| **交叉销售难** | 客户画像不完整 | 多维度客户分析 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** bank APP, wealth advisor, digital banking, mobile banking, AI advisor, product recommendation, financial planning, customer service

**中文触发词（优先）：** 银行APP / 财富顾问 / 智能投顾 / 手机银行 / 数字银行 / 产品推荐 / 理财咨询 / 基金销售 / 资产配置 / 客户分层 / 交叉销售 / 合规话术 / 智能客服 / 风险测评 / 适当性匹配

---

## Core Capabilities / 核心能力

### 1. Product Matching Engine / 产品匹配引擎

```python
class WealthAdvisor:
    """智能财富顾问"""
    
    def match_products(self, customer_profile: dict, 
                      available_products: list) -> list:
        """
        智能产品匹配
        Args:
            customer_profile: 客户画像
            available_products: 可选产品列表
        """
        # 风险匹配
        risk_level_map = {
            "保守型": ["R1", "R2"],
            "稳健型": ["R1", "R2", "R3"],
            "平衡型": ["R2", "R3", "R4"],
            "成长型": ["R3", "R4", "R5"],
            "激进型": ["R4", "R5"]
        }
        
        allowed_risk = risk_level_map.get(
            customer_profile.get("risk_preference", "稳健型"), ["R2", "R3"]
        )
        
        # 收益匹配
        expected_return = customer_profile.get("expected_return", 0.05)
        
        matched = []
        for product in available_products:
            # 风险等级过滤
            if product["risk_level"] not in allowed_risk:
                continue
            
            # 收益率匹配
            if product["expected_return"] >= expected_return - 0.02:
                score = self._calculate_match_score(
                    customer_profile, product
                )
                matched.append({
                    **product,
                    "match_score": score,
                    "recommendation_reason": self._generate_reason(
                        customer_profile, product
                    )
                })
        
        return sorted(matched, key=lambda x: x["match_score"], reverse=True)
    
    def _calculate_match_score(self, customer: dict, 
                               product: dict) -> float:
        """计算匹配度评分"""
        score = 100
        
        # 期限匹配
        preferred_term = customer.get("preferred_term", 365)
        product_term = product.get("term_days", 365)
        term_diff = abs(preferred_term - product_term) / 365
        score -= term_diff * 10
        
        # 起购金额
        if product.get("min_amount", 0) > customer.get("available_fund", 0):
            score -= 30
        
        # 收益率
        expected = customer.get("expected_return", 0.05)
        actual = product.get("expected_return", 0)
        if actual >= expected:
            score += 10
        else:
            score -= abs(actual - expected) * 100
        
        return max(0, min(100, score))
```

### 2. Investment Consultation Scripts / 投资咨询话术

```python
INVESTMENT_SCRIPTS = {
    "基金购买引导": {
        "场景": "客户咨询基金",
        "话术": """
        "您好！根据您的风险测评结果【{risk_level}】，
        我推荐您关注【{fund_name}】基金。
        
        这只基金的特点：
        • 基金类型：{fund_type}
        • 风险等级：{risk_level}
        • 近一年收益：{return_1y}%
        • 基金经理：{manager}（从业{years}年）
        
        适合您的理由：
        1. {reason_1}
        2. {reason_2}
        3. {reason_3}
        
        【风险提示】基金有风险，投资需谨慎。过往业绩不代表未来表现。
        请您根据自身情况谨慎决策。"
        """,
        "合规检查": [
            "不得承诺保本",
            "必须说明基金有风险",
            "过往业绩仅供参考"
        ]
    },
    
    "资产配置建议": {
        "场景": "客户有大额资金",
        "话术": """
        "张先生/女士，您好！
        
        根据您目前的资产状况，我们建议做一个科学的资产配置：
        
        【保守配置】40% → 银行存款+国债
        特点：安全稳健，适合保本需求
        
        【稳健配置】30% → 银行理财+债券基金
        特点：收益稳健，波动较小
        
        【成长配置】20% → 混合基金+股票基金
        特点：追求较高收益，承担一定风险
        
        【流动性】10% → 货币基金
        特点：随存随取，应急备用
        
        这个配置方案可以帮助您分散风险，
        同时实现资产的稳健增值。"
        """
    }
}
```

### 3. Compliance Check / 合规检查

```markdown
## APP投顾合规检查清单

### 必须包含的要素
| 检查项 | 要求 |
|-------|------|
| 风险提示 | 必须出现"投资有风险" |
| 收益说明 | 不得承诺保本保收益 |
| 历史业绩 | 必须注明"仅供参考" |
| 适当性 | 必须匹配客户风险等级 |
| 产品揭示 | 必须包含产品说明书链接 |

### 禁止用语
| 禁止 | 替代 |
|-----|------|
| "保本" | "相对稳健" |
| "稳赚不赔" | "追求稳健收益" |
| "最低收益X%" | "历史平均收益X%" |
| "100%安全" | "风险可控" |
```

---

## Disclaimer

This skill provides wealth advisory tools for educational purposes. All recommendations must comply with applicable regulations and be reviewed by qualified financial advisors.
