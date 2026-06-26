"""Notification callbacks for lint report delivery."""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable

from pylinter_assist.github_actions import WorkflowRunInfo
from pylinter_assist.linter import LintReport
from pylinter_assist.reporter import render


@dataclass
class NotificationMessage:
    """A notification message to be sent."""

    channel: str
    title: str
    content: str
    attachments: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class NotificationCallback(ABC):
    """Abstract base class for notification channels."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the channel name."""
        pass

    @abstractmethod
    def send(self, message: NotificationMessage) -> bool:
        """Send a notification message.

        Args:
            message: The message to send

        Returns:
            True if sent successfully, False otherwise
        """
        pass


class TelegramNotifier(NotificationCallback):
    """Send notifications via Telegram bot."""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    @property
    def name(self) -> str:
        return "telegram"

    def _request(self, endpoint: str, data: dict, timeout: int = 30) -> bool:
        """Make a Telegram API request."""
        import requests  # noqa: PLC0415

        url = f"{self.base_url}/{endpoint}"
        try:
            resp = requests.post(url, json=data, timeout=timeout)
            resp.raise_for_status()
            return resp.json().get("ok", False)
        except requests.exceptions.RequestException:
            return False

    def send(self, message: NotificationMessage) -> bool:
        """Send notification via Telegram.

        Args:
            message: Notification message (content should be formatted for Telegram)

        Returns:
            True if sent successfully, False otherwise
        """
        # Telegram has a 4096 character limit per message
        # Split into multiple messages if needed
        content = message.content[:4096]
        remaining = message.content[4096:]

        payload = {
            "chat_id": self.chat_id,
            "text": content,
            "parse_mode": "Markdown",
        }

        success = True
        if not self._request("sendMessage", payload):
            success = False

        # Send remaining parts if message was split
        while remaining:
            payload["text"] = remaining[:4096]
            remaining = remaining[4096:]
            if not self._request("sendMessage", payload):
                success = False

        return success


class DiscordNotifier(NotificationCallback):
    """Send notifications via Discord webhook."""

    def __init__(self, webhook_url: str, username: str | None = None):
        self.webhook_url = webhook_url
        self.username = username

    @property
    def name(self) -> str:
        return "discord"

    def send(self, message: NotificationMessage) -> bool:
        """Send notification via Discord webhook.

        Args:
            message: Notification message

        Returns:
            True if sent successfully, False otherwise
        """
        import requests  # noqa: PLC0415

        payload = {
            "username": self.username or "Lint Bot",
            "embeds": [
                {
                    "title": message.title,
                    "description": message.content[:4096] if len(message.content) > 4096 else message.content,
                    "color": 10038562,  # Blue color for info
                    "footer": {
                        "text": f"Sent via pylinter-assist | {message.channel}",
                    },
                    **message.metadata,
                }
            ],
        }

        try:
            resp = requests.post(
                self.webhook_url, json=payload, timeout=30
            )
            resp.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False


