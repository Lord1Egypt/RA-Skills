"""
使用示例：表格处理
"""

import asyncio
import base64
import pandas as pd
from io import BytesIO
from main import execute


async def example_clean_data():
    """示例：数据清洗"""
    df = pd.DataFrame({
        '姓名': ['张三', '李四', '张三', '王五', '赵六', None],
        '年龄': [25, 30, 25, 35, None, 28],
        '销售额': [10000, 15000, 10000, 20000, 12000, 50000],
        '部门': ['销售部', '市场部', '销售部', '技术部', '市场部', '销售部']
    })
    
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_data = base64.b64encode(excel_buffer.getvalue()).decode('utf-8')
    
    params = {
        "action": "清洗数据",
        "action_type": "clean_data",
        "data": excel_data,
        "remove_duplicates": True,
        "handle_missing": "mean",
        "remove_outliers": True,
        "outlier_method": "iqr"
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        print(f"  原始行数: {result['data']['original_rows']}")
        print(f"  清洗后行数: {result['data']['cleaned_rows']}")
        print(f"  删除重复项: {result['data']['duplicates_removed']}")
        print(f"  处理缺失值: {result['data']['missing_values_handled']}")
        print(f"  移除异常值: {result['data']['outliers_removed']}")
        
        file_data = base64.b64decode(result["file_data"])
        with open("清洗后数据.xlsx", "wb") as f:
            f.write(file_data)


async def example_analyze_data():
    """示例：数据分析"""
    df = pd.DataFrame({
        '地区': ['华东', '华北', '华东', '华南', '华北', '华东', '华南', '华北'],
        '销售额': [100000, 80000, 120000, 90000, 85000, 110000, 95000, 88000],
        '成本': [60000, 50000, 70000, 55000, 52000, 65000, 58000, 53000],
        '利润': [40000, 30000, 50000, 35000, 33000, 45000, 37000, 35000]
    })
    
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_data = base64.b64encode(excel_buffer.getvalue()).decode('utf-8')
    
    params = {
        "action": "分析表格",
        "action_type": "analyze_data",
        "analysis_type": "sum",
        "data": excel_data,
        "columns": ["销售额", "成本", "利润"],
        "group_by": "地区"
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        print("\n分析结果:")
        for region, values in result['data']['data'].items():
            print(f"\n{region}:")
            for metric, value in values.items():
                print(f"  {metric}: {value:,.2f}")


async def example_generate_chart():
    """示例：图表生成"""
    df = pd.DataFrame({
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '销售额': [100000, 120000, 110000, 130000, 125000, 140000],
        '成本': [60000, 70000, 65000, 75000, 72000, 80000],
        '利润': [40000, 50000, 45000, 55000, 53000, 60000]
    })
    
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_data = base64.b64encode(excel_buffer.getvalue()).decode('utf-8')
    
    params = {
        "action": "生成柱状图",
        "action_type": "generate_chart",
        "chart_type": "bar",
        "data": excel_data,
        "x_column": "月份",
        "y_columns": ["销售额", "成本", "利润"],
        "title": "2026年上半年销售分析"
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        
        file_data = base64.b64decode(result["file_data"])
        with open("销售分析图表.xlsx", "wb") as f:
            f.write(file_data)
        print(f"✓ 图表已保存")


async def example_smart_analysis():
    """示例：自然语言智能分析"""
    df = pd.DataFrame({
        '产品': ['产品A', '产品B', '产品C', '产品D', '产品E'],
        '销量': [1000, 1500, 800, 2000, 1200],
        '单价': [100, 80, 120, 90, 110],
        '销售额': [100000, 120000, 96000, 180000, 132000]
    })
    
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_data = base64.b64encode(excel_buffer.getvalue()).decode('utf-8')
    
    params = {
        "action": "计算销售额的总和",
        "action_type": "analyze_data",
        "analysis_type": "sum",
        "data": excel_data,
        "columns": ["销售额"]
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        print(f"销售额总和: {result['data']['data']['销售额']:,.2f}")


async def main():
    """运行所有示例"""
    print("=" * 60)
    print("示例1: 数据清洗")
    print("=" * 60)
    await example_clean_data()
    
    print("\n" + "=" * 60)
    print("示例2: 数据分析")
    print("=" * 60)
    await example_analyze_data()
    
    print("\n" + "=" * 60)
    print("示例3: 图表生成")
    print("=" * 60)
    await example_generate_chart()
    
    print("\n" + "=" * 60)
    print("示例4: 智能分析")
    print("=" * 60)
    await example_smart_analysis()


if __name__ == "__main__":
    asyncio.run(main())
