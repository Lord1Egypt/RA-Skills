from __future__ import annotations

import base64
import mimetypes
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

from qbo_mileage.config import EmailConfig
from qbo_mileage.http import request_json
from qbo_mileage.models import RunResult
from qbo_mileage.oauth import google_access_token, microsoft_access_token
from qbo_mileage.report import render_report


def maybe_send_email(config: EmailConfig, result: RunResult, attachments: list[Path]) -> None:
    if not config.enabled:
        return
    method = config.method.lower()
    if method == "smtp":
        send_smtp(config, result, attachments)
    elif method == "graph":
        send_graph(config, result, attachments)
    elif method == "gmail":
        send_gmail(config, result, attachments)
    else:
        raise ValueError(f"Unsupported email method: {config.method}")


def build_message(config: EmailConfig, result: RunResult, attachments: list[Path]) -> EmailMessage:
    if not config.to:
        raise ValueError("email.to is required when email is enabled")
    from_address = config.from_address or config.to
    message = EmailMessage()
    message["From"] = from_address
    message["To"] = config.to
    message["Subject"] = (
        f"Mileage CSV - {result.month} ({len(result.legs)} trips, {result.total_miles:.1f} mi)"
    )
    message.set_content(render_report(result))
    for path in attachments:
        data = path.read_bytes()
        mime_type, _ = mimetypes.guess_type(path.name)
        maintype, subtype = (mime_type or "application/octet-stream").split("/", 1)
        message.add_attachment(data, maintype=maintype, subtype=subtype, filename=path.name)
    return message


def send_smtp(config: EmailConfig, result: RunResult, attachments: list[Path]) -> None:
    settings = config.smtp
    host = settings.get("host")
    if not host:
        raise ValueError("email.smtp.host is required")
    port = int(settings.get("port", 587))
    message = build_message(config, result, attachments)
    with smtplib.SMTP(str(host), port, timeout=60) as smtp:
        if settings.get("starttls", True):
            # Explicit context so the server certificate is always verified,
            # regardless of Python version defaults.
            smtp.starttls(context=ssl.create_default_context())
        username = settings.get("username")
        password = settings.get("password")
        if username:
            smtp.login(str(username), str(password or ""))
        smtp.send_message(message)


def send_graph(config: EmailConfig, result: RunResult, attachments: list[Path]) -> None:
    token = _graph_token(config)
    message = _graph_message_payload(config, result, attachments)
    request_json(
        "POST",
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers={"Authorization": f"Bearer {token}"},
        body={"message": message, "saveToSentItems": True},
        timeout=60,
    )


def send_gmail(config: EmailConfig, result: RunResult, attachments: list[Path]) -> None:
    token = _gmail_token(config)
    raw = base64.urlsafe_b64encode(build_message(config, result, attachments).as_bytes()).decode("ascii")
    request_json(
        "POST",
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        headers={"Authorization": f"Bearer {token}"},
        body={"raw": raw},
        timeout=60,
    )


def _graph_token(config: EmailConfig) -> str:
    settings = config.graph
    if settings.get("access_token"):
        return str(settings["access_token"])
    return microsoft_access_token(
        str(settings.get("client_id", "")),
        str(settings.get("refresh_token", "")),
        tenant_id=str(settings.get("tenant_id", "consumers")),
        client_secret=settings.get("client_secret"),
        scope=str(settings.get("scope", "offline_access Mail.Send")),
    )


def _gmail_token(config: EmailConfig) -> str:
    settings = config.gmail
    if settings.get("access_token"):
        return str(settings["access_token"])
    return google_access_token(
        str(settings.get("client_id", "")),
        str(settings.get("client_secret", "")),
        str(settings.get("refresh_token", "")),
    )


def _graph_message_payload(config: EmailConfig, result: RunResult, attachments: list[Path]) -> dict:
    return {
        "subject": f"Mileage CSV - {result.month} ({len(result.legs)} trips, {result.total_miles:.1f} mi)",
        "body": {"contentType": "Text", "content": render_report(result)},
        "toRecipients": [{"emailAddress": {"address": config.to}}],
        "attachments": [_graph_attachment(path) for path in attachments],
    }


def _graph_attachment(path: Path) -> dict:
    return {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": path.name,
        "contentBytes": base64.b64encode(path.read_bytes()).decode("ascii"),
    }
