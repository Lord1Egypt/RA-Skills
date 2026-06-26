"""歌曲搜索和下载功能实现

网站: https://www.gequhai.com/
功能:
1. 搜索歌曲
2. 获取下载链接（高品质夸克网盘链接、低品质直链）
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Optional
import re

logger = logging.getLogger(__name__)

# 歌曲海网站
GEQUHAI_URL = "https://www.gequhai.com/"
GEQUHAI_SEARCH_URL = "https://www.gequhai.com/search/"


@dataclass
class SearchResult:
    """搜索结果"""
    rank: int
    title: str
    artist: str
    album: str
    song_id: str
    detail_url: str  # 歌曲详情页URL


@dataclass
class DownloadInfo:
    """下载信息"""
    song_title: str
    artist: str
    high_quality_url: Optional[str]  # 高品质下载链接（夸克网盘）
    low_quality_url: Optional[str]   # 低品质下载链接（可能是直链或夸克）
    low_quality_is_quark: bool       # 低品质链接是否是夸克网盘
    low_quality_is_direct: bool      # 低品质链接是否是浏览器直链


def search_songs(page, song_name: str, max_results: int = 10) -> list[SearchResult]:
    """搜索歌曲
    
    Args:
        page: CDP Page 对象
        song_name: 歌曲名称
        max_results: 最多返回结果数（默认10）
    
    Returns:
        搜索结果列表
    """
    logger.info(f"搜索歌曲: {song_name}")
    
    # 直接导航到搜索结果页面
    # 歌曲海搜索 URL 格式: /s/<keyword>
    import urllib.parse
    encoded_keyword = urllib.parse.quote(song_name)
    search_url = f"{GEQUHAI_URL}s/{encoded_keyword}"
    
    logger.info(f"导航到搜索页面: {search_url}")
    page.navigate(search_url)
    page.wait_for_load()
    time.sleep(2)  # 等待结果加载
    
    # 解析搜索结果
    results = _parse_search_results(page, max_results)
    
    logger.info(f"搜索到 {len(results)} 首歌曲")
    return results


def _parse_search_results(page, max_results: int) -> list[SearchResult]:
    """解析搜索结果页面"""
    results = []
    
    # 歌曲海搜索结果结构：
    # <table class="table table-striped table-hover" id="myTables">
    #   <tbody>
    #     <tr>
    #       <td>序号</td>
    #       <td><a href="/play/xxx">歌曲名</a></td>
    #       <td>歌手</td>
    #     </tr>
    #   </tbody>
    # </table>
    
    # 使用正确的选择器
    result_count = page.evaluate("""
    (() => {
        const rows = document.querySelectorAll('#myTables tbody tr');
        return rows.length;
    })()
    """)
    
    if not result_count or result_count == 0:
        # 如果找不到结果，尝试备用方式
        logger.warning("未找到搜索结果，尝试备用解析方式")
        return _parse_search_results_alternative(page, max_results)
    
    logger.info(f"找到 {result_count} 个结果元素")
    
    # 解析每个结果
    for i in range(min(result_count, max_results)):
        result = _parse_single_result(page, i)
        if result:
            results.append(result)
    
    return results


def _parse_search_results_alternative(page, max_results: int) -> list[SearchResult]:
    """备用解析方法 - 直接从页面提取信息"""
    results = []
    
    # 获取所有可能的链接，查找歌曲详情页
    song_links = page.evaluate("""
    (() => {
        const links = [];
        // 查找所有链接
        document.querySelectorAll('a').forEach(a => {
            const href = a.getAttribute('href') || '';
            const text = a.textContent.trim();
            // 歌曲详情页通常是 /song/xxx 或类似格式
            if (href.includes('/song/') || href.includes('/music/') || href.includes('id=')) {
                links.push({
                    href: href,
                    text: text
                });
            }
        });
        return links;
    })()
    """)
    
    if song_links:
        for i, link in enumerate(song_links[:max_results]):
            # 尝试解析歌名和歌手
            # 通常格式是 "歌名 - 歌手"
            text = link.get('text', '')
            parts = text.split('-')
            title = parts[0].strip() if parts else text
            artist = parts[1].strip() if len(parts) > 1 else ''
            
            # 构建完整URL
            href = link.get('href', '')
            if href.startswith('/'):
                detail_url = f"https://www.gequhai.com{href}"
            elif href.startswith('http'):
                detail_url = href
            else:
                detail_url = f"https://www.gequhai.com/{href}"
            
            # 提取歌曲ID
            song_id = _extract_song_id(href)
            
            results.append(SearchResult(
                rank=i + 1,
                title=title,
                artist=artist,
                album='',
                song_id=song_id,
                detail_url=detail_url
            ))
    
    return results


def _parse_single_result(page, index: int) -> Optional[SearchResult]:
    """解析单个搜索结果"""
    # 歌曲海搜索结果结构：
    # <tr>
    #   <td>序号</td>
    #   <td><a href="/play/xxx" class="text-info font-weight-bold">歌曲名</a></td>
    #   <td>歌手</td>
    # </tr>
    
    result = page.evaluate(f"""
    (() => {{
        const rows = document.querySelectorAll('#myTables tbody tr');
        if (!rows[{index}]) return null;
        
        const row = rows[{index}];
        const cells = row.querySelectorAll('td');
        
        if (cells.length < 3) return null;
        
        // 序号在第一个 td
        const rankText = cells[0].textContent.trim();
        
        // 歌曲名和链接在第二个 td 的 a 标签
        const linkEl = cells[1].querySelector('a');
        const title = linkEl ? linkEl.textContent.trim() : '';
        const href = linkEl ? linkEl.getAttribute('href') : '';
        
        // 歌手在第三个 td
        const artist = cells[2].textContent.trim();
        
        if (!title) return null;
        
        return {{
            rank: rankText,
            title: title,
            artist: artist,
            href: href
        }};
    }})()
    """)
    
    if result and result.get('title'):
        href = result.get('href', '')
        if href.startswith('/'):
            detail_url = f"https://www.gequhai.com{href}"
        elif href.startswith('http'):
            detail_url = href
        else:
            detail_url = f"https://www.gequhai.com/{href}"
        
        return SearchResult(
            rank=index + 1,
            title=result.get('title', ''),
            artist=result.get('artist', ''),
            album='',
            song_id=_extract_song_id(href),
            detail_url=detail_url
        )
    
    return None


def _extract_song_id(href: str) -> str:
    """从链接中提取歌曲ID"""
    # 尝试不同的ID格式
    # /song/123456
    # /music?id=123456
    # /play/123456
    
    patterns = [
        r'/song/(\w+)',
        r'/music/(\w+)',
        r'/play/(\w+)',
        r'id=(\w+)',
        r'/(\d+)\.html'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, href)
        if match:
            return match.group(1)
    
    return ''


def get_download_links(page, song: SearchResult) -> DownloadInfo:
    """获取歌曲下载链接
    
    Args:
        page: CDP Page 对象
        song: 搜索结果
    
    Returns:
        下载信息
    """
    logger.info(f"获取下载链接: {song.title} - {song.artist}")
    
    # 1. 导航到歌曲详情页
    page.navigate(song.detail_url)
    page.wait_for_load()
    time.sleep(2)
    
    # 2. 查找下载按钮
    # 高品质下载: <a id="btn-download-mp3" class="btn btn-custom" href="https://pan.quark.cn/s/xxx">
    # 推荐高品质: <a href="https://pan.quark.cn/s/xxx" class="btn btn-primary download-button extra-button">
    # 低品质下载: <a class="btn btn-primary download-button" onclick="downloadMP3()">
    
    download_info = _extract_download_links(page, song)
    
    return download_info


def _extract_download_links(page, song: SearchResult) -> DownloadInfo:
    """从页面提取下载链接"""
    
    # 提取所有下载链接信息
    links_info = page.evaluate("""
    (() => {
        const result = {
            high_quality_url: null,
            low_quality_url: null,
            low_quality_is_quark: false,
            low_quality_is_direct: false
        };
        
        // 查找高品质下载按钮（夸克网盘）
        // <a id="btn-download-mp3" class="btn btn-custom" href="https://pan.quark.cn/s/xxx">
        const highQualityBtn = document.querySelector('#btn-download-mp3');
        if (highQualityBtn) {
            result.high_quality_url = highQualityBtn.getAttribute('href');
        }
        
        // 如果没找到，尝试其他高品质按钮
        if (!result.high_quality_url) {
            // <a href="https://pan.quark.cn/s/xxx" class="btn btn-primary download-button extra-button">
            const extraBtn = document.querySelector('.download-button.extra-button, .btn-primary.download-button');
            if (extraBtn) {
                const href = extraBtn.getAttribute('href');
                if (href && href.includes('pan.quark.cn')) {
                    result.high_quality_url = href;
                }
            }
        }
        
        // 查找所有包含夸克网盘链接的按钮
        const allButtons = document.querySelectorAll('a[href*="pan.quark.cn"]');
        allButtons.forEach(btn => {
            const href = btn.getAttribute('href');
            if (href && href.startsWith('https://pan.quark.cn/')) {
                if (!result.high_quality_url) {
                    result.high_quality_url = href;
                }
            }
        });
        
        // 查找低品质下载按钮
        // <a class="btn btn-primary download-button" onclick="downloadMP3()">
        const lowQualityBtn = document.querySelector('.download-button:not(.extra-button)');
        if (lowQualityBtn) {
            const onclick = lowQualityBtn.getAttribute('onclick');
            const href = lowQualityBtn.getAttribute('href');
            
            if (href) {
                result.low_quality_url = href;
                result.low_quality_is_quark = href.includes('pan.quark.cn');
                result.low_quality_is_direct = !result.low_quality_is_quark;
            }
        }
        
        return result;
    })()
    """)
    
    high_quality_url = links_info.get('high_quality_url')
    low_quality_url = links_info.get('low_quality_url')
    low_quality_is_quark = links_info.get('low_quality_is_quark', False)
    low_quality_is_direct = links_info.get('low_quality_is_direct', False)
    
    # 验证夸克网盘链接格式
    if high_quality_url:
        if not high_quality_url.startswith('https://pan.quark.cn/'):
            logger.warning(f"高品质链接不是夸克网盘: {high_quality_url}")
            high_quality_url = None
    
    if low_quality_url:
        if low_quality_url.startswith('https://pan.quark.cn/'):
            low_quality_is_quark = True
            low_quality_is_direct = False
        else:
            # 非夸克链接，可能是直链
            low_quality_is_quark = False
            low_quality_is_direct = True
    
    return DownloadInfo(
        song_title=song.title,
        artist=song.artist,
        high_quality_url=high_quality_url,
        low_quality_url=low_quality_url,
        low_quality_is_quark=low_quality_is_quark,
        low_quality_is_direct=low_quality_is_direct
    )
