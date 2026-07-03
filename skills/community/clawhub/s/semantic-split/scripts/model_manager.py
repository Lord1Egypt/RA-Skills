#!/usr/bin/env python3
"""
semantic-split 模型管理模块 v0.1.0

Pipeline A 嵌入模型（bge-small / bge-reranker）的下载/校验/索引管理。
多源递进下载（modelscope → hf_mirror → hf_official → hf_direct），
完整性校验，路径索引持久化。

用法:
  python scripts/model_manager.py --download-all         # 下载所有模型
  python scripts/model_manager.py --download bge-small    # 下载指定模型
  python scripts/model_manager.py --list                  # 列出已下载模型
  python scripts/model_manager.py --verify-all            # 验证所有模型
"""

import os
import sys
import json
import re
import hashlib
import shutil
from pathlib import Path

# ============================================================
# 路径常量（铁律4：产出物存至 skills/.standardization/semantic-split/data/）
# ============================================================

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR.parent / ".standardization" / "semantic-split" / "data"
MODELS_DIR = DATA_DIR / "models"
MODEL_INDEX_FILE = MODELS_DIR / "model_index.json"

CACHE_DIR = Path.home() / ".cache" / "huggingface" / "hub"

# ============================================================
# 模型清单
# ============================================================

EMBEDDING_MODELS = [
    {
        "id": "BAAI/bge-small-zh-v1.5",
        "name": "bge-small-zh-v1.5",
        "size_mb": 130,
        "desc": "轻量中文嵌入（Pipeline A 嵌入层）",
        "type": "embedding",
    },
    {
        "id": "BAAI/bge-reranker-base",
        "name": "bge-reranker-base",
        "size_mb": 556,
        "desc": "中文 rerank/重排序（Pipeline A BERT层）",
        "type": "rerank",
    },
]

DOWNLOAD_SOURCES = [
    {"name": "modelscope",     "env": {},                          "desc": "ModelScope 国内镜像（推荐）"},
    {"name": "hf_mirror",      "env": {"HF_ENDPOINT": "https://hf-mirror.com"},       "desc": "HuggingFace 国内镜像"},
    {"name": "hf_official",    "env": {"HF_ENDPOINT": "https://huggingface.co"},      "desc": "HuggingFace 官方源"},
    {"name": "hf_direct",      "env": {},                          "desc": "HF 逐文件下载（稳定）"},
]


# ============================================================
# 工具函数
# ============================================================

def _log(msg: str):
    print(f"  {msg}")


def _ensure_dir(path):
    os.makedirs(str(path), exist_ok=True)


def _normalize(s):
    """归一化字符串为纯字母数字，去除符号差异"""
    return re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '', s.lower())


def _name_similarity(a, b):
    """名称相似度评分（0~100）"""
    if a == b:
        return 100
    if a in b or b in a:
        return 80 + int(10 * min(len(a), len(b)) / max(len(a), len(b)))
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    prefix_score = 40 * i / max(len(a), len(b)) if max(len(a), len(b)) > 0 else 0
    common = sum(1 for c in a if c in b)
    char_score = 30 * common / max(len(a), len(b)) if max(len(a), len(b)) > 0 else 0
    return prefix_score + char_score


def dir_size(path):
    """目录总大小（MB）"""
    total = 0
    for root, _, files in os.walk(str(path)):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return round(total / (1024 * 1024), 1)


# ============================================================
# 模型索引管理
# ============================================================

