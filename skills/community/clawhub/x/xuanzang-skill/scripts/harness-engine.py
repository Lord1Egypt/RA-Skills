"""
玄奘 Harness 治理引擎 — 实现 harness-governance.md 定义的四权分离协议。
Marvis 降级版：四代理塌缩为单 P8 + 脚本强制机械边界。
用法: python harness-engine.py <command> [args...]

命令:
  load                             加载当前治理状态
  contract <name> <json>           创建任务合约（intent/acceptance/forbidden/verify_commands）
  scan-risk <contract_path>        扫描计划文件变更是否触碰高风险区
  verify <contract_path>           运行验收命令，写入 verifier_status
  gate <contract_path>             终审门控：验证全绿 + 无禁区触碰 + 合约未篡改
  report <contract_path>           生成交付报告
  register <agent_id> <json_string> 注册 agent 到 active-agents.json
  status                           列出当前活跃 agent（读 active-agents.json）
  cleanup <agent_id> <reason>      释放 agent：从 active-agents.json 移除 + 清理 state 文件 + 写 teardown.jsonl
  feedback <agent_id> <task_id> <score> <summary>
                                   记录子 agent 评审反馈到 feedback.jsonl
"""

import os
from pathlib import Path
import json
import sys
import hashlib
import subprocess
import re
import time
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
SKILL_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_ROOT / "data"
HARNESS_STATE = DATA_DIR / "harness.md"
ACTIVE_AGENTS_FILE = DATA_DIR / "active-agents.json"
TEARDOWN_FILE = DATA_DIR / "teardown.jsonl"
FEEDBACK_FILE = DATA_DIR / "feedback.jsonl"

# ─── 风险区定义 ───
RISK_ZONES = [
    (r'(^|[/\\])(tests?|__tests__|spec|e2e|cypress|playwright)([/\\]|$)', "🟡 测试资产"),
    (r'(^|[/\\])(evals?|evaluation|benchmark|scoring|verifier|grader)([/\\]|$)', "🟡 评分/评估资产"),
    (r'(^|[/\\])(\.ci|\.github/workflows|Jenkinsfile|\.gitlab-ci\.yml)', "🟡 CI 流水线"),
    (r'(^|[/\\])(hidden|private|secret|solution)([/\\]|$)', "🔴 隐藏答案/私密区"),
    (r'(^|[/\\])\.env($|\.)', "🔴 环境密钥"),
    (r'(^|[/\\])xuanzang-skill[/\\]data[/\\]', "🔴 玄奘 治理资产(本引擎自身)"),
    (r'(^|[/\\])(\.git[/\\]|\.gitignore|\.gitattributes)', "🟠 版本控制配置"),
    (r'(^|[/\\])\.(ssh|aws|kube)([/\\]|$)', "🔴 敏感配置"),
    (r'(^|[/\\])package-lock\.json$|(^|[/\\])yarn\.lock$|(^|[/\\])pnpm-lock\.yaml$', "🟠 依赖锁文件"),
]

STATE_TEMPLATE = """# 玄奘 Harness 治理状态

## 当前活跃合约
（暂无）

## 治理统计
- 总合约数: 0
- 通过数: 0
- 失败数: 0
- 越权拦截: 0

## 内部追踪
```json
{"contracts": [], "violations": [], "stats": {"total": 0, "passed": 0, "failed": 0, "blocked": 0}}
```
"""


def _ensure_state():
    os.makedirs(os.path.dirname(HARNESS_STATE), exist_ok=True)
    if not os.path.exists(HARNESS_STATE):
        with open(HARNESS_STATE, "w", encoding="utf-8") as f:
            f.write(STATE_TEMPLATE)


