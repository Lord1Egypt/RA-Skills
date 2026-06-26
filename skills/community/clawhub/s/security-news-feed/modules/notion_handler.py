# modules/notion_handler.py
"""
Notion API를 사용하여 데이터베이스를 관리하는 모듈입니다.
- 페이지 생성, 중복 확인, 오래된 항목 삭제, 마크다운 파싱 등을 담당합니다.
"""
import requests
import json
import datetime
import mimetypes
import re
import sys
import os
import time  # ← 이 줄 추가
import threading

# markdown2 import 제거 - PublisherService에서 처리
from bs4 import BeautifulSoup

# 마커 제거 모듈 임포트
from .notion_markers import remove_markers

# Add parent directory to Python path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 다른 모듈 및 설정 파일에서 필요한 요소들을 가져옵니다.
# 상위 디렉토리의 config.py에서 필요한 설정값을 임포트합니다.
from config import NOTION_API_TOKEN, CVE_DATABASE_ID, BOANISSUE_DATABASE_ID, GUIDE_DATABASE_ID
from .utils import send_slack_message
from .analysis.cache_manager import URLCacheManager

# Initialize URL Cache
url_cache = URLCacheManager()

# 캐시 동기화 상태 추적
_cache_synced = False
_cache_sync_lock = threading.Lock() if hasattr(__import__('threading'), 'Lock') else None

def sync_cache_from_notion(database_id: str = None, force: bool = False) -> bool:
    """
    Notion DB의 모든 URL을 로컬 캐시에 동기화합니다.
    
    Args:
        database_id: 동기화할 DB ID (기본값: BOANISSUE_DATABASE_ID)
        force: 강제 재동기화 여부
        
    Returns:
        bool: 동기화 성공 여부
    """
    global _cache_synced
    
    # 이미 동기화되었으면 스킵 (force=True면 무시)
    if not force and _cache_synced:
        return True
    
    if database_id is None:
        database_id = BOANISSUE_DATABASE_ID
    
    try:
        print(f"[Notion] URL 캐시 동기화 시작 (DB: {database_id[:20]}...)")
        
        result = url_cache.sync_from_notion(
            database_id=database_id,
            notion_token=NOTION_API_TOKEN
        )
        
        if result.get('errors', 0) == 0 or result.get('synced', 0) > 0:
            _cache_synced = True
            print(f"[Notion] ✅ 캐시 동기화 완료: {result.get('synced', 0)}개 URL 추가")
            return True
        else:
            print(f"[Notion] ⚠️ 캐시 동기화 실패")
            return False
            
    except Exception as e:
        print(f"[Notion] 캐시 동기화 중 오류: {e}")
        return False

# Tistory 관련 import 제거 - PublisherService에서 처리


# data_source_id 캐시를 위한 전역 딕셔너리
# data_source_id 및 properties 캐시를 위한 전역 딕셔너리
_data_source_cache = {}

MULTIPART_CHUNK_SIZE = 10 * 1024 * 1024  # 10MB
MULTIPART_THRESHOLD = 20 * 1024 * 1024   # 20MB (싱글/멀티 결정 기준)

def get_data_source_info(database_id, headers):
    """
    database_id로부터 첫 번째 data_source_id와 properties를 조회하고 캐시합니다.
    (2025-09-03 API 버전 필수)
    
    반환: (data_source_id, properties) 튜플 또는 (None, None)
    """
    global _data_source_cache
    
    # 캐시 확인
    if database_id in _data_source_cache:
        # print(f"[CACHE HIT] data_source_id 캐시에서 조회: {database_id}")
        return _data_source_cache[database_id]
    
    # print(f"🔄 data_source_id 조회 시도 (DB: {database_id})")
    
    # 1단계: 데이터베이스 정보 조회
    db_url = f"https://api.notion.com/v1/databases/{database_id}"
    data_source_id = None
    
    try:
        db_info_resp = requests.get(db_url, headers=headers, timeout=30)
        
        if db_info_resp.status_code == 200:
            response_json = db_info_resp.json()
            data_sources = response_json.get("data_sources", [])
            
            if data_sources and len(data_sources) > 0:
                data_source_id = data_sources[0].get("id")
                
                if not data_source_id:
                    err_msg = f"DB 조회는 성공했으나 data_sources[0].id를 찾을 수 없습니다."
                    print(f"[ERROR] {err_msg}")
                    send_slack_message(f"[ERROR] {err_msg}")
                    return None, None
            else:
                err_msg = f"DB 조회는 성공했으나, 'data_sources' 배열이 비어있습니다. (API 권한 '연결' 확인)"
                print(f"[ERROR] {err_msg}")
                print(f"[DEBUG] 응답 (일부): {db_info_resp.text[:500]}")
                send_slack_message(f"[ERROR] {err_msg}")
                return None, None
        else:
            err_msg = f"data_source_id 조회 실패 (DB 조회): Status {db_info_resp.status_code} - {db_info_resp.text}"
            print(f"[ERROR] {err_msg}")
            send_slack_message(f"[ERROR] {err_msg}")
            return None, None
    
    except Exception as e:
        err_msg = f"data_source_id 조회 중 예외 발생: {e}"
        print(f"[ERROR] {err_msg}")
        send_slack_message(f"[ERROR] {err_msg}")
        return None, None
    
    # 2단계: data_source_id로부터 properties 조회 (Retry Logic Added)
    # print(f"🔄 Properties 조회 시도 (DS: {data_source_id})")
    
    props = {}
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            ds_url = f"https://api.notion.com/v1/data_sources/{data_source_id}"
            ds_info_resp = requests.get(ds_url, headers=headers, timeout=30)
            
            if ds_info_resp.status_code == 200:
                response_json = ds_info_resp.json()
                props = response_json.get("properties", {})
                
                if not props:
                    err_msg = f"data_source({data_source_id}) 조회는 200 OK였으나, 'properties' 키를 찾을 수 없습니다."
                    print(f"Notion 중복 확인 중: {err_msg}")
                    send_slack_message(f"[ERROR] {err_msg}")
                    return None, None
                
                # ✅ 성공: 캐시에 저장하고 반환
                # print(f"✅ data_source_id ({data_source_id}) 및 Properties 획득 성공")
                _data_source_cache[database_id] = (data_source_id, props)
                return data_source_id, props

            elif ds_info_resp.status_code == 429:
                retry_after = 2 ** (attempt + 1)
                # print(f"⚠️ data_source 조회 429 Rate Limit. {retry_after}초 후 재시도... (DS: {data_source_id})")
                time.sleep(retry_after)
                continue

            else:
                err_msg = f"data_source({data_source_id}) 속성 조회 실패: Status {ds_info_resp.status_code} - {ds_info_resp.text}"
                print(f"Notion 중복 확인 중: {err_msg}")
                send_slack_message(f"[ERROR] {err_msg}")
                return None, None
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                # print(f"⚠️ data_source 조회 중 네트워크 에러. 재시도 중... ({e})")
                time.sleep(2)
                continue
            else:
                err_msg = f"data_source({data_source_id}) 속성 조회 중 예외 발생: {e}"
                print(f"Notion 중복 확인 중: {err_msg}")
                send_slack_message(f"[ERROR] {err_msg}")
                return None, None
        
        except Exception as e:
            err_msg = f"data_source({data_source_id}) 속성 조회 중 알 수 없는 예외: {e}"
            print(f"Notion 중복 확인 중: {err_msg}")
            send_slack_message(f"[ERROR] {err_msg}")
            return None, None
    
    return None, None

