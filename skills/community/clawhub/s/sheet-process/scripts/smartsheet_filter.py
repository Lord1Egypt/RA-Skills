"""
腾讯文档智能表格（SmartSheet）通用筛选工具

参数化设计：
  A — filter_columns：需要筛选的列，支持列索引(1-based)或列标题
  B — keywords：二维数组，每个子数组对应 A 中该列的关键词列表
  C — union_mode：每列关键词之间取并集(True)还是交集(False)
  D — return_columns：结果表格中需要返回的列

跨列组合方式通过 column_combine 参数控制（交集/并集）。

用法示例：
    from smartsheet_filter import SmartsheetFilter

    sf = SmartsheetFilter(
        file_id="DuDsNLlNBaFZ",
        sheet_title="27届内推企业",
    )

    results = sf.filter(
        filter_columns=["招聘岗位", "所属行业"],           # A
        keywords=[["前端","开发","研发","软件"], ["互联网"]], # B
        union_mode=[True, True],                             # C
        return_columns=["招聘企业", "投递链接"],              # D
        column_combine="intersection",
    )
"""

import json
import subprocess
import sys
import os

# ──────────────────────────────────────────────
# 核心类
# ──────────────────────────────────────────────

class SmartsheetFilter:
    """智能表格通用筛选器"""

    TENCENT_DOCS_DIR = "/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/resources/builtin-plugins/tencent-docs-plugin/skills/tencent-docs"

    def __init__(self, file_id: str, sheet_title: str = None, sheet_id: str = None):
        """
        Args:
            file_id:   腾讯文档 file_id
            sheet_title: 工作表标题（与 sheet_id 二选一）
            sheet_id:  工作表 ID（与 sheet_title 二选一）
        """
        self.file_id = file_id
        self.sheet_title = sheet_title
        self._sheet_id = sheet_id
        self._fields = None          # [{field_id, field_title, field_type}, ...]
        self._all_records = None     # 原始记录列表

    # ── 静态方法：文档级操作（不需要实例） ──

    @classmethod
    def list_tables(cls, file_id: str) -> list:
        """
        列出文档中所有工作表。
        
        Returns:
            list[dict]: [{"sheet_id": "xxx", "title": "xxx"}, ...]
        """
        result = subprocess.run(
            [
                "python3", "tencentdocs.py", "tdoc_call",
                "tencent-docs", "smartsheet.list_tables",
                json.dumps({"file_id": file_id}, ensure_ascii=False)
            ],
            capture_output=True, text=True,
            cwd=cls.TENCENT_DOCS_DIR,
        )
        data = json.loads(result.stdout)
        sc = data.get("result", {}).get("structuredContent", {})
        return sc.get("sheets", [])

    # ── 内部工具方法 ──

    def _tdoc_call(self, service: str, tool: str, args: dict) -> dict:
        """调用腾讯文档 MCP 接口"""
        result = subprocess.run(
            [
                "python3", "tencentdocs.py", "tdoc_call",
                service, tool, json.dumps(args, ensure_ascii=False)
            ],
            capture_output=True, text=True,
            cwd=self.TENCENT_DOCS_DIR,
        )
        data = json.loads(result.stdout)
        sc = data.get("result", {}).get("structuredContent", {})
        text_block = data.get("result", {}).get("content", [{}])[0].get("text", "{}")
        # structuredContent 优先，否则用 text 解析
        if sc:
            return sc
        return json.loads(text_block)

    def _resolve_sheet_id(self):
        """如果只给了标题，自动查找 sheet_id"""
        if self._sheet_id:
            return
        tables = self._tdoc_call("tencent-docs", "smartsheet.list_tables", {"file_id": self.file_id})
        sheets = tables.get("sheets", [])
        for s in sheets:
            if s.get("title") == self.sheet_title:
                self._sheet_id = s["sheet_id"]
                return
        # 也尝试模糊匹配
        for s in sheets:
            if self.sheet_title and self.sheet_title in s.get("title", ""):
                self._sheet_id = s["sheet_id"]
                print(f"[提示] 模糊匹配到工作表: {s['title']}", file=sys.stderr)
                return
        raise ValueError(f"未找到标题为 '{self.sheet_title}' 的工作表。可用表格: {[s['title'] for s in sheets]}")

    @property
    def sheet_id(self):
        if not self._sheet_id:
            self._resolve_sheet_id()
        return self._sheet_id

    def _load_fields(self):
        """加载字段列表"""
        if self._fields is not None:
            return
        data = self._tdoc_call("tencent-docs", "smartsheet.list_fields", {
            "file_id": self.file_id,
            "sheet_id": self.sheet_id,
        })
        self._fields = data.get("fields", [])
        # 构建标题→索引映射 (1-based)
        self._title_to_idx = {}
        self._title_to_field = {}
        for i, f in enumerate(self._fields):
            self._title_to_idx[f["field_title"]] = i + 1
            self._title_to_field[f["field_title"]] = f

    def _load_all_records(self):
        """分页拉取全部记录"""
        if self._all_records is not None:
            return
        self._all_records = []
        offset = 0
        while True:
            data = self._tdoc_call("tencent-docs", "smartsheet.list_records", {
                "file_id": self.file_id,
                "sheet_id": self.sheet_id,
                "limit": 100,
                "offset": offset,
            })
            records = data.get("records", [])
            self._all_records.extend(records)
            if not data.get("has_more"):
                break
            offset = data.get("next", 0)

    # ── 列解析 ──

    def _resolve_column(self, col):
        """
        将列描述符解析为 field_title（API 记录的 field 字段使用标题作为 key）。
        支持：整数索引(1-based)、字符串标题
        """
        if isinstance(col, int):
            if col < 1 or col > len(self._fields):
                raise IndexError(f"列索引 {col} 超出范围 1~{len(self._fields)}")
            return self._fields[col - 1]["field_title"]
        elif isinstance(col, str):
            if col not in self._title_to_idx:
                available = list(self._title_to_idx.keys())
                raise KeyError(f"未找到列 '{col}'。可用列: {available}")
            return col
        else:
            raise TypeError(f"列描述符必须是 int 或 str，不能是 {type(col)}")

    def _resolve_columns(self, cols: list) -> list:
        """批量解析列描述符，返回 field_title 列表"""
        return [self._resolve_column(c) for c in cols]

    def _get_cell_text(self, record: dict, field_title: str) -> str:
        """
        取出记录中某列的纯文本值。
        API 返回的 field_values 中 field key 存的是列标题。
        覆盖 text_value 和 option_value 两种值类型。
        """
        for fv in record.get("field_values", []):
            if fv.get("field") != field_title:
                continue
            # text 类型
            text_items = fv.get("text_value", {}).get("items", [])
            if text_items:
                return "".join(item.get("text", "") for item in text_items)
            # select / singleSelect 类型（key 是 option_value）
            select_items = fv.get("option_value", {}).get("items", [])
            if select_items:
                return "".join(item.get("text", "") for item in select_items)
        return ""

    def _get_cell_value(self, record: dict, field_title: str) -> str:
        """
        取出记录中某列的展示值（覆盖 text / url / option_value 三种类型）。
        """
        for fv in record.get("field_values", []):
            if fv.get("field") != field_title:
                continue
            # text 类型
            text_items = fv.get("text_value", {}).get("items", [])
            if text_items:
                return "".join(item.get("text", "") for item in text_items)
            # url 类型
            url_items = fv.get("url_value", {}).get("items", [])
            if url_items:
                return url_items[0].get("link", "") if url_items else ""
            # select / singleSelect 类型
            select_items = fv.get("option_value", {}).get("items", [])
            if select_items:
                return select_items[0].get("text", "")
        return ""

    # ── 核心筛选逻辑 ──

    def filter(
        self,
        filter_columns: list,       # A: 要筛选的列 [3, 7] 或 ["招聘岗位", "所属行业"]
        keywords: list,             # B: 二维关键词数组 [["前端","开发"], ["互联网"]]
        union_mode: list,           # C: 每列取并集(True)还是交集(False) [True, True]
        return_columns: list,       # D: 返回哪些列 [2, 8] 或 ["招聘企业", "投递链接"]
        column_combine: str = "intersection",  # 跨列组合: "intersection" | "union"
    ) -> list:
        """
        执行筛选，返回匹配的记录列表。

        Args:
            filter_columns (A): 要筛选的列，支持列索引(int)或列标题(str)
            keywords (B):       [[kw1, kw2], [kw3, kw4, ...]]，与 filter_columns 一一对应
            union_mode (C):     [bool, bool, ...]，True=并集, False=交集
            return_columns (D): 结果中需返回的列
            column_combine:     "intersection"(且) / "union"(或)，控制跨列组合方式

        Returns:
            list[dict]: 每条记录包含 {列标题: 值, "_matched": {列标题: [匹配的关键词]}}
        """
        # 初始化
        self._load_fields()
        self._load_all_records()

        # 校验参数
        n_cols = len(filter_columns)
        if len(keywords) != n_cols:
            raise ValueError(f"keywords 长度({len(keywords)})与 filter_columns 长度({n_cols})不匹配")
        if len(union_mode) != n_cols:
            raise ValueError(f"union_mode 长度({len(union_mode)})与 filter_columns 长度({n_cols})不匹配")

        # 解析列为标题列表（API 用标题做 key）
        resolved_filter = self._resolve_columns(filter_columns)
        resolved_return = self._resolve_columns(return_columns)

        results = []
        for record in self._all_records:
            col_match_results = []      # 每列是否匹配
            matched_details = {}        # 匹配详情

            for col_idx in range(n_cols):
                ftitle = resolved_filter[col_idx]
                cell_text = self._get_cell_text(record, ftitle)
                kws = keywords[col_idx]
                is_union = union_mode[col_idx]

                # 逐一检查关键词
                hit_flags = [kw in cell_text for kw in kws]
                hit_kws = [kw for kw, hit in zip(kws, hit_flags) if hit]

                if is_union:
                    col_match = any(hit_flags)
                else:
                    col_match = all(hit_flags)

                col_match_results.append(col_match)
                if hit_kws:
                    matched_details[ftitle] = hit_kws

            # 跨列组合
            if column_combine == "intersection":
                overall_match = all(col_match_results)
            else:  # union
                overall_match = any(col_match_results)

            if overall_match:
                row = {}
                for ftitle in resolved_return:
                    row[ftitle] = self._get_cell_value(record, ftitle)
                row["_matched"] = matched_details
                results.append(row)

        return results

    # ── 便捷方法 ──

    def filter_to_html(
        self,
        filter_columns: list,
        keywords: list,
        union_mode: list,
        return_columns: list,
        column_combine: str = "intersection",
        title: str = "筛选结果",
        output_path: str = None,
    ) -> str:
        """
        执行筛选并生成 HTML 表格文件。

        Returns:
            str: HTML 文件路径
        """
        results = self.filter(filter_columns, keywords, union_mode, return_columns, column_combine)
        return generate_html(results, return_columns, title, output_path)

    def filter_to_json(
        self,
        filter_columns: list,
        keywords: list,
        union_mode: list,
        return_columns: list,
        column_combine: str = "intersection",
        output_path: str = None,
    ) -> dict:
        """
        执行筛选并生成结构化 JSON（适合作为下游节点输入）。

        JSON 结构：
        {
          "meta": {
            "file_id": "...",
            "sheet_title": "...",
            "filter_params": { filter_columns, keywords, union_mode, return_columns, column_combine },
            "total_records": 137,
            "matched_count": 30,
            "timestamp": "2026-07-30T20:23:42"
          },
          "records": [
            { "招聘企业": "...", "投递链接": "...", "_matched": {"招聘岗位": ["前端"]} },
            ...
          ]
        }

        Returns:
            dict: 完整的 JSON 结构（同时也写入 output_path 如果指定）
        """
        from datetime import datetime

        # 先拿总数
        self._load_fields()
        self._load_all_records()
        total = len(self._all_records)

        results = self.filter(filter_columns, keywords, union_mode, return_columns, column_combine)

        # 解析返回列标题
        resolved_return_titles = self._resolve_columns(return_columns)

        payload = {
            "meta": {
                "file_id": self.file_id,
                "sheet_title": self.sheet_title,
                "filter_params": {
                    "filter_columns": filter_columns,
                    "keywords": keywords,
                    "union_mode": union_mode,
                    "return_columns": resolved_return_titles,
                    "column_combine": column_combine,
                },
                "total_records": total,
                "matched_count": len(results),
                "return_columns": resolved_return_titles,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            },
            "records": results,
        }

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)

        return payload

    def list_columns(self):
        """列出所有列及其索引，方便用户选择"""
        self._load_fields()
        for i, f in enumerate(self._fields):
            print(f"  {i+1:>3d}. [{f['field_type']}] {f['field_title']}")

    def describe_fields(self) -> list:
        """
        返回结构化字段列表，方便程序化使用。
        
        Returns:
            list[dict]: [{"index": 1, "title": "招聘企业", "type": "text"}, ...]
        """
        self._load_fields()
        return [
            {"index": i + 1, "title": f["field_title"], "type": f.get("field_type", "text")}
            for i, f in enumerate(self._fields)
        ]


