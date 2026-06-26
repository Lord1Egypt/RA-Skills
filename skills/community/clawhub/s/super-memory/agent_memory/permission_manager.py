from __future__ import annotations
import os
import json
import hashlib
import secrets
import logging
import threading
import tempfile
import time
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

MIN_PASSWORD_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 300


class PermissionManager:

    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "data")
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.roles_file = os.path.join(self.data_dir, "roles.json")
        self._lock = threading.Lock()
        self._login_attempts: Dict[str, dict] = {}

        os.makedirs(self.data_dir, exist_ok=True)

        self.users = self._load_data(self.users_file, {})
        self.roles = self._load_data(self.roles_file, {})

        self._init_defaults()

    def _load_data(self, file_path: str, default: dict) -> dict:
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error("Failed to load data file: %s", e)
        return default

    def _save_data(self, file_path: str, data: dict):
        try:
            tmp_fd, tmp_path = tempfile.mkstemp(
                dir=os.path.dirname(file_path), suffix=".tmp"
            )
            try:
                with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                os.replace(tmp_path, file_path)
            except Exception:
                try:
                    os.unlink(tmp_path)
                except OSError as e:
                    logger.debug("permission_manager: cleanup tmp file: %s", e)
                raise
        except Exception as e:
            logger.error("Failed to save data file: %s", e)

    def _init_defaults(self):
        if "guest" not in self.roles:
            self.create_role("guest", "Guest", ["read"])

        if "user" not in self.roles:
            self.create_role("user", "User", ["read", "write"])

        if "admin" not in self.roles:
            self.create_role("admin", "Admin", [
                "read", "write", "delete",
                "manage_users", "manage_roles", "manage_permissions",
                "export", "import", "admin"
            ])

        if "admin" not in self.users:
            admin_password = os.environ.get("AGENT_MEMORY_ADMIN_PASSWORD")
            if admin_password:
                self.create_user("admin", admin_password, "Administrator")
                self.assign_role("admin", "admin")
            else:
                logger.warning(
                    "No AGENT_MEMORY_ADMIN_PASSWORD set. "
                    "Admin account will NOT be created. "
                    "Set AGENT_MEMORY_ADMIN_PASSWORD env var to enable admin access."
                )

    def _hash_password(self, password: str, salt: str = None) -> str:
        if salt is None:
            salt = secrets.token_hex(16)
        iterations = 100000
        dk = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), iterations
        )
        return f"pbkdf2:{iterations}:{salt}:{dk.hex()}"

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        if stored_hash.startswith("pbkdf2:"):
            parts = stored_hash.split(":")
            if len(parts) != 4:
                return False
            try:
                iterations = int(parts[1])
                salt = parts[2]
                expected = parts[3]
                dk = hashlib.pbkdf2_hmac(
                    "sha256", password.encode(), salt.encode(), iterations
                )
                return secrets.compare_digest(dk.hex(), expected)
            except (ValueError, IndexError):
                return False
        return False

    def _is_locked_out(self, username: str) -> bool:
        info = self._login_attempts.get(username)
        if not info:
            return False
        if info.get("attempts", 0) >= MAX_LOGIN_ATTEMPTS:
            if time.time() - info.get("last_attempt", 0) < LOCKOUT_DURATION:
                return True
            del self._login_attempts[username]
        return False

    def _record_failed_login(self, username: str):
        if username not in self._login_attempts:
            self._login_attempts[username] = {"attempts": 0, "last_attempt": 0}
        self._login_attempts[username]["attempts"] += 1
        self._login_attempts[username]["last_attempt"] = time.time()

    def _reset_login_attempts(self, username: str):
        self._login_attempts.pop(username, None)

    def _validate_password_strength(self, password: str) -> bool:
        if len(password) < MIN_PASSWORD_LENGTH:
            return False
        return True

    def create_user(self, username: str, password: str, full_name: str = None) -> bool:
        with self._lock:
            if username in self.users:
                logger.warning("User already exists: %s", username)
                return False

            if not self._validate_password_strength(password):
                logger.warning(
                    "Password too weak (min %s chars)", MIN_PASSWORD_LENGTH
                )
                return False

            self.users[username] = {
                "password_hash": self._hash_password(password),
                "full_name": full_name or username,
                "roles": [],
                "created_at": int(time.time())
            }

            self._save_data(self.users_file, self.users)
            logger.info("User created: %s", username)
            return True

    def get_user(self, username: str) -> Optional[Dict]:
        user = self.users.get(username)
        if user:
            return {
                "username": username,
                "full_name": user.get("full_name"),
                "roles": user.get("roles", []),
                "created_at": user.get("created_at")
            }
        return None

    def update_user(self, username: str, full_name: str = None, password: str = None) -> bool:
        with self._lock:
            if username not in self.users:
                logger.warning("User not found: %s", username)
                return False

            user = self.users[username]
            if full_name is not None:
                user["full_name"] = full_name
            if password is not None:
                if not self._validate_password_strength(password):
                    logger.warning(
                        "Password too weak (min %s chars)", MIN_PASSWORD_LENGTH
                    )
                    return False
                user["password_hash"] = self._hash_password(password)

            self._save_data(self.users_file, self.users)
            logger.info("User updated: %s", username)
            return True

    def delete_user(self, username: str) -> bool:
        with self._lock:
            if username not in self.users:
                logger.warning("User not found: %s", username)
                return False

            del self.users[username]
            self._save_data(self.users_file, self.users)
            logger.info("User deleted: %s", username)
            return True

    def list_users(self) -> List[Dict]:
        return [self.get_user(username) for username in self.users]

    def authenticate(self, username: str, password: str) -> bool:
        if self._is_locked_out(username):
            logger.warning("Account locked: %s", username)
            return False

        user = self.users.get(username)
        if not user:
            return False

        if self._verify_password(password, user["password_hash"]):
            self._reset_login_attempts(username)
            return True

        self._record_failed_login(username)
        return False

    def create_role(self, role_id: str, role_name: str, permissions: List[str]) -> bool:
        with self._lock:
            if role_id in self.roles:
                logger.warning("Role already exists: %s", role_id)
                return False

            self.roles[role_id] = {
                "name": role_name,
                "permissions": permissions,
                "created_at": int(time.time())
            }

            self._save_data(self.roles_file, self.roles)
            logger.info("Role created: %s", role_id)
            return True

    def get_role(self, role_id: str) -> Optional[Dict]:
        role = self.roles.get(role_id)
        if role:
            return {
                "role_id": role_id,
                "name": role.get("name"),
                "permissions": role.get("permissions", []),
                "created_at": role.get("created_at")
            }
        return None

    def update_role(self, role_id: str, role_name: str = None, permissions: List[str] = None) -> bool:
        with self._lock:
            if role_id not in self.roles:
                logger.warning("Role not found: %s", role_id)
                return False

            role = self.roles[role_id]
            if role_name is not None:
                role["name"] = role_name
            if permissions is not None:
                role["permissions"] = permissions

            self._save_data(self.roles_file, self.roles)
            logger.info("Role updated: %s", role_id)
            return True

    def delete_role(self, role_id: str) -> bool:
        with self._lock:
            if role_id not in self.roles:
                logger.warning("Role not found: %s", role_id)
                return False

            for username, user in self.users.items():
                if role_id in user.get("roles", []):
                    user["roles"].remove(role_id)

            del self.roles[role_id]
            self._save_data(self.roles_file, self.roles)
            self._save_data(self.users_file, self.users)
            logger.info("Role deleted: %s", role_id)
            return True

    def list_roles(self) -> List[Dict]:
        return [self.get_role(role_id) for role_id in self.roles]

    def assign_role(self, username: str, role_id: str) -> bool:
        with self._lock:
            if username not in self.users:
                logger.warning("User not found: %s", username)
                return False

            if role_id not in self.roles:
                logger.warning("Role not found: %s", role_id)
                return False

            user = self.users[username]
            if role_id not in user.get("roles", []):
                user.setdefault("roles", []).append(role_id)
                self._save_data(self.users_file, self.users)
                logger.info("Role assigned: %s -> %s", username, role_id)

            return True

    def revoke_role(self, username: str, role_id: str) -> bool:
        with self._lock:
            if username not in self.users:
                logger.warning("User not found: %s", username)
                return False

            user = self.users[username]
            if role_id in user.get("roles", []):
                user["roles"].remove(role_id)
                self._save_data(self.users_file, self.users)
                logger.info("Role revoked: %s -> %s", username, role_id)
                return True

            return False

    def get_user_roles(self, username: str) -> List[str]:
        user = self.users.get(username)
        if user:
            return user.get("roles", [])
        return []

    def get_role_permissions(self, role_id: str) -> List[str]:
        role = self.roles.get(role_id)
        if role:
            return role.get("permissions", [])
        return []

    def get_user_permissions(self, username: str) -> List[str]:
        permissions = []
        roles = self.get_user_roles(username)
        for role_id in roles:
            role_permissions = self.get_role_permissions(role_id)
            permissions.extend(role_permissions)
        return list(set(permissions))

    def check_permission(self, username: str, permission: str) -> bool:
        permissions = self.get_user_permissions(username)
        return permission in permissions

    def has_role(self, username: str, role_id: str) -> bool:
        roles = self.get_user_roles(username)
        return role_id in roles

    def verify_permission(self, username: str, permission: str) -> Dict:
        if username not in self.users:
            return {"allowed": False, "reason": "User not found"}

        if not self.check_permission(username, permission):
            return {"allowed": False, "reason": "Insufficient permissions"}

        return {"allowed": True, "reason": "Permission verified"}

    def get_stats(self) -> Dict:
        user_count = len(self.users)
        role_count = len(self.roles)

        role_user_count = {}
        for username, user in self.users.items():
            roles = user.get("roles", [])
            for role in roles:
                role_user_count[role] = role_user_count.get(role, 0) + 1

        permission_count = {}
        for role_id, role in self.roles.items():
            permissions = role.get("permissions", [])
            for perm in permissions:
                permission_count[perm] = permission_count.get(perm, 0) + 1

        return {
            "user_count": user_count,
            "role_count": role_count,
            "role_user_count": role_user_count,
            "permission_count": permission_count
        }


_permission_manager = None
_pm_lock = threading.Lock()


def get_permission_manager() -> PermissionManager:
    global _permission_manager
    if _permission_manager is None:
        with _pm_lock:
            if _permission_manager is None:
                _permission_manager = PermissionManager()
    return _permission_manager


PERMISSIONS = {
    "read": "Read permission",
    "write": "Write permission",
    "delete": "Delete permission",
    "manage_users": "Manage users",
    "manage_roles": "Manage roles",
    "manage_permissions": "Manage permissions",
    "export": "Export data",
    "import": "Import data",
    "admin": "Admin access"
}

DEFAULT_ROLES = {
    "guest": {
        "name": "Guest",
        "permissions": ["read"]
    },
    "user": {
        "name": "User",
        "permissions": ["read", "write"]
    },
    "admin": {
        "name": "Admin",
        "permissions": [
            "read", "write", "delete",
            "manage_users", "manage_roles", "manage_permissions",
            "export", "import", "admin"
        ]
    }
}
