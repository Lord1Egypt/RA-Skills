#!/usr/bin/env python3
"""
历史周报管理脚本
保存、查询历史周报
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


def get_history_dir() -> Path:
    """获取历史周报存储目录"""
    home = Path.home()
    history_dir = home / ".weekly-report" / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    return history_dir


def save_report(content: str, week_start: str = None, week_end: str = None) -> dict:
    """保存周报"""
    try:
        history_dir = get_history_dir()
        
        # 如果没有指定日期，使用当前周
        if not week_start:
            now = datetime.now()
            monday = now - datetime.timedelta(days=now.weekday())
            week_start = monday.strftime("%Y-%m-%d")
            week_end = (monday + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        
        # 文件名：2026-03-16_2026-03-22.md
        filename = f"{week_start}_{week_end}.md"
        filepath = history_dir / filename
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 同时保存JSON元数据
        meta_file = history_dir / "metadata.json"
        metadata = {}
        if meta_file.exists():
            with open(meta_file, encoding='utf-8') as f:
                metadata = json.load(f)
        
        metadata[filename] = {
            "week_start": week_start,
            "week_end": week_end,
            "saved_at": datetime.now().isoformat(),
            "filename": filename
        }
        
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return {"success": True, "path": str(filepath)}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_reports(limit: int = 10) -> dict:
    """列出历史周报"""
    try:
        history_dir = get_history_dir()
        meta_file = history_dir / "metadata.json"
        
        if not meta_file.exists():
            return {"success": True, "reports": []}
        
        with open(meta_file, encoding='utf-8') as f:
            metadata = json.load(f)
        
        # 转换为列表并排序
        reports = list(metadata.values())
        reports.sort(key=lambda x: x["week_start"], reverse=True)
        
        return {
            "success": True,
            "reports": reports[:limit]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_report(week_start: str = None, week_end: str = None) -> dict:
    """获取指定周的周报"""
    try:
        history_dir = get_history_dir()
        
        if week_start and week_end:
            filename = f"{week_start}_{week_end}.md"
        else:
            # 默认获取本周
            now = datetime.now()
            monday = now - datetime.timedelta(days=now.weekday())
            week_start = monday.strftime("%Y-%m-%d")
            week_end = (monday + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
            filename = f"{week_start}_{week_end}.md"
        
        filepath = history_dir / filename
        
        if not filepath.exists():
            return {"success": False, "error": "周报不存在"}
        
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "content": content,
            "week_start": week_start,
            "week_end": week_end
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_report(week_start: str, week_end: str) -> dict:
    """删除周报"""
    try:
        history_dir = get_history_dir()
        filename = f"{week_start}_{week_end}.md"
        filepath = history_dir / filename
        
        if filepath.exists():
            filepath.unlink()
        
        # 更新metadata
        meta_file = history_dir / "metadata.json"
        if meta_file.exists():
            with open(meta_file, encoding='utf-8') as f:
                metadata = json.load(f)
            
            if filename in metadata:
                del metadata[filename]
            
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return {"success": True}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="历史周报管理")
    parser.add_argument("--action", choices=["save", "list", "get", "delete"], required=True)
    parser.add_argument("--week-start", help="周开始日期")
    parser.add_argument("--week-end", help="周结束日期")
    parser.add_argument("--content", help="周报内容（save时使用）")
    parser.add_argument("--limit", type=int, default=10, help="列出数量")
    
    args = parser.parse_args()
    
    if args.action == "save":
        result = save_report(args.content, args.week_start, args.week_end)
    elif args.action == "list":
        result = list_reports(args.limit)
    elif args.action == "get":
        result = get_report(args.week_start, args.week_end)
    else:
        result = delete_report(args.week_start, args.week_end)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
