#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库查询 & 测试用例生成模块 v2.0
支持 MySQL 和 PostgreSQL

核心能力：
1. DatabaseClient - 通用数据库查询
2. DbFixture - 为接口测试提供真实数据（db_fixture 模式）
3. TestCaseGenerator - 从数据库自动生成接口测试用例

发票类型字段规则（bw_jms_main1）：
- 数电票（INV_TYPE: 31/32/51/59/61/83/84）
    invoiceNumber -> E_INV_NUM（20位数电号码）
    invoiceCode   -> 无此字段，不传
- 税控票（INV_TYPE: 01/03/04/08/10/11/14/15）
    invoiceCode   -> INV_KIND（发票代码）
    invoiceNumber -> INV_NUM（发票号码）
- 数电纸票（INV_TYPE: 85/86/87/88）
    invoiceCode   -> INV_KIND
    invoiceNumber -> INV_NUM
    （同时也有 E_INV_NUM，可用数电号码查）
"""

import json
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union


# ── 发票类型常量（方便外部引用）──
DIGITAL_INVOICE_TYPES = {"31", "32", "51", "59", "61", "83", "84"}   # 数电票
TAX_CONTROL_TYPES = {"01", "03", "04", "08", "10", "11", "14", "15"}  # 税控票
DIGITAL_PAPER_TYPES = {"85", "86", "87", "88"}                         # 数电纸票


def get_invoice_field_mapping(inv_type: str) -> dict:
    """
    根据票种代码返回数据库字段 -> 接口入参 的映射建议。
    返回的 mapping 可直接传给 TestCaseGenerator 的各方法。

    数电票：不包含 invoiceCode 映射（接口入参不传该字段）
    税控票/数电纸票：包含 invoiceCode / invoiceNumber 映射
    """
    if inv_type in DIGITAL_INVOICE_TYPES:
        return {
            "taxNo":         "BUYER_TAXNO",
            "invoiceNumber": "E_INV_NUM",   # 20位数电号码，不映射 invoiceCode
        }
    elif inv_type in TAX_CONTROL_TYPES or inv_type in DIGITAL_PAPER_TYPES:
        return {
            "taxNo":         "BUYER_TAXNO",
            "invoiceCode":   "INV_KIND",
            "invoiceNumber": "INV_NUM",
        }
    else:
        return {
            "taxNo":         "BUYER_TAXNO",
            "invoiceNumber": "INV_NUM",
        }


# ============================================================
# DatabaseClient - 通用数据库客户端
# ============================================================

class DatabaseClient:
    """通用数据库客户端，支持 MySQL 和 PostgreSQL"""

    def __init__(self, host: str, port: int, user: str, password: str,
                 database: str, charset: str = "utf8mb4", db_type: str = "mysql"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.db_type = db_type.lower()
        self.connection = None
        self.cursor = None
        self._connect()

    def _connect(self):
        if self.db_type == "mysql":
            import pymysql
            self.connection = pymysql.connect(
                host=self.host, port=self.port, user=self.user,
                password=self.password, database=self.database,
                charset=self.charset, connect_timeout=10
            )
        elif self.db_type == "postgresql":
            import psycopg2
            self.connection = psycopg2.connect(
                host=self.host, port=self.port, user=self.user,
                password=self.password, database=self.database
            )
        else:
            raise ValueError("不支持的数据库类型: " + self.db_type)
        self.cursor = self.connection.cursor()

    def query(self, sql: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行查询，返回字典列表"""
        self.cursor.execute(sql, params)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def query_one(self, sql: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """执行查询，返回单条字典（无数据返回 None）"""
        self.cursor.execute(sql, params)
        columns = [desc[0] for desc in self.cursor.description]
        row = self.cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    def count(self, sql: str, params: tuple = None) -> int:
        """执行 COUNT 查询，返回整数"""
        self.cursor.execute(sql, params)
        row = self.cursor.fetchone()
        return row[0] if row else 0

    def execute(self, sql: str, params: tuple = None) -> int:
        """执行 INSERT/UPDATE/DELETE，返回影响行数"""
        self.cursor.execute(sql, params)
        self.connection.commit()
        return self.cursor.rowcount

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# ============================================================
# DbFixture - 数据库夹具（为接口测试注入真实数据）
# ============================================================

class DbFixture:
    """
    数据库夹具 - 为接口测试提供真实数据。
    执行多个 SQL 查询，将结果按 mapping 映射到变量名，
    供 run_isp_test.py / run_api_test.py 的 {{占位符}} 替换使用。
    """

    def __init__(self, connection: Dict[str, Any], queries: List[Dict[str, Any]],
                 variables: Dict[str, Any] = None):
        self.connection_config = connection
        self.queries = queries
        self.variables = variables or {}
        self._data = {}
        self._execute()

    def _execute(self):
        db = DatabaseClient(
            host=self.connection_config.get("host", "127.0.0.1"),
            port=self.connection_config.get("port", 3306),
            user=self.connection_config.get("user"),
            password=self.connection_config.get("password"),
            database=self.connection_config.get("database"),
            charset=self.connection_config.get("charset", "utf8mb4"),
            db_type=self.connection_config.get("type", "mysql")
        )
        try:
            for q in self.queries:
                sql = q.get("sql", "")
                mapping = q.get("mapping", {})
                # 替换 SQL 中的变量占位符
                for var_name, var_value in self.variables.items():
                    sql = sql.replace("{{" + var_name + "}}", str(var_value))
                results = db.query(sql)
                if results:
                    row = results[0]
                    for target_name, column_name in mapping.items():
                        self._data[target_name] = row.get(column_name)
        finally:
            db.close()

    def get_data(self) -> Dict[str, Any]:
        return self._data.copy()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)


