#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球系统 — 回归 / 冒烟测试 (Regression & Smoke Test)

设计目标: 在**不联网、不生成完整报告、不污染生产状态**的前提下,
对核心管线做一次"快而狠"的回归体检, 抓出改动后可能静默引入的破坏:

  1) 全量模块可导入  —— 抓出 `import re` 缺失 / 语法错误 / 模块级未定义名
                        (历史上第21项 AST 闸门抓过的那类事故)
  2) AST 未定义名网关 —— 复用 check_undefined_names.py, 退出码断言
  3) 9 项过滤器单测   —— passes_filters 已知 in/out 用例, 抓逻辑回退
  4) 穷举组合数确定性 —— exhaustive_combos() 重算数 == 缓存 ssq_valid_combos.json
                        数(抓 9 过滤器或缓存任一方漂移)
  5) 端到端预测生成   —— 用离线历史数据跑通 generate_predictions, 断言 5 组结构
                        合法(前6后复式范围正确 / 过 9 过滤器 / 互不相同)

任何一项失败 -> 进程退出码 1(供 build_dist.py / CI 作为回归闸门)。

零网络依赖: 仅读取本地 ssq_history.json / ssq_valid_combos.json /
ssq_expert_picks.json。预测生成阶段在临时目录隔离, 不写回生产状态文件。
"""
import os
import sys
import json
import glob
import shutil
import tempfile
import contextlib
import subprocess
import py_compile

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

PY = sys.executable

# 需要离线喂给预测生成的本地数据(只读, 不修改)
# 双色球规则: 红球1-33选6, 蓝球1-16选1(复式多码); 预测端到端只需历史+合法组合+中奖统计。
# expert_picks(专家抓取, 包内可选不捆绑) / power_baseline(回测基线元数据) / data_source(数据源元数据)
# 均为可选: 缺失时跳过断言, 不阻断回归网(与 healthcheck 优雅跳过可选数据保持一致)。
REQUIRED_DATA = [
    "ssq_history.json",
    "ssq_valid_combos.json",
    "ssq_winner_stats.json",
]
OPTIONAL_DATA = [
    "ssq_expert_picks.json",
    "ssq_power_baseline.json",
    "ssq_data_source.json",
]

failures = []
checks_run = 0


def record(name, ok, detail=""):
    global checks_run
    checks_run += 1
    mark = "✅" if ok else "❌"
    try:
        print(f"  {mark} [{checks_run:02d}] {name}" + (f"  -> {detail}" if detail else ""))
    except Exception:
        # stdout 偶发被关(某些模块 import 副作用), 不因此中断测试
        pass
    if not ok:
        failures.append((name, detail))


# ============================================================
# 1) 全量模块编译 (抓语法错误 / import 解析失败)
#    —— 用 py_compile 而非 import, 避免 ssq_cross_validate 等模块
#       在 import 时执行模块级主逻辑(污染 stdout / 副作用)。
#    —— 运行期未定义名(如漏 import re)由第 2 项 AST 网关专门抓。
# ============================================================
def test_compile():
    print("\n[1] 全量模块编译 (py_compile, 抓语法/import 解析错误)")
    files = sorted(glob.glob(os.path.join(ROOT, "*.py")))
    # 排除自身与一次性探查脚本
    skip = {"ssq_smoke_test.py", "_inspect_schema.py"}
    files = [f for f in files if os.path.basename(f) not in skip]
    bad = []
    for fp in files:
        try:
            py_compile.compile(fp, doraise=True)
        except py_compile.PyCompileError as e:
            bad.append((os.path.basename(fp), str(e).strip().splitlines()[-1]))
    if bad:
        for name, msg in bad:
            record(f"compile {name}", False, msg)
    else:
        record(f"全部 {len(files)} 个 .py 编译通过", True)


# ============================================================
# 2) AST 未定义名网关
# ============================================================
def test_ast_gate():
    print("\n[2] AST 未定义名网关 (check_undefined_names.py)")
    gate = os.path.join(ROOT, "check_undefined_names.py")
    if not os.path.exists(gate):
        record("AST 网关脚本存在", False, "check_undefined_names.py 缺失")
        return
    try:
        r = subprocess.run([PY, gate], cwd=ROOT,
                            capture_output=True, text=True, timeout=120,
                            encoding="utf-8", errors="replace")
        ok = r.returncode == 0
        record("AST 网关返回 0", ok,
               (r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[:120]))
    except Exception as e:
        record("AST 网关执行", False, f"{type(e).__name__}: {e}")


# ============================================================
# 3) 9 项过滤器单测
# ============================================================
def test_filters():
    print("\n[3] passes_filters 单测 (9 项过滤器逻辑)")
    try:
        import ssq_auto
    except Exception as e:
        record("导入 ssq_auto", False, str(e))
        return
    # 已知合法组合(取自 ssq_valid_combos.json 样本)
    record("合法组合过 9 过滤器",
           ssq_auto.passes_filters([1, 2, 18, 28, 31]) is True,
           "预期 True")
    # 全奇数 -> odd_count=5 不在 [2,3]
    record("全奇数被拒 (奇偶过滤)",
           ssq_auto.passes_filters([1, 3, 5, 7, 9]) is False,
           "预期 False")
    # 和值过低 -> sum=15 < 80
    record("和值过低被拒 (和值过滤)",
           ssq_auto.passes_filters([1, 2, 3, 4, 5]) is False,
           "预期 False")
    # 重号超过 2 个 -> 第9项过滤
    record("重号>2 被拒 (重号过滤)",
           ssq_auto.passes_filters([1, 2, 3, 4, 5], prev_front=[1, 2, 3, 4, 5]) is False,
           "预期 False")
    # 连号组过多: 1,2,3,4,5 连续 -> consecutive_groups 应为 1(整组一段)
    # 故意构造两组连号: 1,2, 4,5, 7 -> 两组连号 -> >1 应被拒
    record("连号组>1 被拒 (连号过滤)",
           ssq_auto.passes_filters([1, 2, 4, 5, 7]) is False,
           "预期 False")


# ============================================================
# 4) 穷举组合数确定性
# ============================================================
def test_exhaustive_determinism():
    print("\n[4] exhaustive_combos() 重算 == 缓存 (9 过滤器漂移闸门)")
    try:
        import ssq_auto
        vc_path = os.path.join(ROOT, "ssq_valid_combos.json")
        if not os.path.exists(vc_path):
            record("缓存文件存在", False, "ssq_valid_combos.json 缺失")
            return
        cached = json.load(open(vc_path, encoding="utf-8"))
        got = ssq_auto.exhaustive_combos()
        ok = (len(got) == len(cached))
        record("穷举数 == 缓存数", ok,
               f"重算={len(got):,}  缓存={len(cached):,}")
    except Exception as e:
        record("穷举重算", False, f"{type(e).__name__}: {e}")


# ============================================================
# 5) 端到端预测生成 (临时目录隔离)
# ============================================================
def test_end_to_end_predict():
    print("\n[5] generate_predictions 端到端 (离线数据, 临时目录隔离)")
    try:
        import ssq_auto
    except Exception as e:
        record("导入 ssq_auto", False, str(e))
        return

    # 准备离线数据(只读, 复制到临时目录以隔离写入)
    missing_req = [n for n in REQUIRED_DATA if not os.path.exists(os.path.join(ROOT, n))]
    if missing_req:
        record("离线数据齐全", False, f"缺失必需文件: {missing_req}")
        return

    # 可选数据缺失 → 跳过对应断言(不阻断), 与 healthcheck 优雅跳过一致
    missing_opt = [n for n in OPTIONAL_DATA if not os.path.exists(os.path.join(ROOT, n))]
    if missing_opt:
        print(f"  · 跳过: 可选数据缺失(不影响预测端到端), 缺失={missing_opt}")

    draws = json.load(open(os.path.join(ROOT, "ssq_history.json"), encoding="utf-8"))
    valid_combos = json.load(open(os.path.join(ROOT, "ssq_valid_combos.json"), encoding="utf-8"))
    # 与生产 ssq_auto.main() 完全一致: 转成 (expert, front, back) 元组列表
    # expert_picks 为可选(包内不捆绑专家抓取数据): 缺失则降级为 [] (cross_validate/healthcheck 同逻辑)
    ep_path = os.path.join(ROOT, "ssq_expert_picks.json")
    if os.path.exists(ep_path):
        ep_data = json.load(open(ep_path, encoding="utf-8"))
        expert_picks = [(e["expert"], e["front"], e.get("back", []))
                        for e in ep_data.get("experts", [])]
    else:
        expert_picks = []

    # 数据基本健全性
    if not (isinstance(draws, list) and len(draws) >= 100):
        record("历史数据量充足", False, f"仅 {len(draws)} 期")
        return
    if not (isinstance(valid_combos, list) and len(valid_combos) > 1000):
        record("合法组合缓存充足", False, f"仅 {len(valid_combos)} 个")
        return

    td = tempfile.mkdtemp(prefix="ssq_smoke_")
    try:
        for n in REQUIRED_DATA:
            shutil.copy(os.path.join(ROOT, n), os.path.join(td, n))
        old_cwd = os.getcwd()
        os.chdir(td)
        try:
            # 计算模型(纯内存, 离线)
            models = ssq_auto.compute_models(draws)
            # 抑制冗长打印
            with contextlib.redirect_stdout(open(os.devnull, "w", encoding="utf-8")):
                groups, dantuo = ssq_auto.generate_predictions(
                    draws, models, valid_combos, expert_picks)
        finally:
            os.chdir(old_cwd)

        # 结构断言
        record("返回 5 组推荐", isinstance(groups, list) and len(groups) == 5,
               f"len(groups)={len(groups) if isinstance(groups, list) else 'N/A'}")

        if isinstance(groups, list) and len(groups) == 5:
            all_ok = True
            seen = set()
            bad = []
            for gi, g in enumerate(groups):
                f = g.get("front"); b = g.get("back")
                if not (isinstance(f, list) and len(f) == 6 and len(set(f)) == 6
                        and all(isinstance(x, int) and 1 <= x <= 33 for x in f)):
                    all_ok = False; bad.append(f"组{gi+1}红球非法:{f}"); continue
                # 双色球蓝球为复式(多码, 本系统取3码), 范围 1..16 互不相同
                if not (isinstance(b, list) and 3 <= len(b) <= 16 and len(set(b)) == len(b)
                        and all(isinstance(x, int) and 1 <= x <= 16 for x in b)):
                    all_ok = False; bad.append(f"组{gi+1}蓝球非法:{b}"); continue
                if not ssq_auto.passes_filters(f):
                    all_ok = False; bad.append(f"组{gi+1}未过9过滤器:{f}")
                seen.add(ssq_auto._combo_str(f, b))
            record("每组前6后复式合法且过过滤器", all_ok,
                   ("; ".join(bad[:3]) if bad else "5 组全部合法"))
            record("5 组互不相同 (跨期唯一性闸门)", len(seen) == 5,
                   f"去重后 {len(seen)} 组")

        # 胆拖结构最小断言
        if isinstance(dantuo, dict) and dantuo.get("standard"):
            std = dantuo["standard"]
            ok_struct = all(k in std for k in ("dan", "tuo", "back"))
            record("胆拖方案结构完整", ok_struct,
                   "dan/tuo/back 齐备" if ok_struct else f"缺键: {[k for k in ('dan','tuo','back') if k not in std]}")
        else:
            record("胆拖方案(可选)", True, "本数据下走降级路径, 不强制")
    except Exception as e:
        record("端到端预测生成", False, f"{type(e).__name__}: {e}")
    finally:
        shutil.rmtree(td, ignore_errors=True)


def main():
    # 控制台编码自适应(Windows GBK 下打印 emoji 会抛 UnicodeEncodeError)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    print("=" * 64)
    print("  双色球系统 — 回归 / 冒烟测试")
    print(f"  时间: {__import__('datetime').datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"  根目录: {ROOT}")
    print("=" * 64)

    test_compile()
    test_ast_gate()
    test_filters()
    test_exhaustive_determinism()
    test_end_to_end_predict()

    print("\n" + "=" * 64)
    if failures:
        print(f"  ❌ 冒烟测试失败 {len(failures)}/{checks_run} 项:")
        for n, d in failures:
            print(f"     - {n}  {d}")
        print("  ⛔ 存在回归, 请勿交付!")
        return 1
    print(f"  ✅ 全部 {checks_run} 项通过, 核心管线健康 (回归安全网有效)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
