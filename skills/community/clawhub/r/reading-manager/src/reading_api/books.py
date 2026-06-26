"""
书籍 API 接口
支持 Google Books API 和豆瓣 API
"""
import requests
import json


def search_google_books(query: str, api_key: str = None) -> list:
    """搜索 Google Books"""
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query, "maxResults": 10}
    if api_key:
        params["key"] = api_key
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        books = []
        for item in data.get("items", []):
            info = item.get("volumeInfo", {})
            books.append({
                "title": info.get("title"),
                "subtitle": info.get("subtitle"),
                "authors": info.get("authors", []),
                "publisher": info.get("publisher"),
                "published_date": info.get("publishedDate"),
                "description": info.get("description"),
                "page_count": info.get("pageCount"),
                "categories": info.get("categories", []),
                "isbn10": _get_isbn(info, "ISBN_10"),
                "isbn13": _get_isbn(info, "ISBN_13"),
                "cover_url": info.get("imageLinks", {}).get("thumbnail"),
            })
        return books
    except Exception as e:
        print(f"Google Books API 错误: {e}")
        return []


def search_by_isbn_google(isbn: str, api_key: str = None) -> dict:
    """通过 ISBN 搜索 Google Books"""
    url = f"https://www.googleapis.com/books/v1/volumes"
    params = {"q": f"isbn:{isbn}"}
    if api_key:
        params["key"] = api_key
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        items = data.get("items", [])
        if not items:
            return None
        
        info = items[0].get("volumeInfo", {})
        return {
            "title": info.get("title"),
            "subtitle": info.get("subtitle"),
            "authors": info.get("authors", []),
            "publisher": info.get("publisher"),
            "published_date": info.get("publishedDate"),
            "description": info.get("description"),
            "page_count": info.get("pageCount"),
            "categories": info.get("categories", []),
            "isbn10": _get_isbn(info, "ISBN_10"),
            "isbn13": _get_isbn(info, "ISBN_13"),
            "cover_url": info.get("imageLinks", {}).get("thumbnail"),
        }
    except Exception as e:
        print(f"Google Books API 错误: {e}")
        return None


def search_douban(query: str, api_key: str = None) -> list:
    """搜索豆瓣图书（需要 API Key）"""
    # 注意：豆瓣 API 需要申请，这里提供基础结构
    # 实际使用时需要替换为有效的 API endpoint
    print("豆瓣 API 需要申请使用，请先配置 API Key")
    return []


def search_by_isbn_douban(isbn: str, api_key: str = None) -> dict:
    """通过 ISBN 搜索豆瓣"""
    print("豆瓣 API 需要申请使用，请先配置 API Key")
    return None


def _get_isbn(volume_info: dict, isbn_type: str) -> str:
    """从 volumeInfo 中提取 ISBN"""
    identifiers = volume_info.get("industryIdentifiers", [])
    for identifier in identifiers:
        if identifier.get("type") == isbn_type:
            return identifier.get("identifier")
    return None
