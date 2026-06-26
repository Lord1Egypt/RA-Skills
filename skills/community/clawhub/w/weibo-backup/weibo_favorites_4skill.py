import argparse
import asyncio
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
from playwright.async_api import async_playwright, Browser, Page, BrowserContext

"""

===== 当前支持 分批 batch_size 下载；支持视频下载；支持本地长文章下载
             
=====

# 使用默认配置 下载360尺寸图片，不下载视频，下载10条，覆盖已有记录
python weibo_favorites_4skill.py

# == 日常使用 == 下载原图，下载视频，下载6000条 , 跳过存在记录  使用 headless 模式   使用持久化用户数据目录
 python weibo_favorites_4skill.py --image-size large --download-video --max-download 6000 --skip-existing --user-data-dir ./browser_data --headless

# 方式1: 使用 cookies 文件保存登录状态（默认启用）
python weibo_favorites_4skill.py --max-download 10
# 首次运行需要登录，登录后会自动保存 cookies.json，下次运行自动加载

# 方式2: 使用持久化用户数据目录（推荐，更稳定）
python weibo_favorites_4skill.py --user-data-dir ./browser_data --max-download 10
# 登录状态会保存在 browser_data 目录中，下次运行自动恢复

# 方式3: 使用 headless 模式（后台运行，不显示浏览器窗口）
# 注意：首次登录不能使用 headless，需要先在有界面的模式下登录
python weibo_favorites_4skill.py --user-data-dir ./browser_data --headless --max-download 10

# 方式4: 连接已运行的浏览器（需要先启动 Chrome）
# Windows: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
python weibo_favorites_4skill.py --connect-browser --cdp-endpoint http://localhost:9222

# 自动登录模式说明：
# 1) 若当前目录不存在 cookies.json，或未提供 --url，会先打开 weibo.com
# 2) 提醒用户登录并进入需要下载的页面（收藏页/本人主页/他人主页）
# 3) 等待60秒后自动开始下载
"""

# 默认配置值（可通过命令行参数覆盖）
DEFAULT_MAX_DOWNLOAD = 10
DEFAULT_MAX_IDLE_ROUNDS = 30       # 增大空闲轮次，避免提前退出
DEFAULT_SCROLL_WAIT_SECONDS = 1.5  # 减少等待时间，提高滚动速度
DEFAULT_STABILITY_CHECK_ROUNDS = 2  # 减少稳定性检查轮次
DEFAULT_SCROLL_STEP_RATIO = 0.85   # 每次滚动约一个视口高度
DEFAULT_PAGE_STABLE_MAX_WAIT = 3.0  # 页面稳定性检查最大等待时间
DEFAULT_PAGE_STABLE_CHECK_INTERVAL = 0.3  # 页面稳定性检查间隔
DEFAULT_BATCH_SIZE = 20  # 每批下载数量

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
PICTURES_DIR = OUTPUT_DIR / "pictures"
VIDEOS_DIR = OUTPUT_DIR / "videos"
ARTICLES_DIR = OUTPUT_DIR / "articles"
ARTICLE_PICTURES_DIR = ARTICLES_DIR / "pictures"
USER_DATA_DIR = BASE_DIR / "browser_data"  # 浏览器用户数据目录
COOKIES_FILE = BASE_DIR / "cookies.json"   # Cookies 文件

# 全局缓存：存储已存在的记录ID
_existing_record_ids: set[str] = set()
_existing_article_ids: set[str] = set()
_existing_article_md_map: dict[str, Path] = {}

# 记录链信息
_record_chain_info: dict | None = None  # 存储链的头部和尾部记录信息


def find_record_chain_tail() -> dict | None:
    """
    扫描所有已存在的 markdown 文件，找到记录链的尾部记录。
    通过解析双向链接中的 "下一条" 链接来追踪链的结尾。
    返回尾部记录的信息字典，如果没有找到则返回 None。
    """
    if not OUTPUT_DIR.exists():
        return None
    
    # 获取所有 markdown 文件
    md_files = list(OUTPUT_DIR.glob("*.md"))
    if not md_files:
        return None
    
    # 构建记录ID到文件信息的映射
    # 文件名格式: author_date_time_recordid.md (如: 爱可可-爱生活_2026-04-12_0832_QApYcsCLc.md)
    record_map: dict[str, dict] = {}
    for md_file in md_files:
        record_id = md_file.stem
        # 从文件名提取 record_id: 最后一部分是 record_id
        parts = record_id.rsplit('_', 1)
        if len(parts) == 2:
            rid = parts[1]  # record_id (如 QApYcsCLc)
            prefix = parts[0]  # author_date_time (如 爱可可-爱生活_2026-04-12_0832)
            # 验证 record_id 格式（字母数字组合，通常8位左右）
            if rid and len(rid) >= 6:
                # 从 prefix 中提取作者和时间信息（简化处理）
                # 假设最后两部分是日期和时间
                prefix_parts = prefix.rsplit('_', 2)
                if len(prefix_parts) >= 3:
                    author = '_'.join(prefix_parts[:-2])  # 作者名（可能包含下划线）
                    date_str = prefix_parts[-2]
                    time_str = prefix_parts[-1]
                    timestamp = f"{date_str}_{time_str}"
                else:
                    author = prefix
                    timestamp = ""
                
                record_map[rid] = {
                    "record_id": rid,
                    "file_name": md_file.name,
                    "file_path": md_file,
                    "author": author,
                    "timestamp": timestamp,
                    "full_id": record_id,
                }
    
    if not record_map:
        return None
    
    # 解析每个文件的导航链接，构建链接关系图
    # next_links: record_id -> next_record_id
    # prev_links: record_id -> prev_record_id
    next_links: dict[str, str] = {}
    prev_links: dict[str, str] = {}
    
    for rid, info in record_map.items():
        try:
            content = info["file_path"].read_text(encoding="utf-8")
            lines = content.split("\n")
            
            # 查找导航链接行（在 ## 正文 之前的行）
            for i, line in enumerate(lines):
                if line == "## 正文":
                    # 往前查找导航链接
                    for j in range(i - 1, -1, -1):
                        nav_line = lines[j].strip()
                        if nav_line == "":
                            continue
                        # 解析导航链接
                        # 格式: "前一条：[描述](filename.md) | 下一条：[描述](filename.md)"
                        if "前一条：" in nav_line or "下一条：" in nav_line:
                            # 提取 "下一条" 链接
                            next_match = re.search(r'下一条：\[.*?\]\(([^)]+\.md)\)', nav_line)
                            if next_match:
                                next_file = next_match.group(1)
                                next_rid = Path(next_file).stem.rsplit('_', 1)[-1] if '_' in Path(next_file).stem else Path(next_file).stem
                                if next_rid in record_map:
                                    next_links[rid] = next_rid
                                    prev_links[next_rid] = rid
                            
                            # 提取 "前一条" 链接
                            prev_match = re.search(r'前一条：\[.*?\]\(([^)]+\.md)\)', nav_line)
                            if prev_match:
                                prev_file = prev_match.group(1)
                                prev_rid = Path(prev_file).stem.rsplit('_', 1)[-1] if '_' in Path(prev_file).stem else Path(prev_file).stem
                                if prev_rid in record_map:
                                    prev_links[rid] = prev_rid
                                    next_links[prev_rid] = rid
                        break
                    break
        except Exception as e:
            print(f"  解析文件导航链接失败: {info['file_path'].name} -> {e}")
            continue
    
    # 找到链的尾部：没有 "下一条" 链接的记录
    tail_records = []
    for rid in record_map:
        if rid not in next_links:
            tail_records.append(rid)
    
    if not tail_records:
        # 所有记录都有下一条，可能形成环，选择最新的记录（按文件名排序）
        sorted_records = sorted(record_map.values(), key=lambda x: x["file_name"], reverse=True)
        if sorted_records:
            tail_info = sorted_records[0]
            print(f"  找到链尾部记录(最新): {tail_info['file_name']}")
            return _build_tail_info(tail_info, record_map)
        return None
    
    if len(tail_records) == 1:
        tail_rid = tail_records[0]
        tail_info = record_map[tail_rid]
        print(f"  找到链尾部记录: {tail_info['file_name']}")
        return _build_tail_info(tail_info, record_map)
    
    # 多个尾部记录，选择文件名最新的
    sorted_tails = sorted([record_map[rid] for rid in tail_records], key=lambda x: x["file_name"], reverse=True)
    tail_info = sorted_tails[0]
    print(f"  找到多个链尾部，选择最新: {tail_info['file_name']}")
    return _build_tail_info(tail_info, record_map)


def _build_tail_info(tail_info: dict, record_map: dict) -> dict:
    """构建尾部记录的完整信息，包括文本预览"""
    try:
        content = tail_info["file_path"].read_text(encoding="utf-8")
        lines = content.split("\n")
        
        # 提取正文内容（在 ## 正文 和 --------- 之间）
        body_start = -1
        body_end = -1
        for i, line in enumerate(lines):
            if line == "## 正文":
                body_start = i + 1
            elif body_start > 0 and line == "---------":
                body_end = i
                break
        
        text_preview = "(无正文)"
        if body_start > 0 and body_end > body_start:
            body_lines = lines[body_start:body_end]
            body_text = "\n".join(line for line in body_lines if line.strip()).strip()
            if body_text:
                text_preview = body_text[:30] + "..." if len(body_text) > 30 else body_text
                text_preview = text_preview.replace('\n', ' ').replace('\r', ' ')
        
        return {
            "record_id": tail_info["record_id"],
            "author": tail_info["author"],
            "publish_time": tail_info["timestamp"],
            "file_name": tail_info["file_name"],
            "text_preview": text_preview,
        }
    except Exception as e:
        print(f"  读取尾部记录内容失败: {e}")
        return {
            "record_id": tail_info["record_id"],
            "author": tail_info["author"],
            "publish_time": tail_info["timestamp"],
            "file_name": tail_info["file_name"],
            "text_preview": "(无正文)",
        }


def update_index_md(tail_record_info: dict):
    """
    创建/更新 index.md 入口主页，链接指向最新的链尾部记录。
    文件位置在 python 脚本同一级目录。
    """
    try:
        # index.md 位于脚本同一级目录
        index_path = BASE_DIR / "index.md"
        
        # 构建链接文本：作者 + 时间 + 内容预览
        author = tail_record_info.get("author", "未知作者")
        publish_time = tail_record_info.get("publish_time", "")
        text_preview = tail_record_info.get("text_preview", "")
        file_name = tail_record_info.get("file_name", "")
        
        # 格式化发布时间
        time_display = publish_time.replace('_', ' ') if publish_time else ""
        
        # 构建链接描述
        link_text = f"{author} {time_display} {text_preview}".strip()
        if len(link_text) > 50:
            link_text = link_text[:50] + "..."
        
        # 构建链接路径：指向 output 目录下的文件
        file_path = f"output/{file_name}"
        
        # 创建 index.md 内容
        # 格式：前一条：[描述](output/filename.md)
        index_content = f"前一条：[{link_text}]({file_path})\n"
        
        # 写入文件
        index_path.write_text(index_content, encoding='utf-8')
        print(f"  ✓ 已更新 index.md: {link_text}")
        
    except Exception as e:
        print(f"  ⚠️ 更新 index.md 失败: {e}")


