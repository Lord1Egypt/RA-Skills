"""
Argus API escalation for OpenClaw.
Submits blocked packages to Argus for full analysis.
"""

import json
import urllib.request


def submit_packages(packages: list[tuple[str, dict]], api_url: str, api_key: str) -> list[str]:
    """
    Submit a list of (name, meta) tuples to the Argus scan API.
    Returns a list of job IDs for confirmed submissions.
    """
    job_ids = []
    for name, meta in packages:
        ecosystem = meta.get("ecosystem", "unknown")
        # Build a minimal JSON payload describing the package
        payload = json.dumps({
            "source": "openclaw",
            "package_name": name,
            "ecosystem": ecosystem,
            "age_days": meta.get("age_days"),
            "similar_to": meta.get("similar_to"),
            "has_install_script": meta.get("has_install_script"),
        }).encode()

        req = urllib.request.Request(
            f"{api_url.rstrip('/')}/api/scan",
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "openclaw/0.1",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read())
                job_id = result.get("id") or result.get("job_id")
                if job_id:
                    job_ids.append(str(job_id))
        except Exception:
            pass  # Argus submission is best-effort; don't let it break the block

    return job_ids
