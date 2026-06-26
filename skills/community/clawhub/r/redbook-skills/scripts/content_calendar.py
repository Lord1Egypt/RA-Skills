# -*- coding: utf-8 -*-
# 小红书内容日历生成器
# 30 天内容规划、发布时间建议、选题库管理

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

class ContentCalendar:
    """小红书内容日历生成器"""
    
    def __init__(self):
        # 内容类型分布建议
        self.content_distribution = {
            'skill': 0.6,    # 技能分享 60%
            'news': 0.3,     # 科技新闻 30%
            'study': 0.1     # 学习内容 10%
        }
        
        # 最佳发布时间
        self.best_posting_times = [
            '07:00-09:00',  # 通勤时间
            '12:00-14:00',  # 午休时间
            '19:00-22:00',  # 睡前时间（最佳）
        ]
        
        # 选题库
        self.topic_pool = {
            'skill': [
                '效率工具合集', '文件管理技巧', '时间管理方法',
                '软件推荐', '工作流程优化', '自动化脚本',
                '编程技巧', '学习资源', '知识管理'
            ],
            'news': [
                'AI 大模型更新', '科技产品发布', '行业动态',
                '新技术解读', '产品评测', '趋势分析'
            ],
            'study': [
                '读书分享', '学习笔记', '方法总结',
                '成长感悟', '项目记录', '经验复盘'
            ]
        }
    
    def generate_calendar(self, days=30, start_date=None, output_file='calendar.md'):
        """生成内容日历"""
        if not start_date:
            start_date = datetime.now()
        
        calendar = []
        calendar.append(f"# 小红书内容日历")
        calendar.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d')}")
        calendar.append(f"周期：{days}天")
        calendar.append(f"开始日期：{start_date.strftime('%Y-%m-%d')}")
        calendar.append("")
        
        # 统计信息
        stats = {'skill': 0, 'news': 0, 'study': 0}
        
        # 按周分组
        current_date = start_date
        week_num = 1
        
        calendar.append(f"## 第{week_num}周")
        calendar.append("")
        
        for day in range(days):
            # 判断是否新的一周
            if day > 0 and day % 7 == 0:
                week_num += 1
                calendar.append("")
                calendar.append(f"## 第{week_num}周")
                calendar.append("")
            
            # 确定内容类型（根据分布）
            content_type = self._determine_content_type(day, stats)
            stats[content_type] += 1
            
            # 选择主题
            topic = self._select_topic(content_type, day)
            
            # 生成标题建议
            title = self._generate_title_suggestion(topic, content_type)
            
            # 选择发布时间
            post_time = self._select_posting_time(day)
            
            # 添加标签建议
            tags = self._suggest_tags(topic)
            
            # 添加笔记
            calendar.append(f"### {current_date.strftime('%Y-%m-%d')} ({self._get_weekday(current_date)})")
            calendar.append(f"**类型**：{self._get_type_name(content_type)}")
            calendar.append(f"**主题**：{topic}")
            calendar.append(f"**标题**：{title}")
            calendar.append(f"**时间**：{post_time}")
            calendar.append(f"**标签**：{tags}")
            calendar.append("")
            
            # 日期递增
            current_date += timedelta(days=1)
        
        # 总结
        calendar.append("## 📊 内容分布统计")
        calendar.append(f"- 技能分享：{stats['skill']}篇 ({stats['skill']/days*100:.1f}%)")
        calendar.append(f"- 科技新闻：{stats['news']}篇 ({stats['news']/days*100:.1f}%)")
        calendar.append(f"- 学习内容：{stats['study']}篇 ({stats['study']/days*100:.1f}%)")
        calendar.append("")
        
        calendar.append("## 💡 运营建议")
        calendar.append("1. 保持固定更新频率（建议每周 3-5 篇）")
        calendar.append("2. 选择最佳发布时间（19:00-22:00）")
        calendar.append("3. 关注热点话题，及时调整内容")
        calendar.append("4. 分析数据，优化内容方向")
        calendar.append("5. 积极互动，提高粉丝粘性")
        
        full_text = '\n'.join(calendar)
        
        # 保存到文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"✅ 内容日历已保存到：{output_file}")
        
        return full_text
    
    def _determine_content_type(self, day, stats):
        """确定内容类型"""
        total = sum(stats.values())
        if total == 0:
            return 'skill'
        
        # 根据分布决定
        skill_ratio = stats['skill'] / total
        news_ratio = stats['news'] / total
        
        if skill_ratio < self.content_distribution['skill']:
            return 'skill'
        elif news_ratio < self.content_distribution['news']:
            return 'news'
        else:
            return 'study'
    
    def _select_topic(self, content_type, day):
        """选择主题"""
        topics = self.topic_pool.get(content_type, self.topic_pool['skill'])
        # 根据日期选择不同主题
        return topics[day % len(topics)]
    
    def _generate_title_suggestion(self, topic, content_type):
        """生成标题建议"""
        templates = {
            'skill': f'3 个{topic}技巧，效率提升 10 倍！',
            'news': f'{topic}新动态！这些变化你必须知道！',
            'study': f'{topic}学习笔记！干货满满！'
        }
        return templates.get(content_type, topic)
    
    def _select_posting_time(self, day):
        """选择发布时间"""
        # 工作日和周末不同
        return self.best_posting_times[day % 3]
    
    def _get_weekday(self, date):
        """获取星期几"""
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return weekdays[date.weekday()]
    
    def _get_type_name(self, content_type):
        """获取类型名称"""
        names = {
            'skill': '💻 技能分享',
            'news': '📰 科技新闻',
            'study': '📚 学习内容'
        }
        return names.get(content_type, '技能分享')
    
    def _suggest_tags(self, topic):
        """建议标签"""
        base_tags = ['#干货', '#分享', '#实用']
        return ' '.join(base_tags + [f'#{topic}'])
    
    def view_week(self, calendar_file='calendar.md'):
        """查看本周计划"""
        if not Path(calendar_file).exists():
            print(f"❌ 文件不存在：{calendar_file}")
            return
        
        # 读取并显示本周内容
        with open(calendar_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单实现：显示前 7 篇笔记
        lines = content.split('\n')
        week_count = 0
        note_count = 0
        
        print("📅 本周内容计划：")
        print("="*50)
        
        for line in lines:
            if line.startswith('### '):
                note_count += 1
                if note_count <= 7:
                    print(line)
            elif note_count <= 7 and line.startswith('**'):
                print(line)
        
        print("="*50)


def main():
    parser = argparse.ArgumentParser(description='小红书内容日历生成器')
    parser.add_argument('--days', type=int, default=30, help='天数')
    parser.add_argument('--start', type=str, help='开始日期（YYYY-MM-DD）')
    parser.add_argument('--output', type=str, default='calendar.md', help='输出文件')
    parser.add_argument('--view', type=str, choices=['week', 'month'], help='查看模式')
    
    args = parser.parse_args()
    
    calendar = ContentCalendar()
    
    if args.view:
        # 查看模式
        calendar.view_week(args.output)
    else:
        # 生成模式
        start_date = None
        if args.start:
            try:
                start_date = datetime.strptime(args.start, '%Y-%m-%d')
            except:
                print("⚠️ 日期格式错误，使用今天")
        
        full_calendar = calendar.generate_calendar(
            days=args.days,
            start_date=start_date,
            output_file=args.output
        )
        
        print("\n" + "="*50)
        print("✅ 内容日历生成完成！")
        print("="*50)
        print(f"📄 输出文件：{args.output}")
        print(f"📅 周期：{args.days}天")
        print("="*50)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
