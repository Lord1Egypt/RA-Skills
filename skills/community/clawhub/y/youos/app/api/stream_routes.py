from __future__ import annotations

import json
import os
import re
import signal
import subprocess
from typing import Literal

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.core.rate_limit import RATE_LIMIT_RESPONSE, draft_limiter
from app.core.sender import classify_sender, extract_domain
from app.core.text_utils import strip_quoted_text
from app.generation.service import (
    DraftRequest,
    _adapter_available,
    _apply_cached_order,
    _format_sender_context,
    _get_base_model_id,
    _get_cached_exemplar_ids,
    _load_persona,
    _load_prompts,
    _local_model_available,
    _precedent_summary,
    _score_confidence,
    _top_exemplar_source_ids,
    _update_exemplar_cache,
    assemble_prompt,
    generate_draft,
    lookup_sender_profile,
)
from app.retrieval.service import RetrievalRequest, retrieve_context

router = APIRouter(prefix="/draft", tags=["draft-stream"])


class StreamBody(BaseModel):
    inbound_text: str = Field(min_length=1)
    tone_hint: Literal["shorter", "more_formal", "more_detail"] | None = None
    sender: str | None = None
    mode: Literal["reply", "compose"] | None = "reply"
    user_prompt: str | None = None


def _iter_mlx_body(stdout):
    """Stream the generated text out of mlx_lm's framed stdout.

    mlx_lm frames output as ``<prelude> ===== <generated text> ===== <stats>``.
    We read in small chunks (not lines — a short reply is a single line and would
    otherwise buffer to the end, killing the live-typing effect), drop the
    prelude and stats, and withhold only a trailing run that could be the *start*
    of the closing delimiter (``\\n=*``) so body text streams chunk-by-chunk.
    """
    buf = ""
    in_body = False
    while True:
        chunk = stdout.read(64)
        if not chunk:
            break
        buf += chunk
        if not in_body:
            m = re.search(r"={5,}[^\n]*\n", buf)
            if not m:
                continue
            in_body = True
            buf = buf[m.end():]
        close = re.search(r"\n={5,}", buf)
        if close:
            head = buf[: close.start()]
            if head:
                yield head
            return
        hold = re.search(r"\n=*$", buf)  # might be the opening of the closing delimiter
        if hold:
            out, buf = buf[: hold.start()], buf[hold.start():]
        else:
            out, buf = buf, ""
        if out:
            yield out
    # EOF with no closing delimiter — flush whatever body remains.
    if in_body and buf:
        tail = re.split(r"\n={5,}", buf)[0]
        if tail:
            yield tail