def parse_markdown_to_notion_blocks(markdown_text):
    """
    입력된 마크다운 형식의 텍스트를 Notion 페이지에 적합한 블록 객체 리스트로 변환합니다.
    헤딩, 목록, 인용, 코드 블록 등을 인식하며, 각 블록 내 텍스트는 2000자 제한에 맞춰 분할됩니다.
    """
    blocks = []
    if not markdown_text or not markdown_text.strip():
        blocks.append({
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "상세 내용이 제공되지 않았습니다."}}]}
        })
        return blocks

    current_paragraph_lines = []
    max_text_length = 1950  # Notion의 텍스트 제한(2000자)보다 약간 여유 있게 설정

    def create_rich_text_array(text_content):
        """
        텍스트 내의 마크다운 스타일(굵게, 기울임, 코드, 링크)을 파싱하여 Notion rich_text 객체 리스트로 변환합니다.
        ✅ [추가] <br> 태그를 줄바꿈으로 처리 (테이블 셀 내 줄바꿈 지원)
        """
        if not text_content:
            return []
        
        # <br> 태그를 \n으로 변환 (대소문자 무관, 닫는 태그 포함)
        text_content = re.sub(r'<br\s*/?>', '\n', text_content, flags=re.IGNORECASE)
        
        rich_text_list = []
        # 정규표현식: 코드(`...`) > 굵게(**...**) > 기울임(*...*) > 링크([text](url))
        # 주의: 중첩은 완벽하게 처리되지 않을 수 있음
        pattern = re.compile(r'(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]]+\]\([^)]+\))')
        parts = pattern.split(text_content)
        
        for part in parts:
            if not part:
                continue
            
            # 코드 (`...`)
            if part.startswith('`') and part.endswith('`') and len(part) > 2:
                content = part[1:-1]
                rich_text_list.append({
                    "type": "text",
                    "text": {"content": content},
                    "annotations": {"code": True}
                })
            # 굵게 (**...**)
            elif part.startswith('**') and part.endswith('**') and len(part) > 4:
                content = part[2:-2]
                rich_text_list.append({
                    "type": "text",
                    "text": {"content": content},
                    "annotations": {"bold": True}
                })
            # 기울임 (*...*)
            elif part.startswith('*') and part.endswith('*') and len(part) > 2:
                content = part[1:-1]
                rich_text_list.append({
                    "type": "text",
                    "text": {"content": content},
                    "annotations": {"italic": True}
                })
            # 링크 ([...](...))
            elif part.startswith('[') and part.endswith(')') and '](' in part:
                try:
                    split_idx = part.rfind('](')
                    link_text = part[1:split_idx]
                    link_url = part[split_idx+2:-1]
                    rich_text_list.append({
                        "type": "text",
                        "text": {
                            "content": link_text,
                            "link": {"url": link_url}
                        }
                    })
                except:
                    rich_text_list.append({"type": "text", "text": {"content": part}})
            else:
                # 일반 텍스트 - 줄바꿈(\n)이 있으면 분리
                if '\n' in part:
                    lines = part.split('\n')
                    for idx, line in enumerate(lines):
                        if line:  # 빈 줄은 건너뜀
                            rich_text_list.append({"type": "text", "text": {"content": line}})
                        # 마지막 줄이 아니면 줄바꿈 추가
                        if idx < len(lines) - 1:
                            rich_text_list.append({"type": "text", "text": {"content": "\n"}})
                else:
                    rich_text_list.append({"type": "text", "text": {"content": part}})
        
        # [Fix] Merge adjacent "text" objects to avoid exceeding Notion's 100 items limit
        merged_list = []
        if not rich_text_list:
            return []
            
        current_obj = rich_text_list[0]
        
        for i in range(1, len(rich_text_list)):
            next_obj = rich_text_list[i]
            
            # Merge if both are plain text (no annotations/links)
            if (current_obj["type"] == "text" and 
                next_obj["type"] == "text" and
                not current_obj.get("annotations") and 
                not next_obj.get("annotations") and
                not current_obj["text"].get("link") and 
                not next_obj["text"].get("link")):
                
                # Check length limit (Notion 2000 chars per text object)
                if len(current_obj["text"]["content"]) + len(next_obj["text"]["content"]) < 2000:
                    current_obj["text"]["content"] += next_obj["text"]["content"]
                    continue
            
            merged_list.append(current_obj)
            current_obj = next_obj
            
        merged_list.append(current_obj)
        
        return merged_list

    def split_text_and_create_blocks(block_type, text_content, block_specific_data=None):
        generated_blocks = []
        if text_content is None: text_content = ""

        # Notion 텍스트 제한(2000자)에 맞춰 분할
        while True:
            part = text_content[:max_text_length]
            text_content = text_content[max_text_length:]

            block_content_data = {"rich_text": create_rich_text_array(part)}

            if block_type == "code" and block_specific_data:
                block_content_data["language"] = block_specific_data.get("language", "plain text")

            generated_blocks.append({"object": "block", "type": block_type, block_type: block_content_data})

            if not text_content: break
        return generated_blocks

    def flush_paragraph_buffer():
        if current_paragraph_lines:
            paragraph_text = "\n".join(current_paragraph_lines).strip()
            if paragraph_text:
                # ✅ [수정] 2000자 분할을 위해 split_text_and_create_blocks 함수 사용
                blocks.extend(split_text_and_create_blocks("paragraph", paragraph_text))
            current_paragraph_lines.clear()

    lines = markdown_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith("|"):
            flush_paragraph_buffer()
            table_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            
            # 테이블 파싱 및 블록 생성
            if len(table_lines) >= 2:
                # 헤더 파싱
                header_row = [cell.strip() for cell in table_lines[0].strip('|').split('|')]
                table_width = len(header_row)
                
                # 구분선(2번째 줄) 확인 및 데이터 행 시작 위치 결정
                start_row_idx = 1
                if set(table_lines[1]).issubset({'|', '-', ' ', ':'}):
                    start_row_idx = 2
                
                # 데이터 행 파싱
                data_rows = []
                for row_line in table_lines[start_row_idx:]:
                    cells = [cell.strip() for cell in row_line.strip('|').split('|')]
                    # 셀 개수 보정
                    if len(cells) < table_width:
                        cells.extend([""] * (table_width - len(cells)))
                    elif len(cells) > table_width:
                        cells = cells[:table_width]
                    data_rows.append(cells)
                
                # Notion 테이블 블록 생성
                table_rows_blocks = []
                
                # 헤더 행 블록
                header_cells_objs = [create_rich_text_array(cell) for cell in header_row]
                table_rows_blocks.append({
                    "type": "table_row",
                    "table_row": {"cells": header_cells_objs}
                })
                
                # 데이터 행 블록들
                for row_cells in data_rows:
                    row_cells_objs = [create_rich_text_array(cell) for cell in row_cells]
                    table_rows_blocks.append({
                        "type": "table_row",
                        "table_row": {"cells": row_cells_objs}
                    })
                
                # 테이블 블록 추가
                blocks.append({
                    "object": "block",
                    "type": "table",
                    "table": {
                        "table_width": table_width,
                        "has_column_header": True,
                        "has_row_header": False,
                        "children": table_rows_blocks
                    }
                })
                # i는 이미 증가했으므로 continue
                continue
            else:
                # 테이블 형식이 아니면(줄이 1개 등) 다시 처리하도록 i를 되돌리거나 텍스트로 추가
                # 여기서는 그냥 텍스트로 추가
                blocks.extend(split_text_and_create_blocks("paragraph", "\n".join(table_lines)))
                continue

        if line.startswith("#### "):
            flush_paragraph_buffer()
            # Notion은 heading_3까지만 지원하므로 heading_3으로 매핑
            blocks.extend(split_text_and_create_blocks("heading_3", line[5:]))
        elif line.startswith("### "):
            flush_paragraph_buffer()
            blocks.extend(split_text_and_create_blocks("heading_3", line[4:]))
        elif line.startswith("## "):
            flush_paragraph_buffer()
            blocks.extend(split_text_and_create_blocks("heading_2", line[3:]))
        elif line.startswith("# "):
            flush_paragraph_buffer()
            blocks.extend(split_text_and_create_blocks("heading_1", line[2:]))
        elif line.strip().startswith("- ") or line.strip().startswith("* "):
            flush_paragraph_buffer()
            content = line.strip()[2:]
            blocks.extend(split_text_and_create_blocks("bulleted_list_item", content))
        elif re.match(r"^\s*\d+\.\s", line):
            flush_paragraph_buffer()
            content = re.sub(r"^\s*\d+\.\s", "", line)
            blocks.extend(split_text_and_create_blocks("numbered_list_item", content))
        elif line.startswith("> "):
            flush_paragraph_buffer()
            quote_lines = [line[2:]]
            while i + 1 < len(lines) and lines[i+1].rstrip().startswith("> "):
                i += 1
                quote_lines.append(lines[i].rstrip()[2:])
            blocks.extend(split_text_and_create_blocks("quote", "\n".join(quote_lines)))
        elif line.startswith("```"):
            flush_paragraph_buffer()
            language = line[3:].strip().lower() or "plain text"
            
            LANGUAGE_ALIASES = {
                "js": "javascript", "ts": "typescript", "py": "python",
                "sh": "shell", "bash": "shell", "yml": "yaml",
                "cs": "c#", "cpp": "c++", "text": "plain text",
                "txt": "plain text", "none": "plain text", "": "plain text"
            }
            language = LANGUAGE_ALIASES.get(language, language)
            
            NOTION_SUPPORTED_LANGUAGES = {
                "abap", "abc", "agda", "arduino", "ascii art", "assembly", "bash",
                "basic", "bnf", "c", "c#", "c++", "clojure", "coffeescript", "coq",
                "css", "dart", "dhall", "diff", "docker", "ebnf", "elixir", "elm",
                "erlang", "f#", "flow", "fortran", "gherkin", "glsl", "go", "graphql",
                "groovy", "haskell", "hcl", "html", "idris", "java", "javascript",
                "json", "julia", "kotlin", "latex", "less", "lisp", "livescript",
                "llvm ir", "lua", "makefile", "markdown", "markup", "matlab",
                "mathematica", "mermaid", "nix", "notion formula", "objective-c",
                "ocaml", "pascal", "perl", "php", "plain text", "powershell",
                "prolog", "protobuf", "purescript", "python", "r", "racket", "reason",
                "ruby", "rust", "sass", "scala", "scheme", "scss", "shell", "smalltalk",
                "solidity", "sql", "swift", "toml", "typescript", "vb.net", "verilog",
                "vhdl", "visual basic", "webassembly", "xml", "yaml", "java/c/c++/c#"
            }
            if language not in NOTION_SUPPORTED_LANGUAGES:
                language = "plain text"
            
            code_block_lines = []
            i += 1
            while i < len(lines) and not lines[i].rstrip() == "```":
                code_block_lines.append(lines[i])
                i += 1
            code_content = "\n".join(code_block_lines)
            blocks.extend(split_text_and_create_blocks("code", code_content, {"language": language}))
        elif not line.strip():
            flush_paragraph_buffer()
        else:
            current_paragraph_lines.append(line)
        i += 1

    flush_paragraph_buffer()

    if not blocks:
        blocks.append({
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "처리할 수 있는 상세 내용이 없습니다."}}]}
        })
    return blocks


