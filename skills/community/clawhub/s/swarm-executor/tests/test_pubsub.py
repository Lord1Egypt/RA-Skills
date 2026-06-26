"""
测试Pub/Sub协调器
"""
import pytest
import asyncio
from coordinator.pubsub import PubSubCoordinator, PubSubBackend, Message


class TestPubSubCoordinator:
    """PubSubCoordinator测试类"""
    
    @pytest.fixture
    def coordinator(self):
        """创建协调器实例"""
        return PubSubCoordinator(backend=PubSubBackend.MEMORY)
    
    @pytest.mark.asyncio
    async def test_publish_and_subscribe(self, coordinator):
        """测试发布和订阅"""
        messages_received = []
        
        def callback(message):
            messages_received.append(message)
        
        # 订阅频道
        coordinator.subscribe("test_channel", callback)
        
        # 发布消息
        test_data = {"task": "test_task", "priority": "high"}
        await coordinator.publish("test_channel", test_data)
        
        # 等待消息处理
        await asyncio.sleep(0.1)
        
        # 验证消息
        assert len(messages_received) == 1
        assert messages_received[0].channel == "test_channel"
        assert messages_received[0].data == test_data
    
    @pytest.mark.asyncio
    async def test_multiple_subscribers(self, coordinator):
        """测试多个订阅者"""
        subscriber1_messages = []
        subscriber2_messages = []
        
        def callback1(message):
            subscriber1_messages.append(message)
        
        def callback2(message):
            subscriber2_messages.append(message)
        
        # 两个订阅者订阅同一个频道
        coordinator.subscribe("multi_channel", callback1)
        coordinator.subscribe("multi_channel", callback2)
        
        # 发布消息
        test_data = {"task": "multi_task"}
        await coordinator.publish("multi_channel", test_data)
        
        # 等待消息处理
        await asyncio.sleep(0.1)
        
        # 验证两个订阅者都收到了消息
        assert len(subscriber1_messages) == 1
        assert len(subscriber2_messages) == 1
        assert subscriber1_messages[0].data == test_data
        assert subscriber2_messages[0].data == test_data
    
    @pytest.mark.asyncio
    async def test_unsubscribe(self, coordinator):
        """测试取消订阅"""
        messages_received = []
        
        def callback(message):
            messages_received.append(message)
        
        # 订阅
        coordinator.subscribe("unsub_channel", callback)
        
        # 发布第一条消息
        await coordinator.publish("unsub_channel", {"msg": "first"})
        await asyncio.sleep(0.1)
        assert len(messages_received) == 1
        
        # 取消订阅
        coordinator.unsubscribe("unsub_channel", callback)
        
        # 发布第二条消息
        await coordinator.publish("unsub_channel", {"msg": "second"})
        await asyncio.sleep(0.1)
        
        # 验证只收到第一条消息
        assert len(messages_received) == 1
        assert messages_received[0].data["msg"] == "first"
    
    @pytest.mark.asyncio
    async def test_get_subscriber_count(self, coordinator):
        """测试获取订阅者数量"""
        def callback1(message):
            pass
        
        def callback2(message):
            pass
        
        # 初始订阅者数量为0
        assert coordinator.get_subscriber_count("count_channel") == 0
        
        # 添加订阅者
        coordinator.subscribe("count_channel", callback1)
        assert coordinator.get_subscriber_count("count_channel") == 1
        
        # 添加第二个订阅者
        coordinator.subscribe("count_channel", callback2)
        assert coordinator.get_subscriber_count("count_channel") == 2
        
        # 移除一个订阅者
        coordinator.unsubscribe("count_channel", callback1)
        assert coordinator.get_subscriber_count("count_channel") == 1
    
    @pytest.mark.asyncio
    async def test_get_channels(self, coordinator):
        """测试获取频道列表"""
        def callback(message):
            pass
        
        # 初始为空
        assert coordinator.get_channels() == []
        
        # 添加频道
        coordinator.subscribe("channel1", callback)
        coordinator.subscribe("channel2", callback)
        
        channels = coordinator.get_channels()
        assert "channel1" in channels
        assert "channel2" in channels
        assert len(channels) == 2
    
    @pytest.mark.asyncio
    async def test_get_messages(self, coordinator):
        """测试获取消息历史"""
        # 发布几条消息
        messages = [
            {"id": 1, "content": "first"},
            {"id": 2, "content": "second"},
            {"id": 3, "content": "third"}
        ]
        
        for msg in messages:
            await coordinator.publish("history_channel", msg)
        
        # 获取消息历史
        history = await coordinator.get_messages("history_channel", limit=2)
        
        # 验证获取的消息
        assert len(history) == 2
        assert history[0].data["id"] == 2  # 最近的消息在前
        assert history[1].data["id"] == 3
    
    @pytest.mark.asyncio
    async def test_async_callback(self, coordinator):
        """测试异步回调函数"""
        async_messages_received = []
        
        async def async_callback(message):
            await asyncio.sleep(0.01)  # 模拟异步操作
            async_messages_received.append(message)
        
        # 订阅
        coordinator.subscribe("async_channel", async_callback)
        
        # 发布消息
        await coordinator.publish("async_channel", {"test": "async"})
        
        # 等待异步处理完成
        await asyncio.sleep(0.1)
        
        # 验证消息
        assert len(async_messages_received) == 1
        assert async_messages_received[0].data["test"] == "async"
    
    def test_duplicate_subscription(self, coordinator):
        """测试重复订阅"""
        call_count = 0
        
        def callback(message):
            nonlocal call_count
            call_count += 1
        
        # 第一次订阅
        assert coordinator.subscribe("dup_channel", callback) == True
        
        # 第二次订阅（应该失败）
        assert coordinator.subscribe("dup_channel", callback) == False
        
        # 发布消息
        asyncio.run(coordinator.publish("dup_channel", {"test": "dup"}))
        
        # 验证回调只被调用一次
        assert call_count == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])