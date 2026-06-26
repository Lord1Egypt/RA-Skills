#!/usr/bin/env python3
"""
KataGo 棋谱下载模块
支持断点续传、404检测、内存监控
"""

import gc
import re
import time
import signal
import tarfile
import threading
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Iterator, Callable
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import AutoState for auto mode
from ..auto import AutoState


# KataGo 配置
KATAGO_BASE_URL = "https://katagoarchive.org/kata1/ratinggames/"


class MemoryMonitor:
    """内存监控器"""
    def __init__(self, max_memory_mb: int):
        self.max_memory_mb = max_memory_mb
        self.warning_threshold = max_memory_mb * 0.9
        self.critical_threshold = max_memory_mb
        self._check_import()
    
    def _check_import(self):
        try:
            import psutil
            self.psutil = psutil
            self.has_psutil = True
        except ImportError:
            self.has_psutil = False
    
    def get_memory_mb(self) -> float:
        """获取当前内存使用（MB）"""
        if self.has_psutil:
            process = self.psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        else:
            # 使用简单的对象计数估算
            return 0
    
    def check(self) -> Tuple[str, float]:
        """检查内存状态，返回 (status, memory_mb)
        status: 'ok', 'warning', 'critical'
        """
        mem = self.get_memory_mb()
        if mem >= self.critical_threshold:
            return 'critical', mem
        elif mem >= self.warning_threshold:
            return 'warning', mem
        return 'ok', mem
    
    def force_gc(self):
        """强制垃圾回收"""
        gc.collect()


class ProgressManager:
    """进度管理器（断点续传）"""
    def __init__(self, progress_file: Path):
        self.progress_file = progress_file
        self.data = self._load()
    
    def _load(self) -> dict:
        import json
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"ProgressManager load error: {e}")
                pass
        return {
            'completed_dates': [],
            'count_map': {},
            'total_sgfs': 0,
            'start_time': None
        }
    
    def save(self):
        """保存进度"""
        import json
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def is_completed(self, date_str: str) -> bool:
        return date_str in self.data.get('completed_dates', [])
    
    def mark_completed(self, date_str: str, stats: dict):
        if date_str not in self.data.get('completed_dates', []):
            self.data.setdefault('completed_dates', []).append(date_str)
        # 更新统计
        self.data['total_sgfs'] = self.data.get('total_sgfs', 0) + stats.get('sgf_count', 0)
        self.save()
    
    def update_count_map(self, count_map: dict):
        """更新计数映射"""
        for k, v in count_map.items():
            self.data.setdefault('count_map', {})[k] = self.data.get('count_map', {}).get(k, 0) + v
    
    def get_count_map(self) -> dict:
        return self.data.get('count_map', {})
    
    def clear(self):
        """清除进度"""
        if self.progress_file.exists():
            self.progress_file.unlink()
        self.data = {
            'completed_dates': [],
            'count_map': {},
            'total_sgfs': 0,
            'start_time': None
        }