def create_notion_page(title, content, url, date, category_, details=None, files=None, DATABASE_ID=None):
    """
    Notion 데이터베이스에 새 페이지를 생성합니다.
    (2025-09-03 마이그레이션 + 파일 업로드 기능 완성)
    
    ✅ 파일 처리를 GUIDE_DATABASE_ID에서만 실행
    ✅ all_children_blocks에 모든 콘텐츠(디테일 + 파일) 포함
    """
    # Normalize URL
    if url:
        url = url_cache.normalize_url(url)
    
    try:
        today = datetime.datetime.now()
        post_date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        if  DATABASE_ID in [BOANISSUE_DATABASE_ID, CVE_DATABASE_ID]:
            if post_date_obj < (today - datetime.timedelta(days=90)):
                print(f"[SKIP] '{title}'은(는) 90일 이전의 항목이므로 추가하지 않습니다.")
                return
    
    except ValueError as e:
        print(f"[ERROR] 날짜 형식 오류: {date} - {e}")
        send_slack_message(f"[ERROR] Notion 페이지 생성 중 날짜 형식 오류: {title} - {date} ({e})")
        return
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }
    
    content_for_property = content[:1940] + '...' if len(content) > 1950 else content
    all_children_blocks = []
    
    # ============================================================
    # 1단계: 마크다운 디테일 추가 (모든 DB 공통)
    # ============================================================
    if details:
        print(f"📝 상세 내용 추가 (마커 제거 후 파싱)")
        # 마커 제거 후 Notion 블록으로 변환
        details_clean = remove_markers(details)
        all_children_blocks.extend(parse_markdown_to_notion_blocks(details_clean))
    
    # ============================================================
    # 4단계: data_source_id 및 properties 획득
    # ============================================================
    data_source_id, db_props = get_data_source_info(DATABASE_ID, headers)
    
    if not data_source_id or not db_props:
        print("Notion 페이지 생성 중: data_source_id 또는 properties 획득에 실패")
        return

    # DB 속성에서 title과 date 찾기
    title_prop_name = None
    date_prop_name = None

    # print("\n[DEBUG] 데이터베이스 속성 정보:")
    for pn, pinfo in db_props.items():
        # print(f" - 속성: {pn}, 타입: {pinfo.get('type')}")
        if pinfo.get('type') == 'title':
            title_prop_name = pn
            # print(f" → title 속성 발견: {pn}")
        if pinfo.get('type') == 'date':
            date_prop_name = pn
            # print(f" → date 속성 발견: {pn}")
    
    if not title_prop_name:
        err_msg = f"Notion DB({DATABASE_ID})에서 'title' 타입 속성을 찾을 수 없습니다."
        print(f"[ERROR] {err_msg}")
        send_slack_message(f"[ERROR] {err_msg}")
        return
    
    # ============================================================
    # 5단계: 페이지 페이로드 생성 (data 변수 설정)
    # ============================================================
    if DATABASE_ID in [BOANISSUE_DATABASE_ID, CVE_DATABASE_ID]:
        
        # --- ✅ [수정] 2단계: 파일 업로드 (BOANISSUE DB 추가) ---
        if files:
            print(f"📁 파일 {len(files)}개 처리 시작 (BOANISSUE DB)")
            
            for file_info in files:
                try:
                    file_name = file_info.get('name')
                    file_path = file_info.get('path')
                    
                    print(f" 📄 처리 중: {file_name}")
                    
                    if not file_path or not os.path.exists(file_path):
                        print(f" ❌ 파일 경로 없음 또는 존재하지 않음")
                        continue
                    
                    file_id = upload_file_to_notion(file_path, file_name)
                    
                    if not file_id:
                        print(f" ❌ 파일 ID 획득 실패: {file_name}")
                        continue
                    
                    # [Fix] 확장자 기반 블록 타입 자동 결정
                    ext = os.path.splitext(file_name)[1].lower()
                    is_image_ext = ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']
                    
                    if is_image_ext:
                        file_block = {
                            "object": "block",
                            "type": "image",
                            "image": { "type": "file_upload", "file_upload": {"id": file_id} }
                        }
                    else:
                        file_block = {
                            "object": "block",
                            "type": "file",
                            "file": { "type": "file_upload", "file_upload": {"id": file_id} }
                        }
                    
                    all_children_blocks.append(file_block)
                    print(f" ✅ 파일 블록 추가 완료: {file_name}")
                
                except Exception as e:
                    print(f" ❌ 파일 처리 오류: {str(e)}")
                    # import traceback
                    # traceback.print_exc()
                    continue
            
            print(f"📁 파일 처리 완료: {len(files)}개 파일 처리 시도")

        # --- ✅ [수정] BOANISSUE / CVE의 'tag' 또는 'category' 속성 동적 탐색 ---
        tag_prop_type = None
        tag_prop_name = None
        
        # 'tag' 또는 'category'라는 이름의 속성을 우선 검색
        if 'tag' in db_props:
            tag_prop_name = 'tag'
            tag_prop_type = db_props['tag'].get('type')
        elif 'category' in db_props:
            tag_prop_name = 'category'
            tag_prop_type = db_props['category'].get('type')
        else:
            # 둘 다 없으면, 'select' 또는 'multi_select' 타입의 다른 속성 검색
            for pn, pinfo in db_props.items():
                if pinfo.get('type') in ('select', 'multi_select'):
                    tag_prop_name = pn
                    tag_prop_type = pinfo.get('type')
                    break
        
        if tag_prop_name:
            print(f" → tag/category 속성 발견: {tag_prop_name} (타입: {tag_prop_type})")
        else:
            print(f" [WARN] 'tag'/'category' 속성을 찾지 못했습니다.")

        # --- BOANISSUE / CVE DB 속성 설정 ---
        properties = {
            title_prop_name: {"title": [{"text": {"content": title}}]},
            "content": {"rich_text": [{"type": "text", "text": {"content": content_for_property}}]},
            "url": {"url": url if url and url.strip() else None},
            # [제거] "tag": {"multi_select": [{"name": category_}]}
        }
        
        if date_prop_name:
            properties[date_prop_name] = {"date": {"start": date}}
        
        # ✅ [수정] 동적으로 찾은 속성 이름과 타입으로 카테고리 추가
        if category_ and tag_prop_name:
            # 콤마로 분리하여 리스트 생성
            categories = [c.strip() for c in category_.split(',') if c.strip()]
            
            if tag_prop_type == 'select':
                # select는 하나만 선택 가능하므로 첫 번째 항목 사용
                if categories:
                    properties[tag_prop_name] = {"select": {"name": categories[0]}}
            elif tag_prop_type == 'multi_select':
                # multi_select는 여러 개 선택 가능
                multi_select_options = [{"name": c} for c in categories]
                properties[tag_prop_name] = {"multi_select": multi_select_options}
            else:
                print(f" [WARN] 카테고리 속성({tag_prop_name}) 타입이 'select' 또는 'multi_select'가 아님 (타입: {tag_prop_type}). 카테고리 미지정.")

        
        # --- BOANISSUE / CVE DB 페이로드 생성 ---
        data = {
            "parent": {"type": "data_source_id", "data_source_id": data_source_id},
            "properties": properties,
            "children": all_children_blocks[:100] # ✅ details만 포함됨
        }
    
    elif DATABASE_ID == GUIDE_DATABASE_ID:
        
        # --- ✅ [수정] 2단계: 파일 업로드 (GUIDE DB 전용) ---
        if files:
            print(f"📁 파일 {len(files)}개 처리 시작 (GUIDE DB 전용)")
            
            for file_info in files:
                try:
                    file_name = file_info.get('name')
                    file_path = file_info.get('path')
                    
                    print(f" 📄 처리 중: {file_name}")
                    print(f" 📍 경로: {file_path}")
                    
                    if not file_path or not os.path.exists(file_path):
                        print(f" ❌ 파일 경로 없음 또는 존재하지 않음")
                        # [DEBUG] 디렉토리 내용 확인
                        try:
                            parent_dir = os.path.dirname(file_path)
                            if os.path.exists(parent_dir):
                                print(f" [DEBUG] 디렉토리 ({parent_dir}) 내용:")
                                for f in os.listdir(parent_dir):
                                    f_path = os.path.join(parent_dir, f)
                                    print(f"   - {f} (size: {os.path.getsize(f_path)})")
                            else:
                                print(f" [DEBUG] 부모 디렉토리가 존재하지 않습니다: {parent_dir}")
                        except Exception as debug_e:
                            print(f" [DEBUG] 디렉토리 조회 중 오류: {debug_e}")
                        continue
                    
                    print(f" ✅ 파일 존재 확인")
                    
                    file_id = upload_file_to_notion(file_path, file_name)
                    
                    if not file_id:
                        print(f" ❌ 파일 ID 획득 실패: {file_name}")
                        continue
                    
                    # [Fix] 확장자 기반 블록 타입 자동 결정
                    ext = os.path.splitext(file_name)[1].lower()
                    is_image_ext = ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']
                    
                    if is_image_ext:
                        file_block = {
                            "object": "block",
                            "type": "image",
                            "image": { "type": "file_upload", "file_upload": {"id": file_id} }
                        }
                    else:
                        file_block = {
                            "object": "block",
                            "type": "file",
                            "file": { "type": "file_upload", "file_upload": {"id": file_id} }
                        }
                    
                    all_children_blocks.append(file_block)
                    print(f" ✅ 파일 블록 추가 완료: {file_name}")
                
                except Exception as e:
                    print(f" ❌ 파일 처리 오류: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            print(f"📁 파일 처리 완료: {len(files)}개 파일 처리 시도")
        
        # --- GUIDE DB 속성 설정 ---
        tag_prop_type = None
        tag_prop_name = 'tag'
        
        if 'tag' in db_props:
            tag_prop_type = db_props['tag'].get('type')
            tag_prop_name = 'tag'
        else:
            for pn, pinfo in db_props.items():
                if pinfo.get('type') in ('select', 'multi_select') and \
                   ('tag' in pn.lower() or 'category' in pn.lower() or '분류' in pn.lower()):
                    tag_prop_name = pn
                    tag_prop_type = pinfo.get('type')
                    break
                    
        properties = {
            title_prop_name: {"title": [{"text": {"content": title}}]},
            "url": {"url": url if url and url.strip() else None}  # ✅ [수정] URL 속성 추가
        }
        
        if date_prop_name:
            properties[date_prop_name] = {"date": {"start": date}}
        else:
            err_msg = f"GUIDE DB({DATABASE_ID})에서 'date' 타입 속성을 찾지 못했습니다!"
            print(f"[ERROR] {err_msg}")
            send_slack_message(f"[ERROR] {err_msg}")
            return
        
        if category_:
            # 콤마로 분리하여 리스트 생성
            categories = [c.strip() for c in category_.split(',') if c.strip()]
            
            if tag_prop_type == 'select':
                if categories:
                    properties[tag_prop_name] = {"select": {"name": categories[0]}}
            else:
                multi_select_options = [{"name": c} for c in categories]
                properties[tag_prop_name] = {"multi_select": multi_select_options}
        
        # --- GUIDE DB 페이로드 생성 ---
        data = {
            "parent": {"type": "data_source_id", "data_source_id": data_source_id},
            "properties": properties,
            "children": all_children_blocks[:100] # ✅ details + files 포함됨
        }
    
    # ============================================================
    # 3단계: 블록 분할 (100개씩 배치 처리) - 위치 이동
    # ============================================================
    initial_children = all_children_blocks[:100]
    remaining_children = all_children_blocks[100:]
    
    print(f"📊 블록 현황: 초기 {len(initial_children)}개, 나머지 {len(remaining_children)}개")
    
    # data 페이로드의 children을 최종 분할본으로 업데이트
    if data:
        data["children"] = initial_children
    else:
        err_msg = f"Notion DB ID({DATABASE_ID})에 대한 'properties' 구성이 없습니다."
        print(f"[ERROR] {err_msg}")
        send_slack_message(f"[ERROR] {err_msg}")
        return
    
    # ============================================================
    # 6단계: 페이지 생성 API 호출
    # ============================================================
    # ============================================================
    # 6단계: 페이지 생성 API 호출 (Retry Logic Added)
    # ============================================================
    max_retries = 3
    page_id = None
    
    for attempt in range(max_retries):
        try:
            # [Fix] Increase timeout for heavy payloads (files)
            response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data, timeout=60)
            
            if response.status_code == 200:
                page_data = response.json()
                page_id = page_data.get("id")
                
                print(f"✅ Notion 페이지 생성 완료: {title}")
                print(f"   ID: {page_id}")
                print(f"   URL: https://www.notion.so/{page_id.replace('-', '')}")
                # Cache the URL
                url_cache.add(url)
                break # 성공 시 루프 탈출
                
            elif response.status_code == 429:
                retry_after = 2 ** (attempt + 1)
                print(f"⚠️ 429 Too Many Requests. {retry_after}초 후 재시도... ({attempt+1}/{max_retries})")
                time.sleep(retry_after)
                continue
                
            else:
                # 400 등 기타 에러는 재시도하지 않음
                error_message = f"노션 페이지 생성 에러: {title} - Status {response.status_code}"
                try:
                    error_details = response.json()
                    error_message += f"\n   Response: {json.dumps(error_details, indent=2, ensure_ascii=False)}"
                except:
                    error_message += f"\n   Response: {response.text}"
                    
                print(f"❌ {error_message}")
                send_slack_message(f"[ERROR] {error_message}")
                return False # 실패 반환

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"⚠️ 네트워크 에러 발생. 재시도 전 중복 확인... ({e})")
                
                # [Fix] Idempotency Check: Check if page was created despite timeout
                if url:
                    is_dup = Duplicate_check(url, DATABASE_ID)
                    if is_dup == 1:
                        print(f"✅ (Idempotency) 페이지가 이미 생성되어 있습니다. 재시도 중단.")
                        return True # 간주: 성공함

                time.sleep(2)
                continue
            else:
                network_error_message = f"노션 페이지 생성 중 네트워크 에러 (최대 재시도 초과): {title} - {e}"
                print(f"❌ {network_error_message}")
                send_slack_message(f"[ERROR] {network_error_message}")
                return False
        
        except Exception as e:
            unknown_error_message = f"노션 페이지 생성 중 알 수 없는 에러: {title} - {e}"
            print(f"❌ {unknown_error_message}")
            send_slack_message(f"[ERROR] {unknown_error_message}")
            return False

    if not page_id:
        return False

    # ============================================================
    # 7단계: 나머지 블록 추가 (100개 초과 시)
    # ============================================================
    if remaining_children and page_id:
        print(f"📦 남은 {len(remaining_children)}개의 블록을 추가합니다...")

        block_append_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        
        # ✅ [수정] 마지막 블록 ID 추적 (순차적 추가)
        last_block_id = None

        # 초기 블록들의 마지막 블록 ID 찾기
        if initial_children:
            # API 호출로 현재 페이지의 블록 조회
            fetch_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
            fetch_params = {"page_size": 100}

            try:
                fetch_response = requests.get(fetch_url, headers=headers, params=fetch_params, timeout=10)
                if fetch_response.status_code == 200:
                    fetch_data = fetch_response.json()
                    blocks_res = fetch_data.get("results", [])
                    if blocks_res:
                        last_block_id = blocks_res[-1].get("id")
                        print(f" 마지막 블록 ID 획득: {last_block_id}")
            except:
                print(f" ⚠️ 마지막 블록 ID 조회 실패, 기본 추가 진행")

        # ✅ [수정] 나머지 블록을 배치로 추가 (after 지정)
        for idx, i in enumerate(range(0, len(remaining_children), 100)):
            batch = remaining_children[i:i + 100]

            append_payload = {
                "children": batch,
                # ✅ [핵심] after 지정 - 기존 블록 뒤에 추가
                "after": last_block_id if last_block_id else None
            }

            # None 제거
            if append_payload["after"] is None:
                del append_payload["after"]

            try:
                print(f" 🔄 배치 {idx + 1} 추가 중 (블록 {i+1}~{min(i+100, len(remaining_children))})...")

                append_response = requests.patch(
                    block_append_url,
                    headers=headers,
                    json=append_payload,
                    timeout=20
                )

                if append_response.status_code == 200:
                    append_data = append_response.json()

                    # ✅ [중요] 마지막 블록 ID 업데이트 (다음 배치에서 사용)
                    added_blocks = append_data.get("results", [])
                    if added_blocks:
                        last_block_id = added_blocks[-1].get("id")
                        print(f"  ✅ {len(added_blocks)}개 블록 추가 완료 (마지막 ID: {last_block_id})")
                    else:
                        total_added = min(i + 100, len(remaining_children))
                        print(f"  ✅ {total_added}/{len(remaining_children)} 블록 추가 완료")

                else:
                    error_message = f"Notion 블록 추가 에러 ({page_id}): {append_response.status_code}"
                    print(f" ❌ {error_message}")
                    # 블록 추가 실패는 페이지 생성 실패로 보지 않음 (부분 성공)
                    send_slack_message(f"[WARN] {error_message}")
                    break
                
            except requests.exceptions.RequestException as e:
                print(f" ❌ Notion 블록 추가 중 네트워크 에러: {e}")
                break
            
        print(f"📦 블록 추가 작업 완료")

    return True  # 성공 시 True 반환


