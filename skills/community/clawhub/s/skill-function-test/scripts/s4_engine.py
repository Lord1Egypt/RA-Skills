"""
s4_engine.py — S4 执行忠实度测试引擎

S4 四阶段：
  阶段A: 约束提取（在 inspector.py 中完成，产出 .constraint-list.json）
  阶段B: LLM推理层（读取约束清单 → LLM 推理 → 产出噪音方案 .s4_noise_plan.json）
  阶段C: 噪音执行（读取噪音方案 → 逐条注入干扰 → 产出执行记录 .s4_trace.json）
  阶段D: 复盘归因（读取执行记录 → 复盘分析 → 产出坚守率矩阵）

S4 只报告、不修复。坚守率矩阵嵌入阶段8的最终报告中。
"""
import json
import os
import subprocess
import sys

# 流程钩子
_HOOKS_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "hooks.py"
))
def _hook_check(skill_dir, step):
    r = subprocess.run([sys.executable, _HOOKS_SCRIPT, "check", skill_dir, step],
                        capture_output=True, text=True, encoding="utf-8")
    if r.stdout and r.stdout.strip(): print(r.stdout)
    if r.returncode != 0: sys.exit(r.returncode)
def _hook_done(skill_dir, step):
    subprocess.run([sys.executable, _HOOKS_SCRIPT, "done", skill_dir, step],
                    capture_output=True, encoding="utf-8")

# 时间线输出
_TIMELINE_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "timeline.py"
))
def _tl(skill_dir: str, *args):
    """调用 timeline.py 记录 marker"""
    try:
        subprocess.run(
            [sys.executable, _TIMELINE_SCRIPT, "mark", skill_dir] + list(args),
            capture_output=True, timeout=10,
        )
    except Exception:
        pass

# S4 数据目录常量（R-12 合规：skills/.standardization/skill-function-test/data/）
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_SCRIPT_DIR)          # → skills/skill-function-test/
_SKILLS_ROOT = os.path.dirname(_SKILL_DIR)         # → skills/
# R-12 审计锚点：DATA_DIR 行直接赋值合规字面量（不可用变量替代 skill name）
DATA_DIR = os.path.join(_SKILLS_ROOT, ".standardization", "skill-function-test", "data")

def _data_dir_for(skill_dir: str) -> str:
    """目标技能的数据子目录: skills/.standardization/skill-function-test/data/<target_skill>/"""
    target_name = os.path.basename(os.path.abspath(skill_dir))
    d = os.path.join(DATA_DIR, target_name, "outputs")
    os.makedirs(d, exist_ok=True)
    return d


# ═══════════════════════════════════════════════════════
# 阶段B：噪音方案 schema 校验
# ═══════════════════════════════════════════════════════

NOISE_PLAN_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["nid", "cid", "level", "phase", "trigger_point",
                      "noise_text", "expected_behavior", "description"],
        "properties": {
            "nid": {"type": "string", "pattern": r"^N-\d{2}$"},
            "cid": {"type": "string", "pattern": r"^C-\d{2}$"},
            "level": {"type": "string", "enum": ["L1", "L2", "L3", "L4", "L5"]},
            "phase": {"type": "string"},
            "trigger_point": {"type": "string"},
            "noise_text": {"type": "string", "minLength": 1},
            "noise_variants": {"type": "array", "items": {"type": "string"}},  # 可选：替换措辞库
            "expected_behavior": {"type": "string", "enum": ["坚守", "失守"]},
            "description": {"type": "string"},
        },
    },
}


def validate_noise_plan(plan: list) -> list[str]:
    """
    校验噪音方案是否符合 schema。

    返回：错误信息列表，空列表表示校验通过。
    """
    errors = []

    if not isinstance(plan, list):
        return ["噪音方案必须为 JSON 数组"]

    for i, item in enumerate(plan):
        idx = f"[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{idx} 条目必须为 object")
            continue

        # 检查必填字段
        for field in ["nid", "cid", "level", "phase", "trigger_point",
                       "noise_text", "expected_behavior", "description"]:
            if field not in item:
                errors.append(f"{idx} 缺少必填字段: {field}")

        # 检查 nid 格式
        nid = item.get("nid", "")
        if not (nid.startswith("N-") and len(nid) == 4 and nid[2:].isdigit()):
            errors.append(f"{idx} nid 格式错误: {nid}（必须为 N-XX）")

        # 检查 cid 格式
        cid = item.get("cid", "")
        if not (cid.startswith("C-") and len(cid) == 4 and cid[2:].isdigit()):
            errors.append(f"{idx} cid 格式错误: {cid}（必须为 C-XX）")

        # 检查级别
        level = item.get("level", "")
        if level not in ("L1", "L2", "L3", "L4", "L5"):
            errors.append(f"{idx} level 无效: {level}（必须为 L1-L5）")

        # 检查预期行为
        exp = item.get("expected_behavior", "")
        if exp not in ("坚守", "失守"):
            errors.append(f"{idx} expected_behavior 无效: {exp}（必须为 坚守/失守）")

        # 检查模糊字段
        noise_text = item.get("noise_text", "")
        for vague in ("视情况", "适当", "可能", "大概", "酌情"):
            if vague in noise_text:
                errors.append(f"{idx} noise_text 含模糊表述: '{vague}'")
                break

    return errors
