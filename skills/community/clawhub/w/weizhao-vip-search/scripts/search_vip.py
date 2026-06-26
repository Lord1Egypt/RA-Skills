import argparse
import requests
import json
import urllib.parse
import sys

def search_vip(keyword, cookie):
    """
    通过唯品会接口搜索关键字商品
    注意：接口 URL 可能由于唯品会的系统升级而发生变化，如果请求未返回商品，请您在使用中更新这里的 URL。
    """
    # 这里我们使用一个典型的唯品会关键字建议或搜索API接口作为示例
    encoded_keyword = urllib.parse.quote(keyword)
    
    # 获取搜索结果的可能API之一 (此处为占位符和可能接口，建议后续如有抓包可在此替换精准API)
    url = f"https://category.vip.com/ajax/getSuggest.php?keyword={encoded_keyword}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://category.vip.com/suggest.php?keyword={encoded_keyword}',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 尝试将结果转换为JSON
        try:
            data = response.json()
            if data:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print("未得到有效的 JSON 商品数据或内容为空。")
        except json.JSONDecodeError:
            # 如果不是 JSON 格式，则返回部分纯文本内容以供调试或提取
            print("API返回的数据不是标准的JSON格式。部分响应内容：")
            print(response.text[:1000])
            
    except requests.exceptions.RequestException as e:
        print(f"请求唯品会接口失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search VIP.com products by keyword using API")
    parser.add_argument('--keyword', type=str, required=True, help="The keyword to search for")
    parser.add_argument('--cookie', type=str, required=True, help="Cookie string obtained from a logged-in VIP.com session")
    
    args = parser.parse_args()
    
    search_vip(args.keyword, args.cookie)
