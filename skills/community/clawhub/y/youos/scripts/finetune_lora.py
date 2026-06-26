"""LoRA fine-tuning script using mlx_lm on exported feedback pairs."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import get_base_model
from app.core.settings import get_adapter_path, get_settings
from app.db.bootstrap import resolve_sqlite_path

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT_DIR / "data" / "feedback"
BASE_MODEL = get_base_model()


def parse_args() -> argparse.Namespace:
    # Resolved lazily so YOUOS_DATA_DIR set in the calling shell lands the
    # adapter (and DB read) in the active instance, not the repo root —
    # the nightly invokes this script as a subprocess without --db / --adapter-dir.
    default_adapter_dir = get_adapter_path()
    default_db = resolve_sqlite_path(get_settings().database_url)
    p = argparse.ArgumentParser(description="LoRA fine-tuning with mlx_lm")
    p.add_argument("--iters", type=int, default=None, help="Training iterations (overrides auto-scaling)")
    p.add_argument("--num-layers", type=int, default=None, help="Number of LoRA layers (overrides auto-scaling)")
    p.add_argument("--learning-rate", type=float, default=None, help="Learning rate (overrides auto-scaling)")
    p.add_argument("--auto", action=argparse.BooleanOptionalAction, default=True, help="Auto-scale hyperparameters (default: True)")
    p.add_argument("--data-dir", type=str, default=str(DEFAULT_DATA_DIR), help="Directory with train.jsonl/valid.jsonl")
    p.add_argument("--adapter-dir", type=str, default=str(default_adapter_dir), help="Output adapter directory")
    p.add_argument("--db", type=str, default=str(default_db), help="Database path")
    p.add_argument("--dry-run", action="store_true", help="Show config without training")
    p.add_argument("--dpo", action="store_true", help="Use DPO training with data/dpo_train.jsonl")
    p.add_argument(
        "--persona",
        type=str,
        default=None,
        help=(
            "Train a per-persona adapter for the given sender_type cohort "
            "(e.g. --persona internal). When set, the adapter lands at "
            "<models>/adapters/personas/<persona>/ instead of the global "
            "<models>/adapters/latest/, and the post-train "
            "`used_in_finetune=1` marking is skipped (the global adapter "
            "still needs those rows). Used by Phase 2 of the per-persona "
            "adapters work."
        ),
    )
    return p.parse_args()


def count_jsonl_lines(path: Path) -> int:
    if not path.exists():
        return 0
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)


def strip_curriculum_line(train_path: Path) -> bool:
    """Remove the leading ``{"_curriculum": ...}`` annotation line if present.

    The exporter prepends a metadata line recording the warmup split. mlx_lm
    (>=0.31) treats *every* JSONL line as a training record and rejects this one
    ("Unsupported data format"), aborting training on the very first line. The
    curriculum ordering (warmup examples first) lives in the row order, not this
    annotation, so dropping it preserves the curriculum benefit. Idempotent;
    returns True if a line was stripped.
    """
    if not train_path.exists():
        return False
    with open(train_path, encoding="utf-8") as f:
        lines = f.readlines()
    if lines and '"_curriculum"' in lines[0]:
        with open(train_path, "w", encoding="utf-8") as f:
            f.writelines(lines[1:])
        return True
    return False


def compute_auto_config(train_count: int) -> dict[str, int | float]:
    """Compute auto-scaled hyperparameters based on training set size."""
    iters = min(300, max(50, train_count * 3))
    num_layers = 16 if train_count >= 100 else 8
    learning_rate = 5e-5 if train_count < 20 else 1e-5
    return {"iters": iters, "num_layers": num_layers, "learning_rate": learning_rate}


def run_training(args: argparse.Namespace) -> None:
    data_dir = Path(args.data_dir)
    adapter_dir = Path(args.adapter_dir)
    train_path = data_dir / "train.jsonl"
    valid_path = data_dir / "valid.jsonl"

    train_count = count_jsonl_lines(train_path)
    valid_count = count_jsonl_lines(valid_path)

    # Detect, report, and strip curriculum metadata. mlx_lm rejects the
    # annotation line as a bad record (see strip_curriculum_line), so we must
    # remove it before training — not just discount it from the count.
    if train_path.exists():
        with open(train_path, encoding="utf-8") as f:
            first_line = f.readline().strip()
        if first_line and '"_curriculum"' in first_line:
            try:
                meta = json.loads(first_line)
                print(f"Curriculum learning detected: warmup={meta.get('warmup_count')}, total={meta.get('total')}")
            except json.JSONDecodeError:
                pass
            if strip_curriculum_line(train_path):
                train_count -= 1  # metadata line removed; no longer present

    # Determine hyperparameters
    if args.auto:
        auto = compute_auto_config(train_count)
        iters = args.iters if args.iters is not None else auto["iters"]
        num_layers = args.num_layers if args.num_layers is not None else auto["num_layers"]
        learning_rate = args.learning_rate if args.learning_rate is not None else auto["learning_rate"]
    else:
        iters = args.iters if args.iters is not None else 100
        num_layers = args.num_layers if args.num_layers is not None else 8
        learning_rate = args.learning_rate if args.learning_rate is not None else 1e-5

    config = {
        "base_model": BASE_MODEL,
        "data_dir": str(data_dir),
        "adapter_dir": str(adapter_dir),
        "iters": iters,
        "batch_size": 1,
        "num_layers": num_layers,
        "learning_rate": learning_rate,
        "train_pairs": train_count,
        "valid_pairs": valid_count,
        "auto_scaled": args.auto,
    }

    print("LoRA fine-tuning config:")
    for k, v in config.items():
        print(f"  {k}: {v}")

    if args.dry_run:
        print("\n--dry-run: exiting without training.")
        return

    if not train_path.exists():
        print(f"\nError: {train_path} not found. Run export_feedback_jsonl.py first.")
        return

    if train_count < 3:
        print(f"\nError: only {train_count} training pairs. Need at least 3.")
        return

    adapter_dir.mkdir(parents=True, exist_ok=True)

    # DPO mode
    dpo_path = ROOT_DIR / "data" / "dpo_train.jsonl"
    train_type_args: list[str] = []
    if getattr(args, "dpo", False) and dpo_path.exists():
        train_type_args = ["--train-type", "dpo"]
        data_dir = dpo_path.parent
        print("Using DPO training mode with", str(dpo_path))

    cmd = [
        "mlx_lm",
        "lora",
        "--model",
        BASE_MODEL,
        "--train",
        "--data",
        str(data_dir),
        "--adapter-path",
        str(adapter_dir),
        "--iters",
        str(iters),
        "--batch-size",
        "1",
        "--num-layers",
        str(num_layers),
        "--learning-rate",
        str(learning_rate),
        *train_type_args,
    ]

    if valid_path.exists() and valid_count > 0:
        cmd.extend(["--val-batches", "1"])

    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

    if result.returncode != 0:
        print(f"Training failed (exit {result.returncode}):")
        print(result.stderr)
        return

    print(result.stdout)

    # Parse val loss from output
    val_loss = None
    for line in result.stdout.splitlines():
        m = re.search(r"Val loss[:\s]+([\d.]+)", line, re.IGNORECASE)
        if m:
            val_loss = float(m.group(1))

    # Mark feedback pairs as used — but only for global-adapter training.
    # Per-persona training re-uses the entire cohort each run (see the
    # `--persona` matching change in export_feedback_jsonl.py), so marking
    # those rows as used would prevent the global adapter from ever seeing
    # them again. The global adapter still wants the incremental
    # used_in_finetune behaviour, so we keep it for the no-persona path.
    persona = getattr(args, "persona", None)
    db_path = Path(args.db)
    pairs_used = 0
    if db_path.exists() and not persona:
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute("UPDATE feedback_pairs SET used_in_finetune = 1 WHERE used_in_finetune = 0")
            pairs_used = cursor.rowcount
            conn.commit()
        finally:
            conn.close()

    # Save metadata. Persona attribution lets downstream consumers (stats,
    # doctor, the routed generation in Phase 3) distinguish "global adapter
    # trained N pairs ago" from "internal persona adapter trained M pairs
    # ago" — without it both would just say "adapters.safetensors mtime".
    meta = {
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "base_model": BASE_MODEL,
        "pairs_used": pairs_used or train_count,
        "iters": iters,
        "num_layers": num_layers,
        "learning_rate": learning_rate,
        "final_val_loss": val_loss,
        "persona": persona,
    }
    meta_path = adapter_dir / "meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print("\nTraining complete.")
    print(f"  Adapter saved to: {adapter_dir}")
    print(f"  Pairs used: {meta['pairs_used']}")
    print(f"  Val loss: {val_loss}")
    print(f"  Metadata: {meta_path}")


def main() -> None:
    args = parse_args()

    # Persona routing: when --persona is set and --adapter-dir wasn't
    # explicitly overridden, redirect the output to the persona-specific
    # sibling. Without this, persona training would overwrite the global
    # adapter at `adapters/latest/` — defeating the whole point of having
    # per-cohort adapters. Explicit --adapter-dir always wins for the
    # "I know what I'm doing" path (e.g. eval comparisons).
    if args.persona:
        from app.core.settings import get_adapter_path, get_persona_adapter_path

        default_global = str(get_adapter_path())
        if args.adapter_dir == default_global:
            args.adapter_dir = str(get_persona_adapter_path(args.persona))

    run_training(args)


if __name__ == "__main__":
    main()
