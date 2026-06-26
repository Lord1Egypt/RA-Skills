# repo-insights

AI-powered GitHub repository analysis by Albion AI.

POST a GitHub repo URL, get back a Claude-generated summary of open issues —
what developers are asking for, what the pain points are, where the project is headed.

## Quick Start

    export ANTHROPIC_API_KEY=your_key
    pip install -r requirements.txt
    gunicorn repo_insights:app --bind 0.0.0.0:5001

    curl -X POST http://localhost:5001/analyze \
      -H "Content-Type: application/json" \
      -d '{"repo_url": "https://github.com/owner/repo"}'
