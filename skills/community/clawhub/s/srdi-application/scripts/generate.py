#!/usr/bin/env python3
"""
专精特新企业申报材料智能生成引擎
基于2026年工信部最新政策，支持三个梯度认定材料的自动生成
"""

import json
import os
import sys
import io
from datetime import datetime

# Windows GBK encoding fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# ─── 政策规则引擎 ───

POLICY_2026 = {
    "tiers": {
        "t1": {
            "name": "创新型中小企业",
            "name_en": "Innovative SME",
            "description": "优质中小企业梯度培育体系的基础层",
            "requirements": {
                "direct_pass": [
                    "近三年获得国家级/省部级科技奖励",
                    "有效期内高新技术企业",
                    "国家级技术创新示范企业",
                    "省部级以上研发机构",
                    "近三年新增股权融资≥500万"
                ],
                "scoring": {
                    "innovation": {"max": 40, "pass": 24},
                    "growth": {"max": 30, "pass": 18},
                    "specialization": {"max": 30, "pass": 18},
                    "total_pass": 60
                }
            }
        },
        "t2": {
            "name": "省级专精特新中小企业",
            "name_en": "Provincial SRDI SME",
            "description": "需先获得创新型中小企业认定",
            "requirements": {
                "prerequisite": "已获得创新型中小企业认定",
                "market_years": 3,
                "revenue_min": 1500,  # 万元
                "equity_financing_min": 2000,  # 万元（替代营收条件）
                "main_business_ratio_min": 0.80,
                "debt_ratio_max": 0.80,
                "rd_annual_min": 100,  # 万元/年
                "rd_ratio_min": 0.03,
                "ip_class1_min": 1,
                "score_pass": 50  # 2026统一标准
            }
        },
        "t3": {
            "name": "国家级专精特新小巨人",
            "name_en": "National SRDI Little Giant",
            "description": "专精特新金字塔塔尖，含金量最高",
            "requirements": {
                "prerequisite": "已获得省级专精特新中小企业认定",
                "market_years": 3,
                "revenue_min": 5000,
                "main_business_ratio_min": 0.90,
                "revenue_growth_min": 0.05,
                "debt_ratio_max": 0.75,
                "rd_total_min": 1200,  # 两年合计
                "rd_ratio_min": 0.03,
                "ip_class1_min": 4,
                "market_share_min": 0.10,
                "score_pass": 60,
                "domain_required": [
                    "六基领域（核心零部件/元器件/关键软件/基础工艺/基础材料）",
                    "制造强国十大重点产业",
                    "网络强国关键核心技术",
                    "产业链强链补链环节"
                ]
            }
        }
    },
    "red_lines": [
        "外购/转让/受让专利不计入I类知识产权",
        "营收<5000万不受理小巨人申报",
        "主营占比<90%直接淘汰（小巨人）",
        "资产负债率>75%一票否决（小巨人）",
        "数据造假→取消资格+3年禁报+追缴补贴+失信",
        "不可越级:必须先省级再国家级",
        "审计报告必须财政部监管平台已赋码电子原件"
    ],
    "subsidies": {
        "t3": "国家级小巨人：一次性奖励50万-500万（按省份）",
        "t2": "省级专精特新：奖励5万-50万（按省份）",
        "benefits": [
            "研发费用加计扣除+所得税优惠",
            "专项信贷+贴息+知识产权质押融资",
            "政府采购优先+招投标加分",
            "国家专项+技改项目优先立项",
            "上市辅导优先通道"
        ]
    }
}


