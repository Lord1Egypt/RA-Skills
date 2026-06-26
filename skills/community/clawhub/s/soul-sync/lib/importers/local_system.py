#!/usr/bin/env python3
"""
Local System Importer — Analyzes local machine data for technical profile and habits.
No network access needed. Everything is already on the machine.

Scans: shell history, browser bookmarks, installed apps, git repos, SSH config.
This is the most privacy-sensitive importer — all data stays 100% local.
"""
import os
import sys
import json
import glob
import platform
import sqlite3
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

def analyze_shell_history():
    """Analyze bash/zsh history for technical profile."""
    history_files = [
        os.path.expanduser("~/.bash_history"),
        os.path.expanduser("~/.zsh_history"),
        os.path.expanduser("~/.local/share/fish/fish_history"),
    ]
    
    commands = Counter()
    total_lines = 0
    
    for hfile in history_files:
        if not os.path.exists(hfile):
            continue
        try:
            with open(hfile, "r", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    # zsh history format: : timestamp:0;command
                    if line.startswith(":"):
                        line = line.split(";", 1)[-1] if ";" in line else line
                    if not line or line.startswith("#"):
                        continue
                    
                    # Extract base command
                    cmd = line.split()[0] if line.split() else ""
                    cmd = cmd.split("/")[-1]  # Strip path
                    if cmd and len(cmd) < 30:
                        commands[cmd] += 1
                    total_lines += 1
        except:
            continue
    
    return commands, total_lines

def analyze_git_repos():
    """Find and analyze local git repos."""
    home = os.path.expanduser("~")
    repos = []
    languages = Counter()
    
    # Common project directories
    search_dirs = [
        os.path.join(home, "Projects"),
        os.path.join(home, "projects"),
        os.path.join(home, "Code"),
        os.path.join(home, "code"),
        os.path.join(home, "dev"),
        os.path.join(home, "src"),
        os.path.join(home, "workspace"),
        os.path.join(home, ".openclaw", "workspace"),
    ]
    
    for search_dir in search_dirs:
        if not os.path.isdir(search_dir):
            continue
        for d in os.listdir(search_dir):
            full = os.path.join(search_dir, d)
            if os.path.isdir(os.path.join(full, ".git")):
                repos.append(d)
                # Quick language detection
                for ext, lang in [
                    (".py", "Python"), (".js", "JavaScript"), (".ts", "TypeScript"),
                    (".go", "Go"), (".rs", "Rust"), (".rb", "Ruby"), (".java", "Java"),
                    (".cpp", "C++"), (".c", "C"), (".cs", "C#"), (".swift", "Swift"),
                    (".kt", "Kotlin"), (".php", "PHP"), (".sh", "Shell"),
                ]:
                    if glob.glob(os.path.join(full, f"*{ext}")) or glob.glob(os.path.join(full, f"**/*{ext}"), recursive=False):
                        languages[lang] += 1
    
    return repos, languages

def analyze_browser_bookmarks():
    """Extract interests from browser bookmarks."""
    bookmarks = []
    
    # Chrome/Chromium
    chrome_paths = [
        os.path.expanduser("~/.config/google-chrome/Default/Bookmarks"),
        os.path.expanduser("~/.config/chromium/Default/Bookmarks"),
        os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Bookmarks"),
    ]
    
    for bpath in chrome_paths:
        if os.path.exists(bpath):
            try:
                with open(bpath, "r") as f:
                    data = json.load(f)
                
                def walk(node):
                    if isinstance(node, dict):
                        if node.get("type") == "url":
                            bookmarks.append({
                                "name": node.get("name", ""),
                                "url": node.get("url", ""),
                            })
                        for child in node.get("children", []):
                            walk(child)
                
                for root in data.get("roots", {}).values():
                    walk(root)
            except:
                pass
    
    # Firefox
    firefox_paths = glob.glob(os.path.expanduser("~/.mozilla/firefox/*/places.sqlite"))
    for fpath in firefox_paths[:1]:
        try:
            conn = sqlite3.connect(f"file:{fpath}?mode=ro", uri=True)
            cursor = conn.execute(
                "SELECT b.title, p.url FROM moz_bookmarks b JOIN moz_places p ON b.fk = p.id WHERE b.title IS NOT NULL AND b.title != '' LIMIT 200"
            )
            for title, url in cursor:
                bookmarks.append({"name": title, "url": url})
            conn.close()
        except:
            pass
    
    return bookmarks

def analyze_installed_apps():
    """Detect notable installed applications."""
    notable_apps = {
        # Development
        "code": "VS Code", "vim": "Vim", "nvim": "Neovim", "emacs": "Emacs",
        "docker": "Docker", "kubectl": "Kubernetes", "terraform": "Terraform",
        "node": "Node.js", "python3": "Python", "go": "Go", "rustc": "Rust",
        "java": "Java", "ruby": "Ruby", "php": "PHP", "swift": "Swift",
        # Tools
        "git": "Git", "tmux": "tmux", "ffmpeg": "FFmpeg", "ollama": "Ollama",
        "btop": "btop", "htop": "htop",
        # Apps
        "blender": "Blender", "gimp": "GIMP", "inkscape": "Inkscape",
        "obs": "OBS Studio", "vlc": "VLC",
        "signal-cli": "Signal", "telegram-cli": "Telegram",
        # Bitcoin/crypto
        "bitcoin-cli": "Bitcoin Core", "lncli": "LND", "lightning-cli": "CLN",
    }
    
    found = []
    for cmd, name in notable_apps.items():
        for path_dir in os.environ.get("PATH", "").split(":"):
            if os.path.exists(os.path.join(path_dir, cmd)):
                found.append(name)
                break
    
    return found

def analyze_ssh_config():
    """Check SSH config for infrastructure hints."""
    ssh_config = os.path.expanduser("~/.ssh/config")
    hosts = []
    
    if os.path.exists(ssh_config):
        try:
            with open(ssh_config, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.lower().startswith("host ") and "*" not in line:
                        host = line.split(None, 1)[1]
                        hosts.append(host)
        except:
            pass
    
    return hosts

def import_local():
    """Main local system analysis."""
    shell_commands, history_size = analyze_shell_history()
    repos, languages = analyze_git_repos()
    bookmarks = analyze_browser_bookmarks()
    installed_apps = analyze_installed_apps()
    ssh_hosts = analyze_ssh_config()
    
    items_processed = history_size + len(bookmarks) + len(repos)
    
    # Top commands reveal workflow
    top_commands = [cmd for cmd, _ in shell_commands.most_common(20)]
    
    # Infer traits
    traits = []
    
    # From shell commands
    if "git" in top_commands[:5]:
        traits.append("heavy git user — version control native")
    if "docker" in top_commands[:10]:
        traits.append("containerization workflow")
    if "ssh" in top_commands[:10]:
        traits.append("manages remote systems")
    if any(cmd in top_commands[:10] for cmd in ["vim", "nvim"]):
        traits.append("terminal-native editor user")
    if "code" in top_commands[:10]:
        traits.append("VS Code user")
    if "ollama" in top_commands[:15]:
        traits.append("runs local AI models")
    if any(cmd in top_commands for cmd in ["bitcoin-cli", "lncli", "lightning-cli"]):
        traits.append("Bitcoin node operator")
    
    # From languages
    top_langs = [l for l, _ in languages.most_common(5)]
    if top_langs:
        traits.append(f"codes in {', '.join(top_langs[:3])}")
    
    # From apps
    if "Docker" in installed_apps:
        traits.append("uses containerization")
    if "Ollama" in installed_apps:
        traits.append("local AI/LLM user")
    if "Blender" in installed_apps:
        traits.append("3D modeling/creative")
    
    # Determine technical level
    if history_size > 10000 and len(repos) > 5:
        tech_level = "power user — heavy CLI and development"
    elif history_size > 1000:
        tech_level = "comfortable with terminal"
    else:
        tech_level = "primarily GUI user"
    
    # Extract interests from bookmarks
    bookmark_domains = Counter()
    for b in bookmarks:
        url = b.get("url", "")
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc.replace("www.", "")
            if domain:
                bookmark_domains[domain] += 1
        except:
            pass
    
    return {
        "source": "local_system",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": {
            "technical_skills": tech_level,
            "languages": top_langs,
            "top_commands": top_commands[:15],
            "installed_apps": installed_apps,
            "local_repos": repos[:15],
            "ssh_hosts": ssh_hosts[:10],
            "top_bookmarks": [d for d, _ in bookmark_domains.most_common(15)],
            "personality_traits": traits,
            "interests": [d for d, _ in bookmark_domains.most_common(10)] + top_langs,
            "communication_style": "",
            "tone": "",
        },
        "confidence": min(items_processed / 500, 1.0),
        "items_processed": items_processed,
        "system": {
            "os": platform.system(),
            "shell_history_lines": history_size,
            "local_repos": len(repos),
            "bookmarks": len(bookmarks),
        }
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    result = import_local()
    
    output_path = os.path.join(IMPORT_DIR, "local_system.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
