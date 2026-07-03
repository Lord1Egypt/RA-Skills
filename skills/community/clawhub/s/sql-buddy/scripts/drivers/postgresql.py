"""PostgreSQL driver adapter."""
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


def check_available() -> bool:
    """Check if psycopg2 is available."""
    try:
        import psycopg2
        return True
    except ImportError:
        return False


def get_tables(config: Dict) -> list:
    """Get all tables in a PostgreSQL database."""
    if not check_available():
        logger.warning("psycopg2 not installed")
        return []
    
    import psycopg2
    conn = psycopg2.connect(
        host=config["host"], port=config["port"],
        dbname=config["database"], user=config["username"],
        password=config["password"],
    )
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' ORDER BY table_name
        """)
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()
