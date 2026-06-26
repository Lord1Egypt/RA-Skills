#!/usr/bin/env python3
"""
获取企业微信会议详情脚本
用法:
  python3 get_meeting.py --meetingid "MEETINGID"
"""

import argparse
import sys
from pathlib import Path
import json

# 添加当前目录到路径，以便导入wecom_meeting_api
sys.path.insert(0, str(Path(__file__).parent))
from wecom_meeting_api import WeComMeeting


def main():
    parser = argparse.ArgumentParser(
        description="获取企业微信会议详情",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  获取会议详情:
    python3 get_meeting.py --meetingid "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA"

  以JSON格式输出:
    python3 get_meeting.py --meetingid "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA" --json
        """
    )

    parser.add_argument("--meetingid", required=True, help="会议ID（必填）")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出")

    args = parser.parse_args()

    try:
        # 初始化会议客户端
        meeting = WeComMeeting()

        # 获取会议详情
        print("=" * 60)
        print("企业微信会议详情")
        print("=" * 60)
        print()

        print(f"正在查询会议 {args.meetingid}...")

        result = meeting.get_meeting(meetingid=args.meetingid)

        # 显示结果
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("✅ 查询成功!")
            print()
            print("=" * 60)
            print("会议信息")
            print("=" * 60)

            meeting_info = result.get("meeting_info", {})

            print(f"会议ID: {meeting_info.get('meetingid', 'N/A')}")
            print(f"主题: {meeting_info.get('title', 'N/A')}")
            print(f"状态: {meeting_info.get('status', 'N/A')}")

            # 时间信息
            meeting_start = meeting_info.get("meeting_start")
            if meeting_start:
                print(f"开始时间: {meeting.format_timestamp(meeting_start)}")

            meeting_end = meeting_info.get("meeting_end")
            if meeting_end:
                print(f"结束时间: {meeting.format_timestamp(meeting_end)}")

            # 参会人信息
            hosts = meeting_info.get("hosts", [])
            if hosts:
                print(f"主持人: {', '.join(host.get('userid', 'N/A') for host in hosts)}")

            invitees = meeting_info.get("invitees", {})
            user_list = invitees.get("user", [])
            if user_list:
                print(f"参会人: {', '.join(user_list)}")

            # 其他信息
            if meeting_info.get("description"):
                print(f"描述: {meeting_info.get('description')}")

            if meeting_info.get("location"):
                print(f"地点: {meeting_info.get('location')}")

            print("=" * 60)

    except Exception as e:
        print(f"\n❌ 查询会议失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()