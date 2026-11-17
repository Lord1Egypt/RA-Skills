# Twilio Voice Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `twilio-voice`

x402 availability: not enabled for this product.

## `add_conference_participant`

Action slug: `add-conference-participant`

Price: `5` credits

Dial a new participant from the credential outgoing_number into an existing conference.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conference_sid` | `string` | yes | Conference SID or friendly name. |
| `end_conference_on_exit` | `boolean` | no | End the conference when this participant exits. |
| `muted` | `boolean` | no | Join muted. |
| `start_conference_on_enter` | `boolean` | no | Start the conference when this participant enters. |
| `to_number` | `string` | yes | Participant phone number in E.164 format. |

Sample parameters:

```json
{
  "conference_sid": "example conference sid",
  "end_conference_on_exit": true,
  "muted": true,
  "start_conference_on_enter": true,
  "to_number": "example to number"
}
```

Generated JSON parameter schema:

```json
{
  "conference_sid": {
    "description": "Conference SID or friendly name.",
    "required": true,
    "type": "string"
  },
  "end_conference_on_exit": {
    "description": "End the conference when this participant exits.",
    "required": false,
    "type": "boolean"
  },
  "muted": {
    "description": "Join muted.",
    "required": false,
    "type": "boolean"
  },
  "start_conference_on_enter": {
    "description": "Start the conference when this participant enters.",
    "required": false,
    "type": "boolean"
  },
  "to_number": {
    "description": "Participant phone number in E.164 format.",
    "required": true,
    "type": "string"
  }
}
```

## `create_conference`

Action slug: `create-conference`

Price: `5` credits

Dial a participant from the credential outgoing_number into a named conference room.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conference_name` | `string` | yes | Conference room friendly name. |
| `end_conference_on_exit` | `boolean` | no | End the conference when this participant exits. |
| `muted` | `boolean` | no | Join muted. |
| `record` | `boolean` | no | Record the conference from the start. |
| `start_conference_on_enter` | `boolean` | no | Start the conference when this participant enters. |
| `to_number` | `string` | yes | Participant phone number in E.164 format. |

Sample parameters:

```json
{
  "conference_name": "example conference name",
  "end_conference_on_exit": true,
  "muted": true,
  "record": true,
  "start_conference_on_enter": true,
  "to_number": "example to number"
}
```

Generated JSON parameter schema:

```json
{
  "conference_name": {
    "description": "Conference room friendly name.",
    "required": true,
    "type": "string"
  },
  "end_conference_on_exit": {
    "description": "End the conference when this participant exits.",
    "required": false,
    "type": "boolean"
  },
  "muted": {
    "description": "Join muted.",
    "required": false,
    "type": "boolean"
  },
  "record": {
    "description": "Record the conference from the start.",
    "required": false,
    "type": "boolean"
  },
  "start_conference_on_enter": {
    "description": "Start the conference when this participant enters.",
    "required": false,
    "type": "boolean"
  },
  "to_number": {
    "description": "Participant phone number in E.164 format.",
    "required": true,
    "type": "string"
  }
}
```

## `delete_recording`

Action slug: `delete-recording`

Price: `5` credits

Delete a recording.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `recording_sid` | `string` | yes | Recording SID, usually starting with RE. |

Sample parameters:

```json
{
  "recording_sid": "example recording sid"
}
```

Generated JSON parameter schema:

```json
{
  "recording_sid": {
    "description": "Recording SID, usually starting with RE.",
    "required": true,
    "type": "string"
  }
}
```

## `end_call`

Action slug: `end-call`

Price: `5` credits

Hang up an in-progress call.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `call_sid` | `string` | yes | Call SID, usually starting with CA. |

Sample parameters:

```json
{
  "call_sid": "example call sid"
}
```

Generated JSON parameter schema:

```json
{
  "call_sid": {
    "description": "Call SID, usually starting with CA.",
    "required": true,
    "type": "string"
  }
}
```

## `end_conference`

