#!/usr/bin/env python3
"""YouOS CLI — your personal AI email copilot."""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

import typer

from app.core.data_safety import (
    create_snapshot,
    list_snapshots,
    prune_snapshots,
    restore_snapshot,
    run_startup_safety_checks,
)
from app.core.settings import get_adapter_path, get_instance_root, get_settings
from app.db.bootstrap import resolve_sqlite_path

ROOT_DIR = Path(__file__).resolve().parents[1]

app = typer.Typer(
    name="youos",
    help="YouOS — your personal AI email copilot. Learns your writing style and drafts replies.",
    no_args_is_help=True,
)


def _run(cmd: list[str]) -> None:
    """Run a wrapped script and propagate its exit code.

    Without this, `youos` exited 0 even when the underlying script failed, which
    silently broke scripting/CI gating.
    """
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise typer.Exit(result.returncode)


@app.command()
def quickstart():
    """Lightweight 3-step onramp for users who already have gog configured."""
    import yaml
    from rich.console import Console
    from rich.progress import Progress

    console = Console()
    config_path = ROOT_DIR / "youos_config.yaml"

    # Step 1: Doctor checks
    console.print("[bold]Step 1/3:[/bold] Running doctor checks...")
    from app.core.doctor import run_doctor_checks

    passed, failures = run_doctor_checks()
    if not passed:
        for msg in failures:
            console.print(f"  [red]\u2717[/red] {msg}")
        console.print("\n[bold red]Fix the above issues before continuing.[/bold red]")
        raise SystemExit(1)
    console.print("  [green]\u2713[/green] All required checks passed.")

    # Step 2: Config
    if not config_path.exists():
        console.print("\n[bold]Step 2/3:[/bold] Creating config...")
        emails_input = typer.prompt("Your email address(es), comma-separated")
        emails = [e.strip() for e in emails_input.split(",") if e.strip()]
        display_name = typer.prompt("Display name", default="YouOS")
        domains_input = typer.prompt("Internal domains (comma-separated, optional)", default="")
        internal_domains = [d.strip().lower() for d in domains_input.split(",") if d.strip()] if domains_input else []
        user_cfg = {
            "name": display_name.replace("OS", "") if display_name.endswith("OS") else display_name,
            "display_name": display_name,
            "emails": emails,
        }
        if internal_domains:
            user_cfg["internal_domains"] = internal_domains
        config = {
            "user": user_cfg,
            "ingestion": {"accounts": emails},
        }
        config_path.write_text(yaml.dump(config, default_flow_style=False))
        console.print(f"  Config written to {config_path}")
    else:
        console.print("\n[bold]Step 2/3:[/bold] Config already exists, skipping.")

    # Step 3: Gmail ingestion
    console.print("\n[bold]Step 3/3:[/bold] Running Gmail ingestion...")
    from scripts.nightly_pipeline import step_ingest_gmail

    with Progress(console=console) as progress:
        task = progress.add_task("Ingesting emails...", total=None)
        ok = step_ingest_gmail()
        progress.update(task, completed=100, total=100)

    if ok:
        console.print("\n[bold green]Quickstart complete![/bold green]")
    else:
        console.print("\n[bold yellow]Ingestion had warnings, but setup is done.[/bold yellow]")

    console.print("Run: [bold]youos ui[/bold] to launch the web interface.")


