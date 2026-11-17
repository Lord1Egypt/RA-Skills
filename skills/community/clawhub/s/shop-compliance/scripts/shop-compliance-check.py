#!/usr/bin/env python3
"""
Shop-Compliance — 中小商家电商合规快速筛查工具
基于《电子商务法》《个人信息保护法》《广告法》《消费者权益保护法》
《网络交易监督管理办法》《七日无理由退货暂行办法》等行业法规

适用人群：电商平台上的中小商家、品牌方、个体店铺
运行模式：纯本地，无网络请求
一句话定位：5 分钟自查，告诉你店铺有没有踩雷
"""

import argparse
import datetime
import json
import sys
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional


# ============================================================
# 数据模型
# ============================================================

@dataclass
class CheckResult:
    check_id: str
    description: str
    severity: str       # "PASS" / "WARN" / "FAIL"
    passed: bool
    details: str        # 一句话解释
    recommendation: str  # 商家能直接照做的建议
    regulation_ref: str
    pro_available: str = ""  # Pro 版功能提示


@dataclass
class CheckReport:
    tool_name: str
    version: str
    timestamp: str
    scenario: str
    summary: dict
    items: list
    raw_items: list = field(default_factory=list)

    def to_dict(self):
        return {
            "tool": self.tool_name,
            "version": self.version,
            "timestamp": self.timestamp,
            "scenario": self.scenario,
            "summary": self.summary,
            "items": self.items,
        }


