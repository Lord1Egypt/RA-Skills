"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestSystemEndpoints:
    """Test system endpoints"""
    
    def test_root(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["name"] == "Proxy Gateway"
    
    def test_health(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        # May be 200 or 503 depending on Clash availability
        assert response.status_code in [200, 503]
    
    def test_network_info(self, client):
        """Test network info endpoint"""
        response = client.get("/network-info")
        assert response.status_code == 200
        data = response.json()
        assert "network" in data
        assert "is_testnet" in data
        assert "chain_id" in data


class TestPaymentEndpoints:
    """Test payment endpoints"""
    
    def test_deposit_info_without_user_id(self, client):
        """Test deposit info endpoint without user_id returns HTML"""
        response = client.get("/deposit-info")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_deposit_info_with_user_id(self, client):
        """Test deposit info endpoint with user_id returns JSON"""
        response = client.get("/deposit-info?user_id=test_user_123")
        assert response.status_code == 200
        data = response.json()
        assert "address" in data
        assert "network" in data
    
    def test_deposit_info_invalid_user_id(self, client):
        """Test deposit info with invalid user_id"""
        response = client.get("/deposit-info?user_id=ab")  # too short
        assert response.status_code == 400
    
    def test_get_balance_no_user_id(self, client):
        """Test getting balance without user_id"""
        response = client.get("/balance")
        assert response.status_code == 422  # Missing required query param
    
    def test_get_balance_invalid_user_id(self, client):
        """Test getting balance with invalid user_id"""
        response = client.get("/balance?user_id=ab")  # too short
        assert response.status_code == 400
    
    def test_get_balance_valid_user_id(self, client):
        """Test getting balance with valid user_id"""
        response = client.get("/balance?user_id=test_user_123")
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "balance" in data
        assert data["currency"] == "USDC"


class TestProxyEndpoints:
    """Test proxy endpoints"""
    
    def test_regions(self, client):
        """Test regions endpoint"""
        response = client.get("/api/v1/regions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Check region structure
        region = data[0]
        assert "region" in region
        assert "name" in region
    
    def test_fetch_no_auth(self, client):
        """Test fetch without authentication"""
        response = client.post(
            "/api/v1/fetch",
            json={"url": "https://example.com"}
        )
        assert response.status_code == 401
    
    def test_fetch_invalid_client_id(self, client):
        """Test fetch with invalid client_id"""
        response = client.post(
            "/api/v1/fetch",
            headers={"X-Client-ID": "ab"},  # too short
            json={"url": "https://example.com"}
        )
        assert response.status_code == 400
    
    def test_fetch_missing_url(self, client):
        """Test fetch without URL"""
        response = client.post(
            "/api/v1/fetch",
            headers={"X-Client-ID": "test_user"},
            json={}
        )
        assert response.status_code == 422  # Validation error
    
    def test_fetch_invalid_url(self, client):
        """Test fetch with invalid URL"""
        response = client.post(
            "/api/v1/fetch",
            headers={"X-Client-ID": "test_user"},
            json={"url": "not_a_valid_url"}
        )
        assert response.status_code == 400


class TestAdminEndpoints:
    """Test admin endpoints"""
    
    def test_reset_test_balance_no_auth(self, client):
        """Test reset balance without admin token"""
        response = client.post(
            "/reset-test-balance?user_id=test_user"
        )
        assert response.status_code == 403
    
    def test_reset_test_balance_invalid_token(self, client):
        """Test reset balance with invalid admin token"""
        response = client.post(
            "/reset-test-balance?user_id=test_user",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 403


class TestErrorHandling:
    """Test error handling"""
    
    def test_not_found(self, client):
        """Test 404 handling"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Test 405 handling"""
        response = client.post("/health")  # Health is GET only
        assert response.status_code == 405
