from typing import Optional


AGENT_PROFILE_POLICY = {
    "study": {"academic", "workflow"},
    "teacher": {"academic", "workflow"},
    "product": {"product", "workflow", "integration"},
    "pm": {"product", "workflow", "integration"},
    "dev": {"script", "integration", "workflow", "product"},
    "developer": {"script", "integration", "workflow", "product"},
    "pr": {"product", "workflow", "integration"},
    "gongguan": {"product", "workflow", "integration"},
    "money": {"script", "integration", "workflow"},
    "finance": {"script", "integration", "workflow"},
}


def agent_authorization(agent_name: Optional[str], profile: str) -> dict:
    if not agent_name:
        return {"required": False, "allowed": True, "reason": "no agent policy requested"}

    normalized = agent_name.lower().replace("agent", "").replace("bot", "").replace("-", "").strip()
    allowed_profiles = set()
    for key, profiles in AGENT_PROFILE_POLICY.items():
        if key in normalized:
            allowed_profiles = profiles
            break

    if not allowed_profiles:
        return {
            "required": True,
            "allowed": False,
            "agent": agent_name,
            "profile": profile,
            "reason": "unknown agent policy",
        }

    return {
        "required": True,
        "allowed": profile in allowed_profiles,
        "agent": agent_name,
        "profile": profile,
        "allowed_profiles": sorted(allowed_profiles),
        "reason": "profile allowed" if profile in allowed_profiles else "profile blocked for agent",
    }
