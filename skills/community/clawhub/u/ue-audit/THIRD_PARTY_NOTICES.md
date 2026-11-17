# Third-party notices

`ue-audit` has no third-party runtime dependencies in v0.4.0. It uses only the Python standard library.

Optional live mode talks to a locally running HTTP editor bridge. That bridge is not bundled with `ue-audit`; it is installed, configured, and licensed separately by the user. The bridge token is supplied through `--token`, `UE_AUDIT_BRIDGE_TOKEN`, `UE_AUDIT_BRIDGE_TOKEN_FILE`, or `%APPDATA%\ue-audit\bridge-token`.

The test suite uses `pytest` when run by a developer; `pytest` is not a runtime dependency.

The project is licensed under Apache-2.0. See `LICENSE`.
