"""GitHub repository monitoring for OpenClaw integration."""

import time
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from pydantic import BaseModel
from pathlib import Path

from rich.console import Console

from ..config import get_config, OpenClawConfig
from ..storage.database import Database, MonitoredRepo

try:
    from github import Github, Commit, Repository
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

console = Console()


class CommitInfo(BaseModel):
    """Git commit information."""

    sha: str
    message: str
    author: str
    date: datetime
    repository: str
    branch: str
    files_changed: List[str] = []


class GitHubMonitor:
    """Monitor GitHub repositories for code changes."""

    def __init__(self, db_path: str = None, poll_interval: int = 300, token: str = None):
        """
        Initialize GitHub monitor.

        Args:
            db_path: Path to database file
            poll_interval: Polling interval in seconds
            token: GitHub personal access token
        """
        self.db = Database(db_path)
        self.poll_interval = poll_interval
        self.token = token
        self.github = None
        self.running = False
        self.thread = None
        self.last_commits = {}  # Track last commit per repository

    def initialize(self) -> bool:
        """
        Initialize GitHub client.

        Returns:
            True if successful, False otherwise
        """
        if not GITHUB_AVAILABLE:
            console.print("[red]✗ PyGithub not installed. Install with: pip install PyGithub[/red]")
            return False

        if not self.token:
            console.print("[yellow]⚠ GitHub token not provided[/yellow]")
            return False

        try:
            self.github = Github(self.token)
            user = self.github.get_user()
            console.print(f"[green]✓ Connected to GitHub as {user.login}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to initialize GitHub client: {e}[/red]")
            return False

    def start(self, callback: Optional[Callable[[CommitInfo], None]] = None):
        """
        Start monitoring daemon.

        Args:
            callback: Optional callback function for new commits
        """
        if self.running:
            console.print("[yellow]⚠ Monitor is already running[/yellow]")
            return

        if not self.initialize():
            return

        console.print("[green]✓ Starting GitHub monitor daemon[/green]")
        self.running = True
        self.thread = threading.Thread(target=self._run_monitor_loop, args=(callback,), daemon=True)
        self.thread.start()

    def stop(self):
        """Stop monitoring daemon."""
        console.print("[yellow]⚠ Stopping GitHub monitor daemon...[/yellow]")
        self.running = False

        if self.thread:
            self.thread.join(timeout=5)
            console.print("[green]✓ GitHub monitor stopped[/green]")

    def _run_monitor_loop(self, callback: Optional[Callable[[CommitInfo], None]]):
        """Main monitoring loop."""
        while self.running:
            try:
                # Poll all monitored repositories
                repos = self.db.get_monitored_repos()

                for monitored_repo in repos:
                    if not monitored_repo.enabled:
                        continue

                    self._check_repository(monitored_repo.owner_repo, callback)

                # Wait before next poll
                time.sleep(self.poll_interval / len(repos) if repos else self.poll_interval)

            except Exception as e:
                console.print(f"[red]✗ Monitor loop error: {e}[/red]")
                time.sleep(self.poll_interval)

    def _check_repository(self, repo_name: str, callback: Optional[Callable[[CommitInfo], None]]):
        """
        Check repository for new commits.

        Args:
            repo_name: Repository name (owner/repo)
            callback: Callback function for new commits
        """
        try:
            repo = self.github.get_repo(repo_name)

            # Get last commit
            default_branch = repo.default_branch
            last_commit = repo.get_commits(sha=default_branch)[0]

            # Check if this is a new commit
            last_seen = self.last_commits.get(repo_name)
            current_sha = last_commit.sha

            if last_seen != current_sha:
                # New commit found
                commit_info = CommitInfo(
                    sha=current_sha,
                    message=last_commit.commit.message,
                    author=last_commit.author.login,
                    date=last_commit.commit.author.date,
                    repository=repo_name,
                    branch=default_branch,
                    files_changed=[file.filename for file in last_commit.files[:5]]
                )

                console.print(
                    f"[cyan]New commit detected: {repo_name} @ {default_branch}[/cyan]"
                )
                console.print(f"  Author: {commit_info.author}")
                console.print(f"  Message: {commit_info.message[:50]}...")

                # Update database
                self.db.update_repo_commit(repo_name, current_sha)

                # Track last commit
                self.last_commits[repo_name] = current_sha

                # Call callback if provided
                if callback:
                    try:
                        callback(commit_info)
                    except Exception as e:
                        console.print(f"[yellow]⚠ Callback error: {e}[/yellow]")

        except Exception as e:
            console.print(f"[red]✗ Error checking repository {repo_name}: {e}[/red]")

    def add_repository(self, repo_name: str, enabled: bool = True) -> Optional[int]:
        """
        Add a repository to monitor.

        Args:
            repo_name: Repository name (owner/repo)
            enabled: Enable monitoring (default: True)

        Returns:
            MonitoredRepo ID if successful, None otherwise
        """
        console.print(f"[cyan]Adding repository to monitor: {repo_name}[/cyan]")

        # Validate repository format
        if '/' not in repo_name:
            console.print("[red]✗ Invalid repository format. Use owner/repo[/red]")
            return None

        try:
            # Test access to repository
            if not self.github:
                if not self.initialize():
                    return None

            repo = self.github.get_repo(repo_name)
            console.print(f"[green]✓ Repository exists: {repo.full_name}[/green]")

            # Add to database
            repo_id = self.db.add_monitored_repo(repo_name, enabled)

            # Track last commit
            default_branch = repo.default_branch
            last_commit = repo.get_commits(sha=default_branch)[0]
            self.last_commits[repo_name] = last_commit.sha

            console.print(f"[green]✓ Repository added with ID: {repo_id}[/green]")
            return repo_id

        except Exception as e:
            console.print(f"[red]✗ Failed to add repository: {e}[/red]")
            return None

    def remove_repository(self, repo_name: str) -> bool:
        """
        Remove a repository from monitoring.

        Args:
            repo_name: Repository name

        Returns:
            True if successful, False otherwise
        """
        console.print(f"[cyan]Removing repository from monitor: {repo_name}[/cyan]")

        try:
            success = self.db.remove_monitored_repo(repo_name)

            if success:
                # Remove from cache
                if repo_name in self.last_commits:
                    del self.last_commits[repo_name]

                console.print(f"[green]✓ Repository removed: {repo_name}[/green]")
            else:
                console.print(f"[yellow]⚠ Repository not found in database[/yellow]")

            return success
        except Exception as e:
            console.print(f"[red]✗ Failed to remove repository: {e}[/red]")
            return False

    def list_repositories(self) -> List[MonitoredRepo]:
        """List all monitored repositories.

        Returns:
            List of MonitoredRepo objects
        """
        repos = self.db.get_monitored_repos()

        if not repos:
            console.print("[yellow]No repositories being monitored[/yellow]")
        else:
            console.print(f"[cyan]Monitored repositories ({len(repos)}):[/cyan]")

            for repo in repos:
                status = "[green]enabled[/green]" if repo.enabled else "[red]disabled[/red]"
                console.print(f"  [cyan]{repo.owner_repo}[/cyan] - {status}")
                console.print(f"    Last commit: {repo.last_commit or 'N/A'}")
                console.print(f"    Last checked: {repo.last_checked.strftime('%Y-%m-%d %H:%M')}")

        return repos

    def get_recent_commits(self, repo_name: str, limit: int = 10) -> List[CommitInfo]:
        """
        Get recent commits from a repository.

        Args:
            repo_name: Repository name
            limit: Maximum number of commits

        Returns:
            List of CommitInfo objects
        """
        console.print(f"[cyan]Getting recent commits from {repo_name}[/cyan]")

        try:
            repo = self.github.get_repo(repo_name)
            commits = repo.get_commits()[:limit]

            commit_list = []
            for commit in commits:
                commit_info = CommitInfo(
                    sha=commit.sha,
                    message=commit.commit.message,
                    author=commit.author.login,
                    date=commit.commit.author.date,
                    repository=repo_name,
                    branch=repo.default_branch,
                    files_changed=[file.filename for file in commit.files[:5]]
                )
                commit_list.append(commit_info)

            console.print(f"[green]✓ Retrieved {len(commit_list)} commits[/green]")

            return commit_list

        except Exception as e:
            console.print(f"[red]✗ Failed to get commits: {e}[/red]")
            return []

    def set_poll_interval(self, interval: int):
        """
        Set polling interval.

        Args:
            interval: Interval in seconds
        """
        if interval < 60:
            console.print("[yellow]⚠ Minimum poll interval is 60 seconds[/yellow]")
            interval = 60

        self.poll_interval = interval
        console.print(f"[cyan]Poll interval set to {interval} seconds[/cyan]")

    def get_status(self) -> Dict[str, Any]:
        """Get monitor status.

        Returns:
            Dictionary with status information
        """
        repos = self.db.get_monitored_repos()
        enabled_repos = [r for r in repos if r.enabled]

        return {
            "running": self.running,
            "total_repos": len(repos),
            "enabled_repos": len(enabled_repos),
            "poll_interval": self.poll_interval,
            "last_check": datetime.now().isoformat()
        }

    def export_activity(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Export monitoring activity.

        Args:
            days: Number of days to export

        Returns:
            List of activity records
        """
        console.print(f"[cyan]Exporting activity for last {days} days[/cyan]")

        # This would need an activity tracking table
        # For now, return repository list
        repos = self.db.get_monitored_repos()

        activity = []
        for repo in repos:
            activity.append({
                "repository": repo.owner_repo,
                "last_commit": repo.last_commit,
                "last_checked": repo.last_checked.isoformat(),
                "enabled": repo.enabled
            })

        console.print(f"[green]✓ Exported {len(activity)} records[/green]")
        return activity

    def generate_report(self) -> str:
        """Generate monitoring report.

        Returns:
            Markdown report
        """
        repos = self.db.get_monitored_repos()

        report = "# GitHub Monitoring Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        report += f"Total Repositories: {len(repos)}\n\n"

        for repo in repos:
            status = "✓ Enabled" if repo.enabled else "✗ Disabled"
            report += f"## {repo.owner_repo} {status}\n\n"
            report += f"- Last Commit: {repo.last_commit or 'N/A'}\n"
            report += f"- Last Checked: {repo.last_checked.strftime('%Y-%m-%d %H:%M') if repo.last_checked else 'N/A'}\n\n"

        console.print("[green]✓ Report generated[/green]")
        return report
