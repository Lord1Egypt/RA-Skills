"""
Tencent Docs Markdown Skill - API Module

Provides all API operations for Tencent Docs Markdown:
- Create document
- Delete document
- Read document content
- Write/update document content
- Get document info
- Rename document
- Resolve real padId from document URL
"""

import re
import base64
import json
import random
import string
from urllib.parse import urlencode, urlparse

import requests

from .auth import get_cookie_string, get_xsrf_token

BASE_URL = 'https://docs.qq.com'
DEFAULT_DOMAIN_ID = '300000000'
DOC_TYPE_MARKDOWN = 14


def get_headers(cookies: list) -> dict:
    """Create common HTTP headers for API requests."""
    return {
        'Cookie': get_cookie_string(cookies),
        'Referer': f'{BASE_URL}/',
        'Origin': BASE_URL,
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ),
    }


def create_document(cookies: list, title: str, folder_id: str = '/') -> dict:
    """
    Create a new Markdown document on Tencent Docs.

    The real API uses query string parameters (not POST body).
    Key params: create_type=1, doc_type=14, folder_id=/, hum=1

    Args:
        cookies: Session cookies
        title: Document title
        folder_id: Target folder ID ('/' for root)

    Returns:
        dict with keys: docUrl, padId, globalPadId, title, raw
    """
    xsrf = get_xsrf_token(cookies)
    params = urlencode({
        'create_type': 1,
        'doc_type': DOC_TYPE_MARKDOWN,
        'folder_id': folder_id,
        'title': title or 'Untitled',
        'hum': 1,
        'dont_add_recent': 0,
        'xsrf': xsrf,
    })

    url = f'{BASE_URL}/cgi-bin/online_docs/createdoc_new?{params}'

    resp = requests.get(
        url,
        headers={
            **get_headers(cookies),
            'Accept': 'application/json, text/plain, */*',
        },
        timeout=30,
    )

    result = resp.json()
    if result.get('retcode') != 0:
        msg = result.get('msg') or f"retcode={result.get('retcode')}"
        raise RuntimeError(f"Failed to create document: {msg}")

    pad_id = ''
    doc_id = result.get('doc_id') or result.get('docId') or {}
    if isinstance(doc_id, dict):
        pad_id = doc_id.get('pad_id', '')

    doc_url = result.get('doc_url') or result.get('docUrl') or ''
    global_pad_id = result.get('global_pad_id') or f'{DEFAULT_DOMAIN_ID}{pad_id}'

    if doc_url.startswith('//'):
        doc_url = f'https:{doc_url}'

    return {
        'docUrl': doc_url,
        'padId': pad_id,
        'globalPadId': global_pad_id,
        'title': title,
        'raw': result,
    }


