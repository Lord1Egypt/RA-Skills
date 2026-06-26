"""
security_audit.py - 安全配置审计模块

对 Agent Memory 系统进行安全配置审计，检测潜在风险。

检查项按严重度分级：
  CRITICAL - 必须立即修复的安全问题
  WARNING  - 建议尽快修复的安全隐患
  INFO     - 信息性提示，供运维参考

用法:
    python -m agent_memory.security_audit
    python -m agent_memory.security_audit --format json
    python -m agent_memory.security_audit --db /path/to/memories.db
"""

from __future__ import annotations

import argparse
import ast
import json
import logging
import os
import re
import stat
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

# ── 严重度常量 ──────────────────────────────────────────────
CRITICAL = "CRITICAL"
WARNING = "WARNING"
INFO = "INFO"

# ── 已知默认 JWT 密钥 ──────────────────────────────────────
_DEFAULT_JWT_SECRETS = {
    "",
    "agent-memory-default-secret",
    "agent-memory-default-secret-change-in-production",
    "secret",
    "changeme",
    "my-secret-key",
    "my-secret",
    "default",
}

# ── 项目根目录 ──────────────────────────────────────────────
_PACKAGE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _PACKAGE_DIR.parent


# ═══════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════

@dataclass
class AuditResult:
    """单项审计结果。"""
    severity: str    # CRITICAL / WARNING / INFO
    name: str        # 检查项名称
    status: str      # PASS / FAIL / SKIP / WARN
    message: str     # 详细说明
    recommendation: str = ""  # 修复建议


@dataclass
class AuditReport:
    """审计报告，包含所有检查结果和汇总。"""
    results: List[AuditResult] = field(default_factory=list)

    @property
    def summary(self) -> dict:
        total = len(self.results)
        by_severity = {CRITICAL: 0, WARNING: 0, INFO: 0}
        by_status = {"PASS": 0, "FAIL": 0, "WARN": 0, "SKIP": 0}
        for r in self.results:
            by_severity[r.severity] = by_severity.get(r.severity, 0) + 1
            by_status[r.status] = by_status.get(r.status, 0) + 1
        return {
            "total": total,
            "critical_fail": sum(1 for r in self.results if r.severity == CRITICAL and r.status == "FAIL"),
            "warning_fail": sum(1 for r in self.results if r.severity == WARNING and r.status in ("FAIL", "WARN")),
            "by_severity": by_severity,
            "by_status": by_status,
        }

    def to_dict(self) -> dict:
        return {
            "results": [asdict(r) for r in self.results],
            "summary": self.summary,
        }

    def to_text(self) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("  Agent Memory 安全审计报告")
        lines.append("=" * 60)
        for r in self.results:
            icon = {"PASS": "[PASS]", "FAIL": "[FAIL]", "WARN": "[WARN]", "SKIP": "[SKIP]"}.get(r.status, "[?]")
            lines.append(f"\n{r.severity:8s} {icon} {r.name}")
            lines.append(f"         {r.message}")
            if r.recommendation:
                lines.append(f"         建议: {r.recommendation}")
        lines.append("\n" + "=" * 60)
        s = self.summary
        lines.append(f"  汇总: 共 {s['total']} 项 | CRITICAL FAIL: {s['critical_fail']} | WARNING FAIL: {s['warning_fail']}")
        lines.append("=" * 60)
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# CRITICAL 级别检查
# ═══════════════════════════════════════════════════════════

