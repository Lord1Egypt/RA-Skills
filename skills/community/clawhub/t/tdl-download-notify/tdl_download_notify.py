#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDL 下载 + Server 酱通知
用法：
  python3 tdl_download_notify.py <chat_id> <message_id> [output_dir]
  
示例：
  python3 tdl_download_notify.py 1340124720 126326 /root/tdl_download
"""

import subprocess
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Server 酱配置
SENDKEY = "sctp6765tcomfljakjcquc4e7mdaman"
SERVERCHAN_API = f"https://sctapi.ftqq.com/{SENDKEY}.send"

# TDL 下载目录
DEFAULT_DOWNLOAD_DIR = "/root/tdl_download"


def send_serverchan(title, desp):
    """发送 Server 酱推送"""
    import requests
    
    data = {
        "title": title,
        "desp": desp
    }
    
    try:
        response = requests.post(SERVERCHAN_API, data=data, timeout=10)
        result = response.json()
        return result.get("code") == 0, result
    except Exception as e:
        return False, {"error": str(e)}


def get_file_info(filepath):
    """获取文件信息"""
    try:
        stat = os.stat(filepath)
        size = stat.st_size
        
        # 格式化大小
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                size_str = f"{size:.2f} {unit}"
                break
            size /= 1024.0
        
        return {
            "name": os.path.basename(filepath),
            "path": filepath,
            "size": size_str,
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "name": os.path.basename(filepath),
            "error": str(e)
        }


def download_and_notify(chat_id, message_id, output_dir=None):
    """执行下载并发送通知"""
    
    if output_dir is None:
        output_dir = DEFAULT_DOWNLOAD_DIR
    
    # 确保下载目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取下载前的文件列表
    files_before = set(os.listdir(output_dir))
    
    # 构建 tdl 下载命令
    tdl_cmd = [
        "tdl", "download",
        "-d", output_dir,
        "-u", f"https://t.me/c/{chat_id}/{message_id}"
    ]
    
    print(f"开始下载：https://t.me/c/{chat_id}/{message_id}")
    print(f"下载目录：{output_dir}")
    
    # 执行下载
    start_time = datetime.now()
    try:
        result = subprocess.run(
            tdl_cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 小时超时
        )
        end_time = datetime.now()
        duration = end_time - start_time
        
        download_success = result.returncode == 0
        
    except subprocess.TimeoutExpired:
        end_time = datetime.now()
        duration = end_time - start_time
        download_success = False
        result = subprocess.CompletedProcess(tdl_cmd, -1, "", "下载超时")
    except Exception as e:
        end_time = datetime.now()
        duration = end_time - start_time
        download_success = False
        result = subprocess.CompletedProcess(tdl_cmd, -1, "", str(e))
    
    # 获取下载后的文件列表
    files_after = set(os.listdir(output_dir))
    
    # 找出新下载的文件
    new_files = files_after - files_before
    
    # 获取新文件的详细信息
    file_infos = []
    total_size = 0
    
    for filename in new_files:
        filepath = os.path.join(output_dir, filename)
        if os.path.isfile(filepath):
            info = get_file_info(filepath)
            file_infos.append(info)
            if "size_bytes" in info:
                total_size += info["size_bytes"]
    
    # 格式化总大小
    total_size_str = f"{total_size / 1024 / 1024 / 1024:.2f} GB" if total_size > 1024**3 else \
                     f"{total_size / 1024 / 1024:.2f} MB" if total_size > 1024**2 else \
                     f"{total_size / 1024:.2f} KB"
    
    # 构建通知消息
    if download_success:
        title = "✅ 下载完成"
        
        if file_infos:
            # 文件列表
            file_list = "\n".join([
                f"📄 **{info['name']}**\n   大小：{info['size']}\n   时间：{info.get('modified', 'N/A')}"
                for info in file_infos
            ])
            
            desp = f"""
**下载成功！**

📥 来源：https://t.me/c/{chat_id}/{message_id}
📁 目录：`{output_dir}`
📊 数量：{len(file_infos)} 个文件
💾 总大小：{total_size_str}

**文件列表:**

{file_list}

⏱️ 耗时：{duration.seconds // 60}分 {duration.seconds % 60}秒
🕐 完成时间：{end_time.strftime("%Y-%m-%d %H:%M:%S")}
"""
        else:
            desp = f"""
**下载成功！**

📥 来源：https://t.me/c/{chat_id}/{message_id}
📁 目录：`{output_dir}`
⚠️ 未检测到新文件（可能已存在）

⏱️ 耗时：{duration.seconds // 60}分 {duration.seconds % 60}秒
"""
    else:
        title = "❌ 下载失败"
        desp = f"""
**下载失败**

📥 来源：https://t.me/c/{chat_id}/{message_id}
❌ 错误：{result.stderr or result.stdout or '未知错误'}

⏱️ 耗时：{duration.seconds // 60}分 {duration.seconds % 60}秒
🕐 失败时间：{end_time.strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    # 发送 Server 酱通知
    print(f"\n发送通知...")
    success, response = send_serverchan(title, desp)
    
    if success:
        print(f"✅ 通知已发送")
    else:
        print(f"❌ 通知发送失败：{response}")
    
    # 返回结果
    return {
        "download_success": download_success,
        "notify_success": success,
        "files": file_infos,
        "duration": str(duration),
        "error": result.stderr if not download_success else None
    }


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "message": "用法：python3 tdl_download_notify.py <chat_id> <message_id> [output_dir]",
            "example": "python3 tdl_download_notify.py 1340124720 126326 /root/tdl_download"
        }, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    chat_id = sys.argv[1]
    message_id = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = download_and_notify(chat_id, message_id, output_dir)
    
    print(f"\n{json.dumps(result, indent=2, ensure_ascii=False)}")
    sys.exit(0 if result["download_success"] and result["notify_success"] else 1)


if __name__ == "__main__":
    main()
