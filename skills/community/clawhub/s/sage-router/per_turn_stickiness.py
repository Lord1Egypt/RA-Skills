"""
Per-turn model stickiness patch for sage-router.

Problem: Each API call from OpenClaw gets independently routed, which means
within a single agent turn (multiple tool calls), the model can switch between
providers. This causes inconsistent behavior — e.g., a cheap model terminates
early with NO_REPLY while the thinking model would have continued.

Solution: Cache the selected (provider, model) pair per request_id prefix
(session key). Once a model is selected for a turn, all subsequent requests
in that same turn use the same provider/model.

Implementation:
1. Add a TURN_STICKINESS_CACHE dict (session_key -> (provider, model, timestamp))
2. In prepare_route(), check the cache first. If a recent entry exists for this
   session, use it as the forced provider/model.
3. In route_request(), after successful model selection, cache the result.
4. TTL of 5 minutes — long enough for a multi-tool-call turn, short enough to
   not stale across different conversations.

This patch should be applied to router.py at the following locations:

A) After TEMP_MODEL_BLOCKS dict (around line 278), add:
    TURN_STICKINESS_CACHE = {}
    TURN_STICKINESS_TTL_SECONDS = 300  # 5 minutes

B) Add a helper function after clear_temp_model_block():
    def get_turn_sticky_model(request_id):
        \"\"\"Check if there's a recent turn-sticky model for this session.\"\"\"
        # Extract session key from request_id (format: agent:session:turnN or similar)
        # Use everything before the last colon/turn number as the session key
        if not request_id or request_id == 'req-unknown':
            return None
        parts = request_id.rsplit(':', 1)
        session_key = parts[0] if len(parts) > 1 else request_id
        entry = TURN_STICKINESS_CACHE.get(session_key)
        if not entry:
            return None
        provider, model, ts = entry
        if time.time() - ts > TURN_STICKINESS_TTL_SECONDS:
            del TURN_STICKINESS_CACHE[session_key]
            return None
        # Check if provider/model is still available
        if provider in DISABLED_PROVIDERS:
            del TURN_STICKINESS_CACHE[session_key]
            return None
        if provider not in PROVIDERS:
            del TURN_STICKINESS_CACHE[session_key]
            return None
        if model_disabled_reason(provider, model):
            del TURN_STICKINESS_CACHE[session_key]
            return None
        return (provider, model)
    
    def set_turn_sticky_model(request_id, provider, model):
        \"\"\"Cache the selected model for this session turn.\"\"\"
        if not request_id or request_id == 'req-unknown':
            return
        parts = request_id.rsplit(':', 1)
        session_key = parts[0] if len(parts) > 1 else request_id
        TURN_STICKINESS_CACHE[session_key] = (provider, model, time.time())

C) In prepare_route(), AFTER the force_provider block and BEFORE the 
   select_model() call, add:
        # Per-turn stickiness: if this session recently selected a model, reuse it
        sticky = get_turn_sticky_model(request_id)
        if sticky and not force_provider:
            sp, sm = sticky
            prov = PROVIDERS.get(sp)
            if prov and prov.api_type == 'ollama':
                fetch_ollama_models(prov)
            if prov and provider_endpoint_reachable(prov):
                logger.info(f"[{request_id}] Turn stickiness: reusing {sp}/{sm} for session")
                chain = [(sp, sm)]
                LAST_ROUTE_DEBUG.update({'updated_at': int(time.time()), 'request_id': request_id, 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'requirements': requirements, 'estimatedTokens': estimated_tokens, 'json': want_json, 'chain': chain, 'scores': [{'provider': sp, 'model': sm, 'score': 100, 'reason': 'turn_stickiness'}], 'rejections': [], 'selected': None, 'attempts': [], 'streaming': streaming_mode or ('buffered-wrapper' if requirements.get('streaming') else 'disabled'), 'status': 'routing', 'error': None, 'totalElapsedMs': None, 'turnStickiness': True})
                return normalized_messages, intent, complexity, estimated_tokens, chain
            else:
                logger.info(f"[{request_id}] Turn stickiness: {sp}/{sm} not reachable, falling back to normal routing")

D) In route_request(), after successful model selection (the `if ok:` block),
   add:
        if ok:
            set_turn_sticky_model(request_id, pn, model)
            # ... rest of existing ok handling

E) In handle_openai_chat_completions(), after successful model selection (the 
   `if ok and result` block), add the same:
        set_turn_sticky_model(request_id, pn, model)

This ensures that within a single agent turn (identified by request_id session 
prefix), all API calls consistently use the same provider and model.
"""
PASS
