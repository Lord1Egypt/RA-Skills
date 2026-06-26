from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json

from apify_client import ApifyClient
from redis import Redis
from redis.exceptions import RedisError

from .config import Settings
from .contextual_grounding import GroundingSnippet, ground_query


PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
PRIORITY_EMOJI = {"P0": "🔴", "P1": "🟠", "P2": "🟡", "P3": "🟢"}


@dataclass(slots=True)
class IncidentRecord:
    incident_id: str
    source: str
    title: str
    severity: str
    service: str
    status: str
    description: str
    started_at: datetime
    region: str | None = None
    url: str | None = None
    raw: dict[str, object] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "IncidentRecord":
        title = str(payload.get("title") or payload.get("name") or "Untitled incident")
        started_at = payload.get("started_at") or payload.get("timestamp") or datetime.now(
            timezone.utc
        ).isoformat()
        return cls(
            incident_id=str(
                payload.get("incident_id")
                or payload.get("id")
                or _stable_id(title, str(started_at))
            ),
            source=str(payload.get("source") or "unknown"),
            title=title,
            severity=str(payload.get("severity") or _infer_severity(title)),
            service=str(payload.get("service") or _infer_service(title)),
            status=str(payload.get("status") or "active"),
            description=str(
                payload.get("description") or payload.get("summary") or payload.get("body") or ""
            ),
            started_at=datetime.fromisoformat(str(started_at)),
            region=str(payload["region"]) if payload.get("region") else None,
            url=str(payload["url"]) if payload.get("url") else None,
            raw=dict(payload),
        )

    def fingerprint(self) -> str:
        digest = sha256(
            f"{self.source}:{self.title}:{self.started_at.isoformat()}".encode("utf-8")
        ).hexdigest()
        return digest

    def to_dict(self) -> dict[str, object]:
        return {
            "incident_id": self.incident_id,
            "source": self.source,
            "title": self.title,
            "severity": self.severity,
            "service": self.service,
            "status": self.status,
            "description": self.description,
            "started_at": self.started_at.isoformat(),
            "region": self.region,
            "url": self.url,
            "raw": self.raw,
        }


@dataclass(slots=True)
class IncidentTriage:
    incident: IncidentRecord
    priority: str
    summary: str
    recommended_actions: list[str]
    grounding: list[GroundingSnippet] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "incident": self.incident.to_dict(),
            "priority": self.priority,
            "summary": self.summary,
            "recommended_actions": self.recommended_actions,
            "grounding": [
                {
                    "source": item.source,
                    "excerpt": item.excerpt,
                    "score": item.score,
                    "url": item.url,
                }
                for item in self.grounding
            ],
        }


@dataclass(slots=True)
class KubeWatchReport:
    generated_at: datetime
    source: str
    overview: str
    deduped_count: int
    triaged_incidents: list[IncidentTriage]

    def to_dict(self) -> dict[str, object]:
        return {
            "generated_at": self.generated_at.isoformat(),
            "source": self.source,
            "overview": self.overview,
            "deduped_count": self.deduped_count,
            "triaged_incidents": [item.to_dict() for item in self.triaged_incidents],
        }

    def to_markdown(self) -> str:
        lines = [
            "# Situation Monitor / KubeWatch Report",
            "",
            f"_Generated: {self.generated_at.isoformat()}_",
            "",
            f"**Overview**: {self.overview}",
            "",
            f"**Duplicates skipped**: {self.deduped_count}",
            "",
            "## Incidents",
            "",
        ]
        if not self.triaged_incidents:
            lines.append("- No incidents found")
            lines.append("")
            return "\n".join(lines)

        for item in self.triaged_incidents:
            emoji = PRIORITY_EMOJI[item.priority]
            lines.append(
                f"- {emoji} `{item.priority}` `{item.incident.service}` from `{item.incident.source}`: {item.incident.title}"
            )
            lines.append(f"  Summary: {item.summary}")
            if item.recommended_actions:
                lines.append(
                    f"  Actions: {'; '.join(item.recommended_actions)}"
                )
            if item.grounding:
                sources = " | ".join(
                    f"{note.source}: {note.excerpt[:120].strip()}"
                    for note in item.grounding
                )
                lines.append(f"  Grounding: {sources}")
            if item.incident.url:
                lines.append(f"  Link: {item.incident.url}")
        lines.append("")
        return "\n".join(lines)