def sanitize_name(value: str) -> str:
    """清理文件名中的非法字符"""
    sanitized = re.sub(r"[^\w\-\.]+", "_", value.strip(), flags=re.UNICODE)
    return sanitized.strip("._") or "record"


def canonicalize_text(value: str) -> str:
    """清理微博卡片里的冗余文案，避免同一条内容在不同展开状态下生成不同指纹。"""
    text = str(value or "").replace("\r\n", "\n")
    lines = []
    skip_exact = {
        "播放视频",
        "展开",
        "收起",
        "添加",
    }
    skip_prefixes = (
        "来自 ",
        "转发",
        "评论",
        "赞",
        "收藏",
        "分享",
    )
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line in skip_exact:
            continue
        if any(line.startswith(prefix) for prefix in skip_prefixes):
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", line):
            continue
        if re.fullmatch(r"\d+(?:\.\d+)?[万千]次观看", line):
            continue
        if re.fullmatch(r"\d+", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def normalize_record(raw: dict, fallback_index: int) -> dict:
    """规范化微博记录数据"""
    text = str(raw.get("text", "") or "").strip()
    canonical_text = canonicalize_text(text)
    author = str(raw.get("author", "") or "").strip() or "unknown"
    publish_time = str(raw.get("publish_time", "") or "").strip()
    source_url = str(raw.get("source_url", "") or "").strip()
    dom_id = str(raw.get("id", "") or "").strip()
    
    # 使用从时间链接中提取的微博短ID作为唯一标识
    raw_id = dom_id if dom_id else ""

    image_groups = []
    for group in raw.get("image_groups", []) or []:
        valid_images = []
        for img in group:
            url_text = str(img.get("url", "") or "").strip()
            if url_text.startswith("http://") or url_text.startswith("https://"):
                valid_images.append({
                    "url": url_text,
                    "width": img.get("width", 300),
                    "height": img.get("height", 300)
                })
        if valid_images:
            image_groups.append(valid_images)

    # 生成去重指纹
    if raw_id:
        dedupe_key = raw_id
    else:
        dedupe_seed_parts = [
            source_url,
            author,
            publish_time,
            canonical_text or text,
        ]
        dedupe_seed = "|".join(part for part in dedupe_seed_parts if part)
        if not dedupe_seed:
            dedupe_seed = f"fallback|{fallback_index}"
        dedupe_key = hashlib.sha1(dedupe_seed.encode("utf-8")).hexdigest()[:16]
        raw_id = dedupe_key
    
    # 处理视频URL
    video_urls = []
    for url in raw.get("video_urls", []) or []:
        url_text = str(url or "").strip()
        if url_text.startswith("http://") or url_text.startswith("https://"):
            video_urls.append(url_text)
    video_urls = list(dict.fromkeys(video_urls))

    # 检测长文章链接
    long_article_url = ""
    for link in raw.get("web_links", []) or []:
        url = str(link.get("url", "") or link.get("realUrl", "") or link.get("real_url", "") or "").strip()
        if "/ttarticle/p/show" in url or "ttarticle" in url or "article/m/show" in url:
            long_article_url = url
            break
    
    return {
        "record_id": sanitize_name(raw_id),
        "dedupe_key": dedupe_key,
        "author": author,
        "publish_time": publish_time,
        "text": canonical_text or text,
        "source_url": source_url,
        "image_groups": image_groups,
        "video_urls": video_urls,
        "long_article_url": long_article_url,
    }


def image_extension(image_url: str) -> str:
    """获取图片扩展名"""
    ext = Path(urlparse(image_url).path).suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}:
        return ext
    return ".jpg"


def convert_image_size(image_url: str, target_size: str) -> str:
    """
    转换微博图片URL到指定尺寸。
    target_size: '360' -> orj360, '480' -> orj480, '690' -> mw690, '2000' -> mw2000, 'large' -> large
    """
    size_map = {
        '360': 'orj360',
        '480': 'orj480', 
        '690': 'mw690',
        '2000': 'mw2000',
        'large': 'large'
    }
    
    if target_size not in size_map:
        return image_url
    
    target_prefix = size_map[target_size]
    
    for size_key, prefix in size_map.items():
        if prefix in image_url:
            return image_url.replace(prefix, target_prefix)
    
    return image_url


def video_extension(video_url: str) -> str:
    """获取视频扩展名"""
    ext = Path(urlparse(video_url).path).suffix.lower()
    if ext in {".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv"}:
        return ext
    return ".mp4"


async def get_browser_cookies(page: Page) -> str:
    """从浏览器获取cookies字符串 - Playwright 版本"""
    cookies = await page.context.cookies()
    return "; ".join(f"{c['name']}={c['value']}" for c in cookies)


async def save_cookies(context: BrowserContext):
    """保存 cookies 到文件"""
    cookies = await context.cookies()
    COOKIES_FILE.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✓ 已保存登录状态到: {COOKIES_FILE}")


async def load_cookies(context: BrowserContext) -> bool:
    """从文件加载 cookies"""
    if not COOKIES_FILE.exists():
        return False
    
    try:
        cookies = json.loads(COOKIES_FILE.read_text(encoding='utf-8'))
        await context.add_cookies(cookies)
        print(f"✓ 已加载登录状态: {COOKIES_FILE}")
        return True
    except Exception as e:
        print(f"⚠️  加载 cookies 失败: {e}")
        return False


async def get_browser_user_agent(page: Page) -> str:
    """从浏览器获取User-Agent - Playwright 版本"""
    return await page.evaluate("navigator.userAgent")


async def download_image_with_context(
    context: BrowserContext, 
    image_url: str, 
    target_path: Path, 
    min_size_kb: int = 5,
    user_agent: str = ""
) -> bool:
    """
    使用 Playwright 的浏览器上下文下载图片。
    返回True表示成功，False表示失败。
    """
    try:
        # 构建请求头（微博图片需要 Referer）
        headers = {
            "Referer": "https://weibo.com/",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        }
        
        if user_agent:
            headers["User-Agent"] = user_agent
        
        # 使用浏览器的 request 上下文下载，带上 cookies 和正确的请求头
        response = await context.request.get(image_url, headers=headers)
        
        if not response.ok:
            print(f"图片下载失败（HTTP {response.status}）: {image_url}")
            return False
        
        data = await response.body()
        
        # 检查文件大小
        file_size_kb = len(data) / 1024
        if file_size_kb < min_size_kb:
            print(f"图片文件太小（{file_size_kb:.1f}KB < {min_size_kb}KB），跳过: {image_url}")
            return False
        
        target_path.write_bytes(data)
        return True
    except Exception as e:
        print(f"图片下载失败: {image_url} -> {e}")
        return False


