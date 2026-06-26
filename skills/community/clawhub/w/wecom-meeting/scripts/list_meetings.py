#!/usr/bin/env python3
"""
获取企业微信成员会议列表脚本
用法:
  python3 list_meetings.py --userid "USERID"
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
        description="获取企业微信成员会议列表",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  获取成员的会议列表:
    python3 list_meetings.py --userid "WanHuiYi"

  以JSON格式输出:
    python3 list_meetings.py --userid "WanHuiYi" --json
        """
    )

    parser.add_argument("--userid", required=True, help="成员UserID（必填）")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出")

    args = parser.parse_args()

    try:
        # 初始化会议客户端
        meeting = WeComMeeting()

        # 获取会议列表
        print("=" * 60)
        print("企业微信会议列表")
        print("=" * 60)
        print()

        print(f"正在查询 {args.userid} 的会议...")

        result = meeting.get_user_meetings(userid=args.userid)

        # 显示结果
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("✅ 查询成功!")
            print()
            print("=" * 60)

            meeting_ids = result.get("meetingid_list", [])

            if not meeting_ids:
                print(f"📭 {args.userid} 没有会议")
            else:
                print(f"📋 {args.userid} 的会议列表:")
                print()
                print(f"共 {len(meeting_ids)} 个会议")
                print()
                for i, meeting_id in enumerate(meeting_ids, 1):
                    print(f"{i}. {meeting_id}")

            print("=" * 60)

    except Exception as e:
        print(f"\n❌ 查询会议列表失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()