#!/usr/bin/env python3
"""
when-clock-skill - WHEN/WHEN Voice 多设备控制入口

支持通过 --device-id 指定不同设备，自动检测设备型号并分发到对应处理模块。
"""
import argparse
import sys
from pathlib import Path
from urllib import error

from when_common import (
    _load_config,
    _resolve_config_path,
    _build_base_url,
    _get_timeout,
    detect_device_type,
    SUPPORTED_MODES,
    ALARM_MODE_CODES,
)


def _find_device_config(config: dict, device_id: str) -> dict:
    """根据 device_id 查找设备配置"""
    devices = config.get("devices", [])

    # 新格式：devices 数组
    for dev in devices:
        if dev.get("id") == device_id:
            return dev

    # 兼容旧格式：顶层 clock_ip
    if "clock_ip" in config and device_id == "default":
        return config

    # default 且 devices 数组非空时，自动选择第一个设备
    if device_id == "default" and devices:
        return devices[0]

    raise ValueError(f"设备 ID '{device_id}' 不存在，请检查 config.json 中的 devices 列表")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="when-clock-skill: WHEN/WHEN Voice 多设备控制入口"
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=SUPPORTED_MODES,
        help="模式: chime, weather, get_alarm, set_alarm, delete_alarm, edit_alarm, set_timer",
    )
    parser.add_argument(
        "--device-id",
        default="default",
        help="设备ID（对应 config.json devices[].id），默认为 default",
    )
    parser.add_argument("--volume", type=int, default=None, help="chime/weather 模式可选：指定音量(1~30)")
    parser.add_argument("--alarm-time", default=None, help="set_alarm 模式必填：闹钟时间，格式 HH:MM 或 HH:MM:SS")
    parser.add_argument(
        "--alarm-mode",
        default=None,
        choices=tuple(ALARM_MODE_CODES.keys()),
        help="set_alarm/edit_alarm 可选：off/once/weekly/workday/restday",
    )
    parser.add_argument("--alarm-week", default=None, help="set_alarm 每周模式可选：星期计划，如 1,2,3,4,5")
    parser.add_argument("--alarm-ring", type=int, default=None, help="铃音编号(1基)")
    parser.add_argument("--alarm-delay", type=int, default=None, help="响铃时长档位(0基)")
    parser.add_argument("--alarm-volume", type=int, default=None, help="set_alarm 可选：音量(1~30)")
    parser.add_argument("--alarm-index", type=int, default=None, help="delete_alarm/edit_alarm 必填：目标闹钟序号（1基）")
    parser.add_argument("--timer-offset", default=None, help="set_timer 必填：多久后提醒，例如: '5m', '1h30m', '90s'")
    parser.add_argument("--timeout", type=float, default=None, help="覆盖超时秒数")
    parser.add_argument("--config", default="config.json", help="配置文件路径，默认 config.json")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    config_path = _resolve_config_path(args.config)

    try:
        config = _load_config(config_path)

        # 根据 device_id 查找设备配置
        device_config = _find_device_config(config, args.device_id)
        base_url = _build_base_url(device_config)
        timeout = _get_timeout(device_config, args.timeout)

        # 检测设备类型
        device_type = detect_device_type(base_url, timeout)

        # 动态导入对应模块并分发
        if device_type == "WHEN Voice":
            from when_voice import run_mode as run_device_mode
        elif device_type == "WHEN":
            from when import run_mode as run_device_mode
        else:
            raise ValueError(f"不支持的设备类型: {device_type}")

        code = run_device_mode(
            mode=args.mode,
            base_url=base_url,
            timeout=timeout,
            config=device_config,
            volume=args.volume,
            alarm_time=args.alarm_time,
            alarm_mode=args.alarm_mode,
            alarm_week=args.alarm_week,
            alarm_ring=args.alarm_ring,
            alarm_delay=args.alarm_delay,
            alarm_volume=args.alarm_volume,
            alarm_index=args.alarm_index,
            timer_offset=args.timer_offset,
        )

        raise SystemExit(code)

    except FileNotFoundError:
        print(f"未找到配置文件，已创建默认配置文件：{config_path}，请先填写 clock_ip 后重试。", file=sys.stderr)
        raise SystemExit(2)
    except (ValueError, KeyError) as exc:
        print(f"参数或响应错误: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except error.HTTPError as exc:
        print(f"HTTP 错误: {exc.code} {exc.reason}", file=sys.stderr)
        raise SystemExit(3)
    except error.URLError as exc:
        print(f"网络错误: {exc.reason}", file=sys.stderr)
        raise SystemExit(4)


if __name__ == "__main__":
    main()