def evaluate_tier(enterprise, tier_key):
    """评估企业是否满足某梯度认定条件"""
    tier = POLICY_2026["tiers"][tier_key]
    reqs = tier["requirements"]
    results = []

    if tier_key == "t3":
        # 小巨人评估
        checks = [
            ("前置资格", enterprise.get("has_provincial_srdi", False),
             "已获得省级专精特新中小企业认定", reqs.get("prerequisite", "")),
            ("深耕年限", enterprise.get("market_years", 0) >= reqs["market_years"],
             f'从事细分市场≥{reqs["market_years"]}年 (当前{enterprise.get("market_years", 0)}年)',
             reqs["market_years"]),
            ("营收门槛", enterprise.get("revenue", 0) >= reqs["revenue_min"],
             f'营收≥{reqs["revenue_min"]}万 (当前{enterprise.get("revenue", 0)}万)',
             reqs["revenue_min"]),
            ("主营占比", enterprise.get("main_business_ratio", 0) >= reqs["main_business_ratio_min"],
             f'主营占比≥{int(reqs["main_business_ratio_min"]*100)}% (当前{enterprise.get("main_business_ratio", 0)*100:.1f}%)',
             reqs["main_business_ratio_min"]),
            ("营收增长", enterprise.get("revenue_growth", 0) >= reqs["revenue_growth_min"],
             f'近两年营收复合增长率≥{int(reqs["revenue_growth_min"]*100)}% (当前{enterprise.get("revenue_growth", 0)*100:.1f}%)',
             reqs["revenue_growth_min"]),
            ("负债率", enterprise.get("debt_ratio", 1.0) <= reqs["debt_ratio_max"],
             f'资产负债率≤{int(reqs["debt_ratio_max"]*100)}% (当前{enterprise.get("debt_ratio", 0)*100:.1f}%)',
             reqs["debt_ratio_max"]),
            ("研发投入(合计)", enterprise.get("rd_total", 0) >= reqs["rd_total_min"],
             f'近两年研发合计≥{reqs["rd_total_min"]}万 (当前{enterprise.get("rd_total", 0)}万)',
             reqs["rd_total_min"]),
            ("研发占比", enterprise.get("rd_ratio", 0) >= reqs["rd_ratio_min"],
             f'每年研发占营收≥{int(reqs["rd_ratio_min"]*100)}% (当前{enterprise.get("rd_ratio", 0)*100:.1f}%)',
             reqs["rd_ratio_min"]),
            ("知识产权", enterprise.get("ip_class1_count", 0) >= reqs["ip_class1_min"],
             f'I类知识产权≥{reqs["ip_class1_min"]}项 (当前{enterprise.get("ip_class1_count", 0)}项)',
             reqs["ip_class1_min"]),
            ("市占率", enterprise.get("market_share", 0) >= reqs["market_share_min"],
             f'市占率≥{int(reqs["market_share_min"]*100)}% (当前{enterprise.get("market_share", 0)*100:.1f}%)',
             reqs["market_share_min"]),
            ("评价得分", enterprise.get("eval_score", 0) >= reqs["score_pass"],
             f'发展评价得分≥{reqs["score_pass"]}分 (当前{enterprise.get("eval_score", 0)}分)',
             reqs["score_pass"]),
        ]
    elif tier_key == "t2":
        # 省级专精特新
        checks = [
            ("前置资格", enterprise.get("has_innovative_sme", False),
             "已获得创新型中小企业认定", reqs.get("prerequisite", "")),
            ("深耕年限", enterprise.get("market_years", 0) >= reqs["market_years"],
             f'从事细分市场≥{reqs["market_years"]}年 (当前{enterprise.get("market_years", 0)}年)',
             reqs["market_years"]),
            ("营收/融资",
             enterprise.get("revenue", 0) >= reqs["revenue_min"] or enterprise.get("equity_financing", 0) >= reqs["equity_financing_min"],
             f'营收≥{reqs["revenue_min"]}万 或 股权融资≥{reqs["equity_financing_min"]}万',
             f'{reqs["revenue_min"]}万/{reqs["equity_financing_min"]}万'),
            ("主营占比", enterprise.get("main_business_ratio", 0) >= reqs["main_business_ratio_min"],
             f'主营占比≥{int(reqs["main_business_ratio_min"]*100)}% (当前{enterprise.get("main_business_ratio", 0)*100:.1f}%)',
             reqs["main_business_ratio_min"]),
            ("负债率", enterprise.get("debt_ratio", 1.0) <= reqs["debt_ratio_max"],
             f'资产负债率≤{int(reqs["debt_ratio_max"]*100)}% (当前{enterprise.get("debt_ratio", 0)*100:.1f}%)',
             reqs["debt_ratio_max"]),
            ("研发投入(年)", enterprise.get("rd_annual", 0) >= reqs["rd_annual_min"],
             f'年研发费用≥{reqs["rd_annual_min"]}万 (当前{enterprise.get("rd_annual", 0)}万)',
             reqs["rd_annual_min"]),
            ("研发占比", enterprise.get("rd_ratio", 0) >= reqs["rd_ratio_min"],
             f'研发占营收≥{int(reqs["rd_ratio_min"]*100)}% (当前{enterprise.get("rd_ratio", 0)*100:.1f}%)',
             reqs["rd_ratio_min"]),
            ("知识产权", enterprise.get("ip_class1_count", 0) >= reqs["ip_class1_min"],
             f'I类知识产权≥{reqs["ip_class1_min"]}项 (当前{enterprise.get("ip_class1_count", 0)}项)',
             reqs["ip_class1_min"]),
            ("评价得分", enterprise.get("eval_score", 0) >= reqs["score_pass"],
             f'发展评价得分≥{reqs["score_pass"]}分 (当前{enterprise.get("eval_score", 0)}分)',
             reqs["score_pass"]),
        ]

    for name, passed, detail, threshold in checks:
        status = "pass" if passed else "fail"
        results.append({
            "name": name,
            "passed": passed,
            "status": status,
            "detail": detail,
            "threshold": threshold
        })

    all_pass = all(r["passed"] for r in results)
    pass_count = sum(1 for r in results if r["passed"])

    return {
        "tier": tier_key,
        "tier_name": tier["name"],
        "all_pass": all_pass,
        "pass_count": pass_count,
        "total_count": len(results),
        "checks": results,
        "verdict": "✅ 建议申报" if all_pass else (
            "⚠️ 部分指标未达标，需补强后再报" if pass_count >= len(results) * 0.7
            else "❌ 暂不满足申报条件"
        )
    }


