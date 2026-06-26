#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-Improving Enhancement - 完整聊天记录工具
记录所有聊天内容（文字 + 图片），防止重启后丢失

功能:
- 记录所有文字对话
- 记录图片引用（不存储图片文件本身，只存路径和描述）
- 按日期分文件存储
- 自动压缩旧记录
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import hashlib

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class ChatLogger:
    """完整聊天记录器"""
    
    def __init__(self):
        self.base_dir = Path.home() / "self-improving" / "chat-logs"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.today_file = self.base_dir / f"{self.today}.jsonl"
        self.index_file = self.base_dir / "index.json"
        self.load_index()
    
    def load_index(self):
        """加载索引"""
        if self.index_file.exists():
            try:
                self.index = json.loads(self.index_file.read_text(encoding='utf-8'))
            except:
                self.index = {"days": [], "total_messages": 0, "total_images": 0}
        else:
            self.index = {"days": [], "total_messages": 0, "total_images": 0}
    
    def save_index(self):
        """保存索引"""
        self.index_file.write_text(
            json.dumps(self.index, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    def log_message(self, role: str, content: str, metadata: dict = None):
        """
        记录消息
        
        Args:
            role: 'user' 或 'assistant'
            content: 消息内容
            metadata: 额外信息（图片、文件等）
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        
        # 写入今日文件
        with open(self.today_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # 更新索引
        self.index["total_messages"] += 1
        if metadata and metadata.get("type") == "image":
            self.index["total_images"] += 1
        
        if self.today not in self.index["days"]:
            self.index["days"].append(self.today)
        
        self.save_index()
        print(f"[✓] 已记录 {role} 消息")
    
    def log_image(self, image_path: str, description: str = "", context: str = ""):
        """
        记录图片（只记录路径和描述，不存储文件）
        
        Args:
            image_path: 图片文件路径
            description: 图片描述
            context: 上下文信息
        """
        metadata = {
            "type": "image",
            "path": str(image_path),
            "description": description,
            "context": context,
            "hash": self._file_hash(image_path)
        }
        
        self.log_message(
            role="system",
            content=f"[图片记录] {description}",
            metadata=metadata
        )
        print(f"[✓] 已记录图片：{image_path}")
    
    def _file_hash(self, file_path: str) -> str:
        """计算文件哈希"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def get_today_messages(self) -> list:
        """获取今天的消息"""
        if not self.today_file.exists():
            return []
        
        messages = []
        with open(self.today_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    messages.append(json.loads(line))
                except:
                    continue
        return messages
    
    def get_messages_by_date(self, date: str) -> list:
        """获取指定日期的消息"""
        file_path = self.base_dir / f"{date}.jsonl"
        if not file_path.exists():
            return []
        
        messages = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    messages.append(json.loads(line))
                except:
                    continue
        return messages
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "total_days": len(self.index["days"]),
            "total_messages": self.index["total_messages"],
            "total_images": self.index["total_images"],
            "today_messages": len(self.get_today_messages())
        }
    
    def cleanup_old_logs(self, keep_days: int = 30, auto_confirm: bool = False, specific_dates: list = None):
        """
        清理旧记录（保留最近 N 天）
        
        Args:
            keep_days: 保留天数（默认 30 天，30 天内的不会清理）
            auto_confirm: 是否自动确认（默认 False，需要用户确认）
            specific_dates: 指定清理的日期列表（用户明确指定的）
        """
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=keep_days)
        to_remove = []
        
        # 如果有指定日期，只清理指定的（但必须超过 30 天）
        if specific_dates:
            for day in specific_dates:
                if day not in self.index["days"]:
                    print(f"[!] 日期 {day} 没有聊天记录")
                    continue
                
                try:
                    day_date = datetime.strptime(day, "%Y-%m-%d")
                    if day_date < cutoff:
                        file_path = self.base_dir / f"{day}.jsonl"
                        if file_path.exists():
                            msg_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
                            to_remove.append({
                                "date": day,
                                "file": str(file_path),
                                "messages": msg_count
                            })
                    else:
                        print(f"[!] 日期 {day} 的记录在 {keep_days} 天内，不能清理（保护近期记录）")
                except:
                    continue
        else:
            # 默认清理所有超过 keep_days 的记录
            for day in self.index["days"][:]:
                try:
                    day_date = datetime.strptime(day, "%Y-%m-%d")
                    if day_date < cutoff:
                        file_path = self.base_dir / f"{day}.jsonl"
                        if file_path.exists():
                            msg_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
                            to_remove.append({
                                "date": day,
                                "file": str(file_path),
                                "messages": msg_count
                            })
                except:
                    continue
        
        if not to_remove:
            print(f"[✓] 没有需要清理的旧记录（保留最近 {keep_days} 天）")
            return
        
        # 显示清理预览
        print("\n🗑️  发现可清理的旧记录")
        print("=" * 60)
        print(f"保留最近 {keep_days} 天的记录，以下记录将被清理：\n")
        
        total_messages = 0
        for item in to_remove:
            print(f"  📅 {item['date']} - {item['messages']} 条消息")
            total_messages += item['messages']
        
        print(f"\n共计：{len(to_remove)} 天，{total_messages} 条消息")
        print("=" * 60)
        
        # 询问确认
        if not auto_confirm:
            print("\n⚠️  清理后无法恢复，确认要清理吗？")
            response = input("输入 'yes' 确认清理，其他取消：").strip().lower()
            if response != 'yes':
                print("[✗] 已取消清理操作")
                return
        
        # 执行清理
        removed = 0
        for item in to_remove:
            try:
                Path(item['file']).unlink()
                self.index["days"].remove(item['date'])
                removed += 1
            except:
                continue
        
        self.save_index()
        print(f"\n[✓] 已清理 {removed} 天的旧记录（共 {total_messages} 条消息）")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="完整聊天记录工具")
    parser.add_argument("action", choices=["log", "stats", "cleanup", "view"],
                       help="操作类型")
    parser.add_argument("--role", default="user", help="消息角色")
    parser.add_argument("--content", default="", help="消息内容")
    parser.add_argument("--image", help="图片路径")
    parser.add_argument("--desc", help="图片描述")
    parser.add_argument("--date", help="查看日期 (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=30, help="保留天数")
    parser.add_argument("--auto", action="store_true", help="自动确认，不询问")
    
    args = parser.parse_args()
    logger = ChatLogger()
    
    if args.action == "log":
        if args.image:
            logger.log_image(args.image, args.desc or "", args.content or "")
        else:
            logger.log_message(args.role, args.content or "")
    
    elif args.action == "stats":
        stats = logger.get_stats()
        print("\n📊 聊天记录统计")
        print("=" * 40)
        print(f"总天数：{stats['total_days']}")
        print(f"总消息数：{stats['total_messages']}")
        print(f"总图片数：{stats['total_images']}")
        print(f"今日消息：{stats['today_messages']}")
        print()
    
    elif args.action == "cleanup":
        # 解析指定日期
        dates = None
        if args.date:
            dates = [d.strip() for d in args.date.split(',')]
        logger.cleanup_old_logs(args.days, auto_confirm=args.auto, specific_dates=dates)
    
    elif args.action == "view":
        if args.date:
            messages = logger.get_messages_by_date(args.date)
        else:
            messages = logger.get_today_messages()
        
        print(f"\n📝 聊天记录 ({len(messages)} 条)")
        print("=" * 40)
        for msg in messages[:20]:  # 只显示前 20 条
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:100]
            ts = msg.get("timestamp", "")[:19]
            print(f"[{ts}] {role}: {content}...")
        if len(messages) > 20:
            print(f"... 还有 {len(messages) - 20} 条")
        print()


if __name__ == "__main__":
    main()
