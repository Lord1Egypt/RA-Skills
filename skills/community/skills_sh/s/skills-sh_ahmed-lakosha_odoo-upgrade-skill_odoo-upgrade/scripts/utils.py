#!/usr/bin/env python3
"""Shared utilities for Odoo upgrade scripts."""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Generator, Optional, Set

# Directories to skip when walking project trees
SKIP_DIRS: Set[str] = {
    '__pycache__', 'node_modules', '.git', '.venv', 'venv',
    'backup', '.mypy_cache', '.tox', '.eggs', '*.egg-info',
}

# File extensions to skip
SKIP_EXTENSIONS: Set[str] = {'.min.js', '.min.css', '.map'}

# The canonical _jsonRpc helper method for Odoo 19 frontend components.
# Replaces useService("rpc") which is not available in public/frontend context.
JSONRPC_HELPER_METHOD = '''
    async _jsonRpc(endpoint, params = {}) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Csrf-Token': document.querySelector('meta[name="csrf-token"]')?.content || '',
                },
                body: JSON.stringify({
                    jsonrpc: "2.0",
                    method: "call",
                    params: params,
                    id: Math.floor(Math.random() * 1000000)
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error.message || 'RPC call failed');
            }
            return data.result;
        } catch (error) {
            console.error('JSON-RPC call failed:', error);
            throw error;
        }
    }'''

# Standalone jsonrpc function (for non-component contexts)
JSONRPC_STANDALONE_FUNCTION = '''
async function jsonrpc(endpoint, params = {}) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Csrf-Token': document.querySelector('meta[name="csrf-token"]')?.content || '',
            },
            body: JSON.stringify({
                jsonrpc: "2.0",
                method: "call",
                params: params,
                id: Math.floor(Math.random() * 1000000)
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.error) {
            throw new Error(data.error.message || 'RPC call failed');
        }
        return data.result;
    } catch (error) {
        console.error('JSON-RPC call failed:', error);
        throw error;
    }
}'''


def _should_skip_dir(dirname: str) -> bool:
    """Check if a directory should be skipped during traversal."""
    return dirname in SKIP_DIRS or dirname.endswith('.egg-info')


def _should_skip_file(filepath: Path) -> bool:
    """Check if a file should be skipped based on extension."""
    return any(str(filepath).endswith(ext) for ext in SKIP_EXTENSIONS)


def iter_project_files(
    root: str | Path,
    extensions: tuple[str, ...],
    skip_dirs: Set[str] | None = None,
) -> Generator[Path, None, None]:
    """
    Yield file paths matching the given extensions, skipping excluded dirs.

    Args:
        root: Root directory to walk.
        extensions: Tuple of file extensions to match (e.g., ('.py', '.xml')).
        skip_dirs: Optional override for directories to skip.
    """
    skip = skip_dirs if skip_dirs is not None else SKIP_DIRS
    root_path = Path(root)

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Prune skipped directories in-place
        dirnames[:] = [d for d in dirnames if not _should_skip_dir(d)]

        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fpath.suffix in extensions and not _should_skip_file(fpath):
                yield fpath


def create_backup(project_path: str | Path, label: str = "backup") -> Path:
    """
    Create a timestamped backup of the project directory.

    Returns the path to the backup directory.
    """
    project_path = Path(project_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{project_path.name}_{label}_{timestamp}"
    backup_path = project_path.parent / backup_name

    print(f"Creating backup at: {backup_path}")
    shutil.copytree(project_path, backup_path)
    return backup_path


def read_file_safe(path: str | Path, encoding: str = 'utf-8') -> Optional[str]:
    """Read a file with encoding fallback. Returns None on failure."""
    path = Path(path)
    for enc in (encoding, 'utf-8-sig', 'latin-1'):
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
        except OSError as e:
            print(f"  Error reading {path}: {e}")
            return None
    return None


def write_file_safe(path: str | Path, content: str, encoding: str = 'utf-8') -> bool:
    """Write content to file. Returns True on success."""
    try:
        Path(path).write_text(content, encoding=encoding)
        return True
    except OSError as e:
        print(f"  Error writing {path}: {e}")
        return False