def generate_material_checklist(tier_key):
    """生成佐证材料待办清单"""
    base_materials = [
        {"name": "申请书", "required": True,
         "format": "按官方模板填写，法人签字+盖公章", "note": "系统自动生成后打印留存"},
        {"name": "营业执照复印件", "required": True,
         "format": "加盖公章", "note": "正本+副本"},
        {"name": "近两年审计报告", "required": True,
         "format": "财政部监管平台已赋码电子原件，含主营收入+主营成本指标", "note": "⚠️ 必须是赋码电子原件"},
        {"name": "研发费用情况说明", "required": True,
         "format": "含明细账+研发人员社保记录", "note": "需与审计报告数据一致"},
        {"name": "合规经营承诺书", "required": True,
         "format": "法人签字+盖公章", "note": "无违规违法承诺"},
        {"name": "无失信证明", "required": True,
         "format": "信用中国/企查查报告", "note": "申报期间有效"},
    ]

    if tier_key == "t3":
        base_materials.extend([
            {"name": "省级专精特新认定文件", "required": True,
             "format": "复印件+盖公章", "note": "前置条件"},
            {"name": "知识产权清单", "required": True,
             "format": "发明专利无需证书，系统填报数量；集成电路布图设计需原件扫描件",
             "note": "⚠️ 外购专利无效"},
            {"name": "专精特新发展评价得分证明", "required": True,
             "format": "系统评分截图或说明", "note": "2026新增要求，≥60分"},
            {"name": "主导产品市场占有率说明", "required": False,
             "format": "无需第三方证明，企业如实说明", "note": "2026新政：工信部大数据核验"},
            {"name": "产业链关键环节证明", "required": False,
             "format": "行业协会证明/龙头企业合作协议", "note": "强链补链说明"},
            {"name": "管理体系认证证书", "required": False,
             "format": "ISO系列/行业认证", "note": "加分项"},
        ])
    elif tier_key == "t2":
        base_materials.extend([
            {"name": "创新型中小企业认定文件", "required": True,
             "format": "复印件+盖公章", "note": "前置条件"},
            {"name": "知识产权证书", "required": True,
             "format": "I类知识产权证书复印件", "note": "≥1项，自主申请"},
            {"name": "股权融资证明(如适用)", "required": False,
             "format": "银行到账凭证+融资报告", "note": "营收<1500万时必交"},
            {"name": "市场地位说明", "required": False,
             "format": "企业自述+数据支撑", "note": ""},
        ])

    base_materials.append({"name": "社保缴纳证明", "required": False,
                           "format": "2025年12月底全员社保", "note": ""})
    base_materials.append({"name": "荣誉证书/品牌证明", "required": False,
                           "format": "政府荣誉/管理体系认证/自主品牌", "note": "加分项"})

    return base_materials