def check_jwt_default_secret() -> AuditResult:
    """检查 auth_middleware.py 中是否使用默认 JWT 密钥。"""
    jwt_secret = os.environ.get("AGENT_MEMORY_JWT_SECRET", "")
    if jwt_secret in _DEFAULT_JWT_SECRETS:
        return AuditResult(
            severity=CRITICAL,
            name="JWT 默认密钥检测",
            status="FAIL",
            message=f"JWT 密钥为空或使用默认值（长度={len(jwt_secret)}字符），攻击者可伪造任意令牌。",
            recommendation="设置环境变量 AGENT_MEMORY_JWT_SECRET 为至少32字符的随机字符串。"
                           " 生成方式: python -c \"import secrets; print(secrets.token_urlsafe(48))\"",
        )
    if len(jwt_secret) < 32:
        return AuditResult(
            severity=CRITICAL,
            name="JWT 默认密钥检测",
            status="FAIL",
            message=f"JWT 密钥过短 (长度 {len(jwt_secret)} < 32)，存在被暴力破解风险。",
            recommendation="设置 AGENT_MEMORY_JWT_SECRET 为至少32字符的随机字符串。",
        )
    return AuditResult(
        severity=CRITICAL,
        name="JWT 默认密钥检测",
        status="PASS",
        message=f"JWT 密钥已配置 (长度 {len(jwt_secret)})。",
    )


def check_web_auth() -> AuditResult:
    """检查 web_server.py 是否配置了 AGENT_MEMORY_API_KEY。"""
    api_key = os.environ.get("AGENT_MEMORY_API_KEY", "")
    if not api_key:
        return AuditResult(
            severity=CRITICAL,
            name="Web 服务认证检测",
            status="FAIL",
            message="AGENT_MEMORY_API_KEY 未设置，Web 服务运行在无认证模式（开发模式），任何人可访问。",
            recommendation="设置环境变量 AGENT_MEMORY_API_KEY 为强随机字符串以启用 API Key 认证。",
        )
    return AuditResult(
        severity=CRITICAL,
        name="Web 服务认证检测",
        status="PASS",
        message="AGENT_MEMORY_API_KEY 已配置，Web 服务认证已启用。",
    )


def check_crypto_store_status() -> AuditResult:
    """检查 CryptoStore 激活状态。"""
    try:
        from .storage import crypto_store as _cs_mod
    except ImportError:
        return AuditResult(
            severity=CRITICAL,
            name="CryptoStore 激活检测",
            status="FAIL",
            message="无法导入 CryptoStore 模块。",
            recommendation="检查 agent_memory.storage.crypto_store 模块是否完整。",
        )

    if not _cs_mod._HAS_CRYPTO:
        return AuditResult(
            severity=CRITICAL,
            name="CryptoStore 激活检测",
            status="FAIL",
            message="cryptography 库未安装，CryptoStore 降级为透传模式（不加密），confidential 数据将以明文存储。",
            recommendation="运行 pip install cryptography 启用加密功能。",
        )

    # cryptography 已安装，检查是否能真正初始化
    try:
        from .store import MemoryStore
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "_audit_check.db")
            store = MemoryStore(db_path)
            cs = _cs_mod.CryptoStore(store)
            active = cs.is_active
            store.close()
    except Exception as e:
        logger.debug("CryptoStore temp init failed: %s", e)
        active = False
        enc_key = os.environ.get("AGENT_MEMORY_ENCRYPTION_KEY")
        key_file = _PACKAGE_DIR / "storage" / ".encryption_key"
        if enc_key or key_file.exists():
            active = True

    if active:
        return AuditResult(
            severity=CRITICAL,
            name="CryptoStore 激活检测",
            status="PASS",
            message="cryptography 已安装且 CryptoStore 已激活，敏感数据将被加密存储。",
        )
    return AuditResult(
        severity=CRITICAL,
        name="CryptoStore 激活检测",
        status="WARN",
        message="cryptography 已安装但 CryptoStore 未能激活（密钥初始化失败），敏感数据可能未加密。",
        recommendation="检查 AGENT_MEMORY_ENCRYPTION_KEY 环境变量或 .encryption_key 文件是否有效。",
    )


# ═══════════════════════════════════════════════════════════
# WARNING 级别检查
# ═══════════════════════════════════════════════════════════

