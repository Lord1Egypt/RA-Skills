# Troubleshooting — Word

## `Word not running` or no active object

Cause:
- Word is closed
- no live instance exists to attach to

Fix:
- launch Word intentionally or attach only after confirming an open document exists

## Selection-based edit landed in the wrong place

Cause:
- wrong story range
- user cursor moved
- selection was not re-verified before write

Fix:
- re-read active document and selection context
- prefer object-based actions when possible

## Review actions fail silently

Cause:
- protected document
- track changes mode mismatch
- compatibility mode limitations

Fix:
- confirm protection state
- confirm review mode before trying accept/reject operations

## PDF export looks stale

Cause:
- fields, TOC, or references were not updated

Fix:
- update fields first
- re-export only after Word confirms the document state

## macOS script errors against Word

Cause:
- wrong terminology for the Word dictionary
- app not fully ready

Fix:
- keep scripts short
- validate document identity first
- retry only after verifying Word is frontmost and document count is correct

## `osascript` can see Word but actions still fail

Cause:
- modal dialog open
- wrong document is frontmost
- Word dictionary term does not match the intended object

Fix:
- re-read active document identity
- close or acknowledge the modal dialog
- reduce the script to the smallest reproducible action
