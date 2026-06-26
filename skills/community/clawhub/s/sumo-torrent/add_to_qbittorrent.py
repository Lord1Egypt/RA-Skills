#!/usr/bin/env python3
"""
SumoTorrent - qBittorrent 橋樑工具
讓蘇茉可以直接將 magnet link 添加到 qBittorrent 下載

用法:
    python add_to_qbittorrent.py "<magnet_link>"
    python add_to_qbittorrent.py --list
    python add_to_qbittorrent.py --status
"""

import sys
import os
import re
import argparse
import requests
from urllib.parse import urlencode, urlparse

# qBittorrent Web UI 設定（老爺已設定）
QB_URL = "http://localhost:8080"
QB_USER = "admin"
QB_PASS = "adminadmin"

# 常用 tracker 列表（自動附加到 magnet link）
TRACKERS = [
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://open.stealth.si:80/announce",
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://tracker.bittor.pw:1337/announce",
    "udp://public.popcorn-tracker.org:6969/announce",
    "udp://tracker.dler.org:6969/announce",
    "udp://exodus.desync.com:6969/announce",
    "udp://open.demonii.com:1337/announce",
    "udp://glotorrents.pw:6969/announce",
    "udp://tracker.coppersurfer.tk:6969/announce",
    "udp://p4p.arenabg.com:1337/announce",
    "udp://tracker.internetwarriors.net:1337/announce",
    "http://tracker.opentrackr.org:1337/announce",
    "http://tracker.torrent.eu.org:451/announce",
    "https://tracker.lilith档.com:443/announce",
    "https://tr.highhopes.xyz:443/announce",
    "https://t.trackers.net:443/announce",
]

def add_trackers_to_magnet(magnet):
    """將 trackers 加入 magnet link"""
    if not magnet.startswith("magnet:?"):
        return magnet
    
    # 檢查是否已有 tr= 參數
    if "&tr=" in magnet or "tr=" in magnet:
        # 已有 trackers，直接返回
        return magnet
    
    # 附加 trackers
    trackers_str = "&tr=".join(TRACKERS)
    return f"{magnet}&tr={trackers_str}"

