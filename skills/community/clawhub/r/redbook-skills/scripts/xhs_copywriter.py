# -*- coding: utf-8 -*-
# 小红书智能文案生成器
# 自动生成笔记文案、标题优化、标签推荐

import argparse
import json
import random
from datetime import datetime
from pathlib import Path

class XHSCopywriter:
    """小红书文案生成器"""
    
    def __init__(self):
        # 标题模板库
        self.title_templates = {
            'skill': [
                "{num}个{topic}神器，{target}必备！",
                "没想到，{topic}竟然可以这么简单！",
                "用了{time}年，今天才发现这个{topic}功能！",
                "{topic}全攻略！看完这篇就够了！",
                "0 基础学会{topic}，只要{time}！",
            ],
            'news': [
                "{topic}又更新了！这些功能太香了！",
                "重磅！{topic}发布，{impact}！",
                "{topic}大更新！这{num}个变化你必须知道！",
                "刚刚！{topic}刷屏了，原因是...",
                "{topic}新动态！{impact}！",
            ],
            'study': [
                "{time}学会{topic}，我的学习路线！",
                "{topic}入门指南！零基础也能学会！",
                "读完这{num}本书，我{result}！",
                "{topic}学习笔记！干货满满！",
                "从入门到精通，{topic}学习全记录！",
            ]
        }
        
        # 开头模板
        self.intro_templates = [
            "作为一个{role}，每天都要{pain_point}...",
            "最近很多人问我{topic}，今天统一回复！",
            "用了{time}{topic}，今天来分享一下心得...",
            "没想到{topic}可以这么好用！",
            "花{time}整理的{topic}干货，建议收藏！",
        ]
        
        # 结尾模板
        self.outro_templates = [
            "💬 互动话题：{question}\n评论区聊聊～",
            "🎁 福利：评论区抽{num}个小伙伴送{gift}！",
            "⭐ 记得点赞收藏，不然找不到了！",
            "➕ 关注我，分享更多{topic}干货！",
            "📮 有问题私信我，看到必回！",
        ]
    
    def generate_title(self, topic, content_type='skill', num=5):
        """生成标题"""
        templates = self.title_templates.get(content_type, self.title_templates['skill'])
        titles = []
        
        # 替换变量
        replacements = {
            '{num}': str(random.randint(2, 7)),
            '{topic}': topic,
            '{target}': random.choice(['打工人', '学生党', '小白', '新手', '职场人']),
            '{time}': random.choice(['3 天', '7 天', '30 天', '1 小时', '10 分钟']),
            '{impact}': random.choice(['这 5 个职业要被替代', '看完再决定', '太香了', '必须知道']),
            '{result}': random.choice(['工资涨了 3 倍', '效率提升 10 倍', '成功转行', '拿到 offer']),
        }
        
        for template in templates:
            title = template
            for key, value in replacements.items():
                title = title.replace(key, value)
            titles.append(title)
        
        return titles[:num]
    
    def generate_content(self, topic, content_type='skill', points=None):
        """生成正文内容"""
        content = []
        
        # 开头
        intro = random.choice(self.intro_templates).format(
            role=random.choice(['打工人', '程序员', '学生党', '职场新人']),
            pain_point=random.choice(['处理大量文件', '学习效率低', '时间不够用', '找不到资源']),
            topic=topic,
            time=random.choice(['3 年', '半年', '1 个月', '30 天'])
        )
        content.append(intro)
        content.append("")
        
        # 正文（分点说明）
        if points:
            for i, point in enumerate(points, 1):
                content.append(f"{i}️⃣ {point['title']}")
                content.append(point.get('desc', ''))
                content.append("")
        else:
            # 默认内容结构
            content.append("✨ 核心功能/要点：")
            content.append("")
            for i in range(3, 6):
                content.append(f"{i}️⃣ 功能{i-2}")
                content.append(f"   描述{i-2}...")
                content.append("")
        
        # 结尾
        outro = random.choice(self.outro_templates).format(
            question=random.choice(['你平时用什么管理文件？', '你有什么效率神器？', '你想学习什么技能？']),
            num=random.randint(1, 5),
            gift=random.choice(['VIP 会员', '学习资料', '软件安装包', '一对一咨询']),
            topic=topic
        )
        content.append(outro)
        
        return '\n'.join(content)
    
    def generate_tags(self, topic, content_type='skill', count=15):
        """生成标签"""
        # 基础标签
        base_tags = {
            'skill': ['#技能分享', '#干货', '#教程', '#学习', '#成长'],
            'news': ['#科技新闻', '#热点', '#资讯', '#行业动态', '#前沿'],
            'study': ['#学习打卡', '#读书笔记', '#学习心得', '#自我提升', '#成长'],
        }
        
        # 领域标签
        domain_tags = {
            '效率工具': ['#效率工具', '#软件推荐', '#神器', '#打工人', '#职场'],
            '科技': ['#科技', '#数码', '#AI', '#人工智能', '#互联网'],
            '编程': ['#编程', '#Python', '#代码', '#开发者', '#程序员'],
            '学习': ['#学习方法', '#时间管理', '#自律', '#逆袭', '#努力'],
        }
        
        # 热门标签
        hot_tags = ['#小红书成长笔记', '#日常', '#分享', '#推荐', '#必看', 
                   '#收藏', '#实用', '#免费', '#平替', '#学生党']
        
        tags = []
        tags.extend(base_tags.get(content_type, base_tags['skill'])[:3])
        
        # 添加领域标签
        for key, domain_tag_list in domain_tags.items():
            if key in topic:
                tags.extend(domain_tag_list[:5])
                break
        
        # 添加热门标签
        tags.extend(random.sample(hot_tags, min(5, count - len(tags))))
        
        # 添加自定义话题标签
        tags.append(f'#{topic}')
        
        return tags[:count]
    
    def generate_cover_suggestion(self, topic, content_type='skill'):
        """生成封面设计建议"""
        suggestions = {
            'style': random.choice(['简约风', '渐变风', '拼贴风', '手绘风', '科技风']),
            'color': random.choice(['紫色渐变', '蓝色渐变', '橙色系', '绿色系', '粉色系']),
            'font': random.choice(['大字标题', '手写体', '粗体', '艺术字']),
            'layout': random.choice(['居中布局', '左右分割', '上下分割', '对角线布局']),
            'elements': [
                '主图（产品截图/场景图）',
                '大字标题（醒目）',
                '副标题/标签',
                '装饰元素（箭头/圆圈/线条）'
            ]
        }
        
        return suggestions
    
    def generate_draft(self, topic, content_type='skill', points=None, output_file=None):
        """生成完整草稿"""
        draft = []
        draft.append(f"# 小红书笔记草稿")
        draft.append(f"主题：{topic}")
        draft.append(f"类型：{content_type}")
        draft.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        draft.append("")
        
        # 标题备选
        draft.append("## 📝 标题备选（5 选 1）")
        titles = self.generate_title(topic, content_type)
        for i, title in enumerate(titles, 1):
            draft.append(f"{i}. {title}")
        draft.append("")
        
        # 正文
        draft.append("## 📄 正文内容")
        content = self.generate_content(topic, content_type, points)
        draft.append(content)
        draft.append("")
        
        # 标签
        draft.append("## 🏷️ 推荐标签")
        tags = self.generate_tags(topic, content_type)
        draft.append(' '.join(tags))
        draft.append("")
        
        # 封面建议
        draft.append("## 🎨 封面设计建议")
        cover = self.generate_cover_suggestion(topic, content_type)
        draft.append(f"风格：{cover['style']}")
        draft.append(f"配色：{cover['color']}")
        draft.append(f"字体：{cover['font']}")
        draft.append(f"布局：{cover['layout']}")
        draft.append(f"元素：{', '.join(cover['elements'])}")
        draft.append("")
        
        # 发布建议
        draft.append("## ⏰ 发布建议")
        draft.append("最佳时间：19:00-22:00（睡前）")
        draft.append("次佳时间：12:00-14:00（午休）")
        draft.append("发布频率：每周 3-5 篇")
        draft.append("")
        
        full_text = '\n'.join(draft)
        
        # 保存到文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"✅ 草稿已保存到：{output_file}")
        
        return full_text


def main():
    parser = argparse.ArgumentParser(description='小红书智能文案生成器')
    parser.add_argument('--type', type=str, default='skill', 
                       choices=['skill', 'news', 'study'],
                       help='内容类型：skill=技能分享，news=科技新闻，study=学习内容')
    parser.add_argument('--topic', type=str, required=True, help='主题/话题')
    parser.add_argument('--output', type=str, default='draft.md', help='输出文件名')
    parser.add_argument('--points', type=str, help='要点列表（JSON 格式）')
    
    args = parser.parse_args()
    
    # 解析要点
    points = None
    if args.points:
        try:
            points = json.loads(args.points)
        except:
            print("⚠️ points 格式错误，使用默认内容")
    
    # 生成草稿
    copywriter = XHSCopywriter()
    draft = copywriter.generate_draft(
        topic=args.topic,
        content_type=args.type,
        points=points,
        output_file=args.output
    )
    
    print("\n" + "="*50)
    print("✅ 文案生成完成！")
    print("="*50)
    print(draft)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
