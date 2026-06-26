"""
main.py - 微信画像分析主脚本
运行方式: python main.py [--sync-only]
"""
import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

# 导入本地模块
sys.path.insert(0, str(Path(__file__).parent))
from config import DECRYPTED_BASE, STORAGE_DIR, JUNK_PATTERNS, PUBLIC_PREFIXES, MSG_TYPE_MAP

# ============================================================
# 工具函数
# ============================================================

def get_db_conn(db_path):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def ts_to_str(ts):
    try:
        return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M')
    except:
        return str(ts)

def is_junk_session(s):
    username = s['username'].lower()
    summary = (s.get('summary') or '').lower()
    display = (s.get('last_sender_display_name') or '').lower()
    for p in PUBLIC_PREFIXES:
        if p.lower() in username:
            return True
    for kw in JUNK_PATTERNS:
        if kw.lower() in summary or kw.lower() in display:
            return True
    return False

def get_contacts():
    """获取所有联系人"""
    conn = get_db_conn(DECRYPTED_BASE / "contact" / "contact.db")
    cur = conn.cursor()
    rows = cur.execute("SELECT username, nick_name, remark, alias FROM contact").fetchall()
    conn.close()
    return {r['username']: dict(r) for r in rows}

def get_sessions():
    """获取所有会话，过滤垃圾"""
    conn = get_db_conn(DECRYPTED_BASE / "session" / "session.db")
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM SessionTable ORDER BY sort_timestamp DESC").fetchall()
    conn.close()
    sessions = [dict(r) for r in rows]
    return [s for s in sessions if not is_junk_session(s)]

def get_big_tables(limit=10):
    """获取消息量最大的N个Msg表"""
    conn = get_db_conn(DECRYPTED_BASE / "message" / "message_0.db")
    cur = conn.cursor()
    tables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Msg_%'"
    ).fetchall()
    result = []
    for t in tables:
        name = t[0]
        try:
            cnt = cur.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
            result.append((name, cnt))
        except:
            pass
    conn.close()
    result.sort(key=lambda x: x[1], reverse=True)
    return result[:limit]

def analyze_table(table_name):
    """分析单个Msg表"""
    conn = get_db_conn(DECRYPTED_BASE / "message" / "message_0.db")
    cur = conn.cursor()
    
    # 总消息数
    total = cur.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    
    # 时间范围
    row = cur.execute(f"SELECT MIN(create_time), MAX(create_time) FROM {table_name}").fetchone()
    min_ts, max_ts = row[0] or 0, row[1] or 0
    
    # 文本消息发送者排行
    sender_counts = cur.execute(f"""
        SELECT real_sender_id, COUNT(*) as cnt 
        FROM {table_name} 
        WHERE local_type = 1 AND message_content IS NOT NULL AND message_content != ''
        GROUP BY real_sender_id 
        ORDER BY cnt DESC 
        LIMIT 10
    """).fetchall()
    
    # 最新消息样本
    latest = cur.execute(f"""
        SELECT local_id, create_time, real_sender_id, local_type, message_content 
        FROM {table_name} 
        WHERE local_type = 1 AND message_content IS NOT NULL AND length(message_content) > 2
        ORDER BY local_id DESC 
        LIMIT 10
    """).fetchall()
    
    conn.close()
    
    return {
        'total': total,
        'time_range': (min_ts, max_ts),
        'top_senders': [(r[0], r[1]) for r in sender_counts],
        'latest': [dict(zip(['local_id','create_time','sender_id','type','content'], r)) for r in latest]
    }

