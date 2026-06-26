#!/usr/bin/env python3
"""
Version-Master 核心实现 (v3.0)

提供**单文件级别**的版本管理功能。
每个文件独立管理版本历史，支持保存、恢复、对比和清理。
"""

import os
import json
import hashlib
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class VersionMaster:
    """单文件版本管理工具"""

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd()).resolve()
        self.storage_path = Path.home() / ".workbuddy" / "versions" / "version-master"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # 全局索引文件
        self.index_file = self.storage_path / "index.json"
        self._load_index()

    # ============================================================
    # 元数据管理
    # ============================================================

    def _load_index(self):
        """加载全局索引，加载失败时从磁盘重建"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
                return
            except Exception:
                pass
        # 加载失败或不存在，从磁盘重建索引
        self._rebuild_index_from_disk()

    def _rebuild_index_from_disk(self):
        """扫描 storage_path 下所有 v*.json 文件，从磁盘重建索引"""
        self.index = {"files": {}}
        if not self.storage_path.exists():
            return

        for entry in os.listdir(self.storage_path):
            subdir = os.path.join(self.storage_path, entry)
            if not os.path.isdir(subdir):
                continue
            versions = []
            for vfile in sorted(os.listdir(subdir)):
                if not vfile.startswith('v') or not vfile.endswith('.json'):
                    continue
                vpath = os.path.join(subdir, vfile)
                try:
                    with open(vpath, 'r', encoding='utf-8') as f:
                        vdata = json.load(f)
                    versions.append({
                        "version": vdata["version"],
                        "timestamp": vdata["timestamp"],
                        "content_hash": vdata["content_hash"],
                        "file_size": vdata["file_size"],
                        "summary": vdata.get("summary", ""),
                        "message": vdata.get("message", ""),
                        "version_file": f"{entry}/{vfile}"
                    })
                except Exception:
                    continue
            if versions:
                # 从 v1.json 的 rel_path 推断原始文件名
                rel_path = self._infer_rel_path(entry, subdir, versions)
                file_key = self._file_key(rel_path)
                self.index["files"][file_key] = {
                    "rel_path": rel_path,
                    "versions": versions,
                    "next_version": max(v["version"] for v in versions) + 1
                }
        self._save_index()

    def _infer_rel_path(self, dir_name: str, subdir: str, versions: list) -> str:
        """从目录名和版本数据推断原始相对路径"""
        # 1. 优先使用 v1.json 中嵌入的 rel_path（最可靠）
        v1_path = os.path.join(subdir, "v1.json")
        if os.path.exists(v1_path):
            try:
                with open(v1_path, 'r', encoding='utf-8') as f:
                    v1_data = json.load(f)
                if v1_data.get("rel_path"):
                    return v1_data["rel_path"]
            except Exception:
                pass

        # 2. 从目录名推断：格式为 "工作区ID_文件名"（/ → _，. → -）
        if "_" in dir_name:
            parts = dir_name.split("_", 1)
            if len(parts) == 2:
                # 前缀为工作区ID，剩余部分中 - 还原为 .
                return parts[1].replace("-", ".")

        # 3. 无法识别，原样返回
        return dir_name

    def _save_index(self):
        """保存全局索引"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def _get_file_versions_path(self, file_key: str) -> Path:
        """获取某个文件的版本存储目录"""
        dir_path = self.storage_path / file_key
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def _validate_path(self, rel_path: str) -> Path:
        """
        验证文件路径安全性，防止路径穿越攻击。

        将 rel_path 解析为绝对路径后，确认其位于 workspace_path 内部。
        返回解析后的安全绝对路径，若路径越界则抛出 ValueError。
        """
        # 先规范化，再 resolve 消除 ../ 等
        candidate = (self.workspace_path / rel_path).resolve()
        try:
            candidate.relative_to(self.workspace_path.resolve())
        except ValueError:
            raise ValueError(
                f"不安全的文件路径 '{rel_path}'：路径必须位于工作区目录内，"
                f"不允许使用 '../' 等路径穿越序列。"
            )
        return candidate

    def _file_key(self, rel_path: str) -> str:
        """将文件相对路径转为安全的存储 key，加入工作区标识避免不同工作区同名文件冲突"""
        normalized = rel_path.replace("\\", "/")
        # 用工作区目录名作为前缀，直接可读且天然唯一
        workspace_id = self.workspace_path.name
        # 统一替换路径分隔符和文件名中的点号，确保唯一性
        # 用 _ 表示路径分隔符，用 - 表示原始点号，避免 test_file.txt 和 test.file.txt 冲突
        file_key = normalized.replace("/", "_").replace(".", "-")
        return f"{workspace_id}_{file_key}"

    def _find_file_key_by_rel_path(self, rel_path: str) -> Optional[str]:
        """通过 rel_path 在索引中查找对应的 file_key（支持跨工作区匹配）

        优先匹配当前工作区的 hash 前缀，其次匹配其他工作区。
        返回匹配到的 file_key，未找到返回 None。
        """
        current_key = self._file_key(rel_path)
        if current_key in self.index.get("files", {}):
            return current_key
        # 跨工作区查找：遍历所有 file_key，通过 rel_path 匹配
        normalized = rel_path.replace("\\", "/")
        for key, data in self.index.get("files", {}).items():
            if data.get("rel_path", "").replace("\\", "/") == normalized:
                return key
        return None

    # ============================================================
    # 文件读写工具
    # ============================================================

    def _read_file_content(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """读取文件内容（仅文本文件返回内容；二进制文件返回 type=binary 用于标识）"""
        try:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return {"type": "text", "content": f.read()}
            except UnicodeDecodeError:
                return {"type": "binary"}
        except Exception:
            return None

    def _copy_binary_to_version(self, src_path: Path, version_dir: Path, version_num: int) -> Optional[str]:
        """将二进制文件复制到版本目录，返回文件引用名"""
        try:
            # 保留原始文件扩展名
            ref_name = f"v{version_num}{src_path.suffix}"
            ref_path = version_dir / ref_name
            shutil.copy2(str(src_path), str(ref_path))
            return ref_name
        except Exception:
            return None

    def _write_file_content(self, filepath: Path, version_dir: Path,
                            file_data: Dict[str, Any]) -> bool:
        """恢复文件内容（文本从 JSON 内容写入，二进制从版本目录引用文件复制）"""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            if file_data.get("type") == "binary":
                ref_name = file_data.get("binary_ref")
                if not ref_name:
                    return False
                ref_path = version_dir / ref_name
                if not ref_path.exists():
                    return False
                shutil.copy2(str(ref_path), str(filepath))
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(file_data["content"])
            return True
        except Exception:
            return False

    def _get_content_hash(self, filepath: Path) -> str:
        """从原始文件计算 SHA256 哈希（用于去重）"""
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""

    # ============================================================
    # 智能命名与摘要
    # ============================================================

    def _extract_preview(self, content_data: Optional[Dict[str, Any]], max_len: int = 500) -> str:
        """提取文件内容预览"""
        if not content_data or content_data.get("type") != "text":
            return ""
        text = content_data.get("content", "")
        return text[:max_len].strip()

    def _generate_summary(self, content_data: Optional[Dict[str, Any]], custom_message: Optional[str] = None) -> str:
        """生成版本摘要"""
        parts = []
        if custom_message:
            parts.append(custom_message)
        preview = self._extract_preview(content_data)
        if preview:
            # 取第一行非空内容作为摘要（通常是标题）
            for line in preview.split('\n'):
                line = line.strip().lstrip('#').strip()
                if line and len(line) > 2:
                    parts.append(line[:50])
                    break
        if not parts:
            parts.append("无描述")
        return " | ".join(parts)

    # ============================================================
    # 核心功能：保存版本（单文件）
    # ============================================================

    def save_version(self, file_path: Optional[str] = None, message: Optional[str] = None) -> Dict[str, Any]:
        """
        保存文件版本。

        参数:
            file_path: 要保存的文件路径（相对于工作区）。如果为 None，返回提示信息。
            message: 版本描述/摘要。如果为 None，自动从内容提取。
        """
        try:
            if file_path:
                return self._save_single_file(file_path, message)
            else:
                # 未指定文件：由 AI 调用层负责自动判断上下文中要保存的文件
                return {"success": False, "error": "未指定文件路径，请通过 file_path 参数指定要保存的文件"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _save_single_file(self, rel_path: str, message: Optional[str] = None) -> Dict[str, Any]:
        """保存单个文件的版本"""
        try:
            full_path = self._validate_path(rel_path)
        except ValueError as e:
            return {"success": False, "error": str(e)}
        if not full_path.exists():
            return {"success": False, "error": f"文件不存在: {rel_path}"}

        # 读取文件内容
        content_data = self._read_file_content(full_path)
        if not content_data:
            return {"success": False, "error": f"无法读取文件: {rel_path}"}

        content_hash = self._get_content_hash(full_path)
        file_size = full_path.stat().st_size
        file_key = self._file_key(rel_path)

        # 获取该文件的版本历史
        if file_key not in self.index["files"]:
            # 跨工作区兼容：检查其他工作区是否已保存过同名文件
            existing_key = self._find_file_key_by_rel_path(rel_path)
            if existing_key and existing_key != file_key:
                # 复用已有版本历史，在新 key 下也注册
                existing_data = self.index["files"][existing_key]
                self.index["files"][file_key] = {
                    "rel_path": rel_path,
                    "versions": existing_data["versions"],
                    "next_version": existing_data["next_version"]
                }
            else:
                self.index["files"][file_key] = {
                    "rel_path": rel_path,
                    "versions": [],
                    "next_version": 1
                }

        file_index = self.index["files"][file_key]

        # 去重：检查与最新版本是否相同
        if file_index["versions"]:
            latest = file_index["versions"][-1]
            if latest.get("content_hash") == content_hash:
                return {"success": False, "error": f"文件内容未变化，无需保存新版本"}

        # 生成版本号
        version_num = file_index["next_version"]
        file_index["next_version"] += 1

        # 生成摘要
        summary = self._generate_summary(content_data, message)

        # 保存版本内容
        version_dir = self._get_file_versions_path(file_key)
        version_file = version_dir / f"v{version_num}.json"

        # 二进制文件：复制到版本目录，JSON 中只存引用
        saved_content = content_data
        if content_data.get("type") == "binary":
            binary_ref = self._copy_binary_to_version(full_path, version_dir, version_num)
            if not binary_ref:
                return {"success": False, "error": f"无法保存二进制文件: {rel_path}"}
            saved_content = {"type": "binary", "binary_ref": binary_ref}

        version_data = {
            "version": version_num,
            "timestamp": datetime.now().isoformat(),
            "content_hash": content_hash,
            "file_size": file_size,
            "summary": summary,
            "message": message,
            "rel_path": rel_path,
            "content": saved_content
        }

        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(version_data, f, indent=2, ensure_ascii=False)

        # 更新索引（version_file 使用相对于 storage_path 的相对路径）
        rel_version_file = f"{file_key}/v{version_num}.json"
        file_index["versions"].append({
            "version": version_num,
            "timestamp": version_data["timestamp"],
            "content_hash": content_hash,
            "file_size": file_size,
            "summary": summary,
            "message": message,
            "version_file": rel_version_file
        })

        self._save_index()

        return {
            "success": True,
            "file": rel_path,
            "version": version_num,
            "summary": summary,
            "timestamp": version_data["timestamp"],
            "file_size": file_size
        }

    # ============================================================
    # 核心功能：列出版本
    # ============================================================

    def list_versions(self, file_path: Optional[str] = None, limit: int = 20) -> Dict[str, Any]:
        """
        列出版本历史。

        参数:
            file_path: 文件路径。如果为 None，列出所有有版本历史的文件概览。
            limit: 每个文件最多显示的版本数。
        """
        try:
            if file_path:
                return self._list_file_versions(file_path, limit)
            else:
                return self._list_all_files_versions(limit)
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _list_file_versions(self, rel_path: str, limit: int) -> Dict[str, Any]:
        """列出某个文件的版本历史"""
        file_key = self._find_file_key_by_rel_path(rel_path)
        if not file_key:
            return {"success": False, "error": f"未找到文件 '{rel_path}' 的版本历史"}

        file_index = self.index["files"][file_key]
        versions = list(reversed(file_index["versions"]))  # 最新在前
        versions = versions[:limit]

        return {
            "success": True,
            "file": rel_path,
            "total_versions": len(file_index["versions"]),
            "versions": versions
        }

    def _list_all_files_versions(self, limit: int) -> Dict[str, Any]:
        """列出所有有版本历史的文件及其最新版本"""
        files_info = []
        total_versions = 0
        seen_paths = set()

        for file_key, file_data in self.index["files"].items():
            rel_path = file_data.get("rel_path", file_key)
            if rel_path in seen_paths:
                continue
            seen_paths.add(rel_path)
            versions = file_data.get("versions", [])
            total_versions += len(versions)

            if versions:
                latest = versions[-1]
                files_info.append({
                    "file": rel_path,
                    "version_count": len(versions),
                    "latest_version": latest.get("version"),
                    "latest_summary": latest.get("summary", ""),
                    "latest_timestamp": latest.get("timestamp", ""),
                    "file_size": latest.get("file_size", 0)
                })

        # 按最新修改时间倒序
        files_info.sort(key=lambda x: x.get("latest_timestamp", ""), reverse=True)

        return {
            "success": True,
            "total_files": len(files_info),
            "total_versions": total_versions,
            "files": files_info
        }

    # ============================================================
    # 核心功能：恢复版本
    # ============================================================

    def restore_version(self, file_path: str, version: Optional[int] = None,
                        confirm: bool = False) -> Dict[str, Any]:
        """
        恢复文件到指定版本。

        参数:
            file_path: 文件路径（相对于工作区）
            version: 目标版本号。如果为 None，恢复到最新版本。
            confirm: 是否已确认（安全机制）
        """
        if not confirm:
            return {
                "success": False,
                "requires_confirmation": True,
                "message": f"即将恢复 '{file_path}'，当前文件内容将被覆盖。",
                "file": file_path,
                "version": version
            }

        try:
            file_key = self._find_file_key_by_rel_path(file_path)
            if not file_key:
                return {"success": False, "error": f"未找到文件 '{file_path}' 的版本历史"}

            file_index = self.index["files"][file_key]
            versions = file_index["versions"]

            if not versions:
                return {"success": False, "error": f"文件 '{file_path}' 没有版本历史"}

            # 找到目标版本
            target = None
            if version is not None:
                for v in versions:
                    if v["version"] == version:
                        target = v
                        break
                if not target:
                    return {"success": False, "error": f"版本 v{version} 不存在"}
            else:
                target = versions[-1]

            # 加载版本内容
            version_file_path = self.storage_path / target["version_file"]
            if not version_file_path.exists():
                return {"success": False, "error": f"版本文件丢失: {target['version_file']}"}

            with open(version_file_path, 'r', encoding='utf-8') as f:
                version_data = json.load(f)

            content_data = version_data.get("content")
            if not content_data:
                return {"success": False, "error": "版本数据不完整，缺少文件内容"}

            # 备份当前文件
            try:
                full_path = self._validate_path(file_path)
            except ValueError as e:
                return {"success": False, "error": str(e)}
            if full_path.exists():
                backup_dir = self.workspace_path / ".version_backup"
                backup_dir.mkdir(exist_ok=True)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = backup_dir / f"{ts}_{Path(file_path).name}"
                try:
                    shutil.copy2(str(full_path), str(backup_path))
                except Exception:
                    pass

            # 写入文件（传入版本目录用于二进制文件引用）
            version_dir = self.storage_path / target["version_file"].rsplit("/", 1)[0]
            if self._write_file_content(full_path, version_dir, content_data):
                return {
                    "success": True,
                    "file": file_path,
                    "restored_version": target["version"],
                    "summary": target.get("summary", ""),
                    "message": f"已恢复 '{file_path}' 到版本 v{target['version']}"
                }
            else:
                return {"success": False, "error": "文件写入失败"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============================================================
    # 核心功能：对比版本
    # ============================================================

    def diff_versions(self, file_path: str, version1: Optional[int] = None,
                      version2: Optional[int] = None) -> Dict[str, Any]:
        """
        对比文件的两个版本。

        参数:
            file_path: 文件路径
            version1: 第一个版本号（None 表示当前工作区文件）
            version2: 第二个版本号
        """
        try:
            file_key = self._find_file_key_by_rel_path(file_path)
            if not file_key:
                return {"success": False, "error": f"未找到文件 '{file_path}' 的版本历史"}

            file_index = self.index["files"][file_key]

            # 加载版本2
            target2 = self._find_version_entry(file_index["versions"], version2)
            if not target2:
                return {"success": False, "error": f"版本 v{version2} 不存在"}
            v2_data = self._load_version_content(target2)
            if not v2_data:
                return {"success": False, "error": f"版本 v{version2} 数据不完整"}

            # 加载版本1（或当前文件）
            if version1 is None:
                # 对比当前文件
                try:
                    full_path = self._validate_path(file_path)
                except ValueError as e:
                    return {"success": False, "error": str(e)}
                if not full_path.exists():
                    return {"success": False, "error": f"文件不存在: {file_path}"}
                v1_hash = self._get_content_hash(full_path)
                v1_size = full_path.stat().st_size
                v1_label = "当前版本"
                same = (v1_hash == v2_data["content_hash"])
            else:
                target1 = self._find_version_entry(file_index["versions"], version1)
                if not target1:
                    return {"success": False, "error": f"版本 v{version1} 不存在"}
                v1_data = self._load_version_content(target1)
                if not v1_data:
                    return {"success": False, "error": f"版本 v{version1} 数据不完整"}
                v1_hash = v1_data["content_hash"]
                v1_size = v1_data["file_size"]
                v1_label = f"v{version1}"
                same = (v1_hash == v2_data["content_hash"])

            v2_size = v2_data["file_size"]
            size_diff = v2_size - v1_size

            return {
                "success": True,
                "file": file_path,
                "version1": v1_label,
                "version2": f"v{version2}",
                "same_content": same,
                "version1_size": v1_size,
                "version2_size": v2_size,
                "size_diff": size_diff,
                "version1_hash": v1_hash[:16],
                "version2_hash": v2_data["content_hash"][:16],
                "version1_summary": v1_data.get("summary", "") if version1 is not None else "当前文件",
                "version2_summary": v2_data.get("summary", ""),
                "version1_timestamp": v1_data.get("timestamp", "") if version1 is not None else datetime.now().isoformat(),
                "version2_timestamp": v2_data.get("timestamp", "")
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _find_version_entry(self, versions: List[Dict], version_num: int) -> Optional[Dict]:
        """在版本列表中查找指定版本号"""
        for v in versions:
            if v["version"] == version_num:
                return v
        return None

    def _load_version_content(self, version_entry: Dict) -> Optional[Dict]:
        """加载版本完整内容"""
        try:
            version_file_path = self.storage_path / version_entry["version_file"]
            if not version_file_path.exists():
                return None
            with open(version_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    # ============================================================
    # 核心功能：清理版本
    # ============================================================

    def clean_versions(self, file_path: str, version: Optional[int] = None,
                       confirm: bool = False) -> Dict[str, Any]:
        """
        清理版本。

        参数:
            file_path: 文件路径
            version: 要删除的版本号。如果为 None，删除该文件所有版本历史。
            confirm: 是否已确认
        """
        if not confirm:
            target_desc = f"'{file_path}' 的版本 v{version}" if version else f"'{file_path}' 的所有版本"
            return {
                "success": False,
                "requires_confirmation": True,
                "message": f"即将永久删除 {target_desc}，此操作不可撤销。",
                "file": file_path,
                "version": version
            }

        try:
            file_key = self._find_file_key_by_rel_path(file_path)
            if not file_key:
                return {"success": False, "error": f"未找到文件 '{file_path}' 的版本历史"}

            file_index = self.index["files"][file_key]
            cleaned = 0

            if version is not None:
                # 删除指定版本
                target = self._find_version_entry(file_index["versions"], version)
                if not target:
                    return {"success": False, "error": f"版本 v{version} 不存在"}
                # 删除版本文件
                vf_path = self.storage_path / target["version_file"]
                try:
                    vf_path.unlink()
                except Exception:
                    pass
                file_index["versions"] = [v for v in file_index["versions"] if v["version"] != version]
                cleaned = 1
            else:
                # 删除所有版本
                version_dir = self._get_file_versions_path(file_key)
                for v in file_index["versions"]:
                    try:
                        vf_path = self.storage_path / v["version_file"]
                        vf_path.unlink()
                    except Exception:
                        pass
                # 清空目录
                try:
                    for f in version_dir.iterdir():
                        f.unlink()
                    version_dir.rmdir()
                except Exception:
                    pass
                cleaned = len(file_index["versions"])
                del self.index["files"][file_key]

            self._save_index()

            return {
                "success": True,
                "cleaned_versions": cleaned,
                "message": f"已清理 {cleaned} 个版本"
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


# 全局实例
_instance = None

def get_tool(workspace_path: Optional[str] = None) -> VersionMaster:
    """获取工具实例"""
    global _instance
    if _instance is None:
        _instance = VersionMaster(workspace_path)
    return _instance


if __name__ == "__main__":
    import argparse
    import difflib
    import shutil

    parser = argparse.ArgumentParser(
        description="VersionMaster v3.0 - 单文件版本管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python version_tool.py list
  python version_tool.py list --file report.md
  python version_tool.py save --file report.md -m "更新第三章"
  python version_tool.py diff --file report.md --v1 1 --v2 2
  python version_tool.py restore --file report.md --version 1
  python version_tool.py clean --file report.md --version 1"""
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # list
    list_parser = subparsers.add_parser("list", help="查看版本历史")
    list_parser.add_argument("--file", help="指定文件路径（不指定则列出所有文件）")

    # save
    save_parser = subparsers.add_parser("save", help="保存版本")
    save_parser.add_argument("--file", help="指定文件路径")
    save_parser.add_argument("-m", "--message", help="版本描述")

    # diff
    diff_parser = subparsers.add_parser("diff", help="对比两个版本")
    diff_parser.add_argument("--file", required=True, help="文件路径")
    diff_parser.add_argument("--v1", type=int, help="第一个版本号（不指定则对比当前文件）")
    diff_parser.add_argument("--v2", type=int, required=True, help="第二个版本号")

    # restore
    restore_parser = subparsers.add_parser("restore", help="恢复版本")
    restore_parser.add_argument("--file", required=True, help="文件路径")
    restore_parser.add_argument("--version", type=int, help="目标版本号（不指定则恢复到最新）")
    restore_parser.add_argument("--confirm", action="store_true", help="确认执行（安全机制）")

    # clean
    clean_parser = subparsers.add_parser("clean", help="清理版本")
    clean_parser.add_argument("--file", required=True, help="文件路径")
    clean_parser.add_argument("--version", type=int, help="指定版本号（不指定则删除所有版本）")
    clean_parser.add_argument("--confirm", action="store_true", help="确认执行（安全机制）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(0)

    tool = VersionMaster()
    result = {}

    if args.command == "list":
        result = tool.list_versions(args.file)
        if result.get("success"):
            if args.file:
                # 单文件版本详情
                print(f"\n{result['file']} ({result['total_versions']}个版本)")
                for v in result["versions"]:
                    ts = v.get("timestamp", "")[:19].replace("T", " ")
                    print(f"  v{v['version']} - {v.get('summary', '')} | {ts}")
            else:
                # 所有文件概览
                if not result.get("files"):
                    print("暂无版本历史")
                else:
                    for f in result.get("files", []):
                        print(f"{f['file']} ({f['version_count']}个版本) 最新: v{f['latest_version']} - {f['latest_summary']}")
        else:
            print(f"错误: {result.get('error', '未知错误')}")

    elif args.command == "save":
        result = tool.save_version(args.file, args.message)
        if result.get("success"):
            print(f"已保存 {result['file']} 为 v{result['version']} - {result.get('summary', '')}")
        else:
            print(f"错误: {result.get('error', '未知错误')}")

    elif args.command == "diff":
        result = tool.diff_versions(args.file, args.v1, args.v2)
        if result.get("success"):
            print(f"\n对比: {result['file']} [{result['version1']}] vs [{result['version2']}]")
            if result.get("same_content"):
                print("内容相同，无差异")
            else:
                print(f"大小: {result['version1_size']} -> {result['version2_size']} bytes ({result['size_diff']:+d})")
                print(f"摘要: {result.get('version1_summary', '')} vs {result.get('version2_summary', '')}")
                # 尝试输出行级 diff
                file_key = tool._find_file_key_by_rel_path(args.file)
                file_index = tool.index["files"].get(file_key, {})
                v2_entry = tool._find_version_entry(file_index.get("versions", []), args.v2)
                v2_data = tool._load_version_content(v2_entry) if v2_entry else None
                if v2_data and v2_data["content"].get("type") == "text":
                    if args.v1 is not None:
                        v1_entry = tool._find_version_entry(file_index.get("versions", []), args.v1)
                        v1_data = tool._load_version_content(v1_entry) if v1_entry else None
                    else:
                        v1_data = tool._read_file_content(tool._validate_path(args.file))
                    if v1_data and v1_data.get("type") == "text":
                        lines1 = v1_data["content"].splitlines()
                        lines2 = v2_data["content"]["content"].splitlines()
                        diff_lines = list(difflib.unified_diff(
                            lines1, lines2,
                            fromfile=f"v{args.v1}" if args.v1 else "当前文件",
                            tofile=f"v{args.v2}",
                            lineterm=""
                        ))
                        if diff_lines:
                            print("\n差异详情:")
                            for line in diff_lines:
                                print(line)
        else:
            print(f"错误: {result.get('error', '未知错误')}")

    elif args.command == "restore":
        result = tool.restore_version(args.file, args.version, args.confirm)
        if result.get("success"):
            print(f"已恢复 {result['file']} 到版本 v{result['restored_version']}")
        elif result.get("requires_confirmation"):
            print(f"需要确认: {result.get('message', '')}")
            print("请添加 --confirm 参数确认执行")
        else:
            print(f"错误: {result.get('error', '未知错误')}")

    elif args.command == "clean":
        result = tool.clean_versions(args.file, args.version, args.confirm)
        if result.get("success"):
            print(f"已清理: {result.get('message', '')}")
        elif result.get("requires_confirmation"):
            print(f"需要确认: {result.get('message', '')}")
            print("请添加 --confirm 参数确认执行")
        else:
            print(f"错误: {result.get('error', '未知错误')}")
