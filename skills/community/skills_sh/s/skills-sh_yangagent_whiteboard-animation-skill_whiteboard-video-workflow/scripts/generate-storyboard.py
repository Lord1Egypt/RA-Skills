#!/usr/bin/env python3
"""
generate-storyboard.py

根据 SRT 文件和 AI 生成的分组信息，生成 storyboard.json

用法: python3 generate-storyboard.py <srtPath> <groupsPath> <outputPath>

输入:
  - srtPath: SRT 字幕文件路径
  - groupsPath: AI 生成的 groups.json 路径
  - outputPath: 输出的 storyboard.json 路径

groups.json 格式:
  {
    "groups": [
      {
        "sceneId": "scene_001",
        "fromIndex": 1,
        "toIndex": 3,
        "semanticTags": ["开场", "介绍"],
        "visualHint": "大标题居中，配合动画演示稿相关图标"
      },
      ...
    ]
  }
"""

import json
import re
import sys


# ============ SRT 解析 ============

def parse_time_code(time_str):
    """解析时间码为毫秒"""
    match = re.match(r'(\d{2}):(\d{2}):(\d{2})[,.](\d{3})', time_str.strip())
    if not match:
        raise ValueError(f'无效的时间码格式: {time_str}')
    hours, minutes, seconds, ms = match.groups()
    return (
        int(hours) * 3600000 +
        int(minutes) * 60000 +
        int(seconds) * 1000 +
        int(ms)
    )


def parse_srt(srt_content):
    """解析 SRT 文件"""
    subtitles = []

    # 统一换行符，兼容 CRLF (\r\n) 和 LF (\n)
    normalized = srt_content.replace('\r\n', '\n').replace('\r', '\n')
    blocks = re.split(r'\n\s*\n', normalized.strip())

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue

        # 第一行: 序号
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue

        # 第二行: 时间码
        time_line = lines[1].strip()
        time_match = re.match(r'(.+?)\s*-->\s*(.+)', time_line)
        if not time_match:
            continue

        start_ms = parse_time_code(time_match.group(1))
        end_ms = parse_time_code(time_match.group(2))

        # 第三行及以后: 文本
        text = '\n'.join(lines[2:]).strip()

        subtitles.append({'index': index, 'startMs': start_ms, 'endMs': end_ms, 'text': text})

    # 按序号排序
    subtitles.sort(key=lambda a: a['index'])

    return subtitles


# ============ 分组验证 ============

def validate_groups(groups, total_subtitles):
    """验证分组数据的完整性和连续性"""
    errors = []

    if not groups:
        errors.append('分组数据为空')
        return {'valid': False, 'errors': errors}

    # 检查第一个分组的 fromIndex 是否为 1
    if groups[0]['fromIndex'] != 1:
        errors.append(f"第一个分组的 fromIndex 必须为 1，实际为 {groups[0]['fromIndex']}")

    # 检查最后一个分组的 toIndex 是否等于字幕总数
    last_group = groups[-1]
    if last_group['toIndex'] != total_subtitles:
        errors.append(f"最后一个分组的 toIndex 必须为 {total_subtitles}，实际为 {last_group['toIndex']}")

    # 检查连续性和 sceneId 格式
    for i, group in enumerate(groups):
        expected_scene_id = f"scene_{str(i + 1).zfill(3)}"

        # 检查 sceneId 格式
        if group['sceneId'] != expected_scene_id:
            errors.append(f"分组 {i + 1} 的 sceneId 应为 {expected_scene_id}，实际为 {group['sceneId']}")

        # 检查 fromIndex <= toIndex
        if group['fromIndex'] > group['toIndex']:
            errors.append(f"分组 {group['sceneId']} 的 fromIndex ({group['fromIndex']}) 大于 toIndex ({group['toIndex']})")

        # 检查与前一个分组的连续性
        if i > 0:
            prev_group = groups[i - 1]
            if group['fromIndex'] != prev_group['toIndex'] + 1:
                errors.append(f"分组 {group['sceneId']} 的 fromIndex ({group['fromIndex']}) 与前一个分组的 toIndex ({prev_group['toIndex']}) 不连续")

    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


# ============ 生成 Storyboard ============

