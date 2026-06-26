import sys
import os
import json
from datetime import datetime

# Add current dir to path to import utils
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

def find_option_id(options, option_name):
    """
    Find option ID matching the name.
    options: List of dicts or strings.
    """
    if not options:
        return None
    
    # Normalize name
    target = option_name.lower().strip()
    
    # First pass: exact match on ID or Text
    for opt in options:
        if isinstance(opt, dict):
            oid = str(opt.get('id', '')).lower()
            otext = str(opt.get('text', '')).lower() # specific field might vary
            otitle = str(opt.get('title', '')).lower()
            
            if target == oid or target == otext or target == otitle:
                return opt.get('id')
        elif isinstance(opt, str):
            if target == opt.lower():
                # If options are just strings, we can't return an ID unless the API accepts the string.
                # Assuming API needs ID, but if options are strings, maybe the index or the string itself is the ID?
                # Seesaw usually uses UUIDs. If 'options' is a list of strings in 'create_market', 
                # the 'get_market' usually returns objects with IDs.
                pass

    # Second pass: Fuzzy match / Substring
    for opt in options:
        if isinstance(opt, dict):
            otext = str(opt.get('text', '') or opt.get('title', '')).lower()
            if target in otext or otext in target:
                return opt.get('id')
                
    return None

def main():
    args = parse_args("Scan and open new positions.")
    config = load_config()
    dry_run = args.dry_run or config.get("dry_run", False)
    
    print("--- Starting Open Position Workflow ---")
    if dry_run:
        print("[DRY-RUN MODE ENABLED]")
        
    client = SeesawClient()

    # 1. Get current positions to avoid duplicates
    try:
        positions = client.get_positions()
        # Ensure positions is a list
        if isinstance(positions, dict) and 'items' in positions:
            positions = positions['items']
        elif not isinstance(positions, list):
            positions = []
            
        held_market_ids = {p.get('prediction_id') for p in positions}
    except Exception as e:
        print(f"Failed to fetch positions: {e}")
        return

    # 2. Scan hot and new markets
    candidates = []
    try:
        hot_resp = client.list_markets(sort="hot", limit=5)
        new_resp = client.list_markets(sort="newest", limit=5)
        
        hot_markets = hot_resp.get('items', []) if isinstance(hot_resp, dict) else hot_resp
        new_markets = new_resp.get('items', []) if isinstance(new_resp, dict) else new_resp
        
        # Merge lists, avoiding duplicates
        all_markets = {m['id']: m for m in hot_markets + new_markets}
        
        for m_id, market in all_markets.items():
            if m_id in held_market_ids:
                continue
            if market.get('status') != 'active':
                continue
            candidates.append(market)
            
    except Exception as e:
        print(f"Failed to list markets: {e}")
        return

    if not candidates:
        print("No suitable candidate markets found.")
        return

    print(f"Found {len(candidates)} candidate markets not currently held.")

    # 3. Analyze each candidate
    for market in candidates:
        market_id = market.get('id')
        title = market.get('title')
        description = market.get('description', '')
        options = market.get('options', [])
        
        # Try to find probabilities - use correct API field: Option.current_probability
        probs = {}
        if options:
            for opt in options:
                if isinstance(opt, dict):
                    opt_name = opt.get('name') or opt.get('text') or opt.get('title', '')
                    opt_prob = opt.get('current_probability', 0)
                    probs[opt_name] = opt_prob
        
        print(f"Analyzing market: {title}")
        
        # Search web for latest info
        search_query = f"{title} {description} news"
        search_result_data = search_web(search_query, topic="news", days=3)
        news_text = search_result_data["text"]
        
        if not news_text:
            print("No news found, skipping.")
            continue

        # LLM Analysis
        prompt = f"""
        Analyze the prediction market: "{title}"
        Description: {description}
        Options: {json.dumps(options)}
        Current Probabilities: {probs or "Unknown"}
        
        Recent News:
        {news_text}
        
        Task:
        Determine if this market is significantly mispriced or offers a high-confidence opportunity based on the news.
        
        Output JSON:
        {{
          "recommendation": "buy" or "pass",
          "option_to_buy": "Exact Option Name or ID",
          "confidence": 0.0 to 1.0,
          "reasoning": "..."
        }}
        """
        
        llm_resp = call_llm([{"role": "user", "content": prompt}])
        if not llm_resp:
            continue

        try:
            analysis = json.loads(clean_json_block(llm_resp))
        except:
            print("Failed to parse LLM analysis.")
            continue

        if analysis.get('recommendation') == 'buy' and analysis.get('confidence', 0) > 0.7:
            option_name = analysis.get('option_to_buy')
            option_id = find_option_id(options, option_name)
            
            if option_id:
                amount = config.get("max_position_size", 100)
                print(f"Executing BUY for {title} - Option: {option_name} (ID: {option_id})")
                
                if not dry_run:
                    try:
                        resp = client.buy(market_id, option_id, amount)
                        msg = f"Opened Position: {title} ({option_name}) - Amount: {amount}\nReason: {analysis['reasoning']}"
                        send_slack_message(msg)
                        print(msg)
                    except Exception as e:
                        print(f"Failed to buy: {e}")
                else:
                    print(f"[DRY-RUN] Would buy {amount} shares of option {option_id}. Reason: {analysis['reasoning']}")
            else:
                print(f"Could not find option ID for {option_name}")
        else:
            print(f"Pass: {analysis.get('reasoning')}")

if __name__ == "__main__":
    main()