class SlackNotifier(NotificationCallback):
    """Send notifications via Slack webhook."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    @property
    def name(self) -> str:
        return "slack"

    def send(self, message: NotificationMessage) -> bool:
        """Send notification via Slack webhook.

        Args:
            message: Notification message

        Returns:
            True if sent successfully, False otherwise
        """
        import requests  # noqa: PLC0415

        payload = {
            "text": f"*{message.title}*",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": message.title,
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message.content[:3000] if len(message.content) > 3000 else message.content,
                    },
                },
            ],
        }

        try:
            resp = requests.post(
                self.webhook_url, json=payload, timeout=30
            )
            resp.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False


class EmailNotifier(NotificationCallback):
    """Send notifications via email (SMTP)."""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_address: str,
        to_addresses: list[str],
        use_tls: bool = True,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.use_tls = use_tls

    @property
    def name(self) -> str:
        return "email"

    def send(self, message: NotificationMessage) -> bool:
        """Send notification via email.

        Args:
            message: Notification message

        Returns:
            True if sent successfully, False otherwise
        """
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg["From"] = self.from_address
        msg["To"] = ", ".join(self.to_addresses)
        msg["Subject"] = message.title

        msg.attach(MIMEText(message.content, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if self.use_tls:
                server.starttls()
            if self.username and self.password:
                server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception:
            return False


def create_notifier_from_config(config: dict[str, Any]) -> NotificationCallback | None:
    """Create a notifier instance from configuration.

    Args:
        config: Configuration dictionary with channel settings

    Returns:
        NotificationCallback instance or None if invalid config
    """
    channel_type = config.get("type")

    if channel_type == "telegram":
        bot_token = config.get("bot_token")
        chat_id = config.get("chat_id")
        if not bot_token or not chat_id:
            return None
        return TelegramNotifier(bot_token, str(chat_id))

    elif channel_type == "discord":
        webhook_url = config.get("webhook_url")
        if not webhook_url:
            return None
        return DiscordNotifier(
            webhook_url, config.get("username")
        )

    elif channel_type == "slack":
        webhook_url = config.get("webhook_url")
        if not webhook_url:
            return None
        return SlackNotifier(webhook_url)

    elif channel_type == "email":
        return EmailNotifier(
            config.get("smtp_server", ""),
            config.get("smtp_port", 587),
            config.get("username", ""),
            config.get("password", ""),
            config.get("from_address", ""),
            config.get("to_addresses", []),
            config.get("use_tls", True),
        )

    return None


def format_report_for_notification(
    report: LintReport, run_info: WorkflowRunInfo | None = None
) -> NotificationMessage:
    """Format a lint report as a notification message.

    Args:
        report: The lint report to format
        run_info: Optional workflow run information

    Returns:
        Formatted NotificationMessage
    """
    # Generate markdown summary
    md_output = render(report, fmt="markdown", include_info=True)

    # Create a concise summary for the message header
    error_count = len(report.by_severity.get("error", []))
    warning_count = len(report.by_severity.get("warning", []))
    info_count = len(report.by_severity.get("info", []))

    title_parts = ["Lint Report"]
    if run_info:
        title_parts.append(f"for {run_info.run.head_branch}")
        title_parts.append(f"#{run_info.run.id}")
    title = " ".join(title_parts)

    # Create a concise summary
    summary_lines = [
        f"**Files checked:** {len(report.files_checked)}",
        f"**Errors:** {error_count}",
        f"**Warnings:** {warning_count}",
        f"**Info:** {info_count}",
        "",
        "See full report below:",
        "",
    ]

    summary = "\n".join(summary_lines)

    return NotificationMessage(
        channel="lint-report",
        title=title,
        content=summary + md_output,
        metadata={
            "error_count": error_count,
            "warning_count": warning_count,
            "info_count": info_count,
            "files_checked": len(report.files_checked),
        },
    )


def send_notifications(
    report: LintReport,
    run_info: WorkflowRunInfo | None = None,
    channels: list[dict[str, Any]] | None = None,
    fallback_to_stdout: bool = True,
) -> dict[str, bool]:
    """Send notifications to multiple channels.

    Args:
        report: The lint report to send
        run_info: Optional workflow run information
        channels: List of channel configurations
        fallback_to_stdout: Whether to print to stdout if all channels fail

    Returns:
        Dictionary mapping channel names to success status
    """
    message = format_report_for_notification(report, run_info)
    results: dict[str, bool] = {}

    if not channels:
        if fallback_to_stdout:
            print(message.content)
        return {"none": True}

    for channel_config in channels:
        notifier = create_notifier_from_config(channel_config)
        if not notifier:
            results[channel_config.get("type", "unknown")] = False
            continue

        success = notifier.send(message)
        results[channel_config["type"]] = success

    # Fallback to stdout if all channels failed
    if fallback_to_stdout and not any(results.values()):
        print(message.content)

    return results
