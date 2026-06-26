"""SSML and text processing helpers for TTS."""
import re
import uuid
from xml.sax.saxutils import escape


def mark_english_terms(text):
    """Wrap English terms in SSML lang tags, preserving existing XML tags."""
    tags = []
    tag_pattern = r'<[^>]+>'
    placeholder_prefix = f"__XMLTAG_{uuid.uuid4().hex[:8]}_"

    def save_tag(m):
        tags.append(m.group(0))
        return f'{placeholder_prefix}{len(tags)-1}__'

    text_with_placeholders = re.sub(tag_pattern, save_tag, text)
    result = escape(text_with_placeholders)

    multi_word_phrases = [
        "Claude Code", "Final Cut Pro", "Visual Studio Code", "VS Code",
        "Google Chrome", "Open AI", "OpenAI", "GPT 4", "GPT-4"
    ]
    for phrase in multi_word_phrases:
        escaped = escape(phrase)
        if escaped in result:
            result = result.replace(escaped, f'<lang xml:lang="en-US">{escaped}</lang>')

    pattern = r'\b[A-Za-z][A-Za-z0-9\-\.]*[A-Za-z0-9]\b|\b[A-Za-z]{2,}\b'
    matches = list(re.finditer(pattern, result))

    for match in reversed(matches):
        word = match.group(0)
        start, end = match.start(), match.end()
        before = result[:start]
        last_open = before.rfind('<')
        last_close = before.rfind('>')
        if last_open > last_close:
            continue
        open_tags = before.count('<lang xml:lang="en-US">')
        close_tags = before.count('</lang>')
        if open_tags > close_tags:
            continue
        if word.isdigit() or len(word) == 1:
            continue
        result = result[:start] + f'<lang xml:lang="en-US">{word}</lang>' + result[end:]

    for i, tag in enumerate(tags):
        result = result.replace(f'{placeholder_prefix}{i}__', tag)

    return result