class DownloadManager:
    """下载管理器（支持重试、进度显示、404检测）"""
    def __init__(self, cache_dir: Path, max_retries: int = 3, workers: int = 1, keep_cache: bool = True, delay: int = 10):
        self.cache_dir = cache_dir
        self.max_retries = max_retries
        self.workers = workers
        self.keep_cache = keep_cache
        self.delay = delay
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._completed = 0
        self._total = 0
        self._current_file = ""
        self._start_time = time.time()
    
    def set_keep_cache(self, keep: bool):
        """设置是否保留缓存"""
        self.keep_cache = keep
    
    def stop(self):
        self._stop_event.set()
    
    def is_stopped(self) -> bool:
        return self._stop_event.is_set()
    
    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds/60)}m{int(seconds%60)}s"
        else:
            return f"{int(seconds/3600)}h{int((seconds%3600)/60)}m"
    
    def download_single(self, date_str: str) -> Tuple[str, Optional[Path], Optional[str], bool]:
        """
        下载单个日期文件
        
        返回:
            (date_str, file_path, error, from_cache)
            error为None表示成功，为"404"表示文件不存在（也算成功但不下载），其他为错误信息
            from_cache为True表示从缓存读取，False表示新下载
        """
        url = f"{KATAGO_BASE_URL}{date_str}rating.tar.bz2"
        output_path = self.cache_dir / f"{date_str}rating.tar.bz2"
        
        # 如果文件已存在且有效，跳过
        if output_path.exists() and output_path.stat().st_size > 1000:
            with self._lock:
                self._completed += 1
            return date_str, output_path, None, True
        
        # 执行下载（已通过fetch_available_dates确认文件存在）
        for attempt in range(self.max_retries):
            if self._stop_event.is_set():
                return date_str, None, "stopped"
            
            try:
                self._current_file = f"{date_str}.tar.bz2"
                # 下载（使用完整浏览器请求头）
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Referer': 'https://katagoarchive.org/kata1/ratinggames/',
                    'Connection': 'keep-alive',
                })
                
                with urllib.request.urlopen(req, timeout=60) as response:
                    with open(output_path, 'wb') as f:
                        while True:
                            if self._stop_event.is_set():
                                return date_str, None, "stopped"
                            chunk = response.read(8192)
                            if not chunk:
                                break
                            f.write(chunk)
                
                with self._lock:
                    self._completed += 1
                # 下载成功后延迟，避免触发服务器频率限制
                time.sleep(self.delay)
                return date_str, output_path, None, False
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(5 * (2 ** attempt))  # 指数退避，基础5秒
                else:
                    with self._lock:
                        self._completed += 1
                    return date_str, None, str(e), False
        
        return date_str, None, "max retries exceeded", False
    
    def download(self, dates: List[str], on_progress: Optional[Callable[[str, int, int], None]] = None) -> Tuple[Dict[str, Path], Dict[str, str], int]:
        """
        批量下载，返回成功下载的文件映射、失败信息和缓存命中数
        
        Args:
            dates: 日期列表
            on_progress: 进度回调函数(date_str, current, total)
        
        返回:
            (success_map, error_map, cache_hits)
            success_map: {date_str: file_path, ...}
            error_map: {date_str: error_message, ...}
            cache_hits: 缓存命中数
        """
        self._total = len(dates)
        self._completed = 0
        self._start_time = time.time()
        
        success_map = {}
        error_map = {}
        cache_hits = 0
        completed_count = 0
        
        def download_single_wrapped(date_str: str) -> Tuple[str, Optional[Path], Optional[str], bool]:
            return self.download_single(date_str)
        
        # 使用线程池并行下载
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {executor.submit(download_single_wrapped, d): d for d in dates}
            
            for future in as_completed(futures):
                if self._stop_event.is_set():
                    break
                date_str, path, error, from_cache = future.result()
                completed_count += 1
                if on_progress:
                    on_progress(date_str, completed_count, self._total)
                if path:
                    success_map[date_str] = path
                    if from_cache:
                        cache_hits += 1
                elif error:
                    error_map[date_str] = error
        
        return success_map, error_map, cache_hits
    
    def print_progress(self):
        """打印当前进度"""
        elapsed = time.time() - self._start_time
        if self._completed > 0:
            avg_time = elapsed / self._completed
            remaining = (self._total - self._completed) * avg_time
        else:
            remaining = 0
        
        percent = (self._completed / self._total * 100) if self._total > 0 else 0
        
        print(f"\r📥 下载进度: {self._completed}/{self._total} ({percent:.1f}%) "
              f"| 当前: {self._current_file:<20} "
              f"| 剩余时间: {self._format_time(remaining)}", end='', flush=True)


def iter_sgf_from_tar(tar_path: Path) -> Iterator[str]:
    """
    从tar.bz2文件中迭代读取SGF内容
    
    Yields:
        SGF字符串
    """
    tar_path = Path(tar_path) if isinstance(tar_path, str) else tar_path
    if not tar_path.exists():
        return
    
    try:
        with tarfile.open(tar_path, 'r:bz2') as tar:
            for member in tar.getmembers():
                if not member.isfile() or not member.name.endswith('.sgf'):
                    continue
                
                try:
                    f = tar.extractfile(member)
                    if f is None:
                        continue
                    
                    sgf_data = f.read().decode('utf-8', errors='ignore')
                    yield sgf_data
                except:
                    continue
    except Exception:
        return


