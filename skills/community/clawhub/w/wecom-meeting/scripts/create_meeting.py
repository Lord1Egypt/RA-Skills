#!/usr/bin/env python3
"""
企业微信会议创建脚本
基于企业微信官方API文档：https://developer.work.weixin.qq.com/document/path/99104

用法:
  python3 create_meeting.py --userid "USERID" --title "TITLE" --time "HH:MM" [选项]
"""

import argparse
import sys
from pathlib import Path

# 添加当前目录到路径，以便导入wecom_meeting_api
sys.path.insert(0, str(Path(__file__).parent))
from wecom_meeting_api import WeComMeeting


def main():
    parser = argparse.ArgumentParser(
        description="创建企业微信预约会议",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  创建简单会议:
    python3 create_meeting.py --userid "WanHuiYi" --title "项目讨论" --time "14:00"

  创建多参会人会议:
    python3 create_meeting.py --userid "WanHuiYi" --title "周会" --time "09:30" --duration 60 --attendees "WanHuiYi,WanLang"

  创建明天的会议:
    python3 create_meeting.py --userid "WanHuiYi" --title "项目评审" --time "10:00" --date "2026-03-07"

  创建带提醒的会议:
    python3 create_meeting.py --userid "WanHuiYi" --title "重要会议" --time "15:00" --remind 15
        """
    )

    parser.add_argument("--userid", required=True, help="发起人UserID（必填）")
    parser.add_argument("--title", required=True, help="会议主题（必填）")
    parser.add_argument("--time", required=True, help="会议开始时间，格式：HH:MM（必填）")
    parser.add_argument("--duration", type=int, default=60, help="会议时长（分钟），默认60")
    parser.add_argument("--date", help="会议日期，格式：YYYY-MM-DD，默认今天")
    parser.add_argument("--attendees", help="参会人列表，用逗号分隔")
    parser.add_argument("--description", default="", help="会议描述")
    parser.add_argument("--remind", type=int, default=2, help="提前提醒（分钟），默认2")

    args = parser.parse_args()

    try:
        # 初始化会议客户端
        meeting = WeComMeeting()

        # 验证时长
        duration_seconds = args.duration * 60
        if duration_seconds < 300:
            print("❌ 会议时长不能少于5分钟")
            sys.exit(1)
        if duration_seconds > 86399:
            print("❌ 会议时长不能超过约24小时")
            sys.exit(1)

        # 解析时间
        try:
            meeting_start = meeting.parse_time(args.time, args.date)
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)

        # 检查时间是否在未来
        current_time = meeting.parse_time("00:00")
        if meeting_start < int(current_time):
            print("❌ 会议开始时间必须在未来")
            sys.exit(1)

        # 构建参会人列表（发起人必须在参会人列表中）
        attendees_list = [args.userid]  # 发起人必须参会

        if args.attendees:
            # 添加其他参会人
            for uid in args.attendees.split(","):
                uid = uid.strip()
                if uid and uid not in attendees_list:  # 避免重复
                    attendees_list.append(uid)

        invitees = {"userid": attendees_list}

        # 构建提醒设置
        remind_seconds = args.remind * 60
        reminders = {
            "is_repeat": 0,
            "remind_before": [remind_seconds]
        }

        # 显示会议信息
        print("=" * 60)
        print("企业微信会议创建")
        print("=" * 60)
        print()

        start_dt = meeting.format_timestamp(meeting_start)
        end_dt = meeting.format_timestamp(meeting_start + duration_seconds)

        print("📋 会议信息:")
        print(f"  主题: {args.title}")
        print(f"  开始时间: {start_dt}")
        print(f"  结束时间: {end_dt}")
        print(f"  时长: {args.duration} 分钟")
        print(f"  发起人: {args.userid}")
        print(f"  参会人: {', '.join(attendees_list)}")
        if args.description:
            print(f"  描述: {args.description}")
        print(f"  提前提醒: {args.remind} 分钟")
        print()

        # 创建会议
        print("🎯 正在创建会议...")

        result = meeting.create_meeting(
            admin_userid=args.userid,
            title=args.title,
            meeting_start=meeting_start,
            meeting_duration=duration_seconds,
            description=args.description,
            invitees=invitees,
            reminders=reminders
        )

        # 显示结果
        print("✅ 会议创建成功!")
        print()
        print("=" * 60)
        print("会议详情")
        print("=" * 60)
        print(f"会议ID: {result.get('meetingid', 'N/A')}")
        print(f"主题: {args.title}")
        print(f"开始时间: {start_dt}")
        print(f"结束时间: {end_dt}")
        print(f"发起人: {args.userid}")
        if args.attendees:
            print(f"参会人: {args.attendees}")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 创建会议失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()