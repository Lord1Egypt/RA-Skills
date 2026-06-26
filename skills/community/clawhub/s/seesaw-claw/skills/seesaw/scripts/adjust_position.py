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

def main():
    args = parse_args("Adjust existing positions based on news.")
    config = load_config()
    dry_run = args.dry_run or config.get("dry_run", False)
    
    print("--- Starting Adjust Position Workflow ---")
    if dry_run:
        print("[DRY-RUN MODE ENABLED]")
        
    client = SeesawClient()

    # Get Balance for risk check
    try:
        balance_info = client.get_balance() if not dry_run else {"balance": 1000}
        # Balance format: {"balance": 26269.238}
        available_balance = float(balance_info.get("balance", 0))
        print(f"Available Balance: {available_balance}")
    except Exception as e:
        print(f"Failed to fetch balance: {e}")
        available_balance = 0

    try:
        positions = client.get_positions()
        if isinstance(positions, dict) and 'items' in positions:
            positions = positions['items']
        elif not isinstance(positions, list):
            positions = []
            
        if not positions:
            print("No active positions found.")
            return

        print(f"Found {len(positions)} positions.")

        # Process each position
        for pos in positions:
            market_id = pos.get('prediction_id')
            option_id = pos.get('option_id')
            current_shares = int(pos.get('amount', 0))
            
            # Fetch market details
            try:
                market = client.get_market(market_id)
            except Exception as e:
                print(f"Failed to fetch market {market_id}: {e}")
                continue
                
            status = market.get('status')
            title = market.get('title')
            
            print(f"Processing position: {title} (Status: {status})")
            
            if status == 'completed':
                # Try to settle
                print(f"Market completed. Attempting to settle...")
                if not dry_run:
                    try:
                        resp = client.settle(market_id)
                        msg = f"Settled Market: {title} ({market_id})"
                        send_slack_message(msg)
                        print(msg)
                    except Exception as e:
                        print(f"Failed to settle: {e}")
                else:
                    print(f"[DRY-RUN] Would settle market {market_id}")
            
            elif status == 'active':
                # Check for news and adjust
                search_query = f"{title} news update"
                search_result_data = search_web(search_query, topic="news", days=1)
                news_text = search_result_data["text"]
                
                if not news_text:
                    print("No new news found.")
                    continue

                # LLM Analysis
                prompt = f"""
                Analyze my position in prediction market: "{title}"
                Current Position: Holding {current_shares} shares of Option ID {option_id}
                Market Status: Active
                
                Recent News:
                {news_text}
                
                Task:
                Decide whether to HOLD, BUY MORE, or SELL based on the news.
                Consider the risk and potential return.
                
                Output JSON:
                {{
                  "action": "hold" | "buy" | "sell",
                  "amount": integer (suggested amount to trade),
                  "reasoning": "..."
                }}
                """
                
                llm_resp = call_llm([{"role": "user", "content": prompt}])
                if not llm_resp:
                    continue

                try:
                    decision = json.loads(clean_json_block(llm_resp))
                except:
                    print("Failed to parse decision.")
                    continue

                action = decision.get('action')
                trade_amount = int(decision.get('amount', 0))
                reason = decision.get('reasoning')

                if action == 'sell' and trade_amount > 0:
                    # Sell logic
                    trade_amount = min(trade_amount, current_shares) # Cannot sell more than held
                    print(f"Selling {trade_amount} shares of {title}...")
                    
                    if not dry_run:
                        try:
                            client.sell(market_id, option_id, trade_amount)
                            msg = f"Sold Position: {title} - Amount: {trade_amount}\nReason: {reason}"
                            send_slack_message(msg)
                            print(msg)
                        except Exception as e:
                            print(f"Failed to sell: {e}")
                    else:
                        print(f"[DRY-RUN] Would sell {trade_amount} shares. Reason: {reason}")
                
                elif action == 'buy' and trade_amount > 0:
                    # Buy more logic with risk check
                    max_size = config.get("max_position_size", 100)
                    trade_amount = min(trade_amount, max_size)
                    
                    # Simple cost check (assuming price ~ 1 for simplicity, real check needs quote)
                    # We should get a quote to know the cost
                    if not dry_run:
                        try:
                            # Check cost
                            quote = client.get_quote(market_id, option_id, trade_amount, side="buy")
                            cost = float(quote.get("cost", 0)) if quote else 0
                            
                            if cost > available_balance:
                                print(f"Insufficient funds to buy {trade_amount} (Cost: {cost}, Bal: {available_balance})")
                                continue
                                
                            print(f"Buying {trade_amount} more shares of {title} (Cost: {cost})...")
                            client.buy(market_id, option_id, trade_amount)
                            msg = f"Increased Position: {title} - Amount: {trade_amount}\nReason: {reason}"
                            send_slack_message(msg)
                            print(msg)
                            available_balance -= cost # Update local balance estimate
                        except Exception as e:
                            print(f"Failed to buy: {e}")
                    else:
                        print(f"[DRY-RUN] Would buy {trade_amount} shares. Reason: {reason}")
                
                else:
                    print(f"Holding position. Reason: {reason}")

    except Exception as e:
        print(f"Error processing positions: {e}")

if __name__ == "__main__":
    main()
