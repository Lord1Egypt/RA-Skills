#!/usr/bin/env python3
"""
工作日计算器使用示例
展示各种使用场景和功能
"""

import subprocess
import json
import sys
from datetime import date, datetime

def run_command(cmd):
    """运行命令并返回结果"""
    print(f"\n🚀 运行命令: {cmd}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ 命令执行失败: {result.stderr}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False

def demo_basic_usage():
    """演示基本使用"""
    print("\n" + "="*60)
    print("📋 基本使用示例")
    print("="*60)
    
    examples = [
        ("2025年1月工作日", "python3 workday_calculator.py 2025-01-01 2025-01-31"),
        ("2026年春节月份", "python3 workday_calculator.py 2026-02-01 2026-02-28"),
        ("2025年一整年", "python3 workday_calculator.py 2025-01-01 2025-12-31"),
        ("跨越两年的计算", "python3 workday_calculator.py 2025-12-01 2026-01-15"),
    ]
    
    for name, cmd in examples:
        print(f"\n📅 {name}:")
        run_command(cmd)

def demo_detailed_view():
    """演示详细信息查看"""
    print("\n" + "="*60)
    print("🔍 详细信息查看示例")
    print("="*60)
    
    examples = [
        ("2026年元旦期间", "python3 workday_calculator.py 2026-01-01 2026-01-10 --details"),
        ("2026年劳动节期间", "python3 workday_calculator.py 2026-04-25 2026-05-10 --details"),
        ("2026年国庆节期间", "python3 workday_calculator.py 2026-09-25 2026-10-10 --details"),
    ]
    
    for name, cmd in examples:
        print(f"\n📅 {name}:")
        run_command(cmd)

def demo_export_function():
    """演示导出功能"""
    print("\n" + "="*60)
    print("💾 导出功能示例")
    print("="*60)
    
    examples = [
        ("导出2025年3月数据", "python3 workday_calculator.py 2025-03-01 2025-03-31 --details --export march_2025.json"),
        ("导出2026年第一季度", "python3 workday_calculator.py 2026-01-01 2026-03-31 --details --export q1_2026.json"),
    ]
    
    for name, cmd in examples:
        print(f"\n📅 {name}:")
        if run_command(cmd):
            # 如果是导出命令，显示导出文件内容
            if "--export" in cmd:
                export_file = cmd.split()[-1]
                try:
                    with open(export_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"\n📄 导出文件 {export_file} 内容摘要:")
                    print(f"  时间区间: {data['start_date']} 到 {data['end_date']}")
                    print(f"  总天数: {data['total_days']}")
                    print(f"  工作日数量: {data['workday_count']}")
                    print(f"  生成时间: {data['generated_at']}")
                except Exception as e:
                    print(f"❌ 读取导出文件失败: {e}")

def demo_update_tool():
    """演示更新工具使用"""
    print("\n" + "="*60)
    print("🔄 节假日更新工具")
    print("="*60)
    
    print("\n💡 运行节假日更新工具:")
    print("python3 update_holidays.py")
    
    print("\n📋 主要功能:")
    print("1. 查看当前节假日数据")
    print("2. 添加新的节假日")
    print("3. 添加调休工作日")
    print("4. 在线搜索节假日信息")
    print("5. 生成Python代码")
    
    print("\n⚠️  注意:")
    print("- 节假日数据需要每年更新")
    print("- 最权威的信息来源是中国政府网 (www.gov.cn)")
    print("- 注意验证日期的准确性")

def demo_as_python_module():
    """演示作为Python模块使用"""
    print("\n" + "="*60)
    print("🐍 作为Python模块使用")
    print("="*60)
    
    python_code = '''
from workday_calculator import WorkdayCalculator
from datetime import date

# 创建计算器实例
calculator = WorkdayCalculator()

# 计算工作日数量
start_date = date(2025, 1, 1)
end_date = date(2025, 1, 31)
workdays = calculator.calculate_workdays(start_date, end_date)
print(f"2025年1月工作日数量: {workdays}")

# 获取详细信息
details = calculator.get_workday_details(date(2026, 2, 1), date(2026, 2, 28))
print(f"2026年2月总天数: {details['total_days']}")
print(f"2026年2月工作日: {details['workday_count']}")

# 添加自定义节假日
calculator.add_holiday(date(2025, 12, 25), "圣诞节")
calculator.add_extra_workday(date(2025, 12, 27), "公司团建")
'''
    
    print("💡 示例代码:")
    print(python_code)

def show_help():
    """显示帮助信息"""
    print("\n" + "="*60)
    print("❓ 工作日计算器帮助信息")
    print("="*60)
    
    print("\n📋 主要脚本:")
    print("1. workday_calculator.py - 主程序")
    print("   python3 workday_calculator.py <开始日期> <结束日期>")
    print("   python3 workday_calculator.py 2025-01-01 2025-01-31 --details")
    
    print("\n2. update_holidays.py - 节假日更新工具")
    print("   python3 update_holidays.py")
    
    print("\n3. example_usage.py - 使用示例")
    print("   python3 example_usage.py")
    
    print("\n📅 日期格式:")
    print("必须使用 YYYY-MM-DD 格式")
    print("例如: 2025-01-01, 2026-12-31")
    
    print("\n⚙️  命令行选项:")
    print("  --details    显示详细信息")
    print("  --export     导出到JSON文件")
    print("  --version    显示版本信息")
    
    print("\n💡 使用技巧:")
    print("- 节假日数据每年需要更新")
    print("- 导出功能可用于数据分析和报告")
    print("- 可以作为Python模块集成到其他应用中")

def main():
    """主函数"""
    print("="*60)
    print("📅 工作日计算器 - 使用示例")
    print("="*60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "help":
            show_help()
            return
    
    print("\n📋 选择演示功能:")
    print("1. 基本使用示例")
    print("2. 详细信息查看")
    print("3. 导出功能演示")
    print("4. 节假日更新工具")
    print("5. Python模块使用")
    print("6. 查看帮助信息")
    print("7. 全部演示")
    print("8. 退出")
    
    choice = input("\n请选择 (1-8): ").strip()
    
    if choice == '1':
        demo_basic_usage()
    elif choice == '2':
        demo_detailed_view()
    elif choice == '3':
        demo_export_function()
    elif choice == '4':
        demo_update_tool()
    elif choice == '5':
        demo_as_python_module()
    elif choice == '6':
        show_help()
    elif choice == '7':
        demo_basic_usage()
        demo_detailed_view()
        demo_export_function()
        demo_update_tool()
        demo_as_python_module()
        show_help()
    elif choice == '8':
        print("\n👋 退出示例程序")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()