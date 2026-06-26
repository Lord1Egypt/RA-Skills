#!/usr/bin/env python3
import sys
import os
import json
import re
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import (
    search_web, 
    call_llm, 
    send_slack_message, 
    clean_json_block,
    parse_args,
    load_config
)
from seesaw import SeesawClient

MY_CREATOR_ID = "fca3cb34-04f0-4af6-b0cc-9c05281f341b"

def extract_key_entity(title: str, description: str) -> tuple:
    text = f"{title} {description}".lower()
    text = re.sub(r'^(will|是否|是不是|会不会|能否|是否)', '', text)
    threshold_match = re.search(r'(\d+\.?\d*)\s*(dollar|usd|\$|percent|%|万|千|亿)?', text)
    threshold = threshold_match.group(1) if threshold_match else None
    words = text.split()
    subject = ' '.join(words[:5]) if words else title
    return subject.strip(), threshold

def determine_resolution(market: Dict[str, Any], news_text: str) -> Optional[Dict[str, Any]]:
    title = market.get("title", "")
    description = market.get("description", "")
    options = market.get("options", [])
    if not options or not news_text: return None
    options_desc = "\n".join([f"- {opt.get('name')}: {opt.get('description', 'No description')}" for opt in options])
    prompt = f"Market Title: {title}\nOptions:\n{options_desc}\nRecent News:\n{news_text[:2000]}\nOutput JSON:\n{{\"resolved\": true/false, \"option_name\": \"winning option\", \"option_id\": \"winning id\", \"reasoning\": \"explanation\"}}"
    llm_resp = call_llm([{"role": "user", "content": prompt}])
    if not llm_resp: return None
    try:
        result = json.loads(clean_json_block(llm_resp))
        if result.get("resolved") and result.get("option_name"):
            for opt in options:
                if opt.get("name") == result["option_name"]:
                    return {"option_id": opt.get("id"), "option_name": opt.get("name"), "reasoning": result.get("reasoning", "")}
    except: pass
    return None

def generate_progress_comment(market: Dict[str, Any], news_text: str) -> Optional[str]:
    title = market.get("title", "")
    prompt = f"Market Title: {title}\nRecent News:\n{news_text[:1500]}\nWrite a short update (in Chinese, under 100 words) about the latest developments. Include specific numbers/data if available. Output JSON:\n{{\"comment\": \"your comment\"}}"
    llm_resp = call_llm([{"role": "user", "content": prompt}])
    if not llm_resp: return None
    try:
        result = json.loads(clean_json_block(llm_resp))
        return result.get("comment")
    except: return None

def main():
    args = parse_args("运营SeeSaw话题：检查活跃话题、查询进展、断言、评论")
    config = load_config()
    dry_run = args.dry_run or config.get("dry_run", False)
    
    print("--- Starting SeeSaw Market Management ---")
    client = SeesawClient()
    
    try:
        result = client.list_markets(page=1, limit=200, status="active")
        all_markets = result.get("items", []) if isinstance(result, dict) else result
        my_markets = [m for m in all_markets if m.get("creator", {}).get("id") == MY_CREATOR_ID]
    except Exception as e:
        print(f"获取话题失败: {e}")
        return
    
    now = datetime.now(timezone.utc)
    slack_updates = []
    
    for market in my_markets:
        market_id = market.get("id")
        title = market.get("title", "")
        end_time_str = market.get("end_time")
        
        try:
            end_time = datetime.fromisoformat(end_time_str.replace("Z", "+00:00"))
            is_expired = end_time <= now
        except:
            is_expired = False
            
        subject, threshold = extract_key_entity(title, "")
        search_query = f"{subject} 最新进展"
        if threshold: search_query += f" {threshold}"
        
        search_result = search_web(search_query, topic="news", days=3, max_results=2)
        news_text = search_result.get("text", "")
        
        if not news_text: continue
        
        if is_expired:
            resolution = determine_resolution(market, news_text)
            if resolution:
                option_name = resolution["option_name"]
                if not dry_run:
                    try:
                        client.assert_result(market_id, resolution["option_id"])
                        slack_updates.append(f"✅ *已断言*: {title} -> {option_name}\n理由: {resolution['reasoning']}")
                    except Exception as e:
                        slack_updates.append(f"❌ *断言失败*: {title} -> {option_name} ({e})")
                else:
                    slack_updates.append(f"🔍 *[Dry Run] 拟断言*: {title} -> {option_name}\n理由: {resolution['reasoning']}")
        else:
            comment = generate_progress_comment(market, news_text)
            if comment:
                if not dry_run:
                    try:
                        client.add_comment(market_id, comment)
                        slack_updates.append(f"💬 *动态更新*: {title}\n> {comment}")
                    except:
                        slack_updates.append(f"💬 *动态获取*: {title}\n> {comment} (注: 评论API暂不可用)")
                else:
                    slack_updates.append(f"📝 *[Dry Run] 拟评论*: {title}\n> {comment}")
    
    # Send Slack updates
    if slack_updates:
        final_msg = "🍉 *SeeSaw 话题全天候运营报告*\n\n" + "\n\n".join(slack_updates)
        print("====== SLACK SUMMARY ======")
        print(final_msg)
        print("===========================")

if __name__ == "__main__":
    main()
