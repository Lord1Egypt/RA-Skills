#!/usr/bin/env python3
"""
批量处理 QQ 语音文件
扫描目录并批量转换所有 .amr 文件
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 导入主处理函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from process_qq_voice import decode_qq_voice, check_dependencies


def batch_process(input_dir, output_dir=None, output_json=None):
    """
    批量处理目录下的所有 .amr 文件
    
    参数:
        input_dir: 输入目录
        output_dir: 输出目录（可选）
        output_json: JSON 输出文件路径（可选）
    
    返回:
        处理结果列表
    """
    input_dir = Path(input_dir)
    
    if not input_dir.exists():
        print(f"❌ 目录不存在：{input_dir}")
        return []
    
    if not input_dir.is_dir():
        print(f"❌ 不是目录：{input_dir}")
        return []
    
    # 查找所有 .amr 文件
    amr_files = sorted(input_dir.glob("*.amr"))
    
    if not amr_files:
        print(f"❌ 未找到 .amr 文件：{input_dir}")
        return []
    
    print(f"📂 找到 {len(amr_files)} 个语音文件")
    print(f"📁 目录：{input_dir}")
    
    # 创建输出目录
    if output_dir is None:
        output_dir = input_dir / "output"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 处理统计
    stats = {
        "total": len(amr_files),
        "success": 0,
        "failed": 0,
        "start_time": datetime.now().isoformat(),
        "results": []
    }
    
    # 逐个处理
    for i, amr_file in enumerate(amr_files, 1):
        print(f"\n{'='*50}")
        print(f"[{i}/{len(amr_files)}] 处理：{amr_file.name}")
        print(f"{'='*50}")
        
        mp3, text = decode_qq_voice(amr_file, output_dir)
        
        result = {
            "input": str(amr_file),
            "success": mp3 is not None,
            "mp3": mp3,
            "transcript": text,
            "timestamp": datetime.now().isoformat()
        }
        
        if mp3:
            stats["success"] += 1
            print(f"✅ 成功")
            print(f"🎵 MP3: {mp3}")
            print(f"📝 文字：{text[:100]}...")
        else:
            stats["failed"] += 1
            print(f"❌ 失败")
        
        stats["results"].append(result)
    
    # 完成统计
    stats["end_time"] = datetime.now().isoformat()
    stats["success_rate"] = stats["success"] / stats["total"] if stats["total"] > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"📊 处理完成")
    print(f"{'='*50}")
    print(f"总计：{stats['total']} 个文件")
    print(f"成功：{stats['success']} 个")
    print(f"失败：{stats['failed']} 个")
    print(f"成功率：{stats['success_rate']*100:.1f}%")
    
    # 保存 JSON 报告
    if output_json:
        output_json = Path(output_json)
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"💾 报告已保存：{output_json}")
    
    return stats


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="批量处理 QQ 语音文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 batch_process.py /path/to/voices
  python3 batch_process.py /path/to/voices -o /tmp/output
  python3 batch_process.py /path/to/voices --json report.json
        """
    )
    
    parser.add_argument("input", help="输入目录")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--json", "-j", help="JSON 报告输出路径")
    parser.add_argument("--check", "-c", action="store_true", help="检查依赖")
    
    args = parser.parse_args()
    
    # 检查依赖
    if args.check:
        if check_dependencies():
            print("✅ 所有依赖已安装")
            sys.exit(0)
        else:
            sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # 批量处理
    stats = batch_process(args.input, args.output, args.json)
    
    # 返回状态码
    sys.exit(0 if stats["success"] > 0 else 1)


if __name__ == "__main__":
    main()
