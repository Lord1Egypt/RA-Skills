"""chain_hook.py - 调用链流程钩子系统

在每个里程碑步骤或末尾步骤执行前，检查预期产出物是否存在。
不存在 → HOOK-BLOCK 阻断执行（与 chain_gate 一致）。
"""

import os
import sys
from pathlib import Path

# ============================================================
# 钩子检查结果
# ============================================================

class HookResult:
    """单个钩子检查结果"""
    def __init__(self, path: str, exists: bool):
        self.path = path
        self.exists = exists

    @property
    def passed(self) -> bool:
        return self.exists

    def __repr__(self) -> str:
        status = "✅" if self.exists else "❌"
        return f"  {status} {self.path}"


class CheckResult:
    """步骤的钩子检查汇总"""
    def __init__(self, step_index: int, step_name: str, results: list[HookResult]):
        self.step_index = step_index
        self.step_name = step_name
        self.results = results

    @property
    def passed(self) -> bool:
        """全部通过才算通过"""
        return len(self.results) > 0 and all(r.passed for r in self.results)

    def print_report(self) -> None:
        """打印钩子检查报告"""
        print(f"\n[HOOK] 步骤 {self.step_index}「{self.step_name}」检查:")
        for r in self.results:
            print(f"  {r}")
        if self.passed:
            print(f"[HOOK] {self.step_index} 全部通过 ✅")
        else:
            print(f"[HOOK] {self.step_index} 预期产出缺失 ❌")

    def print_block(self) -> None:
        """打印 HOOK-BLOCK 信息"""
        print(f"\n{'='*55}")
        print(f"  HOOK-BLOCK [HARD]")
        print(f"  步骤 {self.step_index}「{self.step_name}」检查点未通过")
        for r in self.results:
            if not r.passed:
                print(f"    缺失: {r.path}")
        print(f"{'='*55}")
        print(f"  → 请确保前置步骤已正确执行并产出预期文件后重试")
        print()


# ============================================================
# 钩子执行
# ============================================================

def check_step(step: dict, base_dir: str | Path = None) -> CheckResult | None:
    """检查一个步骤的钩子。
    
    步骤定义中需包含 hook 字段：
    {
        "hook": {
            "expects": ["path/to/file1", "path/to/file2"]
        }
    }
    
    路径解释：
    - 相对路径 → 相对于 base_dir（默认 CWD 或技能数据目录）
    - 绝对路径 → 直接使用
    
    Returns:
        None: 步骤没有钩子
        CheckResult: 钩子检查结果
    """
    hook = step.get("hook") if isinstance(step, dict) else None
    if not hook or not isinstance(hook, dict):
        return None
    
    expects = hook.get("expects", [])
    if not expects:
        return None
    
    if base_dir is None:
        base_dir = Path.cwd()
    base_dir = Path(base_dir)
    
    results = []
    for p in expects:
        p_str = str(p)
        if os.path.isabs(p_str):
            full_path = Path(p_str)
        else:
            full_path = base_dir / p_str
        exists = full_path.exists()
        results.append(HookResult(p_str, exists))
    
    step_index = step.get("index", 0)
    step_name = step.get("step_name", "")
    return CheckResult(step_index, step_name, results)


def check_chain(steps: list[dict], base_dir: str | Path = None) -> list[CheckResult]:
    """检查整条链所有需要钩子的步骤。
    
    在以下步骤上挂载钩子：
    1. 标记了 is_milestone=true 的步骤
    2. 最后一步（末尾步骤）
    
    Returns:
        所有有 hook 且需要检查的步骤的结果列表
    """
    if not steps:
        return []
    
    results = []
    for i, step in enumerate(steps):
        is_last = (i == len(steps) - 1)
        fm = step.get("failure_mode", {}) if isinstance(step, dict) else {}
        is_milestone = fm.get("is_milestone", False) if isinstance(fm, dict) else False
        
        hook = step.get("hook") if isinstance(step, dict) else None
        expects = hook.get("expects", []) if isinstance(hook, dict) else []
        
        if (is_milestone or is_last) and expects:
            cr = check_step(step, base_dir)
            if cr is not None:
                results.append(cr)
    
    return results


# ============================================================
# CLI 入口
# ============================================================

def cmd_check(args):
    """检查指定链的挂钩结果"""
    chain_name = args.name
    # 从数据目录加载链
    from .chain_manager import ChainManager
    mgr = ChainManager()
    chain = mgr.load_chain(chain_name)
    if not chain:
        print(f"调用链 '{chain_name}' 未找到")
        return
    
    steps = chain.get("steps", [])
    results = check_chain(steps)
    
    if not results:
        print(f"[HOOK] 调用链 '{chain_name}' 无流程钩子配置")
        return
    
    all_passed = True
    for cr in results:
        cr.print_report()
        if not cr.passed:
            all_passed = False
    
    print(f"\n[HOOK] 检查完成: {'全部通过 ✅' if all_passed else '存在阻断项 ❌'}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chain Hook - 流程钩子检查")
    subparsers = parser.add_subparsers(dest="command")
    
    check_parser = subparsers.add_parser("check", help="检查链的流程钩子")
    check_parser.add_argument("--name", required=True, help="调用链名称")
    
    args = parser.parse_args()
    
    if args.command == "check":
        cmd_check(args)
    else:
        parser.print_help()
