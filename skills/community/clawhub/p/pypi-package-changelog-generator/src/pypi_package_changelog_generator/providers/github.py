from __future__ import annotations

import time
from typing import Any
from urllib.parse import quote, urlparse

from pypi_package_changelog_generator._http import (
    HttpClient,
    HttpResponse,
    HttpTransport,
    HttpTransportError,
)
from pypi_package_changelog_generator.diff_text import format_git_diff_patch
from pypi_package_changelog_generator.models import WarningInfo
from pypi_package_changelog_generator.providers.base import (
    ProviderError,
    RepositoryProvider,
)
from pypi_package_changelog_generator.versioning import build_tag_candidates


class GitHubProvider(RepositoryProvider):
    def __init__(
        self,
        *,
        token: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        transport: HttpTransport | None = None,
    ) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._client = HttpClient(
            base_url="https://api.github.com",
            headers=headers,
            timeout=timeout,
            transport=transport,
            trust_env=True,
        )
        self._max_retries = max_retries

    def close(self) -> None:
        self._client.close()

    def compare_versions(
        self, repo_url: str, from_version: str, to_version: str
    ) -> dict:
        owner, repo = parse_github_repo(repo_url)
        tags = self._fetch_tags(owner, repo)
        from_tag = resolve_tag_name(tags, from_version)
        to_tag = resolve_tag_name(tags, to_version)
        if not from_tag or not to_tag:
            missing = from_version if not from_tag else to_version
            raise ProviderError(
                code="github_tag_not_found",
                message=f"Could not match a GitHub tag for version '{missing}'.",
            )

        compare_path = f"/repos/{owner}/{repo}/compare/{quote(from_tag, safe='')}...{quote(to_tag, safe='')}"
        payload = self._get_json(compare_path)
        warnings: list[WarningInfo] = []
        if len(payload.get("files", [])) >= 300:
            warnings.append(
                WarningInfo(
                    code="github_file_limit",
                    message="GitHub compare returned 300 files; additional files may be omitted.",
                )
            )

        commits = [
            {
                "sha": commit.get("sha"),
                "title": (commit.get("commit", {}).get("message") or "").splitlines()[
                    0
                ],
                "message": commit.get("commit", {}).get("message"),
                "author": commit.get("commit", {}).get("author", {}).get("name"),
                "date": commit.get("commit", {}).get("author", {}).get("date"),
                "url": commit.get("html_url"),
            }
            for commit in payload.get("commits", [])
        ]

        file_changes = [
            {
                "path": file_info.get("filename"),
                "previous_path": file_info.get("previous_filename"),
                "status": file_info.get("status"),
                "additions": file_info.get("additions", 0),
                "deletions": file_info.get("deletions", 0),
                "changes": file_info.get("changes", 0),
                "patch": format_git_diff_patch(
                    path=file_info.get("filename"),
                    previous_path=file_info.get("previous_filename"),
                    status=file_info.get("status"),
                    patch=file_info.get("patch"),
                ),
            }
            for file_info in payload.get("files", [])
        ]

        reviews = self._collect_pull_requests(owner, repo, payload.get("commits", []))
        return {
            "mode": "git",
            "source": {
                "provider": "github",
                "repository_url": repo_url,
                "compare_url": payload.get("html_url"),
            },
            "commits": commits,
            "reviews": reviews,
            "file_changes": file_changes,
            "warnings": warnings,
        }

    def _collect_pull_requests(
        self, owner: str, repo: str, commits: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        collected: dict[int, dict[str, Any]] = {}
        for commit in commits[:50]:
            sha = commit.get("sha")
            if not sha:
                continue
            try:
                payload = self._get_json(f"/repos/{owner}/{repo}/commits/{sha}/pulls")
            except ProviderError:
                continue
            for pull in payload:
                number = pull.get("number")
                if number is None or number in collected:
                    continue
                collected[number] = {
                    "number": number,
                    "title": pull.get("title"),
                    "url": pull.get("html_url"),
                    "state": pull.get("state"),
                    "merged_at": pull.get("merged_at"),
                }
        return list(collected.values())

    def _fetch_tags(self, owner: str, repo: str) -> list[str]:
        tags: list[str] = []
        page = 1
        while page <= 10:
            payload = self._get_json(
                f"/repos/{owner}/{repo}/tags", params={"per_page": 100, "page": page}
            )
            if not payload:
                break
            tags.extend(tag.get("name") for tag in payload if tag.get("name"))
            if len(payload) < 100:
                break
            page += 1
        return tags

    def _get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.get(path, params=params)
            except HttpTransportError as exc:
                if attempt >= self._max_retries:
                    raise ProviderError(
                        code="github_http_error",
                        message=f"GitHub request failed for {path}.",
                        retryable=True,
                    ) from exc
                time.sleep(2**attempt)
                continue

            if response.status_code < 400:
                return response.json()

            if (
                response.status_code in {403, 429, 500, 502, 503, 504}
                and attempt < self._max_retries
            ):
                delay = compute_retry_delay(response.headers, attempt)
                if delay is not None:
                    time.sleep(delay)
                    continue

            message = _extract_error_message(response)
            retryable = response.status_code in {403, 429, 500, 502, 503, 504}
            code = f"github_http_{response.status_code}"
            if response.status_code in {403, 429} and is_rate_limited(response):
                code = "github_rate_limited"
                retryable = True
            raise ProviderError(code=code, message=message, retryable=retryable)

        raise ProviderError(
            code="github_retry_exhausted",
            message=f"GitHub request failed for {path}.",
            retryable=True,
        )


def parse_github_repo(repo_url: str) -> tuple[str, str]:
    parsed = urlparse(repo_url)
    if parsed.netloc.lower() != "github.com":
        raise ProviderError(
            code="unsupported_repository",
            message="Only GitHub repositories are supported in Mode A.",
        )
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise ProviderError(
            code="invalid_repository_url",
            message="Repository URL must include owner and repo.",
        )
    return parts[0], parts[1]


def resolve_tag_name(tags: list[str], version: str) -> str | None:
    candidate_names = build_tag_candidates(version)
    lower_map = {tag.lower(): tag for tag in tags}
    for candidate in candidate_names:
        matched = lower_map.get(candidate.lower())
        if matched:
            return matched
    return None


def is_rate_limited(response: HttpResponse) -> bool:
    if response.headers.get("retry-after"):
        return True
    if response.headers.get("x-ratelimit-remaining") == "0":
        return True
    try:
        payload = response.json()
    except ValueError:
        return False
    return "rate limit" in str(payload.get("message", "")).lower()


def compute_retry_delay(
    headers: dict[str, str], attempt: int, now: float | None = None
) -> float | None:
    retry_after = headers.get("retry-after")
    if retry_after:
        try:
            return max(float(retry_after), 0.0)
        except ValueError:
            return None

    remaining = headers.get("x-ratelimit-remaining")
    reset = headers.get("x-ratelimit-reset")
    if remaining == "0" and reset:
        reference = time.time() if now is None else now
        try:
            return max(float(reset) - reference, 0.0) + 1.0
        except ValueError:
            return None

    return float(60 * (2**attempt))


def _extract_error_message(response: HttpResponse) -> str:
    try:
        payload = response.json()
    except ValueError:
        return f"GitHub request failed with HTTP {response.status_code}."
    message = (
        payload.get("message")
        or f"GitHub request failed with HTTP {response.status_code}."
    )
    return str(message)
