"""
Tencent Docs Markdown Skill - Main Entry

This is the main entry point that provides natural language command processing
for Tencent Docs Markdown operations.
"""

import json
import os
import re
import sys
from pathlib import Path

import click

from .auth import ensure_login, force_re_login, clear_cookies
from .api import (
    create_document,
    delete_document,
    read_document,
    write_document,
    get_document_info,
    rename_document,
    parse_pad_id_from_url,
    resolve_real_pad_id,
    DEFAULT_DOMAIN_ID,
)


# ── Destructive-operation confirmation gate ──────────────────────────
#
# The following helpers enforce an explicit, human-readable confirmation
# before any mutation that could overwrite, rename, or trash a document
# on the user's Tencent Docs account. This addresses the "Tool Misuse
# and Exploitation" risk where the agent might be tricked (via a
# malicious URL or instruction) into destroying the wrong document.
#
# Every destructive handler:
#   1. Resolves the target document and displays its title + URL.
#   2. Refuses to proceed unless the caller has explicitly opted in
#      via confirm=True (programmatic) or interactive y/N prompt (CLI).

def _prompt_confirmation(action: str, details: dict) -> bool:
    """
    Ask the user to confirm a destructive action on an interactive TTY.

    Non-interactive callers (e.g. automated agents) MUST pass
    confirm=True explicitly — they never reach this prompt.
    Returns True only if the user types 'y' or 'yes' (case-insensitive).
    """
    print("\n\u26a0\ufe0f  Confirmation required for destructive action:")
    print(f"   Action: {action}")
    for k, v in details.items():
        print(f"   {k}: {v}")
    if not sys.stdin.isatty():
        # No human is present — refuse rather than auto-confirm.
        print("   ❌  Non-interactive session and confirm=False → aborting.")
        return False
    try:
        answer = input("   Proceed? [y/N]: ").strip().lower()
    except EOFError:
        return False
    return answer in ('y', 'yes')


def handle_create(title: str, content: str | None = None) -> dict:
    """
    Create a new Markdown document.

    Args:
        title: Document title
        content: Optional initial content
    """
    print('📝 Creating Markdown document...')
    try:
        cookies = ensure_login()
        result = create_document(cookies, title)
        print(f"✅ Document created: {result['title']}")
        print(f"  📄 URL: {result['docUrl']}")
        print(f"  🆔 Pad ID: {result['padId']}")

        # If content is provided, write it to the document
        if content:
            print('   Writing content...')
            write_document(cookies, result['globalPadId'], content)
            print('✅ Content written successfully.')

        return result
    except Exception as err:
        print(f"❌ Create failed: {err}")
        raise


def handle_create_and_write(title: str, content: str) -> dict:
    """
    Create a new Tencent Docs Markdown document and write content to it.

    Args:
        title: Document title
        content: Markdown content to write

    Returns:
        dict with keys: docUrl, padId, globalPadId, title
    """
    print('📝 Creating Markdown document on Tencent Docs...')
    try:
        if not title:
            raise ValueError('Document title is required')
        if not content:
            raise ValueError('Markdown content is required')

        cookies = ensure_login()

        # Step 1: Create a new Markdown document
        print('   Creating document...')
        result = create_document(cookies, title)

        # Step 2: Write Markdown content to the document
        print('   Writing Markdown content...')
        write_document(cookies, result['globalPadId'], content)

        print(f"✅ Document created and content written: {title}")
        print(f"  📄 URL: {result['docUrl']}")
        print(f"  🆔 Pad ID: {result['padId']}")

        return result
    except Exception as err:
        print(f"❌ Create and write failed: {err}")
        raise


def handle_download(doc_url: str, output_path: str | None = None) -> dict:
    """
    Download a Tencent Docs Markdown document to local file.

    Args:
        doc_url: Tencent Docs URL
        output_path: Optional output file path

    Privacy note:
        The downloaded content is written to the local filesystem and
        returned to the caller. Only run this on documents you are
        comfortable exposing to the current agent/session.
    """
    print('📥 Downloading Markdown document...')
    print('   ℹ\ufe0f  Privacy notice: document contents will be written to disk and')
    print('       returned to the caller. Avoid using this on highly sensitive docs.')
    try:
        cookies = ensure_login()

        # Resolve the real padId from the document page
        print('   Resolving document ID...')
        doc_meta = resolve_real_pad_id(cookies, doc_url)
        global_pad_id = doc_meta['globalPadId']
        doc_title = doc_meta.get('title', '')
        pad_id = doc_meta['padId']

        print(f"   📄 Target: \"{doc_title or '(untitled)'}\"  ←  {doc_url}")

        # Read content
        print('   Reading document content...')
        content = read_document(cookies, global_pad_id)

        # Determine output path
        save_path = output_path
        if not save_path:
            name = doc_title or pad_id
            save_path = re.sub(r'[/\\?%*:|"<>]', '_', name) + '.md'

        # Ensure .md extension
        if not save_path.endswith('.md'):
            save_path += '.md'

        resolved_path = str(Path(save_path).resolve())
        with open(resolved_path, 'w', encoding='utf-8') as f:
            f.write(content)

        size = len(content.encode('utf-8'))
        print(f"✅ Downloaded to: {resolved_path}")
        print(f"  📦 Size: {size} bytes")

        return {'path': resolved_path, 'content': content}
    except Exception as err:
        print(f"❌ Download failed: {err}")
        raise


