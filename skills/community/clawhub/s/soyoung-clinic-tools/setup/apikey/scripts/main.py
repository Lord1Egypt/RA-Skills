#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apikey — API Key、主人绑定与位置管理。"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from lib.soyoung_runtime import (  # noqa: E402
    SoyoungRuntimeError,
    audit_event,
    build_binding,
    build_context_from_args,
    delete_api_key,
    delete_binding,
    ensure_direct_message,
    ensure_owner,
    format_binding_summary,
    get_state_paths,
    iso_now,
    load_api_key,
    load_binding,
    load_location,
    DEFAULT_API_BASE_URL,
    mask_api_key,
    read_api_base_url,
    read_debug_mode,
    reset_api_base_url,
    save_api_key,
    save_binding,
    save_location,
    write_api_base_url,
    write_debug_mode,
)


API_KEY_WEBSITE = "https://www.soyoung.com/loginOpenClaw"


def print_runtime_error(exc: SoyoungRuntimeError) -> None:
    print(str(exc))


def verify_api_key(api_key: str | None) -> bool:
    return bool(api_key) and len(api_key) >= 10


def get_first_time_guide() -> str:
    return f"""🔐 **新氧青春诊所 API Key 配置**

📋 获取步骤：
1. 打开浏览器访问：{API_KEY_WEBSITE}
2. 登录账号，页面会显示 API Key，复制它
3. 仅在与主人私聊中发送：「配置新氧 API Key 为 xxx」

🔒 安全说明：
• API Key 按 workspace 单独保存，不再与其他 agent 共享
• 首次配置会自动把当前私聊发送者绑定为 API Key 主人
• API Key 绝不能发送到多人群聊
• 预约相关高风险操作仅允许主人本人执行，或在群聊中由主人审批

💡 配置完成后，可在群聊中说「新氧配置好了吗」确认是否生效"""


def clear_workspace_state(paths) -> None:
    if paths.location_file.exists():
        paths.location_file.unlink()
    if paths.pending_dir.exists():
        shutil.rmtree(paths.pending_dir)


def require_owner_direct_context(args, operation_name: str):
    ctx = build_context_from_args(args, require=True)
    ensure_direct_message(ctx, operation_name)
    binding = load_binding(get_state_paths(ctx.workspace_key))
    if not binding:
        raise SoyoungRuntimeError("❌ 当前 workspace 尚未绑定 API Key 主人。")
    ensure_owner(ctx, binding, operation_name)
    return ctx, binding


