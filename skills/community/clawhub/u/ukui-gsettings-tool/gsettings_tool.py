#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


UKUI_CORE_SCHEMAS = [
    "org.ukui.peripherals-keyboard",
    "org.ukui.peripherals-mouse",
    "org.ukui.peripherals-touchpad",
    "org.ukui.peripherals-touchscreen",
    "org.ukui.font-rendering",
    "org.ukui.SettingsDaemon.plugins.media-keys",
    "org.ukui.SettingsDaemon.plugins.power",
    "org.ukui.SettingsDaemon.plugins.sound",
    "org.ukui.SettingsDaemon.plugins.color",
    "org.ukui.SettingsDaemon.plugins.keyboard",
    "org.ukui.SettingsDaemon.plugins.xrandr",
]


def run_gsettings(args_list):
    try:
        result = subprocess.run(
            ["gsettings"] + args_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("错误：系统中未找到 gsettings 命令。", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"gsettings 命令失败: gsettings {' '.join(args_list)}", file=sys.stderr)
        if e.stderr:
            print(e.stderr.strip(), file=sys.stderr)
        sys.exit(1)


def export_schema(schema):
    keys_output = run_gsettings(["list-keys", schema])
    keys = [k for k in keys_output.splitlines() if k.strip()]
    data = {}
    for key in keys:
        value = run_gsettings(["get", schema, key])
        data[key] = value
    return data


def cmd_export(args):
    if not args.schemas:
        print("错误：必须至少指定一个 --schema", file=sys.stderr)
        sys.exit(1)

    result = {}
    for schema in args.schemas:
        result[schema] = export_schema(schema)

    json_str = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json_str, encoding="utf-8")
        print(f"已导出到 {out_path}")
    else:
        print(json_str)


def cmd_export_ukui(args):
    result = {}
    for schema in UKUI_CORE_SCHEMAS:
        try:
            result[schema] = export_schema(schema)
        except SystemExit:
            print(f"警告：schema 不存在或无法访问：{schema}", file=sys.stderr)
            continue

    json_str = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json_str, encoding="utf-8")
        print(f"已导出 UKUI 配置到 {out_path}")
    else:
        print(json_str)


def cmd_apply(args):
    preset_name = args.preset
    script_dir = Path(__file__).resolve().parent
    default_path = script_dir / "presets" / f"{preset_name}.json"
    if args.path:
        preset_path = Path(args.path)
    else:
        preset_path = default_path

    if not preset_path.is_file():
        print(f"错误：未找到 preset 文件：{preset_path}", file=sys.stderr)
        sys.exit(1)

    try:
        content = preset_path.read_text(encoding="utf-8")
        data = json.loads(content)
    except Exception as e:
        print(f"错误：读取或解析 JSON 失败：{preset_path}\n{e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print("错误：preset JSON 顶层必须是 {schema: {key: value}} 的对象。", file=sys.stderr)
        sys.exit(1)

    for schema, kv in data.items():
        if not isinstance(kv, dict):
            print(f"警告：schema {schema} 的值不是对象，已跳过。", file=sys.stderr)
            continue
        for key, value in kv.items():
            if not isinstance(value, str):
                print(
                    f"警告：{schema}::{key} 的值不是字符串（实际是 {type(value)}），已跳过。",
                    file=sys.stderr,
                )
                continue
            print(f"设置 {schema} {key} = {value}")
            run_gsettings(["set", schema, key, value])

    print(f"preset 已应用：{preset_path}")


def cmd_get(args):
    schema = args.schema
    key = args.key
    value = run_gsettings(["get", schema, key])
    print(value)


def cmd_set(args):
    schema = args.schema
    key = args.key
    value = args.value
    print(f"设置 {schema} {key} = {value}")
    run_gsettings(["set", schema, key, value])


def build_parser():
    parser = argparse.ArgumentParser(
        description="gsettings 导出/应用工具（支持 UKUI 预设与单项 get/set）。"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_export = subparsers.add_parser(
        "export", help="导出指定 schema 的全部 key/value 为 JSON"
    )
    p_export.add_argument(
        "--schema",
        dest="schemas",
        action="append",
        required=True,
        help="要导出的 gsettings schema，可重复多次。",
    )
    p_export.add_argument(
        "-o",
        "--output",
        help="输出 JSON 文件路径，不指定则打印到 stdout。",
    )
    p_export.set_defaults(func=cmd_export)

    p_export_ukui = subparsers.add_parser(
        "export-ukui", help="导出 UKUI 相关 schema 的全部 gsettings 配置为 JSON"
    )
    p_export_ukui.add_argument(
        "-o",
        "--output",
        help="输出 JSON 文件路径，不指定则打印到 stdout。",
    )
    p_export_ukui.set_defaults(func=cmd_export_ukui)

    p_apply = subparsers.add_parser(
        "apply", help="从 presets/*.json 读入并批量写入 gsettings"
    )
    p_apply.add_argument(
        "preset",
        help="preset 名称（默认从 presets/<name>.json 读取）",
    )
    p_apply.add_argument(
        "--path",
        help="可选：直接指定 preset JSON 文件路径，优先于名称。",
    )
    p_apply.set_defaults(func=cmd_apply)

    p_get = subparsers.add_parser(
        "get", help="读取单个 schema/key 的 gsettings 值"
    )
    p_get.add_argument("schema", help="gsettings schema 名称，例如 org.ukui.power-manager")
    p_get.add_argument("key", help="键名，例如 brightness-ac")
    p_get.set_defaults(func=cmd_get)

    p_set = subparsers.add_parser(
        "set", help="设置单个 schema/key 的 gsettings 值（值使用 gsettings 语法）"
    )
    p_set.add_argument("schema", help="gsettings schema 名称，例如 org.ukui.power-manager")
    p_set.add_argument("key", help="键名，例如 brightness-ac")
    p_set.add_argument(
        "value",
        help="要设置的值，使用 gsettings 的原始语法，例如 80, true, \"'Adwaita-dark'\" 等。",
    )
    p_set.set_defaults(func=cmd_set)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

