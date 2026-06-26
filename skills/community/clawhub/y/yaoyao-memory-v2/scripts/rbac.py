#!/usr/bin/env python3
"""RBAC 权限控制系统
参考 xiaoyi-claw-omega-final 的权限治理体系
"""
import json
from datetime import datetime
from typing import Dict, List, Optional, Set
from pathlib import Path
from enum import Enum

# 权限定义
class Permission(Enum):
    # 记忆操作
    MEMORY_READ = "memory:read"
    MEMORY_WRITE = "memory:write"
    MEMORY_DELETE = "memory:delete"
    MEMORY_ADMIN = "memory:admin"
    
    # 技能操作
    SKILL_READ = "skill:read"
    SKILL_INSTALL = "skill:install"
    SKILL_UNINSTALL = "skill:uninstall"
    SKILL_ADMIN = "skill:admin"
    
    # 系统操作
    SYSTEM_CONFIG = "system:config"
    SYSTEM_RESTART = "system:restart"
    SYSTEM_ADMIN = "system:admin"
    
    # 诊断操作
    DIAGNOSE_RUN = "diagnose:run"
    DIAGNOSE_VIEW = "diagnose:view"

# 角色定义
class Role(Enum):
    ADMIN = "admin"           # 管理员 - 全部权限
    DEVELOPER = "developer"   # 开发者 - 大部分操作权限
    USER = "user"            # 普通用户 - 基础操作
    GUEST = "guest"          # 访客 - 只读权限

# 角色权限映射
ROLE_PERMISSIONS = {
    Role.ADMIN: {p for p in Permission},
    Role.DEVELOPER: {
        Permission.MEMORY_READ,
        Permission.MEMORY_WRITE,
        Permission.SKILL_READ,
        Permission.SKILL_INSTALL,
        Permission.SYSTEM_CONFIG,
        Permission.DIAGNOSE_RUN,
        Permission.DIAGNOSE_VIEW,
    },
    Role.USER: {
        Permission.MEMORY_READ,
        Permission.MEMORY_WRITE,
        Permission.SKILL_READ,
        Permission.DIAGNOSE_VIEW,
    },
    Role.GUEST: {
        Permission.MEMORY_READ,
        Permission.SKILL_READ,
    },
}

class User:
    """用户"""
    
    def __init__(self, user_id: str, role: Role = Role.USER):
        self.user_id = user_id
        self.role = role
        self.permissions = ROLE_PERMISSIONS.get(role, set())
        self.created_at = datetime.now().isoformat()
    
    def has_permission(self, permission: Permission) -> bool:
        """检查是否有权限"""
        return permission in self.permissions
    
    def grant_permission(self, permission: Permission):
        """授予权限"""
        self.permissions.add(permission)
    
    def revoke_permission(self, permission: Permission):
        """撤销权限"""
        self.permissions.discard(permission)
    
    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "role": self.role.value,
            "permissions": [p.value for p in self.permissions],
            "created_at": self.created_at
        }

class RBACManager:
    """RBAC 权限管理器"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or (Path.home() / ".openclaw" / "workspace" / "memory" / "rbac.json")
        self.users: Dict[str, User] = {}
        self.load()
    
    def load(self):
        """从磁盘加载"""
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                self.users = {
                    uid: User(u["user_id"], Role(u["role"]))
                    for uid, u in data.get("users", {}).items()
                }
            except:
                self.users = {}
    
    def save(self):
        """保存到磁盘"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "users": {uid: u.to_dict() for uid, u in self.users.items()}
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def add_user(self, user_id: str, role: Role = Role.USER) -> User:
        """添加用户"""
        user = User(user_id, role)
        self.users[user_id] = user
        self.save()
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户"""
        return self.users.get(user_id)
    
    def remove_user(self, user_id: str) -> bool:
        """移除用户"""
        if user_id in self.users:
            del self.users[user_id]
            self.save()
            return True
        return False
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """检查用户权限"""
        user = self.get_user(user_id)
        if not user:
            return False
        return user.has_permission(permission)
    
    def require_permission(self, user_id: str, permission: Permission):
        """要求权限（如果无权限抛出异常）"""
        if not self.check_permission(user_id, permission):
            raise PermissionError(f"用户 {user_id} 没有权限: {permission.value}")
    
    def get_role_permissions(self, role: Role) -> List[str]:
        """获取角色权限列表"""
        return [p.value for p in ROLE_PERMISSIONS.get(role, set())]
    
    def format_permissions_report(self, user_id: str) -> str:
        """格式化权限报告"""
        user = self.get_user(user_id)
        if not user:
            return f"❓ 用户 {user_id} 不存在"
        
        report = f"👤 用户: {user_id}\n"
        report += f"🎭 角色: {user.role.value}\n"
        report += f"📋 权限 ({len(user.permissions)} 个):\n"
        
        for perm in sorted(user.permissions, key=lambda p: p.value):
            category = perm.value.split(":")[0]
            report += f"  • [{category}] {perm.value}\n"
        
        return report


class PermissionMatrix:
    """权限矩阵"""
    
    # 操作定义
    OPERATIONS = {
        "read_memory": {"permission": Permission.MEMORY_READ, "roles": ["admin", "developer", "user", "guest"]},
        "write_memory": {"permission": Permission.MEMORY_WRITE, "roles": ["admin", "developer", "user"]},
        "delete_memory": {"permission": Permission.MEMORY_DELETE, "roles": ["admin"]},
        "install_skill": {"permission": Permission.SKILL_INSTALL, "roles": ["admin", "developer"]},
        "uninstall_skill": {"permission": Permission.SKILL_UNINSTALL, "roles": ["admin"]},
        "system_config": {"permission": Permission.SYSTEM_CONFIG, "roles": ["admin", "developer"]},
        "run_diagnose": {"permission": Permission.DIAGNOSE_RUN, "roles": ["admin", "developer"]},
    }
    
    @classmethod
    def can_do(cls, operation: str, role: str) -> bool:
        """检查角色是否有权限执行操作"""
        if operation not in cls.OPERATIONS:
            return False
        return role in cls.OPERATIONS[operation]["roles"]
    
    @classmethod
    def get_matrix(cls) -> str:
        """获取权限矩阵表格"""
        lines = ["📊 权限矩阵\n", "=" * 60]
        lines.append(f"{'操作':<20} {'Admin':<10} {'Developer':<10} {'User':<10} {'Guest':<10}")
        lines.append("-" * 60)
        
        for op, info in cls.OPERATIONS.items():
            roles = info["roles"]
            admin = "✅" if "admin" in roles else "❌"
            dev = "✅" if "developer" in roles else "❌"
            user = "✅" if "user" in roles else "❌"
            guest = "✅" if "guest" in roles else "❌"
            lines.append(f"{op:<20} {admin:<10} {dev:<10} {user:<10} {guest:<10}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # 测试
    print("=== RBAC 测试 ===")
    
    manager = RBACManager()
    
    # 添加用户
    admin = manager.add_user("admin_001", Role.ADMIN)
    developer = manager.add_user("dev_001", Role.DEVELOPER)
    user = manager.add_user("user_001", Role.USER)
    
    print(f"添加了 {len(manager.users)} 个用户")
    
    # 检查权限
    print(f"\nadmin_001 可以删除记忆: {manager.check_permission('admin_001', Permission.MEMORY_DELETE)}")
    print(f"user_001 可以删除记忆: {manager.check_permission('user_001', Permission.MEMORY_DELETE)}")
    
    # 权限矩阵
    print("\n" + PermissionMatrix.get_matrix())
    
    # 用户权限报告
    print("\n" + manager.format_permissions_report("dev_001"))
