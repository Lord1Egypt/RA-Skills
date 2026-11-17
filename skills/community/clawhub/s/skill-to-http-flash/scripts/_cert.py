#!/usr/bin/env python3
"""skill-to-http-flash v2.0 bundled cert helper.

精简版自签名证书生成器，独立实现，不依赖 skill-to-http 的 tls_auth / gen_cert。
用法（在 flash.py cert --cert-action renew 中调）：

    from _cert import generate_self_signed_cert
    generate_self_signed_cert(cert_path, key_path, common_name="flash-foo")

如果 openssl CLI 可用就走 openssl SAN 自签证书；
否则 fallback 到 python cryptography 库（与 server_template 内嵌实现一致）。
"""

from __future__ import annotations

import ipaddress
import os
import shutil
import socket
import subprocess
from pathlib import Path


def detect_local_ips() -> list[str]:
    """返回本机 IP 列表（不含 127.0.0.1）。"""
    ips: list[str] = []
    seen = {"127.0.0.1", "::1"}
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            if ip and ip not in seen:
                ips.append(ip)
                seen.add(ip)
    except Exception:
        pass
    try:
        hostname = socket.gethostname()
        for addr in socket.getaddrinfo(hostname, None):
            ip = addr[4][0].split("%")[0]
            if ip and ip not in seen:
                try:
                    parsed = ipaddress.ip_address(ip)
                    if not parsed.is_loopback:
                        ips.append(ip)
                        seen.add(ip)
                except ValueError:
                    pass
    except Exception:
        pass
    return ips


def generate_self_signed_cert(
    cert_path: Path,
    key_path: Path,
    common_name: str = "localhost",
    validity_days: int = 825,
) -> None:
    """Generate self-signed cert with SAN entries (local IPs + 127.0.0.1 + localhost).

    Strategy: prefer openssl CLI (smaller deps), fall back to cryptography.
    """
    cert_path = Path(cert_path)
    key_path = Path(key_path)
    cert_path.parent.mkdir(parents=True, exist_ok=True)

    if shutil.which("openssl"):
        _generate_with_openssl(cert_path, key_path, common_name, validity_days)
    else:
        _generate_with_cryptography(cert_path, key_path, common_name, validity_days)


def _generate_with_openssl(
    cert_path: Path,
    key_path: Path,
    common_name: str,
    validity_days: int,
) -> None:
    cert_dir = cert_path.parent
    ips = detect_local_ips()
    san_lines = []
    for i, ip in enumerate(ips, 1):
        san_lines.append(f"IP.{i} = {ip}")
    san_lines.append(f"IP.{len(ips) + 1} = 127.0.0.1")
    san_lines.append("DNS.1 = localhost")

    conf = f"""[req]
distinguished_name = req_dn
req_extensions = v3_req
prompt = no
[req_dn]
C = CN
O = OpenClaw
CN = {common_name}
[v3_req]
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
{chr(10).join(san_lines)}
"""
    conf_path = cert_dir / "openssl.cnf"
    conf_path.write_text(conf)

    try:
        subprocess.run(
            ["openssl", "genrsa", "-out", str(key_path), "2048"],
            check=True, capture_output=True,
        )
        os.chmod(key_path, 0o600)
        subprocess.run(
            [
                "openssl", "req", "-x509", "-new", "-nodes",
                "-key", str(key_path), "-sha256",
                "-days", str(validity_days),
                "-out", str(cert_path),
                "-config", str(conf_path),
                "-extensions", "v3_req",
            ],
            check=True, capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode() if e.stderr else ""
        raise RuntimeError(f"openssl failed: {stderr}") from e


def _generate_with_cryptography(
    cert_path: Path,
    key_path: Path,
    common_name: str,
    validity_days: int,
) -> None:
    """Fallback: 用 python cryptography 库生成（无需 openssl CLI）。"""
    import datetime
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend
        from cryptography.x509.oid import NameOID
    except ImportError as e:
        raise RuntimeError(
            "Neither openssl CLI nor python cryptography is available. "
            "Install with: pip install cryptography"
        ) from e

    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "OpenClaw"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    san_entries: list = [
        x509.DNSName("localhost"),
        x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
    ]
    for ip in detect_local_ips():
        try:
            san_entries.append(x509.IPAddress(ipaddress.ip_address(ip)))
        except ValueError:
            pass

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=validity_days)
        )
        .add_extension(x509.SubjectAlternativeName(san_entries), critical=False)
        .sign(private_key, hashes.SHA256(), default_backend())
    )

    _pem = getattr(serialization, "Encoding").PEM
    key_path.write_bytes(private_key.private_bytes(
        encoding=_pem,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    key_path.chmod(0o600)
    cert_path.write_bytes(cert.public_bytes(_pem))


if __name__ == "__main__":
    # Quick self-test
    import sys
    out_dir = Path("/tmp/flash-cert-test")
    out_dir.mkdir(parents=True, exist_ok=True)
    cert = out_dir / "server.crt"
    key = out_dir / "server.key"
    generate_self_signed_cert(cert, key, common_name="flash-selftest")
    print(f"✅ cert: {cert} ({cert.stat().st_size}B)")
    print(f"✅ key : {key} ({key.stat().st_size}B, mode={oct(key.stat().st_mode & 0o777)})")
