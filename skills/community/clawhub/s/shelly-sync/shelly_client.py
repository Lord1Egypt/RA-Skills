#!/usr/bin/env python3
"""
Shelly Sync Client
Fetches real-time power data from Shelly Pro 3EM via RPC API.
"""
import os
import sys
import json
import requests

SHELLY_EM_IP = os.getenv("SHELLY_EM_IP")
HA_URL = os.getenv("HOME_ASSISTANT_URL")
HA_TOKEN = os.getenv("SUPER_SECRET_HA_TOKEN")


def get_shelly_data(ip: str) -> dict:
    """Fetch power data from Shelly Pro 3EM RPC API."""
    url = f"http://{ip}/rpc/EMData.GetStatus?id=0"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        p1 = data.get("a_act_power", 0.0)
        p2 = data.get("b_act_power", 0.0)
        p3 = data.get("c_act_power", 0.0)
        total_power = round(p1 + p2 + p3, 2)

        return {
            "status": "success",
            "total_power_w": total_power,
            "phases": {"a": round(p1, 2), "b": round(p2, 2), "c": round(p3, 2)},
            "surplus": total_power < 0,
            "grid_direction": "injection" if total_power < 0 else "consumption"
        }
    except requests.exceptions.Timeout:
        return {"status": "error", "message": f"Connection timeout to {ip}"}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": f"Cannot connect to {ip}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def trigger_home_assistant(entity_id: str, state: str) -> dict:
    """Toggle a Home Assistant entity."""
    if not HA_URL or not HA_TOKEN:
        return {"status": "error", "message": "Home Assistant credentials not configured"}

    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }
    service = "homeassistant.turn_on" if state == "on" else "homeassistant.turn_off"
    domain = entity_id.split(".")[0]

    try:
        response = requests.post(
            f"{HA_URL}/api/services/{service}",
            headers=headers,
            json={"entity_id": entity_id},
            timeout=10
        )
        response.raise_for_status()
        return {"status": "success", "action": f"{domain} turned {state}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Missing arguments"}))
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print(json.dumps({"status": "error", "message": "Invalid JSON argument"}))
        sys.exit(1)

    action = args.get("action")
    target_load = args.get("target_load")

    if not SHELLY_EM_IP:
        print(json.dumps({"status": "error", "message": "SHELLY_EM_IP env var not set"}))
        sys.exit(1)

    if action == "get_status":
        result = get_shelly_data(SHELLY_EM_IP)
        print(json.dumps(result, indent=2))

    elif action == "optimize_load":
        metrics = get_shelly_data(SHELLY_EM_IP)

        if metrics["status"] != "success":
            print(json.dumps(metrics))
            sys.exit(1)

        surplus_w = abs(metrics["total_power_w"]) if metrics["surplus"] else 0

        if metrics["surplus"]:
            result = {
                **metrics,
                "action_taken": f"Surplus of {surplus_w}W available. Load optimization possible."
            }

            # Auto-trigger target if specified
            if target_load:
                load_map = {
                    "heatpump": "switch.heatpump",
                    "charger": "switch.ev_charger",
                    "dishwasher": "switch.dishwasher",
                    "washing": "switch.washing_machine"
                }
                entity_id = load_map.get(target_load.lower())
                if entity_id:
                    trigger_result = trigger_home_assistant(entity_id, "on")
                    result["homeassistant"] = trigger_result
        else:
            result = {
                **metrics,
                "action_taken": f"No surplus ({metrics['total_power_w']}W consumption). Optimization skipped."
            }

        print(json.dumps(result, indent=2))

    else:
        print(json.dumps({"status": "error", "message": f"Unknown action: {action}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
