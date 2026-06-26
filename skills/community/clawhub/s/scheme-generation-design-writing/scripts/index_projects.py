#!/usr/bin/env python3
"""
项目索引构建器 - 扫描历史项目并生成索引

这个脚本会扫描指定目录下的所有项目文件夹，提取项目信息并生成索引文件。
索引文件用于快速匹配相关项目。

用法:
    python index_projects.py
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# 配置文件路径
SKILL_ROOT = Path(__file__).parent.parent
CONFIG_FILE = SKILL_ROOT / "config.json"
INDEX_FILE = SKILL_ROOT / "data" / "project_index.json"

# 支持的文件扩展名
SUPPORTED_DOCS = {'.docx', '.doc', '.pdf', '.md', '.txt'}
SUPPORTED_IMAGES = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'}

# 行业关键词映射
INDUSTRY_KEYWORDS = {
    '金融': ['银行', '金融', '保险', '证券', '支付', '理财', '信用社'],
    '电商': ['电商', '购物', '商城', '零售', '交易', '电子商务'],
    '医疗': ['医疗', '健康', '医院', '诊所', '药品', '医药'],
    '教育': ['教育', '学习', '培训', '课程', '学校', '教学'],
    '社交': ['社交', '聊天', '社区', '论坛', '交友', '通讯'],
    '工具': ['工具', '效率', '办公', '管理', '协作', '生产力'],
    'IoT': ['智能', '物联网', 'iot', '硬件', '设备', '家居'],
    '出行': ['出行', '交通', '导航', '打车', '地图', '旅游'],
    '娱乐': ['娱乐', '游戏', '视频', '音乐', '直播', '影视'],
    '政务': ['政务', '政府', '公共', '服务', '民生'],
}

# 项目类型关键词
TYPE_KEYWORDS = {
    'APP': ['app', '应用', '移动端', '手机', 'mobile'],
    '网站': ['网站', 'web', '官网', '门户', 'website'],
    '小程序': ['小程序', '微信', '支付宝', 'miniprogram'],
    '系统': ['系统', '平台', '管理', '后台', 'system'],
    '品牌': ['品牌', 'vi', 'logo', '视觉', 'brand'],
}


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {CONFIG_FILE}\n"
            f"请确保 config.json 存在于技能根目录"
        )
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_date_from_name(name: str) -> str:
    """从项目名称中提取日期"""
    patterns = [
        r'(\d{4})\.(\d{1,2})\.(\d{1,2})',
        r'(\d{4})\.(\d{1,2})',
        r'(\d{4})-(\d{1,2})-(\d{1,2})',
        r'(\d{4})-(\d{1,2})',
        r'(\d{4})(\d{2})(\d{2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                return f"{groups[0]}-{groups[1].zfill(2)}-{groups[2].zfill(2)}"
            elif len(groups) == 2:
                return f"{groups[0]}-{groups[1].zfill(2)}-01"
    
    return "未知"


def detect_industry(name: str) -> str:
    """检测项目所属行业"""
    name_lower = name.lower()
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name_lower:
                return industry
    return "其他"


def detect_type(name: str) -> str:
    """检测项目类型"""
    name_lower = name.lower()
    for ptype, keywords in TYPE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name_lower:
                return ptype
    return "其他"


def extract_keywords(name: str) -> List[str]:
    """从项目名称中提取关键词"""
    # 移除日期
    cleaned = re.sub(r'\d{4}[.-]?\d{1,2}[.-]?\d{0,2}', '', name)
    # 替换分隔符为空格
    cleaned = re.sub(r'[_\-\.]+', ' ', cleaned)
    # 分词
    words = cleaned.split()
    # 停用词
    stop_words = {'项目', '标书', '设计', '咨询', '服务', '的', '和', '与', '及'}
    # 过滤并返回
    keywords = [w.strip() for w in words if w.strip() and w.strip() not in stop_words]
    return keywords[:10]


def scan_project_files(project_path: Path) -> Dict[str, List[str]]:
    """扫描项目文件夹，分类文件"""
    files = {
        'requirements': [],
        'design_docs': [],
        'designs': [],
        'others': []
    }
    
    if not project_path.exists():
        return files
    
    try:
        for file in project_path.rglob('*'):
            if not file.is_file():
                continue
            
            ext = file.suffix.lower()
            name_lower = file.name.lower()
            
            # 文档类型
            if ext in SUPPORTED_DOCS:
                if any(kw in name_lower for kw in ['需求', 'requirement', 'prd', '规格', 'spec']):
                    files['requirements'].append(file.name)
                elif any(kw in name_lower for kw in ['设计', 'design', '说明', 'description']):
                    files['design_docs'].append(file.name)
                else:
                    files['others'].append(file.name)
            # 图片类型
            elif ext in SUPPORTED_IMAGES:
                files['designs'].append(file.name)
    except Exception as e:
        print(f"  警告: 扫描文件时出错 - {e}")
    
    return files


def build_project_index(projects_path: str) -> List[Dict[str, Any]]:
    """构建项目索引"""
    projects_root = Path(projects_path)
    
    if not projects_root.exists():
        raise FileNotFoundError(f"项目路径不存在: {projects_path}")
    
    projects = []
    project_dirs = [d for d in projects_root.iterdir() if d.is_dir()]
    
    print(f"找到 {len(project_dirs)} 个项目文件夹\n")
    
    for idx, project_dir in enumerate(project_dirs, 1):
        project_name = project_dir.name
        print(f"[{idx}/{len(project_dirs)}] 索引项目: {project_name}")
        
        project_date = extract_date_from_name(project_name)
        industry = detect_industry(project_name)
        ptype = detect_type(project_name)
        keywords = extract_keywords(project_name)
        files = scan_project_files(project_dir)
        
        project = {
            'id': f"proj_{idx:03d}",
            'name': project_name,
            'path': str(project_dir),
            'date': project_date,
            'industry': industry,
            'type': ptype,
            'keywords': keywords,
            'files': files,
            'file_count': sum(len(v) for v in files.values()),
            'indexed_at': datetime.now().isoformat()
        }
        
        projects.append(project)
    
    return projects


def save_index(projects: List[Dict[str, Any]]):
    """保存索引到文件"""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    index_data = {
        'version': '1.0',
        'created_at': datetime.now().isoformat(),
        'total_projects': len(projects),
        'projects': projects
    }
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n索引已保存到: {INDEX_FILE}")
    print(f"总项目数: {len(projects)}")


def print_statistics(projects: List[Dict[str, Any]]):
    """打印统计信息"""
    print("\n=== 索引统计 ===")
    
    # 按行业统计
    industries = {}
    for p in projects:
        ind = p['industry']
        industries[ind] = industries.get(ind, 0) + 1
    
    print("\n按行业分布:")
    for ind, count in sorted(industries.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ind}: {count} 个项目")
    
    # 按类型统计
    types = {}
    for p in projects:
        pt = p['type']
        types[pt] = types.get(pt, 0) + 1
    
    print("\n按类型分布:")
    for pt, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pt}: {count} 个项目")
    
    # 文件统计
    total_files = sum(p['file_count'] for p in projects)
    print(f"\n总文件数: {total_files}")
    
    if projects:
        avg_files = total_files / len(projects)
        print(f"平均每个项目: {avg_files:.1f} 个文件")


def main():
    print("=== 项目索引构建器 ===\n")
    
    try:
        config = load_config()
        projects_path = config['projects_path']
        
        print(f"项目路径: {projects_path}\n")
        
        projects = build_project_index(projects_path)
        save_index(projects)
        print_statistics(projects)
        print("\n✓ 索引构建完成!")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
