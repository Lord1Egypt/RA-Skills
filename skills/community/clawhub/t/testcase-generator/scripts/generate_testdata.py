#!/usr/bin/env python3
"""
测试数据生成工具
根据测试用例自动生成测试数据集
"""

import sys
import json
import random
import string

def generate_string(length=10, charset='alphanumeric'):
    """生成字符串"""
    if charset == 'alphanumeric':
        chars = string.ascii_letters + string.digits
    elif charset == 'letters':
        chars = string.ascii_letters
    elif charset == 'digits':
        chars = string.digits
    elif charset == 'special':
        chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    elif charset == 'chinese':
        chars = '测试用户登录功能模块数据验证'
    else:
        chars = string.ascii_letters + string.digits
    
    return ''.join(random.choice(chars) for _ in range(length))

def generate_test_data(test_cases):
    """根据用例生成测试数据"""
    test_data = []
    
    for tc in test_cases:
        tc_id = tc[1]
        title = tc[2]
        test_type = tc[6]
        priority = tc[7]
        
        data_item = {
            "用例 ID": tc_id,
            "用例标题": title,
            "测试数据": {}
        }
        
        # 根据用例类型生成数据
        if "登录" in title or "auth" in title.lower():
            data_item["测试数据"] = generate_auth_data(tc)
        elif "搜索" in title:
            data_item["测试数据"] = generate_search_data(tc)
        elif "边界" in test_type or "boundary" in test_type.lower():
            data_item["测试数据"] = generate_boundary_data(tc)
        elif "异常" in test_type or "exception" in test_type.lower():
            data_item["测试数据"] = generate_exception_data(tc)
        elif "性能" in test_type or "performance" in test_type.lower():
            data_item["测试数据"] = generate_performance_data(tc)
        else:
            data_item["测试数据"] = generate_default_data(tc)
        
        test_data.append(data_item)
    
    return test_data

def generate_auth_data(tc):
    """生成认证相关测试数据"""
    return {
        "有效用户名": "testuser001",
        "有效邮箱": "test@example.com",
        "有效手机号": "13800138000",
        "有效密码": "Test123456",
        "无效用户名_过短": "te",
        "无效用户名_过长": "t" * 100,
        "无效用户名_特殊字符": "test<script>",
        "无效密码_缺大写字母": "test123456",
        "无效密码_缺小写字母": "TEST123456",
        "无效密码_缺数字": "Testpassword",
        "无效密码_过短": "T1",
        "锁定次数": 5,
        "锁定时间_分钟": 30
    }

def generate_search_data(tc):
    """生成搜索相关测试数据"""
    return {
        "有效关键词_中文": "测试",
        "有效关键词_英文": "test",
        "有效关键词_数字": "12345",
        "有效关键词_混合": "测试 Test123",
        "边界值_2 字符": "测试",
        "边界值_50 字符": "测" * 50,
        "无效_1 字符": "测",
        "无效_51 字符": "测" * 51,
        "无效_纯空格": "   ",
        "XSS 尝试": "<script>alert(1)</script>",
        "SQL 注入尝试": "' OR '1'='1",
        "特殊字符": "<>&\"'",
        "emoji": "😀😁😂",
        "全角字符": "测试搜索",
        "零宽字符": "test\u200bsearch"
    }

def generate_boundary_data(tc):
    """生成边界值测试数据"""
    return {
        "最小值": 0,
        "最小值 -1": -1,
        "最小值 +1": 1,
        "最大值": 100,
        "最大值 -1": 99,
        "最大值 +1": 101,
        "空值": None,
        "空字符串": "",
        "空数组": [],
        "单元素": [1],
        "临界值": 50,
        "溢出值": 2**31
    }

def generate_exception_data(tc):
    """生成异常测试数据"""
    return {
        "null 值": None,
        "未定义": "undefined",
        "超大字符串": "x" * 10000,
        "恶意 HTML": "<img src=x onerror=alert(1)>",
        "恶意 JS": "javascript:alert(document.cookie)",
        "路径遍历": "../../etc/passwd",
        "命令注入": "; rm -rf /",
        "超长 URL": "http://" + "a" * 2000 + ".com",
        "非法 JSON": "{invalid json}",
        "编码错误": "\xff\xfe",
        "并发请求": 100,
        "超时时间_ms": 30000
    }

def generate_performance_data(tc):
    """生成性能测试数据"""
    return {
        "并发用户数": 100,
        "请求次数": 1000,
        "数据量_条": 10000,
        "响应时间要求_ms": 500,
        "吞吐量要求_tps": 100,
        "CPU 使用率上限": 80,
        "内存使用率上限": 80,
        "测试持续时间_s": 60,
        " rampup 时间_s": 10
    }

def generate_default_data(tc):
    """生成默认测试数据"""
    return {
        "字符串数据": generate_string(10),
        "数字数据": random.randint(1, 100),
        "布尔数据": random.choice([True, False]),
        "数组数据": [1, 2, 3, 4, 5],
        "对象数据": {"key": "value", "count": 42}
    }

def export_to_json(test_data, output_path):
    """导出为 JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    return f"✅ 测试数据已导出：{output_path}"

def export_to_csv(test_data, output_path):
    """导出为 CSV"""
    import csv
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["用例 ID", "用例标题", "数据名称", "数据值", "数据类型"])
        for item in test_data:
            for key, value in item["测试数据"].items():
                writer.writerow([
                    item["用例 ID"],
                    item["用例标题"],
                    key,
                    str(value),
                    type(value).__name__
                ])
    return f"✅ 测试数据 CSV 已导出：{output_path}"

def main():
    if len(sys.argv) < 3:
        print("用法：python generate_testdata.py <输入用例 JSON> <输出路径> [格式]")
        print("格式：json (默认), csv")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    format_type = sys.argv[3] if len(sys.argv) > 3 else 'json'
    
    # 读取测试用例
    with open(input_path, 'r', encoding='utf-8') as f:
        test_cases_data = json.load(f)
    
    # 转换为列表格式
    test_cases = []
    for tc in test_cases_data:
        test_cases.append([
            tc.get('module', '模块'),
            tc.get('id', 'TC-001'),
            tc.get('title', '标题'),
            tc.get('precondition', ''),
            tc.get('steps', ''),
            tc.get('expected', ''),
            tc.get('type', '功能测试'),
            tc.get('priority', 'P2'),
            tc.get('stage', '系统测试')
        ])
    
    # 生成测试数据
    test_data = generate_test_data(test_cases)
    
    # 导出
    if format_type == 'csv':
        result = export_to_csv(test_data, output_path)
    else:
        result = export_to_json(test_data, output_path)
    
    print(result)
    print(f"📊 共生成 {len(test_data)} 条测试数据")

if __name__ == '__main__':
    main()
