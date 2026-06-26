#!/usr/bin/env python3
"""
http_transfer.py — agent 通过 TunnelProxy HTTP 接口传输文件

用法：
    export TUNNEL_HOST="<用户提供的地址>"
    export TUNNEL_HTTP_PORT="<用户提供的端口>"
    
    from http_transfer import TunnelHTTP
    http = TunnelHTTP()
    http.download("/path/on/remote/file.txt", "/workspace/file.txt")
"""
import os
import sys
import urllib.request
import urllib.error
import pathlib

# 默认本地，用户必须通过环境变量覆盖
HOST = os.environ.get("TUNNEL_HOST", "127.0.0.1")
HTTP_PORT = int(os.environ.get("TUNNEL_HTTP_PORT", "8080"))
TIMEOUT = int(os.environ.get("TUNNEL_TIMEOUT", "60"))


class TunnelHTTP:
    def __init__(self, host=None, port=None, timeout=TIMEOUT):
        self.host = host or HOST
        self.port = port or HTTP_PORT
        self.base_url = f"http://{self.host}:{self.port}"
        self.timeout = timeout

    def ping(self) -> bool:
        try:
            urllib.request.urlopen(self.base_url + "/", timeout=5)
            return True
        except Exception:
            return False

    def list_files(self, path: str = "/") -> str:
        url = self.base_url + "/" + path.lstrip("/")
        r = urllib.request.urlopen(url, timeout=self.timeout)
        return r.read().decode("utf-8", errors="replace")

    def download(self, remote_path: str, local_path: str) -> int:
        url = self.base_url + "/" + remote_path.lstrip("/")
        r = urllib.request.urlopen(url, timeout=self.timeout)
        data = r.read()
        pathlib.Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(data)
        return len(data)

    def upload(self, local_path: str) -> str:
        filename = os.path.basename(local_path)
        with open(local_path, "rb") as f:
            data = f.read()

        boundary = "----TunnelProxyBoundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + data + f"\r\n--{boundary}--\r\n".encode()

        req = urllib.request.Request(
            self.base_url + "/upload",
            data=body,
            method="POST",
        )
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

        try:
            r = urllib.request.urlopen(req, timeout=self.timeout)
            return r.read().decode("utf-8", errors="replace").strip()
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"上传失败 HTTP {e.code}: {e.read().decode()[:200]}")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "ping"
    http = TunnelHTTP()

    if action == "ping":
        print("✅ 可达" if http.ping() else "❌ 不可达")
    elif action == "download" and len(sys.argv) == 4:
        size = http.download(sys.argv[2], sys.argv[3])
        print(f"✅ 已下载 {size} bytes → {sys.argv[3]}")
    elif action == "upload" and len(sys.argv) == 3:
        resp = http.upload(sys.argv[2])
        print(f"✅ 已上传 → {resp}")
    else:
        print("用法:")
        print("  export TUNNEL_HOST='<用户提供的地址>'")
        print("  export TUNNEL_HTTP_PORT='<用户提供的端口>'")
        print("  python3 http_transfer.py ping")
        print("  python3 http_transfer.py download <remote_path> <local_path>")
        print("  python3 http_transfer.py upload <local_path>")