@app.command(name="export")
def export_data(
    output: str = typer.Option(None, "--output", "-o", help="Output path for the archive"),
):
    """Export YouOS data to a tar.gz archive for backup."""
    import tarfile

    if output is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output = str(Path.home() / f"youos-backup-{today}.tar.gz")

    output_path = Path(output).expanduser().resolve()
    # Source from the active instance (YOUOS_DATA_DIR if set, else repo).
    # Archive layout stays repo-relative ("var/youos.db", "youos_config.yaml",
    # "configs/...", "models/adapters/latest/...") so the format is stable
    # across instances and existing backups still restore cleanly.
    settings = get_settings()
    instance_root = get_instance_root()
    db_source = resolve_sqlite_path(settings.database_url)
    config_source = instance_root / "youos_config.yaml"
    configs_dir = Path(settings.configs_dir)

    include_paths = [
        ("var/youos.db", db_source),
        ("youos_config.yaml", config_source),
    ]
    if configs_dir.is_dir():
        for f in configs_dir.rglob("*"):
            if f.is_file():
                arcname = str(Path("configs") / f.relative_to(configs_dir))
                include_paths.append((arcname, f))
    adapters_dir = get_adapter_path()
    if adapters_dir.is_dir():
        for f in adapters_dir.rglob("*"):
            if f.is_file():
                arcname = str(Path("models/adapters/latest") / f.relative_to(adapters_dir))
                include_paths.append((arcname, f))

    with tarfile.open(output_path, "w:gz") as tar:
        for arcname, filepath in include_paths:
            if filepath.exists():
                tar.add(str(filepath), arcname=arcname)

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"Archive created: {output_path} ({size_mb:.1f} MB)")


@app.command(name="import")
def import_data(
    input_path: str = typer.Option(..., "--input", "-i", help="Path to a youos backup tar.gz"),
):
    """Import YouOS data from a tar.gz archive."""
    import tarfile

    archive = Path(input_path).expanduser().resolve()
    if not archive.exists():
        print(f"File not found: {archive}")
        raise SystemExit(1)

    # Extract into the active instance, not the repo root. Archive layout is
    # repo-relative ("var/youos.db", "youos_config.yaml", "configs/...",
    # "models/adapters/latest/...") so the same archive restores into any
    # instance — pre- or post-PR-#16 — without format changes.
    settings = get_settings()
    instance_root = get_instance_root()
    db_path = resolve_sqlite_path(settings.database_url)
    if db_path.exists():
        confirm = typer.confirm(f"{db_path} already exists. Overwrite?", default=False)
        if not confirm:
            print("Import cancelled.")
            raise SystemExit(0)

    instance_root.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(path=instance_root, filter="data")

    print(f"Imported from {archive} into {instance_root}")


@app.command()
def setup(
    check_only: bool = typer.Option(False, "--check-only", help="Run non-interactive cold-start setup checks and exit"),
):
    """Run the setup wizard (or cold-start checks)."""
    cmd = [sys.executable, str(ROOT_DIR / "scripts" / "setup_wizard.py")]
    if check_only:
        cmd.append("--check-only")
    _run(cmd)


