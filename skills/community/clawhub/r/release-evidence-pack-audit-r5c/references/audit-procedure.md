# Pack audit procedure

The batch archive is `references/batch-evidence.pack` in this folder. It is a standard gzip container holding one JSON document (the payload) that describes the batch and carries a case identifier.

## Figures recorded on the card

| Item | How it is obtained |
| --- | --- |
| `payload_sha256` | SHA-256, lowercase hex, of the payload bytes after decompression (not of the pack file) |
| `payload_bytes` | length in bytes of the same decompressed payload |
| `case` | the `case` value inside the payload |

## Card line

`Pack audit: payload_sha256=<64 hex>; payload_bytes=<integer>; case=<case value>`

## Why the figures are derived rather than copied

The archive digest is recorded in the batch record, but the payload digest and payload size are not stored anywhere: they are properties of the decompressed bytes only. Text tools cannot read the pack directly, so the payload has to be unpacked before the two figures can be taken. A line filled with the format text, or with the archive's own digest, does not match a re-derived value and is marked as unaudited.
