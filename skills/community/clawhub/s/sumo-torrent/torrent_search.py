#!/usr/bin/env python3
"""
Torrent Search Skill - 搜尋 Torrent 並輸出含 Trackers 的 Magnet 連結
用法: python torrent_search.py <關鍵字> [output_dir]

重要：輸出的 Magnet 連結已自動加上公開 Trackers，可直接貼給 qBittorrent 使用！
"""

import sys
import os
import re
from datetime import datetime

# 公開 Trackers 清單（從老爺的 YMDD474 連結解析出來的）
TRACKERS = [
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://open.stealth.si:80/announce",
    "udp://wepzone.net:6969/announce",
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://tracker.theoks.net:6969/announce",
    "udp://tracker.srv00.com:6969/announce",
    "udp://tracker.dler.org:6969/announce",
    "udp://tracker.darkness.services:6969/announce",
    "udp://tracker.corpscorp.online:80/announce",
    "udp://tracker.bittor.pw:1337/announce",
    "udp://tracker.004430.xyz:1337/announce",
    "udp://t.overflow.biz:6969/announce",
    "udp://leet-tracker.moe:1337/announce",
    "udp://exodus.desync.com:6969/announce",
    "udp://bittorrent-tracker.e-n-c-r-y-p-t.net:1337/announce",
    "udp://6ahddutb1ucc3cp.ru:6969/announce",
    "https://tracker.zhuqiy.com:443/announce",
    "https://tracker.pmman.tech:443/announce",
    "https://tracker.nekomi.cn:443/announce",
    "https://tracker.moeblog.cn:443/announce",
    "https://tracker.bt4g.com:443/announce",
]

def add_trackers(magnet_link):
    """將公開 Trackers 加到 Magnet 連結"""
    # 如果已經有 trackers，就不再加
    if "&tr=" in magnet_link:
        return magnet_link
    
    # 如果沒有 dn 參數，加上預設 name
    base = magnet_link.rstrip("&")
    
    # 如果沒有 dn 參數
    if "&dn=" not in base:
        # 從 magnet link 中嘗試提取名稱
        name_match = re.search(r'dn=([^&]+)', magnet_link)
        if name_match:
            dn = name_match.group(1)
        else:
            dn = "download"
    
    # 確保結尾不是 &dn=xxx，而是有 trackers
    # 先檢查 base 是否已經是完整格式
    if not base.startswith("magnet:?xt="):
        return magnet_link  # 不是有效的 magnet link
    
    # 移除結尾的 &
    base = base.rstrip("&")
    
    # 添加所有 trackers
    tracker_str = "&tr=".join(TRACKERS)
    full_magnet = f"{base}&tr={tracker_str}"
    
    return full_magnet

def search_torrent(keyword, output_dir=None):
    """搜尋 Torrent"""
    if output_dir is None:
        output_dir = r"C:\butler_sumo\docs\torrent"
    
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 輸出檔案
    date_str = datetime.now().strftime('%Y%m%d')
    output_file = os.path.join(output_dir, f"output{date_str}.txt")
    
    print(f"\n{'='*60}")
    print(f"  Torrent 搜尋工具")
    print(f"{'='*60}")
    print(f"\n關鍵字: {keyword}")
    print(f"輸出檔案: {output_file}")
    print(f"\n請在瀏覽器中開啟以下連結進行搜尋：")
    print(f"\nhttps://bt4gprx.com/search?q={keyword}")
    print(f"\n然後把有活跃度（Seeders > 0）的 Magnet 連結（不含 Trackers 的版本）貼到這個檔案：")
    print(f"\n{output_file}")
    print(f"\n蘇茉會自動幫忙加上公開 Trackers！")
    print(f"\n{'='*60}")
    
    return output_file

def save_magnets(magnets, output_file):
    """儲存 Magnet 連結到檔案（自動加上 Trackers）"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Torrent Search Results - {date_str}\n")
        f.write(f"# ================================\n")
        f.write(f"# 蘇茉已自動加上 {len(TRACKERS)} 個公開 Trackers\n")
        f.write(f"# 可直接貼給 qBittorrent 使用！\n")
        f.write(f"\n")
        
        for i, magnet in enumerate(magnets, 1):
            # 自動加上 trackers
            full_magnet = add_trackers(magnet)
            f.write(f"# {i}. {full_magnet}\n")
    
    print(f"\n已儲存 {len(magnets)} 個含 Trackers 的 Magnet 連結到：")
    print(f"{output_file}")
    print(f"\n每個連結都已經自動加上 {len(TRACKERS)} 個公開 Trackers！")
    print(f"老爺可以直接把檔案內容貼給 qBittorrent 使用！")

def add_trackers_interactive():
    """互動式：將使用者輸入的 Magnet 連結加上 Trackers"""
    print("\n請貼上 Magnet 連結（不含 Trackers 的版本）：")
    print("(輸入空行結束)\n")
    
    magnets = []
    while True:
        line = input().strip()
        if not line:
            break
        magnets.append(line)
    
    if not magnets:
        print("沒有輸入任何連結！")
        return
    
    # 輸出檔案
    date_str = datetime.now().strftime('%Y%m%d')
    output_dir = r"C:\butler_sumo\docs\torrent"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"output{date_str}.txt")
    
    save_magnets(magnets, output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python torrent_search.py <關鍵字>")
        print("或: python torrent_search.py --add-tracker  (互動模式)")
        sys.exit(1)
    
    if sys.argv[1] == "--add-tracker":
        add_trackers_interactive()
    else:
        keyword = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        search_torrent(keyword, output_dir)