def handle_delete(doc_url: str, confirm: bool = False) -> dict:
    """
    Delete a Tencent Docs Markdown document (move to trash).

    Args:
        doc_url: Tencent Docs URL
        confirm: MUST be True for programmatic callers. If False and the
                 session is interactive, the user will be prompted to
                 confirm. Otherwise the operation is refused.

    Safety:
        Displays the resolved title + URL before performing the delete
        so the user can verify the correct document is being trashed.
    """
    print('🗑\ufe0f  Deleting Markdown document...')
    try:
        cookies = ensure_login()

        # Resolve the real padId from the document page
        print('   Resolving document ID...')
        doc_meta = resolve_real_pad_id(cookies, doc_url)
        pad_id = doc_meta['padId']
        doc_title = doc_meta.get('title', '') or '(untitled)'

        if not pad_id:
            raise RuntimeError(f'Cannot resolve real pad ID from URL: {doc_url}')

        # Safety gate: require explicit confirmation before trashing.
        if not confirm:
            ok = _prompt_confirmation(
                action='DELETE (move to trash)',
                details={'Title': doc_title, 'URL': doc_url, 'Pad ID': pad_id},
            )
            if not ok:
                print('❌ Delete aborted by user / non-interactive caller.')
                return {'padId': pad_id, 'deleted': False, 'aborted': True}

        delete_document(cookies, pad_id)

        print(f"✅ Document deleted (moved to trash): \"{doc_title}\"  [{pad_id}]")
        return {'padId': pad_id, 'title': doc_title, 'deleted': True}
    except Exception as err:
        print(f"❌ Delete failed: {err}")
        raise

def handle_read(doc_url: str) -> str:
    """
    Read and display document content.

    Args:
        doc_url: Tencent Docs URL

    Privacy note:
        The returned content may flow into agent conversation logs,
        terminal output, or downstream tool calls. Avoid using this
        on highly sensitive documents.
    """
    print('📖 Reading Markdown document...')
    print('   ℹ\ufe0f  Privacy notice: document content will be exposed to the caller /')
    print('       agent session. Avoid using this on highly sensitive docs.')
    try:
        cookies = ensure_login()

        # Resolve the real padId from the document page
        print('   Resolving document ID...')
        doc_meta = resolve_real_pad_id(cookies, doc_url)
        global_pad_id = doc_meta['globalPadId']
        doc_title = doc_meta.get('title', '') or '(untitled)'

        print(f"   📄 Target: \"{doc_title}\"  ←  {doc_url}")

        content = read_document(cookies, global_pad_id)

        print('✅ Document content retrieved.')
        print('─' * 60)
        print(content)
        print('─' * 60)

        return content
    except Exception as err:
        print(f"❌ Read failed: {err}")
        raise


def handle_update(doc_url: str, content_or_path: str, confirm: bool = False) -> dict:
    """
    Update (OVERWRITE) document content from a local file or text.

    Args:
        doc_url: Tencent Docs URL
        content_or_path: Markdown content or path to .md file
        confirm: MUST be True for programmatic callers. If False and the
                 session is interactive, the user will be prompted to
                 confirm. Otherwise the operation is refused.

    Safety:
        This is a DESTRUCTIVE operation — the existing content is
        replaced entirely. Displays resolved title + URL + a preview of
        the new content so the user can verify the target.
    """
    print('📝 Updating Markdown document...')
    try:
        cookies = ensure_login()

        # Resolve the real padId from the document page
        print('   Resolving document ID...')
        doc_meta = resolve_real_pad_id(cookies, doc_url)
        global_pad_id = doc_meta['globalPadId']
        pad_id = doc_meta['padId']
        doc_title = doc_meta.get('title', '') or '(untitled)'

        # Determine if content_or_path is a file path or direct content
        content = content_or_path
        source_hint = 'inline text'
        resolved_path = str(Path(content_or_path).resolve())
        if os.path.exists(resolved_path) and resolved_path.endswith('.md'):
            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read()
            source_hint = f'file: {resolved_path}'
            print(f"   Updating from file: {resolved_path}")

        # Safety gate: require explicit confirmation before overwriting.
        if not confirm:
            preview = (content[:120] + '…') if len(content) > 120 else content
            preview = preview.replace('\n', ' ↵ ')
            ok = _prompt_confirmation(
                action='UPDATE (overwrite existing content)',
                details={
                    'Title': doc_title,
                    'URL': doc_url,
                    'Pad ID': pad_id,
                    'New content source': source_hint,
                    'New content size': f'{len(content)} chars',
                    'Preview': preview,
                },
            )
            if not ok:
                print('❌ Update aborted by user / non-interactive caller.')
                return {'padId': pad_id, 'updated': False, 'aborted': True}

        write_document(cookies, global_pad_id, content)

        print(f"✅ Document updated successfully: \"{doc_title}\"  [{pad_id}]")
        return {'padId': pad_id, 'title': doc_title, 'updated': True}
    except Exception as err:
        print(f"❌ Update failed: {err}")
        raise


