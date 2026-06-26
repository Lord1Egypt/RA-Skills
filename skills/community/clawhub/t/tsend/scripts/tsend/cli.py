"""CLI interface for tsend with profile support"""

import asyncio
import sys
import typer
from pathlib import Path
from typing import Optional, List

from tsend.config import Config
from tsend.client import TelegramClient, TelegramError
from tsend.utils import get_file_type, format_bytes

# Fix Windows console encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, errors="replace")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, errors="replace")

app = typer.Typer(help="Send files via Telegram Bot")
config_app = typer.Typer(name="config", help="Manage tsend configuration")
app.add_typer(config_app, name="config")


def get_config(profile: Optional[str] = None) -> Config:
    """Helper to get config with optional profile override"""
    return Config(profile=profile)


@app.command()
def send(
    file_paths: List[Path] = typer.Argument(..., help="Path(s) to the file(s) to send", exists=True),
    caption: Optional[str] = typer.Option(None, "--caption", "-c", help="File caption (sent with first file, max 1024 chars)"),
    token: Optional[str] = typer.Option(None, "--token", "-t", help="Override bot token"),
    chat_id: Optional[str] = typer.Option(None, "--chat-id", help="Override chat ID"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p", help="Use specific profile"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without sending"),
):
    """Send file(s) to Telegram"""
    config = get_config(profile)

    # Override config with CLI options (highest priority)
    token = token or config.token
    chat_id = chat_id or config.chat_id

    # Validate
    valid, error = config.validate()
    if not valid:
        typer.echo(f"❌ {error}", err=True)
        raise typer.Exit(1)

    # Validate all files exist
    missing_files = [f for f in file_paths if not f.exists()]
    if missing_files:
        for f in missing_files:
            typer.echo(f"❌ File not found: {f}", err=True)
        raise typer.Exit(1)

    total_size = sum(f.stat().st_size for f in file_paths)

    # Display preview
    typer.echo(f"📄 Files ({len(file_paths)}):")
    for i, fp in enumerate(file_paths, 1):
        typer.echo(f"   {i}. {fp.name} ({format_bytes(fp.stat().st_size)})")
    typer.echo(f"📊 Total size: {format_bytes(total_size)}")
    if caption:
        typer.echo(f"💬 Caption: {caption[:100]}{'...' if len(caption) > 100 else ''}")
    if config.active_profile_name:
        typer.echo(f"🔧 Profile: {config.active_profile_name}")
    typer.echo()

    if dry_run:
        typer.echo("🔍 Dry run mode - not sending")
        raise typer.Exit()

    # Send files
    client = TelegramClient(token, chat_id)

    async def send_files() -> None:
        success_count = 0
        errors = []

        for i, file_path in enumerate(file_paths, 1):
            file_size = file_path.stat().st_size
            file_type = get_file_type(file_path)
            # Only first file gets caption
            file_caption = caption if i == 1 else None

            typer.echo(f"📤 [{i}/{len(file_paths)}] Sending {file_path.name}...")

            try:
                if file_type == "photo":
                    result = await client.send_photo(file_path, file_caption)
                else:
                    result = await client.send_document(file_path, file_caption)

                if result.get("ok"):
                    typer.echo(f"   ✅ Sent")
                    success_count += 1
                else:
                    error_msg = result.get('description', 'Unknown error')
                    typer.echo(f"   ❌ Failed: {error_msg}", err=True)
                    errors.append(f"{file_path.name}: {error_msg}")
            except TelegramError as e:
                typer.echo(f"   ❌ Error: {e}", err=True)
                errors.append(f"{file_path.name}: {e}")

        # Summary
        typer.echo()
        if success_count == len(file_paths):
            typer.echo(f"✅ All {success_count} file(s) sent successfully!")
        elif success_count > 0:
            typer.echo(f"⚠️  {success_count}/{len(file_paths)} files sent successfully")
            typer.echo(f"❌ {len(errors)} failed:")
            for err in errors:
                typer.echo(f"   - {err}", err=True)
            raise typer.Exit(1)
        else:
            typer.echo(f"❌ All {len(file_paths)} files failed to send")
            raise typer.Exit(1)

        await client.close()

    asyncio.run(send_files())


