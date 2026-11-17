#!/usr/bin/env python3
"""SQL 迁移脚本风险检查：找出会锁表、丢数据或让线上部署踩坑的语句。纯标准库，正则启发式。

用法：
  python3 sql_migration_check.py <文件或目录 ...> [--dialect auto|mysql|postgres] [--json] [--strict]
  也可从 stdin 读：cat 001.sql | python3 sql_migration_check.py -
"""
import argparse, json, os, re, sys


def strip_comments(sql):
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"^\s*#[^\n]*$", " ", sql, flags=re.M)
    return sql


def split_statements(sql):
    """按分号切分，忽略引号内的分号；返回 [(起始行, 语句)]。"""
    out, buf, line, start, q = [], [], 1, 1, None
    for ch in sql:
        if q:
            buf.append(ch)
            if ch == q:
                q = None
        elif ch in ("'", '"', "`"):
            q = ch; buf.append(ch)
        elif ch == ";":
            s = "".join(buf).strip()
            if s:
                out.append((start, s))
            buf, start = [], line
        else:
            buf.append(ch)
        if ch == "\n":
            line += 1
            if not "".join(buf).strip():
                start = line
    s = "".join(buf).strip()
    if s:
        out.append((start, s))
    return out


def detect_dialect(sql):
    low = sql.lower()
    if re.search(r"\bconcurrently\b|\bserial\b|::|\bnot valid\b|\busing\s+btree\b|\bbigserial\b|\btimestamptz\b|\bwith time zone\b|\bjsonb\b|\bnow\(\)", low):
        return "postgres"
    if re.search(r"\bengine\s*=|\balgorithm\s*=|\bauto_increment\b|`", low):
        return "mysql"
    return "unknown"


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def check_statement(stmt, dialect):
    s = norm(stmt); low = s.lower()
    f = []

    def add(rule, sev, msg, fix):
        f.append({"rule": rule, "severity": sev, "message": msg, "fix": fix})

    if re.match(r"drop\s+table", low):
        add("SM001", "high", "DROP TABLE 会永久删除数据", "先确认没有读写方；先改名（保留一段时间）或备份后再删；放到单独的迁移里")
    if re.search(r"alter\s+table\b.*\bdrop\s+(column\s+)?(?!constraint|index|key|foreign|primary)\w+", low):
        add("SM001", "high", "DROP COLUMN 会永久删除该列数据", "采用扩展-收缩：先让代码不再读写该列并发布，再在后续迁移里删除")
    if re.match(r"truncate\b", low):
        add("SM002", "high", "TRUNCATE 清空整表", "确认是否真的要清空；通常不该出现在自动迁移中")
    if re.match(r"(update|delete)\b", low) and " where " not in low + " ":
        add("SM006", "high", "UPDATE/DELETE 没有 WHERE", "补上 WHERE；大表分批（LIMIT / 主键区间）执行")
    m = re.search(r"add\s+(column\s+)?[`\"]?(\w+)[`\"]?\s+([^,]+?)\bnot\s+null\b(?![^,]*\bdefault\b)", low)
    if "alter table" in low and m and not re.search(r"\bdefault\b[^,]*\bnot\s+null\b", low):
        add("SM003", "high", f"新增列 {m.group(2)} 为 NOT NULL 但没有 DEFAULT", "已有数据行会导致失败或需要全表回填；先加可空列 → 回填 → 再设 NOT NULL，或提供 DEFAULT")
    if "alter table" in low and re.search(r"\badd\s+(column\s+)?\w+.*\bdefault\s+\(?(now|current_timestamp|uuid|gen_random_uuid|random|nextval)\b", low) and dialect != "mysql":
        add("SM015", "warn", "新增列的 DEFAULT 是易变函数（now()/uuid 等）", "PostgreSQL 会重写整表并长时间锁表；先加列再分批 UPDATE，或用常量默认值")
    if "alter table" in low and re.search(r"\b(alter\s+column\s+\w+\s+(set\s+data\s+)?type|modify\s+column|modify\s+\w+\s+\w|change\s+column|change\s+\w+\s+\w+\s+\w)", low):
        add("SM004", "warn", "修改列类型/定义会重写表并持锁", "大表在低峰期执行；MySQL 考虑 pt-online-schema-change / gh-ost，PostgreSQL 考虑加新列迁移数据")
    if re.search(r"\brename\s+(table|to|column)\b|\balter\s+table\s+\S+\s+rename\b", low):
        add("SM005", "warn", "RENAME 会让仍在运行的旧版本代码立刻报错", "扩展-收缩：新建 → 双写 → 切换 → 删除；或确保部署期间没有旧版本在跑")
    if re.match(r"create\s+(unique\s+)?index\b", low):
        if dialect == "postgres" and "concurrently" not in low:
            add("SM007", "warn", "PostgreSQL 建索引未加 CONCURRENTLY", "CREATE INDEX CONCURRENTLY …（注意不能在事务块内执行）")
        elif dialect == "mysql" and "algorithm=" not in low.replace(" ", ""):
            add("SM007", "info", "MySQL 建索引未指定 ALGORITHM/LOCK", "视版本加 ALGORITHM=INPLACE, LOCK=NONE，确认不会长时间锁表")
        elif dialect == "unknown":
            add("SM007", "info", "在已有大表上建索引会持锁", "PostgreSQL 用 CONCURRENTLY；MySQL 用 ALGORITHM=INPLACE, LOCK=NONE")
        if "unique" in low:
            add("SM009", "warn", "对已有数据加唯一索引", "先查重复数据，否则迁移会失败")
    if re.search(r"\badd\s+(constraint\s+\w+\s+)?foreign\s+key\b", low):
        add("SM008", "warn", "增加外键会校验全表并加锁", "PostgreSQL：ADD CONSTRAINT … NOT VALID 后再 VALIDATE CONSTRAINT；MySQL：低峰期执行并确认被引用列有索引")
    if re.search(r"\badd\s+(constraint\s+\w+\s+)?unique\b", low):
        add("SM009", "warn", "对已有数据加唯一约束", "先查重复数据，否则迁移会失败")
    if re.search(r"\balter\s+column\s+\w+\s+set\s+not\s+null\b", low):
        add("SM012", "warn", "SET NOT NULL 需要全表扫描并持锁", "PostgreSQL 12+：先 ADD CONSTRAINT … CHECK (col IS NOT NULL) NOT VALID → VALIDATE → SET NOT NULL")
    if re.match(r"create\s+table\b", low) and "primary key" not in low and " like " not in low and " as select" not in low:
        add("SM013", "warn", "CREATE TABLE 没有主键", "加主键；无主键的表在复制、在线 DDL 与去重时都很麻烦")
    if re.match(r"drop\s+index\b", low):
        add("SM016", "info", "删除索引", "确认没有查询依赖它（看慢查询与执行计划），PostgreSQL 可用 DROP INDEX CONCURRENTLY")
    if re.match(r"lock\s+table", low):
        add("SM017", "warn", "显式 LOCK TABLE", "确认锁级别与持有时长，避免阻塞线上读写")
    if re.search(r"\bengine\s*=\s*myisam\b", low):
        add("SM018", "warn", "使用 MyISAM 引擎", "改用 InnoDB，MyISAM 不支持事务与行锁")
    if re.match(r"alter\s+table\b", low) and low.count(" add ") + low.count(" drop ") + low.count(" modify ") + low.count(" change ") >= 3:
        add("SM011", "info", "一条 ALTER 里堆了多个变更", "可以，但失败时难以定位；确认每个子变更都评估过锁与时长")
    return f


