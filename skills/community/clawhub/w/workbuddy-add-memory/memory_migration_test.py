#!/usr/bin/env python3
"""
记忆迁移测试脚本
将记忆从旧系统迁移到新版本workbuddy-add-memory技能
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

def check_memory_sources():
    """检查记忆源目录"""
    print("🔍 检查记忆源目录...")
    
    # 全局记忆目录
    global_memory_dir = Path.home() / ".workbuddy" / "unified_memory"
    
    # 检查目录是否存在
    if not global_memory_dir.exists():
        print(f"❌ 全局记忆目录不存在: {global_memory_dir}")
        return False
    
    print(f"✅ 找到全局记忆目录: {global_memory_dir}")
    
    # 检查目录内容
    memory_files = list(global_memory_dir.glob("*.json"))
    print(f"   找到 {len(memory_files)} 个记忆JSON文件")
    
    # 检查记忆索引
    index_file = global_memory_dir / "memory_index.json"
    if index_file.exists():
        print(f"✅ 找到记忆索引文件: {index_file}")
        with open(index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
            print(f"   索引包含 {len(index_data.get('knowledge_points', []))} 个知识要点")
    else:
        print(f"⚠️  未找到记忆索引文件")
    
    return True

def check_skill_memory_system():
    """检查技能记忆系统"""
    print("\n🔍 检查技能记忆系统...")
    
    # 当前工作空间技能目录
    skill_dir = Path(__file__).parent
    
    # 检查技能核心文件
    required_files = [
        "memory_retriever.py",
        "config_loader.py", 
        "start_work.py",
        "work_preparation.py"
    ]
    
    for file in required_files:
        file_path = skill_dir / file
        if file_path.exists():
            print(f"✅ 找到技能文件: {file}")
        else:
            print(f"❌ 缺少技能文件: {file}")
            return False
    
    return True

def test_memory_retrieval():
    """测试记忆检索功能"""
    print("\n🧠 测试记忆检索功能...")
    
    try:
        from memory_retriever import MemoryRetriever
        from config_loader import config_loader
        
        print("✅ 成功导入技能模块")
        
        # 初始化检索器
        mr = MemoryRetriever()
        print("✅ 记忆检索器初始化成功")
        
        # 获取记忆源
        memory_sources = config_loader.get_memory_sources()
        print(f"✅ 获取到 {len(memory_sources)} 个记忆源")
        
        # 加载记忆
        memory_count = mr.load_memories(memory_sources)
        print(f"✅ 加载了 {memory_count} 个记忆")
        
        # 测试检索
        test_queries = [
            "workbuddy-add-memory",
            "技能安装",
            "记忆系统",
            "Excel处理"
        ]
        
        print("\n📊 测试记忆检索结果:")
        for query in test_queries:
            results = mr.search(query, top_k=3)
            print(f"  🔍 '{query}': 找到 {len(results)} 条相关记忆")
            for i, result in enumerate(results[:2], 1):
                # 检查结果格式
                if isinstance(result, dict):
                    title = result.get('title', '无标题')
                else:
                    title = str(result)[:50]
                print(f"     {i}. {title[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 记忆检索测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_migration_summary():
    """创建迁移总结报告"""
    print("\n📋 创建迁移总结报告...")
    
    summary = {
        "migration_time": datetime.now().isoformat(),
        "skill_version": "v3.0",
        "skill_author": "zcg007",
        "workspace": str(Path(__file__).parent),
        "tests": {
            "memory_sources_check": False,
            "skill_system_check": False,
            "memory_retrieval_test": False
        },
        "migration_status": "pending"
    }
    
    # 运行测试
    summary["tests"]["memory_sources_check"] = check_memory_sources()
    summary["tests"]["skill_system_check"] = check_skill_memory_system()
    summary["tests"]["memory_retrieval_test"] = test_memory_retrieval()
    
    # 确定迁移状态
    all_tests_passed = all(summary["tests"].values())
    summary["migration_status"] = "completed" if all_tests_passed else "failed"
    
    # 保存总结
    summary_file = Path(__file__).parent / "memory_migration_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 迁移总结已保存到: {summary_file}")
    
    # 创建Markdown报告
    md_file = Path(__file__).parent / "MEMORY_MIGRATION_REPORT.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"""# 记忆迁移测试报告

## 迁移信息
- **迁移时间**: {summary['migration_time']}
- **技能版本**: {summary['skill_version']}
- **技能作者**: {summary['skill_author']}
- **工作空间**: {summary['workspace']}
- **迁移状态**: **{summary['migration_status'].upper()}**

## 测试结果

### 1. 记忆源检查
状态: {'✅ 通过' if summary['tests']['memory_sources_check'] else '❌ 失败'}

### 2. 技能系统检查  
状态: {'✅ 通过' if summary['tests']['skill_system_check'] else '❌ 失败'}

### 3. 记忆检索测试
状态: {'✅ 通过' if summary['tests']['memory_retrieval_test'] else '❌ 失败'}

## 总体评估
{'🎉 **所有测试通过！记忆迁移成功完成！**' if all_tests_passed else '⚠️ **部分测试失败，需要检查问题**'}

## 下一步
1. 使用新版本技能开始工作:
   ```bash
   python start_work.py "您的任务描述"
   ```

2. 验证记忆检索功能正常

3. 如有问题，检查日志文件: `workbuddy_add_memory.log`
""")
    
    print(f"✅ Markdown报告已保存到: {md_file}")
    
    return summary

def main():
    """主函数"""
    print("=" * 60)
    print("🧠 记忆迁移测试开始")
    print("=" * 60)
    
    # 创建迁移总结
    summary = create_migration_summary()
    
    print("\n" + "=" * 60)
    print("📊 迁移测试完成")
    print("=" * 60)
    
    # 显示结果
    if summary["migration_status"] == "completed":
        print("🎉 恭喜！记忆迁移测试全部通过！")
        print(f"   迁移时间: {summary['migration_time']}")
        print(f"   技能版本: {summary['skill_version']}")
        print(f"   技能作者: {summary['skill_author']}")
    else:
        print("⚠️  记忆迁移测试失败，请检查问题")
        failed_tests = [k for k, v in summary["tests"].items() if not v]
        print(f"   失败的测试: {', '.join(failed_tests)}")
    
    print(f"\n📁 报告文件:")
    print(f"   JSON总结: {Path(__file__).parent / 'memory_migration_summary.json'}")
    print(f"   Markdown报告: {Path(__file__).parent / 'MEMORY_MIGRATION_REPORT.md'}")

if __name__ == "__main__":
    main()