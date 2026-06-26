#!/usr/bin/env python3
"""
测试真正的思源笔记文档创建功能
"""

import json
import requests
import sys
import os

# 配置信息
API_URL = "http://192.168.1.6:6811"
TOKEN = "xz1eblvxst0zqcpm"

headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def test_create_doc_api():
    """测试思源笔记的createDoc API"""
    print("=" * 60)
    print("测试思源笔记createDoc API")
    print("=" * 60)
    
    # 1. 首先获取笔记本ID
    print("📚 获取笔记本列表...")
    response = requests.post(
        f'{API_URL}/api/notebook/lsNotebooks',
        headers=headers,
        json={},
        timeout=10
    )
    
    if response.status_code != 200:
        print(f"❌ 获取笔记本失败: {response.status_code}")
        return False
    
    notebooks = response.json().get('data', {}).get('notebooks', [])
    print(f"✅ 找到 {len(notebooks)} 个笔记本")
    
    # 查找'其他'笔记本
    target_notebook = "其他"
    notebook_id = None
    for nb in notebooks:
        if nb['name'] == target_notebook:
            notebook_id = nb['id']
            print(f"✅ 找到笔记本: {nb['name']} (ID: {nb['id']})")
            break
    
    if not notebook_id:
        print(f"❌ 未找到笔记本: {target_notebook}")
        return False
    
    # 2. 测试createDoc API
    document_name = "666-test"
    print(f"\n📝 测试创建文档: {document_name}")
    
    # 根据思源笔记API文档，createDoc需要notebook和path参数
    # path应该是文档的路径，如"/666-test"
    create_data = {
        'notebook': notebook_id,
        'path': f'/{document_name}',
        'title': document_name
    }
    
    print(f"📋 创建参数: {json.dumps(create_data, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            f'{API_URL}/api/filetree/createDoc',
            headers=headers,
            json=create_data,
            timeout=10
        )
        
        print(f"📡 API响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📊 API响应内容: {json.dumps(result, ensure_ascii=False)}")
            
            if result.get('code') == 0:
                document_id = result.get('data')
                print(f"✅ 文档创建成功!")
                print(f"📄 文档ID: {document_id}")
                return True
            else:
                print(f"❌ API返回错误: {result.get('msg')}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_list_docs():
    """测试列出文档"""
    print("\n" + "=" * 60)
    print("测试列出文档")
    print("=" * 60)
    
    # 获取笔记本ID
    response = requests.post(
        f'{API_URL}/api/notebook/lsNotebooks',
        headers=headers,
        json={},
        timeout=10
    )
    
    notebooks = response.json().get('data', {}).get('notebooks', [])
    notebook_id = None
    for nb in notebooks:
        if nb['name'] == "其他":
            notebook_id = nb['id']
            break
    
    if not notebook_id:
        print("❌ 未找到笔记本")
        return
    
    # 列出文档
    response = requests.post(
        f'{API_URL}/api/filetree/listDocsByPath',
        headers=headers,
        json={
            'notebook': notebook_id,
            'path': '/'
        },
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            files = result.get('data', {}).get('files', [])
            print(f"📁 找到 {len(files)} 个文档/文件夹:")
            for file in files:
                print(f"  - {file.get('name')} (ID: {file.get('id')}, 类型: {file.get('type')})")
        else:
            print(f"❌ API错误: {result.get('msg')}")
    else:
        print(f"❌ HTTP错误: {response.status_code}")

if __name__ == "__main__":
    # 先列出当前文档
    test_list_docs()
    
    # 测试创建文档
    print("\n" + "=" * 60)
    success = test_create_doc_api()
    
    # 再次列出文档查看是否创建成功
    if success:
        print("\n" + "=" * 60)
        print("验证文档创建...")
        test_list_docs()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 测试完成 - 文档创建成功!")
    else:
        print("❌ 测试完成 - 文档创建失败")
    print("=" * 60)