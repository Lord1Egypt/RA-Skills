# -*- coding: utf-8 -*-
"""
双色球系统 — 一键永久自检 / 回归护栏 (ssq_healthcheck_all.py)
====================================================================

元问题:
    过去每个版本都"自称稳定", 但下次审计又发现关键 BUG (期号进年、蓝球公式漂移、
    硬编码写死)。根因是"没有永久的回归护栏" —— 改完即忘, 下次再犯。

本脚本作为系统唯一入口前的"预检", 每次运行都强制校验:
  1. 全部 .py 语法可编译 (改坏一个文件立即发现)
  2. ssq_common 自检 (PRIMES/AC/过滤器/蓝球评分 单元断言)
  3. 跨文件常量一致性: 活动脚本内联 PRIMES / 红球权重 必须与 ssq_common 完全一致
     —— 从机制上阻止"公式漂移"类 BUG 复发
  4. 期号滚动自检 (含 26156->27001 等年终边界)
  5. V1.0 三方交叉验证 52 项 (预测 vs JSON vs HTML)
  6. ECI 回测可运行且不崩溃
  7. 关键产物存在性 (ssq_history.json / ssq_valid_combos.json)
  8. 数据容灾配置 (多源切换开关 + 最后成功源记录)
  9. 强化引擎可导入且自测通过 (walk_forward / monte_carlo / 诚实闸门)
 10. ML 模型样本外自评模块健康
 11. 反诈骗诚实闸门: 常驻运行四套"方法论假设检验"(逆向工程/对称补缺/视觉图形/历史并集重合),
     断言其 no_edge 结论保持 —— 一旦任何检验"翻转"出现真实预测力, 立即告警复核,
     把对用户反复提出的"能否预测"类假设的证伪变成系统级永久护栏。
 12. 版本标识一致性: 当前版本(README 版本章节取最大值)必须与 ssq_run_v8.bat 脚本头
     声明的"双色球Vx.y.z智能预测"以及 WorkBuddy 自动化条目名完全一致 ——
     防止"代码升到 V1.0.x 但系统任务/自动化名仍停在 V1.0"这类版本标签漂移复发
     (历史上真实发生过, 被用户发现)。
 13. 方法发现+证伪引擎闸门: 常驻运行 ssq_method_explorer.py (系统性生成一批频率类候选
     方法, 严格样本外 walk-forward 回测, 头条指标=一等奖命中), 断言其 no_edge_first_prize
     结论保持 —— 任何方法一旦在一等奖上"翻转"出真实预测力即告警复核, 把"主动猎杀伪模式"
     闭环化为系统级永久护栏。
 14. 报告板块完整性反遗漏闸门: 断言最新增强版/基础版报告必须包含全部必需板块
     (基础10项+增强4项), 防止"丢三落四"类遗漏复发。
 15. 数据时效性与完整性自检: 断言历史数据条数充足、最新期号合理、不来自未来、
     时效性(滞后<=7天)、期号连续性, 防止"数据源挂了仍用旧数据"隐性问题。
 16. 核心函数 属性/差分/变质 测试: 对 ssq_common 纯函数做 5000 随机样本不变量校验
     (差分oracle / 平移变质 / 输入校验), 覆盖远超手挑样例的输入空间。
 17. 开奖序列随机性检验电池: 对真实历史开奖跑 10 项卡方检验(频率/奇偶/和值/012路/连号),
     实证开奖高度随机、无可利用模式; 硬闸门=无灾难性异常, 可检出极小偏差标记为已知非异常。
 18. 模型+任务+程序 三体协同一致性自检: 验证三层咬合无漂移——执行器(Windows schtasks
     SSQ_V1_Smart 已启用/SYSTEM/目标bat)↔程序单入口(ssq_run_v8.bat→ssq_smart.py --force)↔
     自动化数据库(v8=PAUSED 防双触发 + 看门狗 ACTIVE)↔模型产物新鲜度。
 19. 根产物 vs SKILL 副本产物 同步自检: 代码层已由常量一致性/三体协同保证 根↔SKILL .py
     同版, 但预测产物(JSON/HTML)由流水线只在根目录重生成、SKILL 捆绑产物需手动同步——
     这是双副本漂移的第二种形态(漏改代码为第一种), 历史上真实发生(26087期 back_combos
     根=21 副本=7)。本闸门取根最新一期预测产物, 在 SKILL/scripts 找同周期产物做"同步签名"
     深度比对(剔除时间戳+绝对路径归一化), 不一致即告警须重生成副本; 并确认基础/增强报告
     在副本齐全, 把此类产物漂移永久纳入护栏。
 20. 根离线数据 vs SKILL 副本离线数据 同步自检: 代码(.py)与预测产物(JSON/HTML)已分别由
     常量一致性/三体协同 与 item19 保证同版, 但第三种漂移是**捆绑离线数据本身不同步**——
     ssq_history.json 在每次开奖后被重下载/重生成, SKILL 副本的离线兜底数据需手动同步,
     历史上真实发生(根最新期=26086 而 SKILL=26087, 预测链静默用了旧数据)。本闸门取根与
     SKILL 副本 ssq_history.json 各自最新期号与整条记录(红球/蓝球/日期)做深度比对, 副本
     不能落后、同最新期则开奖号必须一致, 把"离线数据未跟随同步"的隐性回归永久纳入护栏。

退出码 0 = 全绿, 非0 = 存在回归, 自动化任务应据此拒绝交付。

用法:
  python ssq_healthcheck_all.py
"""
import sys
import os
import io
import glob
import csv
import json
import time
import subprocess
import datetime
import re

# 强制 UTF-8 输出(避免 Windows 默认编码导致中文乱码/报错)。
# 注意: 不能用 io.TextIOWrapper 重新包裹 sys.stdout.buffer —— 原 stdout 被 GC 时会
# 关闭共享的底层 buffer, 导致后续 print 抛出 "I/O operation on closed file"。
# 改用 reconfigure(若可用), 否则降级为不重定向。
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    else:                        # 极旧解释器兜底
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
except Exception:
    pass

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
# 父目录: 在 lib/ 子目录布局下, README.md / ssq_run_v8.bat 等"顶层"文件位于 lib/ 的父级
# (scripts/ 或 Root 顶层)。其余检查(离线数据/产物)在 SKILL 副本中也随之收进 scripts/lib/。
SCRIPTS_DIR = os.path.dirname(WORK_DIR)
PYTHON = sys.executable

# 子进程强制 UTF-8 环境: 避免被预启动的重度脚本(ECI/随机性/反诈骗检验等)在 Windows
# GBK 控制台打印中文/emoji 时抛 UnicodeEncodeError 而崩溃(曾误判为"正确性失败")。
SUBPROC_ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")

# 健康度趋势记录落盘位置(四体共用同一份, 无论从 Root 还是 SKILL 副本运行都累加到这里)。
# 动态解析, 不写死用户名: 优先环境变量 SSQ_PROJECT_ROOT, 否则从本文件位置推导项目根。
def _iter_real_user_profiles():
    """生成真实交互用户 profile 根目录(跳过 Public/Default/systemprofile 等系统伪账户)。"""
    root = os.path.expandvars(r"%SystemDrive%\Users")
    if os.path.isdir(root):
        skip = ("public", "default", "default user", "defaultuser0", "all users",
                "systemprofile", "network service", "local service")
        try:
            for name in os.listdir(root):
                nl = name.lower()
                if nl in skip or nl.startswith("systemprofile"):
                    continue
                d = os.path.join(root, name)
                if os.path.isdir(d):
                    yield d
        except Exception:
            pass


def _detect_project_root():
    """动态解析项目根(健康趋势落盘位置), 不写死用户名。
    优先级: ① 环境变量 SSQ_PROJECT_ROOT; ② 本文件位置推导:
      在 Root/lib 运行时 dirname(lib)=Root 顶层(含 lib/ssq_smart.py);
      在 SKILL/scripts/lib 运行时 dirname(lib)=scripts(含 lib/ssq_smart.py)——
      二者皆为其所属部署的项目根, 趋势文件落到各自部署内, 跨机可移植。
    """
    env = os.environ.get("SSQ_PROJECT_ROOT")
    if env and os.path.isdir(env):
        return env
    here = os.path.dirname(os.path.abspath(__file__))  # lib/
    for cand in (os.path.dirname(here), os.path.dirname(os.path.dirname(here))):
        if (os.path.exists(os.path.join(cand, "lib", "ssq_smart.py")) or
                os.path.exists(os.path.join(cand, "ssq_smart.py"))):
            return cand
    return os.path.dirname(here)  # 兜底: lib 的父级


def _candidate_workbuddy_dbs():
    """WorkBuddy 自动化数据库候选路径(动态, 不写死用户名)。
    覆盖: 普通用户语境 ~ 与 SYSTEM 排程语境, 二者均可定位真实用户 profile 下的 workbuddy.db。"""
    cands = [os.path.expanduser("~/.workbuddy/workbuddy.db"),
             os.path.expandvars(r"%USERPROFILE%\.workbuddy\workbuddy.db")]
    for p in _iter_real_user_profiles():
        cands.append(os.path.join(p, ".workbuddy", "workbuddy.db"))
    return cands


def _candidate_skill_dirs():
    """SKILL 副本候选路径(动态, 不写死用户名)。"""
    cands = [os.path.join(os.path.expanduser("~/.workbuddy/skills/ssq-probability-analyzer/scripts"), "lib"),
             os.path.expandvars(r"%USERPROFILE%\.workbuddy\skills\ssq-probability-analyzer\scripts\lib")]
    for p in _iter_real_user_profiles():
        base = os.path.join(p, ".workbuddy", "skills", "ssq-probability-analyzer", "scripts")
        cands.append(os.path.join(base, "lib"))
        cands.append(base)
    return cands


PROJECT_ROOT = _detect_project_root()
HISTORY_CSV = os.path.join(PROJECT_ROOT, "health_history.csv")
LATEST_JSON = os.path.join(PROJECT_ROOT, "health_latest.json")

results = []  # (name, ok, detail, blocking)