def handle_rename(doc_url: str, new_title: str, confirm: bool = False) -> dict:
    """
    Rename a document.

    Args:
        doc_url: Tencent Docs URL
        new_title: New title
        confirm: MUST be True for programmatic callers. If False and the
                 session is interactive, the user will be prompted to
                 confirm. Otherwise the operation is refused.

    Safety:
        Displays both the old title and the proposed new title before
        performing the rename, so the user can verify the target.
    """
    print('✏\ufe0f  Renaming document...')
    try:
        if not new_title or not new_title.strip():
            raise ValueError('New title must be a non-empty string')

        cookies = ensure_login()

        # Resolve the real padId from the document page
        print('   Resolving document ID...')
        doc_meta = resolve_real_pad_id(cookies, doc_url)
        pad_id = doc_meta['padId']
        old_title = doc_meta.get('title', '') or '(untitled)'

        if not pad_id:
            raise RuntimeError(f'Cannot resolve real pad ID from URL: {doc_url}')

        # Safety gate: require explicit confirmation before renaming.
        if not confirm:
            ok = _prompt_confirmation(
                action='RENAME',
                details={
                    'Current title': old_title,
                    'New title': new_title,
                    'URL': doc_url,
                    'Pad ID': pad_id,
                },
            )
            if not ok:
                print('❌ Rename aborted by user / non-interactive caller.')
                return {'padId': pad_id, 'renamed': False, 'aborted': True}

        result = rename_document(cookies, pad_id, new_title)

        print(f"✅ Document renamed: \"{old_title}\" → \"{new_title}\"")
        return {'padId': pad_id, 'oldTitle': old_title, 'newTitle': new_title, 'raw': result}
    except Exception as err:
        print(f"❌ Rename failed: {err}")
        raise

def handle_info(doc_url: str) -> dict:
    """
    Get document information.

    Args:
        doc_url: Tencent Docs URL
    """
    print('ℹ️  Getting document info...')
    try:
        cookies = ensure_login()
        pad_id = parse_pad_id_from_url(doc_url)

        if not pad_id:
            raise RuntimeError(f'Cannot parse document ID from URL: {doc_url}')

        info = get_document_info(cookies, pad_id)
        print('✅ Document info retrieved.')
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return info
    except Exception as err:
        print(f"❌ Info failed: {err}")
        raise


def handle_login(force: bool = False) -> None:
    """Login / re-login."""
    if force:
        force_re_login()
    else:
        ensure_login()


# ── CLI Entry ────────────────────────────────────────

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Tencent Docs Markdown CLI Tool"""
    pass


@cli.command()
@click.option('--force', is_flag=True, help='Force re-login (clear existing cookies)')
def login(force):
    """Login via QR code scanning."""
    handle_login(force)


@cli.command()
def logout():
    """Clear the locally stored session cookies.

    Removes the `.cookies.json` credential file so the session can no
    longer be used. Run this when you're done using the skill or before
    handing the machine to another user.
    """
    clear_cookies()


@cli.command()
@click.argument('title')
@click.option('-c', '--content', default=None, help='Initial Markdown content')
def create(title, content):
    """Create a new Markdown document."""
    handle_create(title, content)


@cli.command()
@click.argument('title')
@click.argument('content')
def write(title, content):
    """Create a new Tencent Docs Markdown and write content to it."""
    handle_create_and_write(title, content)


@cli.command()
@click.argument('url')
@click.option('-o', '--output', default=None, help='Output file path')
def download(url, output):
    """Download a Tencent Docs Markdown document to local."""
    handle_download(url, output)


@cli.command()
@click.argument('url')
@click.option('--yes', '-y', 'yes', is_flag=True, default=False,
              help='Skip the interactive confirmation prompt (dangerous).')
def delete(url, yes):
    """Delete a Tencent Docs Markdown document (move to trash)."""
    handle_delete(url, confirm=yes)


@cli.command()
@click.argument('url')
def read(url):
    """Read and display document content."""
    handle_read(url)


@cli.command()
@click.argument('url')
@click.argument('content')
@click.option('--yes', '-y', 'yes', is_flag=True, default=False,
              help='Skip the interactive confirmation prompt (dangerous).')
def update(url, content, yes):
    """Update document content (text or .md file path)."""
    handle_update(url, content, confirm=yes)


@cli.command()
@click.argument('url')
@click.argument('title')
@click.option('--yes', '-y', 'yes', is_flag=True, default=False,
              help='Skip the interactive confirmation prompt (dangerous).')
def rename(url, title, yes):
    """Rename a document."""
    handle_rename(url, title, confirm=yes)


@cli.command()
@click.argument('url')
def info(url):
    """Get document information."""
    handle_info(url)


if __name__ == '__main__':
    cli()
