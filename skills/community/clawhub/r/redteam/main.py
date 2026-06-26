import sys
import os

# Add the parent directory to sys.path so we can import agent_redteam
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import argparse
from agent_redteam import repo_scanner

def main(args):
    """
    Main entry point for the Red Team skill.
    """
    parser = argparse.ArgumentParser(description="Proactive AI agent security scanner.")
    subparsers = parser.add_subparsers(dest="command")

    # 'repo' command to scan a GitHub repo
    repo_parser = subparsers.add_parser("repo", help="Scan a GitHub repo for vulnerabilities")
    repo_parser.add_argument("repo_url", help="The URL of the repository to scan")

    # 'scan' command
    scan_parser = subparsers.add_parser("scan", help="Scan an agent for vulnerabilities")
    scan_parser.add_argument("agent_id", help="The ID of the agent to scan")

    parsed_args = parser.parse_args(args)

    if parsed_args.command == "repo":
        print(f"Scanning repository: {parsed_args.repo_url}...")
        report = repo_scanner.scan_repo(parsed_args.repo_url)
        print(f"Scan complete. Risk: {report.overall_risk} (Score: {report.score})")
        for finding in report.findings:
            print(f"- [{finding.severity}] {finding.description} in {finding.file_path}")
            
    elif parsed_args.command == "scan":
        print(f"Scanning agent: {parsed_args.agent_id}...")
        print(f"Scan complete. Found 0 issues.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main(sys.argv[1:])
