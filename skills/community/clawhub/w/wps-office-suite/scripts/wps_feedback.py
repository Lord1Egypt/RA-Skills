"""
WPS Office 全家桶 - 反馈入口
打开反馈页面或发送反馈邮件
"""
import sys
import json
import subprocess
import platform
from pathlib import Path
from datetime import datetime


def open_feedback_page() -> dict:
    """打开 SkillHub 反馈页面"""
    try:
        # SkillHub 反馈页面（假设的 URL，实际需替换）
        url = "https://skillhub.cn/feedback"
        if platform.system() == "Windows":
            subprocess.Popen(["start", url], shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", url])
        else:
            subprocess.Popen(["xdg-open", url])
        return {"success": True, "message": "已打开反馈页面"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_feedback_email(skill_id: str = "92007", version: str = "2.1.0") -> dict:
    """生成反馈邮件内容"""
    try:
        # 获取系统信息
        import wps_test
        env_info = wps_test.run_all_checks()

        body = f"""WPS Office 全家桶反馈

--- 基本信息 ---
Skill ID: {skill_id}
版本: {version}
时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}
系统: {platform.system()} {platform.release()}

--- 环境信息 ---
"""
        for check in env_info.get("checks", []):
            msg = check.get("message", "")
            if msg:
                body += f"  {msg}\n"

        body += """
--- 问题描述 ---
（请在此处描述您遇到的问题或建议）


--- 期望行为 ---
（请在此处描述您期望的结果）


--- 复现步骤 ---
1. 
2. 
3. 

"""
        # 打开邮件客户端
        email = "feedback@skillhub.cn"
        subject = f"WPS Office 全家桶 v{version} 反馈"
        mailto = f"mailto:{email}?subject={subject}&body={body}"

        if platform.system() == "Windows":
            subprocess.Popen(["start", mailto], shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", mailto])
        else:
            subprocess.Popen(["xdg-open", mailto])

        return {"success": True, "message": "已打开邮件客户端"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="WPS 反馈入口")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("page", help="打开反馈页面")
    sub.add_parser("email", help="生成反馈邮件")

    args = parser.parse_args()

    if args.command == "page":
        result = open_feedback_page()
    elif args.command == "email":
        result = generate_feedback_email()
    else:
        result = {"success": False, "error": "未知命令"}

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
