"""
Natural Language Query Parser for sql-buddy.
Extracts query intent from Chinese/English descriptions.
"""
import re
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


# Common query intent patterns (Chinese)
INTENT_PATTERNS_CN = {
    "count": [r"多少", r"几个", r"数量", r"总数", r"共计", r"统计", r"count"],
    "sum": [r"总额", r"总和", r"合计", r"sum", r"总共"],
    "avg": [r"平均", r"avg", r"average", r"均值"],
    "max": [r"最大", r"最高", r"最多", r"max", r"最大值"],
    "min": [r"最小", r"最低", r"最少", r"min", r"最小值"],
    "list": [r"列出", r"展示", r"显示", r"查询", r"查找", r"找", r"看看", r"list", r"show", r"find", r"get"],
    "compare": [r"对比", r"比较", r"vs", r"versus", r"difference"],
    "top": [r"前", r"top", r"排名", r"排行", r"最"],
    "group": [r"分组", r"按.*分组", r"group by", r"each", r"每"],
    "filter": [r"条件", r"where", r"筛选", r"过滤"],
    "join": [r"关联", r"join", r"结合", r"一起", r"同时.*表", r"连表"],
}

# Time range patterns
TIME_PATTERNS = [
    (r"最近(\d+)天", "last_days"),
    (r"过去(\d+)天", "last_days"),
    (r"最近(\d+)周", "last_weeks"),
    (r"过去(\d+)周", "last_weeks"),
    (r"最近(\d+)个月", "last_months"),
    (r"过去(\d+)个月", "last_months"),
    (r"昨天", "yesterday"),
    (r"今天", "today"),
    (r"上个月", "last_month"),
    (r"这个月", "this_month"),
    (r"这周", "this_week"),
    (r"上周", "last_week"),
    (r"本年", "this_year"),
    (r"去年", "last_year"),
]


def parse_intent(query: str) -> Dict:
    """
    Parse the natural language query and extract structured intent info.
    
    Args:
        query: Natural language query string.
        
    Returns:
        Dict with intent type, tables mentioned, time range, conditions.
    """
    query_lower = query.lower().strip()
    
    detected_intents = []
    for intent, patterns in INTENT_PATTERNS_CN.items():
        for pattern in patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                detected_intents.append(intent)
                break
    
    # Detect time range
    time_range = None
    time_value = None
    for pattern, time_type in TIME_PATTERNS:
        match = re.search(pattern, query_lower)
        if match:
            time_range = time_type
            if match.groups():
                time_value = int(match.group(1))
            break
    
    # Detect tables mentioned
    # This is a simple heuristic; full table detection happens in sql_generator
    potential_tables = _extract_table_hints(query)
    
    primary_intent = "select"
    if "count" in detected_intents:
        primary_intent = "aggregate_count"
    elif "sum" in detected_intents:
        primary_intent = "aggregate_sum"
    elif "avg" in detected_intents:
        primary_intent = "aggregate_avg"
    elif "list" in detected_intents:
        primary_intent = "select"
    
    return {
        "primary_intent": primary_intent,
        "secondary_intents": [i for i in detected_intents if i != primary_intent or detected_intents.count(i) > 1][:3],
        "time_range": time_range,
        "time_value": time_value,
        "table_hints": potential_tables,
        "requires_join": "join" in detected_intents or _needs_join(query),
        "requires_group": "group" in detected_intents or "each" in query_lower or "每" in query,
        "requires_sort": "top" in detected_intents or "排序" in query or "order" in query_lower,
        "raw_query": query,
    }


def _extract_table_hints(query: str) -> list:
    """Extract possible table/field names from the query."""
    # Look for Chinese entity mentions that might map to table names
    # This is a simplified version; real matching requires schema knowledge
    hints = []
    
    # Common entity words often map to table names
    entities_cn = {
        "用户": "users", "订单": "orders", "商品": "products", "产品": "products",
        "分类": "categories", "类别": "categories", "文章": "articles", "评论": "comments",
        "交易": "transactions", "支付": "payments", "日志": "logs", "记录": "records",
        "员工": "employees", "部门": "departments", "客户": "customers", "供应商": "suppliers",
    }
    
    for cn_term, en_table in entities_cn.items():
        if cn_term in query:
            hints.append(en_table)
    
    return hints


def _needs_join(query: str) -> bool:
    """Heuristic: does the query mention multiple entities that likely span tables?"""
    entity_count = 0
    entities = ["用户", "订单", "商品", "产品", "分类", "用户", "评论", "支付", "部门"]
    for entity in entities:
        if entity in query:
            entity_count += 1
    return entity_count >= 2


def build_nl_prompt(query: str, schema_text: str, dialect: str = "sqlite") -> str:
    """
    Build the LLM prompt for NL → SQL generation.
    
    Args:
        query: The natural language query.
        schema_text: The formatted schema string.
        dialect: Target database dialect.
        
    Returns:
        Prompt string for LLM.
    """
    # Few-shot examples
    examples = {
        "sqlite": """Examples (SQLite):
Q: "有几张表"
A: SELECT name FROM sqlite_master WHERE type='table'

Q: "每种状态有多少用户"
A: SELECT status, COUNT(*) as count FROM users GROUP BY status

Q: "最近7天注册了多少用户"
A: SELECT COUNT(*) as new_users FROM users WHERE created_at >= DATE('now', '-7 days')

Q: "查询订单最多的前10个用户"
A: SELECT u.name, COUNT(o.id) as order_count 
   FROM users u JOIN orders o ON u.id = o.user_id 
   GROUP BY u.id ORDER BY order_count DESC LIMIT 10
""",
        "postgresql": """Examples (PostgreSQL):
Q: "最近7天注册了多少用户"  
A: SELECT COUNT(*) as new_users FROM users WHERE created_at >= NOW() - INTERVAL '7 days'

Q: "每个品类上个月的销售额"
A: SELECT c.name, SUM(oi.quantity * oi.price) as total_sales
   FROM order_items oi JOIN products p ON oi.product_id = p.id
   JOIN categories c ON p.category_id = c.id
   JOIN orders o ON oi.order_id = o.id
   WHERE o.created_at >= DATE_TRUNC('month', NOW() - INTERVAL '1 month')
     AND o.created_at < DATE_TRUNC('month', NOW())
   GROUP BY c.name ORDER BY total_sales DESC
""",
        "mysql": """Examples (MySQL):
Q: "最近7天注册了多少用户"
A: SELECT COUNT(*) as new_users FROM users WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
""",
    }
    
    example_text = examples.get(dialect, examples["sqlite"])
    
    prompt = f"""You are a SQL expert. Given a database schema and a natural language query, generate the correct SQL.

Target dialect: {dialect}

{schema_text}

{example_text}

Rules:
- Generate ONLY the SQL statement, no explanations unless asked
- Use the correct {dialect} dialect syntax
- Always use AS aliases for computed columns
- Use table aliases for JOIN queries
- Add LIMIT clause for SELECT queries if not specified
- The query MUST be read-only (SELECT only)
- Do NOT generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE

Natural Language Query: {query}

SQL:"""
    
    return prompt


def extract_query_summary(query: str) -> str:
    """Create a concise, searchable summary of the query intent."""
    # Remove common filler words
    cleaned = query.strip()
    # Truncate
    if len(cleaned) > 80:
        cleaned = cleaned[:77] + "..."
    return cleaned