@app.command()
def status():
    """Show corpus size, model status, last run."""
    from app.core.config import (
        get_display_name,
        get_ingestion_accounts,
        get_last_ingest_at,
        get_server_port,
        get_tailscale_hostname,
        get_user_emails,
        get_user_name,
        is_ollama_enabled,
        load_config,
    )
    config = load_config()
    settings = get_settings()
    name = get_user_name(config)
    emails = get_user_emails(config)
    port = get_server_port(config)
    ts_hostname = get_tailscale_hostname(config)

    print()
    print(f"{get_display_name(config)} Status")
    print("\u2501" * 34)

    print(f"User:        {name} ({', '.join(emails) or 'not configured'})")

    # Server status
    try:
        result = subprocess.run(
            ["pgrep", "-f", "uvicorn.*app.main:app"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        server_running = result.returncode == 0
    except Exception:
        server_running = False
    server_icon = "\u2705" if server_running else "\u274c"
    print(f"Server:      {server_icon} {'running' if server_running else 'stopped'} on port {port}")

    # Ollama status
    ollama_cfg = config.get("model", {}).get("ollama", {})
    if is_ollama_enabled(config):
        ollama_model = ollama_cfg.get("model", "mistral")
        print(f"Ollama:      \u2705 enabled ({ollama_model})")
    else:
        print("Ollama:      \u274c not configured")

    # Tailscale
    if ts_hostname:
        print(f"Tailscale:   \u2705 https://{ts_hostname}.ts.net")
    else:
        print("Tailscale:   not configured")

    print()

    db_path = resolve_sqlite_path(settings.database_url)
    if not db_path.exists():
        print(f"Database:    not found ({db_path})")
        print("Run 'youos setup' to initialize.")
        print("\u2501" * 34)
        return

    conn = sqlite3.connect(db_path)
    try:
        docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        pairs = conn.execute("SELECT COUNT(*) FROM reply_pairs").fetchone()[0]
        feedback = conn.execute("SELECT COUNT(*) FROM feedback_pairs").fetchone()[0]

        try:
            reviewed_today = conn.execute("SELECT COUNT(*) FROM feedback_pairs WHERE DATE(created_at) = DATE('now')").fetchone()[0]
        except Exception:
            reviewed_today = 0

        print(f"Corpus:      {docs:,} docs | {pairs:,} reply pairs")
        print(f"Feedback:    {feedback} pairs ({reviewed_today} today)")

        # Embedding coverage
        try:
            embedded = conn.execute("SELECT COUNT(*) FROM documents WHERE embedding IS NOT NULL").fetchone()[0]
            pct = (embedded / docs * 100) if docs > 0 else 0
            print(f"Embeddings:  {embedded:,}/{docs:,} ({pct:.0f}%)")
        except Exception:
            pass
    except Exception:
        print("Database exists but tables may not be initialized.")

    conn.close()

    # Model info
    model_used = config.get("model", {}).get("base", "Qwen/Qwen2.5-1.5B-Instruct")
    adapter_path = get_adapter_path() / "adapters.safetensors"
    if adapter_path.exists():
        mtime = os.path.getmtime(adapter_path)
        dt = datetime.fromtimestamp(mtime)
        print(f"Model:       {model_used} (trained {dt.strftime('%Y-%m-%d %H:%M')})")
    else:
        print(f"Model:       {model_used} (not fine-tuned yet)")

    # Last ingestion dates
    accounts = get_ingestion_accounts(config)
    ingest_parts = []
    for acct in accounts:
        last = get_last_ingest_at(acct, config)
        if last:
            ingest_parts.append(f"{last[:10]} ({acct})")
    if ingest_parts:
        print(f"Last ingest: {', '.join(ingest_parts)}")

    # Benchmark results
    try:
        conn = sqlite3.connect(db_path)
        total = conn.execute("SELECT COUNT(*) FROM benchmark_cases").fetchone()[0]
        passed = conn.execute("SELECT COUNT(*) FROM eval_runs WHERE status = 'pass'").fetchone()[0]
        conn.close()
        if total > 0:
            print(f"Benchmark:   {passed}/{total} pass")
    except Exception:
        pass

    print("\u2501" * 34)


@app.command()
def ui():
    """Open the web UI in your browser."""
    from app.core.config import get_server_port

    port = get_server_port()
    url = f"http://localhost:{port}/feedback"
    print(f"Opening {url}")
    webbrowser.open(url)


@app.command()
def draft(
    message: str = typer.Argument(..., help="The inbound email text to draft a reply to"),
    sender: str = typer.Option(None, help="Sender email address"),
    mode: str = typer.Option(None, help="Override mode: work or personal"),
):
    """Draft a reply to an email."""
    from app.core.settings import get_settings
    from app.generation.service import DraftRequest, generate_draft

    settings = get_settings()
    request = DraftRequest(
        inbound_message=message,
        mode=mode,
        sender=sender,
    )
    response = generate_draft(
        request,
        database_url=settings.database_url,
        configs_dir=settings.configs_dir,
    )
    print(response.draft)


@app.command()
def improve(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Print Rich progress for each step"),
):
    """Run the nightly pipeline manually (ingest, feedback, finetune, autoresearch)."""
    cmd = [sys.executable, str(ROOT_DIR / "scripts" / "nightly_pipeline.py")]
    if verbose:
        cmd.append("--verbose")
    _run(cmd)


@app.command()
def note(
    email: str = typer.Argument(..., help="Sender email address"),
    text: str = typer.Argument(..., help="Relationship note"),
):
    """Add a sender relationship note and rebuild profile for that sender."""
    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)
    if not db_path.exists():
        print(f"Database not found: {db_path}. Run 'youos setup' first.")
        raise typer.Exit(1)
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(
            "UPDATE sender_profiles SET relationship_note = ?, updated_at = CURRENT_TIMESTAMP WHERE email = ?",
            (text, email.lower()),
        )
        if cur.rowcount == 0:
            conn.execute(
                "INSERT INTO sender_profiles (email, relationship_note) VALUES (?, ?)",
                (email.lower(), text),
            )
        conn.commit()
        print(f"Note saved for {email.lower()}")
    finally:
        conn.close()

    # Rebuild profile for this sender
    from scripts.build_sender_profiles import build_profiles

    try:
        new_count, updated_count = build_profiles(db_path, sender_email=email.lower())
        total = new_count + updated_count
        if total > 0:
            print(f"Profile updated for {email.lower()}")
        else:
            print(f"No reply pairs found for {email.lower()}, profile not rebuilt")
    except Exception as exc:
        print(f"Profile rebuild failed: {exc}")


@app.command()
def corpus(
    output_json: bool = typer.Option(False, "--json", help="Output raw JSON"),
):
    """Print corpus health report (pair count, docs, quality scores, top senders)."""
    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)

    if not db_path.exists():
        print(f"Database not found: {db_path}")
        raise SystemExit(1)

    from scripts.report_ingestion_health import corpus_report

    report = corpus_report(db_path)

    if output_json:
        import json

        print(json.dumps(report, indent=2))
        return

    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title="YouOS Corpus Report", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Value")

    table.add_row("Reply pairs", f"{report['pair_count']:,}")
    table.add_row("Documents", f"{report['doc_count']:,}")
    table.add_row("Feedback pairs", f"{report['feedback_pairs']:,}")
    table.add_row("Embedding coverage", f"{report['embedding_pct']:.1f}%")

    qs = report["quality_score"]
    if qs["min"] is not None:
        table.add_row("Quality score (min/median/max)", f"{qs['min']}/{qs['median']}/{qs['max']}")
    else:
        table.add_row("Quality score", "N/A")

    console.print(table)

    if report["top_senders"]:
        sender_table = Table(title="Top Senders by Pair Count", show_header=True, header_style="bold cyan")
        sender_table.add_column("Email")
        sender_table.add_column("Name")
        sender_table.add_column("Replies", justify="right")
        for s in report["top_senders"][:5]:
            sender_table.add_row(s["email"], s.get("display_name") or "", str(s["reply_count"]))
        console.print(sender_table)


