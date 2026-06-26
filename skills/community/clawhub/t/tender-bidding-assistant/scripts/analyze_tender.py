#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招标文件分析器 v3.1
自动解析招标文件（文本格式），输出结构化分析报告，含2026新政合规检测

⚠️ 数据安全提醒：
本脚本会读取并处理传入的招标文件文本内容，包括计算文本 SHA-256 哈希值用于存证。
传入的文件可能包含商业秘密、报价信息、技术方案等敏感内容。
使用前请确保：
  1. 已对敏感信息进行脱敏处理（移除具体报价、客户名称、核心技术参数等）
  2. 有权限将相关文件内容用于 AI 辅助分析
  3. 符合所在组织的数据安全政策规定

用法:
    python analyze_tender.py <招标文件路径或文本> [--json]

功能:
    - 自动识别项目名称、预算、评分标准、采购方式
    - 提取资格条件与必须满足的门槛
    - 识别废标条款与2026异常低价红线
    - 2026新政影响评估（价格权重/绿色采购/AI合规/中小企业优惠）
    - 生成材料准备清单和合规风险报告
    - 计算文件 SHA-256 哈希值（用于电子投标文件存证声明）
"""

import sys
import re
import json
import hashlib
from datetime import datetime


# ===================== 2026 新政常量 =====================

POLICY_2026 = {
    "abnormal_price_ratio": 0.45,  # 低于最高限价45%触发异常低价审查
    "abnormal_price_ratio_second": 0.50,  # 低于次低报价50%触发
    "service_price_weight_max": 0.50,  # 服务类价格分上限50%
    "goods_price_weight_max": 0.60,   # 货物/工程类价格分上限60%
    "sme_price_deduction_min": 0.06,  # 小微企业价格扣除下限6%
    "sme_price_deduction_max": 0.10,  # 小微企业价格扣除上限10%
    "sme_goods_service_threshold": 2000000,  # 200万以下货物服务预留小微企业
    "sme_engineering_threshold": 4000000,  # 400万以下工程预留小微企业
    "green_required": True,  # 绿色采购已为法定评审标准
    "electronic_guarantee_required": True,  # 电子保函替代现金保证金
    "ai_audit_required": True,  # AI辅助评标已部署
}

# 招投标常见废标关键词
DISQUALIFICATION_KEYWORDS = [
    "废标", "无效投标", "投标无效", "取消资格", "否决",
    "一票否决", "实质性要求", "不接受", "必须满足",
    "高于预算", "超出限价", "低于成本", "不满足资格"
]

# 绿色采购关键词
GREEN_KEYWORDS = [
    "绿色", "低碳", "碳排放", "碳中和", "节能", "环保",
    "环境影响", "碳足迹", "绿色建材", "绿色供应链", "ESG",
    "新能源", "可再生能源", "清洁能源"
]

# 行业资质映射表
QUALIFICATION_MAP = {
    "保险": ["保险经营许可证", "偿付能力报告", "条款备案号"],
    "软件": ["软件企业认定", "ISO 27001", "CMMI", "ISO 20000"],
    "IT服务": ["ITSS", "ISO 20000", "等保测评报告"],
    "工程": ["建筑业企业资质", "安全生产许可证", "注册建造师"],
    "咨询": ["工程咨询资质", "造价咨询资质"],
    "设计": ["工程设计资质", "ISO 9001"],
    "监理": ["工程监理资质", "注册监理工程师"],
}

# 电子招标平台特征
E_PLATFORM_FEATURES = {
    "政府采购云平台": {"ca": "CA互认（省内通办）", "format": "PDF+XML", "upload": "7×24小时"},
    "中招联合": {"ca": "自有CA", "format": "PDF", "upload": "7×24小时"},
    "优质采": {"ca": "自有CA", "format": "PDF+WORD", "upload": "按标段设置窗口"},
    "公共资源交易中心": {"ca": "各省CA不互通", "format": "PDF", "upload": "按标段设置窗口"},
}


def analyze_tender_text(text: str) -> dict:
    """全面分析招标文件文本"""

    result = {
        "project_name": None,
        "project_no": None,
        "budget": None,
        "procurement_method": None,
        "contract_type": None,
        "procurement_type": None,  # 服务/货物/工程
        "qualification_requirements": [],
        "scoring_criteria": {},
        "required_documents": [],
        "disqualification_risks": [],
        "key_dates": {},
        "policy_2026_check": {},
        "green_requirements": [],
        "sme_policy_applied": False,
        "e_platform_info": {},
        "warnings": [],
    }

    # --- 项目名称 ---
    m = re.search(r"项目名称[：:\s]*([^。\n]+)", text)
    if m:
        result["project_name"] = m.group(1).strip()

    # --- 招标编号 ---
    m = re.search(r"(?:招标|项目)[编号号][：:\s]*([A-Za-z0-9\-/（）()]+)", text)
    if m:
        result["project_no"] = m.group(1).strip()

    # --- 预算 ---
    budget_patterns = [
        r"预算[金额]*[为：:\s]*([¥￥]?[\d,]+\.?\d*\s*万?元?)",
        r"采购预算[：:\s]*([¥￥]?[\d,]+\.?\d*\s*万?元?)",
        r"最高限价[：:\s]*([¥￥]?[\d,]+\.?\d*\s*万?元?)",
        r"项目预算[：:\s]*([¥￥]?[\d,]+\.?\d*\s*万?元?)",
    ]
    for pat in budget_patterns:
        m = re.search(pat, text)
        if m:
            result["budget"] = m.group(1).strip()
            break

    # --- 采购方式 ---
    methods = ["公开招标", "邀请招标", "竞争性谈判", "单一来源", "询价", "框架协议"]
    for method in methods:
        if method in text:
            result["procurement_method"] = method
            break

    # --- 合同类型 ---
    contract_types = ["单次", "框架协议", "多年期", "长期服务", "一采三年"]
    for ct in contract_types:
        if ct in text:
            result["contract_type"] = ct
            break

    # --- 采购类型 ---
    if any(k in text for k in ["服务", "咨询服务", "技术服务", "物业管理", "培训"]):
        result["procurement_type"] = "服务类"
    elif any(k in text for k in ["货物", "设备", "产品", "硬件", "软件"]):
        result["procurement_type"] = "货物类"
    elif any(k in text for k in ["工程", "施工", "总承包", "装修", "安装"]):
        result["procurement_type"] = "工程类"

    # --- 关键时间节点 ---
    date_patterns = {
        "投标截止": r"投标截止[时间日期]*[：:\s]*([\d]{4}年[\d]{1,2}月[\d]{1,2}日[\s\d:：至到]+)",
        "开标时间": r"开标[时间日期]*[：:\s]*([\d]{4}年[\d]{1,2}月[\d]{1,2}日[\s\d:：]+)",
        "答疑截止": r"答疑截止[：:\s]*([\d]{4}年[\d]{1,2}月[\d]{1,2}日[\s\d:：]+)",
        "文件获取": r"文件获取[截止]*[：:\s]*([\d]{4}年[\d]{1,2}月[\d]{1,2}日[\s\d:：]+)",
        "中标公示": r"中标公示[：:\s]*([\d]{4}年[\d]{1,2}月[\d]{1,2}日[\s\d:：]+)",
    }
    for key, pat in date_patterns.items():
        m = re.search(pat, text)
        if m:
            result["key_dates"][key] = m.group(1).strip()

    # --- 资格条件 ---
    qual_patterns = [
        (r"注册[资本][金]*[不少于不低]*[¥￥]?[\d,\.]+\s*万", "注册资本要求"),
        (r"(?:具[有备])[^。]*资质[证书格]", "资质证书要求"),
        (r"业绩[要求：:\s]*[^。]{5,50}", "业绩要求"),
        (r"人员[要求：:\s]*[^。]{5,50}", "人员要求"),
        (r"社保[：:\s]*[^。]{5,30}", "社保缴纳要求"),
        (r"信用[：:\s]*[^。]{5,30}", "信用要求"),
        (r"偿付能力[：:\s]*[^。]{5,30}", "偿付能力要求"),
    ]
    for pat, desc in qual_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            result["qualification_requirements"].append({
                "type": desc,
                "content": m.group(0).strip()
            })

    # --- 评分标准 ---
    price_weight_m = re.search(r"价格[分权]*[：:\s]*(\d+)[分%]", text)
    tech_weight_m = re.search(r"技术[分权]*[：:\s]*(\d+)[分%]", text)
    business_weight_m = re.search(r"商务[分权]*[：:\s]*(\d+)[分%]", text)
    service_weight_m = re.search(r"服务[分权]*[：:\s]*(\d+)[分%]", text)

    if price_weight_m:
        result["scoring_criteria"]["price_weight"] = int(price_weight_m.group(1))
    if tech_weight_m:
        result["scoring_criteria"]["tech_weight"] = int(tech_weight_m.group(1))
    if business_weight_m:
        result["scoring_criteria"]["business_weight"] = int(business_weight_m.group(1))
    if service_weight_m:
        result["scoring_criteria"]["service_weight"] = int(service_weight_m.group(1))

    # 识别评分计算方法
    if "最低价" in text or "低价优先" in text:
        result["scoring_criteria"]["method"] = "最低价法"
    elif "平均价" in text or "偏离度" in text or "偏差率" in text:
        result["scoring_criteria"]["method"] = "平均价偏差法"
    elif "去头去尾" in text or "去除最高" in text:
        result["scoring_criteria"]["method"] = "去头去尾平均法"
    elif "综合评分" in text:
        result["scoring_criteria"]["method"] = "综合评分法"

    # --- 废标条款 ---
    for kw in DISQUALIFICATION_KEYWORDS:
        for line in text.split("\n"):
            if kw in line and len(line) > 10:
                result["disqualification_risks"].append({
                    "keyword": kw,
                    "context": line.strip()[:100]
                })
                break

    # ===================== 2026 新政检测 =====================

    # --- 价格权重检查 ---
    pw = result["scoring_criteria"].get("price_weight", 0)
    pt = result.get("procurement_type", "")
    if pt == "服务类" and pw > POLICY_2026["service_price_weight_max"] * 100:
        result["policy_2026_check"]["price_weight"] = (
            f"⚠️ 价格分{pw}%可能超出2026服务类上限50%，"
            f"建议核实招标文件是否为旧版模板"
        )
    elif pt in ["货物类", "工程类"] and pw > POLICY_2026["goods_price_weight_max"] * 100:
        result["policy_2026_check"]["price_weight"] = (
            f"⚠️ 价格分{pw}%可能超出2026货物/工程类上限60%"
        )

    # --- 绿色采购要求检测 ---
    for kw in GREEN_KEYWORDS:
        if kw in text:
            result["green_requirements"].append(kw)
    if result["green_requirements"]:
        result["policy_2026_check"]["green"] = (
            f"✅ 检测到绿色采购指标：{', '.join(result['green_requirements'][:5])}。"
            f"2026年已为法定评审标准，需准备碳排放数据/节能认证/环保认证材料"
        )
    else:
        result["policy_2026_check"]["green"] = (
            "📌 未检测到绿色采购要求。2026年建议主动准备绿色低碳相关材料作为加分项"
        )

    # --- 中小企业政策检测 ---
    if any(k in text for k in ["中小企业", "小微企业", "预留", "价格扣除"]):
        result["sme_policy_applied"] = True
        result["policy_2026_check"]["sme"] = (
            "✅ 检测到中小企业优惠政策。小微企业可享受6%-10%价格扣除"
        )

    # --- 电子保函检测 ---
    if any(k in text for k in ["电子保函", "电子保单", "线上保函"]):
        result["policy_2026_check"]["e_guarantee"] = (
            "✅ 已支持电子保函，建议优先使用（费率0.3%-1.5%）替代现金保证金"
        )
    elif any(k in text for k in ["保证金", "保函", "担保"]):
        result["policy_2026_check"]["e_guarantee"] = (
            "⚠️ 检测到保证金要求但未明确支持电子保函。"
            "2026年政策鼓励电子保函全面替代现金保证金，建议在澄清环节提出"
        )

    # --- 电子招标平台检测 ---
    for platform, features in E_PLATFORM_FEATURES.items():
        if platform in text:
            result["e_platform_info"] = {"name": platform, **features}
            result["policy_2026_check"]["e_platform"] = (
                f"检测到电子招标平台：{platform}，CA证书：{features['ca']}"
            )
            break

    # --- AI合规检测项 ---
    result["policy_2026_check"]["ai_compliance"] = [
        "📋 确认电子标书制作设备/网络环境独立性",
        "📋 确认文件编辑痕迹中无其他公司信息",
        "📋 确认技术方案语义独创性（不与已公开方案高度雷同）",
        "📋 确认电子文件哈希值已生成并存证",
    ]

    # --- 异常低价预警 ---
    if result["budget"]:
        try:
            budget_str = result["budget"].replace("¥", "").replace("￥", "").replace(",", "")
            budget_num = float(re.sub(r'[万万元]', '', budget_str))
            if "万" in result["budget"]:
                budget_num *= 10000
            red_line = budget_num * POLICY_2026["abnormal_price_ratio"]
            result["policy_2026_check"]["abnormal_price"] = (
                f"🚨 异常低价红线：报价低于 ¥{red_line:,.0f}（最高限价45%）"
                f"将触发成本证明审查，需准备人材机明细+管理费及利润测算表（加盖公章）"
            )
        except:
            pass

    # --- 综合警告 ---
    if not result["sme_policy_applied"] and result.get("budget"):
        result["warnings"].append(
            "该项目未标注中小企业优惠政策。如本公司符合小微企业标准，"
            "建议在澄清环节询问是否可以享受6%-10%价格扣除"
        )
    if not result["green_requirements"]:
        result["warnings"].append(
            "招标文件未明确绿色采购评审指标。"
            "2026年政策要求将碳排放/节能环保纳入法定评审，建议主动提交绿色资质"
        )

    return result


def generate_checklist(analysis: dict) -> str:
    """生成2026增强版材料准备清单"""

    pt = analysis.get("procurement_type", "通用")

    lines = [
        f"# 材料准备清单（{pt} — 2026增强版）",
        f"# 项目：{analysis.get('project_name', '未识别')}",
        f"# 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 一、商务类材料",
        "- [ ] 营业执照副本（加盖公章，三证合一）",
        "- [ ] 法定代表人身份证复印件（加盖公章）",
        "- [ ] 授权委托书（如需委托代表）+ 受托人身份证复印件",
        "- [ ] 投标函（签字盖章，大小写金额一致）",
        "- [ ] 报价明细表 + 总报价汇总表（签字盖章）",
        "- [ ] 投标保证金凭证：□ 电子保函（推荐） □ 银行保函 □ 现金汇款",
        "- [ ] 电子投标文件哈希值存证确认函",
        "- [ ] 电子签章CA证书有效期检查",
        "",
        "## 二、资质类材料",
        "- [ ] 行业资质证书（有效期内，按评分排序）",
        "- [ ] 近三年审计报告或财务报表",
        "- [ ] 银行资信证明/开户许可证",
        "- [ ] 纳税证明（近X期）",
        "- [ ] 社保缴纳证明（关键人员近X个月）",
        "",
        "## 三、业绩类材料",
        "- [ ] 类似项目业绩合同（首页+金额页+验收报告，三件套）",
        "- [ ] 业绩按金额从大到小排序，优先与本次需求高度相似的项目",
        "- [ ] 中标通知书（如有）",
        "",
        "## 四、技术类材料",
        "- [ ] 技术方案/服务方案（按招标条款逐条编号响应）",
        "- [ ] 公司综合实力介绍（聚焦本项目相关优势）",
        "- [ ] 项目组织架构与人员配置表",
        "- [ ] 核心人员简历 + 资质证书 + 社保证明",
        "- [ ] 项目实施计划（甘特图 + 里程碑 + 交付物清单）",
        "- [ ] 质量保证体系文件",
        "- [ ] 售后服务方案（量化承诺优先）",
        "- [ ] 风险管理与应急预案",
        "",
        "## 五、2026新政专项材料",
        "- [ ] 绿色采购合规声明（碳排放数据/节能认证/环保认证）",
        "- [ ] 异常低价成本合理性说明（如报价低于最高限价45%）",
        "- [ ] 中小企业声明函（如适用，享受6%-10%价格扣除）",
        "- [ ] AI合规自查声明（机器码/IP/哈希值/语义独创性）",
        "- [ ] 电子保函确认函（如使用电子保函）",
        "",
        "## 六、承诺函类材料",
        "- [ ] 廉洁投标承诺函",
        "- [ ] 不串标/围标承诺函",
        "- [ ] 诚信投标承诺函",
        "- [ ] 知识产权承诺函（科技/IT类项目）",
        "- [ ] 绿色采购承诺函（如涉及）",
        "- [ ] 电子投标合规承诺函",
        "",
        "## 七、AI合规预审清单",
        "- [ ] 电子投标文件已过AI合规检测工具预审",
        "- [ ] 招标文件响应度 ≥ 95%",
        "- [ ] 错敏词清零",
        "- [ ] 技术方案语义独创性通过（与已公开方案相似度 < 30%）",
        "- [ ] 报价清单不平衡报价偏差 ≤ 15%",
        "- [ ] 关键人员社保单位与投标人一致",
        "- [ ] 电子文件机器码/IP/MAC地址独立性确认",
        "",
        "## 八、投标文件封装清单",
        "- [ ] 正本：___份",
        "- [ ] 副本：___份",
        "- [ ] 电子文件：U盘___份 / 网上递交（已确认平台上传窗口开放时段）",
        "- [ ] 密封要求：________",
        "- [ ] 装订方式：________",
    ]

    return "\n".join(lines)


def generate_risk_report(analysis: dict) -> str:
    """生成风险报告"""
    lines = [
        "# 废标风险与合规分析报告",
        f"# 项目：{analysis.get('project_name', '未识别')}",
        "",
        "## 一、一票否决风险",
    ]

    if analysis["disqualification_risks"]:
        for i, risk in enumerate(analysis["disqualification_risks"][:10], 1):
            lines.append(f"{i}. [{risk['keyword']}] {risk['context']}")
    else:
        lines.append("✅ 未检测到明确的一票否决条款")

    lines.append("")
    lines.append("## 二、2026新政合规检查")

    for check_name, check_msg in analysis.get("policy_2026_check", {}).items():
        if isinstance(check_msg, list):
            lines.append(f"\n### {check_name}")
            for item in check_msg:
                lines.append(f"- {item}")
        elif isinstance(check_msg, str):
            lines.append(f"\n### {check_name}")
            lines.append(f"{check_msg}")

    lines.append("")
    lines.append("## 三、综合风险提示")
    for warning in analysis.get("warnings", []):
        lines.append(f"- ⚠️ {warning}")

    if not analysis.get("warnings"):
        lines.append("✅ 未发现需要特别关注的合规风险")

    return "\n".join(lines)


if __name__ == "__main__":
    text = ""
    output_json = "--json" in sys.argv

    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        if first_arg == "--json":
            pass  # no file, json mode only
        else:
            try:
                with open(first_arg, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except FileNotFoundError:
                text = first_arg  # treat as inline text

    analysis = analyze_tender_text(text)
    checklist = generate_checklist(analysis)
    risk_report = generate_risk_report(analysis)

    if output_json:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("     招 标 文 件 分 析 报 告（2026增强版）")
        print("=" * 60)
        print()
        print("### 项目基本信息")
        print(f"项目名称：{analysis.get('project_name', '未识别')}")
        print(f"招标编号：{analysis.get('project_no', '未识别')}")
        print(f"预算金额：{analysis.get('budget', '未识别')}")
        print(f"采购方式：{analysis.get('procurement_method', '未识别')}")
        print(f"采购类型：{analysis.get('procurement_type', '未识别')}")
        print(f"合同类型：{analysis.get('contract_type', '未识别')}")

        print()
        print("### 关键时间节点")
        for k, v in analysis.get("key_dates", {}).items():
            print(f"  {k}: {v}")

        print()
        print("### 评分标准")
        sc = analysis.get("scoring_criteria", {})
        for k, v in sc.items():
            print(f"  {k}: {v}")

        print()
        print("### 资格条件")
        for q in analysis.get("qualification_requirements", []):
            print(f"  [{q['type']}] {q['content']}")

        print()
        print("=" * 60)
        print(risk_report)
        print()
        print("=" * 60)
        print(checklist)

    # 生成文件哈希（用于AI合规存证）
    if text:
        file_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        print()
        print("### 文件存证")
        print(f"SHA-256: {file_hash}")
        print("（可将此哈希值用于电子投标文件存证声明）")
