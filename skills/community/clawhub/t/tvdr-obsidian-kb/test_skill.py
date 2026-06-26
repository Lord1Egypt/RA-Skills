#!/usr/bin/env python3
"""
Obsidian知识库技能测试脚本
"""

import json
import subprocess
import sys
import time

def wget_request(url, method='GET', data=None, timeout=10):
    """使用wget发送HTTP请求"""
    cmd = ['wget', '--timeout', str(timeout), '-q', '-O', '-']
    
    if method == 'POST':
        cmd.extend(['--post-data'])
        if isinstance(data, dict):
            cmd.append(json.dumps(data, ensure_ascii=False))
        else:
            cmd.append(str(data))
        # BusyBox wget不支持-H选项，需要手动处理headers
        cmd.append(url)
    else:
        cmd.append(url)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return result.returncode, result.stdout, result.stderr

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    url = "http://192.168.18.15:5000/health"
    return_code, stdout, stderr = wget_request(url)
    
    if return_code == 0 and 'status' in stdout:
        print(f"✅ 健康检查通过: {stdout.strip()}")
        return True
    else:
        print(f"❌ 健康检查失败: {stderr}")
        return False

def test_create_note():
    """测试创建笔记"""
    print("📝 测试创建笔记...")
    url = "http://192.168.18.15:5000/api/note"
    
    test_data = {
        "title": "测试笔记-来自小编",
        "content": "# 测试笔记\n\n这是一条来自小编的测试笔记。\n\n## 测试内容\n- 测试创建功能\n- 验证API正常\n",
        "tags": ["测试", "小编", "技能"]
    }
    
    return_code, stdout, stderr = wget_request(url, method='POST', data=test_data)
    
    if return_code == 0:
        try:
            result = json.loads(stdout)
            if 'success' in result and result['success']:
                print("✅ 笔记创建成功")
                return True, result.get('file', '')
            else:
                print(f"❌ 笔记创建失败: {result.get('error', '未知错误')}")
                return False, None
        except json.JSONDecodeError:
            print(f"❌ 响应解析失败: {stdout}")
            return False, None
    else:
        print(f"❌ 请求失败: {stderr}")
        return False, None

def test_search_notes():
    """测试搜索笔记"""
    print("🔍 测试搜索笔记...")
    url = "http://192.168.18.15:5000/api/search"
    
    search_data = {
        "query": "测试"
    }
    
    return_code, stdout, stderr = wget_request(url, method='POST', data=search_data)
    
    if return_code == 0:
        try:
            result = json.loads(stdout)
            if 'results' in result:
                print(f"✅ 搜索成功，找到 {len(result['results'])} 条结果")
                for i, note in enumerate(result['results'][:3]):  # 显示前3条
                    print(f"  {i+1}. {note.get('title', '无标题')}")
                return True
            else:
                print(f"❌ 搜索结果格式异常: {result}")
                return False
        except json.JSONDecodeError:
            print(f"❌ 响应解析失败: {stdout}")
            return False
    else:
        print(f"❌ 搜索请求失败: {stderr}")
        return False

def test_get_stats():
    """测试获取统计信息"""
    print("📊 测试获取统计信息...")
    url = "http://192.168.18.15:5000/api/stats"
    
    return_code, stdout, stderr = wget_request(url)
    
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
        print(f"❌ 统计信息获取失败: {stderr}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始Obsidian知识库技能测试...\n")
    
    # 检查API状态
    if not test_health_check():
        print("\n❌ API服务不可用，测试终止")
        sys.exit(1)
    
    print("\n" + "="*50)
    
    # 测试创建笔记
    create_success, created_file = test_create_note()
    
    if create_success:
        print(f"\n📄 创建的文件名: {created_file}")
    else:
        print("\n⚠️ 创建笔记测试失败，继续其他测试")
    
    print("\n" + "="*50)
    
    # 测试搜索功能
    test_search_notes()
    
    print("\n" + "="*50)
    
    # 测试统计信息
    test_get_stats()
    
    print("\n" + "="*50)
    print("🎉 Obsidian知识库技能测试完成！")
    print("\n💡 小编可以使用此技能：")
    print("  - 保存编剧工作经验")
    print("  - 搜索项目相关资料")
    print("  - 管理剧本创作文档")
    print("  - 与其他agent共享知识")

if __name__ == "__main__":
    main()