# ============================================================
# TestCaseGenerator - 从数据库自动生成接口测试用例
# ============================================================

class TestCaseGenerator:
    """
    从数据库自动生成接口测试用例。

    核心流程：
    1. 定义"查询场景"：描述"从DB查什么 → 映射到哪些接口入参"
    2. 自动执行 DB 查询，将结果映射为请求体
    3. 输出可直接写入 test_config_xxx.json 的 test_cases 数组

    支持的场景模式：
    - single_row        : 查单条记录，字段值映射到入参
    - multi_row_safe    : 查多条记录，确认 < 500 条后将查询条件映射到入参
    - invoice_by_taxno  : 按购方税号查发票，自动加时间范围

    重要提示（发票类型）：
    - 数电票（31/32/51/59/61/83/84）：mapping 中不要映射 invoiceCode，
      invoiceNumber 映射 E_INV_NUM（20位数电号码）
    - 税控票（01/03/04/08/10/11/14/15）：invoiceCode -> INV_KIND, invoiceNumber -> INV_NUM
    - 数电纸票（85/86/87/88）：invoiceCode -> INV_KIND, invoiceNumber -> INV_NUM
    """

    def __init__(self, connection: Dict[str, Any],
                 buyer_tax_no: str = None,
                 variables: Dict[str, Any] = None):
        self.connection_config = connection
        self.buyer_tax_no = buyer_tax_no
        self.variables = variables or {}
        self._db = None
        self._generated_cases = []
        self._logs = []

    def _get_db(self) -> DatabaseClient:
        if self._db is None:
            self._db = DatabaseClient(
                host=self.connection_config.get("host", "127.0.0.1"),
                port=self.connection_config.get("port", 3306),
                user=self.connection_config.get("user"),
                password=self.connection_config.get("password"),
                database=self.connection_config.get("database"),
                charset=self.connection_config.get("charset", "utf8mb4"),
                db_type=self.connection_config.get("type", "mysql")
            )
        return self._db

    def _replace_vars(self, sql: str) -> str:
        """替换 SQL 中的 {{变量名}} 占位符"""
        for var_name, var_value in self.variables.items():
            sql = sql.replace("{{" + var_name + "}}", str(var_value))
        if self.buyer_tax_no:
            sql = sql.replace("{{buyer_tax_no}}", self.buyer_tax_no)
        return sql

    def _map_row(self, row: Dict[str, Any], mapping: Dict[str, str]) -> Dict[str, Any]:
        """将数据库行按映射规则转换为接口入参字典（None 值跳过）"""
        result = {}
        for api_field, db_column in mapping.items():
            val = row.get(db_column)
            if val is not None:
                result[api_field] = str(val) if not isinstance(val, (int, float, bool)) else val
        return result

    def _log(self, msg: str):
        self._logs.append(msg)
        print("[TestCaseGen] " + msg)

    def _build_time_range(self, days_back: int = 90) -> Dict[str, str]:
        """构建时间范围（默认近90天）"""
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=days_back)
        return {
            "startTime": start_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "endTime": end_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "billingDateStart": start_dt.strftime("%Y-%m-%d"),
            "billingDateEnd": end_dt.strftime("%Y-%m-%d"),
        }

    # ----------------------------------------------------------
    # 场景1: 单条记录映射
    # ----------------------------------------------------------
    def generate_single_row_case(
        self,
        case_id: str,
        case_name: str,
        case_group: str = "正常流程",
        case_desc: str = "",
        sql: str = None,
        mapping: Dict[str, str] = None,
        extra_params: Dict[str, Any] = None,
        time_range_days: int = None,
        expect_success: bool = True,
    ) -> Optional[Dict]:
        """
        从DB查询单条记录，将字段映射到接口入参，生成1个测试用例。

        注意：数电票的 mapping 中不要包含 invoiceCode 的映射；
        invoiceNumber 应映射到 E_INV_NUM（20位数电号码）。
        """
        mapping = mapping or {}
        db = self._get_db()
        sql_exec = self._replace_vars(sql)
        row = db.query_one(sql_exec)

        if row is None:
            self._log("[跳过] {} {} - DB查询无数据".format(case_id, case_name))
            return None

        body = self._map_row(row, mapping)
        if extra_params:
            body.update(extra_params)
        if time_range_days:
            body.update(self._build_time_range(time_range_days))

        case = {
            "id": case_id,
            "group": case_group,
            "name": case_name,
            "desc": case_desc or "从DB查询单条记录，映射字段: {}".format(", ".join(mapping.keys())),
            "body": body,
            "expect": {"success": expect_success},
        }
        self._generated_cases.append(case)
        self._log("[生成] {} {} - body字段: {}".format(case_id, case_name, list(body.keys())))
        return case

    # ----------------------------------------------------------
    # 场景2: 多条记录（< 500）条件映射
    # ----------------------------------------------------------
    def generate_multi_row_safe_case(
        self,
        case_id: str,
        case_name: str,
        case_group: str = "正常流程",
        case_desc: str = "",
        sql: str = None,
        count_sql: str = None,
        mapping: Dict[str, str] = None,
        filter_params: Dict[str, Any] = None,
        extra_params: Dict[str, Any] = None,
        time_range_days: int = 90,
        max_rows: int = 500,
        expect_success: bool = True,
    ) -> Optional[Dict]:
        """
        从DB按条件查询，确认结果 < max_rows 后，将查询条件映射到接口入参。
        数据量 == 0 或 > max_rows 时跳过（返回 None）。
        """
        mapping = mapping or {}
        db = self._get_db()

        if count_sql is None:
            count_sql = "SELECT COUNT(*) FROM ({}) AS _cnt".format(sql)

        count_sql_exec = self._replace_vars(count_sql)
        total = db.count(count_sql_exec)

        if total == 0:
            self._log("[跳过] {} {} - DB查询无数据".format(case_id, case_name))
            return None
        if total > max_rows:
            self._log("[跳过] {} {} - 数据量{}超过{}条限制".format(
                case_id, case_name, total, max_rows))
            return None

        data_sql = self._replace_vars(sql)
        first_row = db.query_one(data_sql)

        body = {}
        if filter_params:
            body.update(filter_params)
        if mapping and first_row:
            body.update(self._map_row(first_row, mapping))
        if extra_params:
            body.update(extra_params)
        if time_range_days:
            body.update(self._build_time_range(time_range_days))

        case = {
            "id": case_id,
            "group": case_group,
            "name": case_name,
            "desc": case_desc or "按条件查询，DB数据{}条（<{}），条件: {}".format(
                total, max_rows, ", ".join(body.keys())),
            "body": body,
            "expect": {"success": expect_success},
        }
        self._generated_cases.append(case)
        self._log("[生成] {} {} - DB数据{}条, 入参: {}".format(
            case_id, case_name, total, list(body.keys())))
        return case

    # ----------------------------------------------------------
    # 场景3: 按购方税号查询具体发票
    # ----------------------------------------------------------
    def generate_invoice_by_taxno_case(
        self,
        case_id: str,
        case_name: str,
        case_group: str = "正常流程",
        case_desc: str = "",
        sql: str = None,
        mapping: Dict[str, str] = None,
        extra_params: Dict[str, Any] = None,
        time_range_days: int = 90,
        expect_success: bool = True,
    ) -> Optional[Dict]:
        """
        按指定购方税号从DB查询发票数据，映射到接口入参（含时间范围）。
        自动在 body 中添加 taxNo（来自初始化时的 buyer_tax_no）。
        """
        if not self.buyer_tax_no:
            self._log("[跳过] {} {} - 未设置 buyer_tax_no".format(case_id, case_name))
            return None

        mapping = mapping or {}
        db = self._get_db()
        sql_exec = self._replace_vars(sql)
        row = db.query_one(sql_exec)

        if row is None:
            self._log("[跳过] {} {} - 税号{}查询无数据".format(
                case_id, case_name, self.buyer_tax_no))
            return None

        body = {"taxNo": self.buyer_tax_no}
        if mapping:
            body.update(self._map_row(row, mapping))
        if extra_params:
            body.update(extra_params)
        if time_range_days:
            body.update(self._build_time_range(time_range_days))

        case = {
            "id": case_id,
            "group": case_group,
            "name": case_name,
            "desc": case_desc or "按税号{}查询，映射字段: {}".format(
                self.buyer_tax_no, ", ".join(body.keys())),
            "body": body,
            "expect": {"success": expect_success},
        }
        self._generated_cases.append(case)
        self._log("[生成] {} {} - 税号: {}, 入参: {}".format(
            case_id, case_name, self.buyer_tax_no, list(body.keys())))
        return case

    # ----------------------------------------------------------
    # 批量生成
    # ----------------------------------------------------------
    def generate_from_scenarios(self, scenarios: List[Dict[str, Any]]) -> List[Dict]:
        """
        从场景配置列表批量生成测试用例。

        每个场景配置包含：
        - mode: "single_row" | "multi_row_safe" | "invoice_by_taxno"
        - case_id, case_name, case_group, case_desc, sql, mapping
        - （可选）count_sql, filter_params, extra_params, time_range_days, max_rows, expect_success
        """
        results = []
        for sc in scenarios:
            mode = sc.get("mode", "single_row")
            common = {
                "case_id":        sc.get("case_id", ""),
                "case_name":      sc.get("case_name", ""),
                "case_group":     sc.get("case_group", "正常流程"),
                "case_desc":      sc.get("case_desc", ""),
                "sql":            sc.get("sql", ""),
                "mapping":        sc.get("mapping", {}),
                "extra_params":   sc.get("extra_params"),
                "time_range_days": sc.get("time_range_days"),
                "expect_success": sc.get("expect_success", True),
            }

            if mode == "single_row":
                case = self.generate_single_row_case(**common)
            elif mode == "multi_row_safe":
                common["count_sql"]    = sc.get("count_sql")
                common["filter_params"] = sc.get("filter_params")
                common["max_rows"]     = sc.get("max_rows", 500)
                case = self.generate_multi_row_safe_case(**common)
            elif mode == "invoice_by_taxno":
                case = self.generate_invoice_by_taxno_case(**common)
            else:
                self._log("[跳过] 未知模式: " + mode)
                case = None

            if case:
                results.append(case)

        self._log("批量生成完成: {}/{} 个用例成功".format(len(results), len(scenarios)))
        return results

    # ----------------------------------------------------------
    # 输出
    # ----------------------------------------------------------
    def get_cases(self) -> List[Dict]:
        return list(self._generated_cases)

    def get_logs(self) -> List[str]:
        return list(self._logs)

    def export_as_json(self, output_path: str = None, indent: int = 2) -> str:
        """导出为 JSON 字符串，可选写入文件"""
        data = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_cases": len(self._generated_cases),
            "buyer_tax_no": self.buyer_tax_no,
            "cases": self._generated_cases,
        }
        json_str = json.dumps(data, ensure_ascii=False, indent=indent)
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_str)
            self._log("用例已导出: " + output_path)
        return json_str

    def close(self):
        if self._db:
            self._db.close()
            self._db = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# ============================================================
