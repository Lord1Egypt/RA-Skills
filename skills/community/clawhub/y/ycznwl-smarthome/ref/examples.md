# Workflow Examples

Complete, validated import payloads for common automation patterns.
All use placeholder UUIDs — the server remaps them on import.

Replace `DEVICE_UUID_*` placeholders with actual device UUIDs from `GET /devices`.

---

## Example 1: Motion-Activated Light

When motion is detected, turn on a light. When motion stops, turn it off.

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Motion Light",
    "description": "Turn on light when motion detected, off when cleared",
    "timeout_s": 60,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "device_event",
          "label": "Motion Detected",
          "enabled": true,
          "device_uuid": "DEVICE_UUID_MOTION_SENSOR",
          "device_property": "motion",
          "compare_op": "changed",
          "compare_value": "",
          "pos_x": 100, "pos_y": 200
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "condition",
          "node_subtype": "device_state",
          "label": "Is Motion Active?",
          "config": {
            "device_uuid": "DEVICE_UUID_MOTION_SENSOR",
            "property": "motion",
            "operator": "is_true",
            "value": ""
          },
          "enabled": true,
          "pos_x": 350, "pos_y": 200
        },
        {
          "uuid": "n2",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Turn On Light",
          "config": {
            "device_uuid": "DEVICE_UUID_LIGHT",
            "action": "turn_on",
            "params": {}
          },
          "enabled": true,
          "pos_x": 600, "pos_y": 100
        },
        {
          "uuid": "n3",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Turn Off Light",
          "config": {
            "device_uuid": "DEVICE_UUID_LIGHT",
            "action": "turn_off",
            "params": {}
          },
          "enabled": true,
          "pos_x": 600, "pos_y": 300
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e2",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n2",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e3",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "false",
          "target_uuid": "n3",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Graph**: `trigger(motion changed) → condition(motion is_true?) → true: turn_on / false: turn_off`

---

## Example 2: Scheduled Curtain Control

Open curtains at 8 AM on weekdays, close at sunset.

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Weekday Curtain Schedule",
    "description": "Open curtains at 8 AM weekdays, close at sunset",
    "timeout_s": 60,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "cron",
          "label": "8 AM Weekdays",
          "enabled": true,
          "cron_expr": "0 8 * * 1-5",
          "pos_x": 100, "pos_y": 100
        },
        {
          "uuid": "t2",
          "trigger_type": "sun_event",
          "label": "Sunset",
          "enabled": true,
          "sun_event": "sunset",
          "sun_offset_min": 0,
          "pos_x": 100, "pos_y": 350
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Open Curtain",
          "config": {
            "device_uuid": "DEVICE_UUID_CURTAIN",
            "action": "open",
            "params": {}
          },
          "enabled": true,
          "pos_x": 400, "pos_y": 100
        },
        {
          "uuid": "n2",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Close Curtain",
          "config": {
            "device_uuid": "DEVICE_UUID_CURTAIN",
            "action": "close",
            "params": {}
          },
          "enabled": true,
          "pos_x": 400, "pos_y": 350
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e2",
          "source_uuid": "t2",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n2",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Graph**: `cron(8 AM weekdays) → open_curtain` | `sun_event(sunset) → close_curtain`

---

## Example 3: Temperature-Based AC Control with Notification

When temperature exceeds 28°C during business hours, turn on AC to cool mode at 24°C
and send a notification. When temperature drops below 22°C, turn off AC.

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Smart AC Control",
    "description": "Auto AC based on temperature during business hours",
    "timeout_s": 120,
    "cooldown_ms": 300000,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "device_event",
          "label": "Temp Change",
          "enabled": true,
          "device_uuid": "DEVICE_UUID_TEMP_SENSOR",
          "device_property": "temperature",
          "compare_op": "changed",
          "compare_value": "",
          "pos_x": 100, "pos_y": 250
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "condition",
          "node_subtype": "schedule_match",
          "label": "Business Hours?",
          "config": {
            "days": [1, 2, 3, 4, 5],
            "from": "09:00",
            "to": "18:00",
            "timezone": "Asia/Shanghai"
          },
          "enabled": true,
          "pos_x": 300, "pos_y": 250
        },
        {
          "uuid": "n2",
          "node_type": "condition",
          "node_subtype": "device_state",
          "label": "Temp > 28°C?",
          "config": {
            "device_uuid": "DEVICE_UUID_TEMP_SENSOR",
            "property": "temperature",
            "operator": "gt",
            "value": "28"
          },
          "enabled": true,
          "pos_x": 550, "pos_y": 150
        },
        {
          "uuid": "n3",
          "node_type": "condition",
          "node_subtype": "device_state",
          "label": "Temp < 22°C?",
          "config": {
            "device_uuid": "DEVICE_UUID_TEMP_SENSOR",
            "property": "temperature",
            "operator": "lt",
            "value": "22"
          },
          "enabled": true,
          "pos_x": 550, "pos_y": 350
        },
        {
          "uuid": "n4",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "AC On + Cool",
          "config": {
            "device_uuid": "DEVICE_UUID_AC",
            "action": "turn_on",
            "params": {}
          },
          "enabled": true,
          "pos_x": 800, "pos_y": 50
        },
        {
          "uuid": "n5",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Set Cool Mode",
          "config": {
            "device_uuid": "DEVICE_UUID_AC",
            "action": "set_mode",
            "params": { "mode": "cool" }
          },
          "enabled": true,
          "pos_x": 1050, "pos_y": 50
        },
        {
          "uuid": "n6",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Set 24°C",
          "config": {
            "device_uuid": "DEVICE_UUID_AC",
            "action": "set_target_temperature",
            "params": { "target_temperature": 24 }
          },
          "enabled": true,
          "pos_x": 1300, "pos_y": 50
        },
        {
          "uuid": "n7",
          "node_type": "action",
          "node_subtype": "notify",
          "label": "Notify: AC On",
          "config": {
            "channel": "system",
            "body": "Temperature {{trigger.new_value}}°C — AC activated",
            "level": "info"
          },
          "enabled": true,
          "pos_x": 1300, "pos_y": 200
        },
        {
          "uuid": "n8",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "AC Off",
          "config": {
            "device_uuid": "DEVICE_UUID_AC",
            "action": "turn_off",
            "params": {}
          },
          "enabled": true,
          "pos_x": 800, "pos_y": 350
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e2",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n2",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e3",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n3",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e4",
          "source_uuid": "n2",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n4",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e5",
          "source_uuid": "n4",
          "source_type": "node",
          "source_handle": "output",
          "target_uuid": "n5",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e6",
          "source_uuid": "n5",
          "source_type": "node",
          "source_handle": "output",
          "target_uuid": "n6",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e7",
          "source_uuid": "n6",
          "source_type": "node",
          "source_handle": "output",
          "target_uuid": "n7",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e8",
          "source_uuid": "n3",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n8",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Graph**:
```
trigger(temp changed)
  → condition(business hours?)
    → true: condition(temp > 28?)
      → true: turn_on_ac → set_cool → set_24c → notify
    → true: condition(temp < 22?)
      → true: turn_off_ac
```

---

## Example 4: KNX Switch Controls Light with Delay

When a KNX wall switch (DPT 1.001) is pressed ON, turn on a light.
When pressed OFF, wait 5 seconds then turn off the light.

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "KNX Switch to Light with Delay Off",
    "timeout_s": 30,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "knx_group_event",
          "label": "Wall Switch",
          "enabled": true,
          "knx_addresses": ["1/1/1"],
          "knx_event_types": ["write"],
          "knx_dpt": "1.001",
          "compare_op": "changed",
          "compare_value": "",
          "pos_x": 100, "pos_y": 200
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "condition",
          "node_subtype": "numeric_compare",
          "label": "Switch ON?",
          "config": {
            "left": { "source": "trigger", "value": "knx_value" },
            "operator": "eq",
            "right": { "source": "literal", "value": "1" }
          },
          "enabled": true,
          "pos_x": 350, "pos_y": 200
        },
        {
          "uuid": "n2",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Light On",
          "config": {
            "device_uuid": "DEVICE_UUID_LIGHT",
            "action": "turn_on",
            "params": {}
          },
          "enabled": true,
          "pos_x": 600, "pos_y": 100
        },
        {
          "uuid": "n3",
          "node_type": "delay",
          "node_subtype": "fixed_delay",
          "label": "Wait 5s",
          "config": { "seconds": 5 },
          "enabled": true,
          "pos_x": 600, "pos_y": 300
        },
        {
          "uuid": "n4",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Light Off",
          "config": {
            "device_uuid": "DEVICE_UUID_LIGHT",
            "action": "turn_off",
            "params": {}
          },
          "enabled": true,
          "pos_x": 850, "pos_y": 300
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e2",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n2",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e3",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "false",
          "target_uuid": "n3",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e4",
          "source_uuid": "n3",
          "source_type": "node",
          "source_handle": "output",
          "target_uuid": "n4",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Graph**: `knx_switch → condition(value==1?) → true: light_on / false: wait_5s → light_off`

---

## Example 5: MQTT Bridge with Value Mapping via Variable

Classify temperature as "critical" or "normal" using `set_variable`, then publish
to MQTT using `{{var.severity}}`. This demonstrates how variables let you set a value
in one branch and reference it in a shared downstream node.

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Temp to MQTT with Severity",
    "timeout_s": 30,
    "debounce_ms": 5000,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "device_event",
          "label": "Temp Change",
          "enabled": true,
          "device_uuid": "DEVICE_UUID_TEMP_SENSOR",
          "device_property": "temperature",
          "compare_op": "changed",
          "compare_value": "",
          "pos_x": 100, "pos_y": 200
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "condition",
          "node_subtype": "device_state",
          "label": "Temp > 30?",
          "config": {
            "device_uuid": "DEVICE_UUID_TEMP_SENSOR",
            "property": "temperature",
            "operator": "gt",
            "value": "30"
          },
          "enabled": true,
          "pos_x": 350, "pos_y": 200
        },
        {
          "uuid": "n2",
          "node_type": "action",
          "node_subtype": "set_variable",
          "label": "Set: Critical",
          "config": {
            "key": "severity",
            "value": { "source": "literal", "value": "critical" }
          },
          "enabled": true,
          "pos_x": 600, "pos_y": 100
        },
        {
          "uuid": "n3",
          "node_type": "action",
          "node_subtype": "set_variable",
          "label": "Set: Normal",
          "config": {
            "key": "severity",
            "value": { "source": "literal", "value": "normal" }
          },
          "enabled": true,
          "pos_x": 600, "pos_y": 300
        },
        {
          "uuid": "n4",
          "node_type": "action",
          "node_subtype": "mqtt_publish",
          "label": "Publish Temp (Critical)",
          "config": {
            "topic": "home/temperature/status",
            "payload": "{\"temp\": {{trigger.new_value}}, \"severity\": \"{{var.severity}}\"}",
            "qos": 1
          },
          "enabled": true,
          "pos_x": 900, "pos_y": 100
        },
        {
          "uuid": "n5",
          "node_type": "action",
          "node_subtype": "mqtt_publish",
          "label": "Publish Temp (Normal)",
          "config": {
            "topic": "home/temperature/status",
            "payload": "{\"temp\": {{trigger.new_value}}, \"severity\": \"{{var.severity}}\"}",
            "qos": 0
          },
          "enabled": true,
          "pos_x": 900, "pos_y": 300
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e2",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n2",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e3",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "false",
          "target_uuid": "n3",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e4",
          "source_uuid": "n2",
          "source_type": "node",
          "source_handle": "output",
          "target_uuid": "n4",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e5",
          "source_uuid": "n3",
          "source_type": "node",
          "source_handle": "output",
          "target_uuid": "n5",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Graph**: `trigger(temp changed) → condition(temp > 30?) → true: set(severity=critical) → mqtt` / `false: set(severity=normal) → mqtt`

Both branches publish to the same topic with `{{var.severity}}` — the variable carries the branch result into the payload.

---

## Example 6: Multi-Condition with Logic AND

Turn on a fan only when temperature > 26°C AND humidity > 70%.

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Hot & Humid Fan Control",
    "timeout_s": 60,
    "cooldown_ms": 60000,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "device_event",
          "label": "Temp or Humidity Change",
          "enabled": true,
          "device_uuid": "DEVICE_UUID_TEMP_SENSOR",
          "device_property": "temperature",
          "compare_op": "changed",
          "compare_value": "",
          "pos_x": 100, "pos_y": 200
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "condition",
          "node_subtype": "device_state",
          "label": "Temp > 26°C?",
          "config": {
            "device_uuid": "DEVICE_UUID_TEMP_SENSOR",
            "property": "temperature",
            "operator": "gt",
            "value": "26"
          },
          "enabled": true,
          "pos_x": 350, "pos_y": 100
        },
        {
          "uuid": "n2",
          "node_type": "condition",
          "node_subtype": "device_state",
          "label": "Humidity > 70%?",
          "config": {
            "device_uuid": "DEVICE_UUID_HUMIDITY_SENSOR",
            "property": "humidity",
            "operator": "gt",
            "value": "70"
          },
          "enabled": true,
          "pos_x": 350, "pos_y": 300
        },
        {
          "uuid": "n3",
          "node_type": "logic",
          "node_subtype": "and",
          "label": "Both True?",
          "config": {},
          "enabled": true,
          "pos_x": 600, "pos_y": 200
        },
        {
          "uuid": "n4",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Fan On",
          "config": {
            "device_uuid": "DEVICE_UUID_FAN",
            "action": "turn_on",
            "params": {}
          },
          "enabled": true,
          "pos_x": 850, "pos_y": 100
        },
        {
          "uuid": "n5",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Fan Off",
          "config": {
            "device_uuid": "DEVICE_UUID_FAN",
            "action": "turn_off",
            "params": {}
          },
          "enabled": true,
          "pos_x": 850, "pos_y": 300
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e2",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n2",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e3",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n3",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e4",
          "source_uuid": "n2",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n3",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e5",
          "source_uuid": "n3",
          "source_type": "node",
          "source_handle": "true",
          "target_uuid": "n4",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e6",
          "source_uuid": "n3",
          "source_type": "node",
          "source_handle": "false",
          "target_uuid": "n5",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Graph**:
```
trigger(temp changed) ─┬→ condition(temp > 26?) ──true──→ AND ──true──→ fan_on
                        └→ condition(humidity > 70?) ──true──↗    └──false──→ fan_off
```

**Note**: The `AND` logic node correctly receives edges from two condition nodes (not
directly from the trigger). This satisfies the validation rule that logic nodes must have
condition nodes as inputs.

**Important — single trigger limitation**: This workflow only fires on temperature
changes. A humidity spike alone will not trigger it (the humidity condition reads the
current snapshot value). If you also need humidity changes to fire the workflow, add a
second `device_event` trigger watching `DEVICE_UUID_HUMIDITY_SENSOR / humidity / changed`
and connect it to both condition nodes the same way.

---

## Example 7: Scheduled Scene Execution (Good Night / Good Morning)

Execute a "Good Night" scene at 11 PM and a "Good Morning" scene at 7 AM.
This uses the `scene_exec` action node to trigger pre-configured scenes.

First, find scene UUIDs via `GET /scenes`.

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Daily Scene Schedule",
    "description": "Good Night at 11 PM, Good Morning at 7 AM",
    "timeout_s": 120,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "cron",
          "label": "11 PM",
          "enabled": true,
          "cron_expr": "0 23 * * *",
          "pos_x": 100, "pos_y": 100
        },
        {
          "uuid": "t2",
          "trigger_type": "cron",
          "label": "7 AM",
          "enabled": true,
          "cron_expr": "0 7 * * *",
          "pos_x": 100, "pos_y": 350
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "action",
          "node_subtype": "scene_exec",
          "label": "Good Night Scene",
          "config": {
            "scene_uuid": "SCENE_UUID_GOOD_NIGHT"
          },
          "enabled": true,
          "pos_x": 400, "pos_y": 100
        },
        {
          "uuid": "n2",
          "node_type": "action",
          "node_subtype": "scene_exec",
          "label": "Good Morning Scene",
          "config": {
            "scene_uuid": "SCENE_UUID_GOOD_MORNING"
          },
          "enabled": true,
          "pos_x": 400, "pos_y": 350
        },
        {
          "uuid": "n3",
          "node_type": "action",
          "node_subtype": "notify",
          "label": "Notify: Night",
          "config": {
            "channel": "system",
            "body": "Good Night scene activated",
            "level": "info"
          },
          "enabled": true,
          "pos_x": 650, "pos_y": 100
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e2",
          "source_uuid": "t2",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n2",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e3",
          "source_uuid": "n1",
          "source_type": "node",
          "source_handle": "output",
          "target_uuid": "n3",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Graph**: `cron(11 PM) → scene_exec(Good Night) → notify` | `cron(7 AM) → scene_exec(Good Morning)`

---

## Example 8: Motion Triggers Scene via Virtual Device

When motion is detected, execute a "Welcome Home" scene by controlling the
virtual scene device (alternative to `scene_exec` — using `device_control`
with a virtual scene device UUID).

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Motion Welcome Scene",
    "description": "Execute Welcome Home scene when motion detected",
    "timeout_s": 60,
    "cooldown_ms": 60000,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "device_event",
          "label": "Motion Detected",
          "enabled": true,
          "device_uuid": "DEVICE_UUID_MOTION_SENSOR",
          "device_property": "motion",
          "compare_op": "is_true",
          "compare_value": "",
          "pos_x": 100, "pos_y": 200
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "action",
          "node_subtype": "device_control",
          "label": "Execute Welcome Scene",
          "config": {
            "device_uuid": "scene-SCENE_UUID_WELCOME",
            "action": "activate_scene",
            "params": {}
          },
          "enabled": true,
          "pos_x": 400, "pos_y": 200
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Note**: The `device_uuid` uses the virtual device UUID pattern `scene-<scene_uuid>`.
This approach works identically to `scene_exec` but goes through the `device_control`
path. Prefer `scene_exec` for clarity in most cases.

---

## Example 9: KNX Send — Mirror Gateway Light State to KNX Bus

When the gateway changes a light's power state (via app, automation, etc.), write the
new value back to a KNX group address so physical KNX panels stay in sync.

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Mirror Light State to KNX",
    "description": "Sync gateway light state back to KNX group address",
    "timeout_s": 30,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "device_event",
          "label": "Light Power Changed",
          "enabled": true,
          "device_uuid": "DEVICE_UUID_LIGHT",
          "device_property": "power",
          "compare_op": "changed",
          "compare_value": "",
          "pos_x": 100, "pos_y": 200
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "action",
          "node_subtype": "knx_send",
          "label": "Write State to KNX Bus",
          "config": {
            "targets": [
              {
                "address": "1/1/1",
                "command_type": "write",
                "dpt": "1.001",
                "value": { "source": "trigger", "value": "new_value" }
              }
            ]
          },
          "enabled": true,
          "pos_x": 400, "pos_y": 200
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Graph**: `trigger(light power changed) → knx_send(write new_value to 1/1/1 as DPT 1.001)`

**Key point**: `value: { "source": "trigger", "value": "new_value" }` passes the trigger's
new value directly into the KNX telegram — no condition node needed when you want to forward
every change unconditionally.

To send multiple addresses at once (e.g. status feedback + scene recall), add more objects
to the `targets` array within the same `knx_send` node.

---

## Example 10: HTTP Request — Notify LAN Service on Smoke Alert

When smoke is detected, send a local system notification and notify a reviewed LAN service
(for example a local security panel, local notification service, or Home Assistant instance).
Use off-LAN endpoints only when the user explicitly asks for them and approves the exact URL.

```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Smoke Alert LAN Notify",
    "description": "System notify + LAN HTTP call when smoke sensor fires",
    "timeout_s": 30,
    "cooldown_ms": 300000,
    "flow_data": {
      "triggers": [
        {
          "uuid": "t1",
          "trigger_type": "device_event",
          "label": "Smoke Detected",
          "enabled": true,
          "device_uuid": "DEVICE_UUID_SMOKE_SENSOR",
          "device_property": "smoke",
          "compare_op": "is_true",
          "compare_value": "",
          "pos_x": 100, "pos_y": 200
        }
      ],
      "nodes": [
        {
          "uuid": "n1",
          "node_type": "action",
          "node_subtype": "notify",
          "label": "System Alert",
          "config": {
            "channel": "system",
            "body": "Smoke detected by {{trigger.device_uuid}}",
            "level": "error"
          },
          "enabled": true,
          "pos_x": 400, "pos_y": 100
        },
        {
          "uuid": "n2",
          "node_type": "action",
          "node_subtype": "http_request",
          "label": "Notify LAN Service",
          "config": {
            "method": "POST",
            "url": "http://lan-notifier.local/api/alerts",
            "headers": {
              "Content-Type": "application/json"
            },
            "body": "{\"event\": \"smoke\", \"device\": \"{{trigger.device_uuid}}\", \"value\": {{trigger.new_value}}}",
            "timeout_s": 10
          },
          "enabled": true,
          "pos_x": 400, "pos_y": 300
        }
      ],
      "edges": [
        {
          "uuid": "e1",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n1",
          "target_handle": "input",
          "enabled": true
        },
        {
          "uuid": "e2",
          "source_uuid": "t1",
          "source_type": "trigger",
          "source_handle": "output",
          "target_uuid": "n2",
          "target_handle": "input",
          "enabled": true
        }
      ]
    }
  }
}
```

**Graph**: `trigger(smoke=true) ─┬→ notify(system error)` / `└→ http_request(POST to LAN endpoint)`

Both nodes receive the trigger output directly — they run in parallel (both are in separate
branches from the same trigger). `cooldown_ms: 300000` prevents repeated alerts within 5 minutes.

**Template note**: In JSON body strings, string values need quotes around the template
(`"{{trigger.device_uuid}}"`), but numeric values do not (`{{trigger.new_value}}`).
Make sure the JSON stays valid after template substitution.
