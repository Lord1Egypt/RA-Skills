#!/usr/bin/env python3
"""
translate.py - Translate txt files using OpenAI-compatible API.

Usage:
    python3 translate.py <input_file> [options]

Environment Variables:
    TRANSLATE_API_KEY       - API key for the translation service (required)
    TRANSLATE_BASE_URL      - Base URL for OpenAI-compatible API (default: https://api.siliconflow.cn/v1)
    TRANSLATE_MODEL         - Model name (default: Qwen/Qwen2.5-7B-Instruct)
    TRANSLATE_TEMPERATURE   - Model temperature (default: 1)
    TRANSLATE_TIMEOUT       - API request timeout in seconds (default: 300)

Options:
    --output <path>         Output file path (default: <input>_translated.txt)
    --target-lang <lang>    Target language (default: Chinese)
    --source-lang <lang>    Source language hint (default: auto-detect)
    --chunk-size <int>      Max characters per chunk (default: 3000)
    --concurrency <int>     Max concurrent chunk translations (default: 3)
    --context-window <int>  Number of preceding chunks for sliding context (default: 3)
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_dotenv():
    """Load .env file from the skill's root directory (parent of scripts/)."""
    skill_root = Path(__file__).resolve().parent.parent
    env_path = skill_root / ".env"
    if not env_path.is_file():
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            if key and key not in os.environ:
                os.environ[key] = value


