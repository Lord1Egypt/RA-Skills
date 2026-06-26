#!/usr/bin/env python3
"""Create a no-thinking Ollama tag for a local Qwen model."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_SYSTEM = """你是一个直接回答的助手。
默认关闭思考模式；不要输出思考过程、推理草稿、<think>、thinking 或 reasoning 内容。
直接给出最终答案。"""

NO_THINK_TEMPLATE = """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
<think>

</think>

"""

DEFAULT_VERIFY_PROMPT = "用一句话回答：1+1等于几？"
BAD_MARKERS = ("thinking...", "<think", "</think", "thinking process", "reasoning process")


class CommandError(RuntimeError):
    pass


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise CommandError(f"{' '.join(cmd)} failed: {detail}")
    return proc


def split_model_ref(ref: str) -> tuple[str, str]:
    last_slash = ref.rfind("/")
    last_colon = ref.rfind(":")
    if last_colon > last_slash:
        name = ref[:last_colon]
        tag = ref[last_colon + 1 :]
    else:
        name = ref
        tag = "latest"
    if not name or not tag:
        raise ValueError(f"Invalid Ollama model reference: {ref!r}")
    return name, tag


def default_target(source: str) -> str:
    name, tag = split_model_ref(source)
    if tag == "latest":
        return f"{name}-nothink:latest"
    return f"{name}:{tag}-nothink"


def looks_like_registry(component: str) -> bool:
    return "." in component or ":" in component or component == "localhost"


def manifest_path(models_dir: Path, model_ref: str) -> Path:
    name, tag = split_model_ref(model_ref)
    parts = name.split("/")
    if len(parts) == 1:
        manifest_parts = ["registry.ollama.ai", "library", parts[0], tag]
    elif looks_like_registry(parts[0]):
        if len(parts) == 2:
            manifest_parts = [parts[0], "library", parts[1], tag]
        else:
            manifest_parts = [parts[0], *parts[1:], tag]
    else:
        manifest_parts = ["registry.ollama.ai", *parts, tag]
    return models_dir / "manifests" / Path(*manifest_parts)


def models_dir_from_args(value: str | None) -> Path:
    if value:
        return Path(value).expanduser()
    env_value = os.environ.get("OLLAMA_MODELS")
    if env_value:
        return Path(env_value).expanduser()
    return Path.home() / ".ollama" / "models"


def parse_parameters(text: str) -> list[tuple[str, str]]:
    params: list[tuple[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.match(r"^(\S+)\s+(.+)$", line)
        if match:
            params.append((match.group(1), match.group(2).strip()))
    return params


def build_modelfile(source: str, params: list[tuple[str, str]], system: str) -> str:
    lines = [
        f"FROM {source}",
        f'TEMPLATE """{NO_THINK_TEMPLATE}"""',
    ]
    saw_stop = False
    for key, value in params:
        if key == "stop":
            saw_stop = True
            continue
        lines.append(f"PARAMETER {key} {value}")
    if not saw_stop:
        lines.append('PARAMETER stop "<|im_end|>"')
    else:
        lines.append('PARAMETER stop "<|im_end|>"')
    lines.append(f'SYSTEM """\n{system}\n"""')
    return "\n".join(lines) + "\n"


def compact_json_bytes(data: object) -> bytes:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def patch_target_manifest(models_dir: Path, target: str) -> tuple[Path, str]:
    target_manifest = manifest_path(models_dir, target)
    if not target_manifest.exists():
        raise FileNotFoundError(f"Target manifest not found: {target_manifest}")

    manifest = json.loads(target_manifest.read_text(encoding="utf-8"))
    old_digest = manifest["config"]["digest"]
    if not old_digest.startswith("sha256:"):
        raise ValueError(f"Unsupported config digest: {old_digest}")

    blobs_dir = models_dir / "blobs"
    old_blob = blobs_dir / f"sha256-{old_digest.split(':', 1)[1]}"
    config = json.loads(old_blob.read_text(encoding="utf-8"))
    config["capabilities"] = [c for c in config.get("capabilities", []) if c != "thinking"]
    config["renderer"] = ""
    config["parser"] = ""

    new_config_bytes = compact_json_bytes(config)
    new_digest = hashlib.sha256(new_config_bytes).hexdigest()
    new_blob = blobs_dir / f"sha256-{new_digest}"
    new_blob.write_bytes(new_config_bytes)

    manifest["config"]["digest"] = f"sha256:{new_digest}"
    manifest["config"]["size"] = len(new_config_bytes)
    target_manifest.write_bytes(compact_json_bytes(manifest))
    return target_manifest, new_digest


def normalize_host(host: str | None) -> str:
    value = host or os.environ.get("OLLAMA_HOST") or "http://127.0.0.1:11434"
    if not value.startswith(("http://", "https://")):
        value = f"http://{value}"
    return value.rstrip("/")


def verify_chat(model: str, prompt: str, host: str) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    request = urllib.request.Request(
        f"{host}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise CommandError(f"Verification request failed: {exc}") from exc

    content = data.get("message", {}).get("content", "")
    lowered = content.lower()
    bad = [marker for marker in BAD_MARKERS if marker in lowered]
    if bad:
        raise CommandError(f"Verification failed; output contains {bad[0]!r}: {content}")
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Existing local Qwen Ollama model, e.g. qwen3.6:35b-mlx")
    parser.add_argument("--target", help="Target no-thinking tag. Defaults to SOURCE with -nothink.")
    parser.add_argument("--models-dir", help="Ollama models directory. Defaults to OLLAMA_MODELS or ~/.ollama/models.")
    parser.add_argument("--host", help="Ollama host for verification. Defaults to OLLAMA_HOST or localhost.")
    parser.add_argument("--system", default=DEFAULT_SYSTEM, help="System message for the derived tag.")
    parser.add_argument("--verify-prompt", default=DEFAULT_VERIFY_PROMPT, help="Prompt used to verify no-thinking output.")
    parser.add_argument("--skip-verify", action="store_true", help="Create and patch the tag without API verification.")
    parser.add_argument("--dry-run", action="store_true", help="Print the target and generated Modelfile without writing.")
    parser.add_argument("--allow-non-qwen", action="store_true", help="Allow model names that do not contain 'qwen'.")
    args = parser.parse_args()

    source = args.source
    target = args.target or default_target(source)
    if source == target:
        parser.error("target must differ from source; never overwrite the source model")
    if "qwen" not in source.lower() and not args.allow_non_qwen:
        parser.error("source name does not contain 'qwen'; pass --allow-non-qwen if this is intentional")

    try:
        run(["ollama", "show", source])
        parameters = parse_parameters(run(["ollama", "show", "--parameters", source]).stdout)
        modelfile = build_modelfile(source, parameters, args.system)

        if args.dry_run:
            print(f"source: {source}")
            print(f"target: {target}")
            print("\n--- Modelfile ---")
            print(modelfile)
            return 0

        with tempfile.TemporaryDirectory(prefix="qwen-nothink-") as tmp:
            modelfile_path = Path(tmp) / "Modelfile"
            modelfile_path.write_text(modelfile, encoding="utf-8")
            run(["ollama", "create", target, "-f", str(modelfile_path)])

        models_dir = models_dir_from_args(args.models_dir)
        target_manifest, new_digest = patch_target_manifest(models_dir, target)

        print(f"created: {target}")
        print(f"manifest: {target_manifest}")
        print(f"config: sha256:{new_digest}")

        if not args.skip_verify:
            content = verify_chat(target, args.verify_prompt, normalize_host(args.host))
            print(f"verified: {content}")

    except (CommandError, FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