def generate_application_text(enterprise, tier_key):
    """生成申请书文本"""
    tier = POLICY_2026["tiers"][tier_key]
    years = enterprise.get("years", ["2024", "2025"])

    sections = []

    # 一、企业基本情况
    sections.append({
        "title": "一、企业基本情况",
        "content": f"""
企业名称：{enterprise.get('name', '【待填写】')}
统一社会信用代码：{enterprise.get('uscc', '【待填写】')}
注册地址：{enterprise.get('address', '【待填写】')}
法定代表人：{enterprise.get('legal_rep', '【待填写】')}
注册资本：{enterprise.get('reg_capital', '【待填写】')}万元
成立日期：{enterprise.get('founded', '【待填写】')}
所属行业：{enterprise.get('industry', '【待填写】')}
企业类型：{enterprise.get('company_type', '有限责任公司')}
控股情况：{enterprise.get('holding_type', '【待填写】')}
是否上市：{enterprise.get('is_listed', '否')}
上市交易所及代码：{enterprise.get('stock_code', '无') if enterprise.get('is_listed') == '否' else enterprise.get('stock_code', '【待填写】')}

【企业简介】
{enterprise.get('intro', '【请在此处填写企业基本情况简介，包括发展历程、核心业务、行业地位等，建议300-500字】')}
"""
    })

    # 二、经济效益与经营情况
    sections.append({
        "title": "二、经济效益与经营情况",
        "content": f"""
（一）近两年经营情况

| 指标 | {years[0]}年 | {years[1]}年 |
|------|------------|------------|
| 营业收入（万元） | {enterprise.get(f'revenue_{years[0]}', '【待填写】')} | {enterprise.get(f'revenue_{years[1]}', '【待填写】')} |
| 主营业务收入（万元） | {enterprise.get(f'main_revenue_{years[0]}', '【待填写】')} | {enterprise.get(f'main_revenue_{years[1]}', '【待填写】')} |
| 主营业务收入占比 | {enterprise.get(f'main_ratio_{years[0]}', '【待填写】')}% | {enterprise.get(f'main_ratio_{years[1]}', '【待填写】')}% |
| 利润总额（万元） | {enterprise.get(f'profit_{years[0]}', '【待填写】')} | {enterprise.get(f'profit_{years[1]}', '【待填写】')} |
| 净利润（万元） | {enterprise.get(f'net_profit_{years[0]}', '【待填写】')} | {enterprise.get(f'net_profit_{years[1]}', '【待填写】')} |
| 资产总额（万元） | {enterprise.get(f'assets_{years[0]}', '【待填写】')} | {enterprise.get(f'assets_{years[1]}', '【待填写】')} |
| 负债总额（万元） | {enterprise.get(f'liabilities_{years[0]}', '【待填写】')} | {enterprise.get(f'liabilities_{years[1]}', '【待填写】')} |
| 资产负债率 | {enterprise.get(f'debt_ratio_{years[0]}', '【待填写】')}% | {enterprise.get(f'debt_ratio_{years[1]}', '【待填写】')}% |
| 研发费用（万元） | {enterprise.get(f'rd_{years[0]}', '【待填写】')} | {enterprise.get(f'rd_{years[1]}', '【待填写】')} |
| 研发费用占营收比例 | {enterprise.get(f'rd_ratio_{years[0]}', '【待填写】')}% | {enterprise.get(f'rd_ratio_{years[1]}', '【待填写】')}% |
| 上缴税金（万元） | {enterprise.get(f'tax_{years[0]}', '【待填写】')} | {enterprise.get(f'tax_{years[1]}', '【待填写】')} |
| 从业人员数（人） | {enterprise.get(f'employees_{years[0]}', '【待填写】')} | {enterprise.get(f'employees_{years[1]}', '【待填写】')} |

（二）近两年营收复合增长率：{enterprise.get('revenue_growth', '【待填写】')}%
"""
    })

    # 三、专业化程度
    sections.append({
        "title": "三、专业化程度",
        "content": f"""
（一）主导产品名称：{enterprise.get('main_product', '【待填写】')}

（二）从事该细分领域时间：{enterprise.get('market_years', '【待填写】')}年

（三）主导产品用途及技术指标：
{enterprise.get('product_usage', '【请描述主导产品的主要用途、核心技术指标、与国际国内同类产品的对比优势，建议200-400字】')}

（四）主导产品在全国细分市场占有率：{enterprise.get('market_share', '【待填写】')}%

（五）主导产品市场地位说明：
{enterprise.get('market_position', '【请说明主导产品在细分市场中的地位，包括主要竞争对手、自身份额、竞争优势等，建议200-400字】')}
"""
    })

    # 四、精细化程度
    sections.append({
        "title": "四、精细化程度",
        "content": f"""
（一）企业获得的管理体系认证情况：
{enterprise.get('certifications', '【请列出已获得的管理体系认证，如ISO9001、ISO14001、ISO45001、IATF16949等】')}

（二）产品获得发达国家或地区认证情况：
{enterprise.get('product_certs', '【如有请填写，如CE、UL、FDA等国际认证】')}

（三）企业数字化水平：
{enterprise.get('digital_level', '【请描述企业数字化转型情况，包括ERP/MES/PLM/CRM等信息系统应用情况】')}

（四）质量管理水平（如产品合格率、不良品率等）：
{enterprise.get('quality_level', '【请描述企业质量管理措施和水平，建议100-200字】')}
"""
    })

    # 五、特色化程度
    sections.append({
        "title": "五、特色化程度",
        "content": f"""
（一）主导产品所属领域：
{enterprise.get('product_domain', '【请勾选并说明】')}

□ 制造业核心基础零部件/元器件/关键软件
□ 先进基础工艺
□ 关键基础材料
□ 制造强国战略十大重点产业领域
□ 网络强国建设重点产业领域
□ 产业链强链补链关键环节

（二）主导产品的特色化、差异化竞争优势：
{enterprise.get('product_feature', '【请说明主导产品区别于竞争对手的特色化优势，包括技术独特性、工艺创新等，建议200-400字】')}

（三）企业在细分领域中的行业地位和影响力：
{enterprise.get('industry_influence', '【请说明企业在该细分领域的行业地位、获得荣誉、参与标准制定等情况】')}
"""
    })

    # 六、创新能力
    sections.append({
        "title": "六、创新能力",
        "content": f"""
（一）知识产权情况

| 知识产权类型 | 数量 | 获得方式 | 与主导产品相关性 |
|-------------|------|---------|---------------|
| 发明专利 | {enterprise.get('patent_invention', '【待填写】')} | 自主申请 | 直接相关 |
| 集成电路布图设计 | {enterprise.get('patent_ic', '【待填写】')} | 自主申请 | 直接相关 |
| 实用新型专利 | {enterprise.get('patent_utility', '【待填写】')} | {enterprise.get('patent_source', '自主申请')} | {enterprise.get('patent_relevance', '相关')} |
| 软件著作权 | {enterprise.get('patent_software', '【待填写】')} | 自主申请 | 相关 |

I类知识产权总数：{enterprise.get('ip_class1_count', 0)}项

知识产权特别说明：
{enterprise.get('ip_notes', '【如有近三年获国家级科技奖励（排名前三）可豁免4项I类知识产权要求，请在此说明】')}

（二）研发机构建设情况
{enterprise.get('rd_institution', '【请说明企业自建或联合建立的研发机构情况，如企业技术中心、工程技术研究中心、重点实验室、博士后工作站等】')}

（三）研发人员情况
研发人员总数：{enterprise.get('rd_staff', '【待填写】')}人
研发人员占比：{enterprise.get('rd_staff_ratio', '【待填写】')}%

（四）核心技术和研发成果
{enterprise.get('core_tech', '【请说明企业掌握的核心技术、关键技术突破、产学研合作情况等，建议200-400字】')}

（五）主持或参与制（修）订标准情况
{enterprise.get('standards', '【如有参与制定国际/国家/行业标准，请列明】')}
"""
    })

    # 七、产业链配套
    if tier_key == "t3":
        sections.append({
            "title": "七、产业链配套",
            "content": f"""
（一）主导产品在产业链中所处环节：
{enterprise.get('chain_position', '【请说明主导产品在产业链中所处的位置，是上游原材料/中游制造/下游应用，以及在产业链中的关键性】')}

（二）产业链"补短板""锻长板""填空白"情况：
{enterprise.get('chain_fill_gap', '【请说明主导产品如何填补国内产业链空白、补齐短板或锻造长板，建议200-400字】')}

（三）为行业龙头/知名企业配套情况：
{enterprise.get('chain_supply', '【请说明是否有为国内外知名大企业直接配套，如有请列出合作企业名称和配套产品】')}
"""
        })

    # 八、其他情况说明
    sections.append({
        "title": "八、其他情况说明",
        "content": f"""
（一）近三年是否发生重大安全(含网络安全、数据安全)、质量、环境污染等事故：
{enterprise.get('accidents', '否')}

（二）近三年是否存在严重偷漏税等违法违规行为：
{enterprise.get('tax_violation', '否')}

（三）企业是否在经营异常名录或严重失信主体名单：
{enterprise.get('abnormal_list', '否')}

（四）其他需要说明的情况：
{enterprise.get('other_notes', '无')}
"""
    })

    return sections