def guess_group_identity(table_name, analysis, sessions, contacts):
    """根据消息内容猜测群身份"""
    latest = analysis['latest']
    time_range = analysis['time_range']
    
    # 分析关键词
    all_content = ' '.join([
        m['content'][:100] for m in latest 
        if isinstance(m.get('content'), str)
    ]).lower()
    
    tags = []
    name = table_name  # 默认用表名
    
    # 关键词识别
    if any(k in all_content for k in ['满仓', '仓位', '山顶', '买入', '卖出', '股票']):
        tags.append('炒股')
    if any(k in all_content for k in ['openclaw', 'claude', 'cursor', 'ai', 'gpt']):
        tags.append('AI工具')
    if any(k in all_content for k in ['洛克王国', '罗隐', '末日', '翼王', '游戏']):
        tags.append('游戏')
    if any(k in all_content for k in ['直播', '抖音', '虚伪']):
        tags.append('直播')
    if any(k in all_content for k in ['pbl', '临床', '医学', '病例']):
        tags.append('医学')
    
    return name, tags

# ============================================================
# 生成 Markdown 文件
# ============================================================

def gen_wechat_profile(sessions, contacts, big_tables, analyses, output_dir):
    """生成基础人格画像"""
    
    # 群聊/私聊分类
    groups = [s for s in sessions if '@chatroom' in s['username']]
    privates = [s for s in sessions if '@chatroom' not in s['username']]
    
    # 大群
    group_summaries = []
    for s in groups[:20]:
        c = contacts.get(s['username'], {})
        display = c.get('remark') or c.get('nick_name') or s['username']
        ts = ts_to_str(s.get('last_timestamp', 0))
        group_summaries.append({
            'name': display,
            'username': s['username'],
            'last': ts,
            'summary': s.get('summary', '')[:80],
            'unread': s.get('unread_count', 0)
        })
    
    # 常联系人
    contact_summaries = []
    for s in privates[:20]:
        c = contacts.get(s['username'], {})
        display = c.get('remark') or c.get('nick_name') or s['username']
        ts = ts_to_str(s.get('last_timestamp', 0))
        contact_summaries.append({
            'name': display,
            'username': s['username'],
            'last': ts,
            'summary': s.get('summary', '')[:80],
            'unread': s.get('unread_count', 0)
        })
    
    content = f"""# 微信画像 - 良

> 来源：wechat-decrypt 导出分析 | 时间：{datetime.now().strftime('%Y-%m-%d')} | 消息跨度：2024-06 ~ 现在

## 基础信息

- **微信号**: YOLO
- **身份**: 浙江中医药大学 临床医学 22级（2027届）
- **位置**: 杭州（立业院）+ 台州临海

---

## 群聊关系网络

### 群聊 ({len(groups)}个有效群)

| 群名 | 最后活跃 | 摘要 | 未读 |
|---|---|---|---|
"""
    for g in group_summaries:
        unread = f"[未读{g['unread']}条]" if g['unread'] > 0 else ""
        content += f"| {g['name'][:25]} | {g['last']} | {g['summary'][:40]} | {unread} |\n"

    content += f"""
### 私聊 ({len(privates)}个有效会话)

| 联系人 | 最后活跃 | 摘要 | 未读 |
|---|---|---|---|
"""
    for p in contact_summaries:
        unread = f"[未读{p['unread']}条]" if p['unread'] > 0 else ""
        content += f"| {p['name'][:25]} | {p['last']} | {p['summary'][:40]} | {unread} |\n"

    content += f"""
---

## 大群消息分析

| 群 | 消息量 | 时间跨度 | 标签 |
|---|---|---|---|
"""
    for (table_name, total), (_, analysis) in zip(big_tables[:10], list(analyses.items())[:10]):
        min_ts, max_ts = analysis['time_range']
        try:
            time_str = f"{datetime.fromtimestamp(min_ts).strftime('%Y-%m-%d')} ~ {datetime.fromtimestamp(max_ts).strftime('%Y-%m-%d')}"
        except:
            time_str = 'N/A'
        name, tags = guess_group_identity(table_name, analysis, sessions, contacts)
        tag_str = ' '.join([f'`{t}`' for t in tags])
        content += f"| {table_name[:30]} | {total:,} | {time_str} | {tag_str} |\n"

    content += f"""
---

## 更新日志

- {datetime.now().strftime('%Y-%m-%d')}: 首次微信数据导出分析
"""
    
    (output_dir / "wechat-profile.md").write_text(content, encoding='utf-8')
    print(f"  ✅ wechat-profile.md")

