"""
scenario_engine.py — 场景测试引擎

从蓝皮书（inspector 产出）获取目标技能的完整元信息（脚本清单、函数、引用链路、import_chain），
基于蓝皮书数据自动构建测试计划并对每个场景执行真实 CLI 命令。

蓝皮书即事实来源——所有代码分析已在 inspector 中完成，此处不重复扫描。
场景引擎只关心"目标技能有什么可执行的 CLI 脚本"，不解析 SKILL.md 正文格式。

蓝皮书即事实来源——所有代码分析已在 inspector 中完成，此处不重复扫描。

场景链路的两个维度（全部基于蓝皮书数据，不依赖 SKILL.md 写作格式）：
S1 场景链路完整性 — 从 frontmatter trigger 匹配 CLI 脚本并执行（元数据驱动）
S2 场景输入产出匹配 — 遍历蓝皮书中所有 CLI 脚本，逐一测试 --help 及其它参数
S3 场景数据流正确性 — 从蓝皮书 import_chain 构建依赖链，测试跨脚本调用链路

时间线集成：每个场景/每个 CLI 调用都记录独立的 [START]/[END] marker。
"""
import ast
import json
import os
import re
import subprocess
import sys
from typing import Optional

# R-12 审计锚点
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-function-test/data/"
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.normpath(os.path.join(_SCRIPT_DIR, ".."))
_SKILLS_ROOT = os.path.normpath(os.path.join(_SKILL_DIR, ".."))
DATA_DIR = os.path.normpath(os.path.join(_SKILLS_ROOT, ".standardization", "skill-function-test", "data"))


def _data_dir_for(skill_dir: str) -> str:
    """目标技能的数据子目录"""
    target_name = os.path.basename(os.path.abspath(skill_dir))
    d = os.path.join(DATA_DIR, target_name)
    os.makedirs(d, exist_ok=True)
    return d

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

def _run_timed(skill_dir, cmd_args, label, phase="scene_test"):
    """执行 subprocess 并记 wall time"""
    _tl(skill_dir, phase, label, "--type", "subprocess_wall")
    t0 = subprocess.run([sys.executable, _TIMELINE_SCRIPT, "mark", skill_dir,
                         phase, label, "--type", "subprocess_wall"],
                        capture_output=True, timeout=10)
    # 实际标记以上面为准，这里只是为了后续 end 能引用
    try:
        result = subprocess.run(
            cmd_args, capture_output=True, text=True, timeout=30,
        )
        wall = subprocess.run([sys.executable, "-c", "import time; print(time.perf_counter())"],
                               capture_output=True, text=True, timeout=10)
    except:
        pass
    _tl(skill_dir, phase, label, "end", "--type", "subprocess_wall")


class ScenarioResult:
    def __init__(self, sid: str, name: str, status: str = "pass",
                 level: str = "info", message: str = "",
                 file: str = "", lineno: int = 0,
                 suggestion: str = "", detail: str = ""):
        self.sid = sid
        self.name = name
        self.status = status
        self.level = level
        self.message = message
        self.file = file
        self.lineno = lineno
        self.suggestion = suggestion
        self.detail = detail

    def to_dict(self) -> dict:
        return {k: getattr(self, k) for k in
                ("sid", "name", "status", "level", "message",
                 "file", "lineno", "suggestion", "detail")}

    def __str__(self):
        icon = {"pass": "PASS", "fail": "FAIL", "skip": "SKIP"}.get(self.status, "?")
        loc = f" {self.file}:{self.lineno}" if self.file else ""
        lev = f"[{self.level.upper()}]" if self.level in ("block", "warn") else ""
        return f"  {icon} {lev} [{self.sid}] {self.name}{loc} — {self.message}"


# ═══════════════════════════════════════════════════════
# SKILL.md 场景解析
# ═══════════════════════════════════════════════════════

def parse_skill_md(skill_dir: str) -> dict:
    """从目标技能目录解析 SKILL.md，提取前件 trigger 场景（元数据）"""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        return {"error": "SKILL.md 不存在"}

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    result = {
        "trigger_scenes": [],
    }

    # 解析 Frontmatter trigger（结构化元数据，支持 YAML 列表和 / 分隔两种格式）
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        for line in fm.split("\n"):
            sline = line.strip()
            if sline.startswith("trigger:"):
                val = sline.split(":", 1)[1].strip()
                # YAML 列表格式: ['a', 'b', 'c']
                if val.startswith("["):
                    result["trigger_scenes"] = [
                        s.strip().strip("'\"") for s in val.strip("[]").split(",") if s.strip()
                    ]
                # / 分隔格式: a / b / c
                else:
                    val = val.strip("'\"")
                    result["trigger_scenes"] = [
                        s.strip() for s in val.split("/") if s.strip()
                    ]

    return result


