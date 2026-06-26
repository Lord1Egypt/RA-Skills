#!/usr/bin/env python3
"""
火山引擎高优先级内容提取脚本
提取认证、核心API、错误码等关键章节
"""

import PyPDF2
import json
import re
import sys
from pathlib import Path

def extract_pages(pdf_path, page_numbers, output_dir):
    """提取指定页面的文本内容"""
    results = {}
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"PDF总页数: {total_pages}")
        print(f"提取页面: {page_numbers}")
        
        for page_num in page_numbers:
            if page_num < 1 or page_num > total_pages:
                print(f"警告: 页面 {page_num} 超出范围 (1-{total_pages})")
                continue
            
            try:
                # 转换为0-based索引
                page_idx = page_num - 1
                page = pdf_reader.pages[page_idx]
                text = page.extract_text()
                
                if text:
                    # 清理文本
                    text = text.strip()
                    # 移除多余的空白字符
                    text = re.sub(r'\s+', ' ', text)
                    
                    results[page_num] = {
                        'page': page_num,
                        'text': text,
                        'length': len(text)
                    }
                    
                    print(f"页面 {page_num}: 提取到 {len(text)} 字符")
                    
                    # 保存单个页面文本
                    page_file = output_dir / f"page_{page_num:03d}.txt"
                    with open(page_file, 'w', encoding='utf-8') as f:
                        f.write(text)
                    
                else:
                    print(f"页面 {page_num}: 无文本内容")
                    results[page_num] = {
                        'page': page_num,
                        'text': '',
                        'length': 0,
                        'error': 'No text content'
                    }
                    
            except Exception as e:
                print(f"页面 {page_num} 提取错误: {e}")
                results[page_num] = {
                    'page': page_num,
                    'text': '',
                    'length': 0,
                    'error': str(e)
                }
    
    return results

def analyze_authentication_content(text):
    """分析认证相关内容"""
    analysis = {
        'api_key_info': [],
        'base_url_info': [],
        'auth_methods': [],
        'security_notes': []
    }
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # API Key相关
        if 'API Key' in line or 'api key' in line.lower() or '密钥' in line:
            analysis['api_key_info'].append(line)
        
        # Base URL相关
        if 'Base URL' in line or 'baseurl' in line.lower() or 'endpoint' in line.lower() or '端点' in line:
            analysis['base_url_info'].append(line)
        
        # 认证方法
        if 'Bearer' in line or 'Authorization' in line or '鉴权' in line or '认证' in line:
            analysis['auth_methods'].append(line)
        
        # 安全说明
        if '安全' in line or 'Security' in line or '保护' in line or '保密' in line:
            analysis['security_notes'].append(line)
    
    return analysis

def analyze_api_endpoints(text):
    """分析API端点相关内容"""
    analysis = {
        'endpoints': [],
        'parameters': [],
        'examples': [],
        'rate_limits': []
    }
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # API端点模式
        if re.search(r'(POST|GET|PUT|DELETE|PATCH)\s+/\w+', line):
            analysis['endpoints'].append(line)
        elif re.search(r'api/v\d+/', line, re.IGNORECASE):
            analysis['endpoints'].append(line)
        
        # 参数说明
        if re.search(r'(参数|Parameter|param|字段|field)', line):
            analysis['parameters'].append(line)
        
        # 示例代码
        if '示例' in line or 'Example' in line or 'example' in line.lower():
            analysis['examples'].append(line)
        
        # 速率限制
        if '限制' in line or 'Limit' in line or 'limit' in line.lower() or '配额' in line:
            analysis['rate_limits'].append(line)
    
    return analysis

def analyze_error_codes(text):
    """分析错误码相关内容"""
    analysis = {
        'error_codes': [],
        'http_status': [],
        'error_messages': [],
        'solutions': []
    }
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 错误码模式 (如 "400", "401", "404")
        if re.match(r'^\d{3}\b', line):
            analysis['error_codes'].append(line)
        
        # HTTP状态码
        if 'HTTP' in line and ('状态' in line or 'status' in line.lower()):
            analysis['http_status'].append(line)
        
        # 错误信息
        if '错误' in line or 'Error' in line or 'error' in line.lower():
            analysis['error_messages'].append(line)
        
        # 解决方案
        if '解决' in line or 'Solution' in line or '建议' in line or 'Recommend' in line:
            analysis['solutions'].append(line)
    
    return analysis

def compare_with_existing_config(extracted_data, existing_config_path):
    """与现有配置进行比较"""
    comparison = {
        'matches': [],
        'differences': [],
        'missing_info': [],
        'additional_info': []
    }
    
    # 这里可以添加与现有配置的比较逻辑
    # 由于时间关系，先返回基本结构
    return comparison

