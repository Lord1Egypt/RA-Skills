#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
checker = root / "scripts/check_eligibility.py"
for filename, expected in [("success.json", "122.00"), ("failure.json", "待确认")]:
    raw = (root / "fixtures" / filename).read_text()
    result = subprocess.run([sys.executable, str(checker)], input=raw, text=True, capture_output=True)
    if result.returncode: raise SystemExit(result.stderr)
    got = json.loads(result.stdout)["calculation"]["应付草稿"]
    if got != expected: raise SystemExit(f"{filename}: got {got}, expected {expected}")
    delivery = root / "fixtures" / filename.replace('.json', '-delivery.json')
    if json.loads(result.stdout) != json.loads(delivery.read_text()):
        raise SystemExit(f"{filename}: delivery fixture does not match actual output")
# Regression checks: order must override array order, excluded SKU must remain
# undiscounted, and a known type without its value must yield a draft.
success = json.loads((root / "fixtures/success.json").read_text())
result = subprocess.run([sys.executable, str(checker)], input=json.dumps(success), text=True, capture_output=True)
payload = json.loads(result.stdout)
if [step["优惠"] for step in payload["calculation"]["steps"]] != success["stacking_order"]:
    raise SystemExit("stacking_order was not applied")
if payload["calculation"]["steps"][-1]["应付小计"] != "122.00":
    raise SystemExit("excluded SKU was discounted")
# Same two promotions in reverse JSON order must still run fixed then percent;
# without the excluded line this is the documented 100 -> 80 -> 72 case.
order_case = json.loads(json.dumps(success))
order_case["cart"] = [{"sku": "A", "unit_price": "100", "quantity": 1}]
result = subprocess.run([sys.executable, str(checker)], input=json.dumps(order_case), text=True, capture_output=True)
if json.loads(result.stdout)["calculation"]["应付草稿"] != "72.00":
    raise SystemExit("explicit stacking order did not override JSON array order")
order_case["stacking_order"] = ["A款9折", "满100减20"]
result = subprocess.run([sys.executable, str(checker)], input=json.dumps(order_case), text=True, capture_output=True)
if json.loads(result.stdout)["calculation"]["应付草稿"] != "70.00":
    raise SystemExit("percent-then-fixed stacking calculation is incorrect")
failure = json.loads((root / "fixtures/failure.json").read_text())
result = subprocess.run([sys.executable, str(checker)], input=json.dumps(failure), text=True, capture_output=True)
if "满减金额未提供" not in result.stdout or "折扣比例未提供" not in result.stdout:
    raise SystemExit("missing promotion values were not reported")
failure_output = json.loads(result.stdout)
if not any(c["条件"] == "门槛运费口径" and "运费是否计入门槛未明确" in c["依据"] for c in failure_output["conditions"]):
    raise SystemExit("missing threshold shipping inclusion must be reported as an independent condition")
later_basis = failure_output["calculation"]["steps"][1]["计算依据"]
if later_basis["当前优惠前余额"] != "待确认" or "100.00" in later_basis["公式"]:
    raise SystemExit("a prior pending same-SKU offer must not publish the original cart balance as the later current balance")
def evaluate(data):
    r = subprocess.run([sys.executable, str(checker)], input=json.dumps(data), text=True, capture_output=True)
    return r
def evaluate_raw(raw):
    return subprocess.run([sys.executable, str(checker)], input=raw, text=True, capture_output=True)
partial = json.loads(json.dumps(failure))
partial["promotions"][0].update({"name":"门槛不足但时间未知","eligible_skus":["A"],"threshold_basis":"优惠前商品额","threshold":"200","threshold_includes_shipping":False,"timezone":"Asia/Shanghai"})
partial["promotions"][1].update({"name":"另一优惠","eligible_skus":["A"],"threshold_basis":"商品额","threshold":"0","threshold_includes_shipping":False,"timezone":"No/Such_Zone","start":"2026-01-01T00:00:00+08:00","end":"2027-01-01T00:00:00+08:00"})
partial["current_time"] = "2026-10-04T12:00:00+08:00"
partial["stacking_order"] = ["门槛不足但时间未知", "另一优惠"]
out = evaluate(partial)
if out.returncode: raise SystemExit("invalid timezone must return a reviewable result")
conditions = json.loads(out.stdout)["conditions"]
first = {c["条件"]: c["状态"] for c in conditions if c["优惠"] == "门槛不足但时间未知"}
if first.get("有效期") != "待确认" or first.get("门槛") != "不可用": raise SystemExit("condition states must preserve unknown time and known unmet threshold")
if {c["状态"] for c in conditions if c["优惠"] == "另一优惠" and c["条件"] == "有效期"} != {"待确认"}: raise SystemExit("invalid timezone must be an explicit pending condition")
# Missing shipping is unknown payable, never an implicit free-shipping amount.
no_shipping = json.loads(json.dumps(success))
no_shipping.pop("shipping_fee", None)
out = evaluate(no_shipping)
missing_ship = json.loads(out.stdout)
if missing_ship["calculation"]["应付草稿"] != "待确认" or missing_ship["calculation"]["运费"] != "待确认":
    raise SystemExit("missing shipping fee must keep payable draft pending")