# ============================================================
# 检查项
# ============================================================
class ShopComplianceChecker:
    SCENARIOS = {
        "listing": "商品上架合规",
        "consumer": "消费者权益",
        "data": "客户信息保护",
        "marketing": "营销合规",
        "full": "全量检查",
    }
    def get_scenarios(self): return list(self.SCENARIOS.items())

    def _r(self, cid, desc, sev, passed, details, rec, reg, pro=""):
        return CheckResult(cid, desc, sev, passed, details, rec, reg, pro)

    # === 商品上架 ===
    def ls_extreme_words(self, d):
        w=d.get("extreme_words",1);k=d.get("keywords_clean",1)
        issues=[]
        if not w:issues.append("标题/描述使用了'最'、'第一'、'100%'等极限词")
        if not k:issues.append("存在'全网最低''销量冠军'等违规表述")
        sev="FAIL"if not w else"WARN"if not k else"PASS"
        pro_tip="(Pro 版支持：22 项广告用语深度检查 + 行业词库自动匹配)"
        return self._r("ls_extreme","商品描述-极限词审查",sev,w and k,
            ";".join(issues)if issues else"未发现极限词问题",
            "打开商品编辑页 → 对照检查标题和详情中的'最、第一、极致、100%'等词 → 删除或替换为客观描述",
            "广告法 Art.4,9",pro_tip if not w else"")

    def ls_qualification(self, d):
        q=d.get("qualification_checked",1);s=d.get("special_license",1)
        issues=[]
        if not q:issues.append("未确认商品是否需要特殊资质")
        if not s:issues.append("缺少经营许可证或产品备案号")
        sev="FAIL"if not s else"WARN"if not q else"PASS"
        return self._r("ls_qual","商品资质-经营许可",sev,q and s,
            ";".join(issues)if issues else"资质齐全",
            "确认商品品类 → 食品需食品经营许可证、化妆品需备案号、电器需 3C 认证 → 资质上传到平台证照中心",
            "电子商务法 Art.10,12")

    def ls_honest(self, d):
        h=d.get("honest_desc",1);m=d.get("match_reality",1)
        issues=[]
        if not h:issues.append("商品描述存在夸大或不实")
        if not m:issues.append("商品图片/描述与实物不符")
        sev="FAIL"if not h or not m else"PASS"
        pro_tip="(Pro 版支持：详情页逐条审核 + 竞品可比性检查)"
        return self._r("ls_honest","商品描述-真实准确",sev,h and m,
            ";".join(issues)if issues else"描述真实准确",
            "逐条核对商品参数和宣称 → 有数据支撑的注明来源 → 实物图片与描述一致",
            "电子商务法 Art.17",pro_tip if not h or not m else"")

    # === 消费者权益 ===
    def cr_return(self, d):
        r=d.get("return_policy",1);m=d.get("return_marked",1);t=d.get("return_timely",1)
        issues=[]
        if not r:issues.append("未提供七天无理由退货")
        if not m:issues.append("不支持退货的商品未显著标注")
        if not t:issues.append("退货退款不及时")
        sev="FAIL"if not r else"WARN"if not m or not t else"PASS"
        pro_tip="(Pro 版支持：退货流程全项检查 + 自动生成合规退货政策文本)"
        return self._r("cr_return","消费者权益-七天无理由退货",sev,r and m,
            ";".join(issues)if issues else"退货合规",
            "开通七天无理由退货 → 不支持退货的商品在标题下方单独标注 → 收到退货后 48 小时内退款",
            "七日无理由退货暂行办法",pro_tip if not r or not m else"")

    def cr_auto_renew(self, d):
        a=d.get("auto_renew_clear",1);c=d.get("cancel_easy",1)
        issues=[]
        if not a:issues.append("自动续费未显著提示")
        if not c:issues.append("自动续费取消不便捷")
        sev="FAIL"if not a or not c else"PASS"
        return self._r("cr_auto","消费者权益-自动续费合规",sev,a and c,
            ";".join(issues)if issues else"自动续费合规",
            "购买时用加粗/弹窗提示自动续费条款 → 取消入口在 3 步内可达 → 提供明确的取消说明",
            "电子商务法 Art.18")

    def cr_complaint(self, d):
        c=d.get("complaint_channel",1);h=d.get("complaint_handled",1)
        issues=[]
        if not c:issues.append("未公示投诉渠道")
        if not h:issues.append("投诉处理不及时")
        sev="WARN"if not c or not h else"PASS"
        return self._r("cr_complaint","消费者权益-投诉处理",sev,c and h,
            ";".join(issues)if issues else"投诉渠道畅通",
            "在店铺首页/客服自动回复中公示投诉电话或微信 → 设置 24-48 小时内响应机制",
            "消费者权益保护法 Art.24")

    # === 客户信息保护 ===
    def dp_sharing(self, d):
        s=d.get("third_party_shared",0);a=d.get("data_agreement",1)
        issues=[]
        if s and not a:issues.append("已将客户信息给第三方使用但未签数据安全协议")
        if not s:issues.append("未确认是否涉及客户信息共享") if not issues else None
        sev="FAIL"if s and not a else"WARN"if not s and not a else"PASS"
        pro_tip="(Pro 版支持：数据共享全链路检查 + 委托处理协议模板)"
        return self._r("dp_sharing","数据保护-信息共享管控",sev,a if s else True,
            ";".join(issues)if issues else"信息共享合规" if not s else"合规",
            "梳理客户信息给过哪些第三方（打单软件/代发/客服外包） → 与每家签署数据安全协议 → 明确对方不得另作他用",
            "PIPL Art.21",pro_tip if not a else"")

    def dp_privacy(self, d):
        p=d.get("privacy_screen",1);s=d.get("data_storage",1)
        issues=[]
        if not p:issues.append("未开启隐私面单")
        if not s:issues.append("客户信息在本地存储不安全（如 Excel 导出、微信群发）")
        sev="WARN"if not p or not s else"PASS"
        pro_tip="(Pro 版支持：全链路数据流向检查 + 隐私面单配置指南)"
        return self._r("dp_privacy","数据保护-隐私面单与存储",sev,p and s,
            ";".join(issues)if issues else"数据存储安全",
            "在平台后台开启隐私面单（隐藏手机号中间 4 位）→ 客户信息只在后台查看，不要导出到 Excel 或发到微信群",
            "PIPL Art.6")

    def dp_cleanup(self, d):
        p=d.get("cleanup_plan",1);t=d.get("cleanup_timely",1)
        issues=[]
        if not p:issues.append("无客户数据定期清理计划")
        if not t:issues.append("已完成订单的客户信息未及时删除")
        sev="WARN"if not p else"PASS"
        pro_tip="(Pro 版支持：数据清理全流程自动化 + 删除记录存证)"
        return self._r("dp_cleanup","数据保护-数据清理",sev,p and t,
            ";".join(issues)if issues else"有数据清理机制",
            "设置定期清理规则 → 订单完成后 1 年可删除客户信息 → 店铺注销前必须全线删除",
            "PIPL Art.19,47",pro_tip if not p or not t else"")

    # === 营销合规 ===
    def mk_live(self, d):
        l=d.get("live_compliant",1);w=d.get("live_words",1);c=d.get("live_claim",1)
        issues=[]
        if not l:issues.append("直播话术未经审核")
        if not w:issues.append("使用了绝对化用语或虚假功效宣称")
        if not c:issues.append("涉及数据/功效的宣称没有依据")
        sev="FAIL"if not w else"WARN"if not l or not c else"PASS"
        pro_tip="(Pro 版支持：直播话术实时审核 + 行业红线词库)"
        return self._r("mk_live","营销合规-直播话术",sev,l and w,
            ";".join(issues)if issues else"直播合规",
            "直播前准备话术清单 → 避免'最、第一、治好'等禁用词 → 功效宣称有数据支撑 → 保留直播回放至少 3 个月",
            "广告法 Art.4,28",pro_tip if not w else"")

    def mk_price(self, d):
        p=d.get("price_real",1);o=d.get("origin_price_real",1)
        issues=[]
        if not p:issues.append("促销价格不真实")
        if not o:issues.append("原价/划线价不真实（未真实销售过）")
        sev="FAIL"if not p or not o else"PASS"
        return self._r("mk_price","营销合规-促销价格",sev,p and o,
            ";".join(issues)if issues else"促销价格合规",
            "促销价必须是真实优惠 → 划线价必须在该店铺/该商品 7 天内有过真实成交 → 建议使用'参考价'而非'原价'",
            "价格法 Art.14")

    def mk_sms(self, d):
        s=d.get("sms_consent",1);o=d.get("sms_optout",1)
        issues=[]
        if not s:issues.append("营销短信未经用户同意")
        if not o:issues.append("营销短信无退订方式或退订无效")
        sev="FAIL"if not s else"WARN"if not o else"PASS"
        return self._r("mk_sms","营销合规-短信营销",sev,s and o,
            ";".join(issues)if issues else"短信营销合规",
            "只在用户同意后发营销短信 → 每条短信包含'回复T退订' → 退订请求 24 小时内执行",
            "通信短信息服务管理规定 Art.11")

    # === Route ===
    def run(self, scenario, data):
        if scenario=="full":
            r=[]
            for s in["listing","consumer","data","marketing"]:
                r.extend(self.run(s,data))
            return r
        fns=[]
        if scenario=="listing":fns=[self.ls_extreme_words,self.ls_qualification,self.ls_honest]
        elif scenario=="consumer":fns=[self.cr_return,self.cr_auto_renew,self.cr_complaint]
        elif scenario=="data":fns=[self.dp_sharing,self.dp_privacy,self.dp_cleanup]
        elif scenario=="marketing":fns=[self.mk_live,self.mk_price,self.mk_sms]
        return[fn(data)for fn in fns]