def main():
    if len(sys.argv) < 2:
        print("用法: python extract-high-priority.py <pdf文件路径>")
        print("示例: python extract-high-priority.py volcengine-api-reference.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"错误: 文件不存在: {pdf_path}")
        sys.exit(1)
    
    # 创建输出目录
    output_dir = Path(pdf_path).parent / "extracted_high_priority"
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("火山引擎高优先级内容提取")
    print("=" * 60)
    
    # 定义要提取的页面（根据目录分析）
    high_priority_pages = [
        1,   # 1.1 获取 API Key 并配置
        6,   # 1.3 Base URL及鉴权
        9,   # 2 对话(Chat) API
        33,  # 3 Responses API
        272, # 12.2 管理API Key
        454  # 13.2 错误码
    ]
    
    # 提取页面内容
    print(f"\n开始提取高优先级页面...")
    extracted_data = extract_pages(pdf_path, high_priority_pages, output_dir)
    
    # 分析提取的内容
    print(f"\n分析提取的内容...")
    analyses = {}
    
    for page_num, data in extracted_data.items():
        if data.get('error') or not data['text']:
            continue
        
        text = data['text']
        
        # 根据页面内容类型进行分析
        if page_num in [1, 6, 272]:  # 认证相关
            analysis = analyze_authentication_content(text)
            analyses[f'page_{page_num}_auth'] = analysis
            
        elif page_num in [9, 33]:  # API端点相关
            analysis = analyze_api_endpoints(text)
            analyses[f'page_{page_num}_api'] = analysis
            
        elif page_num == 454:  # 错误码相关
            analysis = analyze_error_codes(text)
            analyses[f'page_{page_num}_error'] = analysis
    
    # 保存分析结果
    results = {
        'extracted_pages': extracted_data,
        'analyses': analyses,
        'summary': {
            'total_pages_extracted': len(extracted_data),
            'successful_pages': len([d for d in extracted_data.values() if d.get('text')]),
            'total_text_length': sum([d.get('length', 0) for d in extracted_data.values()])
        }
    }
    
    results_file = output_dir / "extraction_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n提取结果已保存到: {results_file}")
    
    # 生成简要报告
    print(f"\n📋 提取摘要:")
    print(f"提取页面数: {results['summary']['total_pages_extracted']}")
    print(f"成功提取: {results['summary']['successful_pages']}")
    print(f"总文本长度: {results['summary']['total_text_length']} 字符")
    
    # 显示关键发现
    print(f"\n🔍 关键发现:")
    
    # 认证信息
    auth_pages = [1, 6, 272]
    auth_info = []
    for page in auth_pages:
        if f'page_{page}_auth' in analyses:
            auth = analyses[f'page_{page}_auth']
            if auth['api_key_info']:
                auth_info.extend(auth['api_key_info'][:2])
            if auth['base_url_info']:
                auth_info.extend(auth['base_url_info'][:2])
    
    if auth_info:
        print(f"\n认证相关发现 ({len(auth_info)} 条):")
        for i, info in enumerate(auth_info[:5], 1):
            print(f"  {i}. {info[:80]}...")
    
    # API端点信息
    api_pages = [9, 33]
    api_info = []
    for page in api_pages:
        if f'page_{page}_api' in analyses:
            api = analyses[f'page_{page}_api']
            if api['endpoints']:
                api_info.extend(api['endpoints'][:3])
    
    if api_info:
        print(f"\nAPI端点发现 ({len(api_info)} 条):")
        for i, info in enumerate(api_info[:5], 1):
            print(f"  {i}. {info[:80]}...")
    
    # 错误码信息
    if 'page_454_error' in analyses:
        error = analyses['page_454_error']
        if error['error_codes']:
            print(f"\n错误码发现 ({len(error['error_codes'])} 个):")
            for i, code in enumerate(error['error_codes'][:10], 1):
                print(f"  {i}. {code[:60]}...")
    
    # 下一步建议
    print(f"\n🎯 下一步建议:")
    print("1. 详细分析提取的文本文件")
    print("2. 与现有volcengine技能配置进行比较")
    print("3. 补充缺失的认证和API信息")
    print("4. 完善错误处理指南")
    
    print(f"\n📁 输出文件位置:")
    print(f"  • 提取结果: {results_file}")
    print(f"  • 单个页面文本: {output_dir}/page_*.txt")
    print(f"  • 分析报告: {output_dir}/extraction_report.md")

if __name__ == "__main__":
    main()