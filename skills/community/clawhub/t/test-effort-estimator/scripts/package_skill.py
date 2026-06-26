import os
import zipfile
import sys

def package_skill(skill_path, output_dir=None):
    skill_name = os.path.basename(skill_path)
    
    if output_dir is None:
        output_dir = os.path.dirname(skill_path)
    
    zip_path = os.path.join(output_dir, f"{skill_name}.zip")
    
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    print(f"正在打包技能: {skill_path}")
    print(f"输出文件: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, skill_path)
                zipf.write(file_path, arcname)
                print(f"  添加: {arcname}")
    
    print(f"\n技能打包完成: {zip_path}")
    print(f"文件大小: {os.path.getsize(zip_path)} 字节")
    
    return zip_path

if __name__ == '__main__':
    if len(sys.argv) > 1:
        skill_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        skill_path = 'test-effort-estimator'
        output_dir = None
    
    package_skill(skill_path, output_dir)
