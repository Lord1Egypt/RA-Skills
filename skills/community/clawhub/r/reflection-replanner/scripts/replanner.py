#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reflection-replanner —— 反思驱动重规划。

当验证引擎(reason-verify)判定执行失败（而非一次性执行）时，本技能触发「反思」：
对失败根因分类，并自动修订计划（补缺/加假设校验门/加工具容错/加数据准备/加最终验证门），
形成「规划→执行→验证→反思→重规划」的反思驱动闭环。

用法：
  python replanner.py --selftest
  python replanner.py --plan "a|b|c" --issues "部署后缺少健康检查步骤"
"""
import os, sys, json


class FailureClassifier:
    """把验证失败的根因分类为可操作的类别。"""

    KEYWORDS = {
        "missing_step": ["缺", "少", "未包含", "遗漏", "依赖", "missing", "lack", "incomplete"],
        "wrong_assumption": ["假设", "assum", "错误", "不符", "wrong", "incorrect"],
        "tool_failure": ["工具", "tool", "调用失败", "超时", "timeout", "error", "失败"],
        "data_issue": ["数据", "data", "空", "格式", "format", "缺失字段"],
    }

    @classmethod
    def classify(cls, issues):
        text = " ".join(issues).lower()
        for cat, kws in cls.KEYWORDS.items():
            if any(k in text for k in kws):
                return cat
        return "verification_gap"


class Replanner:
    def __init__(self, plan, trace=None, verify=None):
        self.plan = list(plan)
        self.trace = trace or []
        self.verify = verify or {"passed": False, "issues": []}

    def reflect(self):
        failing = [t for t in self.trace if not t.get("ok")]
        category = FailureClassifier.classify(self.verify.get("issues", []))
        return {
            "category": category,
            "failing_steps": [t["step"] for t in failing],
            "passed": self.verify.get("passed", False),
        }

    def replan(self):
        r = self.reflect()
        # 通过即停：不噪声式改动计划
        if r["passed"]:
            return {"category": "none", "revised_plan": list(self.plan), "added": []}
        cat = r["category"]
        new_steps = list(self.plan)
        insert_at = len(new_steps)
        if r["failing_steps"]:
            try:
                insert_at = new_steps.index(r["failing_steps"][0])
            except ValueError:
                insert_at = len(new_steps)
        additions = []
        if cat == "missing_step":
            additions.append("补充缺失步骤：补齐被遗漏的依赖/前置动作")
        elif cat == "wrong_assumption":
            additions.append("增加前置假设校验门：执行前先验证关键假设是否成立")
        elif cat == "tool_failure":
            additions.append("增加工具容错：为失败的工具调用补充重试/备选工具路径")
        elif cat == "data_issue":
            additions.append("增加数据准备与格式校验步骤，确保输入满足下游要求")
        else:
            additions.append("增加针对性验证探针，定位未通过的根因")
        # 反思闭环：针对性补救插在失败点之前
        for add in reversed(additions):
            new_steps.insert(insert_at, add)
        # 反思闭环：无论何种失败，末尾都补一道最终验证门（始终在计划最末）
        new_steps.append("末尾追加最终验证门：对修订后结果再做一次端到端校验")
        return {"category": cat, "revised_plan": new_steps, "added": additions + ["末尾追加最终验证门：对修订后结果再做一次端到端校验"]}


def _selftest():
    # 场景1：缺失步骤
    plan = ["读取需求", "生成方案", "部署", "验证"]
    trace = [
        {"step": "读取需求", "ok": True},
        {"step": "生成方案", "ok": True},
        {"step": "部署", "ok": False},
        {"step": "验证", "ok": False},
    ]
    verify = {"passed": False, "issues": ["部署后缺少健康检查步骤，服务未真正可达"]}
    rp = Replanner(plan, trace, verify)
    out = rp.replan()
    assert out["category"] == "missing_step", "分类错误: %s" % out["category"]
    assert any("补充缺失步骤" in s for s in out["revised_plan"]), "未插入缺失步骤"
    assert "末尾追加最终验证门" in out["revised_plan"][-1], "未追加最终验证门"
    idx_add = next(i for i, s in enumerate(out["revised_plan"]) if "补充缺失步骤" in s)
    idx_dep = out["revised_plan"].index("部署")
    assert idx_dep > idx_add, "缺失步骤应插在部署之前"

    # 场景2：错误假设
    verify2 = {"passed": False, "issues": ["关键假设错误：认为端口已开放，实际被防火墙拦截"]}
    rp2 = Replanner(plan, trace, verify2)
    out2 = rp2.replan()
    assert out2["category"] == "wrong_assumption", "分类错误: %s" % out2["category"]
    assert any("前置假设校验门" in s for s in out2["revised_plan"]), "未加假设校验门"

    # 场景3：无失败不应触发重规划（直接返回原计划+无新增）
    rp3 = Replanner(plan, [{"step": s, "ok": True} for s in plan], {"passed": True, "issues": []})
    out3 = rp3.replan()
    assert out3["revised_plan"] == plan, "通过时不应改动计划"
    assert out3["added"] == [], "通过时不应新增步骤"

    print("✅ reflection-replanner selftest 全过 (缺失/假设/通过 三场景)")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        _selftest()
        return
    plan = []
    issues = []
    i = 1
    while i < len(args):
        a = args[i]
        if a == "--plan":
            plan = [s for s in args[i + 1].split("|") if s]
            i += 2
        elif a == "--issues":
            issues = [s for s in args[i + 1].split("|") if s]
            i += 2
        else:
            i += 1
    rp = Replanner(plan, [], {"passed": False, "issues": issues})
    out = rp.replan()
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
