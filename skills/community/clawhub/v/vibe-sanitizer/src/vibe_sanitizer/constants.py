from __future__ import annotations

DEFAULT_CONFIG_FILE = ".vibe-sanitizer.yml"

DEFAULT_PLACEHOLDERS = {
    "openai_key": "<REDACTED_OPENAI_KEY>",
    "aws_access_key": "<REDACTED_AWS_ACCESS_KEY>",
    "github_token": "<REDACTED_GITHUB_TOKEN>",
    "slack_token": "<REDACTED_SLACK_TOKEN>",
    "bearer_token": "<REDACTED_BEARER_TOKEN>",
    "private_key_block": "<REDACTED_PRIVATE_KEY_BLOCK>",
    "credential_url_user": "<REDACTED_USER>",
    "credential_url_password": "<REDACTED_PASSWORD>",
    "generic_secret": "<REDACTED_SECRET>",
    "workspace_path": "<WORKSPACE_PATH>",
    "home_path": "<HOME_PATH>",
    "temp_path": "<TEMP_PATH>",
    "windows_user_path": "<WINDOWS_USER_PATH>",
}

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_ERROR = 2

SUPPORTED_SCOPES = ("working-tree", "tracked", "staged", "commit")
