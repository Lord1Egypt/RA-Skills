#!/usr/bin/env bash
# tistory-publish — 범용 티스토리 발행 스크립트 (OpenClaw Playwright CDP 기반)
#
# 사용법:
#   bash publish.sh --title "글 제목" --body-file body.html --category "카테고리"
#   bash publish.sh --template mk-review --article-title "기사 제목" --body-file body.html --banner banner.jpg
#
# 필수: --title, --body-file, --category
# 선택: --tags, --banner, --blog, --helper, --private, --template, --article-title, --cdp-port

set -euo pipefail

# ── 기본값 ──
TITLE=""
ARTICLE_TITLE=""
BODY_FILE=""
CATEGORY=""
TAGS=""
BANNER=""
BLOG=""
HELPER=""
TEMPLATE=""
PRIVATE=false
CDP_PORT="${TISTORY_CDP_PORT:-18800}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

log() { echo "[$(date +%H:%M:%S)] $*" >&2; }
fail() { echo "{\"success\":false,\"error\":\"$*\"}" ; exit 1; }

usage() {
  cat >&2 <<'EOF'
Usage:
  bash publish.sh --title "글 제목" --body-file body.html --category "카테고리"
  bash publish.sh --template mk-review --article-title "기사 제목" --body-file body.html --banner banner.jpg

Options:
  --template       템플릿 preset (mk-review, simple-post)
  --title          최종 제목
  --article-title  mk-review용 기사 제목 (자동 접두사 생성)
  --body-file      본문 HTML 파일
  --category       카테고리명
  --tags           쉼표 구분 태그
  --banner         배너 이미지 파일
  --blog           블로그 도메인 (예: bongman.tistory.com)
  --helper         JS helper 경로
  --cdp-port       OpenClaw Chrome CDP 포트 (기본: 18800)
  --private        비공개 발행
EOF
}

# ── 인자 파싱 ──
while [[ $# -gt 0 ]]; do
  case "$1" in
    --template)      TEMPLATE="$2"; shift 2;;
    --title)         TITLE="$2"; shift 2;;
    --article-title) ARTICLE_TITLE="$2"; shift 2;;
    --body-file)     BODY_FILE="$2"; shift 2;;
    --category)      CATEGORY="$2"; shift 2;;
    --tags)          TAGS="$2"; shift 2;;
    --banner)        BANNER="$2"; shift 2;;
    --blog)          BLOG="$2"; shift 2;;
    --helper)        HELPER="$2"; shift 2;;
    --cdp-port)      CDP_PORT="$2"; shift 2;;
    --private)       PRIVATE=true; shift;;
    -h|--help)       usage; exit 0;;
    *) echo "Unknown option: $1" >&2; usage; exit 1;;
  esac
done

# ── 템플릿 preset ──
if [[ -n "$TEMPLATE" ]]; then
  case "$TEMPLATE" in
    mk-review)
      if [[ -n "$ARTICLE_TITLE" && -z "$TITLE" ]]; then
        DOW_KR=$(python3 -c "from datetime import datetime;d=datetime.now();dow='월화수목금토일';print(dow[d.weekday()])")
        DATE_PREFIX=$(date "+%Y.%m.%d(${DOW_KR})")
        TITLE="[매경] ${DATE_PREFIX} - ${ARTICLE_TITLE}"
      fi
      [[ -z "$CATEGORY" ]] && CATEGORY="신문 리뷰"
      [[ -z "$BLOG" ]] && BLOG="bongman.tistory.com"
      ;;
    simple-post) ;;
    *) fail "unknown template: $TEMPLATE" ;;
  esac
fi