# 工具函数
# ============================================================

def replace_variables(template: Union[str, dict, list],
                      variables: Dict[str, Any]) -> Union[str, dict, list]:
    """替换模板中的变量占位符 {{变量名}}"""
    if isinstance(template, str):
        result = template
        for key, value in variables.items():
            result = result.replace("{{" + key + "}}", str(value))
        return result
    elif isinstance(template, dict):
        return {k: replace_variables(v, variables) for k, v in template.items()}
    elif isinstance(template, list):
        return [replace_variables(item, variables) for item in template]
    return template


# ============================================================
# 独立运行示例
# ============================================================

def main():
    """示例：按票种查各类型发票样本数据"""
    conn = {
        "host": "10.115.96.247", "port": 3306,
        "user": "jxindependent", "password": "Xj2zCkLJXTkEJ5j",
        "database": "jxindependent0", "charset": "utf8mb4"
    }
    buyer_tax_no = "91440606MA4WHN8C8X"

    scenarios = [
        # 税控票（01）：invoiceCode + invoiceNumber
        {
            "mode": "single_row",
            "case_id": "TC_001",
            "case_name": "01-增值税专用发票",
            "case_group": "票种覆盖-税控票",
            "sql": (
                "SELECT INV_KIND, INV_NUM, BUYER_TAXNO FROM bw_jms_main1 "
                "WHERE INV_TYPE='01' AND INV_KIND IS NOT NULL AND INV_NUM IS NOT NULL "
                "AND BUYER_TAXNO IS NOT NULL LIMIT 1"
            ),
            "mapping": {
                "taxNo":         "BUYER_TAXNO",
                "invoiceCode":   "INV_KIND",
                "invoiceNumber": "INV_NUM",
            },
        },
        # 数电票（31）：只传 invoiceNumber = E_INV_NUM，不传 invoiceCode
        {
            "mode": "single_row",
            "case_id": "TC_009",
            "case_name": "31-数电票（增值税专用发票）",
            "case_group": "票种覆盖-数电票",
            "sql": (
                "SELECT E_INV_NUM, BUYER_TAXNO FROM bw_jms_main1 "
                "WHERE INV_TYPE='31' AND E_INV_NUM IS NOT NULL "
                "AND BUYER_TAXNO IS NOT NULL LIMIT 1"
            ),
            "mapping": {
                "taxNo":         "BUYER_TAXNO",
                "invoiceNumber": "E_INV_NUM",   # 20位数电号码，不映射 invoiceCode
            },
        },
        # 按购方税号查询发票池（含时间范围）
        {
            "mode": "invoice_by_taxno",
            "case_id": "TC_020",
            "case_name": "按购方税号+销方税号查询发票池",
            "case_group": "精确查询",
            "sql": (
                "SELECT SELLER_TAXNO FROM bw_jms_main1 "
                "WHERE BUYER_TAXNO='{{buyer_tax_no}}' "
                "AND SELLER_TAXNO IS NOT NULL LIMIT 1"
            ),
            "mapping": {"salesTaxNo": "SELLER_TAXNO"},
            "extra_params": {"pageNum": 1},
            "time_range_days": 90,
        },
    ]

    with TestCaseGenerator(connection=conn, buyer_tax_no=buyer_tax_no) as gen:
        cases = gen.generate_from_scenarios(scenarios)
        print("\n生成用例数: {}".format(len(cases)))
        for c in cases:
            print("  {} {} - body keys: {}".format(c["id"], c["name"], list(c["body"].keys())))
        print(gen.export_as_json())


if __name__ == "__main__":
    main()
