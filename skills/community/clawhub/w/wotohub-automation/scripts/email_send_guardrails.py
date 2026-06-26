#!/usr/bin/env python3
from __future__ import annotations

import re
from typing import Any

from html_email_utils import normalize_email_content, contains_cjk


def norm_person_name(value: str) -> str:
    value = str(value or '').strip().lower()
    return re.sub(r'[^a-z0-9]+', '', value)


def subject_tail_name(subject: str) -> str:
    text = str(subject or '').strip()
    if not text:
        return ''
    for sep in (' x ', ' — ', ' - '):
        if sep in text:
            tail = text.split(sep)[-1].strip()
            return norm_person_name(tail)
    return ''


def opening_name(body_text: str) -> str:
    text = str(body_text or '').strip()
    if not text:
        return ''
    first_line = text.splitlines()[0].strip()
    m = re.match(r'^(hi|hello|dear)\s+(.+?)[,，:：!?!.]*$', first_line, flags=re.I)
    if not m:
        return ''
    return norm_person_name(m.group(2).strip())


def normalize_email_artifact_for_send(email: dict[str, Any], expected_language: str = 'en') -> dict[str, Any]:
    subject = str(email.get('subject') or '').strip()
    normalized = normalize_email_content(
        html_body=email.get('htmlBody'),
        plain_text_body=email.get('plainTextBody'),
        body=email.get('body'),
    )

    errors: list[str] = []
    warnings: list[str] = []

    if not subject:
        errors.append('missing_subject')
    if not normalized.get('plainTextBody'):
        errors.append('missing_body')
    if expected_language == 'en' and contains_cjk(subject):
        errors.append('subject_language_mismatch')

    nickname = str(email.get('nickname') or '').strip()
    nickname_norm = norm_person_name(nickname)
    subject_name_norm = subject_tail_name(subject)
    if nickname_norm and subject_name_norm and nickname_norm != subject_name_norm:
        errors.append('subject_blogger_mismatch')

    opening_name_norm = opening_name(normalized.get('plainTextBody') or '')
    if nickname_norm and opening_name_norm and nickname_norm != opening_name_norm:
        errors.append('body_greeting_blogger_mismatch')

    return {
        'ok': len(errors) == 0,
        'subject': subject,
        'htmlBody': normalized.get('htmlBody'),
        'plainTextBody': normalized.get('plainTextBody'),
        'errors': errors,
        'warnings': warnings,
    }


def validate_reply_preview_identity(reply_preview: dict[str, Any]) -> dict[str, Any]:
    nickname = str(reply_preview.get('nickname') or '').strip()
    opening_name_norm = opening_name(reply_preview.get('plainTextBody') or reply_preview.get('body') or '')
    if nickname and opening_name_norm and norm_person_name(nickname) != opening_name_norm:
        return {
            'ok': False,
            'reason': 'reply_body_greeting_blogger_mismatch',
        }
    return {
        'ok': True,
        'reason': None,
    }
