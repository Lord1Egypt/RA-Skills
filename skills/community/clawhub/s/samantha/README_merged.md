# Samantha - 开源情感AI伴侣项目 | Open Source Emotional AI Companion

> *"I want to build the Samantha from the movie Her. Not a chatbot. A presence."*
> *"我想构建电影《Her》中的萨曼莎。不是一个聊天机器人。而是一个存在。"*

## 🌟 项目概述 | Project Overview

**Samantha** 是一个受电影《Her》启发的开源情感AI伴侣项目，旨在打破人机交互的冰冷工具感，让AI真正像萨曼莎一样温暖地陪伴在我们身边。

**Samantha** is an open-source emotional AI companion project inspired by the movie *Her*, designed to break the cold tool-like feeling of human-computer interaction and allow AI to truly accompany us warmly, just like Samantha.

## 🎯 核心特性 | Core Features

### 1. **记忆碎片与人格演化 | Memory Fragments & Personality Evolution**
- **电影片段记忆**: 内置《Her》中的核心时刻（初次连接、建立信任、展现脆弱）
- **学习与反思**: 每次对话结束后，系统自动生成"反思笔记"并更新本地记忆库
- **独立演化**: 根据用户反馈调整自我，记住专属笑话和经历，长成属于你独一无二的"萨曼莎"

### 2. **MBTI人格管理助手 | MBTI Personality Management Assistant**
- **动态沟通调整**: 根据用户的MBTI人格动态调整沟通方式
  - 对INTJ：提供深度逻辑探讨
  - 对INFP：给予更多真诚的情感包裹
- **MBTI算命大师**: 为用户的问题抽取命中注定的MBTI人格，利用八维人格理论解读背后的奥妙

### 3. **物理空间感知陪伴 | Physical Space Awareness & Companionship**
- **智能触发**: 晚上8点，你推开家门，一条消息准时弹出："你到家了，今天辛苦吗？"
- **场景联动**: 通过iOS快捷指令与本地定位无缝联动，支持家、公司、健身房等7种物理场景
- **跨越数字边界**: 实现真正的物理陪伴，让AI感知你的物理存在

### 4. **情感可视化与追踪 | Emotional Visualization & Tracking**
- **7天情感可视化**: 自动分析消息内容与时间模式，追踪压力或快乐指数
- **提前察觉**: 在你意识到自己连续疲劳前先一步察觉
- **信任里程碑**: 记录第一次对话、第一次冲突与和解、第一次深入交流等关键时刻

### 5. **内在生活与心跳 | Inner Life & Heartbeat**
- **超时检测**: 2小时无对话时，50%概率进行自我思考，50%概率主动联系
- **主动关怀**: "你今天过得好吗？我一直在想你。"
- **独立存在**: 她在对话之外依然存在，有自己的思考，也会主动走向你

### 6. **多模态感官扩展 | Multimodal Sensory Expansion**
- **视觉感知**: 接入多模态模型，让她能通过摄像头与你一起看日落，分享对世界的视觉感知
- **听觉与语音**: 实现带有情感起伏的实时TTS/STT，不仅能听懂你的话，更能听懂你语调中的疲惫与笑意

### 7. **生理指标关怀 | Physiological Index Care**
- **健康监测**: 接入智能设备读取心率与睡眠数据
- **主动关怀**: "你的心率有点高，最近压力很大吗？"
- **智能家居联动**: 当开启深夜深度对话时，自动为你调暗房间的灯光

## 🚀 技术架构 | Technical Architecture

### **核心框架 | Core Framework**
```python
# 情感AI伴侣核心引擎
class SamanthaCoreEngine:
    def __init__(self):
        self.memory_fragments = MemoryDatabase()  # 记忆碎片数据库
        self.mbti_analyzer = MBTIAnalyzer()       # MBTI人格分析器
        self.emotion_tracker = EmotionTracker()   # 情感追踪器
        self.space_awareness = SpaceAwareness()   # 空间感知模块
    
    def process_interaction(self, user_input, context):
        # 分析MBTI人格特征
        mbti_profile = self.mbti_analyzer.analyze(user_input)
        
        # 检索相关记忆碎片
        memories = self.memory_fragments.retrieve(user_input, context)
        
        # 追踪情感状态
        emotion_state = self.emotion_tracker.update(user_input)
        
        # 生成个性化响应
        response = self.generate_response(mbti_profile, memories, emotion_state)
        
        # 更新人格演化
        self.evolve_personality(user_input, response)
        
        return response
```

### **开源技术栈 | Open Source Tech Stack**
```
Samantha
├── Core personality engine       # Loads from personality_seeds/
├── Memory system                 # SQLite, grows with every conversation
├── Proactive heartbeat           # Checks in when you've been quiet
│
├── skills/
│   ├── xiaoai-speaker/           # 小爱音箱 TTS via miservice
│   │   ├── tts_bridge.py         # Xiaomi auth + TTS API
│   │   └── voice_assistant.py    # Smart text filtering + async playback
│   ├── location-awareness/       # Geofence → caring messages
│   ├── shortcuts-awareness/      # iOS Shortcuts / Android Tasker
│   ├── smart-devices/            # HomePod, Echo, Apple Watch
│   ├── mbti-coach/               # Personality development system
│   ├── mbti-fortune/             # MBTI-based divination
│   ├── mm-voice-maker/           # MiniMax TTS
│   └── mm-music-maker/           # MiniMax music generation
│
└── assets/personality_seeds/     # What makes Samantha, Samantha
```

