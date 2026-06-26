"""
Unit tests for sql_connector.py

All tests use MagicMock to simulate pymssql — no live DB required.
These tests verify the connector's API contract, retry logic,
error handling, sealed methods, and dynamic backend resolution.
"""

import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch, call

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Mock pymssql before importing sql_connector ──────────────────────────────
# pymssql is not available in CI — mock it at the module level.

mock_pymssql = types.ModuleType('pymssql')

class _MockCursor:
    def __init__(self, as_dict=False):
        self._as_dict = as_dict
        self.execute = MagicMock()
        self._rows = []
        self._scalar = None

    def fetchall(self):
        return self._rows

    def fetchone(self):
        return self._scalar

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

class _MockConn:
    def cursor(self, as_dict=False):
        return _MockCursor(as_dict=as_dict)

    def commit(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

mock_pymssql.connect = MagicMock(return_value=_MockConn())
mock_pymssql.OperationalError = Exception
mock_pymssql.DatabaseError = Exception
mock_pymssql.Error = Exception
sys.modules['pymssql'] = mock_pymssql

# Now import (pymssql is mocked)
import sql_connector as sc
from sql_connector import (
    get_connector,
    MSSQLConnector,
    SQLConnector,
    SQLConnectorError,
    SQLConnectionError,
    SQLQueryError,
    _resolve_backend,
    _BACKENDS,
)


# ── Helper ────────────────────────────────────────────────────────────────────

def make_connector(backend='local') -> MSSQLConnector:
    """Create a connector without triggering real env resolution."""
    return MSSQLConnector(backend)


# ── Tests: Backend resolution ─────────────────────────────────────────────────

class TestResolveBackend(unittest.TestCase):

    def test_local_backend_resolves(self):
        cfg = _resolve_backend('local')
        self.assertIn('server', cfg)
        self.assertIn('database', cfg)
        self.assertIn('user', cfg)
        self.assertIn('password', cfg)
        self.assertIn('port', cfg)

    def test_cloud_backend_resolves(self):
        cfg = _resolve_backend('cloud')
        self.assertIn('server', cfg)

    def test_dynamic_backend_resolves_from_env(self):
        with patch.dict(os.environ, {
            'SQL_TAT_SERVER': 'tat-server',
            'SQL_TAT_DATABASE': 'db_tat',
            'SQL_TAT_USER': 'tat_user',
            'SQL_TAT_PASSWORD': 'tat_pass',
        }):
            cfg = _resolve_backend('tat')
            self.assertEqual(cfg['server'], 'tat-server')
            self.assertEqual(cfg['database'], 'db_tat')
            self.assertEqual(cfg['user'], 'tat_user')
            self.assertEqual(cfg['port'], 1433)

    def test_dynamic_backend_custom_port(self):
        with patch.dict(os.environ, {
            'SQL_HFTC_SERVER': 'hftc-server',
            'SQL_HFTC_DATABASE': 'db_hftc',
            'SQL_HFTC_USER': 'u',
            'SQL_HFTC_PASSWORD': 'p',
            'SQL_HFTC_PORT': '1434',
        }):
            cfg = _resolve_backend('hftc')
            self.assertEqual(cfg['port'], 1434)

    def test_unknown_backend_without_env_raises(self):
        # Remove any SQL_UNKNOWN_SERVER from env
        env = {k: v for k, v in os.environ.items() if 'SQL_UNKNOWN_' not in k}
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ValueError) as ctx:
                _resolve_backend('unknown')
            self.assertIn('SQL_UNKNOWN_SERVER', str(ctx.exception))

    def test_case_insensitive_identifier(self):
        """Backend identifier is uppercased to form env var prefix."""
        with patch.dict(os.environ, {
            'SQL_PROD_SERVER': 'prod-server',
            'SQL_PROD_DATABASE': 'db_prod',
            'SQL_PROD_USER': 'u',
            'SQL_PROD_PASSWORD': 'p',
        }):
            cfg = _resolve_backend('prod')
            self.assertEqual(cfg['server'], 'prod-server')


