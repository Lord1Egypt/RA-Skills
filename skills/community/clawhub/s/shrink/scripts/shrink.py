#!/usr/bin/env python3
"""
shrink.py — Replace base64 image blocks in OpenClaw session JSONL files
with concise text descriptions from a vision model.

Images in session history can be 15,000–25,000+ tokens each as base64.
A text description is ~50–150 tokens — a 99%+ reduction.
"""

import argparse
import glob
import hashlib
import json
import os
import shutil
import sys
import tempfile

import requests

DEFLATED_MARKER = "[🖼️ Image deflated:"
VISION_MODEL_DEFAULT = "auto"  # auto-detect best model based on auth type
VISION_MODEL_OAUTH = "claude-haiku-4-5"  # OAuth tokens (Max/Max Pro) — only Haiku works direct
VISION_MODEL_APIKEY = "claude-sonnet-4-6"  # API keys — full model access
MAX_DESCRIPTION_TOKENS = {"standard": 500, "full": 800}
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

MODEL_PRICING = {
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},      # per MTok
    "claude-haiku-4-5": {"input": 0.25, "output": 1.25},       # per MTok
}

# Estimated tokens per API call
EST_IMAGE_INPUT_TOKENS = 1300   # image processing overhead
EST_PROMPT_TOKENS = 200         # prompt + context
EST_OUTPUT_TOKENS = 300         # average description length (context + data extraction)


def detect_key_type(key):
    """Detect whether a key is OAuth, API key, or unknown from its prefix."""
    if key.startswith("sk-ant-oat"):
        return "oauth"
    elif key.startswith("sk-ant-api"):
        return "apikey"
    elif key.startswith("sk-ant-sid"):
        return "setup"
    return "unknown"


def resolve_model(model_arg, key_type, verbose=True):
    """Resolve the vision model based on user preference and auth type.
    
    - 'auto': picks best model based on key type
    - Explicit model: uses it directly (user override)
    """
    if model_arg != "auto":
        return model_arg
    
    if key_type == "apikey":
        model = VISION_MODEL_APIKEY
        if verbose:
            print(f"   🔑 API key detected → using {model} (best quality)")
        return model
    elif key_type == "oauth":
        model = VISION_MODEL_OAUTH
        if verbose:
            print(f"   🔑 OAuth token detected → using {model} (compatible with Max/Max Pro)")
        return model
    else:
        model = VISION_MODEL_OAUTH  # safe default
        if verbose:
            print(f"   🔑 Unknown auth type → defaulting to {model}")
        return model


def get_all_api_keys(target_agent=None):
    """Collect Anthropic keys from env and auth-profiles.json.
    
    Args:
        target_agent: If specified, only read keys from this agent's auth-profiles.json.
                      If None, reads from all agents (fleet mode).
    
    Returns list of (key, key_type) tuples, sorted: API keys first, then OAuth.
    Deduplicates by key value.
    """
    found = {}  # key -> key_type (dedup)
    
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        found[key] = detect_key_type(key)

    home = os.path.expanduser("~")
    agents_dir = os.path.join(home, ".openclaw", "agents")
    
    if os.path.isdir(agents_dir):
        # If target_agent specified, only read that agent's credentials
        if target_agent:
            agent_list = [target_agent]
        else:
            # Only scan all agents if ANTHROPIC_API_KEY is not set
            # (need to find a key somewhere). If env key exists, don't scan.
            if found:
                agent_list = []  # already have a key from env, skip disk scan
            else:
                agent_list = ["main"]  # default to main agent only, not fleet
        
        for agent in agent_list:
            auth_path = os.path.join(agents_dir, agent, "agent", "auth-profiles.json")
            if os.path.isfile(auth_path):
                try:
                    with open(auth_path) as f:
                        data = json.load(f)
                    profiles = data.get("profiles", {})
                    for profile_name, profile in profiles.items():
                        if "anthropic" in profile_name:
                            token = profile.get("token")
                            if token and token not in found:
                                found[token] = detect_key_type(token)
                except Exception:
                    continue

    if not found:
        return []

    # Sort: API keys first (broader model support), then OAuth
    priority = {"apikey": 0, "oauth": 1, "setup": 2, "unknown": 3}
    return sorted(found.items(), key=lambda x: priority.get(x[1], 99))


