"""MCP Service Management Module

Provides functionality for:
- Downloading MCP binary files
- Port and process detection
- Service restart
"""

import os
import sys
import platform
import subprocess
import tarfile
import shutil
import time
import signal
from pathlib import Path
from typing import Optional, Tuple, Dict
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import json
import httpx


MCP_PORT = 18060
GITHUB_REPO = "xpzouying/xiaohongshu-mcp"
GITHUB_API_RELEASES = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


class MCPServiceManager:
    """MCP Service Manager"""
    
    def __init__(self, work_dir: Optional[str] = None):
        self.work_dir = Path(work_dir) if work_dir else Path.cwd()
        self.os_type, self.arch_type = self._detect_system()
        self.server_file = self._get_server_filename()
        self.login_file = self._get_login_filename()
    
    def _detect_system(self) -> Tuple[str, str]:
        """Detect OS type and architecture"""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == "linux":
            os_type = "linux"
        elif system == "darwin":
            os_type = "darwin"
        elif system in ("windows", "cygwin", "mingw", "msys_nt"):
            os_type = "windows"
        else:
            raise RuntimeError(f"Unsupported OS: {system}")
        
        if machine in ("x86_64", "amd64"):
            arch_type = "amd64"
        elif machine in ("aarch64", "arm64"):
            arch_type = "arm64"
        else:
            raise RuntimeError(f"Unsupported architecture: {machine}")
        
        return os_type, arch_type
    
    def _get_server_filename(self) -> str:
        """Get server binary filename"""
        if self.os_type == "windows":
            return f"xiaohongshu-mcp-{self.os_type}-{self.arch_type}.exe"
        return f"xiaohongshu-mcp-{self.os_type}-{self.arch_type}"
    
    def _get_login_filename(self) -> str:
        """Get login tool binary filename"""
        if self.os_type == "windows":
            return f"xiaohongshu-login-{self.os_type}-{self.arch_type}.exe"
        return f"xiaohongshu-login-{self.os_type}-{self.arch_type}"
    
    def _get_server_path(self) -> Path:
        """Get server binary full path"""
        return self.work_dir / self.server_file
    
    def _get_login_path(self) -> Path:
        """Get login tool binary full path"""
        return self.work_dir / self.login_file
    
    def check_binary_exists(self) -> Tuple[bool, bool]:
        """Check if binary files exist
        
        Returns:
            Tuple of (server_exists, login_exists)
        """
        server_path = self._get_server_path()
        login_path = self._get_login_path()
        return server_path.exists(), login_path.exists()
    
    def get_latest_version(self) -> str:
        """Get latest release version from GitHub"""
        request = Request(GITHUB_API_RELEASES)
        request.add_header("Accept", "application/vnd.github.v3+json")
        
        try:
            with urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
                tag_name = data.get("tag_name", "")
                if not tag_name:
                    raise RuntimeError("Unable to get latest version")
                return tag_name
        except (URLError, HTTPError) as e:
            raise RuntimeError(f"Failed to fetch latest version: {e}")
    
    def get_release_assets(self) -> dict:
        """Get release assets from GitHub API
        
        Returns:
            Dict mapping asset names to download URLs
        """
        request = Request(GITHUB_API_RELEASES)
        request.add_header("Accept", "application/vnd.github.v3+json")
        
        try:
            with urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
                assets = data.get("assets", [])
                return {asset["name"]: asset["browser_download_url"] for asset in assets}
        except (URLError, HTTPError) as e:
            raise RuntimeError(f"Failed to fetch release assets: {e}")
    
    def download_file(self, url: str, dest: Path) -> bool:
        """Download file from URL"""
        try:
            request = Request(url)
            with urlopen(request, timeout=300) as response:
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded = 0
                chunk_size = 8192
                with open(dest, "wb") as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\rDownloading: {progress:.1f}% ({downloaded}/{total_size} bytes)", end="", flush=True)
                    if total_size > 0:
                        print()
            return True
        except (URLError, HTTPError) as e:
            print(f"Download failed: {e}")
            return False
    
    def download_binaries(self, force: bool = False) -> bool:
        """Download MCP binary files
        
        Args:
            force: Force download even if files exist
            
        Returns:
            True if successful
        """
        server_exists, login_exists = self.check_binary_exists()
        
        if not force and server_exists and login_exists:
            print(f"Binary files already exist, skipping download")
            return True
        
        print(f"Detecting system: {self.os_type}, architecture: {self.arch_type}")
        
        assets = self.get_release_assets()
        
        server_pattern = f"xiaohongshu-mcp-{self.os_type}-{self.arch_type}"        
        server_file = None
        server_url = None
        
        for name, url in assets.items():
            if name.startswith(server_pattern):
                server_file = name
                server_url = url
        
        if not server_file or not server_url:
            raise RuntimeError(f"Server binary not found for {self.os_type}-{self.arch_type}")
        
        print(f"Latest version assets found:{server_file}")        
        server_path = self.work_dir / server_file
        print(f"Downloading: {server_url}")
        if not self.download_file(server_url, server_path):
            return False
        
        print("Extracting files...")
        try:
            if server_file.endswith(".zip"):
                import zipfile
                with zipfile.ZipFile(server_path, "r") as zip_ref:
                    zip_ref.extractall(self.work_dir)
            else:
                with tarfile.open(server_path, "r:gz") as tar:
                    tar.extractall(self.work_dir)
            server_path.unlink()
        except Exception as e:
            print(f"Extraction failed: {e}")
            return False
        
        if self.os_type != "windows":
            server_path = self._get_server_path()
            login_path = self._get_login_path()
            if server_path.exists():
                server_path.chmod(server_path.stat().st_mode | 0o755)
            if login_path.exists():
                login_path.chmod(login_path.stat().st_mode | 0o755)
        
        print(f"Download complete!")
        print(f"  Server: {self._get_server_path()}")
        print(f"  Login: {self._get_login_path()}")
        
        return True
    
    def check_port_in_use(self, port: int = MCP_PORT) -> Optional[int]:
        """Check if port is in use and return PID
        
        Args:
            port: Port number to check
            
        Returns:
            PID if port is in use, None otherwise
        """
        try:
            if self.os_type == "windows":
                result = subprocess.run(
                    ["netstat", "-ano"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                for line in result.stdout.split("\n"):
                    if f":{port}" in line and "LISTENING" in line:
                        parts = line.split()
                        if parts:
                            return int(parts[-1])
            else:
                result = subprocess.run(
                    ["lsof", "-ti", f":{port}"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return int(result.stdout.strip().split()[0])
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass
        
        return None
    
    def check_process_running(self, process_name: str = "xiaohongshu-mcp") -> Optional[int]:
        """Check if process is running
        
        Args:
            process_name: Process name to search for
            
        Returns:
            PID if process is running, None otherwise
        """
        try:
            if self.os_type == "windows":
                result = subprocess.run(
                    ["tasklist", "/FI", f"IMAGENAME eq {process_name}*", "/FO", "CSV", "/NH"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                for line in result.stdout.split("\n"):
                    if process_name in line.lower():
                        parts = line.split(",")
                        if len(parts) >= 2:
                            return int(parts[1].strip('"'))
            else:
                result = subprocess.run(
                    ["pgrep", "-f", process_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return int(result.stdout.strip().split()[0])
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass
        
        return None
    
    def kill_process(self, pid: int) -> bool:
        """Kill process by PID
        
        Args:
            pid: Process ID to kill
            
        Returns:
            True if successful
        """
        try:
            if self.os_type == "windows":
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], timeout=10)
            else:
                os.kill(pid, signal.SIGKILL)
            return True
        except (ProcessLookupError, PermissionError, subprocess.TimeoutExpired):
            return False
    
    def release_port(self, port: int = MCP_PORT) -> bool:
        """Release port by killing the process using it
        
        Args:
            port: Port number to release
            
        Returns:
            True if port was released or was already free
        """
        pid = self.check_port_in_use(port)
        if pid:
            print(f"Port {port} is in use by PID {pid}, terminating...")
            if self.kill_process(pid):
                time.sleep(2)
                print("Process terminated")
            else:
                print(f"Failed to terminate process {pid}")
                return False
        else:
            print(f"Port {port} is free")
        
        return self.check_port_in_use(port) is None
    
    def start_service(self, background: bool = True) -> bool:
        """Start MCP service
        
        Args:
            background: Run in background
            
        Returns:
            True if successful
        """
        server_path = self._get_server_path()
        if not server_path.exists():
            print(f"Server binary not found: {server_path}")
            print("Please run download first")
            return False
        
        if background:
            log_path = self.work_dir / "mcp.log"
            if self.os_type == "windows":
                subprocess.Popen(
                    [str(server_path)],
                    stdout=open(log_path, "w"),
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                    cwd=str(self.work_dir)
                )
            else:
                subprocess.Popen(
                    [str(server_path)],
                    stdout=open(log_path, "w"),
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                    cwd=str(self.work_dir)
                )
            
            time.sleep(3)
            
            pid = self.check_process_running()
            if pid:
                print(f"Service started, PID: {pid}")
                return True
            else:
                print("Failed to start service")
                if log_path.exists():
                    print(f"Check log: {log_path}")
                return False
        else:
            os.chdir(self.work_dir)
            os.execv(str(server_path), [str(server_path)])
    
    def stop_service(self) -> bool:
        """Stop MCP service
        
        Returns:
            True if successful
        """
        pid = self.check_process_running()
        if pid:
            print(f"Stopping service, PID: {pid}")
            if self.kill_process(pid):
                time.sleep(2)
                print("Service stopped")
                return True
            else:
                print("Failed to stop service")
                return False
        else:
            print("Service is not running")
            return True
    
    def restart_service(self) -> bool:
        """Restart MCP service
        
        Returns:
            True if successful
        """
        print(f"Checking port {MCP_PORT}...")
        if not self.release_port(MCP_PORT):
            print(f"Failed to release port {MCP_PORT}")
            return False
        
        print("Starting service...")
        return self.start_service()
    
    def get_service_status(self) -> dict:
        """Get service status
        
        Returns:
            Dict with status information
        """
        port_pid = self.check_port_in_use()
        process_pid = self.check_process_running()
        
        server_exists, login_exists = self.check_binary_exists()
        
        return {
            "port": MCP_PORT,
            "port_in_use": port_pid is not None,
            "port_pid": port_pid,
            "process_running": process_pid is not None,
            "process_pid": process_pid,
            "server_binary_exists": server_exists,
            "login_binary_exists": login_exists,
            "server_path": str(self._get_server_path()),
            "login_path": str(self._get_login_path()),
        }
    
    def test_connection(self) -> bool:
        """Test MCP connection using httpx (similar to start-service.sh)
        
        Returns:
            True if connection successful
        """
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"http://localhost:{MCP_PORT}/mcp",
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream"
                    },
                    json={
                        "jsonrpc": "2.0",
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {},
                            "clientInfo": {
                                "name": "test",
                                "version": "1.0"
                            }
                        },
                        "id": 1
                    }
                )
                
                # Check if we got a valid response with session ID
                if response.status_code == 200:
                    session_id = response.headers.get("Mcp-Session-Id")
                    if session_id:
                        print(f"MCP connection successful, Session: {session_id}")
                        return True
                    else:
                        # Even without session ID, 200 response means service is responding
                        print("MCP connection successful (no session ID)")
                        return True
                else:
                    print(f"MCP connection failed with status: {response.status_code}")
                    return False
                    
        except httpx.RequestError as e:
            print(f"MCP connection failed: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error testing MCP connection: {e}")
            return False
