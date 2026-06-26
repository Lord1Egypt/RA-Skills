import os
import json
import requests
from datetime import datetime
import markdown
import hashlib

# 配置
TAVILY_API_KEY = "your-tavily-api-key"  # 需要替换为实际的 API Key
KNOWLEDGE_BASE_DIR = r"D:\code\openclaw_lakeskill\files\tavily_news"
SEARCH_QUERIES = [
    "水务设备 新品发布",
    "雷达液位计 技术突破",
    "水质监测 行业新闻",
    "流量计 最新技术",
    "液位计 市场趋势"
]
MAX_RESULTS = 5
TIME_RANGE = "year"
INCLUDE_DOMAINS = ["watertech.com", "instrumentationtools.com", "processindustryforum.com"]


def tavily_search(query, max_results=5, time_range="year", include_domains=None):
    """调用 Tavily API 进行搜索"""
    url = "https://api.tavily.com/search"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "time_range": time_range,
        "include_domains": include_domains,
        "include_answer": True,
        "include_snippets": True,
        "include_images": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Tavily 搜索失败 {query}: {e}")
        return None


def generate_markdown(result, query):
    """将搜索结果转换为 Markdown 格式"""
    md_content = f"# {query}\n\n"
    md_content += f"## 搜索时间\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # 添加 AI 总结
    if "answer" in result and result["answer"]:
        md_content += f"## AI 总结\n{result['answer']}\n\n"
    
    # 添加搜索结果
    if "results" in result:
        for i, item in enumerate(result["results"], 1):
            md_content += f"## 结果 {i}\n"
            md_content += f"### 标题\n{item.get('title', '无标题')}\n\n"
            md_content += f"### 链接\n{item.get('url', '无链接')}\n\n"
            md_content += f"### 摘要\n{item.get('content', '无摘要')}\n\n"
            if "snippet" in item and item["snippet"]:
                md_content += f"### 关键片段\n{item['snippet']}\n\n"
            md_content += "---\n\n"
    
    return md_content


def save_to_knowledge_base(content, query):
    """将 Markdown 内容保存到知识库"""
    # 确保目录存在
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = query.replace(" ", "_")[:50]
    filename = f"{timestamp}_{safe_query}.md"
    file_path = os.path.join(KNOWLEDGE_BASE_DIR, filename)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已保存到知识库: {filename}")
        return file_path
    except Exception as e:
        print(f"保存文件失败 {filename}: {e}")
        return None


def update_knowledge_base():
    """更新知识库"""
    results = []
    
    for query in SEARCH_QUERIES:
        print(f"正在搜索: {query}")
        
        # 调用 Tavily API
        search_result = tavily_search(query, MAX_RESULTS, TIME_RANGE, INCLUDE_DOMAINS)
        
        if search_result:
            # 生成 Markdown
            md_content = generate_markdown(search_result, query)
            
            # 保存到知识库
            file_path = save_to_knowledge_base(md_content, query)
            
            if file_path:
                results.append({
                    "query": query,
                    "file_path": file_path,
                    "timestamp": datetime.now().isoformat(),
                    "results_count": len(search_result.get("results", []))
                })
        
        print()
    
    return results


def on_demand_update(user_query):
    """按需更新：当用户查询包含特定关键词时触发"""
    # 检查是否包含触发关键词
    trigger_words = ["最新", "最近", "2026", "今年"]
    for word in trigger_words:
        if word in user_query:
            print(f"检测到触发词 '{word}'，正在进行按需更新...")
            
            # 提取相关查询
            device_keywords = ["液位计", "水尺", "流量计", "水质传感器"]
            relevant_query = user_query
            
            # 调用 Tavily API
            search_result = tavily_search(relevant_query, max_results=3, time_range="month")
            
            if search_result:
                # 生成 Markdown
                md_content = generate_markdown(search_result, relevant_query)
                
                # 保存到知识库
                file_path = save_to_knowledge_base(md_content, relevant_query)
                
                if file_path:
                    return {
                        "success": True,
                        "message": "知识库已更新最新信息",
                        "file_path": file_path
                    }
            
            break
    
    return {
        "success": False,
        "message": "未触发按需更新"
    }


def main():
    """主函数"""
    print("开始 Tavily 知识库更新...")
    
    results = update_knowledge_base()
    
    print("\n更新完成!")
    print(f"成功更新 {len(results)} 个查询")
    
    for result in results:
        print(f"  - {result['query']}: {result['file_path']}")


if __name__ == "__main__":
    main()