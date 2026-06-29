"""钟馗评分计算器"""


class Scorer:
    """综合评分与裁定 — 依据 references/scoring.md 公式"""

    def compute(self, audit_result, l2_score=None, l3_penalty=None):
        """
        计算总分并返回 (score, verdict, flags)

        参数:
            audit_result: Auditor 实例（已执行 run_full()）
            l2_score: Layer 2 行为模拟得分 (0-100)。未运行时传 None，权重自动重分配。
            l3_penalty: Layer 3 供应链溯源罚分 (0-30，上限 30)。未运行时默认 0。

        返回:
            (score: float, verdict: str, flags: dict)
            verdict: "clean" / "suspicious_low" / "suspicious_high" / "malicious"
        """
        # 一票否决判定
        veto_hits = audit_result.get_veto_hits()
        if veto_hits:
            return (0, "malicious", {"veto": True, "veto_count": len(veto_hits)})

        # 即时拒绝红线判定
        redline_hits = audit_result.get_redline_hits()
        if redline_hits:
            return (0, "malicious", {"redline": True, "redline_count": len(redline_hits)})

        hits = audit_result.get_deductions()

        # Layer 1 分数：满分 100，每项扣分累加（剔除数据安全维度 D1-D7）
        total_penalty = sum(h.get('points', 0) for h in hits if not h['check'].startswith('D'))
        l1_score = max(0, 100 - total_penalty)

        # 数据安全得分（D1-D7 共 7 项，每项满分约 14.3）
        d_count = sum(1 for h in hits if h['check'].startswith('D'))
        data_score = max(0, 100 - d_count * 14.3)

        # L3 罚分：未传入时默认 0，上限 30
        l3_penalty = min(l3_penalty or 0, 30)

        # 动态权重分配：根据实际运行的层数调整
        if l2_score is not None:
            # L1 + L2 + 数据安全 - L3 罚分
            total = round(l1_score * 0.35 + l2_score * 0.55 + data_score * 0.10 - l3_penalty, 1)
        else:
            # 仅 L1 + 数据安全 - L3 罚分（离线默认路径）
            total = round(l1_score * 0.85 + data_score * 0.15 - l3_penalty, 1)

        # 裁定四级制
        if total >= 85:
            return (total, "clean", {})
        elif total >= 70:
            return (total, "suspicious_low", {})
        elif total >= 60:
            return (total, "suspicious_high", {})
        else:
            return (total, "malicious", {})
