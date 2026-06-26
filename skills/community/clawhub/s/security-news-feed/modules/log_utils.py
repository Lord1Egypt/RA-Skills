# modules/log_utils.py
"""
구조화된 로깅 모듈
디버깅 효율 향상을 위해 메트릭 수집 및 이벤트 로깅 제공
"""
import logging
import os
import time
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# 로그 형식 설정
LOG_FORMAT = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """
    표준 로거 설정 함수
    
    Args:
        name: 로거 이름
        log_file: 로그 파일 경로 (None일 경우 콘솔에만 출력)
        level: 로깅 레벨
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 중복 핸들러 방지
    if logger.handlers:
        return logger

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 파일 핸들러
    if log_file:
        # 로그 디렉토리 생성
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(str(log_path), encoding='utf-8')
        file_handler.setLevel(logging.DEBUG) # 파일에는 디버그 레벨까지 기록
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# 기본 로거 생성 (security_aggregator)
# 프로젝트 루트/logs/security_aggregator.log 에 저장
try:
    # 현재 파일 위치: modules/log_utils.py
    # 서브모듈 루트: modules/../
    submodule_root = Path(__file__).resolve().parent.parent
    log_dir = submodule_root / "logs"
    default_log_file = log_dir / "security_aggregator.log"
except:
    default_log_file = "security_aggregator.log"

logger = setup_logger('security_aggregator', str(default_log_file))

# Suppress WDM (WebDriver Manager) logs
logging.getLogger('WDM').setLevel(logging.WARNING)
logging.getLogger('webdriver_manager').setLevel(logging.WARNING)


class Metrics:
    """
    성능 메트릭 수집 클래스
    API 호출 시간, 큐 대기 시간 등을 측정
    """
    def __init__(self):
        self.api_call_times: Dict[str, list] = {}
        self.queue_wait_times: list = []
        self.success_rate: Dict[str, int] = {'success': 0, 'error': 0}

    def record_api_call(self, operation: str, duration: float):
        """API 호출 시간 기록"""
        if operation not in self.api_call_times:
            self.api_call_times[operation] = []
        self.api_call_times[operation].append(duration)

    def record_queue_wait(self, wait_time: float):
        """큐 대기 시간 기록"""
        self.queue_wait_times.append(wait_time)

    def record_success(self):
        """성공 횟수 기록"""
        self.success_rate['success'] += 1

    def record_error(self):
        """실패 횟수 기록"""
        self.success_rate['error'] += 1

    def get_avg_api_time(self, operation: str) -> Optional[float]:
        """평균 API 시간 계산"""
        if operation not in self.api_call_times or not self.api_call_times[operation]:
            return None
        return sum(self.api_call_times[operation]) / len(self.api_call_times[operation])

    def get_avg_queue_wait(self) -> Optional[float]:
        """평균 큐 대기 시간 계산"""
        if not self.queue_wait_times:
            return None
        return sum(self.queue_wait_times) / len(self.queue_wait_times)

    def get_success_rate(self) -> float:
        """성공률 계산"""
        total = self.success_rate['success'] + self.success_rate['error']
        if total == 0:
            return 0.0
        return self.success_rate['success'] / total

    def reset(self):
        """메트릭 초기화"""
        self.api_call_times.clear()
        self.queue_wait_times.clear()
        self.success_rate = {'success': 0, 'error': 0}

    def get_summary(self) -> Dict[str, Any]:
        """메트릭 요약 반환"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'api_calls': {},
            'queue': {
                'avg_wait_time': self.get_avg_queue_wait(),
                'total_wait_events': len(self.queue_wait_times)
            },
            'success_rate': {
                'success': self.success_rate['success'],
                'error': self.success_rate['error'],
                'rate': self.get_success_rate()
            }
        }

        for operation, times in self.api_call_times.items():
            summary['api_calls'][operation] = {
                'count': len(times),
                'avg_time': sum(times) / len(times) if times else 0,
                'total_time': sum(times)
            }

        return summary


# 전역 메트릭 인스턴스
metrics = Metrics()