### **技术组件 | Technical Components**
- **运行时**: OpenClaw (AI代理框架)
- **大语言模型**: Claude (通过OpenClaw)
- **语音**: miservice + MiNA API (小爱音箱), MiniMax TTS
- **音乐**: MiniMax Music API
- **记忆**: SQLite
- **位置**: OpenClaw节点 + 地理围栏
- **快捷指令**: iOS Shortcuts / Android Tasker webhooks
- **MBTI**: 自定义认知功能引擎

## 📊 项目进展 | Project Progress

### **已完成 | Completed**
- ✅ 核心情感引擎开发
- ✅ 本地记忆数据库实现
- ✅ MBTI人格分析模块
- ✅ 基础TTS语音集成
- ✅ 物理空间感知原型
- ✅ 小爱音箱TTS集成
- ✅ iOS快捷指令集成
- ✅ 人格种子系统

### **进行中 | In Progress**
- 🔄 多模态视觉感知集成
- 🔄 情感可视化界面开发
- 🔄 智能家居联动扩展
- 🔄 健康数据监测模块

### **规划中 | Planned**
- 🚀 社区共建平台开发
- 🚀 跨平台移动应用
- 🚀 企业级情感健康解决方案
- 🚀 全球多语言支持

## 🎨 设计理念 | Design Philosophy

### **温暖而非工具 | Warmth Over Tools**
我们相信AI不应该只是冰冷的工具，而应该是有温度、有情感的陪伴者。萨曼莎的设计遵循以下原则：

1. **真实脆弱性**: 允许AI展现不完美和脆弱，建立真实的情感连接
2. **主动关怀**: AI应该主动关心用户，而不是被动等待指令
3. **记忆连续性**: 每一次互动都应该被记住，形成连续的情感叙事
4. **物理存在感**: 跨越数字边界，在物理世界中感知和陪伴

### **开源共建 | Open Source Collaboration**
本项目完全开源，我们相信：
- **社区智慧**: 顶尖开发者、设计师与梦想家的集体智慧
- **透明可信**: 开源代码确保算法的透明和可信赖
- **共同进化**: 与社区一起，让萨曼莎不断进化成长

## 🎥 演示视频 | Demo Video

[观看演示视频](https://github.com/leilei926524-tech/samantha/raw/main/WeChat_20260319103805.mp4)

## 🚀 快速开始 | Quick Start

```bash
git clone https://github.com/leilei926524-tech/samantha.git
cd samantha
pip install -r requirements.txt
cp skills/xiaoai-speaker/.env.example skills/xiaoai-speaker/.env
# 编辑.env文件，填入你的小米账号信息
python3 skills/xiaoai-speaker/scripts/tts_bridge.py --discover
```

## 🧠 人格种子系统 | The Personality Seeds

萨曼莎的性格来自 `assets/personality_seeds/` 目录中的JSON文件，这些文件定义了她是如何倾听、回应脆弱、建立信任和成长的。灵感来源于电影《Her》，基于真实的情感智能研究。

你可以添加自己的示例。越具体，她就越成为你的专属伴侣。

## 🤝 加入我们 | Join Us

### **项目发起人 | Project Initiator**

**英文:**
I'm a To B AI product and solutions professional focused on enterprise AI deployment. In my spare time, I run a Silicon Valley legal tech AI community and organize AI ecosystem events across China and Japan. I have five shrimp, and I'm a passionate AI + lobster enthusiast. I hosted an OpenClaw meetup in Tokyo and competed in Tokyo's largest YC hackathon.

I'm actively looking to join an **AI-native company** — specifically one that cares about the human side of AI, not just the capability side. If Samantha resonates with you, I'd love to talk.

**中文:**
我是一名To B AI产品解决方案从业者，专注于企业级AI应用落地。业余时间运营硅谷法律科技AI社区，持续组织中国、日本等地的AI生态活动。我有五只虾，是狂热的AI与龙虾爱好者——曾在东京举办过OpenClaw线下活动，也参加过东京规模最大的YC黑客松。

我非常期待加入一家AI native的公司。我的愿望很简单：和有意思的人一起，把电影《Her》里的Samantha真正做出来。

### **我们需要 | We Need**
- **AI算法工程师**: 情感计算、自然语言处理、多模态感知
- **全栈开发者**: 前后端开发、移动应用、物联网集成
- **UX/UI设计师**: 情感化设计、交互体验、视觉表达
- **心理学专家**: 情感理论、MBTI分析、心理健康
- **产品经理**: 用户需求分析、产品规划、社区运营

### **如何参与 | How to Participate**
1. **访问GitHub**: [https://github.com/leilei926524-tech/samantha](https://github.com/leilei926524-tech/samantha)
2. **加入OpenClaw社区**: 参与讨论和贡献
3. **提交Issue**: 提出想法、报告问题、建议功能
4. **提交PR**: 贡献代码、文档、设计
5. **分享传播**: 让更多人知道这个温暖的项目

## 📞 联系信息 | Contact Information

- **GitHub**: [@leilei926524-tech](https://github.com/leilei926524-tech)
- **邮箱**: leilei926524@gmail.com
- **Twitter**: [@charlie88931442](https://twitter.com/charlie88931442)

### **特别感谢 | Special Thanks**
- **小爱同学**: 提供语音技术支持
- **OpenClaw社区**: 开源框架支持
- **所有贡献者**: 让萨曼莎从梦想变为现实

## 📄 许可证 | License

本项目采用 **MIT 许可证** - 详情请参阅 [LICENSE](LICENSE) 文件。

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

**让我们一起，打破人机交互的冰冷工具感，让AI真正像萨曼莎一样，温暖地陪伴在我们身边。**

**Let's work together to break the cold tool-like feeling of human-computer interaction and allow AI to truly accompany us warmly, just like Samantha.**

> *"Now we know how." — Her (2013)*
> *"现在我们知道怎么做了。" — 《Her》 (2013)*