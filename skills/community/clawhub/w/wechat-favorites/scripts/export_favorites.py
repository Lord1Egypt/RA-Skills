# -*- coding: utf-8 -*-
"""
微信收藏导出脚本
从 decrypted/favorite/favorite.db 导出全部收藏记录为 CSV
依赖：sqlite3（标准库）, zstandard（解压）
"""
import sqlite3, csv, os, sys, re, zstandard

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "exported_favorites")

# 解析 fav_local_type
FAV_TYPE_MAP = {
    1: "文章", 2: "图文", 3: "图片", 4: "视频",
    5: "音乐", 6: "语音", 7: "文件", 8: "位置",
    9: "小程序", 10: "卡券", 11: "聊天记录", 12: "新闻"
}


def parse_xml_field(raw_bytes, compressed_flag):
    """解析 content BLOB 字段，返回 dict"""
    if not raw_bytes:
        return {}

    # 尝试 zstd 解压
    if compressed_flag == 4:
        try:
            dctx = zstandard.ZstdDecompressor()
            raw_bytes = dctx.decompress(raw_bytes)
        except Exception:
            pass

    # 尝试多种编码
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb2312"):
        try:
            xml_str = raw_bytes.decode(enc)
            break
        except Exception:
            continue
    else:
        return {}

    result = {"raw": xml_str[:200]}

    # 提取关键字段
    for tag in ("title", "description", "url", "source", "appusername", "link"):
        m = re.search(rf"<{tag}><!\[CDATA\[(.*?)\]\]></{tag}>", xml_str, re.S)
        if not m:
            m = re.search(rf"<{tag}>(.*?)</{tag}>", xml_str, re.S)
        if m:
            result[tag] = m.group(1).strip()

    return result


def export(db_path, output_path):
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT local_id, fav_local_type, status, create_time, "
        "source_id, source_type, content, WCDB_CT_content "
        "FROM fav_db_item ORDER BY create_time DESC"
    ).fetchall()
    conn.close()

    print(f"查询到 {len(rows)} 条收藏记录")

    records = []
    for row in rows:
        local_id, fav_type, status, create_time, source_id, source_type, content, comp_flag = row

        parsed = parse_xml_field(content, comp_flag or 0)

        from datetime import datetime
        time_str = ""
        if create_time and create_time > 0:
            try:
                time_str = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass

        records.append({
            "local_id": local_id,
            "type": FAV_TYPE_MAP.get(fav_type, str(fav_type)),
            "status": status,
            "create_time": time_str,
            "timestamp": create_time or 0,
            "source_id": source_id or "",
            "source_type": source_type or 0,
            "title": parsed.get("title", ""),
            "description": parsed.get("description", "")[:200],
            "url": parsed.get("url", ""),
            "source": parsed.get("source", ""),
            "appusername": parsed.get("appusername", ""),
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = ["local_id", "type", "status", "create_time", "timestamp",
                  "source_id", "source_type", "title", "description", "url", "source", "appusername"]

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"已导出: {output_path} ({len(records)} 条)")
    return records


def main():
    print("=" * 60)
    print("  微信收藏导出")
    print("=" * 60)

    db_path = os.path.join(SCRIPT_DIR, "decrypted", "favorite", "favorite.db")
    output_path = os.path.join(OUTPUT_DIR, "favorites_all.csv")

    if not os.path.exists(db_path):
        print(f"[ERROR] 数据库不存在: {db_path}")
        print("请先运行 decrypt_db.py 解密收藏数据库")
        sys.exit(1)

    records = export(db_path, output_path)

    # 打印各类型统计
    print("\n收藏类型分布:")
    type_counts = {}
    for r in records or []:
        t = r["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
