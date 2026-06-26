from __future__ import annotations

import re

from vibe_sanitizer.masking import mask_bearer_token, mask_token, preview_credential_url, sanitize_credential_url

from .base import DetectorContext, RegexDetector


PATH_CHARS = r"[^\s'\"`<>,;(){}]+"


def build_builtin_detectors(context: DetectorContext) -> list[RegexDetector]:
    repo_root_value = str(context.repo_root)
    repo_root_pattern = re.escape(repo_root_value) + rf"(?:[\\/]{PATH_CHARS})*"

    detectors = [
        RegexDetector(
            detector_id="private_key_block",
            title="Private key block",
            category="secret",
            severity="critical",
            message="Private key material should never be committed or shared.",
            pattern=re.compile(
                r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----",
                re.DOTALL,
            ),
            preview_builder=lambda match: "-----BEGIN PRIVATE KEY-----\n***\n-----END PRIVATE KEY-----",
            replacement_builder=lambda _match, placeholders: placeholders["private_key_block"],
            priority=100,
            editable_in_place=True,
            review_required=False,
        ),
        RegexDetector(
            detector_id="openai_key",
            title="OpenAI-style API key",
            category="secret",
            severity="high",
            message="OpenAI-style API keys should be removed or moved to environment variables.",
            pattern=re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
            preview_builder=lambda match: mask_token(match.group(), keep_prefix=3, keep_suffix=4),
            replacement_builder=lambda _match, placeholders: placeholders["openai_key"],
            priority=90,
            editable_in_place=True,
            review_required=False,
        ),
        RegexDetector(
            detector_id="aws_access_key",
            title="AWS access key id",
            category="secret",
            severity="high",
            message="AWS access key ids should not be stored in repository files.",
            pattern=re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
            preview_builder=lambda match: mask_token(match.group(), keep_prefix=4, keep_suffix=4),
            replacement_builder=lambda _match, placeholders: placeholders["aws_access_key"],
            priority=85,
            editable_in_place=True,
            review_required=False,
        ),
        RegexDetector(
            detector_id="github_token",
            title="GitHub token",
            category="secret",
            severity="high",
            message="GitHub personal access tokens should never be committed.",
            pattern=re.compile(r"\b(?:gh[pours]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
            preview_builder=lambda match: mask_token(match.group(), keep_prefix=4, keep_suffix=4),
            replacement_builder=lambda _match, placeholders: placeholders["github_token"],
            priority=84,
            editable_in_place=True,
            review_required=False,
        ),
        RegexDetector(
            detector_id="slack_token",
            title="Slack token",
            category="secret",
            severity="high",
            message="Slack tokens should not appear in repository content.",
            pattern=re.compile(r"\bxox(?:a|b|p|s|r)-[A-Za-z0-9-]{10,}\b"),
            preview_builder=lambda match: mask_token(match.group(), keep_prefix=4, keep_suffix=4),
            replacement_builder=lambda _match, placeholders: placeholders["slack_token"],
            priority=83,
            editable_in_place=True,
            review_required=False,
        ),
        RegexDetector(
            detector_id="bearer_token",
            title="Bearer token",
            category="secret",
            severity="high",
            message="Bearer tokens should be removed from code and configuration files.",
            pattern=re.compile(r"\bBearer\s+(?P<token>[A-Za-z0-9\-._~+/]+=*)", re.IGNORECASE),
            preview_builder=lambda match: mask_bearer_token(match.group("token")),
            replacement_builder=lambda _match, placeholders: placeholders["bearer_token"],
            priority=82,
            editable_in_place=True,
            review_required=False,
            span_group="token",
        ),
        RegexDetector(
            detector_id="credential_url",
            title="Credential-bearing URL",
            category="secret",
            severity="high",
            message="URLs containing usernames and passwords need review before commit.",
            pattern=re.compile(
                r"\b[A-Za-z][A-Za-z0-9+.-]{1,20}://[^/\s:@]+:[^@\s/]+@[^\s'\"`<>]+"
            ),
            preview_builder=lambda match: preview_credential_url(match.group()),
            replacement_builder=lambda match, placeholders: sanitize_credential_url(
                match.group(),
                placeholders["credential_url_user"],
                placeholders["credential_url_password"],
            ),
            priority=70,
            editable_in_place=False,
            review_required=True,
        ),
        RegexDetector(
            detector_id="secret_assignment",
            title="Secret-like assignment",
            category="secret",
            severity="medium",
            message="Quoted secret assignments need review before commit.",
            pattern=re.compile(
                r"(?P<prefix>(?:['\"])?(?:api[_-]?key|access[_-]?token|auth[_-]?token|token|secret|password|passwd|client[_-]?secret)(?:['\"])?\s*[:=]\s*)"
                r"(?P<quote>['\"])(?P<value>[^'\"\n]{8,})(?P=quote)",
                re.IGNORECASE,
            ),
            preview_builder=lambda match: mask_token(match.group("value"), keep_prefix=2, keep_suffix=2),
            replacement_builder=lambda _match, placeholders: placeholders["generic_secret"],
            priority=60,
            editable_in_place=False,
            review_required=True,
            span_group="value",
            match_filter=lambda match: not match.group("value").startswith(("<REDACTED_", "${")),
        ),
        RegexDetector(
            detector_id="workspace_path",
            title="Workspace path",
            category="path",
            severity="medium",
            message="Workspace-specific file paths leak local machine context.",
            pattern=re.compile(repo_root_pattern),
            preview_builder=lambda match: match.group(),
            replacement_builder=lambda _match, placeholders: placeholders["workspace_path"],
            priority=55,
            editable_in_place=True,
            review_required=False,
        ),
        RegexDetector(
            detector_id="home_path",
            title="Home directory path",
            category="path",
            severity="medium",
            message="Home-directory paths leak local machine details.",
            pattern=re.compile(
                rf"(?:/Users/[A-Za-z0-9._-]+(?:/{PATH_CHARS})+|/home/[A-Za-z0-9._-]+(?:/{PATH_CHARS})+)"
            ),
            preview_builder=lambda match: match.group(),
            replacement_builder=lambda _match, placeholders: placeholders["home_path"],
            priority=50,
            editable_in_place=True,
            review_required=False,
        ),
        RegexDetector(
            detector_id="temp_path",
            title="Temporary directory path",
            category="path",
            severity="low",
            message="Temporary directory paths can leak machine-specific details.",
            pattern=re.compile(rf"(?:/var/folders/{PATH_CHARS}+|/tmp/{PATH_CHARS}+)", re.IGNORECASE),
            preview_builder=lambda match: match.group(),
            replacement_builder=lambda _match, placeholders: placeholders["temp_path"],
            priority=45,
            editable_in_place=True,
            review_required=False,
        ),
        RegexDetector(
            detector_id="windows_user_path",
            title="Windows user path",
            category="path",
            severity="medium",
            message="Windows user paths leak local machine details.",
            pattern=re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+(?:\\[^\s'\"`<>,;(){}]+)+"),
            preview_builder=lambda match: match.group(),
            replacement_builder=lambda _match, placeholders: placeholders["windows_user_path"],
            priority=50,
            editable_in_place=True,
            review_required=False,
        ),
    ]
    return detectors