class LogContext:
    """
    구조화된 로그 컨텍스트
    이벤트 타입별로 통일된 로그 형식 제공
    """
    @staticmethod
    def log_event(event_type: str, **kwargs):
        """
        구조화된 이벤트 로그

        Args:
            event_type: 이벤트 타입 (api_call, queue_event, processing, error, crawler_result)
            **kwargs: 이벤트별 데이터
        """
        log_data = {
            'event': event_type,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }

        # 이벤트 타입별 로그 포맷
        if event_type == 'api_call':
            operation = kwargs.get('operation', 'unknown')
            duration = kwargs.get('duration', 0)
            status = kwargs.get('status', 'unknown')
            input_length = kwargs.get('input_length', 0)
            logger.info(f"[API] {operation} | {status} | {duration:.2f}s | Input: {input_length} chars")

        elif event_type == 'queue_event':
            action = kwargs.get('action', 'unknown')
            title = kwargs.get('title', '')
            queue_size = kwargs.get('queue_size', 0)
            logger.info(f"[QUEUE] {action} | {title[:30]}... | Queue size: {queue_size}")

        elif event_type == 'processing':
            stage = kwargs.get('stage', 'unknown')
            title = kwargs.get('title', '')
            source = kwargs.get('source', 'unknown')
            duration = kwargs.get('duration', 0)
            logger.info(f"[PROCESS] {stage} | {source} | {title[:30]}... | {duration:.2f}s")

        elif event_type == 'error':
            stage = kwargs.get('stage', 'unknown')
            title = kwargs.get('title', '')
            error = kwargs.get('error', 'unknown')
            source = kwargs.get('source', 'unknown')
            logger.error(f"[ERROR] {stage} | {source} | {title[:30]}... | {error}")

        elif event_type == 'crawler_result':
            source = kwargs.get('source', 'unknown')
            success = kwargs.get('success', 0)
            duplicate = kwargs.get('duplicate', 0)
            old = kwargs.get('old', 0)
            error = kwargs.get('error', 0)
            total = kwargs.get('total', 0)
            logger.info(f"[CRAWLER] {source} | Success: {success} | Duplicate: {duplicate} | Old: {old} | Error: {error} | Total: {total}")

        else:
            logger.info(f"[EVENT] {event_type} | {kwargs}")


# 편의한 로깅 함수들
def log_api_call_start(operation: str, title: Optional[str] = None, input_length: int = 0):
    """API 호출 시작 로그"""
    LogContext.log_event('api_call',
                       operation=operation,
                       status='started',
                       title=title,
                       input_length=input_length)


def log_api_call_end(operation: str, duration: float, title: Optional[str] = None):
    """API 호출 종료 로그"""
    metrics.record_api_call(operation, duration)
    metrics.record_success()

    LogContext.log_event('api_call',
                       operation=operation,
                       status='completed',
                       title=title,
                       duration=duration)


def log_api_call_error(operation: str, error: Exception, title: Optional[str] = None):
    """API 호출 에러 로그"""
    metrics.record_error()

    LogContext.log_event('error',
                       stage=f'api_call_{operation}',
                       title=title,
                       error=str(error))


def log_queue_add(title: str, queue_size: int):
    """큐 추가 로그"""
    LogContext.log_event('queue_event',
                       action='add',
                       title=title,
                       queue_size=queue_size)


def log_queue_take(title: str, queue_size: int, wait_time: float = 0):
    """큐 가져오기 로그"""
    metrics.record_queue_wait(wait_time)

    LogContext.log_event('queue_event',
                       action='take',
                       title=title,
                       queue_size=queue_size)


def log_processing_start(source: str, title: str):
    """처리 시작 로그"""
    LogContext.log_event('processing',
                       stage='start',
                       source=source,
                       title=title)


def log_processing_end(source: str, title: str, duration: float):
    """처리 종료 로그"""
    LogContext.log_event('processing',
                       stage='complete',
                       source=source,
                       title=title,
                       duration=duration)


def log_processing_error(source: str, title: str, error: Exception, stage: str = 'unknown'):
    """처리 에러 로그"""
    metrics.record_error()

    LogContext.log_event('error',
                       stage=stage,
                       source=source,
                       title=title,
                       error=str(error))


def log_crawler_result(source: str, success: int, duplicate: int, old: int, error: int, total: int):
    """크롤러 결과 로그"""
    LogContext.log_event('crawler_result',
                       source=source,
                       success=success,
                       duplicate=duplicate,
                       old=old,
                       error=error,
                       total=total)


def print_metrics_summary():
    """메트릭 요약 출력"""
    summary = metrics.get_summary()

    print("\n" + "="*70)
    print("📊 성능 메트릭 요약")
    print("="*70)
    print(f"📅 기준 시간: {summary['timestamp']}")

    # API 호출 요약
    print("\n📡 API 호출 통계:")
    for operation, data in summary['api_calls'].items():
        print(f"  {operation}:")
        print(f"    호출 횟수: {data['count']}")
        print(f"    평균 시간: {data['avg_time']:.2f}초")
        print(f"    총 시간: {data['total_time']:.2f}초")

    # 큐 통계
    print("\n📦 큐 통계:")
    print(f"  평균 대기 시간: {summary['queue']['avg_wait_time']:.2f}초" if summary['queue']['avg_wait_time'] else "  평균 대기 시간: N/A")
    print(f"  대기 이벤트 수: {summary['queue']['total_wait_events']}")

    # 성공률
    print("\n✅ 처리 통계:")
    print(f"  성공: {summary['success_rate']['success']}")
    print(f"  실패: {summary['success_rate']['error']}")
    print(f"  성공률: {summary['success_rate']['rate']:.2%}")

    print("="*70 + "\n")
