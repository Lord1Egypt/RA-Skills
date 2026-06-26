#!/usr/bin/env python3
"""
Moji辞書生词本管理器
支持：获取、筛选、删除单词
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from typing import List, Dict

APP_ID = "E62VyFVLMiW7kvbtVq3p"
INSTALL_ID = "60c39bef-8039-4b07-9669-64d1bb0327d7"
BASE_URL = "https://api.mojidict.com/parse/functions"

class MojiVocabManager:
    def __init__(self, token: str, device_id: str):
        self.token = token
        self.device_id = device_id
    
    def _fetch_headers(self):
        return {
            "Content-Type": "text/plain",
            "Origin": "https://www.mojidict.com",
            "Referer": "https://www.mojidict.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def _delete_headers(self):
        return {
            "Content-Type": "application/json",
            "Origin": "https://www.mojidict.com",
            "Referer": "https://www.mojidict.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "x-moji-app-id": "com.mojitec.mojidict",
            "x-moji-app-version": "4.15.4",
            "x-moji-device-id": self.device_id,
            "x-moji-os": "MobileWeb_iOS",
            "x-moji-session-id": self.token,
            "x-moji-token": self.token
        }
    
    def fetch_page(self, page: int, count: int = 30, sort_type: int = 5) -> List[Dict]:
        """拉取收藏夹一页数据
        sort_type: 1=按时间排序, 5=从最老的开始
        """
        payload = json.dumps({
            "fid": "ROOT#com.mojitec.mojidict#zh-CN_ja",
            "count": count, "sortType": sort_type, "pageIndex": page,
            "g_os": "PCWeb", "g_ver": "4.15.4",
            "_ApplicationId": APP_ID, "_ClientVersion": "js4.3.1",
            "_InstallationId": INSTALL_ID, "_SessionToken": self.token
        }).encode()
        
        req = urllib.request.Request(
            f"{BASE_URL}/folder-fetchContentWithRelatives",
            data=payload, headers=self._fetch_headers()
        )
        
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                result = json.loads(resp.read().decode())
                return result.get("result", {}).get("result", [])
        except Exception as e:
            print(f"获取第{page}页失败: {e}")
            return []
    
    def get_all_words(self, max_pages: int = 10, sort_type: int = 5) -> List[Dict]:
        """获取单词（默认最多10页=300个，避免太多）
        sort_type: 1=按时间排序(最新的), 5=从最老的开始
        """
        all_words = []
        page = 0
        
        while page < max_pages:
            items = self.fetch_page(page, sort_type=sort_type)
            if not items:
                break
            
            all_words.extend(items)
            print(f"第{page+1}页: {len(items)} 个，累计: {len(all_words)}")
            
            if len(items) < 30:
                break
            page += 1
            time.sleep(0.1)
        
        return all_words
    
    def get_oldest_words(self, count: int = 30) -> List[Dict]:
        """获取最早添加的单词（2020年的）"""
        print("正在获取最早的单词（sortType=5）...")
        return self.get_all_words(max_pages=1, sort_type=5)
    
    def get_stats(self) -> Dict:
        """获取收藏夹统计"""
        words = self.get_all_words()
        
        stats = {
            "total": len(words),
            "by_level": {"N1": 0, "N2": 0, "N3": 0, "N4": 0, "N5": 0, "未知": 0}
        }
        
        for w in words:
            target = w.get("target", {})
            tags = target.get("tags", "") or ""
            
            level_found = False
            for level in ["N1", "N2", "N3", "N4", "N5"]:
                if level in tags:
                    stats["by_level"][level] += 1
                    level_found = True
                    break
            
            if not level_found:
                stats["by_level"]["未知"] += 1
        
        return stats
    
    def delete_items(self, ids: List[str], dry_run: bool = False) -> Dict:
        """批量删除单词"""
        if dry_run:
            return {"success": ids, "failed": []}
        
        payload = json.dumps({"itemIds": ids}).encode()
        req = urllib.request.Request(
            "https://api.mojidict.com/app/mojidict/api/v1/folder/batchUnfollow",
            data=payload, headers=self._delete_headers()
        )
        
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}
    
    def delete_by_level(self, levels: List[str], keep_levels: tuple = ("N1", "N2"), 
                        dry_run: bool = False) -> Dict:
        """按 JLPT 级别删除"""
        words = self.get_all_words()
        to_delete = []
        
        for w in words:
            target = w.get("target", {})
            tags = target.get("tags", "") or ""
            
            if not tags:
                continue
            
            tag_list = [t.strip() for t in tags.split("#") if t.strip()]
            
            # 如果包含保留级别，跳过
            if any(t in tag_list for t in keep_levels):
                continue
            
            # 如果包含要删除的级别，加入删除列表
            if any(t in tag_list for t in levels):
                obj_id = w.get("objectId")
                if obj_id:
                    to_delete.append(obj_id)
        
        print(f"\n找到 {len(to_delete)} 个待删除单词")
        
        if dry_run:
            print("【试运行模式】不会真正删除")
            return {"deleted": 0, "dry_run": True}
        
        # 分批删除（每批30个）
        total_deleted = 0
        for i in range(0, len(to_delete), 30):
            batch = to_delete[i:i+30]
            result = self.delete_items(batch)
            success = len(result.get("success", []))
            total_deleted += success
            print(f"批次 {i//30 + 1}: 删除 {success}/{len(batch)} 个")
            time.sleep(0.2)
        
        return {"deleted": total_deleted}


def main():
    parser = argparse.ArgumentParser(description="Moji辞書生词本管理器")
    parser.add_argument("--token", help="sessionToken，或设置环境变量 MOJI_TOKEN")
    parser.add_argument("--device-id", help="deviceId，或设置环境变量 MOJI_DEVICE_ID")
    parser.add_argument("--action", choices=["stats", "list", "delete", "delete-by-level"],
                       required=True, help="操作类型")
    parser.add_argument("--levels", default="N3,N4,N5", help="要删除的级别（逗号分隔）")
    parser.add_argument("--word-id", help="要删除的单词ID")
    parser.add_argument("--dry-run", action="store_true", help="试运行，不真正删除")
    
    args = parser.parse_args()
    
    # 获取凭证
    token = args.token or os.environ.get("MOJI_TOKEN")
    device_id = args.device_id or os.environ.get("MOJI_DEVICE_ID")
    
    if not token or not device_id:
        print("❌ 错误: 请提供 --token 和 --device-id，或设置环境变量 MOJI_TOKEN / MOJI_DEVICE_ID")
        sys.exit(1)
    
    manager = MojiVocabManager(token, device_id)
    
    if args.action == "stats":
        print("正在统计...")
        stats = manager.get_stats()
        print(f"\n📊 收藏夹统计")
        print(f"总计: {stats['total']} 个单词")
        print("\n按 JLPT 级别:")
        for level, count in stats["by_level"].items():
            print(f"  {level}: {count} 个")
    
    elif args.action == "list":
        print("正在获取所有单词...")
        words = manager.get_all_words()
        print(f"\n总计: {len(words)} 个单词")
        for w in words[:10]:
            target = w.get("target", {})
            word = target.get("word", "N/A")
            tags = target.get("tags", "无标签")
            print(f"  - {word} [{tags}]")
        if len(words) > 10:
            print(f"  ... 还有 {len(words)-10} 个")
    
    elif args.action == "delete-by-level":
        levels = [l.strip() for l in args.levels.split(",")]
        print(f"将删除级别: {', '.join(levels)}")
        result = manager.delete_by_level(levels, dry_run=args.dry_run)
        if args.dry_run:
            print("✅ 试运行完成，未实际删除")
        else:
            print(f"✅ 成功删除 {result.get('deleted', 0)} 个单词")


if __name__ == "__main__":
    main()
