"""GitHub Actions workflow monitoring and artifact handling."""

from __future__ import annotations

import json
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class WorkflowRun:
    """Represents a GitHub Actions workflow run."""

    id: int
    name: str
    status: str  # queued, in_progress, completed, etc.
    conclusion: str | None  # success, failure, cancelled, timed_out, etc.
    created_at: str
    updated_at: str
    html_url: str
    head_branch: str
    head_sha: str


@dataclass
class Artifact:
    """Represents a GitHub Actions artifact."""

    id: int
    name: str
    size_in_bytes: int
    created_at: str
    expires_at: str | None
    download_url: str


@dataclass
class WorkflowRunInfo:
    """Combined workflow run and artifact information."""

    run: WorkflowRun
    artifacts: list[Artifact] = field(default_factory=list)
    report_data: dict[str, Any] | None = None


class GitHubActionsMonitor:
    """Monitor GitHub Actions workflow runs and download artifacts."""

    def __init__(self, token: str | None = None):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"

    def _request(
        self, method: str, url: str, params: dict | None = None, timeout: int = 30
    ) -> dict[str, Any]:
        """Make a GitHub API request with retry logic."""
        import requests  # noqa: PLC0415

        retries = 3
        backoff = 1

        for attempt in range(retries):
            try:
                resp = requests.request(
                    method, url, params=params, headers=self.headers, timeout=timeout
                )

                if resp.status_code == 429:
                    # Rate limited - respect Retry-After header
                    retry_after = int(resp.headers.get("Retry-After", backoff))
                    time.sleep(retry_after)
                    backoff *= 2
                    continue

                resp.raise_for_status()
                return resp.json()

            except requests.exceptions.RequestException as exc:
                if attempt == retries - 1:
                    raise RuntimeError(f"API request failed after {retries} attempts: {exc}")
                time.sleep(backoff)
                backoff *= 2

    def get_workflow_runs(
        self,
        repo: str,
        branch: str | None = None,
        event_type: str = "pull_request",
        status: str = "completed",
        per_page: int = 10,
    ) -> list[WorkflowRun]:
        """Get recent workflow runs for a repository.

        Args:
            repo: Owner/repo format (e.g., 'owner/repo')
            branch: Filter by branch (optional)
            event_type: GitHub event type (pull_request, push, workflow_dispatch)
            status: Filter by status (completed, in_progress, etc.)
            per_page: Max results per page (max 100)

        Returns:
            List of WorkflowRun objects
        """
        url = f"{self.base_url}/repos/{repo}/actions/runs"
        params = {
            "status": status,
            "event": event_type,
            "per_page": per_page,
        }

        if branch:
            params["branch"] = branch

        data = self._request("GET", url, params=params)
        results = []

        for item in data.get("workflow_runs", []):
            results.append(
                WorkflowRun(
                    id=item["id"],
                    name=item["name"],
                    status=item["status"],
                    conclusion=item.get("conclusion"),
                    created_at=item["created_at"],
                    updated_at=item["updated_at"],
                    html_url=item["html_url"],
                    head_branch=item["head_branch"],
                    head_sha=item["head_sha"],
                )
            )

        return results

    def check_workflow_run_status(
        self, repo: str, run_id: int, token: str | None = None
    ) -> WorkflowRun:
        """Get the current status of a workflow run.

        Args:
            repo: Owner/repo format
            run_id: Workflow run ID
            token: GitHub token (optional, uses instance token if not provided)

        Returns:
            Updated WorkflowRun object with current status
        """
        url = f"{self.base_url}/repos/{repo}/actions/runs/{run_id}"
        data = self._request("GET", url)

        return WorkflowRun(
            id=data["id"],
            name=data["name"],
            status=data["status"],
            conclusion=data.get("conclusion"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            html_url=data["html_url"],
            head_branch=data["head_branch"],
            head_sha=data["head_sha"],
        )

    def poll_workflow_completion(
        self,
        repo: str,
        run_id: int,
        timeout: int = 1800,
        poll_interval: int = 10,
    ) -> WorkflowRun | None:
        """Poll a workflow run until it completes or timeout is reached.

        Args:
            repo: Owner/repo format
            run_id: Workflow run ID to monitor
            timeout: Maximum seconds to wait (default: 30 minutes)
            poll_interval: Seconds between status checks (default: 10)

        Returns:
            Completed WorkflowRun if finished within timeout, None otherwise
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            run = self.check_workflow_run_status(repo, run_id)

            if run.status == "completed":
                return run

            time.sleep(poll_interval)

        return None

    def list_artifacts(self, repo: str, run_id: int) -> list[Artifact]:
        """List artifacts for a completed workflow run.

        Args:
            repo: Owner/repo format
            run_id: Workflow run ID

        Returns:
            List of Artifact objects
        """
        url = f"{self.base_url}/repos/{repo}/actions/runs/{run_id}/artifacts"
        data = self._request("GET", url)
        results = []

        for item in data.get("artifacts", []):
            results.append(
                Artifact(
                    id=item["id"],
                    name=item["name"],
                    size_in_bytes=item["size_in_bytes"],
                    created_at=item["created_at"],
                    expires_at=item.get("expires_at"),
                    download_url=item["archive_download_url"],
                )
            )

        return results

    def download_artifact(
        self, repo: str, artifact_id: int, output_dir: str | Path = "."
    ) -> Path:
        """Download a workflow artifact.

        Args:
            repo: Owner/repo format
            artifact_id: Artifact ID to download
            output_dir: Directory to save extracted content

        Returns:
            Path to the downloaded JSON report file
        """
        import requests  # noqa: PLC0415

        url = f"{self.base_url}/repos/{repo}/actions/artifacts/{artifact_id}/zip"
        output_path = Path(output_dir) / "artifact.zip"

        resp = requests.get(url, headers=self.headers, timeout=60)
        resp.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(resp.content)

        # Extract and find JSON report
        with zipfile.ZipFile(output_path, "r") as zf:
            zf.extractall(output_dir)

        # Look for lint-report.json in extracted content
        output_path = Path(output_dir)
        for json_file in output_path.rglob("lint-report.json"):
            return json_file

        # If not found, return the zip path for manual extraction
        return output_path

    def download_latest_artifact(
        self,
        repo: str,
        run_id: int | None = None,
        artifact_name: str = "lint-report",
        output_dir: str | Path = ".",
    ) -> Path | None:
        """Download the latest lint report artifact from a workflow run.

        Args:
            repo: Owner/repo format
            run_id: Specific run ID (if None, uses most recent completed run)
            artifact_name: Name of artifact to download (default: "lint-report")
            output_dir: Directory to save extracted content

        Returns:
            Path to the JSON report file, or None if not found
        """
        # Get workflow runs if run_id not specified
        if run_id is None:
            runs = self.get_workflow_runs(repo, status="completed", per_page=1)
            if not runs:
                raise RuntimeError(f"No completed workflow runs found in {repo}")
            run_id = runs[0].id

        # List artifacts for the run
        artifacts = self.list_artifacts(repo, run_id)

        # Find matching artifact
        target_artifact = None
        for artifact in artifacts:
            if artifact_name in artifact.name.lower():
                target_artifact = artifact
                break

        if not target_artifact:
            available_names = [a.name for a in artifacts]
            raise RuntimeError(
                f"Artifact '{artifact_name}' not found in run {run_id}. "
                f"Available: {available_names}"
            )

        # Download and extract
        zip_path = Path(output_dir) / f"{artifact_name}.zip"
        output_path = Path(output_dir) / artifact_name

        import requests  # noqa: PLC0415

        resp = requests.get(
            target_artifact.download_url, headers=self.headers, timeout=60
        )
        resp.raise_for_status()

        with open(zip_path, "wb") as f:
            f.write(resp.content)

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(output_path)

        # Find JSON report
        json_file = output_path / "lint-report.json"
        if json_file.exists():
            return json_file

        # Try alternative names
        for candidate in output_path.rglob("*.json"):
            if "report" in candidate.name.lower() or "lint" in candidate.name.lower():
                return candidate

        return None

    def download_all_reports(
        self,
        repo: str,
        run_id: int | None = None,
        output_dir: str | Path = ".",
    ) -> dict[str, Path]:
        """Download all lint report artifacts (JSON and Markdown) from a workflow run.

        Args:
            repo: Owner/repo format
            run_id: Specific run ID (if None, uses most recent completed run)
            output_dir: Directory to save extracted content

        Returns:
            Dictionary mapping report type ('json', 'markdown') to file paths
        """
        # Get workflow runs if run_id not specified
        if run_id is None:
            runs = self.get_workflow_runs(repo, status="completed", per_page=1)
            if not runs:
                raise RuntimeError(f"No completed workflow runs found in {repo}")
            run_id = runs[0].id

        # List artifacts for the run
        artifacts = self.list_artifacts(repo, run_id)

        results: dict[str, Path] = {}
        output_path = Path(output_dir)

        for artifact in artifacts:
            artifact_lower = artifact.name.lower()

            # Download JSON report
            if "json" in artifact_lower and "report" in artifact_lower:
                zip_path = output_path / f"{artifact.name}.zip"
                extract_dir = output_path / artifact.name

                import requests  # noqa: PLC0415

                resp = requests.get(
                    artifact.download_url, headers=self.headers, timeout=60
                )
                resp.raise_for_status()

                with open(zip_path, "wb") as f:
                    f.write(resp.content)

                with zipfile.ZipFile(zip_path, "r") as zf:
                    zf.extractall(extract_dir)

                # Find the JSON file
                json_file = extract_dir / "lint-report.json"
                if json_file.exists():
                    results["json"] = json_file
                else:
                    for candidate in extract_dir.rglob("*.json"):
                        if "report" in candidate.name.lower():
                            results["json"] = candidate
                            break

            # Download Markdown report
            elif "md" in artifact_lower and "report" in artifact_lower:
                zip_path = output_path / f"{artifact.name}.zip"
                extract_dir = output_path / artifact.name

                import requests  # noqa: PLC0415

                resp = requests.get(
                    artifact.download_url, headers=self.headers, timeout=60
                )
                resp.raise_for_status()

                with open(zip_path, "wb") as f:
                    f.write(resp.content)

                with zipfile.ZipFile(zip_path, "r") as zf:
                    zf.extractall(extract_dir)

                # Find the Markdown file
                md_file = extract_dir / "lint-report.md"
                if md_file.exists():
                    results["markdown"] = md_file
                else:
                    for candidate in extract_dir.rglob("*.md"):
                        if "report" in candidate.name.lower():
                            results["markdown"] = candidate
                            break

        return results

    def load_report_from_json(self, json_path: str | Path) -> dict[str, Any]:
        """Load lint report from a JSON file.

        Args:
            json_path: Path to the JSON report file

        Returns:
            Parsed report data as dictionary
        """
        path = Path(json_path)
        data = json.loads(path.read_text(encoding="utf-8"))

        # Normalize structure if needed
        if "summary" in data and "results" in data:
            return data

        # Handle alternative structures
        if "reports" in data:
            return {
                "summary": {},
                "results": data["reports"],
                "errors": [],
            }

        return data
