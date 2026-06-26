#!/usr/bin/env python3
"""
Telnyx AI Missions API client using only Python standard library.
Usage: python telnyx_api.py <command> [args...]
"""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = "https://api.telnyx.com/v2"
STATE_FILE = Path(".missions_state.json")


def get_api_key():
    """Get API key from environment."""
    key = os.environ.get("TELNYX_API_KEY")
    if not key:
        print("ERROR: TELNYX_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return key


def api_request(method: str, endpoint: str, data: dict = None) -> dict:
    """Make an API request to Telnyx."""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            response_body = response.read().decode("utf-8")
            if response_body:
                return json.loads(response_body)
            return {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        if error_body:
            try:
                error_json = json.loads(error_body)
                print(f"Details: {json.dumps(error_json, indent=2)}", file=sys.stderr)
            except json.JSONDecodeError:
                print(f"Details: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def slugify(name: str) -> str:
    """Convert name to URL-safe slug."""
    import re

    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def load_state() -> dict:
    """Load state from file."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict):
    """Save state to file."""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_mission_state(slug: str) -> dict:
    """Get state for a specific mission."""
    state = load_state()
    return state.get(slug, {})


def update_mission_state(slug: str, updates: dict):
    """Update state for a specific mission."""
    state = load_state()
    if slug not in state:
        state[slug] = {}
    state[slug].update(updates)
    save_state(state)


def remove_mission_state(slug: str):
    """Remove a mission from state."""
    state = load_state()
    if slug in state:
        del state[slug]
        save_state(state)


def save_memory(slug: str, key: str, value):
    """Save a piece of memory/data to the mission state."""
    state = load_state()
    if slug not in state:
        state[slug] = {}
    if "memory" not in state[slug]:
        state[slug]["memory"] = {}
    state[slug]["memory"][key] = value
    state[slug]["last_updated"] = (
        datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )
    save_state(state)
    print(f"Saved memory '{key}' for mission '{slug}'")


def get_memory(slug: str, key: str = None):
    """Get memory from mission state. If key is None, returns all memory."""
    state = get_mission_state(slug)
    memory = state.get("memory", {})
    if key:
        return memory.get(key)
    return memory


def append_memory(slug: str, key: str, item):
    """Append an item to a list in memory. Creates list if doesn't exist."""
    state = load_state()
    if slug not in state:
        state[slug] = {}
    if "memory" not in state[slug]:
        state[slug]["memory"] = {}
    if key not in state[slug]["memory"]:
        state[slug]["memory"][key] = []
    if not isinstance(state[slug]["memory"][key], list):
        state[slug]["memory"][key] = [state[slug]["memory"][key]]
    state[slug]["memory"][key].append(item)
    state[slug]["last_updated"] = (
        datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )
    save_state(state)
    print(
        f"Appended to memory '{key}' for mission '{slug}' (now {len(state[slug]['memory'][key])} items)"
    )


# ============================================================================
# MISSIONS API
# ============================================================================


def create_mission(name: str, instructions: str) -> str:
    """Create a new mission. Returns mission_id."""
    result = api_request(
        "POST", "/ai/missions", {"name": name, "instructions": instructions}
    )
    mission_id = result["data"]["mission_id"]
    print(f"Created mission: {mission_id}")
    return mission_id


def get_mission(mission_id: str) -> dict:
    """Get mission details."""
    result = api_request("GET", f"/ai/missions/{mission_id}")
    print(json.dumps(result["data"], indent=2))
    return result["data"]


def list_missions(page_size: int = 20) -> list:
    """List all missions."""
    result = api_request("GET", f"/ai/missions?page[size]={page_size}")
    missions = result.get("data", [])
    for m in missions:
        print(f"{m['mission_id']}: {m['name']}")
    return missions


# ============================================================================
# RUNS API
# ============================================================================


def create_run(mission_id: str, input_data: dict) -> str:
    """Create a new run. Returns run_id."""
    result = api_request(
        "POST", f"/ai/missions/{mission_id}/runs", {"input": input_data}
    )
    run_id = result["data"]["run_id"]
    print(f"Created run: {run_id}")
    return run_id


def get_run(mission_id: str, run_id: str) -> dict:
    """Get run details."""
    result = api_request("GET", f"/ai/missions/{mission_id}/runs/{run_id}")
    print(json.dumps(result["data"], indent=2))
    return result["data"]


def update_run(
    mission_id: str,
    run_id: str,
    status: str = None,
    result_summary: str = None,
    result_payload: dict = None,
) -> dict:
    """Update a run's status or results."""
    data = {}
    if status:
        data["status"] = status
    if result_summary:
        data["result_summary"] = result_summary
    if result_payload:
        data["result_payload"] = result_payload

    result = api_request("PATCH", f"/ai/missions/{mission_id}/runs/{run_id}", data)
    print(f"Updated run {run_id}: {status or 'updated'}")
    return result.get("data", {})


def list_runs(mission_id: str) -> list:
    """List runs for a mission."""
    result = api_request("GET", f"/ai/missions/{mission_id}/runs")
    runs = result.get("data", [])
    for r in runs:
        print(f"{r['run_id']}: {r['status']}")
    return runs


# ============================================================================
# PLAN API
# ============================================================================


def create_plan(mission_id: str, run_id: str, steps: list) -> dict:
    """Create a plan with steps."""
    result = api_request(
        "POST", f"/ai/missions/{mission_id}/runs/{run_id}/plan", {"steps": steps}
    )
    print(f"Created plan with {len(steps)} steps")
    return result.get("data", {})


def get_plan(mission_id: str, run_id: str) -> dict:
    """Get the plan for a run."""
    result = api_request("GET", f"/ai/missions/{mission_id}/runs/{run_id}/plan")
    print(json.dumps(result.get("data", {}), indent=2))
    return result.get("data", {})


def update_plan_step(mission_id: str, run_id: str, step_id: str, status: str) -> dict:
    """Update a plan step's status. Valid statuses: pending, in_progress, completed, skipped, failed."""
    result = api_request(
        "PATCH",
        f"/ai/missions/{mission_id}/runs/{run_id}/plan/steps/{step_id}",
        {"status": status},
    )
    print(f"Updated step '{step_id}': {status}")
    return result.get("data", {})


# ============================================================================
# EVENTS API
# ============================================================================


def log_event(
    mission_id: str,
    run_id: str,
    event_type: str,
    summary: str,
    agent_id: str = "claude-code",
    step_id: str = None,
    payload: dict = None,
) -> dict:
    """Log an event to the run."""
    data = {
        "type": event_type,
        "summary": summary,
    }
    if agent_id:
        data["agent_id"] = agent_id
    if step_id:
        data["step_id"] = step_id
    if payload:
        data["payload"] = payload

    result = api_request(
        "POST", f"/ai/missions/{mission_id}/runs/{run_id}/events", data
    )
    print(f"Logged event: {summary}")
    return result.get("data", {})


def list_events(mission_id: str, run_id: str) -> list:
    """List events for a run."""
    result = api_request("GET", f"/ai/missions/{mission_id}/runs/{run_id}/events")
    events = result.get("data", [])
    for e in events:
        print(f"[{e.get('type')}] {e.get('summary')}")
    return events


# ============================================================================
# ASSISTANTS API
# ============================================================================


def create_assistant(
    name: str,
    instructions: str,
    greeting: str,
    features: list = None,
    model: str = "openai/gpt-4o",
    tools: list = None,
    voice: str = "Minimax.speech-2.6-turbo.English_Upbeat_Woman",
    voice_settings: dict = None,
    transcription: dict = None,
    telephony_settings: dict = None,
    messaging_settings: dict = None,
    description: str = None,
    llm_api_key_ref: str = None,
    insight_settings: dict = None,
    privacy_settings: dict = None,
    dynamic_variables_webhook_url: str = None,
    dynamic_variables: dict = None,
    widget_settings: dict = None,
) -> str:
    """Create an AI assistant. Returns assistant_id.

    Tools can include any combination of:
      - {"type": "hangup", "hangup": {"description": "..."}}
      - {"type": "webhook", "webhook": {"name": "...", "description": "...", "url": "...", ...}}
      - {"type": "transfer", "transfer": {"targets": [{"name": "...", "to": "..."}], "from": "...", ...}}
      - {"type": "handoff", "handoff": {"ai_assistants": [{"name": "...", "id": "..."}], ...}}
      - {"type": "retrieval", "retrieval": {"bucket_ids": ["..."], ...}}
      - {"type": "refer", "refer": {"targets": [{"name": "...", "sip_address": "..."}], ...}}
      - {"type": "send_dtmf", "send_dtmf": {}}
      - {"type": "send_message", "send_message": {}}

    If tools is None, defaults to a hangup tool.
    """
    if tools is None:
        tools = [
            {
                "type": "hangup",
                "hangup": {
                    "description": "To be used whenever the conversation has ended and it would be appropriate to hangup the call."
                },
            },
            {
                "type": "send_dtmf",
                "send_dtmf": {},
            },
        ]

    data = {
        "name": name,
        "model": model,
        "instructions": instructions,
        "greeting": greeting,
        "tools": tools,
        "voice_settings": voice_settings or {"voice": voice},
        "transcription": transcription or {
            "model": "deepgram/flux",
            "settings": {
                "eot_threshold": 0.7,
                "eager_eot_threshold": 0.7,
            },
        },
        "telephony_settings": telephony_settings or {
            "noise_suppression": "disabled",
        },
    }
    if features:
        data["enabled_features"] = features
    if description:
        data["description"] = description
    if llm_api_key_ref:
        data["llm_api_key_ref"] = llm_api_key_ref
    if messaging_settings:
        data["messaging_settings"] = messaging_settings
    if insight_settings:
        data["insight_settings"] = insight_settings
    if privacy_settings:
        data["privacy_settings"] = privacy_settings
    if dynamic_variables_webhook_url:
        data["dynamic_variables_webhook_url"] = dynamic_variables_webhook_url
    if dynamic_variables:
        data["dynamic_variables"] = dynamic_variables
    if widget_settings:
        data["widget_settings"] = widget_settings

    result = api_request("POST", "/ai/assistants", data)
    assistant_id = result["id"]
    print(f"Created assistant: {assistant_id}")
    return assistant_id


def list_assistants(
    page_size: int = 25, page_number: int = 1, name_filter: str = None
) -> list:
    """List assistants with optional name filter and pagination.

    Args:
        name_filter: Filter assistants by name (substring match).
        page_number: Page number (1-indexed).
        page_size: Results per page.
    """
    params = f"page[size]={page_size}&page[number]={page_number}"
    if name_filter:
        params += f"&filter[name]={urllib.parse.quote(name_filter)}"

    result = api_request("GET", f"/ai/assistants?{params}")
    assistants = result.get("data", [])

    meta = result.get("meta", {})
    total = meta.get("total_results") or meta.get("total") or len(assistants)
    total_pages = meta.get("total_pages", 1)

    for a in assistants:
        aid = a.get("id") or a.get("assistant_id")
        name = a.get("name", "unnamed")
        model = a.get("model", "")
        features = a.get("enabled_features", [])
        print(f"{aid}: {name} (model={model}, features={features})")

    print(f"\nPage {page_number}/{total_pages} ({total} total)", file=sys.stderr)
    return assistants


def get_assistant(assistant_id: str) -> dict:
    """Get assistant details."""
    result = api_request("GET", f"/ai/assistants/{assistant_id}")
    print(json.dumps(result, indent=2))
    return result


def update_assistant(assistant_id: str, updates: dict) -> dict:
    """Update an assistant. Accepts any fields from create_assistant."""
    result = api_request("POST", f"/ai/assistants/{assistant_id}", updates)
    print(f"Updated assistant {assistant_id}")
    return result


def get_assistant_connection_id(assistant_id: str, feature: str = "telephony") -> str:
    """Get the connection ID for an assistant (texml_app_id or messaging_profile_id)."""
    result = api_request("GET", f"/ai/assistants/{assistant_id}")

    if feature == "telephony":
        conn_id = result.get("telephony_settings", {}).get("default_texml_app_id")
    else:
        conn_id = result.get("messaging_settings", {}).get(
            "default_messaging_profile_id"
        )

    if conn_id:
        print(f"Connection ID: {conn_id}")
    else:
        print(f"No connection ID found for {feature}", file=sys.stderr)
    return conn_id


# ============================================================================
# PHONE NUMBERS API
# ============================================================================


def list_phone_numbers(available_only: bool = False) -> list:
    """List phone numbers. If available_only, show only unassigned ones."""
    result = api_request("GET", "/phone_numbers?page[size]=100")
    numbers = result.get("data", [])

    if available_only:
        numbers = [n for n in numbers if not n.get("connection_id")]

    for n in numbers:
        status = "available" if not n.get("connection_id") else "assigned"
        print(f"{n['id']}: {n['phone_number']} [{status}]")

    return numbers


def get_available_phone_number(prefer_hd_voice: bool = True) -> tuple:
    """Get first available phone number. Returns (id, phone_number) or (None, None).

    When prefer_hd_voice is True, prioritizes numbers that support HD voice,
    but falls back to non-HD numbers if none are available.
    """
    result = api_request("GET", "/phone_numbers?page[size]=100")
    numbers = result.get("data", [])

    available = [n for n in numbers if not n.get("connection_id")]

    if not available:
        print("ERROR: No available phone numbers found", file=sys.stderr)
        print("Purchase numbers at https://portal.telnyx.com", file=sys.stderr)
        return None, None

    if prefer_hd_voice:
        # Try HD-capable numbers first
        hd_numbers = [n for n in available if n.get("hd_voice_enabled")]
        if hd_numbers:
            chosen = hd_numbers[0]
            print(f"Found available (HD voice): {chosen['phone_number']}")
            return chosen["id"], chosen["phone_number"]
        print("No HD voice numbers available, falling back to standard", file=sys.stderr)

    chosen = available[0]
    print(f"Found available: {chosen['phone_number']}")
    return chosen["id"], chosen["phone_number"]


def assign_phone_number(
    phone_number_id: str,
    connection_id: str,
    connection_type: str = "voice",
    hd_voice: bool = True,
) -> dict:
    """Assign a phone number to a connection.

    Args:
        hd_voice: If True, attempt to enable HD voice on the number.
            Not all number types support HD voice, so failures are non-fatal.
    """
    if connection_type == "voice":
        data = {"connection_id": connection_id}
    else:
        data = {"messaging_profile_id": connection_id}

    if hd_voice and connection_type == "voice":
        data["hd_voice_enabled"] = True

    try:
        result = api_request("PATCH", f"/phone_numbers/{phone_number_id}", data)
        print(f"Assigned phone number {phone_number_id}")
        return result.get("data", {})
    except SystemExit:
        if hd_voice:
            # Retry without HD voice — not available for all number types
            print("HD voice not available for this number, retrying without it...", file=sys.stderr)
            if "hd_voice_enabled" in data:
                del data["hd_voice_enabled"]
            result = api_request("PATCH", f"/phone_numbers/{phone_number_id}", data)
            print(f"Assigned phone number {phone_number_id} (without HD voice)")
            return result.get("data", {})
        raise


# ============================================================================
# SCHEDULED EVENTS API
# ============================================================================


def schedule_call(
    assistant_id: str,
    end_user_phone: str,
    agent_phone: str,
    scheduled_time: str,
    mission_id: str,
    mission_run_id: str,
    mission_step_id: str = None,
    dynamic_variables: dict = None,
) -> str:
    """Schedule a phone call. Returns scheduled_event_id."""
    metadata = {
        "mission_id": mission_id,
        "mission_run_id": mission_run_id,
    }
    if mission_step_id:
        metadata["mission_step_id"] = mission_step_id
    data = {
        "telnyx_conversation_channel": "phone_call",
        "telnyx_end_user_target": end_user_phone,
        "telnyx_agent_target": agent_phone,
        "scheduled_at_fixed_datetime": scheduled_time,
        "conversation_metadata": metadata,
    }
    if dynamic_variables:
        data["dynamic_variables"] = dynamic_variables

    result = api_request(
        "POST", f"/ai/assistants/{assistant_id}/scheduled_events", data
    )
    event_id = result["scheduled_event_id"]
    print(f"Scheduled call: {event_id}")
    return event_id


def schedule_sms(
    assistant_id: str,
    end_user_phone: str,
    agent_phone: str,
    scheduled_time: str,
    text: str,
    mission_id: str = None,
    mission_run_id: str = None,
    mission_step_id: str = None,
    dynamic_variables: dict = None,
) -> str:
    """Schedule an SMS. Returns scheduled_event_id."""
    metadata = {}
    if mission_id:
        metadata["mission_id"] = mission_id
    if mission_run_id:
        metadata["mission_run_id"] = mission_run_id
    if mission_step_id:
        metadata["mission_step_id"] = mission_step_id
    data = {
        "telnyx_conversation_channel": "sms_chat",
        "telnyx_end_user_target": end_user_phone,
        "telnyx_agent_target": agent_phone,
        "scheduled_at_fixed_datetime": scheduled_time,
        "text": text,
    }
    if metadata:
        data["conversation_metadata"] = metadata
    if dynamic_variables:
        data["dynamic_variables"] = dynamic_variables

    result = api_request(
        "POST", f"/ai/assistants/{assistant_id}/scheduled_events", data
    )
    event_id = result["scheduled_event_id"]
    print(f"Scheduled SMS: {event_id}")
    return event_id


def get_scheduled_event(assistant_id: str, event_id: str) -> dict:
    """Get scheduled event status including call_status for phone calls."""
    result = api_request(
        "GET", f"/ai/assistants/{assistant_id}/scheduled_events/{event_id}"
    )
    status = result.get("status", "unknown")
    call_status = result.get("call_status")
    conv_id = result.get("conversation_id")
    retry_count = result.get("retry_count", 0)
    parts = [f"Status: {status}"]
    if call_status:
        parts.append(f"call_status: {call_status}")
    if conv_id:
        parts.append(f"conversation_id: {conv_id}")
    if retry_count > 0:
        parts.append(f"retry_count: {retry_count}")
    print(", ".join(parts))
    return result


def delete_scheduled_event(assistant_id: str, event_id: str):
    """Delete a scheduled event."""
    api_request(
        "DELETE", f"/ai/assistants/{assistant_id}/scheduled_events/{event_id}"
    )
    print(f"Deleted scheduled event: {event_id}")


def list_scheduled_events(assistant_id: str) -> list:
    """List scheduled events for an assistant."""
    result = api_request("GET", f"/ai/assistants/{assistant_id}/scheduled_events")
    events = result.get("data", [])
    for e in events:
        parts = [f"{e.get('scheduled_event_id')}: {e.get('status')}"]
        call_status = e.get("call_status")
        if call_status:
            parts.append(f"call_status={call_status}")
        print(", ".join(parts))
    return events


# ============================================================================
# MISSION RUN AGENTS API (Linking Telnyx agents to mission runs)
# ============================================================================


def link_telnyx_agent(mission_id: str, run_id: str, telnyx_agent_id: str) -> dict:
    """Link a Telnyx agent (assistant) to a mission run."""
    data = {"telnyx_agent_id": telnyx_agent_id}
    result = api_request(
        "POST", f"/ai/missions/{mission_id}/runs/{run_id}/telnyx-agents", data
    )
    print(f"Linked agent {telnyx_agent_id} to run {run_id}")
    return result.get("data", {})


def list_linked_agents(mission_id: str, run_id: str) -> list:
    """List Telnyx agents linked to a mission run."""
    result = api_request(
        "GET", f"/ai/missions/{mission_id}/runs/{run_id}/telnyx-agents"
    )
    agents = result.get("data", [])
    for a in agents:
        print(f"Agent: {a.get('telnyx_agent_id')}")
    return agents


def unlink_telnyx_agent(mission_id: str, run_id: str, telnyx_agent_id: str):
    """Unlink a Telnyx agent from a mission run."""
    api_request(
        "DELETE",
        f"/ai/missions/{mission_id}/runs/{run_id}/telnyx-agents/{telnyx_agent_id}",
    )
    print(f"Unlinked agent {telnyx_agent_id} from run {run_id}")


# ============================================================================
# CONVERSATION INSIGHTS API
# ============================================================================


def rename_conversation(conversation_id: str, name: str) -> dict:
    """Rename a conversation. Useful for labeling calls with meaningful names."""
    result = api_request(
        "PUT", f"/ai/conversations/{conversation_id}", {"name": name}
    )
    print(f"Renamed conversation {conversation_id}: {name}")
    return result.get("data", {})


def get_conversation_insights(conversation_id: str) -> list:
    """Get insights from a conversation."""
    result = api_request(
        "GET", f"/ai/conversations/{conversation_id}/conversations-insights"
    )
    insights = result.get("data", [])

    for insight in insights:
        if insight.get("status") == "completed":
            for ci in insight.get("conversation_insights", []):
                print(f"Insight: {ci.get('result')}")

    return insights


# ============================================================================
# INSIGHTS MANAGEMENT API
# ============================================================================


def create_insight(
    name: str,
    instructions: str,
    json_schema: dict = None,
    webhook: str = None,
) -> str:
    """Create an insight template. Returns insight_id.

    For structured insights, pass a json_schema defining the expected output format.
    Example json_schema:
        {
            "type": "object",
            "properties": {
                "high_temp_f": {"type": "number", "description": "Today's high temperature in Fahrenheit"},
                "snow_mentioned": {"type": "boolean", "description": "Whether snow was mentioned"},
                "snow_chance_pct": {"type": "number", "description": "Snow probability percentage if mentioned"}
            },
            "required": ["high_temp_f", "snow_mentioned"]
        }
    """
    data = {"name": name, "instructions": instructions}
    if json_schema is not None:
        data["json_schema"] = json_schema
    if webhook:
        data["webhook"] = webhook

    result = api_request("POST", "/ai/conversations/insights", data)
    insight_data = result.get("data", result)
    insight_id = insight_data.get("insight_id") or insight_data.get("id")
    print(f"Created insight: {insight_id}")
    return insight_id


def get_insight(insight_id: str) -> dict:
    """Get an insight template."""
    result = api_request("GET", f"/ai/conversations/insights/{insight_id}")
    data = result.get("data", result)
    print(json.dumps(data, indent=2))
    return data


def list_insights(page_size: int = 25, page_number: int = 1) -> list:
    """List all insight templates with pagination."""
    result = api_request(
        "GET",
        f"/ai/conversations/insights?page[size]={page_size}&page[number]={page_number}",
    )
    insights = result.get("data", [])
    for i in insights:
        iid = i.get("insight_id") or i.get("id")
        has_schema = "structured" if i.get("json_schema") else "unstructured"
        print(f"{iid}: {i.get('name')} ({has_schema})")
    return insights


def update_insight(
    insight_id: str,
    name: str = None,
    instructions: str = None,
    json_schema: dict = None,
    webhook: str = None,
) -> dict:
    """Update an insight template."""
    data = {}
    if name:
        data["name"] = name
    if instructions:
        data["instructions"] = instructions
    if json_schema is not None:
        data["json_schema"] = json_schema
    if webhook is not None:
        data["webhook"] = webhook

    result = api_request("PUT", f"/ai/conversations/insights/{insight_id}", data)
    print(f"Updated insight {insight_id}")
    return result.get("data", result)


# ============================================================================
# INSIGHT GROUPS API
# ============================================================================


def create_insight_group(
    name: str,
    description: str = None,
    webhook: str = None,
) -> str:
    """Create an insight group. Returns group_id."""
    data = {"name": name}
    if description:
        data["description"] = description
    if webhook:
        data["webhook"] = webhook

    result = api_request("POST", "/ai/conversations/insight-groups", data)
    group_data = result.get("data", result)
    group_id = group_data.get("group_id") or group_data.get("id")
    print(f"Created insight group: {group_id}")
    return group_id


def get_insight_group(group_id: str) -> dict:
    """Get an insight group."""
    result = api_request("GET", f"/ai/conversations/insight-groups/{group_id}")
    data = result.get("data", result)
    print(json.dumps(data, indent=2))
    return data


def list_insight_groups(page_size: int = 25, page_number: int = 1) -> list:
    """List all insight groups with pagination."""
    result = api_request(
        "GET",
        f"/ai/conversations/insight-groups?page[size]={page_size}&page[number]={page_number}",
    )
    groups = result.get("data", [])
    for g in groups:
        gid = g.get("group_id") or g.get("id")
        insights_count = len(g.get("insights", []))
        print(f"{gid}: {g.get('name')} ({insights_count} insights)")
    return groups


def update_insight_group(
    group_id: str,
    name: str = None,
    description: str = None,
    webhook: str = None,
) -> dict:
    """Update an insight group."""
    data = {}
    if name:
        data["name"] = name
    if description:
        data["description"] = description
    if webhook is not None:
        data["webhook"] = webhook

    result = api_request("PUT", f"/ai/conversations/insight-groups/{group_id}", data)
    print(f"Updated insight group {group_id}")
    return result.get("data", result)


def assign_insight_to_group(group_id: str, insight_id: str) -> dict:
    """Assign an insight to a group."""
    result = api_request(
        "POST",
        f"/ai/conversations/insight-groups/{group_id}/insights/{insight_id}/assign",
    )
    print(f"Assigned insight {insight_id} to group {group_id}")
    return result.get("data", result)


def unassign_insight_from_group(group_id: str, insight_id: str):
    """Remove an insight from a group."""
    api_request(
        "DELETE",
        f"/ai/conversations/insight-groups/{group_id}/insights/{insight_id}/unassign",
    )
    print(f"Unassigned insight {insight_id} from group {group_id}")


# ============================================================================
# HIGH-LEVEL WORKFLOW FUNCTIONS
# ============================================================================


def init_mission(
    name: str, instructions: str, user_request: str, plan_steps: list = None
) -> tuple:
    """
    Initialize a mission with run and optional plan.
    Returns (mission_id, run_id).
    Resumes existing mission if found.
    """
    slug = slugify(name)
    existing = get_mission_state(slug)

    if existing.get("mission_id") and existing.get("run_id"):
        print(f"Resuming existing mission: {slug}")
        return existing["mission_id"], existing["run_id"]

    # Create new mission
    mission_id = create_mission(name, instructions)
    update_mission_state(
        slug,
        {
            "mission_name": name,
            "mission_id": mission_id,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        },
    )

    # Create run
    run_id = create_run(mission_id, {"original_request": user_request})
    update_mission_state(slug, {"run_id": run_id})

    # Create plan if provided
    if plan_steps:
        create_plan(mission_id, run_id, plan_steps)

    # Set running
    update_run(mission_id, run_id, status="running")

    return mission_id, run_id


def setup_voice_agent(
    mission_slug: str,
    name: str,
    instructions: str,
    greeting: str,
    tools: list = None,
    voice: str = None,
    voice_settings: dict = None,
    transcription: dict = None,
    telephony_settings: dict = None,
    model: str = "openai/gpt-4o",
) -> tuple:
    """
    Create voice assistant, assign phone number, and link to mission run.
    Returns (assistant_id, phone_number).

    Supports full assistant configuration including tools, voice, transcription,
    telephony_settings (voicemail detection, noise suppression, etc.).
    """
    existing = get_mission_state(mission_slug)

    if existing.get("assistant_id") and existing.get("agent_phone"):
        print(f"Using existing assistant: {existing['assistant_id']}")
        return existing["assistant_id"], existing["agent_phone"]

    # Build kwargs for create_assistant
    kwargs = {}
    if tools is not None:
        kwargs["tools"] = tools
    if voice is not None:
        kwargs["voice"] = voice
    if voice_settings is not None:
        kwargs["voice_settings"] = voice_settings
    if transcription is not None:
        kwargs["transcription"] = transcription
    if telephony_settings is not None:
        kwargs["telephony_settings"] = telephony_settings

    # Create assistant
    assistant_id = create_assistant(
        name, instructions, greeting, ["telephony"], model=model, **kwargs
    )
    update_mission_state(mission_slug, {"assistant_id": assistant_id})

    # Link agent to mission run if IDs are available
    mission_id = existing.get("mission_id")
    run_id = existing.get("run_id")
    if mission_id and run_id:
        link_telnyx_agent(mission_id, run_id, assistant_id)

    # Get available phone number
    phone_id, phone_number = get_available_phone_number()
    if not phone_id:
        return assistant_id, None

    # Get connection ID and assign
    connection_id = get_assistant_connection_id(assistant_id, "telephony")
    if connection_id:
        assign_phone_number(phone_id, connection_id, "voice")
        update_mission_state(
            mission_slug, {"agent_phone": phone_number, "phone_number_id": phone_id}
        )

    return assistant_id, phone_number


def complete_mission(
    mission_slug: str, mission_id: str, run_id: str, summary: str, payload: dict = None
):
    """Complete a mission and clean up state."""
    update_run(
        mission_id,
        run_id,
        status="succeeded",
        result_summary=summary,
        result_payload=payload,
    )
    remove_mission_state(mission_slug)
    print(f"Mission '{mission_slug}' completed successfully")


# ============================================================================
# CLI INTERFACE
# ============================================================================


def print_usage():
    """Print usage information."""
    print("""
Telnyx AI Missions API Client

Usage: python telnyx_api.py <command> [args...]

Commands:
  check-key                          Verify API key is set

  Missions:
    create-mission <name> <instructions>
    get-mission <mission_id>
    list-missions

  Runs:
    create-run <mission_id> <input_json>
    get-run <mission_id> <run_id>
    update-run <mission_id> <run_id> <status> [result_summary] [result_payload_json]
    list-runs <mission_id>

  Plan:
    create-plan <mission_id> <run_id> <steps_json>
    get-plan <mission_id> <run_id>
    update-step <mission_id> <run_id> <step_id> <status>
      status: pending, in_progress, completed, skipped, failed

  Events:
    log-event <mission_id> <run_id> <type> <summary> <step_id> [payload_json]
    list-events <mission_id> <run_id>

  Assistants:
    create-assistant <name> <instructions> <greeting> [options_json]
      options_json keys: features, model, tools, voice, voice_settings,
        transcription, telephony_settings (incl. voicemail_detection),
        messaging_settings, description, llm_api_key_ref, insight_settings,
        privacy_settings, dynamic_variables_webhook_url, dynamic_variables,
        widget_settings
      Defaults: voice=Minimax.speech-2.6-turbo.English_Upbeat_Woman,
        transcription=deepgram/flux (eot 0.7, eager_eot 0.7),
        tools=[hangup]
      Tool types: hangup, webhook, transfer, handoff, retrieval, refer,
        send_dtmf, send_message
    list-assistants [--name=<filter>] [--page=<n>] [--size=<n>]
    get-assistant <assistant_id>
    update-assistant <assistant_id> <updates_json>
    get-connection-id <assistant_id> [telephony|messaging]

  Phone Numbers:
    list-phones [--available]
    get-available-phone
    assign-phone <phone_id> <connection_id> [voice|sms]

  Scheduled Events:
    schedule-call <assistant_id> <to_phone> <from_phone> <datetime> <mission_id> <run_id> [step_id] [dynamic_variables_json]
    schedule-sms <assistant_id> <to_phone> <from_phone> <datetime> <text> [mission_id] [mission_run_id] [step_id] [dynamic_variables_json]
    get-event <assistant_id> <event_id>
    cancel-scheduled-event <assistant_id> <event_id>
    list-events-assistant <assistant_id>

  Insights (conversation results):
    get-insights <conversation_id>
    rename-conversation <conversation_id> <name>

  Insight Templates (CRUD):
    create-insight <name> <instructions> [options_json]
      options_json keys: json_schema (for structured), webhook
    get-insight <insight_id>
    list-insights
    update-insight <insight_id> <updates_json>
  Insight Groups:
    create-insight-group <name> [options_json]
      options_json keys: description, webhook
    get-insight-group <group_id>
    list-insight-groups
    update-insight-group <group_id> <updates_json>
    assign-insight <group_id> <insight_id>
    unassign-insight <group_id> <insight_id>

  Mission Run Agents (linking agents to runs):
    link-agent <mission_id> <run_id> <telnyx_agent_id>
    list-linked-agents <mission_id> <run_id>
    unlink-agent <mission_id> <run_id> <telnyx_agent_id>

  State:
    list-state                       List all missions in state file
    get-state <slug>                 Get state for a mission
    remove-state <slug>              Remove mission from state

  Memory (SAVE OFTEN!):
    save-memory <slug> <key> <value_json>   Save data to mission memory
    get-memory <slug> [key]                 Get memory (all or specific key)
    append-memory <slug> <key> <item_json>  Append item to a list in memory

  High-level:
    init <name> <instructions> <request> [steps_json]
    setup-agent <slug> <name> <instructions> <greeting>
    complete <slug> <mission_id> <run_id> <summary> [payload_json]

Examples:
  python telnyx_api.py create-mission "Find contractors" "Call and negotiate"
  python telnyx_api.py create-run mis_abc123 '{"request": "Find window washers"}'
  python telnyx_api.py schedule-call ast_xyz "+15551234567" "+15559876543" "2024-12-01T15:00:00Z" mis_abc run_def step_1
  python telnyx_api.py schedule-call ast_xyz "+15551234567" "+15559876543" "2024-12-01T15:00:00Z" mis_abc run_def step_1 '{"best_quote": "$350"}'
""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        # Basic
        if cmd == "check-key":
            key = get_api_key()
            print(f"API key configured: {key[:8]}...{key[-4:]}")

        # Missions
        elif cmd == "create-mission":
            create_mission(args[0], args[1])
        elif cmd == "get-mission":
            get_mission(args[0])
        elif cmd == "list-missions":
            list_missions()

        # Runs
        elif cmd == "create-run":
            create_run(args[0], json.loads(args[1]))
        elif cmd == "get-run":
            get_run(args[0], args[1])
        elif cmd == "update-run":
            # update-run <mission_id> <run_id> <status> [result_summary] [result_payload_json]
            result_summary = args[3] if len(args) > 3 else None
            result_payload = json.loads(args[4]) if len(args) > 4 else None
            update_run(args[0], args[1], status=args[2], result_summary=result_summary, result_payload=result_payload)
        elif cmd == "list-runs":
            list_runs(args[0])

        # Plan
        elif cmd == "create-plan":
            create_plan(args[0], args[1], json.loads(args[2]))
        elif cmd == "get-plan":
            get_plan(args[0], args[1])
        elif cmd == "update-step":
            update_plan_step(args[0], args[1], args[2], args[3])

        # Events
        elif cmd == "log-event":
            # log-event <mission_id> <run_id> <type> <summary> <step_id> [payload_json]
            # step_id is required - use "-" if event doesn't belong to a specific step
            if len(args) < 5:
                print("ERROR: log-event requires at least 5 arguments: <mission_id> <run_id> <type> <summary> <step_id>", file=sys.stderr)
                print('Use "-" for step_id if event doesn\'t belong to a specific step', file=sys.stderr)
                sys.exit(1)
            if args[4].startswith("{") or args[4].startswith("["):
                print("ERROR: step_id appears to be JSON. You likely forgot the step_id argument.", file=sys.stderr)
                print("Expected: log-event <mission_id> <run_id> <type> <summary> <step_id> [payload_json]", file=sys.stderr)
                print('Use "-" for step_id if event doesn\'t belong to a specific step', file=sys.stderr)
                sys.exit(1)
            step_id = args[4] if args[4] != "-" else None
            payload = json.loads(args[5]) if len(args) > 5 else None
            log_event(
                args[0], args[1], args[2], args[3], step_id=step_id, payload=payload
            )
        elif cmd == "list-events":
            list_events(args[0], args[1])

        # Assistants
        elif cmd == "create-assistant":
            # create-assistant <name> <instructions> <greeting> [options_json]
            # options_json can include: features, model, tools, voice, voice_settings,
            # transcription, telephony_settings, messaging_settings, description,
            # llm_api_key_ref, insight_settings, privacy_settings,
            # dynamic_variables_webhook_url, dynamic_variables, widget_settings
            if len(args) > 3:
                opts = json.loads(args[3])
            else:
                opts = {}
            features = opts.pop("features", None) or opts.pop("enabled_features", None)
            create_assistant(
                args[0],
                args[1],
                args[2],
                features=features,
                **opts,
            )
        elif cmd == "list-assistants":
            # list-assistants [--name=<filter>] [--page=<n>] [--size=<n>]
            name_filter = None
            page_num = 1
            page_size = 25
            for a in args:
                if a.startswith("--name="):
                    name_filter = a.split("=", 1)[1]
                elif a.startswith("--page="):
                    page_num = int(a.split("=", 1)[1])
                elif a.startswith("--size="):
                    page_size = int(a.split("=", 1)[1])
            list_assistants(
                page_size=page_size, page_number=page_num, name_filter=name_filter
            )
        elif cmd == "get-assistant":
            get_assistant(args[0])
        elif cmd == "update-assistant":
            updates = json.loads(args[1])
            update_assistant(args[0], updates)
        elif cmd == "get-connection-id":
            feature = args[1] if len(args) > 1 else "telephony"
            get_assistant_connection_id(args[0], feature)

        # Phone Numbers
        elif cmd == "list-phones":
            available = "--available" in args
            list_phone_numbers(available)
        elif cmd == "get-available-phone":
            get_available_phone_number()
        elif cmd == "assign-phone":
            hd = "--no-hd" not in args
            positional = [a for a in args if not a.startswith("--")]
            conn_type = positional[2] if len(positional) > 2 else "voice"
            assign_phone_number(positional[0], positional[1], conn_type, hd_voice=hd)

        # Scheduled Events
        elif cmd == "schedule-call":
            # schedule-call <assistant_id> <to> <from> <datetime> <mission_id> <run_id> [step_id] [dynamic_variables_json]
            step_id = None
            dyn_vars = None
            if len(args) > 6:
                # If arg 6 looks like JSON, it's dynamic_variables; otherwise it's step_id
                try:
                    dyn_vars = json.loads(args[6])
                except (json.JSONDecodeError, ValueError):
                    step_id = args[6]
                    dyn_vars = json.loads(args[7]) if len(args) > 7 else None
            schedule_call(args[0], args[1], args[2], args[3], args[4], args[5], mission_step_id=step_id, dynamic_variables=dyn_vars)
        elif cmd == "schedule-sms":
            # schedule-sms <assistant_id> <to> <from> <datetime> <text> [mission_id] [mission_run_id] [step_id] [dynamic_variables_json]
            mission_id = args[5] if len(args) > 5 else None
            run_id = args[6] if len(args) > 6 else None
            step_id = args[7] if len(args) > 7 else None
            dyn_vars = json.loads(args[8]) if len(args) > 8 else None
            schedule_sms(args[0], args[1], args[2], args[3], args[4], mission_id=mission_id, mission_run_id=run_id, mission_step_id=step_id, dynamic_variables=dyn_vars)
        elif cmd == "get-event":
            get_scheduled_event(args[0], args[1])
        elif cmd == "cancel-scheduled-event":
            delete_scheduled_event(args[0], args[1])
        elif cmd == "list-events-assistant":
            list_scheduled_events(args[0])

        # Insights (conversation results)
        elif cmd == "get-insights":
            get_conversation_insights(args[0])
        elif cmd == "rename-conversation":
            rename_conversation(args[0], args[1])

        # Insight Templates (CRUD)
        elif cmd == "create-insight":
            opts = json.loads(args[2]) if len(args) > 2 else {}
            create_insight(args[0], args[1], **opts)
        elif cmd == "get-insight":
            get_insight(args[0])
        elif cmd == "list-insights":
            list_insights()
        elif cmd == "update-insight":
            updates = json.loads(args[1])
            update_insight(args[0], **updates)
        # Insight Groups
        elif cmd == "create-insight-group":
            opts = json.loads(args[1]) if len(args) > 1 else {}
            create_insight_group(args[0], **opts)
        elif cmd == "get-insight-group":
            get_insight_group(args[0])
        elif cmd == "list-insight-groups":
            list_insight_groups()
        elif cmd == "update-insight-group":
            updates = json.loads(args[1])
            update_insight_group(args[0], **updates)
        elif cmd == "assign-insight":
            assign_insight_to_group(args[0], args[1])
        elif cmd == "unassign-insight":
            unassign_insight_from_group(args[0], args[1])

        # Mission Run Agents (linking)
        elif cmd == "link-agent":
            link_telnyx_agent(args[0], args[1], args[2])
        elif cmd == "list-linked-agents":
            list_linked_agents(args[0], args[1])
        elif cmd == "unlink-agent":
            unlink_telnyx_agent(args[0], args[1], args[2])

        # State management
        elif cmd == "list-state":
            state = load_state()
            for slug, data in state.items():
                print(
                    f"{slug}: {data.get('mission_name')} [{data.get('status', 'unknown')}]"
                )
        elif cmd == "get-state":
            state = get_mission_state(args[0])
            print(json.dumps(state, indent=2))
        elif cmd == "remove-state":
            remove_mission_state(args[0])
            print(f"Removed {args[0]} from state")

        # Memory
        elif cmd == "save-memory":
            value = (
                json.loads(args[2])
                if args[2].startswith("{") or args[2].startswith("[")
                else args[2]
            )
            save_memory(args[0], args[1], value)
        elif cmd == "get-memory":
            key = args[1] if len(args) > 1 else None
            memory = get_memory(args[0], key)
            if memory is not None:
                print(
                    json.dumps(memory, indent=2)
                    if isinstance(memory, (dict, list))
                    else memory
                )
            else:
                print("No memory found" if key else "{}")
        elif cmd == "append-memory":
            item = (
                json.loads(args[2])
                if args[2].startswith("{") or args[2].startswith("[")
                else args[2]
            )
            append_memory(args[0], args[1], item)

        # High-level
        elif cmd == "init":
            steps = json.loads(args[3]) if len(args) > 3 else None
            init_mission(args[0], args[1], args[2], steps)
        elif cmd == "setup-agent":
            # setup-agent <slug> <name> <instructions> <greeting> [options_json]
            opts = json.loads(args[4]) if len(args) > 4 else {}
            setup_voice_agent(args[0], args[1], args[2], args[3], **opts)
        elif cmd == "complete":
            payload = json.loads(args[4]) if len(args) > 4 else None
            complete_mission(args[0], args[1], args[2], args[3], payload)

        else:
            print(f"Unknown command: {cmd}", file=sys.stderr)
            print_usage()
            sys.exit(1)

    except IndexError:
        print(f"Missing arguments for command: {cmd}", file=sys.stderr)
        print_usage()
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
