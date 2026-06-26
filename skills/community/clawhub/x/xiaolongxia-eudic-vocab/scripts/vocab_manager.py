#!/usr/bin/env python3
"""
欧路词典生词本管理器
支持：获取、添加、删除单词，管理分类
"""

import argparse
import json
import urllib.request
import urllib.error
from typing import List, Dict, Optional

BASE_URL = "https://api.frdic.com/api/open/v1"

class EudicVocabManager:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"NIS {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        """发送 HTTP 请求"""
        url = f"{BASE_URL}{endpoint}"
        if params:
            query = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{query}"
        
        req = urllib.request.Request(url, method=method)
        for k, v in self.headers.items():
            req.add_header(k, v)
        
        if data and method in ["POST", "PUT"]:
            req.data = json.dumps(data).encode('utf-8')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.read().decode()[:200]}"}
        except Exception as e:
            return {"error": str(e)}
    
    # ========== 分类管理 ==========
    def get_categories(self, language: str = "en") -> List[Dict]:
        """获取生词本分类列表"""
        result = self._request("GET", "/studylist/category", params={"language": language})
        return result.get("data", [])
    
    def add_category(self, name: str, language: str = "en") -> dict:
        """添加新分类"""
        return self._request("POST", "/studylist/category", data={
            "name": name,
            "language": language
        })
    
    def rename_category(self, category_id: str, new_name: str) -> dict:
        """重命名分类"""
        return self._request("PUT", f"/studylist/category/{category_id}", data={
            "name": new_name
        })
    
    def delete_category(self, category_id: str) -> dict:
        """删除分类"""
        return self._request("DELETE", f"/studylist/category/{category_id}")
    
    # ========== 单词管理 ==========
    def get_words(self, category_id: str = "0", language: str = "en", 
                  page: int = 1, page_size: int = 100) -> dict:
        """获取生词本单词"""
        return self._request("GET", "/studylist/words", params={
            "language": language,
            "category_id": category_id,
            "page": page,
            "page_size": page_size
        })
    
    def get_all_words(self, category_id: str = "0", language: str = "en") -> List[Dict]:
        """获取所有单词（自动翻页）"""
        all_words = []
        page = 1
        
        while True:
            result = self.get_words(category_id, language, page, 100)
            words = result.get("data", [])
            
            if not words:
                break
            
            all_words.extend(words)
            print(f"第{page}页: {len(words)} 个，累计: {len(all_words)}")
            
            if len(words) < 100:
                break
            page += 1
        
        return all_words
    
    def add_word(self, word: str, exp: str = "", phon: str = "", 
                 language: str = "en", category_id: str = "0") -> dict:
        """添加单词到生词本"""
        return self._request("POST", "/studylist/words", data={
            "language": language,
            "category_id": category_id,
            "word": word,
            "exp": exp,
            "phon": phon
        })
    
    def delete_word(self, word_id: str) -> dict:
        """从生词本删除单词"""
        return self._request("DELETE", f"/studylist/words/{word_id}")
    
    def delete_words_batch(self, word_ids: List[str]) -> dict:
        """批量删除单词"""
        return self._request("DELETE", "/studylist/words", data={
            "ids": word_ids
        })
    
    def get_word_detail(self, word_id: str) -> dict:
        """获取单词详情"""
        return self._request("GET", f"/studylist/words/{word_id}")


def main():
    parser = argparse.ArgumentParser(description="欧路词典生词本管理器")
    parser.add_argument("--token", help="API Token (NIS xxx)，如不填则从环境变量 EUDIC_TOKEN 读取")
    parser.add_argument("--action", choices=["list", "add", "delete", "categories", "detail"], 
                       required=True, help="操作类型")
    parser.add_argument("--word", help="单词")
    parser.add_argument("--exp", help="释义")
    parser.add_argument("--word-id", help="单词ID")
    parser.add_argument("--category-id", default="0", help="分类ID")
    parser.add_argument("--language", default="en", help="语言")
    
    args = parser.parse_args()
    
    # 优先从参数获取，其次环境变量
    token = args.token or os.environ.get("EUDIC_TOKEN")
    if not token:
        print("❌ 错误: 请提供 --token 或设置环境变量 EUDIC_TOKEN")
        sys.exit(1)
    
    manager = EudicVocabManager(token)
    
    if args.action == "list":
        print("正在获取所有单词...")
        words = manager.get_all_words(args.category_id, args.language)
        print(f"\n总计: {len(words)} 个单词")
        for w in words[:10]:
            print(f"  - {w.get('word')}: {w.get('exp', 'N/A')[:40]}...")
        if len(words) > 10:
            print(f"  ... 还有 {len(words)-10} 个")
    
    elif args.action == "categories":
        cats = manager.get_categories(args.language)
        print(f"分类列表 ({len(cats)} 个):")
        for c in cats:
            print(f"  - ID: {c.get('id')}, 名称: {c.get('name')}, 语言: {c.get('language')}")
    
    elif args.action == "add":
        if not args.word:
            print("错误: 需要提供 --word")
            return
        result = manager.add_word(args.word, args.exp, "", args.language, args.category_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "delete":
        if not args.word_id:
            print("错误: 需要提供 --word-id")
            return
        result = manager.delete_word(args.word_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "detail":
        if not args.word_id:
            print("错误: 需要提供 --word-id")
            return
        result = manager.get_word_detail(args.word_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
