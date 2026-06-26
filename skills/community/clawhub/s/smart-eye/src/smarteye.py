"""
smarteye.py - SmartEye Skill 主入口

直接运行时执行测试；被 import 时暴露 handle() 函数。
"""

import logging
from pathlib import Path

# ---- 动作映射 ----

_ACTIONS = {
    # 看
    "看看":        "snapshot",      # 抽帧并返回路径（供 Agent AI 分析）
    "分析":        "snapshot",      # 同上，分析画面内容
    "分析一下":    "snapshot",      # 同上
    "画面":        "snapshot",      # 同上
    "截图":        "snapshot",      # 抽帧保存
    "调阅":        "open_vlc",      # VLC 打开实时流
    # 动
    "点头":    "nod",
    "摇头":    "shake",
    "上转":    "move_up",
    "下转":    "move_down",
    "左转":    "move_left",
    "右转":    "move_right",
    "放大":    "zoom_in",
    "缩小":   "zoom_out",
    "居中":    "home",
    "停止":    "stop",
    # 知
    "状态":    "get_status",
    "列表":    "list_cameras",
    "有哪些摄像头": "list_cameras",
}


def _extract_action(text: str):
    """从消息中分离摄像头名称和动作。动作从后往前匹配。"""
    sorted_actions = sorted(_ACTIONS.keys(), key=len, reverse=True)
    for action in sorted_actions:
        if text.endswith(action):
            camera_name = text[:-len(action)].strip()
            return camera_name, action
    if text in _ACTIONS:
        return None, text
    return None, None


def parse_and_execute(message: str, devices: dict = None) -> str:
    """解析用户消息，执行对应动作，返回结果描述。"""
    from config import load_devices, find_camera, list_cameras

    if devices is None:
        devices = load_devices()

    text = message.strip()

    # 列出所有摄像头
    if text in ("有哪些摄像头", "列表", "摄像头列表", "list"):
        lines = list_cameras(devices)
        if not lines:
            return "尚未配置任何摄像头，请编辑 camera-devices.json 添加设备。"
        return "已配置的摄像头：\n" + "\n".join(lines)

    camera_name, action = _extract_action(text)
    if action is None:
        available = " / ".join(sorted(_ACTIONS.keys()))
        return f"未识别动作。可用动作：{available}"

    camera_cfg = find_camera(devices, camera_name)
    if camera_cfg is None:
        return f"未找到名为「{camera_name or '默认'}」的摄像头。"

    from protocol.brands import get_brand, BRANDS
    brand_cls = get_brand(camera_cfg.get("brand", ""))
    if brand_cls is None:
        return f"不支持的品牌：{camera_cfg.get('brand')}。已支持：{', '.join(BRANDS.keys())}"

    try:
        camera = brand_cls(camera_cfg)
    except Exception as e:
        return f"连接摄像头失败：{e}"

    method_name = _ACTIONS.get(action, action)
    if not hasattr(camera, method_name):
        return f"摄像头 {camera_cfg['id']} 不支持动作「{action}」。"

    try:
        method = getattr(camera, method_name)
        aliases = camera_cfg.get("aliases", [camera_cfg["id"]])

        # 截图类动作（截图、看看、分析、分析一下、画面）：返回文件路径
        if action in ("截图", "看看", "分析", "分析一下", "画面"):
            path = method()
            return f"✅ {aliases[0]} 截图已保存：{path}"

        # 调阅：VLC 打开实时流
        if action == "调阅":
            ok = method()
            if ok:
                return f"✅ {aliases[0]} 已用 VLC 打开实时流"
            return f"⚠️ {aliases[0]} 未配置 VLC 路径，无法打开。请在 camera-devices.json 中添加 vlc_path 字段。"

        # 普通 PTZ 动作
        method()
        return f"✅ {aliases[0]} 执行「{action}」完成。"
    except Exception as e:
        return f"❌ 执行「{action}」失败：{e}"


# ---- OpenClaw Skill 入口 ----

def handle(message: str) -> str:
    """OpenClaw Skill 入口函数。"""
    try:
        text = message.strip()

        # 检测"帮我找XX"类查询 → 多摄像头并行搜索
        term, _ = _parse_find_query(text)
        if term:
            return find_in_cameras(term)

        return parse_and_execute(text)
    except Exception as e:
        logging.exception("SmartEye skill error")
        return f"SmartEye 出错：{e}"