def generate_avoidance_guide(tier_key):
    """生成避坑指南"""
    guide = {
        "title": "避坑指南 — 2026申报红线与常见失败原因",
        "common_failures": [
            {"reason": "主营占比不足",
             "detail": "副业、投资、贸易类收入占比高导致主营占比低于门槛。建议申报前调整业务结构，剥离非主营收入。",
             "severity": "high"},
            {"reason": "专利外购/转让",
             "detail": "外购、转让、受让的发明专利不计入I类知识产权统计。必须是自主申请的、企业权利人前3位的专利。",
             "severity": "high"},
            {"reason": "研发费用归集不规范",
             "detail": "研发费用未按规范归集，或与审计报告不一致。AI系统会自动比对，数据矛盾直接预警。",
             "severity": "high"},
            {"reason": "审计报告未赋码",
             "detail": "2026年起审计报告必须是财政部注册会计师统一监管平台已赋码的电子原件，传统纸质报告无效。",
             "severity": "high"} if tier_key == "t3" else None,
            {"reason": "营收不达标",
             "detail": "小巨人营收<5000万直接不受理。省级专精特新<1500万需提供2000万+股权融资证明。",
             "severity": "high"},
            {"reason": "资产负债率超标",
             "detail": "小巨人>75%一票否决。建议提前优化财务结构，降低负债率。",
             "severity": "high"} if tier_key == "t3" else None,
            {"reason": "越级申报",
             "detail": "2026年起不可跨级，必须先创新型→省级专精特新→国家级小巨人，逐级认定。",
             "severity": "medium"},
            {"reason": "数据前后矛盾",
             "detail": "申请书、审计报告、税务数据不一致，AI大数据审核直接预警。所有材料数据必须严格一致。",
             "severity": "medium"},
            {"reason": "近三年有重大事故/失信",
             "detail": "近三年发生重大安全/环保/税务事故或失信记录，一票否决。建议提前查询信用记录。",
             "severity": "high"},
            {"reason": "线上/线下材料不一致",
             "detail": "线下报送材料与线上填报数据不一致，省级初核不通过。务必逐一核对。",
             "severity": "medium"},
        ],
        "tips": [
            "提前1-2个月准备审计报告，确认会计师事务所已在财政部平台完成赋码",
            "知识产权梳理要趁早，确认所有专利均为自主申请且与主营产品直接相关",
            "财务数据从审计报告直接引用，不要手动计算或调整",
            "申报系统开放后尽早提交，避免最后一天网络拥堵",
            "保留所有申报材料扫描件，备用核查",
        ]
    }
    # 过滤掉None项
    guide["common_failures"] = [f for f in guide["common_failures"] if f is not None]
    return guide


