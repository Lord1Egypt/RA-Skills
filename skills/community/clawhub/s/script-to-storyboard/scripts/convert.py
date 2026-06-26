#!/usr/bin/env python3
"""
Script to Storyboard Converter
将剧本转换为分镜脚本表格
"""

import re
import csv
import sys
from pathlib import Path

# 景别关键词
SHOT_TYPES = {
    '远景': '远景', '全景': '全景', '全景': '全景',
    '中景': '中景', '中近景': '中近景', '近景': '近景',
    '特写': '特写', '大特写': '特写',
}

# 角度关键词
ANGLE_TYPES = {
    '俯拍': '俯拍', '俯视': '俯拍', '鸟瞰': '俯拍',
    '仰拍': '仰拍', '仰视': '仰拍', '蚂蚁视角': '仰拍',
    '平拍': '平拍', '平视': '平拍',
    '斜拍': '斜拍', '侧拍': '侧拍',
}

# 镜头运动关键词
CAMERA_MOVES = {
    '推': '推镜头', '拉': '拉镜头',
    '摇': '摇镜头', '移': '移镜头',
    '跟': '跟镜头', '甩': '甩镜头',
    '旋转': '旋转', '升降': '升降',
}

def parse_script(text):
    """解析剧本文本，提取分镜信息"""
    lines = text.strip().split('\n')
    shots = []
    current_shot = None
    
    # 提取场景信息
    scene_match = re.search(r'场景[：:]\s*(.+)', text)
    location_match = re.search(r'(海滩|沙滩|室内|室外|森林|城市|乡村|海边|酒店|房间|办公室|教室|街道|厨房|客厅|卧室|浴室|阳台|花园|泳池|码头|船上|车内|机场|车站|商场|餐厅|酒吧|咖啡馆|图书馆|博物馆|剧院|电影院|医院|学校|工厂|仓库|停车场|公园|广场|山林|湖边|河边|山顶|山坡|沙漠|草原|沼泽|废墟|古堡|宫殿|教堂|寺庙|塔楼|桥上|隧道|矿井|地道|水下|太空|外星|梦境|回忆|虚构)', text)
    
    scene = scene_match.group(1) if scene_match else location_match.group(1) if location_match else "未标注"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检测镜头指示
        shot_indicator = None
        for keyword in list(SHOT_TYPES.keys()) + list(ANGLE_TYPES.keys()) + list(CAMERA_MOVES.keys()):
            if keyword in line:
                shot_indicator = keyword
                break
        
        # 如果是新的镜头指示，开始新镜头
        if shot_indicator or re.match(r'^\d+[.、]\s*', line) or '镜头' in line:
            if current_shot and current_shot.get('content'):
                shots.append(current_shot)
            
            # 提取镜头信息
            shot_info = {
                'shot_type': '',
                'angle': '',
                'camera_move': '',
                'content': '',
                'characters': [],
                'scene': scene,
                'sound': '',
            }
            
            # 解析景别
            for keyword, value in SHOT_TYPES.items():
                if keyword in line:
                    shot_info['shot_type'] = value
                    break
            
            # 解析角度
            for keyword, value in ANGLE_TYPES.items():
                if keyword in line:
                    shot_info['angle'] = value
                    break
            
            # 解析运镜
            for keyword, value in CAMERA_MOVES.items():
                if keyword in line:
                    shot_info['camera_move'] = value
                    break
            
            current_shot = shot_info
            continue
        
        # 如果有当前镜头，追加内容
        if current_shot is not None:
            # 提取人物
            char_match = re.findall(r'【([^】]+)】', line)
            if char_match:
                current_shot['characters'].extend(char_match)
            
            # 提取对白中的角色
            dialogue_chars = re.findall(r'^([A-Za-z]+)：', line)
            if dialogue_chars:
                current_shot['characters'].extend(dialogue_chars)
            
            # 提取音效
            if '音效' in line or '音乐' in line or '声音' in line:
                sound_match = re.search(r'[音效音乐声音][：:]\s*(.+)', line)
                if sound_match:
                    current_shot['sound'] = sound_match.group(1)
            
            # 追加画面内容
            # 移除角色名和对白，只保留动作描述
            content_line = re.sub(r'【[^】]+】', '', line)
            content_line = re.sub(r'^[A-Za-z]+：.*$', '', content_line)
            content_line = content_line.strip()
            
            if content_line:
                if current_shot['content']:
                    current_shot['content'] += ' ' + content_line
                else:
                    current_shot['content'] = content_line
    
    # 添加最后一个镜头
    if current_shot and current_shot.get('content'):
        shots.append(current_shot)
    
    return shots

def generate_shot_number(shots):
    """生成镜号"""
    for i, shot in enumerate(shots, 1):
        shot['shot_number'] = f"{i:02d}"
    return shots

