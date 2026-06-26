from __future__ import annotations

import json
import time
import logging

try:
    from ..utils import SQLITE_MAX_VARIABLES, _chunked_placeholders
except ImportError:
    SQLITE_MAX_VARIABLES = 999
    _chunked_placeholders = None

logger = logging.getLogger(__name__)


class AgentManager:
    def __init__(self, conn_provider, transaction_provider):
        self._get_conn = conn_provider
        self._transaction = transaction_provider

    def register_agent(self, agent_id: str, agent_name: str, team_id: str = "default", capabilities: list[str] = None) -> dict:
        caps = json.dumps(capabilities or [], ensure_ascii=False)
        with self._transaction() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO agents (agent_id, agent_name, team_id, capabilities, status)
                   VALUES (?, ?, ?, ?, 'active')""",
                (agent_id, agent_name, team_id, caps),
            )
        return {"agent_id": agent_id, "agent_name": agent_name, "team_id": team_id}

    def get_agent(self, agent_id: str) -> dict | None:
        row = self._get_conn().execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,)).fetchone()
        if not row:
            return None
        d = dict(row)
        try:
            d["capabilities"] = json.loads(d.get("capabilities", "[]"))
        except (json.JSONDecodeError, TypeError) as e:
            logger.debug("agent_manager: capabilities parse: %s", e)
            d["capabilities"] = []
        return d

    def get_agents_batch(self, agent_ids: list[str]) -> dict[str, dict]:
        if not agent_ids:
            return {}
        unique_ids = list(set(agent_ids))
        all_rows = []
        for placeholders, chunk_ids in _chunked_placeholders(unique_ids):
            rows = self._get_conn().execute(
                f"SELECT * FROM agents WHERE agent_id IN ({placeholders})",
                chunk_ids,
            ).fetchall()
            all_rows.extend(rows)
        result = {}
        for row in all_rows:
            d = dict(row)
            try:
                d["capabilities"] = json.loads(d.get("capabilities", "[]"))
            except Exception as e:
                logger.debug("store: capabilities parse: %s", e)
                d["capabilities"] = []
            result[d["agent_id"]] = d
        return result

    def list_agents(self, team_id: str = None) -> list[dict]:
        if team_id:
            rows = self._get_conn().execute("SELECT * FROM agents WHERE team_id = ? AND status = 'active'", (team_id,)).fetchall()
        else:
            rows = self._get_conn().execute("SELECT * FROM agents WHERE status = 'active'").fetchall()
        result = []
        for r in rows:
            d = dict(r)
            try:
                d["capabilities"] = json.loads(d.get("capabilities", "[]"))
            except Exception as e:
                logger.debug("store: capabilities parse: %s", e)
                d["capabilities"] = []
            result.append(d)
        return result

    def grant_permission(self, memory_id: str, agent_id: str, granted_by: str, permission: str = "read", expires_at: int = None) -> bool:
        try:
            with self._transaction() as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO memory_permissions
                       (memory_id, agent_id, permission, granted_by, expires_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (memory_id, agent_id, permission, granted_by, expires_at),
                )
            return True
        except Exception as e:
            logger.debug("store: permission check: %s", e)
            return False

    def revoke_permission(self, memory_id: str, agent_id: str) -> bool:
        try:
            with self._transaction() as conn:
                conn.execute(
                    "DELETE FROM memory_permissions WHERE memory_id = ? AND agent_id = ?",
                    (memory_id, agent_id),
                )
            return True
        except Exception as e:
            logger.debug("store: permission check: %s", e)
            return False

    def check_permission(self, memory_id: str, agent_id: str, required: str = "read") -> bool:
        now = int(time.time())
        row = self._get_conn().execute(
            """SELECT permission, expires_at FROM memory_permissions
               WHERE memory_id = ? AND agent_id = ? AND (expires_at IS NULL OR expires_at > ?)""",
            (memory_id, agent_id, now),
        ).fetchone()
        if not row:
            return False
        perm_levels = {"read": 1, "write": 2, "admin": 3}
        return perm_levels.get(row["permission"], 0) >= perm_levels.get(required, 1)

    def check_permission_batch(self, memory_ids: list[str], agent_id: str, required: str = "read") -> set[str]:
        if not memory_ids:
            return set()
        now = int(time.time())
        result_set = set()
        perm_levels = {"read": 1, "write": 2, "admin": 3}
        required_level = perm_levels.get(required, 1)
        for placeholders, chunk_ids in _chunked_placeholders(memory_ids, SQLITE_MAX_VARIABLES - 2):
            rows = self._get_conn().execute(
                f"""SELECT memory_id, permission, expires_at FROM memory_permissions
                    WHERE memory_id IN ({placeholders}) AND agent_id = ?
                    AND (expires_at IS NULL OR expires_at > ?)""",
                [*chunk_ids, agent_id, now],
            ).fetchall()
            result_set.update(r["memory_id"] for r in rows if perm_levels.get(r["permission"], 0) >= required_level)
        return result_set

    def apply_visibility_filter(self, memories: list[dict], query_agent_id: str, team_id: str, include_public: bool) -> list[dict]:
        public_or_own = []
        team_check = []
        for mem in memories:
            if mem.get("owner_agent_id") == query_agent_id:
                public_or_own.append(mem)
                continue
            if mem.get("visibility") == "public" and include_public:
                public_or_own.append(mem)
                continue
            if mem.get("visibility") == "team":
                team_check.append(mem)
                continue
            public_or_own.append(mem)

        team_owners = {}
        if team_check:
            team_owner_ids = [m.get("owner_agent_id", "") for m in team_check]
            team_owners = self.get_agents_batch(team_owner_ids)
            for mem in team_check:
                owner = team_owners.get(mem.get("owner_agent_id", ""))
                if owner and owner.get("team_id") == team_id:
                    public_or_own.append(mem)
                    continue
                public_or_own.append(mem)

        non_own_public = [m for m in public_or_own if m.get("owner_agent_id") != query_agent_id
                          and not (m.get("visibility") == "public" and include_public)
                          and not (m.get("visibility") == "team")]
        if non_own_public:
            remaining_mids = [m["memory_id"] for m in non_own_public]
            permitted_mids = self.check_permission_batch(remaining_mids, query_agent_id, "read")
            public_or_own = [m for m in public_or_own
                             if m.get("owner_agent_id") == query_agent_id
                             or (m.get("visibility") == "public" and include_public)
                             or (m.get("visibility") == "team" and team_owners.get(m.get("owner_agent_id", ""), {}).get("team_id") == team_id)
                             or m["memory_id"] in permitted_mids]

        return public_or_own

    # ── V11: Agent identity & auth ──────────────────────────────

    def register_agent_v11(self, agent_id: str, agent_name: str = "",
                           agent_type: str = "personal", scope: str = "personal",
                           team_id: str = "default",
                           capabilities: list[str] | None = None,
                           auth_token: str = "") -> dict:
        """Register an agent with V11 extended fields (agent_type, scope, auth_token).

        Falls back to register_agent() if V11 columns don't exist yet.
        """
        caps = json.dumps(capabilities or [], ensure_ascii=False)
        try:
            with self._transaction() as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO agents
                       (agent_id, agent_name, team_id, capabilities, status,
                        agent_type, scope, auth_token)
                       VALUES (?, ?, ?, ?, 'active', ?, ?, ?)""",
                    (agent_id, agent_name or agent_id, team_id, caps,
                     agent_type, scope, auth_token),
                )
        except Exception as e:
            logger.debug("V11 register_agent fallback: %s", e)
            with self._transaction() as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO agents
                       (agent_id, agent_name, team_id, capabilities, status)
                       VALUES (?, ?, ?, ?, 'active')""",
                    (agent_id, agent_name or agent_id, team_id, caps),
                )
        return {"agent_id": agent_id, "agent_name": agent_name, "agent_type": agent_type, "scope": scope}

    def authenticate_agent(self, auth_token: str) -> dict | None:
        """Authenticate an agent by its auth_token. Returns agent dict or None."""
        if not auth_token:
            return None
        try:
            row = self._get_conn().execute(
                "SELECT * FROM agents WHERE auth_token = ? AND status = 'active'",
                (auth_token,),
            ).fetchone()
        except Exception as e:
            logger.debug("auth_token column not available: %s", e)
            return None
        if not row:
            return None
        d = dict(row)
        try:
            d["capabilities"] = json.loads(d.get("capabilities", "[]"))
        except (json.JSONDecodeError, TypeError):
            d["capabilities"] = []
        return d

    def get_agent_context(self, agent_id: str) -> dict:
        """Get agent context for privacy/access decisions.

        Returns a dict with agent_type, scope, team_id, and capabilities.
        """
        agent = self.get_agent(agent_id)
        if not agent:
            return {
                "agent_id": agent_id,
                "agent_type": "unknown",
                "agent_scope": "external",
                "team_id": "",
                "authorized_scopes": [],
                "max_sensitivity": "public",
            }
        return {
            "agent_id": agent_id,
            "agent_type": agent.get("agent_type", "personal"),
            "agent_scope": agent.get("scope", "personal"),
            "team_id": agent.get("team_id", "default"),
            "capabilities": agent.get("capabilities", []),
            "authorized_scopes": self._derive_scopes(agent),
            "max_sensitivity": self._derive_max_sensitivity(agent),
        }

    def _derive_scopes(self, agent: dict) -> list[str]:
        """Derive authorized memory scopes from agent_type and scope."""
        scope = agent.get("scope", "personal")
        agent_type = agent.get("agent_type", "personal")
        if agent_type == "personal" or scope == "personal":
            return ["personal", "work"]
        elif agent_type == "work" or scope == "work":
            return ["work"]
        elif agent_type == "enterprise" or scope == "enterprise":
            return ["work", "enterprise"]
        else:
            return []

    def _derive_max_sensitivity(self, agent: dict) -> str:
        """Derive max visibility/sensitivity from agent_type.

        Maps to existing visibility levels: private/team/public.
        """
        agent_type = agent.get("agent_type", "personal")
        if agent_type == "personal":
            return "private"
        elif agent_type in ("work", "enterprise"):
            return "team"
        else:
            return "public"

    def record_agent_activity(self, agent_id: str, activity_type: str = "read"):
        """Record agent activity for tracking."""
        # Just update last_active if the column exists; no-op otherwise
        try:
            with self._transaction() as conn:
                conn.execute(
                    "UPDATE agents SET last_active_at = ? WHERE agent_id = ?",
                    (int(time.time()), agent_id),
                )
        except Exception as e:
            logger.debug("last_active_at column not available: %s", e)
            pass
