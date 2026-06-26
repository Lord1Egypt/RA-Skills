"""Account management module"""

import json
import os
from typing import Optional, Dict, Any
from datetime import datetime


class AccountManager:
    """Account manager for Xiaohongshu MCP"""

    def __init__(self, user_cookies_path: str = "user_cookies.json", mcp_exe_path: str = "."):
        """Initialize account manager"""
        self.user_cookies_path = user_cookies_path
        self.mcp_exe_path = mcp_exe_path
        self.cookies_json_path = os.path.join(mcp_exe_path, "cookies.json")
        self._load_user_cookies()

    def _load_user_cookies(self) -> None:
        """Load user cookies from file"""
        if os.path.exists(self.user_cookies_path):
            try:
                with open(self.user_cookies_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.accounts = data.get("accounts", {})
                    self.current_account = data.get("current_account")
            except Exception:
                self.accounts = {}
                self.current_account = None
        else:
            self.accounts = {}
            self.current_account = None

    def _save_user_cookies(self) -> None:
        """Save user cookies to file"""
        data = {
            "accounts": self.accounts,
            "current_account": self.current_account
        }
        with open(self.user_cookies_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_account(self, username: str, cookies: Dict[str, Any], notes: str = "") -> None:
        """Add a new account"""
        self.accounts[username] = {
            "cookies": cookies,
            "last_used": datetime.now().isoformat(),
            "notes": notes
        }
        self._save_user_cookies()

    def remove_account(self, username: str) -> None:
        """Remove an account"""
        if username in self.accounts:
            del self.accounts[username]
            if self.current_account == username:
                self.current_account = None
            self._save_user_cookies()

    def list_accounts(self) -> Dict[str, Dict[str, Any]]:
        """List all accounts"""
        return self.accounts

    def get_current_account(self) -> Optional[str]:
        """Get current account"""
        return self.current_account

    def switch_account(self, username: str) -> bool:
        """Switch to another account"""
        if username not in self.accounts:
            return False

        # Write cookies to mcp cookies.json
        cookies = self.accounts[username]["cookies"]
        try:
            with open(self.cookies_json_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            # Update last used time
            self.accounts[username]["last_used"] = datetime.now().isoformat()
            self.current_account = username
            self._save_user_cookies()
            return True
        except Exception:
            return False

    def import_cookies(self, username: str, notes: str = "") -> bool:
        """Import cookies from mcp cookies.json"""
        if not os.path.exists(self.cookies_json_path):
            return False

        try:
            with open(self.cookies_json_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            
            self.add_account(username, cookies, notes)
            return True
        except Exception:
            return False

    def export_cookies(self, username: str) -> Optional[Dict[str, Any]]:
        """Export cookies for an account"""
        if username not in self.accounts:
            return None
        return self.accounts[username]["cookies"]