def gen_relationship_network(sessions, contacts, analyses, output_dir):
    """生成关系图谱"""
    
    groups = [s for s in sessions if '@chatroom' in s['username']]
    privates = [s for s in sessions if '@chatroom' not in s['username']]
    
    # 核心关系
    close = []
    trade = []
    
    for s in privates:
        username = s['username']
        c = contacts.get(username, {})
        display = c.get('remark') or c.get('nick_name') or username
        summary = s.get('summary', '')
        
        entry = f"- **{display}** — {summary[:60]}"
        
        if any(k in summary.lower() for k in ['已收款', '转账', '交易']):
            trade.append(entry)
        else:
            close.append(entry)
    
    content = f"""# 关系图谱

> 更新时间：{datetime.now().strftime('%Y-%m-%d')}

## 核心关系

### 🟢 密切关系
{chr(10).join(close[:15]) if close else '（无数据）'}

### 🟡 交易关系
{chr(10).join(trade[:10]) if trade else '（无数据）'}

---

## 群聊角色

"""
    for s in groups[:15]:
        c = contacts.get(s['username'], {})
        display = c.get('remark') or c.get('nick_name') or s['username']
        summary = s.get('summary', '')[:80]
        ts = ts_to_str(s.get('last_timestamp', 0))
        
        # 识别群类型
        if any(k in summary.lower() for k in ['满仓', '炒股', '仓位']):
            tag = '📈'
        elif any(k in summary.lower() for k in ['openclaw', 'ai', 'claude']):
            tag = '🦞'
        elif any(k in summary.lower() for k in ['家教', '学生']):
            tag = '📚'
        elif any(k in summary.lower() for k in ['福利', '外卖', '奶茶']):
            tag = '🧋'
        else:
            tag = '💬'
        
        content += f"{tag} **{display}** ({ts})\n   {summary}\n\n"
    
    (output_dir / "relationship-network.md").write_text(content, encoding='utf-8')
    print(f"  ✅ relationship-network.md")

def gen_interest_profile(sessions, analyses, output_dir):
    """生成兴趣画像"""
    
    # 从大群消息分析兴趣
    interests = {
        '投资理财': [],
        'AI工具': [],
        '游戏': [],
        '医学学业': [],
        '生活消费': [],
    }
    
    for table_name, analysis in list(analyses.items())[:5]:
        content = ' '.join([
            m['content'][:100] for m in analysis['latest']
            if isinstance(m.get('content'), str)
        ]).lower()
        
        if any(k in content for k in ['满仓', '仓位', '股票', '买入', '卖出']):
            interests['投资理财'].append(table_name[:30])
        if any(k in content for k in ['openclaw', 'cursor', 'claude', 'gpt', 'ai']):
            interests['AI工具'].append(table_name[:30])
        if any(k in content for k in ['洛克王国', '末日', '游戏', '罗隐']):
            interests['游戏'].append(table_name[:30])
        if any(k in content for k in ['pbl', '医学', '临床', '病例']):
            interests['医学学业'].append(table_name[:30])
    
    content = f"""# 兴趣画像

> 更新时间：{datetime.now().strftime('%Y-%m-%d')}

## 兴趣分布

"""
    for interest, tables in interests.items():
        if tables:
            content += f"### {interest}\n"
            for t in tables:
                content += f"- {t}\n"
            content += "\n"
    
    (output_dir / "interest-profile.md").write_text(content, encoding='utf-8')
    print(f"  ✅ interest-profile.md")

