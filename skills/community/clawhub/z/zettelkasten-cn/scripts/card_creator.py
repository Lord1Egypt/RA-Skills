#!/usr/bin/env python3
"""
Zettelkasten Interactive Card Creator - 交互式卡片创建器
流程化的卡片创建流程：输入 -> 处理 -> 输出
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List

# 配置 - 支持环境变量覆盖
SKILL_DIR = Path(os.environ.get("ZETTELKASTEN_SKILL_DIR", ".")).resolve()
SCRIPT_DIR = SKILL_DIR / "scripts"
CARDS_DIR = Path(os.environ.get("ZETTELKASTEN_CARDS_DIR", "~/Desktop/cardsdata")).expanduser()

# 九大领域分类
CATEGORIES = ["身心", "学习", "投资", "家庭", "事业", "社交", "物品", "爱好", "体验"]

# 笔记类型
NOTE_TYPES = {
    "1": ("fleeting", "闪念笔记", "快速记录想法，临时存储"),
    "2": ("literature", "文献笔记", "阅读笔记，保留出处"),
    "3": ("permanent", "永久笔记", "核心知识，永久保存"),
    "4": ("project", "项目笔记", "特定项目相关"),
    "5": ("map", "主题地图", "索引和组织入口")
}

class CardCreationWorkflow:
    """卡片创建工作流"""
    
    def __init__(self):
        self.data = {
            "type": None,
            "title": None,
            "content": None,
            "category": None,  # 仅 permanent
            "tags": [],
            "source": None,
            "source_type": None,  # 仅 literature
            "source_title": None,
            "author": None,
            "goal": None,  # 仅 project
            "deadline": None,
            "memory_date": None,
            "context": ""
        }
        self.result = None
    
    def run(self) -> Dict[str, Any]:
        """运行完整流程"""
        print("=" * 60)
        print("📝 卡片创建流程")
        print("=" * 60)
        
        # 阶段1：输入
        self._phase_input()
        
        # 阶段2：处理
        self._phase_process()
        
        # 阶段3：输出
        return self._phase_output()
    
    def _phase_input(self):
        """阶段1：输入 - 收集信息"""
        print("\n📥 阶段1：输入")
        print("-" * 60)
        
        # 选择笔记类型
        print("\n选择笔记类型：")
        for key, (type_id, name, desc) in NOTE_TYPES.items():
            print(f"  {key}. {name} - {desc}")
        
        while True:
            choice = input("\n请选择 (1-5): ").strip()
            if choice in NOTE_TYPES:
                self.data["type"] = NOTE_TYPES[choice][0]
                print(f"✓ 已选择: {NOTE_TYPES[choice][1]}")
                break
            print("❌ 无效选择，请重试")
        
        # 输入标题
        while True:
            title = input("\n📝 笔记标题: ").strip()
            if title:
                self.data["title"] = title
                break
            print("❌ 标题不能为空")
        
        # 输入内容
        print("\n📄 笔记内容（输入空行结束）：")
        lines = []
        while True:
            line = input()
            if line.strip() == "" and lines:
                break
            lines.append(line)
        self.data["content"] = "\n".join(lines)
        
        # 永久笔记需要选择分类
        if self.data["type"] == "permanent":
            print("\n选择分类（九大领域）：")
            for i, cat in enumerate(CATEGORIES, 1):
                print(f"  {i}. {cat}")
            
            while True:
                cat_choice = input("\n请选择 (1-9): ").strip()
                if cat_choice.isdigit() and 1 <= int(cat_choice) <= 9:
                    self.data["category"] = CATEGORIES[int(cat_choice) - 1]
                    print(f"✓ 已选择: {self.data['category']}")
                    break
                print("❌ 无效选择，请重试")
        
        # 文献笔记需要额外信息
        if self.data["type"] == "literature":
            print("\n📚 文献信息：")
            self.data["source_type"] = input("  类型 (book/article/video): ").strip()
            self.data["source_title"] = input("  原标题: ").strip()
            self.data["author"] = input("  作者: ").strip()
        
        # 项目笔记需要目标
        if self.data["type"] == "project":
            self.data["goal"] = input("\n🎯 项目目标: ").strip()
            self.data["deadline"] = input("📅 截止日期 (可选): ").strip()
        
        # 标签
        tags_input = input("\n🏷️  标签（逗号分隔，可选）: ").strip()
        if tags_input:
            self.data["tags"] = [t.strip() for t in tags_input.split(",")]
        
        # 关联记忆
        self.data["memory_date"] = input("\n🔗 关联记忆日期 (YYYY-MM-DD，可选）: ").strip()
        if self.data["memory_date"]:
            self.data["context"] = input("  上下文描述: ").strip()
    
    def _phase_process(self):
        """阶段2：处理 - 构建命令并执行"""
        print("\n⚙️  阶段2：处理")
        print("-" * 60)
        
        # 构建命令
        cmd = ["python3", str(SCRIPT_DIR / "card_manager.py"), "create"]
        cmd.append(self.data["type"])
        cmd.append(self.data["title"])
        
        if self.data["content"]:
            cmd.extend(["--content", self.data["content"]])
        
        if self.data["tags"]:
            cmd.extend(["--tags", ",".join(self.data["tags"])])
        
        if self.data["category"]:
            cmd.extend(["--category", self.data["category"]])
        
        if self.data["memory_date"]:
            cmd.extend(["--memory", self.data["memory_date"]])
        
        print(f"\n执行命令: {' '.join(cmd[:5])}...")
        
        # 执行命令
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(SKILL_DIR)
            )
            
            if result.returncode == 0:
                self.result = json.loads(result.stdout)
                
                # 记录操作到历史
                self._log_operation()
                
                print("✓ 卡片创建成功")
            else:
                print(f"❌ 创建失败: {result.stderr}")
                self.result = {"error": result.stderr}
        
        except Exception as e:
            print(f"❌ 执行错误: {e}")
            self.result = {"error": str(e)}
    
    def _phase_output(self) -> Dict[str, Any]:
        """阶段3：输出 - 展示结果"""
        print("\n📤 阶段3：输出")
        print("-" * 60)
        
        if self.result and "id" in self.result:
            print(f"\n✅ 创建成功！")
            print(f"\n📋 卡片信息：")
            print(f"  ID: {self.result['id']}")
            print(f"  类型: {self.result['type']}")
            print(f"  标题: {self.result['title']}")
            print(f"  路径: {self.result['path']}")
            print(f"  创建时间: {self.result['created']}")
            
            if self.data["category"]:
                print(f"  分类: {self.data['category']}")
            
            if self.data["memory_date"]:
                print(f"  关联记忆: {self.data['memory_date']}")
            
            print(f"\n💡 后续操作：")
            print(f"  - 查看: python scripts/card_manager.py read {self.result['id']}")
            print(f"  - 撤销: python scripts/undo_manager.py undo")
            print(f"  - 关联: python scripts/card_manager.py link {self.result['id']} <other_id>")
        
        else:
            print("\n❌ 创建失败")
            if self.result and "error" in self.result:
                print(f"错误: {self.result['error']}")
        
        return self.result
    
    def _log_operation(self):
        """记录操作到撤销历史"""
        try:
            if self.result and "path" in self.result:
                cmd = [
                    "python3",
                    str(SCRIPT_DIR / "undo_manager.py"),
                    "log",
                    "create",
                    "--details",
                    json.dumps({
                        "id": self.result["id"],
                        "type": self.result["type"],
                        "title": self.result["title"],
                        "path": self.result["path"]
                    }, ensure_ascii=False)
                ]
                subprocess.run(cmd, capture_output=True, cwd=str(SKILL_DIR))
        except:
            pass  # 记录失败不影响主流程


def quick_create(title: str, content: str, note_type: str = "permanent", 
                 category: Optional[str] = None, memory_date: Optional[str] = None) -> Dict[str, Any]:
    """
    快速创建卡片（非交互式）
    
    Args:
        title: 标题
        content: 内容
        note_type: 笔记类型
        category: 分类（仅 permanent）
        memory_date: 关联记忆日期
    
    Returns:
        创建结果
    """
    cmd = [
        "python3",
        str(SCRIPT_DIR / "card_manager.py"),
        "create",
        note_type,
        title,
        "--content", content
    ]
    
    if category:
        cmd.extend(["--category", category])
    
    if memory_date:
        cmd.extend(["--memory", memory_date])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(SKILL_DIR)
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr}
    
    except Exception as e:
        return {"error": str(e)}


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="交互式卡片创建器")
    parser.add_argument("--quick", "-q", action="store_true", help="快速模式（非交互）")
    parser.add_argument("--title", "-t", help="标题")
    parser.add_argument("--content", "-c", help="内容")
    parser.add_argument("--type", choices=["fleeting", "literature", "permanent", "project", "map"], 
                        default="permanent", help="笔记类型")
    parser.add_argument("--category", choices=CATEGORIES, help="分类（仅 permanent）")
    parser.add_argument("--memory", "-m", help="关联记忆日期")
    
    args = parser.parse_args()
    
    if args.quick:
        # 快速模式
        if not args.title or not args.content:
            print("❌ 快速模式需要提供 --title 和 --content")
            sys.exit(1)
        
        result = quick_create(
            title=args.title,
            content=args.content,
            note_type=args.type,
            category=args.category,
            memory_date=args.memory
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        # 交互模式
        workflow = CardCreationWorkflow()
        result = workflow.run()
        
        if result and "error" in result:
            sys.exit(1)


if __name__ == "__main__":
    main()
