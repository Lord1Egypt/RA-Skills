#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能文件下载器
支持多线程、断点续传、进度显示
"""

import sys
import asyncio
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any
from urllib.parse import urlparse
from datetime import datetime

# 检查依赖
try:
    import httpx
    from httpx import HTTPStatusError, RequestError, StreamError
    from rich.progress import (
        Progress,
        BarColumn,
        DownloadColumn,
        TextColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
        TransferSpeedColumn,
        SpinnerColumn
    )
except ImportError as e:
    print(f"错误: 缺少必要的依赖库")
    print(f"请安装: pip install httpx aiofiles rich")
    sys.exit(1)


class SmartDownloader:
    """智能文件下载器"""

    def __init__(
        self,
        urls: List[str],
        output_dir: str,
        max_workers: int = 4,
        chunk_size: int = 2 * 1024 * 1024,  # 2MB
        timeout: int = 10,
        retry: int = 5,
        headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None
    ):
        self.urls = urls
        self.output_dir = Path(output_dir)
        self.temp_dir = self.output_dir / ".temp"
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        self.timeout = timeout
        self.retry = retry
        self.headers = headers or {}
        self.proxy = proxy

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

        # 默认请求头
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.default_headers.update(self.headers)

    async def download_file(
        self,
        client: httpx.AsyncClient,
        url: str,
        progress: Progress,
        task_id: Any
    ) -> bool:
        """
        下载单个文件

        Args:
            client: HTTP 客户端
            url: 下载 URL
            progress: Rich 进度对象
            task_id: 任务 ID

        Returns:
            是否成功
        """
        # 解析文件名
        parsed = urlparse(url)
        filename = Path(parsed.path).name or f"download_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_path = self.output_dir / filename
        temp_path = self.temp_dir / f"{filename}.tmp"

        # 检查是否已下载
        if output_path.exists():
            print(f"✓ 文件已存在，跳过: {filename}")
            return True

        # 检查断点续传
        downloaded_size = 0
        if temp_path.exists():
            downloaded_size = temp_path.stat().st_size
            print(f"✓ 检测到临时文件，从断点继续: {filename} ({downloaded_size} bytes)")

        # 下载参数
        headers = self.default_headers.copy()
        if downloaded_size > 0:
            headers["Range"] = f"bytes={downloaded_size}-"

        # 下载文件
        attempt = 0
        while attempt < self.retry:
            try:
                async with client.stream(
                    "GET",
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    follow_redirects=True
                ) as response:
                    response.raise_for_status()

                    # 获取总大小
                    total_size = int(response.headers.get("content-length", 0))
                    if downloaded_size > 0:
                        total_size += downloaded_size

                    # 下载文件
                    mode = "ab" if downloaded_size > 0 else "wb"
                    with open(temp_path, mode) as f:
                        async for chunk in response.aiter_bytes(chunk_size=self.chunk_size):
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            progress.update(task_id, completed=downloaded_size, total=total_size)

                    # 下载完成，移动文件
                    temp_path.rename(output_path)
                    progress.update(task_id, completed=total_size, total=total_size)
                    print(f"✓ 下载成功: {filename}")
                    return True

            except (HTTPStatusError, RequestError, StreamError) as e:
                attempt += 1
                if attempt < self.retry:
                    print(f"✗ 下载失败，重试 ({attempt}/{self.retry}): {filename} - {e}")
                    await asyncio.sleep(1)
                else:
                    print(f"✗ 下载失败，已达到最大重试次数: {filename} - {e}")
                    return False
            except Exception as e:
                print(f"✗ 下载失败: {filename} - {e}")
                return False

        return False

    async def download_all(self) -> None:
        """下载所有文件"""
        # 配置 HTTP 客户端
        client_config = {
            "timeout": self.timeout,
            "follow_redirects": True,
        }
        if self.proxy:
            client_config["proxies"] = {
                "http://": self.proxy,
                "https://": self.proxy
            }

        async with httpx.AsyncClient(**client_config) as client:
            # 使用 Rich 进度条
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=None,  # 使用默认控制台
            ) as progress:
                # 创建下载任务
                tasks = []
                for url in self.urls:
                    filename = Path(urlparse(url).path).name or "unknown"
                    task_id = progress.add_task(f"[cyan]{filename}", total=None)
                    tasks.append((url, task_id))

                # 并发下载
                semaphore = asyncio.Semaphore(self.max_workers)

                async def download_with_semaphore(url: str, task_id: Any):
                    async with semaphore:
                        return await self.download_file(client, url, progress, task_id)

                await asyncio.gather(*[
                    download_with_semaphore(url, task_id)
                    for url, task_id in tasks
                ])

        # 清理临时目录
        if self.temp_dir.exists():
            for file in self.temp_dir.iterdir():
                try:
                    file.unlink()
                except Exception:
                    pass
            print("\n✓ 临时目录已清理")


def load_urls_from_file(file_path: str) -> List[str]:
    """从文件加载 URL 列表"""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            if url and not url.startswith('#'):
                urls.append(url)
    return urls


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='智能文件下载器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s urls.txt output/
  %(prog)s "https://example.com/file1.jpg,https://example.com/file2.jpg" output/
  %(prog)s urls.txt output/ --max-workers 8 --timeout 30
  %(prog)s urls.txt output/ --proxy http://127.0.0.1:7890
        """
    )
    parser.add_argument('urls',
                       help='URL 列表（逗号分隔或文件路径）')
    parser.add_argument('output_dir',
                       help='输出目录')
    parser.add_argument('--max-workers', '-w', type=int, default=4,
                       help='最大并发数（默认: 4）')
    parser.add_argument('--chunk-size', type=int, default=2*1024*1024,
                       help='分块大小（字节，默认: 2MB）')
    parser.add_argument('--timeout', type=int, default=10,
                       help='请求超时时间（秒，默认: 10）')
    parser.add_argument('--retry', type=int, default=5,
                       help='最大重试次数（默认: 5）')
    parser.add_argument('--headers',
                       help='自定义请求头（JSON 格式）')
    parser.add_argument('--proxy',
                       help='代理地址（HTTP/HTTPS/SOCKS5）')

    args = parser.parse_args()

    # 加载 URL
    urls = []
    if Path(args.urls).exists():
        urls = load_urls_from_file(args.urls)
        print(f"✓ 从文件加载 {len(urls)} 个 URL")
    else:
        urls = [url.strip() for url in args.urls.split(',') if url.strip()]
        print(f"✓ 从命令行加载 {len(urls)} 个 URL")

    if not urls:
        print("错误: 没有有效的 URL")
        sys.exit(1)

    # 解析请求头
    headers = None
    if args.headers:
        import json
        try:
            headers = json.loads(args.headers)
        except json.JSONDecodeError as e:
            print(f"错误: 无效的 JSON 格式: {e}")
            sys.exit(1)

    # 创建下载器
    downloader = SmartDownloader(
        urls=urls,
        output_dir=args.output_dir,
        max_workers=args.max_workers,
        chunk_size=args.chunk_size,
        timeout=args.timeout,
        retry=args.retry,
        headers=headers,
        proxy=args.proxy
    )

    # 下载
    print(f"\n✓ 准备下载 {len(urls)} 个文件到: {args.output_dir}")
    print(f"✓ 并发数: {args.max_workers}")
    print(f"✓ 分块大小: {args.chunk_size // 1024 // 1024} MB")
    print(f"✓ 超时: {args.timeout} 秒")
    print(f"✓ 重试次数: {args.retry}")
    if args.proxy:
        print(f"✓ 代理: {args.proxy}")
    print()

    asyncio.run(downloader.download_all())


if __name__ == '__main__':
    main()