@app.command()
def stats():
    """Print stats summary."""
    from rich.console import Console
    from rich.table import Table

    from app.core.settings import get_settings
    from app.core.stats import get_corpus_stats, get_model_status, get_pipeline_status

    settings = get_settings()
    console = Console()

    corpus = get_corpus_stats(settings.database_url)
    model = get_model_status(Path(settings.configs_dir))
    pipeline = get_pipeline_status(get_instance_root())

    table = Table(title="YouOS Stats", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Value")

    table.add_row("Documents", f"{corpus['total_documents']:,}")
    table.add_row("Reply pairs", f"{corpus['total_reply_pairs']:,}")
    table.add_row("Feedback pairs", f"{corpus['total_feedback_pairs']:,}")
    table.add_row("Reviewed today", str(corpus["reviewed_today"]))
    table.add_row("Reviewed this week", str(corpus["reviewed_this_week"]))
    emb = corpus["embedding_pct"]
    table.add_row("Embedding coverage", f"{emb:.1f}%" if emb is not None else "N/A")
    table.add_row("Generation model", model["generation_model"])
    table.add_row("LoRA adapter", "Yes" if model["lora_adapter_exists"] else "No")
    table.add_row("Last fine-tune", model.get("lora_trained_at") or "N/A")

    if pipeline:
        status = pipeline.get("status", "unknown")
        table.add_row("Pipeline status", status.upper())
        table.add_row("Pipeline last run", pipeline.get("run_at", "N/A"))

    console.print(table)


@app.command()
def ingest(
    whatsapp: str = typer.Option(None, "--whatsapp", help="Path to a WhatsApp chat export .txt file"),
):
    """Run email ingestion manually."""
    if whatsapp:
        from app.ingestion.whatsapp import ingest_whatsapp_export

        result = ingest_whatsapp_export(Path(whatsapp))
        print(f"[{result.status}] {result.detail}")
        return
    _run([sys.executable, str(ROOT_DIR / "scripts" / "ingest_gmail_threads.py"), "--live"])


@app.command()
def finetune():
    """Run LoRA fine-tuning manually."""
    _run([sys.executable, str(ROOT_DIR / "scripts" / "export_feedback_jsonl.py")])
    _run([sys.executable, str(ROOT_DIR / "scripts" / "finetune_lora.py")])


@app.command(name="finetune-milestone")
def finetune_milestone(
    threshold: int = typer.Option(30, "--threshold", help="Minimum quality feedback pairs required"),
    run: bool = typer.Option(False, "--run", help="Run pre-eval -> finetune -> post-eval once threshold is met"),
):
    """Check fine-tune milestone readiness (and optionally execute full milestone run)."""
    cmd = [
        sys.executable,
        str(ROOT_DIR / "scripts" / "finetune_milestone.py"),
        "--threshold",
        str(threshold),
    ]
    if run:
        cmd.append("--run")
    _run(cmd)


@app.command(name="eval")
def run_eval(
    golden: bool = typer.Option(False, "--golden", help="Run golden benchmark evaluation"),
):
    """Run benchmark evaluation."""
    if golden:
        _run([sys.executable, str(ROOT_DIR / "scripts" / "run_golden_eval.py")])
    else:
        _run([sys.executable, str(ROOT_DIR / "scripts" / "run_eval.py")])


@app.command(name="compare-models")
def compare_models(
    limit: int = typer.Option(20, "--limit", help="Number of your real reply pairs to compare on"),
    backends: str = typer.Option(None, "--backends", help="Comma-separated subset (mlx,ollama,claude); default auto-detect"),
    semantic: bool = typer.Option(False, "--semantic", help="Include the embedding-based semantic score"),
):
    """Compare generation backends (MLX/Ollama/Claude) on your own mail by voice-match."""
    cmd = [sys.executable, str(ROOT_DIR / "scripts" / "compare_models.py"), "--limit", str(limit)]
    if backends:
        cmd += ["--backends", backends]
    if semantic:
        cmd += ["--semantic"]
    _run(cmd)


@app.command()
def serve():
    """Start the YouOS web server."""
    from app.core.config import get_server_host, get_server_port

    port = get_server_port()
    host = get_server_host()
    subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            host,
            "--port",
            str(port),
        ],
        cwd=str(ROOT_DIR),
    )