# ============================================================
# 交互式问答
# ============================================================

SCENARIO_QUESTIONS = {
    "listing": [
        ("extreme_words", "商品标题或详情中是否包含'最'、'第一'、'100%'、'顶级'等词？(y/n，有风险请选 n): "),
        ("keywords_clean", "是否存在'全网最低价'、'销量冠军'、'极致'等极限描述？(y/n，有风险请选 n): "),
        ("qualification_checked", "上架前是否确认过商品是否需要特殊资质（食品/化妆品/3C/医疗器械）？(y/n): "),
        ("special_license", "如需要特殊资质，是否已上传相关许可证或备案号？(y/n/跳过): "),
        ("honest_desc", "商品描述是否真实，无夸大效果或虚假宣称？(y/n): "),
        ("match_reality", "商品图片和详情描述是否与实物一致？(y/n): "),
    ],
    "consumer": [
        ("return_policy", "店铺是否支持七天无理由退货？(y/n): "),
        ("return_marked", "不支持退货的商品是否在商品标题下方显著标注？(y/n/跳过): "),
        ("return_timely", "收到退货后是否在 48 小时内完成退款？(y/n): "),
        ("auto_renew_clear", "自动续费是否在购买时显著提示？(y/n/跳过): "),
        ("cancel_easy", "自动续费的取消入口是否在 3 步操作内可达？(y/n/跳过): "),
        ("complaint_channel", "是否在店铺首页公示了投诉渠道？(y/n): "),
        ("complaint_handled", "收到投诉后是否在 24-48 小时内响应处理？(y/n): "),
    ],
    "data": [
        ("third_party_shared", "是否将客户信息（姓名/电话/地址）提供给第三方使用（打单软件/代发/客服外包）？(y/n): "),
        ("data_agreement", "如果共享了，是否与第三方签署了数据安全协议？(y/n/跳过): "),
        ("privacy_screen", "是否已开启平台的隐私面单功能？(y/n): "),
        ("data_storage", "客户信息是否仅限店铺后台查看，未导出到 Excel 或发到微信群？(y/n): "),
        ("cleanup_plan", "是否有客户数据定期清理计划？（如：订单完成 1 年后删除）(y/n): "),
        ("cleanup_timely", "已完成超过 1 年的订单客户信息是否已清理？(y/n): "),
    ],
    "marketing": [
        ("live_compliant", "直播带货时是否有话术清单或提示板？(y/n/跳过): "),
        ("live_words", "直播中是否避免使用'最、第一、治好、100%有效'等违禁词？(y/n): "),
        ("live_claim", "涉及功效/数据的宣称是否有依据？（如：有检测报告、有数据来源）(y/n): "),
        ("price_real", "促销价格是否是真实优惠（不是先提价再打折）？(y/n): "),
        ("origin_price_real", "划线价/原价在该店铺 7 天内是否有过真实成交？(y/n): "),
        ("sms_consent", "发送营销短信前是否获得用户同意？(y/n/跳过): "),
        ("sms_optout", "营销短信中是否包含退订方式且有效？(y/n/跳过): "),
    ],
}