def format_characters(chars):
    """格式化出场人物"""
    if not chars:
        return "无"
    # 去重
    unique_chars = list(set(chars))
    return '、'.join(unique_chars)

def format_sound(shot, prev_shot=None):
    """格式化音效"""
    if shot.get('sound'):
        return shot['sound']
    
    # 根据场景推断默认音效
    scene = shot.get('scene', '')
    shot_type = shot.get('shot_type', '')
    
    if '沙滩' in scene or '海' in scene:
        return '海浪声、背景音乐'
    elif '室内' in scene:
        return '环境音、背景音乐'
    elif shot_type == '特写':
        return '环境音'
    else:
        return '背景音乐'

def enhance_shots(shots):
    """增强镜头信息"""
    for i, shot in enumerate(shots):
        # 设置默认景别
        if not shot.get('shot_type'):
            if i == 0:
                shot['shot_type'] = '远景'  # 开场通常是全景
            elif i == len(shots) - 1:
                shot['shot_type'] = '全景'  # 结尾通常是全景
            else:
                shot['shot_type'] = '中景'
        
        # 设置默认角度
        if not shot.get('angle'):
            shot['angle'] = '平拍'
        
        # 格式化出场人物
        shot['characters_str'] = format_characters(shot.get('characters', []))
        
        # 格式化音效
        prev_shot = shots[i-1] if i > 0 else None
        shot['sound_str'] = format_sound(shot, prev_shot)
        
        # 清理画面内容
        if not shot.get('content'):
            shot['content'] = '（待补充）'
    
    return shots

def generate_csv(shots, output_file):
    """生成分镜CSV文件"""
    fieldnames = ['镜号', '景别/拍摄角度', '画面内容', '出场人物', '场景', '音效']
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for shot in shots:
            # 合并景别和角度
            shot_type = shot.get('shot_type', '中景')
            angle = shot.get('angle', '平拍')
            camera_move = shot.get('camera_move', '')
            
            if camera_move:
                shot_type_angle = f"{shot_type}/{angle}/{camera_move}"
            else:
                shot_type_angle = f"{shot_type}/{angle}"
            
            writer.writerow({
                '镜号': shot.get('shot_number', ''),
                '景别/拍摄角度': shot_type_angle,
                '画面内容': shot.get('content', ''),
                '出场人物': shot.get('characters_str', '无'),
                '场景': shot.get('scene', ''),
                '音效': shot.get('sound_str', ''),
            })
    
    return output_file

def print_storyboard(shots):
    """打印分镜表格到控制台"""
    print("\n" + "="*100)
    print(f"{'镜号':^6}{'景别/角度':^20}{'画面内容':^30}{'出场人物':^15}{'场景':^15}{'音效':^15}")
    print("="*100)
    
    for shot in shots:
        shot_type = shot.get('shot_type', '')
        angle = shot.get('angle', '')
        camera_move = shot.get('camera_move', '')
        
        if camera_move:
            shot_type_angle = f"{shot_type}/{angle}/{camera_move}"
        else:
            shot_type_angle = f"{shot_type}/{angle}"
        
        content = shot.get('content', '')[:28] + '..' if len(shot.get('content', '')) > 30 else shot.get('content', '')
        chars = shot.get('characters_str', '无')[:13] + '..' if len(shot.get('characters_str', '无')) > 15 else shot.get('characters_str', '无')
        scene = shot.get('scene', '')[:13] + '..' if len(shot.get('scene', '')) > 15 else shot.get('scene', '')
        sound = shot.get('sound_str', '')[:13] + '..' if len(shot.get('sound_str', '')) > 15 else shot.get('sound_str', '')
        
        print(f"{shot.get('shot_number', ''):^6}{shot_type_angle:^20}{content:^30}{chars:^15}{scene:^15}{sound:^15}")
    
    print("="*100 + "\n")

def main():
    if len(sys.argv) < 2:
        print("用法: python3 convert.py <输入剧本.txt> [输出分镜.csv]")
        print("示例: python3 convert.py script.txt storyboard.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'storyboard.csv'
    
    # 读取剧本
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            script_text = f.read()
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取文件失败 - {e}")
        sys.exit(1)
    
    # 解析剧本
    shots = parse_script(script_text)
    
    if not shots:
        print("警告: 未能从剧本中解析出镜头信息")
        print("请确保剧本包含镜头指示（如：特写、远景、推镜头等）")
        sys.exit(1)
    
    # 生成镜号
    shots = generate_shot_number(shots)
    
    # 增强镜头信息
    shots = enhance_shots(shots)
    
    # 打印分镜表格
    print_storyboard(shots)
    
    # 生成CSV
    generate_csv(shots, output_file)
    print(f"分镜脚本已保存到: {output_file}")

if __name__ == '__main__':
    main()
