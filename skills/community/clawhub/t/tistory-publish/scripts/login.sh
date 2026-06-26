#!/usr/bin/env bash
# login.sh — Tistory 카카오 로그인 세션 복구 스크립트
# publish.sh 실행 전 로그인 세션이 만료됐을 때 사용
#
# 사용:
#   bash scripts/login.sh --cred-file /path/to/credentials.json [--cdp-port 18800]
#
# 자격증명 파일 형식 (JSON 또는 key: value):
#   {"email": "...", "password": "..."}
#   또는
#   email: ...
#   password: ...
#
# 환경변수로도 지정 가능:
#   TISTORY_CRED_FILE=/path/to/credentials.json

set -euo pipefail

CDP_PORT=18800
CRED_FILE="${TISTORY_CRED_FILE:-}"

while [[ $# -gt 0 ]]; do
  case $1 in
    --cdp-port) CDP_PORT="$2"; shift 2 ;;
    --cred-file) CRED_FILE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$CRED_FILE" ]]; then
  echo "❌ 자격증명 파일 미지정"
  echo "   사용: bash login.sh --cred-file /path/to/credentials.json"
  echo "   또는: TISTORY_CRED_FILE=/path/to/cred.json bash login.sh"
  exit 1
fi

if [[ ! -f "$CRED_FILE" ]]; then
  echo "❌ 자격증명 파일 없음: $CRED_FILE"
  exit 1
fi

python3 - "$CDP_PORT" "$CRED_FILE" << 'PYTHON_SCRIPT'
import sys, json, time
CDP_PORT = sys.argv[1]
CRED_FILE = sys.argv[2]
CDP_URL = f"http://127.0.0.1:{CDP_PORT}"

with open(CRED_FILE) as f:
    content = f.read()
# Support both JSON and YAML-like (key: value) format
kakao_id = ""
kakao_pw = ""
try:
    cred = json.loads(content)
    kakao_id = cred.get("email") or cred.get("id") or ""
    kakao_pw = cred.get("password") or cred.get("pw") or ""
except json.JSONDecodeError:
    import re
    m_email = re.search(r'email:\s*(.+)', content)
    m_pw = re.search(r'password:\s*(.+)', content)
    if m_email: kakao_id = m_email.group(1).strip()
    if m_pw: kakao_pw = m_pw.group(1).strip()
if not kakao_id or not kakao_pw:
    print("❌ 자격증명 불완전 (email/password 필드 확인)")
    sys.exit(1)

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_URL)
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.new_page()

    print(f"[{time.strftime('%H:%M:%S')}] Tistory 로그인 페이지 이동...")
    page.goto("https://www.tistory.com/auth/login", wait_until="domcontentloaded", timeout=20000)

    login_domains = ["auth/login", "accounts.kakao.com", "logins.daum.net"]
    if not any(x in page.url for x in login_domains):
        print(f"✅ 이미 로그인됨 ({page.url})")
        sys.exit(0)

    # 카카오계정으로 로그인 버튼 클릭
    try:
        page.locator('a:has-text("카카오계정으로 로그인"), button:has-text("카카오계정으로 로그인")').first.click()
        page.wait_for_url(lambda url: "kakao" in url, timeout=10000)
    except Exception:
        pass  # 이미 카카오 폼이 바로 보이는 경우

    print(f"[{time.strftime('%H:%M:%S')}] 카카오 로그인 폼 입력...")
    page.locator('input[placeholder*="이메일"], input[placeholder*="아이디"], input[type="email"], input[name="loginId"]').first.fill(kakao_id)
    page.locator('input[type="password"]').first.fill(kakao_pw)
    page.locator('button[type="submit"], button:has-text("로그인")').first.click()
    page.wait_for_url(lambda url: not any(x in url for x in login_domains), timeout=15000)
    print(f"✅ 로그인 성공 → {page.url}")
    page.close()
PYTHON_SCRIPT
