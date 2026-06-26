#!/usr/bin/env python3
"""
Fetch skills from Xfyun SkillHub using browser automation.
"""

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

DATA_DIR = Path.home() / ".openclaw" / "skill-rank"
DB_PATH = DATA_DIR / "rankings.db"


def fetch_skills_from_browser():
    """Use browser to fetch skills from SkillHub."""
    print("Fetching skills from Xfyun SkillHub via browser...")
    
    # JavaScript to extract skills from current page
    js_code = '''
    () => {
        const skills = [];
        document.querySelectorAll('[class*="card"]').forEach(card => {
            const nameEl = card.querySelector('h3');
            const descEl = card.querySelector('p');
            const stats = card.innerText.match(/v[\\d.]+\\s*(\\d+)\\s*(\\d+)\\s*([\\d.]+)/) || [];
            if (nameEl) {
                skills.push({
                    name: nameEl.innerText.trim(),
                    description: (descEl?.innerText || '').trim().substring(0, 200),
                    downloads: parseInt(stats[1]) || 0,
                    stars: parseInt(stats[2]) || 0,
                    rating: parseFloat(stats[3]) || 0
                });
            }
        });
        return JSON.stringify(skills);
    }
    '''
    
    # This would need to be called from the browser tool
    print("Please run this in the browser context")
    return []


def save_skills_to_db(skills):
    """Save skills to database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for skill in skills:
        name = skill.get("name", "")
        description = skill.get("description", "")
        downloads = skill.get("downloads", 0)
        stars = skill.get("stars", 0)
        rating = skill.get("rating", 0)
        
        # Calculate score based on downloads and stars
        import math
        popularity_score = min(math.log10(downloads + stars + 1) * 25, 100)
        
        cursor.execute('''
            INSERT OR REPLACE INTO skills (
                name, repo_url, description, stars, forks,
                total_score, last_updated, metadata
            ) VALUES (?, ?, ?, ?, 0, ?, CURRENT_TIMESTAMP, ?)
        ''', (
            name,
            f"https://skill.xfyun.cn/skill/{name}",
            description,
            stars,
            popularity_score,
            json.dumps({"downloads": downloads, "rating": rating, "source": "xfyun-skillhub"})
        ))
    
    conn.commit()
    conn.close()
    print(f"Saved {len(skills)} skills to database")


if __name__ == "__main__":
    # Skills data from browser (paste here)
    skills_json = sys.argv[1] if len(sys.argv) > 1 else "[]"
    skills = json.loads(skills_json)
    save_skills_to_db(skills)
