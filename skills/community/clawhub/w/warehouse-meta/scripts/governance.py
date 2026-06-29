#!/usr/bin/env python3
"""
Data Governance CLI
用法：python governance.py <init|scan|review|status|detect> [options]

连接模式自动探测：
  pyhive 可用且连接成功 → pyhive 模式（读 + 写回 Hive COMMENT）
  pyhive 不可用或连接失败 → MCP 模式（Claude 通过 MCP 读取，只持久化到 SQLite）
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import yaml

# ──────────────────────────────────────────────
# 连接器探测
# ──────────────────────────────────────────────

def detect_connector(cfg) -> tuple[str, object]:
    """
    探测可用的数仓连接方式。
    返回 ("pyhive", conn) 或 ("mcp", None)。
    """
    # Step1：检查 pyhive 是否安装
    try:
        from pyhive import hive as _hive
    except ImportError:
        _print_connector_status("mcp", reason="pyhive 未安装")
        return "mcp", None

    # Step2：检查配置文件中是否有 hive 配置
    hcfg = cfg.get("hive", {})
    if not hcfg.get("host"):
        _print_connector_status("mcp", reason="配置文件未填写 hive.host")
        return "mcp", None

    # Step3：尝试连接
    try:
        conn = _hive.connect(
            host=hcfg["host"],
            port=hcfg.get("port", 10000),
            username=hcfg.get("username", "hive"),
            auth=hcfg.get("auth", "NONE"),
        )
        conn.cursor().execute("SELECT 1")
        _print_connector_status("pyhive", host=hcfg["host"])
        return "pyhive", conn
    except Exception as e:
        _print_connector_status("mcp", reason=f"Hive 连接失败：{e}")
        return "mcp", None


def _print_connector_status(mode, host=None, reason=None):
    if mode == "pyhive":
        print(f"  🔌 连接模式：pyhive（{host}）→ 支持读写，可写回 Hive COMMENT")
    else:
        print(f"  🔌 连接模式：MCP 只读（{reason}）→ 结果仅持久化到 SQLite")


# ──────────────────────────────────────────────
# 依赖检测
# ──────────────────────────────────────────────

REQUIRED_CORE = {"sqlglot": "sqlglot", "openai": "openai",
                 "yaml": "pyyaml", "sentence_transformers": "sentence-transformers"}
OPTIONAL = {"pyhive": "pyhive[hive] thrift", "dspy": "dspy-ai"}

def check_core_deps():
    missing = [pkg for mod, pkg in REQUIRED_CORE.items()
               if not _can_import(mod)]
    if missing:
        print("❌ 缺少核心依赖，请运行：")
        print(f"   pip install {' '.join(missing)}")
        sys.exit(1)

def _can_import(mod):
    try:
        __import__(mod)
        return True
    except ImportError:
        return False


# ──────────────────────────────────────────────
# 配置加载
# ──────────────────────────────────────────────

def load_config(path=".governance_config.yaml"):
    if not Path(path).exists():
        print(f"❌ 配置文件不存在：{path}")
        print("   运行：python governance.py init")
        sys.exit(1)
    with open(path) as f:
        cfg = yaml.safe_load(f)
    _expand_env(cfg)
    return cfg

def _expand_env(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                obj[k] = os.environ.get(v[2:-1], "")
            else:
                _expand_env(v)
    elif isinstance(obj, list):
        for item in obj:
            _expand_env(item)


# ──────────────────────────────────────────────
# SQLite 初始化
# ──────────────────────────────────────────────

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS field_metadata (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name        TEXT NOT NULL,
    field_name        TEXT NOT NULL,
    field_type        TEXT,
    generated_comment TEXT,
    confidence        REAL,
    reviewed_by       TEXT DEFAULT 'auto',
    review_status     TEXT DEFAULT 'pending',
    schema_fingerprint TEXT,
    dml_expression    TEXT,
    connector_mode    TEXT DEFAULT 'unknown',
    created_at        TEXT,
    updated_at        TEXT,
    UNIQUE(table_name, field_name)
);
CREATE TABLE IF NOT EXISTS table_metadata (
    table_name        TEXT PRIMARY KEY,
    table_comment     TEXT,
    business_domain   TEXT,
    schema_fingerprint TEXT,
    field_count       INTEGER,
    coverage_rate     REAL,
    updated_at        TEXT
);
CREATE TABLE IF NOT EXISTS gold_labels (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT, field_name TEXT, field_type TEXT,
    comment    TEXT, context TEXT, embedding TEXT,
    source     TEXT DEFAULT 'human', created_at TEXT
);
CREATE TABLE IF NOT EXISTS corrections (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name     TEXT, field_name TEXT,
    level1_comment TEXT, level2_comment TEXT, final_comment TEXT,
    processed      INTEGER DEFAULT 0, created_at TEXT
);
CREATE TABLE IF NOT EXISTS abbrev_dict (
    token TEXT PRIMARY KEY, meaning TEXT,
    count INTEGER DEFAULT 1, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS prompt_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule TEXT UNIQUE, priority TEXT DEFAULT 'medium', created_at TEXT
);
CREATE TABLE IF NOT EXISTS domain_prompts (
    domain TEXT PRIMARY KEY, hint TEXT,
    sample_count INTEGER, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS system_state (
    key TEXT PRIMARY KEY, value TEXT
);
"""

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.executescript(DB_SCHEMA)
    conn.commit()
    conn.close()
    print(f"  ✓ {db_path} 已就绪")


