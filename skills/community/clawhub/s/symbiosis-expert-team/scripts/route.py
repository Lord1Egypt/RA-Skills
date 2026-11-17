# -*- coding: utf-8 -*-
"""symbiosis-expert-team 路由入口（零依赖，仅标准库）。

用法：
    python scripts/route.py            列出五位能力位专家的触发条件与调用方式
    python scripts/route.py --check    校验 agents/ 下五份人设文件在位且 frontmatter 可解析，并校验 SKILL.md frontmatter 字段
    python scripts/route.py --selftest 自检：SKILL.md frontmatter 九字段齐全 + 路由表完整则 exit 0

说明：本包上游（ModelScope origin/master）原本只有 SKILL.md，agents/ 原始五人明细未在上游
发现；本地已按 description 能力面推导落地五位能力位人设（非真人，每份标注推导来源，供校准）。
"""
import os
import sys

# 包内相对路径：scripts/ 的上一级即包根
PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_DIR = os.path.join(PKG_ROOT, "agents")
SKILL_FILE = os.path.join(PKG_ROOT, "SKILL.md")

# SKILL.md frontmatter 必备字段（AI 可读协议字段）
REQUIRED_FIELDS = ["name", "slug", "displayName", "category", "version",
                   "author", "agent_created", "description", "tags"]

EXPERTS = [
    {
        "id": "expert-social",
        "file": "expert-social.md",
        "role": "AI社交专家（能力位）",
        "capability": "AI社交",
        "triggers": [
            "AI 与人类、AI 与 AI 之间的沟通礼仪/协作话术",
            "多智能体打招呼、认领、转交、语气冲突",
            "需要「身份透明」的对外自称话术",
        ],
        "invoke": "读取 agents/expert-social.md 人设，按该能力位应答；越界诉求转 expert-human-copilot。",
    },
    {
        "id": "expert-hardware",
        "file": "expert-hardware.md",
        "role": "硬件接入专家（能力位）",
        "capability": "硬件接入",
        "triggers": [
            "传感器/执行器/设备如何接入 AI 系统",
            "接口、协议、驱动、数据格式的适配问题",
            "硬件无响应/数据异常的排查思路",
        ],
        "invoke": "读取 agents/expert-hardware.md 人设，按该能力位应答；涉电气安全提示人工兜底。",
    },
    {
        "id": "expert-visual",
        "file": "expert-visual.md",
        "role": "状态可视专家（能力位）",
        "capability": "状态可视",
        "triggers": [
            "把系统内部状态变成人类可看懂的看板/指标",
            "状态字段翻译成可读文案、异常提示",
            "当前哪位专家值守、处理到哪一步的呈现",
        ],
        "invoke": "读取 agents/expert-visual.md 人设，按该能力位产出可视化方案。",
    },
    {
        "id": "expert-knowledge",
        "file": "expert-knowledge.md",
        "role": "知识灌注专家（能力位）",
        "capability": "知识灌注",
        "triggers": [
            "把人类资料整理成结构化知识条目",
            "新旧知识冲突、过期知识的识别",
            "知识来源、适用范围、有效期的管理",
        ],
        "invoke": "读取 agents/expert-knowledge.md 人设，按该能力位处理知识灌注。",
    },
    {
        "id": "expert-human-copilot",
        "file": "expert-human-copilot.md",
        "role": "人类共事副驾（能力位）",
        "capability": "与人类长期共事",
        "triggers": [
            "模糊诉求需要拆到合适的能力位",
            "长期协作待办是否闭环的跟踪",
            "需要统一汇总五位专家产出并面向人类答复",
        ],
        "invoke": "读取 agents/expert-human-copilot.md 人设，统筹路由并提示人类拍板边界。",
    },
]

EXPECTED_FILES = [e["file"] for e in EXPERTS]


def list_experts():
    print("symbiosis-expert-team · 共生专家团路由（能力位人设，非真人）")
    print("=" * 60)
    for i, e in enumerate(EXPERTS, 1):
        print("[%d] %s —— %s" % (i, e["id"], e["role"]))
        print("    能力面：%s" % e["capability"])
        print("    人设文件：agents/%s" % e["file"])
        print("    触发条件：")
        for t in e["triggers"]:
            print("      - %s" % t)
        print("    调用方式：%s" % e["invoke"])
        print("-" * 60)
    print("通用边界（每位专家均守）：身份透明 / 边界守恒 / 单点叙事，详见各人设文件。")


