---
name: ESG Investment Analysis Assistant
slug: security-esg-investing
description: AI-powered ESG investing analysis assistant — covers ESG rating analysis, green finance screening, carbon footprint assessment, and sustainable investment portfolio construction. Built for ESG analysts, sustainable fund managers, and institutional investors. Keywords: ESG investing, sustainability, green finance, carbon footprint, ESG rating, responsible investing, China ESG, ESG分析, 绿色金融, 可持续发展, 碳足迹, ESG评级, 碳中和, 绿色债券, ESG投资组合, 责任投资, 碳核算, 碳交易.
version: "3.0.1"
---

# ESG Investment Analysis Assistant / ESG投资分析助手

> **English:** AI-powered ESG investing analysis assistant — covers ESG rating comparison, green finance products, carbon accounting, and sustainable portfolio construction. Built for ESG analysts and sustainable investors.
>
> **中文:** ESG投资分析助手——覆盖ESG评级对比、绿色金融产品筛选、碳核算、可持续组合构建。适用：ESG分析师、可持续基金经理、机构投资者。

---


### 证券监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 证券监管 | 2026年Q1：ESG信息披露要求扩大至非上市企业 | ESG投资分析框架需更新最新信披要求和绿色金融政策 |
| 证券监管 | 绿色金融信贷导向政策升级，ESG投资环境改善 | ESG投资分析框架需更新最新信披要求和绿色金融政策 |
| 证券监管 | 证监会加强ESG相关信披监管，ESG评级标准趋严 | ESG投资分析框架需更新最新信披要求和绿色金融政策 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **ESG数据分散** | 评级机构超过10家，标准不统一 | 跨评级对比框架+综合评分 |
| **"漂绿"风险** | 虚假绿色宣传导致合规风险 | 实质性分析+数据核实 |
| **碳核算复杂** | Scope 1/2/3核算专业门槛高 | 分级碳核算模板+简化方法 |
| **政策变化快** | 碳市场/ESG披露要求频繁更新 | 实时政策跟踪+合规提醒 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** ESG investing, sustainability, green finance, carbon footprint, ESG rating, responsible investing, ESG analysis, carbon trading, sustainable portfolio, China ESG

**中文触发词（优先）：** ESG投资 / 可持续发展 / 绿色金融 / 碳足迹 / ESG评级 / 责任投资 / ESG分析 / 碳交易 / 可持续组合 / 碳中和 / 碳达峰 / 绿色债券 / ESG披露 / MSCI ESG / 责任投资 / 影响力投资

---

## Core Capabilities / 核心能力

### 1. ESG Rating Analysis / ESG评级分析

```python
class ESGAnalyzer:
    """ESG评级分析"""
    
    RATING_PROVIDERS = {
        "MSCI": {"scale": "CCC-AAA", "weight": {"E": 0.25, "S": 0.25, "G": 0.50}},
        "Sustainalytics": {"scale": "0-100", "weight": {"E": 0.33, "S": 0.33, "G": 0.33}},
        "商道融绿": {"scale": "D-A+", "weight": {"E": 0.30, "S": 0.30, "G": 0.40}},
        "中证ESG": {"scale": "C-AAA", "weight": {"E": 0.20, "S": 0.20, "G": 0.60}}
    }
    
    def normalize_rating(self, provider: str, raw_score: float) -> float:
        """标准化评分到0-100"""
        if provider == "MSCI":
            scale = {"CCC": 10, "B": 20, "BB": 35, "BBB": 50, "A": 65, "AA": 80, "AAA": 95}
            return scale.get(raw_score, 50)
        elif provider == "Sustainalytics":
            return 100 - raw_score  # 反转，风险分数→ESG分数
        elif provider == "商道融绿":
            scale = {"D": 20, "C": 40, "B": 60, "B+": 70, "A": 85, "A+": 95}
            return scale.get(raw_score, 50)
        return raw_score
    
    def comprehensive_analysis(self, company: str, 
                               ratings: dict) -> dict:
        """综合ESG分析"""
        normalized = {
            provider: self.normalize_rating(provider, score)
            for provider, score in ratings.items()
        }
        
        # 加权综合评分
        weights = [0.30, 0.25, 0.25, 0.20]  # 权重分配
        providers = list(normalized.keys())
        comprehensive = sum(
            normalized[p] * w 
            for p, w in zip(providers, weights)
        )
        
        return {
            "comprehensive_score": round(comprehensive, 1),
            "rating_level": self._score_to_level(comprehensive),
            "individual_ratings": normalized,
            "key_strengths": self._identify_strengths(normalized),
            "key_concerns": self._identify_concerns(normalized),
            "peer_comparison": self._compare_to_peer(company, comprehensive)
        }
    
    def _score_to_level(self, score: float) -> str:
        levels = {
            (90, 100): "AAA - 卓越",
            (80, 90): "AA - 优秀",
            (70, 80): "A - 良好",
            (60, 70): "BBB - 平均偏上",
            (50, 60): "BB - 平均",
            (40, 50): "B - 低于平均",
            (0, 40): "CCC/B - 落后"
        }
        for (low, high), level in levels.items():
            if low <= score <= high:
                return level
        return "未知"
```