# ──────────────────────────────────────────────
# pyhive 读取函数
# ──────────────────────────────────────────────

def hive_query(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    cols = [d[0] for d in cur.description] if cur.description else []
    return [dict(zip(cols, row)) for row in cur.fetchall()]

def pyhive_get_databases(conn):
    return [list(r.values())[0] for r in hive_query(conn, "SHOW DATABASES")]

def pyhive_get_tables(conn, db):
    hive_query(conn, f"USE {db}")
    return [list(r.values())[0] for r in hive_query(conn, "SHOW TABLES")]

def pyhive_get_desc(conn, db, table):
    try:
        return hive_query(conn, f"DESC {db}.{table}")
    except Exception:
        return []

def pyhive_get_samples(conn, db, table, field, n=20):
    try:
        rows = hive_query(conn, f"SELECT `{field}` FROM {db}.{table} WHERE `{field}` IS NOT NULL LIMIT {n}")
        return [list(r.values())[0] for r in rows]
    except Exception:
        return []

def pyhive_get_dml(conn, db, table):
    try:
        rows = hive_query(conn, f"SHOW CREATE TABLE {db}.{table}")
        ddl = "\n".join(list(r.values())[0] for r in rows)
        return ddl if ("AS SELECT" in ddl.upper() or "CREATE VIEW" in ddl.upper()) else ""
    except Exception:
        return ""

def pyhive_writeback(conn, db, table, field, comment) -> bool:
    try:
        conn.cursor().execute(
            f"ALTER TABLE {db}.{table} CHANGE `{field}` `{field}` COMMENT '{comment}'"
        )
        return True
    except Exception as e:
        print(f"  ⚠️  写回失败 {table}.{field}：{e}")
        return False


# ──────────────────────────────────────────────
# MCP 模式：接受 Claude 传入的 schema JSON
# ──────────────────────────────────────────────

def load_mcp_schema(schema_file: str) -> list[dict]:
    """
    读取由 Claude（MCP 工具）采集并写入的 schema JSON。
    格式见 references/mcp_schema_format.json。
    """
    with open(schema_file) as f:
        return json.load(f)


# ──────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────

def compute_fingerprint(fields: list[dict]) -> str:
    key = json.dumps(
        [(f.get("col_name", ""), f.get("data_type", "")) for f in fields],
        sort_keys=True
    )
    return hashlib.md5(key.encode()).hexdigest()

def get_stored_fingerprint(db_conn, table_name):
    row = db_conn.execute(
        "SELECT schema_fingerprint FROM table_metadata WHERE table_name=?",
        (table_name,)
    ).fetchone()
    return row[0] if row else None

def extract_field_expr(dml_sql, field_name):
    if not dml_sql:
        return ""
    try:
        import sqlglot
        ast = sqlglot.parse_one(dml_sql)
        for alias in ast.find_all(sqlglot.exp.Alias):
            if alias.alias.lower() == field_name.lower():
                return str(alias.this)
    except Exception:
        pass
    return ""

def get_abbrev_hints(db_conn, field_name):
    tokens = re.split(r'[_\-]', field_name.lower())
    hints = []
    for t in tokens:
        row = db_conn.execute("SELECT meaning FROM abbrev_dict WHERE token=?", (t,)).fetchone()
        if row:
            hints.append(f"{t}={row[0]}")
    return "、".join(hints)

def get_rules_text(db_conn):
    rows = db_conn.execute(
        "SELECT rule FROM prompt_rules ORDER BY priority DESC LIMIT 20"
    ).fetchall()
    return "\n".join(f"- {r[0]}" for r in rows)

def get_fewshots(db_conn, db_prefix, n=5):
    rows = db_conn.execute("""
        SELECT table_name, field_name, comment FROM gold_labels
        WHERE table_name LIKE ? ORDER BY id DESC LIMIT ?
    """, (f"{db_prefix}.%", n)).fetchall()
    return [{"table_name": r[0], "field_name": r[1], "comment": r[2]} for r in rows]


# ──────────────────────────────────────────────
# LLM 推断
# ──────────────────────────────────────────────

def build_prompt(table_name, field_name, field_type, samples,
                 existing_comment, sibling_fields, dml_expr,
                 abbrev_hints, rules, fewshots):
    parts = []
    if rules:
        parts.append(f"标注规则：\n{rules}\n")
    if fewshots:
        parts.append("参考示例：")
        for fs in fewshots[:5]:
            parts.append(f"  {fs['table_name']}.{fs['field_name']} → \"{fs['comment']}\"")
        parts.append("")
    parts += [
        f"表名：{table_name}",
        f"字段名：{field_name}（类型：{field_type}）",
    ]
    if abbrev_hints:
        parts.append(f"缩写提示：{abbrev_hints}")
    if dml_expr:
        parts.append(f"计算表达式（优先以此推断）：{dml_expr}")
    if sibling_fields:
        parts.append(f"同表其他字段：{'、'.join(sibling_fields[:10])}")
    if samples:
        parts.append(f"数据样本：{samples[:10]}")
    if existing_comment:
        parts.append(f"现有注释（供参考）：{existing_comment}")
    parts.append('\n输出 JSON：{"comment": "15字以内中文注释", "confidence": 0-100, "reasoning": "推断依据"}')
    return "\n".join(parts)

def call_llm(cfg_model, messages, temperature=None):
    from openai import OpenAI
    client = OpenAI(
        base_url=cfg_model["base_url"],
        api_key=cfg_model.get("api_key", "dummy"),
    )
    resp = client.chat.completions.create(
        model=cfg_model["model"],
        messages=messages,
        temperature=temperature or cfg_model.get("temperature", 0.1),
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)

def infer_l1(cfg, prompt):
    return call_llm(cfg["models"]["level1"], [
        {"role": "system", "content": "你是企业数仓元数据专家，根据字段名、样本和上下文推断业务含义。"},
        {"role": "user",   "content": prompt},
    ])

def infer_l2(cfg, prompt, l1_result):
    return call_llm(cfg["models"]["level2"], [
        {"role": "system", "content": "你是高级数据架构师，负责审核和修正字段注释。"},
        {"role": "user",   "content": prompt + f"\n\nLevel1 建议：{l1_result.get('comment','')}（置信度 {l1_result.get('confidence',0)}），请给出最终判断。"},
    ])

def self_consistency(cfg, prompt, n=5, min_agreement=0.6):
    """多次采样投票，返回 (comment, agreement_rate)"""
    results = []
    for _ in range(n):
        try:
            r = call_llm(cfg["models"]["level1"], [
                {"role": "system", "content": "你是企业数仓元数据专家。"},
                {"role": "user",   "content": prompt},
            ], temperature=0.7)
            results.append(r.get("comment", ""))
        except Exception:
            pass
    if not results:
        return None, 0.0
    counter = defaultdict(int)
    for c in results:
        counter[c] += 1
    best = max(counter, key=counter.get)
    return best, counter[best] / len(results)


# ──────────────────────────────────────────────
# Active Learning 排序
# ──────────────────────────────────────────────

def al_score(confidence, field_name, db_conn):
    uncertainty = 1.0 - abs(confidence - 70) / 70
    token = re.split(r'[_\-]', field_name.lower())[0]
    cnt = db_conn.execute(
        "SELECT COUNT(*) FROM field_metadata WHERE field_name LIKE ?", (f"{token}%",)
    ).fetchone()[0]
    coverage = min(cnt / 100, 1.0)
    return uncertainty * 0.6 + coverage * 0.4


# ──────────────────────────────────────────────
# 进化函数
# ──────────────────────────────────────────────

def mine_abbreviations(db_conn, cfg, new_labels):
    if not new_labels:
        return 0
    token_meanings = defaultdict(list)
    for label in new_labels:
        try:
            prompt = f'字段名：{label["field_name"]}，注释：{label["comment"]}\n提取各部分含义，输出JSON：{{"mappings":{{"token":"含义"}}}}'
            result = call_llm(cfg["models"]["level2"], [{"role": "user", "content": prompt}])
            for token, meaning in result.get("mappings", {}).items():
                token_meanings[token.lower()].append(meaning)
        except Exception:
            pass
    added = 0
    now = datetime.now().isoformat()
    for token, meanings in token_meanings.items():
        if len(meanings) < 2:
            continue
        best = max(set(meanings), key=meanings.count)
        if meanings.count(best) < 2:
            continue
        db_conn.execute("""
            INSERT INTO abbrev_dict (token, meaning, count, updated_at)
            VALUES (?,?,?,?)
            ON CONFLICT(token) DO UPDATE SET count=count+?, updated_at=?
        """, (token, best, meanings.count(best), now, meanings.count(best), now))
        added += 1
    db_conn.commit()
    return added

def evolve_rules(db_conn, cfg):
    corrections = db_conn.execute(
        "SELECT * FROM corrections WHERE processed=0 LIMIT 200"
    ).fetchall()
    if len(corrections) < 200:
        return 0
    cases = "\n".join(
        f"字段：{c[1]}.{c[2]}，Level1：{c[3]}，修正后：{c[5]}" for c in corrections
    )
    try:
        result = call_llm(cfg["models"]["level2"], [{"role": "user", "content":
            f"以下是被修正的标注案例：\n{cases}\n提炼5-10条规则避免类似错误。"
            f'\n输出JSON：{{"rules":[{{"rule":"...","priority":"high|medium"}}]}}'
        }])
        now = datetime.now().isoformat()
        added = 0
        for r in result.get("rules", []):
            try:
                db_conn.execute(
                    "INSERT OR IGNORE INTO prompt_rules (rule,priority,created_at) VALUES (?,?,?)",
                    (r["rule"], r.get("priority", "medium"), now)
                )
                added += 1
            except Exception:
                pass
        ids = [c[0] for c in corrections]
        db_conn.execute(
            f"UPDATE corrections SET processed=1 WHERE id IN ({','.join('?'*len(ids))})", ids
        )
        db_conn.commit()
        return added
    except Exception:
        return 0

def maybe_dspy_bootstrap(db_conn, cfg, force=False):
    try:
        import dspy
        from dspy.teleprompt import MIPROv2
    except ImportError:
        return False

    rows = db_conn.execute("""
        SELECT table_name, field_name, field_type, generated_comment
        FROM field_metadata WHERE review_status='approved' AND confidence>=85 LIMIT 500
    """).fetchall()

    min_n = cfg.get("dspy", {}).get("min_trainset_size", 100)
    if len(rows) < min_n and not force:
        print(f"  ℹ️  黄金样本 {len(rows)} 条（需 {min_n} 条），跳过 DSPy 优化")
        return False

    print(f"  🔧 DSPy 冷启动（{len(rows)} 条样本）...")

    class FieldAnnotation(dspy.Signature):
        """根据字段名、类型和缩写提示，推断字段的中文业务含义"""
        table_name:    str = dspy.InputField()
        field_name:    str = dspy.InputField()
        field_type:    str = dspy.InputField()
        abbrev_hints:  str = dspy.InputField()
        comment:       str = dspy.OutputField(desc="中文注释，15字以内")

    class Annotator(dspy.Module):
        def __init__(self):
            self.ann = dspy.ChainOfThought(FieldAnnotation)
        def forward(self, **kw):
            return self.ann(**kw)

    l1 = cfg["models"]["level1"]
    lm = dspy.LM(model=f"openai/{l1['model']}",
                 api_base=l1["base_url"], api_key=l1.get("api_key","dummy"))
    dspy.configure(lm=lm)

    examples = [
        dspy.Example(
            table_name=r[0], field_name=r[1], field_type=r[2] or "STRING",
            abbrev_hints=get_abbrev_hints(db_conn, r[1]), comment=r[3]
        ).with_inputs("table_name", "field_name", "field_type", "abbrev_hints")
        for r in rows
    ]

    def metric(ex, pred, trace=None):
        p, g = pred.comment.strip(), ex.comment.strip()
        return p == g or len(set(p) & set(g)) / max(len(set(p)), len(set(g)), 1) > 0.6

    n = int(len(examples) * 0.8)
    opt = MIPROv2(metric=metric, num_candidates=cfg.get("dspy", {}).get("optimizer_trials", 30))
    try:
        optimized = opt.compile(Annotator(), trainset=examples[:n], valset=examples[n:])
        out = cfg.get("dspy", {}).get("optimized_model_path", "./optimized_annotator.json")
        optimized.save(out)
        db_conn.execute(
            "INSERT OR REPLACE INTO system_state VALUES ('dspy_last_compile',?)",
            (datetime.now().isoformat(),)
        )
        db_conn.commit()
        print(f"  ✓ DSPy 优化完成 → {out}")
        return True
    except Exception as e:
        print(f"  ⚠️  DSPy 失败：{e}")
        return False


# ──────────────────────────────────────────────
# 核心推断循环（pyhive 和 MCP 模式共用）
# ──────────────────────────────────────────────

def process_table(table_data: dict, cfg: dict, db_conn, connector_mode: str,
                  hive_conn=None) -> dict:
    """
    处理单张表的所有字段。
    table_data 格式：
    {
      "db": "loan_dw",
      "table": "loan_detail",
      "full_name": "loan_dw.loan_detail",
      "fields": [{"col_name": "...", "data_type": "...", "comment": "..."}, ...],
      "samples": {"field_name": [v1, v2, ...]},   # 可为空
      "dml": "..."                                  # 可为空
    }
    """
    full_name    = table_data["full_name"]
    fields       = table_data.get("fields", [])
    samples_map  = table_data.get("samples", {})
    dml          = table_data.get("dml", "")
    thresholds   = cfg["thresholds"]

    if not fields:
        return {"auto": 0, "l2": 0, "human": 0}

    fp = compute_fingerprint(fields)
    sibling_fields = [f.get("col_name", "") for f in fields]
    rules_text     = get_rules_text(db_conn)
    fewshots       = get_fewshots(db_conn, table_data["db"])

    counts = {"auto": 0, "l2": 0, "human": 0}
    now = datetime.now().isoformat()

    for row in fields:
        field_name       = row.get("col_name", "").strip()
        field_type       = row.get("data_type", "STRING")
        existing_comment = row.get("comment", "") or ""

        if not field_name or field_name.startswith("#"):
            continue

        samples    = samples_map.get(field_name, [])
        dml_expr   = extract_field_expr(dml, field_name)
        abbrev     = get_abbrev_hints(db_conn, field_name)

        prompt = build_prompt(
            full_name, field_name, field_type, samples,
            existing_comment, sibling_fields, dml_expr, abbrev, rules_text, fewshots
        )

        # Level1
        try:
            r1      = infer_l1(cfg, prompt)
            comment = r1.get("comment", "")
            conf    = float(r1.get("confidence", 0))
        except Exception:
            comment, conf = "", 0

        final_comment = comment
        reviewed_by   = "auto"
        review_status = "pending"

        if conf >= thresholds["auto_approve"]:
            review_status = "approved"
            counts["auto"] += 1

        elif conf >= thresholds["level2_review"]:
            sc_comment, sc_agree = self_consistency(
                cfg, prompt,
                n=thresholds.get("self_consistency_n", 5),
                min_agreement=thresholds.get("self_consistency_min_agreement", 0.6)
            )
            if sc_agree >= thresholds.get("self_consistency_min_agreement", 0.6) and sc_comment:
                final_comment = sc_comment
                conf          = sc_agree * 100
                review_status = "approved"
                reviewed_by   = "self_consistency"
                counts["auto"] += 1
            else:
                try:
                    r2      = infer_l2(cfg, prompt, r1)
                    l2_c    = r2.get("comment", comment)
                    l2_conf = float(r2.get("confidence", conf))
                    if l2_conf >= thresholds["auto_approve"]:
                        final_comment = l2_c
                        conf          = l2_conf
                        reviewed_by   = "level2"
                        review_status = "approved"
                        counts["auto"] += 1
                        if l2_c != comment:
                            db_conn.execute(
                                "INSERT INTO corrections (table_name,field_name,level1_comment,level2_comment,final_comment,created_at) VALUES (?,?,?,?,?,?)",
                                (full_name, field_name, comment, l2_c, l2_c, now)
                            )
                    else:
                        final_comment = l2_c
                        reviewed_by   = "level2"
                        counts["l2"]  += 1
                except Exception:
                    counts["l2"] += 1
        else:
            counts["human"] += 1

        # 持久化到 SQLite
        db_conn.execute("""
            INSERT INTO field_metadata
                (table_name,field_name,field_type,generated_comment,confidence,
                 reviewed_by,review_status,schema_fingerprint,dml_expression,
                 connector_mode,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(table_name,field_name) DO UPDATE SET
                generated_comment=excluded.generated_comment,
                confidence=excluded.confidence,
                reviewed_by=excluded.reviewed_by,
                review_status=excluded.review_status,
                schema_fingerprint=excluded.schema_fingerprint,
                dml_expression=excluded.dml_expression,
                connector_mode=excluded.connector_mode,
                updated_at=excluded.updated_at
        """, (full_name, field_name, field_type, final_comment, conf,
              reviewed_by, review_status, fp, dml_expr,
              connector_mode, now, now))

        # 写回 Hive COMMENT（仅 pyhive 模式且已批准）
        if connector_mode == "pyhive" and review_status == "approved" and hive_conn:
            if cfg.get("writeback", {}).get("hive_comment", True):
                pyhive_writeback(hive_conn, table_data["db"], table_data["table"],
                                 field_name, final_comment)

    # 更新表元数据
    db_conn.execute("""
        INSERT OR REPLACE INTO table_metadata (table_name,schema_fingerprint,field_count,updated_at)
        VALUES (?,?,?,?)
    """, (full_name, fp, len(fields), now))
    db_conn.commit()

    return counts


# ──────────────────────────────────────────────
# DETECT 命令：只探测连接模式，不扫描
# ──────────────────────────────────────────────

def cmd_detect(args):
    check_core_deps()
    cfg = load_config(args.config)
    print("\n🔍 探测数仓连接模式...")
    mode, conn = detect_connector(cfg)
    if mode == "pyhive":
        print("\n✓ pyhive 连接成功，支持：")
        print("  - 读取 Hive 表结构和数据样本")
        print("  - 写回 Hive COMMENT 字段")
        print("  - 自动获取 View/CTAS DML 逻辑")
    else:
        print("\n✓ 将使用 MCP 模式，支持：")
        print("  - Claude 通过 MCP 工具读取 schema 和样本")
        print("  - 结果持久化到 SQLite")
        print("  - 不写回 Hive COMMENT（需配置 pyhive 才可写回）")
        print("\n  若需开启写回，安装并配置 pyhive：")
        print("  pip install pyhive[hive] thrift")
        print("  然后在 .governance_config.yaml 中填写 hive.host")


# ──────────────────────────────────────────────
# SCAN 命令
# ──────────────────────────────────────────────

def cmd_scan(args, cfg):
    db_path = cfg["storage"]["db_path"]
    init_db(db_path)
    db_conn = sqlite3.connect(db_path)

    print("\n🔍 探测连接模式...")
    connector_mode, hive_conn = detect_connector(cfg)

    # ── pyhive 模式：脚本自行采集 ──
    if connector_mode == "pyhive":
        databases = [args.db] if args.db and args.db != "all" \
                    else pyhive_get_databases(hive_conn)

        total_fields = auto = l2 = human = 0
        changed = []

        print(f"\n📂 扫描数据库：{databases}（模式：{args.mode}）\n")

        for db in databases:
            tables = pyhive_get_tables(hive_conn, db)
            if args.table and args.table != "all":
                tables = [t for t in tables if t == args.table]

            for table in tables:
                full_name = f"{db}.{table}"
                fields = pyhive_get_desc(hive_conn, db, table)
                if not fields:
                    continue

                fp = compute_fingerprint(fields)
                if args.mode == "incremental" and get_stored_fingerprint(db_conn, full_name) == fp:
                    continue

                changed.append(full_name)
                dml = pyhive_get_dml(hive_conn, db, table)
                samples_map = {
                    f.get("col_name",""): pyhive_get_samples(hive_conn, db, table, f.get("col_name",""))
                    for f in fields if f.get("col_name","")
                }

                table_data = {
                    "db": db, "table": table, "full_name": full_name,
                    "fields": fields, "samples": samples_map, "dml": dml
                }
                c = process_table(table_data, cfg, db_conn, connector_mode, hive_conn)
                total_fields += sum(c.values())
                auto += c["auto"]; l2 += c["l2"]; human += c["human"]
                print(f"  ✓ {full_name}（{sum(c.values())} 字段，自动:{c['auto']} L2:{c['l2']} 人工:{c['human']}）")

    # ── MCP 模式：读取 Claude 传入的 schema JSON ──
    else:
        if not args.input_schema:
            print("\n❌ MCP 模式下需要 --input-schema 参数")
            print("   请由 Claude 调用 MCP 工具采集 schema 后传入，见 SKILL.md")
            db_conn.close()
            return

        tables_data = load_mcp_schema(args.input_schema)
        total_fields = auto = l2 = human = 0
        changed = []

        print(f"\n📂 MCP 模式扫描（{len(tables_data)} 张表）\n")

        for table_data in tables_data:
            full_name = table_data["full_name"]
            fields    = table_data.get("fields", [])

            fp = compute_fingerprint(fields)
            if args.mode == "incremental" and get_stored_fingerprint(db_conn, full_name) == fp:
                continue

            changed.append(full_name)
            c = process_table(table_data, cfg, db_conn, connector_mode, hive_conn=None)
            total_fields += sum(c.values())
            auto += c["auto"]; l2 += c["l2"]; human += c["human"]
            print(f"  ✓ {full_name}（{sum(c.values())} 字段，自动:{c['auto']} L2:{c['l2']} 人工:{c['human']}）")

    # 触发进化
    if connector_mode == "pyhive":
        state = db_conn.execute(
            "SELECT value FROM system_state WHERE key='dspy_last_compile'"
        ).fetchone()
        if not state:
            print("\n💡 首次运行，触发 DSPy 冷启动...")
            maybe_dspy_bootstrap(db_conn, cfg)

    new_rules = evolve_rules(db_conn, cfg)
    if new_rules:
        print(f"\n🔧 规则提炼：新增 {new_rules} 条")

    if args.evolve:
        print("\n🔧 强制重新编译 DSPy...")
        maybe_dspy_bootstrap(db_conn, cfg, force=True)

    writeback_note = "→ 已写回 Hive COMMENT" if connector_mode == "pyhive" else "→ 仅持久化到 SQLite（MCP 只读模式）"

    print(f"""
📊 扫描完成 {writeback_note}
──────────────────────────────────────
  变更表数：{len(changed)} 张
  处理字段：{total_fields:,} 个
  自动写回：{auto:,} 个 ({auto/max(total_fields,1)*100:.0f}%)
  Level2：  {l2:,} 个 ({l2/max(total_fields,1)*100:.0f}%)
  人工队列：{human:,} 个 ({human/max(total_fields,1)*100:.0f}%)
──────────────────────────────────────""")

    db_conn.close()


# ──────────────────────────────────────────────
# REVIEW 命令
# ──────────────────────────────────────────────

def cmd_review(args, cfg):
    db_path = cfg["storage"]["db_path"]
    db_conn = sqlite3.connect(db_path)

    # 判断是否有 pyhive（写回用）
    connector_mode, hive_conn = detect_connector(cfg)

    pending = db_conn.execute("""
        SELECT table_name, field_name, field_type, generated_comment,
               confidence, dml_expression
        FROM field_metadata WHERE review_status='pending'
        ORDER BY confidence ASC LIMIT 200
    """).fetchall()

    if not pending:
        print("✓ 人工审核队列为空")
        db_conn.close()
        return

    print(f"\n📋 人工审核队列：{len(pending)} 个字段\n")
    if connector_mode == "mcp":
        print("  ℹ️  MCP 只读模式：确认后写入 SQLite，不写回 Hive COMMENT\n")

    new_gold = []
    for i, row in enumerate(pending):
        table_name, field_name, field_type, comment, conf, dml_expr = row
        parts = table_name.split(".")
        db_name = parts[0] if len(parts) == 2 else "default"
        tbl     = parts[1] if len(parts) == 2 else parts[0]

        # pyhive 模式下取样本
        samples = []
        if connector_mode == "pyhive" and hive_conn:
            samples = pyhive_get_samples(hive_conn, db_name, tbl, field_name)

        print(f"[{i+1}/{len(pending)}] ──────────────────────")
        print(f"  表：    {table_name}")
        print(f"  字段：  {field_name}（{field_type}）")
        if samples:
            print(f"  样本：  {samples[:8]}")
        if dml_expr:
            print(f"  DML：   {dml_expr}")
        print(f"  推断：  \"{comment}\"  (置信度 {conf:.0f}%)")
        print(f"\n  回车=接受  输入=修改  s=跳过  q=退出")
        print(f"  > ", end="", flush=True)

        user_input = input().strip()
        if user_input.lower() == "q":
            break
        if user_input.lower() == "s":
            continue

        final = user_input if user_input else comment
        now   = datetime.now().isoformat()

        if final != comment:
            db_conn.execute("""
                INSERT INTO corrections
                    (table_name,field_name,level1_comment,final_comment,created_at)
                VALUES (?,?,?,?,?)
            """, (table_name, field_name, comment, final, now))

        db_conn.execute("""
            UPDATE field_metadata
            SET generated_comment=?, reviewed_by='human',
                review_status='approved', updated_at=?
            WHERE table_name=? AND field_name=?
        """, (final, now, table_name, field_name))

        # 写回 Hive（仅 pyhive 模式）
        if connector_mode == "pyhive" and hive_conn:
            if cfg.get("writeback", {}).get("hive_comment", True):
                ok = pyhive_writeback(hive_conn, db_name, tbl, field_name, final)
                print(f"  ✓ 已保存：\"{final}\"" + ("（已写回 Hive）" if ok else "（SQLite 已更新，Hive 写回失败）"))
            else:
                print(f"  ✓ 已保存：\"{final}\"（writeback.hive_comment=false，仅 SQLite）")
        else:
            print(f"  ✓ 已保存：\"{final}\"（SQLite）")

        db_conn.execute("""
            INSERT OR REPLACE INTO gold_labels
                (table_name,field_name,field_type,comment,source,created_at)
            VALUES (?,?,?,'human',?,?)
        """, (table_name, field_name, field_type, final, now))
        new_gold.append({"table_name": table_name, "field_name": field_name,
                         "field_type": field_type, "comment": final})
        db_conn.commit()

    if new_gold:
        print(f"\n🧠 新增黄金样本 {len(new_gold)} 条，触发缩写词典挖掘...")
        added = mine_abbreviations(db_conn, cfg, new_gold)
        if added:
            print(f"  ✓ 缩写词典新增 {added} 条")

        gold_total = db_conn.execute("SELECT COUNT(*) FROM gold_labels").fetchone()[0]
        last = int((db_conn.execute(
            "SELECT value FROM system_state WHERE key='gold_count_at_last_compile'"
        ).fetchone() or ("0",))[0])
        if gold_total - last >= cfg.get("dspy", {}).get("recompile_every_n_gold", 5000):
            print(f"\n🔧 黄金样本 {gold_total} 条，触发 DSPy 重新编译...")
            maybe_dspy_bootstrap(db_conn, cfg)
            db_conn.execute(
                "INSERT OR REPLACE INTO system_state VALUES ('gold_count_at_last_compile',?)",
                (str(gold_total),)
            )
            db_conn.commit()

    db_conn.close()


# ──────────────────────────────────────────────
# STATUS 命令
# ──────────────────────────────────────────────

def cmd_status(args, cfg):
    db_path = cfg["storage"]["db_path"]
    if not Path(db_path).exists():
        print("❌ 数据库不存在，请先运行 scan")
        return

    db_conn = sqlite3.connect(db_path)

    rows = db_conn.execute("""
        SELECT substr(table_name,1,instr(table_name,'.')-1) as db_name,
               COUNT(DISTINCT table_name), COUNT(*),
               SUM(CASE WHEN review_status='approved' THEN 1 ELSE 0 END),
               MAX(connector_mode)
        FROM field_metadata GROUP BY db_name ORDER BY 3 DESC
    """).fetchall()

    gold     = db_conn.execute("SELECT COUNT(*) FROM gold_labels").fetchone()[0]
    abbrev   = db_conn.execute("SELECT COUNT(*) FROM abbrev_dict").fetchone()[0]
    pending  = db_conn.execute("SELECT COUNT(*) FROM field_metadata WHERE review_status='pending'").fetchone()[0]
    last_cpl = db_conn.execute("SELECT value FROM system_state WHERE key='dspy_last_compile'").fetchone()

    print(f"""
📈 数据治理状态
══════════════════════════════════════════════════════════
{"数据库":<15} {"表数":>6} {"字段总数":>10} {"覆盖率":>8} {"连接模式":>10}
──────────────────────────────────────────────────────────""")

    total_t = total_f = total_a = 0
    for r in rows:
        db_name, tables, fields, approved, mode = r
        cov = approved / max(fields, 1) * 100
        total_t += tables; total_f += fields; total_a += approved
        print(f"{db_name:<15} {tables:>6} {fields:>10,} {cov:>7.1f}% {(mode or '-'):>10}")

    overall = total_a / max(total_f, 1) * 100
    print(f"──────────────────────────────────────────────────────────")
    print(f"{'合计':<15} {total_t:>6} {total_f:>10,} {overall:>7.1f}%")
    print(f"""
🧠 系统状态
  黄金样本池：    {gold:,} 条
  缩写词典：      {abbrev:,} 条
  DSPy 上次优化：{last_cpl[0][:10] if last_cpl else '从未'}
  待人工审核：    {pending:,} 个
══════════════════════════════════════════════════════════""")

    db_conn.close()


# ──────────────────────────────────────────────
# INIT 命令
# ──────────────────────────────────────────────

def cmd_init(args):
    check_core_deps()
    cfg_path  = getattr(args, "config", ".governance_config.yaml")
    tmpl_path = Path(__file__).parent.parent / "references" / "config_template.yaml"

    if Path(cfg_path).exists():
        print(f"✓ 配置文件已存在：{cfg_path}")
    else:
        print("🔧 初始化配置\n")
        host   = input("Hive 主机地址（无 pyhive 可留空）[]: ").strip()
        port   = input("Hive 端口 [10000]: ").strip() or "10000"
        user   = input("Hive 用户名 [hive]: ").strip() or "hive"
        l1_url = input("Level1 模型 API 地址 [http://localhost:8000/v1]: ").strip() or "http://localhost:8000/v1"
        l1_mod = input("Level1 模型名称 [qwen2.5-7b]: ").strip() or "qwen2.5-7b"
        l2_url = input("Level2 模型 API 地址 [https://api.deepseek.com/v1]: ").strip() or "https://api.deepseek.com/v1"
        l2_mod = input("Level2 模型名称 [deepseek-chat]: ").strip() or "deepseek-chat"

        with open(tmpl_path) as f:
            content = f.read()
        content = content.replace("host: localhost", f"host: {host or 'localhost'}", 1)
        content = content.replace("port: 10000", f"port: {port}", 1)
        content = content.replace("username: hive", f"username: {user}", 1)
        content = content.replace("http://localhost:8000/v1", l1_url, 1)
        content = content.replace("qwen2.5-7b", l1_mod, 1)
        content = content.replace("https://api.deepseek.com/v1", l2_url, 1)
        content = content.replace("deepseek-chat", l2_mod, 1)

        with open(cfg_path, "w") as f:
            f.write(content)
        print(f"✓ 配置文件已生成：{cfg_path}")

    cfg = load_config(cfg_path)
    init_db(cfg["storage"]["db_path"])

    print("\n🔍 探测连接模式...")
    mode, _ = detect_connector(cfg)

    print(f"\n✅ 初始化完成（{mode} 模式）")
    if mode == "mcp":
        print("   下一步：运行 /data-governance scan")
        print("   Claude 将自动调用 MCP 工具采集 schema 并推断注释")
    else:
        print("   下一步：/data-governance scan --db your_database")


# ──────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="warehouse-meta CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init")

    p_detect = sub.add_parser("detect")
    p_detect.add_argument("--config", default=".governance_config.yaml")

    p_scan = sub.add_parser("scan")
    p_scan.add_argument("--config", default=".governance_config.yaml")
    p_scan.add_argument("--db",           default="all")
    p_scan.add_argument("--table",        default="all")
    p_scan.add_argument("--mode",         choices=["full","incremental"], default="incremental")
    p_scan.add_argument("--input-schema", default=None,
                        help="MCP 模式下由 Claude 传入的 schema JSON 路径")
    p_scan.add_argument("--evolve",       action="store_true")

    p_review = sub.add_parser("review")
    p_review.add_argument("--config", default=".governance_config.yaml")

    p_status = sub.add_parser("status")
    p_status.add_argument("--config", default=".governance_config.yaml")
    p_status.add_argument("--db",     default="all")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "detect":
        cmd_detect(args)
    elif args.command == "scan":
        check_core_deps()
        cmd_scan(args, load_config(args.config))
    elif args.command == "review":
        check_core_deps()
        cmd_review(args, load_config(args.config))
    elif args.command == "status":
        cmd_status(args, load_config(args.config))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