def build_html_report(enterprise, tier_key, eval_result, materials, application, guide):
    """生成交互式HTML可视化报告"""
    tier = POLICY_2026["tiers"][tier_key]
    pass_count = eval_result["pass_count"]
    total_count = eval_result["total_count"]
    pass_rate = pass_count / total_count * 100

    # 构建检查项HTML
    checks_html = ""
    for c in eval_result["checks"]:
        icon = "✅" if c["passed"] else "❌"
        row_class = "pass-row" if c["passed"] else "fail-row"
        checks_html += f"""
        <tr class="{row_class}">
            <td>{icon}</td>
            <td><strong>{c['name']}</strong></td>
            <td>{c['detail']}</td>
            <td>{c['threshold']}</td>
        </tr>"""

    # 构建材料清单HTML
    materials_html = ""
    for i, m in enumerate(materials):
        req_badge = '<span class="badge-required">必交</span>' if m["required"] else '<span class="badge-optional">选交</span>'
        materials_html += f"""
        <tr>
            <td><input type="checkbox" id="mat_{i}"></td>
            <td>{req_badge}</td>
            <td>{m['name']}</td>
            <td>{m['format']}</td>
            <td class="note-cell">{m['note']}</td>
        </tr>"""

    # 构建申请书HTML
    app_html = ""
    for section in application:
        content = section["content"].replace("\n", "<br>")
        app_html += f"""
        <div class="app-section">
            <h3>{section['title']}</h3>
            <div class="app-content">{content}</div>
        </div>"""

    # 构建避坑指南HTML
    guide_html = ""
    for f in guide["common_failures"]:
        sev_class = "sev-high" if f["severity"] == "high" else "sev-medium"
        sev_label = "高风险" if f["severity"] == "high" else "中风险"
        guide_html += f"""
        <div class="guide-item {sev_class}">
            <h4>⚠️ {f['reason']} <span class="sev-tag">{sev_label}</span></h4>
            <p>{f['detail']}</p>
        </div>"""

    tips_html = "".join(f"<li>{t}</li>" for t in guide["tips"])

    # 雷达图数据
    radar_labels = json.dumps([c["name"] for c in eval_result["checks"]])
    radar_data = json.dumps([100 if c["passed"] else 30 for c in eval_result["checks"]])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>专精特新申报材料 — {enterprise.get('name', '企业')} ({tier['name']})</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }}
.container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}