class qBittorrentBridge:
    def __init__(self, url=QB_URL, username=QB_USER, password=QB_PASS):
        self.url = url.rstrip("/")
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.sid = None
        
    def login(self):
        """登入 qBittorrent"""
        try:
            resp = self.session.post(
                f"{self.url}/api/v2/auth/login",
                data={"username": self.username, "password": self.password},
                timeout=30
            )
            if resp.status_code == 200 and resp.text == "Ok.":
                # 取得 SID
                self.sid = self.session.cookies.get("SID")
                print(f"[OK] Login success! SID: {self.sid[:16]}...")
                return True
            else:
                print(f"[FAIL] Login failed: {resp.status_code} - {resp.text}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Cannot connect to qBittorrent ({self.url})")
            print(f"   Please check if qBittorrent Web UI is running!")
            return False
        except Exception as e:
            print(f"[ERROR] Login error: {e}")
            return False
    
    def is_magnet(self, link):
        """檢查是否為 magnet link"""
        return link.strip().startswith("magnet:?")
    
    def extract_hash(self, magnet):
        """從 magnet link 提取 info hash"""
        match = re.search(r'btih:([a-fA-F0-9]{40})', magnet)
        if match:
            return match.group(1).lower()
        return None
    
    def add_magnet(self, magnet):
        """添加 magnet link 到 qBittorrent（自動加入 trackers）"""
        if not self.sid and not self.login():
            return False
        
        # 自動加入 trackers
        original_magnet = magnet
        magnet = add_trackers_to_magnet(magnet)
        if magnet != original_magnet:
            print(f"[INFO] Added {len(TRACKERS)} trackers to magnet link")
        
        try:
            # qBittorrent API - 添加 magnet link
            resp = self.session.post(
                f"{self.url}/api/v2/torrents/add",
                data={"urls": magnet.strip()},
                timeout=30
            )
            
            if resp.status_code == 200:
                hash40 = self.extract_hash(magnet)
                if hash40:
                    print(f"[OK] Magnet link added to qBittorrent!")
                    print(f"     Info Hash: {hash40}")
                    return True
                else:
                    print(f"[OK] Added (cannot parse info hash)")
                    return True
            else:
                print(f"[FAIL] Add failed: {resp.status_code} - {resp.text}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Add error: {e}")
            return False
    
    def add_torrent_file(self, file_path):
        """添加 torrent 檔案到 qBittorrent"""
        if not self.sid and not self.login():
            return False
        
        try:
            with open(file_path, "rb") as f:
                files = {"torrents": f}
                resp = self.session.post(
                    f"{self.url}/api/v2/torrents/add",
                    files=files,
                    timeout=30
                )
            
            if resp.status_code == 200:
                print(f"[OK] Torrent file added!")
                return True
            else:
                print(f"[FAIL] Add failed: {resp.status_code}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Add error: {e}")
            return False
    
    def list_torrents(self):
        """列出所有 torrents"""
        if not self.sid and not self.login():
            return
        
        try:
            resp = self.session.get(
                f"{self.url}/api/v2/torrents/info",
                timeout=10
            )
            
            if resp.status_code == 200:
                torrents = resp.json()
                if not torrents:
                    print("[EMPTY] No active downloads")
                    return
                
                print(f"\n[qBittorrent] Download list ({len(torrents)} items)\n")
                print(f"{'#':<4} {'名稱':<50} {'狀態':<12} {'進度':<8} {'大小'}")
                print("-" * 100)
                
                for i, t in enumerate(torrents, 1):
                    name = t.get("name", "Unknown")[:48]
                    state = t.get("state", "Unknown")
                    progress = t.get("progress", 0) * 100
                    size = t.get("total_size", 0)
                    size_str = self._format_size(size)
                    
                    # 狀態翻譯
                    state_map = {
                        "downloading": "下載中",
                        "seeding": "做種中",
                        "paused": "暫停",
                        "queued": "排隊中",
                        "checking": "檢查中",
                        "error": "錯誤",
                        "uploading": "上傳中",
                        "stalled": "停滯",
                    }
                    state_cn = state_map.get(state.lower(), state)
                    
                    print(f"{i:<4} {name:<50} {state_cn:<12} {progress:>6.1f}%  {size_str}")
                    
        except Exception as e:
            print(f"[ERROR] Get list error: {e}")
    
    def get_download_speed(self):
        """取得目前下載速度"""
        if not self.sid and not self.login():
            return None, None
        
        try:
            resp = self.session.get(
                f"{self.url}/api/v2/torrents/info",
                timeout=30
            )
            
            if resp.status_code == 200:
                torrents = resp.json()
                total_down = 0
                total_up = 0
                
                for t in torrents:
                    total_down += t.get("dlspeed", 0)
                    total_up += t.get("upspeed", 0)
                
                return total_down, total_up
                
        except:
            pass
        return None, None
    
    @staticmethod
    def _format_size(size_bytes):
        """格式化檔案大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"


def main():
    parser = argparse.ArgumentParser(description="SumoTorrent - qBittorrent 橋樑工具")
    parser.add_argument("magnet", nargs="?", help="Magnet link 或 torrent 檔案路徑")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有下載任務")
    parser.add_argument("--status", "-s", action="store_true", help="顯示下載速度")
    parser.add_argument("--url", default=QB_URL, help=f"qBittorrent URL (預設: {QB_URL})")
    parser.add_argument("--user", default=QB_USER, help=f"qBittorrent 帳號 (預設: {QB_USER})")
    parser.add_argument("--pass", dest="password", default=QB_PASS, help="qBittorrent 密碼")
    
    args = parser.parse_args()
    
    bridge = qBittorrentBridge(url=args.url, username=args.user, password=args.password)
    
    if args.list:
        bridge.list_torrents()
    elif args.status:
        down, up = bridge.get_download_speed()
        if down is not None:
            print(f"[DOWN] Download: {bridge._format_size(down)}/s")
            print(f"[UP]   Upload:   {bridge._format_size(up)}/s")
        else:
            print("[ERROR] Cannot get status")
    elif args.magnet:
        if os.path.isfile(args.magnet):
            bridge.add_torrent_file(args.magnet)
        elif bridge.is_magnet(args.magnet):
            bridge.add_magnet(args.magnet)
        else:
            print(f"[ERROR] Invalid magnet link or file path")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