def _parse_find_query(text: str):
    """
    从自然语言中解析出搜索目标。
    支持：
      "帮我找钥匙" → "钥匙"
      "钥匙在哪里" → "钥匙"
      "帮我看看有没有猫" → "猫"
      "有没有手机" → "手机"
    返回 (search_term, matched_pattern)
    """
    import re
    patterns = [
        r"帮我找(.+?)$",
        r"找一下(.+?)$",
        r"(.+?)在哪里",
        r"有没有(.+?)$",
        r"在不在(.+?)$",
        r"帮我看看有没有(.+?)$",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            term = m.group(1).strip()
            # 去掉常见前缀，让搜索词更精准
            term = re.sub(r"^(?:我的|那只|一个|the|a|这个)(?=\S)", "", term, flags=re.IGNORECASE).strip()
            return term, pat
    return None, None


def find_in_cameras(search_term: str, devices: dict = None) -> str:
    """
    并行对所有已配置摄像头截图，返回截图路径列表供 Agent AI 分析。
    Returns:
        描述性的多行文本，包含截图路径和提示 Agent 如何分析
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from protocol.brands import get_brand
    from config import load_devices
    import os
    from pathlib import Path

    if devices is None:
        devices = load_devices()

    cameras = devices.get("cameras", [])
    if not cameras:
        return "没有任何已配置的摄像头，请先在 camera-devices.json 中添加设备。"

    MAX_CAMERAS = 8

    results = []   # (camera_id, camera_alias, snapshot_path, error_msg)

    def _snapshot_one(cfg: dict):
        try:
            brand_cls = get_brand(cfg.get("brand", ""))
            if brand_cls is None:
                return cfg["id"], cfg["aliases"][0] if cfg.get("aliases") else cfg["id"], None, f"不支持的品牌: {cfg.get('brand')}"
            cam = brand_cls(cfg)
            save_dir = Path(__file__).parent.parent / "snapshots"
            path = cam.snapshot(str(save_dir))
            return cfg["id"], cfg["aliases"][0] if cfg.get("aliases") else cfg["id"], path, None
        except Exception as e:
            return cfg["id"], cfg["aliases"][0] if cfg.get("aliases") else cfg["id"], None, str(e)

    with ThreadPoolExecutor(max_workers=MAX_CAMERAS) as pool:
        futures = {pool.submit(_snapshot_one, c): c for c in cameras}
        for f in as_completed(futures):
            results.append(f.result())

    # 整理输出
    lines = [f"已对 {len(cameras)} 个摄像头完成截图，开始 AI 分析寻找「{search_term}」...\n"]
    has_any_snapshot = False
    for cid, alias, path, err in sorted(results, key=lambda x: x[0]):
        if err:
            lines.append(f"  [{alias}] 出错：{err}")
        else:
            lines.append(f"  [{alias}] {path}")
            has_any_snapshot = True

    if not has_any_snapshot:
        return "\n".join(lines) + "\n所有摄像头截图均失败，无法继续分析。"

    # 构建分析指令，引导 Agent 在下一轮用 image tool 分析
    snapshot_list = "\n".join(
        f"- [{alias}] {path}" for _, alias, path, _ in sorted(results, key=lambda x: x[0]) if path
    )
    return (
        f"已对 {len(cameras)} 个摄像头完成截图，正在寻找「{search_term}」...\n\n"
        f"{snapshot_list}\n\n"
        f"请使用 image tool 同时分析以上截图（多图模式），\n"
        f"判断「{search_term}」出现在哪张图中。\n"
        f"找到后返回：摄像头名称 + 截图路径 + 在图中的大概位置。\n"
        f"如果都没找到，也请明确告知。"
    )


# ---- 直接运行：执行测试 ----
if __name__ == "__main__":
    print("=== SmartEye 内置测试 ===\n")

    from config import load_devices, find_camera, list_cameras
    from protocol.brands import get_brand, BRANDS

    devices = load_devices()
    print(f"加载了 {len(devices.get('cameras', []))} 个摄像头")
    print("摄像头列表:")
    for line in list_cameras(devices):
        print(" ", line)

    print(f"\n已注册品牌: {list(BRANDS.keys())}")

    test_inputs = [
        "tplink点头",
        "建国路摄像头摇头",
        "华为放大",
        "摄像头停止",
        "有哪些摄像头",
    ]
    print("\n动作解析:")
    for inp in test_inputs:
        cam, action = _extract_action(inp)
        print(f"  「{inp}」→ cam={cam!r}  action={action!r}")

    print("\n执行测试:")
    for inp in test_inputs:
        result = parse_and_execute(inp, devices)
        print(f"  「{inp}」→ {result[:80]}")

    print("\n测试完成!")