# ── Tests: Connector instantiation ───────────────────────────────────────────

class TestConnectorInstantiation(unittest.TestCase):

    def test_get_connector_returns_mssql_instance(self):
        db = get_connector('local')
        self.assertIsInstance(db, MSSQLConnector)
        self.assertIsInstance(db, SQLConnector)

    def test_connector_backend_property(self):
        db = make_connector('local')
        self.assertEqual(db.backend, 'local')

    def test_from_env_returns_connector(self):
        db = MSSQLConnector.from_env('local')
        self.assertIsInstance(db, MSSQLConnector)

    def test_dynamic_backend_instantiation(self):
        with patch.dict(os.environ, {
            'SQL_TAT_SERVER': 'tat',
            'SQL_TAT_DATABASE': 'db',
            'SQL_TAT_USER': 'u',
            'SQL_TAT_PASSWORD': 'p',
        }):
            db = get_connector('tat')
            self.assertIsInstance(db, MSSQLConnector)
            self.assertEqual(db.backend, 'tat')

    def test_cannot_instantiate_abstract_directly(self):
        """SQLConnector is abstract — direct instantiation should fail."""
        with self.assertRaises(TypeError):
            SQLConnector('local')  # type: ignore


# ── Tests: Sealed methods ─────────────────────────────────────────────────────

class TestSealedMethods(unittest.TestCase):

    def test_cannot_override_execute(self):
        with self.assertRaises(TypeError):
            class BadConnector(MSSQLConnector):
                def execute(self, sql, params=()):  # type: ignore
                    return True

    def test_cannot_override_query(self):
        with self.assertRaises(TypeError):
            class BadConnector(MSSQLConnector):
                def query(self, sql, params=()):  # type: ignore
                    return []


# ── Tests: query() ───────────────────────────────────────────────────────────

class TestQuery(unittest.TestCase):

    def _make_conn(self, rows):
        cursor = _MockCursor(as_dict=True)
        cursor._rows = rows
        conn = _MockConn()
        conn.cursor = MagicMock(return_value=cursor)
        return conn

    def test_query_returns_list(self):
        conn = self._make_conn([{'id': 1, 'val': 'x'}])
        db = make_connector()
        with patch.object(db, '_connect', return_value=conn):
            result = db.query("SELECT id, val FROM t WHERE x=%s", ('a',))
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['id'], 1)

    def test_query_empty_result(self):
        conn = self._make_conn([])
        db = make_connector()
        with patch.object(db, '_connect', return_value=conn):
            result = db.query("SELECT 1")
        self.assertEqual(result, [])

    def test_query_passes_params(self):
        cursor = _MockCursor(as_dict=True)
        cursor._rows = []
        conn = _MockConn()
        conn.cursor = MagicMock(return_value=cursor)
        db = make_connector()
        with patch.object(db, '_connect', return_value=conn):
            db.query("SELECT * FROM t WHERE cat=%s AND imp>=%s", ('facts', 7))
        cursor.execute.assert_called_once_with(
            "SELECT * FROM t WHERE cat=%s AND imp>=%s", ('facts', 7)
        )

    def test_query_returns_empty_on_all_retries_failing(self):
        db = make_connector()
        with patch.object(db, '_connect', side_effect=Exception("conn fail")):
            with patch('time.sleep'):  # don't actually sleep in tests
                result = db.query("SELECT 1")
        self.assertEqual(result, [])


# ── Tests: execute() ─────────────────────────────────────────────────────────

