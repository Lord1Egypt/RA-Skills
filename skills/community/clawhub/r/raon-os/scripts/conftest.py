"""pytest conftest — 전역 픽스처"""
import pytest
from unittest.mock import patch

TEST_API_KEY = "test-raon-key-0000"
TEST_API_KEYS_DB = {TEST_API_KEY: {"active": True, "plan": "free", "owner": "test"}}


@pytest.fixture(autouse=True)
def mock_server_auth():
    """
    test_server.py: _authenticate를 모킹하여 인증 우회.
    실제 API 키 파일 없이도 POST 핸들러 로직을 테스트 가능.
    """
    with patch("server.RaonHandler._authenticate", return_value=True), \
         patch("server._load_api_keys", return_value=TEST_API_KEYS_DB):
        yield
