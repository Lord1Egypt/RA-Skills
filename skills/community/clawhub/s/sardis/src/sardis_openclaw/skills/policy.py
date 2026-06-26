"""Policy update skill."""
from __future__ import annotations

from typing import Any

import httpx

from sardis_openclaw.base import OpenClawSkill, SkillContext, SkillResult


class PolicyUpdateSkill(OpenClawSkill):
    """Set or update spending policy for an agent wallet using natural language."""

    @property
    def name(self) -> str:
        return "policy_update"

    @property
    def description(self) -> str:
        return "Set or update spending policy for an agent wallet using natural language"

    @property
    def parameters(self) -> list[str]:
        return ["agent_id", "policy_rules"]

    @property
    def required_permissions(self) -> list[str]:
        return ["policy:write"]

    async def execute(self, params: dict[str, Any], context: SkillContext) -> SkillResult:
        err = self.validate_params(params)
        if err:
            return SkillResult(success=False, error=err)

        agent_id = params["agent_id"]
        policy_rules = params["policy_rules"]

        # policy_rules can be a natural language string or a structured dict
        payload: dict[str, Any] = {"agent_id": agent_id}
        if isinstance(policy_rules, str):
            payload["natural_language"] = policy_rules
        else:
            payload["policy_rules"] = policy_rules

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{context.base_url}/policies/apply",
                headers={"Authorization": f"Bearer {context.api_key}"},
                json=payload,
                timeout=30.0,
            )
            if resp.status_code not in (200, 201):
                return SkillResult(success=False, error=f"API error: {resp.status_code} {resp.text}")
            return SkillResult(success=True, data=resp.json())