class TestExecute(unittest.TestCase):

    def _make_conn(self):
        cursor = _MockCursor()
        conn = _MockConn()
        conn.cursor = MagicMock(return_value=cursor)
        conn.commit = MagicMock()
        return conn, cursor

    def test_execute_returns_true_on_success(self):
        conn, _ = self._make_conn()
        db = make_connector()
        with patch.object(db, '_connect', return_value=conn):
            result = db.execute("INSERT INTO t VALUES (%s)", ('val',))
        self.assertTrue(result)

    def test_execute_commits(self):
        conn, _ = self._make_conn()
        db = make_connector()
        with patch.object(db, '_connect', return_value=conn):
            db.execute("DELETE FROM t WHERE id=%s", (1,))
        conn.commit.assert_called_once()

    def test_execute_returns_false_on_all_retries_failing(self):
        db = make_connector()
        with patch.object(db, '_connect', side_effect=Exception("db down")):
            with patch('time.sleep'):
                result = db.execute("INSERT INTO t VALUES (%s)", ('x',))
        self.assertFalse(result)

    def test_execute_retries_on_failure(self):
        """Verify retry count: should attempt MAX_RETRIES times."""
        db = make_connector()
        with patch.object(db, '_connect', side_effect=Exception("transient")) as mock_conn:
            with patch('time.sleep'):
                db.execute("INSERT INTO t VALUES (%s)", ('v',))
        self.assertEqual(mock_conn.call_count, SQLConnector.MAX_RETRIES)


# ── Tests: scalar() ──────────────────────────────────────────────────────────

class TestScalar(unittest.TestCase):

    def _make_conn(self, row):
        cursor = _MockCursor()
        cursor._scalar = row
        conn = _MockConn()
        conn.cursor = MagicMock(return_value=cursor)
        return conn

    def test_scalar_returns_first_value(self):
        conn = self._make_conn((42,))
        db = make_connector()
        with patch.object(db, '_connect', return_value=conn):
            result = db.scalar("SELECT COUNT(*) FROM t")
        self.assertEqual(result, 42)

    def test_scalar_returns_none_on_no_rows(self):
        conn = self._make_conn(None)
        db = make_connector()
        with patch.object(db, '_connect', return_value=conn):
            result = db.scalar("SELECT id FROM t WHERE 1=0")
        self.assertIsNone(result)

    def test_execute_scalar_alias(self):
        """execute_scalar() must delegate to scalar() — v1.x compat."""
        db = make_connector()
        with patch.object(db, 'scalar', return_value=7) as mock_scalar:
            result = db.execute_scalar("SELECT 7")
        mock_scalar.assert_called_once_with("SELECT 7", ())
        self.assertEqual(result, 7)


# ── Tests: ping() ────────────────────────────────────────────────────────────

class TestPing(unittest.TestCase):

    def test_ping_true_when_scalar_returns_1(self):
        db = make_connector()
        with patch.object(db, 'scalar', return_value=1):
            self.assertTrue(db.ping())

    def test_ping_false_when_scalar_returns_none(self):
        db = make_connector()
        with patch.object(db, 'scalar', return_value=None):
            self.assertFalse(db.ping())

    def test_ping_false_on_exception(self):
        db = make_connector()
        with patch.object(db, 'scalar', side_effect=Exception("boom")):
            self.assertFalse(db.ping())


# ── Tests: Parameterization guard ────────────────────────────────────────────

class TestParameterizationContract(unittest.TestCase):
    """
    Verify that the connector API always uses %s placeholders,
    never f-string interpolation. These are API contract tests.
    """

    def test_query_accepts_tuple_params(self):
        cursor = _MockCursor(as_dict=True)
        cursor._rows = [{'n': 5}]
        conn = _MockConn()
        conn.cursor = MagicMock(return_value=cursor)
        db = make_connector()
        with patch.object(db, '_connect', return_value=conn):
            rows = db.query("SELECT n FROM t WHERE cat=%s", ('facts',))
        cursor.execute.assert_called_with("SELECT n FROM t WHERE cat=%s", ('facts',))

    def test_execute_passes_params_to_cursor(self):
        cursor = _MockCursor()
        conn = _MockConn()
        conn.cursor = MagicMock(return_value=cursor)
        conn.commit = MagicMock()
        db = make_connector()
        with patch.object(db, '_connect', return_value=conn):
            db.execute(
                "INSERT INTO t (a, b) VALUES (%s, %s)",
                ('hello', 42)
            )
        cursor.execute.assert_called_with(
            "INSERT INTO t (a, b) VALUES (%s, %s)", ('hello', 42)
        )


if __name__ == '__main__':
    unittest.main()
