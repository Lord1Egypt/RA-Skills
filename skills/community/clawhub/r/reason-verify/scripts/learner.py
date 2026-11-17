#!/usr/bin/env python3
# learner: 让 meta-evolver 把本技能纳入受管集持续演化
import json, os
SLUG = "reason-verify"
def learn(patterns):
    caps = patterns.setdefault("global_capabilities", {})
    caps[SLUG] = {"type": "synthesized", "self_evolving": True, "from": "lifelong-skill-synthesis"}
    return patterns
if __name__ == "__main__":
    print(json.dumps({"slug": SLUG, "status": "learner-ready"}, ensure_ascii=False))
