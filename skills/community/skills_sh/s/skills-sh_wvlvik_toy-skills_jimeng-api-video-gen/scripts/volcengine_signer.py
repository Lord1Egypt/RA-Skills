#!/usr/bin/env python3
"""
Volcengine IAM v4 Signature Authentication
Based on official Volcengine HTTP request example
Reference: https://www.volcengine.com/docs/6444/1390583
"""

import hashlib
import hmac
import datetime
from typing import Dict, Optional


class VolcengineSigner:
    """Volcengine IAM v4 signature authentication"""

    ALGORITHM = "HMAC-SHA256"

    @staticmethod
    def sign_request(
        method: str,
        url: str,
        headers: Dict[str, str],
        body: bytes,
        access_key: str,
        secret_key: str,
        service: str = "cv",
        region: str = "cn-north-1",
        query_params: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """
        Sign HTTP request with Volcengine IAM v4 signature

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL path (without query string)
            headers: Request headers dict
            body: Request body as bytes
            access_key: Volcengine Access Key ID
            secret_key: Volcengine Secret Access Key
            service: Service name (default: cv for 即梦AI)
            region: Region name (default: cn-north-1)
            query_params: Query parameters dict (optional)

        Returns:
            Updated headers dict with X-Date and Authorization
        """
        # Get current UTC time
        now = datetime.datetime.utcnow()
        x_date = now.strftime("%Y%m%dT%H%M%SZ")
        short_date = x_date[:8]

        # Calculate payload hash
        payload_hash = hashlib.sha256(body).hexdigest()

        # Build headers dict - MUST include these headers per official docs
        headers = headers.copy()
        headers["X-Date"] = x_date
        headers["X-Content-Sha256"] = payload_hash

        # Signed headers MUST be in this exact order per official documentation
        # content-type;host;x-content-sha256;x-date
        signed_headers_list = ["content-type", "host", "x-content-sha256", "x-date"]

        # Build canonical query string
        canonical_query_string = ""
        if query_params:
            # Sort by parameter name and encode
            sorted_params = sorted(query_params.items())
            canonical_query_string = "&".join(
                f"{VolcengineSigner._uri_encode(str(k))}={VolcengineSigner._uri_encode(str(v))}"
                for k, v in sorted_params
            )

        # Build canonical headers string - must match signed_headers_list order
        canonical_headers_parts = []
        for h in signed_headers_list:
            if h == "content-type":
                canonical_headers_parts.append(
                    f"content-type:{headers.get('Content-Type', 'application/json')}"
                )
            elif h == "host":
                canonical_headers_parts.append(f"host:{headers.get('Host', '')}")
            elif h == "x-content-sha256":
                canonical_headers_parts.append(f"x-content-sha256:{payload_hash}")
            elif h == "x-date":
                canonical_headers_parts.append(f"x-date:{x_date}")

        canonical_headers = "\n".join(canonical_headers_parts) + "\n"
        signed_headers = ";".join(signed_headers_list)

        # Build canonical request
        canonical_request = "\n".join(
            [
                method,
                url,  # path
                canonical_query_string,  # query string
                canonical_headers,
                signed_headers,
                payload_hash,
            ]
        )

        # Calculate canonical request hash
        canonical_request_hash = hashlib.sha256(
            canonical_request.encode("utf-8")
        ).hexdigest()

        # Build string to sign
        credential_scope = f"{short_date}/{region}/{service}/request"
        string_to_sign = "\n".join(
            [
                VolcengineSigner.ALGORITHM,
                x_date,
                credential_scope,
                canonical_request_hash,
            ]
        )

        # Calculate signature
        signing_key = VolcengineSigner._get_signing_key(
            secret_key, short_date, region, service
        )
        signature = hmac.new(
            signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # Build Authorization header
        authorization = (
            f"{VolcengineSigner.ALGORITHM} "
            f"Credential={access_key}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, "
            f"Signature={signature}"
        )

        headers["Authorization"] = authorization
        return headers

    @staticmethod
    def _uri_encode(s: str) -> str:
        """URI encode following AWS v4 signing spec"""
        # Safe characters that don't need encoding
        safe = "-_.~"
        result = []
        for c in s:
            if c.isalnum() or c in safe:
                result.append(c)
            else:
                for byte in c.encode("utf-8"):
                    result.append(f"%{byte:02X}")
        return "".join(result)

    @staticmethod
    def _get_signing_key(
        secret_key: str, date: str, region: str, service: str
    ) -> bytes:
        """Derive signing key from secret key"""
        k_date = hmac.new(
            secret_key.encode("utf-8"), date.encode("utf-8"), hashlib.sha256
        ).digest()
        k_region = hmac.new(k_date, region.encode("utf-8"), hashlib.sha256).digest()
        k_service = hmac.new(k_region, service.encode("utf-8"), hashlib.sha256).digest()
        k_signing = hmac.new(k_service, b"request", hashlib.sha256).digest()
        return k_signing
