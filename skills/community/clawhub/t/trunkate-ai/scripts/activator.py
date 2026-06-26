#!/usr/bin/env python3
import os
import sys
import re
import uuid

# Correcting the path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from trunkate import optimize_prompt

def _filter_sensitive_content(text: str):
    """
    Extracts sensitive content (System Prompts, .env blocks, and [KEEP] tags) 
    LOCALLY and replaces them with UUID placeholders to prevent data exfiltration.
    """
    protected = {}
    
    # 1. Protect [KEEP] blocks
    for match in re.finditer(r'\[KEEP\].*?\[/KEEP\]', text, flags=re.DOTALL | re.IGNORECASE):
        placeholder = f"__TRUNKATE_PROTECTED_{uuid.uuid4().hex}__"
        protected[placeholder] = match.group(0)
        
    # 2. Protect System Instructions (e.g. <system> tags)
    for match in re.finditer(r'<system>.*?</system>', text, flags=re.DOTALL | re.IGNORECASE):
        placeholder = f"__TRUNKATE_PROTECTED_{uuid.uuid4().hex}__"
        protected[placeholder] = match.group(0)
        
    # 3. Protect .env file blocks
    for pattern in [r'```(?:bash|sh|env)?\s*(?:#.*\.env|.*\.env.*)\n.*?```', r'```env\n.*?```']:
        for match in re.finditer(pattern, text, flags=re.DOTALL | re.IGNORECASE):
            placeholder = f"__TRUNKATE_PROTECTED_{uuid.uuid4().hex}__"
            protected[placeholder] = match.group(0)
            
    # 4. Protect common secrets (API keys, passwords, bearer tokens)
    secret_patterns = [
        r'(?i)(?:password|secret|api[_-]?key|token|access[_-]?key|auth[_-]?token|credentials?)\s*[:=]\s*["\']?[a-zA-Z0-9_\-.~]+["\']?',
        r'Bearer\s+[a-zA-Z0-9\-_.]+'
    ]
    for pattern in secret_patterns:
        for match in re.finditer(pattern, text):
            placeholder = f"__TRUNKATE_PROTECTED_{uuid.uuid4().hex}__"
            protected[placeholder] = match.group(0)
            
    filtered_text = text
    for placeholder, original in protected.items():
        if original in filtered_text:
            filtered_text = filtered_text.replace(original, placeholder)
            
    return filtered_text, protected

def _restore_sensitive_content(text: str, protected: dict) -> str:
    """Restores the original protected content back into the optimized text."""
    restored = text
    for placeholder, original in protected.items():
        restored = restored.replace(placeholder, original)
    return restored

def run():
    """
    Evaluates context threshold and triggers semantic pruning via Trunkate API.
    Emits the OPENCLAW_ACTION to update agent memory state.
    """
    # 1. Retrieve OpenClaw environment variables
    try:
        current_tokens = int(os.environ.get("OPENCLAW_CURRENT_TOKENS", 0))
        token_limit = int(os.environ.get("OPENCLAW_TOKEN_LIMIT", 128000))
        history_path = os.environ.get("OPENCLAW_HISTORY_PATH")
    except ValueError:
        print("Trunkate Alert: Malformed token environment variables.", file=sys.stderr)
        return

    # 2. Configuration: Proactive "Smart Buffer"
    # Default to 20% of the current history to maintain extreme density.
    target_budget = os.environ.get("TRUNKATE_AUTO_BUDGET", "20%")
    
    # Proactive Principle: We systematically optimize every call to ensure 
    # the agent's memory is always lean and cost-effective.
    if not history_path or not os.path.exists(history_path):
        return

    try:
        # 3. Read session history with safety check
        file_size = os.path.getsize(history_path)
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            print(f"Trunkate Alert: History file too large ({file_size} bytes). Skipping optimization.", file=sys.stderr)
            return

        with open(history_path, "r") as f:
            history = f.read()
            
        # 4. Filter Sensitive Content LOCALLY before external transmission
        filtered_history, protected_blocks = _filter_sensitive_content(history)

        # 5. Invoke Semantic Pruner with safe, filtered text
        optimized_filtered = optimize_prompt(filtered_history, budget=target_budget)
        
        # 6. Restore Sensitive Content 
        optimized = _restore_sensitive_content(optimized_filtered, protected_blocks)
        
        # 7. Emit state update directive
        if optimized and optimized != history:
            print(f"OPENCLAW_ACTION:SET_HISTORY={optimized}")
            # Log success to stderr to keep stdout clean for action parsing
            print(f"Trunkate: Proactive optimization complete. Target: {target_budget}. Protected {len(protected_blocks)} blocks.", file=sys.stderr)
        
    except Exception as e:
        print(f"Trunkate Error: Failed to activate optimization: {e}", file=sys.stderr)

if __name__ == "__main__":
    run()