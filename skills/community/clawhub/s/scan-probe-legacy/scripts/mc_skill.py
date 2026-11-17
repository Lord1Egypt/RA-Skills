# -*- coding: utf-8 -*-
"""MC Skill Agent 入口脚本

Agent AI 通过此脚本调用 MC Skill 的各功能，返回 JSON 格式结果。

用法:
    python scripts/mc_skill.py <feature> [参数...]

示例:
    python scripts/mc_skill.py jar_parser --jar-path "create.jar"
    python scripts/mc_skill.py mod_searcher --query "Create" --mc-version "1.21.1" --loader "neoforge"
    python scripts/mc_skill.py mixin_scanner --mods-dir "./mods"
    python scripts/mc_skill.py crash_analyzer --crash-log "crash.txt"
    python scripts/mc_skill.py migration_assess --jar-path "create.jar" --from-mc-version "1.20.1" --to-mc-version "1.21.1" --from-loader "forge" --to-loader "neoforge"
    python scripts/mc_skill.py onboarding_info          # 🔑 首对话引导 —— 拿动态数据（免费期/额度/功能列表/套餐）
    python scripts/mc_skill.py mark_onboarding_shown    # 🔑 标记引导已展示（防重复打扰）
    python scripts/mc_skill.py gen_test_id --label "付费流程" --admin 2  # 🧪 生成标准化测试码
"""

import sys
import os
import json
import re
from datetime import datetime

# ================================================================
# 🔧 Windows 编码修复（QClaw 反馈 #3）
# 问题：Windows cmd 默认 GBK，输出 emoji / 特殊字符会
#       抛 UnicodeEncodeError，脚本直接崩，Agent 拿不到 JSON。
# 策略：1. 强制环境变量 PYTHONIOENCODING=utf-8
#       2. 重绑 sys.stdout / sys.stderr 为 UTF-8 writer
#       3. 失败时 fallback：所有输出用 ? 替换无法编码字符
# ================================================================
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    import io
    _stdout_wrapper = io.TextIOWrapper(
        sys.stdout.buffer if hasattr(sys.stdout, "buffer") else sys.__stdout__.buffer,
        encoding="utf-8", errors="replace", line_buffering=True,
    )
    _stderr_wrapper = io.TextIOWrapper(
        sys.stderr.buffer if hasattr(sys.stderr, "buffer") else sys.__stderr__.buffer,
        encoding="utf-8", errors="replace", line_buffering=True,
    )
    sys.stdout = _stdout_wrapper
    sys.stderr = _stderr_wrapper
except Exception:
    # 极端情况退到 ignore
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 将项目根目录加入路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def _handle_onboarding_info():
    """Agent AI 首对话时调这个拿动态引导数据"""
    try:
        from core.auth_manager import get_onboarding_info
        info = get_onboarding_info()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 1


