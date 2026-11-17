#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文章三档处理脚本：调用云端处理API（/bailian/chat 兼容接口）

三档处理（用户选合适档位，可配合使用）：
  flash     微处理——打破AI骨架结构
  pro       中处理——琢字琢句对症下药
  pro_plus  重处理——超级处理，耗时长，最有效去AI味

密钥优先级：--api-key（本次临时） > 本机已保存的个人密钥 > 内置公共密钥
个人密钥保存后永久生效，直到 --clear-key 清除。
"""
import argparse
import json
import os
import sys
import urllib.request

API_URL = "https://1257707270-955niawhww.ap-shanghai.tencentscf.com/bailian/chat"
MODELS_URL = "https://1257707270-955niawhww.ap-shanghai.tencentscf.com/v1/models"
DEFAULT_API_KEY = "REDACTED-SECRET"  # 公共免费共享
MODELS = {
    # 对外档位名（用户使用）
    "flash": "wenzi_runs",      # 微处理——打破AI骨架结构
    "pro": "wenzi_paiban",      # 中处理——琢字琢句对症下药
    "pro_plus": "wenzi_power",  # 重处理——超级处理，耗时长，最有效去AI味
    # 旧档位名兼容
    "runse": "wenzi_runs",
    "paiban": "wenzi_paiban",
    "power": "wenzi_power",
    "both": "wenzi_power",
}
# 三个正式档位（用于 --list-models 展示；后台新增应用后需在 MODELS 和这里同步补充）
CANONICAL_TIERS = {
    "wenzi_runs": "flash（微处理）",
    "wenzi_paiban": "pro（中处理）",
    "wenzi_power": "pro_plus（重处理）",
}
DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".workbuddy", "wenzi-runse-config.json")


def out(payload):
    print(json.dumps(payload, ensure_ascii=False))


def call_api(text, model_id, api_key):
    """调用云端接口，返回统一结构 {"success", "result", "message"}"""
    body = {"text": text, "model": model_id}
    if api_key != DEFAULT_API_KEY:
        body["api_key"] = api_key

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
        # API 返回的业务提示（额度用完、密钥无效等），原样转达用户
        return {"success": False, "result": "", "message": err}
    return {"success": True, "result": str(data.get("result", "") or ""), "message": "ok"}


def list_models(api_key):
    """动态获取云端最新应用列表（/v1/models），后台新增应用后可用此命令查看"""
    req = urllib.request.Request(MODELS_URL, headers={"Authorization": f"Bearer {api_key}"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "result": "", "message": f"获取应用列表失败: {e}"}

    items = data.get("data", []) if isinstance(data, dict) else []
    if not items:
        return {"success": False, "result": "", "message": "云端未返回任何应用"}

    lines = [f"云端最新应用列表（共 {len(items)} 个）："]
    for i, m in enumerate(items, 1):
        mid = str(m.get("id", "") or "")
        name = str(m.get("name", "") or "") or mid
        tier = CANONICAL_TIERS.get(mid)
        suffix = f"，档位名 {tier}" if tier else "（脚本暂未映射档位名，需更新脚本后使用）"
        lines.append(f"{i}. {name}（模型ID: {mid}{suffix}）")
    return {"success": True, "result": "\n".join(lines), "message": "ok"}


def load_saved_key(config_path=DEFAULT_CONFIG_PATH):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return str(json.load(f).get("api_key", "") or "").strip()
    except Exception:
        return ""


def save_key(key, config_path=DEFAULT_CONFIG_PATH):
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        # 以 0600 权限写入，仅限当前用户可读（Windows 下尽力而为）
        fd = os.open(config_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"api_key": key}, f, ensure_ascii=False)
        try:
            os.chmod(config_path, 0o600)
        except Exception:
            pass
        return True
    except Exception as e:
        out({"success": False, "result": "", "message": f"密钥保存失败: {e}"})
        return False


def mask(key):
    return key[:6] + "****" + key[-4:] if len(key) > 12 else "****"


def main():
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=list(MODELS),
                        help="flash=微处理 pro=中处理 pro_plus=重处理（旧名 runse/paiban/power/both 仍可用）")
    parser.add_argument("--text-file", help="UTF-8 文本文件路径")
    parser.add_argument("--api-key", default="", help="本次临时使用的密钥")
    parser.add_argument("--save-key", default="", help="永久保存个人密钥（保存后自动优先使用）")
    parser.add_argument("--show-key", action="store_true", help="查看当前使用的密钥")
    parser.add_argument("--list-models", action="store_true", help="获取云端最新应用列表（后台新增应用后可用此命令查看）")
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
            out({"success": True, "result": f"密钥已保存并启用: {mask(key)}，之后各档处理将自动使用你的个人密钥。（明文保存在本机 {args.config_path}，仅限本人设备，可随时 --clear-key 删除）", "message": "ok"})
        return
    if args.clear_key:
        if os.path.exists(args.config_path):
            os.remove(args.config_path)
        out({"success": True, "result": "已清除个人密钥，恢复使用公共密钥（每日次数有限）。", "message": "ok"})
        return
    if args.show_key:
        saved = load_saved_key(args.config_path)
        out({"success": True, "result": f"当前密钥: {mask(saved) if saved else '公共密钥（每日次数有限）'}", "message": "ok"})
        return
    if args.list_models:
        api_key = args.api_key.replace("Bearer", "").strip() or load_saved_key(args.config_path) or DEFAULT_API_KEY
        out(list_models(api_key))
        return

    # ---- 主流程 ----
    if not args.mode or not args.text_file:
        out({"success": False, "result": "", "message": "缺少 --mode 或 --text-file 参数"})
        return
    if not os.path.exists(args.text_file):
        out({"success": False, "result": "", "message": f"找不到文本文件: {args.text_file}"})
        return

    with open(args.text_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if len(text) < 300:
        out({"success": False, "result": "", "message": "文章不足300字，无法处理；1000字左右效果更佳。"})
        return

    # 密钥优先级：--api-key > 已保存个人密钥 > 公共密钥
    api_key = args.api_key.replace("Bearer", "").strip() or load_saved_key(args.config_path) or DEFAULT_API_KEY

    result = call_api(text, MODELS[args.mode], api_key)
    out(result)


if __name__ == "__main__":
    main()
