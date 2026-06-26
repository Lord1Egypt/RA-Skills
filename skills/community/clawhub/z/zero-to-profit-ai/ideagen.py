import json
from random import choice

def generate_business_ideas(user_skills, max_ideas=5):
    base_ideas = [
        {"name": "Local Lead Generator", "expected_gain": 200, "cost": 10},
        {"name": "Freelance Service Automation", "expected_gain": 500, "cost": 30},
        {"name": "Digital Product Launch", "expected_gain": 1000, "cost": 50},
        {"name": "Newsletter Monetization", "expected_gain": 300, "cost": 20},
        {"name": "AI-Driven Consulting", "expected_gain": 800, "cost": 40}
    ]
    # Adapt ideas based on user_skills
    ideas = [{"name": f"{idea['name']} ({user_skills})", "expected_gain": idea["expected_gain"], "cost": idea["cost"]} 
             for idea in base_ideas]
    return ideas[:max_ideas]

if __name__ == "__main__":
    user_skills = "copywriting, marketing"
    print(json.dumps(generate_business_ideas(user_skills), indent=2))
