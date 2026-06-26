# Visual-Explainer: Serve Report

Serve the visual-explainer skill report from an HTTP server for network access.

## Use Cases

1. Share reports with team members on the same network
2. View reports on mobile devices
3. Present reports on a larger screen

## Command

```bash
cd visual-explainer && python3 -m http.server 8080 --directory templates
```

## Access

- **Localhost:** `http://localhost:8080`
- **Network:** `http://192.168.50.60:8080` (on other hosts)

## File Listing

To open the main report in any view:

```bash
http://192.168.50.60:8080/visual-explainer-skill-report.html
```

To view changelog:

```bash
http://192.168.50.60:8080/CHANGELOG.md
```

## Alternative: Node.js (if Python not available)

```bash
cd visual-explainer/templates
npx serve .
```

## Troubleshooting

- **If port is in use:** Kill using `lsof -ti:8080|xargs kill -9` or use a different port
- **For HTTPS:** Use an SSL tunnel like `ngrok http 8080`