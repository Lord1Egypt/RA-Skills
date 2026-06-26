import sys
import os
import json
from datetime import datetime, timedelta

# Add current dir to path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import (
    search_web, 
    search_image,
    call_llm, 
    send_slack_message, 
    load_json, 
    save_json, 
    clean_json_block,
    parse_args
)
from seesaw import SeesawClient

TOPICS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "created_topics.json")

def main():
    args = parse_args("Generate and create prediction market topics.")
    dry_run = args.dry_run
    
    print("--- Starting Generate Topic Workflow ---")
    if dry_run:
        print("[DRY-RUN MODE ENABLED]")

    # 1. Search for hotspots
    print("Searching for recent hotspots...")
    search_query = "recent global news hotspots trending topics prediction markets"
    search_result_data = search_web(search_query, topic="news", days=3)
    search_text = search_result_data["text"]
    
    if not search_text:
        print("No search results found.")
        return

    # Load existing topics to avoid duplicates
    created_topics = load_json(TOPICS_FILE)
    if not isinstance(created_topics, list):
        created_topics = []
    
    existing_titles = {t.get("title") for t in created_topics}
    existing_summaries = [t.get("title") for t in created_topics] # Simplified context for LLM

    # 2. Generate potential topics via LLM with Ranking
    print("Analyzing hotspots and generating topics...")
    prompt = f"""
    Based on the following news search results, identify 3 potential events suitable for a prediction market.
    
    Search Results:
    {search_text}
    
    Existing Topics (Do not duplicate):
    {json.dumps(existing_summaries)}
    
    Requirements:
    1. The event must have a clear outcome resolvable within the next 2 weeks (before {(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')}).
    2. Generate 2 distinct prediction market titles for each event.
    3. Titles should be in the format "Will X happen by [Date]?" or similar.
    4. Rank the events by "suitability" (controversy, public interest, clarity of resolution).
    
    Output strictly in JSON format:
    [
      {{
        "rank": 1,
        "event_summary": "Brief summary",
        "titles": ["Title 1", "Title 2"],
        "reasoning": "Why this is a good topic"
      }},
      ...
    ]
    """
    
    llm_response = call_llm([{"role": "user", "content": prompt}])
    if not llm_response:
        print("Failed to generate topics from LLM.")
        return

    try:
        candidates = json.loads(clean_json_block(llm_response))
    except json.JSONDecodeError:
        print(f"Failed to parse LLM response: {llm_response}")
        return

    best_topic = None
    
    # Select the best valid candidate
    # Candidates are already ranked by LLM
    for cand in candidates:
        for title in cand["titles"]:
            if title in existing_titles:
                print(f"Skipping duplicate: {title}")
                continue
            
            best_topic = {
                "title": title,
                "summary": cand["event_summary"],
                "reasoning": cand.get("reasoning", "")
            }
            break
        if best_topic:
            break
    
    if not best_topic:
        print("No suitable new topics found (all duplicates or none generated).")
        return

    print(f"Selected topic: {best_topic['title']}")
    print(f"Reasoning: {best_topic['reasoning']}")

    # 3. Generate details
    print("Generating market details...")
    prompt_details = f"""
    For the prediction market topic: "{best_topic['title']}"
    Event Summary: {best_topic['summary']}
    
    Tasks:
    1. Write a clear, neutral description explaining the context, current status, and resolution criteria.
    2. Provide 2 mutually exclusive options (e.g., "Yes", "No").
    3. Estimate initial probabilities for these options (integers summing to 100).
    4. Suggest a specific image search query for Tavily that returns a relevant image. Use format: "site: wikipedia.org [subject]" or "[company name] logo official" or "[event name] photo news". IMPORTANT: Use queries that return high-quality images from reliable sources.
    
    Output strictly in JSON format:
    {{
      "description": "...",
      "options": ["Option1", "Option2"],
      "probabilities": [50, 50],
      "image_search_query": "..."
    }}
    """
    
    details_resp = call_llm([{"role": "user", "content": prompt_details}])
    if not details_resp:
        print("Failed to generate details.")
        return

    try:
        details = json.loads(clean_json_block(details_resp))
    except json.JSONDecodeError:
        print("Failed to parse details JSON.")
        return

    # 4. Search for image
    image_query = details.get('image_search_query', best_topic['title'])
    print(f"Searching for image using query: {image_query}...")
    image_url = search_image(image_query)
    
    if image_url:
        print(f"Found image URL: {image_url}")
    else:
        print("No image found. Using default placeholder if needed.")

    # 5. Confirm via Slack
    msg = (
        f"*New Prediction Market Proposal*\n"
        f"*Title:* {best_topic['title']}\n"
        f"*Description:* {details['description']}\n"
        f"*Options:* {', '.join(details['options'])} (Probs: {details['probabilities']})\n"
        f"*Image:* {image_url or 'None'}\n"
        f"Waiting for confirmation..."
    )
    send_slack_message(msg, dry_run=dry_run)
    
    print("\n" + "="*40)
    print(msg)
    print("="*40 + "\n")
    
    # 6. Confirmation
    if args.yes:
        confirm = "y"
    elif dry_run:
        confirm = "y"
        print("[DRY-RUN] Auto-confirming.")
    else:
        confirm = input("Create this market? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Cancelled.")
        send_slack_message("Market creation cancelled.", dry_run=dry_run)
        return

    if dry_run:
        print("[DRY-RUN] Would create market now.")
        # Simulate ID
        market_id = "mock-market-id-123"
    else:
        # Create market
        client = SeesawClient()
        end_time = (datetime.utcnow() + timedelta(days=14)).isoformat() + "Z"
        
        try:
            resp = client.create_market(
                title=best_topic['title'],
                options=details['options'],
                end_time=end_time,
                description=details['description'],
                initial_probabilities=details['probabilities'],
                image_urls=[image_url] if image_url else None
            )
            market_id = resp.get('id', 'unknown')
        except Exception as e:
            err_msg = f"Failed to create market: {str(e)}"
            print(err_msg)
            send_slack_message(err_msg)
            return

    print(f"Market created successfully: {market_id}")
    
    if not dry_run:
        # Record locally
        created_topics.append({
            "title": best_topic['title'],
            "id": market_id,
            "created_at": datetime.now().isoformat()
        })
        save_json(TOPICS_FILE, created_topics)
        
        send_slack_message(f"Market created successfully! ID: {market_id}")
    else:
        print("[DRY-RUN] Would record market to local DB.")

if __name__ == "__main__":
    main()