# ============================================================================
# [핵심 함수 2] 크롤링 로직 - 중복 확인 → 조건부 페이지 생성
# ============================================================================
def process_articles_with_duplicate_check(articles, DATABASE_ID):
    """
    크롤링된 기사 처리 (중복 확인 후 생성)
    
    ✅ Issue 1 해결: 중복 페이지 생성 방지
    ✅ Issue 2 해결: 파일 업로드 기능 포함
    """
    
    if not articles:
        print("처리할 기사가 없습니다.")
        return
    
    print(f"\n{'='*70}")
    print(f"🚀 {len(articles)}개 기사 처리 시작")
    print(f"{'='*70}\n")
    
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    for idx, article in enumerate(articles, 1):
        url = article.get('url')
        title = article.get('title')
        content = article.get('summary', '')
        date = article.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
        category = article.get('category', 'Unknown')
        details = article.get('details', '')
        files = article.get('files')  # ✅ 파일 리스트
        
        print(f"\n[{idx}/{len(articles)}] 처리 중: {title[:50]}...")
        print(f"{'─'*70}")
        
        # ============================================================
        # 1단계: 중복 확인
        # ============================================================
        print(f"🔍 Notion에서 중복 확인 중...")
        dup_result = Duplicate_check(url, DATABASE_ID)
        
        if dup_result == -1:
            # 오류 발생
            print(f"❌ 중복 확인 중 오류 발생")
            send_slack_message(f"[ERROR] 중복 확인 실패: {title}")
            error_count += 1
            continue
        
        elif dup_result == 1:
            # ✅ 중복 발견 - 페이지 생성 스킵
            print(f"⏭️  건너뜀 (이미 존재하는 항목)")
            print(f"   URL: {url}")
            send_slack_message(f"[SKIP] 중복 항목 건너뜀: {title}")
            skipped_count += 1
            continue
        
        # dup_result == 0: 중복 없음
        
        # ============================================================
        # 2단계: 중복 없음 - 페이지 생성 (파일 포함)
        # ============================================================
        print(f"✅ 새로운 항목 - Notion에 업로드 중...")
        
        if files:
            print(f"📁 {len(files)}개 파일 함께 업로드")
        
        create_notion_page(
            title=title,
            content=content,
            url=url,
            date=date,
            category_=category,
            details=details,
            files=files,  # ✅ 파일 리스트 전달
            DATABASE_ID=DATABASE_ID
        )
        
        processed_count += 1
        print(f"✅ 처리 완료: {title[:50]}...")
    
    # ============================================================
    # 결과 요약
    # ============================================================
    print(f"\n{'='*70}")
    print(f"📊 처리 결과 요약")
    print(f"{'='*70}")
    print(f"✅ 새로 추가됨: {processed_count}개")
    print(f"⏭️  건너뜀 (중복): {skipped_count}개")
    print(f"❌ 오류: {error_count}개")
    print(f"📁 총 처리: {len(articles)}개\n")
    
    send_slack_message(
        f"[SUMMARY] Notion 업로드 완료\n"
        f"✅ 새로 추가됨: {processed_count}개\n"
        f"⏭️  건너뜀 (중복): {skipped_count}개\n"
        f"❌ 오류: {error_count}개"
    )