def scan_file(path, dialect):
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8", errors="replace").read()
    clean = strip_comments(text)
    d = dialect if dialect != "auto" else detect_dialect(clean)
    findings = []
    for line, stmt in split_statements(clean):
        for f in check_statement(stmt, d):
            f.update({"line": line, "statement": norm(stmt)[:120]})
            findings.append(f)
    order = {"high": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["line"]))
    return {"file": path, "dialect": d, "statements": len(split_statements(clean)), "findings": findings}


def targets(paths):
    out = []
    for p in paths:
        if p == "-":
            out.append(p)
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [x for x in dirs if x not in (".git", "node_modules", "vendor")]
                out += sorted(os.path.join(root, fn) for fn in files if fn.lower().endswith(".sql"))
        else:
            out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser(description="SQL 迁移风险检查")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--dialect", default="auto", choices=["auto", "mysql", "postgres"])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="有 high 则退出码 1")
    a = ap.parse_args()
    results = [scan_file(p, a.dialect) for p in targets(a.paths)]
    if not results:
        print("没有找到 .sql 文件", file=sys.stderr); sys.exit(2)
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"== {r['file']}  （方言 {r['dialect']}，{r['statements']} 条语句）")
            if not r["findings"]:
                print("  ✓ 没有发现风险")
            for f in r["findings"]:
                print(f"  [{f['severity'].upper():4}] {f['rule']} L{f['line']}: {f['message']}\n         语句：{f['statement']}\n         → {f['fix']}")
            c = {s: sum(1 for f in r["findings"] if f["severity"] == s) for s in ("high", "warn", "info")}
            print(f"  小计：high {c['high']} / warn {c['warn']} / info {c['info']}")
    bad = any(f["severity"] == "high" for r in results for f in r["findings"])
    sys.exit(1 if (a.strict and bad) else 0)


if __name__ == "__main__":
    main()
