#!/usr/bin/env python3
"""
Notion Database 연결 상태 확인
"""
import json
import urllib.request
from pathlib import Path

# Database ID
database_id = "fe8277a4484243db8b3b2f1a15399d40"

# Notion 토큰 로드
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
notion_token = None

with open(env_file, 'r') as f:
    for line in f:
        if line.startswith('NOTION_API_KEY='):
            notion_token = line.split('=', 1)[1].strip()

print("="*70)
print("NOTION DATABASE CONNECTION CHECK")
print("="*70)
print(f"\nDatabase ID: {database_id}")
print(f"Integration: openclaw\n")

# 1. Database 존재 확인
print("1️⃣ Checking database...")
try:
    req = urllib.request.Request(
        f'https://api.notion.com/v1/databases/{database_id}',
        headers={
            'Authorization': f'Bearer {notion_token}',
            'Notion-Version': '2022-06-28'
        }
    )
    
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read())
    
    print("✅ Database exists")
    print(f"   Title: {data['title'][0]['text']['content']}")
    
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    error_data = json.loads(error_body)
    
    print(f"❌ Database not found: {e.code}")
    print(f"   Message: {error_data.get('message', 'Unknown')}")
    print("\n🔧 해결 방법:")
    print("   1. Notion에서 Database 열기")
    print("   2. '...' 메뉴 → 'Connections'")
    print("   3. 'openclaw' Integration 연결")
    exit(1)

# 2. 페이지 생성 테스트
print("\n2️⃣ Testing write permission...")
try:
    test_page = {
        "parent": {"database_id": database_id},
        "properties": {
            "내용": {
                "title": [{"text": {"content": "🧪 연결 테스트"}}]
            }
        }
    }
    
    req = urllib.request.Request(
        'https://api.notion.com/v1/pages',
        data=json.dumps(test_page).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {notion_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
    )
    
    with urllib.request.urlopen(req, timeout=10) as response:
        page_data = json.loads(response.read())
    
    print("✅ Write permission confirmed")
    print(f"   Test page created: {page_data['id']}")
    
    # 테스트 페이지 삭제 (보관)
    print("\n3️⃣ Archiving test page...")
    delete_req = urllib.request.Request(
        f"https://api.notion.com/v1/pages/{page_data['id']}",
        data=json.dumps({"archived": True}).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {notion_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        },
        method='PATCH'
    )
    
    urllib.request.urlopen(delete_req, timeout=10)
    print("✅ Test page archived")
    
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    error_data = json.loads(error_body)
    
    print(f"❌ Write permission denied: {e.code}")
    print(f"   Message: {error_data.get('message', 'Unknown')}")
    print("\n🔧 Integration에 쓰기 권한이 없습니다")
    exit(1)

print("\n" + "="*70)
print("✅ ALL CHECKS PASSED - Ready to use!")
print("="*70)
