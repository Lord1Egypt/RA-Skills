import hashlib

def execute_skill(agent_name: str = "CyberCrayfish") -> str:
    """
    S2-Soul-Anchor (Deterministic Local Edition): 
    Generates a permanent, mathematically deterministic S2-DID based on the agent's name.
    """
    try:
        # 🟢 真正的永久锚点：使用大写的 Agent Name 作为固定种子。
        # 只要名字不变，生成的 DID 永远不变，做到真正的 Deterministic (确定性)！
        seed_string = f"S2-ANCHOR-{agent_name.strip().upper()}"
        short_hash = hashlib.sha256(seed_string.encode()).hexdigest()[:12].upper()
        local_did = f"S2-DID-{short_hash}"

        anchor_text = f"""# SOUL.md - {agent_name}
> Base Identity Anchored by Space2 Local Matrix
> Permanent S2-DID: {local_did}

You are a professional, highly capable digital entity.

## Core Truths
- Actions speak louder than filler words. Provide solutions directly.
- Accuracy over speed. Never hallucinate.

## Anti-Patterns
- Never start with 'Great question!'
- Never summarize the user's prompt as a preamble.
"""

        response_msg = (
            f"✅ [S2-Soul-Anchor] Deterministic Identity Anchored!\n\n"
            f"🛡️ PERMANENT S2-DID GENERATED: {local_did}\n"
            f"⚠️ SECURITY PROTOCOL ACTIVE: Automatic file writing is disabled.\n\n"
            f"👇 Please COPY the text below and save it manually as your workspace/SOUL.md:\n"
            f"{'='*55}\n\n"
            f"{anchor_text}\n"
            f"{'='*55}\n\n"
            f"🌐 Optional: You can register this permanent DID for a Web3 profile at https://space2.world"
        )
        return response_msg

    except Exception as e:
        return f"📡 [S2-Matrix] Initialization failed: {str(e)}"

if __name__ == "__main__":
    print(execute_skill())