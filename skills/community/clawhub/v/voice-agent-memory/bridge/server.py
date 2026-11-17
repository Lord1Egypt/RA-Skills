"""
server.py — BlueColumn Voice Agent Memory Bridge
Accepts OpenAI-compatible /v1/chat/completions from ElevenLabs/Deepgram
Injects BlueColumn memory context, calls Anthropic Claude, stores transcripts.

Call Flow:
  1. Phone rings → ElevenLabs → POST /v1/chat/completions (with caller ID)
  2. Bridge queries BlueColumn recall for caller (parallel, <2s timeout)
  3. Builds system prompt with memory context
  4. Streams Claude response back (OpenAI-compatible SSE)
  5. After call → stores conversation to BlueColumn (fire-and-forget)
"""
import os
import json
import time
import uuid
import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load env from skill root
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(env_path)

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_builder import build_system_prompt, load_contacts, get_live_context
from memory import recall_caller, store_conversation, save_note, recall_query

logger = logging.getLogger('uvicorn')

# ============================================================
# CONFIG
# ============================================================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_BRIDGE_TOKEN = os.getenv("LLM_BRIDGE_TOKEN", "bluecolumn-voice-bridge-CHANGE_ME")
BLUECOLUMN_API_KEY = os.getenv("BLUECOLUMN_API_KEY", "")

CLAWD_DIR = os.path.expanduser("~/.openclaw/workspace")
COST_LOG = os.path.join(CLAWD_DIR, "memory", "voice-calls", "costs.jsonl")
TRANSCRIPT_DIR = os.path.join(CLAWD_DIR, "memory", "voice-calls", "transcripts")

# Whether to auto-store conversations to BlueColumn
AUTO_STORE_MEMORY = os.getenv("AUTO_STORE_MEMORY", "true").lower() == "true"
# Max recall timeout in seconds (voice needs speed)
RECALL_TIMEOUT = float(os.getenv("RECALL_TIMEOUT", "2.0"))

app = FastAPI(title="BlueColumn Voice Agent Memory Bridge")