# ──────────────────────────────────────────────
# HTML 生成工具
# ──────────────────────────────────────────────

def generate_html(
    results: list,
    column_titles: list,
    title: str = "筛选结果",
    output_path: str = None,
) -> str:
    """将筛选结果生成 HTML 表格"""

    # 解析列标题（可能是 int 索引或 str 标题，这里都是 str）
    resolved_titles = []
    for col in column_titles:
        if isinstance(col, int):
            resolved_titles.append(f"第{col}列")
        else:
            resolved_titles.append(str(col))

    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="zh-CN">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>{title}</title>',
        '<style>',
        '  *{margin:0;padding:0;box-sizing:border-box;}',
        '  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#f5f5f5;color:#333;padding:24px;}',
        '  .container{max-width:1000px;margin:0 auto;}',
        '  h1{font-size:22px;color:#1a1a1a;margin-bottom:8px;}',
        '  .subtitle{font-size:14px;color:#888;margin-bottom:20px;}',
        '  .stats{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap;}',
        '  .stat-badge{background:#e8f0fe;color:#1a73e8;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:500;}',
        '  .stat-badge.total{background:#fce8e6;color:#d93025;}',
        '  table{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.08);}',
        '  thead th{background:#1a73e8;color:#fff;padding:12px 16px;text-align:left;font-size:14px;font-weight:600;}',
        '  thead th:first-child{width:50px;text-align:center;}',
        '  tbody td{padding:10px 16px;border-bottom:1px solid #eee;font-size:14px;vertical-align:middle;}',
        '  tbody td:first-child{text-align:center;color:#999;}',
        '  tbody td .company{font-weight:600;color:#1a1a1a;}',
        '  tbody td .matched-kw{display:inline-block;font-size:11px;color:#1a73e8;background:#e8f0fe;padding:2px 8px;border-radius:4px;margin-right:4px;}',
        '  tbody td a{color:#1a73e8;text-decoration:none;word-break:break-all;font-size:13px;}',
        '  tbody td a:hover{text-decoration:underline;}',
        '  tbody tr:hover{background:#f8faff;}',
        '  tbody tr:nth-child(even){background:#fafafa;}',
        '  .footer{margin-top:16px;font-size:12px;color:#aaa;text-align:center;}',
        '</style>',
        '</head>',
        '<body>',
        '<div class="container">',
        f'<h1>{title}</h1>',
        f'<p class="subtitle">共筛选出 {len(results)} 条结果</p>',
        '<div class="stats">',
        f'<span class="stat-badge total">共 {len(results)} 条</span>',
        '</div>',
        '<table><thead><tr><th>#</th>',
    ]

    # 表头
    for t in resolved_titles:
        html_parts.append(f'<th>{t}</th>')

    html_parts.append('</tr></thead><tbody>')

    # 行
    for i, row in enumerate(results, 1):
        html_parts.append(f'<tr><td>{i}</td>')
        for t in resolved_titles:
            val = row.get(t, "")
            if val.startswith("http"):
                val = f'<a href="{val}" target="_blank">{val}</a>'
            else:
                val = val.replace("<", "&lt;").replace(">", "&gt;")
            html_parts.append(f'<td>{val}</td>')
        html_parts.append('</tr>')

    html_parts.extend([
        '</tbody></table>',
        '<p class="footer">由 SmartsheetFilter 工具自动生成</p>',
        '</div></body></html>',
    ])

    html = "\n".join(html_parts)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    return html


