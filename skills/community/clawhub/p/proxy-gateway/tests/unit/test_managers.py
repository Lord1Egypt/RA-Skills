"""
Unit tests for managers module
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch, AsyncMock
from app.managers.storage import MemoryStorage, RedisStorage, StorageBackend, create_storage_backend
from app.managers.testnet_payment import TestnetPaymentManager
from app.core.config import get_settings


class TestMemoryStorage:
    """Test memory storage backend"""
    
    @pytest.fixture
    def storage(self):
        return MemoryStorage()
    
    def test_get_set(self, storage):
        """Test basic get/set operations"""
        key = "test_key"
        
        # Initial should be None
        value = storage.get(key)
        assert value is None
        
        # Set value
        storage.set(key, {"data": "test"})
        value = storage.get(key)
        assert value == {"data": "test"}
    
    def test_exists(self, storage):
        """Test exists operation"""
        key = "test_exists_key"
        assert storage.exists(key) is False
        
        storage.set(key, "value")
        assert storage.exists(key) is True
    
    def test_delete(self, storage):
        """Test delete operation"""
        key = "test_delete_key"
        storage.set(key, "value")
        assert storage.exists(key) is True
        
        storage.delete(key)
        assert storage.exists(key) is False
    
    def test_hget_hset(self, storage):
        """Test hash operations"""
        key = "test_hash"
        field = "field1"
        
        # Initial should be None
        value = storage.hget(key, field)
        assert value is None
        
        # Set field
        storage.hset(key, field, "value1")
        value = storage.hget(key, field)
        assert value == "value1"
    
    def test_hgetall(self, storage):
        """Test hgetall operation"""
        key = "test_hash_all"
        storage.hset(key, "field1", "value1")
        storage.hset(key, "field2", "value2")
        
        all_fields = storage.hgetall(key)
        assert all_fields == {"field1": "value1", "field2": "value2"}
    
    def test_setnx_new_key(self, storage):
        """Test setnx on new key"""
        key = "test_setnx"
        result = storage.setnx(key, "value")
        assert result is True
        assert storage.get(key) == "value"
    
    def test_setnx_existing_key(self, storage):
        """Test setnx on existing key"""
        key = "test_setnx_existing"
        storage.set(key, "original")
        
        result = storage.setnx(key, "new_value")
        assert result is False
        assert storage.get(key) == "original"
    
    def test_setnx_with_expire(self, storage):
        """Test setnx with expiration"""
        import time
        key = "test_setnx_expire"
        
        result = storage.setnx(key, "value", expire=1)
        assert result is True
        
        # Should exist immediately
        assert storage.exists(key) is True
        
        # Wait for expiration
        time.sleep(1.1)
        assert storage.exists(key) is False
    
    def test_multiple_users_isolation(self, storage):
        """Test data isolation between users"""
        user1_key = "user:001:balance"
        user2_key = "user:002:balance"
        
        storage.hset(user1_key, "available", 100.0)
        storage.hset(user2_key, "available", 200.0)
        
        assert storage.hget(user1_key, "available") == 100.0
        assert storage.hget(user2_key, "available") == 200.0


class TestTestnetPaymentManager:
    """Test testnet payment manager"""
    
    def test_get_deposit_address(self):
        """Test getting deposit address"""
        manager = TestnetPaymentManager()
        address_info = manager.get_deposit_address("test_user")
        
        assert "address" in address_info
        assert "network" in address_info
        assert "token" in address_info
        assert "auto_confirm" in address_info
    
    def test_get_balance_new_user(self):
        """Test getting balance for new user"""
        manager = TestnetPaymentManager()
        balance = manager.get_balance("new_user_test")
        assert balance == Decimal("0")
    
    @pytest.mark.asyncio
    async def test_reset_and_get_balance(self):
        """Test reset balance and get balance"""
        manager = TestnetPaymentManager()
        user_id = "test_balance_user"
        
        # Reset balance
        result = manager.reset_test_balance(user_id, Decimal("100"))
        assert "100" in result
        
        # Check balance
        balance = manager.get_balance(user_id)
        assert balance == Decimal("100")
    
    @pytest.mark.asyncio
    async def test_deduct_balance_success(self):
        """Test successful balance deduction"""
        manager = TestnetPaymentManager()
        user_id = "test_deduct_user"
        
        # Set initial balance
        manager.reset_test_balance(user_id, Decimal("10"))
        
        # Deduct
        success, message, remaining = await manager.deduct(user_id)
        assert success is True
        assert remaining == Decimal("9.999")
    
    @pytest.mark.asyncio
    async def test_deduct_balance_insufficient(self):
        """Test deduct with insufficient balance"""
        manager = TestnetPaymentManager()
        user_id = "test_insufficient_user"
        
        # Set low balance
        manager.reset_test_balance(user_id, Decimal("0.0005"))
        
        # Try to deduct
        success, message, remaining = await manager.deduct(user_id)
        assert success is False
        assert "Insufficient" in message
    
    @pytest.mark.asyncio
    async def test_charge_for_request(self):
        """Test charge for request wrapper"""
        manager = TestnetPaymentManager()
        user_id = "test_charge_user"
        
        # Set balance
        manager.reset_test_balance(user_id, Decimal("10"))
        
        # Charge
        result = await manager.charge_for_request(user_id)
        assert "success" in result
        assert "can_proceed" in result
        assert result["can_proceed"] is True
    
    def test_calculate_cost(self):
        """Test cost calculation"""
        manager = TestnetPaymentManager()
        
        cost = manager._calculate_cost(1)
        assert cost == Decimal("0.001")
        
        cost = manager._calculate_cost(10)
        assert cost == Decimal("0.01")
    
    def test_transaction_history(self):
        """Test transaction history"""
        manager = TestnetPaymentManager()
        user_id = "test_tx_history_user"
        
        # Initially empty
        history = manager.get_transaction_history(user_id)
        assert history == []


class TestCreateStorageBackend:
    """Test storage backend factory"""
    
    def test_returns_memory_storage_when_redis_unavailable(self):
        """Test fallback to memory when Redis fails"""
        storage = create_storage_backend()
        assert isinstance(storage, MemoryStorage)


class TestStorageBackendAbstract:
    """Test storage backend abstract class"""
    
    def test_cannot_instantiate_abstract(self):
        """Test that StorageBackend cannot be instantiated directly"""
        with pytest.raises(TypeError):
            StorageBackend()