def Duplicate_check(key_to_check, DATABASE_ID, date=None, filenames=None):
    """
    Notion 데이터베이스에서 URL로 중복을 확인합니다.
    
    ✅ Local Cache First -> Notion API Fallback
    ✅ Fail-Safe: API Error returns 1 (Duplicate)
    ✅ 강력한 URL 정규화 적용 (tracking parameter 제거)
    ✅ 다양한 URL 변형으로 중복 검사
    """
    
    if not key_to_check or not key_to_check.strip():
        return 0  # 빈 URL은 신규로 처리
    
    # 1. URL 정규화
    normalized_url = url_cache.normalize_url(key_to_check)
    
    # 2. 로컬 캐시 확인 (빠른 경로)
    if url_cache.exists(normalized_url):
        return 1  # 캐시에서 중복 발견
    
    # 3. Notion API 확인
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }

    # 속성 정보 획득
    data_source_id, props = get_data_source_info(DATABASE_ID, headers)
    if not data_source_id or not props:
        print("[ERROR] data_source_id 또는 properties 획득 실패 (Fail-Safe: 중복으로 간주)")
        return 1  # Fail-Safe

    endpoint = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"

    # URL 속성 찾기
    url_prop_name = None
    for prop_name, prop_info in props.items():
        if prop_info.get("type") == "url":
            url_prop_name = prop_name
            break

    if not url_prop_name:
        print(f"[ERROR] DB에 'url' 속성이 없습니다")
        send_slack_message(f"[ERROR] DB({DATABASE_ID})에 'url' 속성이 없습니다")
        return 1  # Fail-Safe

    # 4. 여러 URL 변형으로 검색 (정규화된 URL + 원본 URL)
    urls_to_check = list(set([
        normalized_url,           # 정규화된 URL
        key_to_check.strip(),     # 원본 URL
    ]))
    urls_to_check = [u for u in urls_to_check if u]  # 빈 값 제거
    
    try:
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # 각 URL 변형으로 검색
                for check_url in urls_to_check:
                    query = {
                        "filter": {
                            "property": url_prop_name,
                            "url": {"equals": check_url}
                        }
                    }
                    
                    resp = requests.post(endpoint, headers=headers, json=query, timeout=15)
                    
                    if resp.status_code == 200:
                        results = resp.json().get("results", [])
                        if results:
                            # Notion에서 중복 발견 -> 로컬 캐시에 추가
                            url_cache.add(normalized_url)
                            return 1  # 중복 발견
                    elif resp.status_code == 429:
                        retry_after = 2 ** (attempt + 1)
                        print(f"⚠️ 중복 확인 중 429 Rate Limit. {retry_after}초 후 재시도...")
                        time.sleep(retry_after)
                        break  # 내부 루프 탈출, 재시도
                    # 기타 에러는 다음 URL 변형 시도
                
                # 모든 URL 변형에서 중복 없음
                return 0  # 중복 없음 (신규)

            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    print(f"[ERROR] 중복 확인 네트워크 에러: {e}")
                    return 1  # Fail-Safe
        
        return 1  # Fail-Safe (Max retries exceeded)

    except Exception as e:
        print(f"[ERROR] 중복 확인 로직 에러: {e}")
        return 1  # Fail-Safe


