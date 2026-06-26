"""
Unit tests for core module
"""
import pytest
from app.core.config import Settings, get_settings
from app.core.security import validate_user_id, validate_api_key, validate_tx_hash
from app.core.exceptions import ValidationError


class TestConfig:
    """Test configuration management"""
    
    def test_default_settings(self, monkeypatch):
        """Test default settings creation"""
        monkeypatch.setenv("NETWORK", "testnet")
        monkeypatch.setenv("ADMIN_TOKEN", "test_token")
        
        # Clear cache to get fresh settings
        from app.core.config import get_settings
        get_settings.cache_clear()
        
        settings = get_settings()
        assert settings.NETWORK == "testnet"
        assert settings.is_testnet is True
        assert settings.is_mainnet is False
    
    def test_mainnet_settings(self, monkeypatch):
        """Test mainnet settings"""
        monkeypatch.setenv("NETWORK", "mainnet")
        monkeypatch.setenv("ADMIN_TOKEN", "test_token")
        monkeypatch.setenv("HOSTED_WALLET", "0x1234567890123456789012345678901234567890")
        
        # Clear cache to get fresh settings
        from app.core.config import get_settings
        get_settings.cache_clear()
        
        settings = get_settings()
        assert settings.NETWORK == "mainnet"
        assert settings.is_mainnet is True
        assert settings.is_testnet is False
    
    def test_cors_origins_list(self, monkeypatch):
        """Test CORS origins parsing"""
        monkeypatch.setenv("NETWORK", "testnet")
        monkeypatch.setenv("ADMIN_TOKEN", "test_token")
        monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000,https://example.com")
        
        # Clear cache to get fresh settings
        from app.core.config import get_settings
        get_settings.cache_clear()
        
        settings = get_settings()
        origins = settings.cors_origins_list
        assert "http://localhost:3000" in origins
        assert "https://example.com" in origins


class TestSecurity:
    """Test security utility functions"""
    
    def test_validate_user_id_valid(self):
        """Test valid user ID validation"""
        valid_ids = [
            "user123",
            "my_agent_001",
            "test-user",
            "user_123_test"
        ]
        for uid in valid_ids:
            assert validate_user_id(uid) is True
    
    def test_validate_user_id_invalid(self):
        """Test invalid user ID validation"""
        invalid_ids = [
            "",  # empty
            "ab",  # too short
            "a" * 65,  # too long
            "user@123",  # special char
            "user 123",  # space
        ]
        for uid in invalid_ids:
            assert validate_user_id(uid) is False
    
    def test_validate_api_key_valid(self):
        """Test valid API key validation"""
        valid_keys = [
            "api_key_12345",
            "my-api-key",
            "test_key_001"
        ]
        for key in valid_keys:
            assert validate_api_key(key) is True
    
    def test_validate_api_key_invalid(self):
        """Test invalid API key validation"""
        invalid_keys = [
            "",  # empty
            "key",  # too short
            "key@123",  # special char
        ]
        for key in invalid_keys:
            assert validate_api_key(key) is False
    
    def test_validate_tx_hash_valid(self):
        """Test valid transaction hash validation"""
        valid_hashes = [
            "0x" + "a" * 64,
            "0x" + "1" * 64,
        ]
        for tx_hash in valid_hashes:
            assert validate_tx_hash(tx_hash) is True
    
    def test_validate_tx_hash_invalid(self):
        """Test invalid transaction hash validation"""
        invalid_hashes = [
            "",  # empty
            "0x123",  # too short
            "0x" + "g" * 64,  # invalid hex
            "0x" + "a" * 63,  # odd length
        ]
        for tx_hash in invalid_hashes:
            assert validate_tx_hash(tx_hash) is False
