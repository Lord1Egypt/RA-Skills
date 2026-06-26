#!/usr/bin/env python3
"""
项目匹配器 - 基于需求关键词匹配相关历史项目

这个脚本会根据用户输入的关键词，从项目索引中找到最相关的项目。
匹配算法考虑关键词匹配度、项目新鲜度和完整度。

用法:
    python match_projects.py "智能家居 IoT 科技感"
    python match_projects.py "金融 手机银行" --max 5
    python match_projects.py "电商" --json
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# 索引文件路径
SKILL_ROOT = Path(__file__).parent.parent
INDEX_FILE = SKILL_ROOT / "data" / "project_index.json"


def load_index() -> Dict[str, Any]:
    """加载项目索引"""
    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            f"项目索引不存在: {INDEX_FILE}\n"
            f"请先运行: python scripts/index_projects.py"
        )
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_relevance(project: Dict[str, Any], query_keywords: List[str]) -> float:
    """计算项目与查询的相关度
    
    评分规则:
    - 项目名称完全匹配: +3.0
    - 行业匹配: +2.5
    - 类型匹配: +2.0
    - 关键词匹配: +1.5
    - 其他文本匹配: +1.0
    - 项目新鲜度: +0.5~1.0
    - 项目完整度: +0.5~1.0
    """
    score = 0.0
    
    # 提取项目的所有文本信息
    project_text = ' '.join([
        project['name'],
        project['industry'],
        project['type'],
        ' '.join(project['keywords'])
    ]).lower()
    
    # 计算关键词匹配度
    for keyword in query_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in project_text:
            # 完全匹配得分更高
            if keyword_lower in project['name'].lower():
                score += 3.0
            elif keyword_lower == project['industry'].lower():
                score += 2.5
            elif keyword_lower == project['type'].lower():
                score += 2.0
            elif keyword_lower in [k.lower() for k in project['keywords']]:
                score += 1.5
            else:
                score += 1.0
    
    # 考虑项目新鲜度（越新越好）
    if project['date'] != "未知":
        try:
            year = int(project['date'][:4])
            if year >= 2024:
                score += 1.0
            elif year >= 2020:
                score += 0.5
        except:
            pass
    
    # 考虑项目完整度（文件越多越好）
    file_count = project['file_count']
    if file_count > 10:
        score += 1.0
    elif file_count > 5:
        score += 0.5
    
    return score


def match_projects(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """匹配相关项目"""
    # 加载索引
    index_data = load_index()
    projects = index_data['projects']
    
    # 分词（简单按空格分割）
    query_keywords = [k.strip() for k in query.split() if k.strip()]
    
    if not query_keywords:
        print("错误: 查询关键词为空")
        return []
    
    # 计算每个项目的相关度
    scored_projects = []
    for project in projects:
        score = calculate_relevance(project, query_keywords)
        if score > 0:
            scored_projects.append({
                'project': project,
                'score': score
            })
    
    # 按相关度排序
    scored_projects.sort(key=lambda x: x['score'], reverse=True)
    
    # 返回 Top N
    return scored_projects[:max_results]


def print_results(results: List[Dict[str, Any]]):
    """打印匹配结果"""
    if not results:
        print("未找到相关项目")
        return
    
    print(f"\n找到 {len(results)} 个相关项目:\n")
    
    for idx, item in enumerate(results, 1):
        project = item['project']
        score = item['score']
        
        print(f"{idx}. {project['name']}")
        print(f"   相关度: {score:.1f}")
        print(f"   行业: {project['industry']} | 类型: {project['type']}")
        print(f"   日期: {project['date']}")
        print(f"   路径: {project['path']}")
        print(f"   文件数: {project['file_count']}")
        
        # 显示关键文件
        if project['files']['design_docs']:
            print(f"   设计文档: {', '.join(project['files']['design_docs'][:3])}")
        
        print()


def main():
    if len(sys.argv) < 2:
        print("用法: python match_projects.py <查询关键词> [--max N] [--json]")
        print("示例: python match_projects.py '智能家居 IoT 科技感'")
        print("      python match_projects.py '金融 银行' --max 5")
        print("      python match_projects.py '电商' --json")
        return 1
    
    query = sys.argv[1]
    max_results = 5
    output_json = False
    
    # 解析参数
    if '--max' in sys.argv:
        try:
            max_idx = sys.argv.index('--max')
            max_results = int(sys.argv[max_idx + 1])
        except:
            print("警告: --max 参数无效，使用默认值 5")
    
    if '--json' in sys.argv:
        output_json = True
    
    print(f"查询: {query}")
    print(f"最大结果数: {max_results}")
    
    try:
        results = match_projects(query, max_results)
        
        if not output_json:
            print_results(results)
        
        # 输出 JSON 格式（供程序调用）
        if output_json:
            output = {
                'query': query,
                'total': len(results),
                'results': [
                    {
                        'id': item['project']['id'],
                        'name': item['project']['name'],
                        'path': item['project']['path'],
                        'industry': item['project']['industry'],
                        'type': item['project']['type'],
                        'date': item['project']['date'],
                        'score': item['score'],
                        'files': item['project']['files']
                    }
                    for item in results
                ]
            }
            print("\n=== JSON 输出 ===")
            print(json.dumps(output, ensure_ascii=False, indent=2))
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n错误: {e}")
        return 1
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
