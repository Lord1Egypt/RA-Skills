#!/usr/bin/env python3
"""
sync_to_nas.py - 记忆文件同步到NAS
"""
import sys
from pathlib import Path

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

from cloud_adapter import CloudSyncConfig, AdapterFactory

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
SKIP_FILES = {".", "..", ".gitignore", "exports"}

def main():
    configs = CloudSyncConfig.load_from_secrets()
    
    if "samba" not in configs:
        print("❌ 未配置 Samba/NAS")
        return
    
    adapter = AdapterFactory.create(configs["samba"])
    
    # 获取所有记忆文件
    files = []
    for f in MEMORY_DIR.iterdir():
        if f.is_file() and f.name not in SKIP_FILES:
            files.append(f)
    
    if not files:
        print("没有文件需要同步")
        return
    
    print(f"开始同步 {len(files)} 个文件到 NAS...")
    
    success = 0
    failed = 0
    
    for f in sorted(files):
        if adapter.upload(f, f.name):
            success += 1
        else:
            failed += 1
            print(f"  ❌ {f.name}")
    
    print(f"\\n✅ 同步完成: {success} 成功, {failed} 失败")

if __name__ == "__main__":
    main()
