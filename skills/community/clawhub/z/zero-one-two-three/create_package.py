import os
import zipfile
from pathlib import Path

EXCLUDE_DIRS = {"__pycache__", ".vscode", ".git", "tools", "genesis_engine", "knowledge_library", "ephemeral_shares", "data", "temp"}
EXCLUDE_FILES = {
    "Zero-One-Two-Three-SkillHub.zip",
    "package_for_skillhub.ps1",
    "create_package.py",
    "test_sample.md",
    "test_sample.md.locked",
    "unlock_output.txt",
    "lock_test_output.txt",
    "mailbox_output.txt",
    "connector_output.txt",
    "output_test.txt",
}
# 保留 .md (README.md, SKILL.md), .txt (requirements.txt), .json (_meta.json)
EXCLUDE_EXTS = {".pyc", ".whl", ".html", ".bat", ".locked", ".backup"}


def should_include(file_path: str, root: str) -> bool:
    rel = os.path.relpath(file_path, root).replace("\\", "/")
    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()

    if filename in EXCLUDE_FILES:
        return False
    if ext in EXCLUDE_EXTS and filename not in ("requirements.txt", "SKILL.md"):
        return False
    for excl_dir in EXCLUDE_DIRS:
        if rel == excl_dir or rel.startswith(excl_dir + "/"):
            return False
    return True


def create_skill_package():
    root = Path(".")
    zip_filename = "Zero-One-Two-Three-SkillHub.zip"

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in root.rglob("*"):
            if file_path.is_dir():
                continue
            rel = str(file_path)
            if not should_include(rel, str(root)):
                continue
            zipf.write(rel, rel)

    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"打包完成！文件大小: {size_mb:.2f} MB")
    print(f"文件路径: {os.path.abspath(zip_filename)}")


if __name__ == "__main__":
    create_skill_package()