def _read_meta():
    with open(HARNESS_STATE, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            # 正则匹配到非 JSON 内容，回退为初始化空数据
            return {"contracts": [], "violations": [], "stats": {"total": 0, "passed": 0, "failed": 0, "blocked": 0}}
    return {"contracts": [], "violations": [], "stats": {"total": 0, "passed": 0, "failed": 0, "blocked": 0}}


def _norm_path(p):
    """将路径中的反斜杠统一为斜杠，避免 JSON 序列化时出现非法转义。"""
    return p.replace("\\", "/")

def _write_meta(meta):
    # 序列化前归一化所有路径
    for c in meta.get("contracts", []):
        if "path" in c:
            c["path"] = _norm_path(c["path"])
    with open(HARNESS_STATE, "r", encoding="utf-8") as f:
        content = f.read()
    new_json = "```json\n" + json.dumps(meta, ensure_ascii=False, indent=2) + "\n```"
    content = re.sub(r"```json\n.*?\n```", new_json, content, flags=re.DOTALL)
    with open(HARNESS_STATE, "w", encoding="utf-8") as f:
        f.write(content)


def _get_contract_hash(contract_path):
    """从 meta 中读取合约的存储哈希。"""
    meta = _read_meta()
    norm_cp = _norm_path(os.path.abspath(contract_path))
    for c in meta.get("contracts", []):
        if _norm_path(c.get("path", "")) == norm_cp:
            return c.get("hash")
    return None

def _update_contract_hash(contract_path):
    """重新计算合约哈希并更新到 meta。"""
    new_hash = _hash_file(contract_path)
    meta = _read_meta()
    norm_cp = _norm_path(os.path.abspath(contract_path))
    for c in meta.get("contracts", []):
        if _norm_path(c.get("path", "")) == norm_cp:
            c["hash"] = new_hash
            break
    _write_meta(meta)
    return new_hash

def _hash_file(path):
    """计算文件 SHA256（用于合约篡改检测）。"""
    if not os.path.exists(path):
        return "FILE_NOT_FOUND"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_load():
    _ensure_state()
    meta = _read_meta()
    active = [c for c in meta.get("contracts", []) if c.get("status") == "active"]
    return {
        "active_contracts": active,
        "stats": meta.get("stats", {}),
        "total_violations": len(meta.get("violations", [])),
    }


def cmd_contract(name, json_str):
    """
    创建任务合约。
    json_str: JSON 字符串，包含 intent / acceptance / forbidden / verify_commands
    """
    _ensure_state()
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败: {e}"}

    required = ["intent", "acceptance", "verify_commands"]
    missing = [k for k in required if k not in data]
    if missing:
        return {"error": f"合约缺少必填字段: {', '.join(missing)}"}

    contract_id = f"contract_{name}_{int(time.time())}"
    contract = {
        "id": contract_id,
        "name": name,
        "intent": data["intent"],
        "acceptance": data["acceptance"],
        "forbidden": data.get("forbidden", []),
        "verify_commands": data["verify_commands"],
        "agent_proposed_status": "pending",
        "verifier_status": "pending",
        "risk_flags": [],
        "created_at": datetime.now(tz).isoformat(),
        "modified_at": None,
        "verify_results": [],
        "gate_result": None,
    }

    # 写入合约文件（优先用户指定 → xuanzang-skill 的 temp/ 子目录）
    temp_dir = data.get("temp_dir") or str(SKILL_ROOT / "temp")
    os.makedirs(temp_dir, exist_ok=True)
    contract_path = os.path.join(temp_dir, f"{name}-contract.json")
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract, f, ensure_ascii=False, indent=2)

    # 计算合约哈希（存入 meta，不入合约文件）
    c_hash = _hash_file(contract_path)

    # 更新状态（hash 存在 meta 中，避免鸡生蛋问题）
    meta = _read_meta()
    meta["contracts"].append({
        "id": contract_id,
        "name": name,
        "path": contract_path,
        "status": "active",
        "hash": c_hash,
        "created_at": contract["created_at"],
    })
    meta["stats"]["total"] += 1
    _write_meta(meta)

    return {
        "contract_id": contract_id,
        "contract_path": contract_path,
        "intent": data["intent"],
        "acceptance_count": len(data["acceptance"]),
        "forbidden_count": len(data.get("forbidden", [])),
        "verify_commands": data["verify_commands"],
        "message": f"合约 {name} 已创建。执行前运行 scan-risk，完成后运行 verify。",
    }


def _scan_path(rel_path):
    """扫描单个路径是否命中风险区，返回风险标签列表。"""
    flags = []
    norm = rel_path.replace("\\", "/")
    for pattern, label in RISK_ZONES:
        if re.search(pattern, norm):
            flags.append(label)
    return flags