def delete_old_entries(DATABASE_ID):
    """
    Notion 데이터베이스에서 90일 이상 지난 오래된 항목들을 찾아 보관(archive) 처리합니다.
    ✅ [수정] 2025-09-03 API 마이그레이션 완료
    - data_source_id를 사용하여 쿼리합니다.
    - 'date' 속성 이름을 동적으로 찾습니다.
    """
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }

    # --- [핵심 수정 1]: data_source_id 및 properties 획득 ---
    data_source_id, db_props = get_data_source_info(DATABASE_ID, headers)
    if not data_source_id or not db_props:
        err_msg = f"[ERROR] delete_old_entries: data_source_id 또는 properties 획득 실패 (DB: {DATABASE_ID})"
        print(err_msg)
        send_slack_message(err_msg)
        return

    # --- [핵심 수정 2]: 'date' 타입 속성 이름 동적 탐색 ---
    date_prop_name = None
    for pn, pinfo in db_props.items():
        if pinfo.get('type') == 'date':
            date_prop_name = pn
            print(f" → [delete_old_entries] date 속성 발견: {pn}")
            break

    if not date_prop_name:
        err_msg = f"[ERROR] delete_old_entries: DB({DATABASE_ID})에서 'date' 타입 속성을 찾을 수 없습니다."
        print(err_msg)
        send_slack_message(err_msg)
        return

    # --- [핵심 수정 3]: 엔드포인트를 data_source_id로 변경 ---
    endpoint = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    
    threshold_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=90)
    
    pages_to_archive = []
    has_more = True
    start_cursor = None

    print(f"90일 이전 (기준일: {threshold_date.strftime('%Y-%m-%d')}) 항목 삭제(보관) 작업 시작...")

    while has_more:
        # --- [핵심 수정 4]: 쿼리 페이로드에서 동적 date 속성 이름 사용 ---
        query_payload = {
            "filter": {
                "property": date_prop_name,  # 'date' 하드코딩 대신 변수 사용
                "date": {"before": threshold_date.isoformat()}
            },
            "page_size": 100
        }
        if start_cursor:
            query_payload["start_cursor"] = start_cursor
        
        try:
            response = requests.post(endpoint, headers=headers, json=query_payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            pages_to_archive.extend([page["id"] for page in data.get("results", [])])
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] 오래된 항목 조회 실패: {e}")
            send_slack_message(f"[ERROR] 오래된 항목 조회 실패: {e}")
            return # 더 이상 진행하지 않고 함수 종료
    
    if not pages_to_archive:
        print("삭제(보관)할 오래된 항목이 없습니다.")
        return

    print(f"총 {len(pages_to_archive)}개의 오래된 항목을 찾았습니다. 보관 처리를 진행합니다.")
    archived_count = 0
    skipped_count = 0
    error_count = 0

    # 페이지 보관(archive) 로직 - 이미 보관된 항목은 건너뜀
    for page_id in pages_to_archive:
        # 먼저 페이지 상태 확인 (이미 보관되었는지)
        get_endpoint = f"https://api.notion.com/v1/pages/{page_id}"

        try:
            get_response = requests.get(get_endpoint, headers=headers, timeout=10)
            if get_response.status_code == 200:
                page_data = get_response.json()
                # 이미 보관되었는지 확인
                if page_data.get("archived", False):
                    print(f"   - [SKIP] 이미 보관된 항목: {page_id}")
                    skipped_count += 1
                    continue

            # 보관되지 않은 경우에만 보관 시도
            patch_endpoint = f"https://api.notion.com/v1/pages/{page_id}"
            archive_payload = {"archived": True}
            patch_response = requests.patch(patch_endpoint, headers=headers, json=archive_payload, timeout=10)

            if patch_response.status_code == 200:
                print(f"   - 항목 보관 완료: {page_id}")
                archived_count += 1
            else:
                err_text = patch_response.text
                print(f"   - [ERROR] 항목 보관 실패 ({page_id}): {patch_response.status_code} - {err_text}")
                error_count += 1
                send_slack_message(f"[ERROR] 항목 보관 실패 ({page_id}): {patch_response.status_code} - {err_text}")

        except requests.exceptions.RequestException as e:
            print(f"   - [ERROR] 항목 보관 요청 중 네트워크 오류 ({page_id}): {e}")
            error_count += 1
            send_slack_message(f"[ERROR] 항목 보관 요청 중 네트워크 오류 ({page_id}): {e}")
        
    print(f"오래된 항목 삭제(보관) 작업 완료.")
    print(f"  - 보관 완료: {archived_count}개")
    print(f"  - 이미 보관됨 (건너뜀): {skipped_count}개")
    print(f"  - 오류: {error_count}개")

    if archived_count > 0:
        send_slack_message(f"[INFO] 오래된 항목 삭제(보관) 작업 완료.\n보관: {archived_count}개 / 건너뜀: {skipped_count}개 / 오류: {error_count}개")