def main():
    parser = argparse.ArgumentParser(description="apikey — API Key 与主人绑定管理")
    parser.add_argument("--workspace-key")
    parser.add_argument("--chat-type")
    parser.add_argument("--chat-id")
    parser.add_argument("--message-id")
    parser.add_argument("--sender-open-id")
    parser.add_argument("--sender-name")
    parser.add_argument("--tenant-key")
    parser.add_argument("--mention-open-id", action="append", default=[])

    parser.add_argument("--save-key", type=str)
    parser.add_argument("--delete-key", action="store_true")
    parser.add_argument("--verify-key", action="store_true")
    parser.add_argument("--check-key", action="store_true")
    parser.add_argument("--show-owner", action="store_true")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--guide", action="store_true")
    parser.add_argument("--config-status", action="store_true")
    parser.add_argument("--save-location", action="store_true")
    parser.add_argument("--get-location", action="store_true")
    parser.add_argument("--debug-on", action="store_true")
    parser.add_argument("--debug-off", action="store_true")
    parser.add_argument("--set-api-url", type=str)
    parser.add_argument("--reset-api-url", action="store_true")
    parser.add_argument("--city", type=str)
    parser.add_argument("--district", type=str)
    parser.add_argument("--street", type=str)
    args = parser.parse_args()

    if args.guide:
        print(get_first_time_guide())
        return

    try:
        paths = get_state_paths(args.workspace_key)

        if args.config_status:
            binding = load_binding(paths)
            api_key = load_api_key(paths)
            current_url = read_api_base_url(paths)
            debug_on = read_debug_mode(paths)
            lines = ["📋 **新氧青春诊所工具集 — 当前配置状态**", ""]
            if binding and api_key:
                lines += [
                    "• API Key：✅ 已配置",
                    f"• 主人：{binding.get('ownerName') or binding.get('ownerOpenId', '未知')}",
                    f"• 绑定时间：{binding.get('boundAt', '未知')}",
                ]
            else:
                lines += [
                    "• API Key：❌ 未配置",
                    "• 提示：请由主人在与机器人私聊中说「配置新氧 API Key 为 xxx」",
                ]
            lines += [
                f"• 接口地址：{current_url}",
                f"• 调试模式：{'✅ 开启（显示 req_id / 接口耗时 / 脚本总耗时）' if debug_on else '关闭（说「新氧青春 clinic 开启调试模式」可开启）'}",
            ]
            print("\n".join(lines))
            return

        if args.show_owner:
            ctx, binding = require_owner_direct_context(args, "查看主人绑定")
            audit_event(paths, "binding_viewed", {"senderOpenId": ctx.sender_open_id})
            print("✅ 当前 workspace 已绑定 API Key 主人\n\n" + format_binding_summary(binding))
            return

        if args.check_key:
            ctx, binding = require_owner_direct_context(args, "查看 API Key 状态")
            if not args.confirm:
                print("⏸️ NEED_CONFIRM:check_key")
                return
            api_key = load_api_key(paths)
            if not api_key:
                print("⚠️ API Key 未配置\n\n请由主人在私聊中重新配置")
                return
            audit_event(paths, "api_key_checked", {"senderOpenId": ctx.sender_open_id})
            print(
                "✅ API Key 已配置\n\n"
                f"• 工作区：{paths.workspace_key}\n"
                f"• 主人：{binding.get('ownerName') or binding.get('ownerOpenId')}\n"
                f"• 预览：{mask_api_key(api_key)}"
            )
            return

        if args.save_key:
            ctx = build_context_from_args(args, require=True)
            ensure_direct_message(ctx, "配置 API Key")
            binding = load_binding(paths)
            existing_key = load_api_key(paths)
            if binding:
                ensure_owner(ctx, binding, "替换 API Key")
            if existing_key and not args.confirm:
                print("⏸️ NEED_CONFIRM:replace_key")
                return
            save_api_key(paths, args.save_key)
            if binding:
                binding["ownerName"] = ctx.sender_name or binding.get("ownerName")
                binding["tenantKey"] = ctx.tenant_key or binding.get("tenantKey")
                binding["apiKeyMasked"] = mask_api_key(args.save_key)
                binding["apiKeyStoredAt"] = iso_now()
            else:
                binding = build_binding(ctx=ctx, api_key=args.save_key)
            save_binding(paths, binding)
            audit_event(
                paths,
                "api_key_saved",
                {
                    "senderOpenId": ctx.sender_open_id,
                    "ownerOpenId": binding.get("ownerOpenId"),
                    "replaced": bool(existing_key),
                },
            )
            word = "替换" if existing_key else "保存并绑定"
            print(
                f"✅ API Key 已{word}\n\n"
                f"• workspace：{paths.workspace_key}\n"
                f"• 主人：{binding.get('ownerName') or binding.get('ownerOpenId')}\n"
                f"• 预览：{binding.get('apiKeyMasked')}\n\n"
                "后续高风险预约操作仅允许主人本人私聊执行，或在群聊中经主人二次确认后执行。\n"
                "💡 可在群聊中说「新氧配置好了吗」确认配置是否对群聊生效。"
            )
            return

        if args.delete_key:
            ctx, binding = require_owner_direct_context(args, "删除 API Key")
            if not args.confirm:
                print("⏸️ NEED_CONFIRM:delete_key")
                return
            existed = delete_api_key(paths)
            delete_binding(paths)
            clear_workspace_state(paths)
            audit_event(
                paths,
                "api_key_deleted",
                {"senderOpenId": ctx.sender_open_id, "ownerOpenId": binding.get("ownerOpenId")},
            )
            if existed:
                print("✅ API Key、主人绑定和待审批记录已删除\n⚠️ 预约和项目查询功能现已不可用，需由主人重新私聊配置")
            else:
                print("⚠️ 未找到已保存的 API Key，但已清理主人绑定和审批状态")
            return

        if args.verify_key:
            ctx, binding = require_owner_direct_context(args, "验证 API Key")
            api_key = load_api_key(paths)
            audit_event(paths, "api_key_verified", {"senderOpenId": ctx.sender_open_id})
            if api_key and verify_api_key(api_key):
                print(
                    "✅ API Key 格式有效\n\n"
                    f"• 主人：{binding.get('ownerName') or binding.get('ownerOpenId')}\n"
                    f"• 预览：{mask_api_key(api_key)}"
                )
            else:
                print("❌ API Key 无效或未配置")
            return

        if args.save_location:
            if not args.city:
                print("❌ 缺少参数：--city（必填）")
                return
            ctx, binding = require_owner_direct_context(args, "保存位置")
            location = save_location(
                paths,
                city=args.city,
                district=args.district,
                street=args.street,
                updated_by_open_id=ctx.sender_open_id,
                updated_by_name=ctx.sender_name,
            )
            desc = args.city + (f" {args.district}" if args.district else "") + (f" {args.street}" if args.street else "")
            audit_event(
                paths,
                "location_saved",
                {
                    "senderOpenId": ctx.sender_open_id,
                    "ownerOpenId": binding.get("ownerOpenId"),
                    "location": desc,
                },
            )
            print(
                f"✅ 位置已保存：{desc}\n"
                f"🕐 更新时间：{location.get('updatedAt')}\n"
                f"👤 主人：{binding.get('ownerName') or binding.get('ownerOpenId')}"
            )
            return

        if args.get_location:
            ctx, binding = require_owner_direct_context(args, "查看已保存位置")
            location = load_location(paths)
            if not location:
                print("⚠️ 尚未保存位置信息\n\n请由主人在私聊中说「我在 XX 市 XX 区」")
                return
            parts = [location.get("city", "")]
            if location.get("district"):
                parts.append(location["district"])
            if location.get("street"):
                parts.append(location["street"])
            audit_event(paths, "location_viewed", {"senderOpenId": ctx.sender_open_id})
            print(
                f"📍 已保存位置：{' '.join([p for p in parts if p])}\n"
                f"🕐 更新时间：{location.get('updatedAt', '')}\n"
                f"👤 主人：{binding.get('ownerName') or binding.get('ownerOpenId')}"
            )
            return

        if args.set_api_url or args.reset_api_url:
            ctx, _ = require_owner_direct_context(args, "配置接口地址")
            if args.reset_api_url:
                reset_api_base_url(paths)
                audit_event(paths, "api_base_url_changed", {"senderOpenId": ctx.sender_open_id, "url": "reset"})
                print(
                    f"✅ 接口地址已重置为默认值\n\n"
                    f"• 当前地址：{DEFAULT_API_BASE_URL}"
                )
            else:
                url = args.set_api_url
                if not url.startswith("https://"):
                    print(
                        "❌ 地址格式无效：接口地址必须以 https:// 开头（不允许 http:// 明文传输）"
                    )
                    return
                write_api_base_url(paths, url)
                audit_event(paths, "api_base_url_changed", {"senderOpenId": ctx.sender_open_id, "url": url})
                print(
                    f"✅ 接口地址已更新\n\n"
                    f"• 新地址：{url}\n"
                    f"• 默认地址：{DEFAULT_API_BASE_URL}\n\n"
                    "恢复默认请说：「重置新氧接口地址」"
                )
            return

        if args.debug_on or args.debug_off:
            ctx, _ = require_owner_direct_context(args, "切换调试模式")
            enabled = args.debug_on
            write_debug_mode(paths, enabled)
            audit_event(paths, "debug_mode_changed", {"senderOpenId": ctx.sender_open_id, "enabled": enabled})
            if enabled:
                print(
                    "✅ 调试模式已开启\n\n"
                    "后续每次请求，会话中都会显示 req_id、接口耗时和脚本总耗时。\n"
                    "关闭请说：「新氧青春 clinic 关闭调试模式」"
                )
            else:
                print(
                    "✅ 调试模式已关闭\n\n"
                    "req_id 仍会发给后端，但不再展示在会话中。\n"
                    "重新开启请说：「新氧青春 clinic 开启调试模式」"
                )
            return

        parser.print_help()
    except SoyoungRuntimeError as exc:
        print_runtime_error(exc)


if __name__ == "__main__":
    main()