def gen_social_behavior(sessions, output_dir):
    """生成社交行为分析"""
    
    groups = [s for s in sessions if '@chatroom' in s['username']]
    privates = [s for s in sessions if '@chatroom' not in s['username']]
    
    total_sessions = len(sessions)
    group_count = len(groups)
    private_count = len(privates)
    
    content = f"""# 社交行为分析

> 更新时间：{datetime.now().strftime('%Y-%m-%d')}

## 基本数据

- **总会话数**: {total_sessions}
- **群聊数**: {group_count} ({group_count/total_sessions*100:.0f}%)
- **私聊数**: {private_count} ({private_count/total_sessions*100:.0f}%)

## 活跃群聊 TOP5

"""
    for s in sorted(groups, key=lambda x: x.get('last_timestamp', 0), reverse=True)[:5]:
        ts = ts_to_str(s.get('last_timestamp', 0))
        content += f"- {s.get('summary','')[:60]} ({ts})\n"
    
    (output_dir / "social-behavior.md").write_text(content, encoding='utf-8')
    print(f"  ✅ social-behavior.md")

def gen_linguistic_signature(analyses, output_dir):
    """生成语言印记"""
    
    # 从最新消息提取语言风格
    samples = []
    for table_name, analysis in list(analyses.items())[:3]:
        for m in analysis['latest'][:5]:
            if isinstance(m.get('content'), str) and len(m['content']) > 2:
                samples.append(m['content'][:100])
    
    content = f"""# 语言印记

> 更新时间：{datetime.now().strftime('%Y-%m-%d')}

## 语言风格样本

```
{chr(10).join(samples[:20]) if samples else '（无数据）'}
```

## 语言特点

- 口语化直接
- 简短句子为主
- 偶尔游戏术语
- emoji 正常使用

"""
    (output_dir / "linguistic-signature.md").write_text(content, encoding='utf-8')
    print(f"  ✅ linguistic-signature.md")

def main():
    print("=" * 50)
    print("另一个我 - 微信画像分析引擎")
    print("=" * 50)
    
    # 检查数据目录
    if not DECRYPTED_BASE.exists():
        print(f"\n❌ 错误: 解密数据不存在")
        print(f"   请先运行: python setup.py && python C:\\wechat-decrypt\\main.py decrypt")
        return
    
    print(f"\n📂 数据目录: {DECRYPTED_BASE}")
    
    # 确保输出目录
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    timeline_dir = STORAGE_DIR / "timeline"
    timeline_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n[1/6] 读取联系人...")
    contacts = get_contacts()
    print(f"  ✅ {len(contacts)} 联系人")
    
    print("\n[2/6] 读取会话...")
    sessions = get_sessions()
    print(f"  ✅ {len(sessions)} 有效会话 (已过滤垃圾)")
    
    print("\n[3/6] 扫描大群...")
    big_tables = get_big_tables(10)
    for t, cnt in big_tables[:5]:
        print(f"  {cnt:>8,} | {t[:40]}")
    
    print("\n[4/6] 分析消息表...")
    analyses = {}
    for table_name, total in big_tables[:5]:
        print(f"  分析 {table_name[:40]}...", end=" ")
        analyses[table_name] = analyze_table(table_name)
        print(f"{analyses[table_name]['total']:,} 条")
    
    print("\n[5/6] 生成画像文件...")
    gen_wechat_profile(sessions, contacts, big_tables, analyses, STORAGE_DIR)
    gen_relationship_network(sessions, contacts, analyses, STORAGE_DIR)
    gen_interest_profile(sessions, analyses, STORAGE_DIR)
    gen_social_behavior(sessions, STORAGE_DIR)
    gen_linguistic_signature(analyses, STORAGE_DIR)
    
    print("\n[6/6] 生成时间线归档...")
    quarter = f"{datetime.now().year}-Q{(datetime.now().month-1)//3 + 1}"
    timeline_file = timeline_dir / f"{quarter}.md"
    timeline_file.write_text(f"""# {quarter} 微信数据归档

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 本季度数据快照

- 有效会话: {len(sessions)} 个
- 分析群聊: {len(big_tables[:5])} 个
- 总消息: {sum(a['total'] for a in analyses.values()):,}

## 主要变化

（由 Micro Sync 自动更新）
""", encoding='utf-8')
    print(f"  ✅ timeline/{quarter}.md")
    
    print(f"\n{'='*50}")
    print(f"✅ 分析完成！文件保存在:")
    print(f"   {STORAGE_DIR}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