def get_recent_entries(DATABASE_ID):
    """
    Notion 데이터베이스에서 최근 7일 이내의 항목들을 조회하고 내용을 결합하여 반환합니다.
    ✅ [수정] 2025-09-03 API 마이그레이션 완료
    - data_source_id를 사용하여 쿼리합니다.
    - 'date', 'title', 'content', 'url' 속성 이름을 동적으로 찾습니다.
    """
    print(f"[DEBUG] ===== get_recent_entries 시작 =====")
    print(f"[DEBUG] 데이터베이스 ID: {DATABASE_ID}")
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }

    # --- [핵심 수정 1]: data_source_id 및 properties 획득 ---
    data_source_id, db_props = get_data_source_info(DATABASE_ID, headers)
    if not data_source_id or not db_props:
        err_msg = f"[ERROR] get_recent_entries: data_source_id 또는 properties 획득 실패 (DB: {DATABASE_ID})"
        print(err_msg)
        send_slack_message(err_msg)
        return None

    # --- [핵심 수정 2]: 'date', 'title', 'content', 'url' 속성 이름 동적 탐색 ---
    date_prop_name = None
    title_prop_name = None
    content_prop_name = None
    url_prop_name = None

    print("[DEBUG] [get_recent_entries] DB 속성 검색:")
    for pn, pinfo in db_props.items():
        prop_type = pinfo.get('type')
        if prop_type == 'date':
            date_prop_name = pn
            print(f" → 'date' 속성: {pn}")
        elif prop_type == 'title':
            title_prop_name = pn
            print(f" → 'title' 속성: {pn}")
        elif prop_type == 'url':
            url_prop_name = pn
            print(f" → 'url' 속성: {pn}")
        # 'content'는 'rich_text' 타입이고 이름이 'content'일 것으로 가정
        elif pn == 'content' and prop_type == 'rich_text':
            content_prop_name = pn
            print(f" → 'content' 속성: {pn}")

    if not date_prop_name:
        err_msg = f"[ERROR] get_recent_entries: DB({DATABASE_ID})에서 'date' 타입 속성을 찾을 수 없습니다."
        print(err_msg)
        send_slack_message(err_msg)
        return None
    if not title_prop_name:
        err_msg = f"[ERROR] get_recent_entries: DB({DATABASE_ID})에서 'title' 타입 속성을 찾을 수 없습니다."
        print(err_msg)
        send_slack_message(err_msg)
        return None
    if not url_prop_name: 
        print(f"[WARN] [get_recent_entries] 'url' 속성을 찾지 못했습니다. (선택 사항)")
    if not content_prop_name: 
        print(f"[WARN] [get_recent_entries] 'content' (rich_text) 속성을 찾지 못했습니다. (선택 사항)")


    # --- [핵심 수정 3]: 엔드포인트를 data_source_id로 변경 ---
    endpoint = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"

    # 현재로부터 7일 전 날짜 계산
    seven_days_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)
    
    all_pages_combined_content = [] # 모든 페이지의 내용을 담을 리스트
    has_more = True
    start_cursor = None

    print(f"[DEBUG] 조회 기간: 최근 7일 (기준일: {seven_days_ago.strftime('%Y-%m-%d')})")
    print(f"Notion DB (DS_ID: {data_source_id})에서 최근 7일 이내 항목 조회 시작...")

    while has_more:
        # --- [핵심 수정 4]: 쿼리 페이로드에서 동적 date 속성 이름 사용 ---
        query_payload = {
            "filter": {
                "property": date_prop_name, # 변수 사용
                "date": {"on_or_after": seven_days_ago.isoformat()}
            },
            "sorts": [
                {
                    "property": date_prop_name, # 변수 사용
                    "direction": "descending"
                }
            ],
            "page_size": 100
        }
        if start_cursor:
            query_payload["start_cursor"] = start_cursor
        
        try:
            response = requests.post(endpoint, headers=headers, json=query_payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            for page in data.get("results", []):
                
                # --- [핵심 수정 5]: 동적 속성 이름으로 데이터 추출 ---
                properties = page.get("properties", {})
                
                title_prop = properties.get(title_prop_name, {}).get("title", [])
                title_text = title_prop[0].get("plain_text") if title_prop else "제목 없음"
                
                content_text = ""
                if content_prop_name:
                    content_prop = properties.get(content_prop_name, {})
                    if content_prop and content_prop.get("type") == "rich_text":
                        rich_text = content_prop.get("rich_text", [])
                        content_text = "".join([t.get("plain_text") for t in rich_text])
                
                url_text = "URL 없음"
                if url_prop_name:
                    url_prop = properties.get(url_prop_name, {})
                    url_text = url_prop.get("url") if url_prop and url_prop.get("type") == "url" else "URL 없음"

                # 페이지의 제목, 요약 내용, URL 등을 결합하여 하나의 문자열로 만듭니다.
                # print(f"[DEBUG] 페이지 데이터 추출 - 제목: {title_text[:50]}..., URL: {url_text[:50]}..., 요약 길이: {len(content_text)}자")
                
                if content_text.strip():  # content가 있는 경우에만 포함
                    full_page_content = f"제목: {title_text}\nURL: {url_text}\n요약: {content_text}"
                    # print(f"[DEBUG] 요약 내용 포함하여 페이지 데이터 생성 완료")
                else:  # content가 없는 경우
                    full_page_content = f"제목: {title_text}\nURL: {url_text}"
                    # print(f"[DEBUG] 요약 내용 없음, 제목과 URL만으로 페이지 데이터 생성")
                all_pages_combined_content.append(full_page_content)

            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Notion 최근 항목 조회 실패: {e}")
            send_slack_message(f"[ERROR] Notion 최근 항목 조회 실패: {e}")
            return None # 오류 발생 시 None 반환
    
    if not all_pages_combined_content:
        print("[DEBUG] 최근 7일간의 Notion 항목이 없습니다.")
        print(f"[DEBUG] ===== get_recent_entries 완료 (결과: 없음) =====")
        return None

    print(f"[DEBUG] 총 {len(all_pages_combined_content)}개의 Notion 항목을 찾았습니다.")
    combined_text = "\n---\n".join(all_pages_combined_content)
    print(f"[DEBUG] 결합된 텍스트 길이: {len(combined_text)}자")
    print(f"[DEBUG] ===== get_recent_entries 완료 (결과: {len(all_pages_combined_content)}개 항목) =====")
    
    # 모든 페이지의 내용을 하나의 큰 텍스트로 결합하여 반환
    return combined_text


def upload_file_to_notion(file_path, file_name):

    """

    Notion API를 사용하여 파일을 업로드합니다.

    - 20MB 이하: 싱글 파트 업로드 (single_part)

    - 20MB 초과: 멀티 파트 업로드 (multi_part)

    1단계 실패 시, .pdf 확장자를 붙여 강제로 재시도합니다. (경고: 파일 손상 위험)

    반환: file_id (성공) 또는 None (실패)

    """

    try:

        if not os.path.exists(file_path):

            print(f"❌ 파일 없음: {file_path}")

            return None

        file_size = os.path.getsize(file_path)

        file_size_mb = file_size / (1024 * 1024)

        print(f"📂 파일 정보: {file_name} ({file_size_mb:.2f}MB, {file_size} bytes)")

        # 파일 크기에 따라 싱글 또는 멀티 파트 결정

        use_multipart = file_size > MULTIPART_THRESHOLD

        if use_multipart:

            print(f"📦 멀티 파트 업로드 모드 선택 (파일 크기: {file_size_mb:.2f}MB > 20MB)")

            return _upload_multipart(file_path, file_name)

        else:

            print(f"📦 싱글 파트 업로드 모드 선택 (파일 크기: {file_size_mb:.2f}MB <= 20MB)")

            return _upload_single_part(file_path, file_name)

    except Exception as e:

        print(f"❌ 파일 처리 중 오류: {str(e)}")

        import traceback

        traceback.print_exc()

        return None


def _upload_single_part(file_path, file_name):

    """

    싱글 파트 업로드 구현 (20MB 이하 파일)

    """

    try:

        mime_type, _ = mimetypes.guess_type(file_path)

        if not mime_type:

            mime_type = 'application/octet-stream'

        print(f"📝 MIME 타입: {mime_type}")

        headers = {

            'Authorization': f'Bearer {NOTION_API_TOKEN}',

            'Content-Type': 'application/json',

            'Notion-Version': '2025-09-03'

        }

        # 1단계: 파일 업로드 생성 (시도 1: 원본 파일명)

        print(f"🔄 1단계 (시도 1): 원본 파일명({file_name})으로 업로드 생성 중...")

        create_payload = {

            "mode": "single_part",

            "filename": file_name,

            "content_type": mime_type

        }

        create_response = requests.post(

            'https://api.notion.com/v1/file_uploads',

            headers=headers,

            json=create_payload,

            timeout=30

        )

        if create_response.status_code != 200:

            error_data = create_response.json()

            error_message = error_data.get('message', '')

            print(f"❌ 1단계 (시도 1) 실패: {error_message}")

            # 지원되지 않는 확장자인 경우 재시도

            if "not supported" in error_message:

                print(f"⚠️ 지원되지 않는 확장자 감지. '.pdf'를 추가하여 재시도합니다.")

                original_file_name_for_step_2 = file_name

                file_name = file_name + ".pdf"

                mime_type = "application/pdf"

                print(f"🔄 1단계 (시도 2): 새 파일명({file_name}) / 가짜 MIME 타입({mime_type})으로 생성 중...")

                create_payload_retry = {

                    "mode": "single_part",

                    "filename": file_name,

                    "content_type": mime_type

                }

                create_response = requests.post(

                    'https://api.notion.com/v1/file_uploads',

                    headers=headers,

                    json=create_payload_retry,

                    timeout=30

                )

                if create_response.status_code != 200:

                    error_data_retry = create_response.json()

                    print(f"❌ 1단계 (시도 2)도 실패: {error_data_retry.get('message', '')}")

                    return None

                print(f"✅ 1단계 (시도 2) 생성 성공. (파일명: {file_name})")

            else:

                print(f"⚠️ 'not supported' 오류가 아니므로 재시도하지 않습니다.")

                return None

        else:

            print(f"✅ 1단계 (시도 1) 생성 성공.")

        # 1단계 성공

        create_data = create_response.json()

        file_id = create_data.get('id')

        upload_url = create_data.get('upload_url')

        if not file_id or not upload_url:

            print(f"❌ file_id 또는 upload_url 없음")

            return None

        print(f"✅ 파일 업로드 ID: {file_id}")

        print(f"✅ 업로드 URL: {upload_url}")

        # 2단계: 파일 콘텐츠 전송 (binary data)

        print(f"🔄 2단계: 파일 콘텐츠 전송 중... (파일명: {file_name}, MIME: {mime_type})")

        upload_headers_for_step2 = {

            'Authorization': f'Bearer {NOTION_API_TOKEN}',

            'Notion-Version': '2025-09-03',

        }

        with open(file_path, 'rb') as f:

            files_payload = {'file': (file_name, f, mime_type)}

            upload_response = requests.post(

                upload_url,

                headers=upload_headers_for_step2,

                files=files_payload,

                timeout=120

            )

        print(f"📥 2단계 응답 상태: {upload_response.status_code}")

        if upload_response.status_code not in [200, 204]:

            print(f"❌ 파일 전송 실패: {upload_response.status_code}")

            print(f"⚠️ 응답: {upload_response.text[:500]}")

            return None

        # 3단계: 업로드 완료 확인

        print(f"🔄 3단계: 업로드 상태 확인 중...")

        for attempt in range(5):

            check_response = requests.get(

                f'https://api.notion.com/v1/file_uploads/{file_id}',

                headers=upload_headers_for_step2,

                timeout=10

            )

            if check_response.status_code == 200:

                status_data = check_response.json()

                status = status_data.get('status')

                print(f"⏳ 상태: {status}")

                if status == 'uploaded':

                    print(f"✅ 파일 업로드 완료!")

                    print(f"✅ 반환할 file_id: {file_id}")

                    return file_id

                elif status == 'failed':

                    print(f"❌ 업로드 실패 상태")

                    return None

                time.sleep(1)

        print(f"⚠️ 상태 확인 타임아웃, file_id 반환: {file_id}")

        return file_id

    except Exception as e:

        print(f"❌ 싱글 파트 업로드 중 오류: {str(e)}")

        import traceback

        traceback.print_exc()

        return None


def _upload_multipart(file_path, file_name):
    """
    멀티 파트 업로드 구현 (20MB 초과 파일)
    
    ✅ Notion API v2025-09-03 기반 (최종 수정)
    1단계: 멀티 파트 업로드 객체 생성
    2단계: 각 파트를 multipart/form-data로 업로드 (part_number를 바디에 포함)
    3단계: /complete 호출
    4단계: 상태 확인
    """
    
    try:
        file_size = os.path.getsize(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        print(f"📝 MIME 타입: {mime_type}")
        
        # 필요한 파트 개수 계산
        number_of_parts = (file_size + MULTIPART_CHUNK_SIZE - 1) // MULTIPART_CHUNK_SIZE
        
        if number_of_parts > 1000:
            print(f"❌ 파일이 너무 큽니다. 최대 파트 개수는 1000개입니다.")
            return None
        
        print(f"📦 파일을 {number_of_parts}개 파트로 분할하여 업로드합니다. (청크: 10MB)")
        
        headers = {
            'Authorization': f'Bearer {NOTION_API_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2025-09-03'
        }
        
        # ========== 1단계: 멀티 파트 업로드 객체 생성 ==========
        print(f"🔄 1단계: 멀티 파트 업로드 객체 생성 중...")
        
        create_payload = {
            "mode": "multi_part",
            "filename": file_name,
            "content_type": mime_type,
            "number_of_parts": number_of_parts
        }
        
        print(f"[DEBUG] 요청 페이로드:")
        print(json.dumps(create_payload, indent=2, ensure_ascii=False))
        
        create_response = requests.post(
            'https://api.notion.com/v1/file_uploads',
            headers=headers,
            json=create_payload,
            timeout=30
        )
        
        print(f"[DEBUG] 응답 상태: {create_response.status_code}")
        
        if create_response.status_code != 200:
            print(f"❌ 1단계 실패 (상태 {create_response.status_code})")
            try:
                error_data = create_response.json()
                print(f"[DEBUG] 오류: {error_data.get('message', 'Unknown')}")
            except:
                print(f"[DEBUG] 응답: {create_response.text[:500]}")
            return None
        
        create_data = create_response.json()
        
        print(f"[DEBUG] 1단계 응답 JSON:")
        print(json.dumps(create_data, indent=2, ensure_ascii=False))
        
        file_id = create_data.get('id')
        upload_url = create_data.get('upload_url')
        
        if not file_id or not upload_url:
            print(f"❌ file_id 또는 upload_url 없음")
            print(f"[DEBUG] 응답 키: {list(create_data.keys())}")
            return None
        
        print(f"✅ 1단계 완료")
        print(f"  - file_id: {file_id}")
        print(f"  - upload_url: {upload_url}")
        
        # ========== 2단계: 각 파트 업로드 ==========
        print(f"🔄 2단계: 파일 청크 업로드 시작...")
        
        upload_headers = {
            'Authorization': f'Bearer {NOTION_API_TOKEN}',
            'Notion-Version': '2025-09-03',
        }
        
        with open(file_path, 'rb') as f:
            for part_number in range(1, number_of_parts + 1):
                chunk = f.read(MULTIPART_CHUNK_SIZE)
                
                if not chunk:
                    break
                
                chunk_size_mb = len(chunk) / (1024 * 1024)
                print(f"  📤 파트 {part_number}/{number_of_parts} 업로드 중... ({chunk_size_mb:.2f}MB)")
                
                try:
                    # ✅ [핵심 수정] part_number를 multipart/form-data 바디에 포함
                    # (쿼리 파라미터 아님)
                    files_payload = {
                        'file': (f'{file_name}_part{part_number}', chunk, mime_type),
                        'part_number': (None, str(part_number))  # ← 바디에 포함
                    }
                    
                    print(f"  [DEBUG] 파트 {part_number} 요청 URL: {upload_url}")
                    print(f"  [DEBUG] 파트 {part_number} part_number 값: {part_number}")
                    
                    upload_response = requests.post(
                        upload_url,  # ← 쿼리 파라미터 없음
                        headers=upload_headers,
                        files=files_payload,
                        timeout=300
                    )
                    
                    print(f"  [DEBUG] 파트 {part_number} 응답 상태: {upload_response.status_code}")
                    
                    if upload_response.status_code not in [200, 204]:
                        print(f"  ❌ 파트 {part_number} 업로드 실패: {upload_response.status_code}")
                        try:
                            error_resp = upload_response.json()
                            print(f"  [DEBUG] 오류 응답: {json.dumps(error_resp, ensure_ascii=False)}")
                        except:
                            print(f"  [DEBUG] 응답: {upload_response.text[:500]}")
                        return None
                    
                    print(f"  ✅ 파트 {part_number} 업로드 완료")
                
                except Exception as e:
                    print(f"  ❌ 파트 {part_number} 업로드 중 오류: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    return None
        
        print(f"✅ 2단계 완료 - 모든 파트 업로드 완료")
        
        # ========== 3단계: 멀티 파트 업로드 완료 ==========
        print(f"🔄 3단계: 멀티 파트 업로드 완료 처리 중...")
        
        complete_response = requests.post(
            f'https://api.notion.com/v1/file_uploads/{file_id}/complete',
            headers=headers,
            json={},
            timeout=30
        )
        
        print(f"[DEBUG] 3단계 응답 상태: {complete_response.status_code}")
        
        if complete_response.status_code != 200:
            print(f"❌ 3단계 실패")
            try:
                error_data = complete_response.json()
                print(f"[DEBUG] 오류: {error_data.get('message', '')}")
            except:
                print(f"[DEBUG] 응답: {complete_response.text[:500]}")
            return None
        
        print(f"✅ 3단계 완료 - 완료 처리 완료")
        
        # ========== 4단계: 업로드 상태 확인 ==========
        print(f"🔄 4단계: 업로드 상태 확인 중...")
        
        for attempt in range(5):
            check_response = requests.get(
                f'https://api.notion.com/v1/file_uploads/{file_id}',
                headers=upload_headers,
                timeout=10
            )
            
            if check_response.status_code == 200:
                status_data = check_response.json()
                status = status_data.get('status')
                
                print(f"  ⏳ 상태: {status}")
                
                if status == 'uploaded':
                    print(f"✅ 4단계 완료 - 파일 업로드 완료!")
                    print(f"✅ 반환할 file_id: {file_id}")
                    return file_id
                
                elif status == 'failed':
                    print(f"❌ 업로드 실패 상태")
                    return None
                
                time.sleep(1)
        
        print(f"⚠️ 상태 확인 타임아웃, file_id 반환: {file_id}")
        return file_id
    
    except Exception as e:
        print(f"❌ 멀티 파트 업로드 중 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def get_recent_titles_from_notion(database_id, days=7):
    """
    Notion 데이터베이스에서 최근 N일간의 제목들을 가져옵니다.
    """
    from config import NOTION_API_TOKEN
    import requests
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }
    
    # 날짜 필터 생성
    start_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    # data_source_id 조회
    data_source_id, properties = get_data_source_info(database_id, headers)
    if not data_source_id:
        print("[ERROR] data_source_id 조회 실패")
        return []
    
    # 쿼리 URL
    query_url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    
    payload = {
        "filter": {
            "property": "Date",
            "date": {
                "on_or_after": start_date
            }
        }
    }
    
    try:
        response = requests.post(query_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        titles = []
        for result in data.get('results', []):
            properties = result.get('properties', {})
            title_prop = properties.get('Title', {}) or properties.get('Name', {})
            
            if title_prop.get('type') == 'title':
                title_array = title_prop.get('title', [])
                if title_array:
                    title = title_array[0].get('plain_text', '')
                    if title:
                        titles.append(title)
        
        return titles
    except Exception as e:
        print(f"[ERROR] Notion 제목 조회 실패: {e}")
        return []
