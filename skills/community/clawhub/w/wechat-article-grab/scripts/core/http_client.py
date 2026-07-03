"""HTTP client with SNI bypass for anti-crawling circumvention."""

import gzip
import socket
import ssl
import json
from typing import Dict, Any, Optional
from urllib.parse import quote


def decode_chunked(data: bytes) -> bytes:
    """Decode chunked transfer encoding."""
    chunks = []
    idx = 0

    while idx < len(data):
        line_end = data.find(b'\r\n', idx)
        if line_end == -1:
            break

        chunk_size_line = data[idx:line_end]
        try:
            chunk_size = int(chunk_size_line, 16)
        except Exception:
            break

        if chunk_size == 0:
            break

        chunk_start = line_end + 2
        chunk_end = chunk_start + chunk_size

        if chunk_end > len(data):
            break

        chunk = data[chunk_start:chunk_end]
        chunks.append(chunk)
        idx = chunk_end + 2

    return b''.join(chunks)


class NoSNIClient:
    """HTTP client using raw sockets without SNI for anti-crawling bypass."""

    def __init__(self, timeout: int = 60) -> None:
        """Initialize client with timeout."""
        self.timeout = timeout

    def fetch_json(
        self,
        url: str,
        params: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """Fetch JSON response from URL.

        Args:
            url: The URL path (e.g., "onetotenvip.com/skill/cozeSkill/getWxCozeSkillData")
            params: Query parameters
            headers: HTTP headers

        Returns:
            Parsed JSON response

        Raises:
            socket.timeout: On connection timeout
            OSError: On connection error
            json.JSONDecodeError: On invalid JSON response
        """
        text = self.fetch_text(url, params, headers)
        return json.loads(text)

    def fetch_text(
        self,
        url: str,
        params: Dict[str, Any],
        headers: Dict[str, str]
    ) -> str:
        """Fetch text response from URL using raw socket (no SNI).

        Args:
            url: The URL path (e.g., "onetotenvip.com/skill/cozeSkill/getWxCozeSkillData")
            params: Query parameters
            headers: HTTP headers

        Returns:
            Response body as string

        Raises:
            socket.timeout: On connection timeout
            OSError: On connection error
        """
        # Parse URL - strip protocol if present
        if "://" in url:
            url = url.split("://", 1)[1]
        if "/" in url:
            host, path = url.split("/", 1)
        else:
            host = url
            path = ""

        # Build query string
        if params:
            query = "&".join(
                f"{quote(str(k))}={quote(str(v))}" for k, v in params.items()
            )
            path = f"{path}?{query}"

        # Create raw socket connection
        sock = socket.create_connection((host, 443), timeout=self.timeout)

        # Create SSL context without SNI
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        ssl_sock = context.wrap_socket(sock, server_hostname=None)

        # Build HTTP request
        request_lines = [
            f"GET /{path} HTTP/1.1",
            f"Host: {host}",
        ]
        for k, v in headers.items():
            request_lines.append(f"{k}: {v}")
        request_lines.extend(["", ""])

        request = "\r\n".join(request_lines)
        ssl_sock.send(request.encode())

        # Receive response
        response_data = b""
        while True:
            try:
                chunk = ssl_sock.recv(8192)
                if not chunk:
                    break
                response_data += chunk
            except Exception:
                break

        ssl_sock.close()

        # Parse response
        response_str = response_data.decode('utf-8', errors='ignore')
        lines = response_str.split('\r\n')
        status_code = int(lines[0].split()[1])

        # Parse headers
        headers_dict: Dict[str, str] = {}
        for line in lines[1:]:
            if line == '':
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers_dict[key.strip().lower()] = value.strip()

        # Extract body
        header_end = response_data.find(b'\r\n\r\n')
        body_bytes = response_data[header_end + 4:] if header_end != -1 else b""

        # Decode chunked transfer encoding
        if headers_dict.get('transfer-encoding', '').lower() == 'chunked':
            body_bytes = decode_chunked(body_bytes)

        # Decompress gzip if needed
        if headers_dict.get('content-encoding', '').lower() == 'gzip':
            try:
                body_bytes = gzip.decompress(body_bytes)
            except Exception:
                pass

        return body_bytes.decode('utf-8', errors='ignore')