def fetch_available_dates() -> List[str]:
    """
    从KataGo Archive列表页面获取所有可下载的日期
    
    Returns:
        可下载的日期列表 (YYYY-MM-DD格式)
    """
    index_url = f"{KATAGO_BASE_URL}index.html"
    
    try:
        req = urllib.request.Request(index_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://katagoarchive.org/',
            'Connection': 'keep-alive',
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # 提取所有 YYYY-MM-DD rating.tar.bz2 链接
        # 匹配模式如: 2024-01-15rating.tar.bz2
        pattern = r'(\d{4}-\d{2}-\d{2})rating\.tar\.bz2'
        matches = re.findall(pattern, html)
        
        # 去重并排序
        available_dates = sorted(set(matches))
        return available_dates
        
    except Exception as e:
        print(f"⚠️  获取可用日期列表失败: {e}")
        return []


def download_katago_games(
    start_date: str,
    end_date: str,
    cache_dir: Optional[Path] = None,
    max_retries: int = 3,
    workers: int = 1,
    keep_cache: bool = True,
    resume: bool = False,
    delay: int = 10,
    on_progress: Optional[Callable[[str, int, int], None]] = None
) -> Tuple[List[Path], List[str]]:
    """
    下载KataGo棋谱文件
    
    Args:
        start_date: 起始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        cache_dir: 缓存目录，默认 ~/.weiqi-joseki/katago-cache
        max_retries: 最大重试次数
        workers: 并行下载线程数
        keep_cache: 是否保留缓存文件
        resume: 是否断点续传
        delay: 下载间隔延迟（秒）
        on_progress: 进度回调函数(date_str, current, total)
    
    返回:
        (downloaded_files, missing_dates)
        downloaded_files: 成功下载的文件路径列表
        missing_dates: 文件不存在的日期列表（404）
    """
    from pathlib import Path
    
    # 获取服务器上可用的日期列表
    print("📋 正在获取可用日期列表...")
    available_dates = fetch_available_dates()
    if not available_dates:
        print("⚠️  无法获取可用日期列表，将尝试所有日期")
        available_dates = []
    else:
        print(f"✅ 服务器共有 {len(available_dates)} 个日期的棋谱")
    
    # 解析日期
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # 生成日期列表
    all_dates = []
    current = start
    while current <= end:
        all_dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    
    # 与可用日期取交集
    if available_dates:
        available_set = set(available_dates)
        dates = [d for d in all_dates if d in available_set]
        skipped_dates = [d for d in all_dates if d not in available_set]
        if skipped_dates:
            print(f"⏭️  跳过 {len(skipped_dates)} 个服务器不存在的日期")
    else:
        dates = all_dates
    
    # 确保日期按升序排列
    dates = sorted(dates)
    
    # 设置默认缓存目录
    if cache_dir is None:
        cache_dir = Path.home() / ".weiqi-joseki" / "katago-cache"
    
    # 创建下载管理器
    manager = DownloadManager(
        cache_dir=cache_dir,
        max_retries=max_retries,
        workers=workers,
        keep_cache=keep_cache,
        delay=delay
    )
    
    # 断点续传：加载进度文件
    progress_file = cache_dir.parent / "katago-progress.json"
    if resume and progress_file.exists():
        import json
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
            completed = progress_data.get('completed_dates', [])
            dates = [d for d in dates if d not in completed]
        except:
            pass
    
    # 下载
    downloaded_map, error_map, cache_hits = manager.download(dates, on_progress=on_progress)
    
    # 分类结果
    downloaded_files = list(downloaded_map.values())
    missing_dates = [d for d in dates if d not in downloaded_map]
    
    # 计算统计信息
    total_to_download = len(dates)
    new_downloads = len(downloaded_map) - cache_hits
    failed_downloads = len(error_map)
    
    # 显示下载统计
    print(f"\n📊 下载统计:")
    print(f"  - 总计需要: {total_to_download} 个")
    print(f"  - 缓存命中: {cache_hits} 个 ({cache_hits/total_to_download*100:.1f}%)")
    print(f"  - 新下载成功: {new_downloads} 个")
    if new_downloads > 0:
        success_rate = new_downloads / (new_downloads + failed_downloads) * 100 if (new_downloads + failed_downloads) > 0 else 0
        print(f"  - 新下载失败: {failed_downloads} 个")
        print(f"  - 新下载成功率: {success_rate:.1f}%")
    
    # 显示下载失败原因
    if error_map:
        print(f"\n⚠️  下载失败详情:")
        # 按错误类型统计
        error_counts = {}
        for date_str, error in error_map.items():
            # 简化错误信息
            short_error = error.split(':')[0] if ':' in error else error
            error_counts[short_error] = error_counts.get(short_error, 0) + 1
        
        for error_type, count in sorted(error_counts.items(), key=lambda x: -x[1]):
            print(f"  - {error_type}: {count} 个")
        
        # 显示前10个具体失败案例
        if len(error_map) > 0:
            print(f"\n  前10个失败示例:")
            for i, (date_str, error) in enumerate(list(error_map.items())[:10]):
                print(f"    {date_str}: {error[:80]}")
    
    return downloaded_files, missing_dates


def download_auto(
    state: AutoState,
    cache_dir: Optional[Path] = None,
    max_retries: int = 3,
    delay: int = 10,
    on_progress: Optional[Callable[[str, int, int], None]] = None
) -> List[str]:
    """自动增量下载KataGo棋谱
    
    根据state中记录的已下载日期，自动检测并下载缺失的日期。
    每成功下载一个日期，自动更新state。
    
    Args:
        state: 自动模式状态管理器
        cache_dir: 缓存目录，默认 ~/.weiqi-joseki/katago-cache
        max_retries: 最大重试次数
        delay: 下载间隔延迟（秒）
        on_progress: 进度回调函数(date_str, current, total)
    
    Returns:
        本次新下载的日期列表（已排序）
    """
    # 设置默认缓存目录
    if cache_dir is None:
        cache_dir = Path.home() / ".weiqi-joseki" / "katago-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取服务器上所有可用日期
    print("📋 正在获取可用日期列表...")
    available_dates = fetch_available_dates()
    if not available_dates:
        print("⚠️  无法获取可用日期列表")
        return []
    
    print(f"✅ 服务器共有 {len(available_dates)} 个日期的棋谱")
    
    # 获取待下载的日期（基于文件系统检查）
    pending_dates = []
    for date_str in available_dates:
        tar_path = cache_dir / f"{date_str}rating.tar.bz2"
        if not tar_path.exists():
            pending_dates.append(date_str)
    
    if not pending_dates:
        print("✅ 所有可用日期已下载，无需增量下载")
        return []
    
    print(f"📥 需要下载 {len(pending_dates)} 个新日期: {pending_dates[0]} ~ {pending_dates[-1]}")
    
    # 创建下载管理器
    manager = DownloadManager(
        cache_dir=cache_dir,
        max_retries=max_retries,
        workers=1,  # 串行下载，避免触发频率限制
        keep_cache=True,
        delay=delay
    )
    
    # 执行下载
    downloaded_map, error_map, cache_hits = manager.download(pending_dates, on_progress=on_progress)
    
    # 收集新下载的日期
    new_downloaded = []
    for date_str in pending_dates:
        if date_str in downloaded_map:
            new_downloaded.append(date_str)
    
    # 统计输出
    print(f"\n📊 下载统计:")
    print(f"  - 需要下载: {len(pending_dates)} 个")
    print(f"  - 成功: {len(new_downloaded)} 个")
    print(f"  - 失败: {len(error_map)} 个")
    print(f"  - 缓存命中: {cache_hits} 个")
    
    if error_map:
        print(f"\n⚠️  下载失败:")
        for date_str, error in list(error_map.items())[:5]:
            print(f"    {date_str}: {error[:60]}")
        if len(error_map) > 5:
            print(f"    ... 还有 {len(error_map) - 5} 个")
    
    return new_downloaded
