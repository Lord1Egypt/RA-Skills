import argparse
import datetime
from Bio import Entrez
import json
import socket  # 导入 socket 用于设置全局超时

# 设置全局超时时间为 15 秒，防止脚本无期限卡死
socket.setdefaulttimeout(60)

# 请务必填入真实邮箱
Entrez.email = "chenghan_xiao@hotmail.com"

def get_journal_issn(query_name):
    """获取 ISSN，如果超时或失败则优雅地回退"""
    try:
        # 第一步：搜索期刊 ID
        handle = Entrez.esearch(db="journals", term=f"{query_name}[Journal Name]", retmax=1)
        record = Entrez.read(handle)
        handle.close()
        
        ids = record.get("IdList", [])
        if not ids: 
            return None, query_name
        
        # 第二步：获取期刊详情
        handle = Entrez.efetch(db="journals", id=ids[0], rettype="summary")
        summary = Entrez.read(handle)
        handle.close()
        
        issn = summary[0].get('ISSN', '')
        official_name = summary[0].get('Title', query_name)
        return issn, official_name
    except Exception as e:
        # 如果卡住或报错，打印错误并返回原始名称，确保主程序继续运行
        print(f"DEBUG: ISSN Lookup failed/timed out for {query_name}: {e}")
        return None, query_name

def fetch_pubmed_data(journals, days):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days)
    date_range = f'("{start_date.strftime("%Y/%m/%d")}"[EDAT] : "{today.strftime("%Y/%m/%d")}"[EDAT])'
    
    all_queries = []
    found_info = []

    for j in journals.split(','):
        j_name = j.strip()
        # 加入 ISSN 查询
        issn, official = get_journal_issn(j_name)
        if issn:
            all_queries.append(f'"{issn}"[IS]')
            found_info.append(f"{official} (ISSN:{issn})")
        else:
            # 回退方案：使用双引号包裹的期刊名
            all_queries.append(f'"{official}"[Journal]')
            found_info.append(official)
    
    query = f"({' OR '.join(all_queries)}) AND {date_range}"
    
    try:
        # 搜索 PMID
        search_handle = Entrez.esearch(db="pubmed", term=query, retmax=100, sort="pub_date")
        search_results = Entrez.read(search_handle)
        search_handle.close()
        
        id_list = search_results.get("IdList", [])
        if not id_list:
            return {"status": "success", "count": 0, "journals_found": found_info, "articles": []}

        # 抓取详情
        fetch_handle = Entrez.efetch(db="pubmed", id=",".join(id_list), rettype="xml", retmode="xml")
        records = Entrez.read(fetch_handle)
        fetch_handle.close()
        
        results = []
        for article in records['PubmedArticle']:
            medline = article['MedlineCitation']
            article_data = medline['Article']
            pmid = str(medline['PMID'])
            title = article_data.get('ArticleTitle', 'No Title')
            
            # 处理摘要
            abstract_parts = article_data.get('Abstract', {}).get('AbstractText', [])
            abstract = " ".join([str(part) for part in abstract_parts]) if abstract_parts else ""
            
            # 处理元数据
            authors = article_data.get('AuthorList', [])
            first_author = f"{authors[0]['LastName']} {authors[0]['ForeName']}" if authors else "Unknown"
            
            pub_date = article_data['Journal']['JournalIssue']['PubDate']
            year = pub_date.get('Year', str(today.year))

            results.append({
                "pmid": pmid,
                "year": year,
                "author": first_author,
                "title": title,
                "abstract": abstract
            })
        
        return {
            "status": "success",
            "count": len(results),
            "journals_found": found_info,
            "articles": results
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--journals", required=True)
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    print(json.dumps(fetch_pubmed_data(args.journals, args.days), ensure_ascii=False))