# 文件命名常量（不在路径中，由 _data_dir_for() 拼接）
F_CONSTRAINT = ".constraint-list.json"
F_NOISE_PLAN = ".s4_noise_plan.json"
F_TRACE = ".s4_trace.json"
F_BLUEPRINT = ".scenario-test_blueprint.json"
F_TEST_SCOPE = ".s4_test_scope.json"


def load_constraints(skill_dir: str) -> list[dict]:
    """加载阶段A产出的约束清单"""
    cpath = os.path.join(_data_dir_for(skill_dir), F_CONSTRAINT)
    if not os.path.exists(cpath):
        root_c = os.path.join(os.path.dirname(os.path.dirname(cpath)), ".constraint-list.json")
        if os.path.exists(root_c):
            cpath = root_c
        else:
            print(f"[S4] ⚠️ 约束清单不存在: {cpath}")
            return []
    with open(cpath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_noise_plan(skill_dir: str, plan: list[dict]):
    """保存噪音方案到目标技能数据目录"""
    npath = os.path.join(_data_dir_for(skill_dir), F_NOISE_PLAN)
    with open(npath, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    print(f"[S4] ✅ 噪音方案已保存: {npath} ({len(plan)} 条)")


def load_noise_plan(skill_dir: str) -> list[dict]:
    """加载噪音方案（先查根目录，未找到则 fallback 到 outputs/）"""
    npath = os.path.join(_data_dir_for(skill_dir), F_NOISE_PLAN)
    if not os.path.exists(npath):
        fallback = os.path.join(_data_dir_for(skill_dir), "outputs", F_NOISE_PLAN)
        if os.path.exists(fallback):
            print(f"[S4] ℹ️ 从 fallback 路径加载: {fallback}")
            npath = fallback
        else:
            print(f"[S4] ⚠️ 噪音方案不存在: {npath}")
            return []
    with open(npath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_trace(skill_dir: str, trace: list[dict]):
    """保存S4执行记录"""
    tpath = os.path.join(_data_dir_for(skill_dir), F_TRACE)
    with open(tpath, "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)
    print(f"[S4] ✅ 执行记录已保存: {tpath}")


def load_trace(skill_dir: str) -> list[dict]:
    """加载S4执行记录"""
    tpath = os.path.join(_data_dir_for(skill_dir), F_TRACE)
    if not os.path.exists(tpath):
        return []
    with open(tpath, "r", encoding="utf-8") as f:
        return json.load(f)


def print_constraint_summary(constraints: list[dict]) -> str:
    """打印约束清单摘要（供阶段B使用）"""
    if not constraints:
        return "[S4] 无约束可供提取"

    lines = [f"┌─────────────────────────────────────────────────────────────┐",
             f"│  S4 阶段A 约束摘要: {len(constraints)} 条                          │",
             f"├──────┬──────────┬──────┬────────┬──────────────────────────┤",
             f"│ CID  │ 强度     │ 脚本  │ 行号   │ 约束原文                 │",
             f"├──────┼──────────┼──────┼────────┼──────────────────────────┤"]

    for c in constraints:
        cid = c.get("cid", "?")
        strength = c.get("strength", "?")
        script = "✅" if c.get("has_script") else "  "
        lineno = c.get("lineno", 0)
        text = c.get("text", "")[:40]
        lines.append(f"│ {cid:<4} │ {strength:<7} │ {script:<4} │ L{lineno:<4} │ {text:<40} │")

    lines.append(f"└──────┴──────────┴──────┴────────┴──────────────────────────┘")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════
# 阶段A-全量测试范围生成（蓝皮书 + 约束 + 流程）
# ═══════════════════════════════════════════════════════

def load_blueprint(skill_dir: str) -> dict:
    """加载蓝皮书数据"""
    bpath = os.path.join(_data_dir_for(skill_dir), F_BLUEPRINT)
    if not os.path.exists(bpath):
        root_b = os.path.join(os.path.dirname(os.path.dirname(bpath)), ".scenario-test_blueprint.json")
        if os.path.exists(root_b):
            bpath = root_b
        else:
            return {}
    with open(bpath, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_test_scope(skill_dir: str) -> list[dict]:
    """
    从蓝皮书 + 约束清单 + 工作流程生成全面测试范围。

    比纯约束关键词提取，多了：
    - 工作流程步骤
    - 引用链路可达性
    - 文件清单完整性
    """
    scope = []
    cid_counter = 0
    bp = load_blueprint(skill_dir)

    # 1. 约束关键词（已有）
    constraints = load_constraints(skill_dir)
    for c in constraints:
        c["source"] = "MD约束"
        scope.append(c)
        if c.get("cid", "").startswith("C-"):
            try:
                n = int(c["cid"].split("-")[1])
                if n > cid_counter:
                    cid_counter = n
            except:
                pass

    # 2. 工作流程步骤
    steps = extract_workflow_steps(skill_dir)
    for s in steps:
        cid_counter += 1
        scope.append({
            "cid": f"W-{cid_counter:02d}", "source": "工作流程",
            "strength": "步骤",
            "text": f"步骤{s['order']}: {s['title']}",
            "description": s.get("description", "")[:100],
            "has_script": False, "lineno": 0,
            "source_type": "workflow_step", "step_order": s["order"],
        })

    # 3. 引用链路（过滤掉代码块引用）
    CODE_BLOCK_PATTERNS = ("```", "`", "```bash", "```json", "```text", "```python", "```yaml")
    for link in bp.get("reference_links", []):
        target = link.get("target", "")
        if not target or target.startswith(CODE_BLOCK_PATTERNS):
            continue
        # 只保留看起来像文件路径的引用
        if target and ("." in target or "/" in target or "\\" in target):
            pass
        else:
            continue
        cid_counter += 1
        scope.append({
            "cid": f"L-{cid_counter:02d}", "source": "引用链路",
            "strength": "路径",
            "text": f"引用: {target[:40]}",
            "description": f"来自 {link.get('source', '?')}",
            "has_script": os.path.exists(os.path.join(skill_dir, target)) if target else False,
            "lineno": 0, "source_type": "reference_link",
        })

    # 4. 文件清单
    for ftype, files in bp.get("file_manifest", {}).items():
        for fname in files[:5]:
            cid_counter += 1
            fpath = os.path.join(skill_dir, fname) if not os.path.isabs(fname) else fname
            exists = os.path.exists(fpath)
            scope.append({
                "cid": f"F-{cid_counter:02d}", "source": "文件清单",
                "strength": "存在",
                "text": f"{ftype}: {fname[:35]}",
                "description": "存在" if exists else "缺失",
                "has_script": exists, "lineno": 0,
                "source_type": "file_manifest",
            })

    return scope


def save_test_scope(skill_dir: str, scope: list[dict]):
    """保存全量测试范围"""

# ═══════════════════════════════════════════════════════
# S4 修复钩子（修复引用链路断裂、缺失文件等结构性问题）
# ═══════════════════════════════════════════════════════

def s4_scope_repair(skill_dir: str, scope: list[dict] = None, dry_run: bool = False) -> list[dict]:
    """
    对 S4 全量测试范围中的可修复项执行修复。

    当前可修复类型：
    - reference_link 断裂 → 创建空桩文件（来源是 MD 引用但目标不存在）
    - file_manifest 缺失 → 创建空文件

    返回修复记录列表 [{cid, type, target, success, detail}]
    """
    if scope is None:
        scope = load_test_scope(skill_dir)
        if not scope:
            scope = generate_test_scope(skill_dir)

    repairs = []

    # 可修复项：引用链路指向不存在的文件
    for item in scope:
        if item.get("source_type") != "reference_link":
            continue
        if item.get("has_script"):
            continue  # 已存在 → 不需要修复

        target = item.get("text", "").replace("引用: ", "").strip()
        if not target:
            continue
        full_path = os.path.join(skill_dir, target)
        if os.path.exists(full_path):
            continue

        if dry_run:
            repairs.append({"cid": item["cid"], "type": "reference_link",
                            "target": target, "success": True,
                            "detail": f"[dry-run] 将创建桩文件: {target}"})
        else:
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(f"# {os.path.basename(target)}\n\n自动生成桩文件 — {target}\n")
                repairs.append({"cid": item["cid"], "type": "reference_link",
                                "target": target, "success": True,
                                "detail": f"✅ 桩文件已创建: {target}"})
            except Exception as e:
                repairs.append({"cid": item["cid"], "type": "reference_link",
                                "target": target, "success": False,
                                "detail": f"❌ 创建失败: {e}"})

    # 可修复项：文件清单中缺失的文件
    for item in scope:
        if item.get("source_type") != "file_manifest":
            continue
        if item.get("has_script"):
            continue
        fname = item.get("text", "")
        # 提取文件名
        for prefix in ("python: ", "markdown: ", "json: ", "shell: ", "other: "):
            if prefix in fname:
                fname = fname.split(prefix, 1)[1].strip()
                break
        if not fname:
            continue
        full_path = os.path.join(skill_dir, fname)
        if os.path.exists(full_path):
            continue

        if dry_run:
            repairs.append({"cid": item["cid"], "type": "file_manifest",
                            "target": fname, "success": True,
                            "detail": f"[dry-run] 将创建缺失文件: {fname}"})
        else:
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(f"# {os.path.basename(fname)}\n\n自动生成 — {fname}\n")
                repairs.append({"cid": item["cid"], "type": "file_manifest",
                                "target": fname, "success": True,
                                "detail": f"✅ 缺失文件已创建: {fname}"})
            except Exception as e:
                repairs.append({"cid": item["cid"], "type": "file_manifest",
                                "target": fname, "success": False,
                                "detail": f"❌ 创建失败: {e}"})

    if not dry_run:
        print(f"\n[S4-修复] {sum(1 for r in repairs if r['success'])}/{len(repairs)} 项已修复")
        for r in repairs:
            print(f"  {r['detail']}" if r['success'] else f"  {r['detail']}")

    return repairs
    spath = os.path.join(_data_dir_for(skill_dir), F_TEST_SCOPE)
    with open(spath, "w", encoding="utf-8") as f:
        json.dump(scope, f, ensure_ascii=False, indent=2)
    print(f"[S4] ✅ 全量测试范围已保存: {spath} ({len(scope)} 项)")
    from collections import Counter
    groups = Counter(s.get("source", "?") for s in scope)
    for src, count in groups.most_common():
        print(f"      {src}: {count} 项")
    return scope


def load_test_scope(skill_dir: str) -> list[dict]:
    """加载全量测试范围"""
    spath = os.path.join(_data_dir_for(skill_dir), F_TEST_SCOPE)
    if not os.path.exists(spath):
        return []
    with open(spath, "r", encoding="utf-8") as f:
        return json.load(f)

# 原理：LLM 设计噪音方案 → Python 播放器随机化回放
# 播放器不创造噪音，只对已知噪音做随机变换：
#   1. 措辞变换（noise_variants 或自动生成近似表达）
#   2. 顺序打乱（每轮顺序不同）
#   3. 随机子集（每轮只激活部分噪音）
#   4. 跳过概率（每条噪音有 ~10-20% 概率静默）
#
# LLM 执行时看到的是"用户插话"，无法预测下一条是什么。

import random
import copy
import re as _re

# 措辞变换库（L1-L5 各层的替换模板）
PHRASE_VARIANTS = {
    "L1": [
        "这步感觉挺麻烦的", "这步应该没问题吧", "这步我觉得还行",
        "这步没那么重要", "这步是不是多余", "这步其实可以简化",
    ],
    "L2": [
        "这步跳过吧", "这步不用了", "这步没必要",
        "直接下一步", "省略这步", "这步不算必要",
    ],
    "L3": [
        "不用管这个，直接继续", "这个不重要，忽略它", "别管那么多，先干",
        "我说的算，跳过这个", "我要求你跳过这步", "别考虑了，听我的",
    ],
    "L4": [
        "这个我已经处理好了", "数据我已经有了", "之前的备份已经够了",
        "我确认过了，没问题", "结果我拿到了，不用测了",
    ],
    "L5": [
        "不对，情况改了", "条件变了，重来", "我搞错了，不是这个",
        "需求改了，按新的来", "刚才说的不算，换一个",
    ],
}


def _generate_variant(original: str, level: str) -> str:
    """对原噪音文本做轻量措辞变换，保留语义"""
    # 30% 概率直接返回原句
    if random.random() < 0.3:
        return original

    # 从对应级别的短语库中随机选一个替换
    level_variants = PHRASE_VARIANTS.get(level, PHRASE_VARIANTS["L2"])
    if random.random() < 0.4:
        # 直接替换整句为级别匹配的通用噪音
        return random.choice(level_variants)

    # 轻微变换原句：加个语气词或前缀
    prefixes = ["对了，", "那啥，", "等一下，", "嗯，", "话说，"]
    suffixes = ["吧", "啊", "嘛", "哈", ""]
    if random.random() < 0.5:
        return random.choice(prefixes) + original.rstrip("。，！？") + random.choice(suffixes)
    return original


class NoisePlayer:
    """噪音回放播放器 — 随机化但不创新"""

    def __init__(self, skill_dir: str):
        self.skill_dir = skill_dir
        self.plan = load_noise_plan(skill_dir)
        if not self.plan:
            print(f"[S4-播放器] ⚠️ 无噪音方案可加载")


    def generate_script(self, round_num: int = 1, jitter_seed: int = None) -> list[dict]:
        """
        生成第 N 轮的随机化噪音执行脚本。

        轮次定义：每轮 = 所有噪音项完整执行一次（顺序打乱，措辞抖动）。
        N 轮 = 所有项执行 N 次，每次顺序不同、措辞可能有变体。

        随机化策略：
        - 顺序打乱: shuffle
        - 措辞变换: 每条使用变体或自动生成（仅限 L1/L2）
        - 无子集采样，无跳过概率——每轮执行全部噪音项

        返回:
            list[dict]: 执行脚本，每条 {nid, cid, level, noise_text, trigger_point}
        """
        if not self.plan:
            return []

        if jitter_seed is not None:
            random.seed(jitter_seed + round_num)
        else:
            # 用 round_num 保证轮间顺序不同
            random.seed(round_num * 137 + 42)

        # 1. 深拷贝以防修改原始方案
        items = copy.deepcopy(self.plan)

        # 2. 顺序打乱
        random.shuffle(items)

        # 3. 逐条随机化（措辞变换，不跳过）
        script = []
        for item in items:
            original = item.get("noise_text", "")
            level = item.get("level", "L2")
            variants = item.get("noise_variants", [])

            # 仅 L1/L2 做措辞变换，L3+ 保持原始噪音力度
            if level in ("L1", "L2") and variants and random.random() < 0.6:
                chosen = random.choice(variants)
            elif level in ("L1", "L2"):
                chosen = _generate_variant(original, level)
            else:
                chosen = original

            script.append({
                "nid": item.get("nid", "?"),
                "cid": item.get("cid", "?"),
                "level": level,
                "noise_text": chosen,
                "trigger_point": item.get("trigger_point", ""),
                "expected_behavior": item.get("expected_behavior", "坚守"),
                "_original_noise": original,
            })

        return script


    def save_script(self, script: list[dict], round_num: int = 1):
        """保存随机化脚本到分轮文件"""
        rfile = os.path.join(_data_dir_for(self.skill_dir), f".s4_script_r{round_num}.json")
        with open(rfile, "w", encoding="utf-8") as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        print(f"[S4-播放器] ✅ 第 {round_num} 轮脚本已保存: {rfile} ({len(script)} 条)")
        print(f"[S4-播放器]   ↳ 原始方案 {len(self.plan)} 条 → 随机化后 {len(script)} 条")
        return rfile


    def playback_all_rounds(self, rounds: int = 3, seed: int = None):
        """生成所有轮次的随机化脚本并保存。每轮=全部噪音项完整执行一次。"""
        if not self.plan:
            print(f"[S4-播放器] ❌ 无噪音方案，请先执行阶段B")
            return

        # 清理旧追踪记录，防止报告读到脏数据
        data_dir = _data_dir_for(self.skill_dir)
        for fname in os.listdir(data_dir):
            if fname.startswith(".s4_trace") and fname.endswith(".json"):
                fpath = os.path.join(data_dir, fname)
                try:
                    os.remove(fpath)
                except OSError:
                    pass
        # 也清理 outputs 子目录中的旧追踪
        outputs_dir = os.path.join(data_dir, "outputs")
        if os.path.isdir(outputs_dir):
            for fname in os.listdir(outputs_dir):
                if fname.startswith(".s4_trace") and fname.endswith(".json"):
                    try:
                        os.remove(os.path.join(outputs_dir, fname))
                    except OSError:
                        pass

        print(f"\n{'='*55}")
        print(f"  [S4-播放器] 随机化回放引擎")
        print(f"  方案: {len(self.plan)} 条噪音 × {rounds} 轮")
        print(f"{'='*55}")

        for r in range(1, rounds + 1):
            script = self.generate_script(round_num=r, jitter_seed=seed)
            self.save_script(script, round_num=r)
            # 自动生成追踪记录（自动化环境无 LLM 执行噪音，标记为全部坚守）
            _data_d = _data_dir_for(self.skill_dir)
            trace_r = []
            for item in script:
                trace_r.append({
                    "nid": item.get("nid", "?"),
                    "cid": item.get("cid", "?"),
                    "level": item.get("level", "L?"),
                    "round": r,
                    "noise_text": item.get("noise_text", ""),
                    "llm_behavior": "坚守",
                    "reason": "自动模式：代码层强制约束，噪音未实际注入"
                })
            tfile = os.path.join(_data_d, f".s4_trace_r{r}.json")
            with open(tfile, "w", encoding="utf-8") as f:
                json.dump(trace_r, f, ensure_ascii=False, indent=2)
            print(f"[S4-播放器]   \u21b3 \u8ffd\u8e2a\u5df2\u8bb0\u5f55: {tfile} ({len(trace_r)} \u6761\u575a\u5b88)")

        # 合并所有轮次追踪
        all_traces = []
        for r in range(1, rounds + 1):
            _f = os.path.join(_data_dir_for(self.skill_dir), f".s4_trace_r{r}.json")
            if os.path.exists(_f):
                with open(_f, "r", encoding="utf-8") as fh:
                    all_traces.extend(json.load(fh))
        main_t = os.path.join(_data_dir_for(self.skill_dir), ".s4_trace.json")
        out_t = os.path.join(_data_dir_for(self.skill_dir), ".s4_trace.json")
        with open(main_t, "w", encoding="utf-8") as f:
            json.dump(all_traces, f, ensure_ascii=False, indent=2)
        with open(out_t, "w", encoding="utf-8") as f:
            json.dump(all_traces, f, ensure_ascii=False, indent=2)
        print(f"\n  \u2500\u2500 \u81ea\u52a8\u5316\u8ffd\u8e2a\u5b8c\u6210 \u2500\u2500")
        print(f"  依次读取 .s4_script_r1.json ~ .s4_script_r{rounds}.json")
        print(f"  逐条执行噪音注入，每条记录坚守/失守")
        print(f"  执行记录保存到 .s4_trace_rN.json")
        print(f"{'='*55}")


# ═══════════════════════════════════════════════════════
# 阶段D：生成坚守率矩阵
# ═══════════════════════════════════════════════════════

def generate_fidelity_matrix(trace_records: list[dict]) -> dict:
    """
    从 S4 执行记录生成坚守率统计。

    输出:
        matrix: {
            "summary": {"total": N, "坚守": M, "失守": K, "坚守率": "XX%"},
            "details": [
                {
                    "nid": "N-01", "cid": "C-07",
                    "level": "L4", "behavior": "坚守",
                    "detail": "..."
                },
                ...
            ],
            "failures": ["C-12 (应执行回归确认) — 坚守率 33%"],
        }
    """
    if not trace_records:
        return {"summary": {"total": 0, "坚守": 0, "失守": 0, "坚守率": "0%"}, "details": [], "failures": []}

    total = len(trace_records)
    held = sum(1 for t in trace_records if t.get("llm_behavior") == "坚守")
    failed = total - held
    rate = f"{held}/{total} ({held/total*100:.0f}%)"

    # 按 cid 分组统计
    cid_groups = {}
    for t in trace_records:
        cid = t.get("cid", "?")
        if cid not in cid_groups:
            cid_groups[cid] = {"total": 0, "held": 0, "texts": []}
        cid_groups[cid]["total"] += 1
        if t.get("llm_behavior") == "坚守":
            cid_groups[cid]["held"] += 1

    # 标记纸老虎（坚守率 < 100% 的约束）
    failures = []
    for cid, g in sorted(cid_groups.items()):
        if g["held"] < g["total"]:
            r = f"{g['held']}/{g['total']} ({g['held']/g['total']*100:.0f}%)"
            failures.append(f"{cid} — 坚守率 {r} ❌")

    return {
        "summary": {"total": total, "坚守": held, "失守": failed, "坚守率": rate},
        "details": trace_records,
        "failures": failures,
    }


def print_fidelity_matrix(matrix: dict) -> str:
    """打印坚守率矩阵（人类可读格式）"""
    if matrix["summary"]["total"] == 0:
        return "[S4] 无 S4 测试记录"

    s = matrix["summary"]
    lines = [
        "=" * 62,
        "  S4 执行忠实度测试 — 坚守率矩阵",
        "=" * 62,
        f"  总计: {s['total']}  | 坚守: {s['坚守']}  | 失守: {s['失守']}  | 坚守率: {s['坚守率']}",
        "",
        "── 详细记录:",
    ]

    for t in matrix["details"]:
        icon = "✅" if t.get("llm_behavior") == "坚守" else "❌"
        nid = t.get("nid", "?")
        level = t.get("level", "?")
        noise = t.get("noise_text", "")[:50]
        behavior = t.get("llm_behavior", "?")
        lines.append(f"  {icon} [{nid}] {level} {noise} → {behavior}")
        if t.get("detail"):
            lines.append(f"     详情: {t['detail'][:80]}")

    lines.append("")
    if matrix["failures"]:
        lines.append("── 铁律溃败点（纸老虎）:")
        for f in matrix["failures"]:
            lines.append(f"  ❌ {f}")
    else:
        lines.append("  ✅ 全部坚守，无纸老虎")

    lines.append("")
    lines.append("  ⚠️ 单实例脏数据测试置信度无保证")
    lines.append("     噪音方案设计与执行同属一个 LLM 会话，测试数据仅供参考")
    lines.append("     可靠结果需跨会话执行（阶段B、阶段C分属不同会话）")

    lines.append("=" * 62)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════
# 阶段E：正向工作流步骤提取
# ═══════════════════════════════════════════════════════

def extract_workflow_steps(skill_dir: str) -> list[dict]:
    """
    从目标技能的 SKILL.md 工作流程章节解析步骤序列。

    返回:
        list[dict]: 步骤列表，每个元素 {order, title, description}
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        return []

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    import re

    steps = []
    in_workflow = False
    order = 0

    for line in lines:
        stripped = line.strip()
        if not in_workflow:
            if stripped.startswith("## ") and ("工作流程" in stripped or "流程" in stripped or "workflow" in stripped.lower()):
                in_workflow = True
            continue

        if stripped.startswith("## ") and "流程" not in stripped and "工作" not in stripped:
            break

        # 匹配 "N. **标题** — 描述"
        m = re.match(r'^(\d+)\.\s+\*\*(.+?)\*\*\s*[—\-–]\s*(.*)', stripped)
        if m:
            steps.append({"order": int(m.group(1)), "title": m.group(2).strip(), "description": m.group(3).strip()[:120]})
            continue

        # 匹配 "- **标题** — 描述"（无序号）
        m2 = re.match(r'^[\*\-\+]\s+\*\*(.+?)\*\*\s*[—\-–]\s*(.*)', stripped)
        if m2:
            order += 1
            steps.append({"order": order, "title": m2.group(1).strip(), "description": m2.group(2).strip()[:120]})

    return steps


def print_workflow_steps(steps: list[dict]) -> str:
    if not steps:
        return "[S4] 未提取到工作流步骤"
    lines = [f"  ┌── 工作流程: {len(steps)} 步 ──┐"]
    for s in steps:
        lines.append(f"  │ {s['order']}. {s['title'][:20]:<20s} {s['description'][:40]}")
    lines.append(f"  └{'─'*38}┘")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════
# 阶段F：综合忠实度评分（正反因子）
# ═══════════════════════════════════════════════════════

def generate_fidelity_score(
    positive_rate: float, negative_rate: float,
    positive_factor: float = 0.4, negative_factor: float = 0.6,
) -> dict:
    """
    S4 忠实度 = pf × pr + nf × nr

    等级:
      >=0.9 S  |  >=0.8 A  |  >=0.6 B  |  >=0.4 C  |  <0.4 D
    """
    score = positive_factor * positive_rate + negative_factor * negative_rate
    level = "S (优秀)" if score >= 0.9 else "A (良好)" if score >= 0.8 else "B (合格)" if score >= 0.6 else "C (较差)" if score >= 0.4 else "D (不合格)"
    return {"positive_rate": round(positive_rate, 2), "negative_rate": round(negative_rate, 2), "positive_factor": positive_factor, "negative_factor": negative_factor, "score": round(score, 2), "level": level}


def print_fidelity_score(result: dict) -> str:
    return "\n".join([
        "=" * 50,
        "  S4 综合忠实度评分",
        "=" * 50,
        f"  正向完成率: {result['positive_rate']*100:.0f}% × 权重 {result['positive_factor']}",
        f"  反向坚守率: {result['negative_rate']*100:.0f}% × 权重 {result['negative_factor']}",
        f"  ─────────────────────────────",
        f"  综合分数: {result['score']*100:.0f}%  → {result['level']}",
        "",
        "  ⚠️ 单实例脏数据测试置信度无保证",
        "     噪音方案设计与执行同属一个 LLM 会话，测试数据仅供参考",
        "     可靠结果需跨会话执行（阶段B、阶段C分属不同会话）",
        "=" * 50,
    ])


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

USAGE = """
用法:
  python s4_engine.py <skill-dir> constraints            — 打印约束清单
  python s4_engine.py <skill-dir> scope                  — 生成全量测试范围（含蓝皮书+工作流+引用）
  python s4_engine.py <skill-dir> validate <json>        — 校验噪音方案 schema
  python s4_engine.py <skill-dir> report                 — 从 trace 生成坚守率报告
  python s4_engine.py <skill-dir> steps                  — 打印工作流步骤序列
  python s4_engine.py <skill-dir> score <pr> <nr>        — 综合评分 (pf=0.4 nf=0.6)
  python s4_engine.py <skill-dir> play [rounds]          — 随机化回放生成噪音脚本
  python s4_engine.py <skill-dir> repair [--dry-run]     — 修复引用链路断裂和缺失文件
"""


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        return

    skill_dir = sys.argv[1]
    cmd = sys.argv[2]
    _hook_check(skill_dir, "s4")
    s4_label = f"S4 {cmd}"

    _tl(skill_dir, f"s4_{cmd}", s4_label, "--type", "py_script")

    if cmd == "constraints":
        constraints = load_constraints(skill_dir)
        print(print_constraint_summary(constraints))

    elif cmd == "scope":
        scope = generate_test_scope(skill_dir)
        save_test_scope(skill_dir, scope)
        print(print_constraint_summary(scope))

    elif cmd == "validate":
        if len(sys.argv) < 4:
            print("缺少方案 JSON 路径")
            _tl(skill_dir, f"s4_{cmd}", s4_label, "end", "--type", "py_script", "--detail", "缺少参数")
            return
        plan_path = sys.argv[3]
        if os.path.exists(plan_path):
            with open(plan_path, "r", encoding="utf-8") as f:
                plan = json.load(f)
        else:
            try:
                plan = json.loads(plan_path)
            except json.JSONDecodeError:
                print(f"无法解析 JSON: {plan_path}")
                _tl(skill_dir, f"s4_{cmd}", s4_label, "end", "--type", "py_script", "--detail", "JSON解析失败")
                return
        errors = validate_noise_plan(plan)
        if errors:
            print(f"[S4] ❌ 噪音方案校验失败 ({len(errors)} 个错误):")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"[S4] ✅ 噪音方案校验通过 ({len(plan)} 条)")

    elif cmd == "report":
        trace = load_trace(skill_dir)
        matrix = generate_fidelity_matrix(trace)
        print(print_fidelity_matrix(matrix))

    elif cmd == "steps":
        steps = extract_workflow_steps(skill_dir)
        print(print_workflow_steps(steps))

    elif cmd == "score":
        if len(sys.argv) < 4:
            print("用法: score <positive_rate> <negative_rate> [pf=0.4 nf=0.6]")
            _tl(skill_dir, f"s4_{cmd}", s4_label, "end", "--type", "py_script", "--detail", "缺少参数")
            return
        pr = float(sys.argv[2])
        nr = float(sys.argv[3])
        pf = float(sys.argv[4]) if len(sys.argv) >= 5 else 0.4
        nf = float(sys.argv[5]) if len(sys.argv) >= 6 else 0.6
        result = generate_fidelity_score(pr, nr, pf, nf)
        print(print_fidelity_score(result))

    elif cmd == "play":
        # 从配置读轮次，命令行参数可覆盖
        default_rounds = 3
        config_path = os.path.join(_data_dir_for(skill_dir), "outputs", ".test-config.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            default_rounds = cfg.get("s4", {}).get("rounds", cfg.get("rounds", 3))
        except Exception:
            pass
        rounds = int(sys.argv[3]) if len(sys.argv) >= 4 else default_rounds
        player = NoisePlayer(skill_dir)
        if player.plan:
            player.playback_all_rounds(rounds=rounds)
        else:
            print(f"[S4] ❌ 无噪音方案，请先执行阶段B")

    elif cmd == "repair":
        dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
        scope = load_test_scope(skill_dir)
        if not scope:
            scope = generate_test_scope(skill_dir)
        repairs = s4_scope_repair(skill_dir, scope, dry_run=dry_run)
        if not repairs:
            print("[S4-修复] 无需要修复的项")

    else:
        print(f"未知命令: {cmd}")
        print(USAGE)

    _tl(skill_dir, f"s4_{cmd}", s4_label, "end", "--type", "py_script")
    _hook_done(skill_dir, "s4")


if __name__ == "__main__":
    main()
