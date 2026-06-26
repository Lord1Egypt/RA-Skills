#!/usr/bin/env python3
"""
paths.py - OpenClaw 记忆路径自动发现模块

自动发现 OpenClaw 的记忆存储位置，无需硬编码

功能：
1. 自动发现 OpenClaw 安装路径
2. 自动发现记忆目录（memory-* 模式）
3. 自动发现向量数据库
4. 自动发现 persona 文件
5. 缓存发现结果避免重复扫描
6. 向后兼容别名（旧代码兼容）

用法：
    from paths import get_memory_path, get_vectors_db, setup_paths
    # 或使用便捷别名
    from paths import MEMORY_DIR, VECTORS_DB, PERSONA_FILE
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

# OpenClaw 标准路径模式
OPENCLAW_PATTERNS = [
    ".openclaw",
    ".openclaw-workspace",
    ".claw",
    "openclaw-data",
]

MEMORY_PATTERNS = [
    "memory",
    "memory-tdai",
    "memory-default",
    "workspace",
    "memory-shared",
    "memory-cache",
]

VECTOR_FILES = [
    "vectors.db",
    "chroma_db",
    "vector.db",
    "memories.db",
]

# Skill 路径模式
SKILL_PATTERNS = [
    "skills",
    ".skills",
    "plugins",
    ".plugins",
]

# 配置路径模式
CONFIG_PATTERNS = [
    "config",
    "settings",
    ".config",
]


class PathDiscovery:
    """路径发现器"""
    
    def __init__(self):
        self._cache: Dict[str, Path] = {}
        self._openclaw_home: Optional[Path] = None
        self._memory_base: Optional[Path] = None
        self._vectors_db: Optional[Path] = None
        self._persona_file: Optional[Path] = None
    
    def find_openclaw_home(self) -> Path:
        """发现 OpenClaw 主目录"""
        if self._openclaw_home:
            return self._openclaw_home
        
        home = Path.home()
        
        # 1. 检查环境变量
        env_paths = [
            os.environ.get("OPENCLAW_HOME"),
            os.environ.get("OPENCLAW_PATH"),
            os.environ.get("HOME") + "/.openclaw",
        ]
        
        for p in env_paths:
            if p:
                path = Path(p)
                if path.exists():
                    self._openclaw_home = path
                    return path
        
        # 2. 扫描 home 目录
        for item in home.iterdir():
            if item.is_dir():
                # 检查是否是 openclaw 目录
                if "openclaw" in item.name.lower():
                    # 验证是否是 openclaw（检查关键文件）
                    if self._is_openclaw_dir(item):
                        self._openclaw_home = item
                        return item
        
        # 3. 扫描 home 下所有 .* 目录
        for item in home.iterdir():
            if item.name.startswith(".") and item.is_dir():
                if self._is_openclaw_dir(item):
                    self._openclaw_home = item
                    return item
        
        # 4. 默认路径
        default = home / ".openclaw"
        default.mkdir(exist_ok=True)
        self._openclaw_home = default
        return default
    
    def _is_openclaw_dir(self, path: Path) -> bool:
        """检查目录是否是 OpenClaw 安装"""
        # 检查关键文件和目录
        markers = [
            "workspace",
            "agents",
            "skills",
            ".config",
        ]
        
        # 如果有任何一个标记目录，认为是 openclaw
        for marker in markers:
            if (path / marker).exists():
                return True
        
        # 或者检查是否有 agents.json
        if (path / "agents.json").exists():
            return True
        
        return False
    
    def find_memory_base(self) -> Path:
        """发现记忆存储根目录"""
        if self._memory_base:
            return self._memory_base
        
        openclaw_home = self.find_openclaw_home()
        
        # 1. 环境变量
        if os.environ.get("OPENCLAW_MEMORY_PATH"):
            self._memory_base = Path(os.environ["OPENCLAW_MEMORY_PATH"])
            return self._memory_base
        
        # 2. 查找 memory-* 模式目录（多用户隔离）
        for item in openclaw_home.iterdir():
            if item.is_dir() and "memory" in item.name.lower():
                # 优先使用 memory-tdai 或 memory-default
                if item.name in ["memory-tdai", "memory-default", "memory"]:
                    self._memory_base = item
                    return item
        
        # 3. 查找 workspace/memory
        workspace = openclaw_home / "workspace"
        if workspace.exists():
            memory = workspace / "memory"
            if memory.exists():
                self._memory_base = memory
                return memory
        
        # 4. 默认 memory 目录
        default = openclaw_home / "memory"
        default.mkdir(exist_ok=True)
        self._memory_base = default
        return default
    
    def find_vectors_db(self) -> Path:
        """发现向量数据库路径"""
        if self._vectors_db:
            return self._vectors_db
        
        openclaw_home = self.find_openclaw_home()
        
        # 1. 环境变量
        if os.environ.get("OPENCLAW_VECTORS_DB"):
            self._vectors_db = Path(os.environ["OPENCLAW_VECTORS_DB"])
            return self._vectors_db
        
        # 2. 在 memory_base 中查找
        memory_base = self.find_memory_base()
        
        # 直接在目录中
        for fname in VECTOR_FILES:
            if fname == "vectors.db":
                db_path = memory_base / fname
                if db_path.exists():
                    self._vectors_db = db_path
                    return db_path
        
        # 3. 查找子目录
        for subdir in memory_base.iterdir():
            if subdir.is_dir():
                for fname in VECTOR_FILES:
                    db_path = subdir / fname
                    if db_path.exists():
                        self._vectors_db = db_path
                        return db_path
        
        # 4. 查找 memory-tdai
        tdai_dir = openclaw_home / "memory-tdai"
        if tdai_dir.exists():
            db_path = tdai_dir / "vectors.db"
            if db_path.exists():
                self._vectors_db = db_path
                return db_path
        
        # 5. 默认位置
        default = memory_base / "vectors.db"
        self._vectors_db = default
        return default
    
    def find_persona_file(self) -> Path:
        """发现 persona 文件路径"""
        if self._persona_file:
            return self._persona_file
        
        openclaw_home = self.find_openclaw_home()
        
        # 1. 环境变量
        if os.environ.get("OPENCLAW_PERSONA_PATH"):
            self._persona_file = Path(os.environ["OPENCLAW_PERSONA_PATH"])
            return self._persona_file
        
        # 2. memory-tdai 目录
        tdai_dir = openclaw_home / "memory-tdai"
        if tdai_dir.exists():
            persona = tdai_dir / "persona.md"
            if persona.exists():
                self._persona_file = persona
                return persona
        
        # 3. memory_base
        memory_base = self.find_memory_base()
        persona = memory_base / "persona.md"
        if persona.exists():
            self._persona_file = persona
            return persona
        
        # 4. workspace
        workspace = openclaw_home / "workspace"
        if workspace.exists():
            persona = workspace / "persona.md"
            if persona.exists():
                self._persona_file = persona
                return persona
        
        # 5. 默认
        default = tdai_dir / "persona.md"
        self._persona_file = default
        return default
    
    def get_all_paths(self) -> Dict[str, Path]:
        """获取所有发现的路径"""
        return {
            "openclaw_home": self.find_openclaw_home(),
            "memory_base": self.find_memory_base(),
            "vectors_db": self.find_vectors_db(),
            "persona_file": self.find_persona_file(),
        }
    
    def dump_discovery(self) -> str:
        """生成路径发现报告"""
        paths = self.get_all_paths()
        
        lines = [
            "🔍 OpenClaw 路径发现报告",
            "=" * 40,
            f"时间: {datetime.now().isoformat()}",
            "",
        ]
        
        for name, path in paths.items():
            exists = "✅" if path.exists() else "❌"
            lines.append(f"{exists} {name}: {path}")
        
        return "\n".join(lines)


# 全局单例
_discovery = PathDiscovery()


# 便捷函数
def get_openclaw_home() -> Path:
    """获取 OpenClaw 主目录"""
    return _discovery.find_openclaw_home()


def get_memory_base() -> Path:
    """获取记忆存储根目录"""
    return _discovery.find_memory_base()


def get_vectors_db() -> Path:
    """获取向量数据库路径"""
    return _discovery.find_vectors_db()


def get_persona_file() -> Path:
    """获取 persona 文件路径"""
    return _discovery.find_persona_file()


def get_all_paths() -> Dict[str, Path]:
    """获取所有路径"""
    return _discovery.get_all_paths()


def dump_discovery() -> str:
    """生成路径发现报告"""
    return _discovery.dump_discovery()


def setup_paths():
    """设置并验证路径（创建必要目录）"""
    paths = get_all_paths()
    
    # 创建必要目录
    for name, path in paths.items():
        if name != "vectors_db" and name != "persona_file":
            path.mkdir(parents=True, exist_ok=True)
    
    # 检查向量扩展
    vec_installed, vec_path = check_sqlite_vec_installed()
    if not vec_installed:
        print("⚠️ 警告: sqlite-vec 向量扩展未安装")
        print("📦 安装方法:")
        print("   openclaw plugin install memory-tencentdb")
        print("")
    
    return paths


# =============================================================================
# 向后兼容别名 - 保持旧代码兼容
# =============================================================================
# 兼容旧的硬编码路径名称，让现有代码无需修改

# 基础路径别名（兼容旧代码）
OPENCLAW_HOME = get_openclaw_home()
MEMORY_DIR = get_memory_base()
VECTORS_DB = get_vectors_db()
PERSONA_FILE = get_persona_file()

# 扩展名别名
SKILLS_DIR = OPENCLAW_HOME / "workspace" / "skills"
WORKSPACE_DIR = OPENCLAW_HOME / "workspace"
CONFIG_DIR = OPENCLAW_HOME / "workspace" / "skills" / "yaoyao-memory-v2" / "config"

# 向量扩展路径（需要 memory-tencentdb 插件）
VEC_EXT_PATHS = [
    OPENCLAW_HOME / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec-linux-x64" / "vec0",
    OPENCLAW_HOME / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec" / "vec0",
]

def check_sqlite_vec_installed() -> tuple[bool, str]:
    """检查 sqlite-vec 是否已安装"""
    for path in VEC_EXT_PATHS:
        if path.exists():
            return True, str(path)
    # 尝试 .so 扩展名
    for path in VEC_EXT_PATHS:
        so_path = Path(str(path) + ".so")
        if so_path.exists():
            return True, str(so_path)
    return False, ""

def get_vec_ext() -> str:
    """获取向量扩展路径（带错误提示）"""
    installed, path = check_sqlite_vec_installed()
    if installed:
        return path
    
    # 返回默认值（实际使用时会失败，给出清晰错误）
    default_path = str(VEC_EXT_PATHS[0])
    print(f"⚠️ 警告: sqlite-vec 未安装，向量搜索功能不可用")
    print(f"📦 请先安装 memory-tencentdb 插件:")
    print(f"   openclaw plugin install memory-tencentdb")
    print(f"   或参考: https://github.com/openclaw/plugins")
    return default_path

VEC_EXT = get_vec_ext()

def is_vector_search_available() -> bool:
    """检查向量搜索是否可用"""
    installed, _ = check_sqlite_vec_installed()
    return installed


if __name__ == "__main__":
    print(dump_discovery())
    print("")
    print("向后兼容别名:")
    print(f"  MEMORY_DIR = {MEMORY_DIR}")
    print(f"  VECTORS_DB = {VECTORS_DB}")
    print(f"  PERSONA_FILE = {PERSONA_FILE}")
    print(f"  VEC_EXT = {VEC_EXT}")