def check_encryption_key_file_security() -> AuditResult:
    """检查 .encryption_key 文件是否存在于源码目录且权限过宽。"""
    key_file = _PACKAGE_DIR / "storage" / ".encryption_key"
    if not key_file.exists():
        return AuditResult(
            severity=WARNING,
            name="加密密钥文件安全",
            status="PASS",
            message=".encryption_key 文件不存在于源码目录（密钥可能来自环境变量或尚未生成）。",
        )

    issues = []
    # 检查是否在源码目录（应加入 .gitignore）
    gitignore_path = _PROJECT_ROOT / ".gitignore"
    in_gitignore = False
    if gitignore_path.exists():
        try:
            gitignore_content = gitignore_path.read_text(encoding="utf-8")
            in_gitignore = ".encryption_key" in gitignore_content
        except Exception as e:
            logger.debug("gitignore read failed: %s", e)
            pass
    if not in_gitignore:
        issues.append("文件未在 .gitignore 中排除，可能被提交到版本控制")

    # 检查文件权限（仅 Unix）
    if os.name != "nt":
        try:
            file_stat = key_file.stat()
            mode = file_stat.st_mode
            if mode & stat.S_IROTH:
                issues.append("文件对其他用户可读 (o+r)")
            if mode & stat.S_IWOTH:
                issues.append("文件对其他用户可写 (o+w)")
        except Exception as e:
            logger.debug("File stat check failed: %s", e)
            pass

    if issues:
        return AuditResult(
            severity=WARNING,
            name="加密密钥文件安全",
            status="WARN",
            message=f".encryption_key 文件存在安全问题: {'; '.join(issues)}。",
            recommendation="将 .encryption_key 加入 .gitignore，并设置文件权限为 600 (仅所有者可读写)。"
                           " 生产环境建议使用 AGENT_MEMORY_ENCRYPTION_KEY 环境变量。",
        )
    return AuditResult(
        severity=WARNING,
        name="加密密钥文件安全",
        status="PASS",
        message=".encryption_key 文件安全配置正常。",
    )


def check_sse_connection_limit() -> AuditResult:
    """检查 api_v3.py 中 SSE 最大连接数是否合理。"""
    api_v3_path = _PACKAGE_DIR / "api_v3.py"
    max_conn = None
    if api_v3_path.exists():
        try:
            content = api_v3_path.read_text(encoding="utf-8")
            match = re.search(r"_MAX_SSE_CONNECTIONS\s*=\s*(\d+)", content)
            if match:
                max_conn = int(match.group(1))
        except Exception as e:
            logger.debug("SSE config read failed: %s", e)
            pass

    if max_conn is None:
        return AuditResult(
            severity=WARNING,
            name="SSE 连接数限制",
            status="SKIP",
            message="无法从 api_v3.py 中读取 SSE 最大连接数配置。",
        )

    if max_conn > 100:
        return AuditResult(
            severity=WARNING,
            name="SSE 连接数限制",
            status="WARN",
            message=f"SSE 最大连接数为 {max_conn}，超过建议上限 100，可能导致资源耗尽。",
            recommendation=f"将 api_v3.py 中 _MAX_SSE_CONNECTIONS 调整为 <= 100。",
        )
    return AuditResult(
        severity=WARNING,
        name="SSE 连接数限制",
        status="PASS",
        message=f"SSE 最大连接数为 {max_conn}，在合理范围内 (<= 100)。",
    )


def check_cors_config() -> AuditResult:
    """检查 CORS 是否允许 * 来源。"""
    cors_origins_str = os.environ.get("AGENT_MEMORY_CORS_ORIGINS", "")
    if not cors_origins_str.strip():
        return AuditResult(
            severity=WARNING,
            name="CORS 配置",
            status="WARN",
            message="AGENT_MEMORY_CORS_ORIGINS 未设置，CORS 默认允许所有来源 (*)，存在跨站请求风险。",
            recommendation="设置 AGENT_MEMORY_CORS_ORIGINS 为允许的域名列表（逗号分隔），"
                           "例如: AGENT_MEMORY_CORS_ORIGINS=https://app.example.com,https://admin.example.com",
        )

    origins = [o.strip() for o in cors_origins_str.split(",") if o.strip()]
    if "*" in origins:
        return AuditResult(
            severity=WARNING,
            name="CORS 配置",
            status="WARN",
            message="CORS 配置中包含通配符 '*'，允许任何来源的跨站请求。",
            recommendation="移除 '*' 并指定具体允许的域名。",
        )
    return AuditResult(
        severity=WARNING,
        name="CORS 配置",
        status="PASS",
        message=f"CORS 已配置允许来源: {', '.join(origins)}",
    )


