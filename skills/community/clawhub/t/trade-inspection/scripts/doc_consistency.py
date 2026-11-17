#!/usr/bin/env python3
"""
doc_consistency.py — 外贸单证跨文档一致性核查工具
用法：python doc_consistency.py（交互式）或 python doc_consistency.py --batch data.json（批量）
JSON格式示例见文件注释部分。
"""

import json
import sys
import re
import io
from typing import Dict, Any, List, Tuple

# Fix Windows GBK encoding for console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 定义各文档类型的标准字段映射（标准化用）
NORMALIZATION_RULES = {
    "company_name": lambda v: re.sub(r"[.,\s]+", "", str(v).upper()),
    "invoice_no": lambda v: re.sub(r"[^A-Z0-9]", "", str(v).upper()),
    "hs_code": lambda v: re.sub(r"[^0-9.]", "", str(v)),
    "weight": lambda v: float(re.findall(r"[\d.]+", str(v))[0]) if re.findall(r"[\d.]+", str(v)) else None,
    "quantity": lambda v: int(re.findall(r"\d+", str(v))[0]) if re.findall(r"\d+", str(v)) else None,
    "text": lambda v: re.sub(r"\s+", " ", str(v).strip().lower()),
}


def normalize_field(value, field_type):
    """标准化字段值以便比对"""
    if value is None or value == "":
        return None
    normalizer = NORMALIZATION_RULES.get(field_type, NORMALIZATION_RULES["text"])
    return normalizer(value)


def compare_fields(doc1_name: str, doc2_name: str,
                   field_name: str, val1, val2,
                   field_type: str = "text") -> Tuple[str, str]:
    """
    比对两个字段，返回 (判定, 说明)
    判定：✅ 一致 / ⚠️ 形式差异 / ❌ 不一致 / — 无法比对
    """
    n1 = normalize_field(val1, field_type)
    n2 = normalize_field(val2, field_type)

    if n1 is None and n2 is None:
        return "—", "双方均无此字段"
    if n1 is None:
        return "⚠️", f"{doc1_name} 无此字段，{doc2_name} 有：{val2}"
    if n2 is None:
        return "⚠️", f"{doc2_name} 无此字段，{doc1_name} 有：{val1}"

    if n1 == n2:
        return "✅", f"一致：{val1}"
    else:
        # 进一步判断是形式差异还是实质差异
        # 形式差异：原始值去掉空格/大小写后相同
        raw1 = re.sub(r"\s+", "", str(val1)).lower()
        raw2 = re.sub(r"\s+", "", str(val2)).lower()
        if raw1 == raw2:
            return "⚠️", f"形式差异（实质一致）：{val1} vs {val2}"
        else:
            return "❌", f"实质不一致：{val1} ←→ {val2}"


def consistency_matrix(docs: Dict[str, Dict]) -> List[Dict]:
    """
    计算所有文档之间的字段一致性矩阵
    返回问题列表
    """
    # 定义需要比对的核心字段及类型
    CORE_FIELDS = [
        ("品名/产品描述", "description", "text"),
        ("HS编码", "hs_code", "hs_code"),
        ("数量", "quantity", "quantity"),
        ("计量单位", "unit", "text"),
        ("总毛重", "gross_weight", "weight"),
        ("总净重", "net_weight", "weight"),
        ("件数/箱数", "total_packages", "text"),
        ("原产国", "country_of_origin", "text"),
        ("发货人", "shipper", "company_name"),
        ("收货人", "consignee", "company_name"),
        ("发票号", "invoice_no", "invoice_no"),
        ("品牌/商标", "brand", "text"),
        ("唛头", "marks", "text"),
    ]

    issues = []
    doc_names = list(docs.keys())

    for field_cn, field_en, field_type in CORE_FIELDS:
        # 收集各文档中该字段的值
        values = {}
        for doc_name in doc_names:
            if field_en in docs[doc_name]:
                values[doc_name] = docs[doc_name][field_en]

        if not values:
            continue

        # 两两比对
        doc_list = list(values.keys())
        for i in range(len(doc_list)):
            for j in range(i + 1, len(doc_list)):
                doc1, doc2 = doc_list[i], doc_list[j]
                status, detail = compare_fields(
                    doc1, doc2, field_cn,
                    values[doc1], values[doc2], field_type
                )
                if status in ("❌", "⚠️"):
                    issues.append({
                        "field": field_cn,
                        "doc1": doc1,
                        "doc2": doc2,
                        "val1": values.get(doc1),
                        "val2": values.get(doc2),
                        "status": status,
                        "detail": detail,
                    })

    return issues


