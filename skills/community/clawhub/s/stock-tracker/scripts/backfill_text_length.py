#!/usr/bin/env python3
"""
回填公告正文长度统计
对已有 clean_text 但 clean_text_length = 0 的记录，计算并回填字数
"""
import sys

sys.path.insert(0, "scripts")
from db import _get_conn


def main():
    conn = _get_conn()
    try:
        # 找出 clean_text 非空但 clean_text_length = 0 的记录
        rows = conn.execute(
            "SELECT ann_id, clean_text FROM announcements "
            "WHERE clean_text IS NOT NULL AND clean_text != '' AND clean_text_length = 0"
        ).fetchall()

        if not rows:
            print("无需回填，所有记录的 clean_text_length 已正确设置")
            return

        updated = 0
        for ann_id, clean_text in rows:
            conn.execute(
                "UPDATE announcements SET clean_text_length = ? WHERE ann_id = ?",
                (len(clean_text), ann_id),
            )
            updated += 1

        conn.commit()
        print(f"已回填 {updated} 条记录的 clean_text_length")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