Action slug: `end-conference`

Price: `5` credits

End a conference for all participants.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `announce_url` | `string` | no | Optional URL returning TwiML to announce before ending. |
| `conference_sid` | `string` | yes | Conference SID or friendly name. |

Sample parameters:

```json
{
  "announce_url": "https://example.com",
  "conference_sid": "example conference sid"
}
```

Generated JSON parameter schema:

```json
{
  "announce_url": {
    "description": "Optional URL returning TwiML to announce before ending.",
    "required": false,
    "type": "string"
  },
  "conference_sid": {
    "description": "Conference SID or friendly name.",
    "required": true,
    "type": "string"
  }
}
```

## `end_live_call`

Action slug: `end-live-call`

Price: `5` credits

Hang up a live call started with start_live_call.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `session_id` | `string` | yes | UUID4 returned by start_live_call. |

Sample parameters:

```json
{
  "session_id": "example session id"
}
```

Generated JSON parameter schema:

```json
{
  "session_id": {
    "description": "UUID4 returned by start_live_call.",
    "required": true,
    "type": "string"
  }
}
```

## `get_call_history`

Action slug: `get-call-history`

Price: `5` credits

List calls with optional filters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date_created_after` | `string` | no | Only calls started on or after this ISO 8601 date. |
| `date_created_before` | `string` | no | Only calls started before this ISO 8601 date. |
| `limit` | `integer` | no | Maximum calls to return. |
| `status_filter` | `string` | no | Filter by call status. |

Sample parameters:

```json
{
  "date_created_after": "example date created after",
  "date_created_before": "example date created before",
  "limit": 1,
  "status_filter": "example status filter"
}
```

Generated JSON parameter schema:

```json
{
  "date_created_after": {
    "description": "Only calls started on or after this ISO 8601 date.",
    "required": false,
    "type": "string"
  },
  "date_created_before": {
    "description": "Only calls started before this ISO 8601 date.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Maximum calls to return.",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "status_filter": {
    "description": "Filter by call status.",
    "required": false,
    "type": "string"
  }
}
```

## `get_call_status`

Action slug: `get-call-status`

Price: `5` credits

Fetch the status and details of a single call.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `call_sid` | `string` | yes | Call SID, usually starting with CA. |

Sample parameters:

```json
{
  "call_sid": "example call sid"
}
```

Generated JSON parameter schema:

```json
{
  "call_sid": {
    "description": "Call SID, usually starting with CA.",
    "required": true,
    "type": "string"
  }
}
```

## `get_ivr_session`

Action slug: `get-ivr-session`

Price: `5` credits

Fetch an IVR session's status, transcript, and outcome by session_id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `session_id` | `string` | yes | UUID4 returned by start_ivr_call. |

Sample parameters:

```json
{
  "session_id": "example session id"
}
```

Generated JSON parameter schema:

```json
{
  "session_id": {
    "description": "UUID4 returned by start_ivr_call.",
    "required": true,
    "type": "string"
  }
}
```

## `get_live_session`

Action slug: `get-live-session`

Price: `5` credits

Fetch a live-call-only session summary by session_id, including transcript, spoken messages, call summary, bounded gateway/Voice-Insights latency_events, and latency_summary. Token-playback and speaker WebSocket telemetry are not exposed by the documented ConversationRelay protocol.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `after_latency_index` | `integer` | no | First latency event index to return when include_latency_events is true. |
| `include_latency_events` | `boolean` | no | Include bounded live-call latency events in the response. |
| `session_id` | `string` | yes | UUID4 returned by start_live_call. |

Sample parameters:

```json
{
  "after_latency_index": 0,
  "include_latency_events": true,
  "session_id": "example session id"
}
```

Generated JSON parameter schema:

```json
{
  "after_latency_index": {
    "description": "First latency event index to return when include_latency_events is true.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "include_latency_events": {
    "description": "Include bounded live-call latency events in the response.",
    "required": false,
    "type": "boolean"
  },
  "session_id": {
    "description": "UUID4 returned by start_live_call.",
    "required": true,
    "type": "string"
  }
}
```

## `get_live_transcript`

Action slug: `get-live-transcript`

Price: `5` credits

Fetch new transcript entries for a live call, optionally long-polling for caller input and latency-event slices.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `after_index` | `integer` | no | First transcript index to return. Use next_after_index from the previous response. |
| `after_latency_index` | `integer` | no | First latency event index to return when include_latency_events is true. |
| `include_latency_events` | `boolean` | no | Include bounded live-call latency event slices in the response. |
| `session_id` | `string` | yes | UUID4 returned by start_live_call. |
| `wait_seconds` | `integer` | no | Optional long-poll wait time for new entries. |

Sample parameters:

```json
{
  "after_index": 0,
  "after_latency_index": 0,
  "include_latency_events": true,
  "session_id": "example session id",
  "wait_seconds": 0
}
```

Generated JSON parameter schema:

```json
{
  "after_index": {
    "description": "First transcript index to return. Use next_after_index from the previous response.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "after_latency_index": {
    "description": "First latency event index to return when include_latency_events is true.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "include_latency_events": {
    "description": "Include bounded live-call latency event slices in the response.",
    "required": false,
    "type": "boolean"
  },
  "session_id": {
    "description": "UUID4 returned by start_live_call.",
    "required": true,
    "type": "string"
  },
  "wait_seconds": {
    "description": "Optional long-poll wait time for new entries.",
    "maximum": 20,
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `get_recording`

Action slug: `get-recording`

Price: `5` credits

Fetch recording details and optionally save the audio to the File Manager.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `recording_sid` | `string` | yes | Recording SID, usually starting with RE. |
| `save_to_file_manager` | `boolean` | no | Download the audio and return a file_id plus signed URL. |

Sample parameters:

```json
{
  "recording_sid": "example recording sid",
  "save_to_file_manager": true
}
```

Generated JSON parameter schema:

```json
{
  "recording_sid": {
    "description": "Recording SID, usually starting with RE.",
    "required": true,
    "type": "string"
  },
  "save_to_file_manager": {
    "description": "Download the audio and return a file_id plus signed URL.",
    "required": false,
    "type": "boolean"
  }
}
```

## `list_conference_participants`

Action slug: `list-conference-participants`

Price: `5` credits

List participants in a conference.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conference_sid` | `string` | yes | Conference SID or friendly name. |

Sample parameters:

```json
{
  "conference_sid": "example conference sid"
}
```

Generated JSON parameter schema:

```json
{
  "conference_sid": {
    "description": "Conference SID or friendly name.",
    "required": true,
    "type": "string"
  }
}
```

## `list_conferences`

Action slug: `list-conferences`

Price: `5` credits

List conferences with optional filters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conference_name` | `string` | no | Filter by conference friendly name. |
| `date_created_after` | `string` | no | Only conferences created on or after this ISO 8601 date. |
| `date_created_before` | `string` | no | Only conferences created before this ISO 8601 date. |
| `limit` | `integer` | no | Maximum conferences to return. |
| `status_filter` | `string` | no | Filter by conference status. |

Sample parameters:

```json
{
  "conference_name": "example conference name",
  "date_created_after": "example date created after",
  "date_created_before": "example date created before",
  "limit": 1,
  "status_filter": "example status filter"
}
```

Generated JSON parameter schema:

```json
{
  "conference_name": {
    "description": "Filter by conference friendly name.",
    "required": false,
    "type": "string"
  },
  "date_created_after": {
    "description": "Only conferences created on or after this ISO 8601 date.",
    "required": false,
    "type": "string"
  },
  "date_created_before": {
    "description": "Only conferences created before this ISO 8601 date.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Maximum conferences to return.",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "status_filter": {
    "description": "Filter by conference status.",
    "required": false,
    "type": "string"
  }
}
```

## `list_recordings`

Action slug: `list-recordings`

Price: `5` credits

List call recordings, optionally scoped to one call.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `call_sid` | `string` | no | Optional Call SID to scope recordings. |
| `date_created_after` | `string` | no | Only recordings created on or after this ISO 8601 date. |
| `date_created_before` | `string` | no | Only recordings created before this ISO 8601 date. |
| `limit` | `integer` | no | Maximum recordings to return. |

Sample parameters:

```json
{
  "call_sid": "example call sid",
  "date_created_after": "example date created after",
  "date_created_before": "example date created before",
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "call_sid": {
    "description": "Optional Call SID to scope recordings.",
    "required": false,
    "type": "string"
  },
  "date_created_after": {
    "description": "Only recordings created on or after this ISO 8601 date.",
    "required": false,
    "type": "string"
  },
  "date_created_before": {
    "description": "Only recordings created before this ISO 8601 date.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Maximum recordings to return.",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `make_call`

Action slug: `make-call`

Price: `5` credits

Place an outbound call from the fixed outgoing_number in the connected Twilio credential using inline TwiML or a TwiML URL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `machine_detection` | `string` | no | Answering-machine detection mode. |
| `record` | `boolean` | no | Record the call. |
| `send_digits` | `string` | no | DTMF digits to play once connected. |
| `status_callback` | `string` | no | URL to receive call status callbacks. |
| `status_callback_event` | `array` | no | Events that trigger status callbacks. |
| `timeout` | `integer` | no | Seconds to ring before giving up. |
| `to_number` | `string` | yes | Recipient phone number in E.164 format. |
| `twiml` | `string` | no | Inline TwiML XML, max 4000 characters. Provide twiml or twiml_url. |
| `twiml_url` | `string` | no | Public URL returning TwiML. Provide twiml or twiml_url. |

Sample parameters:

```json
{
  "machine_detection": "Enable",
  "record": true,
  "send_digits": "example send digits",
  "status_callback": "example status callback",
  "status_callback_event": [
    "initiated"
  ],
  "timeout": 5,
  "to_number": "example to number",
  "twiml": "example twiml"
}
```

Generated JSON parameter schema:

```json
{
  "machine_detection": {
    "description": "Answering-machine detection mode.",
    "enum": [
      "Enable",
      "DetectMessageEnd"
    ],
    "required": false,
    "type": "string"
  },
  "record": {
    "description": "Record the call.",
    "required": false,
    "type": "boolean"
  },
  "send_digits": {
    "description": "DTMF digits to play once connected.",
    "required": false,
    "type": "string"
  },
  "status_callback": {
    "description": "URL to receive call status callbacks.",
    "required": false,
    "type": "string"
  },
  "status_callback_event": {
    "description": "Events that trigger status callbacks.",
    "items": {
      "enum": [
        "initiated",
        "ringing",
        "answered",
        "completed"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "timeout": {
    "description": "Seconds to ring before giving up.",
    "maximum": 600,
    "minimum": 5,
    "required": false,
    "type": "integer"
  },
  "to_number": {
    "description": "Recipient phone number in E.164 format.",
    "required": true,
    "type": "string"
  },
  "twiml": {
    "description": "Inline TwiML XML, max 4000 characters. Provide twiml or twiml_url.",
    "required": false,
    "type": "string"
  },
  "twiml_url": {
    "description": "Public URL returning TwiML. Provide twiml or twiml_url.",
    "required": false,
    "type": "string"
  }
}
```

## `play_audio`

Action slug: `play-audio`

Price: `5` credits

Call the recipient from the credential outgoing_number and play an audio file.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `audio_url` | `string` | yes | Public audio file URL to play. |
| `loop` | `integer` | no | Times to loop; 0 means until the call ends. |
| `record` | `boolean` | no | Record the call. |
| `to_number` | `string` | yes | Recipient phone number in E.164 format. |

Sample parameters:

```json
{
  "audio_url": "https://example.com",
  "loop": 0,
  "record": true,
  "to_number": "example to number"
}
```

Generated JSON parameter schema:

```json
{
  "audio_url": {
    "description": "Public audio file URL to play.",
    "required": true,
    "type": "string"
  },
  "loop": {
    "description": "Times to loop; 0 means until the call ends.",
    "maximum": 100,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "record": {
    "description": "Record the call.",
    "required": false,
    "type": "boolean"
  },
  "to_number": {
    "description": "Recipient phone number in E.164 format.",
    "required": true,
    "type": "string"
  }
}
```

## `record_live_latency_event`

Action slug: `record-live-latency-event`

Price: `5` credits

Record external-agent live-call latency markers around non-Twilio tool calls. This only records timing metadata; it does not execute or inspect tools.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `duration_ms` | `number` | no | Optional elapsed time in milliseconds, normally sent with agent_tool_returned. |
| `latency_event` | `string` | yes | External-agent latency marker to record. |
| `session_id` | `string` | yes | UUID4 returned by start_live_call. |
| `tool_operation` | `string` | no | Optional operation/action name for the external tool call. |
| `tool_slug` | `string` | no | Optional AgentPMT tool slug associated with the external-agent latency marker. |
| `turn_id` | `string` | no | Optional caller turn_id being handled by the external tool call. |

Sample parameters:

```json
{
  "duration_ms": 0,
  "latency_event": "agent_tool_started",
  "session_id": "example session id",
  "tool_operation": "example tool operation",
  "tool_slug": "example tool slug",
  "turn_id": "example turn id"
}
```

Generated JSON parameter schema:

```json
{
  "duration_ms": {
    "description": "Optional elapsed time in milliseconds, normally sent with agent_tool_returned.",
    "maximum": 3600000,
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "latency_event": {
    "description": "External-agent latency marker to record.",
    "enum": [
      "agent_tool_started",
      "agent_tool_returned"
    ],
    "required": true,
    "type": "string"
  },
  "session_id": {
    "description": "UUID4 returned by start_live_call.",
    "required": true,
    "type": "string"
  },
  "tool_operation": {
    "description": "Optional operation/action name for the external tool call.",
    "required": false,
    "type": "string"
  },
  "tool_slug": {
    "description": "Optional AgentPMT tool slug associated with the external-agent latency marker.",
    "required": false,
    "type": "string"
  },
  "turn_id": {
    "description": "Optional caller turn_id being handled by the external tool call.",
    "required": false,
    "type": "string"
  }
}
```

## `redirect_call`

Action slug: `redirect-call`

Price: `5` credits

Redirect an in-progress call to new TwiML.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `call_sid` | `string` | yes | Call SID, usually starting with CA. |
| `twiml` | `string` | no | New inline TwiML. Provide twiml or twiml_url. |
| `twiml_url` | `string` | no | New TwiML URL. Provide twiml or twiml_url. |

Sample parameters:

```json
{
  "call_sid": "example call sid",
  "twiml": "example twiml",
  "twiml_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "call_sid": {
    "description": "Call SID, usually starting with CA.",
    "required": true,
    "type": "string"
  },
  "twiml": {
    "description": "New inline TwiML. Provide twiml or twiml_url.",
    "required": false,
    "type": "string"
  },
  "twiml_url": {
    "description": "New TwiML URL. Provide twiml or twiml_url.",
    "required": false,
    "type": "string"
  }
}
```

## `remove_conference_participant`

Action slug: `remove-conference-participant`

Price: `5` credits

Remove a participant from a conference.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `call_sid` | `string` | yes | Participant Call SID. |
| `conference_sid` | `string` | yes | Conference SID or friendly name. |

Sample parameters:

```json
{
  "call_sid": "example call sid",
  "conference_sid": "example conference sid"
}
```

Generated JSON parameter schema:

```json
{
  "call_sid": {
    "description": "Participant Call SID.",
    "required": true,
    "type": "string"
  },
  "conference_sid": {
    "description": "Conference SID or friendly name.",
    "required": true,
    "type": "string"
  }
}
```

## `say_on_call`

Action slug: `say-on-call`

Price: `5` credits

Queue text for the gateway to speak into an active live call.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `session_id` | `string` | yes | UUID4 returned by start_live_call. |
| `text` | `string` | yes | Text to speak, max 4096 characters. |
| `turn_id` | `string` | no | Optional caller turn_id to correlate this response with a transcript turn. |

Sample parameters:

```json
{
  "session_id": "example session id",
  "text": "example text",
  "turn_id": "example turn id"
}
```

Generated JSON parameter schema:

```json
{
  "session_id": {
    "description": "UUID4 returned by start_live_call.",
    "required": true,
    "type": "string"
  },
  "text": {
    "description": "Text to speak, max 4096 characters.",
    "required": true,
    "type": "string"
  },
  "turn_id": {
    "description": "Optional caller turn_id to correlate this response with a transcript turn.",
    "required": false,
    "type": "string"
  }
}
```

## `send_dtmf`

Action slug: `send-dtmf`

Price: `5` credits

Queue DTMF digits for an active live call.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `digits` | `string` | yes | DTMF digits matching ^[0-9wW#*]{1,32}$; w or W inserts a wait. |
| `session_id` | `string` | yes | UUID4 returned by start_live_call. |
| `turn_id` | `string` | no | Optional caller turn_id to correlate this DTMF command with a transcript turn. |

Sample parameters:

```json
{
  "digits": "example digits",
  "session_id": "example session id",
  "turn_id": "example turn id"
}
```

Generated JSON parameter schema:

```json
{
  "digits": {
    "description": "DTMF digits matching ^[0-9wW#*]{1,32}$; w or W inserts a wait.",
    "required": true,
    "type": "string"
  },
  "session_id": {
    "description": "UUID4 returned by start_live_call.",
    "required": true,
    "type": "string"
  },
  "turn_id": {
    "description": "Optional caller turn_id to correlate this DTMF command with a transcript turn.",
    "required": false,
    "type": "string"
  }
}
```

## `send_tts`

Action slug: `send-tts`

Price: `5` credits

Call the recipient from the credential outgoing_number and speak text using text-to-speech.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | `string` | no | Language code such as en-US. |
| `record` | `boolean` | no | Record the call. |
| `text` | `string` | yes | Text to speak, max 4096 characters. |
| `to_number` | `string` | yes | Recipient phone number in E.164 format. |
| `voice` | `string` | no | Voice name such as alice, man, woman, or Polly.Joanna. |

Sample parameters:

```json
{
  "language": "example language",
  "record": true,
  "text": "example text",
  "to_number": "example to number",
  "voice": "example voice"
}
```

Generated JSON parameter schema:

```json
{
  "language": {
    "description": "Language code such as en-US.",
    "required": false,
    "type": "string"
  },
  "record": {
    "description": "Record the call.",
    "required": false,
    "type": "boolean"
  },
  "text": {
    "description": "Text to speak, max 4096 characters.",
    "required": true,
    "type": "string"
  },
  "to_number": {
    "description": "Recipient phone number in E.164 format.",
    "required": true,
    "type": "string"
  },
  "voice": {
    "description": "Voice name such as alice, man, woman, or Polly.Joanna.",
    "required": false,
    "type": "string"
  }
}
```

## `start_ivr_call`

Action slug: `start-ivr-call`

Price: `5` credits

Initiate a multi-turn IVR session from the credential outgoing_number using a directed voice_script graph. Returns a session_id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `machine_detection` | `string` | no | Answering-machine detection mode. |
| `record` | `boolean` | no | Record the full call. |
| `send_digits` | `string` | no | DTMF digits to play once connected. |
| `timeout` | `integer` | no | Seconds to ring before giving up. |
| `to_number` | `string` | yes | Recipient phone number in E.164 format. |
| `voice_script` | `object` | yes | Voice script graph with start_node_id and nodes. Nodes support say, play, gather, hangup, and redirect. |

Sample parameters:

```json
{
  "machine_detection": "Enable",
  "record": true,
  "send_digits": "example send digits",
  "timeout": 5,
  "to_number": "example to number",
  "voice_script": {
    "nodes": [
      {}
    ],
    "start_node_id": "example start node id"
  }
}
```

Generated JSON parameter schema:

```json
{
  "machine_detection": {
    "description": "Answering-machine detection mode.",
    "enum": [
      "Enable",
      "DetectMessageEnd"
    ],
    "required": false,
    "type": "string"
  },
  "record": {
    "description": "Record the full call.",
    "required": false,
    "type": "boolean"
  },
  "send_digits": {
    "description": "DTMF digits to play once connected.",
    "required": false,
    "type": "string"
  },
  "timeout": {
    "description": "Seconds to ring before giving up.",
    "maximum": 600,
    "minimum": 5,
    "required": false,
    "type": "integer"
  },
  "to_number": {
    "description": "Recipient phone number in E.164 format.",
    "required": true,
    "type": "string"
  },
  "voice_script": {
    "description": "Voice script graph with start_node_id and nodes. Nodes support say, play, gather, hangup, and redirect.",
    "properties": {
      "nodes": {
        "description": "Voice nodes, maximum 30.",
        "items": {
          "properties": {},
          "type": "object"
        },
        "required": false,
        "type": "array"
      },
      "start_node_id": {
        "description": "ID of the first node.",
        "required": false,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  }
}
```

## `start_live_call`

Action slug: `start-live-call`

Price: `5` credits

Start a live ConversationRelay call from the credential outgoing_number, controlled by the external MCP agent. The gateway stores transcript entries and delivers queued speech or DTMF; it does not auto-respond or execute tools.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dtmf_detection` | `boolean` | no | Whether ConversationRelay should report DTMF input. |
| `interruptible` | `string` | no | ConversationRelay interruptible mode. Defaults to none when omitted. |
| `machine_detection` | `string` | no | Answering-machine detection mode. |
| `max_call_seconds` | `integer` | no | Maximum live call duration in seconds. |
| `record` | `boolean` | no | Record the call. |
| `relay_language` | `string` | no | ConversationRelay language, default en-US. |
| `relay_voice` | `string` | no | ConversationRelay TTS voice identifier. |
| `report_input_during_agent_speech` | `string` | no | Whether to report input during relayed speech. |
| `send_digits` | `string` | no | DTMF digits to play once connected, useful for bridge PINs. |
| `speech_model` | `string` | no | Provider-specific speech recognition model. |
| `timeout` | `integer` | no | Seconds to ring before giving up. |
| `to_number` | `string` | yes | Recipient or conference bridge phone number in E.164 format. |
| `transcription_provider` | `string` | no | ConversationRelay transcription provider. |
| `tts_provider` | `string` | no | ConversationRelay TTS provider. |
| `welcome_greeting` | `string` | no | Optional initial spoken greeting. |

Sample parameters:

```json
{
  "dtmf_detection": true,
  "interruptible": "none",
  "machine_detection": "Enable",
  "max_call_seconds": 30,
  "record": true,
  "relay_language": "example relay language",
  "relay_voice": "example relay voice",
  "report_input_during_agent_speech": "none"
}
```

Generated JSON parameter schema:

```json
{
  "dtmf_detection": {
    "description": "Whether ConversationRelay should report DTMF input.",
    "required": false,
    "type": "boolean"
  },
  "interruptible": {
    "description": "ConversationRelay interruptible mode. Defaults to none when omitted.",
    "enum": [
      "none",
      "dtmf",
      "speech",
      "any"
    ],
    "required": false,
    "type": "string"
  },
  "machine_detection": {
    "description": "Answering-machine detection mode.",
    "enum": [
      "Enable",
      "DetectMessageEnd"
    ],
    "required": false,
    "type": "string"
  },
  "max_call_seconds": {
    "description": "Maximum live call duration in seconds.",
    "maximum": 3600,
    "minimum": 30,
    "required": false,
    "type": "integer"
  },
  "record": {
    "description": "Record the call.",
    "required": false,
    "type": "boolean"
  },
  "relay_language": {
    "description": "ConversationRelay language, default en-US.",
    "required": false,
    "type": "string"
  },
  "relay_voice": {
    "description": "ConversationRelay TTS voice identifier.",
    "required": false,
    "type": "string"
  },
  "report_input_during_agent_speech": {
    "description": "Whether to report input during relayed speech.",
    "enum": [
      "none",
      "dtmf",
      "speech",
      "any"
    ],
    "required": false,
    "type": "string"
  },
  "send_digits": {
    "description": "DTMF digits to play once connected, useful for bridge PINs.",
    "required": false,
    "type": "string"
  },
  "speech_model": {
    "description": "Provider-specific speech recognition model.",
    "required": false,
    "type": "string"
  },
  "timeout": {
    "description": "Seconds to ring before giving up.",
    "maximum": 600,
    "minimum": 5,
    "required": false,
    "type": "integer"
  },
  "to_number": {
    "description": "Recipient or conference bridge phone number in E.164 format.",
    "required": true,
    "type": "string"
  },
  "transcription_provider": {
    "description": "ConversationRelay transcription provider.",
    "enum": [
      "Google",
      "Deepgram"
    ],
    "required": false,
    "type": "string"
  },
  "tts_provider": {
    "description": "ConversationRelay TTS provider.",
    "enum": [
      "Google",
      "Amazon",
      "ElevenLabs"
    ],
    "required": false,
    "type": "string"
  },
  "welcome_greeting": {
    "description": "Optional initial spoken greeting.",
    "required": false,
    "type": "string"
  }
}
```

## `sync_live_latency_insights`

Action slug: `sync-live-latency-insights`

Price: `5` credits

After a live call ends, import Twilio Voice Insights provider-side ConversationRelay latency events when available.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `session_id` | `string` | yes | UUID4 returned by start_live_call. |

Sample parameters:

```json
{
  "session_id": "example session id"
}
```

Generated JSON parameter schema:

```json
{
  "session_id": {
    "description": "UUID4 returned by start_live_call.",
    "required": true,
    "type": "string"
  }
}
```

## `transcribe_call`

Action slug: `transcribe-call`

Price: `5` credits

Get the transcription text for a recording if transcription was enabled.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `recording_sid` | `string` | yes | Recording SID, usually starting with RE. |

Sample parameters:

```json
{
  "recording_sid": "example recording sid"
}
```

Generated JSON parameter schema:

```json
{
  "recording_sid": {
    "description": "Recording SID, usually starting with RE.",
    "required": true,
    "type": "string"
  }
}
```

## `update_conference_participant`

Action slug: `update-conference-participant`

Price: `5` credits

Mute, unmute, hold, or unhold a conference participant.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `call_sid` | `string` | yes | Participant Call SID. |
| `conference_sid` | `string` | yes | Conference SID or friendly name. |
| `hold` | `boolean` | no | Place the participant on hold or remove hold. |
| `muted` | `boolean` | no | Mute or unmute the participant. |

Sample parameters:

```json
{
  "call_sid": "example call sid",
  "conference_sid": "example conference sid",
  "hold": true,
  "muted": true
}
```

Generated JSON parameter schema:

```json
{
  "call_sid": {
    "description": "Participant Call SID.",
    "required": true,
    "type": "string"
  },
  "conference_sid": {
    "description": "Conference SID or friendly name.",
    "required": true,
    "type": "string"
  },
  "hold": {
    "description": "Place the participant on hold or remove hold.",
    "required": false,
    "type": "boolean"
  },
  "muted": {
    "description": "Mute or unmute the participant.",
    "required": false,
    "type": "boolean"
  }
}
```