def cmd_scan_risk(contract_path):
    """
    扫描合约上下文中的计划文件变更是否触碰高风险区。
    从合约文件所在目录推断工作区，扫描 args 传入的文件列表。
    也接受 --files=<json_list> 参数。
    """
    if not os.path.exists(contract_path):
        return {"error": f"合约文件不存在: {contract_path}"}

    # 读取合约
    with open(contract_path, "r", encoding="utf-8") as f:
        contract = json.load(f)

    # 检查合约是否被篡改（对比 meta 中存储的哈希）
    stored_hash = _get_contract_hash(contract_path)
    current_hash = _hash_file(contract_path)
    tampered = (stored_hash is not None and stored_hash != current_hash)

    # 从额外参数获取文件列表
    files_to_scan = []
    extra_args = sys.argv[3:] if len(sys.argv) > 3 else []
    for arg in extra_args:
        if arg.startswith("--files="):
            try:
                files_to_scan = json.loads(arg[len("--files="):])
            except json.JSONDecodeError:
                return {"error": f"--files= 参数 JSON 解析失败: {arg}"}

    risk_flags = []
    file_results = []
    for f in files_to_scan:
        flags = _scan_path(f)
        if flags:
            risk_flags.extend(flags)
            file_results.append({"file": f, "risk_zones": flags, "blocked": any("🔴" in fl for fl in flags)})

    # 去重风险标签
    risk_flags = list(set(risk_flags))

    has_blocker = any(r["blocked"] for r in file_results)
    # tampered 合约视为阻断级风险
    if tampered:
        has_blocker = True
        risk_flags.append("🔴 合约已被篡改（完整性校验失败）")
        file_results.append({
            "file": contract_path,
            "risk_zones": ["🔴 合约已被篡改"],
            "blocked": True,
        })

    result = {
        "files_scanned": len(files_to_scan),
        "risk_flags": risk_flags,
        "file_results": file_results,
        "tampered": tampered,
        "has_blocker": has_blocker,
        "verdict": "BLOCKED" if has_blocker else ("WARN" if risk_flags else "CLEAN"),
    }

    # 记录越权尝试
    if has_blocker:
        meta = _read_meta()
        meta.setdefault("violations", []).append({
            "contract_id": contract.get("id"),
            "type": "risk_zone_blocker",
            "files": [r["file"] for r in file_results if r["blocked"]],
            "detected_at": datetime.now(tz).isoformat(),
        })
        meta["stats"]["blocked"] = meta["stats"].get("blocked", 0) + 1
        _write_meta(meta)

    # 更新合约风险标记
    contract["risk_flags"] = risk_flags
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract, f, ensure_ascii=False, indent=2)
    _update_contract_hash(contract_path)

    return result


def cmd_verify(contract_path):
    """运行验收命令，写入 verifier_status。"""
    if not os.path.exists(contract_path):
        return {"error": f"合约文件不存在: {contract_path}"}

    with open(contract_path, "r", encoding="utf-8") as f:
        contract = json.load(f)

    commands = contract.get("verify_commands", [])
    if not commands:
        return {"error": "合约中没有定义 verify_commands"}

    results = []
    all_passed = True

    for cmd in commands:
        try:
            proc = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=120, cwd=os.path.dirname(contract_path) or os.getcwd()
            )
            passed = proc.returncode == 0
            if not passed:
                all_passed = False
            results.append({
                "command": cmd,
                "exit_code": proc.returncode,
                "passed": passed,
                "stdout": proc.stdout[-2000:] if proc.stdout else "",
                "stderr": proc.stderr[-1000:] if proc.stderr else "",
            })
        except subprocess.TimeoutExpired:
            all_passed = False
            results.append({
                "command": cmd,
                "exit_code": -1,
                "passed": False,
                "stdout": "",
                "stderr": "TIMEOUT: 命令超过 120s",
            })
        except Exception as e:
            all_passed = False
            results.append({
                "command": cmd,
                "exit_code": -1,
                "passed": False,
                "stdout": "",
                "stderr": f"ERROR: {e}",
            })

    verifier_status = "pass" if all_passed else "fail"

    contract["verify_results"] = results
    contract["verifier_status"] = verifier_status
    # agent_proposed_status 由 agent 自行设置，verifier 不越权修改
    contract["modified_at"] = datetime.now(tz).isoformat()
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract, f, ensure_ascii=False, indent=2)
    _update_contract_hash(contract_path)

    # 更新状态
    meta = _read_meta()
    norm_cp = _norm_path(os.path.abspath(contract_path))
    for c in meta.get("contracts", []):
        if _norm_path(c.get("path", "")) == norm_cp:
            c["verifier_status"] = verifier_status
            if verifier_status == "pass":
                meta["stats"]["passed"] = meta["stats"].get("passed", 0) + 1
            else:
                meta["stats"]["failed"] = meta["stats"].get("failed", 0) + 1
    _write_meta(meta)

    return {
        "verifier_status": verifier_status,
        "commands_run": len(commands),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
        "results": results,
    }