# A pending first promotion makes later post-discount thresholds and amount steps uncertain.
uncertain_chain = json.loads(json.dumps(order_case))
uncertain_chain["promotions"][0].pop("start", None)
uncertain_chain["promotions"][0].pop("end", None)
uncertain_chain["promotions"][1]["threshold_basis"] = "优惠后商品额"
uncertain_chain["promotions"][1]["threshold"] = "75"
out = evaluate(uncertain_chain)
chain = json.loads(out.stdout)
second_threshold = next(c for c in chain["conditions"] if c["优惠"] == uncertain_chain["promotions"][1]["name"] and c["条件"] == "门槛")
if second_threshold["状态"] != "待确认" or "前序优惠状态待确认" not in second_threshold["依据"]:
    raise SystemExit("post-discount threshold must inherit prior promotion uncertainty")
if chain["calculation"]["steps"][0]["优惠额"] != "待确认" or chain["calculation"]["steps"][1]["应付小计"] != "待确认":
    raise SystemExit("uncertain promotion amounts and subsequent subtotal must remain pending")
unavailable_after_pending = json.loads(json.dumps(order_case))
unavailable_after_pending["cart"] = [{"sku":"A","unit_price":"10","quantity":1}]
unavailable_after_pending["promotions"] = [
    {"name":"前券金额待确认","eligible_skus":["A"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"type":"fixed"},
    {"name":"后券门槛不可能达到","eligible_skus":["A"],"threshold":"100","threshold_basis":"优惠前商品额","threshold_includes_shipping":False,"type":"fixed","amount":"2"}
]
unavailable_after_pending["stacking_order"] = ["前券金额待确认","后券门槛不可能达到"]
unavailable_result = json.loads(evaluate(unavailable_after_pending).stdout)
unavailable_step = unavailable_result["calculation"]["steps"][1]
if (unavailable_step["优惠额"] != "0.00"
        or unavailable_step["计算依据"]["行级扣减"][0]["本步扣减"] != "0.00"
        or "实际应用金额 0.00" not in unavailable_step["计算依据"]["公式"]):
    raise SystemExit("a deterministically unavailable later offer must have zero amount and zero line deductions despite prior uncertainty")
sku_local = json.loads(json.dumps(order_case))
sku_local["cart"] = [{"sku":"A","unit_price":"100","quantity":1},{"sku":"B","unit_price":"100","quantity":1}]
sku_local["promotions"] = [
    {"name":"A款时间待确认","eligible_skus":["A"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"type":"fixed","amount":"10"},
    {"name":"B款优惠后门槛","eligible_skus":["B"],"threshold":"90","threshold_basis":"优惠后商品额","threshold_includes_shipping":False,"type":"fixed","amount":"10"}
]
sku_local["stacking_order"] = ["A款时间待确认","B款优惠后门槛"]
sku_local_result = json.loads(evaluate(sku_local).stdout)
b_threshold = next(c for c in sku_local_result["conditions"] if c["优惠"]=="B款优惠后门槛" and c["条件"]=="门槛")
if b_threshold["状态"] != "可用": raise SystemExit("an uncertain promotion on SKU A must not poison a post-discount threshold on SKU B")
if sku_local_result["calculation"]["steps"][1]["应付小计"] != "待确认" or sku_local_result["calculation"]["应付草稿"] != "待确认":
    raise SystemExit("uncertainty on SKU A must keep the whole-cart subtotal pending even while SKU B is calculable")
same_sku_pending = json.loads(json.dumps(sku_local))
same_sku_pending["promotions"][1]["eligible_skus"] = ["A"]
same_sku_pending["promotions"][1]["threshold_basis"] = "优惠前商品额"
same_sku_pending_result = json.loads(evaluate(same_sku_pending).stdout)
same_sku_value = next(c for c in same_sku_pending_result["conditions"] if c["优惠"]=="B款优惠后门槛" and c["条件"]=="优惠值")
if same_sku_value["状态"] != "待确认" or "前序优惠状态待确认" not in same_sku_value["依据"]:
    raise SystemExit("a pending earlier promotion on the same SKU must keep later fixed-discount affordability pending")
multi = json.loads(json.dumps(order_case))
multi["cart"] = [{"sku":"A","unit_price":"100","quantity":1},{"sku":"B","unit_price":"50","quantity":1}]
multi["promotions"] = [{"name":"跨SKU减额","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"20"}]
multi["stacking_order"] = ["跨SKU减额"]
out = evaluate(multi)
payload = json.loads(out.stdout)
if payload["calculation"]["steps"][0]["优惠额"] != "20.00" or payload["calculation"]["应付草稿"] != "130.00": raise SystemExit("a merchant-confirmed cart-order allocation rule must be applied")
# A later SKU-specific discount makes an unstated allocation materially affect
# the answer.  Reversing cart rows must therefore never turn either variant
# into a definite payable draft.
allocation_chain = json.loads(json.dumps(multi))
allocation_chain["cart"] = [{"sku":"A","unit_price":"100","quantity":1},{"sku":"B","unit_price":"100","quantity":1}]
allocation_chain["promotions"] = [
    {"name":"跨SKU减100","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"100"},
    {"name":"A款9折","eligible_skus":["A"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"percent","percent":"90","rounding_mode":"total_half_up_2"},
]
allocation_chain["stacking_order"] = ["跨SKU减100", "A款9折"]
for cart in (allocation_chain["cart"], list(reversed(allocation_chain["cart"]))):
    case = json.loads(json.dumps(allocation_chain))
    case["cart"] = cart
    result = json.loads(evaluate(case).stdout)
    if result["calculation"]["应付草稿"] != "待确认" or any(step["优惠额"] != "待确认" for step in result["calculation"]["steps"]):
        raise SystemExit("unstated fixed-discount allocation must stay pending regardless of cart row order")
    first_basis = result["calculation"]["steps"][0]["计算依据"]["行级扣减"]
    if any(row["本步扣减"] != "待确认" for row in first_basis):
        raise SystemExit("unstated allocation must not expose guessed cart-order line deductions")
allocation_chain["promotions"][0]["allocation_rule"] = "cart_order"
allocated_results = []
for cart in (allocation_chain["cart"], list(reversed(allocation_chain["cart"]))):
    case = json.loads(json.dumps(allocation_chain)); case["cart"] = cart
    allocated_results.append(json.loads(evaluate(case).stdout)["calculation"]["应付草稿"])
if allocated_results != ["100.00", "90.00"]: raise SystemExit("the merchant-confirmed cart-order allocation rule was not applied")
# A later full-scope offer can consume the remaining aggregate balance before
# any partial-SKU offer observes the unknown earlier split.
cleared_chain = json.loads(json.dumps(allocation_chain))
cleared_chain["promotions"] = [
    {"name":"AB减20","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"20"},
    {"name":"AB减180","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"180"},
    {"name":"A九折","eligible_skus":["A"],"threshold":"0","threshold_basis":"优惠后商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"percent","percent":"90","rounding_mode":"total_half_up_2"},
]
cleared_chain["stacking_order"] = ["AB减20", "AB减180", "A九折"]
cleared_result = json.loads(evaluate(cleared_chain).stdout)
if cleared_result["calculation"]["应付草稿"] != "0.00" or any(c["优惠"] == "AB减20" and c["条件"] == "优惠分摊" for c in cleared_result["conditions"]):
    raise SystemExit("a later full-scope offer that clears the balance must make the earlier allocation irrelevant")
# A zero post-discount threshold, or a threshold already met by confirmed
# shipping, is certain even when earlier same-SKU discounts are pending.
for threshold_case in (("0", "0", False), ("5", "5", True)):
    pending_threshold = json.loads(json.dumps(allocation_chain))
    pending_threshold["shipping_fee"] = threshold_case[1]
    pending_threshold["promotions"][1].update({"name":"A门槛九折","threshold_basis":"优惠后商品额","threshold":threshold_case[0],"threshold_includes_shipping":threshold_case[2]})
    pending_threshold["stacking_order"] = ["跨SKU减100", "A门槛九折"]
    pending_threshold_result = json.loads(evaluate(pending_threshold).stdout)
    condition = next(c for c in pending_threshold_result["conditions"] if c["优惠"] == "A门槛九折" and c["条件"] == "门槛")
    if condition["状态"] != "可用":
        raise SystemExit("a zero or shipping-covered post-discount threshold must remain deterministically satisfied")
# A current promotion with unresolved required facts cannot establish that a
# line-level allocation is needed.  Its missing fact already keeps the
# promotion pending; allocation is checked only after the promotion is usable.
pending_allocation = json.loads(json.dumps(allocation_chain))
pending_allocation["promotions"][0].pop("end")
pending_allocation["promotions"][0].pop("allocation_rule", None)
pending_allocation_result = json.loads(evaluate(pending_allocation).stdout)
if any(c["优惠"] == "跨SKU减100" and c["条件"] == "优惠分摊" for c in pending_allocation_result["conditions"]):
    raise SystemExit("a pending current promotion must not report allocation before it is usable")
# A known zero-effect later offer cannot observe or depend on earlier line
# allocation, even when it selects only one SKU.
for zero_later in (
    {"name":"A款减0","eligible_skus":["A"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"0"},
    {"name":"A款应付100%","eligible_skus":["A"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"percent","percent":"100","rounding_mode":"total_half_up_2"},
):
    zero_follow = json.loads(json.dumps(multi))
    zero_follow["cart"] = [{"sku":"A","unit_price":"100","quantity":1},{"sku":"B","unit_price":"100","quantity":1}]
    zero_follow["promotions"] = [
        {"name":"AB减20","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"20"},
        zero_later,
    ]
    zero_follow["stacking_order"] = ["AB减20", zero_later["name"]]
    zero_follow_result = json.loads(evaluate(zero_follow).stdout)
    if zero_follow_result["calculation"]["应付草稿"] != "180.00" or any(c["条件"] == "优惠分摊" and c["状态"] == "待确认" for c in zero_follow_result["conditions"]):
        raise SystemExit("a later zero-effect SKU offer must not require allocation from the prior promotion")
# Zero-effect promotions cannot change any line balance, so they must not
# require an allocation rule before a later SKU-specific offer.
for zero_rule in (
    dict(allocation_chain["promotions"][0], name="跨SKU减0", amount="0"),
    dict(allocation_chain["promotions"][0], name="跨SKU应付100%", type="percent", percent="100", rounding_mode="total_half_up_2"),
):
    zero_rule.pop("allocation_rule", None)
    zero_case = json.loads(json.dumps(allocation_chain))
    zero_case["promotions"] = [zero_rule, zero_case["promotions"][1]]
    zero_case["stacking_order"] = [zero_rule["name"], zero_case["promotions"][1]["name"]]
    result = json.loads(evaluate(zero_case).stdout)
    if result["calculation"]["应付草稿"] != "190.00" or any(c["条件"] == "优惠分摊" and c["状态"] == "待确认" for c in result["conditions"]):
        raise SystemExit("a zero-effect promotion must not require allocation for a later SKU-specific promotion")
# Even an otherwise incomplete zero-effect rule cannot change balances.  Its
# missing time facts remain in the condition table but must not poison the
# later SKU-specific calculation or payable draft.
zero_unknown = json.loads(json.dumps(allocation_chain))
zero_unknown["promotions"][0] = {"name":"跨SKU减0时间未知","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"type":"fixed","amount":"0"}
zero_unknown["stacking_order"] = ["跨SKU减0时间未知", "A款9折"]
zero_unknown_result = json.loads(evaluate(zero_unknown).stdout)
if zero_unknown_result["calculation"]["应付草稿"] != "190.00" or zero_unknown_result["calculation"]["steps"][0]["优惠额"] != "0.00":
    raise SystemExit("an uncertain zero-effect promotion must not make later balances pending")
# If the next rule covers the same complete SKU set, only the aggregate
# post-discount balance matters; an arbitrary line allocation cannot change
# the next threshold or payable total.
same_set_chain = json.loads(json.dumps(allocation_chain))
same_set_chain["shipping_fee"] = "0"
same_set_chain["promotions"] = [
    {"name":"AB减20","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"20"},
    {"name":"AB九折","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"优惠后商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"percent","percent":"90","rounding_mode":"total_half_up_2"}
]
same_set_chain["stacking_order"] = ["AB减20","AB九折"]
same_set_result = json.loads(evaluate(same_set_chain).stdout)
if same_set_result["calculation"]["应付草稿"] != "162.00" or any(c["条件"]=="优惠分摊" and c["状态"]=="待确认" for c in same_set_result["conditions"]):
    raise SystemExit("identical eligible SKU sets must not require allocation when aggregate discount is invariant")
# A later offer may cover every SKU affected by the earlier split and also
# include additional SKUs. Its aggregate basis remains known, so it must not
# require the earlier allocation rule.
superset_chain = json.loads(json.dumps(allocation_chain))
superset_chain["shipping_fee"] = "0"
superset_chain["cart"] = [{"sku": sku, "unit_price": "100", "quantity": 1} for sku in ("A", "B", "C")]
superset_chain["promotions"] = [
    {"name":"AB减20","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"20"},
    {"name":"ABC九折","eligible_skus":["A","B","C"],"threshold":"0","threshold_basis":"优惠后商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"percent","percent":"90","rounding_mode":"total_half_up_2"},
]
superset_chain["stacking_order"] = ["AB减20", "ABC九折"]
superset_result = json.loads(evaluate(superset_chain).stdout)
if (superset_result["calculation"]["应付草稿"] != "252.00"
        or any(c["优惠"] == "AB减20" and c["条件"] == "优惠分摊" and c["状态"] == "待确认" for c in superset_result["conditions"])):
    raise SystemExit("a later offer covering all affected SKUs plus extra SKUs must use the known aggregate without requesting allocation")
unknown_same_scope = json.loads(json.dumps(superset_chain))
unknown_same_scope["promotions"][1]["eligible_skus"] = ["A", "B"]
unknown_same_scope["promotions"][1].pop("amount", None)
unknown_same_scope["promotions"][1]["type"] = "fixed"
unknown_same_scope["promotions"][1].pop("percent", None)
unknown_same_scope["promotions"][1].pop("rounding_mode", None)
unknown_same_scope["stacking_order"] = ["AB减20", "ABC九折"]
unknown_same_scope_result = json.loads(evaluate(unknown_same_scope).stdout)
if (unknown_same_scope_result["calculation"]["steps"][0]["优惠额"] != "20.00"
        or any(c["优惠"] == "AB减20" and c["条件"] == "优惠分摊" for c in unknown_same_scope_result["conditions"])):
    raise SystemExit("a later unknown offer on the exact same SKU scope cannot make the prior aggregate discount depend on allocation")
superset_clear = json.loads(json.dumps(superset_chain))
superset_clear["promotions"][1].update({"name":"ABC减280","type":"fixed","amount":"280"})
superset_clear["promotions"].append({"name":"A九折","eligible_skus":["A"],"threshold":"0","threshold_basis":"优惠后商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"percent","percent":"90","rounding_mode":"total_half_up_2"})
superset_clear["stacking_order"] = ["AB减20", "ABC减280", "A九折"]
superset_clear_result = json.loads(evaluate(superset_clear).stdout)
if (superset_clear_result["calculation"]["应付草稿"] != "0.00"
        or any(c["优惠"] == "AB减20" and c["条件"] == "优惠分摊" for c in superset_clear_result["conditions"])):
    raise SystemExit("a later superset offer that certainly consumes the full cart balance must clear the earlier allocation dependency")
# The clearing proof is not limited to a zero threshold: a threshold based on
# the confirmed pre-discount scope total is equally independent of the earlier
# AB line allocation.
superset_positive_threshold = json.loads(json.dumps(superset_clear))
superset_positive_threshold["promotions"][1].update({"threshold": "300", "threshold_basis": "商品额"})
superset_positive_threshold_result = json.loads(evaluate(superset_positive_threshold).stdout)
if (superset_positive_threshold_result["calculation"]["应付草稿"] != "0.00"
        or any(c["优惠"] == "AB减20" and c["条件"] == "优惠分摊" for c in superset_positive_threshold_result["conditions"])):
    raise SystemExit("a confirmed positive pre-discount threshold must also prove superset clearing")
full_balance_chain = json.loads(json.dumps(allocation_chain))
full_balance_chain["shipping_fee"] = "0"
full_balance_chain["promotions"] = [
    {"name":"AB减200","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"200"},
    {"name":"A款九折","eligible_skus":["A"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"percent","percent":"90","rounding_mode":"total_half_up_2"}
]
full_balance_chain["stacking_order"] = ["AB减200", "A款九折"]
full_balance_result = json.loads(evaluate(full_balance_chain).stdout)
if full_balance_result["calculation"]["应付草稿"] != "0.00" or any(c["条件"] == "优惠分摊" and c["状态"] == "待确认" for c in full_balance_result["conditions"]):
    raise SystemExit("a confirmed fixed promotion that consumes the full eligible balance must not require allocation")
percent_zero_chain = json.loads(json.dumps(full_balance_chain))
percent_zero_chain["promotions"][0].update({"name":"AB应付0%", "type":"percent", "percent":"0", "rounding_mode":"total_half_up_2"})
percent_zero_chain["stacking_order"] = ["AB应付0%", "A款九折"]
percent_zero_result = json.loads(evaluate(percent_zero_chain).stdout)
if percent_zero_result["calculation"]["应付草稿"] != "0.00" or any(c["条件"] == "优惠分摊" and c["状态"] == "待确认" for c in percent_zero_result["conditions"]):
    raise SystemExit("a confirmed 0% payable rate that consumes the full eligible balance must not require allocation")
rounded_clear_chain = json.loads(json.dumps(percent_zero_chain))
rounded_clear_chain["cart"] = [{"sku":"A","unit_price":"0.01","quantity":1},{"sku":"B","unit_price":"0.01","quantity":1}]
rounded_clear_chain["promotions"][0].update({"name":"AB应付25%","percent":"25"})
rounded_clear_chain["stacking_order"] = ["AB应付25%", "A款九折"]
rounded_clear_result = json.loads(evaluate(rounded_clear_chain).stdout)
rounded_clear_steps = rounded_clear_result["calculation"]["steps"]
if (rounded_clear_result["calculation"]["应付草稿"] != "0.00"
        or rounded_clear_steps[0]["优惠额"] != "0.02"
        or rounded_clear_steps[1]["计算依据"]["当前优惠前余额"] != "0.00"
        or any(c["优惠"] == "AB应付25%" and c["条件"] == "优惠分摊" and c["状态"] == "待确认" for c in rounded_clear_result["conditions"])):
    raise SystemExit("a rounded percentage discount that consumes the entire balance must not require allocation")
expired_allocation_chain = json.loads(json.dumps(allocation_chain))
expired_allocation_chain["promotions"][0]["end"] = "2026-10-01T00:00:00+08:00"
expired_allocation_chain["stacking_order"] = ["跨SKU减100", "A款9折"]
expired_allocation_result = json.loads(evaluate(expired_allocation_chain).stdout)
if any(c["优惠"] == "跨SKU减100" and c["条件"] == "优惠分摊" for c in expired_allocation_result["conditions"]):
    raise SystemExit("a definitively unavailable promotion must not request an irrelevant allocation rule")
# Unavailable takes precedence over missing details: an expired multi-SKU
# offer must not request allocation merely because its amount is also absent.
expired_incomplete = json.loads(json.dumps(expired_allocation_chain))
expired_incomplete["promotions"][0].pop("amount")
expired_incomplete_result = json.loads(evaluate(expired_incomplete).stdout)
if any(c["优惠"] == "跨SKU减100" and c["条件"] == "优惠分摊" for c in expired_incomplete_result["conditions"]):
    raise SystemExit("an expired promotion with missing details must not request allocation")
# Even a 100% payable rate needs an explicit merchant-confirmed rounding mode,
# because the contract requires that convention for every percentage rule.
missing_zero_rounding = json.loads(json.dumps(full_balance_chain))
missing_zero_rounding["promotions"] = [missing_zero_rounding["promotions"][1]]
missing_zero_rounding["stacking_order"] = ["A款九折"]
missing_zero_rounding["promotions"][0].update({"name":"A款应付100%", "percent":"100"})
missing_zero_rounding["promotions"][0].pop("rounding_mode", None)
missing_rounding_result = json.loads(evaluate(missing_zero_rounding).stdout)
missing_rounding_step = missing_rounding_result["calculation"]["steps"][0]
if (missing_rounding_result["calculation"]["应付草稿"] != "待确认"
        or missing_rounding_step["优惠额"] != "待确认"
        or "total_half_up_2" in missing_rounding_step["计算依据"]["舍入过程"]
        or "缺少商家确认的金额舍入规则" not in missing_rounding_step["计算依据"]["公式"]):
    raise SystemExit("a 100% payable promotion without a confirmed rounding mode must remain pending")
threshold_excludes_later = json.loads(json.dumps(allocation_chain))
threshold_excludes_later["shipping_fee"] = "0"
threshold_excludes_later["promotions"][1].update({"name":"A款门槛不足九折","threshold_basis":"优惠前商品额","threshold":"250"})
threshold_excludes_later["stacking_order"] = ["跨SKU减100", "A款门槛不足九折"]
threshold_excludes_result = json.loads(evaluate(threshold_excludes_later).stdout)
if threshold_excludes_result["calculation"]["应付草稿"] != "100.00" or any(c["条件"]=="优惠分摊" and c["状态"]=="待确认" for c in threshold_excludes_result["conditions"]):
    raise SystemExit("a later percentage promotion that definitively misses its pre-discount threshold must not force allocation")
# A promotion for SKUs absent from the cart is inapplicable even with a zero threshold.
excluded = json.loads(json.dumps(multi))
excluded["cart"] = [{"sku":"C","unit_price":"30","quantity":1}]
excluded["promotions"][0]["eligible_skus"] = ["A", "B"]
excluded["promotions"][0]["threshold"] = "0"
payload = json.loads(evaluate(excluded).stdout)
sku_check = next(c for c in payload["conditions"] if c["条件"] == "适用SKU")
if sku_check["状态"] != "不可用" or payload["calculation"]["应付草稿"] != "30.00": raise SystemExit("a zero threshold cannot make an excluded-only cart eligible")
# Percentage rounding happens once for the eligible total, then the same
# rounded amount is allocated to lines.  Two 0.05 lines at 10% off are 0.01,
# never a displayed 0.01 paired with a 0.02 reduction.
rounding = json.loads(json.dumps(multi))
rounding["cart"] = [{"sku":"A","unit_price":"0.05","quantity":1},{"sku":"B","unit_price":"0.05","quantity":1}]
rounding["promotions"][0] = dict(rounding["promotions"][0], name="九折", type="percent", percent="90", rounding_mode="total_half_up_2")
rounding["stacking_order"] = ["九折"]
payload = json.loads(evaluate(rounding).stdout)
if payload["calculation"]["steps"][0]["优惠额"] != "0.01" or payload["calculation"]["应付草稿"] != "0.09": raise SystemExit("the explicitly selected half-up rounding rule must match the deduction")
no_rounding = json.loads(json.dumps(rounding)); no_rounding["promotions"][0].pop("rounding_mode")
pending_rounding = json.loads(evaluate(no_rounding).stdout)
if pending_rounding["calculation"]["steps"][0]["优惠额"] != "待确认": raise SystemExit("percent discounts without merchant-confirmed rounding must stay pending")
tiny_balance = json.loads(json.dumps(rounding))
tiny_balance["cart"] = [{"sku":"A","unit_price":"0.006","quantity":1}]
tiny_balance["promotions"][0] = dict(tiny_balance["promotions"][0], name="全额减免", percent="0")
tiny_balance["stacking_order"] = ["全额减免"]
tiny_balance_result = json.loads(evaluate(tiny_balance).stdout)
if tiny_balance_result["calculation"]["steps"][0]["优惠额"] != "待确认" or tiny_balance_result["calculation"]["应付草稿"] != "待确认":
    raise SystemExit("rounding above a sub-cent balance must become pending instead of raising or over-discounting")
tiny_lines = json.loads(json.dumps(rounding))
tiny_lines["cart"] = [{"sku":"A","unit_price":"0.01","quantity":1} for _ in range(5)]
tiny_lines["shipping_fee"] = "0"
tiny_lines["promotions"][0] = dict(tiny_lines["promotions"][0], name="六七折", percent="67")
tiny_lines["stacking_order"] = ["六七折"]
tiny_result = json.loads(evaluate(tiny_lines).stdout)
if tiny_result["calculation"]["steps"][0]["优惠额"] != "0.02" or tiny_result["calculation"]["应付草稿"] != "0.03":
    raise SystemExit("aggregate percentage rounding must be fully deducted across tiny cart lines")
precision_result = evaluate_raw('{"currency":"CNY","shipping_fee":"0","cart":[{"sku":"A","unit_price":0.100000000000000005,"quantity":1}],"promotions":[]}')
if precision_result.returncode or json.loads(precision_result.stdout)["calculation"]["商品额"] != "0.100000000000000005":
    raise SystemExit("JSON decimal precision must be preserved before Decimal calculations")
precision_long = evaluate_raw('{"currency":"CNY","shipping_fee":"0","cart":[{"sku":"A","unit_price":0.12345678901234567890123456789,"quantity":1}],"promotions":[]}')
if precision_long.returncode or json.loads(precision_long.stdout)["calculation"]["商品额"] != "0.12345678901234567890123456789":
    raise SystemExit("long decimal calculations must not use the default 28-digit Decimal context")
impossible_after = json.loads(json.dumps(allocation_chain))
impossible_after["shipping_fee"] = "0"
impossible_after["cart"] = [{"sku":"A","unit_price":"10","quantity":1},{"sku":"B","unit_price":"10","quantity":1}]
impossible_after["promotions"] = [
    {"name":"AB先减5","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"5"},
    {"name":"A门槛100","eligible_skus":["A"],"threshold":"100","threshold_basis":"优惠后商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"1"}
]
impossible_after["stacking_order"] = ["AB先减5","A门槛100"]
impossible_result = json.loads(evaluate(impossible_after).stdout)
if impossible_result["calculation"]["应付草稿"] != "15.00" or any(c["条件"] == "优惠分摊" and c["状态"] == "待确认" for c in impossible_result["conditions"]):
    raise SystemExit("an impossible post-discount threshold must not require upstream allocation")
if next(c for c in impossible_result["conditions"] if c["优惠"] == "A门槛100" and c["条件"] == "门槛")["状态"] != "不可用":
    raise SystemExit("an unreachable post-discount threshold must be marked unavailable")
nonoverlap = json.loads(json.dumps(allocation_chain))
nonoverlap["cart"] = [{"sku":"A","unit_price":"100","quantity":1},{"sku":"B","unit_price":"100","quantity":1},{"sku":"C","unit_price":"100","quantity":1}]
nonoverlap["promotions"] = [
    {"name":"AB减20","eligible_skus":["A","B"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"20"},
    {"name":"C减10","eligible_skus":["C"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"start":"2026-10-01T00:00:00+08:00","end":"2026-10-10T00:00:00+08:00","timezone":"Asia/Shanghai","type":"fixed","amount":"10"}
]
nonoverlap["stacking_order"] = ["AB减20","C减10"]
nonoverlap_result = json.loads(evaluate(nonoverlap).stdout)
if nonoverlap_result["calculation"]["应付草稿"] != "270.00" or any(c["条件"]=="优惠分摊" and c["状态"]=="待确认" for c in nonoverlap_result["conditions"]):
    raise SystemExit("a later promotion on disjoint SKUs must not require allocation")
over_balance = json.loads(json.dumps(multi))
over_balance["cart"] = [{"sku":"A","unit_price":"100","quantity":1}]
over_balance["shipping_fee"] = "0"
over_balance["promotions"] = [dict(over_balance["promotions"][0],name="超过余额",eligible_skus=["A"],type="fixed",amount="200")]
over_balance["stacking_order"] = ["超过余额"]
over_balance_result = json.loads(evaluate(over_balance).stdout)
if over_balance_result["calculation"]["应付草稿"] != "待确认" or next(c for c in over_balance_result["conditions"] if c["条件"]=="优惠值")["状态"] != "待确认":
    raise SystemExit("fixed discount above eligible balance must remain pending without an explicit rule")
pay_90 = json.loads(json.dumps(order_case)); pay_90["promotions"] = [dict(pay_90["promotions"][0], name="九折", type="percent", percent="90", rounding_mode="total_half_up_2")]; pay_90["stacking_order"] = ["九折"]
if json.loads(evaluate(pay_90).stdout)["calculation"]["应付草稿"] != "90.00": raise SystemExit("percent=90 must mean 90 percent payable (九折)")
step_basis = json.loads(evaluate(pay_90).stdout)["calculation"]["steps"][0]["计算依据"]
if (not step_basis["公式"] or not step_basis["舍入过程"] or not step_basis["行级扣减"]
        or step_basis["行级扣减"][0]["本步扣减"] != "10.00"):
    raise SystemExit("calculation steps must show formula, rounding, and actual line-level deduction")
# Invalid core monetary input must fail instead of producing a payable result.
for field, value, expected in [("shipping_fee", "-1", "运费"), ("unit_price", "-1", "商品单价")]:
    invalid = json.loads(json.dumps(success))
    if field == "unit_price": invalid["cart"][0][field] = value
    else: invalid[field] = value
    out = evaluate(invalid)
    if out.returncode == 0 or expected not in out.stderr: raise SystemExit(f"invalid {field} was accepted")
invalid = json.loads(json.dumps(success)); next(rule for rule in invalid["promotions"] if rule["type"] == "fixed")["amount"] = "-20"
if evaluate(invalid).returncode == 0: raise SystemExit("negative fixed discount was accepted")
invalid = json.loads(json.dumps(success)); next(rule for rule in invalid["promotions"] if rule["type"] == "percent")["percent"] = "101"
if evaluate(invalid).returncode == 0: raise SystemExit("out-of-range percent was accepted")
invalid = json.loads(json.dumps(success)); invalid["cart"][0]["quantity"] = "-1"
if evaluate(invalid).returncode == 0: raise SystemExit("negative quantity was accepted")
invalid_period = json.loads(json.dumps(pay_90))
invalid_period["current_time"] = "2026-10-05T12:00:00+08:00"
invalid_period["promotions"][0].update({"start":"2026-10-10T00:00:00+08:00","end":"2026-10-01T00:00:00+08:00"})
period_result = json.loads(evaluate(invalid_period).stdout)
period_condition = next(c for c in period_result["conditions"] if c["条件"]=="有效期")
if period_condition["状态"] != "待确认" or "开始时间晚于结束时间" not in period_condition["依据"] or period_result["calculation"]["应付草稿"] != "待确认":
    raise SystemExit("a reversed validity range must remain pending rather than become a definite payable result")
invalid = json.loads(json.dumps(success)); invalid["cart"][0].pop("sku")
if evaluate(invalid).returncode == 0 or "SKU" not in evaluate(invalid).stderr: raise SystemExit("missing cart SKU must not become a known inapplicable result")
inapplicable = {"currency":"CNY","shipping_fee":"5","cart":[{"sku":"X","unit_price":"30","quantity":1}],"promotions":[{"name":"仅A款可用","eligible_skus":["A"],"threshold":"0","threshold_basis":"商品额","threshold_includes_shipping":False,"type":"fixed","amount":"10"}]}
if json.loads(evaluate(inapplicable).stdout)["calculation"]["应付草稿"] != "35.00": raise SystemExit("unknown expiry of a known inapplicable promotion must not poison payable total")
multi["promotions"].append(dict(multi["promotions"][0]))
out = evaluate(multi)
if out.returncode == 0 or "优惠名称重复" not in out.stderr: raise SystemExit("duplicate promotion names must be rejected")
print("self-test passed: ordering, SKU scope, shipping ambiguity, uncertainty propagation, rounding, and input ranges verified")
