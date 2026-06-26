from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import quote   # FIX (security): URL-encode grounding search queries
import logging
import asyncio
import random
import requests
import re
import time
import sqlite3

logger = logging.getLogger("openclaw.cost")


class CostCapException(Exception):
    pass


# Pricing is per 1M tokens (input / output) unless noted otherwise.
# Update these when provider pricing changes.
PRICING = {
    "gemini-2.5-flash":         {"input": 0.075,  "output": 0.30},
    "gemini-2.5-pro":           {"input": 1.25,   "output": 10.00},
    "gpt-4o-mini":              {"input": 0.150,  "output": 0.60},
    "gpt-4o":                   {"input": 2.50,   "output": 10.00},
    "claude-3-5-haiku-latest":  {"input": 0.25,   "output": 1.25},
    "claude-3-5-sonnet-latest": {"input": 3.00,   "output": 15.00},
    "grounding":                {"per_call": 35.00 / 1000},
}


@dataclass
class LLMSession:
    config: dict
    db_conn: object
    run_id: str
    _session_input_tokens:  int   = field(default=0,   init=False)
    _session_output_tokens: int   = field(default=0,   init=False)
    _session_cost_usd:      float = field(default=0.0, init=False)
    _call_count:            int   = field(default=0,   init=False)

    def __post_init__(self):
        self.provider = self.config.get("LLM_PROVIDER", "gemini").lower()
        self.clients = {}

        if self.provider == "openai":
            from openai import AsyncOpenAI
            self.clients["openai"] = AsyncOpenAI(api_key=self.config["OPENAI_API_KEY"])

        elif self.provider == "anthropic":
            from anthropic import AsyncAnthropic
            self.clients["anthropic"] = AsyncAnthropic(api_key=self.config["ANTHROPIC_API_KEY"])

        else:  # Default: Gemini
            import google.generativeai as genai
            genai.configure(api_key=self.config["GEMINI_API_KEY"])
            self.clients["gemini"] = genai

    async def _check_cap(self, projected_call_cost: float = 0.0) -> None:
        """
        Pulls real-time sum directly from the database to prevent concurrent 
        workers from bypassing the cost cap due to stale memory references.
        """
        today = datetime.now(timezone.utc).date().isoformat()
        
        def _get_cap():
            max_retries = 10
            for attempt in range(max_retries):
                try:
                    return self.db_conn.execute(
                        "SELECT COALESCE(SUM(estimated_cost_usd), 0) FROM run_log "
                        "WHERE DATE(created_at) = ?",
                        (today,)
                    ).fetchone()
                except sqlite3.OperationalError as e:
                    if "locked" in str(e).lower() and attempt < max_retries - 1:
                        # Linear backoff with jitter to resolve SQLite contention
                        time.sleep(random.uniform(0.1, 0.5) + (attempt * 0.2))
                    else:
                        raise
            
        row = await asyncio.to_thread(_get_cap)
        
        current_day_total = float(row[0]) if row else 0.0
        cap = self.config.get("DAILY_COST_CAP_USD", 2.00)
        total = current_day_total + projected_call_cost
        
        if total >= cap:
            raise CostCapException(
                f"Daily cost cap ${cap:.2f} exceeded. Projected total: ${total:.4f}"
            )

    async def generate(
        self,
        prompt: str,
        model_type: str = "PRIMARY_MODEL",
        grounded: bool = False,
        is_json: bool = False
    ) -> str:
        raw_model = self.config.get(model_type, "gemini-2.5-flash")
        
        # --- Auto-Correct Model Mismatches ---
        # Prevents API crashes if the user switches LLM_PROVIDER but forgets to 
        # update the PRIMARY_MODEL/REASONING_MODEL strings in their config.
        model = raw_model
        if self.provider == "anthropic" and ("gemini" in raw_model or "gpt" in raw_model):
            model = "claude-3-5-haiku-latest" if model_type == "PRIMARY_MODEL" else "claude-3-5-sonnet-latest"
        elif self.provider == "openai" and ("gemini" in raw_model or "claude" in raw_model):
            model = "gpt-4o-mini" if model_type == "PRIMARY_MODEL" else "gpt-4o"
        elif self.provider == "gemini" and ("claude" in raw_model or "gpt" in raw_model):
            model = "gemini-2.5-flash" if model_type == "PRIMARY_MODEL" else "gemini-2.5-pro"

        # --- Grounding Fallback for Non-Gemini Models ---
        # Intercepts grounded requests for Claude/GPT and injects real-time Jina Search 
        # context to prevent aggressive URL hallucination.
        if grounded and self.provider != "gemini":
            try:
                # Attempt to extract the exact search query from the prompt template
                query_match = re.search(r"query:\s*'([^']+)'", prompt)
                search_query = query_match.group(1) if query_match else prompt[:100]
                
                headers = {"Accept": "application/json"}
                if self.config.get("JINA_API_KEY"):
                    headers["Authorization"] = f"Bearer {self.config.get('JINA_API_KEY')}"
                
                # FIX (security): URL-encode search_query before concatenation.
                # Without this, characters like '?', '/', '#', and spaces break the
                # HTTP path, causing the request to fail or route to the wrong endpoint.
                encoded_query = quote(search_query, safe="")

                logger.debug(f"Executing Jina Search fallback for grounding query: {search_query}")
                jina_resp = await asyncio.to_thread(
                    requests.get,
                    f"https://s.jina.ai/{encoded_query}",
                    headers=headers,
                    timeout=15
                )
                jina_resp.raise_for_status()
                data = jina_resp.json().get("data", [])
                
                if data:
                    search_context = "\n\n--- REAL-TIME SEARCH CONTEXT ---\n"
                    for item in data[:4]:  # Feed top 4 results into context window
                        search_context += f"URL: {item.get('url')}\nContent: {item.get('content', '')[:800]}\n\n"
                    
                    prompt += (
                        search_context + 
                        "CRITICAL INSTRUCTION: You MUST base your answer on the search context provided above. "
                        "You MUST explicitly include the real 'URL' values from this context as your reference links. "
                        "Do NOT hallucinate or make up URLs."
                    )
            except Exception as e:
                logger.warning(f"Jina Search fallback failed: {e}. LLM may hallucinate reference URLs.")

        pricing = PRICING.get(model, PRICING["gemini-2.5-flash"])
        est_cost = (
            ((len(prompt) / 4) / 1_000_000) * pricing["input"]
            + (1500 / 1_000_000) * pricing["output"]
        )
        await self._check_cap(projected_call_cost=est_cost)

        RETRYABLE_ERRORS = ["429", "503", "500", "502", "quota", "rate", "overloaded"]
        MAX_RETRIES = 3
        BASE_DELAY = 2.0

        last_exception = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                response_text = ""
                actual_input = int(len(prompt) / 4)
                actual_output = 1000

                if self.provider == "openai":
                    kwargs = {
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                    }
                    if is_json:
                        kwargs["response_format"] = {"type": "json_object"}

                    response = await self.clients["openai"].chat.completions.create(**kwargs)
                    response_text = response.choices[0].message.content
                    actual_input = response.usage.prompt_tokens
                    actual_output = response.usage.completion_tokens

                elif self.provider == "anthropic":
                    # Anthropic enforces JSON strictly through prompting (is_json flag is
                    # handled upstream by callers via _safe_json_loads in daily_worker.py).
                    response = await self.clients["anthropic"].messages.create(
                        model=model,
                        max_tokens=4000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    response_text = response.content[0].text
                    actual_input = response.usage.input_tokens
                    actual_output = response.usage.output_tokens

                else:  # Default to Gemini
                    gemini_model = self.clients["gemini"].GenerativeModel(model)
                    tools = (
                        [{"google_search_retrieval": {}}]
                        if grounded and self.provider == "gemini"
                        else None
                    )
                    gen_config = {"response_mime_type": "application/json"} if is_json else None

                    response = await gemini_model.generate_content_async(
                        prompt,
                        tools=tools,
                        generation_config=gen_config
                    )
                    response_text = response.text
                    if hasattr(response, "usage_metadata"):
                        actual_input = response.usage_metadata.prompt_token_count
                        actual_output = response.usage_metadata.candidates_token_count

                actual_cost = (
                    (actual_input  / 1_000_000) * pricing["input"]
                    + (actual_output / 1_000_000) * pricing["output"]
                )
                if grounded and self.provider == "gemini":
                    actual_cost += PRICING["grounding"]["per_call"]

                # Memory Aggregation Only (SQLite writes removed from this loop)
                self._session_input_tokens  += actual_input
                self._session_output_tokens += actual_output
                self._session_cost_usd      += actual_cost
                self._call_count            += 1

                logger.debug(
                    f"LLM Call [{model}]: {actual_input}in / {actual_output}out | ${actual_cost:.4f}"
                )
                return response_text

            except Exception as e:
                last_exception = e
                err_str = str(e).lower()
                is_retryable = any(err in err_str for err in RETRYABLE_ERRORS)

                if not is_retryable or attempt == MAX_RETRIES:
                    raise

                wait = (BASE_DELAY * (2 ** attempt)) + random.uniform(-0.2, 0.2)
                logger.warning(
                    f"API error (attempt {attempt + 1}/{MAX_RETRIES}): {e}. "
                    f"Retrying in {wait:.1f}s..."
                )
                await asyncio.sleep(wait)

        raise last_exception

    def finalize(self) -> dict:
        """
        Executes a single, aggregated write to SQLite at the end of the session
        to prevent database locks and write contention.
        """
        max_db_retries = 10
        for db_attempt in range(max_db_retries):
            try:
                self.db_conn.execute("""
                    INSERT INTO run_log (run_id, estimated_cost_usd, llm_calls)
                    VALUES (?, ?, ?)
                    ON CONFLICT(run_id) DO UPDATE SET
                        estimated_cost_usd = estimated_cost_usd + excluded.estimated_cost_usd,
                        llm_calls = llm_calls + excluded.llm_calls
                """, (self.run_id, self._session_cost_usd, self._call_count))
                self.db_conn.commit()
                break
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and db_attempt < max_db_retries - 1:
                    # Linear backoff with jitter to resolve SQLite contention
                    time.sleep(random.uniform(0.1, 0.5) + (db_attempt * 0.2))
                else:
                    raise

        return {
            "llm_calls":         self._call_count,
            "input_tokens":      self._session_input_tokens,
            "output_tokens":     self._session_output_tokens,
            "estimated_cost_usd": round(self._session_cost_usd, 6),
        }
