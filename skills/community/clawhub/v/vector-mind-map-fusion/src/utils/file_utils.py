#!/usr/bin/env python3
"""
文件工具 / 脑图解析
"""
import json
import hashlib
from pathlib import Path
from typing import Optional


def atomic_write(file_path: str | Path, content: str, mode: str = 'w'):
    """
    原子写入：先写 tmp，再 rename

    Args:
        file_path: 目标文件路径
        content: 文件内容
        mode: 写入模式
    """
    file_path = Path(file_path)
    tmp_path = file_path.with_suffix('.tmp')

    with open(tmp_path, mode, encoding='utf-8') as f:
        f.write(content)

    tmp_path.rename(file_path)


def ensure_dir(dir_path: str | Path):
    """确保目录存在"""
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def read_jsonl(file_path: str | Path) -> list[dict]:
    """读取 JSONL 文件"""
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results


def write_jsonl(file_path: str | Path, data: list[dict]):
    """写入 JSONL 文件（原子操作）"""
    lines = [json.dumps(obj, ensure_ascii=False) for obj in data]
    atomic_write(file_path, '\n'.join(lines) + '\n')


def chunk_id_hash(session_id: str, byte_offset: int, content: str) -> str:
    """生成 chunk ID（基于 session_id + byte_offset + content 前100字符）"""
    return hashlib.sha256(
        f"{session_id}:{byte_offset}:{content[:100]}".encode()
    ).hexdigest()[:16]


def parse_session_file(session_file: Path) -> dict:
    """解析 session JSONL 文件"""
    return {
        "stem": session_file.stem,
        "size": session_file.stat().st_size,
        "mtime": session_file.stat().st_mtime,
    }