### 2. Carbon Footprint Analysis / 碳足迹分析

```python
class CarbonAnalyzer:
    """碳足迹核算"""
    
    def calculate_carbon_footprint(self, company_data: dict) -> dict:
        """
        计算碳足迹（Scope 1, 2, 3）
        """
        # Scope 1: 直接排放
        scope1 = (
            company_data.get("fuel_combustion", 0) * 2.02 +  # CO2系数
            company_data.get("vehicle_fleet", 0) * 2.32 +
            company_data.get("fugitive_emissions", 0) * 25  # CH4当量
        )
        
        # Scope 2: 间接排放（电力）
        scope2 = (
            company_data.get("electricity_kwh", 0) * 
            company_data.get("grid_emission_factor", 0.68)  # 中国电网系数
        )
        
        # Scope 3: 价值链排放（简化版）
        scope3 = {
            "上游采购": company_data.get("purchased_goods", 0) * 0.5,
            "运输配送": company_data.get("transportation", 0) * 0.1,
            "员工通勤": company_data.get("employee_commute", 0) * 0.02,
            "产品使用": company_data.get("product_use", 0) * 0.8,
            "报废处理": company_data.get("end_of_life", 0) * 0.05
        }
        
        total_scope3 = sum(scope3.values())
        
        return {
            "scope1_tCO2e": round(scope1, 2),
            "scope2_tCO2e": round(scope2, 2),
            "scope3_tCO2e": round(total_scope3, 2),
            "total_emissions": round(scope1 + scope2 + total_scope3, 2),
            "intensity_metrics": {
                "per_revenue": round((scope1+scope2+total_scope3) / 
                                    max(company_data.get("revenue_yuan", 1), 1) * 1e6, 2),  # tCO2e/百万营收
                "per_employee": round((scope1+scope2+total_scope3) / 
                                      max(company_data.get("employees", 1), 1), 2)  # tCO2e/人
            },
            "scope_breakdown": {
                "Scope 1": round(scope1/(scope1+scope2+total_scope3+0.001)*100, 1),
                "Scope 2": round(scope2/(scope1+scope2+total_scope3+0.001)*100, 1),
                "Scope 3": round(total_scope3/(scope1+scope2+total_scope3+0.001)*100, 1)
            }
        }
```

### 3. Green Bond Analysis / 绿色债券分析

```markdown
## 绿色债券投资分析框架

### 一、绿色债券认定
| 标准 | 中国绿债标准 | 国际标准（GBP） |
|-----|------------|---------------|
| 募集资金用途 | ≥80%用于绿色项目 | ≥95%用于绿色项目 |
| 项目评估 | 需第三方认证 | 需外部评审 |
| 信息披露 | 年度+事件披露 | 发行时+续存期披露 |

### 二、绿色债券筛选矩阵
- [ ] 是否获得绿色债券认证
- [ ] 第三方认证机构资质
- [ ] 募集资金用途透明度
- [ ] 环境效益量化指标
- [ ] 续存期管理机制

### 三、环境效益量化
```python
def calculate_green_benefits(bond_data: dict) -> dict:
    """计算绿色债券环境效益"""
    green_proceeds = bond_data["total_amount"] * bond_data["green_ratio"]
    
    benefits = {
        "annual_co2_reduction": green_proceeds / 10000 * bond_data["carbon_factor"],  # 吨CO2/年
        "annual_energy_saving": green_proceeds / 10000 * bond_data["energy_factor"],  # 吨标煤/年
        "equivalent_forests": green_proceeds / 10000 * bond_data["forest_factor"]  # 相当于造林面积(公顷)
    }
    
    return benefits
```
```

---

## Disclaimer

This skill provides ESG analysis tools for educational purposes. ESG ratings and analysis are for reference only and should be combined with other investment research methods.