def estimate_tokens(text_or_base64):
    """Rough token estimate: ~4 chars per token for base64/text."""
    return len(text_or_base64) // 4


def image_fingerprint(base64_data):
    """Fast fingerprint for dedup: hash first+last 1000 chars, or full if short."""
    if len(base64_data) <= 2000:
        sample = base64_data
    else:
        sample = base64_data[:1000] + base64_data[-1000:]
    return hashlib.md5(sample.encode()).hexdigest()


def estimate_cost(num_api_calls, model):
    """Estimate API cost for N calls."""
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["claude-sonnet-4-6"])
    input_tokens_per_call = EST_IMAGE_INPUT_TOKENS + EST_PROMPT_TOKENS
    output_tokens_per_call = EST_OUTPUT_TOKENS
    total_input = num_api_calls * input_tokens_per_call
    total_output = num_api_calls * output_tokens_per_call
    cost = (total_input / 1_000_000) * pricing["input"] + (total_output / 1_000_000) * pricing["output"]
    return cost


def extract_surrounding_context(lines, line_idx, content, content_idx, context_depth=5):
    """Extract conversation context around an image for context-aware description."""
    context_parts = []

    # 1. Get text from the SAME message
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            text = item.get("text", "").strip()
            if text and DEFLATED_MARKER not in text:
                human_text = text
                if "Sender (untrusted metadata)" in text:
                    parts = text.split("\n\n")
                    for part in reversed(parts):
                        part = part.strip()
                        if part and not part.startswith("Conversation info") and not part.startswith("Sender") and not part.startswith("```") and not part.startswith("[media attached"):
                            human_text = part
                            break
                if human_text and len(human_text) < 500:
                    context_parts.append(f"User message: {human_text}")
                elif human_text:
                    context_parts.append(f"User message: {human_text[:500]}...")

    # 2. Get PRECEDING messages
    preceding = []
    for prev_idx in range(max(0, line_idx - 20), line_idx):
        try:
            prev_obj = json.loads(lines[prev_idx])
            prev_msg = prev_obj.get("message", prev_obj)
            role = prev_msg.get("role", "")
            if role not in ("user", "assistant"):
                continue
            prev_content = prev_msg.get("content", "")
            snippet = ""
            if isinstance(prev_content, str) and prev_content.strip():
                snippet = prev_content.strip()[:200]
            elif isinstance(prev_content, list):
                for block in prev_content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        t = block.get("text", "").strip()
                        if t and DEFLATED_MARKER not in t:
                            if "Sender (untrusted metadata)" in t:
                                parts = t.split("\n\n")
                                for part in reversed(parts):
                                    p = part.strip()
                                    if p and not p.startswith("Conversation") and not p.startswith("Sender") and not p.startswith("```") and not p.startswith("[media"):
                                        snippet = p[:200]
                                        break
                            elif len(t) > 10:
                                snippet = t[:200]
                        if snippet:
                            break
            if snippet:
                preceding.append(f"{role}: {snippet}")
        except (json.JSONDecodeError, KeyError):
            continue

    if preceding:
        context_parts.insert(0, "Preceding conversation:\n" + "\n".join(preceding[-context_depth:]))

    # 3. Get the next assistant response
    for next_idx in range(line_idx + 1, min(line_idx + 8, len(lines))):
        try:
            next_obj = json.loads(lines[next_idx])
            next_msg = next_obj.get("message", next_obj)
            role = next_msg.get("role", "")
            if role == "assistant":
                next_content = next_msg.get("content", "")
                if isinstance(next_content, str) and next_content.strip():
                    assistant_text = next_content.strip()[:500]
                    context_parts.append(f"Assistant response: {assistant_text}")
                elif isinstance(next_content, list):
                    for block in next_content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            assistant_text = block.get("text", "").strip()[:500]
                            if assistant_text:
                                context_parts.append(f"Assistant response: {assistant_text}")
                                break
                break
            elif role == "user":
                break
        except (json.JSONDecodeError, KeyError):
            continue

    return "\n".join(context_parts) if context_parts else ""


_dead_keys = set()  # Cache of keys that have failed — skip on subsequent calls


