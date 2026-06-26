#!/usr/bin/env python3
"""
Obsidian知识库技能测试脚本
"""

import json
import subprocess
import sys

def curl_request(url, method='GET', data=None, timeout=10):
    """使用curl发送HTTP请求"""
    cmd = ['curl', '-s', '--connect-timeout', str(timeout)]
    
    if method == 'POST':
        cmd.extend(['-X', 'POST'])
        if data:
            cmd.extend(['-H', 'Content-Type: application/json'])
            cmd.extend(['-d', json.dumps(data, ensure_ascii=False)])
    
    cmd.append(url)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    url = "http://192.168.18.15:5000/health"
    return_code, stdout, stderr = curl_request(url)
    
    if return_code == 0:
        try:
            result = json.loads(stdout)
            if result.get('status') == 'ok':
                print(f"✅ 健康检查通过: {result.get('service')}")
                return True
            else:
                print(f"❌ 健康检查异常: {result}")
                return False
        except json.JSONDecodeError:
            print(f"❌ 响应解析失败: {stdout}")
            return False
    else:
        print(f"❌ 请求失败: {stderr}")
        return False

def test_stats():
    """测试统计信息"""
    print("📊 测试统计信息...")
    url = "http://192.168.18.15:5000/api/stats"
    return_code, stdout, stderr = curl_request(url)
    
    if return_code == 0:
        try:
            result = json.loads(stdout)
            print(f"✅ 统计信息获取成功")
            print(f"  总笔记数: {result.get('total_notes', 0)}")
            print(f"  总文件数: {result.get('total_files', 0)}")
            return True
        except json.JSONDecodeError:
            print(f"❌ 响应解析失败: {stdout}")
            return False
    else:
        print(f"❌ 请求失败: {stderr}")
        return False

def test_list_notes():
    """测试列出笔记"""
    print("📄 测试列出笔记...")
    url = "http://192.168.18.15:5000/api/notes"
    return_code, stdout, stderr = curl_request(url)
    
    if return_code == 0:
        try:
            result = json.loads(stdout)
            notes = result.get('notes', [])
            print(f"✅ 笔记列表获取成功，共 {len(notes)} 条笔记")
            for i, note in enumerate(notes[:3]):  # 显示前3条
                title = note.get('title', '无标题')
                file = note.get('file', '无文件名')
                print(f"  {i+1}. {title} ({file})")
            return True
        except json.JSONDecodeError:
            print(f"❌ 响应解析失败: {stdout}")
            return False
    else:
        print(f"❌ 请求失败: {stderr}")
        return False

def test_search():
    """测试搜索功能"""
    print("🔍 测试搜索功能...")
    url = "http://192.168.18.15:5000/api/search"
    data = {"query": "测试"}
    
    return_code, stdout, stderr = curl_request(url, method='POST', data=data)
    
    if return_code == 0:
        try:
            result = json.loads(stdout)
            results = result.get('results', [])
            print(f"✅ 搜索成功，找到 {len(results)} 条相关结果")
            for i, note in enumerate(results[:2]):  # 显示前2条
                title = note.get('title', '无标题')
                score = note.get('score', 0)
                print(f"  {i+1}. {title} (相似度: {score:.3f})")
            return True
        except json.JSONDecodeError:
            print(f"❌ 响应解析失败: {stdout}")
            return False
    else:
        print(f"❌ 请求失败: {stderr}")
        return False

def test_create_note():
    """测试创建笔记"""
    print("📝 测试创建笔记...")
    url = "http://192.168.18.15:5000/api/note"
    
    test_data = {
        "title": "测试笔记-小编创建",
        "content": "# 测试笔记\n\n这是一条由小编创建的测试笔记。\n\n## 测试内容\n- 测试创建功能\n- 验证API正常\n- 用于技能学习\n",
        "tags": ["测试", "小编", "技能"]
    }
    
    return_code, stdout, stderr = curl_request(url, method='POST', data=test_data)
    
    if return_code == 0:
        try:
            result = json.loads(stdout)
            if result.get('success'):
                file = result.get('file', '未知文件')
                print(f"✅ 笔记创建成功: {file}")
                return True
            else:
                error = result.get('error', '未知错误')
                print(f"❌ 笔记创建失败: {error}")
                return False
        except json.JSONDecodeError:
            print(f"❌ 响应解析失败: {stdout}")
            return False
    else:
        print(f"❌ 请求失败: {stderr}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始Obsidian知识库技能测试...\n")
    
    # 测试基本功能
    tests = [
        ("健康检查", test_health),
        ("统计信息", test_stats),
        ("列出笔记", test_list_notes),
        ("搜索功能", test_search),
        ("创建笔记", test_create_note)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"{'='*50}")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print("🎉 测试结果总结")
    print(f"✅ 通过: {passed} 项")
    print(f"❌ 失败: {failed} 项")
    
    if failed == 0:
        print("\n🎉 所有测试通过！obsidian_kb技能学习成功！")
        print("\n💡 小编可以使用此技能：")
        print("  - 保存编剧工作经验")
        print("  - 搜索项目相关资料")
        print("  - 管理剧本创作文档")
        print("  - 与其他agent共享知识")
    else:
        print(f"\n⚠️ {failed} 项测试失败，需要进一步检查")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)