async def download_video_with_context(
    context: BrowserContext,
    video_url: str,
    target_path: Path,
    user_agent: str = "",
    timeout_ms: int = 300000,  # 默认5分钟超时，大视频需要更长时间
) -> bool:
    """
    使用流式下载方式下载视频，避免大文件内存问题。
    """
    try:
        # 从浏览器获取 cookies
        cookies = await context.cookies()
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        
        # 构建请求头（微博视频需要 Referer）
        headers = {
            "Referer": "https://weibo.com/",
            "Cookie": cookie_str,
        }
        
        if user_agent:
            headers["User-Agent"] = user_agent
        
        # 使用 aiohttp 进行流式下载，避免大文件内存问题
        timeout = aiohttp.ClientTimeout(total=timeout_ms / 1000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(video_url, headers=headers) as response:
                if response.status != 200:
                    print(f"视频下载失败（HTTP {response.status}）: {video_url}")
                    return False
                
                # 流式写入文件
                downloaded_size = 0
                with open(target_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                
                print(f"✓ 视频下载成功: {target_path.name} ({downloaded_size / 1024 / 1024:.1f}MB)")
                return True
    except Exception as e:
        print(f"视频下载失败: {video_url} -> {e}")
        return False


async def extract_real_video_url(page: Page, video_page_url: str) -> dict | None:
    """
    从微博视频播放页面提取真实的视频文件URL - Playwright 版本
    返回格式: {"url": "视频URL", "width": 宽度, "height": 高度}
    """
    # 在新标签页中打开视频页面
    video_page = await page.context.new_page()
    
    best_source = None
    try:
        # 使用 domcontentloaded 而不是 networkidle，避免视频页面加载超时
        # 视频页面有很多媒体资源，networkidle 可能会超时
        try:
            await video_page.goto(video_page_url, wait_until="domcontentloaded", timeout=30000)
        except Exception as e:
            print(f"  页面加载警告（可忽略）: {str(e)[:100]}")
        
        # 等待视频元素或脚本加载
        await asyncio.sleep(3)
        
        # 提取所有视频源及其分辨率信息
        script = """() => {
            const videos = [];
            
            // 方法1: 检查 video 元素的 source 子元素
            const videoElement = document.querySelector('video');
            if (videoElement) {
                // 主视频源
                if (videoElement.src || videoElement.currentSrc) {
                    videos.push({
                        url: videoElement.src || videoElement.currentSrc,
                        width: videoElement.videoWidth || 0,
                        height: videoElement.videoHeight || 0
                    });
                }
                
                // 检查 source 子元素
                const sources = videoElement.querySelectorAll('source');
                sources.forEach(source => {
                    const url = source.src || source.getAttribute('src');
                    if (url) {
                        videos.push({
                            url: url,
                            width: source.getAttribute('data-width') || videoElement.videoWidth || 0,
                            height: source.getAttribute('data-height') || videoElement.videoHeight || 0
                        });
                    }
                });
            }
            
            // 方法2: 从页面脚本中提取视频信息
            const scripts = document.querySelectorAll('script');
            scripts.forEach(script => {
                const content = script.textContent || '';
                const urlMatches = content.match(/https?:\\/\\/[^"\\s]+\\.mp4[^"\\s]*/g) || [];
                urlMatches.forEach(url => {
                    const sizeMatch = url.match(/(\\d+)x(\\d+)/);
                    videos.push({
                        url: url,
                        width: sizeMatch ? parseInt(sizeMatch[1]) : 0,
                        height: sizeMatch ? parseInt(sizeMatch[2]) : 0
                    });
                });
            });
            
            // 方法3: 查找播放器配置
            const playerConfig = window.__INITIAL_STATE__ || window.__playinfo__ || window.videoData;
            if (playerConfig) {
                try {
                    const configStr = JSON.stringify(playerConfig);
                    const urlMatches = configStr.match(/https?:\\/\\/[^"\\s]+\\.mp4[^"\\s]*/g) || [];
                    urlMatches.forEach(url => {
                        const sizeMatch = url.match(/(\\d+)x(\\d+)/);
                        videos.push({
                            url: url,
                            width: sizeMatch ? parseInt(sizeMatch[1]) : 0,
                            height: sizeMatch ? parseInt(sizeMatch[2]) : 0
                        });
                    });
                } catch (e) {}
            }
            
            return videos;
        }"""
        
        videos = await video_page.evaluate(script)
        
        if videos:
            # 选择分辨率最高的视频
            valid_videos = [v for v in videos if v.get('url') and v['url'].startswith('http')]
            if valid_videos:
                best_source = max(valid_videos, key=lambda v: v.get('width', 0) * v.get('height', 0))
        
    except Exception as e:
        print(f"提取视频URL失败: {video_page_url} -> {e}")
    finally:
        await video_page.close()
    
    return best_source


async def extract_long_article(page: Page, article_url: str) -> dict | None:
    """
    抓取长文章的完整内容和图片 - Playwright 版本
    返回包含 title, content, images 等字段的字典。
    图片和图片说明会被正确提取并配对。
    """
    article_page = await page.context.new_page()
    
    try:
        await article_page.goto(article_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)
        
        # 主脚本：提取标题、内容和图片（包括图片说明）
        script = """() => {
            try {
                // 尝试多种方式提取文章标题
                var title = '';
                // 1. 尝试从 h1 标签获取
                var h1 = document.querySelector('h1');
                if (h1 && h1.innerText && h1.innerText.trim()) {
                    title = h1.innerText.trim();
                }
                // 2. 尝试从特定 class 的元素获取（微博长文章常见标题 class）
                if (!title) {
                    var titleSelectors = [
                        '[class*="title"]',
                        '[class*="Title"]',
                        '[class*="article-title"]',
                        '[class*="article_title"]',
                        '[class*="headline"]',
                        '.main-content h2',
                        '.article-content h2'
                    ];
                    for (var i = 0; i < titleSelectors.length; i++) {
                        var el = document.querySelector(titleSelectors[i]);
                        if (el && el.innerText && el.innerText.trim() && el.innerText.trim().length < 200) {
                            title = el.innerText.trim();
                            break;
                        }
                    }
                }
                // 3. 回退到 document.title
                if (!title) {
                    title = document.title || '';
                }
                // 清理标题（移除 "- 微博" 等后缀）
                title = title.replace(/\\s*[-|]\\s*微博.*$/i, '').trim();

                // 查找文章主体内容区域
                var rootCandidates = Array.from(document.querySelectorAll('.WB_editor_iframe_new, article, [class*="article"], [class*="content"], [class*="text"], main'))
                    .filter(function(el) { return el && el.innerText && (el.innerText || '').length > 200; });
                var root = rootCandidates.sort(function(a, b) { return ((b.innerText || '').length - (a.innerText || '').length); })[0] || document.body;

                var images = [];
                var processedUrls = {};
                var imageIndex = 0;

                // 检查是否为有效图片
                var isValidImage = function(img) {
                    if (!img) return false;
                    var url = img.src || img.getAttribute('data-src') || '';
                    if (!url || url.indexOf('http') !== 0) return false;
                    if (url.indexOf('sinaimg.cn') === -1) return false;

                    var parent = img.parentElement;
                    var depth = 0;
                    var parentChain = '';
                    while (parent && depth < 5) {
                        var className = parent.className || '';
                        parentChain += ' ' + className;
                        if (/avatar|head|icon|logo/i.test(className)) return false;
                        parent = parent.parentElement;
                        depth++;
                    }
                    if (/woo-avatar|user-info|author-info|icon-main/i.test(parentChain)) return false;

                    var width = img.naturalWidth || img.width || 0;
                    var height = img.naturalHeight || img.height || 0;
                    if (width > 0 && height > 0 && (width < 100 || height < 100)) return false;
                    return true;
                };

                // 检查段落是否为图片说明（以▲开头或包含"图 /"）
                var isImageCaption = function(text) {
                    if (!text) return false;
                    text = text.trim();
                    return text.indexOf('▲') === 0 || text.indexOf('图 /') >= 0 || text.indexOf('图/') >= 0;
                };

                // 提取图片说明文本
                var extractCaption = function(text) {
                    if (!text) return '';
                    text = text.trim();
                    // 移除开头的▲符号
                    if (text.indexOf('▲') === 0) {
                        text = text.substring(1).trim();
                    }
                    return text;
                };

                // 序列化节点，提取图片和图片说明
                var serializeNode = function(node) {
                    if (!node) return '';
                    if (node.nodeType === 3) { // Node.TEXT_NODE
                        return node.nodeValue || '';
                    }
                    if (node.nodeType !== 1) return ''; // Node.ELEMENT_NODE

                    var tag = node.tagName.toLowerCase();
                    
                    // 处理图片
                    if (tag === 'img') {
                        var url = node.src || node.getAttribute('data-src') || '';
                        if (!isValidImage(node) || processedUrls[url]) return '';
                        processedUrls[url] = true;
                        var width = node.naturalWidth || node.width || 300;
                        var height = node.naturalHeight || node.height || 300;
                        imageIndex++;
                        var placeholder = '__WEIBO_IMG_' + imageIndex + '__';
                        
                        // 查找图片说明（下一个兄弟节点）
                        var caption = '';
                        var nextSibling = node.parentElement ? node.parentElement.nextElementSibling : null;
                        
                        // 如果父元素是figure，查找figure的下一个兄弟节点
                        if (node.parentElement && node.parentElement.tagName.toLowerCase() === 'figure') {
                            nextSibling = node.parentElement.nextElementSibling;
                        }
                        
                        // 检查下一个节点是否为图片说明
                        if (nextSibling && nextSibling.tagName.toLowerCase() === 'p') {
                            var nextText = (nextSibling.innerText || '').trim();
                            if (isImageCaption(nextText)) {
                                caption = extractCaption(nextText);
                                // 标记这个段落已被处理为图片说明
                                nextSibling.setAttribute('data-is-caption', 'true');
                            }
                        }
                        
                        images.push({ 
                            url: url, 
                            width: width, 
                            height: height, 
                            placeholder: placeholder,
                            caption: caption
                        });
                        return '\\n' + placeholder + '\\n';
                    }

                    if (tag === 'script' || tag === 'style' || tag === 'noscript') return '';

                    // 处理段落
                    if (tag === 'p') {
                        // 检查是否已被标记为图片说明
                        if (node.getAttribute && node.getAttribute('data-is-caption') === 'true') {
                            return ''; // 跳过，已经在图片处理时提取了
                        }
                        
                        // 检查段落内容是否为图片说明
                        var pText = (node.innerText || '').trim();
                        if (isImageCaption(pText)) {
                            // 检查前一个兄弟节点是否为图片
                            var prevSibling = node.previousElementSibling;
                            if (prevSibling) {
                                // 如果前一个节点是figure，说明这个说明已经被处理了
                                if (prevSibling.tagName.toLowerCase() === 'figure') {
                                    return ''; // 跳过，已经在图片处理时提取了
                                }
                                // 检查figure内是否有图片
                                var prevImg = prevSibling.querySelector('img');
                                if (prevImg && isValidImage(prevImg)) {
                                    return ''; // 跳过，已经在图片处理时提取了
                                }
                            }
                        }
                    }

                    var children = '';
                    for (var i = 0; i < node.childNodes.length; i++) {
                        children += serializeNode(node.childNodes[i]);
                    }
                    if (tag === 'br') return '\\n';
                    if (tag === 'p' || tag === 'div' || tag === 'section' || tag === 'article' || tag === 'li') return children + '\\n';
                    return children;
                };

                var content = serializeNode(root)
                    .replace(/\\n{3,}/g, '\\n\\n')
                    .replace(/[ \\t]+\\n/g, '\\n')
                    .trim();

                if (content.length < 200) {
                    content = (document.body.innerText || '').trim();
                }

                var dateMatch = content.match(/(\\d{4}-\\d{2}-\\d{2})/);
                var publishDate = dateMatch ? dateMatch[1] : '';

                return {
                    title: title,
                    content: content,
                    images: images,
                    publish_date: publishDate,
                    url: window.location.href
                };
            } catch (e) {
                return { error: e.toString() };
            }
        }"""
        
        article_data = await article_page.evaluate(script)
        
        # 检查是否有错误
        if article_data and isinstance(article_data, dict):
            if article_data.get("error"):
                print(f"提取长文章时 JavaScript 错误: {article_data.get('error')}")
                # 尝试备用方案
                return await extract_long_article_simple(article_page, article_url)
            if article_data.get("content"):
                await article_page.close()
                return article_data
        
        await article_page.close()
        return None
        
    except Exception as e:
        print(f"提取长文章失败: {article_url} -> {e}")
        # 确保在异常情况下也关闭页面
        try:
            await article_page.close()
        except:
            pass
        return None


async def extract_long_article_simple(page: Page, article_url: str) -> dict | None:
    """
    使用更简单的 JavaScript 提取长文章（备用方案）- Playwright 版本
    也支持提取图片说明，并在正确位置插入图片占位符。
    """
    try:
        # 备用脚本：使用更简单的 ES5 语法
        script = """() => {
            try {
                // 提取标题
                var title = '';
                var h1 = document.querySelector('h1');
                if (h1 && h1.innerText) {
                    title = h1.innerText.trim();
                }
                if (!title) {
                    title = document.title || '';
                }
                title = title.replace(/\\s*[-|]\\s*微博.*$/i, '').trim();

                // 检查段落是否为图片说明
                var isImageCaption = function(text) {
                    if (!text) return false;
                    text = text.trim();
                    return text.indexOf('▲') === 0 || text.indexOf('图 /') >= 0 || text.indexOf('图/') >= 0;
                };

                // 提取图片说明文本
                var extractCaption = function(text) {
                    if (!text) return '';
                    text = text.trim();
                    if (text.indexOf('▲') === 0) {
                        text = text.substring(1).trim();
                    }
                    return text;
                };

                // 查找文章主体内容区域
                var rootCandidates = Array.from(document.querySelectorAll('.WB_editor_iframe_new, article, [class*="article"], [class*="content"], main'))
                    .filter(function(el) { return el && el.innerText && (el.innerText || '').length > 200; });
                var root = rootCandidates.sort(function(a, b) { return ((b.innerText || '').length - (a.innerText || '').length); })[0] || document.body;

                // 提取图片（包括图片说明）
                var images = [];
                var imageIndex = 0;
                var processedUrls = {};
                var imagePlaceholders = {}; // 用于记录图片URL到占位符的映射
                
                // 首先提取所有图片
                var imgElements = root.querySelectorAll('img');
                for (var i = 0; i < imgElements.length; i++) {
                    var img = imgElements[i];
                    var url = img.src || img.getAttribute('data-src') || '';
                    if (!url || url.indexOf('http') !== 0) continue;
                    if (url.indexOf('sinaimg.cn') === -1) continue;
                    if (processedUrls[url]) continue;
                    
                    // 检查尺寸
                    var width = img.naturalWidth || img.width || 0;
                    var height = img.naturalHeight || img.height || 0;
                    if (width > 0 && height > 0 && (width < 100 || height < 100)) continue;
                    
                    processedUrls[url] = true;
                    imageIndex++;
                    var placeholder = '__WEIBO_IMG_' + imageIndex + '__';
                    imagePlaceholders[url] = placeholder;
                    
                    // 查找图片说明
                    var caption = '';
                    var parent = img.parentElement;
                    var nextSibling = null;
                    
                    // 如果父元素是figure，查找figure的下一个兄弟节点
                    if (parent && parent.tagName.toLowerCase() === 'figure') {
                        nextSibling = parent.nextElementSibling;
                    } else if (parent) {
                        nextSibling = parent.nextElementSibling;
                    }
                    
                    // 检查下一个节点是否为图片说明
                    if (nextSibling && nextSibling.tagName.toLowerCase() === 'p') {
                        var nextText = (nextSibling.innerText || '').trim();
                        if (isImageCaption(nextText)) {
                            caption = extractCaption(nextText);
                        }
                    }
                    
                    images.push({ 
                        url: url, 
                        width: width || 300, 
                        height: height || 300, 
                        placeholder: placeholder,
                        caption: caption
                    });
                }

                // 序列化节点，在图片位置插入占位符
                var serializeNode = function(node) {
                    if (!node) return '';
                    if (node.nodeType === 3) { // Node.TEXT_NODE
                        return node.nodeValue || '';
                    }
                    if (node.nodeType !== 1) return ''; // Node.ELEMENT_NODE

                    var tag = node.tagName.toLowerCase();
                    
                    // 处理图片
                    if (tag === 'img') {
                        var url = node.src || node.getAttribute('data-src') || '';
                        if (url && imagePlaceholders[url]) {
                            return '\\n' + imagePlaceholders[url] + '\\n';
                        }
                        return '';
                    }

                    if (tag === 'script' || tag === 'style' || tag === 'noscript') return '';

                    // 处理段落
                    if (tag === 'p') {
                        var pText = (node.innerText || '').trim();
                        // 检查是否为图片说明
                        if (isImageCaption(pText)) {
                            // 检查前一个兄弟节点是否为图片
                            var prevSibling = node.previousElementSibling;
                            if (prevSibling) {
                                // 如果前一个节点是figure，说明这个说明已经被处理了
                                if (prevSibling.tagName.toLowerCase() === 'figure') {
                                    return ''; // 跳过，已经在图片处理时提取了
                                }
                                // 检查figure内是否有图片
                                var prevImg = prevSibling.querySelector('img');
                                if (prevImg && prevImg.src && imagePlaceholders[prevImg.src]) {
                                    return ''; // 跳过，已经在图片处理时提取了
                                }
                            }
                        }
                    }

                    var children = '';
                    for (var i = 0; i < node.childNodes.length; i++) {
                        children += serializeNode(node.childNodes[i]);
                    }
                    if (tag === 'br') return '\\n';
                    if (tag === 'p' || tag === 'div' || tag === 'section' || tag === 'article' || tag === 'li') return children + '\\n';
                    return children;
                };

                var content = serializeNode(root)
                    .replace(/\\n{3,}/g, '\\n\\n')
                    .replace(/[ \\t]+\\n/g, '\\n')
                    .trim();

                if (content.length < 200) {
                    content = (document.body.innerText || '').trim();
                }

                // 提取日期
                var dateMatch = content.match(/(\\d{4}-\\d{2}-\\d{2})/);
                var publishDate = dateMatch ? dateMatch[1] : '';

                return {
                    title: title,
                    content: content,
                    images: images,
                    publish_date: publishDate,
                    url: window.location.href
                };
            } catch (e) {
                return { error: e.toString() };
            }
        }"""
        
        article_data = await page.evaluate(script)
        
        if article_data and isinstance(article_data, dict):
            if article_data.get("error"):
                print(f"备用方案提取长文章时 JavaScript 错误: {article_data.get('error')}")
                return None
            if article_data.get("content"):
                print(f"使用备用方案成功提取长文章")
                return article_data
        
        return None
        
    except Exception as e:
        print(f"备用方案提取长文章失败: {e}")
        return None


async def scroll_and_extract(
    page: Page,
    max_download: int,
    skip_existing: bool,
    image_size: str,
    download_video: bool,
    download_article: bool,
    max_idle_rounds: int,
    scroll_wait_seconds: float,
    stability_check_rounds: int,
    scroll_step_ratio: float,
    batch_size: int,
    user_agent: str,
) -> int:
    """
    滚动页面并提取微博记录，达到 batch_size 即下载该批次。
    返回实际下载数量。
    """
    pending_records: list[dict] = []
    seen_keys = set()
    idle_rounds = 0
    round_count = 0
    downloaded_count = 0
    batch_count = 0
    effective_batch_size = batch_size if batch_size and batch_size > 0 else 1
    
    # 加载已存在的记录
    if skip_existing:
        load_existing_records()
    
    # 使用记录链的尾部作为前一条记录，保持链的连续性
    global _record_chain_info
    prev_record_info: dict | None = _record_chain_info if _record_chain_info else None
    
    if prev_record_info:
        print(f"\n将从链尾部记录继续链接: {prev_record_info['file_name']}")
    
    print(f"开始滚动提取并分批下载，目标下载数: {max_download}，batch_size: {effective_batch_size}")

    async def flush_pending(force: bool = False):
        """按批次下载待处理记录；force=True 时会下载所有剩余记录。"""
        nonlocal pending_records, downloaded_count, batch_count, prev_record_info

        while pending_records:
            if not force and len(pending_records) < effective_batch_size:
                return

            current_batch_size = len(pending_records) if force else effective_batch_size
            current_batch = pending_records[:current_batch_size]
            pending_records = pending_records[current_batch_size:]
            batch_count += 1

            print(f"\n--- 开始下载第 {batch_count} 批，本批 {len(current_batch)} 条 ---")
            for record in current_batch:
                if downloaded_count >= max_download:
                    pending_records = []
                    return

                current_idx = downloaded_count + 1
                print(f"\n[{current_idx}/{max_download}] 处理: {record['record_id']}")
                # 传递前一条记录的信息，并接收当前记录的信息用于下一条
                current_record_info = await download_record(
                    page=page,
                    record=record,
                    image_size=image_size,
                    download_video=download_video,
                    download_article=download_article,
                    user_agent=user_agent,
                    prev_record_info=prev_record_info,
                )
                # 更新前一条记录信息为当前记录
                prev_record_info = current_record_info
                downloaded_count += 1
            print(f"--- 第 {batch_count} 批下载完成，累计已下载 {downloaded_count} 条 ---")
    
    while downloaded_count < max_download and idle_rounds < max_idle_rounds:
        round_count += 1
        print(
            f"\n=== 第 {round_count} 轮滚动 "
            f"(已下载: {downloaded_count}, 待下载: {len(pending_records)}, 空闲: {idle_rounds}/{max_idle_rounds}) ==="
        )
        
        # 提取当前视口中的记录（使用原版本的完整提取逻辑）
        extract_script = """async () => {
            const toAbs = (href) => {
                if (!href) return '';
                try { return new URL(href, location.origin).href; } catch { return ''; }
            };
            
            // 等待函数
            const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
            
            const articles = [...document.querySelectorAll('article')];
            
            // 自动点击所有"展开"按钮
            for (const article of articles) {
                // 查找展开按钮（多种可能的选择器）
                const expandSelectors = [
                    'a[action-type="feed_list_show_more"]',
                    'a[action-type="feed_list_show_all_text"]',
                    '.expand',
                    '[class*="expand"]',
                    'a:has-text("展开")',
                    'span:has-text("展开")'
                ];
                
                for (const selector of expandSelectors) {
                    try {
                        const expandBtn = article.querySelector(selector);
                        if (expandBtn && (expandBtn.textContent.includes('展开') || expandBtn.textContent.includes('...'))) {
                            expandBtn.click();
                            await sleep(100); // 等待展开动画
                            break;
                        }
                    } catch (e) {}
                }
            }
            
            // 等待所有展开动画完成
            await sleep(300);
            
            // 处理 Markdown 开关：如果存在 "Markdown: 开"，点击关闭以获取原始 Markdown 文本
            for (const article of articles) {
                const allElements = article.querySelectorAll('*');
                for (const el of allElements) {
                    if (el.childNodes.length === 1 && el.childNodes[0].nodeType === 3) {
                        const text = el.textContent.trim();
                        if (text === 'Markdown: 开') {
                            el.click();
                            await sleep(800); // 等待切换动画
                            break;
                        }
                    }
                }
            }
            
            const rawRecords = articles.map((article, idx) => {
                const statusLink = [...article.querySelectorAll('a[href*="/status/"]')]
                    .map(a => toAbs(a.getAttribute('href')))
                    .find(Boolean) || '';
                
                // 提取真实的微博短ID（从时间链接中）
                const timeLink = article.querySelector('a[href*="weibo.com"][title]');
                let rawId = '';
                let fullWeiboUrl = '';
                
                if (timeLink) {
                    fullWeiboUrl = toAbs(timeLink.getAttribute('href'));
                    const match = fullWeiboUrl.match(/weibo\\.com\\/\\d+\\/([a-zA-Z0-9]+)/);
                    if (match) {
                        rawId = match[1];
                    }
                }
                
                if (!rawId && statusLink) {
                    const statusMatch = statusLink.match(/\\/status\\/(\\d+)/);
                    if (statusMatch) {
                        rawId = statusMatch[1];
                    }
                }
                
                // 提取图片及其布局信息
                const imageGroups = [];
                const processedImages = new Set();
                let imagesPerRow = 3;
                
                const isValidContentImage = (img) => {
                    const url = img.url || '';
                    const width = img.width || 0;
                    const height = img.height || 0;
                    const parentChain = img.parentChain || [];
                    
                    const invalidParentClasses = [
                        'avatar', 'head', 'user-info', 'author-info',
                        'woo-icon', 'icon-main', 'woo-avatar',
                        '_wbtext_', 'card-small', 'timeline-card'
                    ];
                    
                    for (const parent of parentChain) {
                        const className = parent.className || '';
                        for (const invalidClass of invalidParentClasses) {
                            if (className.toLowerCase().includes(invalidClass.toLowerCase())) {
                                return false;
                            }
                        }
                    }
                    
                    if (url.includes('tva') && url.includes('sinaimg.cn')) {
                        return false;
                    }
                    if (url.includes('h5.sinaimg.cn')) {
                        return false;
                    }
                    if (url.includes('/upload/') || url.includes('/crop.')) {
                        return false;
                    }
                    if (width > 0 && height > 0 && (width < 100 || height < 100)) {
                        return false;
                    }
                    if (url.includes('emoji') || url.includes('emotion')) {
                        return false;
                    }
                    
                    return true;
                };
                
                const pictureContainers = article.querySelectorAll('[class*="picture"]');
                pictureContainers.forEach(container => {
                    const innerContainer = container.querySelector('[class*="inlineNum"]');
                    if (innerContainer) {
                        const classMatch = innerContainer.className.match(/inlineNum(\\d+)/);
                        if (classMatch) {
                            imagesPerRow = parseInt(classMatch[1]);
                        }
                    }
                    
                    const images = [...container.querySelectorAll('img')]
                        .map(img => {
                            let parent = img.parentElement;
                            const parentChain = [];
                            let depth = 0;
                            while (parent && parent !== article && depth < 5) {
                                parentChain.push({
                                    className: parent.className || '',
                                    tagName: parent.tagName || ''
                                });
                                parent = parent.parentElement;
                                depth++;
                            }
                            
                            return {
                                url: toAbs(img.getAttribute('src') || img.getAttribute('data-src') || ''),
                                width: img.naturalWidth || img.width || 300,
                                height: img.naturalHeight || img.height || 300,
                                parentChain: parentChain
                            };
                        })
                        .filter(img => /^https?:\\/\\//.test(img.url) && 
                                       !processedImages.has(img.url) && 
                                       isValidContentImage(img));
                    
                    if (images.length > 0) {
                        images.forEach(img => processedImages.add(img.url));
                        for (let i = 0; i < images.length; i += imagesPerRow) {
                            imageGroups.push(images.slice(i, i + imagesPerRow));
                        }
                    }
                });
                
                if (imageGroups.length === 0) {
                    const contentSelectors = [
                        '[class*="content"]',
                        '[class*="text"]',
                        '[class*="detail"]',
                        '[class*="main"]'
                    ];
                    
                    let contentImages = [];
                    for (const selector of contentSelectors) {
                        const contentArea = article.querySelector(selector);
                        if (contentArea) {
                            contentImages = [...contentArea.querySelectorAll('img')]
                                .map(img => {
                                    let parent = img.parentElement;
                                    const parentChain = [];
                                    let depth = 0;
                                    while (parent && parent !== article && depth < 5) {
                                        parentChain.push({
                                            className: parent.className || '',
                                            tagName: parent.tagName || ''
                                        });
                                        parent = parent.parentElement;
                                        depth++;
                                    }
                                    
                                    return {
                                        url: toAbs(img.getAttribute('src') || img.getAttribute('data-src') || ''),
                                        width: img.naturalWidth || img.width || 300,
                                        height: img.naturalHeight || img.height || 300,
                                        parentChain: parentChain
                                    };
                                })
                                .filter(img => /^https?:\\/\\//.test(img.url) && isValidContentImage(img));
                            
                            if (contentImages.length > 0) {
                                break;
                            }
                        }
                    }
                    
                    if (contentImages.length === 0) {
                        contentImages = [...article.querySelectorAll('img')]
                            .map(img => {
                                let parent = img.parentElement;
                                const parentChain = [];
                                let depth = 0;
                                while (parent && parent !== article && depth < 5) {
                                    parentChain.push({
                                        className: parent.className || '',
                                        tagName: parent.tagName || ''
                                    });
                                    parent = parent.parentElement;
                                    depth++;
                                }
                                
                                return {
                                    url: toAbs(img.getAttribute('src') || img.getAttribute('data-src') || ''),
                                    width: img.naturalWidth || img.width || 300,
                                    height: img.naturalHeight || img.height || 300,
                                    parentChain: parentChain
                                };
                            })
                            .filter(img => /^https?:\\/\\//.test(img.url) && isValidContentImage(img));
                    }
                    
                    if (contentImages.length > 0) {
                        imageGroups.push(contentImages);
                    }
                }
                
                // 提取视频URL - 增强版，支持多种微博视频格式
                const videoUrls = [];
                
                // 方法1: 直接从 video 元素提取
                const videoElements = article.querySelectorAll('video');
                videoElements.forEach(video => {
                    const src = video.getAttribute('src') || video.currentSrc || '';
                    if (src) videoUrls.push(toAbs(src));
                    // 也检查 source 子元素
                    video.querySelectorAll('source').forEach(source => {
                        const sourceSrc = source.getAttribute('src');
                        if (sourceSrc) videoUrls.push(toAbs(sourceSrc));
                    });
                });
                
                // 方法2: 从视频链接提取
                const videoLinks = article.querySelectorAll('a[href*="video"], a[href*="play"]');
                videoLinks.forEach(link => {
                    const href = toAbs(link.getAttribute('href'));
                    if (href && !videoUrls.includes(href)) {
                        videoUrls.push(href);
                    }
                });
                
                // 方法3: 从 data-url 属性提取（微博常用）
                article.querySelectorAll('[data-url*="video"], [data-url*=".mp4"]').forEach(el => {
                    const url = el.getAttribute('data-url');
                    if (url && !videoUrls.includes(url)) {
                        videoUrls.push(toAbs(url));
                    }
                });
                
                // 方法4: 从背景视频样式提取
                article.querySelectorAll('[style*="video"]').forEach(el => {
                    const style = el.getAttribute('style') || '';
                    const match = style.match(/url\(["']?(https?:\/\/[^"')]+\.(?:mp4|m3u8))["']?\)/);
                    if (match && !videoUrls.includes(match[1])) {
                        videoUrls.push(match[1]);
                    }
                });
                
                // 方法5: 从 action-data 属性提取（微博视频卡片）
                article.querySelectorAll('[action-data*="video"]').forEach(el => {
                    const actionData = el.getAttribute('action-data') || '';
                    // 提取视频URL
                    const urlMatch = actionData.match(/(https?:\/\/[^\s&]+\.(?:mp4|m3u8))/);
                    if (urlMatch && !videoUrls.includes(urlMatch[1])) {
                        videoUrls.push(urlMatch[1]);
                    }
                    // 提取视频播放页链接
                    const videoPageMatch = actionData.match(/(https?:\/\/[^\s&]*video[^\s&]*)/);
                    if (videoPageMatch && !videoUrls.includes(videoPageMatch[1])) {
                        videoUrls.push(videoPageMatch[1]);
                    }
                });
                
                // 方法6: 从 script 标签附近的视频容器提取
                article.querySelectorAll('div[onclick*="video"], div[onclick*="play"]').forEach(el => {
                    const onclick = el.getAttribute('onclick') || '';
                    const urlMatch = onclick.match(/(https?:\/\/[^'"\s]+)/);
                    if (urlMatch && !videoUrls.includes(urlMatch[1])) {
                        videoUrls.push(urlMatch[1]);
                    }
                });
                
                // 提取作者：优先从头部用户信息区提取，多级备用策略
                let finalAuthor = '';
                
                // 策略1: 从头像/用户信息区域附近的昵称链接提取
                // 微博卡片结构中，作者昵称通常在 header/head 区域的 <a> 内
                const authorAreaSelectors = [
                    '[class*="head"] a[href*="/u/"]',
                    '[class*="header"] a[href*="/u/"]',
                    '[class*="name"] a[href*="/u/"]',
                    '[class*="nick"] a[href*="/u/"]',
                    '[class*="author"] a[href*="/u/"]',
                    '[class*="user"] a[href*="/u/"]',
                ];
                for (const sel of authorAreaSelectors) {
                    const el = article.querySelector(sel);
                    if (el) {
                        const t = (el.textContent || '').trim();
                        if (t && t.length >= 2 && !t.includes('公开') && !t.includes('发布于') && !t.startsWith('@')) {
                            finalAuthor = t;
                            break;
                        }
                    }
                }
                
                // 策略2: 从 a[href*="/u/"] 提取，排除无效文本
                if (!finalAuthor) {
                    const userLinks = [...article.querySelectorAll('a[href*="/u/"]')];
                    for (const link of userLinks) {
                        const t = (link.textContent || '').trim();
                        // 排除：太短、包含"公开"/"发布于"、以@开头（是提及而非作者）、纯数字
                        if (t && t.length >= 2 && !t.includes('公开') && !t.includes('发布于')
                            && !t.startsWith('@') && !/^\\d+$/.test(t)) {
                            finalAuthor = t;
                            break;
                        }
                    }
                }
                
                // 策略3: 从 weibo.com/{uid}/{mid} 格式的时间链接附近找作者
                if (!finalAuthor && timeLink) {
                    // 时间链接同级或父节点里找 /u/ 链接
                    const parent = timeLink.parentElement;
                    if (parent) {
                        const siblingLink = parent.querySelector('a[href*="/u/"]');
                        if (siblingLink) {
                            const t = (siblingLink.textContent || '').trim();
                            if (t && t.length >= 2 && !t.startsWith('@')) {
                                finalAuthor = t;
                            }
                        }
                    }
                }
                
                // 策略4: 兜底——找第一个非空、非@符号、看起来像昵称的 span/a
                if (!finalAuthor) {
                    const candidates = [...article.querySelectorAll('a[href*="weibo.com/"], span[class*="name"], span[class*="nick"]')];
                    for (const el of candidates) {
                        const t = (el.textContent || '').trim();
                        if (t && t.length >= 2 && t.length <= 30 && !t.startsWith('@')
                            && !t.includes('收藏') && !t.includes('转发') && !t.includes('评论')
                            && !t.includes('公开') && !/^\\d+$/.test(t)) {
                            finalAuthor = t;
                            break;
                        }
                    }
                }
                
                // 提取发布时间：优先从带 title 的时间链接（chrome_mcp_client 的方式）
                let publishTime = '';
                if (timeLink) {
                    // timeLink 的 title 属性有时包含完整时间
                    const titleAttr = (timeLink.getAttribute('title') || '').trim();
                    const linkText = (timeLink.textContent || '').trim();
                    // title 属性格式通常是 "YYYY-MM-DD HH:mm" 或类似
                    if (titleAttr && /\\d{4}-\\d{2}-\\d{2}/.test(titleAttr)) {
                        publishTime = titleAttr;
                    } else if (linkText && /\\d{4}-\\d{2}-\\d{2}|\\d{2}-\\d{2}-\\d{2}|\\d{2}-\\d{2}/.test(linkText)) {
                        publishTime = linkText;
                    }
                }
                // 如果没有从时间链接提取到，扫描所有 a/span/time
                if (!publishTime) {
                    const timeEl = [...article.querySelectorAll('a[href*="weibo.com"][title], time, a[title], span[title]')].find(el => {
                        const t = (el.getAttribute('title') || el.textContent || '').trim();
                        return /\\d{4}-\\d{2}-\\d{2}|\\d{2}-\\d{2}-\\d{2}|\\d{2}:\\d{2}|分钟前|小时前|今天/.test(t);
                    });
                    if (timeEl) {
                        const titleAttr = (timeEl.getAttribute('title') || '').trim();
                        publishTime = titleAttr || (timeEl.textContent || '').trim();
                    }
                }
                // 最后兜底：找任意符合时间格式的文本节点
                if (!publishTime) {
                    const anyTimeEl = [...article.querySelectorAll('a, span, time')].find(el => {
                        const t = (el.textContent || '').trim();
                        return /\\d{4}-\\d{2}-\\d{2}|\\d{2}:\\d{2}|分钟前|小时前|今天/.test(t);
                    });
                    if (anyTimeEl) {
                        publishTime = (anyTimeEl.textContent || '').trim();
                    }
                }
                
                // 提取并处理网页链接
                const webLinks = [];
                article.querySelectorAll('a[href*="sinaurl"]').forEach(link => {
                    const href = link.getAttribute('href') || '';
                    const text = (link.textContent || '').trim();
                    if (href.includes('sinaurl?u=')) {
                        try {
                            const urlMatch = href.match(/[?&]u=([^&]+)/);
                            if (urlMatch) {
                                const realUrl = decodeURIComponent(urlMatch[1]);
                                webLinks.push({
                                    originalText: text,
                                    realUrl: realUrl
                                });
                            }
                        } catch (e) {}
                    }
                });

                article.querySelectorAll('a[href*="ttarticle"]').forEach(link => {
                    const href = toAbs(link.getAttribute('href') || '');
                    const text = (link.textContent || '').trim();
                    if (href && !webLinks.find(l => l.realUrl === href)) {
                        webLinks.push({
                            originalText: text,
                            realUrl: href
                        });
                    }
                });
                
                // 处理文本
                let text = (article.innerText || '').trim();
                
                const visibilityMarkers = ['公开', '仅自己可见', '好友可见', '分组可见'];
                let textLines = text.split('\\n');
                textLines = textLines.filter(line => {
                    const trimmed = line.trim();
                    return !visibilityMarkers.includes(trimmed);
                });
                text = textLines.join('\\n');
                
                let replaceIndex = 0;
                text = text.replace(/网页链接/g, (match) => {
                    if (replaceIndex < webLinks.length) {
                        const link = webLinks[replaceIndex];
                        replaceIndex++;
                        return `[${link.originalText}](${link.realUrl})`;
                    }
                    return match;
                });
                
                return {
                    id: rawId || '',
                    author: finalAuthor || '',
                    publish_time: publishTime || '',
                    text: text,
                    source_url: fullWeiboUrl || statusLink,
                    image_groups: imageGroups,
                    video_urls: [...new Set(videoUrls)],
                    article_index: idx,
                    web_links: webLinks
                };
            });
            return rawRecords;
        }"""
        
        raw_records = await page.evaluate(extract_script)
        
        new_records_count = 0
        for idx, raw in enumerate(raw_records):
            record = normalize_record(raw, downloaded_count + len(pending_records) + idx)
            
            if record["dedupe_key"] in seen_keys:
                continue
            
            seen_keys.add(record["dedupe_key"])
            
            # 检查是否已存在（通过检查 markdown 文件是否存在）
            if skip_existing and record["record_id"] in _existing_record_ids:
                print(f"  跳过已存在记录: {record['record_id']}")
                # 注意：这里直接跳过，不加入 pending_records，所以不会更新链接
                continue
            
            if (downloaded_count + len(pending_records)) >= max_download:
                break

            pending_records.append(record)
            new_records_count += 1
            print(f"  ✓ 提取记录: {record['record_id']} - {record['author']}")

        # 达到 batch_size 就立即下载，不等待全部滚动结束
        await flush_pending(force=False)
        
        # 判断是否有新记录
        if new_records_count == 0:
            idle_rounds += 1
        else:
            idle_rounds = 0
        
        # 检查是否已经达到目标下载数量（包括待下载的）
        total_extracted = downloaded_count + len(pending_records)
        if total_extracted >= max_download:
            print(f"\n✓ 已达到目标下载数量: {total_extracted}/{max_download}，停止滚动")
            break
        
        # 滚动页面
        if downloaded_count < max_download and idle_rounds < max_idle_rounds:
            await page.evaluate(f"window.scrollBy(0, window.innerHeight * {scroll_step_ratio})")
            await asyncio.sleep(scroll_wait_seconds)

    # 滚动结束后，下载最后不足 batch_size 的尾批
    await flush_pending(force=True)

    print(f"\n提取并下载完成，共下载 {downloaded_count} 条记录")
    return downloaded_count


def load_existing_records():
    """加载已存在的记录ID，同时扫描记录链找到尾部记录"""
    global _existing_record_ids, _existing_article_ids, _existing_article_md_map, _record_chain_info
    
    if not OUTPUT_DIR.exists():
        return
    
    # 加载微博记录（通过检查 markdown 文件是否存在来判断）
    # 文件名格式: author_date_time_recordid.md (如: 爱可可-爱生活_2026-04-12_0832_QApYcsCLc.md)
    for md_file in OUTPUT_DIR.glob("*.md"):
        # 从文件名提取 record_id: 最后一部分是 record_id
        parts = md_file.stem.rsplit('_', 1)
        if len(parts) == 2:
            # parts[1] 应该是 record_id (如 QApYcsCLc)
            # 验证 record_id 是否符合微博ID格式（字母数字组合，通常8位左右）
            record_id = parts[1]
            if record_id and len(record_id) >= 6:
                _existing_record_ids.add(record_id)
                print(f"    已加载记录: {record_id} ({md_file.name})")
    
    # 加载文章记录
    for md_file in ARTICLES_DIR.glob("*.md"):
        article_id = md_file.stem
        _existing_article_ids.add(article_id)
        _existing_article_md_map[article_id] = md_file
    
    print(f"已加载 {_existing_record_ids.__len__()} 条微博记录，{_existing_article_ids.__len__()} 篇文章")
    
    # 扫描记录链，找到尾部记录
    print("扫描记录链，查找尾部记录...")
    _record_chain_info = find_record_chain_tail()
    if _record_chain_info:
        print(f"  将从尾部记录继续链接: {_record_chain_info['file_name']}")
        # 创建/更新 index.md 入口主页，链接指向最新的链尾部记录
        update_index_md(_record_chain_info)


async def download_record(
    page: Page,
    record: dict,
    image_size: str,
    download_video: bool,
    download_article: bool,
    user_agent: str = "",
    prev_record_info: dict | None = None,
) -> dict:
    """下载单条记录的图片、视频和文章，并创建 markdown 文件
    
    Args:
        prev_record_info: 前一条记录的信息，包含 record_id, author, publish_time, file_name, text_preview
    
    Returns:
        当前记录的信息字典，用于下一条记录的链接
    """
    record_id = record["record_id"]
    author = record.get("author", "unknown")
    publish_time = record.get("publish_time", "")
    text_content = record.get("text", "(无正文)")
    
    # 移除"已编辑"标记
    text_content = re.sub(r'\s*已编辑\n', '', text_content)
    
    # 从正文内容中提取并修正作者和发表时间
    def extract_date(date_str):
        """从日期字符串中提取并标准化日期YYYY-MM-DD，支持2位和4位年份"""
        s = date_str.strip()
        # 匹配4位年份: YYYY-M-D, YYYY-MM-DD, YYYY-M-DD, YYYY-MM-D
        match = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})', s)
        if match:
            year, month, day = match.groups()
            return f"{year}-{int(month):02d}-{int(day):02d}"
        # 匹配2位年份: YY-M-D, YY-MM-DD, YY-M-DD, YY-MM-D
        match = re.match(r'^(\d{1,2})-(\d{1,2})-(\d{1,2})', s)
        if match:
            year, month, day = match.groups()
            full_year = f"20{int(year):02d}"
            return f"{full_year}-{int(month):02d}-{int(day):02d}"
        return None

    def is_valid_author(author_name):
        """检查作者名是否有效（与 chrome_mcp_client 保持一致）"""
        if not author_name or len(author_name) < 2:
            return False
        if author_name.startswith('@'):
            return False
        # 排除纯数字、包含无效字眼的文本
        if re.fullmatch(r'\d+', author_name):
            return False
        invalid_keywords = ['公开', '发布于', '收藏', '转发', '评论', '赞', '分享', '播放视频', '展开']
        for kw in invalid_keywords:
            if kw in author_name:
                return False
        return True

    # 若 JS 层面 author 已是 unknown 或空，尝试从正文前两行回落提取
    # 逻辑参考 chrome_mcp_client.write_record_markdown
    if author == 'unknown' or not author:
        text_lines = [line for line in text_content.split('\n') if line.strip()]
        if len(text_lines) >= 2:
            candidate_author = text_lines[0].strip()
            candidate_date_str = text_lines[1].strip()
            candidate_date = extract_date(candidate_date_str)
            if is_valid_author(candidate_author) and candidate_date:
                author = candidate_author
                publish_time = candidate_date
                remaining_lines = text_lines[2:]
                text_content = '\n'.join(remaining_lines).strip() if remaining_lines else "(无正文)"
                print(f"从正文提取并修正作者/日期: {author} @ {publish_time}")
    else:
        # author 已有值，但检查 publish_time 是否需要修正（例如只有 HH:MM 格式）
        # 如果 publish_time 缺失，也尝试从正文第二行提取
        if not publish_time or re.fullmatch(r'\d{1,2}:\d{2}', publish_time):
            text_lines = [line for line in text_content.split('\n') if line.strip()]
            # 正文第一行是否与 author 相同（即 innerText 里第一行就是作者名）
            offset = 0
            if text_lines and text_lines[0].strip() == author:
                offset = 1
            if len(text_lines) > offset:
                candidate_date = extract_date(text_lines[offset].strip())
                if candidate_date:
                    publish_time = candidate_date
                    remaining_lines = text_lines[offset + 1:]
                    text_content = '\n'.join(remaining_lines).strip() if remaining_lines else "(无正文)"
                    print(f"补充修正发布时间: {author} @ {publish_time}")
    
    context = page.context
    
    # 格式化发布时间用于文件名（提前到这里，供图片、视频下载使用）
    if publish_time:
        publish_time_formatted = publish_time.replace(' ', '_').replace(':', '')
        # 处理不同的时间格式
        if re.match(r'^\d{2}-\d{2}$', publish_time_formatted):
            publish_time_formatted = f"26-{publish_time_formatted}"
        elif re.match(r'^\d{2}-\d{2}-\d{2}$', publish_time_formatted):
            pass
    else:
        publish_time_formatted = datetime.now().strftime("%y-%m-%d_%H%M")
    
    author_name = sanitize_name(author)
    file_prefix = f"{author_name}_{publish_time_formatted}_{record_id}"
    
    # 下载图片（使用与markdown一致的命名）
    local_image_groups = []
    if record["image_groups"]:
        print(f"\n下载图片: {record_id}")
        for group_idx, group in enumerate(record["image_groups"]):
            local_group = []
            for img_idx, img in enumerate(group):
                # 转换图片尺寸
                img_url = convert_image_size(img["url"], image_size)
                ext = image_extension(img_url)
                # 使用与markdown一致的命名: author_timestamp_recordid_img_序号.扩展名
                img_name = f"{file_prefix}_img_{group_idx + 1}_{img_idx + 1}{ext}"
                img_path = PICTURES_DIR / img_name
                
                if img_path.exists():
                    print(f"  跳过已存在: {img_name}")
                    local_group.append({
                        "path": f"pictures/{img_name}",
                        "width": img.get("width", 300),
                        "height": img.get("height", 300)
                    })
                    continue
                
                success = await download_image_with_context(context, img_url, img_path, user_agent=user_agent)
                if success:
                    print(f"  ✓ {img_name}")
                    local_group.append({
                        "path": f"pictures/{img_name}",
                        "width": img.get("width", 300),
                        "height": img.get("height", 300)
                    })
                else:
                    # 下载失败，保留原始URL
                    local_group.append({
                        "path": img_url,
                        "width": img.get("width", 300),
                        "height": img.get("height", 300)
                    })
            if local_group:
                local_image_groups.append(local_group)
    
    # 下载视频（只下载最高分辨率）
    if download_video and record["video_urls"]:
        print(f"\n下载视频: {record_id}")
        print(f"  发现 {len(record['video_urls'])} 个视频URL")
        
        # 收集所有视频URL及其分辨率信息
        all_video_sources = []
        
        for video_url in record["video_urls"]:
            try:
                # 更精确的判断：只有明确的播放页面才需要提取URL
                # 直接的 .mp4 URL 不需要提取
                is_direct_video = video_url.endswith('.mp4') or '.mp4?' in video_url
                is_player_page = 'video.weibo.com' in video_url and not is_direct_video
                
                if is_player_page:
                    # 从播放页面提取真实的视频URL
                    print(f"  从视频播放页面提取最高分辨率视频: {video_url[:80]}...")
                    real_video_info = await extract_real_video_url(page, video_url)
                    if real_video_info:
                        print(f"  提取到视频: {real_video_info['width']}x{real_video_info['height']}")
                        all_video_sources.append({
                            'url': real_video_info['url'],
                            'width': real_video_info.get('width', 0),
                            'height': real_video_info.get('height', 0)
                        })
                    else:
                        print(f"  ⚠️ 无法提取视频URL: {video_url[:80]}...")
                else:
                    # 已经是直接的视频URL，尝试从URL中提取分辨率信息
                    size_match = re.search(r'(\d+)x(\d+)', video_url)
                    # 或者从 label 参数中提取
                    label_match = re.search(r'label=mp4_(\d+)p', video_url)
                    height = 0
                    if size_match:
                        height = int(size_match.group(2))
                    elif label_match:
                        height = int(label_match.group(1))
                    
                    all_video_sources.append({
                        'url': video_url,
                        'width': 0,
                        'height': height
                    })
            except Exception as e:
                print(f"  处理视频URL异常: {video_url[:80]}... -> {e}")
        
        # 选择最高分辨率的视频（优先选择高度最大的）
        if all_video_sources:
            best_source = max(all_video_sources, key=lambda x: (x['height'], x['width']))
            print(f"  共找到 {len(all_video_sources)} 个视频源，选择最高分辨率: {best_source['height']}p")
            
            # 下载视频，使用与markdown一致的命名
            ext = video_extension(best_source['url'])
            video_name = f"{file_prefix}_video{ext}"
            video_path = VIDEOS_DIR / video_name
            video_path.parent.mkdir(parents=True, exist_ok=True)
            
            if video_path.exists():
                print(f"  跳过已存在: {video_name}")
            else:
                print(f"  开始下载: {video_name}")
                success = await download_video_with_context(context, best_source['url'], video_path, user_agent=user_agent)
                if success:
                    print(f"  ✓ 视频下载完成: {video_name}")
                else:
                    print(f"  ✗ 视频下载失败")
    
    # 处理长文章
    long_article_md_name = None
    long_article_title = None
    if record.get("long_article_url"):
        if download_article:
            print(f"\n提取长文章: {record_id}")
            article_data = await extract_long_article(page, record["long_article_url"])
            
            if article_data:
                # 保存文章，使用与主markdown一致的命名前缀
                article_title = sanitize_name(article_data.get('title', 'article')[:50])
                article_file_prefix = f"{file_prefix}_article_{article_title}"
                article_md_name = f"{article_file_prefix}.md"
                article_md = ARTICLES_DIR / article_md_name
                article_md.parent.mkdir(parents=True, exist_ok=True)
                
                # 下载文章中的图片，并记录原始 URL 到本地文件的映射
                image_url_map = {}
                downloaded_urls = set()
                
                for img_idx, img_info in enumerate(article_data.get("images", []), start=1):
                    original_url = img_info.get("url", "")
                    if not original_url or original_url in downloaded_urls:
                        continue
                    
                    downloaded_urls.add(original_url)
                    img_url = convert_image_size(original_url, image_size)
                    
                    # 命名规则: prefix_article_img_序号.扩展名
                    img_name = f"{article_file_prefix}_img_{img_idx:03d}{image_extension(img_url)}"
                    img_path = ARTICLE_PICTURES_DIR / img_name
                    
                    try:
                        success = await download_image_with_context(context, img_url, img_path, user_agent=user_agent)
                        if success:
                            # 长文章Markdown文件在 articles/ 目录下，图片在 articles/pictures/ 目录下
                            # 所以相对路径应该是 pictures/ 而不是 articles/pictures/
                            image_url_map[original_url] = f"pictures/{img_name}"
                    except Exception as e:
                        print(f"  长文章图片下载失败: {original_url} -> {e}")
                
                # 将正文中的图片占位符替换为本地图片链接和图片说明
                rendered_content = article_data.get('content', '')
                for img_info in article_data.get("images", []):
                    original_url = img_info.get("url", "")
                    placeholder = img_info.get("placeholder", "")
                    local_path = image_url_map.get(original_url, "")
                    caption = img_info.get("caption", "")
                    
                    if placeholder and local_path:
                        # 构建图片标签
                        img_tag = f'<img src="{local_path}" width="{img_info.get("width", 300)}" height="{img_info.get("height", 300)}">'
                        
                        # 如果有图片说明，添加到图片下方
                        if caption:
                            img_with_caption = f'{img_tag}\n\n*{caption}*'
                        else:
                            img_with_caption = img_tag
                        
                        rendered_content = rendered_content.replace(placeholder, img_with_caption)
                
                # 构建Markdown内容
                md_content = f"# {article_data.get('title', record_id)}\n\n"
                md_content += f"**作者**: {article_data.get('author', record['author'])}\n\n"
                md_content += f"**发布时间**: {article_data.get('publish_date', record['publish_time'])}\n\n"
                md_content += f"**原文链接**: {record['long_article_url']}\n\n"
                md_content += "---------\n\n"
                md_content += "## 正文\n\n"
                md_content += rendered_content
                
                article_md.write_text(md_content, encoding='utf-8')
                print(f"  ✓ 文章已保存: {article_md.name}")
                
                # 记录长文章信息，用于主markdown中的链接
                long_article_md_name = article_md_name
                long_article_title = article_data.get('title', '长文章')
    
    # 创建 Markdown 文件（file_prefix 已在前面定义）
    md_name = f"{file_prefix}.md"
    md_path = OUTPUT_DIR / md_name
    
    # 构建 Markdown 内容
    lines = [
        f"# {author}     发布于： {publish_time}".strip(),
        "",
        "---------",
        "## 正文",
        "",
        text_content,
        "",
        "---------",
    ]
    
    # 添加图片部分（仅当有图片时）
    if local_image_groups:
        lines.append("## 图片")
        lines.append("")
        for group in local_image_groups:
            # 每组图片放在一行（并排显示）
            img_tags = []
            for img in group:
                img_tags.append(f'<img src="{img["path"]}" width="300" height="300">')
            lines.append("".join(img_tags))
            lines.append("")
    
    # 添加视频链接
    video_files = []
    video_urls = record.get("video_urls", [])
    
    if video_urls:
        # 如果启用了视频下载，检查本地视频文件
        if download_video:
            ext = ".mp4"  # 默认扩展名
            video_name = f"{file_prefix}_video{ext}"
            video_path = VIDEOS_DIR / video_name
            if video_path.exists():
                video_files.append({"name": video_name, "path": f"videos/{video_name}", "is_local": True})
        
        # 添加视频部分到Markdown
        lines.append("")
        lines.append("---------")
        lines.append("## 视频")
        lines.append("")
        
        # 如果有本地视频文件，添加播放器
        for video in video_files:
            lines.append(f"**视频文件**: [{video['name']}]({video['path']})")
            lines.append("")
            # 添加HTML5视频播放器
            lines.append(f'<video controls width="100%" style="max-width: 600px;">')
            lines.append(f'  <source src="{video["path"]}" type="video/mp4">')
            lines.append(f'  您的浏览器不支持视频播放')
            lines.append(f'</video>')
            lines.append("")
        
        # 添加源视频链接（无论是否下载了视频）
        if video_urls:
            lines.append("**源视频链接**:")
            lines.append("")
            for idx, video_url in enumerate(video_urls, 1):
                lines.append(f"{idx}. [{video_url}]({video_url})")
            lines.append("")
    
    # 添加长文章链接
    if record.get("long_article_url"):
        lines.append("")
        lines.append("---------")
        lines.append("## 长文章")
        lines.append("")
        if long_article_md_name:
            # 如果成功下载了长文章，链接到本地文件
            article_link_text = long_article_title if long_article_title else "点击查看完整文章"
            lines.append(f"**长文章链接**: [{article_link_text}](articles/{long_article_md_name})")
            lines.append("")
            lines.append(f"**原文链接**: {record['long_article_url']}")
        else:
            # 如果没有下载长文章，直接链接到原文
            lines.append(f"**长文章链接**: [点击查看完整文章]({record['long_article_url']})")
    
    # 添加双向导航链接
    # 注意：下一条链接会在处理下一条记录时通过更新当前文件来添加
    nav_links = []
    if prev_record_info:
        prev_desc = prev_record_info.get("text_preview", "前一条")
        # 将换行符替换为空格，确保链接描述在一行内
        prev_desc = prev_desc.replace('\n', ' ').replace('\r', ' ')
        prev_file = prev_record_info.get("file_name", "")
        if prev_file:
            nav_links.append(f"前一条：[{prev_desc}]({prev_file})")
    
    # 将导航链接插入到正文标题之前（在 ## 正文 之前）
    # 找到 "## 正文" 的位置
    body_idx = -1
    for i, line in enumerate(lines):
        if line == "## 正文":
            body_idx = i
            break
    
    if nav_links and body_idx > 0:
        # 在 "## 正文" 之前插入空行和导航链接（所有链接在同一行，用 | 分隔）
        lines.insert(body_idx, "")
        lines.insert(body_idx, " | ".join(nav_links))
    
    # 写入文件
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  ✓ Markdown 已保存: {md_path.name}")
    
    # 更新前一条记录的文件，添加指向当前记录的链接
    if prev_record_info:
        prev_md_path = OUTPUT_DIR / prev_record_info.get("file_name", "")
        if prev_md_path.exists():
            try:
                prev_content = prev_md_path.read_text(encoding="utf-8")
                # 获取当前记录的描述（用于链接文本）
                current_text_preview = text_content[:30] + "..." if len(text_content) > 30 else text_content
                if not current_text_preview.strip():
                    current_text_preview = "(无正文)"
                # 将换行符替换为空格，确保链接描述在一行内
                current_text_preview = current_text_preview.replace('\n', ' ').replace('\r', ' ')
                
                # 查找前一条记录中已有的导航链接行
                lines_prev = prev_content.split("\n")
                body_idx_prev = -1
                for i, line in enumerate(lines_prev):
                    if line == "## 正文":
                        body_idx_prev = i
                        break
                
                if body_idx_prev > 0:
                    # 构建下一条链接
                    next_link = f"下一条：[{current_text_preview}]({md_name})"
                    
                    # 查找是否已有导航链接行（在 ## 正文 之前）
                    # 从正文往前找，跳过空行，找到第一个非空行
                    nav_line_idx = -1
                    for i in range(body_idx_prev - 1, -1, -1):
                        line_content = lines_prev[i].strip()
                        if line_content == "":
                            continue
                        # 找到非空行，检查是否是导航链接
                        if "前一条：" in line_content or "下一条：" in line_content:
                            nav_line_idx = i
                        break
                    
                    if nav_line_idx >= 0:
                        # 已有导航链接，在同一行追加下一条（用 | 分隔）
                        lines_prev[nav_line_idx] = lines_prev[nav_line_idx] + " | " + next_link
                    else:
                        # 没有导航链接，在正文前插入新行（前面留一个空行）
                        lines_prev.insert(body_idx_prev, "")
                        lines_prev.insert(body_idx_prev, next_link)
                    
                    prev_md_path.write_text("\n".join(lines_prev), encoding="utf-8")
                    print(f"  ✓ 已更新前一条记录的导航链接: {prev_md_path.name}")
            except Exception as e:
                print(f"  ⚠️ 更新前一条记录导航链接失败: {e}")
    
    # 返回当前记录的信息，用于下一条记录的链接
    text_preview = text_content[:30] + "..." if len(text_content) > 30 else text_content
    if not text_preview.strip():
        text_preview = "(无正文)"
    # 将换行符替换为空格，确保链接描述在一行内
    text_preview = text_preview.replace('\n', ' ').replace('\r', ' ')
    
    return {
        "record_id": record_id,
        "author": author,
        "publish_time": publish_time,
        "file_name": md_name,
        "text_preview": text_preview,
    }