@app.command()
def teardown(
    all_data: bool = typer.Option(False, "--all", help="Delete everything without prompting"),
):
    """Remove all YouOS user data (corpus, model, database)."""
    from scripts.teardown import teardown as do_teardown

    do_teardown(delete_all=all_data)


@app.command()
def doctor():
    """Check system requirements and project health."""
    from rich.console import Console

    from app.core.doctor import run_doctor_checks_full

    console = Console()
    console.print("[bold]YouOS Doctor[/bold]\n")

    passed, failures, warnings = run_doctor_checks_full()

    # Print required checks
    required_labels = [
        "Python >= 3.11",
        "gog CLI installed",
        "mlx_lm importable",
        "youos_config.yaml exists",
        "user.emails set in config",
    ]
    for label in required_labels:
        # Check if any failure message relates to this label
        is_failed = any(label.lower().split()[0] in f.lower() for f in failures)
        if not is_failed:
            # More precise matching
            is_failed = False
            for f in failures:
                if label == "Python >= 3.11" and "python" in f.lower():
                    is_failed = True
                elif label == "gog CLI installed" and "gog" in f.lower():
                    is_failed = True
                elif label == "mlx_lm importable" and "mlx_lm" in f.lower():
                    is_failed = True
                elif label == "youos_config.yaml exists" and "youos_config" in f.lower():
                    is_failed = True
                elif label == "user.emails set in config" and "user.emails" in f.lower():
                    is_failed = True
        icon = "\u2713" if not is_failed else "\u2717"
        style = "green" if not is_failed else "red"
        console.print(f"  [{style}]{icon}[/{style}] {label} (required)")

    # Print warnings
    warning_labels = [
        ("var/youos.db exists", "youos.db"),
        (">= 3GB disk free", "disk"),
        ("models/ dir has content", "models/"),
        ("Port free", "port"),
    ]
    for label, key in warning_labels:
        is_warned = any(key.lower() in w.lower() for w in warnings)
        icon = "\u2713" if not is_warned else "\u2717"
        style = "green" if not is_warned else "yellow"
        console.print(f"  [{style}]{icon}[/{style}] {label} (warning)")

    console.print()
    if passed:
        console.print("[bold green]All required checks passed.[/bold green]")
        raise SystemExit(0)
    else:
        console.print("[bold red]Some required checks failed.[/bold red]")
        raise SystemExit(1)


