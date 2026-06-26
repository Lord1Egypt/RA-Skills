#!/usr/bin/env python3
"""
企业微信会议取消脚本
用法:
  python3 cancel_meeting.py --userid "USERID" --meetingid "MEETINGID"
"""

import argparse
import sys
from pathlib import Path

# 添加当前目录到路径，以便导入wecom_meeting_api
sys.path.insert(0, str(Path(__file__).parent))
from wecom_meeting_api import WeComMeeting


def main():
    parser = argparse.ArgumentParser(
        description="取消企业微信预约会议",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  取消会议:
    python3 cancel_meeting.py --userid "WanHuiYi" --meetingid "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA"

  强制取消（不确认）:
    python3 cancel_meeting.py --userid "WanHuiYi" --meetingid "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA" --force
        """
    )

    parser.add_argument("--userid", required=True, help="发起人UserID（必填）")
    parser.add_argument("--meetingid", required=True, help="会议ID（必填）")
    parser.add_argument("--force", action="store_true", help="强制取消，不确认")

    args = parser.parse_args()

    try:
        # 初始化会议客户端
        meeting = WeComMeeting()

        # 确认取消
        if not args.force:
            print(f"⚠️  即将取消会议")
            print(f"  会议ID: {args.meetingid}")
            print(f"  发起人: {args.userid}")
            print()
            confirm = input("确认取消？(y/n): ")
            if confirm.lower() != 'y':
                print("已取消操作")
                sys.exit(0)

        # 取消会议
        print("=" * 60)
        print("企业微信会议取消")
        print("=" * 60)
        print()

        print(f"正在取消会议 {args.meetingid}...")

        result = meeting.cancel_meeting(
            meetingid=args.meetingid,
            admin_userid=args.userid
        )

        # 显示结果
        print("✅ 会议取消成功!")
        print()
        print("=" * 60)
        print(f"会议ID: {args.meetingid}")
        print(f"发起人: {args.userid}")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 取消会议失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()