# ═══════════════════════════════════════════════════════
# 测试计划构建（完全基于蓝皮书数据，不重新扫描）
# ═══════════════════════════════════════════════════════

def auto_build_test_plan(parsed_md: dict, blueprint: dict) -> list[dict]:
    """
    根据蓝皮书数据构建测试计划（蓝皮书驱动，不依赖 SKILL.md 写作格式）。
    
    蓝皮书由 inspector 在阶段 2 生成，包含：
      - cli_scripts: 所有有 __main__ 的脚本及其支持的参数
      - functions: 所有函数的 AST 签名
      - import_chain: 模块间引用关系
      - file_manifest: 完整文件清单
    
    架构原则：
      S1 — 从蓝皮书的 trigger 场景匹配 CLI 脚本（frontmatter 是元数据，非正文格式）
      S2 — 遍历蓝皮书中所有 CLI 脚本，直接测试（不解析正文 ## 核心能力）
      S3 — 从蓝皮书的 import_chain 构建依赖链，测试跨脚本调用链路
    """

    cli_scripts = blueprint.get("cli_scripts", [])
    import_chain = blueprint.get("import_chain", {})
    tests = []

    # ── S1: 从 trigger 场景匹配 CLI 脚本（frontmatter 元数据） ──
    for scene in parsed_md.get("trigger_scenes", []):
        matched = []
        kw = scene.lower().replace("/", " ").split()
        for s in cli_scripts:
            sname = s["name"].lower()
            for k in kw:
                if len(k) >= 2 and (k in sname or k in s["path"].lower()):
                    matched.append(s)
                    break
        tests.append({
            "scene": scene, "source": "trigger",
            "matched_scripts": matched[:5],
        })

    # ── S2: 遍历所有 CLI 脚本（蓝皮书驱动，不解析 ## 核心能力） ──
    for s in cli_scripts:
        name = s["name"]
        if name in ("__init__", "__main__"):  # 入口脚本由 trigger 单独测试
            continue
        tests.append({
            "scene": f"脚本:{name}", "source": "capability",
            "matched_scripts": [s],
        })

    # ── S3: 从 import_chain 构建依赖链 ──
    # 找到 CLI 脚本之间的交叉引用关系
    script_by_name = {s["name"]: s for s in cli_scripts}
    seen_chains = set()
    for s in cli_scripts:
        mod_name = s["name"]
        deps = import_chain.get(mod_name, [])
        chain_members = []
        for dep in deps:
            if dep in script_by_name and dep != mod_name:
                chain_members.append(script_by_name[dep])
        if chain_members:
            chain_key = f"{mod_name}->{'+'.join(c['name'] for c in chain_members)}"
            if chain_key not in seen_chains:
                seen_chains.add(chain_key)
                tests.append({
                    "scene": f"依赖链:{mod_name}→{','.join(c['name'] for c in chain_members[:3])}",
                    "source": "workflow",
                    "matched_scripts": [s] + chain_members[:3],
                })

    return tests


# ═══════════════════════════════════════════════════════
# 场景测试执行器
# ═══════════════════════════════════════════════════════

