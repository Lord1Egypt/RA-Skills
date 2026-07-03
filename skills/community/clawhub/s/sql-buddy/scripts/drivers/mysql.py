"""MySQL driver adapter."""
import logging
logger = logging.getLogger(__name__)


def check_available() -> bool:
    try:
        import pymysql
        return True
    except ImportError:
        return False


def get_tables(config: Dict) -> list:
    if not check_available():
        logger.warning("pymysql not installed")
        return []
    
    import pymysql
    conn = pymysql.connect(
        host=config["host"], port=config["port"],
        database=config["database"], user=config["username"],
        password=config["password"],
    )
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()")
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()