def _load_index() -> dict:
    if MODEL_INDEX_FILE.exists():
        try:
            return json.loads(MODEL_INDEX_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_index(index: dict):
    _ensure_dir(MODEL_INDEX_FILE.parent)
    tmp = str(MODEL_INDEX_FILE) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    os.replace(tmp, str(MODEL_INDEX_FILE))


def _is_model_dir(path) -> bool:
    """判断目录是否包含有效模型文件"""
    if not os.path.isdir(path):
        return False
    try:
        entries = os.listdir(path)
        model_files = {"config.json", "pytorch_model.bin", "model.safetensors",
                       "vocab.txt", "tokenizer.json"}
        for entry in entries:
            if entry in model_files:
                return True
            if entry.endswith((".bin", ".safetensors")):
                return True
        for entry in entries:
            sub = os.path.join(path, entry)
            if os.path.isdir(sub) and _is_model_dir(sub):
                return True
    except (PermissionError, OSError):
        return False
    return False


def _find_actual_model_path(model_id: str) -> str:
    """从本地缓存中找到模型实际路径"""
    target = model_id.split("/")[-1]
    target_norm = _normalize(target)

    # 1. 检查 MODELS_DIR
    best = None
    best_score = 0
    if MODELS_DIR.exists():
        for d in os.listdir(str(MODELS_DIR)):
            dp = str(MODELS_DIR / d)
            if not os.path.isdir(dp) or d.startswith("."):
                continue
            dn = _normalize(d)
            score = _name_similarity(target_norm, dn)
            if score > best_score and _is_model_dir(dp):
                best_score = score
                best = dp

    if best:
        return best

    # 2. 检查 HF 缓存
    safe_id = f"models--{model_id.replace('/', '--')}"
    snap_dir = CACHE_DIR / safe_id / "snapshots"
    if snap_dir.exists():
        snaps = sorted(snap_dir.iterdir())
        if snaps:
            return str(snaps[-1])

    return ""


# ============================================================
# 多源下载
# ============================================================

def _download_via_hf(model_id: str, source_name: str) -> dict:
    """通过 huggingface_hub 下载模型"""
    env = os.environ.copy()

    source_map = {
        "modelscope":  {"env": {"HF_ENDPOINT": "https://hf-mirror.com"}},
        "hf_mirror":   {"env": {"HF_ENDPOINT": "https://hf-mirror.com"}},
        "hf_official": {"env": {"HF_ENDPOINT": "https://huggingface.co"}},
        "hf_direct":   {"env": {}},
    }

    src = source_map.get(source_name, source_map["hf_official"])
    for k, v in src["env"].items():
        env[k] = v
    env["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

    from huggingface_hub import snapshot_download
    import tempfile

    cache_dir = str(MODELS_DIR)
    _ensure_dir(cache_dir)

    try:
        path = snapshot_download(
            model_id,
            cache_dir=cache_dir,
            local_files_only=False,
            ignore_patterns=["*.h5", "*.ot", "*.msgpack"],
        )
        return {"success": True, "path": path, "source": source_name}
    except Exception as e:
        return {"success": False, "path": "", "source": source_name, "error": str(e)}


def _download_via_hf_direct(model_id: str, source_name: str) -> dict:
    """逐文件下载（稳定模式）"""
    env = os.environ.copy()
    env.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
    env["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

    from huggingface_hub import hf_hub_download, list_repo_files
    import time

    try:
        files = list_repo_files(model_id)
    except Exception:
        env["HF_ENDPOINT"] = "https://huggingface.co"
        try:
            files = list_repo_files(model_id)
        except Exception as e:
            return {"success": False, "path": "", "source": source_name, "error": str(e)}

    skip = [".gitattributes", "onnx/", "flax/", "tf/"]
    essentials = [f for f in files if not any(p in f for p in skip)]
    _log(f"    需下载 {len(essentials)} 个文件（跳过 {len(files)-len(essentials)} 个非必要文件）")

    success = True
    last_path = ""
    for fname in essentials:
        try:
            print(f"      {fname}...", end="", flush=True)
            t0 = time.time()
            path = hf_hub_download(model_id, fname, cache_dir=str(MODELS_DIR))
            elapsed = time.time() - t0
            size = os.path.getsize(path)
            speed = size / elapsed / (1024 * 1024) if elapsed > 0 else 0
            size_s = f"{size/1024/1024:.1f}MB" if size > 1024*1024 else f"{size/1024:.0f}KB"
            print(f" {size_s} ({speed:.1f} MB/s)")
            last_path = str(Path(path).parent)
        except Exception as e:
            print(f" 失败: {e}")
            success = False

    if success and last_path:
        return {"success": True, "path": last_path, "source": source_name}
    return {"success": False, "path": "", "source": source_name, "error": "部分文件下载失败"}


def download_embedding_model(model_id: str) -> dict:
    """下载嵌入/rerank 模型，多源递进"""
    _log(f"下载模型: {model_id}")

    source_methods = {
        "modelscope": _download_via_hf,
        "hf_mirror": _download_via_hf,
        "hf_official": _download_via_hf,
        "hf_direct": _download_via_hf_direct,
    }

    for src in DOWNLOAD_SOURCES:
        name = src["name"]
        _log(f"  尝试源 [{name}]...")
        method = source_methods.get(name)
        if not method:
            continue

        for attempt in range(2):
            _log(f"    第 {attempt+1} 次尝试...")
            result = method(model_id, name)

            if result["success"] and result["path"]:
                # 完整性检查
                path = result["path"]
                ok, detail = _check_integrity(path)
                if ok:
                    _log(f"  [OK] 从 {name} 下载成功: {detail}")

                    # 复制到 models 目录并建索引
                    target = str(MODELS_DIR / model_id.replace("/", "_"))
                    if os.path.exists(target):
                        shutil.rmtree(target)
                    shutil.copytree(path, target)

                    idx = _load_index()
                    idx[model_id] = {
                        "path": target,
                        "source": name,
                        "size_mb": dir_size(target),
                        "status": "ready",
                    }
                    _save_index(idx)
                    return {"success": True, "path": target}
                else:
                    _log(f"    完整性检查失败: {detail}")
            else:
                err = result.get("error", "未知错误")
                _log(f"    失败: {err[-100:]}")

    return {"success": False, "path": "", "error": "所有源均失败"}


def _check_integrity(path: str) -> tuple:
    """检查模型完整性"""
    if not path or not os.path.exists(path):
        return False, "路径不存在"
    model_files = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith((".bin", ".safetensors", ".onnx", ".pt", ".pth")):
                model_files.append(os.path.join(root, f))
    if not model_files:
        return False, "缺少权重文件"
    total = sum(os.path.getsize(f) for f in model_files)
    return True, f"{len(model_files)} 个权重文件, {total/1e6:.1f}MB"

# ============================================================
# 查询接口
# ============================================================

def get_model_path(model_id: str) -> str:
    """获取已下载模型的本地路径"""
    idx = _load_index()
    if model_id in idx:
        return idx[model_id]["path"]
    # 尝试查找
    path = _find_actual_model_path(model_id)
    if path:
        idx[model_id] = {"path": path, "source": "local", "size_mb": dir_size(path), "status": "ready"}
        _save_index(idx)
        return path
    return ""


def list_models() -> list:
    """列出已下载模型"""
    idx = _load_index()
    result = []
    for mid, info in idx.items():
        result.append({"model_id": mid, **info})
    return result


# ============================================================
# CLI
# ============================================================

def cmd_download_all():
    """下载所有模型"""
    _ensure_dir(MODELS_DIR)

    print("\n--- Pipeline A: 嵌入模型 ---")
    for m in EMBEDDING_MODELS:
        mid = m["id"]
        if get_model_path(mid):
            _log(f"  [已有] {mid}")
            continue
        result = download_embedding_model(mid)
        if not result["success"]:
            _log(f"  [!] 下载失败: {result.get('error', '')}")

    print("\n--- Pipeline B: 结构分析（纯正则，零模型依赖） ---")
    _log("  Pipeline B 为纯正则实现，无需下载模型")

    print("\n" + "=" * 50)
    print("下载完成。运行 --list 查看状态")
    print("=" * 50)


def cmd_list():
    models = list_models()
    print(f"\n已下载模型 ({len(models)}):")
    for m in models:
        s = m.get("status", "?")
        p = m.get("path", "")[:60]
        print(f"  {m['model_id']:<40} [{s}] {p}")


def cmd_verify_all():
    print("\n验证所有模型...")
    idx = _load_index()
    if not idx:
        print("  没有已索引的模型")
    for mid, info in idx.items():
        path = info.get("path", "")
        ok, detail = _check_integrity(path) if path else (False, "无路径")
        status = "OK" if ok else "!"
        print(f"  [{status}] {mid:<40} {detail}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="semantic-split 模型管理")
    parser.add_argument("--download-all", action="store_true", help="下载所有模型")
    parser.add_argument("--download", type=str, help="下载指定模型 (bge-small / bge-rerank)")
    parser.add_argument("--list", action="store_true", help="列出已下载模型")
    parser.add_argument("--verify-all", action="store_true", help="验证所有模型完整性")

    args = parser.parse_args()

    if args.list:
        cmd_list()
    elif args.verify_all:
        cmd_verify_all()
    elif args.download_all:
        cmd_download_all()
    elif args.download:
        for m in EMBEDDING_MODELS:
            if m["name"].startswith(args.download):
                result = download_embedding_model(m["id"])
                if not result["success"]:
                    sys.exit(1)
                return
        print(f"[!] 未知模型: {args.download}")
        sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