def describe_image(api_keys, base64_data, mime_type, model, context="", detail="standard", redact=None, verbose=True):
    """Call Anthropic vision API with automatic failover across available keys.
    
    api_keys: list of (key, key_type) tuples
    detail: 'standard' (context + data) or 'full' (context + data + visual)
    Tries each key in order, skipping known-dead keys.
    Adjusts model automatically if falling back from API key to OAuth.
    Returns (description, model_used, key_type_used) or (None, None, None).
    """
    # Filter out known-dead keys, but keep at least one to try
    live_keys = [(k, t) for k, t in api_keys if k not in _dead_keys]
    if not live_keys:
        live_keys = api_keys  # all dead, try them all again as last resort
    api_keys = live_keys

    # Build tier sections based on detail level
    visual_section = ""
    if detail == "full":
        if context:
            visual_section = (
                "\n\nVISUAL: Describe the visual design and layout details that are relevant "
                "to the conversation above. Use the conversation context as a guide for what "
                "visual aspects matter most — if the discussion is about UI layout, focus on "
                "spacing, alignment, and component arrangement. If about styling, focus on colors, "
                "fonts, and visual hierarchy. If about bugs, focus on visual anomalies. "
                "Include: colors (with hex where identifiable), layout structure, component sizes, "
                "spacing, visual hierarchy, icons, badges, typography, and any design patterns. "
                "Be specific enough that someone could reconstruct the layout from your description."
            )
        else:
            visual_section = (
                "\n\nVISUAL: Describe the visual design and layout of the image. "
                "Include: colors (with hex where identifiable), layout structure, component "
                "arrangement, spacing, visual hierarchy, typography, icons, badges, and "
                "any notable design patterns or anomalies."
            )

    # Build redaction instructions based on --redact level
    redact_instruction = ""
    if redact:
        redact_types = {
            "pii": (
                "\n\n⚠️ REDACTION (PII): Replace ALL personally identifiable information with "
                "redaction markers. This includes: full names → [REDACTED-NAME], dates of birth → "
                "[REDACTED-DOB], Social Security numbers → [REDACTED-SSN], phone numbers → "
                "[REDACTED-PHONE], email addresses → [REDACTED-EMAIL], physical/mailing addresses → "
                "[REDACTED-ADDR], account numbers → [REDACTED-ACCT], driver's license numbers → "
                "[REDACTED-DL], any other personal identifiers → [REDACTED-PII]. "
                "Keep non-PII data (amounts, statuses, dates that aren't birthdays, technical values) readable."
            ),
            "keys": (
                "\n\n⚠️ REDACTION (KEYS): Replace ALL secrets and credentials with redaction markers. "
                "This includes: API keys → [REDACTED-KEY], passwords → [REDACTED-PASS], tokens/bearer "
                "tokens → [REDACTED-TOKEN], connection strings → [REDACTED-CONN], private keys → "
                "[REDACTED-PRIVKEY], webhook URLs with auth → [REDACTED-WEBHOOK], any string that "
                "looks like a secret or credential → [REDACTED-SECRET]. "
                "Keep non-secret technical values (ports, hostnames, status codes, config names) readable."
            ),
            "all": (
                "\n\n⚠️ REDACTION (ALL): Replace ALL sensitive information with redaction markers. "
                "This includes everything in PII and KEYS categories, plus: IP addresses → "
                "[REDACTED-IP], URLs containing auth parameters → [REDACTED-URL], financial amounts → "
                "[REDACTED-FINANCIAL], internal hostnames/domains → [REDACTED-HOST], file paths "
                "containing usernames → [REDACTED-PATH], any data that could identify a person, "
                "system, or account → [REDACTED]. "
                "Keep only generic labels, statuses, UI element names, and structural descriptions readable."
            ),
        }
        redact_instruction = redact_types.get(redact, redact_types["all"])

    format_spec = "CONTEXT: <conversational description>\nDATA: <key: value | key: value | ...>"
    if detail == "full":
        format_spec += "\nVISUAL: <visual design description>"

    if context:
        prompt = (
            f"Analyze this image in {'three' if detail == 'full' else 'two'} sections:\n\n"
            "CONTEXT: In 1-3 sentences, describe what this image shows and why it matters "
            "in the conversation. Here is the conversation context:\n\n"
            f"{context}\n\n"
            "DATA: Extract ALL readable text, numbers, values, labels, statuses, dates, "
            "names, IDs, URLs, error messages, and data points visible in the image. "
            "Format as key-value pairs separated by pipes. Include everything — even "
            "details not discussed in the conversation. Someone may need to reference "
            "specific values later."
            f"{visual_section}"
            f"{redact_instruction}\n\n"
            f"Format your response exactly as:\n{format_spec}"
        )
    else:
        prompt = (
            f"Analyze this image in {'three' if detail == 'full' else 'two'} sections:\n\n"
            "CONTEXT: In 1-2 sentences, describe what this image shows. "
            "Focus on UI elements, text content, error messages, or key visual information.\n\n"
            "DATA: Extract ALL readable text, numbers, values, labels, statuses, dates, "
            "names, IDs, URLs, error messages, and data points visible in the image. "
            "Format as key-value pairs separated by pipes."
            f"{visual_section}"
            f"{redact_instruction}\n\n"
            f"Format your response exactly as:\n{format_spec}"
        )

    FAILOVER_CODES = {401, 402, 403, 529}  # auth, billing, forbidden, overloaded

    for key_idx, (api_key, key_type) in enumerate(api_keys):
        # If falling back from API key to OAuth, downgrade model automatically
        use_model = model
        if key_type == "oauth" and model in (VISION_MODEL_APIKEY, "claude-sonnet-4-6"):
            use_model = VISION_MODEL_OAUTH
            if verbose and key_idx > 0:
                print(f"      🔄 Falling back to OAuth → switching model to {use_model}")

        headers = {
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "content-type": "application/json",
        }

        payload = {
            "model": use_model,
            "max_tokens": MAX_DESCRIPTION_TOKENS.get(detail, 500),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,
                                "data": base64_data,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        }

        try:
            resp = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=30)
            
            # Check if we should failover
            if resp.status_code in FAILOVER_CODES and key_idx < len(api_keys) - 1:
                error_type = "unknown"
                try:
                    error_type = resp.json().get("error", {}).get("type", "unknown")
                except Exception:
                    pass
                # Mark this key as dead so we skip it for all remaining images
                _dead_keys.add(api_key)
                key_label = f"{key_type} (...{api_key[-8:]})"
                if verbose:
                    print(f"      ⚠️  {key_label}: HTTP {resp.status_code} ({error_type}) — marked dead, trying next key...")
                continue
            
            resp.raise_for_status()
            result = resp.json()
            for block in result.get("content", []):
                if block.get("type") == "text":
                    return block["text"], use_model, key_type
            return None, None, None
            
        except requests.exceptions.HTTPError as e:
            _dead_keys.add(api_key)
            if key_idx < len(api_keys) - 1:
                if verbose:
                    print(f"      ⚠️  Key failed: {e} — marked dead, trying next key...")
                continue
            if verbose:
                print(f"      ❌ All keys exhausted. Last error: {e}", file=sys.stderr)
            return None, None, None
        except Exception as e:
            if verbose:
                print(f"      ❌ API error: {e}", file=sys.stderr)
            return None, None, None
    
    return None, None, None


