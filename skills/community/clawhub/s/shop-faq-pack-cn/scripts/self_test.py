#!/usr/bin/env python3
"""Offline contract checks for the Markdown examples; no real merchant policy is verified."""
from pathlib import Path
import json
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "SKILL.md", "manifest.yaml", "agents/openai.yaml", "README.md", "README.en.md",
    "LICENSE", "icon-512.png", "assets/promo-1600x900.png",
    "fixtures/success.json", "fixtures/success-output.md",
    "fixtures/partial-unapproved-input.json", "fixtures/partial-unapproved-output.md",
    "fixtures/failure-missing-fields.json", "fixtures/failure-output.md",
]
errors = [f"missing file: {item}" for item in required if not (ROOT / item).is_file()]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def load(path):
    return json.loads(read(path))

if not errors:
    skill, manifest, agent = read("SKILL.md"), read("manifest.yaml"), read("agents/openai.yaml")
    checks = [
        ("name: shop-faq-pack-cn" in skill, "SKILL frontmatter name"),
        ("name: shop-faq-pack-cn" in manifest and "slug: shop-faq-pack-cn" in manifest, "manifest name/slug"),
        (re.search(r"^icon: icon-512\.png$", manifest, re.MULTILINE) is not None, "manifest root icon reference"),
        ("self_test: python3 scripts/self_test.py" in manifest, "self-test command"),
        ('default_prompt: "$shop-faq-pack-cn' in manifest, "manifest default prompt invocation"),
        ('default_prompt: "$shop-faq-pack-cn' in agent, "agent default prompt invocation"),
    ]
    errors.extend(f"invalid {name}" for ok, name in checks if not ok)
    for image, size in [("icon-512.png", (512, 512)), ("assets/promo-1600x900.png", (1600, 900))]:
        raw = (ROOT / image).read_bytes()
        if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 24:
            errors.append(f"invalid PNG: {image}")
        elif struct.unpack(">II", raw[16:24]) != size:
            errors.append(f"wrong PNG dimensions: {image}")

    success, success_output = load("fixtures/success.json"), read("fixtures/success-output.md")
    partial, partial_output = load("fixtures/partial-unapproved-input.json"), read("fixtures/partial-unapproved-output.md")
    failure, failure_output = load("fixtures/failure-missing-fields.json"), read("fixtures/failure-output.md")
    if "虚构测试商家" not in success.get("store_name", "") or "仅为虚构测试商家" not in success.get("approval_status", ""):
        errors.append("success input must explicitly be a fictional offline approval simulation")
    if not all(success.get(k) for k in ("shipping", "delivery", "after_sales", "specifications")):
        errors.append("success input lacks a required policy category")
    for phrase in ("签收后7日内", "商品未使用且包装完整", "非质量问题退货运费由买家承担",
                   "质量问题退货运费由商家承担", "支持换货", "质量问题及非质量问题均适用",
                   "非质量问题换货运费由买家承担", "质量问题换货运费由商家承担", "退款原路退回"):
        if phrase not in success.get("after_sales", ""):
            errors.append(f"success input lacks complete after-sales rule: {phrase}")
    if "不是现实商户授权" not in success_output or "不可作为真实店铺对外资料" not in success_output:
        errors.append("success output must state the fictional/offline scope")
    answer_lines = [line for line in success_output.splitlines() if line.startswith("A：")]
    citations = [line for line in success_output.splitlines() if line.startswith("依据：")]
    if not answer_lines or len(answer_lines) != len(citations):
        errors.append("every success answer must have one immediately following policy reference")
    lines = success_output.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("A：") and (index + 1 == len(lines) or not lines[index + 1].startswith("依据：")):
            errors.append("success answer missing adjacent policy reference")
            break
        if line.startswith("依据：") and not any(line.startswith(f"依据：{field}：") for field in ("shipping", "delivery", "after_sales", "specifications")):
            errors.append("success policy reference must name its source field")
            break

    if partial.get("approval_status") or "没有“已批准可对外使用”的明确状态" not in partial_output:
        errors.append("former unapproved facts must remain labeled as partial, not approved success")
    if partial.get("shipping") != "中国大陆订单满99元包邮；未满99元收取8元运费。新疆、西藏地区按结算页显示运费。":
        errors.append("partial fixture must preserve the former unapproved source facts")
    if "换货" in partial.get("after_sales", ""):
        errors.append("partial fixture must not supply an exchange rule")
    if "换货运费承担" not in partial_output:
        errors.append("partial output must list exchange-shipping responsibility as missing")

    expected_missing = {
        "approval_status", "shipping.free_shipping_condition", "shipping.non_free_shipping_charge", "shipping.region_rules",
        "delivery.processing_time", "delivery.transit_time", "delivery.holiday_notice",
        "after_sales.eligibility_conditions", "after_sales.request_period", "after_sales.return_shipping_responsibility",
        "after_sales.exchange_conditions", "after_sales.exchange_shipping_responsibility", "after_sales.refund_method", "specifications",
    }
    if set(failure.get("expected_missing_fields", [])) != expected_missing:
        errors.append("failure fixture must enumerate approval and every missing policy field")
    if failure.get("specifications") or failure.get("approval_status"):
        errors.append("failure fixture must lack specifications and approval status")
    if not all(term in failure_output for term in ("批准版本和状态", "换货运费承担", "规格")):
        errors.append("failure output must explain approval, exchange-freight, and specification gaps")

if errors:
    print("SELF-TEST FAILED (offline fixture/structure contract):")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("SELF-TEST PASSED: fictional approved success, preserved unapproved partial, answer citations, missing approval/exchange rules, and package structure.")
print("Note: this checks offline examples only; it does not verify any real merchant approval or policy truth.")
