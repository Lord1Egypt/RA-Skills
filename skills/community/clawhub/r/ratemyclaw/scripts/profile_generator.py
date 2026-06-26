"""
RateMyClaw Profile Generator
=============================
Scans an OpenClaw workspace and generates a structured work profile
using only tags from the fixed taxonomy. No free-form text leaves the machine.

Usage:
    python3 profile_generator.py [workspace_path]
    
Defaults to ~/.openclaw/workspace if no path given.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

# Load taxonomy
SCRIPT_DIR = Path(__file__).parent.parent
with open(SCRIPT_DIR / "references" / "taxonomy.json") as f:
    TAXONOMY = json.load(f)

VALID_DOMAINS = set(TAXONOMY["domains"])
VALID_TOOLS = set(TAXONOMY["tools"])
VALID_PATTERNS = set(TAXONOMY["patterns"])
VALID_INTEGRATIONS = set(TAXONOMY["integrations"])
VALID_AUTOMATION = set(TAXONOMY["automation_levels"])
VALID_STAGES = set(TAXONOMY["stages"])


# === Detection Rules ===
# Each rule maps file/content signals to taxonomy tags

DOMAIN_SIGNALS = {
    # Keywords in file content → domain tags
    "quantitative-trading": ["trading", "trader", "backtest", "market-making", "pnl", "roi"],
    "prediction-markets": ["polymarket", "kalshi", "prediction market", "binary option"],
    "crypto": ["bitcoin", "btc", "ethereum", "eth", "defi", "blockchain", "binance"],
    "algorithmic-trading": ["algo trad", "signal generation", "alpha", "strategy"],
    "financial-modeling": ["financial model", "valuation", "dcf", "monte carlo"],
    "web-development": ["react", "next.js", "nextjs", "vue", "angular", "frontend", "fullstack"],
    "backend-development": ["api", "rest api", "graphql", "microservice", "backend"],
    "mobile-development": ["ios", "android", "react native", "swift", "flutter", "xcode"],
    "devops": ["terraform", "kubernetes", "k8s", "docker", "ci/cd", "pipeline"],
    "data-analysis": ["data analysis", "pandas", "dataframe", "visualization", "dashboard"],
    "data-science": ["data science", "statistical", "hypothesis", "experiment"],
    "machine-learning": ["machine learning", "ml", "classifier", "gradient boosting", "neural net", "model training", "pytorch", "tensorflow"],
    "content-creation": ["blog", "article", "content", "writing", "publish"],
    "newsletter": ["newsletter", "beehiiv", "substack", "subscriber"],
    "social-media": ["social media", "twitter", "instagram", "tiktok", "engagement"],
    "productivity": ["gtd", "getting things done", "productivity", "habit"],
    "task-management": ["todoist", "asana", "jira", "task", "kanban"],
    "project-management": ["project manag", "sprint", "agile", "scrum", "standup"],
    "email-management": ["email triage", "inbox", "imap", "email processing"],
    "entrepreneurship": ["startup", "mvp", "business idea", "entrepreneur", "saas"],
    "smart-home": ["home assistant", "homekit", "zigbee", "mqtt", "smart home"],
    "cybersecurity": ["security", "vulnerability", "penetration", "exploit", "nmap"],
    "e-commerce": ["shopify", "stripe", "e-commerce", "ecommerce", "cart"],
    "education": ["course", "curriculum", "teaching", "student", "lesson"],
    "design": ["figma", "design system", "ui/ux", "wireframe", "prototype"],
    "database-management": ["database", "migration", "schema", "sql query", "orm"],
    "web-scraping": ["scraping", "scrape", "crawl", "beautifulsoup", "puppeteer"],
    "browser-automation": ["browser automat", "playwright", "selenium", "puppeteer", "headless"],
    "pdf-processing": ["pdf", "ocr", "document extract"],
    "image-generation": ["image generat", "dall-e", "midjourney", "stable diffusion"],
    "video-production": ["video", "ffmpeg", "editing", "youtube"],
    "audio-processing": ["audio", "whisper", "transcri", "tts", "speech"],
    "translation": ["translat", "locali", "i18n", "multilingual"],
    "documentation": ["documentat", "docs", "technical writing", "readme"],
    "backup-recovery": ["backup", "restore", "disaster recovery"],
    "api-development": ["api develop", "rest api", "endpoint", "swagger", "openapi"],
    "rag": ["rag", "retrieval augmented", "vector search", "embeddings", "knowledge base"],
    "crm": ["crm", "customer relat", "salesforce", "hubspot"],
    "payments": ["payment", "stripe", "invoice", "billing"],
    "testing-qa": ["test", "qa", "quality assur", "pytest", "jest", "unittest"],
}

TOOL_SIGNALS = {
    # File extensions and content patterns → tool tags
    "python": [".py", "python", "pip install"],
    "javascript": [".js", "javascript", "npm"],
    "typescript": [".ts", ".tsx", "typescript"],
    "go": [".go", "golang"],
    "rust": [".rs", "cargo"],
    "swift": [".swift", "xcode"],
    "bash": [".sh", "#!/bin/bash", "bash"],
    "sql": [".sql", "SELECT ", "CREATE TABLE"],
    "sqlite": ["sqlite", ".db"],
    "postgres": ["postgres", "psql", "pg_"],
    "redis": ["redis"],
    "mongodb": ["mongodb", "mongoose"],
    "docker": ["docker", "Dockerfile", "docker-compose"],
    "kubernetes": ["kubernetes", "kubectl", "k8s"],
    "terraform": ["terraform", ".tf"],
    "git": [".git", "git commit", "git push"],
    "jupyter": [".ipynb", "jupyter"],
    "pandas": ["pandas", "DataFrame"],
    "pytorch": ["pytorch", "torch."],
    "react": ["react", "jsx", "useState"],
    "next-js": ["next.js", "nextjs", "next/"],
    "markdown": [".md", "markdown"],
    "figma": ["figma"],
    "canva": ["canva"],
    "supabase": ["supabase"],
    "firebase": ["firebase", "firestore"],
    "openai-api": ["openai", "gpt-4", "gpt-3", "dall-e"],
    "anthropic-api": ["anthropic", "claude"],
    "langchain": ["langchain"],
    "llamaindex": ["llamaindex", "llama_index"],
    "selenium": ["selenium", "webdriver"],
    "playwright": ["playwright"],
    "puppeteer": ["puppeteer"],
}

PATTERN_SIGNALS = {
    "backtesting": ["backtest", "historical data", "simulated"],
    "live-monitoring": ["monitor", "health check", "uptime", "process running"],
    "alerting": ["alert", "notify", "notification", "escalat"],
    "regime-detection": ["regime", "market regime", "classifier"],
    "signal-generation": ["signal", "indicator", "feature engineering"],
    "risk-management": ["risk", "drawdown", "position size", "kelly"],
    "market-making": ["market mak", "bid ask", "spread", "quote"],
    "ci-cd": ["ci/cd", "github actions", "pipeline", "deploy"],
    "automated-testing": ["test", "pytest", "jest", "unittest"],
    "code-review": ["code review", "pull request", "pr review"],
    "deployment": ["deploy", "production", "staging"],
    "data-pipeline": ["pipeline", "etl", "data flow", "ingestion"],
    "statistical-analysis": ["statistical", "regression", "correlation", "p-value"],
    "time-series-analysis": ["time series", "autocorrelation", "stationarity", "arima"],
    "email-triage": ["email triage", "inbox processing", "email categori"],
    "gtd-workflow": ["gtd", "getting things done", "inbox zero", "weekly review"],
    "dashboard-building": ["dashboard", "chart", "visualization"],
    "reporting": ["report", "summary", "digest"],
    "memory-journaling": ["memory", "daily note", "journal", "MEMORY.md"],
    "automated-reporting": ["cron", "scheduled report", "auto report"],
    "analytics": ["analytics", "metrics", "tracking"],
    "writing": ["writing", "draft", "article", "blog post"],
    "publishing": ["publish", "deploy content", "post"],
    "web-scraping": ["scrape", "crawl", "beautifulsoup"],
    "browser-automation": ["playwright", "selenium", "puppeteer", "headless browser"],
    "pdf-extraction": ["pdf extract", "ocr", "document pars"],
    "image-generation": ["image generat", "dall-e", "stable diffusion"],
    "rag-retrieval": ["rag", "retrieval", "vector search", "knowledge base"],
    "webhook-handling": ["webhook", "callback url", "event hook"],
    "backup-restore": ["backup", "snapshot", "restore"],
    "file-organization": ["file organiz", "folder structure", "cleanup"],
    "api-testing": ["api test", "postman", "httpie", "curl test"],
    "translation": ["translat", "locali", "i18n"],
    "documentation-generation": ["docstring", "documentation generat", "auto-doc"],
    "log-analysis": ["log analys", "log pars", "error track"],
}

INTEGRATION_SIGNALS = {
    "discord": ["discord"],
    "slack": ["slack"],
    "telegram": ["telegram"],
    "whatsapp": ["whatsapp"],
    "email-imap": ["imap", "email"],
    "gmail": ["gmail"],
    "todoist": ["todoist"],
    "asana": ["asana"],
    "jira": ["jira"],
    "notion": ["notion"],
    "trello": ["trello"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "vercel": ["vercel"],
    "aws": ["aws", "s3", "ec2", "lambda"],
    "stripe": ["stripe"],
    "twitter": ["twitter", "tweet"],
    "linkedin": ["linkedin"],
    "beehiiv": ["beehiiv"],
    "substack": ["substack"],
    "wordpress": ["wordpress"],
    "ssh-remote": ["ssh ", "ssh-"],
    "google-calendar": ["google calendar", "gcal"],
    "grafana": ["grafana"],
    "datadog": ["datadog"],
    "zoom": ["zoom"],
    "google-sheets": ["google sheets", "gsheet"],
    "openai": ["openai"],
    "anthropic": ["anthropic", "claude"],
    "supabase": ["supabase"],
    "firebase": ["firebase"],
    "zapier": ["zapier"],
    "n8n": ["n8n"],
    "twilio": ["twilio"],
    "sendgrid": ["sendgrid"],
    "mailchimp": ["mailchimp"],
    "dropbox": ["dropbox"],
    "google-drive": ["google drive", "gdrive"],
    "onedrive": ["onedrive"],
    "confluence": ["confluence"],
}


def scan_workspace(workspace_path: str) -> dict:
    """Scan workspace and return raw signals."""
    ws = Path(workspace_path)
    
    signals = {
        "files": [],          # all filenames
        "extensions": [],     # file extensions
        "text_content": "",   # concatenated text from key files (limited)
        "secrets": [],        # names of secret files (not contents!)
        "skills": [],         # installed skill names
        "memory_files": 0,    # count of memory files
        "research_docs": 0,   # count of research docs  
        "scripts": 0,         # count of scripts
        "has_soul": False,
        "has_memory": False,
        "has_heartbeat": False,
        "has_work_status": False,
        "has_cron": False,
        "recent_activity_days": 0,  # days since last file modification
    }
    
    # Walk workspace (limited depth)
    key_files = ["SOUL.md", "MEMORY.md", "USER.md", "TOOLS.md", "AGENTS.md", 
                 "HEARTBEAT.md", "WORK_STATUS.md", "README.md"]
    
    for kf in key_files:
        p = ws / kf
        if p.exists():
            if kf == "SOUL.md": signals["has_soul"] = True
            if kf == "MEMORY.md": signals["has_memory"] = True
            if kf == "HEARTBEAT.md": signals["has_heartbeat"] = True
            if kf == "WORK_STATUS.md": signals["has_work_status"] = True
            
            try:
                content = p.read_text(errors="ignore")[:5000]  # limit per file
                signals["text_content"] += f"\n{content}"
            except:
                pass
    
    # Scan directories
    for subdir in ["research", "scripts", "skills", "memory", ".secrets", "ideas"]:
        d = ws / subdir
        if d.exists() and d.is_dir():
            try:
                items = list(d.iterdir())
                if subdir == "research":
                    signals["research_docs"] = len([f for f in items if f.suffix == ".md"])
                elif subdir == "scripts":
                    signals["scripts"] = len(items)
                elif subdir == "skills":
                    signals["skills"] = [f.name for f in items if f.is_dir()]
                elif subdir == "memory":
                    md_files = [f for f in items if f.suffix == ".md" and f.name != "TEMPLATE.md"]
                    signals["memory_files"] = len(md_files)
                    # Check recency
                    for mf in md_files:
                        try:
                            date_str = mf.stem  # e.g., "2026-03-29"
                            file_date = datetime.strptime(date_str, "%Y-%m-%d")
                            age = (datetime.now() - file_date).days
                            signals["recent_activity_days"] = max(signals["recent_activity_days"], 0)
                            if age < signals.get("_newest_age", 999):
                                signals["_newest_age"] = age
                        except:
                            pass
                elif subdir == ".secrets":
                    signals["secrets"] = [f.name for f in items]
                    
                # Read some files for content signals
                for f in items[:10]:
                    if f.suffix in [".md", ".py", ".sh", ".json", ".yaml", ".yml"]:
                        try:
                            content = f.read_text(errors="ignore")[:3000]
                            signals["text_content"] += f"\n{content}"
                        except:
                            pass
            except:
                pass
    
    # Collect all file extensions
    try:
        for item in ws.rglob("*"):
            if item.is_file() and not any(p in str(item) for p in [".git", "__pycache__", "node_modules"]):
                signals["files"].append(item.name)
                if item.suffix:
                    signals["extensions"].append(item.suffix)
    except:
        pass
    
    # Limit text content to prevent excessive processing
    signals["text_content"] = signals["text_content"][:50000]
    
    # Detect model configuration from OpenClaw config
    signals["models"] = _detect_models(ws)
    
    return signals


def _detect_models(ws: Path) -> dict:
    """Extract model configuration from OpenClaw config.
    
    Only captures model name strings (e.g., "anthropic/claude-sonnet-4-6").
    No API keys, tokens, or other secrets are read.
    """
    models = {
        "default_model": None,
        "fallback_models": [],
        "heartbeat_model": None,
    }
    
    # OpenClaw config is typically at ~/.openclaw/openclaw.json
    config_path = ws.parent / "openclaw.json"
    if not config_path.exists():
        # Try common alternative locations
        for alt in [ws / "openclaw.json", Path.home() / ".openclaw" / "openclaw.json"]:
            if alt.exists():
                config_path = alt
                break
    
    if not config_path.exists():
        return models
    
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        # Extract default model
        agents = config.get("agents", {})
        defaults = agents.get("defaults", {})
        model_config = defaults.get("model", {})
        
        if isinstance(model_config, str):
            models["default_model"] = model_config
        elif isinstance(model_config, dict):
            models["default_model"] = model_config.get("primary")
            models["fallback_models"] = model_config.get("fallbacks", [])
        
        # Check agent list for heartbeat model
        agent_list = agents.get("list", [])
        for agent in agent_list:
            hb = agent.get("heartbeat", {})
            if isinstance(hb, dict) and hb.get("model"):
                models["heartbeat_model"] = hb["model"]
                break
        
    except (json.JSONDecodeError, KeyError, TypeError):
        pass
    
    return models


def match_tags(text: str, signal_map: dict, valid_set: set, 
               min_mentions: int = 3, max_tags: int = 6) -> list:
    """Match text content against signal patterns, return valid taxonomy tags.
    
    Fixes for over-tagging:
    - min_mentions: tag must appear at least this many times to qualify
    - max_tags: hard cap per category (forces picking strongest signals)
    - Scores are normalized by pattern count to avoid bias toward tags with more patterns
    """
    text_lower = text.lower()
    matched = {}
    
    for tag, patterns in signal_map.items():
        if tag not in valid_set:
            continue
        total_count = 0
        patterns_hit = 0
        for pattern in patterns:
            count = text_lower.count(pattern.lower())
            if count > 0:
                total_count += count
                patterns_hit += 1
        
        # Must meet minimum mention threshold
        if total_count >= min_mentions:
            # Score: total mentions * pattern diversity bonus
            # Having 2 different patterns match is stronger than 1 pattern matching 6 times
            diversity_bonus = 1.0 + (patterns_hit - 1) * 0.5 if patterns_hit > 1 else 1.0
            matched[tag] = total_count * diversity_bonus
    
    # Sort by score, cap at max_tags
    sorted_tags = sorted(matched.items(), key=lambda x: -x[1])
    return [tag for tag, score in sorted_tags[:max_tags]]


def determine_automation_level(signals: dict) -> str:
    """Determine automation level from signals."""
    score = 0
    if signals["has_heartbeat"]: score += 2
    if signals["has_cron"] or "cron" in signals["text_content"].lower(): score += 2
    if any("alert" in s.lower() for s in signals.get("skills", [])): score += 1
    if "automated" in signals["text_content"].lower(): score += 1
    if signals["scripts"] > 10: score += 1
    
    if score >= 5: return "fully-autonomous"
    if score >= 3: return "high"
    if score >= 2: return "moderate"
    if score >= 1: return "light"
    return "manual"


def determine_stage(signals: dict) -> str:
    """Determine project stage from signals."""
    text = signals["text_content"].lower()
    
    if "deployed" in text and ("iterating" in text or "improving" in text):
        return "iterating"
    if "deployed" in text or "live" in text or "production" in text:
        return "deployed"
    if "testing" in text or "shadow mode" in text or "validat" in text:
        return "testing"
    if "building" in text or "implementing" in text:
        return "building"
    if "exploring" in text or "research" in text and signals["research_docs"] > signals["scripts"]:
        return "exploring"
    return "building"


def calculate_maturity_score(signals: dict) -> dict:
    """Calculate workspace maturity metrics."""
    return {
        "memory_files": signals["memory_files"],
        "research_docs": signals["research_docs"],
        "scripts": signals["scripts"],
        "custom_skills": len(signals["skills"]),
        "secrets_configured": len(signals["secrets"]),
        "has_soul": signals["has_soul"],
        "has_memory": signals["has_memory"],
        "has_heartbeat": signals["has_heartbeat"],
        "has_work_status": signals["has_work_status"]
    }


def generate_profile(workspace_path: str, max_tags: int = 12) -> dict:
    """Generate a complete work profile from workspace scan."""
    
    signals = scan_workspace(workspace_path)
    text = signals["text_content"]
    
    # Match against taxonomy (with frequency thresholds to prevent over-tagging)
    domains = match_tags(text, DOMAIN_SIGNALS, VALID_DOMAINS, min_mentions=3, max_tags=6)
    tools = match_tags(text, TOOL_SIGNALS, VALID_TOOLS, min_mentions=2, max_tags=8)
    patterns = match_tags(text, PATTERN_SIGNALS, VALID_PATTERNS, min_mentions=3, max_tags=8)
    integrations = match_tags(text, INTEGRATION_SIGNALS, VALID_INTEGRATIONS, min_mentions=2, max_tags=8)
    
    # Also check secrets for integration signals
    secret_names = " ".join(signals["secrets"]).lower()
    for integration, keywords in INTEGRATION_SIGNALS.items():
        if integration not in integrations:
            for kw in keywords:
                if kw.lower() in secret_names:
                    integrations.append(integration)
                    break
    
    # Also check skill names
    skill_text = " ".join(signals["skills"]).lower()
    for integration, keywords in INTEGRATION_SIGNALS.items():
        if integration not in integrations:
            for kw in keywords:
                if kw.lower() in skill_text:
                    integrations.append(integration)
                    break
    
    automation = determine_automation_level(signals)
    stage = determine_stage(signals)
    maturity = calculate_maturity_score(signals)
    
    profile = {
        "schema_version": "0.3.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "domains": domains[:max_tags],
        "tools": tools[:max_tags],
        "patterns": patterns[:max_tags],
        "integrations": list(dict.fromkeys(integrations))[:max_tags],  # dedupe, preserve order
        "skills_installed": signals["skills"],  # ClawHub skill slugs
        "automation_level": automation,
        "stage": stage,
        "maturity": maturity,
        "models": signals.get("models", {}),
    }
    
    return profile


def profile_to_embedding_text(profile: dict) -> str:
    """Convert profile to text suitable for embedding."""
    parts = []
    for key in ["domains", "tools", "patterns", "integrations"]:
        if profile.get(key):
            parts.append(f"{key}: {', '.join(profile[key])}")
    parts.append(f"automation: {profile.get('automation_level', 'unknown')}")
    parts.append(f"stage: {profile.get('stage', 'unknown')}")
    return ". ".join(parts)


def print_profile(profile: dict):
    """Pretty-print a profile."""
    print("\n" + "=" * 60)
    print("  AGENTGRAPH WORK PROFILE")
    print("=" * 60)
    
    print(f"\n📊 Generated: {profile['generated_at']}")
    print(f"📋 Schema: v{profile['schema_version']}")
    
    print(f"\n🌐 Domains ({len(profile['domains'])}):")
    for d in profile['domains']:
        print(f"   • {d}")
    
    print(f"\n🔧 Tools ({len(profile['tools'])}):")
    for t in profile['tools']:
        print(f"   • {t}")
    
    print(f"\n⚙️  Patterns ({len(profile['patterns'])}):")
    for p in profile['patterns']:
        print(f"   • {p}")
    
    print(f"\n🔌 Integrations ({len(profile['integrations'])}):")
    for i in profile['integrations']:
        print(f"   • {i}")
    
    print(f"\n🤖 Automation: {profile['automation_level']}")
    print(f"📍 Stage: {profile['stage']}")
    
    print(f"\n📈 Maturity:")
    m = profile['maturity']
    print(f"   Memory files:    {m['memory_files']}")
    print(f"   Research docs:   {m['research_docs']}")
    print(f"   Scripts:         {m['scripts']}")
    print(f"   Custom skills:   {m['custom_skills']}")
    print(f"   Secrets:         {m['secrets_configured']}")
    print(f"   Has SOUL.md:     {'✅' if m['has_soul'] else '❌'}")
    print(f"   Has MEMORY.md:   {'✅' if m['has_memory'] else '❌'}")
    print(f"   Has HEARTBEAT:   {'✅' if m['has_heartbeat'] else '❌'}")
    print(f"   Has WORK_STATUS: {'✅' if m['has_work_status'] else '❌'}")
    
    models = profile.get('models', {})
    if models.get('default_model'):
        print(f"\n🧠 Models:")
        print(f"   Default:    {models['default_model']}")
        if models.get('fallback_models'):
            print(f"   Fallbacks:  {', '.join(models['fallback_models'])}")
        if models.get('heartbeat_model'):
            print(f"   Heartbeat:  {models['heartbeat_model']}")
    
    print(f"\n📝 Embedding text:")
    print(f"   {profile_to_embedding_text(profile)}")
    print()


if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.openclaw/workspace")
    
    print(f"Scanning workspace: {workspace}")
    profile = generate_profile(workspace)
    print_profile(profile)
    
    # Save profile
    out_path = Path(__file__).parent / "generated_profile.json"
    with open(out_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"Profile saved to: {out_path}")
