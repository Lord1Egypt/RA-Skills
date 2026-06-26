#!/usr/bin/env python3
"""
示例：使用 Code Analyzer 分析代码
"""

from analyzer import CodeAnalyzer

# 示例代码 - 包含多个问题
sample_code = '''
def get_data(url):
    import requests
    API_KEY = "sk-1234567890abcdef"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None
'''

# 保存到临时文件
with open('/tmp/sample.py', 'w') as f:
    f.write(sample_code)

# 分析
analyzer = CodeAnalyzer()
result = analyzer.analyze_file('/tmp/sample.py')

# 打印报告
print(analyzer.generate_report(result))
print("\n" + "="*50)
print("按严重性分类的问题数量:")
print(f"  P0 (必须修复): {len(result.get_by_severity(__import__('analyzer').Severity.P0))}")
print(f"  P1 (重要): {len(result.get_by_severity(__import__('analyzer').Severity.P1))}")
print(f"  P2 (建议): {len(result.get_by_severity(__import__('analyzer').Severity.P2))}")
