"""Test script for Samantha's emotional analysis"""
from emotional_intelligence import EmotionalIntelligence

ei = EmotionalIntelligence()

# Test messages
test_messages = [
    '今天心情很好，阳光特别温暖',
    '工作压力好大，感觉快要崩溃了',
    '我有点害怕明天的演讲',
    '其实我一直觉得自己不够好'
]

print("=" * 50)
print("Samantha 情绪分析测试")
print("=" * 50)

for msg in test_messages:
    result = ei.analyze(msg)
    print(f"\n消息: {msg}")
    print(f"主要情绪: {result['primary_emotion']}")
    print(f"检测到的情绪: {result['detected_emotions']}")
    print(f"强度: {result['intensity']:.1f}")
    print(f"是否脆弱: {result['is_vulnerable']}")
    print(f"需要支持: {result['needs_support']}")
    print("-" * 50)
