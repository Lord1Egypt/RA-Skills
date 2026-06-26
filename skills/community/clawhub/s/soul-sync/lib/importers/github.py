#!/usr/bin/env python3
"""
GitHub Importer — Analyzes GitHub profile and repos for technical insights.
Uses GitHub REST API. Requires a GitHub token (PAT) or public profile access.
"""
import os
import sys
import json
import subprocess
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"

def get_github_data(username=None, token=None):
    """Fetch GitHub profile and repo data."""
    import urllib.request
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    def fetch(url):
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    
    # Get authenticated user or specified username
    if username:
        user = fetch(f"https://api.github.com/users/{username}")
        repos = fetch(f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated")
    else:
        user = fetch("https://api.github.com/user")
        repos = fetch("https://api.github.com/user/repos?per_page=100&sort=updated&affiliation=owner")
    
    return user, repos

def analyze(user, repos):
    """Extract personality/technical insights from GitHub data."""
    languages = Counter()
    topics = []
    total_stars = 0
    total_forks = 0
    has_blog = bool(user.get("blog"))
    
    for repo in repos:
        if repo.get("fork") and not repo.get("stargazers_count", 0) > 0:
            continue  # Skip unmodified forks
        
        lang = repo.get("language")
        if lang:
            languages[lang] += 1
        
        total_stars += repo.get("stargazers_count", 0)
        total_forks += repo.get("forks_count", 0)
        
        if repo.get("topics"):
            topics.extend(repo["topics"])
        
        # Use description as interest signal
        desc = repo.get("description", "")
        if desc:
            topics.append(desc)
    
    top_languages = [lang for lang, _ in languages.most_common(8)]
    topic_counts = Counter(topics)
    top_topics = [t for t, _ in topic_counts.most_common(15) if len(t) < 50]
    
    # Determine technical level
    repo_count = len([r for r in repos if not r.get("fork")])
    if repo_count > 50 and total_stars > 100:
        level = "advanced — prolific open source contributor"
    elif repo_count > 20:
        level = "experienced — active developer with many projects"
    elif repo_count > 5:
        level = "intermediate — builds personal projects"
    elif repo_count > 0:
        level = "beginner — getting started with public code"
    else:
        level = "unknown — no public repos"
    
    return {
        "source": "github",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": {
            "technical_skills": f"{', '.join(top_languages[:5])} developer — {level}",
            "languages": top_languages,
            "interests": top_topics[:15],
            "key_contacts": [],  # Could analyze collaborators
            "communication_style": f"{'Active open source contributor' if repo_count > 10 else 'Builds primarily private/personal projects'}",
            "profile": {
                "username": user.get("login"),
                "name": user.get("name"),
                "bio": user.get("bio"),
                "company": user.get("company"),
                "location": user.get("location"),
                "blog": user.get("blog"),
                "public_repos": repo_count,
                "followers": user.get("followers", 0),
                "total_stars": total_stars,
            }
        },
        "confidence": min(repo_count / 20, 1.0),
        "items_processed": len(repos),
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    # Try to find GitHub token
    token = os.environ.get("GITHUB_TOKEN")
    username = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not token:
        # Try git credential store
        try:
            result = subprocess.run(
                ["git", "credential", "fill"],
                input="protocol=https\nhost=github.com\n",
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if line.startswith("password="):
                    token = line.split("=", 1)[1]
        except:
            pass
    
    try:
        user, repos = get_github_data(username=username, token=token)
        result = analyze(user, repos)
        
        output_path = os.path.join(IMPORT_DIR, "github.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