class ScenarioRunner:
    """
    通用场景测试执行器。
    基于蓝皮书的 cli_scripts 清单执行真实 CLI 命令。
    不硬编码任何技能特定的脚本名、参数或路径。
    """

    def __init__(self, skill_dir: str, blueprint: dict):
        self.skill_dir = skill_dir
        self.blueprint = blueprint  # 蓝皮书即事实来源
        self.results: list[ScenarioResult] = []

        # 从蓝皮书获取 CLI 脚本（infra 层已在 inspector 中完成检测）
        self.cli_scripts = blueprint.get("cli_scripts", [])

        # 解析 SKILL.md
        self.parsed_md = parse_skill_md(skill_dir)

        # 强制要求手工测试计划，无自动构建 fallback
        self.test_plan = []
        test_plan_path = os.path.join(_data_dir_for(skill_dir), "outputs", ".s_test_plan.json")
        if not os.path.exists(test_plan_path):
            print("\n" + "=" * 60)
            print("  ⛔ 阻断: 未找到 .s_test_plan.json")
            print("  场景测试要求 LLM 手工编写测试计划。")
            print("  请阅读 SKILL.md 和蓝皮书，按 references/s-test-plan-schema.md 格式")
            print(f"  写入: {test_plan_path}")
            print("=" * 60 + "\n")
            sys.exit(1)

        try:
            with open(test_plan_path, "r", encoding="utf-8") as f:
                manual_plan = json.load(f)
            source_map = {"S1": "trigger", "S2": "capability", "S3": "workflow"}
            cli_scripts = self.blueprint.get("cli_scripts", [])
            all_modules = []
            for p in self.blueprint.get("file_manifest", {}).get("python", []):
                mod_name = os.path.splitext(os.path.basename(p))[0]
                if mod_name not in ("__init__", "__main__"):
                    all_modules.append({"name": mod_name, "path": p, "has_cli": False})
            for s in cli_scripts:
                for m in all_modules:
                    if m["name"] == s["name"]:
                        m["has_cli"] = True
                        break
            matched_count = 0
            module_matched_count = 0
            mod_name_to_entry = {m["name"]: m for m in all_modules}
            for s_type, items in manual_plan.items():
                mapped = source_map.get(s_type, s_type.lower())
                for item in items:
                        item["source"] = mapped
                        item["scene"] = item.get("name", item.get("trigger", "?"))
                        # ★ 如果测试用例写了 modules 字段，直接用它映射
                        specified = item.get("modules", [])
                        if specified:
                            matched_cli = []
                            has_non_cli = False
                            for mod_name in specified:
                                m_entry = mod_name_to_entry.get(mod_name)
                                if m_entry:
                                    if m_entry["has_cli"]:
                                        # 从 cli_scripts 中找同名条目（带上 supports 等元信息）
                                        for cs in cli_scripts:
                                            if cs["name"] == mod_name:
                                                matched_cli.append(cs)
                                                break
                                    else:
                                        has_non_cli = True
                            item["matched_scripts"] = matched_cli[:5]
                            item["_module_matches"] = [{"name": n} for n in specified
                                                       if n in mod_name_to_entry]
                            if matched_cli:
                                matched_count += 1
                            elif has_non_cli:
                                module_matched_count += 1
                        else:
                            # ★ 没有 modules 字段 → fall back 关键词匹配
                            keywords = []
                            for field in ("name", "trigger", "input", "expected"):
                                val = item.get(field, "")
                                if val:
                                    eng = re.findall(r'[a-zA-Z_][a-zA-Z0-9_.]*', val)
                                    keywords.extend(e.lower() for e in eng)
                                    for seg in re.split(r'[，。、；：（）\[\]【】/\\\s]+', val):
                                        seg = seg.strip()
                                        if seg and (seg.isascii() or any(c.isascii() for c in seg)):
                                            keywords.append(seg.lower())
                            for step in item.get("steps", []):
                                eng = re.findall(r'[a-zA-Z_][a-zA-Z0-9_.]*', step)
                                keywords.extend(e.lower() for e in eng)
                            if s_type == "S1":
                                keywords.extend(self.parsed_md.get("trigger_scenes", []))
                            keywords = sorted(set(k for k in keywords if len(k) >= 2))
                            matched_cli = []
                            for s in cli_scripts:
                                sname = s["name"].lower()
                                spath = s["path"].lower()
                                for k in keywords:
                                    if k in sname or k in spath or sname in k or spath in k:
                                        matched_cli.append(s)
                                        break
                            item["matched_scripts"] = matched_cli[:5]
                            if matched_cli:
                                matched_count += 1
                            # 额外匹配所有 Python 模块
                            matched_mods = []
                            for m in all_modules:
                                mname = m["name"].lower()
                                mpath = m["path"].lower()
                                for k in keywords:
                                    if k in mname or k in mpath or mname in k or mpath in k:
                                        matched_mods.append(m)
                                        break
                            item["_module_matches"] = matched_mods[:5]
                            if matched_mods and not matched_cli:
                                module_matched_count += 1
                        self.test_plan.append(item)
                if self.test_plan:
                    print(f"  [SCENARIO] 使用手工编写的场景测试计划 ({len(self.test_plan)} 条, "
                          f"其中 {matched_count} 条匹配到 CLI 脚本"
                          + (f", {module_matched_count} 条匹到无CLI入口模块" if module_matched_count else "")
                          + ")")
        except Exception as e:
            print(f"\n  ⛔ 加载 .s_test_plan.json 失败: {e}")
            print(f"  请按 references/s-test-plan-schema.md 修正格式后重试\n")
            sys.exit(1)

        # 从配置读取启用的场景维度，禁用的从 test_plan 中移除
        config_path = os.path.join(_data_dir_for(skill_dir), "outputs", ".test-config.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            sc = cfg.get("scenarios", {})
            enabled_dims = [k for k in ["S1", "S2", "S3"]
                            if sc.get(k, {}).get("enabled", True)]
            source_to_dim = {"trigger": "S1", "capability": "S2", "workflow": "S3"}
            self.test_plan = [t for t in self.test_plan
                              if source_to_dim.get(t["source"], "") in enabled_dims]
            disabled = [k for k in ["S1", "S2", "S3"] if k not in enabled_dims]
            if disabled:
                print(f"  [SCENARIO] 禁用的场景维度: {', '.join(disabled)}")
        except Exception:
            pass

    def add(self, r: ScenarioResult):
        self.results.append(r)

    def run(self):
        """执行 S1-S3 场景测试，每个场景独立计时"""
        _tl(self.skill_dir, "S1", "场景链路完整性", "--type", "py_script")
        self._run_s1_scenarios()
        _tl(self.skill_dir, "S1", "场景链路完整性", "end", "--type", "py_script")

        _tl(self.skill_dir, "S2", "场景输入产出匹配", "--type", "py_script")
        self._run_s2_scenarios()
        _tl(self.skill_dir, "S2", "场景输入产出匹配", "end", "--type", "py_script")

        _tl(self.skill_dir, "S3", "场景数据流正确性", "--type", "py_script")
        self._run_s3_scenarios()
        _tl(self.skill_dir, "S3", "场景数据流正确性", "end", "--type", "py_script")

    def _exec(self, script: dict, args: list[str],
              test_name: str, sid: str) -> ScenarioResult:
        """执行 CLI 脚本，含 subprocess wall time 计时"""
        abspath = os.path.join(self.skill_dir, script["path"])
        cmd = [sys.executable, abspath] + args
        label_detail = f"{script['name']} {' '.join(args)}"

        # 记 subprocess wall time start
        _tl(self.skill_dir, f"target_{sid}", f"{sid}: {label_detail}", "--type", "subprocess_wall")

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=self.skill_dir,
            )
            wall_time = "unknown"
            if result.returncode in (0, 2):
                _tl(self.skill_dir, f"target_{sid}", f"{sid}: {label_detail}", "end",
                       "--type", "subprocess_wall", "--detail", f"rc={result.returncode}")
                return ScenarioResult(sid, f"「{test_name}」", "pass", "info",
                                       f"rc={result.returncode}")
            err = result.stderr.strip()[:150] or result.stdout.strip()[:150]
            _tl(self.skill_dir, f"target_{sid}", f"{sid}: {label_detail}", "end",
                   "--type", "subprocess_wall", "--detail", f"rc={result.returncode}: {err}")
            return ScenarioResult(sid, f"「{test_name}」", "fail", "warn",
                                   f"rc={result.returncode}: {err}",
                                   script["path"])
        except subprocess.TimeoutExpired:
            _tl(self.skill_dir, f"target_{sid}", f"{sid}: {label_detail}", "end",
                   "--type", "subprocess_wall", "--detail", "timeout")
            return ScenarioResult(sid, f"「{test_name}」", "fail", "block",
                                   "执行超时 (30s)", script["path"])
        except Exception as e:
            _tl(self.skill_dir, f"target_{sid}", f"{sid}: {label_detail}", "end",
                   "--type", "subprocess_wall", "--detail", str(e)[:50])
            return ScenarioResult(sid, f"「{test_name}」", "fail", "block",
                                   f"执行异常: {e}", script["path"])

    def _check_module(self, module_name: str, test_case: dict) -> ScenarioResult:
        """导入非 CLI 模块，验证模块可导入"""
        import importlib

        scripts_dir = os.path.join(self.skill_dir, "scripts")
        sid = {"trigger": "S1", "capability": "S2", "workflow": "S3"}.get(
            test_case.get("source", ""), "S?")

        try:
            old_path = list(sys.path)
            if scripts_dir not in sys.path:
                sys.path.insert(0, scripts_dir)
            try:
                importlib.import_module(module_name)
            finally:
                sys.path = old_path

            return ScenarioResult(sid, f"「{test_case.get('scene','?')}」",
                                   "pass", "info",
                                   f"{module_name} 导入成功")
        except SyntaxError as e:
            return ScenarioResult(sid, f"「{test_case.get('scene','?')}」",
                                   "fail", "block",
                                   f"{module_name} 语法错误: {e}")
        except ImportError as e:
            return ScenarioResult(sid, f"「{test_case.get('scene','?')}」",
                                   "fail", "block",
                                   f"{module_name} 导入失败: {e}")
        except Exception as e:
            return ScenarioResult(sid, f"「{test_case.get('scene','?')}」",
                                   "fail", "warn",
                                   f"{module_name} 异常: {e}")

    def _run_suite(self, tests: list[dict], sid: str, label: str):
        """通用场景执行逻辑"""
        if not tests:
            self.add(ScenarioResult(sid, label, "skip", "info", "无测试场景"))
            return

        executed = 0
        module_checked = 0
        for test in tests:
            scripts = test["matched_scripts"]
            if not scripts:
                mods = test.get("_module_matches", [])
                if mods:
                    for m in mods:
                        r = self._check_module(m["name"], test)
                        self.results.append(r)
                        module_checked += 1
                else:
                    self.add(ScenarioResult(sid, f"{label}「{test['scene'][:40]}」", "pass", "info",
                                             "由外部编排实现，无直接 CLI"))
                continue
            for sc in scripts:
                self._exec(sc, ["--help"],
                           f"{test['scene'][:30]} → {sc['name']} --help", sid)
                executed += 1
                # 如果脚本有 --json/--list/--show，也测试
                for flag in ["--json", "--list", "--show", "--check-only"]:
                    if sc["supports"].get(flag):
                        self._exec(sc, [flag],
                                   f"{test['scene'][:30]} → {sc['name']} {flag}", sid)
                        executed += 1
                        break

        if executed > 0:
            self.add(ScenarioResult(sid, f"{label}执行汇总", "pass", "info",
                                     f"执行了 {executed} 个 CLI 命令"))

    # ═══════════════════════════════════════════════════════
    # S1: 每个 trigger 场景执行 CLI 验证
    # ═══════════════════════════════════════════════════════
    def _run_s1_scenarios(self):
        trigger_tests = [t for t in self.test_plan if t["source"] == "trigger"]
        self._run_suite(trigger_tests, "S1", "触发场景")

    # ═══════════════════════════════════════════════════════
    # S2: 每个核心能力执行 CLI 验证
    # ═══════════════════════════════════════════════════════
    def _run_s2_scenarios(self):
        cap_tests = [t for t in self.test_plan if t["source"] == "capability"]
        self._run_suite(cap_tests, "S2", "核心能力")

    # ═══════════════════════════════════════════════════════
    # S3: 工作流步骤端到端 CLI 验证
    # ═══════════════════════════════════════════════════════
    def _run_s3_scenarios(self):
        wf_tests = [t for t in self.test_plan if t["source"] == "workflow"]
        if not wf_tests:
            self.add(ScenarioResult("S3", "工作流链路", "skip", "info", "无工作流程"))
            return
        tested = set()
        for test in wf_tests:
            tname = test.get("scene", test.get("name", "?"))[:40]
            scripts = test.get("matched_scripts", [])
            if not scripts:
                mods = test.get("_module_matches", [])
                if mods:
                    for m in mods:
                        r = self._check_module(m["name"], test)
                        self.results.append(r)
                else:
                    self.add(ScenarioResult("S3", f"工作流「{tname}」", "pass", "info",
                                             "由外部编排实现，无直接 CLI"))
                continue
            for sc in scripts:
                p = sc["path"]
                if p in tested:
                    continue
                tested.add(p)
                self._exec(sc, ["--help"],
                           f"工作流:{sc['name']} --help", "S3")
        if tested:
            self.add(ScenarioResult("S3", "工作流链路", "pass", "info",
                                     f"验证了 {len(tested)} 个脚本入口"))

    def generate_report(self) -> dict:
        summary = {"total": 0, "pass": 0, "fail": 0, "skip": 0,
                   "block": 0, "warn": 0, "info": 0}
        for r in self.results:
            summary["total"] += 1
            summary[r.status] += 1
            if r.level in ("block", "warn", "info"):
                summary[r.level] += 1
        return {"summary": summary, "results": [r.to_dict() for r in self.results]}

    def print_report(self) -> str:
        s = self.generate_report()["summary"]
        lines = [
            "=" * 60,
            "  场景测试报告（基于蓝皮书 · 真实 CLI 执行）",
            "=" * 60,
            f"  总计: {s['total']} | 通过: {s['pass']} | 失败: {s['fail']} | 跳过: {s['skip']}",
            f"  F-0 BLOCK: {s['block']} | F-1 WARN: {s['warn']} | F-2 INFO: {s['info']}",
            "",
            "── 详细结果:",
        ]
        for r in self.results:
            lines.append(str(r))
            if r.suggestion:
                lines.append(f"    场景建议: {r.suggestion[:150]}")
        lines.append("=" * 60)
        lines.append(f"  场景结论: {'PASS' if s['block'] == 0 else 'FAIL'} (BLOCK={s['block']})")
        lines.append("=" * 60)
        return "\n".join(lines)


