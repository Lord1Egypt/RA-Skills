#!/usr/bin/env python3
"""
Direct TCP client for RhinoClaw plugin.
Bypasses the MCP server layer for direct Clawdbot integration.
"""

import socket
import json
import logging
import os
import sys
import time
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Optional

# Configure logging based on RHINOMCP_DEBUG env var
_log_level = logging.DEBUG if os.getenv("RHINOMCP_DEBUG") else logging.WARNING
logging.basicConfig(
    level=_log_level,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("rhinoclaw")

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.json"

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}

CONFIG = load_config()
CONNECTION = CONFIG.get("connection", {})

# Defaults from config
DEFAULT_HOST = CONNECTION.get("host", "172.31.96.1")
DEFAULT_PORT = CONNECTION.get("port", 1999)
DEFAULT_TIMEOUT = CONNECTION.get("timeout", 15.0)
DEFAULT_RETRIES = CONNECTION.get("max_retries", 3)
DEFAULT_RETRY_DELAY = CONNECTION.get("retry_delay", 1.0)


# --- Custom Exceptions ---

class RhinoClawError(Exception):
    """Base exception for RhinoClaw."""
    pass

class RhinoConnectionError(RhinoClawError):
    """Could not connect to Rhino."""
    pass

class RhinoTimeoutError(RhinoClawError):
    """Operation timed out."""
    pass

class RhinoCommandError(RhinoClawError):
    """Rhino returned an error."""
    def __init__(self, message: str, command: str = None, details: dict = None):
        super().__init__(message)
        self.command = command
        self.details = details or {}

class ValidationError(RhinoClawError):
    """Invalid parameters."""
    pass


# --- Retry Decorator ---

def with_retry(max_retries: int = None, delay: float = None,
               exceptions: tuple = (RhinoConnectionError, RhinoTimeoutError)):
    """Decorator for automatic retry with exponential backoff."""
    _max = max_retries if max_retries is not None else DEFAULT_RETRIES
    _delay = delay if delay is not None else DEFAULT_RETRY_DELAY

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(_max):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    if attempt < _max - 1:
                        wait = _delay * (2 ** attempt)
                        logger.warning(f"Retry {attempt + 1}/{_max} after {wait:.1f}s: {e}")
                        time.sleep(wait)
            raise last_error
        return wrapper
    return decorator


__all__ = ['RhinoClient', 'get_client', 'RhinoClawError', 'RhinoConnectionError',
           'RhinoTimeoutError', 'RhinoCommandError', 'ValidationError', 'with_retry']


class RhinoClient:
    """TCP client for communicating with RhinoClaw plugin."""
    
    def __init__(self, host: str = None, port: int = None, timeout: float = None):
        self.host = host or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.sock: Optional[socket.socket] = None
    
    def connect(self) -> bool:
        """Connect to Rhino plugin.
        
        Returns:
            True on success.
        
        Raises:
            RhinoConnectionError: If connection fails.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            logger.debug(f"Connecting to {self.host}:{self.port}")
            self.sock.connect((self.host, self.port))
            return True
        except socket.timeout as e:
            logger.error(f"Connection timed out: {e}")
            self.sock = None
            raise RhinoConnectionError(f"Connection timed out to {self.host}:{self.port}: {e}") from e
        except (socket.error, ConnectionError, OSError) as e:
            logger.error(f"Connection failed: {e}")
            self.sock = None
            raise RhinoConnectionError(f"Could not connect to Rhino at {self.host}:{self.port}: {e}") from e
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.sock = None
            raise RhinoConnectionError(f"Connection failed: {e}") from e
    
    def disconnect(self):
        """Close the connection."""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None
    
    def send_command(self, cmd_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a command and receive the response.
        
        Raises:
            RhinoConnectionError: If not connected or connection lost.
            RhinoTimeoutError: If the operation times out.
            RhinoCommandError: If Rhino returns an error response.
        """
        if not self.sock:
            raise RhinoConnectionError("Not connected to Rhino")
        
        command = {
            "type": cmd_type,
            "params": params or {}
        }
        
        try:
            # Send command
            cmd_json = json.dumps(command)
            self.sock.sendall(cmd_json.encode('utf-8'))
            
            # Receive response (handle chunked data)
            chunks = []
            while True:
                try:
                    chunk = self.sock.recv(8192)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    
                    # Try to parse as complete JSON
                    try:
                        data = b''.join(chunks)
                        result = json.loads(data.decode('utf-8'))
                        # Check for error response
                        if result.get('status') == 'error':
                            raise RhinoCommandError(
                                result.get('message', 'Unknown error'),
                                command=cmd_type,
                                details=result
                            )
                        return result
                    except json.JSONDecodeError:
                        continue  # Incomplete, keep receiving
                        
                except socket.timeout:
                    break
            
            if chunks:
                data = b''.join(chunks)
                try:
                    result = json.loads(data.decode('utf-8'))
                    if result.get('status') == 'error':
                        raise RhinoCommandError(
                            result.get('message', 'Unknown error'),
                            command=cmd_type,
                            details=result
                        )
                    return result
                except json.JSONDecodeError:
                    raise RhinoCommandError(
                        f"Invalid JSON response: {data[:200]}",
                        command=cmd_type
                    )
            
            raise RhinoTimeoutError(f"No response received for '{cmd_type}'")
        
        except socket.timeout as e:
            raise RhinoTimeoutError(f"Timeout waiting for response to '{cmd_type}': {e}") from e
        except (socket.error, ConnectionError, OSError) as e:
            raise RhinoConnectionError(f"Connection lost during '{cmd_type}': {e}") from e
        except (RhinoClawError,):
            raise  # Re-raise our own exceptions
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, *args):
        self.disconnect()


def get_client() -> RhinoClient:
    """Get a connected RhinoClient instance.
    
    Raises:
        RhinoConnectionError: If connection fails.
    """
    client = RhinoClient()
    client.connect()  # Raises RhinoConnectionError on failure
    return client


# CLI interface
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='RhinoClaw Client')
    parser.add_argument('command', help='Command: ping, info, or raw command type')
    parser.add_argument('--params', '-p', type=str, help='JSON params', default='{}')
    parser.add_argument('--host', default=None, help=f'Host (default: {DEFAULT_HOST})')
    parser.add_argument('--port', type=int, default=None, help=f'Port (default: {DEFAULT_PORT})')
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON params: {e}")
        sys.exit(1)
    
    # All commands use the same client with host/port from args or config
    with RhinoClient(args.host, args.port) as client:
        if args.command == 'ping':
            result = client.send_command("ping")
        elif args.command == 'info':
            result = client.send_command("get_document_info")
        else:
            result = client.send_command(args.command, params)
    
    print(json.dumps(result, indent=2))