class KubeWatchStore:
    def __init__(self, settings: Settings) -> None:
        self.redis_url = settings.redis_url
        self.path = settings.kubewatch_state_path
        self.client = Redis.from_url(settings.redis_url, decode_responses=True) if settings.redis_url else None
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record_incident(self, incident: IncidentRecord) -> bool:
        fingerprint = incident.fingerprint()
        if self.client:
            try:
                created = self.client.set(
                    f"kubewatch:incidents:{fingerprint}",
                    incident.incident_id,
                    ex=86400,
                    nx=True,
                )
                if created:
                    self.client.lpush("kubewatch:history", json.dumps(incident.to_dict()))
                    self.client.ltrim("kubewatch:history", 0, 99)
                return bool(created)
            except RedisError:
                self.client = None

        payload = self._read()
        seen = payload.setdefault("seen", {})
        if fingerprint in seen:
            return False
        seen[fingerprint] = incident.incident_id
        history = payload.setdefault("history", [])
        history.insert(0, incident.to_dict())
        payload["history"] = history[:100]
        self._write(payload)
        return True

    def save_latest_report(self, report: KubeWatchReport) -> None:
        if self.client:
            try:
                self.client.set("kubewatch:latest_report", json.dumps(report.to_dict()))
                return
            except RedisError:
                self.client = None
        payload = self._read()
        payload["latest_report"] = report.to_dict()
        self._write(payload)

    def load_history(self, limit: int = 5) -> list[IncidentRecord]:
        if self.client:
            try:
                items = self.client.lrange("kubewatch:history", 0, max(limit - 1, 0))
                return [IncidentRecord.from_dict(json.loads(item)) for item in items]
            except RedisError:
                self.client = None
        payload = self._read()
        items = payload.get("history", [])[:limit]
        return [IncidentRecord.from_dict(item) for item in items]

    def _read(self) -> dict[str, object]:
        if not self.path.exists():
            return {"seen": {}, "history": []}
        return json.loads(self.path.read_text())

    def _write(self, payload: dict[str, object]) -> None:
        self.path.write_text(json.dumps(payload, indent=2))


def load_kubewatch_fixture(path: Path) -> list[IncidentRecord]:
    payload = json.loads(path.read_text())
    return [IncidentRecord.from_dict(item) for item in payload]


def fetch_apify_incidents(
    settings: Settings,
    actor_id: str | None = None,
    actor_input_path: Path | None = None,
) -> list[IncidentRecord]:
    if not settings.apify_token:
        raise ValueError("APIFY_TOKEN is required for kubewatch-apify.")

    resolved_actor_id = actor_id or settings.apify_actor_id
    if not resolved_actor_id:
        raise ValueError("Provide --actor-id or set APIFY_ACTOR_ID.")

    run_input: dict[str, object] = {}
    if actor_input_path:
        run_input = json.loads(actor_input_path.read_text())

    client = ApifyClient(settings.apify_token)
    run = client.actor(resolved_actor_id).call(run_input=run_input)
    dataset_id = run.get("defaultDatasetId")
    if not dataset_id:
        return []
    items = client.dataset(dataset_id).list_items().items
    return [IncidentRecord.from_dict(_normalize_apify_item(item)) for item in items]


def build_kubewatch_report(
    incidents: list[IncidentRecord], settings: Settings, source: str
) -> KubeWatchReport:
    store = KubeWatchStore(settings)
    triaged = [triage_incident(incident, settings) for incident in incidents]
    triaged.sort(key=lambda item: PRIORITY_ORDER[item.priority])

    deduped = 0
    for incident in incidents:
        created = store.record_incident(incident)
        if not created:
            deduped += 1

    report = KubeWatchReport(
        generated_at=datetime.now(timezone.utc),
        source=source,
        overview=_overview(triaged),
        deduped_count=deduped,
        triaged_incidents=triaged,
    )
    store.save_latest_report(report)
    return report


def load_kubewatch_history(settings: Settings, limit: int = 5) -> list[IncidentRecord]:
    return KubeWatchStore(settings).load_history(limit=limit)


def triage_incident(incident: IncidentRecord, settings: Settings) -> IncidentTriage:
    grounding = ground_query(
        f"{incident.title}\n{incident.description}\nservice: {incident.service}",
        settings,
    )
    priority = _priority_for(incident)
    actions = _actions_for(incident, grounding)
    summary = _summary_for(incident, grounding)
    return IncidentTriage(
        incident=incident,
        priority=priority,
        summary=summary,
        recommended_actions=actions,
        grounding=grounding,
    )