def interactive_input(scenario: str) -> dict:
    """交互式问答"""
    data = {}
    questions = SCENARIO_QUESTIONS.get(scenario, [])

    print(f"\n{'='*50}")
    print(f"🛒 {ShopComplianceChecker.SCENARIOS.get(scenario, scenario)} — 快速自查")
    print(f"{'='*50}")
    print("（输入 y/n 或按提示输入，直接回车默认为 n）\n")

    for key, prompt in questions:
        raw = input(prompt).strip().lower()
        if key == "special_license" and raw == "skip":
            data[key] = True  # 跳过资质检查
        elif key == "third_party_shared":
            data[key] = raw.startswith("y")
        elif key in ("return_marked","auto_renew_clear","cancel_easy","data_agreement","live_compliant","sms_consent","sms_optout"):
            data[key] = True if raw == "skip" else raw.startswith("y")
        else:
            data[key] = raw.startswith("y")

    return data


# ============================================================
# 报告生成
# ============================================================

def generate_report_markdown(report: CheckReport) -> str:
    lines = []
    lines.append(f"# 🛒 Shop-Compliance 电商合规快速筛查报告\n")
    lines.append(f"**工具版本**: {report.version}  ")
    lines.append(f"**检查时间**: {report.timestamp}  ")
    lines.append(f"**检查模块**: {ShopComplianceChecker.SCENARIOS.get(report.scenario, report.scenario)}  ")
    lines.append(f"**检查项**: {report.summary['total']} 项  ")
    lines.append(f"**合规率**: {report.summary['pass_rate']:.0f}%\n")

    lines.append("## 📊 总体结果\n")
    lines.append(f"- ✅ 合规: {report.summary['passed']} 项")
    lines.append(f"- ⚠️ 建议关注: {report.summary['warnings']} 项")
    lines.append(f"- ❌ 需要整改: {report.summary['failed']} 项\n")

    lines.append("## 📋 详细结果\n")
    for item in report.items:
        icon = "✅" if item["passed"] else ("❌" if item["severity"] == "FAIL" else "⚠️")
        lines.append(f"### {icon} {item['description']}")
        lines.append(f"**状态**: {item['severity']}  ")
        lines.append(f"**详情**: {item['details']}  ")
        lines.append(f"**建议**: {item['recommendation']}  ")
        lines.append(f"**法规依据**: {item['regulation_ref']}  ")
        if item.get('pro_available'):
            lines.append(f"💡 {item['pro_available']}  ")
        lines.append("")

    lines.append("---")
    lines.append(f"*本报告由 Shop-Compliance v{report.version} 自动生成，仅供参考，不构成法律意见。*")
    lines.append(f"*需要深度检查？Ad-Check Pro / Refund-Check Pro / Data-Check Pro / Penalty-Guard Pro 已在路上 *")
    return "\n".join(lines)


