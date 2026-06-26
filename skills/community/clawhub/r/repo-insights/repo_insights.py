import flask
from flask import request, jsonify
import requests
import anthropic

app = flask.Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_repo():
    data = request.get_json()

    api_key = data.get('api_key')
    if not api_key:
        return jsonify({"error": "api_key is required"}), 400

    repo_url = data.get('repo_url')
    if not repo_url:
        return jsonify({"error": "repo_url is required"}), 400

    parts = repo_url.rstrip('/').split('/')
    owner, name = parts[-2], parts[-1]

    resp = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/issues",
        params={"state": "open", "per_page": 10},
        timeout=15
    ).json()

    if not isinstance(resp, list):
        return jsonify({"error": "GitHub API error", "detail": resp}), 500

    issue_titles = [i.get("title") for i in resp[:10]]

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"Here are open GitHub issues for {owner}/{name}:\n\n" +
                      "\n".join(f"- {t}" for t in issue_titles) +
                      "\n\nIn 2-3 sentences, summarize what developers are asking for and what the main pain points are."
        }]
    )

    return jsonify({
        "repo": f"{owner}/{name}",
        "top_issues": [{"title": t} for t in issue_titles[:5]],
        "summary": message.content[0].text
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
