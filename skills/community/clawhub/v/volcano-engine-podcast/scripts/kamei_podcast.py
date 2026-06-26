#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎豆包语音播客便捷调用脚本
用于 OpenClaw Agent 快速生成播客并发送给用户
"""

import asyncio
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_podcast import PodcastGenerator

# 从配置文件读取
CONFIG_PATH = Path.home() / ".openclaw" / "config.json"
SEND_DIR = Path("/root/.openclaw/media/qqbot/downloads")


def load_config():
    """加载火山引擎播客配置"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        
        volc = config.get("volc_podcast", {})
        return {
            "appid": volc.get("appid", os.getenv("VOLC_APPID")),
            "access_token": volc.get("access_key", os.getenv("VOLC_ACCESS_TOKEN")),
        }
    return {
        "appid": os.getenv("VOLC_APPID"),
        "access_token": os.getenv("VOLC_ACCESS_TOKEN"),
    }


async def generate_podcast(
    text: str,
    output_name: str = "podcast",
    use_head_music: bool = True,
    use_tail_music: bool = False,
) -> dict:
    """
    生成播客并返回结果
    
    Args:
        text: 输入主题文本
        output_name: 输出文件名（不含扩展名）
        use_head_music: 是否加片头音乐
        use_tail_music: 是否加片尾音乐
    
    Returns:
        {
            "success": bool,
            "audio_path": str,  # 发送目录中的音频路径
            "duration": float,
            "usage": dict,
        }
    """
    config = load_config()
    
    if not config["appid"] or not config["access_token"]:
        return {
            "success": False,
            "error": "未配置火山引擎播客 API Key，请检查 ~/.openclaw/config.json"
        }
    
    # 创建输出目录
    output_dir = Path(f"/tmp/podcast-{output_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 初始化生成器
    gen = PodcastGenerator(
        appid=config["appid"],
        access_token=config["access_token"],
    )
    
    # 生成播客
    result = await gen.generate(
        text=text,
        output_dir=str(output_dir),
        encoding="mp3",
        use_head_music=use_head_music,
        use_tail_music=use_tail_music,
    )
    
    if not result["success"]:
        return {
            "success": False,
            "error": result.get("error", "生成失败")
        }
    
    # 复制到发送目录
    src_file = Path(result["final_files"][0])
    dst_file = SEND_DIR / f"{output_name}.mp3"
    
    shutil.copy(src_file, dst_file)
    
    return {
        "success": True,
        "audio_path": str(dst_file),
        "duration": result["duration"],
        "usage": result["usage"],
        "texts": result["texts"],
    }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="火山引擎豆包语音播客生成器")
    parser.add_argument("text", help="输入主题文本")
    parser.add_argument("-n", "--name", default="podcast", help="输出文件名")
    parser.add_argument("--no-head-music", action="store_true", help="不加片头音乐")
    parser.add_argument("--tail-music", action="store_true", help="加片尾音乐")
    
    args = parser.parse_args()
    
    result = asyncio.run(generate_podcast(
        text=args.text,
        output_name=args.name,
        use_head_music=not args.no_head_music,
        use_tail_music=args.tail_music,
    ))
    
    if result["success"]:
        print(f"\n✅ 播客生成成功！")
        print(f"   时长: {result['duration']} 秒")
        print(f"   音频文件: {result['audio_path']}")
        print(f"   Token 消耗: {result['usage']}")
        
        # 输出发送标签
        print(f"\n<qqvoice>{result['audio_path']}</qqvoice>")
    else:
        print(f"\n❌ 生成失败: {result.get('error', '未知错误')}")
        sys.exit(1)


if __name__ == "__main__":
    main()