def process_session(session_file, dry_run=False, verbose=True, context_depth=5,
                    model=VISION_MODEL_DEFAULT, max_images=None, no_backup=False,
                    min_tokens=500, json_output=False, dedup_cache=None, detail="standard",
                    target_agent=None, redact=None):
    """Process a session JSONL file, replacing image blocks with descriptions.
    
    Returns a result dict with stats for JSON output / aggregation.
    """
    api_keys = get_all_api_keys(target_agent=target_agent)
    if not api_keys:
        if not json_output:
            print("❌ No Anthropic API key found.", file=sys.stderr)
            print("   Set ANTHROPIC_API_KEY env var or configure auth-profiles.json", file=sys.stderr)
        sys.exit(1)

    # Auto-resolve model based on primary key type
    primary_key_type = api_keys[0][1]
    model = resolve_model(model, primary_key_type, verbose=verbose and not json_output)
    
    if verbose and not json_output:
        key_sources = []
        for _, kt in api_keys:
            if kt == "apikey":
                key_sources.append("API key")
            elif kt == "oauth":
                key_sources.append("OAuth token")
            else:
                key_sources.append(kt)
        source_desc = f"from {'agent ' + target_agent if target_agent else 'environment/fleet'}"
        print(f"   🔑 Using {len(api_keys)} key(s) {source_desc}: {', '.join(key_sources)}")
        if len(api_keys) > 1:
            print(f"   🔄 Automatic failover enabled")
        if redact:
            redact_labels = {"pii": "PII (names, DOBs, phones, emails, addresses)", "keys": "Secrets (API keys, passwords, tokens)", "all": "All sensitive data (PII + secrets + IPs + financials)"}
            print(f"   🔒 Redaction: {redact_labels.get(redact, redact)}")

    if dedup_cache is None:
        dedup_cache = {}

    filename = os.path.basename(session_file)
    log = not json_output  # suppress pretty output in JSON mode

    if log and verbose:
        print(f"\n🔍 Scanning session: {filename}")

    with open(session_file, "r") as f:
        lines = f.readlines()

    # First pass: find all images
    image_locations = []  # (line_idx, content_idx, message_id)
    for line_idx, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        content = None
        msg_id = obj.get("id", "unknown")

        if isinstance(obj.get("content"), list):
            content = obj["content"]
        elif isinstance(obj.get("message"), dict):
            msg = obj["message"]
            msg_id = obj.get("id", msg.get("id", "unknown"))
            if isinstance(msg.get("content"), list):
                content = msg["content"]

        if not content:
            continue

        for content_idx, item in enumerate(content):
            if not isinstance(item, dict):
                continue
            if item.get("type") != "image":
                continue
            if "data" not in item:
                continue
            if DEFLATED_MARKER in item.get("text", ""):
                continue
            image_locations.append((line_idx, content_idx, msg_id))

    total_images = len(image_locations)
    if log and verbose:
        print(f"📊 Found {total_images} image(s) in session history")

    if total_images == 0:
        if log:
            print("\n✅ No unprocessed images found. Session is already optimized!")
        return {
            "session_file": session_file,
            "images_found": 0, "images_processed": 0, "images_skipped": 0,
            "images_deduped": 0, "images_failed": 0, "tokens_saved": 0,
            "tokens_original": 0, "savings_percent": 0.0, "context_freed_kb": 0,
            "estimated_cost_usd": 0.0, "model": model, "dry_run": dry_run,
            "images": [],
        }

    # Apply --max-images limit
    if max_images is not None and max_images < total_images:
        if log and verbose:
            print(f"🔢 --max-images {max_images}: processing first {max_images} of {total_images}")
        image_locations = image_locations[:max_images]

    if log and dry_run:
        print(f"\n🔎 DRY RUN — no changes will be written\n")

    total_saved = 0
    total_original = 0
    processed = 0
    failed = 0
    skipped = 0
    deduped = 0
    api_calls = 0
    image_results = []

    for idx, (line_idx, content_idx, msg_id) in enumerate(image_locations):
        obj = json.loads(lines[line_idx])

        if isinstance(obj.get("content"), list):
            content = obj["content"]
        else:
            content = obj["message"]["content"]

        item = content[content_idx]
        base64_data = item.get("data", "")
        mime_type = item.get("mimeType", "image/jpeg")

        original_tokens = estimate_tokens(base64_data)
        original_kb = len(base64_data) / 1024

        # --min-tokens check
        if original_tokens < min_tokens:
            if log and verbose:
                print(f"\n⏭️  Skipping image {idx + 1}/{len(image_locations)} — {original_tokens:,} tokens < min {min_tokens}")
            skipped += 1
            image_results.append({
                "line": line_idx + 1, "message_id": msg_id,
                "original_tokens": original_tokens, "new_tokens": original_tokens,
                "savings_tokens": 0, "savings_percent": 0.0, "description": None,
                "deduped": False, "skipped": True, "skip_reason": f"below min_tokens ({min_tokens})",
            })
            continue

        if log and verbose:
            print(f"\n🖼️  Processing image {idx + 1}/{len(image_locations)}...")
            print(f"   📍 Message ID: {msg_id} (line {line_idx + 1})")
            print(f"   📐 Original size: ~{original_tokens:,} tokens ({original_kb:,.0f} KB)")

        # Dedup check
        fp = image_fingerprint(base64_data)
        is_dedup = fp in dedup_cache

        if is_dedup:
            description = dedup_cache[fp]
            deduped += 1
            if log and verbose:
                src = dedup_cache.get(f"{fp}_src", "earlier")
                print(f"   ♻️ Duplicate detected — reusing description from {src}")
        else:
            # Extract conversation context
            context = extract_surrounding_context(lines, line_idx, content, content_idx, context_depth)
            if log and verbose and context:
                context_preview = context.split("\n")[0][:100]
                print(f"   💬 Context: {context_preview}...")

            if not dry_run:
                if log and verbose:
                    print(f"   🤖 Generating context-aware description via {model}...")
                desc_result = describe_image(api_keys, base64_data, mime_type, model, context, detail, redact, verbose and log)
                description = desc_result[0] if desc_result else None
                api_calls += 1
            else:
                description = "<dry-run: context-aware description would be generated here>"
                api_calls += 1  # count for cost estimate

            if description is None:
                failed += 1
                if log and verbose:
                    print(f"   ⚠️  Skipped (API call failed)")
                image_results.append({
                    "line": line_idx + 1, "message_id": msg_id,
                    "original_tokens": original_tokens, "new_tokens": original_tokens,
                    "savings_tokens": 0, "savings_percent": 0.0, "description": None,
                    "deduped": False, "skipped": False, "skip_reason": "api_error",
                })
                continue

            # Cache for dedup
            dedup_cache[fp] = description
            dedup_cache[f"{fp}_src"] = f"image {idx + 1}/{len(image_locations)}"

        new_tokens = estimate_tokens(description)
        savings = original_tokens - new_tokens
        savings_pct = (savings / original_tokens * 100) if original_tokens > 0 else 0

        replacement_text = (
            f"{DEFLATED_MARKER} {description} "
            f"| Original: ~{original_tokens:,} tokens → ~{new_tokens:,} tokens "
            f"| Savings: {savings_pct:.1f}%]"
        )

        if log and verbose:
            display_desc = description[:120] + "..." if len(description) > 120 else description
            print(f'   ✅ Description: "{display_desc}"')
            print(f"   💾 New size: ~{new_tokens:,} tokens")
            print(f"   📉 Savings: {savings:,} tokens ({savings_pct:.1f}%)")

        # Replace the image block with a text block
        content[content_idx] = {"type": "text", "text": replacement_text}
        lines[line_idx] = json.dumps(obj, ensure_ascii=False) + "\n"

        total_saved += savings
        total_original += original_tokens
        processed += 1

        image_results.append({
            "line": line_idx + 1, "message_id": msg_id,
            "original_tokens": original_tokens, "new_tokens": new_tokens,
            "savings_tokens": savings, "savings_percent": round(savings_pct, 1),
            "description": description, "deduped": is_dedup,
            "skipped": False, "skip_reason": None,
        })

    # Cost estimate — api_calls already excludes deduped (they don't hit the API)
    est_cost = estimate_cost(api_calls, model)

    total_pct = (total_saved / total_original * 100) if total_original > 0 else 0
    freed_kb = total_saved * 4 / 1024

    result = {
        "session_file": session_file,
        "images_found": total_images,
        "images_processed": processed,
        "images_skipped": skipped,
        "images_deduped": deduped,
        "images_failed": failed,
        "tokens_saved": total_saved,
        "tokens_original": total_original,
        "savings_percent": round(total_pct, 1),
        "context_freed_kb": round(freed_kb),
        "estimated_cost_usd": round(est_cost, 4),
        "model": model,
        "dry_run": dry_run,
        "images": image_results,
    }

    # Pretty summary
    if log:
        print(f"\n{'═' * 50}")
        print(f"📊 DEFLATION {'PREVIEW' if dry_run else 'COMPLETE'}")
        print(f"{'═' * 50}")
        print(f"  Images found:       {total_images}")
        print(f"  Images processed:   {processed}")
        if skipped:
            print(f"  Images skipped:     {skipped} (below {min_tokens} tokens)")
        if deduped:
            print(f"  Images deduped:     {deduped} (reused descriptions)")
        if failed:
            print(f"  Images failed:      {failed}")
        print(f"  Total tokens saved: ~{total_saved:,} ({total_pct:.1f}%)")
        print(f"  Context freed:      ~{freed_kb:,.0f} KB")
        print(f"  API cost:           ~${est_cost:.4f} ({model})")
        if deduped:
            full_cost = estimate_cost(api_calls + deduped, model)
            saved_cost = full_cost - est_cost
            print(f"  Dedup savings:      ~${saved_cost:.4f}")
        print(f"{'═' * 50}")

    if dry_run:
        if log:
            print(f"\n💡 Run without --dry-run to apply changes.")
        return result

    if processed == 0:
        if log:
            print("\n⚠️  No images were processed.")
        return result

    # Backup original
    if not no_backup:
        backup_path = session_file + ".bak"
        shutil.copy2(session_file, backup_path)
        if log and verbose:
            print(f"\n💾 Backup saved: {os.path.basename(backup_path)}")

    # Write modified file
    with open(session_file, "w") as f:
        f.writelines(lines)

    if log and verbose:
        print(f"✅ Session file updated: {filename}")

    return result


