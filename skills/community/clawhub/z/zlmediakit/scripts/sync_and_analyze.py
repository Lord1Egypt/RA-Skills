import os
import subprocess
import urllib.request
import json
import datetime
import argparse

REPO_URL = "https://github.com/ZLMediaKit/ZLMediaKit.git"
API_BASE = "https://api.github.com/repos/ZLMediaKit/ZLMediaKit"
WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR", r"D:\.openclaw\workspace")
TARGET_DIR = os.path.join(WORKSPACE_DIR, "ZLMediaKit")

def run_cmd(cmd, cwd=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing {cmd}:\n{result.stderr}")
    return result.stdout.strip()

def sync_code():
    if not os.path.exists(TARGET_DIR):
        print(f"Directory {TARGET_DIR} not found. Cloning repository...")
        run_cmd(f"git clone {REPO_URL} {TARGET_DIR}")
    else:
        print(f"Directory {TARGET_DIR} exists. Pulling latest code...")
        run_cmd("git pull origin master", cwd=TARGET_DIR)

def fetch_github_data(endpoint, limit=5):
    url = f"{API_BASE}/{endpoint}?per_page={limit}&state=all"
    req = urllib.request.Request(url)
    
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
        
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return []

def generate_report():
    print("Fetching recent issues and PRs...")
    issues = fetch_github_data("issues", 10)
    
    if not issues:
        issues_error = True
    else:
        issues_error = False
        
    # GitHub API returns PRs as issues too, so we filter them out
    real_issues = [i for i in issues if "pull_request" not in i][:5] if not issues_error else []
    pull_requests = [i for i in issues if "pull_request" in i][:5] if not issues_error else []
    
    report_lines = [
        f"# ZLMediaKit Analyzer Report",
        f"*Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "## 📦 仓库状态",
        f"- **本地路径**: `{TARGET_DIR}`",
        f"- **最后提交**: ",
        run_cmd('git log -1 --format="%h - %s (%cr) <%an>"', cwd=TARGET_DIR) if os.path.exists(TARGET_DIR) else "N/A",
        "",
    ]
    
    if issues_error:
        report_lines.append("⚠️ **警告**: 获取 Issue 和 PR 失败，可能是因为触发了 GitHub API 速率限制。请配置 `GITHUB_TOKEN` 环境变量。")
    else:
        report_lines.append("## 🐛 最近 Issues")
        for i in real_issues:
            report_lines.append(f"- [#{i['number']}]({i['html_url']}) {i['title']} ({i['state']})")
            
        report_lines.extend(["", "## 🔄 最近 Pull Requests"])
        for pr in pull_requests:
            report_lines.append(f"- [#{pr['number']}]({pr['html_url']}) {pr['title']} ({pr['state']})")
        
    report_content = "\n".join(report_lines)
    
    report_path = os.path.join(WORKSPACE_DIR, "zlmediakit_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"\nReport generated at: {report_path}")
    return report_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ZLMediaKit Analyzer Skill Script")
    parser.add_argument("--skip-sync", action="store_true", help="Skip git clone/pull")
    args = parser.parse_args()

    if not args.skip_sync:
        sync_code()
        
    generate_report()
    print("Done. To analyze source code, ask the OpenClaw agent to use search tools on the cloned directory.")
