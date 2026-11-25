#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文章处理技能脚本：调用云端处理API（/bailian/chat 兼容接口）

应用列表云端动态管理：后台新增/改名/写简介/上下线，插件立即跟着变，无需发版。
调用方式两种并存：
  --model 应用ID     任意云端应用直调（后台新增的应用用它，推荐）
  --mode 快捷名      旧三档快捷方式（flash=微处理 pro=中处理 pro_plus=重处理）

密钥优先级：--api-key（本次临时） > 本机已保存的个人密钥 > 云端下发的公共密钥
（包内不存任何密钥，公共密钥运行时从公开配置接口拉取，后台换密钥立即生效，无需发版）
个人密钥保存后永久生效；--use public/personal 随时切换（个人密钥保留不删除），--clear-key 彻底删除。
"""
import argparse
import json
import os
import sys
import urllib.request

API_URL = "https://1257707270-955niawhww.ap-shanghai.tencentscf.com/bailian/chat"
MODELS_URL = "https://1257707270-955niawhww.ap-shanghai.tencentscf.com/v1/models"
CONFIG_URL = "https://1257707270-955niawhww.ap-shanghai.tencentscf.com/api/user/config"
# 旧档位快捷名（仅作老用户习惯的映射，新应用不需要进这里，直接用 --model 应用ID）
MODELS = {
    "flash": "wenzi_runs",      # 微处理——打破AI骨架结构
    "pro": "wenzi_paiban",      # 中处理——琢字琢句对症下药
    "pro_plus": "wenzi_power",  # 重处理——超级处理，耗时长，最有效去AI味
    # 旧档位名兼容
    "runse": "wenzi_runs",
    "paiban": "wenzi_paiban",
    "power": "wenzi_power",
    "both": "wenzi_power",
}
# 旧三档的快捷名提示（用于 --list-models 展示）
LEGACY_TIERS = {
    "wenzi_runs": "flash（微处理）",
    "wenzi_paiban": "pro（中处理）",
    "wenzi_power": "pro_plus（重处理）",
}
DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".workbuddy", "wenzi-runse-config.json")


def out(payload):
    print(json.dumps(payload, ensure_ascii=False))


def fetch_public_key():
    """从公开配置接口拉取云端下发的公共密钥（包内不存任何密钥，后台换密钥立即生效）"""
    try:
        req = urllib.request.Request(CONFIG_URL, method="GET")
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.loads(res.read().decode("utf-8"))
        return str(data.get("pluginPublicKey", "") or "").strip()
    except Exception:
        return ""


def resolve_key(args):
    """密钥优先级：--api-key（本次临时） > 本机已保存个人密钥（public 模式时跳过） > 云端下发公共密钥；全空返回空串"""
    explicit = (args.api_key or "").replace("Bearer", "").strip()
    if explicit:
        return explicit
    if load_saved_mode(args.config_path) != "public":
        saved = load_saved_key(args.config_path)
        if saved:
            return saved
    return fetch_public_key()


NO_KEY_MSG = "暂时无法获取公共密钥（后台未配置或网络异常），可稍后重试，或用 --api-key 提供个人密钥。"


def call_api(text, model_id, api_key):
    """调用云端接口，返回统一结构 {"success", "result", "message"}"""
    body = {"text": text, "model": model_id, "api_key": api_key}

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as res:
            data = json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "result": "", "message": f"网络请求失败: {e}"}

    err = str(data.get("error", "") or "").strip()
    if err:
        # API 返回的业务提示（额度用完、密钥无效、应用下线等），原样转达用户
        return {"success": False, "result": "", "message": err}
    return {"success": True, "result": str(data.get("result", "") or ""), "message": "ok"}


def list_models(api_key):
    """动态获取云端应用列表（/v1/models）：后台新增应用/改简介/上下线，这里立即反映"""
    req = urllib.request.Request(MODELS_URL, headers={"Authorization": f"Bearer {api_key}"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "result": "", "models": [], "message": f"获取应用列表失败: {e}"}

    items = data.get("data", []) if isinstance(data, dict) else []
    if not items:
        return {"success": False, "result": "", "models": [], "message": "云端未返回任何应用"}

    models = []
    lines = [f"当前可用的处理应用（共 {len(items)} 个）："]
    for i, m in enumerate(items, 1):
        mid = str(m.get("id", "") or "")
        name = str(m.get("name", "") or "") or mid
        desc = str(m.get("desc", "") or "").strip()
        models.append({"id": mid, "name": name, "desc": desc})
        seg = f"{i}. {name}"
        if desc:
            seg += f" — {desc}"
        tier = LEGACY_TIERS.get(mid)
        if tier:
            seg += f"（快捷名：{tier}）"
        lines.append(seg)
    lines.append("用户回复编号或名称即可，用 --model 应用ID 调用对应应用（旧快捷名 --mode 仍可用）。")
    return {"success": True, "result": "\n".join(lines), "models": models, "message": "ok"}


def load_config(config_path=DEFAULT_CONFIG_PATH):
    """读取本机密钥配置文件，返回 dict（不存在/损坏返回空 dict）"""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def load_saved_key(config_path=DEFAULT_CONFIG_PATH):
    return str(load_config(config_path).get("api_key", "") or "").strip()


def load_saved_mode(config_path=DEFAULT_CONFIG_PATH):
    """auto（默认，用个人密钥） / public（临时切公共，个人密钥保留）"""
    return str(load_config(config_path).get("mode", "") or "").strip()


def save_config(cfg, config_path=DEFAULT_CONFIG_PATH):
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        # 以 0600 权限写入，仅限当前用户可读（Windows 下尽力而为）
        fd = os.open(config_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)
        try:
            os.chmod(config_path, 0o600)
        except Exception:
            pass
        return True
    except Exception as e:
        out({"success": False, "result": "", "message": f"密钥保存失败: {e}"})
        return False


def save_key(key, config_path=DEFAULT_CONFIG_PATH):
    cfg = load_config(config_path)
    cfg["api_key"] = key
    cfg.setdefault("mode", "auto")
    return save_config(cfg, config_path)


def mask(key):
    return key[:6] + "****" + key[-4:] if len(key) > 12 else "****"


def main():
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=list(MODELS),
                        help="旧三档快捷名：flash=微处理 pro=中处理 pro_plus=重处理（新应用请用 --model）")
    parser.add_argument("--model", default="",
                        help="云端应用ID直调（后台新增的应用用它，先用 --list-models 查看列表）")
    parser.add_argument("--text-file", help="UTF-8 文本文件路径")
    parser.add_argument("--api-key", default="", help="本次临时使用的密钥")
    parser.add_argument("--save-key", default="", help="永久保存个人密钥（保存后自动优先使用）")
    parser.add_argument("--use", choices=["public", "personal"], default="",
                        help="切换密钥模式：public=临时改用公共密钥（个人密钥保留）；personal=切回个人密钥")
    parser.add_argument("--show-key", action="store_true", help="查看当前使用的密钥")
    parser.add_argument("--list-models", action="store_true", help="获取云端应用列表（名称+简介，后台改动立即反映）")
    parser.add_argument("--clear-key", action="store_true", help="清除已保存的个人密钥，回到公共密钥")
    parser.add_argument("--config-path", default=DEFAULT_CONFIG_PATH,
                        help="密钥配置文件路径（默认 ~/.workbuddy/wenzi-runse-config.json，可自定义任意位置）")
    args = parser.parse_args()

    # ---- 密钥管理命令 ----
    if args.save_key:
        key = args.save_key.replace("Bearer", "").strip()
        if not key.startswith("sk-"):
            out({"success": False, "result": "", "message": "密钥格式不对，应以 sk- 开头。"})
            return
        if save_key(key, args.config_path):
            out({"success": True, "result": f"密钥已保存并启用: {mask(key)}，之后各档处理将自动使用你的个人密钥。（明文保存在本机 {args.config_path}，仅限本人设备；说「用公共密钥」可临时切回，个人密钥保留不删除）", "message": "ok"})
        return
    if args.use:
        cfg = load_config(args.config_path)
        saved = str(cfg.get("api_key", "") or "").strip()
        if not saved:
            out({"success": False, "result": "", "message": "还没有保存个人密钥，无法切换。把 sk- 开头的密钥发给 AI 并说「保存润色密钥」即可绑定。"})
            return
        if args.use == "public":
            cfg["mode"] = "public"
            if save_config(cfg, args.config_path):
                out({"success": True, "result": f"已临时切换为公共密钥（每日次数有限）。你的个人密钥 {mask(saved)} 已保留，说「用我的密钥」随时切回。", "message": "ok"})
            return
        # personal：切回个人密钥
        cfg["mode"] = "auto"
        if save_config(cfg, args.config_path):
            out({"success": True, "result": f"已切换为你的个人密钥 {mask(saved)}（不限次使用）。", "message": "ok"})
        return
    if args.clear_key:
        if os.path.exists(args.config_path):
            os.remove(args.config_path)
        out({"success": True, "result": "已彻底删除个人密钥（不可恢复），恢复使用公共密钥（每日次数有限）。只是临时想用公共密钥的话，用「用公共密钥」切换即可，不会删除。", "message": "ok"})
        return
    if args.show_key:
        cfg = load_config(args.config_path)
        saved = str(cfg.get("api_key", "") or "").strip()
        if saved and str(cfg.get("mode", "") or "").strip() != "public":
            out({"success": True, "result": f"当前使用: {mask(saved)}（个人密钥，已保存在 {args.config_path}，不限次）", "message": "ok"})
        else:
            pub = fetch_public_key()
            shown = mask(pub) if pub else "（后台暂未配置）"
            extra = f"（个人密钥 {mask(saved)} 已保留，说「用我的密钥」切回）" if saved else "（每日次数有限）"
            out({"success": True, "result": f"当前使用: {shown}（云端下发的公共密钥）{extra}", "message": "ok"})
        return
    if args.list_models:
        api_key = resolve_key(args)
        if not api_key:
            out({"success": False, "result": "", "models": [], "message": NO_KEY_MSG})
            return
        out(list_models(api_key))
        return

    # ---- 主流程 ----
    if not args.text_file:
        out({"success": False, "result": "", "message": "缺少 --text-file 参数"})
        return
    if not args.model and not args.mode:
        out({"success": False, "result": "", "message": "缺少处理模式：请先运行 --list-models 查看云端应用列表，然后用 --model 应用ID 指定；旧快捷名 --mode flash/pro/pro_plus 仍可用。"})
        return
    if not os.path.exists(args.text_file):
        out({"success": False, "result": "", "message": f"找不到文本文件: {args.text_file}"})
        return

    with open(args.text_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if len(text) < 300:
        out({"success": False, "result": "", "message": "文章不足300字，无法处理；1000字左右效果更佳。"})
        return

    # 应用ID优先级：--model（任意云端应用） > --mode（旧快捷名映射）
    model_id = args.model.strip() or MODELS[args.mode]

    # 密钥优先级：--api-key > 已保存个人密钥 > 云端下发公共密钥
    api_key = resolve_key(args)
    if not api_key:
        out({"success": False, "result": "", "message": NO_KEY_MSG})
        return

    result = call_api(text, model_id, api_key)
    out(result)


if __name__ == "__main__":
    main()
