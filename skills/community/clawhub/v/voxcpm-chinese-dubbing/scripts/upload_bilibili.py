#!/usr/bin/env python3
"""B站视频上传脚本"""
import json
import os
import sys
import asyncio
from pathlib import Path
from bilibili_api import video_uploader, Credential

# 加载凭证
CRED_PATH = Path("D:/openclaw_workspace/credentials/bilibili.json")
with open(CRED_PATH) as f:
    creds = json.load(f)

SESSDATA = creds['sessdata']
BILI_JCT = creds['bili_jct']

print('B站凭证已加载')

credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT)

async def upload_video(video_path, title, desc, tags, source="", tid=122, copyright=2):
    """上传视频到B站"""
    print(f'\n[*] 开始上传视频到B站...')
    print(f'    视频文件: {video_path}')
    print(f'    标题: {title}')
    print(f'    标签: {tags}')
    
    video_path = Path(video_path)
    
    # 生成封面
    cover_path = str(video_path.parent / "cover.jpg")
    import subprocess
    subprocess.run([
        'E:/ImageMagick-7.1.1-Q16-HDRI/ffmpeg.exe', '-y', '-i', str(video_path),
        '-vframes', '1', '-q:v', '2', cover_path
    ], capture_output=True)
    print(f'    封面已生成: {cover_path}')
    
    # 创建上传页面
    page = video_uploader.VideoUploaderPage(
        path=str(video_path),
        title=title
    )
    
    # 视频元数据
    meta = {
        "title": title,
        "copyright": copyright,  # 2=转载
        "source": source,
        "tid": tid,  # 科技->科学技术
        "tag": tags,
        "desc_format_id": 9999,
        "desc": desc,
        "recreate": -1,
        "dynamic": "",
        "interactive": 0,
        "act_reserve_create": 0,
        "no_disturbance": 0,
        "no_reprint": 0,
        "subtitle": {"open": 1, "lan": "zh-CN"},
        "dolby": 0,
        "lossless_music": 0,
        "web_os": 1
    }
    
    # 创建上传器
    uploader = video_uploader.VideoUploader(
        pages=[page],
        meta=meta,
        credential=credential,
        cover=cover_path,
    )
    
    # 开始上传
    print('    上传中...')
    result = await uploader.start()
    print(f'\n[OK] 上传完成！')
    print(f'    结果: {result}')
    
    return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='B站视频上传')
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('--title', '-t', help='视频标题')
    parser.add_argument('--source', '-s', default='YouTube', help='来源URL')
    parser.add_argument('--desc', '-d', help='视频简介')
    parser.add_argument('--tags', default='AI配音,科技,工具推荐', help='标签(逗号分隔)')
    
    args = parser.parse_args()
    
    video_path = args.video_path
    title = args.title or Path(video_path).stem
    source = args.source
    desc = args.desc or f"{title}\n\n本视频由AI自动翻译配音生成\n\n来源：{source}"
    tags = args.tags
    
    asyncio.run(upload_video(video_path, title, desc, tags, source=source))