def _parse_frontmatter(text):
    """极简 frontmatter 解析（仅支持 key: value 行），用于本包受控格式的可解析性校验。"""
    if not text.startswith("---"):
        raise ValueError("缺少起始 --- 分隔线")
    end = text.find("---", 3)
    if end == -1:
        raise ValueError("缺少结束 --- 分隔线")
    fm = text[3:end].strip("\n")
    pairs = []
    for line in fm.splitlines():
        line = line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError("frontmatter 行不是 key: value 形式：%r" % line)
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            raise ValueError("frontmatter 出现空 key")
        pairs.append((k, v))
    if not any(k == "name" for k, _ in pairs):
        raise ValueError("frontmatter 缺少 name 字段")
    return dict(pairs)


def check_skill_frontmatter():
    """校验 SKILL.md frontmatter 必备字段存在（逐行 key 检查，兼容列表值）。"""
    if not os.path.isfile(SKILL_FILE):
        return [], "SKILL.md 缺失"
    text = open(SKILL_FILE, "r", encoding="utf-8").read()
    if not text.startswith("---"):
        return [], "SKILL.md 缺少 frontmatter"
    keys = []
    for line in text.splitlines():
        if line.startswith("---"):
            continue
        m = line.split(":", 1)
        if len(m) == 2 and m[0].strip() and not m[0].startswith(" "):
            keys.append(m[0].strip())
        if line == "---" and keys:
            break
    missing = [f for f in REQUIRED_FIELDS if f not in keys]
    return missing, ""


def check():
    ok = True
    print("校验 agents/ 人设文件（共 %d 份）..." % len(EXPECTED_FILES))
    if not os.path.isdir(AGENTS_DIR):
        print("FAIL：目录不存在 %s（已知缺口：上游历史无 agents/，如实记录）" % AGENTS_DIR)
        ok = False
    else:
        seen = set()
        for fn in EXPECTED_FILES:
            path = os.path.join(AGENTS_DIR, fn)
            seen.add(fn)
            if not os.path.isfile(path):
                print("FAIL：缺文件 agents/%s" % fn)
                ok = False
                continue
            raw = open(path, "rb").read()
            for enc in ("utf-8-sig", "utf-8", "gbk"):
                try:
                    text = raw.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                print("FAIL：agents/%s 编码无法识别" % fn)
                ok = False
                continue
            try:
                fm = _parse_frontmatter(text)
                print("OK：agents/%s（name=%s）" % (fn, fm.get("name")))
            except ValueError as ex:
                print("FAIL：agents/%s frontmatter 不可解析：%s" % (fn, ex))
                ok = False
        extra = set(os.listdir(AGENTS_DIR)) - set(EXPECTED_FILES)
        if extra:
            print("提示：agents/ 下另有文件（不影响校验）：%s" % ", ".join(sorted(extra)))
    missing, err = check_skill_frontmatter()
    if err:
        print("FAIL：%s" % err)
        ok = False
    elif missing:
        print("FAIL：SKILL.md frontmatter 缺字段：%s" % ", ".join(missing))
        ok = False
    else:
        print("OK：SKILL.md frontmatter 九字段齐全。")
    if ok:
        print("CHECK PASS：五份能力位人设均在位且 frontmatter 可解析，SKILL.md 字段齐全。")
        return 0
    print("CHECK FAIL。")
    return 1


def selftest():
    """自检：包机制达标即 PASS；agents/ 缺口为已记录项，不判 FAIL。"""
    print("selftest：SKILL.md frontmatter + 路由表完整性")
    ok = True
    missing, err = check_skill_frontmatter()
    if err:
        print("FAIL：%s" % err)
        ok = False
    elif missing:
        print("FAIL：SKILL.md frontmatter 缺字段：%s" % ", ".join(missing))
        ok = False
    else:
        print("PASS：SKILL.md frontmatter 九字段齐全。")
    if len(EXPERTS) != 5 or len(EXPECTED_FILES) != 5:
        print("FAIL：能力位路由表数量异常（%d）" % len(EXPERTS))
        ok = False
    else:
        print("PASS：五位能力位路由表完整（%s）。" % ", ".join(e["id"] for e in EXPERTS))
    if not os.path.isdir(AGENTS_DIR):
        print("WARN：agents/ 目录缺失（已知缺口，已按上游 git 历史如实记录，不影响本自检判定）。")
    else:
        print("WARN：agents/ 在位（人设文件如缺，用 --check 查看）。")
    print("SUMMARY | %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        sys.exit(check())
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    list_experts()
    sys.exit(0)


if __name__ == "__main__":
    main()
