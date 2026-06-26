"""
Proxy Gateway Test Configuration
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings, Settings


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def test_settings():
    """Test settings with memory storage"""
    return Settings(
        network="testnet",
        hosted_wallet=None,
        admin_token="test_admin_token_12345",
        use_redis=False,
        test_balance=100.0,
        free_trial_limit=10
    )


@pytest.fixture
def mock_user_id():
    """Mock user ID for testing"""
    return "test_user_001"


@pytest.fixture
def sample_url():
    """Sample URL for fetch testing"""
    return "https://httpbin.org/get"