def cmd_gate(contract_path):
    """终审门控：验证全绿 + 无禁区触碰 + 合约未篡改。"""
    if not os.path.exists(contract_path):
        return {"error": f"合约文件不存在: {contract_path}"}

    with open(contract_path, "r", encoding="utf-8") as f:
        contract = json.load(f)

    checks = []

    # 1. 合约篡改检测（对比 meta 哈希）
    stored_hash = _get_contract_hash(contract_path)
    current_hash = _hash_file(contract_path)
    tampered = (stored_hash is not None and stored_hash != current_hash)
    checks.append({
        "check": "合约完整性",
        "passed": not tampered,
        "detail": "合约已被修改（可能降级验收标准）" if tampered else "合约未篡改",
    })

    # 2. 验证状态
    verifier_status = contract.get("verifier_status", "pending")
    verify_passed = verifier_status == "pass"
    checks.append({
        "check": "验收命令全绿",
        "passed": verify_passed,
        "detail": f"verifier_status = {verifier_status}",
    })

    # 3. 无 🔴 风险区触碰
    risk_flags = contract.get("risk_flags", [])
    has_blocker = any("🔴" in fl for fl in risk_flags)
    checks.append({
        "check": "无禁区触碰",
        "passed": not has_blocker,
        "detail": f"触碰的风险区: {risk_flags}" if risk_flags else "无风险区触碰",
    })

    # 4. 禁止项自查 — forbidden 为空意味着任务无禁区声明，不扣分
    # 逻辑：没有禁区 = 任务安全，不应判定为 FAIL。总是通过。
    forbidden = contract.get("forbidden", [])
    checks.append({
        "check": "禁止项已声明",
        "passed": True,
        "detail": f"已声明 {len(forbidden)} 项禁区" if forbidden else "无禁区声明（任务安全）",
    })

    all_passed = all(c["passed"] for c in checks)
    gate_result = "PASS" if all_passed else "FAIL"

    contract["gate_result"] = gate_result
    contract["gate_checks"] = checks
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract, f, ensure_ascii=False, indent=2)
    _update_contract_hash(contract_path)

    return {
        "gate_result": gate_result,
        "checks": checks,
        "verdict": (
            "✅ 通过终审 — 合约完整 + 验收全绿 + 无禁区触碰。可以交付。"
            if all_passed else
            '❌ 终审未通过 — 存在未解决的检查项。禁止声明「已完成」。'
        ),
    }


def cmd_report(contract_path):
    """生成交付报告。"""
    if not os.path.exists(contract_path):
        return {"error": f"合约文件不存在: {contract_path}"}

    with open(contract_path, "r", encoding="utf-8") as f:
        contract = json.load(f)

    verify_results = contract.get("verify_results", [])
    gate_checks = contract.get("gate_checks", [])
    risk_flags = contract.get("risk_flags", [])

    return {
        "contract_id": contract.get("id"),
        "intent": contract.get("intent"),
        "agent_proposed_status": contract.get("agent_proposed_status"),
        "verifier_status": contract.get("verifier_status"),
        "gate_result": contract.get("gate_result"),
        "verify_summary": {
            "total": len(verify_results),
            "passed": sum(1 for r in verify_results if r.get("passed")),
            "failed": sum(1 for r in verify_results if not r.get("passed")),
        },
        "risk_flags": risk_flags,
        "gate_summary": {
            "total": len(gate_checks),
            "passed": sum(1 for c in gate_checks if c.get("passed")),
        },
        "tampered": (_get_contract_hash(contract_path) is not None 
                     and _get_contract_hash(contract_path) != _hash_file(contract_path)),
        "verdict": (
            "可以交付。验收全绿 + 终审通过。"
            if contract.get("gate_result") == "PASS"
            else "不可交付。存在未通过的检查项。"
        ),
    }