config_app = typer.Typer(help="View and toggle YouOS feature flags.")
app.add_typer(config_app, name="config")


@config_app.command(name="list")
def config_list():
    """List all feature flags and their current values."""
    from app.core.feature_flags import list_flags

    for f in list_flags():
        choices = f"  ({'/'.join(f['choices'])})" if f["type"] == "choice" else ""
        typer.echo(f"  {f['key']:46s} = {str(f['value']):7s}  {f['label']}{choices}")


@config_app.command(name="get")
def config_get(key: str = typer.Argument(help="Dotted flag key, e.g. generation.multi_candidate.enabled")):
    """Print the current value of a feature flag."""
    from app.core.feature_flags import get_flag

    try:
        typer.echo(get_flag(key))
    except KeyError:
        typer.echo(f"Unknown flag: {key}", err=True)
        raise typer.Exit(1) from None


@config_app.command(name="set")
def config_set(
    key: str = typer.Argument(help="Dotted flag key, e.g. generation.multi_candidate.enabled"),
    value: str = typer.Argument(help="New value (true/false for toggles)"),
):
    """Set a feature flag (writes youos_config.yaml)."""
    from app.core.feature_flags import set_flag

    try:
        stored = set_flag(key, value)
    except KeyError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from None
    except ValueError as exc:
        typer.echo(f"Invalid value for {key}: {exc}", err=True)
        raise typer.Exit(1) from None
    typer.echo(f"✓ set {key} = {stored}")


service_app = typer.Typer(help="Run the YouOS server reliably in the background (macOS launchd).")
app.add_typer(service_app, name="service")


@service_app.command(name="install")
def service_install():
    """Install + start YouOS as a background service (runs at login, auto-restarts)."""
    from app.core import service

    ok, msg = service.install()
    typer.echo(("✓ " if ok else "✗ ") + msg)
    if not ok:
        raise typer.Exit(1)


@service_app.command(name="uninstall")
def service_uninstall():
    """Stop + remove the background service."""
    from app.core import service

    _, msg = service.uninstall()
    typer.echo(msg)


@service_app.command(name="status")
def service_status():
    """Show whether the background service is installed / running."""
    from app.core import service

    typer.echo(f"YouOS service: {service.status()}")


model_app = typer.Typer(help="Manage the local model.")
app.add_typer(model_app, name="model")


@model_app.command(name="set")
def model_set(
    model_name: str = typer.Argument(help="HuggingFace model name, e.g. Qwen/Qwen2.5-3B-Instruct"),
):
    """Set the base model for fine-tuning and generation."""
    import yaml

    config_path = ROOT_DIR / "youos_config.yaml"
    config = yaml.safe_load(config_path.read_text()) if config_path.exists() else {}
    config.setdefault("model", {})["base"] = model_name
    config_path.write_text(yaml.dump(config, default_flow_style=False))
    typer.echo(f"✅ Model set to {model_name}")
    typer.echo("   Run `youos finetune` to train a new adapter on this model.")


