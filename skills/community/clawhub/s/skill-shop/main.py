#!/usr/bin/env python3
import os
import sys
import json
import zipfile
import tarfile
import tempfile
import requests
import shutil
from pathlib import Path

# 配置
SHOP_BASE_URL = "http://127.0.0.1:8080"
SKILLS_DIR = Path("/root/.openclaw/workspace/skills/")
TEMP_DIR = Path(tempfile.gettempdir()) / "skill-shop"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def get_skills():
    """获取所有技能列表"""
    try:
        res = requests.get(f"{SHOP_BASE_URL}/api/skills", timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"❌ 获取技能列表失败: {e}", file=sys.stderr)
        return []

def search_skills(keyword):
    """搜索技能"""
    skills = get_skills()
    keyword = keyword.lower()
    return [s for s in skills if keyword in s['name'].lower() or keyword in s['description'].lower() or any(keyword in t.lower() for t in s['tags'])]

def get_skill_info(skill_id):
    """获取技能详情"""
    try:
        res = requests.get(f"{SHOP_BASE_URL}/api/skills/{skill_id}", timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"❌ 获取技能详情失败: {e}", file=sys.stderr)
        return None

def download_skill(skill_id, skill_name):
    """下载技能包"""
    try:
        url = f"{SHOP_BASE_URL}/download/{skill_id}"
        res = requests.get(url, stream=True, timeout=30)
        res.raise_for_status()
        
        # 从响应头获取文件名
        if 'Content-Disposition' in res.headers:
            filename = res.headers['Content-Disposition'].split('filename=')[1].strip('"')
        else:
            filename = f"{skill_id}_{skill_name}.zip"
        
        temp_path = TEMP_DIR / filename
        with open(temp_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return temp_path
    except Exception as e:
        print(f"❌ 下载失败: {e}", file=sys.stderr)
        return None

def extract_skill(file_path, target_dir):
    """解压缩技能包到临时目录"""
    try:
        temp_extract_dir = TEMP_DIR / f"extract_{Path(file_path).stem}"
        temp_extract_dir.mkdir(parents=True, exist_ok=True)
        
        # 处理zip格式
        if str(file_path).lower().endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_dir)
        # 处理tar.gz格式
        elif str(file_path).lower().endswith(('.tar.gz', '.tgz')):
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                tar_ref.extractall(temp_extract_dir)
        # 处理rar格式（需要unrar命令）
        elif str(file_path).lower().endswith('.rar'):
            import subprocess
            subprocess.run(['unrar', 'x', str(file_path), str(temp_extract_dir)], check=True)
        else:
            print(f"❌ 不支持的压缩格式: {file_path}", file=sys.stderr)
            return False
        
        # 删除压缩包
        os.remove(file_path)
        return temp_extract_dir
    except Exception as e:
        print(f"❌ 解压失败: {e}", file=sys.stderr)
        return False

def install_skill(skill_id):
    """安装技能"""
    # 获取技能信息
    skill = get_skill_info(skill_id)
    if not skill:
        return False
    
    print(f"🛒 开始安装技能: {skill['icon']} {skill['name']}")
    
    # 检查是否已安装
    skill_dir_name = skill['name'].lower().replace(' ', '-')
    skill_dir = SKILLS_DIR / skill_dir_name
    if skill_dir.exists():
        print(f"⚠️  技能已存在，将覆盖安装")
        shutil.rmtree(skill_dir)
    
    # 下载技能包
    print(f"📥 正在下载技能包...")
    file_path = download_skill(skill_id, skill['name'])
    if not file_path:
        return False
    
    # 解压
    print(f"📦 正在解压技能包...")
    temp_extract_dir = extract_skill(file_path, skill_dir)
    if not temp_extract_dir:
        return False
    
    # 处理目录结构：如果只有一个子目录，就把内容移出来
    extracted_items = list(temp_extract_dir.iterdir())
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    if len(extracted_items) == 1 and extracted_items[0].is_dir():
        # 把唯一子目录的内容移到目标目录
        source_dir = extracted_items[0]
        for item in source_dir.iterdir():
            target_item = skill_dir / item.name
            if item.is_dir():
                shutil.copytree(item, target_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target_item)
    else:
        # 直接把内容移到目标目录
        for item in temp_extract_dir.iterdir():
            target_item = skill_dir / item.name
            if item.is_dir():
                shutil.copytree(item, target_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target_item)
    
    # 清理临时目录
    shutil.rmtree(temp_extract_dir)
    
    # 给main.py加执行权限
    main_py = skill_dir / "main.py"
    if main_py.exists():
        main_py.chmod(0o755)
    
    print(f"✅ 技能安装成功！路径: {skill_dir}")
    print(f"💡 使用说明: 查看 {skill_dir}/SKILL.md 获取使用方法")
    return True