# ──────────────────────────────────────────────
# 命令行入口
# ──────────────────────────────────────────────

if __name__ == "__main__":
    """
    命令行用法示例：

    # 1. 列出现有列
    python3 smartsheet_filter.py --file-id DuDsNLlNBaFZ --sheet "27届内推企业" --list-cols

    # 2. 执行筛选（用列标题）
    python3 smartsheet_filter.py --file-id DuDsNLlNBaFZ --sheet "27届内推企业" \\
        --filter-cols "招聘岗位,所属行业" \\
        --keywords "前端#开发#研发#软件,互联网" \\
        --union-mode "true,true" \\
        --return-cols "招聘企业,投递链接" \\
        --combine intersection \\
        --output /tmp/result.html

    # 3. 执行筛选（用列索引 1-based）
    python3 smartsheet_filter.py --file-id DuDsNLlNBaFZ --sheet "27届内推企业" \\
        --filter-cols "1,3" \\
        --keywords "前端#开发#研发,互联网" \\
        --union-mode "true,true" \\
        --return-cols "2,4" \\
        --combine union
    """
    import argparse

    parser = argparse.ArgumentParser(description="腾讯文档智能表格通用筛选工具")
    parser.add_argument("--file-id", required=True, help="腾讯文档 file_id")
    parser.add_argument("--sheet", required=True, help="工作表标题")
    parser.add_argument("--list-cols", action="store_true", help="列出所有列")
    parser.add_argument("--filter-cols", help="筛选列，逗号分隔。如 '3,7' 或 '招聘岗位,所属行业'")
    parser.add_argument("--keywords", help="关键词，#分隔同列关键词，逗号分隔不同列。如 '前端#开发,互联网'")
    parser.add_argument("--union-mode", help="每列取并集(true)还是交集(false)，逗号分隔。如 'true,true'")
    parser.add_argument("--return-cols", help="返回列，逗号分隔。如 '2,8'")
    parser.add_argument("--combine", default="intersection", choices=["intersection", "union"])
    parser.add_argument("--format", default="html", choices=["html", "json", "both"],
                        help="输出格式：html(给人看) / json(给下游节点) / both(同时输出)")
    parser.add_argument("--output", help="输出文件路径（html 和 json 各自加后缀）")
    parser.add_argument("--title", default="筛选结果", help="HTML 标题")

    args = parser.parse_args()

    sf = SmartsheetFilter(file_id=args.file_id, sheet_title=args.sheet)

    if args.list_cols:
        sf.list_columns()
        sys.exit(0)

    # 解析参数
    def parse_cols(s: str):
        """解析列参数，支持整数和字符串"""
        result = []
        for part in s.split(","):
            part = part.strip()
            try:
                result.append(int(part))
            except ValueError:
                result.append(part)
        return result

    filter_cols = parse_cols(args.filter_cols)
    keywords = [[kw.strip() for kw in group.split("#")] for group in args.keywords.split(",")]
    union_mode = [s.strip().lower() == "true" for s in args.union_mode.split(",")]
    return_cols = parse_cols(args.return_cols)

    # 解析输出路径
    base_output = args.output or "/tmp/smartsheet_filter_result"

    if args.format in ("html", "both"):
        html_path = base_output if base_output.endswith(".html") else base_output + ".html"
        count = len(sf.filter(filter_cols, keywords, union_mode, return_cols, args.combine))
        sf.filter_to_html(
            filter_columns=filter_cols,
            keywords=keywords,
            union_mode=union_mode,
            return_columns=return_cols,
            column_combine=args.combine,
            title=args.title,
            output_path=html_path,
        )
        print(f"匹配记录数: {count}")
        print(f"HTML 已输出到: {html_path}")

    if args.format in ("json", "both"):
        json_path = base_output if base_output.endswith(".json") else base_output + ".json"
        payload = sf.filter_to_json(
            filter_columns=filter_cols,
            keywords=keywords,
            union_mode=union_mode,
            return_columns=return_cols,
            column_combine=args.combine,
            output_path=json_path,
        )
        print(f"匹配记录数: {payload['meta']['matched_count']}")
        print(f"JSON 已输出到: {json_path}")
