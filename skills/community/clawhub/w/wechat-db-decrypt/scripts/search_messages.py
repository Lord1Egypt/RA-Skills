#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
读取已解密的微信数据库 - 示例脚本
路径: C:\Users\<用户名>\Documents\xwechat_files\<wxid>\db_storage_decrypted\
"""
import sqlite3, os, datetime, json

LOG_FILE = r"wechat_db_log.txt"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def get_msg_dbs(decrypted_dir):
    """获取所有消息数据库路径"""
    msg_dir = os.path.join(decrypted_dir, "message")
    if not os.path.exists(msg_dir):
        return []
    return [os.path.join(msg_dir, f) for f in os.listdir(msg_dir)
            if f.startswith("message_") and f.endswith(".db") and not f.endswith("-shm") and not f.endswith("-wal")]

def search_messages(decrypted_dir, keywords, max_results=50):
    """搜索所有消息库中的关键词"""
    results = []
    msg_dbs = get_msg_dbs(decrypted_dir)

    for db_path in msg_dbs:
        db_name = os.path.basename(db_path)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cursor.fetchall()]
            msg_tables = [t for t in tables if t.startswith('Msg_')]

            for tbl in msg_tables:
                try:
                    cursor.execute(f"SELECT message_content, create_time FROM {tbl} WHERE message_content IS NOT NULL LIMIT 1000")
                    all_rows = cursor.fetchall()
                except:
                    continue

                for content, ctime in all_rows:
                    if not content:
                        continue
                    text = str(content)
                    for kw in keywords:
                        if kw in text:
                            try:
                                dt = datetime.datetime.fromtimestamp(ctime)
                            except:
                                dt = ctime
                            results.append({
                                'db': db_name,
                                'table': tbl,
                                'keyword': kw,
                                'time': str(dt),
                                'content': text[:300]
                            })
                            if len(results) >= max_results:
                                conn.close()
                                return results

            conn.close()
        except Exception as e:
            pass

    return results

if __name__ == "__main__":
    import sys
    decrypted_dir = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\89627\Documents\xwechat_files\qazzhaokuang_af4f\db_storage_decrypted"
    keywords = sys.argv[2:] if len(sys.argv) > 2 else ['开发', '项目', '需求', '报价', '接单', '程序员']

    log(f"搜索目录: {decrypted_dir}")
    log(f"关键词: {keywords}")

    results = search_messages(decrypted_dir, keywords, max_results=100)

    log(f"\n找到 {len(results)} 条结果:")
    for r in results:
        log(f"\n[{r['time']}] {r['db']}/{r['table']}  '{r['keyword']}':")
        log(f"  {r['content']}")

    # 保存结果
    with open("wechat_search_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"\n结果已保存到 wechat_search_results.json")