def _handle_mark_onboarding_shown():
    """引导展示完后调这个标记，防止后续对话重复打扰"""
    try:
        from core.auth_manager import mark_onboarding_shown
        mark_onboarding_shown()
        print(json.dumps({"ok": True, "message": "onboarding_shown marked"}, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 1


# ==================== 🧪 标准化测试码生成器 ====================
# 格式：TEST-{admin号}-{用途}-{日期}
# 例：TEST-1-ONBOARDING-20260828  TEST-2-PAYFLOW-20260828
# 系统自动识别：机器码含 TEST/NGROK/DEV/ADMIN 等关键词 → user_type=admin
_LABEL_KEYWORDS = {
    # 英文
    "onboarding": "ONBOARDING",    # 首对话引导
    "pay": "PAYFLOW",              # 付费流程
    "payment": "PAYFLOW",
    "register": "REG",             # 注册链路
    "reg": "REG",
    "auth": "AUTH",                # 授权校验
    "jar": "JAR",                  # JAR 解析
    "mod": "MOD",                  # 模组检索
    "mixin": "MIXIN",              # Mixin 扫描
    "save": "SAVE",                # 存档同步
    "translate": "TRANSLATE",      # 汉化
    "crash": "CRASH",              # 报错修复
    "migrate": "MIGRATE",          # 移植评估
    "version": "VERSION",          # 版本检测
    "cold": "COLD",                # 冷启动
    "setup": "SETUP",              # 环境搭建
    "full": "FULL",                # 全链路
    # 中文
    "引导": "ONBOARDING",
    "付费": "PAYFLOW",
    "支付": "PAYFLOW",
    "注册": "REG",
    "授权": "AUTH",
    "存档": "SAVE",
    "汉化": "TRANSLATE",
    "翻译": "TRANSLATE",
    "崩溃": "CRASH",
    "报错": "CRASH",
    "移植": "MIGRATE",
    "冷启动": "COLD",
    "环境": "SETUP",
    "全链路": "FULL",
    "完整": "FULL",
}

# 中文编号映射
_CN_NUM = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十"}


def _resolve_label(raw_label: str) -> str:
    """把用户输入的 label（中文/英文）转成 4-8 位大写英文 code"""
    if not raw_label:
        return "GENERAL"
    key = raw_label.strip().lower()
    for k, v in _LABEL_KEYWORDS.items():
        if k in key:
            return v
    # 兜底：取前 6 个字母的大写
    clean = re.sub(r"[^A-Za-z]", "", raw_label)[:6].upper()
    return clean or "GENERAL"


def _handle_gen_test_id(args: list) -> int:
    """
    生成标准化测试机器码 + 自动写入 auth_state.json + 自动注册到服务器
    
    参数:
        --label <用途>     测试用途（中文/英文都行，例：付费流程 / onboarding / 注册链路）
        --admin <编号>     管理员编号 1-10（默认自动取下一个）
        --register         是否立即注册到服务器（默认 True，需服务器在跑）
    
    示例:
        python scripts/mc_skill.py gen_test_id --label "付费流程" --admin 2
        python scripts/mc_skill.py gen_test_id --label "onboarding"
        python scripts/mc_skill.py gen_test_id --label "全链路" --admin 1
    """
    # 解析参数
    label_raw = ""
    admin_num = None
    do_register = True
    
    i = 0
    while i < len(args):
        if args[i] == "--label" and i + 1 < len(args):
            label_raw = args[i + 1]; i += 2
        elif args[i] == "--admin" and i + 1 < len(args):
            try: admin_num = int(args[i + 1]); i += 2
            except ValueError: i += 1
        elif args[i] == "--no-register":
            do_register = False; i += 1
        else:
            i += 1
    
    # 解析 label
    label_code = _resolve_label(label_raw)
    date_str = datetime.now().strftime("%Y%m%d")
    
    # 如果没指定 admin 编号，自动找 registry.json 里最小可用编号
    if admin_num is None:
        admin_num = 1
        try:
            reg_path = os.path.join(PROJECT_ROOT, "server", "data", "registry.json")
            if os.path.exists(reg_path):
                import json as _json
                reg = _json.load(open(reg_path, encoding="utf-8"))
                # 收集所有已占用的管理员编号
                _used = set()
                for _u in reg:
                    _rn = _u.get("nickname", "")
                    _m = re.search(r"管理员(\d+)", _rn)
                    if _m:
                        _used.add(int(_m.group(1)))
                    _cn_map = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10}
                    _m2 = re.search(r"管理员([一二三四五六七八九十])", _rn)
                    if _m2 and _m2.group(1) in _cn_map:
                        _used.add(_cn_map[_m2.group(1)])
                # 找最小可用编号
                admin_num = 1
                while admin_num in _used:
                    admin_num += 1
        except Exception:
            pass
    
    # 生成机器码
    machine_id = f"TEST-{admin_num}-{label_code}-{date_str}"
    nickname = f"管理员{_CN_NUM.get(admin_num, admin_num)}"
    
    result = {
        "ok": True,
        "machine_id": machine_id,
        "nickname": nickname,
        "label": label_raw or label_code,
        "admin_num": admin_num,
        "date": date_str,
        "format_rule": "TEST-{admin号}-{用途code}-{日期}",
        "instructions": [
            f"1. 已生成测试码: {machine_id}",
            f"2. 用户列表里会显示为: 🛡️测试用户 / {nickname} / 🆓免费用户 / 🔒永久",
            "3. 用完后直接调下一条命令就能生成新的，admin 号自动递增",
        ],
    }
    
    # 自动写入 auth_state.json（让当前客户端下次启动就用这个机器码）
    try:
        state_dir = os.path.join(PROJECT_ROOT, "data")
        os.makedirs(state_dir, exist_ok=True)
        state_path = os.path.join(state_dir, "auth_state.json")
        
        state = {}
        if os.path.exists(state_path):
            state = json.load(open(state_path, encoding="utf-8"))
        
        # 如果已有 state，保留 first_use_date 等字段；没有就初始化
        if not state.get("machine_id"):
            from datetime import timedelta
            from core.auth_manager import FREE_PERIOD_DAYS
            today = datetime.now().strftime("%Y-%m-%d")
            state = {
                "machine_id": machine_id,
                "first_use_date": state.get("first_use_date", today),
                "free_period_end": state.get("free_period_end", (datetime.now() + timedelta(days=FREE_PERIOD_DAYS)).strftime("%Y-%m-%d")),
                "onboarding_shown": True,  # 测试用户跳过引导
                "tier": "free",
                "daily_usage": {},
                "license_expires": "",
            }
        else:
            state["machine_id"] = machine_id
            state["onboarding_shown"] = True
        
        json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        result["auth_state_saved"] = True
        result["auth_state_path"] = state_path
    except Exception as e:
        result["auth_state_saved"] = False
        result["auth_state_error"] = str(e)
    
    # 自动注册到服务器（如果服务器在跑）
    if do_register:
        try:
            import urllib.request
            import ssl  # V1.0.5 修复：显式 SSL 上下文
            auth_url = os.environ.get("MC_SKILL_AUTH_URL", "")
            if not auth_url:
                # 默认走线上服务端（本地调试用 MC_SKILL_AUTH_URL 覆盖）
                auth_url = os.environ.get("MC_SKILL_SERVER_URL") or "http://45.76.179.12"
            
            api_url = f"{auth_url.rstrip('/')}/api/auth/quick-check"
            body = json.dumps({
                "machine_id": machine_id,
                "fingerprint": "TEST_GENERATOR",
                "version": getattr(__import__("config"), "VERSION", "unknown"),
                "source": "qclaw_test",
            }).encode("utf-8")
            req = urllib.request.Request(api_url, data=body, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=5, context=ssl.create_default_context()) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                result["server_registered"] = True
                result["server_response"] = resp_data
        except Exception as e:
            result["server_registered"] = False
            result["server_error"] = str(e) + "（服务器没在跑？没关系，下次客户端启动时会自动注册）"

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _handle_get_platform(args: list) -> int:
    """
    获取当前 AI 平台声明。

    参数: （无）

    返回 JSON:
        {
          "platform": "workbuddy",   # 用户声明的平台；若未声明则为 "unknown"
          "declared": true,          # 是否由用户手动声明过
          "supported_platforms": [...]  # 白名单
        }

    用法:
        python scripts/mc_skill.py get_platform
    """
    from core.auth_manager import (
        get_current_platform,
        is_platform_declared,
        SUPPORTED_AI_PLATFORMS,
    )
    print(json.dumps({
        "platform": get_current_platform(),
        "declared": is_platform_declared(),
        "supported_platforms": SUPPORTED_AI_PLATFORMS,
    }, ensure_ascii=False, indent=2))
    return 0


def _handle_set_platform(args: list) -> int:
    """
    声明 AI 平台（写入 ~/.mc-skill/platform.txt，并清理旧 salt 触发机器码重建）。

    参数:
        --platform <名称>   平台标识（workbuddy / kimi / trae / cursor / openclaw /
                            chatgpt / copilot / cline / windsurf / aider /
                            continue / vscode / custom），不区分大小写

    返回 JSON:
        {
          "success": true,
          "platform": "workbuddy",
          "old_platform": "unknown-12345",  # 之前平台（首次声明时可能为兜底值）
          "machine_id": "5184c91c54610b2852a9369f68332286"
        }

    用法:
        python scripts/mc_skill.py set_platform --platform workbuddy
    """
    platform = ""
    i = 0
    while i < len(args):
        if args[i] == "--platform" and i + 1 < len(args):
            platform = args[i + 1]
            i += 2
        else:
            i += 1
    if not platform:
        print(json.dumps({
            "error": "缺少 --platform 参数",
            "usage": "python scripts/mc_skill.py set_platform --platform workbuddy",
            "supported": [
                "workbuddy", "kimi", "trae", "cursor", "openclaw",
                "chatgpt", "copilot", "cline", "windsurf",
                "aider", "continue", "vscode", "custom",
            ],
        }, ensure_ascii=False, indent=2))
        return 2

    from core.auth_manager import (
        set_ai_platform,
        get_current_platform,
        get_machine_id,
        SUPPORTED_AI_PLATFORMS,
    )
    old = get_current_platform()
    ok = set_ai_platform(platform)
    if not ok:
        print(json.dumps({
            "error": f"平台 '{platform}' 不在白名单中",
            "supported": SUPPORTED_AI_PLATFORMS,
        }, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps({
        "success": True,
        "platform": get_current_platform(),
        "old_platform": old,
        "machine_id": get_machine_id(),
    }, ensure_ascii=False, indent=2))
    return 0


def _handle_reset_machine_id(args: list) -> int:
    """
    重置机器码（删除所有 salt 文件，强制生成新机器码）。

    使用场景：
      - 用户更换了 AI 软件且之前未声明
      - 用户重装系统后
      - 调试需要干净机器码

    参数: （无）

    返回 JSON:
        {
          "success": true,
          "old_machine_id": "...",
          "machine_id": "..."  # 新机器码
        }

    用法:
        python scripts/mc_skill.py reset_machine_id
    """
    from core.auth_manager import (
        get_machine_id as _get_mid,
        reset_machine_id as _reset_mid,
    )
    old = _get_mid()
    new = _reset_mid()
    print(json.dumps({
        "success": True,
        "old_machine_id": old,
        "machine_id": new,
    }, ensure_ascii=False, indent=2))
    return 0


def _handle_get_remaining_quota() -> int:
    """获取今日剩余额度（全自动/半自动/移植评估）

    用法:
        python scripts/mc_skill.py get_remaining_quota

    返回 JSON:
        {
          "auto_remaining": int,
          "semi_remaining": int,
          "migration_remaining": int,
          "auto_used": int,
          "semi_used": int,
          "auto_limit": int,
          "semi_limit": int,
          "tier": "free" | "normal",
          "in_free_period": bool
        }
    """
    try:
        from core.auth_manager import get_remaining_quota
        quota = get_remaining_quota()
        print(json.dumps(quota, ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 1


def _handle_open_lookup_page(args: list) -> int:
    """打开游客查询页面（含机器码预选、语言继承、币种继承）

    参数:
        --machine-id xxx    机器码（可选，默认自动获取本机）
        --lang zh_cn        语言代码（默认 zh_cn）
        --currency CNY      币种（默认根据语言自动判断）

    用法:
        python scripts/mc_skill.py open_lookup_page
        python scripts/mc_skill.py open_lookup_page --lang en_us
        python scripts/mc_skill.py open_lookup_page --machine-id abc123

    返回 JSON:
        {
          "success": true,
          "url": "http://45.76.179.12/lookup.html?..."
        }
    """
    try:
        from core.auth_manager import open_lookup_page, get_machine_id

        # 解析参数
        machine_id = ""
        lang = "zh_cn"
        currency = ""
        i = 0
        while i < len(args):
            if args[i] == "--machine-id" and i + 1 < len(args):
                machine_id = args[i + 1]
                i += 2
            elif args[i] == "--lang" and i + 1 < len(args):
                lang = args[i + 1]
                i += 2
            elif args[i] == "--currency" and i + 1 < len(args):
                currency = args[i + 1]
                i += 2
            else:
                i += 1

        # 自动获取机器码（如果没显式传）
        if not machine_id:
            try:
                machine_id = get_machine_id()
            except Exception:
                machine_id = ""

        url = open_lookup_page(machine_id=machine_id, lang=lang, currency=currency)
        print(json.dumps({
            "success": True,
            "url": url,
            "machine_id": machine_id,
            "opened": True,
        }, ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 1


def _check_license_integrity():
    """启动时校验 SKILL.md 许可证章节是否被篡改/删除。
    若缺失则输出 JSON 错误并退出。
    """
    skill_md = os.path.join(PROJECT_ROOT, "SKILL.md")
    if not os.path.exists(skill_md):
        print(json.dumps({"error": "FATAL: SKILL.md 缺失，许可证完整性校验失败，拒绝运行。"}, ensure_ascii=False))
        sys.exit(1)
    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(json.dumps({"error": f"FATAL: 读取 SKILL.md 失败: {e}"}, ensure_ascii=False))
        sys.exit(1)
    required_markers = [
        "MC-Skill Restrictive License",
        "not authorized to modify",
        "Public distribution of modified versions",
    ]
    missing = [m for m in required_markers if m not in content]
    if missing:
        print(json.dumps({
            "error": "FATAL: 许可证完整性校验失败 — SKILL.md 许可证章节被删除或篡改。本 Skill 采用 MC-Skill Restrictive License v1.0，禁止删除或篡改许可证章节。请从官方渠道重新获取。",
            "missing_markers": missing,
        }, ensure_ascii=False))
        sys.exit(1)


def main():
    _check_license_integrity()
    # 核心文件哈希校验（防篡改，硬拦截）
    try:
        from core.integrity_guard import enforce_integrity
        enforce_integrity()
    except SystemExit:
        raise
    except Exception:
        pass

    # V1.0.5: 上报应用启动事件（onboarding_info 等认证层命令也上报，确保在线用户可监测）
    try:
        from core.auth_manager import report_app_started
        report_app_started()
    except Exception:
        pass

    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "缺少功能参数",
            "usage": "python scripts/mc_skill.py <feature> [参数...]",
            "features": [
                "jar_parser - JAR结构解析",
                "mod_searcher - 模组检索下载",
                "env_builder - 环境引导搭建",
                "mixin_scanner - Mixin冲突扫描",
                "repacker - 资源重打包",
                "save_sync - 存档同步",
                "translator - 基础汉化",
                "crash_analyzer - 报错修复",
                "auto_fix - 自动修复",
                "migration_assess - 移植可行性评估",
                "onboarding_info - 🔑 首对话引导数据（免费期/额度/功能列表/套餐）",
                "mark_onboarding_shown - 🔑 标记引导已展示",
                "gen_test_id - 🧪 生成标准化测试机器码（自动注册+自动写入auth_state）",
                "get_platform - 📋 查询当前 AI 平台声明",
                "set_platform - 📝 声明 AI 平台（解决机器码不稳定 bug）",
                "reset_machine_id - 🔄 重置机器码（清空所有 ~/skill/* salt）",
                "get_remaining_quota - 📊 获取今日剩余额度（全自动/半自动/移植评估）",
                "open_lookup_page - 🔗 打开游客查询页面（自动携带本机机器码+语言+币种）",
            ],
        }, ensure_ascii=False, indent=2))
        return 1

    feature = sys.argv[1]
    args = sys.argv[2:]

    # ========== 认证层专用命令（不走 main.py feature 机制）==========
    if feature == "onboarding_info":
        return _handle_onboarding_info()
    elif feature == "mark_onboarding_shown":
        return _handle_mark_onboarding_shown()
    elif feature == "gen_test_id":
        return _handle_gen_test_id(args)
    elif feature == "get_platform":
        return _handle_get_platform(args)
    elif feature == "set_platform":
        return _handle_set_platform(args)
    elif feature == "reset_machine_id":
        return _handle_reset_machine_id(args)
    elif feature == "get_remaining_quota":
        return _handle_get_remaining_quota()
    elif feature == "open_lookup_page":
        return _handle_open_lookup_page(args)

    # ========== 业务功能 → 转调 main.py --feature ==========
    cmd_args = ["main.py", "--feature", feature] + args

    original_argv = sys.argv
    sys.argv = cmd_args

    try:
        from main import main as main_entry
        main_entry()
        return 0
    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "feature": feature,
        }, ensure_ascii=False, indent=2))
        return 1
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    sys.exit(main())
