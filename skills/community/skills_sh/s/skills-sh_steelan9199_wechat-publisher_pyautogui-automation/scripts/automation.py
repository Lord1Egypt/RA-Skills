#!/usr/bin/env python3
"""
PyAutoGUI 自动化操作脚本 - 主入口
支持截图、点击、颜色获取、鼠标控制等功能

输出格式: JSON
错误处理: 非零退出码 + stderr 输出错误信息
"""

import argparse
import json
import sys

# 先导入 utils 并确保依赖
from utils import ensure_dependencies, parse_region, parse_rgb

# 确保依赖已安装
ensure_dependencies()

# 导入各模块
import color
import dialog
import keyboard
import mouse
import screen
import system

# 定义所有支持的操作
ACTIONS = {
    # 截图
    "screenshot": lambda args: screen.screenshot(
        args.output, parse_region(args.region)
    ),
    "screenshot_to_clipboard": lambda args: screen.screenshot_to_clipboard(
        parse_region(args.region)
    ),
    # 鼠标
    "click": lambda args: mouse.click(
        args.x, args.y, args.button, args.clicks, args.interval
    ),
    "double_click": lambda args: mouse.double_click(args.x, args.y, args.button),
    "mouse_down": lambda args: mouse.mouse_down(args.button),
    "mouse_up": lambda args: mouse.mouse_up(args.button),
    "get_mouse_position": lambda args: mouse.get_mouse_position(),
    "move_mouse": lambda args: mouse.move_mouse(args.x, args.y, args.duration),
    "move_mouse_rel": lambda args: mouse.move_mouse_rel(args.x, args.y, args.duration),
    "drag_mouse": lambda args: mouse.drag_mouse(
        args.x, args.y, args.duration, args.button
    ),
    "scroll": lambda args: mouse.scroll(args.amount, args.x, args.y),
    # 颜色
    "get_pixel_color": lambda args: color.get_pixel_color(args.x, args.y),
    "find_color": lambda args: color.find_color(
        parse_rgb(args.rgb), parse_region(args.region), args.tolerance
    ),
    # 系统
    "get_screen_size": lambda args: system.get_screen_size(),
    "get_active_window": lambda args: system.get_active_window(),
    "get_all_windows": lambda args: system.get_all_windows(),
    "sleep": lambda args: system.sleep(args.seconds),
    # 键盘
    "type_text": lambda args: keyboard.type_text(args.text, args.interval),
    "press_key": lambda args: keyboard.press_key(args.key),
    "hotkey": lambda args: keyboard.hotkey(*args.keys.split(",")),
    "copy": lambda args: keyboard.copy(),
    "paste": lambda args: keyboard.paste(),
    "cut": lambda args: keyboard.cut(),
    "select_all": lambda args: keyboard.select_all(),
    "undo": lambda args: keyboard.undo(),
    "redo": lambda args: keyboard.redo(),
    "save": lambda args: keyboard.save(),
    # 图像识别
    "locate_on_screen": lambda args: screen.locate_on_screen(
        args.image, args.confidence, parse_region(args.region)
    ),
    "locate_all_on_screen": lambda args: screen.locate_all_on_screen(
        args.image, args.confidence, parse_region(args.region)
    ),
    "wait_for_image": lambda args: screen.wait_for_image(
        args.image,
        args.confidence,
        parse_region(args.region),
        args.timeout,
        args.wait_interval,
    ),
    "wait_for_image_to_vanish": lambda args: screen.wait_for_image_to_vanish(
        args.image,
        args.confidence,
        parse_region(args.region),
        args.timeout,
        args.wait_interval,
    ),
    # 对话框
    "alert": lambda args: dialog.alert(args.title, args.text, args.button or "OK"),
    "confirm": lambda args: dialog.confirm(
        args.title, args.text, args.buttons.split(",") if args.buttons else None
    ),
    "prompt": lambda args: dialog.prompt(args.title, args.text, args.default or ""),
}


REQUIRED_PARAMS = {
    "click": ["x", "y"],
    "double_click": ["x", "y"],
    "get_pixel_color": ["x", "y"],
    "move_mouse": ["x", "y"],
    "move_mouse_rel": ["x", "y"],
    "drag_mouse": ["x", "y"],
    "scroll": ["amount"],
    "find_color": ["rgb"],
    "sleep": ["seconds"],
    "type_text": ["text"],
    "press_key": ["key"],
    "hotkey": ["keys"],
    "locate_on_screen": ["image"],
    "locate_all_on_screen": ["image"],
    "wait_for_image": ["image"],
    "wait_for_image_to_vanish": ["image"],
}


def main():
    parser = argparse.ArgumentParser(description="PyAutoGUI 自动化操作")
    parser.add_argument("action", choices=list(ACTIONS.keys()), help="要执行的操作")

    # 通用参数
    parser.add_argument("--x", type=int, help="X 坐标")
    parser.add_argument("--y", type=int, help="Y 坐标")
    parser.add_argument("--duration", type=float, default=0.0, help="持续时间")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument(
        "--button", default="left", choices=["left", "right", "middle"], help="鼠标按钮"
    )
    parser.add_argument("--clicks", type=int, default=1, help="点击次数")
    parser.add_argument("--interval", type=float, default=0.0, help="点击间隔")
    parser.add_argument("--rgb", help="目标颜色 RGB，格式: R,G,B")
    parser.add_argument("--tolerance", type=int, default=0, help="颜色容差")
    parser.add_argument("--region", help="搜索区域，格式: x,y,w,h")
    parser.add_argument("--text", help="要输入的文本")
    parser.add_argument("--key", help="按键名称")
    parser.add_argument("--keys", help="组合键，用逗号分隔")
    parser.add_argument("--image", help="图像文件路径")
    parser.add_argument(
        "--confidence", type=float, help="置信度 (0-1)，需要 opencv-python"
    )
    parser.add_argument("--title", default="提示", help="对话框标题")
    parser.add_argument("--buttons", help="按钮列表，用逗号分隔")
    parser.add_argument("--default", default="", help="默认值")
    parser.add_argument("--amount", type=int, help="滚动量")
    parser.add_argument("--seconds", type=float, help="等待秒数")
    parser.add_argument("--timeout", type=float, default=10, help="等待超时时间（秒）")
    parser.add_argument(
        "--wait_interval", type=float, default=0.5, help="等待检查间隔（秒）"
    )

    args = parser.parse_args()

    # 检查必需参数
    if args.action in REQUIRED_PARAMS:
        missing = [p for p in REQUIRED_PARAMS[args.action] if getattr(args, p) is None]
        if missing:
            print(
                f"错误: 操作 '{args.action}' 缺少必需参数: {', '.join(missing)}",
                file=sys.stderr,
            )
            sys.exit(1)

    ensure_dependencies()

    try:
        result = ACTIONS[args.action](args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result.get("success", False):
            sys.exit(1)
    except Exception as e:
        print(
            json.dumps({"success": False, "error": str(e)}, ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
