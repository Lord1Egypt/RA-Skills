#!/usr/bin/env python3
"""
SolScribe Skill — Book writing companion for OpenClaw.
Call: python3 skill.py <command> [args]
"""

import json
import sys
from pathlib import Path

# Add parent to path for import
sys.path.insert(0, str(Path(__file__).parent))

from solscribe import (
    create_chapter, get_chapter, get_chapters, update_chapter, revise_chapter,
    delete_chapter, append_to_chapter, parse_incoming, set_book_meta,
    export_docx, total_words, load_state, count_words, log_session
)


def handle(text, chapter_hint=None):
    """
    Handle incoming text from Amre.
    Returns (response_text, should_save_to_inbox).
    """
    text = text.strip()
    if not text:
        return ("What would you like to add to the book?", False)

    state = load_state()
    chapters = get_chapters()
    total = total_words()

    # ── Commands ──────────────────────────────────────────────────────────────

    # List chapters
    if text.lower() in ("chapters", "list chapters", "show chapters", "show chapters?"):
        if not chapters:
            return ("No chapters yet. Send me some text and I'll create the first chapter.", False)
        lines = []
        for ch in chapters:
            icon = {"planned": "○", "drafted": "◐", "complete": "●"}.get(ch["status"], "○")
            lines.append(f"  {icon}  {ch['title']} — {ch['word_count']} words")
        lines.append(f"\nTotal: {len(chapters)} chapters, {total} words")
        return ("\n".join(lines), False)

    # Word count
    if text.lower() in ("word count", "words", "total words", "how many words"):
        if not chapters:
            return ("No chapters yet — nothing to count.", False)
        return (f"Total: {total} words across {len(chapters)} chapters.", False)

    # Read chapter
    read_match = text.lower()
    if read_match.startswith("read chapter"):
        import re
        m = re.search(r"chapter\s*(\d+)", text.lower())
        if m:
            num = int(m.group(1))
            for ch in chapters:
                if ch["order"] == num:
                    full = get_chapter(ch["id"])
                    content = full.get("content", "") or "(empty)"
                    wc = full["word_count"]
                    return (
                        f"**{full['title']}** ({wc} words)\n\n{content}",
                        False
                    )
            return (f"There's no Chapter {num} yet.", False)

    # Rename chapter
    import re
    rename_m = re.match(r"rename\s+chapter\s*(\d+)[:\s]+(.+)", text, re.IGNORECASE)
    if rename_m:
        num = int(rename_m.group(1))
        new_title = rename_m.group(2).strip()
        for ch in chapters:
            if ch["order"] == num:
                update_chapter(ch["id"], title=new_title)
                return (f"Renamed Chapter {num} to '{new_title}'.", False)
        return (f"There's no Chapter {num} to rename.", False)

    # Revise chapter — "revise chapter N: [new content]"
    revise_m = re.match(r"revise\s+chapter\s*(\d+)[:\s]+(.+)", text, re.IGNORECASE)
    if revise_m:
        num = int(revise_m.group(1))
        new_content = revise_m.group(2).strip()
        for ch in chapters:
            if ch["order"] == num:
                # Preserve existing content and append new revision
                full = get_chapter(ch["id"])
                # For a full rewrite, new_content is the replacement
                revise_chapter(ch["id"], content=new_content)
                new_wc = len(new_content.split())
                return (f"Revised Chapter {num} ('{ch['title']}'). New content: {new_wc} words.", False)
        return (f"There's no Chapter {num} to revise.", False)

    # Delete chapter
    del_m = re.match(r"delete\s+chapter\s*(\d+)", text, re.IGNORECASE)
    if del_m:
        num = int(del_m.group(1))
        for ch in chapters:
            if ch["order"] == num:
                return (
                    f"Delete '{ch['title']}'? Say 'yes, delete chapter {num}' to confirm.",
                    False
                )
        return (f"There's no Chapter {num} to delete.", False)

    # Confirm delete
    confirm_m = re.match(r"yes,?\s*delete\s*chapter\s*(\d+)", text, re.IGNORECASE)
    if confirm_m:
        num = int(confirm_m.group(1))
        for ch in chapters:
            if ch["order"] == num:
                title = ch["title"]
                delete_chapter(ch["id"])
                return (f"Deleted '{title}'.", False)
        return (f"There's no Chapter {num}.", False)

    # Status change
    status_m = re.match(r"status\s+chapter\s*(\d+)[:\s]+(.+)", text, re.IGNORECASE)
    if status_m:
        num = int(status_m.group(1))
        new_status = status_m.group(2).strip().lower()
        if new_status not in ("planned", "drafted", "complete"):
            return ("Status must be: planned, drafted, or complete.", False)
        for ch in chapters:
            if ch["order"] == num:
                update_chapter(ch["id"], status=new_status)
                icon = {"planned": "○", "drafted": "◐", "complete": "●"}.get(new_status, "○")
                return (f"Chapter {num} marked as {icon} {new_status}.", False)
        return (f"There's no Chapter {num}.", False)

    # Book title
    title_m = re.match(r"book\s*title[:\s]+(.+)", text, re.IGNORECASE)
    if title_m:
        new_title = title_m.group(1).strip()
        set_book_meta(book_title=new_title)
        return (f"Book title set to '{new_title}'.", False)

    # Author
    author_m = re.match(r"author[:\s]+(.+)", text, re.IGNORECASE)
    if author_m:
        new_author = author_m.group(1).strip()
        set_book_meta(author=new_author)
        return (f"Author set to '{new_author}'.", False)

    # Export DOCX
    if text.lower() in ("export docx", "export", "export docx!", "export!"):
        state = load_state()
        if not state["chapters"]:
            return ("Nothing to export yet — no chapters.", False)
        safe_title = re.sub(r'[^\w\s-]', '', state["book_title"]).strip()
        output_path = Path.home() / "Documents" / f"{safe_title}.docx"
        try:
            export_docx(str(output_path))
            return (f"Book exported to:\n{output_path}", False)
        except Exception as e:
            return (f"Export failed: {e}", False)

    # Export to specific path
    export_m = re.match(r"export\s+docx[:\s]+(.+)", text, re.IGNORECASE)
    if export_m:
        output_path = Path(export_m.group(1).strip()).expanduser()
        try:
            export_docx(str(output_path))
            return (f"Book exported to:\n{output_path}", False)
        except Exception as e:
            return (f"Export failed: {e}", False)

    # ── Content parsing ───────────────────────────────────────────────────────

    action, chapter_id, content = parse_incoming(text, chapter_hint)

    if action == "empty":
        return ("What would you like to add to the book?", False)

    if action == "create":
        ch = create_chapter(chapter_id)  # chapter_id is the title here
        return (
            f"Created **{ch['title']}**. It's ready for you to write in.",
            False
        )

    if action == "append":
        ch = get_chapter(chapter_id)
        append_to_chapter(chapter_id, content)
        new_wc = count_words(chapter_id)
        return (
            f"Added to **{ch['title']}**. It's now {new_wc} words.",
            False
        )

    if action == "ask":
        # Multiple chapters — need to know which one
        options = "\n".join(f"  Chapter {ch['order']}: {ch['title']}" for ch in chapters)
        return (
            f"Which chapter?\n\n{options}\n\nOr say 'new chapter: Title' to create one.",
            False
        )

    return ("I'm not sure what to do with that. Try 'chapters' to see what exists, or 'new chapter: Title' to create one.", False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("SolScribe — Book Writing Companion")
        print("Usage: python3 skill.py <command>")
        print("\nCommands: chapters, word count, export docx, [any text to add]")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    response, _ = handle(text)
    log_session(text, response)
    print(response)
