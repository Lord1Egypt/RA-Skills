import os
import shutil
import hashlib
import json
from datetime import datetime

# 配置
SOURCE_DIR = r"D:\code\openclaw_lakeskill\outerfiles"  # 原E盘路径已调整
DEST_DIR = r"D:\code\openclaw_lakeskill\files"
HASH_FILE = r"D:\code\openclaw_lakeskill\water-knowledge-assistant\config\file_hashes.json"
SUPPORTED_EXTENSIONS = ['.pdf', '.md', '.txt', '.docx']


def calculate_sha256(file_path):
    """计算文件的SHA256哈希值"""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # 分块读取文件以处理大文件
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"计算文件哈希时出错 {file_path}: {e}")
        return None


def load_existing_hashes():
    """加载已存在的文件哈希记录"""
    if os.path.exists(HASH_FILE):
        try:
            with open(HASH_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载哈希文件时出错: {e}")
            return {}
    return {}


def save_hashes(hashes):
    """保存文件哈希记录"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(HASH_FILE), exist_ok=True)
        with open(HASH_FILE, "w", encoding="utf-8") as f:
            json.dump(hashes, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"保存哈希文件时出错: {e}")
        return False


def scan_source_directory():
    """扫描源目录中的文件"""
    files_to_process = []
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            # 检查文件扩展名
            _, ext = os.path.splitext(file)
            if ext.lower() in SUPPORTED_EXTENSIONS:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, SOURCE_DIR)
                files_to_process.append((full_path, relative_path))
    return files_to_process


def process_files():
    """处理文件：复制更新的文件到目标目录"""
    # 加载已存在的哈希
    existing_hashes = load_existing_hashes()
    new_hashes = {}
    updated_files = []
    skipped_files = []

    # 扫描源目录
    files_to_process = scan_source_directory()
    print(f"发现 {len(files_to_process)} 个支持的文件")

    # 处理每个文件
    for full_path, relative_path in files_to_process:
        # 计算当前文件的哈希
        current_hash = calculate_sha256(full_path)
        if not current_hash:
            continue

        # 获取目标路径
        dest_path = os.path.join(DEST_DIR, relative_path)
        
        # 检查是否需要更新
        if relative_path not in existing_hashes or existing_hashes[relative_path] != current_hash:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # 复制文件
            try:
                shutil.copy2(full_path, dest_path)
                updated_files.append(relative_path)
                print(f"已更新: {relative_path}")
            except Exception as e:
                print(f"复制文件时出错 {relative_path}: {e}")
                skipped_files.append(relative_path)
        else:
            skipped_files.append(relative_path)
            print(f"未变更: {relative_path}")

        # 更新哈希记录
        new_hashes[relative_path] = current_hash

    # 保存新的哈希记录
    if save_hashes(new_hashes):
        print("哈希记录已保存")
    else:
        print("哈希记录保存失败")

    # 清理目标目录中不存在于源目录的文件
    clean_up_stale_files(new_hashes, existing_hashes)

    # 返回处理结果
    return {
        "total_files": len(files_to_process),
        "updated_files": len(updated_files),
        "skipped_files": len(skipped_files),
        "updated_list": updated_files,
        "timestamp": datetime.now().isoformat()
    }


def clean_up_stale_files(new_hashes, existing_hashes):
    """清理目标目录中不存在于源目录的文件"""
    for relative_path in existing_hashes:
        if relative_path not in new_hashes:
            dest_path = os.path.join(DEST_DIR, relative_path)
            if os.path.exists(dest_path):
                try:
                    os.remove(dest_path)
                    print(f"已删除: {relative_path}")
                except Exception as e:
                    print(f"删除文件时出错 {relative_path}: {e}")


def main():
    """主函数"""
    print("开始知识库导入...")
    print(f"源目录: {SOURCE_DIR}")
    print(f"目标目录: {DEST_DIR}")
    
    result = process_files()
    
    print("\n导入完成!")
    print(f"总文件数: {result['total_files']}")
    print(f"更新文件数: {result['updated_files']}")
    print(f"跳过文件数: {result['skipped_files']}")
    
    if result['updated_files'] > 0:
        print("\n更新的文件:")
        for file in result['updated_list']:
            print(f"  - {file}")


if __name__ == "__main__":
    main()