@app.command()
def text(
    message: str = typer.Argument(..., help="Text message to send"),
    token: Optional[str] = typer.Option(None, "--token", "-t", help="Override bot token"),
    chat_id: Optional[str] = typer.Option(None, "--chat-id", help="Override chat ID"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p", help="Use specific profile"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without sending"),
):
    """Send a text message to Telegram"""
    config = get_config(profile)

    # Override config with CLI options (highest priority)
    token = token or config.token
    chat_id = chat_id or config.chat_id

    # Validate
    valid, error = config.validate()
    if not valid:
        typer.echo(f"❌ {error}", err=True)
        raise typer.Exit(1)

    # Display preview
    preview = message[:100] + "..." if len(message) > 100 else message
    typer.echo(f"💬 Message: {preview}")
    typer.echo(f"📏 Length: {len(message)} chars")
    if config.active_profile_name:
        typer.echo(f"🔧 Profile: {config.active_profile_name}")
    typer.echo()

    if dry_run:
        typer.echo("🔍 Dry run mode - not sending")
        raise typer.Exit()

    # Send message
    client = TelegramClient(token, chat_id)

    async def send_msg() -> None:
        try:
            typer.echo("📤 Sending...")
            result = await client.send_message(message)

            if result.get("ok"):
                typer.echo("✅ Message sent successfully!")
            else:
                typer.echo(f"❌ Failed: {result.get('description')}", err=True)
                raise typer.Exit(1)
        except TelegramError as e:
            typer.echo(f"❌ Error: {e}", err=True)
            raise typer.Exit(1)
        finally:
            await client.close()

    asyncio.run(send_msg())


@config_app.command()
def set(
    token: Optional[str] = typer.Option(None, "--token", "-t", help="Set bot token"),
    chat_id: Optional[str] = typer.Option(None, "--chat-id", help="Set chat ID"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p", help="Profile to update"),
):
    """Set configuration values"""
    cfg = get_config(profile)

    if profile:
        typer.echo(f"🔧 Profile: {profile}")
    elif cfg.active_profile_name:
        typer.echo(f"🔧 Profile: {cfg.active_profile_name}")
    else:
        typer.echo("🔧 Profile: (default)")

    # Set values
    if token:
        cfg.set("token", token)
        typer.echo("✅ Token updated")
    if chat_id:
        cfg.set("chat_id", chat_id)
        typer.echo("✅ Chat ID updated")

    # Save if any changes
    if token or chat_id:
        cfg.save()
    else:
        typer.echo("Use --token or --chat-id to set values")


@config_app.command("show")
def config_show(
    profile: Optional[str] = typer.Option(None, "--profile", "-p", help="Show specific profile"),
):
    """Show current configuration"""
    cfg = get_config(profile)

    typer.echo("📋 Current configuration:")
    if profile:
        typer.echo(f"  Profile: {profile}")
    elif cfg.active_profile_name:
        typer.echo(f"  Profile: {cfg.active_profile_name}")
    else:
        typer.echo(f"  Profile: (default)")
    typer.echo(f"  Token: {'*' * 10 if cfg.token else '(not set)'}")
    typer.echo(f"  Chat ID: {cfg.chat_id or '(not set)'}")


@config_app.command("list")
def config_list():
    """List all profiles"""
    cfg = Config()
    profiles = cfg.profiles
    default = cfg.default_profile

    if not profiles:
        typer.echo("No profiles configured. Use 'tsend config set --profile <name> ...' to create one.")
        raise typer.Exit()

    typer.echo("📋 Available profiles:")
    for p in profiles:
        marker = " (default)" if p == default else ""
        typer.echo(f"  - {p}{marker}")


@config_app.command("default")
def config_default(
    profile: str = typer.Argument(..., help="Profile to set as default"),
):
    """Set default profile"""
    cfg = Config()
    try:
        cfg.set_default_profile(profile)
        cfg.save()
        typer.echo(f"✅ Default profile set to: {profile}")
    except ValueError as e:
        typer.echo(f"❌ {e}", err=True)
        raise typer.Exit(1)


# Backward compatibility: keep old config command (disabled to avoid conflicts)
# @app.command()
# def config_old(
#     token: Optional[str] = typer.Option(None, "--token", "-t", help="Set bot token (deprecated, use 'tsend config set')"),
#     chat_id: Optional[str] = typer.Option(None, "--chat-id", help="Set chat ID (deprecated, use 'tsend config set')"),
#     show: bool = typer.Option(False, "--show", "-s", help="Show current configuration (deprecated, use 'tsend config show')"),
# ):
    """Manage tsend configuration (deprecated, use 'tsend config <subcommand>')"""
    if show:
        config_show()
    elif token or chat_id:
        set(token=token, chat_id=chat_id)
    else:
        typer.echo("⚠️  This command is deprecated. Use 'tsend config <subcommand>' instead:")
        typer.echo("  tsend config set --token TOKEN --profile NAME")
        typer.echo("  tsend config show --profile NAME")
        typer.echo("  tsend config list")
        typer.echo("  tsend config default PROFILE_NAME")