async def main():
    parser = argparse.ArgumentParser(description="微博收藏下载工具 - Playwright 版本")
    parser.add_argument("--url", type=str, help="目标URL（可选）")
    parser.add_argument("--max-download", type=int, default=DEFAULT_MAX_DOWNLOAD, help="最大下载数")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE, help=f"分批下载数量，默认: {DEFAULT_BATCH_SIZE}")
    parser.add_argument("--skip-existing", action="store_true", help="跳过已存在的记录")
    parser.add_argument("--image-size", choices=['360', '480', '690', '2000', 'large'], default='360', help="图片尺寸")
    parser.add_argument("--download-video", action="store_true", help="下载视频")
    parser.add_argument("--download-article", action="store_true", help="下载长文章")
    parser.add_argument("--max-idle-rounds", type=int, default=DEFAULT_MAX_IDLE_ROUNDS, help="最大空闲轮次")
    parser.add_argument("--scroll-wait", type=float, default=DEFAULT_SCROLL_WAIT_SECONDS, help="滚动等待时间")
    parser.add_argument("--headless", action="store_true", help="无头模式运行")
    parser.add_argument("--connect-browser", action="store_true", help="连接到已运行的浏览器")
    parser.add_argument("--cdp-endpoint", default="http://localhost:9222", help="CDP端点地址")
    parser.add_argument("--user-data-dir", type=str, help="浏览器用户数据目录（持久化登录状态）")
    parser.add_argument("--save-cookies", action="store_true", default=True, help="保存登录状态到文件（默认启用）")
    parser.add_argument("--no-save-cookies", action="store_true", help="不保存登录状态")
    parser.add_argument("--output-dir", type=str, help="输出目录路径（默认：脚本所在目录下的 output 文件夹）")
    
    args = parser.parse_args()
    provided_url = (args.url or "").strip()
    cookies_exists = COOKIES_FILE.exists()
    
    # 检查 user_data_dir 是否存在且包含有效的用户数据（Local State 文件存在表示有浏览器数据）
    user_data_dir_exists = False
    if args.user_data_dir:
        user_dir = Path(args.user_data_dir)
        # Local State 文件是 Chromium 用户数据目录的标志文件
        local_state_file = user_dir / "Local State"
        user_data_dir_exists = local_state_file.exists()
    
    # 强制登录模式：当没有 cookies 文件且没有 user_data_dir 时，或者没有提供 URL 时
    # 如果 user_data_dir 存在，则认为可能已经登录，不需要强制等待
    force_login_mode = ((not cookies_exists) and (not user_data_dir_exists)) or (not provided_url)
    
    # 处理参数冲突
    if args.no_save_cookies:
        args.save_cookies = False
    
    # 根据参数设置输出目录
    global OUTPUT_DIR, PICTURES_DIR, VIDEOS_DIR, ARTICLES_DIR, ARTICLE_PICTURES_DIR
    if args.output_dir:
        OUTPUT_DIR = Path(args.output_dir).resolve()
        PICTURES_DIR = OUTPUT_DIR / "pictures"
        VIDEOS_DIR = OUTPUT_DIR / "videos"
        ARTICLES_DIR = OUTPUT_DIR / "articles"
        ARTICLE_PICTURES_DIR = ARTICLES_DIR / "pictures"
    
    # 创建输出目录
    for dir_path in [OUTPUT_DIR, PICTURES_DIR, VIDEOS_DIR, ARTICLES_DIR, ARTICLE_PICTURES_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("微博收藏下载工具 - Playwright 版本")
    print("=" * 60)
    print(f"目标URL: {provided_url or '(未提供)'}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"最大下载数: {args.max_download}")
    print(f"分批下载数: {args.batch_size}")
    print(f"图片尺寸: {args.image_size}")
    print(f"下载视频: {args.download_video}")
    print(f"下载文章: {args.download_article}")
    print(f"跳过已存在: {args.skip_existing}")
    print(f"保存登录状态: {args.save_cookies}")
    print(f"cookies.json 存在: {cookies_exists}")
    print(f"自动登录等待模式: {force_login_mode}")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser: Browser | None = None
        context: BrowserContext
        
        if args.connect_browser:
            # 连接到已运行的浏览器
            print(f"\n连接到浏览器: {args.cdp_endpoint}")
            browser = await p.chromium.connect_over_cdp(args.cdp_endpoint)
            contexts = browser.contexts
            context = contexts[0] if contexts else await browser.new_context()
        elif args.user_data_dir:
            # 使用持久化上下文（推荐方式）
            user_dir = Path(args.user_data_dir)
            user_dir.mkdir(parents=True, exist_ok=True)
            print(f"\n启动浏览器（持久化模式）: {user_dir}")
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(user_dir),
                headless=args.headless,
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                args=['--disable-blink-features=AutomationControlled']
            )
        else:
            # 启动新浏览器（使用 cookies 文件保存登录状态）
            print("\n启动新浏览器...")
            browser = await p.chromium.launch(
                headless=args.headless,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # 尝试加载已保存的 cookies
            if args.save_cookies:
                await load_cookies(context)
        
        # 创建页面
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 获取 User-Agent
        user_agent = await get_browser_user_agent(page)
        
        if force_login_mode:
            login_url = "https://weibo.com"
            wait_seconds = 60
            print(f"\n[自动模式] 导航到: {login_url}")
            print("⚠️ 请在浏览器中完成登录，并进入需要下载的页面：收藏页 / 本人主页 / 他人主页")
            try:
                await page.goto(login_url, wait_until="commit", timeout=20000)
            except Exception as e:
                print(f"⚠️ 登录页面导航超时或失败: {login_url} -> {str(e)[:100]}")
                
            print(f"将等待 {wait_seconds} 秒后自动开始下载...")
            await asyncio.sleep(wait_seconds)

            if args.save_cookies and not args.user_data_dir:
                await save_cookies(context)
            target_url = page.url
            print(f"等待结束，当前页面: {target_url}")
        else:
            # 用户提供了 URL 且 cookies.json 存在，直接开始下载（不等待）
            target_url = provided_url
            print(f"\n导航到: {target_url}")
            try:
                await page.goto(target_url, wait_until="commit", timeout=20000)
            except Exception as e:
                print(f"⚠️ 导航到目标页面超时或失败: {target_url} -> {str(e)[:100]}")
               
            await asyncio.sleep(10)
        
            # 如果不需要登录，也保存一次 cookies（更新）
            if args.save_cookies and not args.user_data_dir:
                await save_cookies(context)
        
        # 滚动提取并分批下载（滚动一批，下载一批）
        downloaded_count = await scroll_and_extract(
            page=page,
            max_download=args.max_download,
            skip_existing=args.skip_existing,
            image_size=args.image_size,
            download_video=args.download_video,
            download_article=args.download_article,
            max_idle_rounds=args.max_idle_rounds,
            scroll_wait_seconds=args.scroll_wait,
            stability_check_rounds=DEFAULT_STABILITY_CHECK_ROUNDS,
            scroll_step_ratio=DEFAULT_SCROLL_STEP_RATIO,
            batch_size=args.batch_size,
            user_agent=user_agent,
        )
        
        # 保存最终的 cookies
        if args.save_cookies and not args.user_data_dir:
            await save_cookies(context)
        
        # 关闭浏览器（仅在非连接模式下且非持久化上下文）
        if browser and not args.connect_browser:
            await browser.close()
        elif args.user_data_dir:
            # 持久化上下文需要手动关闭
            await context.close()
        
        print("\n" + "=" * 60)
        print("✓ 下载完成！")
        print(f"总计: {downloaded_count} 条记录")
        print(f"图片目录: {PICTURES_DIR}")
        print(f"视频目录: {VIDEOS_DIR}")
        print(f"文章目录: {ARTICLES_DIR}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