def _priority_for(incident: IncidentRecord) -> str:
    severity = incident.severity.lower()
    text = f"{incident.title} {incident.description}".lower()
    if severity in {"critical", "sev0", "p0"} or "checkout" in text or "payment" in text:
        return "P0"
    if severity in {"high", "sev1", "p1"} or "imagepullbackoff" in text or "crashloopbackoff" in text:
        return "P1"
    if severity in {"medium", "sev2", "p2"}:
        return "P2"
    return "P3"


def _actions_for(
    incident: IncidentRecord, grounding: list[GroundingSnippet]
) -> list[str]:
    text = f"{incident.title} {incident.description}".lower()
    actions: list[str] = []
    if any(term in text for term in {"oomkilled", "memory", "crashloopbackoff", "oom"}):
        actions.extend(
            [
                "Describe the failing pod and confirm OOMKilled or restart events.",
                "Freeze deploys for the service and roll back to the last healthy revision.",
                "Compare memory requests and limits against actual usage before re-deploying.",
            ]
        )
    elif any(term in text for term in {"imagepullbackoff", "errimagepull", "image tag"}):
        actions.extend(
            [
                "Confirm the broken image tag and check whether old replicas are still healthy.",
                "Run rollout undo or patch the deployment to a known-good image tag.",
                "Pause merges for the affected service until the registry reference is corrected.",
            ]
        )
    else:
        actions.extend(
            [
                "Confirm blast radius and affected service ownership.",
                "Check the most recent rollout and warning events before taking action.",
            ]
        )

    for note in grounding:
        if note.source not in {"Contextual retrieval"}:
            actions.append(f"Grounded by {note.source}.")
            break
    return actions[:4]


def _summary_for(
    incident: IncidentRecord, grounding: list[GroundingSnippet]
) -> str:
    base = (
        f"{incident.service} is affected by {incident.title.lower()} with status "
        f"`{incident.status}` in {incident.region or 'the target region'}."
    )
    if grounding:
        return f"{base} The recommended path is grounded on {grounding[0].source}."
    return base


def _overview(triaged: list[IncidentTriage]) -> str:
    if not triaged:
        return "No Kubernetes incidents were found."
    counts = {priority: 0 for priority in PRIORITY_ORDER}
    for item in triaged:
        counts[item.priority] += 1
    return (
        f"{counts['P0']} P0, {counts['P1']} P1, {counts['P2']} P2, and {counts['P3']} P3 "
        f"incident(s) across {len(triaged)} active record(s)."
    )


def _normalize_apify_item(item: dict[str, object]) -> dict[str, object]:
    title = (
        item.get("title")
        or item.get("name")
        or item.get("headline")
        or item.get("incident_title")
        or "Untitled incident"
    )
    description = (
        item.get("description")
        or item.get("summary")
        or item.get("body")
        or item.get("text")
        or ""
    )
    started_at = (
        item.get("started_at")
        or item.get("timestamp")
        or item.get("publishedAt")
        or item.get("createdAt")
        or datetime.now(timezone.utc).isoformat()
    )
    return {
        "incident_id": item.get("id") or _stable_id(str(title), str(started_at)),
        "source": item.get("source") or item.get("provider") or "apify",
        "title": title,
        "severity": item.get("severity") or _infer_severity(str(title)),
        "service": item.get("service") or _infer_service(f"{title} {description}"),
        "status": item.get("status") or item.get("state") or "active",
        "description": description,
        "started_at": started_at,
        "region": item.get("region") or item.get("location"),
        "url": item.get("url") or item.get("link") or item.get("pageUrl"),
        "raw": item,
    }


def _infer_severity(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in {"critical", "p0", "sev0"}):
        return "critical"
    if any(term in lowered for term in {"high", "p1", "sev1"}):
        return "high"
    if any(term in lowered for term in {"medium", "p2", "sev2"}):
        return "medium"
    return "low"


def _infer_service(text: str) -> str:
    lowered = text.lower()
    for service in ("payment-processor", "user-service", "analytics-worker", "gke", "eks"):
        if service in lowered:
            return service
    return "unknown-service"


def _stable_id(title: str, started_at: str) -> str:
    return sha256(f"{title}:{started_at}".encode("utf-8")).hexdigest()[:12]
