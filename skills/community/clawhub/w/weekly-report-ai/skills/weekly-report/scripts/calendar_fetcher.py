#!/usr/bin/env python3
"""
日历获取脚本
支持 Google Calendar 和飞书日历
"""

import argparse
import os
from datetime import datetime, timedelta
from typing import List, Dict


def get_google_calendar(credentials_path: str, since: str, until: str) -> Dict:
    """获取Google日历事件"""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        creds = Credentials.from_authorized_user_file(credentials_path)
        service = build('calendar', 'v3', credentials=creds)
        
        since_dt = datetime.fromisoformat(since)
        until_dt = datetime.fromisoformat(until)
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=since_dt.isoformat() + 'Z',
            timeMax=until_dt.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        return {
            "events": [
                {
                    "title": e.get("summary", "无标题"),
                    "start": e["start"].get("dateTime", e["start"].get("date")),
                    "end": e["end"].get("dateTime", e["end"].get("date")),
                    "description": e.get("description", ""),
                    "organizer": e.get("organizer", {}).get("displayName", "未知")
                }
                for e in events
            ]
        }
    except Exception as e:
        print(f"Error fetching Google Calendar: {e}")
        return {"events": []}


def get_feishu_calendar(token: str, since: str, until: str) -> Dict:
    """获取飞书日历事件"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 获取日历列表
        cal_list_url = "https://open.feishu.cn/open-apis/calendar/v3/calendars"
        resp = requests.get(cal_list_url, headers=headers)
        
        if resp.status_code != 200:
            return {"events": []}
        
        calendars = resp.json().get("data", {}).get("calendars", [])
        
        all_events = []
        
        for cal in calendars:
            cal_id = cal.get("id")
            if not cal_id:
                continue
                
            # 获取日历事件
            events_url = f"https://open.feishu.cn/open-apis/calendar/v3/calendars/{cal_id}/events"
            params = {
                "start_time": since,
                "end_time": until
            }
            
            resp = requests.get(events_url, headers=headers, params=params)
            if resp.status_code == 200:
                events = resp.json().get("data", {}).get("items", [])
                for e in events:
                    all_events.append({
                        "title": e.get("summary", "无标题"),
                        "start": e.get("start", {}).get("date_time", ""),
                        "end": e.get("end", {}).get("date_time", ""),
                        "description": e.get("description", ""),
                        "organizer": e.get("organizer", {}).get("name", "未知")
                    })
        
        return {"events": all_events}
        
    except Exception as e:
        print(f"Error fetching Feishu Calendar: {e}")
        return {"events": []}


def main():
    parser = argparse.ArgumentParser(description="获取日历事件")
    parser.add_argument("--type", choices=["google", "feishu"], required=True, help="日历类型")
    parser.add_argument("--token", help="飞书Token或Google credentials文件路径")
    parser.add_argument("--since", required=True, help="开始日期")
    parser.add_argument("--until", required=True, help="结束日期")
    
    args = parser.parse_args()
    
    if args.type == "google":
        results = get_google_calendar(args.token, args.since, args.until)
    else:
        results = get_feishu_calendar(args.token, args.since, args.until)
    
    import json
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