# ── 필수값 검증 ──
[[ -z "$TITLE" ]]     && fail "--title required"
[[ -z "$BODY_FILE" ]] && fail "--body-file required"
[[ -z "$CATEGORY" ]]  && fail "--category required"
[[ ! -f "$BODY_FILE" ]] && fail "body file not found: $BODY_FILE"
[[ -n "$BANNER" && ! -f "$BANNER" ]] && fail "banner file not found: $BANNER"
[[ "$TEMPLATE" == "mk-review" && -z "$BANNER" ]] && fail "--banner required for template mk-review"

if [[ -z "$HELPER" ]]; then
  HELPER="$SCRIPT_DIR/tistory-publish.js"
fi
[[ ! -f "$HELPER" ]] && fail "helper JS not found: $HELPER"

# ── 메인: Python Playwright CDP ──
log "Launching Playwright CDP publish (port=$CDP_PORT)"

python3 - "$CDP_PORT" "$BLOG" "$TITLE" "$BODY_FILE" "$CATEGORY" "$TAGS" "$BANNER" "$HELPER" "$PRIVATE" << 'PYTHON_SCRIPT'
import sys, json, time, os, re

CDP_PORT   = sys.argv[1]
BLOG       = sys.argv[2]
TITLE      = sys.argv[3]
BODY_FILE  = sys.argv[4]
CATEGORY   = sys.argv[5]
TAGS_STR   = sys.argv[6]
BANNER     = sys.argv[7]
HELPER_JS  = sys.argv[8]
PRIVATE    = sys.argv[9] == "true"

CDP_URL = f"http://127.0.0.1:{CDP_PORT}"
NEWPOST_URL = f"https://{BLOG}/manage/newpost/?type=post" if BLOG else "https://www.tistory.com/manage/newpost/?type=post"

def log(msg): print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr)
def fail(msg):
    print(json.dumps({"success": False, "error": msg}))
    sys.exit(1)

from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout

start = time.time()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_URL)

    # ── Step 1: 새 글 페이지 열기 ──
    log("Step 1: 새 글 페이지 열기")
    # 기존 탭 재사용 또는 새 탭
    page = None
    for ctx in browser.contexts:
        for pg in ctx.pages:
            if BLOG and BLOG in pg.url and "newpost" in pg.url:
                page = pg
                break
    if not page:
        ctx0 = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx0.new_page()

    page.goto(NEWPOST_URL, wait_until="domcontentloaded", timeout=30000)

    # 로그인 세션 확인
    _login_domains = ["auth/login", "accounts.kakao.com", "logins.daum.net", "kauth.kakao.com"]
    if any(x in page.url for x in _login_domains):
        fail(f"카카오 로그인 세션 만료. scripts/login.sh 로 먼저 로그인하세요. (redirected: {page.url})")

    # TinyMCE 대기
    log("  - tinymce 대기...")
    for i in range(20):
        ready = page.evaluate("typeof tinymce !== 'undefined' && tinymce.activeEditor && tinymce.activeEditor.initialized")
        if ready:
            break
        time.sleep(2)
    if not ready:
        fail("tinymce not ready after 40s")
    log("Step 1: 완료")

    # ── Helper JS 주입 (addScriptTag — CSP 우회) ──
    log("Injecting helper JS...")
    page.add_script_tag(path=HELPER_JS)
    time.sleep(1)
    if not page.evaluate("typeof insertContent === 'function'"):
        fail("helper JS injection failed")

    # ── Step 2: 카테고리 & 제목 ──
    log("Step 2: 카테고리 & 제목")
    page.evaluate("document.getElementById('category-btn').click()")
    time.sleep(0.5)
    cat_result = page.evaluate(f"""(() => {{
        const name = {json.dumps(CATEGORY)};
        const opts = document.querySelectorAll('[role=option]');
        for (const o of opts) {{
            const t = o.textContent.trim();
            if (t === name || t.replace(/^-\\s*/, '') === name || t.includes(name)) {{
                o.click();
                return 'ok: ' + t;
            }}
        }}
        return 'not found: ' + Array.from(opts).map(o => o.textContent.trim()).join('|');
    }})()""")
    if not cat_result.startswith("ok"):
        fail(f"category select failed: {cat_result}")

    page.evaluate(f"""(() => {{
        const t = document.getElementById('post-title-inp');
        if (!t) return 'no el';
        t.textContent = {json.dumps(TITLE)};
        t.dispatchEvent(new Event('input', {{bubbles:true}}));
        return 'ok';
    }})()""")
    log("Step 2: 완료")

    # ── Step 3: 본문 삽입 ──
    log("Step 3: 본문 삽입")
    body_html = open(BODY_FILE, 'r', encoding='utf-8').read()
    page.evaluate("""(html) => {
        tinymce.activeEditor.setContent(html);
        tinymce.activeEditor.setDirty(true);
        tinymce.activeEditor.save();
    }""", body_html)

    content_len = page.evaluate("tinymce.activeEditor.getContent().length")
    log(f"  - content length: {content_len}")
    if content_len < 100:
        fail(f"body too short ({content_len})")
    log("Step 3: 완료")

    # ── Step 4: 배너 업로드 ──
    if BANNER:
        log("Step 4: 배너 업로드")
        # visible한 첨부 버튼 찾기 — aria-label="첨부" 중 visible인 것
        uploaded = False
        try:
            # 메뉴 열기 (첨부 → 사진)
            page.evaluate("""(() => {
                const btns = document.querySelectorAll('[aria-label="첨부"]');
                for (const b of btns) {
                    if (b.offsetParent !== null) { b.click(); return 'clicked'; }
                }
                return 'not found';
            })()""")
            time.sleep(0.5)
            page.click('[role=menuitem]:has-text("사진")', timeout=3000)
            time.sleep(0.5)
            fi = page.query_selector('#openFile')
            if fi:
                fi.set_input_files(BANNER)
                time.sleep(4)
                uploaded = True
                log("  - 배너 파일 전송 완료")
            else:
                log("  ⚠️ #openFile not found after menu open")
        except Exception as e:
            log(f"  ⚠️ 배너 업로드 실패: {e}")

        if not uploaded:
            log("  ⚠️ 배너 업로드 실패 — 발행은 계속 진행")
        log(f"Step 4: {'완료' if uploaded else '⚠️ 미완료 (발행은 계속)'}")
    else:
        log("Step 4: 배너 생략")

    # ── Step 5: OG 카드 ──
    log("Step 5: OG 카드")
    og_urls = page.evaluate("typeof getOGPlaceholders === 'function' ? getOGPlaceholders() : []")
    log(f"  - OG URLs: {len(og_urls)}")
    for url in og_urls:
        page.evaluate(f"prepareOGPlaceholder('{url}')")
        time.sleep(0.5)
        page.keyboard.press("Enter")
        time.sleep(3)
        og_ok = page.evaluate("tinymce.activeEditor.getDoc().querySelector('figure[data-ke-type=\"opengraph\"]') ? 'yes' : 'no'")
        log(f"  - OG [{url[:40]}...]: {og_ok}")
    if og_urls:
        page.evaluate("typeof cleanupOGResiduals === 'function' && cleanupOGResiduals()")
    log("Step 5: 완료")

    # ── Step 6: 대표이미지 ──
    log("Step 6: 대표이미지")
    page.evaluate("typeof setRepresentImageFromEditor === 'function' && setRepresentImageFromEditor()")
    time.sleep(1)
    log("Step 6: 완료")

    # ── Step 7: 태그 ──
    if TAGS_STR:
        log("Step 7: 태그")
        tags = [t.strip() for t in TAGS_STR.split(',') if t.strip()]
        page.evaluate(f"typeof setTags === 'function' && setTags({json.dumps(tags)})")
        time.sleep(1)
        log("Step 7: 완료")
    else:
        log("Step 7: 태그 생략")

    # ── Step 8: 발행 ──
    log("Step 8: 발행")
    # 발행 직전 save 재실행 (빈 본문 방지)
    page.evaluate("tinymce.activeEditor.save()")
    ta_len = page.evaluate("document.getElementById('editor-tistory') ? document.getElementById('editor-tistory').value.length : -1")
    log(f"  - textarea sync check: {ta_len}")
    if ta_len < 100:
        fail(f"textarea too short before publish ({ta_len})")

    # 완료 버튼 — Playwright locator (first visible match)
    page.locator("button:has-text('완료')").first.click(timeout=5000)
    time.sleep(2)

    # 다이얼로그 대기
    for i in range(10):
        dlg = page.evaluate("document.querySelector('[role=dialog]') ? 'yes' : 'no'")
        if dlg == 'yes':
            break
        time.sleep(1)
    if dlg != 'yes':
        fail("publish dialog not found after 10s")

    if PRIVATE:
        page.evaluate("""(() => {
            const r = document.querySelector('input[type=radio][value="0"]');
            if (r) { r.click(); r.checked = true; r.dispatchEvent(new Event('change', {bubbles:true})); }
        })()""")
        time.sleep(0.5)
        page.evaluate("""(() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) { if (b.textContent.includes('비공개 저장')) { b.click(); return; } }
        })()""")
    else:
        page.evaluate("""(() => {
            const r = document.querySelector('input[type=radio][value="20"]');
            if (r) { r.click(); r.checked = true; r.dispatchEvent(new Event('change', {bubbles:true})); }
        })()""")
        time.sleep(0.5)
        page.evaluate("""(() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) { if (b.textContent.includes('공개 발행')) { b.click(); return; } }
        })()""")

    # 완료 대기 — 공개: manage/posts 리다이렉트 / 비공개: 다이얼로그 닫힘
    time.sleep(3)
    if PRIVATE:
        # 비공개 저장은 리다이렉트 안 함 — 다이얼로그 닫힘 확인
        for i in range(10):
            dlg_gone = page.evaluate("document.querySelector('[role=dialog]') ? 'open' : 'closed'")
            if dlg_gone == 'closed':
                break
            time.sleep(1)
        log(f"  - 비공개 저장 완료 (다이얼로그: {dlg_gone})")
    else:
        for i in range(15):
            if "/manage/posts" in page.url:
                break
            time.sleep(2)

    elapsed = int((time.time() - start) * 1000)
    final_url = page.url
    log(f"Step 8: 완료 — {final_url}")

    # ── Step 9: 공개 페이지 재검증 ──
    warning = None
    if not PRIVATE:
        log("Step 9: 공개 페이지 검증")
        import urllib.request
        # 최신 글 URL 추출
        post_url = page.evaluate("""(() => {
            const links = document.querySelectorAll('a');
            for (const a of links) {
                if (a.href && a.href.match(/tistory\\.com\\/\\d+$/)) return a.href;
            }
            return '';
        })()""")
        if post_url:
            log(f"  - 검증 URL: {post_url}")
            try:
                req = urllib.request.Request(post_url, headers={'User-Agent':'Mozilla/5.0'})
                html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8','ignore')
                m = re.search(r'<div[^>]+class="[^"]*tt_article[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
                if not m:
                    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
                text = re.sub('<[^>]+>', '', m.group(1) if m else '').strip() if m else ''
                vlen = len(text)
                log(f"  - 공개 페이지 본문 length: {vlen}")
                if vlen < 100:
                    warning = "public_body_empty"
                    log(f"  ⚠️ 본문 비어있음 ({vlen})")
            except Exception as e:
                log(f"  ⚠️ 검증 실패: {e}")

    result = {"success": True, "url": final_url, "elapsed_ms": elapsed, "private": PRIVATE}
    if warning:
        result["warning"] = warning
    print(json.dumps(result))
    browser.close()

PYTHON_SCRIPT

EXIT_CODE=$?
exit $EXIT_CODE
