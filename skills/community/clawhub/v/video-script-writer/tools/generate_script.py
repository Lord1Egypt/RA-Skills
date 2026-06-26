#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频脚本生成工具
支持抖音、B 站、小红书等平台的视频脚本创作
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any

# 平台风格配置
PLATFORM_STYLES = {
    'douyin': {
        'name': '抖音',
        'duration': '15-60 秒',
        'structure': ['黄金 3 秒', '内容主体', '互动引导'],
        'features': ['节奏快', '前 3 秒抓人', 'BGM 重要', '字幕关键'],
    },
    'xiaohongshu': {
        'name': '小红书',
        'duration': '30-90 秒',
        'structure': ['封面标题', '痛点引入', '干货分享', '总结互动'],
        'features': ['种草风', '真实分享', 'emoji 丰富', '封面精美'],
    },
    'bilibili': {
        'name': 'B 站',
        'duration': '3-10 分钟',
        'structure': ['片头', '引入', '主体内容', '总结', '片尾'],
        'features': ['深度内容', '弹幕互动', 'UP 主风格', '梗文化'],
    },
    'youtube': {
        'name': 'YouTube',
        'duration': '5-15 分钟',
        'structure': ['Hook', 'Intro', 'Content', 'CTA', 'Outro'],
        'features': ['SEO 优化', '缩略图', '章节', '订阅引导'],
    },
}

# 开场 Hook 模板
HOOK_TEMPLATES = [
    "你有没有想过，{痛点}其实可以{解决方案}？",
    "今天我要分享一个{效果}的方法，{时间}就能见效！",
    "90% 的人都做错了！{主题}的正确打开方式是...",
    "花{金额}买的教训，今天免费告诉你！",
    "如果早点知道这个，我就能{避免的损失}了！",
    "这个{产品/方法}，让我{惊人效果}！",
    "别再{错误做法}了！试试这个{正确做法}！",
    "我试了{数量}个{产品}，只有这个值得推荐！",
]

# 转场话术
TRANSITION_TEMPLATES = [
    "接下来，我们来看看...",
    "重点来了，注意听...",
    "你可能会问...",
    "别急，还有更厉害的...",
    "看到这里，你可能已经...",
    "接下来这个才是关键...",
]

# CTA 模板
CTA_TEMPLATES = [
    "觉得有用记得点赞收藏，不然划走就找不到了！",
    "关注我，每天分享{领域}干货！",
    "评论区告诉我你的想法～",
    "有什么想看的，留言告诉我！",
    "转发给需要的朋友吧！",
    "点击主页，查看更多{领域}内容！",
]

def generate_hook(topic: str, style: str = 'douyin') -> str:
    """生成开场 Hook"""
    template = HOOK_TEMPLATES[hash(topic) % len(HOOK_TEMPLATES)]
    
    hooks = {
        '痛点': f'在{topic}上浪费时间',
        '解决方案': '轻松搞定',
        '效果': '让你惊艳',
        '时间': '3 天',
        '主题': topic,
        '金额': '几千块',
        '避免的损失': '少走很多弯路',
        '产品/方法': topic,
        '惊人效果': '彻底改变了',
        '错误做法': '盲目尝试',
        '正确做法': '高效方法',
        '数量': '10+',
    }
    
    for k, v in hooks.items():
        template = template.replace('{' + k + '}', v)
    
    return template

def generate_structure(topic: str, style: str = 'douyin', duration: str = '60 秒') -> List[Dict[str, str]]:
    """生成视频结构"""
    platform = PLATFORM_STYLES.get(style, PLATFORM_STYLES['douyin'])
    
    structure = []
    
    # 根据平台生成不同结构
    if style == 'douyin':
        structure = [
            {
                'section': '黄金 3 秒',
                'time': '0-3 秒',
                'content': generate_hook(topic, style),
                'visual': '特写镜头 + 大字标题',
                'audio': '热门 BGM 前奏',
            },
            {
                'section': '痛点引入',
                'time': '3-10 秒',
                'content': f'你是不是也经常{get_pain_point(topic)}？',
                'visual': '情景再现/对比画面',
                'audio': 'BGM 继续',
            },
            {
                'section': '解决方案',
                'time': '10-45 秒',
                'content': get_solution_points(topic, 3),
                'visual': '步骤演示/产品展示',
                'audio': 'BGM 高潮',
            },
            {
                'section': '效果展示',
                'time': '45-55 秒',
                'content': '看，这就是效果！',
                'visual': '前后对比',
                'audio': '音效强调',
            },
            {
                'section': '互动引导',
                'time': '55-60 秒',
                'content': CTA_TEMPLATES[hash(topic) % len(CTA_TEMPLATES)],
                'visual': '主播正面 + 关注按钮',
                'audio': 'BGM 收尾',
            },
        ]
    elif style == 'xiaohongshu':
        structure = [
            {
                'section': '封面标题',
                'time': '0-2 秒',
                'content': f'{topic}｜亲测有效',
                'visual': '精美封面 + 标题',
                'audio': '轻快 BGM',
            },
            {
                'section': '痛点引入',
                'time': '2-15 秒',
                'content': f'姐妹们，今天来聊聊{topic}这件事...',
                'visual': '主播出镜',
                'audio': 'BGM 继续',
            },
            {
                'section': '干货分享',
                'time': '15-70 秒',
                'content': get_solution_points(topic, 4),
                'visual': '产品展示 + 文字说明',
                'audio': 'BGM 继续',
            },
            {
                'section': '总结互动',
                'time': '70-90 秒',
                'content': '以上就是今天的分享啦，有问题评论区见～',
                'visual': '总结画面',
                'audio': 'BGM 收尾',
            },
        ]
    else:
        # 通用结构
        structure = [
            {
                'section': '开场',
                'time': '0-10 秒',
                'content': generate_hook(topic, style),
                'visual': '吸引注意力的画面',
                'audio': '开场 BGM',
            },
            {
                'section': '主体内容',
                'time': '10-80% 时长',
                'content': get_solution_points(topic, 5),
                'visual': '内容演示',
                'audio': '主体 BGM',
            },
            {
                'section': '总结',
                'time': '最后 10%',
                'content': '总结一下今天的要点...',
                'visual': '要点罗列',
                'audio': '收尾 BGM',
            },
            {
                'section': 'CTA',
                'time': '最后 5 秒',
                'content': CTA_TEMPLATES[hash(topic) % len(CTA_TEMPLATES)],
                'visual': '关注引导',
                'audio': '结束音效',
            },
        ]
    
    return structure

