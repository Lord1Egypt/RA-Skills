#!/usr/bin/env python3
"""
SoulForge CLI - AI Agent Memory Evolution System

Usage:
    python3 soulforge.py run [--workspace PATH] [--dry-run]
    python3 soulforge.py status [--workspace PATH]
    python3 soulforge.py restore FILE [--backup PATH]
    python3 soulforge.py cron [--every MINUTES]

Examples:
    python3 soulforge.py run
    python3 soulforge.py run --dry-run
    python3 soulforge.py status
    python3 soulforge.py restore SOUL.md --backup .soulforge-backups/SOUL.md.20260405_120000.bak
"""

import argparse
import logging
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from soulforge import SoulForgeConfig, MemoryReader, PatternAnalyzer, SoulEvolver


def setup_logging(level: str = "INFO") -> None:
    """Configure logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def cmd_run(args) -> int:
    """Run the evolution process."""
    config = SoulForgeConfig(
        config_path=args.config,
        overrides={
            "dry_run": args.dry_run,
            "workspace": args.workspace,
        }
    )
    setup_logging(config.log_level)

    logger = logging.getLogger("soulforge.run")
    logger.info(f"SoulForge starting (workspace: {config.workspace})")

    # Check API key
    if not config.minimax_api_key:
        logger.error("MINIMAX_API_KEY not configured")
        print("ERROR: MINIMAX_API_KEY environment variable not set")
        print("  export MINIMAX_API_KEY=your-key")
        return 1

    # Step 1: Read memory sources
    print("📖 Reading memory sources...")
    reader = MemoryReader(config.workspace, config)
    entries = reader.read_all()

    if not entries:
        print("⚠️  No memory entries found. Nothing to analyze.")
        print("   Make sure you have:")
        print("   - memory/*.md daily files")
        print("   - .learnings/ directory")
        print("   - hawk-bridge vector store")
        return 0

    summary = reader.summarize()
    print(f"   ✓ Read {summary['total_entries']} entries from {len(summary['sources'])} sources")

    # Step 2: Read existing content of target files
    print("📄 Checking existing file content...")
    existing_content = {}
    for target in config.target_files:
        target_path = Path(config.workspace) / target
        if target_path.exists():
            existing_content[target] = target_path.read_text(encoding="utf-8")
            print(f"   ✓ {target} exists ({len(existing_content[target])} chars)")
        else:
            print(f"   - {target} does not exist yet (will create)")

    # Step 3: Analyze patterns
    print("🔍 Analyzing patterns with MiniMax...")
    analyzer = PatternAnalyzer(config)
    patterns = analyzer.analyze(entries, existing_content)

    if not patterns:
        print("   ⚠️  No significant patterns found.")
        return 0

    # Filter by threshold
    filtered = analyzer.filter_by_threshold(patterns)
    print(f"   ✓ Found {len(filtered)} patterns above threshold")

    # Step 4: Apply updates
    print("✏️  Applying updates...")
    evolver = SoulEvolver(config.workspace, config)
    results = evolver.apply_updates(filtered)

    if results["dry_run"]:
        print(f"   ⚠️  DRY RUN - no files were written")
        print("")
        print("   Would update:")
        for filename in results["files_updated"]:
            print(f"     - {filename}")
    else:
        print(f"   ✓ Updated {len(results['files_updated'])} files")
        print(f"   ✓ Applied {results['patterns_applied']} patterns")

    if results["errors"]:
        print(f"   ⚠️  Errors encountered:")
        for err in results["errors"]:
            for file, error in err.items():
                print(f"     - {file}: {error}")

    # Print summary
    if results.get("changes"):
        print("")
        print(evolver.summarize_changes())

    print("")
    if results["dry_run"]:
        print("🔍 DRY RUN complete. Run without --dry-run to write changes.")
    else:
        print("✅ SoulForge evolution complete!")

    return 0


def cmd_status(args) -> int:
    """Show current status."""
    config = SoulForgeConfig(overrides={"workspace": args.workspace})
    setup_logging(config.log_level)

    logger = logging.getLogger("soulforge.status")
    print(f"SoulForge Status (workspace: {config.workspace})")
    print("=" * 50)

    # Read memory
    reader = MemoryReader(config.workspace, config)
    entries = reader.read_all()
    summary = reader.summarize()

    print(f"\n📊 Memory Overview:")
    print(f"   Total entries: {summary['total_entries']}")
    print(f"   Sources: {len(summary['sources'])}")

    print(f"\n   By source type:")
    for source_type, count in summary.get("by_source_type", {}).items():
        print(f"     - {source_type}: {count}")

    print(f"\n   By category:")
    for category, count in summary.get("by_category", {}).items():
        print(f"     - {category}: {count}")

    # Check target files
    print(f"\n📝 Target Files:")
    for target in config.target_files:
        target_path = Path(config.workspace) / target
        if target_path.exists():
            stat = target_path.stat()
            size = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            print(f"   ✓ {target} ({size} bytes, modified {modified})")
        else:
            print(f"   - {target} (not created)")

    # Check backups
    backup_dir = Path(config.backup_dir)
    if backup_dir.exists():
        backups = list(backup_dir.glob("*.bak"))
        print(f"\n💾 Backups: {len(backups)} files in {backup_dir}")

    return 0


def cmd_restore(args) -> int:
    """Restore a file from backup."""
    config = SoulForgeConfig(overrides={"workspace": args.workspace})
    setup_logging(config.log_level)

    logger = logging.getLogger("soulforge.restore")

    evolver = SoulEvolver(config.workspace, config)

    # List available backups if no specific one given
    if not args.backup:
        print(f"Available backups for {args.file}:")
        backups = evolver.get_backup_list(args.file)
        if not backups:
            print("   No backups found")
            return 1
        for b in backups:
            print(f"   - {b['path']} ({b['timestamp']})")
        print("")
        print("Use: soulforge.py restore FILE --backup PATH")
        return 0

    # Restore
    success = evolver.restore_from_backup(args.file, args.backup)
    if success:
        print(f"✅ Restored {args.file} from {args.backup}")
        return 0
    else:
        print(f"❌ Restore failed")
        return 1


def cmd_cron(args) -> int:
    """Set up cron schedule."""
    if args.every:
        print(f"To schedule SoulForge every {args.every} minutes, add this to your crontab:")
        print("")
        print(f"*/{args.every} * * * * cd {os.getcwd()} && python3 {__file__} run >> /var/log/soulforge.log 2>&1")
        print("")
        print("Or with OpenClaw cron:")
        print(f"  openclaw cron add --name soulforge-evolve --every {args.every}m \\")
        print(f"    --message 'exec python3 {__file__} run'")
    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SoulForge - AI Agent Memory Evolution System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--workspace",
        default=os.environ.get("SOULFORGE_WORKSPACE", "~/.openclaw/workspace"),
        help="Workspace directory (default: ~/.openclaw/workspace)"
    )
    parser.add_argument(
        "--config",
        help="Path to config.json"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )

    # Parse known args first to get workspace
    known, _ = parser.parse_known_args()
    workspace = os.path.expanduser(known.workspace or "~/.openclaw/workspace")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # run command
    run_parser = subparsers.add_parser("run", help="Run evolution process")
    run_parser.add_argument("--dry-run", action="store_true", help="Preview only")
    run_parser.set_defaults(func=cmd_run, workspace=workspace)

    # status command
    status_parser = subparsers.add_parser("status", help="Show current status")
    status_parser.set_defaults(func=cmd_status, workspace=workspace)

    # restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument("file", help="File to restore (e.g., SOUL.md)")
    restore_parser.add_argument("--backup", help="Specific backup path to restore from")
    restore_parser.set_defaults(func=cmd_restore, workspace=workspace)

    # cron command
    cron_parser = subparsers.add_parser("cron", help="Cron setup help")
    cron_parser.add_argument("--every", type=int, metavar="MINUTES", help="Run every N minutes")
    cron_parser.set_defaults(func=cmd_cron, workspace=workspace)

    args = parser.parse_args()

    if not args.command:
        # Default to run
        args.func = cmd_run
    else:
        args.func = args.func

    return args.func(args)


if __name__ == "__main__":
    from datetime import datetime
    sys.exit(main())
