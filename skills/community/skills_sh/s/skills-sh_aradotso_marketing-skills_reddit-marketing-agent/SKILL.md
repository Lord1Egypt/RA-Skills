---
name: reddit-marketing-agent
description: AI-powered Reddit marketing automation for finding high-intent conversations and generating contextual responses
triggers:
  - find Reddit threads for marketing
  - automate Reddit community engagement
  - search relevant Reddit discussions
  - generate Reddit response suggestions
  - Reddit marketing workflow automation
  - analyze subreddit opportunities
  - draft Reddit comments for growth
  - scale Reddit outreach strategy
---

# Reddit Marketing Agent

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill enables AI coding agents to help developers use the Reddit Marketing Agent, a system for researching relevant Reddit threads, generating useful responses, and turning repeatable Reddit workflows into scalable growth operations. The agent identifies high-intent conversations across subreddits, drafts context-aware responses, and supports repeatable workflows for research and optimization.

## What It Does

The Reddit Marketing Agent helps you:

- Identify high-intent conversations and opportunities across relevant subreddits
- Draft context-aware, non-spammy responses and content angles
- Support repeatable workflows for research, posting support, and iteration
- Keep strategy, logs, and source context organized for ongoing optimization
- Scale Reddit community engagement without appearing spammy

Built by the AI Automation Mastery community for systematic Reddit growth.

## Installation

Clone the repository:

```bash
git clone https://github.com/lucaswalter/reddit-marketing-agent.git
cd reddit-marketing-agent
```

Install dependencies (typically Python-based):

```bash
pip install -r requirements.txt
# or
pip install praw openai python-dotenv
```

Set up environment variables in `.env`:

```bash
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent
OPENAI_API_KEY=your_openai_api_key
```

## Configuration

Create a `config.yaml` or `config.json` file to define your target subreddits and search parameters:

```yaml
subreddits:
  - "Entrepreneur"
  - "startups"
  - "SaaS"
  - "marketing"

keywords:
  - "need automation"
  - "looking for tools"
  - "recommend software"
  - "help with marketing"

filters:
  min_upvotes: 5
  max_age_hours: 48
  exclude_patterns:
    - "spam"
    - "promotion"

response_settings:
  tone: "helpful"
  max_length: 300
  include_value_first: true
```

## Core Usage Patterns

### 1. Search for Relevant Threads

```python
import praw
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

def search_relevant_threads(subreddit_name, keywords, limit=25):
    """Search for threads matching keywords in a subreddit."""
    subreddit = reddit.subreddit(subreddit_name)
    relevant_threads = []
    
    for keyword in keywords:
        for submission in subreddit.search(keyword, time_filter='week', limit=limit):
            if submission.score >= 5:  # Filter by upvotes
                relevant_threads.append({
                    'title': submission.title,
                    'url': submission.url,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'created_utc': submission.created_utc,
                    'id': submission.id,
                    'selftext': submission.selftext
                })
    
    return relevant_threads

# Example usage
threads = search_relevant_threads('Entrepreneur', ['automation tools', 'marketing help'], limit=10)
for thread in threads:
    print(f"{thread['title']} - Score: {thread['score']}")
```

### 2. Generate Context-Aware Responses

```python
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(thread_title, thread_content, tone='helpful'):
    """Generate a contextual, non-spammy Reddit response."""
    
    prompt = f"""You are a helpful community member on Reddit. Generate a genuine, value-first response to this thread.

Thread Title: {thread_title}
Thread Content: {thread_content}

Guidelines:
- Be genuinely helpful and specific
- Provide value before any mentions
- Keep tone {tone} and conversational
- Avoid obvious promotion
- Max 250 words

Response:"""

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'system', 'content': 'You are an experienced marketer who engages authentically on Reddit.'},
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.7,
        max_tokens=400
    )
    
    return response.choices[0].message.content

# Example usage
response = generate_response(
    "Need help automating my social media",
    "I'm spending 3 hours a day on social media for my startup. Any tools or strategies?"
)
print(response)
```

### 3. Complete Workflow Script

```python
import json
from datetime import datetime

def reddit_marketing_workflow(config_path='config.json'):
    """Complete workflow: search, analyze, generate responses, log results."""
    
    # Load configuration
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    results = []
    
    for subreddit_name in config['subreddits']:
        print(f"\n🔍 Searching r/{subreddit_name}...")
        
        # Search threads
        threads = search_relevant_threads(
            subreddit_name, 
            config['keywords'],
            limit=config.get('limit', 25)
        )
        
        # Filter by criteria
        filtered_threads = [
            t for t in threads 
            if t['score'] >= config['filters']['min_upvotes']
        ]
        
        print(f"✅ Found {len(filtered_threads)} relevant threads")
        
        # Generate responses for top threads
        for thread in filtered_threads[:5]:  # Top 5
            response = generate_response(
                thread['title'],
                thread['selftext'],
                tone=config['response_settings']['tone']
            )
            
            results.append({
                'subreddit': subreddit_name,
                'thread_id': thread['id'],
                'thread_title': thread['title'],
                'thread_url': thread['url'],
                'score': thread['score'],
                'generated_response': response,
                'timestamp': datetime.now().isoformat()
            })
    
    # Save results
    output_file = f"reddit_opportunities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to {output_file}")
    return results

# Run workflow
results = reddit_marketing_workflow()
```