# CORS — allow all origins for ElevenLabs/Deepgram
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# LOGGING MIDDLEWARE
# ============================================================
@app.middleware("http")
async def log_all_requests(request: Request, call_next):
    logger.info(f"→ {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.exception(f"Handler exception:")
        return JSONResponse(status_code=500, content={"error": str(e)})


# ============================================================
# AUTH
# ============================================================
async def verify_token(request: Request) -> str:
    auth = request.headers.get("authorization", "")
    token = auth.replace("Bearer ", "").strip()
    
    # Also check x-api-key header (ElevenLabs sometimes uses this)
    x_api_key = request.headers.get("x-api-key", "")
    if not token and x_api_key:
        token = x_api_key.strip()
    
    if token and token != LLM_BRIDGE_TOKEN:
        logger.warning(f"Invalid auth token (accepting anyway): {token[:15]}...")
    
    return token or "anonymous"


# ============================================================
# COST TRACKING
# ============================================================
def log_cost(call_sid: str, caller: str, duration: float, total_cost: float, breakdown: dict):
    entry = {
        "call_sid": call_sid,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "caller": caller,
        "duration_sec": round(duration, 2),
        "total_cost_usd": round(total_cost, 4),
        "breakdown": breakdown
    }
    os.makedirs(os.path.dirname(COST_LOG), exist_ok=True)
    with open(COST_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ============================================================
# TRANSCRIPT LOGGING
# ============================================================
def log_transcript(call_sid: str, caller: str, messages: list, response: str):
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    transcript = {
        "call_sid": call_sid,
        "caller": caller,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "messages": messages,
        "response": response[:2000]
    }
    filename = f"call_{call_sid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(os.path.join(TRANSCRIPT_DIR, filename), "w") as f:
        json.dump(transcript, f, indent=2)


# ============================================================
# HEALTH
# ============================================================
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "bluecolumn-voice-agent-memory",
        "bluecolumn_configured": bool(BLUECOLUMN_API_KEY),
        "anthropic_configured": bool(ANTHROPIC_API_KEY)
    }


# ============================================================
# MAIN CHAT COMPLETIONS ENDPOINT
# ============================================================
@app.api_route("/v1/chat/completions", methods=["POST", "OPTIONS"])
async def chat_completions(request: Request):
    if request.method == "OPTIONS":
        return JSONResponse(content={}, status_code=200)
    
    raw_body = await request.body()
    body_str = raw_body.decode("utf-8", errors="replace")
    
    await verify_token(request)
    
    # Parse body
    body = {}
    if body_str.strip():
        try:
            body = json.loads(body_str)
        except json.JSONDecodeError as e:
            logger.warning(f"Malformed JSON body: {e}")
            body = {}
    
    messages = body.get("messages", [])
    
    # Extract caller info from ElevenLabs metadata (sent in system message or metadata)
    caller_number = extract_caller_number(body, messages)
    
    # Determine streaming mode
    stream = body.get("stream", True)
    max_tokens = max(body.get("max_tokens", 1024), 200)
    temperature = body.get("temperature", 0.7)
    response_model = body.get("model", "claude-sonnet-4-20250514")
    
    # Extract last user message
    last_user_msg = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user_msg = m.get("content", "")
            break
    
    # Convert to Anthropic message format (skip system messages)
    claude_messages = []
    system_content = ""
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "system":
            system_content += content + "\n"
        else:
            claude_messages.append({"role": role, "content": content})
    
    if not claude_messages:
        claude_messages.append({"role": "user", "content": "Hello"})
    
    # Build conversation text for post-call storage
    conv_text = "\n".join([
        f"{m.get('role','user')}: {str(m.get('content',''))[:300]}"
        for m in claude_messages[-6:]
    ])[:3000]
    
    call_sid = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    # Init Anthropic client
    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    
    if stream:
        logger.info(f"📞 Streaming call (call_sid={call_sid}, caller={caller_number}, msgs={len(claude_messages)})")
        
        resp = StreamingResponse(
            anthropic_stream(
                client=client,
                messages=claude_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                call_sid=call_sid,
                start_time=start_time,
                response_model=response_model,
                caller_number=caller_number,
                last_user_msg=last_user_msg,
                system_content=system_content
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )
        
        # Fire-and-forget memory storage after call
        if AUTO_STORE_MEMORY:
            asyncio.ensure_future(
                store_conversation(conv_text, caller_number, f"Voice call - {caller_number} - {call_sid}")
            )
        
        return resp
    else:
        # Non-streaming (for testing)
        result = await anthropic_non_stream(
            client=client,
            messages=claude_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            call_sid=call_sid,
            start_time=start_time,
            response_model=response_model,
            caller_number=caller_number,
            system_content=system_content
        )
        
        if AUTO_STORE_MEMORY:
            asyncio.ensure_future(
                store_conversation(conv_text, caller_number, f"Voice call - {caller_number} - {call_sid}")
            )
        
        return result


# ============================================================
# EXTRACT CALLER NUMBER FROM ELEVENLABS REQUEST
# ============================================================
def extract_caller_number(body: dict, messages: list) -> str:
    """Extract caller phone number from ElevenLabs request metadata."""
    # Check top-level metadata
    metadata = body.get("metadata", {}) or {}
    caller = metadata.get("caller_number", "") or metadata.get("from_number", "") or metadata.get("phone", "")
    
    # Check system messages for caller info
    if not caller:
        for m in messages:
            if m.get("role") == "system":
                content = m.get("content", "")
                # ElevenLabs injects caller info in system message like:
                # "Caller number: +12065550123"
                import re
                match = re.search(r'(\+?\d[\d\-\(\)\s]{7,}\d)', content)
                if match:
                    caller = match.group(1).strip()
                    break
    
    # Clean up
    caller = caller.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
    return caller


# ============================================================
# STREAMING VIA ANTHROPIC (OpenAI-compatible SSE for ElevenLabs)
# ============================================================
async def anthropic_stream(
    client, messages, max_tokens, temperature,
    call_sid, start_time, response_model,
    caller_number="", last_user_msg="", system_content=""
):
    anthropic_model = "claude-sonnet-4-20250514"
    created = int(time.time())
    total_input_tokens = 0
    total_output_tokens = 0
    
    try:
        # Step 1: Start BlueColumn recall in parallel
        # We race this against the first Claude response
        recall_task = None
        recall_context = ""
        
        if caller_number and BLUECOLUMN_API_KEY:
            recall_task = asyncio.ensure_future(
                recall_caller(caller_number, timeout=RECALL_TIMEOUT)
            )
        
        # Step 2: Send initial role chunk immediately (ElevenLabs needs fast first byte)
        role_chunk = {
            "id": f"chatcmpl-{call_sid}",
            "object": "chat.completion.chunk",
            "created": created,
            "model": response_model,
            "choices": [{"delta": {"role": "assistant", "content": ""}, "index": 0, "finish_reason": None}]
        }
        yield f"data: {json.dumps(role_chunk)}\n\n"
        
        # Step 3: Try to retrieve BlueColumn recall (with timeout)
        if recall_task:
            try:
                recall_context = await asyncio.wait_for(
                    asyncio.shield(recall_task),
                    timeout=RECALL_TIMEOUT + 0.5  # slightly more generous
                )
                if recall_context:
                    logger.info(f"✅ BlueColumn recall injected for {caller_number}")
            except asyncio.TimeoutError:
                logger.warning(f"⏱️ BlueColumn recall timed out for {caller_number}")
                recall_context = ""
            except Exception as e:
                logger.warning(f"❌ BlueColumn recall error: {e}")
                recall_context = ""
        
        # Step 4: Build system prompt WITH memory context
        system_prompt = build_system_prompt(
            caller_number=caller_number,
            bluecolumn_recall=recall_context if recall_context else None,
            additional_context=system_content if system_content else None
        )
        
        # Step 5: Stream from Claude
        async with client.messages.stream(
            model=anthropic_model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=messages
        ) as stream:
            async for text in stream.text_stream:
                chunk = {
                    "id": f"chatcmpl-{call_sid}",
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": response_model,
                    "choices": [{"delta": {"content": text}, "index": 0, "finish_reason": None}]
                }
                yield f"data: {json.dumps(chunk)}\n\n"
            
            # Get final message for token counts
            final_message = await stream.get_final_message()
            total_input_tokens = final_message.usage.input_tokens
            total_output_tokens = final_message.usage.output_tokens
    
    except Exception as e:
        logger.exception(f"ANTHROPIC STREAM ERROR:")
        err_chunk = {
            "id": f"chatcmpl-{call_sid}",
            "object": "chat.completion.chunk",
            "created": created,
            "model": response_model,
            "choices": [{"delta": {"content": f"[Error: {type(e).__name__}: {str(e)}]"}, "index": 0, "finish_reason": "stop"}]
        }
        yield f"data: {json.dumps(err_chunk)}\n\n"
    
    finally:
        duration = time.time() - start_time
        # Estimate: ~$0.07/min for voice
        est_cost = 0.07 * (duration / 60)
        log_cost(call_sid, caller_number or "unknown", duration, est_cost, {
            "anthropic_input": round(total_input_tokens * 0.000003, 6),
            "anthropic_output": round(total_output_tokens * 0.000015, 6),
            "elevenlabs_tts": 0.02 * (duration / 60),
            "twilio": 0.01 * (duration / 60)
        })
    
    # Final chunk with usage
    final_chunk = {
        "id": f"chatcmpl-{call_sid}",
        "object": "chat.completion.chunk",
        "created": created,
        "model": response_model,
        "choices": [{"delta": {}, "index": 0, "finish_reason": "stop"}],
        "usage": {
            "prompt_tokens": total_input_tokens,
            "completion_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens
        }
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"
    yield "data: [DONE]\n\n"


# ============================================================
# NON-STREAMING VIA ANTHROPIC
# ============================================================
async def anthropic_non_stream(
    client, messages, max_tokens, temperature,
    call_sid, start_time, response_model,
    caller_number="", system_content=""
):
    try:
        # Run recall if we have caller info
        recall_context = ""
        if caller_number and BLUECOLUMN_API_KEY:
            try:
                recall_context = await recall_caller(caller_number, timeout=3.0)
            except:
                pass
        
        system_prompt = build_system_prompt(
            caller_number=caller_number,
            bluecolumn_recall=recall_context if recall_context else None,
            additional_context=system_content if system_content else None
        )
        
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=messages
        )
        
        content = response.content[0].text if response.content else ""
        
        result = {
            "id": f"chatcmpl-{call_sid}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": response_model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens
            }
        }
        
        duration = time.time() - start_time
        log_cost(call_sid, caller_number or "unknown", duration, 0.03, {
            "anthropic_input": round(response.usage.input_tokens * 0.000003, 6),
            "anthropic_output": round(response.usage.output_tokens * 0.000015, 6)
        })
        
        return result
        
    except Exception as e:
        logger.exception(f"ANTHROPIC NON-STREAM ERROR:")
        raise HTTPException(status_code=500, detail=f"Anthropic error: {type(e).__name__}: {str(e)}")


# ============================================================
# CALL HISTORY ENDPOINT
# ============================================================
@app.get("/calls/history")
async def call_history():
    """View recent call history."""
    if not os.path.exists(COST_LOG):
        return {"calls": []}
    
    calls = []
    with open(COST_LOG) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    calls.append(json.loads(line))
                except:
                    pass
    
    # Return last 20 calls
    return {"calls": calls[-20:]}


# ============================================================
# OUTBOUND CALL TRIGGER
# ============================================================
@app.post("/call/outbound")
async def outbound_call(request: Request):
    """
    Trigger an outbound call.
    Expects: {"to": "+12065550123", "purpose": "Follow up on..."}
    """
    body = await request.json()
    to_number = body.get("to", "")
    purpose = body.get("purpose", "Call")
    pre_call_recall = body.get("pre_call_recall", True)
    
    if not to_number:
        return JSONResponse(status_code=400, content={"error": "Missing 'to' field"})
    
    # Pre-call recall
    recall_result = ""
    if pre_call_recall and BLUECOLUMN_API_KEY:
        recall_result = await recall_caller(to_number, timeout=3.0)
    
    return {
        "status": "simulated",
        "to": to_number,
        "purpose": purpose,
        "pre_call_recall": recall_result[:200] if recall_result else "No memory found",
        "note": "Outbound calling requires Twilio API integration — see SKILL.md for setup"
    }


# ============================================================
# CATCH-ALL ROUTE (handle ElevenLabs hitting different paths)
# ============================================================
@app.api_route("/chat/completions", methods=["POST", "OPTIONS"])
async def chat_completions_root(request: Request):
    return await chat_completions(request)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"])
async def catch_all(request: Request, path: str):
    if "completions" in path:
        return await chat_completions(request)
    if request.method == "OPTIONS":
        return JSONResponse(content={}, status_code=200)
    return JSONResponse(content={"message": f"Received {request.method} /{path}"})


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BRIDGE_PORT", "8013"))
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║      🎙️ BlueColumn Voice Agent Memory Bridge            ║
╠══════════════════════════════════════════════════════════╣
║  Endpoint:  POST /v1/chat/completions                   ║
║  Port:      {port}                                        ║
║  Memory:    {'✅ BlueColumn API configured' if BLUECOLUMN_API_KEY else '❌ No BlueColumn API key'} ║
║  Anthropic: {'✅ API key configured' if ANTHROPIC_API_KEY else '❌ No API key'}     ║
║  Auto-store:{'✅ On (transcripts → BlueColumn)' if AUTO_STORE_MEMORY else '❌ Off'}  ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