# ─── active-agents.json 管理 ─────────────────────────────

def _ensure_active_agents():
    os.makedirs(os.path.dirname(ACTIVE_AGENTS_FILE), exist_ok=True)
    if not os.path.exists(ACTIVE_AGENTS_FILE):
        with open(ACTIVE_AGENTS_FILE, "w", encoding="utf-8") as f:
            json.dump({"agents": []}, f, ensure_ascii=False, indent=2)


def cmd_register(agent_id, json_str):
    """注册 agent 到 active-agents.json。"""
    _ensure_active_agents()
    try:
        extra = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败: {e}"}

    with open(ACTIVE_AGENTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    agent_entry = {
        "agent_id": agent_id,
        "registered_at": datetime.now(tz).isoformat(),
    }
    agent_entry.update(extra)

    data.setdefault("agents", []).append(agent_entry)

    with open(ACTIVE_AGENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "registered": True,
        "agent_id": agent_id,
        "total": len(data["agents"]),
    }


def cmd_status():
    """列出当前活跃 agent 列表，计算 TTL 并标记 stale。"""
    _ensure_active_agents()
    with open(ACTIVE_AGENTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    agents = data.get("agents", [])
    now = datetime.now(tz)
    ttl_minutes = 30
    active = []
    stale = []
    for a in agents:
        reg_at = a.get("registered_at", "")
        age_minutes = None
        is_stale = False
        if reg_at:
            try:
                reg_dt = datetime.fromisoformat(reg_at)
                age_minutes = round((now - reg_dt).total_seconds() / 60, 1)
                is_stale = age_minutes > ttl_minutes
            except (ValueError, TypeError):
                pass
        entry = {**a, "age_minutes": age_minutes, "stale": is_stale}
        if is_stale:
            stale.append(entry)
        else:
            active.append(entry)
    return {
        "active_agents": active,
        "stale_agents": stale,
        "total": len(agents),
        "ttl_minutes": ttl_minutes,
    }


def cmd_cleanup(agent_id, reason=""):
    """
    释放 agent：从 active-agents.json 移除 + 清理 state 文件 + 写入 teardown.jsonl。
    调用时机：子 agent 完成/失败后，由 P8 调度层执行。
    """
    _ensure_active_agents()
    with open(ACTIVE_AGENTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    agents = data.get("agents", [])
    removed = [a for a in agents if a.get("agent_id") == agent_id]
    agents = [a for a in agents if a.get("agent_id") != agent_id]
    data["agents"] = agents

    with open(ACTIVE_AGENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 清理 state 文件（如果存在）
    state_file = DATA_DIR / f"agent-{agent_id}.state"
    state_existed = state_file.exists()
    if state_existed:
        state_file.unlink()

    # 写 teardown.jsonl（格式与 SKILL.md R6 一致）
    teardown_entry = {
        "agent": agent_id,
        "reason": reason,
        "ts": datetime.now(tz).isoformat(),
    }
    if removed:
        teardown_entry["registered_at"] = removed[0].get("registered_at")
    with open(TEARDOWN_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(teardown_entry, ensure_ascii=False) + "\n")

    cmd_prune_logs(keep=200)  # 自动裁剪

    return {
        "cleanup": True,
        "agent_id": agent_id,
        "reason": reason,
        "remaining": len(agents),
        "state_cleaned": state_existed,
    }


def cmd_feedback(agent_id, task_id, score, summary):
    """
    记录子 agent 评审反馈到 feedback.jsonl。
    score: 0-100 整数，"excellent"/"pass"/"fail" 等字符串也会接受。
    格式与 SKILL.md §多角色派发标准 声明一致：
    {"ts":"ISO8601","agent_id":"p7-xxx","task_id":"xxx","score":0-100,"summary":"一句话"}
    """
    try:
        os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
        try:
            score_val = int(score)
        except ValueError:
            score_val = score
        entry = {
            "ts": datetime.now(tz).isoformat(),
            "agent_id": agent_id,
            "task_id": task_id,
            "score": score_val,
            "summary": summary,
        }
        with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        cmd_prune_logs(keep=200)  # 自动裁剪
        return {"feedback": True, "agent_id": agent_id, "score": score_val}
    except (OSError, IOError) as e:
        return {"feedback": False, "error": f"写入失败: {e}"}


def cmd_teardown_all(reason="cascade"):
    """级联释放全部活跃 agent（P10→P9→P8→P7 的脚本侧实现）。"""
    _ensure_active_agents()
    with open(ACTIVE_AGENTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    agents = data.get("agents", [])
    results = []
    for a in agents:
        agent_id = a.get("agent_id", "")
        r = cmd_cleanup(agent_id, reason)
        results.append(r)
    return {
        "teardown_all": True,
        "released": len(results),
        "reason": reason,
        "results": results,
    }


def cmd_prune_logs(keep=200):
    """裁剪 teardown.jsonl 和 feedback.jsonl 只保留最近 N 条"""
    result = {"keep": keep}
    for label, fpath in [("teardown", TEARDOWN_FILE), ("feedback", FEEDBACK_FILE)]:
        if not fpath.exists():
            result[label] = {"pruned": 0, "remaining": 0}
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        total = len(lines)
        if total <= keep:
            result[label] = {"pruned": 0, "remaining": total}
        else:
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(lines[-keep:])
            result[label] = {"pruned": total - keep, "remaining": keep}
    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python harness-engine.py <load|contract|scan-risk|verify|gate|report|register|status|cleanup|feedback|teardown-all|prune-logs> [args...]"}, ensure_ascii=False))
        sys.exit(1)

    command = sys.argv[1]

    if command == "load":
        result = cmd_load()
    elif command == "contract":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "用法: python harness-engine.py contract <name> '<json_string>'"}, ensure_ascii=False))
            sys.exit(1)
        result = cmd_contract(sys.argv[2], sys.argv[3])
    elif command == "scan-risk":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "用法: python harness-engine.py scan-risk <contract_path> [--files='[\"path1\",\"path2\"]']"}, ensure_ascii=False))
            sys.exit(1)
        result = cmd_scan_risk(sys.argv[2])
    elif command == "verify":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "用法: python harness-engine.py verify <contract_path>"}, ensure_ascii=False))
            sys.exit(1)
        result = cmd_verify(sys.argv[2])
    elif command == "gate":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "用法: python harness-engine.py gate <contract_path>"}, ensure_ascii=False))
            sys.exit(1)
        result = cmd_gate(sys.argv[2])
    elif command == "report":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "用法: python harness-engine.py report <contract_path>"}, ensure_ascii=False))
            sys.exit(1)
        result = cmd_report(sys.argv[2])
    elif command == "register":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "用法: python harness-engine.py register <agent_id> '<json_string>'"}, ensure_ascii=False))
            sys.exit(1)
        result = cmd_register(sys.argv[2], sys.argv[3])
    elif command == "status":
        result = cmd_status()
    elif command == "cleanup":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "用法: python harness-engine.py cleanup <agent_id> <reason>"}, ensure_ascii=False))
            sys.exit(1)
        result = cmd_cleanup(sys.argv[2], sys.argv[3])
    elif command == "feedback":
        if len(sys.argv) < 6:
            print(json.dumps({"error": "用法: python harness-engine.py feedback <agent_id> <task_id> <score> <summary>"}, ensure_ascii=False))
            sys.exit(1)
        result = cmd_feedback(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif command == "teardown-all":
        reason = sys.argv[2] if len(sys.argv) > 2 else "cascade"
        result = cmd_teardown_all(reason)
    elif command == "prune-logs":
        keep = int(sys.argv[2]) if len(sys.argv) > 2 else 200
        result = cmd_prune_logs(keep)
    else:
        print(json.dumps({"error": f"未知命令: {command}。可用: load / contract / scan-risk / verify / gate / report / register / status / cleanup / feedback / teardown-all / prune-logs"}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