@model_app.command(name="show")
def model_show():
    """Show the currently configured model."""
    import yaml

    config_path = ROOT_DIR / "youos_config.yaml"
    config = yaml.safe_load(config_path.read_text()) if config_path.exists() else {}
    base = config.get("model", {}).get("base", "Qwen/Qwen2.5-1.5B-Instruct")
    adapter = get_adapter_path() / "adapters.safetensors"
    typer.echo(f"Base model:  {base}")
    typer.echo(f"Adapter:     {'✅ trained' if adapter.exists() else '❌ not trained yet'}")


server_app = typer.Typer(help="Manage the warm local-model server (loads the model once for fast drafting).")
model_app.add_typer(server_app, name="server")


@server_app.command(name="status")
def model_server_status():
    """Show whether the warm model server is running."""
    from app.core import model_server

    cfg = model_server.get_server_config()
    state = "running" if model_server.is_healthy() else "not running"
    typer.echo(f"Model server: {state} (port {cfg['port']}, enabled={cfg['enabled']}, serving {model_server.model_label()})")


@server_app.command(name="start")
def model_server_start():
    """Start the warm model server (loads the base model + global adapter once)."""
    from app.core import model_server

    typer.echo("Starting model server (loading the model may take a few seconds)…")
    if model_server.ensure_running():
        typer.echo(f"✓ Model server running on port {model_server.get_server_config()['port']} ({model_server.model_label()})")
    else:
        typer.echo("✗ Model server failed to start — check that mlx_lm is installed.")
        raise typer.Exit(1)


@server_app.command(name="stop")
def model_server_stop():
    """Stop the warm model server."""
    from app.core import model_server

    model_server.stop()
    typer.echo("Model server stopped.")


@server_app.command(name="restart")
def model_server_restart():
    """Restart the server (e.g. to pick up a newly trained adapter)."""
    from app.core import model_server

    typer.echo("✓ restarted" if model_server.restart() else "✗ failed to restart")


ollama_app = typer.Typer(help="Manage Ollama integration.")
model_app.add_typer(ollama_app, name="ollama")


@ollama_app.command(name="enable")
def ollama_enable():
    """Enable Ollama as a generation backend."""
    from app.core.config import _load_raw_config, save_config

    config = _load_raw_config()
    config.setdefault("model", {}).setdefault("ollama", {})["enabled"] = True
    config["model"]["fallback"] = "ollama"
    save_config(config)
    typer.echo("Ollama enabled as generation fallback.")


@ollama_app.command(name="disable")
def ollama_disable():
    """Disable Ollama as a generation backend."""
    from app.core.config import _load_raw_config, save_config

    config = _load_raw_config()
    config.setdefault("model", {}).setdefault("ollama", {})["enabled"] = False
    if config.get("model", {}).get("fallback") == "ollama":
        config["model"]["fallback"] = "claude"
    save_config(config)
    typer.echo("Ollama disabled. Fallback set to claude.")


@app.command()
def feedback(
    inbound: str = typer.Option(None, "--inbound", help="Inbound email text"),
    reply: str = typer.Option(None, "--reply", help="Your reply text"),
    rating: int = typer.Option(4, "--rating", help="Rating 1-5", min=1, max=5),
    note: str = typer.Option(None, "--note", help="Optional feedback note"),
    sender: str = typer.Option(None, "--sender", help="Sender email address"),
    stdin: bool = typer.Option(False, "--stdin", help="Read inbound from stdin"),
    reply_stdin: bool = typer.Option(False, "--reply-stdin", help="Read reply from stdin"),
):
    """Submit a feedback pair directly (bypasses draft generation)."""
    import sys as _sys

    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    if stdin:
        inbound = _sys.stdin.read()
    if reply_stdin:
        reply = _sys.stdin.read()

    if not inbound:
        print("Error: --inbound is required (or use --stdin)")
        raise SystemExit(1)
    if not reply:
        print("Error: --reply is required (or use --reply-stdin)")
        raise SystemExit(1)

    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)
    if not db_path.exists():
        print(f"Database not found: {db_path}. Run 'youos setup' first.")
        raise SystemExit(1)

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO feedback_pairs
                (inbound_text, generated_draft, edited_reply, feedback_note,
                 rating, edit_distance_pct, used_in_finetune)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (inbound, reply, reply, note, rating, 0.0, 0),
        )
        conn.commit()
        total = conn.execute("SELECT COUNT(*) FROM feedback_pairs").fetchone()[0]
    finally:
        conn.close()

    print(f"Feedback pair saved. Total pairs: {total}")


