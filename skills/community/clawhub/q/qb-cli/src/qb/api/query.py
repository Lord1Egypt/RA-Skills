"""Query builder helpers for QuickBooks SQL-like queries."""

from urllib.parse import quote


def build_query(
    entity: str,
    where: str = "",
    select: str = "*",
    max_results: int = 100,
    order_by: str = "",
) -> str:
    """Build a QuickBooks query string.

    Args:
        entity: Entity name (Customer, Invoice, etc.)
        where: Optional WHERE clause (without the WHERE keyword)
        select: Fields to select (default: *)
        max_results: Maximum results to return
        order_by: Optional ORDER BY clause (without the ORDER BY keyword)

    Returns:
        Complete query string.

    Example:
        >>> build_query("Customer", where="Active = true", max_results=50)
        "SELECT * FROM Customer WHERE Active = true MAXRESULTS 50"
    """
    parts = [f"SELECT {select} FROM {entity}"]

    if where:
        parts.append(f"WHERE {where}")

    if order_by:
        parts.append(f"ORDERBY {order_by}")

    parts.append(f"MAXRESULTS {max_results}")

    return " ".join(parts)


def escape_query_value(value: str) -> str:
    """Escape a string value for use in a QuickBooks query.

    QuickBooks uses single quotes for string values and
    escapes single quotes by doubling them.
    """
    return value.replace("'", "''")
