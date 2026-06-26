"""
邮件ID查询工具 - 通过邮件ID快速定位原文件

Usage:
    python3 -m smart_email get-email --id <email_id>
    python3 -m smart_email get-email qq_20250321_143022_abc123

API Usage:
    from smart_email.utils import get_email_by_id
    result = get_email_by_id("qq_20250321_143022_abc123")
"""
import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Tuple


def parse_email_id(email_id: str) -> Tuple[str, str, str]:
    """
    解析邮件ID，提取邮箱类型、日期和目录名

    支持两种格式：
    - 新格式: {provider}_{timestamp} (如 qq_20250321_143022)
    - 旧格式: {provider}_{timestamp}_{subject}_{msg_id_short} (如 qq_20250321_143022_abc123_xyz)

    Args:
        email_id: 邮件ID

    Returns:
        (provider, date_str, folder_name)
        如 ("qq", "2025-03-21", "qq_20250321_143022")

    Raises:
        ValueError: 如果ID格式不正确
    """
    if not email_id:
        raise ValueError("邮件ID不能为空")

    # 清理ID（移除可能的方括号）
    email_id = email_id.strip("[]")

    # 优先尝试新格式: {provider}_{YYYYMMDD}_{HHMMSS}
    # 新格式: qq_20250321_143022
    new_pattern = r'^([a-zA-Z0-9]+)_(\d{8})_(\d{6})$'
    new_match = re.match(new_pattern, email_id)
    
    if new_match:
        provider = new_match.group(1)
        date_compact = new_match.group(2)  # 20250321

        # 转换日期格式: 20250321 -> 2025-03-21
        try:
            year = date_compact[:4]
            month = date_compact[4:6]
            day = date_compact[6:8]
            date_str = f"{year}-{month}-{day}"
        except (IndexError, ValueError):
            raise ValueError(f"日期格式错误: {date_compact}")

        return provider, date_str, email_id

    # 兼容旧格式: {provider}_{YYYYMMDD}_{HHMMSS}_{subject}_{msg_id_short}
    # 旧格式: qq_20250321_143022_subject_msgid
    # 由于 subject 可能包含下划线，尝试找到时间戳部分 (YYYYMMDD_HHMMSS)
    # 然后取其前面的 provider 和后面的内容
    old_pattern = r'^([a-zA-Z0-9]+)_(\d{8})_(\d{6})_(.+)$'
    old_match = re.match(old_pattern, email_id)

    if old_match:
        provider = old_match.group(1)
        date_compact = old_match.group(2)  # 20250321
        suffix = old_match.group(4)        # subject_msg_id_short

        # 转换日期格式: 20250321 -> 2025-03-21
        try:
            year = date_compact[:4]
            month = date_compact[4:6]
            day = date_compact[6:8]
            date_str = f"{year}-{month}-{day}"
        except (IndexError, ValueError):
            raise ValueError(f"日期格式错误: {date_compact}")

        return provider, date_str, email_id

    # 无法解析
    raise ValueError(
        f"邮件ID格式错误: {email_id}\n"
        f"支持格式:\n"
        f"  新格式: {{provider}}_{{YYYYMMDD}}_{{HHMMSS}}\n"
        f"  旧格式: {{provider}}_{{YYYYMMDD}}_{{HHMMSS}}_{{subject}}_{{msg_id}}\n"
        f"例如: qq_20250321_143022"
    )


def get_base_path() -> Path:
    """获取smart-email-data根目录"""
    # 优先从环境变量读取
    if 'SMART_EMAIL_DATA_PATH' in os.environ:
        return Path(os.environ['SMART_EMAIL_DATA_PATH'])

    # 默认路径
    default_path = Path.home() / '.openclaw' / 'workspace' / 'smart-email-data'
    return default_path