def generate_report(issues: List[Dict], docs: Dict[str, Dict]) -> str:
    """生成审核报告"""
    doc_names = list(docs.keys())
    total_fields_checked = len(set(i["field"] for i in issues)) if issues else 0

    report = []
    report.append("=" * 55)
    report.append("  📋 单证跨文档一致性核查报告")
    report.append("=" * 55)
    report.append(f"  审核文档：{', '.join(doc_names)}")
    report.append(f"  文档数量：{len(doc_names)}")
    report.append("-" * 55)

    if not issues:
        report.append("  ✅ 未发现不一致项，各文档字段匹配正常。")
    else:
        critical = [i for i in issues if i["status"] == "❌"]
        warning = [i for i in issues if i["status"] == "⚠️"]

        report.append(f"  发现问题合计：{len(issues)} 项")
        if critical:
            report.append(f"    ❌ 实质不一致（必须修改）：{len(critical)} 项")
        if warning:
            report.append(f"    ⚠️ 形式差异（建议确认）：{len(warning)} 项")

        report.append("")
        report.append("  【实质不一致项 — 必须修改】")
        for i, issue in enumerate(critical, 1):
            report.append(f"  {i}. 字段：{issue['field']}")
            report.append(f"     {issue['doc1']}：{issue['val1']}")
            report.append(f"     {issue['doc2']}：{issue['val2']}")
            report.append(f"     → 建议：核对原始合同/订单，统一表述后修改")

        if warning:
            report.append("")
            report.append("  【形式差异项 — 建议人工确认】")
            for i, issue in enumerate(warning, 1):
                report.append(f"  {i}. 字段：{issue['field']}")
                report.append(f"     {issue['doc1']}：{issue['val1']}")
                report.append(f"     {issue['doc2']}：{issue['val2']}")
                report.append(f"     → 说明：{issue['detail']}")

    report.append("")
    report.append("=" * 55)
    report.append("  ⚠️  本报告仅作辅助参考，不构成正式法律意见。")
    report.append("  ⚠️  任何 ❌ 项在修改前不建议出运。")
    report.append("=" * 55)

    return "\n".join(report)


def interactive_input():
    """交互式输入各文档字段"""
    print("\n📋 请依次输入各文档信息（直接回车跳过该字段）\n")

    docs = {}
    doc_types = {
        "1": ("发票 Invoice", ["invoice_no", "exporter", "buyer", "description",
                               "quantity", "unit", "unit_price", "total_amount",
                               "currency", "hs_code", "country_of_origin",
                               "gross_weight", "net_weight", "marks", "brand"]),
        "2": ("装箱单 Packing List", ["description", "quantity", "unit",
                                      "total_packages", "gross_weight", "net_weight", "marks", "brand"]),
        "3": ("提单 Bill of Lading", ["shipper", "consignee", "notify",
                                      "description", "packages", "gross_weight", "measurement", "hs_code"]),
        "4": ("产地证 Certificate of Origin", ["exporter", "consignee",
                                               "description", "hs_code", "country_of_origin", "invoice_no"]),
    }

    while True:
        print("\n请选择要输入的文档：")
        for k, (name, _) in doc_types.items():
            print(f"  {k}. {name}")
        print("  0. 完成输入，开始核查")

        choice = input("\n请输入选项：").strip()
        if choice == "0":
            break
        if choice not in doc_types:
            print("无效选项，请重试。")
            continue

        doc_name, fields = doc_types[choice]
        doc_data = {}
        print(f"\n📄 输入 {doc_name}（直接回车跳过该字段）:")

        for field in fields:
            val = input(f"  {field}: ").strip()
            if val:
                doc_data[field] = val

        docs[doc_name.split()[0]] = doc_data

    return docs


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--batch":
        # 批量模式
        with open(sys.argv[2], "r", encoding="utf-8-sig") as f:
            docs = json.load(f)
    else:
        # 交互模式
        docs = interactive_input()

    if len(docs) < 2:
        print("\n❌ 至少需要输入2个文档才能进行比对。")
        sys.exit(1)

    issues = consistency_matrix(docs)
    report = generate_report(issues, docs)
    print("\n" + report)


if __name__ == "__main__":
    main()
