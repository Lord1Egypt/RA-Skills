import os
import sys
import zipfile
import subprocess

# 设置 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')

# 7-Zip 路径 - 从注册表获取或使用默认路径
def get_7z_path():
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\7-Zip")
        path = winreg.QueryValueEx(key, "Path")[0]
        winreg.CloseKey(key)
        return os.path.join(path, "7z.exe")
    except:
        # 默认路径
        paths = [r"D:\Program Files\7-Zip\7z.exe", r"C:\Program Files\7-Zip\7z.exe"]
        for p in paths:
            if os.path.exists(p):
                return p
        return None

SEVEN_ZIP = get_7z_path()

# 记录失败的压缩包
FAILED_FILES = []

def extract_zip(file_path, extract_to):
    """解压zip文件，正确处理中文编码"""
    os.makedirs(extract_to, exist_ok=True)
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            for info in zf.infolist():
                original = info.filename
                try:
                    decoded = original.encode('cp437').decode('gbk')
                except:
                    decoded = original
                
                target_path = os.path.join(extract_to, decoded)
                target_dir = os.path.dirname(target_path)
                if target_dir and not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                
                if not decoded.endswith('/'):
                    with open(target_path, 'wb') as f:
                        f.write(zf.read(info))
        print(f"[OK] zip: {os.path.basename(file_path)}")
        return True
    except Exception as e:
        print(f"[错误] zip解压失败: {e}")
        FAILED_FILES.append((file_path, str(e)))
        return False

def extract_7z(file_path, extract_to):
    """解压7z文件"""
    os.makedirs(extract_to, exist_ok=True)
    if not SEVEN_ZIP:
        print(f"[错误] 7-Zip 未安装，无法解压: {os.path.basename(file_path)}")
        FAILED_FILES.append((file_path, "7-Zip未安装"))
        return False
    try:
        cmd = [SEVEN_ZIP, 'x', file_path, f'-o{extract_to}', '-y']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] 7z: {os.path.basename(file_path)}")
            return True
        else:
            err = result.stderr[:200] if result.stderr else "未知错误"
            print(f"[错误] 7z解压失败: {err}")
            FAILED_FILES.append((file_path, err))
            return False
    except Exception as e:
        print(f"[错误] 7z解压异常: {e}")
        FAILED_FILES.append((file_path, str(e)))
        return False

def extract_rar(file_path, extract_to):
    """解压rar文件"""
    return extract_7z(file_path, extract_to)  # 7z也支持rar

def extract_all(target):
    """递归解压所有压缩包"""
    global FAILED_FILES
    FAILED_FILES = []
    
    # 如果是文件，直接解压
    if os.path.isfile(target):
        base_dir = os.path.dirname(target)
        file_name = os.path.basename(target)
        ext = file_name.lower()
        
        if ext.endswith('.zip'):
            folder = file_name.replace('.zip', '')
            extract_to = os.path.join(base_dir, folder)
            if extract_zip(target, extract_to):
                os.remove(target)
                # 继续处理解压后的文件夹中的嵌套压缩包
                extract_all(extract_to)
        elif ext.endswith('.7z'):
            folder = file_name.replace('.7z', '')
            extract_to = os.path.join(base_dir, folder)
            if extract_7z(target, extract_to):
                os.remove(target)
                extract_all(extract_to)
        elif ext.endswith('.rar'):
            folder = file_name.replace('.rar', '')
            extract_to = os.path.join(base_dir, folder)
            if extract_rar(target, extract_to):
                os.remove(target)
                extract_all(extract_to)
        else:
            print(f"[警告] 不是压缩文件: {file_name}")
        return
    
    # 如果是目录，递归处理
    base_dir = target
    
    while True:
        changed = False
        for root, dirs, files in os.walk(base_dir):
            for f in files:
                full_path = os.path.join(root, f)
                ext = f.lower()
                
                if ext.endswith('.zip'):
                    folder = f.replace('.zip', '')
                    extract_to = os.path.join(root, folder)
                    if extract_zip(full_path, extract_to):
                        os.remove(full_path)
                        changed = True
                    break
                elif ext.endswith('.7z'):
                    folder = f.replace('.7z', '')
                    extract_to = os.path.join(root, folder)
                    if extract_7z(full_path, extract_to):
                        os.remove(full_path)
                        changed = True
                    break
                elif ext.endswith('.rar'):
                    folder = f.replace('.rar', '')
                    extract_to = os.path.join(root, folder)
                    if extract_rar(full_path, extract_to):
                        os.remove(full_path)
                        changed = True
                    break
            
            if changed:
                break
        
        if not changed:
            break
    
    # 检查剩余
    remaining = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith(('.zip', '.7z', '.rar')):
                remaining.append(os.path.join(root, f))
    
    # 报告结果
    print("\n" + "="*40)
    if remaining:
        print(f"⚠️ 还有 {len(remaining)} 个压缩包无法解压:")
        for r in remaining:
            print(f"  - {r}")
    else:
        print("✅ 全部解压完成！")
    
    if FAILED_FILES:
        print(f"\n❌ {len(FAILED_FILES)} 个文件解压失败:")
        for path, err in FAILED_FILES:
            print(f"  - {os.path.basename(path)}: {err}")
    
    if not remaining and not FAILED_FILES:
        print("="*40)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python unzip_all.py <文件或目录>")
        sys.exit(1)
    
    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"错误: 路径不存在: {target}")
        sys.exit(1)
    
    extract_all(target)