def check_plaintext_confidential(db_path: Optional[str] = None) -> AuditResult:
    """检查 memories 表中是否有 importance=confidential 但 content 未加密的记录。"""
    if db_path is None:
        db_path = os.environ.get("AGENT_MEMORY_DB_PATH", "")

    if not db_path:
        # 尝试默认路径
        default_path = _PROJECT_ROOT / "memories.db"
        if default_path.exists():
            db_path = str(default_path)
        else:
            return AuditResult(
                severity=WARNING,
                name="敏感数据明文存储",
                status="SKIP",
                message="未指定数据库路径，跳过明文敏感数据检查。使用 --db 参数指定数据库路径。",
            )

    if not os.path.exists(db_path):
        return AuditResult(
            severity=WARNING,
            name="敏感数据明文存储",
            status="SKIP",
            message=f"数据库文件不存在: {db_path}",
        )

    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='memories'")
        if not cursor.fetchone():
            conn.close()
            return AuditResult(
                severity=WARNING,
                name="敏感数据明文存储",
                status="SKIP",
                message="数据库中不存在 memories 表。",
            )

        # 查找 importance=confidential 但 content 未加密的记录
        cursor.execute(
            "SELECT COUNT(*) FROM memories WHERE importance = 'confidential' "
            "AND content IS NOT NULL "
            "AND (content NOT LIKE 'ENC:%' AND content != '')"
        )
        count = cursor.fetchone()[0]
        conn.close()

        if count > 0:
            return AuditResult(
                severity=WARNING,
                name="敏感数据明文存储",
                status="FAIL",
                message=f"发现 {count} 条 importance=confidential 但 content 未加密的记录。",
                recommendation="启用 CryptoStore 并重新写入这些记录以确保加密存储。"
                               " 可使用 AGENT_MEMORY_ENCRYPTION_STRICT=true 强制加密。",
            )
        return AuditResult(
            severity=WARNING,
            name="敏感数据明文存储",
            status="PASS",
            message="未发现 importance=confidential 的明文记录。",
        )
    except Exception as e:
        return AuditResult(
            severity=WARNING,
            name="敏感数据明文存储",
            status="SKIP",
            message=f"检查数据库时出错: {e}",
        )


# ═══════════════════════════════════════════════════════════
# INFO 级别检查
# ═══════════════════════════════════════════════════════════

def check_api_key_configured() -> AuditResult:
    """检查是否配置了 AGENT_MEMORY_API_KEY。"""
    api_key = os.environ.get("AGENT_MEMORY_API_KEY", "")
    if api_key:
        return AuditResult(
            severity=INFO,
            name="API Key 配置状态",
            status="PASS",
            message="AGENT_MEMORY_API_KEY 已配置。",
        )
    return AuditResult(
        severity=INFO,
        name="API Key 配置状态",
        status="WARN",
        message="AGENT_MEMORY_API_KEY 未配置，Web 服务无认证保护。",
    )


def check_jwt_secret_configured() -> AuditResult:
    """检查是否配置了 AGENT_MEMORY_JWT_SECRET。"""
    jwt_secret = os.environ.get("AGENT_MEMORY_JWT_SECRET", "")
    if jwt_secret:
        return AuditResult(
            severity=INFO,
            name="JWT Secret 配置状态",
            status="PASS",
            message=f"AGENT_MEMORY_JWT_SECRET 已配置 (长度 {len(jwt_secret)})。",
        )
    return AuditResult(
        severity=INFO,
        name="JWT Secret 配置状态",
        status="WARN",
        message="AGENT_MEMORY_JWT_SECRET 未配置。",
    )


