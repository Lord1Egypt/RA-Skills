# Local Home

The store is private, schema-versioned, and local to the current user. It contains
one home, rooms, devices, groups, scenes, schedules, and bounded incomplete-operation
records. It never stores credentials, conversation transcripts, raw packets, full
TCP responses, or cloud/Pro identifiers.

The protocol `id` is the identity key. IP/port is observed metadata only. Refresh
updates a same-endpoint record, marks missing devices offline/stale, and preserves
all user relationships. A changed endpoint creates a short-lived one-time rebind
challenge bound to the candidate and store revision. Confirming it consumes the
challenge atomically; a new candidate, revision change, expiry, or replay fails.

Rooms are one-to-many device assignments. Groups are independent many-to-many sets;
a device may belong to several groups. A group requires at least two devices with an
identical normalized control fingerprint. Group deletion never removes devices.

Local batches use a writer lock, revision check, atomic replacement, and a last-known-
good backup. Corruption fails closed rather than silently clearing the home. Export
is sanitized by default.
