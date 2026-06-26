from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import shutil
import subprocess

from .config import Settings
from .kubewatch import IncidentRecord


POD_FAILURE_REASONS = {"CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull"}
TERMINATION_REASONS = {"OOMKilled"}


def fetch_cluster_incidents(
    settings: Settings, namespace: str | None = None
) -> list[IncidentRecord]:
    kubeconfig = settings.resolved_kubeconfig
    if kubeconfig is None or not kubeconfig.exists():
        raise ValueError(
            "No kubeconfig found. Set KUBECONFIG or create .local/kubeconfig."
        )

    target_namespace = namespace or settings.kube_namespace
    pods = _kubectl_json(
        kubeconfig,
        ["get", "pods", "-n", target_namespace, "-o", "json"],
    )
    events = _kubectl_json(
        kubeconfig,
        ["get", "events", "-n", target_namespace, "-o", "json"],
    )
    return detect_incidents_from_cluster(
        pods,
        events,
        namespace=target_namespace,
    )


def detect_incidents_from_cluster(
    pods_payload: dict[str, object],
    events_payload: dict[str, object],
    namespace: str,
) -> list[IncidentRecord]:
    incidents: dict[tuple[str, str], IncidentRecord] = {}
    event_index = _index_events(events_payload)

    for pod in pods_payload.get("items", []):
        metadata = pod.get("metadata", {})
        status = pod.get("status", {})
        pod_name = metadata.get("name", "unknown-pod")
        service = _service_name(metadata)
        created_at = metadata.get("creationTimestamp") or datetime.now(
            timezone.utc
        ).isoformat()

        for container_status in status.get("containerStatuses", []):
            waiting = (container_status.get("state") or {}).get("waiting")
            terminated = (container_status.get("lastState") or {}).get("terminated")
            reason = None
            description = None
            severity = "medium"

            if terminated and terminated.get("reason") in TERMINATION_REASONS:
                reason = terminated.get("reason")
                description = terminated.get("message") or ""
                severity = "critical"
            elif waiting and waiting.get("reason") in POD_FAILURE_REASONS:
                reason = waiting.get("reason")
                description = waiting.get("message") or ""
                severity = "high" if reason == "ImagePullBackOff" else "critical"

            if not reason:
                continue

            related_events = event_index.get(pod_name, [])
            details = [description] if description else []
            details.extend(related_events[:2])
            text = " ".join(part.strip() for part in details if part.strip())
            title = _title_for(reason, service)
            incident = IncidentRecord(
                incident_id=_incident_id(service, reason, created_at),
                source="k8s-cluster",
                title=title,
                severity=severity,
                service=service,
                status="active",
                description=text or f"{service} is failing with {reason} in {namespace}.",
                started_at=datetime.fromisoformat(created_at.replace("Z", "+00:00")),
                region=namespace,
                url=None,
                raw={
                    "pod": pod_name,
                    "reason": reason,
                    "namespace": namespace,
                },
            )
            incidents[(service, reason)] = incident

    return sorted(
        incidents.values(),
        key=lambda item: item.started_at,
        reverse=True,
    )


def _kubectl_json(kubeconfig: Path, args: list[str]) -> dict[str, object]:
    env = os.environ.copy()
    env["KUBECONFIG"] = str(kubeconfig)
    kubectl_bin = _resolve_kubectl_bin()
    completed = subprocess.run(
        [kubectl_bin, *args],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return json.loads(completed.stdout)


def _resolve_kubectl_bin() -> str:
    local = Path(".local/bin/kubectl")
    if local.exists():
        return str(local)
    resolved = shutil.which("kubectl")
    if resolved:
        return resolved
    raise FileNotFoundError(
        "kubectl not found. Install it or place a local binary at .local/bin/kubectl."
    )


def _index_events(events_payload: dict[str, object]) -> dict[str, list[str]]:
    event_index: dict[str, list[str]] = defaultdict(list)
    for item in events_payload.get("items", []):
        involved = item.get("involvedObject", {})
        pod_name = involved.get("name")
        if not pod_name:
            continue
        reason = item.get("reason", "")
        message = item.get("message", "")
        if reason or message:
            event_index[pod_name].append(f"{reason}: {message}".strip(": "))
    return event_index


def _service_name(metadata: dict[str, object]) -> str:
    labels = metadata.get("labels", {})
    return (
        labels.get("app")
        or labels.get("k8s-app")
        or metadata.get("generateName")
        or metadata.get("name")
        or "unknown-service"
    )


def _title_for(reason: str, service: str) -> str:
    if reason == "OOMKilled":
        return f"{service} pods restarting with OOMKilled"
    if reason == "ImagePullBackOff":
        return f"{service} rollout stuck with ImagePullBackOff"
    return f"{service} pods failing with {reason}"


def _incident_id(service: str, reason: str, created_at: str) -> str:
    safe = f"{service}-{reason}-{created_at}"
    return safe.replace(":", "-").replace(".", "-").replace("+", "-")
