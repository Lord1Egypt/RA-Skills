"""歌曲下载 CLI 入口 - 歌曲海下载工具

输出: JSON（ensure_ascii=False）
退出码: 0=成功, 1=错误
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

# Windows 控制台默认编码不支持中文，强制 UTF-8
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("mousic-cli")


def _output(data: dict, exit_code: int = 0) -> None:
    """输出 JSON 并退出。"""
    print(json.dumps(data, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


# ========== 歌曲命令 ==========


def cmd_music_search(args: argparse.Namespace) -> None:
    """搜索歌曲。"""
    from real_mousic.chrome_launcher import ensure_chrome, kill_chrome
    from real_mousic.xhs.cdp import Browser
    from real_mousic.music.search import search_songs

    # 确保 Chrome 运行（使用 headless 模式）
    if not ensure_chrome(port=args.port, headless=True, start_url="https://www.gequhai.com/"):
        _output({"success": False, "error": "无法启动 Chrome"}, exit_code=2)
        return

    browser = Browser(host=args.host, port=args.port)
    browser.connect()
    page = browser.get_or_create_page()

    try:
        results = search_songs(page, args.song, max_results=args.max_results)

        if results:
            songs_output = []
            for r in results:
                songs_output.append({
                    "rank": r.rank,
                    "title": r.title,
                    "artist": r.artist,
                    "album": r.album,
                    "song_id": r.song_id,
                    "detail_url": r.detail_url
                })

            _output({
                "success": True,
                "query": args.song,
                "total_found": len(results),
                "songs": songs_output,
                "hint": "请告诉用户选择第几首歌曲（回复数字序号）"
            })
        else:
            _output({
                "success": False,
                "error": f"未找到歌曲: {args.song}",
                "query": args.song,
                "hint": "建议用户尝试其他关键词"
            })
    finally:
        browser.close_page(page)
        browser.close()
        # 关闭 Chrome 进程
        kill_chrome(port=args.port)


def cmd_music_download(args: argparse.Namespace) -> None:
    """获取歌曲下载链接。"""
    from real_mousic.chrome_launcher import ensure_chrome, kill_chrome
    from real_mousic.xhs.cdp import Browser
    from real_mousic.music.search import get_download_links, SearchResult

    # 确保 Chrome 运行（使用 headless 模式）
    if not ensure_chrome(port=args.port, headless=True, start_url="https://www.gequhai.com/"):
        _output({"success": False, "error": "无法启动 Chrome"}, exit_code=2)
        return

    browser = Browser(host=args.host, port=args.port)
    browser.connect()
    page = browser.get_or_create_page()

    try:
        # 构建搜索结果对象
        song = SearchResult(
            rank=1,
            title=args.title or "",
            artist=args.artist or "",
            album="",
            song_id=args.song_id or "",
            detail_url=args.detail_url
        )

        download_info = get_download_links(page, song)

        output = {
            "success": True,
            "song_title": download_info.song_title,
            "artist": download_info.artist,
            "high_quality": None,
            "low_quality": None
        }

        # 处理高品质下载（夸克网盘）
        if download_info.high_quality_url:
            if download_info.high_quality_url.startswith("https://pan.quark.cn/"):
                output["high_quality"] = {
                    "url": download_info.high_quality_url,
                    "type": "quark",
                    "description": "高品质MP3（夸克网盘）"
                }
            else:
                output["high_quality"] = {
                    "url": download_info.high_quality_url,
                    "type": "unknown",
                    "description": "高品质下载链接（非夸克网盘，请验证）",
                    "warning": "链接不是夸克网盘，请用户确认是否安全"
                }

        # 处理低品质下载
        if download_info.low_quality_url:
            if download_info.low_quality_is_quark:
                output["low_quality"] = {
                    "url": download_info.low_quality_url,
                    "type": "quark",
                    "description": "低品质MP3（夸克网盘）"
                }
            elif download_info.low_quality_is_direct:
                output["low_quality"] = {
                    "url": download_info.low_quality_url,
                    "type": "direct",
                    "description": "低品质MP3（浏览器直链下载）",
                    "warning": "此链接可能触发浏览器直接下载，请用户确认是否继续"
                }
            else:
                output["low_quality"] = {
                    "url": download_info.low_quality_url,
                    "type": "unknown",
                    "description": "低品质下载链接"
                }

        # 添加提示信息
        if not download_info.high_quality_url and not download_info.low_quality_url:
            output["success"] = False
            output["error"] = "未找到下载链接"
            output["hint"] = "该歌曲可能暂无下载资源"

        _output(output)
    finally:
        browser.close_page(page)
        browser.close()
        # 关闭 Chrome 进程
        kill_chrome(port=args.port)


def cmd_music_search_and_download(args: argparse.Namespace) -> None:
    """搜索歌曲并获取下载链接（一步到位）。"""
    from real_mousic.chrome_launcher import ensure_chrome, kill_chrome
    from real_mousic.xhs.cdp import Browser
    from real_mousic.music.search import search_songs, get_download_links

    # 确保 Chrome 运行（使用 headless 模式）
    if not ensure_chrome(port=args.port, headless=True, start_url="https://www.gequhai.com/"):
        _output({"success": False, "error": "无法启动 Chrome"}, exit_code=2)
        return

    browser = Browser(host=args.host, port=args.port)
    browser.connect()
    page = browser.get_or_create_page()

    try:
        # 1. 搜索歌曲
        results = search_songs(page, args.song, max_results=args.max_results)

        if not results:
            _output({
                "success": False,
                "error": f"未找到歌曲: {args.song}",
                "query": args.song
            })
            return

        # 2. 如果指定了序号，直接获取下载链接
        if args.index is not None and 1 <= args.index <= len(results):
            selected_song = results[args.index - 1]
            download_info = get_download_links(page, selected_song)

            output = {
                "success": True,
                "query": args.song,
                "selected": {
                    "rank": selected_song.rank,
                    "title": selected_song.title,
                    "artist": selected_song.artist
                },
                "high_quality": None,
                "low_quality": None
            }

            # 处理高品质下载
            if download_info.high_quality_url:
                if download_info.high_quality_url.startswith("https://pan.quark.cn/"):
                    output["high_quality"] = {
                        "url": download_info.high_quality_url,
                        "type": "quark",
                        "description": "高品质MP3（夸克网盘）"
                    }
                else:
                    output["high_quality"] = {
                        "url": download_info.high_quality_url,
                        "type": "unknown",
                        "warning": "链接不是夸克网盘"
                    }

            # 处理低品质下载
            if download_info.low_quality_url:
                if download_info.low_quality_is_quark:
                    output["low_quality"] = {
                        "url": download_info.low_quality_url,
                        "type": "quark",
                        "description": "低品质MP3（夸克网盘）"
                    }
                elif download_info.low_quality_is_direct:
                    output["low_quality"] = {
                        "url": download_info.low_quality_url,
                        "type": "direct",
                        "warning": "此链接可能触发浏览器直接下载"
                    }
                else:
                    output["low_quality"] = {
                        "url": download_info.low_quality_url,
                        "type": "unknown"
                    }

            _output(output)

        else:
            # 3. 返回搜索结果让用户选择
            songs_output = []
            for r in results:
                songs_output.append({
                    "rank": r.rank,
                    "title": r.title,
                    "artist": r.artist,
                    "album": r.album,
                    "song_id": r.song_id,
                    "detail_url": r.detail_url
                })

            _output({
                "success": True,
                "need_selection": True,
                "query": args.song,
                "total_found": len(results),
                "songs": songs_output,
                "hint": "请告诉用户选择第几首歌曲"
            })
    finally:
        browser.close_page(page)
        browser.close()
        # 关闭 Chrome 进程
        kill_chrome(port=args.port)


# ========== 参数解析 ==========


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mousic",
        description="🐄 Real mousic - 歌曲下载工具",
    )

    # 全局选项
    parser.add_argument("--host", default="127.0.0.1", help="Chrome 调试主机")
    parser.add_argument("--port", type=int, default=9222, help="Chrome 调试端口")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # music-search
    sub = subparsers.add_parser("search", help="搜索歌曲")
    sub.add_argument("--song", required=True, help="歌曲名称")
    sub.add_argument("--max-results", type=int, default=10, help="最多返回结果数（默认10）")
    sub.set_defaults(func=cmd_music_search)

    # music-download
    sub = subparsers.add_parser("download", help="获取歌曲下载链接")
    sub.add_argument("--detail-url", required=True, help="歌曲详情页URL")
    sub.add_argument("--title", help="歌曲标题")
    sub.add_argument("--artist", help="歌手")
    sub.add_argument("--song-id", help="歌曲ID")
    sub.set_defaults(func=cmd_music_download)

    # music-get（搜索+下载一步到位）
    sub = subparsers.add_parser("get", help="搜索歌曲并获取下载链接")
    sub.add_argument("--song", required=True, help="歌曲名称")
    sub.add_argument("--index", type=int, help="直接选择第N首歌曲（可选，不填则返回列表）")
    sub.add_argument("--max-results", type=int, default=10, help="搜索结果数量（默认10）")
    sub.set_defaults(func=cmd_music_search_and_download)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
