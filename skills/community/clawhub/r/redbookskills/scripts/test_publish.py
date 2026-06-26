#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def test_publish():
    """测试发布功能"""
    print("开始测试小红书发布功能...")
    
    # 检查必要文件是否存在
    title_file = "title.txt"
    content_file = "content.txt"
    
    if not os.path.exists(title_file):
        print(f"错误：标题文件 {title_file} 不存在")
        return False
        
    if not os.path.exists(content_file):
        print(f"错误：内容文件 {content_file} 不存在")
        return False
    
    print("文件检查通过")
    
    # 准备发布命令
    cmd = [
        sys.executable, 
        "publish_pipeline.py",
        "--title-file", title_file,
        "--content-file", content_file,
        "--image-urls", "https://picsum.photos/600/400"
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 使用subprocess执行命令
        result = subprocess.run(
            cmd, 
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print("返回码:", result.returncode)
        
        if result.returncode == 0:
            print("✅ 发布测试成功完成")
            return True
        else:
            print("❌ 发布测试失败")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 命令执行超时")
        return False
    except Exception as e:
        print(f"❌ 执行过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = test_publish()
    sys.exit(0 if success else 1)