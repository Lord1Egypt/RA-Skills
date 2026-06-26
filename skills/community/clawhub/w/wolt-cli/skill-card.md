## Description: <br>
Use Nikita's local Wolt CLI to browse venues, inspect menus and item options, and run profile, cart, and checkout-preview actions for wolt.com from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mekedron](https://clawhub.ai/user/mekedron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate a local Wolt CLI for venue discovery, menu inspection, item option resolution, basket management, profile checks, and checkout previews. It is useful when automating Wolt browsing or account workflows while keeping final order placement outside the skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle sensitive Wolt account credentials, cookies, profile details, addresses, payments, orders, and cart state. <br>
Mitigation: Install only from a trusted publisher, avoid exposing tokens or cookies in shell history or logs, use masked payment output, and keep verbose diagnostics private. <br>
Risk: Some supported commands can mutate carts, favorites, addresses, or local profile credentials. <br>
Mitigation: Start with read-only discovery and require explicit user confirmation before running cart, favorite, address, or configure commands. <br>
Risk: Checkout preview may be mistaken for placing an order. <br>
Mitigation: Present checkout preview only as a pricing and basket validation step and never describe it as final order placement. <br>


## Reference(s): <br>
- [Command Reference](references/command-reference.md) <br>
- [Workflows](references/workflows.md) <br>
- [Output and Errors](references/output-and-errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON parsing notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers machine-readable JSON output and surfaces warnings or error envelopes to the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