def get_email_by_id(email_id: str, test_mode: bool = False) -> Dict:
    """
    通过邮件ID获取邮件文件路径

    Args:
        email_id: 邮件ID，如 "qq_20250321_143022_abc123"
        test_mode: 是否查询测试目录

    Returns:
        {
            "found": bool,
            "email_id": str,
            "paths": {
                "eml": str or None,
                "md": str or None,
                "attachments_dir": str or None
            },
            "metadata": {
                "provider": str,
                "date": str,
                "folder_name": str
            },
            "error": str or None
        }
    """
    result = {
        "found": False,
        "email_id": email_id,
        "paths": {
            "eml": None,
            "md": None,
            "attachments_dir": None
        },
        "metadata": {
            "provider": None,
            "date": None,
            "folder_name": None
        },
        "error": None
    }

    try:
        # 解析ID
        provider, date_str, folder_name = parse_email_id(email_id)
        result["metadata"]["provider"] = provider
        result["metadata"]["date"] = date_str
        result["metadata"]["folder_name"] = folder_name

        # 构建基础路径
        base_path = get_base_path()
        if test_mode:
            mail_archives = base_path / "tmp" / "mail-archives"
        else:
            mail_archives = base_path / "mail-archives"

        # 构建邮件目录路径
        email_dir = mail_archives / date_str / folder_name

        # 检查目录是否存在
        if not email_dir.exists():
            # 尝试在测试目录中查找
            if not test_mode:
                test_mail_archives = base_path / "tmp" / "mail-archives"
                test_email_dir = test_mail_archives / date_str / folder_name
                if test_email_dir.exists():
                    email_dir = test_email_dir
                else:
                    result["error"] = f"邮件目录不存在: {email_dir}"
                    return result
            else:
                result["error"] = f"邮件目录不存在: {email_dir}"
                return result

        # 检查各文件是否存在
        eml_path = email_dir / "email.eml"
        md_path = email_dir / "email.md"
        attachments_dir = email_dir / "attachments"

        if eml_path.exists():
            result["paths"]["eml"] = str(eml_path)

        if md_path.exists():
            result["paths"]["md"] = str(md_path)

        if attachments_dir.exists() and attachments_dir.is_dir():
            result["paths"]["attachments_dir"] = str(attachments_dir)

        # 判断是否找到邮件（至少要有eml或md文件）
        if result["paths"]["eml"] or result["paths"]["md"]:
            result["found"] = True
        else:
            result["error"] = f"邮件目录存在，但未找到邮件文件: {email_dir}"

    except ValueError as e:
        result["error"] = str(e)
    except Exception as e:
        result["error"] = f"查询失败: {str(e)}"

    return result


def format_output(result: Dict, format_type: str = "json") -> str:
    """格式化输出结果"""
    if format_type == "json":
        return json.dumps(result, indent=2, ensure_ascii=False)

    elif format_type == "text":
        lines = []
        lines.append(f"邮件ID: {result['email_id']}")
        lines.append(f"查找结果: {'✅ 找到' if result['found'] else '❌ 未找到'}")

        if result['error']:
            lines.append(f"错误: {result['error']}")

        if result['found']:
            lines.append("")
            lines.append("文件路径:")
            if result['paths']['eml']:
                lines.append(f"  📧 EML: {result['paths']['eml']}")
            if result['paths']['md']:
                lines.append(f"  📝 MD:  {result['paths']['md']}")
            if result['paths']['attachments_dir']:
                lines.append(f"  📎 附件: {result['paths']['attachments_dir']}")

            lines.append("")
            lines.append("元数据:")
            lines.append(f"  邮箱类型: {result['metadata']['provider']}")
            lines.append(f"  日期: {result['metadata']['date']}")
            lines.append(f"  目录名: {result['metadata']['folder_name']}")

        return "\n".join(lines)

    else:
        return json.dumps(result, indent=2, ensure_ascii=False)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="通过邮件ID查询原文件路径",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 -m smart_email get-email --id qq_20250321_143022_abc123
  python3 -m smart_email get-email qq_20250321_143022_abc123 --format text
  python3 -m smart_email get-email qq_20250321_143022_abc123 --test-mode
        """
    )

    parser.add_argument(
        "id",
        nargs="?",
        help="邮件ID，如 qq_20250321_143022_abc123"
    )

    parser.add_argument(
        "--id",
        dest="email_id",
        help="邮件ID（与位置参数二选一）"
    )

    parser.add_argument(
        "--test-mode", "-t",
        action="store_true",
        help="查询测试目录"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["json", "text"],
        default="text",
        help="输出格式 (默认: text)"
    )

    args = parser.parse_args()

    # 获取邮件ID
    email_id = args.email_id or args.id
    if not email_id:
        parser.print_help()
        sys.exit(1)

    # 执行查询
    result = get_email_by_id(email_id, test_mode=args.test_mode)

    # 输出结果
    print(format_output(result, args.format))

    # 返回退出码
    sys.exit(0 if result["found"] else 1)


if __name__ == "__main__":
    main()
