#!/usr/bin/env python3
"""
토큰세이버 (TokenSaver) - AI 토큰 96% 절감
한국어 Context DB API 클라이언트
"""

import argparse
import json
import os
import requests
from typing import Optional, Dict, Any, List
from functools import lru_cache
import time

API_BASE = "https://api.tokensaver.ai"

class TokenSaver:
    """
    토큰세이버 - AI 토큰 96% 절감
    
    사용법:
        ts = TokenSaver(api_key="your_key")
        ts.save("project/alpha", "내용...")
        result = ts.search("프로젝트", level=0)  # 96% 절약
    """
    
    def __init__(self, api_key: Optional[str] = None, cache_ttl: int = 300):
        """
        Args:
            api_key: API Key (또는 TOKENSAVER_API_KEY 환경변수)
            cache_ttl: 캐시 유효시간 (초)
        """
        self.api_key = api_key or os.environ.get("TOKENSAVER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key 필요! TOKENSAVER_API_KEY 환경변수 설정 또는 생성자로 전달\n"
                "API Key 발급: https://tokensaver.ai"
            )
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self._cache_ttl = cache_ttl
        self._cache: Dict[str, tuple] = {}  # (data, timestamp)
    
    def _get_cached(self, key: str) -> Optional[Dict]:
        """캐시 조회"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self._cache_ttl:
                return data
        return None
    
    def _set_cached(self, key: str, data: Dict):
        """캐시 저장"""
        self._cache[key] = (data, time.time())
    
    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """API 요청 (에러 처리 강화)"""
        url = f"{API_BASE}{path}"
        try:
            response = requests.request(
                method, 
                url, 
                headers=self.headers, 
                timeout=30,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise ConnectionError("API 요청 시간 초과 (30초)")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise ValueError("API Key가 유효하지 않습니다")
            elif response.status_code == 429:
                raise ValueError("API 호출 한도 초과. 플랜을 확인하세요.")
            else:
                raise ConnectionError(f"API 오류: {e}")
    
    def save(self, uri: str, content: str, category: str = "memories") -> Dict[str, Any]:
        """
        메모리 저장
        
        Args:
            uri: 저장 경로 (예: "project/alpha", "memories/roadmap")
            content: 저장할 내용
            category: 카테고리 (memories, project, business 등)
        
        Returns:
            {"status": "success", "uri": "...", "tokens_saved": 123}
        """
        result = self._request("POST", "/v1/memory/save", json={
            "uri": uri,
            "content": content,
            "category": category
        })
        
        # 캐시 무효화
        self._cache.pop(f"list:{category}", None)
        self._cache.pop("list:all", None)
        
        return result
    
    def search(
        self, 
        query: str, 
        level: int = 0, 
        limit: int = 5,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        메모리 검색 - 토큰 절감!
        
        Args:
            query: 검색 쿼리
            level: 검색 레벨 (0=96%절약, 1=91%, 2=원본)
            limit: 결과 제한
            use_cache: 캐시 사용 여부
        
        Returns:
            {
                "query": "...",
                "level": 0,
                "token_estimate": "~50 tokens (96% 절약)",
                "results": [...]
            }
        """
        cache_key = f"search:{query}:{level}:{limit}"
        
        if use_cache:
            cached = self._get_cached(cache_key)
            if cached:
                return cached
        
        result = self._request("POST", "/v1/memory/search", json={
            "query": query,
            "level": level,
            "limit": limit
        })
        
        if use_cache:
            self._set_cached(cache_key, result)
        
        return result
    
    def list(self, category: Optional[str] = None, use_cache: bool = True) -> Dict[str, Any]:
        """
        저장된 메모리 목록
        
        Args:
            category: 카테고리 필터 (None이면 전체)
            use_cache: 캐시 사용 여부
        """
        cache_key = f"list:{category or 'all'}"
        
        if use_cache:
            cached = self._get_cached(cache_key)
            if cached:
                return cached
        
        params = {"category": category} if category else {}
        result = self._request("GET", "/v1/memory/list", params=params)
        
        if use_cache:
            self._set_cached(cache_key, result)
        
        return result
    
    def usage(self) -> Dict[str, Any]:
        """
        사용량 확인
        
        Returns:
            {
                "api_calls": 127,
                "tokens_saved": 48500,
                "plan": "pro",
                "remaining_credits": 873
            }
        """
        return self._request("GET", "/v1/usage")
    
    def clear_cache(self):
        """캐시 전체 삭제"""
        self._cache.clear()
    
    # === 편의 메서드 ===
    
    def quick_save(self, content: str, tag: str = "general") -> Dict[str, Any]:
        """빠른 저장 (자동 URI 생성)"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        uri = f"quick/{tag}/{timestamp}"
        return self.save(uri, content, category="quick")
    
    def find(self, keyword: str) -> List[Dict]:
        """간편 검색 (결과만 반환)"""
        result = self.search(keyword, level=0, limit=10)
        return result.get("results", [])


# === CLI ===

def main():
    parser = argparse.ArgumentParser(
        description="토큰세이버 - AI 토큰 96% 절약",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  token-saver save "project/alpha" --content "이 프로젝트는..."
  token-saver search "프로젝트" --level 0
  token-saver list --category memories
  token-saver usage
        """
    )
    parser.add_argument("--api-key", help="API Key (또는 TOKENSAVER_API_KEY 환경변수)")
    parser.add_argument("--no-cache", action="store_true", help="캐시 비활성화")
    
    subparsers = parser.add_subparsers(dest="command", help="명령어")
    
    # save
    save_parser = subparsers.add_parser("save", help="메모리 저장")
    save_parser.add_argument("uri", help="저장할 URI (예: project/alpha)")
    save_parser.add_argument("--content", "-c", required=True, help="저장할 내용")
    save_parser.add_argument("--category", default="memories", help="카테고리")
    
    # quick-save
    quick_parser = subparsers.add_parser("quick-save", help="빠른 저장")
    quick_parser.add_argument("content", help="저장할 내용")
    quick_parser.add_argument("--tag", default="general", help="태그")
    
    # search
    search_parser = subparsers.add_parser("search", help="메모리 검색")
    search_parser.add_argument("query", help="검색 쿼리")
    search_parser.add_argument("--level", "-l", type=int, default=0, 
                              help="검색 레벨 (0=96%절약, 1=91%, 2=원본)")
    search_parser.add_argument("--limit", type=int, default=5, help="결과 제한")
    
    # list
    list_parser = subparsers.add_parser("list", help="메모리 목록")
    list_parser.add_argument("--category", help="카테고리 필터")
    
    # usage
    subparsers.add_parser("usage", help="사용량 확인")
    
    # clear-cache
    subparsers.add_parser("clear-cache", help="캐시 삭제")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    ts = TokenSaver(api_key=args.api_key)
    
    if args.command == "save":
        result = ts.save(args.uri, args.content, args.category)
        print(f"✅ 저장 완료: {args.uri}")
        print(f"📊 예상 절약 토큰: {result.get('tokens_saved', 'N/A')}")
    
    elif args.command == "quick-save":
        result = ts.quick_save(args.content, args.tag)
        print(f"✅ 빠른 저장 완료: {result.get('uri', 'N/A')}")
    
    elif args.command == "search":
        result = ts.search(args.query, args.level, args.limit, use_cache=not args.no_cache)
        print(f"🔍 검색: '{args.query}' (레벨 {args.level})")
        print(f"📊 {result.get('token_estimate', 'N/A')}")
        print("\n📝 결과:")
        for r in result.get("results", []):
            print(f"  - {r.get('uri')}: {r.get('summary', '')[:50]}...")
    
    elif args.command == "list":
        result = ts.list(args.category, use_cache=not args.no_cache)
        print(f"📂 메모리 목록 ({result.get('total', 0)}개)")
        for m in result.get("memories", []):
            print(f"  - {m.get('uri')} ({m.get('created')})")
    
    elif args.command == "usage":
        result = ts.usage()
        print(f"📊 사용량")
        print(f"  API 호출: {result.get('api_calls', 0)}")
        print(f"  절약 토큰: {result.get('tokens_saved', 0):,}")
        print(f"  플랜: {result.get('plan', 'unknown')}")
        print(f"  남은 크레딧: {result.get('remaining_credits', 0)}")
    
    elif args.command == "clear-cache":
        ts.clear_cache()
        print("✅ 캐시 삭제 완료")


if __name__ == "__main__":
    main()