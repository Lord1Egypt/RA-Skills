import pyodbc
import sys

conn_str = (
    'DRIVER={SQL Server};'
    'SERVER=LTEDP056\\SQLEXPRESS,1433;'
    'DATABASE=PDFExtraction;'
    'UID=ptcl-bot;PWD=ptcl-bot123'
)

def query_items_by_date(start_date=None, end_date=None):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    if start_date and end_date:
        query = """
        SELECT h.DeliveryNo, h.ScheduledDeliveryDate, i.ItemNo, i.ItemCode, 
               i.ItemDescription, i.DeliveryQty, i.Unit, i.NetWeight, i.Batch
        FROM DeliveryHeaders h
        INNER JOIN DeliveryItems i ON h.DeliveryNo = i.DeliveryNo
        WHERE h.ScheduledDeliveryDate BETWEEN ? AND ?
        ORDER BY h.ScheduledDeliveryDate
        """
        cursor.execute(query, (start_date, end_date))
    else:
        query = """
        SELECT h.DeliveryNo, h.ScheduledDeliveryDate, i.ItemNo, i.ItemCode, 
               i.ItemDescription, i.DeliveryQty, i.Unit, i.NetWeight, i.Batch
        FROM DeliveryHeaders h
        INNER JOIN DeliveryItems i ON h.DeliveryNo = i.DeliveryNo
        ORDER BY h.ScheduledDeliveryDate
        """
        cursor.execute(query)
    
    cols = [c[0] for c in cursor.description]
    result = [" | ".join(cols), "-" * 120]
    for row in cursor.fetchall():
        result.append(" | ".join(str(x) for x in row))
    conn.close()
    return "\n".join(result)

def summary_by_day():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    query = """
    SELECT CAST(h.ScheduledDeliveryDate AS DATE) AS Day, 
           COUNT(*) AS TotalDeliveries, SUM(i.DeliveryQty) AS TotalItems
    FROM DeliveryHeaders h
    INNER JOIN DeliveryItems i ON h.DeliveryNo = i.DeliveryNo
    GROUP BY CAST(h.ScheduledDeliveryDate AS DATE)
    ORDER BY Day
    """
    cursor.execute(query)
    cols = [c[0] for c in cursor.description]
    result = [" | ".join(cols), "-" * 60]
    for row in cursor.fetchall():
        result.append(" | ".join(str(x) for x in row))
    conn.close()
    return "\n".join(result)

def summary_by_month():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    query = """
    SELECT YEAR(h.ScheduledDeliveryDate) AS Year, MONTH(h.ScheduledDeliveryDate) AS Month,
           COUNT(*) AS TotalDeliveries, SUM(i.DeliveryQty) AS TotalItems
    FROM DeliveryHeaders h
    INNER JOIN DeliveryItems i ON h.DeliveryNo = i.DeliveryNo
    GROUP BY YEAR(h.ScheduledDeliveryDate), MONTH(h.ScheduledDeliveryDate)
    ORDER BY Year, Month
    """
    cursor.execute(query)
    cols = [c[0] for c in cursor.description]
    result = [" | ".join(cols), "-" * 60]
    for row in cursor.fetchall():
        result.append(" | ".join(str(x) for x in row))
    conn.close()
    return "\n".join(result)

def summary_by_year():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    query = """
    SELECT YEAR(h.ScheduledDeliveryDate) AS Year,
           COUNT(*) AS TotalDeliveries, SUM(i.DeliveryQty) AS TotalItems
    FROM DeliveryHeaders h
    INNER JOIN DeliveryItems i ON h.DeliveryNo = i.DeliveryNo
    GROUP BY YEAR(h.ScheduledDeliveryDate)
    ORDER BY Year
    """
    cursor.execute(query)
    cols = [c[0] for c in cursor.description]
    result = [" | ".join(cols), "-" * 60]
    for row in cursor.fetchall():
        result.append(" | ".join(str(x) for x in row))
    conn.close()
    return "\n".join(result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if "day" in arg:
            print(summary_by_day())
        elif "month" in arg:
            print(summary_by_month())
        elif "year" in arg:
            print(summary_by_year())
        else:
            print(query_items_by_date())