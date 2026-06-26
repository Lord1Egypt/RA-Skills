#!/usr/bin/env python3
"""
SalesClaw - schema.py
Schema 修复工具：时间字段 + 索引 + 逆边字段

用法：
  python schema.py dry_run     # 查看待执行变更
  python schema.py apply       # 执行变更（需要确认）
  python schema.py check       # 检查当前 schema 状态
"""

import sys
import json
from pathlib import Path
from db import query_all, query_one, execute

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "tools"))

# ─────────────────────────────────────────
# Schema 变更计划
# ─────────────────────────────────────────

SCHEMA_CHANGES = [
    {
        "id": "SC001",
        "table": "fct_prescription_flow",
        "description": "新增 prescription_month_date 派生列（DATE 类型）和产品×月份复合索引",
        "sql": """
            ALTER TABLE fct_prescription_flow
                ADD COLUMN prescription_month_date DATE GENERATED ALWAYS AS (
                    STR_TO_DATE(CONCAT(prescription_month, '-01'), '%Y-%m-%d')
                ),
                ADD INDEX idx_product_month (product_id, prescription_month_date);
        """,
        "rollback": """
            ALTER TABLE fct_prescription_flow
                DROP COLUMN prescription_month_date,
                DROP INDEX idx_product_month;
        """,
        "risk": "low",  # 派生列不影响现有数据
    },
    {
        "id": "SC002",
        "table": "fct_expense_c2",
        "description": "新增代表×月份×审批状态复合索引",
        "sql": """
            ALTER TABLE fct_expense_c2
                ADD INDEX idx_rep_month_approval (rep_id, expense_date, approval_status);
        """,
        "rollback": """
            ALTER TABLE fct_expense_c2
                DROP INDEX idx_rep_month_approval;
        """,
        "risk": "low",
    },
    {
        "id": "SC003",
        "table": "object_links",
        "description": "新增 link_direction 字段（区分正向/反向边）",
        "sql": """
            ALTER TABLE object_links
                ADD COLUMN link_direction ENUM('forward', 'reverse') DEFAULT 'forward'
                    AFTER link_type;
        """,
        "rollback": """
            ALTER TABLE object_links
                DROP COLUMN link_direction;
        """,
        "risk": "medium",  # 新增列，老数据默认 forward
    },
    {
        "id": "SC004",
        "table": "fct_prescription_flow",
        "description": "新增 ukey 业务联合键（品种×医院×医生×月份）",
        "sql": """
            ALTER TABLE fct_prescription_flow
                ADD COLUMN ukey VARCHAR(100) GENERATED ALWAYS AS (
                    CONCAT(product_id, '-', hospital_id, '-', doctor_id, '-', prescription_month)
                );
        """,
        "rollback": """
            ALTER TABLE fct_prescription_flow
                DROP COLUMN ukey;
        """,
        "risk": "low",
    },
    {
        "id": "SC005",
        "table": "dim_products",
        "description": "所有 dim 表新增 schema_version 字段（用于版本追踪）",
        "sql": """
            ALTER TABLE dim_products
                ADD COLUMN schema_version VARCHAR(10) DEFAULT 'v1',
                ADD COLUMN table_version_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP;
        """,
        "rollback": """
            ALTER TABLE dim_products
                DROP COLUMN schema_version,
                DROP COLUMN table_version_updated_at;
        """,
        "risk": "low",
    },
]


def dry_run():
    """查看所有待执行变更"""
    print("=" * 60)
    print("Schema 修复计划（Dry Run）")
    print("=" * 60)
    for change in SCHEMA_CHANGES:
        print(f"\n[{change['id']}] {change['table']}")
        print(f"  描述：{change['description']}")
        print(f"  风险：{change['risk']}")
        print(f"  SQL：{change['sql'].strip()}")
    print(f"\n共 {len(SCHEMA_CHANGES)} 项变更")
    print("提示：运行 `python schema.py apply` 执行变更（需确认）")


def check_current():
    """检查当前 Schema 状态"""
    print("=" * 60)
    print("Schema 健康检查")
    print("=" * 60)

    checks = [
        ("fct_prescription_flow", "prescription_month_date",
         "SELECT COUNT(*) FROM information_schema.columns "
         "WHERE table_schema='salesclaw' AND table_name='fct_prescription_flow' AND column_name='prescription_month_date'"),
        ("fct_prescription_flow", "idx_product_month",
         "SELECT COUNT(*) FROM information_schema.statistics "
         "WHERE table_schema='salesclaw' AND table_name='fct_prescription_flow' AND index_name='idx_product_month'"),
        ("fct_expense_c2", "idx_rep_month_approval",
         "SELECT COUNT(*) FROM information_schema.statistics "
         "WHERE table_schema='salesclaw' AND table_name='fct_expense_c2' AND index_name='idx_rep_month_approval'"),
        ("object_links", "link_direction",
         "SELECT COUNT(*) FROM information_schema.columns "
         "WHERE table_schema='salesclaw' AND table_name='object_links' AND column_name='link_direction'"),
        ("dim_products", "schema_version",
         "SELECT COUNT(*) FROM information_schema.columns "
         "WHERE table_schema='salesclaw' AND table_name='dim_products' AND column_name='schema_version'"),
    ]

    results = []
    for tbl, col, sql in checks:
        r = query_one(sql)
        cnt = r["COUNT(*)"] if r else 0
        status = "✅ 已存在" if cnt > 0 else "❌ 缺失"
        results.append({"table": tbl, "column_or_index": col, "exists": cnt > 0})
        print(f"  {status}  {tbl}.{col}")

    print(f"\n健康度：{sum(1 for r in results if r['exists'])}/{len(results)} 项通过")
    return results


def apply():
    """执行所有 Schema 变更"""
    print("=" * 60)
    print("⚠️  即将执行 Schema 变更")
    print("=" * 60)
    print("风险等级说明：")
    print("  low    - 派生列/索引添加，不影响现有数据和业务")
    print("  medium - 新增列，老数据默认值可能不符合预期")
    print()
    confirm = input("输入 'yes' 确认执行：")
    if confirm.strip().lower() != "yes":
        print("已取消")
        return

    results = []
    for change in SCHEMA_CHANGES:
        print(f"\n[{change['id']}] 执行：{change['description']} ... ", end="", flush=True)
        result = execute(change["sql"])
        if isinstance(result, dict) and "error" in result:
            print(f"❌ 失败：{result['error']}")
            results.append({**change, "status": "error", "detail": result["error"]})
        else:
            print("✅ 成功")
            results.append({**change, "status": "ok"})

    print("\n" + "=" * 60)
    print("执行结果汇总")
    print("=" * 60)
    ok = [r for r in results if r["status"] == "ok"]
    err = [r for r in results if r["status"] == "error"]
    print(f"✅ 成功：{len(ok)} 项")
    if err:
        print(f"❌ 失败：{len(err)} 项")
        for r in err:
            print(f"  [{r['id']}] {r['detail']}")
    print(f"\n回滚脚本已记录在 SCHEMA_CHANGES[].rollback，可手动执行")

    return results


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "dry_run"
    if action == "dry_run":
        dry_run()
    elif action == "apply":
        apply()
    elif action == "check":
        check_current()
    else:
        print(f"用法：python schema.py [dry_run|apply|check]")