def check_crypto_store_active() -> AuditResult:
    """检查 CryptoStore 是否激活。"""
    try:
        from .storage import crypto_store as _cs_mod
    except ImportError:
        return AuditResult(
            severity=INFO,
            name="加密存储状态",
            status="FAIL",
            message="无法导入 CryptoStore 模块。",
        )

    if not _cs_mod._HAS_CRYPTO:
        return AuditResult(
            severity=INFO,
            name="加密存储状态",
            status="WARN",
            message="cryptography 库未安装，CryptoStore 未激活。",
        )

    # 尝试检查是否真正激活
    enc_key = os.environ.get("AGENT_MEMORY_ENCRYPTION_KEY")
    key_file = _PACKAGE_DIR / "storage" / ".encryption_key"
    if enc_key or key_file.exists():
        return AuditResult(
            severity=INFO,
            name="加密存储状态",
            status="PASS",
            message="CryptoStore 已激活（密钥已配置）。",
        )
    return AuditResult(
        severity=INFO,
        name="加密存储状态",
        status="WARN",
        message="CryptoStore 密钥尚未配置，首次使用时会自动生成。",
    )


def check_version_consistency() -> AuditResult:
    """检查 pyproject.toml / __init__.py / VERSION 版本号是否一致。"""
    versions = {}

    # pyproject.toml
    pyproject_path = _PROJECT_ROOT / "pyproject.toml"
    if pyproject_path.exists():
        try:
            content = pyproject_path.read_text(encoding="utf-8")
            match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
            if match:
                versions["pyproject.toml"] = match.group(1)
        except Exception as e:
            logger.debug("pyproject.toml version read failed: %s", e)
            pass

    # __init__.py
    init_path = _PACKAGE_DIR / "__init__.py"
    if init_path.exists():
        try:
            content = init_path.read_text(encoding="utf-8")
            match = re.search(r'__version__\s*=\s*"([^"]+)"', content)
            if match:
                versions["__init__.py"] = match.group(1)
        except Exception as e:
            logger.debug("__init__.py version read failed: %s", e)
            pass

    # VERSION
    version_path = _PROJECT_ROOT / "VERSION"
    if version_path.exists():
        try:
            v = version_path.read_text(encoding="utf-8").strip()
            if v:
                versions["VERSION"] = v
        except Exception as e:
            logger.debug("VERSION file read failed: %s", e)
            pass

    if not versions:
        return AuditResult(
            severity=INFO,
            name="版本号一致性",
            status="SKIP",
            message="未找到任何版本号文件。",
        )

    unique_versions = set(versions.values())
    if len(unique_versions) == 1:
        return AuditResult(
            severity=INFO,
            name="版本号一致性",
            status="PASS",
            message=f"所有版本号一致: {next(iter(unique_versions))} ({', '.join(versions.keys())})",
        )
    return AuditResult(
        severity=INFO,
        name="版本号一致性",
        status="FAIL",
        message=f"版本号不一致: {', '.join(f'{k}={v}' for k, v in versions.items())}",
        recommendation="统一 pyproject.toml、__init__.py 和 VERSION 中的版本号。",
    )


# ═══════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════

def run_audit(db_path: Optional[str] = None) -> AuditReport:
    """运行所有安全审计检查，返回审计报告。"""
    report = AuditReport()

    # CRITICAL
    report.results.append(check_jwt_default_secret())
    report.results.append(check_web_auth())
    report.results.append(check_crypto_store_status())

    # WARNING
    report.results.append(check_encryption_key_file_security())
    report.results.append(check_sse_connection_limit())
    report.results.append(check_cors_config())
    report.results.append(check_plaintext_confidential(db_path))

    # INFO
    report.results.append(check_api_key_configured())
    report.results.append(check_jwt_secret_configured())
    report.results.append(check_crypto_store_active())
    report.results.append(check_version_consistency())

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Agent Memory 安全配置审计",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="输出格式 (默认: text)",
    )
    parser.add_argument(
        "--db",
        default=None,
        help="数据库路径（用于明文敏感数据检查）",
    )
    args = parser.parse_args()

    report = run_audit(db_path=args.db)

    if args.format == "json":
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(report.to_text())

    # 如果有 CRITICAL 级别的 FAIL，返回非零退出码
    if report.summary["critical_fail"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
