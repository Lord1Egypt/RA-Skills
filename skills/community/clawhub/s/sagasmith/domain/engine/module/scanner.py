"""
模组文件扫描与解析函数库
"""

DEPRECATED: file-based persistence. Use the campaign database instead.

This module exists only for backward compatibility with older dnd-engine
workflows. NanoBot stores all campaign state in the SQL database via
CampaignSnapshotService / CampaignService / ModuleProgressService.
No new code should call this module.
import os
import re

MODULES_DIR = 'modules'


def scan_modules():
    """
    扫描 modules/ 目录，返回可用模组清单
    
    返回:
        list[dict]: 每个模组包含:
            - name: str 模组名
            - chapters: list[str] 章节文件名列表
            - chapter_count: int 章节数
            - files: list[str] 完整文件路径
    """
    if not os.path.isdir(MODULES_DIR):
        return []
    
    files = os.listdir(MODULES_DIR)
    md_files = [f for f in files if f.endswith('.md')]
    
    # 通过文件名前缀分组识别不同模组
    modules = {}
    for fn in md_files:
        name = _identify_module(fn)
        if name not in modules:
            modules[name] = []
        modules[name].append(fn)
    
    result = []
    for name, chapter_files in sorted(modules.items()):
        result.append({
            "name": name,
            "chapters": sorted(chapter_files),
            "chapter_count": len(chapter_files),
            "files": sorted([os.path.join(MODULES_DIR, f) for f in chapter_files]),
        })
    
    return result


def _identify_module(filename):
    """
    从文件名识别所属模组名称
    
    规则:
        - 去掉章节标记部分（Ch.X, Chapter X, 第X章）
        - 剩余部分作为模组名
    
    参数:
        filename: str - 文件名
    
    返回:
        str: 模组名称
    """
    # 去掉 .md
    name = filename.replace('.md', '')
    # 去掉常见章节标记
    for pattern in [r'\s*-\s*(?:Ch\.?\s*)?\d+', r'\s*第\d+章\s*',
                    r'\s*Chapter\s+\d+', r'\s*Ch\.\s*\d+']:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    return name.strip()


def get_module_level_range(module_files):
    """
    从模组文件内容中读取等级范围
    
    参数:
        module_files: list[str] - 模组文件路径列表
    
    返回:
        dict: {"min": int, "max": int} 或 None
    """
    for fp in module_files:
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'(\d+)\s*(?:级|级)\s*(?:到|至|→|~)\s*(\d+)\s*级', content)
            if match:
                return {"min": int(match.group(1)), "max": int(match.group(2))}
        except Exception:
            continue
    return None


def read_chapter(module_name, chapter_num):
    """
    读取指定模组的指定章节文件内容
    
    参数:
        module_name: str - 模组名
        chapter_num: int - 章节编号
    
    返回:
        dict: {"content": str, "filename": str} 或 None
    """
    modules = scan_modules()
    for mod in modules:
        if mod['name'] == module_name:
            for fn in mod['files']:
                # 匹配章节编号
                fname = os.path.basename(fn)
                if re.search(rf'(?:Ch\.?\s*)?{chapter_num}(?:\s|\.|$|-)', fname, re.IGNORECASE):
                    with open(fn, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return {"content": content, "filename": fn}
    return None


def build_module_structure(module_name):
    """
    构建模组结构信息（不写入文件，返回结构数据供主系统使用）
    
    参数:
        module_name: str - 模组名
    
    返回:
        dict: 模组结构信息
    """
    modules = scan_modules()
    for mod in modules:
        if mod['name'] == module_name:
            level_range = get_module_level_range(mod['files'])
            return {
                "name": module_name,
                "chapters": mod['chapters'],
                "chapter_count": mod['chapter_count'],
                "level_range": level_range,
            }
    return None