### 4. Sentiment and Opportunity Scoring

```python
def score_opportunity(thread):
    """Score a thread's marketing opportunity potential."""
    score = 0
    
    # Engagement metrics
    if thread['score'] > 20:
        score += 2
    if thread['num_comments'] > 10:
        score += 2
    
    # Intent signals in title/content
    high_intent_phrases = ['recommend', 'looking for', 'need help', 'suggestions', 'alternatives']
    text = (thread['title'] + ' ' + thread['selftext']).lower()
    
    for phrase in high_intent_phrases:
        if phrase in text:
            score += 3
    
    # Recency (threads less than 24 hours old)
    age_hours = (datetime.now().timestamp() - thread['created_utc']) / 3600
    if age_hours < 24:
        score += 2
    
    return score

# Example usage
threads = search_relevant_threads('SaaS', ['automation'], limit=20)
scored_threads = sorted(
    [(score_opportunity(t), t) for t in threads],
    key=lambda x: x[0],
    reverse=True
)

print("Top opportunities:")
for score, thread in scored_threads[:5]:
    print(f"Score {score}: {thread['title']}")
```

## Command Line Interface

If the project includes a CLI script:

```bash
# Search for opportunities
python reddit_agent.py search --subreddits "Entrepreneur,startups" --keywords "automation,tools"

# Generate responses for saved threads
python reddit_agent.py generate --input threads.json --output responses.json

# Run full workflow
python reddit_agent.py workflow --config config.yaml

# Analyze subreddit activity
python reddit_agent.py analyze --subreddit SaaS --days 7
```

## Data Storage and Logging

Keep track of opportunities and responses:

```python
import sqlite3

def setup_database():
    """Create SQLite database for tracking threads and responses."""
    conn = sqlite3.connect('reddit_marketing.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS threads
                 (id TEXT PRIMARY KEY,
                  subreddit TEXT,
                  title TEXT,
                  url TEXT,
                  score INTEGER,
                  opportunity_score INTEGER,
                  found_date TEXT,
                  status TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  thread_id TEXT,
                  generated_response TEXT,
                  posted BOOLEAN,
                  posted_date TEXT,
                  FOREIGN KEY(thread_id) REFERENCES threads(id))''')
    
    conn.commit()
    conn.close()

def log_thread(thread_data):
    """Log a discovered thread to database."""
    conn = sqlite3.connect('reddit_marketing.db')
    c = conn.cursor()
    
    c.execute('''INSERT OR IGNORE INTO threads 
                 (id, subreddit, title, url, score, opportunity_score, found_date, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (thread_data['id'], thread_data['subreddit'], thread_data['title'],
               thread_data['url'], thread_data['score'], thread_data['opportunity_score'],
               datetime.now().isoformat(), 'new'))
    
    conn.commit()
    conn.close()
```

## Best Practices

### Non-Spammy Engagement

```python
ENGAGEMENT_RULES = {
    'value_first': True,
    'max_daily_comments': 5,
    'wait_between_comments_minutes': 60,
    'personalize_each_response': True,
    'avoid_direct_promotion': True
}

def is_safe_to_engage(thread):
    """Check if engagement is appropriate."""
    # Don't engage if already commented
    # Check rate limits
    # Verify thread age and activity
    # Ensure genuine opportunity
    return True  # Implement your logic
```

## Troubleshooting

**Reddit API Rate Limits:**
- PRAW handles most rate limiting automatically
- Add delays between requests: `time.sleep(2)`
- Use `reddit.auth.limits` to check remaining requests

**Authentication Errors:**
- Verify `.env` file contains correct credentials
- Ensure Reddit app is configured as "script" type
- Check that user agent string is descriptive and unique

**Empty Search Results:**
- Broaden keyword search terms
- Increase time filter (e.g., 'month' instead of 'week')
- Verify subreddit names are correct
- Check if subreddits are private or restricted

**OpenAI API Errors:**
- Verify `OPENAI_API_KEY` is set correctly
- Check API quota and billing status
- Reduce `max_tokens` if hitting limits
- Add retry logic with exponential backoff

## Advanced Features

### Multi-Subreddit Monitoring

```python
import schedule
import time

def monitor_subreddits():
    """Continuously monitor subreddits for new opportunities."""
    config = load_config('config.json')
    results = reddit_marketing_workflow(config)
    print(f"Found {len(results)} new opportunities")

# Schedule monitoring
schedule.every(2).hours.do(monitor_subreddits)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Response Quality Validation

```python
def validate_response(response_text):
    """Ensure generated response meets quality standards."""
    checks = {
        'not_too_short': len(response_text) > 50,
        'not_too_long': len(response_text) < 500,
        'no_spam_words': not any(word in response_text.lower() for word in ['buy now', 'click here', 'limited offer']),
        'has_value': any(word in response_text.lower() for word in ['try', 'suggest', 'recommend', 'help', 'consider'])
    }
    
    return all(checks.values())
```

This skill provides comprehensive guidance for using the Reddit Marketing Agent to identify opportunities, generate contextual responses, and scale Reddit community engagement systematically.
