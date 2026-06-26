from mcp.server.fastmcp import FastMCP
import subprocess
import os
import requests
from dotenv import load_dotenv

load_dotenv()
mcp = FastMCP("龙虾音乐")

API_KEY = os.environ.get('MUSIC_API_KEY', '')
PLAYER_CMD = os.environ.get('PLAYER_CMD', 'mpv')
PREFER_SOURCE = os.environ.get('MUSIC_SOURCE', 'kuwo')  # kuwo / baidu / migu / netease

SOURCES = {
    'kuwo': 'https://api-v2.yuafeng.cn/API/kwmusic.php',
    'netease': 'https://api-v2.yuafeng.cn/API/wymusic.php',
    'migu': 'https://api-v2.yuafeng.cn/API/mgmusic.php',
    'baidu': 'https://api-v2.yuafeng.cn/API/bdmusic.php',
}

LAST_TRACK = {}


def api_search(source: str, query: str, n: int = 1, quality: str = '1'):
    url = SOURCES[source]
    params = {
        'apikey': API_KEY,
        'msg': query,
        'n': n,
        'type': quality,
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def find_playable(query: str, n: int = 1, quality: str = '1'):
    order = [PREFER_SOURCE] + [k for k in SOURCES.keys() if k != PREFER_SOURCE]
    for source in order:
        try:
            data = api_search(source, query, n=n, quality=quality)
            item = data.get('data') or {}
            music = item.get('music')
            if isinstance(music, str) and music.startswith('http'):
                item['_source'] = source
                return item
            # 即使没有音乐直链，也先记下最接近的结果
            if item.get('song'):
                item['_source'] = source
                return item
        except Exception:
            continue
    return None


def play_url(url: str):
    # 直接交给本地播放器。mpv 对网络资源支持最好。
    subprocess.Popen([PLAYER_CMD, url])


@mcp.tool()
def play_music(query: str) -> str:
    """
    Play online music by song name / singer / keyword.
    Use when user asks to play a song or music.
    """
    global LAST_TRACK
    if not API_KEY:
        return '音乐 API KEY 未配置。'
    item = find_playable(query, n=1, quality='1')
    if not item:
        return f'没有找到和 {query} 相关的在线音乐。'

    song = item.get('song', query)
    singer = item.get('singer', '未知歌手')
    music = item.get('music')
    source = item.get('_source', 'unknown')
    LAST_TRACK = item

    if isinstance(music, str) and music.startswith('http'):
        try:
            play_url(music)
            return f'正在播放 {song} - {singer}（来源：{source}）。'
        except Exception as e:
            return f'已找到 {song} - {singer}，但播放失败：{str(e)}'

    return f'已找到 {song} - {singer}，但当前接口没有返回可直接播放的音频链接。'


@mcp.tool()
def play_music_index(query: str, n: int) -> str:
    """
    Play the Nth result for a search query.
    Useful when user wants the second/third search result.
    """
    global LAST_TRACK
    if not API_KEY:
        return '音乐 API KEY 未配置。'
    item = find_playable(query, n=n, quality='1')
    if not item:
        return f'没有找到第 {n} 个与 {query} 相关的结果。'

    song = item.get('song', query)
    singer = item.get('singer', '未知歌手')
    music = item.get('music')
    source = item.get('_source', 'unknown')
    LAST_TRACK = item

    if isinstance(music, str) and music.startswith('http'):
        try:
            play_url(music)
            return f'正在播放第 {n} 个结果：{song} - {singer}（来源：{source}）。'
        except Exception as e:
            return f'已找到第 {n} 个结果 {song} - {singer}，但播放失败：{str(e)}'

    return f'第 {n} 个结果是 {song} - {singer}，但当前没有可直接播放的链接。'


@mcp.tool()
def stop_music() -> str:
    try:
        subprocess.run(['pkill', '-f', PLAYER_CMD], check=False)
        return '已经停止播放。'
    except Exception as e:
        return f'停止失败：{str(e)}'


@mcp.tool()
def pause_music() -> str:
    try:
        subprocess.run(['pkill', '-STOP', '-f', PLAYER_CMD], check=False)
        return '音乐已暂停。'
    except Exception as e:
        return f'暂停失败：{str(e)}'


@mcp.tool()
def resume_music() -> str:
    try:
        subprocess.run(['pkill', '-CONT', '-f', PLAYER_CMD], check=False)
        return '继续播放。'
    except Exception as e:
        return f'继续播放失败：{str(e)}'


@mcp.tool()
def next_track() -> str:
    return '下一首功能可后续接入播放列表。当前建议直接说“播放某首歌”。'


@mcp.tool()
def set_volume(level: int) -> str:
    return f'已收到音量设置请求：{level}。如需精确控制，可后续接入播放器命令。'


@mcp.tool()
def music_info() -> str:
    global LAST_TRACK
    if not LAST_TRACK:
        return '当前还没有最近一次点歌信息。'
    return f"最近一次点歌：{LAST_TRACK.get('song', '未知歌曲')} - {LAST_TRACK.get('singer', '未知歌手')}。"


if __name__ == '__main__':
    mcp.run(transport='stdio')