def get_pain_point(topic: str) -> str:
    """获取痛点描述"""
    pain_points = [
        f'在{topic}上踩坑',
        f'花了很多钱却没效果',
        f'试了很多方法都不行',
        f'不知道从哪里开始',
        f'被各种信息搞晕了',
    ]
    return pain_points[hash(topic) % len(pain_points)]

def get_solution_points(topic: str, count: int = 3) -> str:
    """获取解决方案要点"""
    points = [
        f'第一步：明确你的{topic}目标',
        f'第二步：选择适合你的方法',
        f'第三步：坚持执行并调整',
        f'第四步：记录效果并优化',
        f'第五步：分享经验帮助他人',
    ]
    return '\n'.join(points[:count])

def generate_full_script(topic: str, style: str = 'douyin', duration: str = '60 秒') -> Dict[str, Any]:
    """生成完整脚本"""
    platform = PLATFORM_STYLES.get(style, PLATFORM_STYLES['douyin'])
    structure = generate_structure(topic, style, duration)
    
    return {
        'topic': topic,
        'platform': platform['name'],
        'style': style,
        'duration': duration,
        'features': platform['features'],
        'structure': structure,
        'tips': [
            '保持自然，不要过度表演',
            '注意光线和收音质量',
            '字幕要清晰易读',
            'BGM 音量不要盖过人声',
            '发布时间选择流量高峰',
        ],
    }

def main():
    """主函数"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("""
🎬 视频脚本生成工具

用法：
  python3 generate_script.py <命令> [参数]

命令：
  hook <主题> [风格]        - 生成开场 Hook
  structure <主题> [风格]   - 生成视频结构
  full <主题> [风格] [时长] - 生成完整脚本
  platforms                 - 列出支持的平台

风格选项：
  douyin, xiaohongshu, bilibili, youtube

示例：
  python3 generate_script.py hook "护肤"
  python3 generate_script.py structure "护肤" xiaohongshu
  python3 generate_script.py full "护肤" douyin 60 秒
""")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'hook':
        topic = sys.argv[2] if len(sys.argv) > 2 else '主题'
        style = sys.argv[3] if len(sys.argv) > 3 else 'douyin'
        print(f"🎣 开场 Hook（{style}风格）：\n")
        print(generate_hook(topic, style))
    
    elif command == 'structure':
        topic = sys.argv[2] if len(sys.argv) > 2 else '主题'
        style = sys.argv[3] if len(sys.argv) > 3 else 'douyin'
        print(f"📋 视频结构（{style}风格）：\n")
        structure = generate_structure(topic, style)
        for i, section in enumerate(structure, 1):
            print(f"{i}. {section['section']} ({section['time']})")
            print(f"   内容：{section['content']}")
            print(f"   画面：{section['visual']}")
            print(f"   音频：{section['audio']}\n")
    
    elif command == 'full':
        topic = sys.argv[2] if len(sys.argv) > 2 else '主题'
        style = sys.argv[3] if len(sys.argv) > 3 else 'douyin'
        duration = sys.argv[4] if len(sys.argv) > 4 else '60 秒'
        
        script = generate_full_script(topic, style, duration)
        
        print("🎬 完整视频脚本")
        print("=" * 50)
        print(f"\n主题：{script['topic']}")
        print(f"平台：{script['platform']}")
        print(f"时长：{script['duration']}")
        print(f"特点：{', '.join(script['features'])}")
        
        print("\n" + "=" * 50)
        print("\n📋 视频结构：\n")
        for i, section in enumerate(script['structure'], 1):
            print(f"{i}. {section['section']} ({section['time']})")
            print(f"   📝 内容：{section['content']}")
            print(f"   🎬 画面：{section['visual']}")
            print(f"   🎵 音频：{section['audio']}\n")
        
        print("=" * 50)
        print("\n💡 拍摄建议：\n")
        for i, tip in enumerate(script['tips'], 1):
            print(f"{i}. {tip}")
    
    elif command == 'platforms':
        print("📱 支持的平台：\n")
        for key, platform in PLATFORM_STYLES.items():
            print(f"{key}: {platform['name']}")
            print(f"   时长：{platform['duration']}")
            print(f"   特点：{', '.join(platform['features'])}\n")
    
    else:
        print(f"未知命令：{command}")
        print("使用 --help 查看帮助")
        sys.exit(1)

if __name__ == "__main__":
    main()
