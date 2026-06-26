#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys


def load_devices(server: str):
    result = subprocess.run(
        ["mcporter", "call", f"{server}.list_user_devices", "--output", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout or "无法获取设备列表\n")
        raise SystemExit(result.returncode)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"设备列表 JSON 解析失败: {exc}\n")
        raise SystemExit(1)
    if not isinstance(data, list):
        sys.stderr.write("设备列表返回值不是数组\n")
        raise SystemExit(1)
    return data


def match_devices(devices, device_name: str, include_offline: bool):
    if not include_offline:
        online = [item for item in devices if item.get("online_status") is True]
        candidates = online or devices
    else:
        candidates = devices

    exact = [item for item in candidates if item.get("device_name") == device_name]
    if exact:
        return exact

    return [
        item for item in candidates
        if device_name in str(item.get("device_name", ""))
    ]


def emit_nul_payload(payload):
    values = (
        payload["device_name"],
        payload["cuid"],
        payload["client_id"],
    )
    for value in values:
        sys.stdout.buffer.write(str(value).encode("utf-8"))
        sys.stdout.buffer.write(b"\0")


def main():
    parser = argparse.ArgumentParser(description="按设备名解析小度设备标识")
    parser.add_argument("--server", default="xiaodu")
    parser.add_argument("--device-name")
    parser.add_argument("--cuid")
    parser.add_argument("--client-id")
    parser.add_argument("--include-offline", action="store_true")
    parser.add_argument("--format", choices=("json", "nul"), default="json")
    args = parser.parse_args()

    if args.cuid and args.client_id and not args.device_name:
        resolved = {
            "device_name": "",
            "cuid": args.cuid,
            "client_id": args.client_id,
        }
    else:
        if not args.device_name:
            sys.stderr.write("必须提供 --device-name，或者同时提供 --cuid 和 --client-id\n")
            raise SystemExit(1)
        devices = load_devices(args.server)
        matched = match_devices(devices, args.device_name, args.include_offline)
        if not matched:
            sys.stderr.write(f"未找到设备: {args.device_name}\n")
            raise SystemExit(1)
        if len(matched) > 1:
            sys.stderr.write(f"设备名不唯一: {args.device_name}\n")
            for item in matched:
                sys.stderr.write(
                    f"- {item.get('device_name')} | cuid={item.get('cuid')} | client_id={item.get('client_id')}\n"
                )
            raise SystemExit(2)
        resolved = matched[0]

    payload = {
        "device_name": resolved.get("device_name", ""),
        "cuid": resolved.get("cuid", ""),
        "client_id": resolved.get("client_id", ""),
        "online_status": resolved.get("online_status"),
        "location": resolved.get("location"),
    }
    if not payload["cuid"] or not payload["client_id"]:
        sys.stderr.write("解析结果缺少 cuid 或 client_id\n")
        raise SystemExit(1)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False))
        return

    emit_nul_payload(payload)


if __name__ == "__main__":
    main()
