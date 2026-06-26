# security_news_aggregator.py
import os
import time
import schedule
import threading
import fcntl
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# 환경 변수 로드 (필요시 python-dotenv 사용)
# from dotenv import load_dotenv
# load_dotenv()

from config import RUN_SCHEDULER, BOANISSUE_DATABASE_ID, GUIDE_DATABASE_ID, ENABLE_WEEKLY_NOTION, ENABLE_WEEKLY_TISTORY
from modules.utils import send_slack_message
from modules.publisher_service import PublisherService
from modules.notion_handler import Duplicate_check, sync_cache_from_notion # [New] for optimized check
from modules.log_utils import print_metrics_summary, logger  # 구조화된 메트릭 로깅

# 🔒 중복 실행 방지 Lock 파일
LOCK_FILE = Path("/tmp/security_news_aggregator.lock")
LOCK_FD = None

def acquire_lock():
    """
    파일 락을 획득하여 중복 실행을 방지합니다.
    Returns:
        bool: 락 획득 성공 여부 (False = 이미 실행 중)
    """
    global LOCK_FD
    try:
        LOCK_FD = open(LOCK_FILE, 'w')
        fcntl.flock(LOCK_FD.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        LOCK_FD.write(f"{os.getpid()}\n")
        LOCK_FD.flush()
        return True
    except (IOError, BlockingIOError):
        if LOCK_FD:
            try:
                LOCK_FD.close()
            except:
                pass
            LOCK_FD = None
        return False

def release_lock():
    """파일 락 해제"""
    global LOCK_FD
    if LOCK_FD:
        try:
            fcntl.flock(LOCK_FD.fileno(), fcntl.LOCK_UN)
            LOCK_FD.close()
        except:
            pass
        finally:
            LOCK_FD = None
            try:
                LOCK_FILE.unlink()
            except:
                pass

# Import Crawlers
from modules.crawlers.ncsc import NCSCCrawler
from modules.crawlers.krcert import KRCERTCrawler
from modules.crawlers.boannews import BoanNewsCrawler
from modules.crawlers.dailysecu import DailySecuCrawler
from modules.crawlers.nvd import NVDCrawler
from modules.crawlers.weekly import WeeklyTechCrawler
from modules.crawlers.skshieldus import SKShieldusCrawler
from modules.crawlers.ahnlab import AhnLabCrawler
from modules.crawlers.igloo import IglooCrawler
from modules.crawlers.kisa import KISACrawler
from modules.crawlers.kisa_notice import KISANoticeCrawler
from modules.crawlers.keyword_news import KeywordNewsCrawler
from modules.crawlers.boho import BohoCrawler

# Import Analysis
from modules.analysis import analyze_keywords
from modules.llm_handler import summarize_text, details_text, generate_blog_article_2step

# Global Queue for Article Processing
from queue import Queue
import threading

# 큐 최대 크기 설정 (메모리 관리)
MAX_QUEUE_SIZE = 100
GLOBAL_ARTICLE_QUEUE = Queue(maxsize=MAX_QUEUE_SIZE)

# Global URL set for deduplication across crawlers (스레드 안전성 확보)
GLOBAL_SEEN_URLS = set()
GLOBAL_URLS_LOCK = threading.RLock()  # 재귀적 락 for 중첩 접근

class QueueCollector:
    """
    PublisherService 대신 크롤러에 전달되어,
    발견된 기사를 즉시 처리하지 않고 큐에 적재(Collect)하는 역할을 합니다.
    """
    def __init__(self, db_id, enable_notion=True, enable_tistory=False):
        self.db_id = db_id
        self.enable_notion = enable_notion
        self.enable_tistory = enable_tistory

    def update_settings(self, enable_notion, enable_tistory, notion_database_id):
        pass # 설정은 무시하거나 필요시 저장

    def add_article(self, article_data):
        """
        크롤러 호환성을 위한 메서드 (publish_article의 alias)
        """
        return self.publish_article(
            title=article_data.get('title'),
            content=article_data.get('content', ''),
            url=article_data.get('url'),
            date=article_data.get('date'),
            category=article_data.get('category', ''),
            details=article_data.get('details', ''),
            database_id=article_data.get('database_id'),
            files=article_data.get('files')
        )

    def publish_article(self, title, content, url, date, category, details, database_id=None, files=None):
        """
        크롤러가 호출하는 메서드. 실제 발행 대신 큐에 작업 객체를 넣습니다.
        전역 중복 체크를 수행하여 불필요한 LLM 호출 방지
        """
        # 스레드 안전한 전역 중복 체크
        with GLOBAL_URLS_LOCK:
            if url in GLOBAL_SEEN_URLS:
                return False  # 중복: 큐에 넣지 않음
            GLOBAL_SEEN_URLS.add(url)

        task = {
            "title": title,
            "content": content, # Raw Content
            "url": url,
            "date": date,
            "category": category,
            "details": details, # Raw Content (usually same as content)
            "database_id": database_id or self.db_id,
            "files": files,
            "source": category.split('/')[0] if '/' in category else category,
            "enable_notion": self.enable_notion,
            "enable_tistory": self.enable_tistory
        }
        GLOBAL_ARTICLE_QUEUE.put(task)
        # print(f"[Queue] Added: {title[:20]}...")
        return True  # 성공: 큐에 추가됨


def run_crawler_wrapper_producer(crawler, db_id, enable_notion=True, enable_tistory=False, direct_publisher=None):
    """
    Phase 1: Producer (Scanning)
    크롤러를 실행하여 기사를 수집하고 큐에 넣습니다. (병렬 실행됨)
    **Optimization**: direct_publisher가 제공되면 큐를 거치지 않고 즉시 발행합니다. (KISA 등 LLM 불필요 시)
    """
    try:
        # Collector 결정: 직접 발행(PublisherService) vs 큐 적재(QueueCollector)
        collector = direct_publisher if direct_publisher else QueueCollector(db_id, enable_notion, enable_tistory)
        
        # 크롤러 실행
        return crawler.run(collector)
        
    except Exception as e:
        error_msg = f"{crawler.source_name} 실행 중 오류 발생: {e}"
        logger.error(f"[CRITICAL] {error_msg}")
        # send_slack_message(f"[CRITICAL ERROR] {error_msg}")
        return {
            "source": crawler.source_name,
            "success": 0, "duplicate": 0, "old": 0, "error": 1, "total": 0
        }

def print_summary(results):
    """
    모든 크롤러의 실행 결과를 종합하여 테이블 형태로 출력하고 Slack으로 전송합니다.
    """
    from modules.utils import pad_str
    
    lines = []
    # Header
    col_source = "Source"
    col_new = "New"
    col_dup = "Dup"
    col_old = "Old"
    col_err = "Err"
    col_ign = "Ign"
    col_tot = "Tot"
    
    # Widths
    w_src = 18 
    w_num = 5
    
    header = f"{pad_str(col_source, w_src)} | {pad_str(col_new, w_num)} | {pad_str(col_dup, w_num)} | {pad_str(col_old, w_num)} | {pad_str(col_err, w_num)} | {pad_str(col_ign, w_num)} | {pad_str(col_tot, w_num)}"
    sep = "-" * len(header)
    
    lines.append("=" * len(header))
    lines.append(header)
    lines.append(sep)
    
    total_new = 0
    total_dup = 0
    total_old = 0
    total_err = 0
    total_unmatched = 0
    total_items = 0
    
    for res in results:
        if not res or not isinstance(res, dict): continue
        
        name = res.get('source', 'Unknown')
        # 이름 너무 길면 잘림 방지 (Display width 기준)
        # (간단히 문자열 길이로 자르고 패딩은 Display width로)
        if len(name) > 13: name = name[:11] + ".."
        
        new = str(res.get('success', 0))
        dup = str(res.get('duplicate', 0))
        old = str(res.get('old', 0))
        err = str(res.get('error', 0))
        unmatched = str(res.get('unmatched', 0))
        tot = str(res.get('total', 0))
        
        line = f"{pad_str(name, w_src)} | {pad_str(new, w_num)} | {pad_str(dup, w_num)} | {pad_str(old, w_num)} | {pad_str(err, w_num)} | {pad_str(unmatched, w_num)} | {pad_str(tot, w_num)}"
        lines.append(line)
        
        total_new += res.get('success', 0)
        total_dup += res.get('duplicate', 0)
        total_old += res.get('old', 0)
        total_err += res.get('error', 0)
        total_unmatched += res.get('unmatched', 0)
        total_items += res.get('total', 0)
        
    lines.append(sep)
    
    t_new = str(total_new)
    t_dup = str(total_dup)
    t_old = str(total_old)
    t_err = str(total_err)
    t_unm = str(total_unmatched)
    t_tot = str(total_items)
    
    total_line = f"{pad_str('TOTAL', w_src)} | {pad_str(t_new, w_num)} | {pad_str(t_dup, w_num)} | {pad_str(t_old, w_num)} | {pad_str(t_err, w_num)} | {pad_str(t_unm, w_num)} | {pad_str(t_tot, w_num)}"
    lines.append(total_line)
    lines.append("=" * len(header))

    summary_text = "\n".join(lines)
    logger.info("\n" + summary_text + "\n")

    # 성능 메트릭 요약 출력
    print_metrics_summary()

    # Slack 전송
    try:
        from modules.utils import send_slack_message
        slack_msg = f"📊 *크롤링 실행 결과 Report*\n```\n{summary_text}\n```"
        send_slack_message(slack_msg)
        logger.info("[System] Slack으로 실행 결과 리포트를 전송했습니다.")
    except Exception as e:
        logger.warning(f"[Warning] Slack 리포트 전송 실패: {e}")

def process_article_queue_concurrent(publisher_service, stop_event, consumer_id=0):
    """
    Consumer (Processing) - Concurrent Version with Multiple Threads
    큐에 쌓인 기사들을 하나씩 꺼내어 순차적으로 처리합니다.
    stop_event가 설정되고 큐가 비면 종료합니다.
    
    Args:
        publisher_service: PublisherService 인스턴스
        stop_event: 스레드 종료 시그널
        consumer_id: Consumer 식별자 (로그용)
    """
    logger.info(f"\n[{datetime.now()}] 기사 처리(Consumer) 스레드 #{consumer_id + 1} 시작...")

    # 디버깅: 큐 상태 확인
    initial_queue_size = GLOBAL_ARTICLE_QUEUE.qsize()
    logger.info(f"[DEBUG #{consumer_id + 1}] 초기 큐 크기: {initial_queue_size}")

    processed_count = 0
    success_count = 0  # 디버깅 추가
    error_count = 0  # 디버깅 추가

    while not stop_event.is_set() or not GLOBAL_ARTICLE_QUEUE.empty():
        try:
            # 큐에서 작업을 가져옴 (타임아웃 1초)
            # 타임아웃을 두어 loop를 돌게 하고 stop_event를 체크함
            # 큐에서 작업 가져오기
            try:
                task = GLOBAL_ARTICLE_QUEUE.get(timeout=1)
            except:
                continue # 큐가 비었으면 continue (stop_event 체크)

            processed_count += 1
            title = task['title']
            source = task['source']
            logger.info(f"\n[Processing] {source} - {title[:30]}...")

            # [Optimization] LLM 분석 전 중복 및 날짜 재검증 (Double Check)
            # 사용자 요청: "발행 시도 하기 전에 날짜/중복 체크부터 해줘"
            should_skip = False
            skip_reason = ""

            #1. 날짜 체크 (90일 기준)
            task_date_str = task.get('date')
            if task_date_str:
                try:
                    t_date = datetime.strptime(task_date_str, '%Y-%m-%d')
                    if (datetime.now() - t_date).days > 90:
                         should_skip = True
                         skip_reason = f"오래된 기사 (90일 초과, {task_date_str})"
                except: pass

            if not should_skip:
                target_db_id = task.get('database_id', BOANISSUE_DATABASE_ID)
                # Duplicate_check는 존재하면 1 반환
                if Duplicate_check(task['url'], target_db_id) == 1:
                     should_skip = True
                     skip_reason = "이미 존재하는 기사 (중복)"

            if should_skip:
                 logger.info(f"[SKIP] {skip_reason}: {title}")
                 # [Cleanup] 분석 전 Skip 시에도 파일 삭제 필수
                 if task.get('files'):
                     import os
                     for f_info in task['files']:
                         try:
                             if os.path.exists(f_info['path']):
                                 os.remove(f_info['path'])
                                 logger.info(f"  🗑️ 로컬 파일 삭제 완료 (Skip Clean): {f_info['name']}")
                         except: pass
                 continue

            #1. LLM Summary & Details (2-step generation for better content)
            final_content = task['content']
            final_details = task['details']

            needs_llm = True
            if "KISA Guide" in task['category'] or "KISA 가이드라인" in task['category'] or "보호나라 가이드라인" in task['category']:
                needs_llm = False

            if needs_llm:
                # [번역] 영문 제목일 경우 번역 (기사 처리 시점에서 실행)
                # 다른 스레드의 작업과 방해하지 않도록 여기서 처리
                original_title = title
                try:
                    def is_mostly_english(text):
                        """텍스트가 영어인지 확인"""
                        if not text:
                            return False
                        english_chars = sum(1 for c in text if c.isalpha() and ord(c) < 128)
                        total_chars = sum(1 for c in text if c.isalpha())
                        return total_chars > 0 and english_chars / total_chars > 0.5

                    if is_mostly_english(title):
                        from modules.llm_handler import translate_text
                        translated_title = translate_text(title, title=title)
                        if translated_title and translated_title != title:
                            title = f"{translated_title} ({title})"
                            logger.info(f"[번역] 영문 제목 번역 완료")
                except Exception as e:
                    logger.error(f"[번역-ERROR] 번역 실패, 원본 제목 사용: {e}")
                    title = original_title

                logger.info(f"[LLM] 2단계 본문 생성 중... (원문 제목 유지)")
                try:
                    # 2단계 생성: 요약 + 상세 본문 (최소 2000자)
                    # 원문 제목은 그대로 사용, 본문만 생성
                    generated_summary, generated_content = generate_blog_article_2step(
                        title=title,  # 원문 제목 (그대로 사용)
                        url=task['url'],
                        summary=task['content'],
                        source=task['category'],
                        use_cache=False  # 매번 새로운 생성
                    )
                    final_content = generated_summary  # 생성된 요약
                    final_details = generated_content   # 생성된 상세 본문 (2000자 이상)

                    logger.info(f"[LLM] 본문 생성 완료 - 요약: {len(final_content)}자, 상세: {len(final_details)}자")
                except Exception as llm_e:
                    logger.error(f"[LLM-ERROR] 2단계 생성 실패, 기존 방식으로 대체: {llm_e}")
                    # Fallback: 기존 방식으로 재시도
                    try:
                        summarized_content = summarize_text(task['content'], title=title)
                        final_content = summarized_content
                        final_details = details_text(task['details'], title=title)
                    except Exception as e:
                        logger.error(f"[LLM-ERROR] 기존 방식도 실패 (원본 사용): {e}")
                        # 오류 시 원본 그대로 사용

            #2. Publish
            publisher_service.publish_article(
                title=title,
                content=final_content,
                url=task['url'],
                date=task['date'],
                category=task['category'],
                details=final_details,
                database_id=task['database_id'],
                files=task.get('files'),
                enable_notion=task.get('enable_notion', True), # Task specific override
                enable_tistory=task.get('enable_tistory', False)
            )

            # [New] 파일 업로드 후 로컬 파일 삭제 (Clean up)
            if task.get('files'):
                import os
                for f_info in task['files']:
                    try:
                        if os.path.exists(f_info['path']):
                            os.remove(f_info['path'])
                            logger.info(f"  🗑️ 로컬 파일 삭제 완료: {f_info['name']}")
                    except Exception as del_e:
                        logger.warning(f"  ⚠️ 로컬 파일 삭제 실패: {del_e}")

        except Exception as e:
            logger.error(f"[ERROR] 항목 처리 실패 ({title}): {e}")
            # send_slack_message(f"[ERROR] 항목 처리 실패 ({title}): {e}")

        # 큐 작업 완료 표시
        GLOBAL_ARTICLE_QUEUE.task_done()

    logger.info(f"\n[{datetime.now()}] 기사 처리(Consumer) 스레드 종료. (총 {processed_count}건 처리)")

def start_regular_tasks(publisher_service):
    """
    정기 크롤링 작업을 생산자-소비자 패턴으로 실행합니다.
    Phase 1: 병렬 스캔 (수집)
    Phase 2: 순차 처리 (LLM + 발행)

    [NEW] Phase 0: 90일 이상된 글 자동 정리
    """
    logger.info("정기 크롤링 작업 시작 (Producer-Consumer Pattern)...")

    # === [Phase 0] 90일 자동 정리 (비동기) ===
    # [2026-02-18] Option B: 별도 스레드에서 실행하여 메인 작업 차단 방지
    ENABLE_PHASE_0_CLEANUP = True  # 비동기 모드로 활성화
    PHASE_0_MAX_ITEMS = 100  # 한 번에 처리할 최대 항목 수

    def run_phase_0_cleanup():
        """Phase 0를 별도 스레드에서 실행 (비동기)"""
        try:
            from modules.notion_handler import delete_old_entries
            from modules.utils import send_slack_message

            databases_to_cleanup = [BOANISSUE_DATABASE_ID]

            for db_id in databases_to_cleanup:
                try:
                    logger.info(f"[Phase 0-Async] 90일 정리 시작: {db_id[:20]}...")
                    delete_old_entries(db_id)
                    logger.info(f"[Phase 0-Async] 90일 정리 완료: {db_id[:20]}...")
                except Exception as e:
                    logger.error(f"[Phase 0-Async] 정리 중 오류 ({db_id[:20]}...): {e}")

        except ImportError:
            logger.warning("[Phase 0-Async] delete_old_entries 모듈을 찾을 수 없습니다.")
        except Exception as e:
            logger.error(f"[Phase 0-Async] 90일 정리 중 오류 발생: {e}")

    if ENABLE_PHASE_0_CLEANUP:
        # 비동기 실행: 메인 작업을 차단하지 않음
        cleanup_thread = threading.Thread(target=run_phase_0_cleanup, daemon=True, name="Phase0-Cleanup")
        cleanup_thread.start()
        logger.info("Phase 0: 90일 정리 비동기 실행 시작 (메인 작업 계속 진행)")
    else:
        logger.info("Phase 0: 90일 정리 비활성화됨 (건너뜀)")

    # === [Phase 1] 큐 초기화 ===
    # 큐 초기화 (혹시 남아있는게 있다면 비움)
    with GLOBAL_ARTICLE_QUEUE.mutex:
        GLOBAL_ARTICLE_QUEUE.queue.clear()

    # 크롤러 정의
    # 크롤러 정의 (Crawler, DB_ID, Enable_Notion, Enable_Tistory)
    # KeywordNewsCrawler는 마지막에 실행되도록 배치 (다른 크롤러 먼저 처리)
    crawlers = [
        (KISACrawler(), GUIDE_DATABASE_ID, True, False),
        (BohoCrawler(), GUIDE_DATABASE_ID, True, False),
        (NCSCCrawler(), BOANISSUE_DATABASE_ID, True, False),
        (KISANoticeCrawler(), BOANISSUE_DATABASE_ID, True, False),
        (KRCERTCrawler(), BOANISSUE_DATABASE_ID, True, False),
        (BoanNewsCrawler(), BOANISSUE_DATABASE_ID, True, False),
        (DailySecuCrawler(), BOANISSUE_DATABASE_ID, True, False),
        (SKShieldusCrawler(), BOANISSUE_DATABASE_ID, True, False),
        (AhnLabCrawler(), BOANISSUE_DATABASE_ID, True, False),
        (IglooCrawler(), BOANISSUE_DATABASE_ID, True, False),
        # KeywordNewsCrawler는 마지막에 실행 (Google News URL 처리 비동기화)
        (KeywordNewsCrawler(), BOANISSUE_DATABASE_ID, True, False)
    ]
    
    # [2026-02-18] 메모리 최적화: Chrome + LLM 동시 실행으로 인한 OOM 방지
    MAX_WORKERS = 1  # Chrome driver memory optimization (reduced from 2)
    results = []

    # --- Concurrent Consumer Start (Multiple Threads) ---
    # threading은 파일 상단에서 이미 import됨
    stop_event = threading.Event()

    # [2026-02-18] 메모리 최적화: LLM 순차 처리
    MAX_CONSUMERS = 1  # 다중 Consumer 스레드 개수 (reduced from 3)
    consumer_threads = []

    for i in range(MAX_CONSUMERS):
        def consumer_worker():
            # Consumer가 즉시 시작하여 큐를 모니터링하고 처리
            logger.info(f"[Consumer #{i+1}] 시작 - 큐 모니터링 중...")
            process_article_queue_concurrent(publisher_service, stop_event, consumer_id=i)

        thread = threading.Thread(target=consumer_worker, daemon=True)
        thread.start()
        consumer_threads.append(thread)

    logger.info(f"[System] {MAX_CONSUMERS}개의 Consumer 스레드 시작 (즉시 처리 모드)")

    # --- Phase 1: Parallel Scanning with Concurrent Processing ---
    logger.info(f"\n>>> Phase 1: 모든 소스에서 기사 스캔 및 수집 중 (병렬 실행) <<<")
    logger.info(f">>> [중요] 큐에 추가된 기사는 즉시 Consumer가 처리합니다. <<<")

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            from concurrent.futures import as_completed
            
            futures_map = {}
            for crawler, db_id, en_notion, en_tistory in crawlers:
                # [Optimization] KISACrawler와 BohoCrawler는 LLM이 필요없으므로 즉시 발행 (direct_publisher 전달)
                # 다른 크롤러는 QueueCollector를 사용하여 비동기 처리
                direct_pub = publisher_service if isinstance(crawler, (KISACrawler, BohoCrawler)) else None
                
                future = executor.submit(run_crawler_wrapper_producer, crawler, db_id, en_notion, en_tistory, direct_pub)
                futures_map[future] = crawler.source_name
            
            total_crawlers = len(crawlers)
            completed_count = 0
            
            for future in as_completed(futures_map):
                completed_count += 1
                crawler_name = futures_map[future]
                try:
                    res = future.result()
                    results.append(res)
                    logger.info(f"[Scan] Completed {completed_count}/{total_crawlers}: {crawler_name}")
                except Exception as e:
                    logger.error(f"[Scan] Error in {crawler_name}: {e}")
                    results.append({"source": crawler_name, "success": 0, "error": 1})

    except KeyboardInterrupt:
        logger.warning("\n[System] 사용자 중단 감지!")

    # 스캔 완료 알림 (Consumer는 이미 실행 중이므로 종료만 신호)
    logger.info("\n>>> 모든 크롤러 스캔 완료. 남은 큐 항목 처리 중... <<<")
    stop_event.set()  # Consumer에게 종료 신호 (큐가 비면 종료해라)

    # 모든 Consumer 스레드 종료 대기
    for thread in consumer_threads:
        thread.join()

    logger.info(f"[System] 모든 Consumer 스레드 종료 완료")
    
    # 스캔 결과 요약 출력
    print_summary(results)

    # --- Phase 2: Sequential Processing (Already done by consumer) ---
    # logger.info(f"\n>>> Phase 2: 수집된 기사 처리 및 발행 (순차 실행) <<<")
    # process_article_queue(publisher_service)
    
    logger.info(f"[{datetime.now()}] 정기 크롤링 작업 전체 종료.\n")

def start_keyword_analysis_task():
    """
    키워드 통계 분석 작업을 실행합니다. (10분마다 실행)
    """
    try:
        logger.info(f"\n[{datetime.now()}] 키워드 통계 분석 시작...")
        analyze_keywords.run_keyword_analysis()
        logger.info(f"[{datetime.now()}] 키워드 통계 분석 완료.")
    except Exception as e:
        logger.error(f"[ERROR] 키워드 통계 분석 중 오류 발생: {e}")
        send_slack_message(f"[ERROR] 키워드 통계 분석 중 오류 발생: {e}")

def start_weekly_tasks(publisher_service):
    """
    주간 작업 (NVD CVE, 주간 키워드) 실행
    """
    logger.info(f"\n[{datetime.now()}] 주간 요약 작업 시작...")
    
    weekly_crawlers = [
        (NVDCrawler(), ENABLE_WEEKLY_NOTION, ENABLE_WEEKLY_TISTORY),
        (WeeklyTechCrawler(), ENABLE_WEEKLY_NOTION, ENABLE_WEEKLY_TISTORY)
    ]

    for crawler, enable_notion, enable_tistory in weekly_crawlers:
        try:
            # 주간 작업은 DB ID가 각 크롤러 내부에서 처리되거나 별도로 설정되어야 함
            # 모든 주간 작업은 BOANISSUE_DATABASE_ID 사용
            target_db_id = BOANISSUE_DATABASE_ID

            # 주간 작업은 순차 실행 유지 (작업량이 많고 빈도가 낮음)
            # publisher_service.update_settings(...)  # Removed as we now pass flags directly
            
            crawler.run(publisher_service, enable_notion, enable_tistory)
        except Exception as e:
            logger.error(f"[ERROR] {crawler.source_name} 실행 실패: {e}")
            send_slack_message(f"[ERROR] {crawler.source_name} 실행 실패: {e}")

    logger.info(f"[{datetime.now()}] 주간 요약 작업 종료.\n")

def main():
    import argparse
    
    # 🔒 중복 실행 방지 (파일 락 획득)
    if not acquire_lock():
        logger.warning("⚠️  이미 실행 중인 인스턴스가 있습니다. 종료합니다.")
        print("⚠️  Security News Aggregator가 이미 실행 중입니다.")
        print("   새 인스턴스를 시작하지 않습니다.")
        return
    
    try:
        parser = argparse.ArgumentParser(description="Security News Aggregator")
        parser.add_argument("--once", action="store_true", help="Run only once and exit (for external schedulers)")
        parser.add_argument("--skip-sync", action="store_true", help="Skip cache sync from Notion (faster startup)")
        args = parser.parse_args()

        logger.info("=== Security News Aggregator v2.2 Started (Lock Enabled) ===")
        
        # [개선] 캐시 동기화 (Notion DB의 모든 URL을 로컬 캐시에 로드)
        if not args.skip_sync:
            logger.info(">>> URL 캐시 동기화 시작 <<<")
            try:
                # BOANISSUE DB 동기화
                sync_cache_from_notion(BOANISSUE_DATABASE_ID)
                # GUIDE DB도 동기화
                sync_cache_from_notion(GUIDE_DATABASE_ID)
            except Exception as e:
                logger.warning(f"[WARN] 캐시 동기화 실패 (계속 진행): {e}")
        else:
            logger.info("[INFO] --skip-sync 플래그로 캐시 동기화 건너뜀")
        
        # Publisher Service 초기화 (메인 스레드용, 주간 작업 등에서 사용)
        publisher_service = PublisherService()

        # 1회 즉시 실행 (스케줄러 시작 전 또는 단발성 실행 시)
        logger.info(">>> 작업 실행 시작 <<<")
        start_regular_tasks(publisher_service)
        
        # --once 플래그가 있으면 여기서 종료
        if args.once:
            logger.info("--once 플래그 감지: 1회 실행 후 종료합니다.")
            return

        # 스케줄러 설정 (반복 모드일 경우에만 설정)
        # 1. 정기 크롤링 (매 시간)
        schedule.every(1).hours.do(start_regular_tasks, publisher_service)
        
        # 2. 키워드 통계 분석 (6시간마다 - 최적화)
        schedule.every(6).hours.do(start_keyword_analysis_task)
        
        # 3. 주간 작업 (매주 금요일 오후 6시)
        schedule.every().friday.at("18:00").do(start_weekly_tasks, publisher_service)

        if RUN_SCHEDULER:
            logger.info(f"[{datetime.now()}] 내부 스케줄러가 시작되었습니다. (Loop Mode)")
            
            # 이미 위에서 1회 실행했으므로 바로 대기 모드 진입
            # start_keyword_analysis_task() # 필요시 초기 1회 실행
            
            logger.info(f"\n[{datetime.now()}] 스케줄러 대기 모드 진입 (다음 실행 예정)...")
            while True:
                schedule.run_pending()
                time.sleep(60)
        else:
            logger.info("내부 스케줄러 설정(RUN_SCHEDULER)이 비활성화되어 있습니다. 종료합니다.")
    
    finally:
        # 🔒 항상 락 해제 (프로그램 종료 시)
        release_lock()

if __name__ == "__main__":
    main()