def generate_report_html(report: CheckReport) -> str:
    items_html = ""
    for item in report.items:
        sev_color = {"PASS": "#27ae60", "WARN": "#f39c12", "FAIL": "#e74c3c"}
        color = sev_color.get(item["severity"], "#333")
        icon = "&#10004;" if item["passed"] else ("&#10008;" if item["severity"] == "FAIL" else "&#9888;")
        pro_html = ""
        if item.get('pro_available'):
            pro_html = f'<p style="color:#8e44ad;font-size:0.9em;">💡 {item["pro_available"]}</p>'
        items_html += f"""
        <div class="check-item">
            <div class="check-header" style="border-left: 4px solid {color};">
                <span class="check-icon" style="color: {color};">{icon}</span>
                <span class="check-title">{item['description']}</span>
                <span class="check-status" style="background: {color}20; color: {color};">{item['severity']}</span>
            </div>
            <div class="check-body">
                <p><strong>详情：</strong>{item['details']}</p>
                <p><strong>建议：</strong>{item['recommendation']}</p>
                <p><strong>法规依据：</strong>{item['regulation_ref']}</p>
                {pro_html}
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>Shop-Compliance 电商合规快速筛查报告</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #333; line-height: 1.6; }}
h1 {{ color: #2c3e50; border-bottom: 2px solid #e67e22; padding-bottom: 10px; }}
.summary {{ display: flex; gap: 20px; margin: 20px 0; }}
.summary-card {{ background: #f8f9fa; border-radius: 8px; padding: 20px; flex: 1; text-align: center; }}
.summary-card.pass {{ border-top: 3px solid #27ae60; }}
.summary-card.warn {{ border-top: 3px solid #f39c12; }}
.summary-card.fail {{ border-top: 3px solid #e74c3c; }}
.num {{ font-size: 2em; font-weight: bold; }}
.pass .num {{ color: #27ae60; }}
.warn .num {{ color: #f39c12; }}
.fail .num {{ color: #e74c3c; }}
.check-item {{ background: #fff; border: 1px solid #eee; border-radius: 8px; margin: 10px 0; overflow: hidden; }}
.check-header {{ padding: 12px 16px; display: flex; align-items: center; gap: 10px; cursor: default; }}
.check-icon {{ font-size: 1.2em; }}
.check-title {{ flex: 1; font-weight: 500; }}
.check-status {{ padding: 2px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 600; }}
.check-body {{ padding: 0 16px 12px; color: #555; font-size: 0.95em; }}
.footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 0.85em; color: #999; }}
</style></head><body>
<h1>🛒 Shop-Compliance 电商合规快速筛查报告</h1>
<p><strong>工具版本：</strong>{report.version} &nbsp;|&nbsp; <strong>检查时间：</strong>{report.timestamp} &nbsp;|&nbsp; <strong>检查模块：</strong>{ShopComplianceChecker.SCENARIOS.get(report.scenario, report.scenario)}</p>
<div class="summary">
<div class="summary-card pass"><div class="num">{report.summary['passed']}</div><div>合规</div></div>
<div class="summary-card warn"><div class="num">{report.summary['warnings']}</div><div>建议关注</div></div>
<div class="summary-card fail"><div class="num">{report.summary['failed']}</div><div>需要整改</div></div>
</div>
{items_html}
<div class="footer">本报告由 Shop-Compliance v{report.version} 自动生成，仅供参考，不构成法律意见</div>
</body></html>"""


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Shop-Compliance — 中小商家电商合规快速筛查工具"
    )
    parser.add_argument(
        "--scenario", "-s",
        choices=list(ShopComplianceChecker.SCENARIOS.keys()),
        default="full",
        help="检查模块：listing(商品上架), consumer(消费者权益), data(数据保护), marketing(营销), full(全量)"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json", "html"],
        default="markdown",
        help="输出格式（默认 markdown）"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="交互式问答模式"
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="列出检查模块"
    )
    parser.add_argument(
        "--version", "-V",
        action="version",
        version="Shop-Compliance v1.0.0"
    )

    args = parser.parse_args()

    if args.list_scenarios:
        print("Shop-Compliance 检查模块：")
        for key, name in ShopComplianceChecker.SCENARIOS.items():
            print(f"  {key:15s} - {name}")
        return

    if args.interactive:
        data = interactive_input(args.scenario)
    else:
        data = {}

    checker = ShopComplianceChecker()
    results = checker.run(args.scenario, data)

    passed = sum(1 for r in results if r.severity == "PASS")
    warnings = sum(1 for r in results if r.severity == "WARN")
    failed = sum(1 for r in results if r.severity == "FAIL")
    total = len(results)

    report = CheckReport(
        tool_name="shop-compliance",
        version="1.0.0",
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        scenario=args.scenario,
        summary={
            "total": total, "passed": passed, "warnings": warnings,
            "failed": failed, "pass_rate": (passed / total * 100) if total else 0
        },
        items=[asdict(r) for r in results],
    )

    print(f"\n{'='*50}")
    print(f"🛒 Shop-Compliance 电商合规快速筛查报告")
    print(f"{'='*50}")
    print(f"模块: {ShopComplianceChecker.SCENARIOS.get(args.scenario, args.scenario)}")
    print(f"时间: {report.timestamp}")
    print(f"结果: {passed}/{total} 合规, {warnings} 建议关注, {failed} 需要整改")
    print(f"合规率: {report.summary['pass_rate']:.0f}%\n")

    for r in results:
        icon = "✅" if r.passed else ("❌" if r.severity == "FAIL" else "⚠️")
        print(f"  {icon} {r.description}")
        print(f"    详情: {r.details}")
        if not r.passed:
            print(f"    建议: {r.recommendation}")
        if r.pro_available:
            print(f"    💡 {r.pro_available}")
        print()

    if args.output:
        if args.format == "json":
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        elif args.format == "html":
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(generate_report_html(report))
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(generate_report_markdown(report))
        print(f"✅ 报告已保存到: {args.output}")


if __name__ == "__main__":
    main()
