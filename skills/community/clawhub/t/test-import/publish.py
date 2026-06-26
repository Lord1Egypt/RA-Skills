#!/usr/bin/env python3
"""
ClawHub Publish - 将本地 skill 发布到 ClawHub
"""
import os
import sys
import json
import argparse
import requests

TOKEN = "clh_GKYQNYsiccGeacf6up29a0XJdyFdyPOCzzLWaWukx3k"
API_URL = "https://clawhub.ai/api/v1/skills"


def upload_file(filename, content_type="text/plain"):
    """获取上传URL并上传文件"""
    resp = requests.post(
        "https://clawhub.ai/api/cli/upload-url",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"filename": filename, "contentType": content_type}
    )
    data = resp.json()
    upload_url = data.get("uploadUrl")
    
    if upload_url:
        # 上传文件内容
        requests.put(upload_url, data=content, headers={"Content-Type": content_type})
    
    return True


def publish_skill(slug, name, version, skill_dir, changelog=""):
    """发布 skill 到 ClawHub"""
    
    # 获取技能目录
    if not os.path.isdir(skill_dir):
        return {"error": f"目录不存在: {skill_dir}"}
    
    # 获取文件列表
    files = []
    for f in os.listdir(skill_dir):
        if f.endswith(('.md', '.py', '.js', '.json', '.txt')) and not f.startswith('__'):
            filepath = os.path.join(skill_dir, f)
            if os.path.isfile(filepath):
                files.append((f, filepath))
    
    if not files:
        return {"error": "没有找到可发布文件"}
    
    print(f"准备发布 {len(files)} 个文件...")
    
    # 构建 payload
    payload = {
        "slug": slug,
        "displayName": name,
        "version": version,
        "changelog": changelog,
        "tags": ["latest"],
        "acceptLicenseTerms": True
    }
    
    # 构建文件上传
    file_data = []
    for filename, filepath in files:
        with open(filepath, 'rb') as f:
            content = f.read()
        file_data.append(('files', (filename, content, 'text/plain')))
    
    # 发布
    resp = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {TOKEN}"},
        data={"payload": json.dumps(payload)},
        files=file_data
    )
    
    if resp.status_code == 200:
        result = resp.json()
        return {
            "success": True,
            "slug": slug,
            "version": result.get("versionId"),
            "url": f"https://clawhub.ai/skill/{slug}"
        }
    else:
        return {"error": resp.text}


def main():
    parser = argparse.ArgumentParser(description="发布 skill 到 ClawHub")
    parser.add_argument("--slug", required=True, help="Skill slug")
    parser.add_argument("--name", required=True, help="显示名称")
    parser.add_argument("--version", required=True, help="版本号")
    parser.add_argument("--path", default=".", help="技能目录路径")
    parser.add_argument("--changelog", default="", help="更新日志")
    
    args = parser.parse_args()
    
    result = publish_skill(
        slug=args.slug,
        name=args.name,
        version=args.version,
        skill_dir=args.path,
        changelog=args.changelog
    )
    
    if result.get("success"):
        print(f"✓ 发布成功!")
        print(f"  Slug: {result['slug']}")
        print(f"  版本: {result['version']}")
        print(f"  链接: {result['url']}")
    else:
        print(f"✗ 发布失败: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