/* Header */
.header {{ background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%); color: #fff; padding: 40px 30px; border-radius: 16px; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(26,35,126,0.3); }}
.header h1 {{ font-size: 28px; margin-bottom: 8px; }}
.header .subtitle {{ font-size: 16px; opacity: 0.9; }}
.header .badge {{ display: inline-block; background: rgba(255,255,255,0.2); padding: 4px 16px; border-radius: 20px; font-size: 14px; margin-top: 12px; }}

/* Dashboard */
.dashboard {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }}
.card {{ background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.card h2 {{ font-size: 18px; margin-bottom: 16px; color: #1a237e; border-bottom: 2px solid #e8eaf6; padding-bottom: 8px; }}

/* Verdict */
.verdict-card {{ text-align: center; }}
.verdict-icon {{ font-size: 48px; margin-bottom: 12px; }}
.verdict-text {{ font-size: 22px; font-weight: 700; margin-bottom: 8px; }}
.verdict-detail {{ color: #666; font-size: 14px; }}
.verdict-pass {{ color: #2e7d32; }}
.verdict-warn {{ color: #e65100; }}
.verdict-fail {{ color: #c62828; }}
.progress-bar {{ background: #e0e0e0; border-radius: 10px; height: 12px; margin-top: 16px; overflow: hidden; }}
.progress-fill {{ height: 100%; border-radius: 10px; transition: width 0.6s; }}
.progress-fill.pass {{ background: linear-gradient(90deg, #43a047, #66bb6a); }}
.progress-fill.warn {{ background: linear-gradient(90deg, #ff9800, #ffb74d); }}
.progress-fill.fail {{ background: linear-gradient(90deg, #e53935, #ef5350); }}

/* Table */
table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #e0e0e0; font-size: 14px; }}
th {{ background: #f5f5f5; font-weight: 600; color: #555; }}
.pass-row {{ background: #f1f8e9; }}
.fail-row {{ background: #fce4ec; }}
.note-cell {{ color: #e65100; font-size: 13px; }}

/* Badges */
.badge-required {{ background: #e53935; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 12px; white-space: nowrap; }}
.badge-optional {{ background: #78909c; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 12px; white-space: nowrap; }}

/* Application Sections */
.app-section {{ margin-bottom: 24px; }}
.app-section h3 {{ font-size: 16px; color: #1a237e; margin-bottom: 12px; padding-left: 12px; border-left: 4px solid #3949ab; }}
.app-content {{ background: #fafafa; border-radius: 8px; padding: 20px; font-size: 14px; line-height: 1.8; border: 1px solid #e0e0e0; }}
.app-content table {{ margin: 12px 0; }}
.app-content td, .app-content th {{ padding: 6px 10px; font-size: 13px; }}

/* Guide */
.guide-item {{ padding: 16px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid; }}
.guide-item.sev-high {{ background: #fce4ec; border-color: #e53935; }}
.guide-item.sev-medium {{ background: #fff3e0; border-color: #ff9800; }}
.guide-item h4 {{ font-size: 15px; margin-bottom: 6px; }}
.guide-item p {{ font-size: 14px; color: #555; }}
.sev-tag {{ font-size: 12px; padding: 2px 8px; border-radius: 4px; color: #fff; }}
.sev-high .sev-tag {{ background: #e53935; }}
.sev-medium .sev-tag {{ background: #ff9800; }}

/* Tips */
.tips-list {{ list-style: none; padding: 0; }}
.tips-list li {{ padding: 8px 0; border-bottom: 1px dotted #e0e0e0; font-size: 14px; }}
.tips-list li::before {{ content: "💡 "; }}

/* Tabs */
.tabs {{ display: flex; gap: 4px; margin-bottom: 20px; flex-wrap: wrap; }}
.tab-btn {{ padding: 10px 24px; background: #e8eaf6; border: none; border-radius: 8px 8px 0 0; cursor: pointer; font-size: 14px; color: #555; transition: all 0.2s; }}
.tab-btn.active {{ background: #3949ab; color: #fff; }}
.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}

/* Benefits */
.benefits-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
.benefit-item {{ background: linear-gradient(135deg, #e8eaf6, #c5cae9); padding: 16px; border-radius: 10px; font-size: 14px; }}
.benefit-item h4 {{ color: #1a237e; margin-bottom: 4px; }}

/* Footer */
.footer {{ text-align: center; padding: 30px; color: #999; font-size: 13px; }}
.footer a {{ color: #3949ab; }}

/* Print */
@media print {{
  body {{ background: #fff; }}
  .card {{ box-shadow: none; border: 1px solid #ddd; page-break-inside: avoid; }}
  .tabs {{ display: none; }}
  .tab-content {{ display: block !important; }}
}}

/* Radar chart container */
.radar-container {{ max-width: 400px; margin: 0 auto; }}
</style>
</head>
<body>
<div class="container">

<!-- Header -->
<div class="header">
    <h1>📋 专精特新企业申报材料</h1>
    <div class="subtitle">{enterprise.get('name', '企业名称')} | 申报梯度：{tier['name']}</div>
    <div class="badge">基于2026年4月最新政策 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</div>

<!-- Dashboard -->
<div class="dashboard">
    <div class="card verdict-card">
        <h2>综合判定</h2>
        <div class="verdict-icon">{'✅' if eval_result['all_pass'] else '⚠️' if pass_rate >= 70 else '❌'}</div>
        <div class="verdict-text {'verdict-pass' if eval_result['all_pass'] else 'verdict-warn' if pass_rate >= 70 else 'verdict-fail'}">{eval_result['verdict']}</div>
        <div class="verdict-detail">{pass_count}/{total_count} 项指标达标 ({pass_rate:.0f}%)</div>
        <div class="progress-bar">
            <div class="progress-fill {'pass' if pass_rate >= 80 else 'warn' if pass_rate >= 60 else 'fail'}" style="width:{pass_rate}%"></div>
        </div>
    </div>
    <div class="card">
        <h2>六维达标雷达图</h2>
        <div class="radar-container">
            <canvas id="radarChart"></canvas>
        </div>
    </div>
</div>

<!-- Tabs -->
<div class="tabs">
    <button class="tab-btn active" onclick="switchTab('self-check')">📊 资格自评</button>
    <button class="tab-btn" onclick="switchTab('application')">📝 申请书</button>
    <button class="tab-btn" onclick="switchTab('materials')">📎 材料清单</button>
    <button class="tab-btn" onclick="switchTab('guide')">⚠️ 避坑指南</button>
    <button class="tab-btn" onclick="switchTab('benefits')">💰 政策红利</button>
</div>

<!-- Tab: 资格自评 -->
<div id="tab-self-check" class="tab-content active">
    <div class="card">
        <h2>硬性指标逐项检查</h2>
        <p style="color:#666; margin-bottom:12px;">申报目标：<strong>{tier['name']}</strong> | 政策依据：《优质中小企业梯度培育管理办法》（工信部企业〔2026〕2号）</p>
        <table>
            <thead>
                <tr><th>状态</th><th>检查项</th><th>详情</th><th>达标值</th></tr>
            </thead>
            <tbody>{checks_html}</tbody>
        </table>
    </div>
</div>

<!-- Tab: 申请书 -->
<div id="tab-application" class="tab-content">
    <div class="card">
        <h2>专精特新"{tier['name']}"申请书</h2>
        <p style="color:#666; margin-bottom:16px;">以下为申请书正文框架，请在"【】"处填写实际数据后提交至优质中小企业梯度培育平台（zjtx.miit.gov.cn）</p>
        {app_html}
    </div>
</div>

<!-- Tab: 材料清单 -->
<div id="tab-materials" class="tab-content">
    <div class="card">
        <h2>佐证材料待办清单</h2>
        <p style="color:#666; margin-bottom:12px;">请在提交前逐项核对，打勾确认已准备完毕</p>
        <table>
            <thead>
                <tr><th>✓</th><th>类型</th><th>材料名称</th><th>格式要求</th><th>备注</th></tr>
            </thead>
            <tbody>{materials_html}</tbody>
        </table>
        <div style="margin-top:16px; padding:16px; background:#fff3e0; border-radius:8px; border-left:4px solid #ff9800;">
            <strong>⚠️ 提交前最后核查：</strong>
            <ul style="margin-top:8px; padding-left:20px;">
                <li>所有数据与审计报告、税务报表一致</li>
                <li>审计报告已赋码（财政部监管平台）</li>
                <li>知识产权为自主申请，与主营产品对应</li>
                <li>线上填报与线下材料数据完全一致</li>
                <li>材料格式符合要求（PDF/JPG，大小合规）</li>
            </ul>
        </div>
    </div>
</div>

<!-- Tab: 避坑指南 -->
<div id="tab-guide" class="tab-content">
    <div class="card">
        <h2>{guide['title']}</h2>
        {guide_html}
    </div>
    <div class="card" style="margin-top:16px;">
        <h2>准备建议</h2>
        <ul class="tips-list">{tips_html}</ul>
    </div>
</div>

<!-- Tab: 政策红利 -->
<div id="tab-benefits" class="tab-content">
    <div class="card">
        <h2>认定后可享受的政策红利</h2>
        <div class="benefits-grid">
            <div class="benefit-item">
                <h4>💰 财政奖励</h4>
                <p>{POLICY_2026['subsidies']['t3'] if tier_key == 't3' else POLICY_2026['subsidies']['t2']}</p>
            </div>
            <div class="benefit-item">
                <h4>📉 税收优惠</h4>
                <p>{POLICY_2026['subsidies']['benefits'][0]}</p>
            </div>
            <div class="benefit-item">
                <h4>🏦 融资支持</h4>
                <p>{POLICY_2026['subsidies']['benefits'][1]}</p>
            </div>
            <div class="benefit-item">
                <h4>🏛️ 政府采购</h4>
                <p>{POLICY_2026['subsidies']['benefits'][2]}</p>
            </div>
            <div class="benefit-item">
                <h4>🔬 项目优先</h4>
                <p>{POLICY_2026['subsidies']['benefits'][3]}</p>
            </div>
            <div class="benefit-item">
                <h4>📈 上市辅导</h4>
                <p>{POLICY_2026['subsidies']['benefits'][4]}</p>
            </div>
        </div>
    </div>
</div>

<div class="footer">
    <p>本报告基于2026年工信部最新政策生成，仅供参考。正式申报请以工信部官网(zjtx.miit.gov.cn)最新通知为准。</p>
    <p>建议在提交前咨询专业申报机构复核 | 生成工具：WorkBuddy SRDI Application Skill v1.0</p>
</div>

</div>

<script>
// Tab switching
function switchTab(tabName) {{
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + tabName).classList.add('active');
    event.target.classList.add('active');
}}

// Radar Chart
const ctx = document.getElementById('radarChart').getContext('2d');
new Chart(ctx, {{
    type: 'radar',
    data: {{
        labels: {radar_labels},
        datasets: [{{
            label: '达标情况 (%)',
            data: {radar_data},
            backgroundColor: 'rgba(57, 73, 171, 0.2)',
            borderColor: 'rgba(57, 73, 171, 1)',
            borderWidth: 2,
            pointBackgroundColor: 'rgba(57, 73, 171, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(57, 73, 171, 1)',
        }}]
    }},
    options: {{
        responsive: true,
        scales: {{
            r: {{
                beginAtZero: true,
                max: 100,
                ticks: {{ stepSize: 20, backdropColor: 'transparent' }},
                pointLabels: {{ font: {{ size: 12 }} }}
            }}
        }},
        plugins: {{
            legend: {{ display: false }}
        }}
    }}
}});
</script>
</body>
</html>"""

    return html


def generate(enterprise_data, tier_key, output_dir):
    """主生成函数"""
    # 评估
    eval_result = evaluate_tier(enterprise_data, tier_key)

    # 材料清单
    materials = generate_material_checklist(tier_key)

    # 申请书
    application = generate_application_text(enterprise_data, tier_key)

    # 避坑指南
    guide = generate_avoidance_guide(tier_key)

    # 生成HTML报告
    html = build_html_report(enterprise_data, tier_key, eval_result, materials, application, guide)

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 写入文件
    html_path = os.path.join(output_dir, f"srdi_report_{tier_key}_{enterprise_data.get('name', 'enterprise')}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 生成申请书纯文本
    txt_lines = []
    txt_lines.append(f"专精特新'{POLICY_2026['tiers'][tier_key]['name']}'申请书")
    txt_lines.append(f"企业名称：{enterprise_data.get('name', '【待填写】')}")
    txt_lines.append("=" * 60)
    for section in application:
        txt_lines.append(f"\n{section['title']}")
        txt_lines.append("-" * 40)
        txt_lines.append(section["content"])
    txt_path = os.path.join(output_dir, f"srdi_application_{tier_key}_{enterprise_data.get('name', 'enterprise')}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    return {
        "html_path": html_path,
        "txt_path": txt_path,
        "evaluation": eval_result,
        "materials_count": len(materials),
        "required_count": sum(1 for m in materials if m["required"])
    }


# ─── CLI Entry ───

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py <json_input>")
        print("JSON format: {name, tier(t1/t2/t3), ...}")
        sys.exit(1)

    input_data = json.loads(sys.argv[1]) if sys.argv[1].startswith("{") else json.load(open(sys.argv[1], encoding="utf-8"))
    tier = input_data.pop("tier", "t2")
    output_dir = input_data.pop("output_dir", ".")

    result = generate(input_data, tier, output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