def _stream_generate(body: StreamBody, settings):
    """Generator that yields SSE events."""
    clean_inbound = strip_quoted_text(body.inbound_text)

    sender_type_hint = None
    sender_domain_hint = None
    if body.sender:
        sender_type_hint = classify_sender(body.sender)
        sender_domain_hint = extract_domain(body.sender)

    retrieval_response = retrieve_context(
        RetrievalRequest(
            query=clean_inbound,
            scope="all",
            top_k_reply_pairs=5,
            top_k_chunks=3,
            sender_type_hint=sender_type_hint,
            sender_domain_hint=sender_domain_hint,
        ),
        database_url=settings.database_url,
        configs_dir=settings.configs_dir,
    )

    reply_pairs = retrieval_response.reply_pairs

    # Apply exemplar caching (read + write)
    from app.core.intent import classify_intents_multi
    intents = classify_intents_multi(clean_inbound)
    detected_intent = intents[0]

    cached_ids, exemplar_cache_hit, exemplar_cache_key = _get_cached_exemplar_ids(
        detected_intent,
        sender_type_hint,
        database_url=settings.database_url,
    )
    reply_pairs = _apply_cached_order(reply_pairs, cached_ids)

    selected_ids = _top_exemplar_source_ids(reply_pairs)
    _update_exemplar_cache(
        detected_intent,
        sender_type_hint,
        selected_ids,
        database_url=settings.database_url,
    )

    confidence, _ = _score_confidence(reply_pairs)
    precedent_used = [_precedent_summary(rp) for rp in reply_pairs]
    detected_mode = retrieval_response.detected_mode
    # Draft-quality metadata, populated when we fall back to generate_draft
    # (the local-model path; the Claude-CLI streaming path doesn't produce it).
    length_flag: str | None = None
    repairs: list[str] = []
    candidates: list[dict] = []
    # Which model actually produced this draft — the streaming path uses the
    # Claude CLI directly; the non-streaming fallback reports its own model_used.
    model_used: str | None = None

    prompts = _load_prompts(settings.configs_dir)
    persona = _load_persona(settings.configs_dir)

    sender_context = None
    if body.sender:
        sender_profile = lookup_sender_profile(body.sender, settings.database_url)
        if sender_profile:
            sender_context = _format_sender_context(sender_profile)

    prompt = assemble_prompt(
        inbound_message=clean_inbound,
        reply_pairs=reply_pairs,
        persona=persona,
        prompts=prompts,
        detected_mode=detected_mode,
        tone_hint=body.tone_hint,
        sender_context=sender_context,
        sender_type=sender_type_hint,
        user_prompt=body.user_prompt,
    )

    # Prefer the local fine-tuned model for streaming when it's ready (mlx_lm on
    # PATH + a trained adapter) so the Draft Reply tab drafts in YOUR voice,
    # on-device. Fall back to the Claude CLI only when there's no adapter yet;
    # any streaming error drops to the non-streaming generate_draft below.
    from app.core.settings import get_adapter_path

    stream_local = _local_model_available() and _adapter_available()

    # Fastest path: stream from the warm model server (no per-draft reload) when
    # it's enabled and healthy. Falls through to the per-request subprocess /
    # Claude paths below on any failure.
    if stream_local:
        from app.core import model_server

        if model_server.is_enabled() and model_server.ensure_running():
            streamed_any = False
            failed = False
            try:
                for piece in model_server.stream(prompt, max_tokens=400):
                    streamed_any = True
                    yield f"data: {json.dumps({'token': piece})}\n\n"
            except Exception:
                failed = True
            # Return unless it failed before producing anything — only then is it
            # safe to fall through and re-stream from the subprocess/Claude path.
            if streamed_any or not failed:
                done_payload = {
                    "done": True,
                    "confidence": confidence,
                    "precedent_used": precedent_used,
                    "exemplar_cache_hit": exemplar_cache_hit,
                    "exemplar_cache_key": exemplar_cache_key,
                    "length_flag": length_flag,
                    "repairs": repairs,
                    "candidates": candidates,
                    "model_used": model_server.model_label(),
                }
                yield f"data: {json.dumps(done_payload)}\n\n"
                return

    proc = None
    try:
        if stream_local:
            # mlx_lm frames output as: <prelude> ===== <generated text> ===== <stats>.
            # Stream only the body between the delimiters; PYTHONUNBUFFERED so the
            # child flushes tokens as generated instead of buffering to the end.
            cmd = [
                "mlx_lm", "generate",
                "--model", _get_base_model_id(),
                "--adapter-path", str(get_adapter_path()),
                "--prompt", prompt,
                "--max-tokens", "400",
            ]
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
            )
            for piece in _iter_mlx_body(proc.stdout):
                yield f"data: {json.dumps({'token': piece})}\n\n"
            proc.wait(timeout=120)
            if proc.returncode != 0:
                raise RuntimeError("mlx_lm generate failed")
            model_used = "qwen2.5-1.5b-lora"  # streamed from the local LoRA adapter
        else:
            # No trained adapter (or no mlx_lm): stream via the Claude CLI. Pass
            # the prompt via -p so one beginning with '-' isn't parsed as a flag;
            # new session so we can kill the whole process group on cleanup.
            proc = subprocess.Popen(
                ["claude", "--print", "-p", prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )
            for line in proc.stdout:
                # Emit each line including its trailing newline, blank lines too, so
                # paragraph breaks survive streaming. The token carries its own
                # newline; the client must not add one.
                yield f"data: {json.dumps({'token': line})}\n\n"
            proc.wait(timeout=120)
            if proc.returncode != 0:
                raise RuntimeError("claude CLI failed")
            model_used = "claude"  # streamed via the Claude CLI
    except Exception:
        # Fallback: generate full draft non-streaming
        try:
            response = generate_draft(
                DraftRequest(
                    inbound_message=body.inbound_text,
                    tone_hint=body.tone_hint,
                    sender=body.sender,
                    mode=body.mode,
                ),
                database_url=settings.database_url,
                configs_dir=settings.configs_dir,
            )
            yield f"data: {json.dumps({'token': response.draft})}\n\n"
            confidence = response.confidence
            precedent_used = response.precedent_used
            length_flag = response.length_flag
            repairs = response.repairs
            candidates = response.candidates
            model_used = response.model_used
        except Exception as exc:
            yield f"data: {json.dumps({'token': f'[generation failed: {exc}]'})}\n\n"
    finally:
        # Don't leave a hung claude (or its child processes) running if we
        # errored out or the client disconnected mid-stream.
        if proc and proc.poll() is None:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                proc.kill()

    done_payload = {
        "done": True,
        "confidence": confidence,
        "precedent_used": precedent_used,
        "exemplar_cache_hit": exemplar_cache_hit,
        "exemplar_cache_key": exemplar_cache_key,
        "length_flag": length_flag,
        "repairs": repairs,
        "candidates": candidates,
        "model_used": model_used,
    }
    yield f"data: {json.dumps(done_payload)}\n\n"


@router.post("/stream")
def draft_stream(body: StreamBody, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if not draft_limiter.is_allowed(client_ip):
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=429, content=RATE_LIMIT_RESPONSE)
    settings = request.app.state.settings
    return StreamingResponse(
        _stream_generate(body, settings),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