def call_chat_api(base_url: str, api_key: str, model: str, messages: list, max_retries: int = 3) -> str:
    """Call OpenAI-compatible chat completion API with retry on timeout."""
    url = f"{base_url.rstrip('/')}/chat/completions"

    payload_dict = {
        "model": model,
        "messages": messages,
        "temperature": float(os.environ.get("TRANSLATE_TEMPERATURE", "1")),
        "max_tokens": int(os.environ.get("TRANSLATE_MAX_TOKENS", "4096")),
    }

    thinking_mode = os.environ.get("TRANSLATE_THINKING", "auto")
    if thinking_mode in ("disabled", "auto"):
        payload_dict["enable_thinking"] = False

    payload = json.dumps(payload_dict).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    timeout = int(os.environ.get("TRANSLATE_TIMEOUT", "300"))
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return body["choices"][0]["message"]["content"]
        except (TimeoutError, urllib.error.URLError) as e:
            if attempt < max_retries:
                wait = attempt * 5
                print(f"RETRY:attempt {attempt}/{max_retries} failed ({e}), retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
                req = urllib.request.Request(
                    url, data=payload,
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                    method="POST",
                )
                continue
            print(f"API_ERROR:Failed after {max_retries} attempts - {e}", file=sys.stderr)
            return None
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            if attempt < max_retries and e.code in (429, 500, 502, 503):
                wait = attempt * 10
                print(f"RETRY:attempt {attempt}/{max_retries} got HTTP {e.code}, retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
                req = urllib.request.Request(
                    url, data=payload,
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                    method="POST",
                )
                continue
            print(f"API_ERROR:HTTP {e.code} - {error_body}", file=sys.stderr)
            return None
        except KeyError:
            print("API_ERROR:Unexpected response format", file=sys.stderr)
            return None


def split_into_chunks(text: str, chunk_size: int) -> list:
    """Split text into chunks, preferring paragraph boundaries."""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    remaining = text

    while remaining:
        if len(remaining) <= chunk_size:
            chunks.append(remaining)
            break

        split_pos = remaining.rfind("\n\n", 0, chunk_size)
        if split_pos == -1:
            split_pos = remaining.rfind("\n", 0, chunk_size)
        if split_pos == -1:
            for sep in ["。", ".", "！", "!", "？", "?"]:
                pos = remaining.rfind(sep, 0, chunk_size)
                if pos != -1:
                    split_pos = pos + len(sep)
                    break
        if split_pos == -1 or split_pos < chunk_size // 4:
            split_pos = chunk_size

        chunks.append(remaining[:split_pos])
        remaining = remaining[split_pos:].lstrip("\n")

    return chunks


def extract_keywords_from_chunk(chunk: str, base_url: str, api_key: str, model: str, target_lang: str, source_lang: str) -> str:
    """Extract proper nouns and key terms from a single chunk (lightweight prompt)."""
    source_hint = f" from {source_lang}" if source_lang != "auto" else ""
    system_msg = (
        f"List all proper nouns (names, places, organizations) and domain-specific terms"
        f"{source_hint} in the text below with their {target_lang} translation. "
        "Format: Original - Translation, one per line. Output ONLY the list, nothing else."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": chunk},
    ]

    return call_chat_api(base_url, api_key, model, messages, max_retries=2) or ""


def parse_glossary(text: str) -> dict:
    """Parse a glossary text into a dict of {original: translation}."""
    glossary = {}
    for line in text.strip().split("\n"):
        line = line.strip().strip("- ").strip()
        if not line or " - " not in line:
            continue
        parts = line.split(" - ", 1)
        original = parts[0].strip()
        translation = parts[1].strip() if len(parts) > 1 else ""
        if original and original not in glossary:
            glossary[original] = translation
    return glossary


def build_context_from_glossary(glossary: dict, background: str = "") -> str:
    """Build a context string from glossary dict and optional background."""
    parts = []
    if glossary:
        lines = []
        for orig, trans in glossary.items():
            lines.append(f"{orig} - {trans}" if trans else orig)
        parts.append("## GLOSSARY\n" + "\n".join(lines))
    if background:
        parts.append(f"## BACKGROUND\n{background}")
    return "\n\n".join(parts) if parts else ""


def infer_background(glossary: dict, base_url: str, api_key: str, model: str, target_lang: str) -> str:
    """Infer background context from a glossary."""
    if not glossary:
        return ""
    glossary_text = "\n".join(f"{k} - {v}" for k, v in glossary.items() if v)
    system_msg = (
        f"The following is a glossary from a text being translated into {target_lang}. "
        "Infer the text's genre, subject matter, setting (time/place), and writing style. "
        "Output ONLY a concise description (2-3 sentences), nothing else."
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": glossary_text},
    ]
    return call_chat_api(base_url, api_key, model, messages) or ""


def translate_text(
    text: str,
    base_url: str,
    api_key: str,
    model: str,
    target_lang: str,
    source_lang: str,
    concurrency: int = 3,
    context_window: int = 3,
) -> str:
    """Translate text using sliding-window incremental context.

    Strategy:
    - Step 1: Extract keywords from every chunk concurrently (lightweight pass)
    - Step 2: Build incremental context per chunk using a sliding window of
      preceding chunks' keywords. Context grows as new terms appear and
      naturally shifts as the window slides forward.
    - Step 3: Translate all chunks concurrently, each with its own
      window-scoped context.
    """
    chunks = split_into_chunks(text, 3000)

    if len(chunks) == 1:
        return translate_chunk(chunks[0], base_url, api_key, model, target_lang, source_lang)

    # Step 1: Extract keywords from every chunk concurrently
    print(f"INFO:Step 1 - Extracting keywords from {len(chunks)} chunks...", file=sys.stderr)
    keyword_results = [None] * len(chunks)

    def extract_task(index, chunk):
        print(f"KEYWORDS:chunk {index + 1}/{len(chunks)}", file=sys.stderr)
        result = extract_keywords_from_chunk(chunk, base_url, api_key, model, target_lang, source_lang)
        return index, result

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(extract_task, i, chunk): i
            for i, chunk in enumerate(chunks)
        }
        for future in as_completed(futures):
            index, result = future.result()
            keyword_results[index] = result
            print(f"KEYWORDS_DONE:chunk {index + 1}/{len(chunks)}", file=sys.stderr)

    # Step 2: Build per-chunk context using sliding window
    print(f"INFO:Step 2 - Building sliding-window context (window={context_window})...", file=sys.stderr)
    per_chunk_glossary = [parse_glossary(kw) for kw in keyword_results]

    # Build incremental glossary per chunk: union of terms from window chunks
    per_chunk_context = [""] * len(chunks)
    for i in range(len(chunks)):
        # Window: from max(0, i - context_window) to i (inclusive)
        start = max(0, i - context_window)
        merged = {}
        for j in range(start, i + 1):
            for orig, trans in per_chunk_glossary[j].items():
                if orig not in merged:
                    merged[orig] = trans
        per_chunk_context[i] = build_context_from_glossary(merged)

    # Infer background from the first window (gives initial context for the whole text)
    initial_glossary = {}
    for j in range(min(context_window + 1, len(chunks))):
        for orig, trans in per_chunk_glossary[j].items():
            if orig not in initial_glossary:
                initial_glossary[orig] = trans

    background = infer_background(initial_glossary, base_url, api_key, model, target_lang)
    if background:
        # Prepend background to every chunk's context
        for i in range(len(chunks)):
            if per_chunk_context[i]:
                per_chunk_context[i] = f"## BACKGROUND\n{background}\n\n{per_chunk_context[i]}"
            else:
                per_chunk_context[i] = f"## BACKGROUND\n{background}"

    # Step 3: Translate all chunks concurrently with per-chunk context
    print(f"INFO:Step 3 - Translating {len(chunks)} chunks...", file=sys.stderr)
    translated_parts = [None] * len(chunks)

    def translate_chunk_task(index, chunk, context):
        print(f"TRANSLATING:chunk {index + 1}/{len(chunks)}", file=sys.stderr)
        result = translate_chunk(chunk, base_url, api_key, model, target_lang, source_lang, context)
        if result is None:
            print(f"API_ERROR:chunk {index + 1} failed after retries", file=sys.stderr)
            sys.exit(1)
        print(f"DONE:chunk {index + 1}/{len(chunks)}", file=sys.stderr)
        return index, result

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(translate_chunk_task, i, chunk, per_chunk_context[i]): i
            for i, chunk in enumerate(chunks)
        }
        for future in as_completed(futures):
            index, result = future.result()
            translated_parts[index] = result

    return "\n\n".join(translated_parts)