def find_agent_sessions_dir(agent_id):
    """Return the sessions directory for an agent."""
    home = os.path.expanduser("~")
    sessions_dir = os.path.join(home, ".openclaw", "agents", agent_id, "sessions")
    if os.path.isdir(sessions_dir):
        return sessions_dir
    return None


def find_most_recent_session(sessions_dir):
    """Find the most recently modified .jsonl file in a sessions directory."""
    jsonl_files = glob.glob(os.path.join(sessions_dir, "*.jsonl"))
    if not jsonl_files:
        return None
    return max(jsonl_files, key=os.path.getmtime)


def main():
    parser = argparse.ArgumentParser(
        description="Replace base64 images in session JSONL with text descriptions",
        epilog="Examples:\n"
               "  %(prog)s --session-file path/to/session.jsonl --dry-run\n"
               "  %(prog)s --agent main --all-sessions --no-backup\n"
               "  %(prog)s --agent main --max-images 5 --model claude-haiku-4-5\n"
               "  %(prog)s --agent main --all-sessions --json\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--session-file", help="Path to session JSONL file"
    )
    parser.add_argument(
        "--agent", metavar="ID",
        help="Agent ID — targets ~/.openclaw/agents/<ID>/sessions/"
    )
    parser.add_argument(
        "--all-sessions", action="store_true",
        help="Process ALL .jsonl files in the agent's sessions directory"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without modifying"
    )
    parser.add_argument(
        "--model", default=VISION_MODEL_DEFAULT,
        help="Vision model to use (default: auto — picks best model based on auth type)"
    )
    parser.add_argument(
        "--max-images", type=int, default=None, metavar="N",
        help="Only process the first N images found (default: all)"
    )
    parser.add_argument(
        "--no-backup", action="store_true",
        help="Skip creating .bak backup file"
    )
    parser.add_argument(
        "--min-tokens", type=int, default=500, metavar="N",
        help="Skip images with fewer than N estimated tokens (default: 500)"
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output results as JSON instead of pretty-printed text"
    )
    parser.add_argument(
        "--verbose", action="store_true", default=True,
        help="Verbose output (default)"
    )
    parser.add_argument(
        "--no-verbose", action="store_true",
        help="Suppress detailed output"
    )
    parser.add_argument(
        "--detail", choices=["standard", "full"], default="full",
        help="Extraction detail: standard (context + data) or full (+ visual design) (default: full)"
    )
    parser.add_argument(
        "--redact", choices=["pii", "keys", "all"], default=None,
        help="Redact sensitive data during extraction: pii (names, DOBs, SSNs, phones, emails, addresses), keys (API keys, passwords, tokens, secrets), all (pii + keys + IPs, financial amounts, internal hosts)"
    )
    parser.add_argument(
        "--context-depth", type=int, default=10,
        help="Number of preceding messages for context (default: 10)"
    )

    args = parser.parse_args()
    verbose = not args.no_verbose

    # Resolve target session file(s)
    session_files = []

    if args.session_file:
        # --session-file takes precedence
        if not os.path.isfile(args.session_file):
            print(f"❌ File not found: {args.session_file}", file=sys.stderr)
            sys.exit(1)
        if args.all_sessions:
            # Derive sessions dir from file path
            sessions_dir = os.path.dirname(os.path.abspath(args.session_file))
            session_files = sorted(glob.glob(os.path.join(sessions_dir, "*.jsonl")))
        else:
            session_files = [args.session_file]

    elif args.agent:
        sessions_dir = find_agent_sessions_dir(args.agent)
        if not sessions_dir:
            print(f"❌ Sessions directory not found for agent '{args.agent}'", file=sys.stderr)
            print(f"   Expected: ~/.openclaw/agents/{args.agent}/sessions/", file=sys.stderr)
            sys.exit(1)

        if args.all_sessions:
            session_files = sorted(glob.glob(os.path.join(sessions_dir, "*.jsonl")))
            if not session_files:
                print(f"❌ No .jsonl files found in {sessions_dir}", file=sys.stderr)
                sys.exit(1)
        else:
            # Find most recent session
            most_recent = find_most_recent_session(sessions_dir)
            if not most_recent:
                print(f"❌ No .jsonl files found in {sessions_dir}", file=sys.stderr)
                sys.exit(1)
            session_files = [most_recent]
            if not args.json_output and verbose:
                print(f"📂 Using most recent session: {os.path.basename(most_recent)}")

    else:
        print("❌ Must provide either --session-file or --agent", file=sys.stderr)
        print("", file=sys.stderr)
        print("Usage examples:", file=sys.stderr)
        print("  shrink.py --session-file path/to/session.jsonl", file=sys.stderr)
        print("  shrink.py --agent main                           # most recent session", file=sys.stderr)
        print("  shrink.py --agent main --all-sessions            # all sessions", file=sys.stderr)
        sys.exit(1)

    # Shared dedup cache across all files in a run
    dedup_cache = {}
    all_results = []

    for sf in session_files:
        result = process_session(
            sf,
            dry_run=args.dry_run,
            verbose=verbose,
            context_depth=args.context_depth,
            model=args.model,
            max_images=args.max_images,
            no_backup=args.no_backup,
            min_tokens=args.min_tokens,
            json_output=args.json_output,
            dedup_cache=dedup_cache,
            detail=args.detail,
            target_agent=getattr(args, 'agent', None),
            redact=args.redact,
        )
        if result:
            all_results.append(result)

    # Grand total for multi-file runs
    if len(session_files) > 1 and not args.json_output:
        total_found = sum(r["images_found"] for r in all_results)
        total_processed = sum(r["images_processed"] for r in all_results)
        total_skipped = sum(r["images_skipped"] for r in all_results)
        total_deduped = sum(r["images_deduped"] for r in all_results)
        total_failed = sum(r["images_failed"] for r in all_results)
        total_saved = sum(r["tokens_saved"] for r in all_results)
        total_original = sum(r["tokens_original"] for r in all_results)
        total_cost = sum(r["estimated_cost_usd"] for r in all_results)
        total_pct = (total_saved / total_original * 100) if total_original > 0 else 0
        freed_kb = total_saved * 4 / 1024

        print(f"\n{'━' * 50}")
        print(f"📊 GRAND TOTAL ({len(session_files)} session files)")
        print(f"{'━' * 50}")
        print(f"  Images found:       {total_found}")
        print(f"  Images processed:   {total_processed}")
        if total_skipped:
            print(f"  Images skipped:     {total_skipped}")
        if total_deduped:
            print(f"  Images deduped:     {total_deduped}")
        if total_failed:
            print(f"  Images failed:      {total_failed}")
        print(f"  Total tokens saved: ~{total_saved:,} ({total_pct:.1f}%)")
        print(f"  Context freed:      ~{freed_kb:,.0f} KB")
        print(f"  Total API cost:     ~${total_cost:.4f}")
        print(f"{'━' * 50}")

    # JSON output
    if args.json_output:
        if len(all_results) == 1 and not args.all_sessions:
            print(json.dumps(all_results[0], indent=2, ensure_ascii=False))
        else:
            print(json.dumps(all_results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
