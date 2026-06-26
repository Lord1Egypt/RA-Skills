#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间线推进图生成模板
使用方法：修改 events 列表，运行脚本即可生成时间线图
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_timeline(events, output_path, title='时间线推进图'):
    """
    生成时间线推进图
    
    参数:
        events: 事件列表，格式 [(日期, 事件, 标签, 详情), ...]
        output_path: 输出路径
        title: 标题
    """
    # 计算画布尺寸
    num_events = len(events)
    spacing = 200
    timeline_top = 200
    timeline_bottom = timeline_top + (num_events - 1) * spacing
    height = 140 + (num_events - 1) * spacing + 80 + 100
    
    # 创建画布
    width = 1200
    img = Image.new('RGB', (width, height), '#F8FAFC')
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    font_path = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
    font_bold = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
    
    try:
        font_title = ImageFont.truetype(font_bold, 42)
        font_subtitle = ImageFont.truetype(font_path, 30)
        font_date = ImageFont.truetype(font_path, 26)
        font_event = ImageFont.truetype(font_path, 22)
        font_tag = ImageFont.truetype(font_bold, 20)
        font_detail = ImageFont.truetype(font_path, 18)
    except Exception as e:
        print(f"字体加载失败: {e}")
        print("请安装字体: apt-get install -y fonts-noto-cjk")
        raise
    
    # 颜色定义
    blue_primary = '#1E40AF'
    blue_secondary = '#3B82F6'
    blue_light = '#DBEAFE'
    gray_dark = '#1F2937'
    gray_light = '#6B7280'
    white = '#FFFFFF'
    green = '#059669'
    orange = '#D97706'
    
    # 绘制标题背景
    draw.rectangle([(0, 0), (width, 140)], fill=blue_primary)
    
    # 绘制标题
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 25), title, fill=white, font=font_title)
    
    subtitle = '时间线推进图'
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(((width - subtitle_width) // 2, 85), subtitle, fill=blue_light, font=font_subtitle)
    
    # 绘制时间线
    timeline_x = 220
    draw.line([(timeline_x, timeline_top), (timeline_x, timeline_bottom)], 
              fill=blue_secondary, width=5)
    
    # 绘制事件节点
    for i, (date, event, tag, detail) in enumerate(events):
        y = timeline_top + i * spacing
        
        # 绘制连接线到卡片
        card_x = timeline_x + 50
        draw.line([(timeline_x + 15, y), (card_x, y)], fill=blue_secondary, width=2)
        
        # 绘制节点
        if i == 0:
            node_color = green
        elif i == num_events - 1:
            node_color = blue_primary
        elif '放弃' in event or '失败' in event:
            node_color = orange
        else:
            node_color = blue_secondary
        
        # 节点外圈
        draw.ellipse([(timeline_x - 18, y - 18), (timeline_x + 18, y + 18)],
                     fill=white, outline=node_color, width=3)
        # 节点内圈
        draw.ellipse([(timeline_x - 12, y - 12), (timeline_x + 12, y + 12)],
                     fill=node_color)
        
        # 绘制日期
        date_bbox = draw.textbbox((0, 0), date, font=font_date)
        date_width = date_bbox[2] - date_bbox[0]
        date_x = timeline_x - date_width - 40
        draw.text((date_x, y - 13), date, fill=blue_primary, font=font_date)
        
        # 计算卡片高度
        card_y = y - 45
        card_height = 145 if detail else 85
        
        # 卡片背景颜色
        if '放弃' in event or '失败' in event:
            card_fill = '#FEF3C7'  # 浅黄色
        elif i == num_events - 1:
            card_fill = '#D1FAE5'  # 浅绿色
        elif i % 2 == 0:
            card_fill = blue_light
        else:
            card_fill = white
        
        # 绘制卡片
        draw.rounded_rectangle(
            [(card_x, card_y), (card_x + 880, card_y + card_height)],
            radius=12, fill=card_fill, outline=blue_secondary, width=2
        )
        
        # 绘制标签
        tag_bbox = draw.textbbox((0, 0), tag, font=font_tag)
        tag_width = tag_bbox[2] - tag_bbox[0]
        tag_x = card_x + 20
        tag_y = card_y + 12
        
        draw.rounded_rectangle(
            [(tag_x - 5, tag_y - 3), (tag_x + tag_width + 20, tag_y + 30)],
            radius=6, fill=blue_secondary
        )
        draw.text((tag_x + 5, tag_y), tag, fill=white, font=font_tag)
        
        # 绘制事件描述
        draw.text((card_x + 20, card_y + 48), event, fill=gray_dark, font=font_event)
        
        # 绘制详细信息
        if detail:
            detail_y = card_y + 80
            for line in detail.split('\n'):
                draw.text((card_x + 40, detail_y), line, fill=gray_light, font=font_detail)
                detail_y += 26
    
    # 添加底部信息栏
    footer_y = height - 80
    draw.rectangle([(0, footer_y - 10), (width, height)], fill='#F1F5F9')
    
    # 保存图片
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG', quality=95)
    print(f'✅ 时间线图已生成: {output_path}')
    return output_path


# 使用示例
if __name__ == '__main__':
    # 修改这里的事件列表
    events = [
        ('2018-07-24', '总经理办公会决策启动招选工作', '决策启动', None),
        ('2018-08-01', '招选公示发布，报名开始', '公示发布', None),
        ('2018-08-04', '报名截止（4家供应商报名）', '报名截止', None),
        ('2018-08-06', '公开唱价，确定候选人排名', '公开唱价', 
         '第一候选人：神州顶联科技有限公司（支付比例32%）\n第二候选人：上海寰创网络科技有限公司（支付比例30%）'),
        ('2018-08-20', '第一候选人神州顶联科技有限公司放弃项目', '候选人放弃', None),
        ('2018-08-27', '总经理办公会决策同意与第二候选人合作', '决策同意', None),
        ('2018-09-25', '合同完成审批', '审批完成', None),
        ('2018-09-28', '合同签订（协议期8年）', '合同签订', 
         '最终签约：上海寰创网络科技有限公司\n支付比例：30%'),
    ]
    
    # 生成时间线图
    create_timeline(
        events, 
        'output/timeline_example.png',
        '昆明学院无线校园网合作运营项目'
    )