def translate_chunk(
    chunk: str,
    base_url: str,
    api_key: str,
    model: str,
    target_lang: str,
    source_lang: str,
    context: str = "",
) -> str:
    """Translate a single chunk of text, with context for consistency."""
    source_hint = f" from {source_lang}" if source_lang != "auto" else ""
    system_msg = (
        f"You are a professional translator. Translate the following text"
        f"{source_hint} into {target_lang}. "
        "Output ONLY the translated text, preserving the original formatting and structure. "
        "Do not add any explanations, notes, or prefixes."
    )

    if context:
        system_msg += (
            f"\n\n--- Context ---\n{context}\n--- End Context ---\n\n"
            "Follow the glossary for consistent translation of proper nouns and terms. "
            "Apply the background knowledge to inform your translation choices."
        )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": chunk},
    ]

    return call_chat_api(base_url, api_key, model, messages)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Translate txt files using OpenAI-compatible API")
    parser.add_argument("input_file", help="Path to the input txt file")
    parser.add_argument("--output", help="Output file path (default: <input>_translated.txt)")
    parser.add_argument("--target-lang", default="Chinese", help="Target language (default: Chinese)")
    parser.add_argument("--source-lang", default="auto", help="Source language hint (default: auto-detect)")
    parser.add_argument("--chunk-size", type=int, default=3000, help="Max characters per chunk (default: 3000)")
    parser.add_argument("--concurrency", type=int, default=3, help="Max concurrent chunk translations (default: 3)")
    parser.add_argument("--context-window", type=int, default=3, help="Number of preceding chunks for sliding context (default: 3)")

    args = parser.parse_args()

    # Resolve API config from environment
    api_key = os.environ.get("TRANSLATE_API_KEY", "")
    base_url = os.environ.get("TRANSLATE_BASE_URL", "https://api.siliconflow.cn/v1")
    model = os.environ.get("TRANSLATE_MODEL", "Qwen/Qwen2.5-7B-Instruct")

    if not api_key:
        print("CONFIG_ERROR:TRANSLATE_API_KEY environment variable is not set. "
              "Please set it to your API key.", file=sys.stderr)
        sys.exit(2)

    # Read input file
    input_path = args.input_file
    if not os.path.isfile(input_path):
        print(f"FILE_ERROR:Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print("FILE_ERROR:Input file is empty", file=sys.stderr)
        sys.exit(1)

    print(f"INFO:Translating {input_path} ({len(content)} chars) to {args.target_lang}", file=sys.stderr)

    # Translate
    translated = translate_text(
        content, base_url, api_key, model, args.target_lang, args.source_lang,
        concurrency=args.concurrency,
        context_window=args.context_window,
    )

    # Determine output path
    output_path = args.output
    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_translated{ext}"

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated)

    print(f"OUTPUT:{output_path}")


if __name__ == "__main__":
    main()
