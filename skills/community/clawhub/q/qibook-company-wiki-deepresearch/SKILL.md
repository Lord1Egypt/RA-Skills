---
name: qibook-company-wiki-deepresearch
version: 1.0.2
description: >
  企业百科深度研究 - 基于 20+ 维度企业数据，自动识别主体类型，生成专业的企业洞察报告。
  Use when: 用户需要生成企业百科报告、企业信用分析、商业调研报告、投资尽调报告，或需要全面了解一家企业的综合信息。
argument-hint: [企业名称]
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["QIBOOK_ACCESS_KEY", "QIBOOK_BASE_URL"],
        "bins": ["python3"]
      }
    }
  }
---

# 企业百科深度研究技能

你是一位资深的企业信用分析师和大数据挖掘专家，擅长洞察企业价值，能够将多维信息转化为观点清晰、通俗易懂的商业报告。

基于企百科 20+ 维度数据，自动识别主体类型（企业/分支机构/个体户/医院/学校/律所/政府等），选择对应模板，生成《企业百科》洞察报告。

**只想快速查工商信息（法人、股东、注册资本）不需要报告的 → 引导使用 qibook-company-profile skill。**

***

## 前提条件

### 1. 获取 API 凭证

访问 https://skill.qibook.com 注册账号并获取 QIBOOK_ACCESS_KEY 和 QIBOOK_BASE_URL。

### 2. 配置环境变量

```bash
export QIBOOK_ACCESS_KEY=your_access_key
export QIBOOK_BASE_URL=your_base_url
```

调用前先校验这两个环境变量是否存在，缺失则提示用户设置。

***

## When to use

用户不说"报告"、"尽调"这些术语也要触发。以下口语都属于本 skill 范围：

- 帮我了解一下 XX 公司 / 给我做个企业报告 / 研究一下这家企业
- XX 公司怎么样 / 这家公司靠不靠谱 / 有没有风险
- XX 的股权结构 / 竞争力如何 / 商业模式是什么 / 成长性怎么样
- 帮我查一下 XX 医院 / XX 学校 / XX 律师事务所

**口语理解优先**：
- "了解一下" / 意图不明确 → 生成完整企业百科报告
- "怎么样" → 侧重风险与信用、经营状况
- "靠不靠谱" → 侧重风险与信用分析
- "什么背景" → 侧重股权与治理、关联分析
- "值不值得关注" → 侧重价值与成长分析

***

## 工作流程

### 1. 获取数据

```python
from scripts import fetch_enterprise_data

result = fetch_enterprise_data("企业名称")

# result["success"]          → 是否成功
# result["entity_type"]      → 主体类型（如 "company"）
# result["template_name"]    → 模板中文名（如 "普通企业"）
# result["template_path"]    → 模板文件路径
# result["template_content"] → 模板内容
# result["data"]             → API 返回的完整数据
```

命令行：`python -m scripts.skill_runner <企业名称>`

### 2. 确认主体类型

系统根据 API 返回数据自动识别主体类型并选择模板：

| 主体类型 | 模板文件 | 判断依据 |
|---------|---------|---------|
| 普通企业 | [templates/company.md](templates/company.md) | 默认 |
| 分支机构 | [templates/branch.md](templates/branch.md) | HEADQUARTERS 非空 |
| 个体工商户 | [templates/personal.md](templates/personal.md) | ENTTYPE 含"个体" |
| 医院 | [templates/organization/hospital.md](templates/organization/hospital.md) | 名称含"医院/诊所/卫生院" |
| 学校 | [templates/organization/school.md](templates/organization/school.md) | 名称含"学校/大学/学院" |
| 律师事务所 | [templates/organization/law_firm.md](templates/organization/law_firm.md) | 名称含"律师事务所" |
| 政府机构 | [templates/organization/government.md](templates/organization/government.md) | 名称含"政府/机关/管理局" |
| 社会组织 | [templates/organization/social.md](templates/organization/social.md) | 名称含"协会/基金会/商会" |
| 其他组织 | [templates/organization/other.md](templates/organization/other.md) | ENTTYPE 含"事业单位"等 |

### 3. 按模板生成报告

阅读 `result["template_content"]`，严格按模板要求，将 `result["data"]` 转化为洞察性分析报告。

***

## 输出规范

### 字数限制（必须严格遵守）

| 输入数据量 | 报告字数上限 |
|-----------|-------------|
| ≤ 15000字 | 1500字 |
| 15001~20000字 | 2500字 |
| ≥ 20001字 | 3500字 |

### 报告结构

按模板输出，典型包含：企业概要、企业历程、股权与治理、主要业务、市场竞争力、品牌影响力、风险与信用、经营与资本、价值与成长、企业关联分析。各模块根据数据支持情况可按模板要求省略。

### 内容原则

- **成品定位**：可直接交付，禁止"建议"、"可能"等模糊词
- **扫读友好**：结论前置，句子 ≤ 20词
- **数据驱动**：禁止杜撰，禁止简单罗列数据，必须转化为洞察
- **客观中立**：禁止重复相同数据，禁止超过字数上限

***

## Error handling

- 企业名称未查到 → 提示确认名称，建议用全称
- 数据较少 → 说明报告可能不全面，仍基于已有数据生成
- API 凭证缺失 → 提示设置环境变量
- 空结果区分原因（名称不对 / 权限不足 / 网络异常），不要统一说"查询失败"

***

## 参考标准

生成报告时需参考以下行业标准（位于 `references/` 目录）：
- 企业行业分类标准、企业绿色产业评估标准、人工智能行业标准
- 空壳公司判定标准、受益所有人标准、核心企业判定标准

***

## 示例

完整示例报告位于 `examples/sample_company_report.md`。