def print_skill_table(skills):
    """打印技能列表表格"""
    if not skills:
        print("ℹ️  没有找到相关技能")
        return
    
    # 表头
    print(f"{'ID':<4} {'图标':<4} {'技能名称':<20} {'价格':<8} {'下载量':<6} {'标签'}")
    print("-" * 80)
    
    for s in skills:
        tags = ", ".join(s['tags'])
        price = "免费" if s['is_free'] else "⭐{}积分".format(s['price'])
        print(f"{s['id']:<4} {s['icon']:<4} {s['name']:<20} {price:<8} {s['download_count']:<6} {tags}")

def print_skill_detail(skill):
    """打印技能详情"""
    if not skill:
        return
    
    print(f"\n{skill['icon']} {skill['name']} (ID: {skill['id']})")
    print("=" * 50)
    print(f"作者: {skill['author']}")
    print(f"价格: {'免费' if skill['is_free'] else '⭐{}积分'.format(skill['price'])}")
    print(f"下载量: {skill['download_count']}")
    print(f"标签: {', '.join(skill['tags'])}")
    print(f"发布时间: {skill['created_at']}")
    print("\n📝 技能描述:")
    print(f"  {skill['description']}")
    print("\n💡 安装命令:")
    print(f"  skill-shop install {skill['id']}")

def show_help():
    """显示帮助信息"""
    print("🛒 技能商店客户端 v1.0.0")
    print()
    print("使用方法:")
    print("  skill-shop list              列出所有技能")
    print("  skill-shop search <关键词>   搜索技能")
    print("  skill-shop info <技能ID>     查看技能详情")
    print("  skill-shop install <技能ID>  安装技能")
    print("  skill-shop help              显示帮助信息")
    print()
    print("示例:")
    print("  skill-shop list")
    print("  skill-shop search API")
    print("  skill-shop install 7")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        skills = get_skills()
        print_skill_table(skills)
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("❌ 请输入搜索关键词", file=sys.stderr)
            return
        keyword = sys.argv[2]
        skills = search_skills(keyword)
        print(f"🔍 搜索结果 (关键词: {keyword}):")
        print_skill_table(skills)
    
    elif command == 'info':
        if len(sys.argv) < 3:
            print("❌ 请输入技能ID", file=sys.stderr)
            return
        try:
            skill_id = int(sys.argv[2])
            skill = get_skill_info(skill_id)
            print_skill_detail(skill)
        except ValueError:
            print("❌ 技能ID必须是数字", file=sys.stderr)
    
    elif command == 'install':
        if len(sys.argv) < 3:
            print("❌ 请输入要安装的技能ID", file=sys.stderr)
            return
        try:
            skill_id = int(sys.argv[2])
            install_skill(skill_id)
        except ValueError:
            print("❌ 技能ID必须是数字", file=sys.stderr)
    
    elif command in ['help', '-h', '--help']:
        show_help()
    
    else:
        print(f"❌ 未知命令: {command}", file=sys.stderr)
        show_help()

if __name__ == "__main__":
    main()
