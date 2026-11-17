# ClawHub review — 2026-11-07

The registry audit described an obsolete gateway wrapper. GitHub already used direct device-code OAuth, with no gateway-token arguments or subprocess forwarding. This release publishes that source and adds regression coverage rejecting the legacy flags. Stored refresh endpoints now receive the same HTTPS xAI host validation as discovery endpoints; requests refuse redirects and new token files start with mode 0600.

The CLI accesses xAI for requested X searches and stores OAuth state locally. Ordinary mentions of X are not a request to search. No background monitor is created by this skill. Validation uses mocked endpoints and synthetic credentials, not live account data.