def generate_scenes(subtitles, groups):
    """根据分组信息生成场景"""
    scenes = []

    # 创建字幕索引映射 (index -> subtitle)
    subtitle_map = {sub['index']: sub for sub in subtitles}

    # 第一遍：收集每个分组的字幕，计算 startTime
    group_infos = []
    for group in groups:
        group_subtitles = []
        for idx in range(group['fromIndex'], group['toIndex'] + 1):
            sub = subtitle_map.get(idx)
            if sub:
                group_subtitles.append(sub)
        group_infos.append({'group': group, 'groupSubtitles': group_subtitles})

    # 第二遍：计算每个场景的 duration 和 segments
    for i, info in enumerate(group_infos):
        group = info['group']
        group_subtitles = info['groupSubtitles']

        if not group_subtitles:
            print(f"警告: 分组 {group['sceneId']} 没有找到对应的字幕")
            continue

        # 计算场景的 startTime (第一条字幕的开始时间)
        start_time = group_subtitles[0]['startMs']

        # 生成 segments，计算相对时间
        segments = []
        for idx, sub in enumerate(group_subtitles):
            # relativeStart: 相对于场景开始的时间
            # 第一个 segment 的 relativeStart 必须为 0
            relative_start = 0 if idx == 0 else sub['startMs'] - start_time

            # relativeDuration: 该字幕的持续时间
            relative_duration = sub['endMs'] - sub['startMs']

            segments.append({
                'text': sub['text'],
                'relativeStart': relative_start,
                'relativeDuration': relative_duration
            })

        # 计算场景的 duration：包含到下一个场景开始前的间隙
        # 非最后一个场景：用下一个场景的 startTime 减去当前场景的 startTime
        # 最后一个场景：用最后一条字幕的结束时间减去当前场景的 startTime
        if i < len(group_infos) - 1:
            next_group_start_time = group_infos[i + 1]['groupSubtitles'][0]['startMs']
            duration = next_group_start_time - start_time
        else:
            last_segment = segments[-1]
            duration = last_segment['relativeStart'] + last_segment['relativeDuration']

        scene = {
            'id': group['sceneId'],
            'startTime': start_time,
            'duration': duration,
            'segments': segments
        }

        # 添加可选字段
        if group.get('semanticTags'):
            scene['semanticTags'] = group['semanticTags']
        if group.get('visualHint'):
            scene['visualHint'] = group['visualHint']

        scenes.append(scene)

    return scenes


def generate_storyboard(scenes):
    """生成完整的 storyboard 数据"""
    if not scenes:
        return {
            'totalDuration': 0,
            'sceneCount': 0,
            'scenes': []
        }

    last_scene = scenes[-1]
    total_duration = last_scene['startTime'] + last_scene['duration']

    return {
        'totalDuration': total_duration,
        'sceneCount': len(scenes),
        'scenes': scenes
    }


# ============ 主函数 ============

def main():
    args = sys.argv[1:]

    if len(args) < 3:
        print('用法: python3 generate-storyboard.py <srtPath> <groupsPath> <outputPath>')
        print('')
        print('参数:')
        print('  srtPath     SRT 字幕文件路径')
        print('  groupsPath  AI 生成的 groups.json 路径')
        print('  outputPath  输出的 storyboard.json 路径')
        sys.exit(1)

    srt_path, groups_path, output_path = args[0], args[1], args[2]

    try:
        # 1. 解析 SRT 文件
        print(f'📄 解析 SRT 文件: {srt_path}')
        with open(srt_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
        subtitles = parse_srt(srt_content)
        print(f'   找到 {len(subtitles)} 条字幕')

        # 2. 读取分组信息
        print(f'📋 读取分组信息: {groups_path}')
        with open(groups_path, 'r', encoding='utf-8') as f:
            groups_data = json.load(f)
        groups = groups_data['groups']
        print(f'   找到 {len(groups)} 个分组')

        # 3. 验证分组数据
        print('🔍 验证分组数据...')
        validation = validate_groups(groups, len(subtitles))
        if not validation['valid']:
            print('❌ 分组验证失败:')
            for err in validation['errors']:
                print(f'   - {err}')
            sys.exit(1)
        print('   ✅ 分组验证通过')

        # 4. 生成场景
        print('🎬 生成场景...')
        scenes = generate_scenes(subtitles, groups)

        # 5. 生成 storyboard
        storyboard = generate_storyboard(scenes)

        # 6. 写入文件
        print(f'💾 写入文件: {output_path}')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(storyboard, f, ensure_ascii=False, indent=2)

        # 7. 输出摘要
        print('')
        print('✅ 生成完成!')
        print(f'   - 场景数量: {storyboard["sceneCount"]}')
        print(f'   - 总时长: {storyboard["totalDuration"] / 1000:.1f}s')
        print(f'   - 输出文件: {output_path}')

        # 输出 JSON 结果供调用方使用
        print('')
        print('__RESULT_JSON__')
        print(json.dumps({
            'success': True,
            'storyboardPath': output_path,
            'sceneCount': storyboard['sceneCount'],
            'totalDuration': storyboard['totalDuration']
        }, ensure_ascii=False))

    except FileNotFoundError as e:
        print(f'❌ 错误: 文件不存在: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'❌ 错误: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