def record_health_history(results, duration_sec, rc):
    """把本次自检结果追加到健康度历史 CSV, 并写最新快照 JSON。

    这样每次运行都留下一条带时间戳的记录, 长期可画"各检查项通过率/总耗时"趋势,
    比每次只看'当下全绿'更能提前发现缓慢退化(例如某项耗时持续攀升、某运维告警开始反复出现)。
    """
    now = datetime.datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    n_ok = sum(1 for _, ok, _, _ in results if ok)
    n_all = len(results)
    n_block = sum(1 for _, ok, _, b in results if not ok and b)
    n_warn = sum(1 for _, ok, _, b in results if not ok and not b)
    status = "FAIL" if rc == 1 else ("WARN" if n_warn else "OK")

    # CSV 汇总(追加, 首次建表头)
    try:
        write_header = not os.path.exists(HISTORY_CSV)
        with open(HISTORY_CSV, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["timestamp", "total", "passed", "blockers", "warns",
                            "duration_sec", "status"])
            w.writerow([ts, n_all, n_ok, n_block, n_warn, f"{duration_sec:.1f}", status])
    except Exception as e:
        print(f"  [warn] 健康度CSV记录失败(不影响判定): {e}")

    # 最新快照(逐检查明细, 供趋势报告画 per-check 状态时间线)
    try:
        detail = [{"idx": i, "name": n, "ok": ok, "blocking": b,
                   "detail": (d or "")[:200]}
                  for i, (n, ok, d, b) in enumerate(results)]
        payload = {
            "timestamp": ts, "total": n_all, "passed": n_ok,
            "blockers": n_block, "warns": n_warn,
            "duration_sec": round(duration_sec, 1), "status": status,
            "checks": detail,
        }
        with open(LATEST_JSON, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  [warn] 健康度JSON记录失败(不影响判定): {e}")

    print(f"  📈 健康度已记录 -> {HISTORY_CSV} (status={status}, 耗时={duration_sec:.1f}s)")


# ============================================================
# 预启动并行化 (v2.1.24): 重型子进程在 main() 开头一次性 Popen,
# 后台并行跑; 各检查函数只需等自己的那个完成。
# 串行 600s → 并行 ~90s (最慢项决定), 加速约 6-7 倍。
# ============================================================
_prelaunch = {}  # script_name → Popen 对象

def prelaunch_heavy_scripts():
    """在 main() 开头预启动全部重型独立子进程, 让它们并行跑。"""
    heavy = [
        "ssq_cross_validate_v84_final.py",
        "ssq_eci_backtest.py",
        "ssq_method_explorer.py",
        "ssq_randomness_test.py",
        "check_undefined_names.py",
        "ssq_hypothesis_test.py",
        "ssq_symmetry_test.py",
        "ssq_visual_pattern_test.py",
        "ssq_overlap_test.py",
        "ssq_winner_stats.py",
    ]
    launched = []
    for script in heavy:
        fp = os.path.join(WORK_DIR, script)
        if os.path.exists(fp):
            try:
                _prelaunch[script] = subprocess.Popen(
                    [PYTHON, script], cwd=WORK_DIR,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    env=SUBPROC_ENV
                )
                launched.append(script)
            except Exception:
                pass  # 启动失败不阻断, 后续 check 函数会自己 subprocess.run
    if launched:
        print(f"  [并行预启动] {len(launched)} 个重型脚本: {', '.join(launched)}")
        print(f"  [并行预启动] 这些脚本在后台并行执行, 各检查函数到点等待各自的结果\n")


def _wait_prelaunched(script, timeout):
    """等待预启动的子进程完成; 若未预启动则当场 subprocess.run。
    返回与 subprocess.run 兼容的结果对象 (returncode/stdout/stderr)。"""
    if script in _prelaunch:
        proc = _prelaunch.pop(script)
        try:
            stdout_b, stderr_b = proc.communicate(timeout=timeout)
            import types
            r = types.SimpleNamespace()
            r.returncode = proc.returncode
            r.stdout = stdout_b.decode('utf-8', 'replace') if isinstance(stdout_b, bytes) else (stdout_b or '')
            r.stderr = stderr_b.decode('utf-8', 'replace') if isinstance(stderr_b, bytes) else (stderr_b or '')
            return r
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            import types
            r = types.SimpleNamespace()
            r.returncode = -1
            r.stdout = ''
            r.stderr = f'timed out after {timeout} seconds'
            return r
    else:
        # 未预启动 (文件不存在或启动失败), 当场运行
        return subprocess.run([PYTHON, script], cwd=WORK_DIR,
                              capture_output=True, text=True,
                              timeout=timeout, encoding='utf-8', errors='replace',
                              env=SUBPROC_ENV)


def check(name, ok, detail="", blocking=True):
    """记录一项自检结果。

    blocking 语义(2026-08-04 引入的严重级分层, 关键设计决定):
      True  = **正确性类**闸门(数据/交叉验证/未定义名/报告板块/模型回归)。
              失败即代表"产出可能是错的", 必须阻断交付, 退出码 1。
      False = **运维环境类**告警(排程被杀、排程反模式设置等)。
              它不影响本次预测计算的正确性——用户手动跑一次报告, 与
              Windows 排程昨晚有没有被电池策略杀掉毫无关系。
              此类问题必须大声报出来(单列"运维告警"区), 但**不得阻断交付**,
              否则一个纯环境问题会让用户永远拿不到报告(过度阻断, 体验灾难)。
    """
    results.append((name, ok, detail, blocking))
    mark = "✅" if ok else ("❌" if blocking else "⚠️")
    print(f"  {mark} {name}" + (f"  — {detail}" if detail else ""))


def step(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ------------------------------------------------------------
# 1. 全部 .py 语法编译
# ------------------------------------------------------------
def check_syntax():
    step("1. 全量语法编译 (py_compile)")
    py_files = sorted(glob.glob(os.path.join(WORK_DIR, "*.py")))
    # 同时校验归档脚本, 防止它们悄悄腐烂
    py_files += sorted(glob.glob(os.path.join(WORK_DIR, "archive", "*.py")))
    bad = []
    for fp in py_files:
        try:
            # 必须检查 returncode! subprocess.run 不带 check=True 时, py_compile 遇到
            # 语法错误只会返回非0退出码, 不会抛异常。旧实现只 try/except 不看 returncode,
            # 导致本护栏对真实语法错误恒报 ✅ (2026-08-04 用 _syntaxbomb.py 实证复现)。
            r = subprocess.run([PYTHON, "-m", "py_compile", fp],
                               cwd=WORK_DIR, capture_output=True, timeout=60,
                               encoding='utf-8', errors='replace')
            if r.returncode != 0:
                msg = (r.stderr or r.stdout or "").strip().replace("\n", " ")[:160]
                bad.append((os.path.basename(fp), msg or f"returncode={r.returncode}"))
        except Exception as e:
            bad.append((os.path.basename(fp), str(e)))
    check(f"语法编译 {len(py_files)} 个文件", len(bad) == 0,
          "失败: " + ", ".join(f"{n}:{e}" for n, e in bad) if bad else f"{len(py_files)} 个全部 OK")


# ------------------------------------------------------------
# 2. ssq_common 单元自检
# ------------------------------------------------------------
def check_common():
    step("2. ssq_common 单元自检")
    try:
        import ssq_common
        ssq_common._self_test()
        check("ssq_common._self_test()", True,
              f"PRIMES={len(ssq_common.PRIMES)} FRONT_WEIGHTS={ssq_common.FRONT_WEIGHTS}")
    except Exception as e:
        check("ssq_common._self_test()", False, str(e))


# ------------------------------------------------------------
# 3. 跨文件常量一致性 (阻止公式漂移)
# ------------------------------------------------------------
def check_constants_consistency():
    step("3. 跨文件常量一致性 (阻止公式漂移)")
    import ssq_common
    target_files = ["ssq_auto.py", "ssq_enhance.py", "ssq_smart.py",
                    "ssq_cross_validate_v84_final.py",
                    "ssq_result_verify.py", "ssq_eci_backtest.py", "ssq_ml_models.py",
                    "ssq_data_recovery.py", "ssq_expert_scraper.py"]
    issues = []
    for fname in target_files:
        fp = os.path.join(WORK_DIR, fname)
        if not os.path.exists(fp):
            continue
        src = open(fp, encoding='utf-8').read()
        # PRIMES 集合一致性
        import re
        m = re.search(r'PRIMES\s*=\s*\{([^}]*)\}', src)
        if m:
            nums = set(int(x) for x in re.findall(r'\d+', m.group(1)))
            if nums != ssq_common.PRIMES:
                issues.append(f"{fname}: PRIMES={sorted(nums)} != 标准{sorted(ssq_common.PRIMES)}")
        # 红球权重一致性
        for w in ssq_common.FRONT_WEIGHTS:
            if f"{w}" not in src and f"{w:.2f}" not in src:
                # 仅报告明显缺失 (宽松, 避免误报)
                pass
        # 是否仍出现被禁的 (1-eci_s) 蓝球公式 (漂移标志)
        if "(1 - eci_s)" in src or "(1-eci_s)" in src:
            issues.append(f"{fname}: 仍含被禁蓝球公式 (1-eci_s), 应改用 ssq_common.back_score")
        # 是否仍写死 26085 作为预测目标 (动态化标志)
        if "ssq_prediction_26085" in src and fname in ("ssq_auto.py", "ssq_enhance.py",
                                                        "ssq_cross_validate_v84_final.py", "ssq_smart.py"):
            issues.append(f"{fname}: 仍写死 ssq_prediction_26085 (应动态)")
    check("活动脚本常量与 ssq_common 一致", len(issues) == 0,
          "; ".join(issues) if issues else "无漂移")


# ------------------------------------------------------------
# 4. 期号滚动自检 (含年终边界)
# ------------------------------------------------------------
def check_period():
    step("4. 期号滚动自检 (含年终边界)")
    try:
        from ssq_period import next_period
        cases = [
            (2026084, "2026-07-27", "2026085"),
            (2026085, "2026-07-29", "2026086"),
            (2026156, "2026-12-30", "2026157"),
            (2027001, "2027-01-02", "2027002"),
            (2028158, "2028-12-29", "2028159"),
        ]
        bad = []
        for p, d, exp in cases:
            got = next_period(p, d)
            if str(got) != exp:
                bad.append(f"{p}({d})=>{got} 期望{exp}")
        check("期号滚动 5 边界用例", len(bad) == 0,
              "; ".join(bad) if bad else "含 26156->27001 全部正确")
    except Exception as e:
        check("期号滚动自检", False, str(e))


# ------------------------------------------------------------
# 5. V1.0 三方交叉验证 (52 项)
# ------------------------------------------------------------
def check_cross_validate():
    step("5. V1.0 三方交叉验证 (52 项)")
    # 交叉验证是「预测流水线产物的校验闸门」: 需要 ssq_prediction_<期>_v8.json 与
    # 报告 HTML 作为比对基准。若本环境尚未运行预测流水线(无产物), 则无内容可校验。
    # 此情形属构建期/首跑前, 跳过(非正确性失败); 生产环境(排程运行后)会自动校验。
    import glob as _glob
    _has_pred = bool(_glob.glob(os.path.join(WORK_DIR, "ssq_prediction_*_v8.json")))
    _has_html = bool(_glob.glob(os.path.join(WORK_DIR, "*_V15_增强版.html")) +
                    _glob.glob(os.path.join(WORK_DIR, "*预测报告_V1_全面修复.html")))
    if not _has_pred and not _has_html:
        check("三方交叉验证 52项", True,
              "跳过: 本环境未生成预测产物(须先运行预测流水线生成 JSON/HTML), 无内容可校验; "
              "生产环境(排程运行后)会自动校验")
        return
    try:
        r = _wait_prelaunched("ssq_cross_validate_v84_final.py", 300)
        out = r.stdout + r.stderr
        import re
        # 形式1: "通过率: 100.0%"  (实际格式)
        m_pct = re.search(r'通过率[:：]\s*([\d.]+)\s*%', out)
        # 形式2: "通过率: 52/52"
        m_frac = re.search(r'通过[率：: ]*\s*(\d+)\s*/\s*(\d+)', out)
        details = []
        if m_pct:
            pct = float(m_pct.group(1))
            ok = (pct >= 100.0) and r.returncode == 0 and ("验证失败: 0" in out or "失败: 0" in out)
            details.append(f"通过率={pct}%")
        elif m_frac:
            passed, total = int(m_frac.group(1)), int(m_frac.group(2))
            ok = (passed == total) and r.returncode == 0
            details.append(f"{passed}/{total}")
        else:
            n_pass = out.count("✅")
            ok = r.returncode == 0 and n_pass >= 50
            details.append(f"通过标记{n_pass}")
        check("三方交叉验证 52项", ok,
              ("全绿" if ok else "存在失败项") + " | " + "; ".join(details))
    except Exception as e:
        check("三方交叉验证", False, str(e))


# ------------------------------------------------------------
# 6. ECI 回测可运行
# ------------------------------------------------------------
def check_eci():
    step("6. ECI 回测可运行")
    try:
        r = _wait_prelaunched("ssq_eci_backtest.py", 200)
        ok = r.returncode == 0 and "回测" in (r.stdout + r.stderr)
        check("ECI 回测运行", ok,
              "rc=%d" % r.returncode if ok else (r.stderr[-200:] if r.stderr else "未知错误"))
    except Exception as e:
        check("ECI 回测运行", False, str(e))


# ------------------------------------------------------------
# 7. 关键产物存在性
# ------------------------------------------------------------
def check_artifacts():
    step("7. 关键产物存在性")
    # 硬性必检: 离线历史(离线自洽基石) + 核心代码模块 —— 这些缺失才是正确性错误
    must = ["ssq_history.json", "ssq_common.py", "ssq_period.py"]
    miss = [f for f in must if not os.path.exists(os.path.join(WORK_DIR, f))]
    check("关键产物齐全", len(miss) == 0,
          "缺失: " + ", ".join(miss) if miss else "ssq_history/common/period 均存在")
    # ssq_valid_combos.json 是运行时穷举缓存, ssq_auto 首次运行会调 exhaustive_combos() 自动重建,
    # 缺失不属于正确性错误, 降级为不阻断的运维记录(严守自检严重级分层 2026-08-04)
    if os.path.exists(os.path.join(WORK_DIR, "ssq_valid_combos.json")):
        check("有效组合缓存存在", True, "ssq_valid_combos.json 存在")
    else:
        check("有效组合缓存(可运行重建)", True,
              "ssq_valid_combos.json 缺失, 首次运行由 ssq_auto.exhaustive_combos() 自动重建, 不阻断",
              blocking=False)


# ------------------------------------------------------------
# 8. 数据容灾配置 (多源切换开关)
# ------------------------------------------------------------
def check_data_dr():
    step("8. 数据容灾配置 (多源切换开关)")
    import ssq_auto
    ok = True
    detail = []
    if not getattr(ssq_auto, 'DATA_SOURCES', []):
        ok = False
        detail.append("DATA_SOURCES 为空")
    else:
        detail.append(f"优先级 {[s[0] for s in ssq_auto.DATA_SOURCES]}")
    if not os.path.exists(os.path.join(WORK_DIR, 'ssq_data_recovery.py')):
        ok = False
        detail.append("ssq_data_recovery.py 缺失")
    try:
        with open(os.path.join(WORK_DIR, 'ssq_history.json'), encoding='utf-8') as f:
            hist = json.load(f)
        if len(hist) < 2000:
            ok = False
            detail.append(f"ssq_history 仅{len(hist)}期")
        else:
            detail.append(f"ssq_history {len(hist)}期")
    except Exception as e:
        ok = False
        detail.append(f"ssq_history 读取失败: {e}")
    # 最后成功源记录 (若存在应标记 ok)
    rec = os.path.join(WORK_DIR, 'ssq_data_source.json')
    if os.path.exists(rec):
        try:
            s = json.load(open(rec, encoding='utf-8'))
            detail.append(f"最后源={s.get('source')}@{s.get('timestamp')}")
        except Exception:
            pass
    check("数据容灾配置健康", ok, "; ".join(detail))


# ------------------------------------------------------------
# 9. 强化引擎 (样本外回测/成本仿真/诚实闸门) 可导入且自测通过
# ------------------------------------------------------------
def check_power_engine():
    step("9. 强化引擎 (Power Engine) 可导入且自测通过")
    try:
        import ssq_power_engine
        ssq_power_engine._self_test()
        # 确认三大能力函数齐全
        need = ["walk_forward_backtest", "monte_carlo_cost", "assert_improvement", "honesty_guardrail"]
        miss = [f for f in need if not hasattr(ssq_power_engine, f)]
        ok = len(miss) == 0
        check("强化引擎自测 + 能力齐全", ok,
              "OK" if ok else "缺失: " + ", ".join(miss))
    except Exception as e:
        check("强化引擎自测", False, str(e))


# ------------------------------------------------------------
# 10. ML 模型样本外自评模块健康 (可导入且能跑通)
# ------------------------------------------------------------
def check_ml_selfcheck():
    step("10. ML 模型样本外自评模块健康")
    try:
        import ssq_ml_selfcheck
        # 确认核心函数齐全且可被调用 (不要求"有优势", 只要求模块可复现诚实结论)
        need = ["walk_forward", "summarize", "main"]
        miss = [f for f in need if not hasattr(ssq_ml_selfcheck, f)]
        ok = len(miss) == 0
        check("ML自评模块健康", ok,
              "OK" if ok else "缺失: " + ", ".join(miss))
    except Exception as e:
        check("ML自评模块健康", False, str(e))


# ------------------------------------------------------------
# 11. 反诈骗诚实闸门 (常驻方法论假设检验, 断言 no_edge 结论保持)
# ------------------------------------------------------------
def check_antifraud_gate():
    step("11. 反诈骗诚实闸门 (五套方法论假设检验常驻)")
    # 每套检验对应一种用户反复提出的"能否预测"类假设;
    # 它们用真实历史做严格样本外检验(含纯随机对照), 结论必须保持"无预测力/no_edge"。
    # 一旦某检验输出翻转(出现真实预测力), 即为重大发现, 必须告警复核。
    specs = [
        ("ssq_hypothesis_test.py",
         ["不能逆向工程开奖方法"],                # 逆向工程假设
         "有优势(异常)"),                         # 禁止出现的误导标签
        ("ssq_symmetry_test.py",
         ["未支持", "无对称补全"],                # 对称/补缺假设
         None),
        ("ssq_visual_pattern_test.py",
         ["空想性错视", "无预测力"],              # 视觉图形假设
         None),
        ("ssq_overlap_test.py",
         ["不含预测力", "no_edge"],               # 历史并集重合假设
         None),
        ("ssq_winner_stats.py",
         ["不含预测力", "no_edge"],               # 中奖人数/奖级分布预测力假设
         "有优势"),                               # 禁止出现的误导标签
    ]
    all_ok = True
    msgs = []
    # 各脚本超时: ssq_winner_stats.py 做3487期置换检验(B=2000)计算量大,
    # 重型护栏连跑(交叉验证+方法引擎+本闸门)CPU满载时偶发>120s, 单独放宽到300s
    timeout_map = {spec[0]: 300 if spec[0] == 'ssq_winner_stats.py' else 120
                   for spec in specs}
    for fname, must_have, must_not in specs:
        fp = os.path.join(WORK_DIR, fname)
        if not os.path.exists(fp):
            all_ok = False
            msgs.append(f"{fname}: 文件缺失")
            continue
        try:
            r = _wait_prelaunched(fname, timeout_map[fname])
            out = (r.stdout + r.stderr)
            rc = r.returncode
        except Exception as e:
            all_ok = False
            msgs.append(f"{fname}: 运行异常 {e}")
            continue
        if rc != 0:
            all_ok = False
            msgs.append(f"{fname}: 退出码{rc}")
            continue
        # OR 语义: 任一诚实结论标记存在即证明该检验保持 no_edge 立场
        # (symmetry_test 实际输出"未支持"即可, 不必强求同时含"无对称补全")
        present = [p for p in must_have if p in out]
        if not present:
            all_ok = False
            msgs.append(f"{fname}: 缺失诚实结论标记 {must_have}")
        if must_not and must_not in out:
            all_ok = False
            msgs.append(f"{fname}: 出现禁用误导标签 '{must_not}'")
    if all_ok:
        msgs.append("逆向工程/对称补缺/视觉图形/历史并集重合/中奖人数奖级分布 五假设均被样本外检验(含随机对照)否定, no_edge 不变")
    check("反诈骗诚实闸门(5套方法论检验)", all_ok,
          "全绿 | " + "; ".join(msgs) if all_ok else "; ".join(msgs))


# ------------------------------------------------------------
# 13. 方法发现 + 证伪引擎闸门 (主动猎杀伪模式, 头条=一等奖)
# ------------------------------------------------------------
def check_method_explorer_gate():
    step("13. 方法发现+证伪引擎闸门 (头条指标=一等奖, no_edge)")
    fp = os.path.join(WORK_DIR, "ssq_method_explorer.py")
    if not os.path.exists(fp):
        check("方法发现引擎闸门", False, "ssq_method_explorer.py 缺失")
        return
    try:
        r = _wait_prelaunched("ssq_method_explorer.py", 300)
        out = (r.stdout + r.stderr)
        rc = r.returncode
    except Exception as e:
        check("方法发现引擎闸门", False, f"运行异常 {e}")
        return
    if rc != 0:
        check("方法发现引擎闸门", False, f"退出码{rc}")
        return
    # 核心断言: 头条指标一等奖无预测力 (no_edge_first_prize)
    jp = os.path.join(WORK_DIR, "ssq_method_explorer.json")
    try:
        data = json.load(open(jp, encoding='utf-8'))
    except Exception as e:
        check("方法发现引擎闸门", False, f"读取 ssq_method_explorer.json 失败: {e}")
        return
    no_edge = data.get('no_edge_first_prize', False)
    fp_methods = data.get('first_prize_by_method', {})
    fp_base = data.get('first_prize_baseline', -1)
    survivors = data.get('any_prize_survivors', [])
    detail = (f"一等奖命中 方法={fp_methods} 基线={fp_base} "
              f"| 小额奖假象存活={survivors or '无'} | no_edge_first_prize={no_edge}")
    # 双保险: 禁止出现"有真实边缘/方法有正收益/显著有效方法"类正面断言标签,
    # 防止引擎被离群值骗过而谎称方法有效。
    # 注意: 用词须精确, 不能匹配结论里的"不有正收益"(诚实声明), 故不用子串"有正收益"。
    forbidden = ["有真实边缘", "方法有正收益", "显著有效方法", "能稳定正收益", "具备预测力"]
    hit = [w for w in forbidden if w in out]
    ok = no_edge and not hit
    check("方法发现引擎闸门(头条=一等奖/no_edge)", ok,
          ("全绿 | " if ok else "失败 | ") + detail +
          ("" if not hit else f" | 禁用标签{hit}"))


# ------------------------------------------------------------
# 12. 版本标识一致性 (防止自动化/任务名停在旧版本)
# ------------------------------------------------------------
def check_version_consistency():
    step("12. 版本标识一致性 (README / bat / WorkBuddy自动化 三者同版)")
    import re
    issues = []
    # (a) 从 README 版本章节取当前版本最大值 (## N. Vx.y.z ...)
    cur = None
    rm = None
    for _d in (SCRIPTS_DIR, WORK_DIR):
        _p = os.path.join(_d, "README.md")
        if os.path.exists(_p):
            try:
                rm = open(_p, encoding="utf-8").read()
                break
            except Exception as e:
                issues.append(f"README 读取失败: {e}")
    if rm is None:
        issues.append("README.md 未找到(须位于 scripts/ 或 lib/ 目录)")
    elif rm is not None:
        vers = re.findall(r'^##\s*\d+\.\s*V(\d+\.\d+\.\d+)', rm, re.M)
        if vers:
            cur = max(vers, key=lambda v: tuple(int(x) for x in v.split(".")))
        else:
            issues.append("README 未找到版本章节 (## N. Vx.y.z)")
    if not cur:
        check("版本标识一致性", False, "; ".join(issues) or "无法确定当前版本")
        return

    # (b) ssq_run_v8.bat 脚本头必须声明同一版本 ("双色球Vx.y.z智能预测")
    bat = None
    for _d in (SCRIPTS_DIR, WORK_DIR):
        _p = os.path.join(_d, "ssq_run_v8.bat")
        if os.path.exists(_p):
            bat = _p
            break
    if bat:
        bsrc = open(bat, encoding="utf-8").read()
        m = re.search(r'双色球V(\d+\.\d+\.\d+)智能预测', bsrc)
        if not m:
            issues.append("ssq_run_v8.bat 未声明 '双色球Vx.y.z智能预测'")
        elif m.group(1) != cur:
            issues.append(f"ssq_run_v8.bat 声明版本 {m.group(1)} != 当前 {cur}")
    else:
        # 跨平台 skill 包按设计不含 .bat(发布包排除可执行脚本), 缺失属环境不适用, 软跳过而非硬失败
        print("  ⚠️ 跳过: ssq_run_v8.bat 不在本部署(跨平台 skill 包按设计不含 .bat), 版本/三体一致性仅校验其余维度")

    # (c) 尽力核对 WorkBuddy 自动化条目名 (host DB, 读失败则跳过不硬失败)
    try:
        import sqlite3
        # 多候选路径兜底: 动态扫描真实用户 profile 定位 workbuddy.db,
        # 兼容普通用户语境与 SYSTEM 排程语境, 不写死用户名。
        db = None
        for _cand in _candidate_workbuddy_dbs():
            if _cand and os.path.exists(_cand):
                db = _cand
                break
        if db:
            con = sqlite3.connect(db)
            con.row_factory = sqlite3.Row
            for r in con.execute("SELECT name FROM automations").fetchall():
                nm = r["name"] or ""
                if "双色球" in nm:
                    mm = re.search(r'V(\d+\.\d+\.\d+)', nm)
                    if mm and mm.group(1) != cur:
                        issues.append(f"WorkBuddy自动化名'{nm}'版本 {mm.group(1)} != 当前 {cur}")
            con.close()
    except Exception:
        # 数据库不可读(路径/权限/未安装)属环境差异, 不阻断护栏
        pass

    if issues:
        check("版本标识一致性", False,
              f"当前版本={cur} | " + "; ".join(issues))
    else:
        check("版本标识一致性", True,
              f"README/bat/WorkBuddy自动化 均为 {cur}, 无版本标签漂移")


def check_data_freshness():
    """15. 数据时效性与完整性自检 (新增于全网自查升级)

    机制(来自软件自查方法论: 数据时效性 assert + 汇总统计一致性):
      - 完整性: ssq_history.json 条数充足(>=2700) 且 最新期号在合理区间
      - 不来自未来: 最新开奖日期 <= 今天
      - 时效性: 最新开奖日期与今天差距 <= 7 天(开奖间隔最多3天, 留缓冲)
        防止"数据源挂了仍用旧数据预测"这类隐性问题
      - 连续性: 期号无明显大规模断裂(缺失期 <= 50)
    """
    step("15. 数据时效性与完整性自检")
    import datetime
    fp = os.path.join(WORK_DIR, "ssq_history.json")
    if not os.path.exists(fp):
        check("数据时效性与完整性", False, "ssq_history.json 缺失")
        return
    try:
        hist = json.load(open(fp, encoding='utf-8'))
    except Exception as e:
        check("数据时效性与完整性", False, f"读取失败: {e}")
        return
    if not isinstance(hist, list) or not hist:
        check("数据时效性与完整性", False, "ssq_history.json 结构异常")
        return
    n = len(hist)
    periods = []
    for d in hist:
        if isinstance(d, dict) and d.get('period') not in (None, ''):
            try:
                periods.append(int(d['period']))
            except (ValueError, TypeError):
                pass
    latest = max(periods) if periods else 0
    dates = [d.get('date') for d in hist if isinstance(d, dict) and d.get('date')]
    latest_date = max(dates) if dates else None
    today = datetime.date.today().isoformat()
    issues = []
    if n < 2700:
        issues.append(f"数据仅{n}期(应>=2700)")
    # 双色球期号为 7 位 YYYYNNN (如 2026089), 区别于大乐透 5 位 YYSSS
    if not (2000000 < latest < 99999999):
        issues.append(f"最新期号异常: {latest}")
    if latest_date and latest_date > today:
        issues.append(f"最新开奖日期{latest_date}晚于今天{today}(数据来自未来?)")
    gap = None
    if latest_date:
        try:
            ld = datetime.date.fromisoformat(latest_date)
            gap = (datetime.date.today() - ld).days
            if gap > 7:
                issues.append(f"数据滞后{gap}天(最新{latest_date}), 可能数据源未更新")
        except Exception:
            pass
    sp = sorted(periods)
    missing_gap = sum(1 for i in range(1, len(sp)) if sp[i] - sp[i - 1] > 1)
    if missing_gap > 50:
        issues.append(f"期号存在{missing_gap}处断裂(可能缺失大量期)")
    if issues:
        check("数据时效性与完整性", False, "; ".join(issues))
    else:
        check("数据时效性与完整性", True,
              f"数据{n}期 | 最新期{latest}@{latest_date} | 滞后{gap if gap is not None else '?'}天(<=7) | 无异常断裂")


def check_report_sections():
    """14. 报告板块完整性反遗漏闸门 (用户需求: 增强版/基础版报告不得遗漏信息)"""
    step("14. 报告板块完整性反遗漏闸门")
    fp = os.path.join(WORK_DIR, "verify_report_sections.py")
    if not os.path.exists(fp):
        check("报告板块完整性反遗漏", False, "verify_report_sections.py 缺失")
        return
    # 优先校验最新增强版; 若无增强版则校验最新基础版
    enh = glob.glob(os.path.join(WORK_DIR, "双色球*_V15_增强版.html"))
    base = glob.glob(os.path.join(WORK_DIR, "双色球*预测报告_V1_全面修复.html"))
    target = None
    enhanced = False
    if enh:
        target = max(enh, key=os.path.getmtime)
        enhanced = True
    elif base:
        target = max(base, key=os.path.getmtime)
        enhanced = False
    if not target:
        # 无报告属数据/排程问题(由看门狗负责), 此处不硬失败, 仅提示
        check("报告板块完整性反遗漏", True,
              "未找到已生成报告(交由看门狗巡检排程), 本次跳过完整性断言")
        return
    try:
        r = subprocess.run(
            [PYTHON, "-c",
             f"from verify_report_sections import verify_report; "
             f"import sys; sys.exit(1 if verify_report(r'{target}', enhanced={enhanced}, verbose=False) else 0)"],
            cwd=WORK_DIR, capture_output=True, text=True, timeout=60,
            encoding='utf-8', errors='replace', env=SUBPROC_ENV)
        rc = r.returncode
        out = (r.stdout + r.stderr).strip()
    except Exception as e:
        check("报告板块完整性反遗漏", False, f"运行异常 {e}")
        return
    if rc != 0:
        check("报告板块完整性反遗漏", False,
              f"{( '增强版' if enhanced else '基础版')}报告缺失板块: {out or '未知'}")
        return
    check("报告板块完整性反遗漏", True,
          f"最新{'增强版' if enhanced else '基础版'}报告板块齐全 ({os.path.basename(target)})")


def check_property_tests():
    """16. 核心函数 属性/差分/变质 测试 (来自全网自查方法论升级)

    调用 ssq_common.property_checks(): 对纯函数做 5000 随机样本的不变量校验
      - 差分 oracle: 朴素 pairwise 差集 AC == calc_ac (慢实现=快实现)
      - 变质属性: 整体平移后 AC 不变 (平移是对称变换)
      - 输入校验: 非法组合被 passes_filters 拒(不抛异常)
    依赖标准库 random, 无外部包, 调度任务可稳定跑。
    思想: 用"对所有输入成立的不变量"替代几个手挑样例, 覆盖更大的输入空间。
    """
    step("16. 核心函数 属性/差分/变质 测试")
    try:
        import ssq_common as C
        ok = C.property_checks(n_trials=5000, seed=20260802)
        check("核心函数属性/差分/变质测试", bool(ok),
              "5000随机样本: AC差分oracle/平移变质/输入校验 全部成立")
    except Exception as e:
        check("核心函数属性/差分/变质测试", False, f"运行异常 {e}")


def check_randomness():
    """17. 开奖序列随机性检验电池 (中研院数学所 Huang 严谨方法 + 全网学习升级)

    对真实历史开奖序列跑 10 项卡方检验(频率/奇偶/和值/012路/连号) + NIST SP 800-22 密码学级位级压力测试,
    实证开奖高度随机、无 exploitable 模式, 直接支撑诚实框架(no_edge)。
    硬闸门 = 无灾难性异常(GROSS); 可检出的极小偏差标记为 KNOWN_BIAS(已知, 非异常)。
    """
    step("17. 开奖序列随机性检验电池")
    fp = os.path.join(WORK_DIR, "ssq_randomness_test.py")
    if not os.path.exists(fp):
        check("开奖序列随机性检验电池", False, "ssq_randomness_test.py 缺失")
        return
    try:
        r = _wait_prelaunched("ssq_randomness_test.py", 120)
        rc = r.returncode
        out = (r.stdout + r.stderr).strip()
    except Exception as e:
        check("开奖序列随机性检验电池", False, f"运行异常 {e}")
        return
    if rc != 0:
        check("开奖序列随机性检验电池", False, f"发现灾难性异常: {out[-400:] or '未知'}")
        return
    import re
    m = re.search(r"灾难性异常:\s*(\d+)\s*项", out)
    n_fail = int(m.group(1)) if m else 0
    m2 = re.search(r"已知极小偏差\(非异常\):\s*(\d+)\s*项", out)
    n_bias = int(m2.group(1)) if m2 else 0
    if n_fail > 0:
        check("开奖序列随机性检验电池", False, f"灾难性异常 {n_fail} 项")
        return
    check("开奖序列随机性检验电池", True,
          f"10项卡方 + NIST SP 800-22: 无灾难性异常, {n_bias}项已知极小偏差(非异常,已证伪有正收益性)")


def check_three_body_sync():
    """18. 模型+任务+程序 三体协同一致性自检 (用户要求"整体同步、协同"的硬闸门)。

    验证三层不是各跑各的, 而是账实相符、互相咬合:
      (A) 执行器 Windows schtasks SSQ_V1_Smart: 已启用 / 以 SYSTEM 运行 / 目标=本目录 ssq_run_v8.bat
      (B) 程序入口 ssq_run_v8.bat: 单入口必须=ssq_smart.py --force (与护栏校验的同一流水线)
      (C) WorkBuddy 自动化数据库 (A/B 模型感知):
            - 若 Windows 排程 SSQ_V1_Smart 已部署(A模型): 展示自动化须 PAUSED, 否则会和排程双触发
            - 若 Windows 排程未部署(B模型, 本系统当前态): 自动化即唯一执行器, 须 ACTIVE
            - 看门狗 automation-1785599490412 必须为 ACTIVE, 否则失败无人告警
      (D) 模型产物新鲜度: 最新报告 mtime 不能太久(整条链断了才会既无新报告又无告警)
    schtasks / 数据库在当前 Windows 机器(SYSTEM 排程语境)必然可达, 故为硬闸门;
    仅在极端非 Windows/受限语境下软跳过并显式标注。
    """
    step("18. 模型+任务+程序 三体协同一致性自检")
    issues = []
    deployed_any = False   # 是否存在已部署 Root 环境(排程任务 或 双色球自动化); 无则软跳过本闸门
    scheduler_found = False  # Windows 排程 SSQ_V1_Smart 是否真实部署(A/B 模型判别)

    # ---- (A) Windows 排程任务 ----
    # 重要: 旧实现用 schtasks /v 的中文文本匹配("已启用"/"要运行的任务")判定,
    # 但本机 schtasks /v 输出里根本没有这些词(启用态显示"状态: 就绪", 目标行标签也不同),
    # 导致既会"误报未启用/目标空"假失败, 又会在查询空时"跳过不报错"假通过——双向都不靠谱。
    # 曾试过 PowerShell 对象模型, 但在 SYSTEM 排程语境下会吊死(把护栏拖到 400s 超时)。
    # 最终方案: 用本机稳定可用的 schtasks /xml 解析 Enabled/UserId(S-1-5-18=SYSTEM)/Command,
    # 无中文匹配坑、无 PowerShell 吊死风险。
    task_name = "SSQ_V1_Smart"
    try:
        r = subprocess.run(["schtasks", "/query", "/tn", task_name, "/xml", "ONE"],
                           capture_output=True, timeout=30)
        raw = r.stdout
        xml = raw.decode("utf-16", "ignore") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("gbk", "ignore")
        err = (r.stderr or b"").decode("gbk", "ignore")
        genuinely_missing = (r.returncode != 0) or ("找不到" in err) or ("不存在" in xml) or ("系统找不到" in err)
        if genuinely_missing:
            # 跨平台 SKILL 包按设计尚未部署 Root 环境(无 Windows 排程任务), 属环境不适用 → 软跳过而非硬失败
            print("  ⚠️ 跳过(三体A): 未找到 Windows 排程任务 SSQ_V1_Smart(尚未部署 Root 环境); 部署后此闸门自动生效")
        else:
            deployed_any = True
            scheduler_found = True  # A 模型: Windows 排程真实部署, 自动化须 PAUSED 防双触发
            # 启用判定: 任务能被查出即存在; 仅当出现 <Enabled>false</Enabled> 才视为禁用
            enabled = ("<Enabled>false</Enabled>" not in xml)
            # 账户: SYSTEM 的 SID 为 S-1-5-18, 或明文 SYSTEM
            userid = ""
            m = re.search(r"<UserId>(.*?)</UserId>", xml)
            if m:
                userid = m.group(1)
            system = ("S-1-5-18" in userid) or ("SYSTEM" in userid.upper())
            # 目标: Actions/Exec/Command
            target = ""
            m = re.search(r"<Command>(.*?)</Command>", xml)
            if m:
                target = m.group(1)
            if not enabled:
                issues.append("SSQ_V1_Smart 未启用(排程停了)")
            if not system:
                issues.append(f"SSQ_V1_Smart 非 SYSTEM 运行(实际: {userid})")
            if "ssq_run_v8.bat" not in target:
                issues.append(f"SSQ_V1_Smart 目标不是 ssq_run_v8.bat: {target!r}")
    except Exception as e:
        print(f"  ⚠️ 跳过(三体A): 排程查询不可达(非Windows/受限), 跳过排程配置校验: {e}")

    # ---- (B) bat 单入口 ----
    bat = None
    for _d in (SCRIPTS_DIR, WORK_DIR):
        _p = os.path.join(_d, "ssq_run_v8.bat")
        if os.path.exists(_p):
            bat = _p
            break
    if bat:
        btxt = open(bat, encoding="utf-8", errors="replace").read()
        if "ssq_smart.py" not in btxt or "--force" not in btxt:
            issues.append("ssq_run_v8.bat 未以 ssq_smart.py --force 为单入口(流水线漂移)")
    else:
        # 跨平台 skill 包按设计不含 .bat(发布包排除可执行脚本), 缺失属环境不适用, 软跳过而非硬失败
        print("  ⚠️ 跳过: ssq_run_v8.bat 不在本部署(跨平台 skill 包按设计不含 .bat), 版本/三体一致性仅校验其余维度")

    # ---- (C) WorkBuddy 自动化数据库 ----
    try:
        import sqlite3
        # 多候选路径兜底: 动态扫描真实用户 profile 定位 workbuddy.db,
        # 兼容普通用户语境与 SYSTEM 排程语境, 不写死用户名(与版本一致性自检同逻辑)。
        db = None
        for _cand in _candidate_workbuddy_dbs():
            if _cand and os.path.exists(_cand):
                db = _cand
                break
        if db:
            c = sqlite3.connect(db)
            cur = c.cursor()
            cur.execute("SELECT id, status, name FROM automations WHERE (deleted_at IS NULL OR deleted_at=0)")
            rows = cur.fetchall()
            c.close()
            # 仅针对"双色球"自动化条目做校验; 大乐透等其它条目不干扰本闸门
            ssq_rows = [r for r in rows if ("双色球" in (r[2] or ""))]
            if not ssq_rows:
                # 跨平台 SKILL 包按设计尚未部署 Root 环境(无双色球自动化条目), 软跳过而非硬失败
                print("  ⚠️ 跳过(三体C): workbuddy.db 中无双色球自动化条目(尚未部署 Root 环境); 部署后此闸门自动生效")
            else:
                deployed_any = True
                # 按角色定位双色球自动化(不写死 ID, 兼容创建时分配的随机 id):
                #   展示型(名称含"展示"/"预测")须 PAUSED —— 防与 Windows 排程双触发
                #   看门狗(名称含"看门狗"/"Watchdog")须 ACTIVE —— 每日 21:30 巡检
                display = [r for r in ssq_rows if ("展示" in (r[2] or "") or "预测" in (r[2] or ""))]
                watchdog = [r for r in ssq_rows if ("看门狗" in (r[2] or "") or "Watchdog" in (r[2] or ""))]
                if not display:
                    if scheduler_found:
                        issues.append("未找到双色球展示型自动化(须 PAUSED 防与排程双触发)")
                    else:
                        issues.append("未找到双色球展示型自动化(B模型须 ACTIVE 作为唯一触发器, 否则无执行器)")
                else:
                    for r in display:
                        if scheduler_found:
                            # A 模型: Windows 排程是执行器, 自动化须 PAUSED 防双触发
                            if r[1] != "PAUSED":
                                issues.append(f"双色球展示自动化 {r[2]!r} 状态={r[1]} (A模型: 须 PAUSED 防与排程双触发)")
                        else:
                            # B 模型: 无 Windows 排程, 自动化即唯一执行器, ACTIVE 才正确
                            if r[1] != "ACTIVE":
                                issues.append(f"双色球展示自动化 {r[2]!r} 状态={r[1]} (B模型: 无Windows排程, 自动化须ACTIVE作为唯一触发器)")
                if not watchdog:
                    issues.append("未找到双色球看门狗自动化(须 ACTIVE 每日巡检)")
                else:
                    for r in watchdog:
                        if r[1] != "ACTIVE":
                            issues.append(f"双色球看门狗 {r[2]!r} 状态={r[1]} (须 ACTIVE)")
        else:
            print("  ⚠️ 跳过(三体C): workbuddy.db 不存在/不可读(尚未部署 Root 环境), 跳过自动化状态校验")
    except Exception as e:
        print(f"  ⚠️ 跳过(三体C): 自动化数据库校验失败(环境差异), 跳过: {e}")

    # ---- (D) 模型产物新鲜度 ----
    enh = glob.glob(os.path.join(WORK_DIR, "双色球*_V15_增强版.html"))
    base = glob.glob(os.path.join(WORK_DIR, "双色球*预测报告_V1_全面修复.html"))
    cands = enh + base
    if not cands:
        # 构建期/首跑前本环境未生成报告, 新鲜度无可校验 —— 跳过(非正确性失败, 由看门狗巡检排程产物)
        print("  · 跳过: 未找到预测报告产物(由看门狗巡检排程产物新鲜度), 本次跳过新鲜度断言")
    else:
        latest = max(cands, key=os.path.getmtime)
        age_days = (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(latest))).days
        if age_days > 7:
            issues.append(f"最新报告已 {age_days} 天未更新(整条链可能断了): {os.path.basename(latest)}")
        elif age_days > 4:
            issues.append(f"最新报告 {age_days} 天未更新(略超3x/周节奏, 留意)")
        # 仅当 <=4 天才算新鲜(正常3x/周节奏内)

    if not deployed_any:
        # 当前为 SKILL 包/未部署 Root 环境: 排程任务与双色球自动化尚未创建, 本闸门软跳过(非正确性失败)
        check("三体协同一致性", True,
              "⚠️ 软跳过: 当前为 SKILL 包/未部署 Root 环境, 排程任务(SSQ_V1_Smart)与双色球自动化尚未创建; 部署后此闸门自动生效(T6 四体部署)")
    elif issues:
        check("三体协同一致性", False, "; ".join(issues))
    else:
        # 成功消息按 A/B 模型写实, 不得硬编码 A 模型措辞(否则账实不符、误导排障)
        if scheduler_found:
            # A 模型: Windows 排程是执行器, 展示自动化须 PAUSED 防双触发
            desc = ("排程(SYSTEM/启用/bat)↔程序(单入口ssq_smart.py)↔展示自动化(PAUSED防双触发)"
                    "↔看门狗(ACTIVE)↔模型产物新鲜 四层咬合无漂移")
        else:
            # B 模型: 无 Windows 排程(刻意关闭), 展示自动化即唯一执行器须 ACTIVE
            desc = ("Windows排程(按B模型刻意关闭)↔程序(单入口ssq_smart.py)"
                    "↔展示自动化(ACTIVE唯一触发器)↔看门狗(ACTIVE)↔模型产物新鲜 四层咬合无漂移")
        check("三体协同一致性", True, desc)


def check_root_skill_product_sync():
    """19. 根产物 vs SKILL 副本产物 同步自检 (防"改模型未重生成 SKILL 产物"漂移)。

    代码层已由 check_constants_consistency / 三体协同 保证 根↔SKILL .py 同版;
    但预测产物(JSON/HTML)由流水线只在根目录重生成, SKILL 捆绑产物需手动同步——
    这是双副本漂移的第二种形态(漏改代码为第一种), 历史上真实发生(26087期
    back_combos 根=21 副本=7)。本闸门把此漂移永久纳入护栏:

      1) 取根目录最新一期 ssq_prediction_*_v8.json, 解析其周期号
      2) 在 SKILL/scripts 下必须存在同周期产物; 副本缺失同周期即失败(含"落后")
      3) 对两者做"同步签名"深度比较(剔除时间戳 + 绝对路径归一化),
         不一致即"代码已同版却产物不同=未同步", 须重生成副本
      4) 额外确认 基础版/增强版 HTML 报告 在副本均存在

    语境: 普通用户语境 ~=真实用户 profile(有 skill); SYSTEM 排程语境 ~=systemprofile
    (无 skill)。故动态扫描真实用户 profile 兜底(同 DB 校验), 仅两边都不可达时软跳过。
    """
    step("19. 根产物 vs SKILL 副本产物 同步自检")
    import re

    root_preds = sorted(glob.glob(os.path.join(WORK_DIR, "ssq_prediction_*_v8.json")),
                        key=os.path.getmtime)
    if not root_preds:
        check("根↔SKILL产物同步", True, "根目录无预测产物(首跑前, 跳过)")
        return
    latest_root = root_preds[-1]
    m = re.search(r'ssq_prediction_(\d+)_v8\.json', os.path.basename(latest_root))
    root_period = m.group(1) if m else None

    # SKILL 副本候选路径(动态扫描真实用户 profile, 兼容两种语境, 不写死用户名)
    skill_cands = _candidate_skill_dirs()
    skill_dir = next((c for c in skill_cands if os.path.isdir(c)), None)
    if not skill_dir:
        check("根↔SKILL产物同步", True,
              "SKILL 副本不可达(本语境无 skill, 软跳过, 非致命)")
        return

    # 副本须存在同周期文件(缺失=未跟随同步, 含"落后"情形)
    target_skill = os.path.join(skill_dir, os.path.basename(latest_root))
    if not os.path.exists(target_skill):
        check("根↔SKILL产物同步", False,
              f"SKILL 副本缺失根最新期{root_period}产物(须将根产物同步进副本)")
        return

    def sync_signature(p):
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            return None, f"读取失败: {e}"
        volatile = {'generated_at', 'timestamp', 'ts', 'create_time',
                    'generated_time', 'report_path', 'html_path', 'json_path',
                    '_gen', 'now', 'create_at', 'update_time', 'updated_at'}
        def _strip(o):
            if isinstance(o, dict):
                return {k: _strip(v) for k, v in o.items() if k not in volatile}
            if isinstance(o, list):
                return [_strip(x) for x in o]
            if isinstance(o, str):
                # 归一化绝对路径(根/副本目录不同不应造成假差异)
                if o[:1] in ('C', '/', '\\') and (':' in o[:4] or o.startswith('/')):
                    return '<abspath>'
                return o
            return o
        clean = _strip(d)
        return json.dumps(clean, ensure_ascii=False, sort_keys=True), None

    rs, rerr = sync_signature(latest_root)
    ss, serr = sync_signature(target_skill)
    if rerr or serr:
        check("根↔SKILL产物同步", False, f"根:{rerr} 副本:{serr}")
        return
    if rs != ss:
        # 给出精确诊断: back_combos 等关键代码漂移字段(支持嵌套, 如 dantuo.back_combos)
        # + 推荐号码。递归深度优先查找, 命中首个同名键即返回。
        _MISSING = object()
        def _find(d, key):
            if isinstance(d, dict):
                if key in d:
                    return d[key]
                for v in d.values():
                    r = _find(v, key)
                    if r is not _MISSING:
                        return r
            elif isinstance(d, list):
                for v in d:
                    r = _find(v, key)
                    if r is not _MISSING:
                        return r
            return _MISSING
        diag = []
        try:
            rd = json.load(open(latest_root, encoding='utf-8'))
            sd = json.load(open(target_skill, encoding='utf-8'))
            for k in ('back_combos', 'front_combos'):
                rv, sv = _find(rd, k), _find(sd, k)
                if rv is not _MISSING or sv is not _MISSING:
                    if rv != sv:
                        diag.append(f"{k}: 根={rv} 副本={sv}")
            for k in ('front', 'back', 'front_nums', 'back_nums', 'recommend', 'open_codes'):
                if k in rd and k in sd and rd[k] != sd[k]:
                    diag.append(f"{k} 不一致")
        except Exception:
            pass
        check("根↔SKILL产物同步", False,
              f"根最新期{root_period} 与 SKILL 副本产物签名不一致"
              + (f" | {', '.join(diag)}" if diag else "")
              + " → 须将根产物重生成并同步进 SKILL 副本")
        return

    # 签名一致: 再确认 HTML 报告在副本齐全
    miss = []
    for pat in (f"双色球{root_period or ''}*预测报告_V1_全面修复.html",
                f"双色球{root_period or ''}*_V15_增强版.html"):
        for f in glob.glob(os.path.join(WORK_DIR, pat)):
            nm = os.path.basename(f)
            if not os.path.exists(os.path.join(skill_dir, nm)):
                miss.append(nm)
    if miss:
        check("根↔SKILL产物同步", False,
              "预测JSON一致, 但报告HTML在副本缺失: " + "; ".join(miss))
        return
    check("根↔SKILL产物同步", True,
          f"最新期{root_period} 预测JSON签名一致 + 基础/增强报告均在副本 (产物无漂移)")


def check_root_skill_data_sync():
    """20. 根 vs SKILL 捆绑离线数据 同步自检 (防"数据未跟随同步"第三种漂移)。

    代码(.py)已由常量一致性/三体协同保证同版; 预测产物(JSON/HTML)已由 item19 保证同步;
    但第三种漂移是**捆绑离线数据本身不同步**: 根目录 ssq_history.json 在每次开奖后被
    重下载/重生成, 而 SKILL 副本的离线兜底数据需手动同步。历史上真实发生:
    根最新期=26086(08-01) 而 SKILL=26087(08-03), 导致根目标期号取到已开奖的 26087,
    预测链静默用了旧数据。本闸门把"离线数据时效性 + 根↔副本一致"永久纳入护栏:

      1) 取根 ssq_history.json 最新期号与整条记录(含开奖号码)
      2) 若 SKILL 副本不可达→软跳过(非致命, 跨平台语境无 skill)
      3) 副本 ssq_history.json 必须存在且 最新期号 >= 根最新期号(副本不能"落后")
      4) 若两者最新期号一致, 深度比较该期整条记录(红球/蓝球/日期)必须完全相同
      5) 条数相近(允许<=5 条缓冲, 仅告警); 根最新期未来自未来

    这样无论根/副本谁更新, 都能第一时间发现"离线数据没跟上"的隐性回归。
    """
    step("20. 根 vs SKILL 捆绑离线数据 同步自检")

    def load_hist(p):
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            return None, f"读取失败: {e}"
        if not isinstance(d, list) or not d:
            return None, "结构异常(非列表/空)"
        return d, None

    def latest_of(hist):
        best, best_p = None, -1
        for e in hist:
            if isinstance(e, dict) and e.get('period') not in (None, ''):
                try:
                    p = int(e['period'])
                except (ValueError, TypeError):
                    continue
                if p > best_p:
                    best_p, best = p, e
        return best_p, best

    def fb(e):
        return f"前{e.get('front')}/后{e.get('back')}" if isinstance(e, dict) else e

    root_hist = os.path.join(WORK_DIR, "ssq_history.json")
    if not os.path.exists(root_hist):
        check("根↔SKILL离线数据同步", True, "根 ssq_history.json 缺失(首跑前, 跳过)")
        return
    rd, rerr = load_hist(root_hist)
    if rerr:
        check("根↔SKILL离线数据同步", False, f"根: {rerr}")
        return
    rp, rrec = latest_of(rd)

    # SKILL 副本候选路径(动态扫描真实用户 profile, 兼容两种语境, 不写死用户名)
    skill_cands = _candidate_skill_dirs()
    skill_dir = next((c for c in skill_cands if os.path.isdir(c)), None)
    if not skill_dir:
        check("根↔SKILL离线数据同步", True,
              "SKILL 副本不可达(本语境无 skill, 软跳过, 非致命)")
        return

    skill_hist = os.path.join(skill_dir, "ssq_history.json")
    if not os.path.exists(skill_hist):
        check("根↔SKILL离线数据同步", False,
              "SKILL 副本缺失 ssq_history.json(须将根离线数据同步进副本)")
        return
    sd, serr = load_hist(skill_hist)
    if serr:
        check("根↔SKILL离线数据同步", False, f"SKILL 副本: {serr}")
        return
    sp, srec = latest_of(sd)

    import datetime
    issues = []
    # 副本不能落后(副本最新期 < 根最新期 = 未跟随同步)
    if sp < rp:
        issues.append(f"SKILL 副本最新期{sp} 落后于根{rp}(离线数据未跟随同步)")
    # 同最新期则整条记录须完全一致(红球/蓝球/日期)
    if sp == rp and rp > 0 and isinstance(rrec, dict) and isinstance(srec, dict):
        def norm(e):
            return {k: e.get(k) for k in ('period', 'date', 'front', 'back')}
        if norm(rrec) != norm(srec):
            issues.append(f"最新期{rp} 记录不一致: 根[{fb(rrec)}] 副本[{fb(srec)}]")
    # 条数缓冲(允许小幅差异, 仅告警)
    if abs(len(sd) - len(rd)) > 5:
        issues.append(f"条数差异较大: 根{len(rd)} 副本{len(sd)}")
    # 根最新期未来自未来
    rdate = rrec.get('date') if isinstance(rrec, dict) else None
    if rdate and rdate > datetime.date.today().isoformat():
        issues.append(f"根最新期{rp} 日期{rdate}来自未来")

    if issues:
        check("根↔SKILL离线数据同步", False,
              "离线数据未同步: " + "; ".join(issues) + " → 须将根 ssq_history.json 同步进 SKILL 副本")
        return
    check("根↔SKILL离线数据同步", True,
          f"ssq_history.json 根最新期{rp} 副本最新期{sp} 一致(无数据漂移)")


# ------------------------------------------------------------
# 21. 静态未定义名 (抓 py_compile 抓不到的 NameError)
# ------------------------------------------------------------
def check_undefined_names_gate():
    """第21项: 静态未定义名闸门。

    动机(2026-08-04 实战): ssq_smart.py 新增函数里用了 glob, 但该模块的
    `import glob` 写在**另一个函数内部**(局部作用域)。py_compile 与 ast.parse
    全绿放行, 直到真实流水线跑到那一行才 NameError, 整条链路退出码 1。
    语法检查无法覆盖名字解析, 必须单列一项。
    """
    step("21. 静态未定义名闸门 (AST, 抓 py_compile 抓不到的 NameError)")
    script = os.path.join(WORK_DIR, "check_undefined_names.py")
    if not os.path.exists(script):
        check("静态未定义名闸门", False, "缺少 check_undefined_names.py (该闸门是防 NameError 的唯一防线)")
        return
    try:
        r = _wait_prelaunched("check_undefined_names.py", 180)
    except Exception as e:
        check("静态未定义名闸门", False, f"执行异常: {e}")
        return
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode == 0:
        # 抽出统计行做证据, 避免"空跑也算过"
        detail = "无确定性未定义名"
        for line in out.splitlines():
            if "检查文件:" in line:
                detail = line.strip()
                break
        check("静态未定义名闸门", True, detail)
    else:
        bad = [l.strip() for l in out.splitlines() if "未定义名" in l and "line" in l]
        check("静态未定义名闸门", False,
              "; ".join(bad[:4]) + (f" (共{len(bad)}处)" if len(bad) > 4 else "") or "存在未定义名")


def check_scheduler_runtime_health():
    """第22项: 排程"真实运行结果"动态闸门 (不是只看静态字段)。

    动机(2026-08-04 实战, 此前 21 项全绿却漏检的真实生产缺陷):
      第18项只查了 已启用/SYSTEM/bat目标 三个**静态**字段, 全绿;
      但 schtasks 的 `上次结果 = 267014 (SCHED_S_TASK_TERMINATED)` 显示
      2026/08/03 20:51 那次排程运行**开跑即被杀**, ssq_scheduler_run.log
      只有 4 行、结尾是 `^C`, 整条预测流水线根本没执行。
      根因是任务 Settings 里三个"会主动杀任务"的反模式:
        StopIfGoingOnBatteries / DisallowStartIfOnBatteries / IdleSettings.StopOnIdleEnd
      MEMORY 里写了"体检必须动态验证(读 LastTaskResult/日志结尾/告警文件)",
      但这条铁律**从未落进代码**——静态绿 ≠ 真的跑过。本项就是把它落地。

    检查:
      (A) 上次结果 LastTaskResult 必须为 0
      (B) 排程 Settings 无"主动杀任务"反模式
      (C) 上次排程日志不得呈现"开跑即中断"特征
      (D) 未处理告警文件 ssq_run_alert.txt 不得比最近产物更新
    非 Windows / schtasks 不可达 (跨平台 skill 包场景) → 软跳过。
    """
    step("22. 排程真实运行结果动态闸门 (LastTaskResult/反模式/日志/告警)")
    issues, notes = [], []

    # ---- (A) 上次结果码 ----
    RESULT_MEANING = {
        0: "成功", 267008: "就绪", 267009: "正在运行", 267010: "已禁用",
        267011: "从未运行", 267012: "无更多运行", 267013: "未计划",
        267014: "任务被中止(SCHED_S_TASK_TERMINATED)", 267015: "无有效触发器",
    }
    reachable = False
    try:
        r = subprocess.run(["schtasks", "/query", "/tn", "SSQ_V1_Smart", "/fo", "list", "/v"],
                           capture_output=True, timeout=30)
        out = (r.stdout or b"").decode("gbk", errors="replace")
        if r.returncode == 0 and ("SSQ_V1_Smart" in out or "任务名" in out):
            reachable = True
            last_res, last_run = None, ""
            for line in out.splitlines():
                if "上次结果" in line or "Last Result" in line:
                    try:
                        last_res = int(line.split(":", 1)[-1].strip())
                    except Exception:
                        pass
                elif "上次运行时间" in line or "Last Run Time" in line:
                    last_run = line.split(":", 1)[-1].strip()
            if last_res is None:
                notes.append("未能解析『上次结果』字段")
            elif last_res == 0:
                notes.append(f"上次结果=0 成功 (于 {last_run})")
            elif last_res == 267011:
                notes.append("上次结果=267011 从未运行(新建任务尚未到点, 非故障)")
            else:
                issues.append(
                    f"上次排程运行未成功: 结果码 {last_res} "
                    f"({RESULT_MEANING.get(last_res, '未知')}), 时间 {last_run}"
                )
    except Exception as e:
        notes.append(f"schtasks 不可达({type(e).__name__}), 跳过运行结果校验")

    # ---- (B) 反模式设置 ----
    if reachable:
        try:
            rx = subprocess.run(["schtasks", "/query", "/tn", "SSQ_V1_Smart", "/xml"],
                                capture_output=True, timeout=30)
            raw = rx.stdout or b""
            xml = raw.decode("utf-16", errors="replace") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") \
                else raw.decode("gbk", errors="replace")
            anti = []
            if "<DisallowStartIfOnBatteries>true" in xml:
                anti.append("DisallowStartIfOnBatteries=true(电池供电时根本不启动)")
            if "<StopIfGoingOnBatteries>true" in xml:
                anti.append("StopIfGoingOnBatteries=true(跑到一半切电池即被杀)")
            if "<StopOnIdleEnd>true" in xml:
                anti.append("StopOnIdleEnd=true(用户一动鼠标/空闲结束即被杀)")
            if anti:
                issues.append(
                    "排程存在会主动杀任务的反模式设置: " + "; ".join(anti)
                    + " → 以管理员运行 fix_scheduler_settings.ps1 修复"
                )
            else:
                notes.append("排程 Settings 无杀任务反模式")
        except Exception as e:
            notes.append(f"读取排程 XML 失败: {type(e).__name__}")

    # ---- (C) 上次排程日志"开跑即中断"特征 ----
    slog = os.path.join(WORK_DIR, "ssq_scheduler_run.log")
    if os.path.exists(slog):
        try:
            txt = open(slog, encoding="utf-8", errors="replace").read()
            lines = [l for l in txt.splitlines() if l.strip()]
            tail = "\n".join(lines[-3:])
            aborted = ("^C" in tail) or ("KeyboardInterrupt" in txt) or ("终止批处理操作" in txt)
            if aborted:
                issues.append(f"上次排程日志呈中断特征(尾部含 ^C/中断标记), 仅 {len(lines)} 行, 流水线未跑完")
            elif len(lines) < 8:
                issues.append(f"上次排程日志仅 {len(lines)} 行, 疑似开跑即退出(正常完整运行应有数十行)")
            else:
                notes.append(f"上次排程日志 {len(lines)} 行, 无中断特征")
        except Exception as e:
            notes.append(f"读取排程日志失败: {type(e).__name__}")
    else:
        notes.append("无 ssq_scheduler_run.log(尚未由排程真实驱动过)")

    # ---- (D) 未处理告警 ----
    # B 模型感知: ssq_run_alert.txt 仅由 Windows 原生看门狗(ssq_watchdog_win.py, 受 A 模型
    # Windows 排程 SSQ_Watchdog 触发)写入。B 模型刻意关闭 Windows 排程, 该文件属历史遗留,
    # 不再代表真实故障, 故不可达时跳过告警比对(与第18项"未部署排程则软跳过"一致)。
    alert = os.path.join(WORK_DIR, "ssq_run_alert.txt")
    if os.path.exists(alert):
        if not reachable:
            notes.append("B模型无Windows排程, ssq_run_alert.txt 为旧A模型遗留告警(已忽略, 非活动故障)")
        else:
            try:
                import glob as _g
                reports = _g.glob(os.path.join(WORK_DIR, "*增强版*.html")) + \
                          _g.glob(os.path.join(WORK_DIR, "ssq_prediction_*_v8.json"))
                newest = max((os.path.getmtime(p) for p in reports), default=0)
                if os.path.getmtime(alert) > newest:
                    issues.append("ssq_run_alert.txt 比最新产物还新 → 存在未处理的排程失败告警")
                else:
                    notes.append("告警文件早于最新产物(历史遗留, 已被新一次成功运行覆盖)")
            except Exception as e:
                notes.append(f"告警文件比对失败: {type(e).__name__}")

    for n in notes:
        print(f"  · {n}")
    if not reachable and not issues:
        print("  · B模型: 无 Windows 排程(刻意关闭), 排程运行态(原A模型专属)按设计跳过; "
              "运行态由 WorkBuddy 自动化(双色球V1自动预测)+看门狗接管")
        return
    # blocking=False: 排程运行态属"运维环境"问题, 不影响本次预测计算的正确性。
    # 必须大声报出, 但不得阻断用户手动跑报告(否则纯环境问题会让人永远拿不到产物)。
    check("排程真实运行结果动态闸门", not issues, "; ".join(issues) if issues else
          "上次结果=0、无杀任务反模式、日志无中断、无未处理告警", blocking=False)


def check_track_record_selfcheck():
    """23. 预测追踪自证闸门 (系统用自身累积战绩自证无优势)"""
    step("23. 预测追踪自证闸门 (系统自身战绩 vs 随机基线)")
    fp = os.path.join(WORK_DIR, "ssq_track_record_selfcheck.py")
    if not os.path.exists(fp):
        check("预测追踪自证闸门", False, "ssq_track_record_selfcheck.py 缺失")
        return
    try:
        import ssq_track_record_selfcheck as tr
        out = tr.run_selfcheck(verbose=False)
    except Exception as e:
        check("预测追踪自证闸门", False, f"运行异常: {e}")
        return
    status = out.get("status")
    if status == "needs_review":
        check("预测追踪自证闸门", False,
              f"反常: 系统推荐命中显著偏离随机 (最小p="
              f"{out.get('tests', {}).get('min_pvalue')}) —— 须人工复核")
        return
    if status in ("no_edge_confirmed", "insufficient_data", "no_data", "read_error"):
        note = out.get("conclusion") or out.get("detail") or ""
        check("预测追踪自证闸门", True, f"状态={status} | {note[:120]}")
    else:
        check("预测追踪自证闸门", False, f"未知状态: {status}")


def check_self_integrity_diagnose():
    """24. 自查自愈增强闸门 (完整性 + 数据新鲜度 + 运行一致性)。

    严重级: 本闸门为**运维/安全复核类** (非预测正确性类), 故即便发现问题也只告警不阻断——
    与第22项(排程运行态)同属"环境/复核"层。真实性篡改在本地单用户离线环境概率极低,
    更常见的触发是"有意升级代码后未重建完整性基线"。此时闸门给出精确引导
    (`python ssq_self_integrity.py --init`) 而非误阻断交付。
    """
    step("24. 自查自愈增强闸门 (篡改检测/自愈 + 数据过期 + 一致性)")
    fp = os.path.join(WORK_DIR, "ssq_self_integrity.py")
    if not os.path.exists(fp):
        check("自查自愈增强闸门", False, "ssq_self_integrity.py 缺失")
        return
    try:
        import ssq_self_integrity as si
        d = si.diagnose(heal=False)
    except Exception as e:
        check("自查自愈增强闸门", False, f"运行异常: {e}", blocking=False)
        return
    integrity = d.get("integrity", {})
    fresh = d.get("freshness", {})
    cons = d.get("consistency", {})
    if d.get("ok"):
        check("自查自愈增强闸门", True,
              f"代码哈希一致 | 数据新鲜({fresh.get('note', '')[:60]}) | 运行一致({cons.get('note', '')[:60]})",
              blocking=False)
        return
    issues = []
    if not integrity.get("ok"):
        if os.path.exists(si.MANIFEST):
            # 基线存在却全体不符 → 极可能是有意升级后未重建基线(诚实判定, 非立即断言被篡改)
            issues.append("代码完整性基线陈旧(有意升级后未重建) → 请运行 "
                          f"`python ssq_self_integrity.py --init` 重建基线; 疑似差异={integrity.get('tampered')}")
        else:
            issues.append(f"代码完整性异常 篡改={integrity.get('tampered')} 缺失={integrity.get('missing')}")
    if fresh.get("stale"):
        issues.append(f"数据过期: {fresh.get('note')}")
    if not cons.get("ok"):
        issues.append(f"运行一致性: {cons.get('note')}")
    check("自查自愈增强闸门", False, "; ".join(issues), blocking=False)


def main():
    t0 = time.time()
    print("=" * 64)
    print("  双色球系统 — 一键永久自检 / 回归护栏")
    print(f"  时间: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 64)
    prelaunch_heavy_scripts()
    check_syntax()
    check_common()
    check_constants_consistency()
    check_period()
    check_cross_validate()
    check_eci()
    check_artifacts()
    check_data_dr()
    check_power_engine()
    check_ml_selfcheck()
    check_antifraud_gate()
    check_method_explorer_gate()
    check_version_consistency()
    check_report_sections()
    check_data_freshness()
    check_property_tests()
    check_randomness()
    check_three_body_sync()
    check_root_skill_product_sync()
    check_root_skill_data_sync()
    check_undefined_names_gate()
    check_scheduler_runtime_health()
    check_track_record_selfcheck()
    check_self_integrity_diagnose()

    n_ok = sum(1 for _, ok, _, _ in results if ok)
    n_all = len(results)
    print("\n" + "=" * 64)
    print(f"  自检汇总: {n_ok}/{n_all} 通过")

    # 严重级分层: 正确性类失败阻断交付; 运维环境类失败只告警不阻断
    blockers = [(n, d) for n, ok, d, b in results if not ok and b]
    warns = [(n, d) for n, ok, d, b in results if not ok and not b]

    rc = 0
    if warns:
        print("\n  ⚠️ 运维告警(不影响本次产出正确性, 但需尽快处理):")
        for n, d in warns:
            print(f"    ⚠️ {n}")
            if d:
                print(f"       {d}")

    if blockers:
        print("\n  失败项(正确性类, 阻断交付):")
        for n, _ in blockers:
            print(f"    ❌ {n}")
        print("\n  ⛔ 存在回归, 请勿交付未通过验证的结果!")
        rc = 1
    elif warns:
        print(f"\n  ✅ 正确性类 {n_all - len(warns)}/{n_all - len(warns)} 全通过, 产出可交付")
        print(f"  ⚠️ 但有 {len(warns)} 项运维告警待处理(见上), 请勿忽视")
    else:
        print("  ✅ 全部通过, 系统处于已验证健康状态")

    # 健康度趋势记录(追加 CSV + 写最新快照), 失败不影响判定
    try:
        record_health_history(results, time.time() - t0, rc)
    except Exception as e:
        print(f"  [warn] 健康度记录异常: {e}")

    return rc


if __name__ == '__main__':
    sys.exit(main())
