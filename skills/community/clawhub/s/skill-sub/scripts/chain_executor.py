"""
chain_executor.py - Chain Executor v1.22.0
调用链执行引擎：根据调用链定义生成结构化执行计划，
识别依赖关系、并行机会，输出 AI 可直接执行的指令序列。

v1.21.0: 面向对象改造，提升可维护性
v1.3.0: 接入 loop_branch_renderer，支持循环/分支渲染
v1.2.0: 里程碑通用逻辑规则、配置集成（重试次数从设置读取）。
v1.1.0: 三层回退执行规则、分级重试策略、retry_policy/failure_mode 信息输出。

注意：本脚本不直接执行技能（技能执行由 AI 完成），
而是生成详细的执行计划，供 AI 按步骤执行。

零外部依赖，仅使用 Python 标准库。
跨平台支持 Windows/Linux/macOS。
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-sub/data/"

SKILL_DIR = Path(__file__).resolve().parent.parent
# 运行时绝对路径
DATA_DIR = SKILL_DIR.parent / ".standardization" / "skill-sub" / "data"


# ============================================================
# Config - 配置管理
# ============================================================

class Config:
    """配置管理器"""
    
    def __init__(self, skill_dir, chain_home):
        self.skill_dir = skill_dir
        self.chain_home = chain_home
        self._config = None
    
    def load(self):
        """加载用户配置（合并默认值 + 用户覆盖）"""
        defaults_path = self.skill_dir / "scripts" / "default_config.json"
        defaults = {}
        if defaults_path.exists():
            defaults = json.loads(defaults_path.read_text(encoding="utf-8"))
        
        config_path = self.chain_home / "config.json"
        user_cfg = {}
        if config_path.exists():
            user_cfg = json.loads(config_path.read_text(encoding="utf-8"))
        
        defaults.update(user_cfg)
        self._config = defaults
        return defaults
    
    def get(self, key, default=None):
        if self._config is None:
            self.load()
        return self._config.get(key, default)
    
    def get_default_max_retries(self):
        return self.get("default_max_retries", 3)

# ============================================================
# PathManager - 路径管理
# ============================================================

class PathManager:
    """路径管理器（v1.29.0: 统一委托给 chain_manager 的实现）"""
    
    def __init__(self, skill_dir=None):
        self.skill_dir = Path(skill_dir) if skill_dir else Path(__file__).resolve().parent.parent
        self.chain_home = self._get_chain_home()
    
    def _get_chain_home(self):
        """获取调用链数据目录（复用 chain_manager 逻辑）"""
        env_home = os.environ.get("SKILL_SUB_HOME") or os.environ.get("SKILL_CHAIN_HOME")
        if env_home:
            return Path(env_home)
        # 统一使用 ~/.workbuddy 标准目录
        return Path.home() / ".workbuddy" / "skills" / ".standardization" / "skill-sub"
    
    def get_skills_dir(self):
        """获取技能目录"""
        env_dir = os.environ.get("WORKBUDDY_SKILLS_DIR")
        if env_dir:
            return Path(env_dir)
        return Path.home() / ".workbuddy" / "skills"
    
    def get_chain_dir(self, name=None):
        """获取调用链目录（与 chain_manager 统一路径）"""
        return self.chain_home / "chains"
    
    def find_skill_path(self, skill_name):
        """查找技能路径（与 chain_manager 一致）"""
        skills_dir = self.get_skills_dir()
        if not skills_dir.exists():
            return None
        # 精确匹配
        exact = skills_dir / skill_name
        if exact.is_dir():
            return exact
        # 模糊匹配
        target = skill_name.lower().replace(" ", "-")
        for entry in skills_dir.iterdir():
            if entry.is_dir():
                if entry.name.lower().replace(" ", "-") == target or target in entry.name.lower():
                    return entry
        return None

# ============================================================
# Validator - 里程碑判断 + 输入验证
# ============================================================

class Validator:
    """里程碑分类器 + 输入验证器
    
    v1.29.0: 合并 chain_manager.ChainValidator 的 7 条规则（原仅 4 条）
    """
    
    MILESTONE_KEYWORDS = [
        "交付", "完成", "上线", "发布", "部署", "审计", "安全",
        "v1", "v2", "v3", "版本", "里程碑",
        "测试", "验证", "校验", "审批", "审核",
        "付款", "支付", "下单", "提交", "推送",
        "导入", "导出", "迁移", "备份", "恢复",
        "audit", "deploy", "release", "publish", "push",
        "test", "verify", "validate", "approve", "review",
        "payment", "submit", "import", "export", "migrate",
        "backup", "restore", "build", "compile", "install",
    ]
    
    def classify_milestones(self, steps):
        """基于结构特征的通用里程碑判断。
        
        规则优先级（从高到低）：
        1. 用户显式标记 is_milestone=true → 里程碑
        2. 用户显式标记 is_milestone=false → 非里程碑
        3. 总步骤数 <= 2 → 全部里程碑（链太短，每步都关键）
        4. 步骤名包含里程碑关键词 → 里程碑
        5. 被多个后续步骤依赖（瓶颈点，>=2个后续步骤依赖它）→ 里程碑
        6. 是最后一步 → 里程碑（最终交付物）
        7. 其余 → 非里程碑
        
        返回：list[dict] 每项包含 index, is_milestone, reason
        """
        n = len(steps)
        if n == 0:
            return []
        
        depended_by = {}
        for i, step in enumerate(steps):
            idx = step.get("index", i + 1)
            depended_by[idx] = set()
        
        for i, step in enumerate(steps):
            idx = step.get("index", i + 1)
            for dep in step.get("depends_on", []):
                if dep in depended_by:
                    depended_by[dep].add(idx)
        
        results = []
        for i, step in enumerate(steps):
            idx = step.get("index", i + 1)
            fm = step.get("failure_mode", {})
            
            if fm.get("is_milestone") is True:
                results.append({"index": idx, "is_milestone": True, "reason": "用户显式标记"})
                continue
            
            step_name = step.get("step_name", "")
            step_name_lower = step_name.lower()
            
            if n <= 2:
                results.append({"index": idx, "is_milestone": True, "reason": "短链（<=2步），所有步骤均为里程碑"})
                continue
            
            keyword_hit = None
            for kw in self.MILESTONE_KEYWORDS:
                if kw.lower() in step_name_lower:
                    keyword_hit = kw
                    break
            if keyword_hit:
                results.append({"index": idx, "is_milestone": True, "reason": f"关键词匹配: '{keyword_hit}'"})
                continue
            
            downstream_count = len(depended_by.get(idx, set()))
            if downstream_count >= 2:
                results.append({"index": idx, "is_milestone": True, "reason": f"瓶颈点（{downstream_count}个后续步骤依赖）"})
                continue
            
            if i == n - 1:
                results.append({"index": idx, "is_milestone": True, "reason": "最终交付步骤"})
                continue
            
            explicit_false = fm.get("is_milestone") is False
            results.append({
                "index": idx,
                "is_milestone": False,
                "reason": "显式取消里程碑" if explicit_false else "默认规则（非关键节点）"
            })
        
        return results
    
    def validate_retry_policy(self, policy):
        """验证 retry_policy 合法性"""
        valid = ["none", "simple", "exponential", "fixed_interval"]
        if policy not in valid:
            return False, f"无效 retry_policy: {policy}，有效值: {valid}"
        return True, ""
    
    def validate_failure_mode(self, mode):
        """验证 failure_mode 合法性"""
        valid = ["abort", "continue", "rollback", "prompt"]
        if mode not in valid:
            return False, f"无效 failure_mode: {mode}，有效值: {valid}"
        return True, ""

# ============================================================
# TopoSorter - 步骤拓扑排序 + 计数
# ============================================================

class TopoSorter:
    """步骤拓扑排序器"""
    
    def topo_sort_substeps(self, steps):
        """对 loop/branch 内的子步骤进行拓扑排序（仅排序数组内步骤，不展开到顶层）"""
        if not steps:
            return steps
        
        from collections import defaultdict

        
        # 构建子步骤的 index map（支持子步骤有自己的 index）
        step_map = {}
        for i, s in enumerate(steps):
            idx = s.get("index", i + 1)
            step_map[idx] = s
        
        # 拓扑排序（仅考虑子步骤之间的依赖）
        exec_order = []
        executed = set()
        remaining = dict(step_map)
        
        while remaining:
            progress = False
            for idx, step in list(remaining.items()):
                deps = step.get("depends_on", [])
                # 只保留在 step_map 中的依赖（即同层子步骤内的依赖）
                local_deps = [d for d in deps if d in step_map]
                if all(d in executed for d in local_deps):
                    exec_order.append(step)
                    executed.add(idx)
                    del remaining[idx]
                    progress = True
            if not progress and remaining:
                # 有循环依赖，按 index 顺序强制加入
                idx = min(remaining.keys())
                exec_order.append(remaining[idx])
                executed.add(idx)
                del remaining[idx]
        
        # 递归处理嵌套的 loop/branch
        for step in exec_order:
            step_type = step.get("type", "skill")
            if step_type == "loop":
                loop = step.get("loop", {})
                if loop:
                    loop["steps"] = self.topo_sort_substeps(loop.get("steps", []))
            elif step_type == "branch":
                branch = step.get("branch", {})
                if branch:
                    branch["if_steps"] = self.topo_sort_substeps(branch.get("if_steps", []))
                    branch["else_steps"] = self.topo_sort_substeps(branch.get("else_steps", []))
        
        return exec_order
    
    def count_all_steps(self, steps):
        """递归统计所有步骤数（含 loop/branch 子步骤）"""
        count = 0
        for step in steps:
            count += 1  # 当前步骤本身
            step_type = step.get("type", "skill")
            if step_type == "loop":
                loop = step.get("loop", {})
                if loop:
                    mode = loop.get("mode", "for_each")
                    sub_steps = loop.get("steps", [])
                    if mode == "for_each":
                        items = loop.get("items", [])
                        if isinstance(items, list):
                            count += len(items) * self.count_all_steps(sub_steps)
                        else:
                            count += self.count_all_steps(sub_steps)
                    else:  # while
                        count += self.count_all_steps(sub_steps)
            elif step_type == "branch":
                branch = step.get("branch", {})
                if branch:
                    if_steps = branch.get("if_steps", [])
                    else_steps = branch.get("else_steps", [])
                    count += max(self.count_all_steps(if_steps), self.count_all_steps(else_steps))
        return count

# ============================================================
# InstructionGenerator - AI 指令生成器
# ============================================================

class InstructionGenerator:
    """AI 执行指令生成器"""
    
    def generate(self, plan):
        """根据执行计划生成 AI 执行指令"""
        lines = []
        lines.append(f"# 执行计划：{plan['chain_name']}")
        lines.append(f"# 描述：{plan['chain_description']}")

        # 未注册调度强制提醒（v1.26.0）
        sched = plan.get("unregistered_schedule")
        if sched:
            lines.append("")
            lines.append("!" * 60)
            lines.append("!  [强制] 调度尚未在平台注册")
            lines.append("!  此链配置了定时/自动化任务，但尚未注册到平台。")
            lines.append(f"!  类型: {sched.get('type', '?')}")
            lines.append(f"!  表达式: {sched.get('expression', '?')}")
            lines.append(f"!  描述: {sched.get('description', '无')}")
            lines.append("!")
            lines.append("!  AI 必须执行以下操作之一：")
            lines.append("!    1. 调用平台的调度注册接口完成注册")
            lines.append("!    2. 或运行: chain_manager.py register-schedule --name <链名>")
            lines.append("!  未注册前，调度不会生效。")
            lines.append("!" * 60)
            lines.append("")
        lines.append(f"# 目的：{plan['chain_purpose']}")
        lines.append(f"# 总步骤：{plan['total_steps']}")
        lines.append("")
        lines.append("## 执行步骤")
        lines.append("")
        
        for step in plan["exec_order"]:
            idx = step.get("index", "?")
            name = step.get("step_name", "")
            action = step.get("action", "")
            lines.append(f"### 步骤 {idx}: {name}")
            lines.append(f"动作：{action}")
            
            # 处理 loop 步骤
            if step.get("type", "skill") == "loop":
                loop = step.get("loop", {})
                lines.append(f"循环模式：{loop.get('mode', 'for_each')}")
                items = loop.get("items", [])
                if isinstance(items, list):
                    lines.append(f"循环项数：{len(items)}")
                lines.append("循环体步骤：")
                for sub in loop.get("steps", []):
                    sub_idx = sub.get("index", "?")
                    lines.append(f"  - 子步骤 {sub_idx}: {sub.get('step_name', '')}")
            
            # 处理 branch 步骤
            elif step.get("type", "skill") == "branch":
                branch = step.get("branch", {})
                condition = branch.get("condition", "")
                lines.append(f"条件：{condition}")
                lines.append("If 分支：")
                for sub in branch.get("if_steps", []):
                    sub_idx = sub.get("index", "?")
                    lines.append(f"  - 子步骤 {sub_idx}: {sub.get('step_name', '')}")
                lines.append("Else 分支：")
                for sub in branch.get("else_steps", []):
                    sub_idx = sub.get("index", "?")
                    lines.append(f"  - 子步骤 {sub_idx}: {sub.get('step_name', '')}")

            # 处理 adhesion 步骤（v1.25.0）
            elif step.get("type", "skill") == "adhesion":
                adhesion = step.get("adhesion", {})
                lines.append(f"⚠️ 粘连点 — 原因：{adhesion.get('reason', '未知')}")
                solutions = adhesion.get("solutions", [])
                for i, sol in enumerate(solutions, 1):
                    mode = sol.get("mode", "manual")
                    mode_label = {"manual": "纯手工", "auto": "脚本化", "hybrid": "混合"}.get(mode, mode)
                    desc = sol.get("description", "")
                    lines.append(f"  方案{i} [{mode_label}]：{desc}")
                    if mode == "hybrid":
                        if sol.get("llm_steps"): lines.append(f"    LLM: {sol['llm_steps']}")
                        if sol.get("tool_steps"): lines.append(f"    工具: {sol['tool_steps']}")
                    elif mode == "auto":
                        if sol.get("tool_name"): lines.append(f"    工具: {sol['tool_name']}")
                        if sol.get("script_path"): lines.append(f"    脚本: {sol['script_path']}")
                    if sol.get("constraints"):
                        lines.append(f"    约束: {sol['constraints']}")

            lines.append("")
        
        return "\n".join(lines)

# ============================================================
# ExecutionPlanBuilder - 执行计划生成器
# ============================================================

class ExecutionPlanBuilder:
    """执行计划构建器"""
    
    def __init__(self, chain_data, verbose=False, config=None, path_manager=None, validator=None, topo_sorter=None):
        self.chain_data = chain_data
        self.verbose = verbose
        self.config = config or Config(Path(""), Path(""))
        self.path_manager = path_manager or PathManager()
        self.validator = validator or Validator()
        self.topo_sorter = topo_sorter or TopoSorter()
    
    def build(self):
        """构建执行计划"""
        chain = self.chain_data
        steps = chain.get("steps", [])
        
        # 收集所有技能名称（含 loop/branch 嵌套）
        all_skill_names = self._collect_all_skill_names(steps)
        
        # 顶层拓扑排序
        exec_order = self._topo_sort_steps(steps)
        
        # 对 loop/branch 子步骤进行拓扑排序
        for step in exec_order:
            step_type = step.get("type", "skill")
            if step_type == "loop":
                loop = step.get("loop", {})
                if loop:
                    loop["steps"] = self.topo_sorter.topo_sort_substeps(loop.get("steps", []))
            elif step_type == "branch":
                branch = step.get("branch", {})
                if branch:
                    branch["if_steps"] = self.topo_sorter.topo_sort_substeps(branch.get("if_steps", []))
                    branch["else_steps"] = self.topo_sorter.topo_sort_substeps(branch.get("else_steps", []))
        
        # 构建执行计划
        plan = {
            "chain_name": chain.get("name", ""),
            "chain_description": chain.get("description", ""),
            "chain_purpose": chain.get("purpose", ""),
            "total_steps": self.topo_sorter.count_all_steps(steps),
            "exec_order": exec_order,
            "all_skill_names": all_skill_names,
            "generated_at": datetime.now().isoformat(),
        }

        # 检测未注册的调度（v1.26.0）
        sched = chain.get("schedule")
        if sched and not sched.get("registered", False):
            plan["unregistered_schedule"] = sched

        # 生成 AI 指令
        plan["ai_instructions"] = InstructionGenerator().generate(plan)
        
        return plan
    
    def _collect_all_skill_names(self, steps):
        """递归收集所有技能名称"""
        names = []
        for step in steps:
            if step.get("type", "skill") == "skill":
                sn = step.get("skill_name", "")
                if sn:
                    names.append(sn)
            loop = step.get("loop", {})
            if loop:
                for sub in loop.get("steps", []):
                    names.extend(self._collect_all_skill_names([sub]))
            branch = step.get("branch", {})
            if branch:
                for sub in branch.get("if_steps", []):
                    names.extend(self._collect_all_skill_names([sub]))
                for sub in branch.get("else_steps", []):
                    names.extend(self._collect_all_skill_names([sub]))
        return names
    
    def _topo_sort_steps(self, steps):
        """对顶层步骤进行拓扑排序"""
        # 简化实现：按 index 排序，同时尊重 depends_on
        step_map = {s.get("index", i + 1): s for i, s in enumerate(steps)}
        exec_order = []
        executed = set()
        remaining = dict(step_map)
        
        while remaining:
            progress = False
            for idx, step in list(remaining.items()):
                deps = step.get("depends_on", [])
                if all(d in executed for d in deps):
                    exec_order.append(step)
                    executed.add(idx)
                    del remaining[idx]
                    progress = True
            if not progress and remaining:
                idx = min(remaining.keys())
                exec_order.append(remaining[idx])
                executed.add(idx)
                del remaining[idx]
        
        return exec_order
    
    
# ============================================================
# CLIHandler - 命令行处理
# ============================================================

class CLIHandler:
    """命令行处理器"""
    
    def __init__(self, path_manager=None, config=None, validator=None):
        self.path_manager = path_manager or PathManager()
        self.config = config or Config(Path(""), Path(""))
        self.validator = validator or Validator()
    
    def load_chain(self, name):
        """加载调用链"""
        chain_dir = self.path_manager.get_chain_dir(name)
        chain_file = chain_dir / f"{name}.json"
        if not chain_file.exists():
            print(f"[错误] 调用链不存在: {name}")
            return None
        with open(chain_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def cmd_plan(self, args):
        """生成执行计划"""
        name = args.name
        chain_data = self.load_chain(name)
        if not chain_data:
            return
        
        builder = ExecutionPlanBuilder(
            chain_data,
            verbose=args.verbose if hasattr(args, "verbose") else False,
            config=self.config,
            path_manager=self.path_manager,
            validator=self.validator
        )
        plan = builder.build()
        
        if hasattr(args, "json") and args.json:
            print(json.dumps(plan, ensure_ascii=False, indent=2))
        else:
            print(plan["ai_instructions"])
        
        if hasattr(args, "output") and args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(plan["ai_instructions"])
            print(f"[已保存] {args.output}")
    
    def cmd_quick(self, args):
        """快速生成执行计划（不保存调用链）"""
        steps = json.loads(args.steps) if hasattr(args, "steps") else []
        chain_data = {
            "name": args.name or "临时链",
            "description": "快速执行",
            "purpose": "临时任务",
            "steps": steps,
        }
        builder = ExecutionPlanBuilder(chain_data, verbose=True)
        plan = builder.build()
        print(plan["ai_instructions"])
    
    def cmd_validate(self, args):
        """验证调用链"""
        name = args.name
        chain_data = self.load_chain(name)
        if not chain_data:
            return
        
        steps = chain_data.get("steps", [])
        ms = self.validator.classify_milestones(steps)
        
        print(f"调用链: {name}")
        print(f"总步骤: {len(steps)}")
        print(f"里程碑步骤: {len(ms)}")
        for m in ms:
            print(f"  - 步骤 {m['index']}: {m['reason']}")

# ============================================================
# main - 命令行入口
# ============================================================

def main():
    """主函数"""
    # 修复 Windows 控制台编码问题
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python <3.7 不支持
    
    parser = argparse.ArgumentParser(description="Chain Executor - 调用链执行引擎")
    subparsers = parser.add_subparsers(dest="command")
    
    # plan 命令
    plan_parser = subparsers.add_parser("plan", help="生成执行计划")
    plan_parser.add_argument("--name", required=True, help="调用链名称")
    plan_parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    plan_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    plan_parser.add_argument("--output", "-o", help="保存执行计划到文件")
    
    # quick 命令
    quick_parser = subparsers.add_parser("quick", help="快速生成执行计划")
    quick_parser.add_argument("--name", help="临时链名称")
    quick_parser.add_argument("--steps", required=True, help="步骤 JSON")
    
    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="验证调用链")
    validate_parser.add_argument("--name", required=True, help="调用链名称")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    handler = CLIHandler()
    
    if args.command == "plan":
        handler.cmd_plan(args)
    elif args.command == "quick":
        handler.cmd_quick(args)
    elif args.command == "validate":
        handler.cmd_validate(args)

if __name__ == "__main__":
    main()
