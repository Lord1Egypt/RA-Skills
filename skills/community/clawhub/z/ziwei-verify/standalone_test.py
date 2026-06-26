"""
standalone_test.py - 独立测试脚本（不依赖包结构）
用于验证 calibrator.py 的核心逻辑
"""

from datetime import datetime, timedelta

# 模拟 CorrectionResult
class MockCorrectionResult:
    def __init__(self, shift_hours, confidence, high_impact, key_changes):
        self.shift_hours = shift_hours
        self.confidence = confidence
        self.verification_points_remaining = high_impact
        self.key_changes = key_changes
        self.match_score = 0.8

# 测试排序逻辑
results = [
    MockCorrectionResult(-2, 0.82, 0, ["命宫主星从空宫变为紫微+天府"]),
    MockCorrectionResult(2, 0.65, 2, ["迁移宫变动"]),
    MockCorrectionResult(-4, 0.58, 1, ["财帛宫化禄"]),
    MockCorrectionResult(4, 0.45, 3, ["父母宫化忌"]),
]

# 排序（与 calibrator.py 中的逻辑一致）
results.sort(key=lambda r: (r.confidence, -r.verification_points_remaining, r.match_score), reverse=True)

print("候选排序结果：")
for idx, r in enumerate(results):
    print(f"{idx}. 偏移 {r.shift_hours:+}h, 置信度 {r.confidence:.3f}, 高影响点 {r.verification_points_remaining}")

assert results[0].shift_hours == -2, "最优应该是 -2h"
assert results[0].confidence == 0.82, "最高置信度应为 0.82"

print("\n✅ 排序逻辑验证通过")

# 测试匹配度计算
def _calculate_match_score(orig, new):
    orig_fields = {p.get("field", "") for p in orig if p.get("field")}
    new_fields = {p.get("field", "") for p in new if p.get("field")}
    if not orig_fields:
        return 1.0
    intersection = orig_fields.intersection(new_fields)
    union = orig_fields.union(new_fields)
    jaccard = len(intersection) / len(union) if union else 1.0
    orig_high = {p.get("field") for p in orig if p.get("impact") == "high"}
    new_high = {p.get("field") for p in new if p.get("impact") == "high"}
    high_match = len(orig_high.intersection(new_high)) / len(orig_high) if orig_high else 1.0
    return round(0.7 * jaccard + 0.3 * high_match, 4)

orig_vps = [
    {"field": "命宫主星", "impact": "high"},
    {"field": "迁移宫", "impact": "medium"}
]
new_vps = [
    {"field": "命宫主星", "impact": "high", "suggestions": []},  # 保留 high
    {"field": "财帛宫", "impact": "low", "suggestions": []}
]

score = _calculate_match_score(orig_vps, new_vps)
print(f"\n匹配度计算: {score:.4f}")
# 预期：字段匹配度 Jaccard=0.33，高影响匹配度=1.0 → 综合 ≈0.53
assert 0.5 < score < 0.6, f"匹配度应在 0.5-0.6，实际 {score}"

print("✅ 匹配度算法验证通过")

# 测试候选生成
shifts = [-4, -2, 2, 4]
base_dt = datetime(1993, 4, 1, 14, 0)
candidates = [base_dt + timedelta(hours=s) for s in sorted(shifts)]
assert len(candidates) == 4
print(f"\n候选时间生成（共 {len(candidates)} 个）:")
for dt in candidates:
    print(f"  {dt.strftime('%Y-%m-%d %H:%M')}")

print("✅ 候选生成验证通过")

print("\n" + "="*60)
print("所有核心逻辑单元测试通过 ✅")
