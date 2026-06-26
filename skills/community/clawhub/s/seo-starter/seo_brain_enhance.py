"""
Brain Enhancement: seo-audit-pro

Enriches SEO audits with brand positioning and strategy from the brain.
"""

import sys
from pathlib import Path

brain_path = Path("/data/.openclaw/workspace/company-brain")
if str(brain_path) not in sys.path:
    sys.path.insert(0, str(brain_path))

try:
    from brain_wrapper import Brain
    _brain = Brain()
except Exception:
    _brain = None


def get_seo_context(target_url: str = None) -> dict:
    """Query brain for SEO-relevant positioning."""
    if _brain is None:
        return {"enhanced": False, "context": ""}

    try:
        result = _brain.query("SEO strategy and keyword approach")
        if result.get("confidence", 0) > 0.2:
            return {
                "enhanced": True,
                "context": result.get("answer", ""),
                "confidence": result.get("confidence", 0),
            }
    except Exception:
        pass

    return {"enhanced": False, "context": ""}


def enhance_seo_prompt(legacy_prompt: str, target_url: str = None) -> str:
    """Inject brain context into SEO audit prompt."""
    result = get_seo_context(target_url)
    if result["enhanced"]:
        return f"Brand SEO Context:\n{result['context']}\n\n---\n\n{legacy_prompt}"
    return legacy_prompt