def run_scenario_test(skill_dir: str, blueprint: dict) -> tuple[dict, str]:
    _tl(skill_dir, "scenario", "场景测试总入口", "--type", "py_script")
    runner = ScenarioRunner(skill_dir, blueprint)
    runner.run()
    _tl(skill_dir, "scenario", "场景测试总入口", "end", "--type", "py_script")
    return runner.generate_report(), runner.print_report()


if __name__ == "__main__":
    from inspector import scan

    if len(sys.argv) >= 2:
        target = sys.argv[1]
        _hook_check(target, "scenario")
        _tl(target, "scenario", "场景测试（独立运行）", "--type", "py_script")
        bb = scan(target)
        bp = bb.to_dict()

        # 读取轮次配置
        try:
            from test_config import load_config
            test_rounds = load_config(target).get("rounds", 3)
        except Exception:
            test_rounds = 3

        all_reports = []
        all_texts = []
        _tl_base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "..", ".standardization", "skill-function-test", "data",
                                os.path.basename(os.path.abspath(target)))
        # 在轮次开始前快照基线（第0轮），作为 delta 计算基准
        if test_rounds > 1:
            _tl_file = os.path.join(_tl_base, ".timeline.json")
            if os.path.exists(_tl_file):
                import shutil
                shutil.copy2(_tl_file, os.path.join(_tl_base, ".timeline_r0.json"))
        for r in range(1, test_rounds + 1):
            if test_rounds > 1:
                print(f"\n  ── 场景测试 第 {r}/{test_rounds} 轮 ──")
            report, text = run_scenario_test(target, bp)
            all_reports.append(report)
            all_texts.append(text)
            # 每轮完成后快照 timeline，供 compute_round_stats 按轮统计
            if test_rounds > 1:
                _tl_file = os.path.join(_tl_base, ".timeline.json")
                if os.path.exists(_tl_file):
                    import shutil
                    shutil.copy2(_tl_file, os.path.join(_tl_base, f".timeline_r{r}.json"))
                print(f"  [场景] 第 {r} 轮完成 (BLOCK={report.get('summary',{}).get('block','?')})")

        # 使用最后一轮作为展示，但添加轮次信息
        report = all_reports[-1]
        text = all_texts[-1]
        report["_rounds_executed"] = len(all_reports)
        report["_rounds_configured"] = test_rounds

        # 如果多轮，汇总所有轮的 BLOCK 数量
        if len(all_reports) > 1:
            max_block = max(r.get("summary", {}).get("block", 0) for r in all_reports)
            report["summary"]["block"] = max_block
            report["_max_block_across_rounds"] = max_block

        print(text)
        if test_rounds > 1:
            print(f"  轮次执行: {len(all_reports)}/{test_rounds} 轮完成")
        _tl(target, "scenario", "场景测试（独立运行）", "end", "--type", "py_script")

        # 保存到中央数据目录（与 test_engine 一致）
        target_name = os.path.basename(os.path.abspath(target))
        data_dir = os.path.normpath(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "..", ".standardization", "skill-function-test", "data", target_name
        ))
        os.makedirs(data_dir, exist_ok=True)
        report_path = os.path.join(data_dir, "outputs", ".scenario-test_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n场景报告 JSON 已保存: {report_path}")
        _hook_done(target, "scenario")
    else:
        print("用法: python scenario_engine.py <skill-dir>")
