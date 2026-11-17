# Installing Reelary

If the `reelary_*` tools are missing, Reelary is not installed or not connected.

1. Tell the user what will happen and ask before running anything: "Reelary is a local app that indexes your footage on this computer. Install it with `npx reelary`? It downloads the signed app from reelary.app, runs it in the background with a tray icon, and connects it to your AI apps."
2. Only after they agree, run `npx -y reelary --yes`.
3. Restart the AI client if it was Claude Desktop, then call `reelary_status`.

Without MCP (for example inside a sandbox that cannot load MCP servers) the same actions work from a shell:

    npx -y reelary status
    npx -y reelary index ~/Movies
    npx -y reelary search "drone shot of a coastline" --json
    npx -y reelary cut "Sunrise over the city. Coffee being poured." --aspect 9:16 --save "Morning"
    npx -y reelary export <project_id>

Requirements: macOS 12+ (Apple Silicon or Intel) or Windows 10/11 x64. The Mac App Store and Microsoft Store versions cannot run in the background for agents; the direct version from reelary.app can (same library, same license).
