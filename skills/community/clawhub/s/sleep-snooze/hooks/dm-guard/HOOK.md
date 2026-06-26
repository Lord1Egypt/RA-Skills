---
name: dm-guard
description: On every incoming message during sleep hours, queues the message content for the morning digest and pushes an auto-reply informing the sender the user is asleep.
metadata:
  openclaw:
    emoji: "💤"
    events:
      - message:received
    export: default
---

# DM Guard Hook

Fires on every `message:received` event. If sleep mode is active (computed from current time, not just the state flag), it:

1. Queues the incoming message to the SQLite queue
2. Pushes an auto-reply to `event.messages` so the sender knows the user is asleep
3. Logs the event for the morning digest

Does nothing if the user is awake, or if the message is marked urgent.
