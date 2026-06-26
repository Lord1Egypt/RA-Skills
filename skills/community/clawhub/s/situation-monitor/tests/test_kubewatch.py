from pathlib import Path

from monitoring_the_situation.config import Settings
from monitoring_the_situation.kubewatch import (
    IncidentRecord,
    build_kubewatch_report,
    load_kubewatch_fixture,
    triage_incident,
)


def test_kubewatch_fixture_prioritizes_payment_processor() -> None:
    settings = Settings.from_env()
    incidents = load_kubewatch_fixture(Path("examples/kubewatch_incidents.json"))
    report = build_kubewatch_report(
        incidents, settings=settings, source="kubewatch:test"
    )

    top_item = report.triaged_incidents[0]
    assert top_item.incident.service == "payment-processor"
    assert top_item.priority == "P0"


def test_kubewatch_fixture_grounds_image_pull_incident() -> None:
    settings = Settings.from_env()
    incidents = load_kubewatch_fixture(Path("examples/kubewatch_incidents.json"))
    report = build_kubewatch_report(
        incidents, settings=settings, source="kubewatch:test"
    )

    user_service = next(
        item for item in report.triaged_incidents if item.incident.service == "user-service"
    )
    grounding_sources = [note.source for note in user_service.grounding]
    assert "bad-image-deploy.md" in grounding_sources


def test_cluster_network_incident_grounds_network_runbook() -> None:
    settings = Settings(
        mode="fixture",
        state_path=Path(".local/test_state.json"),
        redis_url=None,
        friendli_token=None,
        friendli_base_url="https://api.friendli.ai/serverless/v1",
        friendli_model="meta-llama-3.3-70b-instruct",
        apify_token=None,
        apify_actor_id=None,
        contextual_api_key=None,
        contextual_agent_id=None,
        contextual_base_url="https://api.contextual.ai",
        kubeconfig=None,
        kube_namespace="production",
        discord_bot_token=None,
        discord_guild_id=None,
        discord_channel_ids=(),
        discord_message_limit=75,
        civic_enabled=False,
    )
    incident = IncidentRecord.from_dict(
        {
            "source": "gcp-status",
            "title": "cluster-network incident: Multiple GCP products are experiencing Service issues.",
            "severity": "high",
            "service": "cluster-network",
            "status": "resolved",
            "description": "Regional packet loss and control-plane network degradation in us-east1.",
            "started_at": "2026-03-25T10:00:00+00:00",
            "region": "us-east1",
        }
    )

    triage = triage_incident(incident, settings)

    grounding_sources = [note.source for note in triage.grounding]
    assert "cluster-network-degradation.md" in grounding_sources
