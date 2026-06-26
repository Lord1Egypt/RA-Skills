from __future__ import annotations

import argparse
import json
import os
from typing import Sequence

from pypi_package_changelog_generator.archive_diff import (
    ArchiveComparison,
    ArchiveDiffError,
    compare_release_archives,
)
from pypi_package_changelog_generator.budget import apply_budget
from pypi_package_changelog_generator.metadata_analysis import analyze_metadata
from pypi_package_changelog_generator.models import (
    ChangelogResult,
    ErrorInfo,
    WarningInfo,
)
from pypi_package_changelog_generator.pypi_client import PypiClient, PypiClientError
from pypi_package_changelog_generator.providers.base import ProviderError
from pypi_package_changelog_generator.providers.github import GitHubProvider
from pypi_package_changelog_generator.versioning import (
    VersionResolutionError,
    resolve_version_pair,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pypi-package-changelog-generator",
        description="Generate structured changelog inputs for PyPI package version diffs.",
    )
    parser.add_argument("--package", required=True, help="PyPI package name.")
    parser.add_argument("--from-version", help="Explicit base version.")
    parser.add_argument("--to-version", help="Explicit target version.")
    parser.add_argument(
        "--version-range",
        help="Version range expression such as '>=1.0,<2.0' or 'latest-1'.",
    )
    parser.add_argument(
        "--github-token",
        default=None,
        help="Optional GitHub token. Defaults to GITHUB_TOKEN from the environment.",
    )
    parser.add_argument(
        "--json-indent",
        type=int,
        default=2,
        help="Indent level for JSON output.",
    )
    return parser


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.version_range and (args.from_version or args.to_version):
        parser.error(
            "Use either --version-range or --from-version/--to-version, not both."
        )
    if not args.version_range and not (args.from_version and args.to_version):
        parser.error(
            "Provide either --version-range or both --from-version and --to-version."
        )


def execute_analysis(args: argparse.Namespace) -> ChangelogResult:
    token = os.getenv("GITHUB_TOKEN")
    result = ChangelogResult(
        package=args.package,
        resolved_versions={"from": None, "to": None, "range": args.version_range},
        mode="error",
    )
    result.auth.token_provided = bool(token)
    result.auth.provider = "github" if token else None

    archive_comparison: ArchiveComparison | None = None
    try:
        with PypiClient() as client:
            project_payload = client.get_project(args.package)
            selection = resolve_version_pair(
                project_payload.get("releases", {}),
                from_version=args.from_version,
                to_version=args.to_version,
                version_range=args.version_range,
            )
            result.resolved_versions = {
                "from": selection.from_version,
                "to": selection.to_version,
                "range": selection.range_expression,
            }

            from_release = client.get_release(args.package, selection.from_version)
            to_release = client.get_release(args.package, selection.to_version)

            repo_url = client.extract_repository_url(
                to_release, from_release, project_payload
            )
            if repo_url:
                try:
                    provider = GitHubProvider(token=token)
                    provider_result = provider.compare_versions(
                        repo_url,
                        selection.from_version,
                        selection.to_version,
                    )
                    result.mode = provider_result["mode"]
                    result.source.provider = provider_result["source"]["provider"]
                    result.source.repository_url = provider_result["source"][
                        "repository_url"
                    ]
                    result.source.compare_url = provider_result["source"]["compare_url"]
                    result.commits = provider_result["commits"]
                    result.reviews = provider_result["reviews"]
                    result.file_changes = provider_result["file_changes"]
                    result.warnings.extend(provider_result["warnings"])
                    provider.close()
                except ProviderError as exc:
                    result.warnings.append(
                        WarningInfo(code=exc.code, message=exc.message)
                    )
            else:
                result.warnings.append(
                    WarningInfo(
                        code="repository_missing",
                        message="No public GitHub repository was found in PyPI metadata; archive fallback will be used.",
                    )
                )

            try:
                archive_comparison = compare_release_archives(
                    client, from_release, to_release
                )
            except ArchiveDiffError as exc:
                result.warnings.append(WarningInfo(code=exc.code, message=exc.message))
            else:
                if result.mode != "git":
                    result.mode = "archive"
                    result.source.provider = "archive"
                    result.source.repository_url = None
                    result.source.compare_url = None
                    result.file_changes = archive_comparison.file_changes

            metadata = analyze_metadata(
                from_release,
                to_release,
                from_root=(
                    archive_comparison.from_archive.root if archive_comparison else None
                ),
                to_root=(
                    archive_comparison.to_archive.root if archive_comparison else None
                ),
                file_changes=result.file_changes,
            )
            result.metadata_changes = metadata["metadata_changes"]
            result.dependency_changes = metadata["dependency_changes"]
            result.breaking_signals = metadata["breaking_signals"]

            if result.mode == "error" and result.warnings:
                result.errors.append(
                    ErrorInfo(
                        code="analysis_unavailable",
                        message="Neither GitHub compare nor archive diff produced usable evidence.",
                        retryable=True,
                    )
                )
            apply_budget(result)
    except (PypiClientError, VersionResolutionError) as exc:
        code = getattr(exc, "code", "version_resolution_error")
        retryable = getattr(exc, "retryable", False)
        result.errors.append(
            ErrorInfo(code=code, message=str(exc), retryable=retryable)
        )
    finally:
        if archive_comparison:
            archive_comparison.cleanup()

    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_args(parser, args)
    result = execute_analysis(args)
    try:
        print(json.dumps(result.to_dict(), indent=args.json_indent, sort_keys=True))
    except BrokenPipeError:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