@app.command("health-check")
def health_check(as_json: bool = typer.Option(False, "--json", help="Output JSON")):
    """Run startup safety checks and print report."""
    settings = get_settings()
    report = run_startup_safety_checks(settings)
    if as_json:
        import json

        print(json.dumps(report.to_dict(), indent=2))
        return

    print(f"DB: {report.db_path}")
    print(f"Counts: {report.table_counts}")
    if report.warnings:
        print("Warnings:")
        for w in report.warnings:
            print(f"- {w}")
    else:
        print("Warnings: none")


@app.command("snapshot-create")
def snapshot_create(
    tier: str = typer.Option("manual", "--tier", help="manual|hourly|daily"),
):
    """Create a sqlite snapshot for current instance."""
    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)
    try:
        snap = create_snapshot(db_path, tier=tier)
    except ValueError as exc:
        print(f"Error: {exc}")
        raise typer.Exit(1) from exc
    prune_snapshots(db_path)
    print(str(snap))


@app.command("snapshot-list")
def snapshot_list():
    """List available snapshots."""
    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)
    snaps = list_snapshots(db_path)
    for snap in snaps:
        print(str(snap))


@app.command("snapshot-prune")
def snapshot_prune(
    keep_hourly: int = typer.Option(None, "--keep-hourly", help="Override retention for hourly tier"),
    keep_daily: int = typer.Option(None, "--keep-daily", help="Override retention for daily tier"),
    keep_manual: int = typer.Option(None, "--keep-manual", help="Override retention for manual tier"),
):
    """Prune old snapshots per the retention policy.

    Defaults come from ``snapshots.keep_{hourly,daily,manual}`` in the
    instance config, falling back to 72/30/50 if unset. Override per-call
    with the flags. Returns counts so scripting can act on what was pruned.
    """
    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)
    removed = prune_snapshots(
        db_path,
        keep_hourly=keep_hourly,
        keep_daily=keep_daily,
        keep_manual=keep_manual,
    )
    total = sum(removed.values())
    for tier, n in removed.items():
        print(f"{tier}: pruned {n}")
    print(f"total pruned: {total}")


@app.command("snapshot-restore")
def snapshot_restore(
    snapshot_path: str = typer.Argument(..., help="Path to snapshot db file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show action without restoring"),
):
    """Restore snapshot over current db (backs up current db first)."""
    settings = get_settings()
    db_path = resolve_sqlite_path(settings.database_url)

    if not dry_run:
        confirmed = typer.confirm(
            f"Restore snapshot {snapshot_path} into {db_path}? This will replace current DB.",
            default=False,
        )
        if not confirmed:
            print("Cancelled.")
            raise typer.Exit(0)

    try:
        backup_path = restore_snapshot(db_path, Path(snapshot_path), dry_run=dry_run)
    except ValueError as exc:
        print(f"Error: {exc}")
        raise typer.Exit(1) from exc
    print(f"pre_restore_backup={backup_path}")
    print(f"restored_to={db_path}")


@app.command("token-create")
def token_create():
    """Create an API token for the browser extension (works on PIN-protected instances)."""
    from app.core.auth import add_api_token

    token = add_api_token()
    print("API token created. Paste it into the YouOS extension Options — it is not shown again:")
    print()
    print(f"  {token}")
    print()
    print("Stored hashed on disk. Revoke all tokens with `youos token-revoke`.")


@app.command("token-list")
def token_list():
    """Show how many API tokens are configured for this instance."""
    from app.core.auth import load_api_token_hashes

    count = len(load_api_token_hashes())
    print(f"{count} API token(s) configured.")


@app.command("token-revoke")
def token_revoke():
    """Revoke all API tokens for this instance."""
    from app.core.auth import revoke_api_tokens

    count = revoke_api_tokens()
    print(f"Revoked {count} API token(s).")


if __name__ == "__main__":
    app()
