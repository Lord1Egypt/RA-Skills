#!/usr/bin/env python3
"""
X (Twitter) Reader - 트윗 가져오기
RapidAPI Twitter API 사용
"""

import sys
import json
import re
import os

# API 설정
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")  # 환경 변수에서 API 키 로드
RAPIDAPI_HOST = "twitter-api45.p.rapidapi.com"

def extract_tweet_id(url_or_id):
    """URL 또는 ID에서 트윗 ID 추출"""
    if 'x.com' in url_or_id or 'twitter.com' in url_or_id:
        # https://x.com/username/status/1234567890
        match = re.search(r'status/(\d+)', url_or_id)
        if match:
            return match.group(1)
    # 숫자 ID
    if url_or_id.isdigit():
        return url_or_id
    return None

def fetch_tweet_rapidapi(tweet_id):
    """RapidAPI로 트윗 가져오기"""
    import requests
    
    if not RAPIDAPI_KEY:
        return {"error": "RAPIDAPI_KEY 환경 변수가 설정되지 않았습니다."}
    
    url = f"https://{RAPIDAPI_HOST}/tweet.php"
    querystring = {"id": tweet_id}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 응답 정리
        return {
            "id": tweet_id,
            "text": data.get("text", ""),
            "author": data.get("user", {}).get("name", ""),
            "username": data.get("user", {}).get("screen_name", ""),
            "created_at": data.get("created_at", ""),
            "likes": data.get("favorite_count", 0),
            "retweets": data.get("retweet_count", 0),
            "replies": data.get("reply_count", 0),
            "url": f"https://x.com/{data.get('user', {}).get('screen_name', '')}/status/{tweet_id}"
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"API 요청 실패: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "JSON 파싱 실패"}

def fetch_tweet_nitter(tweet_id, username):
    """Nitter 인스턴스로 트윗 가져오기 (묣료 대안)"""
    import requests
    from html.parser import HTMLParser
    
    nitter_instances = [
        "https://nitter.net",
        "https://nitter.it",
        "https://nitter.privacydev.net"
    ]
    
    for instance in nitter_instances:
        try:
            url = f"{instance}/{username}/status/{tweet_id}"
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            if response.status_code == 200:
                # 간단한 HTML 파싱
                html = response.text
                
                # 트윗 텍스트 추출 (메타 태그에서)
                import re
                text_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
                author_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
                
                if text_match:
                    return {
                        "id": tweet_id,
                        "text": text_match.group(1),
                        "author": author_match.group(1).split("(")[0].strip() if author_match else "Unknown",
                        "username": username,
                        "url": f"https://x.com/{username}/status/{tweet_id}",
                        "source": "nitter"
                    }
        except Exception:
            continue
    
    return {"error": "모든 Nitter 인스턴스 실패"}

def main():
    if len(sys.argv) < 2:
        print("사용법: x-reader.py <tweet_url_or_id>")
        print("예시: x-reader.py https://x.com/rlancemartin/status/2024573404888911886")
        sys.exit(1)
    
    input_str = sys.argv[1]
    tweet_id = extract_tweet_id(input_str)
    
    if not tweet_id:
        print(json.dumps({"error": "유효한 트윗 ID 또는 URL이 아닙니다."}, ensure_ascii=False))
        sys.exit(1)
    
    # 방법 1: RapidAPI (API 키 있을 때)
    if RAPIDAPI_KEY:
        result = fetch_tweet_rapidapi(tweet_id)
    else:
        # 방법 2: Nitter (묣료)
        username = "unknown"
        if 'x.com' in input_str or 'twitter.com' in input_str:
            match = re.search(r'x\.com/([^/]+)/status', input_str)
            if match:
                username = match.group(1)
        result = fetch_tweet_nitter(tweet_id, username)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