def delete_document(cookies: list, pad_id: str) -> dict:
    """
    Delete a Markdown document (move to trash).

    Args:
        cookies: Session cookies
        pad_id: Document pad ID

    Returns:
        API response dict
    """
    xsrf = get_xsrf_token(cookies)
    data = urlencode({
        'domain_id': DEFAULT_DOMAIN_ID,
        'pad_id': pad_id,
        'list_type': 1,
        'folder_id': '',
        'xsrf': xsrf,
    })

    resp = requests.post(
        f'{BASE_URL}/cgi-bin/online_docs/doc_delete',
        data=data,
        headers={
            **get_headers(cookies),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        timeout=30,
    )

    result = resp.json()
    if result.get('retcode') != 0:
        msg = result.get('msg') or f"retcode={result.get('retcode')}"
        raise RuntimeError(f"Failed to delete document: {msg}")

    return result


def read_document(cookies: list, file_id: str) -> str:
    """
    Read Markdown document content.

    Args:
        cookies: Session cookies
        file_id: Global pad ID (e.g. "300000000$xxxxx")

    Returns:
        Markdown text content
    """
    xsrf = get_xsrf_token(cookies)
    url = f'{BASE_URL}/api/markdown/read/data?xsrf={xsrf}'

    resp = requests.post(
        url,
        json={'file_id': file_id},
        headers={
            **get_headers(cookies),
            'Content-Type': 'application/json',
        },
        timeout=30,
    )

    result = resp.json()
    if result.get('retcode') != 0:
        msg = result.get('msg') or result.get('error_msg') or f"retcode={result.get('retcode')}"
        raise RuntimeError(f"Failed to read document: {msg}")

    return (result.get('result') or {}).get('mark_down', '')


def write_document(cookies: list, file_id: str, markdown_text: str) -> dict:
    """
    Write/update Markdown document content.

    Args:
        cookies: Session cookies
        file_id: Global pad ID (e.g. "300000000$xxxxx")
        markdown_text: Markdown content to write

    Returns:
        API response dict
    """
    xsrf = get_xsrf_token(cookies)
    url = f'{BASE_URL}/api/markdown/write/data?xsrf={xsrf}'

    resp = requests.post(
        url,
        json={
            'file_id': file_id,
            'mark_down': markdown_text,
        },
        headers={
            **get_headers(cookies),
            'Content-Type': 'application/json',
        },
        timeout=30,
    )

    result = resp.json()
    if result.get('retcode') != 0:
        msg = result.get('msg') or result.get('error_msg') or f"retcode={result.get('retcode')}"
        raise RuntimeError(f"Failed to write document: {msg}")

    return result


def get_document_info(cookies: list, doc_id: str) -> dict:
    """
    Get document metadata/info.

    Args:
        cookies: Session cookies
        doc_id: Document hash ID (from URL)

    Returns:
        Document info dict
    """
    xsrf = get_xsrf_token(cookies)
    url = f'{BASE_URL}/cgi-bin/online_docs/doc_info?xsrf={xsrf}'

    resp = requests.post(
        url,
        json={'file_id': doc_id},
        headers={
            **get_headers(cookies),
            'Content-Type': 'application/json',
        },
        timeout=30,
    )

    return resp.json()


def rename_document(cookies: list, pad_id: str, new_title: str) -> dict:
    """
    Rename a document.

    Args:
        cookies: Session cookies
        pad_id: Document pad ID
        new_title: New document title

    Returns:
        API response dict
    """
    xsrf = get_xsrf_token(cookies)

    # The real API passes all parameters via URL query string
    params = urlencode({
        'pad_id': pad_id,
        'domain_id': DEFAULT_DOMAIN_ID,
        'xsrf': xsrf,
        'version': 2,
        'auto_change': 0,
        'title': new_title,
    })

    url = f'{BASE_URL}/cgi-bin/online_docs/doc_changetitle?{params}'

    # Body is an empty multipart/form-data (matching the real browser request)
    boundary = '----WebKitFormBoundary' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    body = f'--{boundary}--\r\n'

    resp = requests.post(
        url,
        data=body,
        headers={
            **get_headers(cookies),
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': f'multipart/form-data; boundary={boundary}',
        },
        timeout=30,
    )

    result = resp.json()
    if result.get('retcode') != 0 and result.get('ret') != 0:
        msg = result.get('msg') or f"retcode={result.get('retcode')}"
        raise RuntimeError(f"Failed to rename document: {msg}")

    return result


def parse_pad_id_from_url(url: str) -> str:
    """
    Parse document URL to extract the URL hash identifier.

    Note: The URL hash (e.g. "DSFdDdHBqa2ZESUNw") is NOT the real padId.
    Use resolve_real_pad_id() to get the actual padId from the document page.

    Args:
        url: Tencent Docs Markdown URL (e.g. "https://docs.qq.com/markdown/xxxxx")

    Returns:
        Extracted URL hash identifier
    """
    # Handle URLs like:
    # https://docs.qq.com/markdown/DQxxxxx
    # //docs.qq.com/markdown/DQxxxxx
    match = re.search(r'/markdown/([A-Za-z0-9]+)', url)
    if match:
        return match.group(1)

    # Handle other URL patterns
    parts = [p for p in url.split('/') if p]
    return parts[-1] if parts else ''


def resolve_real_pad_id(cookies: list, doc_url: str) -> dict:
    """
    Resolve the real padId by fetching the document page and parsing basicClientVars.

    The URL hash identifier (from parse_pad_id_from_url) differs from the actual padId
    used by the read/write APIs. This function fetches the document HTML page and
    extracts the real padId from the embedded basicClientVars JSON.

    Args:
        cookies: Session cookies
        doc_url: Full Tencent Docs Markdown URL

    Returns:
        dict with keys: padId, globalPadId, title
    """
    # Security: Validate that doc_url targets an allowed hostname before attaching cookies
    ALLOWED_DOC_HOSTNAMES = ['docs.qq.com']
    try:
        parsed_doc_url = urlparse(doc_url)
        if parsed_doc_url.hostname not in ALLOWED_DOC_HOSTNAMES:
            raise RuntimeError(
                f"Security: Blocked cookie transmission to unauthorized hostname: "
                f"{parsed_doc_url.hostname}. Only docs.qq.com is allowed."
            )
    except RuntimeError:
        raise
    except Exception:
        raise RuntimeError(f"Invalid docUrl: {doc_url}")

    resp = requests.get(
        doc_url,
        headers={
            **get_headers(cookies),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        },
        timeout=30,
        allow_redirects=True,
    )

    html = resp.text

    # Extract base64-encoded basicClientVars from the page
    match = re.search(r"atob\('([^']+)'\)", html)
    if not match:
        raise RuntimeError('Cannot extract basicClientVars from document page')

    decoded = base64.b64decode(match.group(1)).decode('utf-8')
    client_vars = json.loads(decoded)

    pad_info = (client_vars.get('docInfo') or {}).get('padInfo')
    if not pad_info or not pad_info.get('padId'):
        raise RuntimeError('Cannot find padId in basicClientVars')

    pad_id = pad_info['padId']
    domain_id = pad_info.get('domainId', DEFAULT_DOMAIN_ID)
    separator = '$'
    global_pad_id = domain_id + separator + pad_id
    title = pad_info.get('padTitle', '')

    return {'padId': pad_id, 'globalPadId': global_pad_id, 'title': title}
