"""
Phase Manager - 文件生命周期管理
file_manager.py

管理 Phase 产出文件的 CRUD + 版本控制 + 清理。
"""

import os
import json
import shutil
import time
import fcntl
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from .schemas import (
    CONTENT_TYPE_INTEGRATED,
    CONTENT_TYPE_REVIEW,
    CONTENT_TYPE_SUMMARY,
    calculate_content_hash,
    now_iso,
)


# ============================================================================
# 常量
# ============================================================================

WORKSPACE_BASE = os.path.expanduser("~/.openclaw/workspace")
FRESHNESS_THRESHOLD_HOURS = 48  # 文件新鲜度阈值（小时）
LOCK_TIMEOUT_SECONDS = 30       # 锁等待超时（秒）


# ============================================================================
# PhaseFileManager 类
# ============================================================================

class PhaseFileManager:
    """
    管理单个论文项目中各 Phase 的文件生命周期。

    职责：
    - 文件路径计算
    - 保存（带备份 + 锁保护）
    - 读取（带新鲜度校验）
    - 版本控制（.bak 备份）
    - 清理（删除中间文件）
    """

    def __init__(self, paper_name: str, workspace: str = None):
        self.paper_name = paper_name
        self.workspace = workspace or os.path.join(WORKSPACE_BASE, paper_name)
        os.makedirs(self.workspace, exist_ok=True)

    # ------------------------------------------------------------------------
    # 路径计算
    # ------------------------------------------------------------------------

    def get_file_path(self, phase: float, content_type: str, ext: str = None) -> str:
        """
        返回指定 Phase + 类型的目标文件路径。

        Args:
            phase: Phase 编号
            content_type: integrated / review / summary
            ext: 扩展名（默认根据 content_type 自动推断）

        Returns:
            文件绝对路径
        """
        if ext is None:
            if content_type == CONTENT_TYPE_INTEGRATED:
                ext = "md"
            else:
                ext = "json"
        return os.path.join(self.workspace, f"_phase{phase}_{content_type}.{ext}")

    def get_backup_path(self, phase: float, content_type: str) -> str:
        """返回备份文件路径"""
        return f"{self.get_file_path(phase, content_type)}.bak"

    def get_lock_path(self, phase: float) -> str:
        """返回锁文件路径"""
        return os.path.join(self.workspace, f"_phase{phase}.lock")

    def get_summary_path(self, phase: float) -> str:
        """返回 PhaseSummary JSON 文件路径"""
        return os.path.join(self.workspace, f"_phase{phase}_summary.json")

    def get_transition_path(self) -> str:
        """返回流转记录文件路径"""
        return os.path.join(self.workspace, "_transition.json")

    # ------------------------------------------------------------------------
    # 生命周期：保存
    # ------------------------------------------------------------------------

    def save_content(self, phase: float, content_type: str, content: str,
                     create_backup: bool = True) -> Dict[str, Any]:
        """
        保存内容到文件。

        流程：
        1. 计算 content_hash
        2. 检查是否有内容变化
        3. 有变化且 create_backup=True → 自动备份旧版本
        4. 写入新内容（带 .lock 保护）
        5. 返回结果

        Returns:
            {
                ok: bool,
                hash: str,
                backup_path: Optional[str],
                size_bytes: int,
                changed: bool,
                error: Optional[str]
            }
        """
        file_path = self.get_file_path(phase, content_type)
        content_hash = calculate_content_hash(content)

        # 检查是否有变化
        old_hash = None
        changed = False
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                old_content = f.read()
            old_hash = calculate_content_hash(old_content)
            changed = (old_hash != content_hash)

        backup_path = None

        # 备份旧版本
        if changed and create_backup and old_hash is not None:
            backup_path = self.get_backup_path(phase, content_type)
            try:
                shutil.copy2(file_path, backup_path)
            except Exception as e:
                # 备份失败不影响主流程
                backup_path = None

        # 写入文件（带锁保护）
        lock_path = self.get_lock_path(phase)
        lock_fd = None
        try:
            # 获取锁
            lock_fd = os.open(lock_path, os.O_CREAT | os.O_WRONLY)
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            os.truncate(lock_fd, 0)
            os.write(lock_fd, str(os.getpid()).encode("utf-8"))

            # 写入内容
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            size_bytes = os.path.getsize(file_path)

            return {
                "ok": True,
                "file_path": file_path,
                "hash": content_hash,
                "backup_path": backup_path,
                "size_bytes": size_bytes,
                "changed": changed,
                "old_hash": old_hash,
                "error": None,
            }

        except BlockingIOError:
            return {
                "ok": False,
                "file_path": file_path,
                "hash": None,
                "backup_path": None,
                "size_bytes": 0,
                "changed": False,
                "error": f"文件正在被其他进程编辑，请稍后重试（锁文件：{lock_path}）",
            }
        except Exception as e:
            return {
                "ok": False,
                "file_path": file_path,
                "hash": None,
                "backup_path": None,
                "size_bytes": 0,
                "changed": False,
                "error": f"保存文件失败：{str(e)}",
            }
        finally:
            # 释放锁
            if lock_fd is not None:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_UN)
                    os.close(lock_fd)
                    os.unlink(lock_path)
                except Exception:
                    pass

    def save_with_lock(self, phase: float, content_type: str,
                       content: str) -> Dict[str, Any]:
        """
        写入时加锁（防并发覆盖）。是 save_content 的包装。
        """
        return self.save_content(phase, content_type, content, create_backup=True)

    # ------------------------------------------------------------------------
    # 生命周期：读取
    # ------------------------------------------------------------------------

    def load_content(self, phase: float, content_type: str) -> Optional[str]:
        """
        读取指定文件内容。

        文件不存在或校验失败 → 返回 None

        Returns:
            文件内容（str）或 None
        """
        file_path = self.get_file_path(phase, content_type)
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    # ------------------------------------------------------------------------
    # 新鲜度校验
    # ------------------------------------------------------------------------

    def is_fresh(self, phase: float, content_type: str = CONTENT_TYPE_INTEGRATED) -> bool:
        """
        检查文件是否新鲜。

        新鲜条件：
        1. 文件存在
        2. 修改时间在 FRESHNESS_THRESHOLD_HOURS 内

        Returns:
            bool
        """
        file_path = self.get_file_path(phase, content_type)
        if not os.path.exists(file_path):
            return False

        try:
            mtime = os.path.getmtime(file_path)
            age_hours = (time.time() - mtime) / 3600
            return age_hours <= FRESHNESS_THRESHOLD_HOURS
        except Exception:
            return False

    def validate_before_read(self, phase: float,
                             content_type: str = CONTENT_TYPE_INTEGRATED) -> Dict:
        """
        读取前校验。

        Returns:
            {
                ok: bool,
                error: Optional[str],
                fresh: bool,
                hash_changed: bool,
                current_hash: Optional[str]
            }
        """
        file_path = self.get_file_path(phase, content_type)

        # 文件存在性
        if not os.path.exists(file_path):
            return {
                "ok": False,
                "error": f"文件不存在：{file_path}",
                "fresh": False,
                "hash_changed": False,
                "current_hash": None,
            }

        # 读取内容
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            current_hash = calculate_content_hash(content)
        except Exception as e:
            return {
                "ok": False,
                "error": f"读取文件失败：{str(e)}",
                "fresh": False,
                "hash_changed": False,
                "current_hash": None,
            }

        # 新鲜度
        fresh = self.is_fresh(phase, content_type)

        return {
            "ok": True,
            "error": None,
            "fresh": fresh,
            "hash_changed": False,  # 需要调用方提供 expected_hash 才能判断
            "current_hash": current_hash,
            "size_bytes": len(content.encode("utf-8")),
        }

    # ------------------------------------------------------------------------
    # 用户修改检测
    # ------------------------------------------------------------------------

    def detect_user_modification(self, phase: float,
                                 content_type: str = CONTENT_TYPE_INTEGRATED,
                                 expected_hash: str = None) -> bool:
        """
        检测用户是否手动修改了文件。

        通过 content_hash 对比判断。
        如果 expected_hash 为 None，从 summary 文件中读取。

        Returns:
            bool（True = 用户改过）
        """
        file_path = self.get_file_path(phase, content_type)
        if not os.path.exists(file_path):
            return False

        if expected_hash is None:
            summary = self.load_summary(phase)
            if summary:
                expected_hash = summary.get("content_hash")

        if expected_hash is None:
            return False

        current_hash = calculate_content_hash(self.load_content(phase, content_type) or "")
        return current_hash != expected_hash

    # ------------------------------------------------------------------------
    # 版本控制
    # ------------------------------------------------------------------------

    def backup_exists(self, phase: float, content_type: str) -> bool:
        """检查是否有 .bak 备份版本"""
        backup_path = self.get_backup_path(phase, content_type)
        return os.path.exists(backup_path)

    def restore_backup(self, phase: float, content_type: str) -> Dict[str, Any]:
        """
        恢复上一备份版本。

        Returns:
            {ok: bool, restored_path: str, error: Optional[str]}
        """
        backup_path = self.get_backup_path(phase, content_type)
        if not os.path.exists(backup_path):
            return {
                "ok": False,
                "restored_path": None,
                "error": f"备份文件不存在：{backup_path}",
            }

        file_path = self.get_file_path(phase, content_type)
        try:
            shutil.copy2(backup_path, file_path)
            return {
                "ok": True,
                "restored_path": file_path,
                "error": None,
            }
        except Exception as e:
            return {
                "ok": False,
                "restored_path": None,
                "error": f"恢复备份失败：{str(e)}",
            }

    # ------------------------------------------------------------------------
    # Summary 文件
    # ------------------------------------------------------------------------

    def save_summary(self, phase: float, summary_data: Dict) -> bool:
        """
        保存 PhaseSummary 到 JSON 文件。

        Returns:
            bool
        """
        summary_path = self.get_summary_path(phase)
        try:
            with open(summary_path, "w", encoding="utf-8") as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def load_summary(self, phase: float) -> Optional[Dict]:
        """
        加载 PhaseSummary JSON 文件。

        Returns:
            dict 或 None
        """
        summary_path = self.get_summary_path(phase)
        if not os.path.exists(summary_path):
            return None
        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    # ------------------------------------------------------------------------
    # 流转记录
    # ------------------------------------------------------------------------

    def save_transition(self, transition: Dict) -> bool:
        """
        保存 Phase 流转记录。

        追加到 _transition.json 列表中。
        """
        transition_path = self.get_transition_path()

        # 读取现有记录
        transitions = []
        if os.path.exists(transition_path):
            try:
                with open(transition_path, "r", encoding="utf-8") as f:
                    transitions = json.load(f)
            except Exception:
                transitions = []

        # 追加新记录
        transitions.append(transition)

        try:
            with open(transition_path, "w", encoding="utf-8") as f:
                json.dump(transitions, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def load_transitions(self) -> List[Dict]:
        """
        加载所有流转记录。
        """
        transition_path = self.get_transition_path()
        if not os.path.exists(transition_path):
            return []
        try:
            with open(transition_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_last_transition(self) -> Optional[Dict]:
        """
        获取最近一次流转记录。
        """
        transitions = self.load_transitions()
        return transitions[-1] if transitions else None

    # ------------------------------------------------------------------------
    # 清理
    # ------------------------------------------------------------------------

    def cleanup_intermediate(self, phase: float,
                             keep_types: List[str] = None) -> Dict[str, Any]:
        """
        清理指定 Phase 的中间文件。

        Args:
            phase: Phase 编号
            keep_types: 保留的文件类型，默认保留 integrated.md / review.json / summary.json

        删除：.tmp / .bak / .lock 等临时文件
        保留：integrated / review / summary

        Returns:
            {ok: bool, deleted: [file_paths]}
        """
        if keep_types is None:
            keep_types = [
                CONTENT_TYPE_INTEGRATED,
                CONTENT_TYPE_REVIEW,
                CONTENT_TYPE_SUMMARY,
            ]

        # 需要保留的扩展名
        keep_exts = set()
        for ct in keep_types:
            if ct == CONTENT_TYPE_INTEGRATED:
                keep_exts.add("md")
            else:
                keep_exts.add("json")

        # 需要保留的文件名模式
        keep_patterns = [
            f"_phase{phase}_integrated.md",
            f"_phase{phase}_review.json",
            f"_phase{phase}_summary.json",
            f"_phase{phase}.lock",  # 保留锁文件（正在编辑时）
        ]

        deleted = []
        errors = []

        try:
            for filename in os.listdir(self.workspace):
                file_path = os.path.join(self.workspace, filename)

                # 跳过目录
                if os.path.isdir(file_path):
                    continue

                # 检查是否需要保留
                should_keep = False
                for pattern in keep_patterns:
                    if filename == pattern:
                        should_keep = True
                        break

                # 检查扩展名
                if not should_keep:
                    ext = os.path.splitext(filename)[1].lstrip(".")
                    if ext in keep_exts:
                        should_keep = True

                if not should_keep:
                    try:
                        os.unlink(file_path)
                        deleted.append(file_path)
                    except Exception as e:
                        errors.append(f"{file_path}: {str(e)}")

            return {
                "ok": True,
                "deleted": deleted,
                "errors": errors,
            }

        except Exception as e:
            return {
                "ok": False,
                "deleted": deleted,
                "errors": [str(e)],
            }

    def cleanup_all_intermediates(self) -> Dict[str, Any]:
        """
        清理所有 Phase 的中间文件（保留最终产出）。
        用于论文完成后收尾。

        Returns:
            {ok: bool, deleted: [file_paths], errors: [str]}
        """
        all_deleted = []
        all_errors = []

        # 遍历所有 Phase
        for phase in [1, 2, 3, 3.5, 4, 5]:
            result = self.cleanup_intermediate(phase)
            all_deleted.extend(result.get("deleted", []))
            all_errors.extend(result.get("errors", []))

        return {
            "ok": True,
            "deleted": all_deleted,
            "errors": all_errors,
        }

    def cleanup_tmp_files(self, phase: float = None) -> Dict[str, Any]:
        """
        清理 .tmp 临时文件（激进清理，可用于超期未继续的场景）。

        Returns:
            {ok: bool, deleted: [file_paths]}
        """
        deleted = []
        try:
            if phase is not None:
                # 清理指定 Phase 的 tmp 文件
                patterns = [f"_phase{phase}*.tmp"]
            else:
                # 清理所有 Phase 的 tmp 文件
                patterns = ["_phase*.tmp"]

            for pattern in patterns:
                import fnmatch
                for filename in fnmatch.filter(os.listdir(self.workspace), pattern):
                    file_path = os.path.join(self.workspace, filename)
                    try:
                        os.unlink(file_path)
                        deleted.append(file_path)
                    except Exception:
                        pass

            return {
                "ok": True,
                "deleted": deleted,
            }

        except Exception as e:
            return {
                "ok": False,
                "deleted": deleted,
                "error": str(e),
            }

    # ------------------------------------------------------------------------
    # 完整性校验
    # ------------------------------------------------------------------------

    def validate_integrity(self, phase: float,
                           content_type: str = CONTENT_TYPE_INTEGRATED,
                           required_fields: List[str] = None) -> Dict:
        """
        写入后校验文件完整性。

        检查：
        - 文件可读
        - JSON 文件可解析（如果是 json 类型）
        - 最小字数/章节数门槛

        Returns:
            {ok: bool, errors: [str]}
        """
        file_path = self.get_file_path(phase, content_type)
        errors = []

        # 文件存在
        if not os.path.exists(file_path):
            return {
                "ok": False,
                "errors": [f"文件不存在：{file_path}"],
            }

        # 文件可读
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {
                "ok": False,
                "errors": [f"文件读取失败：{str(e)}"],
            }

        # JSON 可解析（review/summary 类型）
        if content_type in (CONTENT_TYPE_REVIEW, CONTENT_TYPE_SUMMARY):
            try:
                json.loads(content)
            except Exception as e:
                errors.append(f"JSON 解析失败：{str(e)}")

        # 最小字数（integrated 类型）
        if content_type == CONTENT_TYPE_INTEGRATED:
            from .schemas import calculate_word_count
            word_count = calculate_word_count(content)
            if word_count < 1000:
                errors.append(f"字数过少（{word_count} < 1000）")
            if word_count > 200000:
                errors.append(f"字数异常（{word_count} > 200000）")

        return {
            "ok": len(errors) == 0,
            "errors": errors,
        }