#!/usr/bin/env python3
"""
Samantha AI伴侣基础使用示例
"""

import asyncio
from src.core.engine import SamanthaEngine
from src.emotion.analyzer import EmotionAnalyzer
from src.mbti.analyzer import MBTIAnalyzer
from src.voice.tts import TTSService

class SamanthaDemo:
    """Samantha演示类"""
    
    def __init__(self):
        """初始化Samantha引擎"""
        print("初始化Samantha AI伴侣...")
        
        # 初始化各模块
        self.engine = SamanthaEngine()
        self.emotion_analyzer = EmotionAnalyzer()
        self.mbti_analyzer = MBTIAnalyzer()
        self.tts_service = TTSService()
        
        print("Samantha初始化完成！")
        print("=" * 50)
    
    async def chat_demo(self):
        """聊天演示"""
        print("🎤 聊天演示开始")
        print("输入 '退出' 结束对话")
        print("-" * 30)
        
        while True:
            # 获取用户输入
            user_input = input("你: ").strip()
            
            if user_input.lower() in ['退出', 'exit', 'quit']:
                print("Samantha: 再见！期待下次聊天～")
                break
            
            # 分析用户情感
            emotion = self.emotion_analyzer.analyze(user_input)
            print(f"[情感分析] {emotion}")
            
            # 分析MBTI倾向
            mbti_profile = self.mbti_analyzer.analyze(user_input)
            print(f"[MBTI分析] {mbti_profile}")
            
            # 生成响应
            response = await self.engine.generate_response(
                user_input=user_input,
                emotion_state=emotion,
                mbti_profile=mbti_profile
            )
            
            # 显示响应
            print(f"Samantha: {response}")
            
            # 语音输出（可选）
            use_voice = input("是否语音朗读？(y/n): ").strip().lower()
            if use_voice == 'y':
                await self.tts_service.speak(response)
            
            print("-" * 30)
    
    async def mbti_demo(self):
        """MBTI人格分析演示"""
        print("🧠 MBTI人格分析演示")
        print("请描述一下你的性格特点或回答几个问题：")
        
        questions = [
            "你更喜欢独处还是社交？",
            "做决定时更依赖逻辑还是情感？",
            "你是一个计划性强的人吗？",
            "你如何看待规则和传统？"
        ]
        
        answers = []
        for i, question in enumerate(questions, 1):
            answer = input(f"Q{i}: {question}\n你的回答: ").strip()
            answers.append(answer)
        
        # 分析MBTI类型
        mbti_type = self.mbti_analyzer.determine_type(answers)
        description = self.mbti_analyzer.get_type_description(mbti_type)
        
        print(f"\n🎯 你的MBTI类型可能是: {mbti_type}")
        print(f"📖 类型描述: {description}")
        
        # 根据MBTI类型调整沟通方式
        communication_style = self.mbti_analyzer.get_communication_style(mbti_type)
        print(f"💬 推荐沟通方式: {communication_style}")
    
    async def emotion_tracking_demo(self):
        """情感追踪演示"""
        print("📊 情感追踪演示")
        print("请分享你今天的心情或经历：")
        
        mood_entries = []
        for i in range(3):
            entry = input(f"心情记录{i+1}: ").strip()
            mood_entries.append(entry)
        
        # 分析情感趋势
        emotion_trend = self.emotion_analyzer.track_trend(mood_entries)
        print(f"\n📈 情感趋势分析: {emotion_trend}")
        
        # 生成情感报告
        report = self.emotion_analyzer.generate_report(mood_entries)
        print(f"📋 情感报告:\n{report}")
    
    async def space_awareness_demo(self):
        """空间感知演示"""
        print("📍 空间感知演示")
        
        locations = ["家", "公司", "健身房", "咖啡馆"]
        print("可用位置:", ", ".join(locations))
        
        location = input("请输入你的当前位置: ").strip()
        
        if location in locations:
            # 根据位置生成问候
            greeting = self.engine.generate_location_greeting(location)
            print(f"\n{Samantha}: {greeting}")
            
            # 根据位置提供建议
            suggestion = self.engine.get_location_suggestion(location)
            print(f"💡 位置建议: {suggestion}")
        else:
            print("未知位置，使用默认问候")
            print(f"Samantha: 你好！无论你在哪里，我都在这里陪伴你。")

async def main():
    """主函数"""
    demo = SamanthaDemo()
    
    print("请选择演示模式:")
    print("1. 聊天演示")
    print("2. MBTI分析演示")
    print("3. 情感追踪演示")
    print("4. 空间感知演示")
    print("5. 全部演示")
    
    choice = input("请输入选择 (1-5): ").strip()
    
    if choice == '1':
        await demo.chat_demo()
    elif choice == '2':
        await demo.mbti_demo()
    elif choice == '3':
        await demo.emotion_tracking_demo()
    elif choice == '4':
        await demo.space_awareness_demo()
    elif choice == '5':
        print("开始完整演示...")
        await demo.mbti_demo()
        print("\n" + "="*50 + "\n")
        await demo.emotion_tracking_demo()
        print("\n" + "="*50 + "\n")
        await demo.space_awareness_demo()
        print("\n" + "="*50 + "\n")
        await demo.chat_demo()
    else:
        print("无效选择，退出程序")

if __name__ == "__main__":
    asyncio.run(main())