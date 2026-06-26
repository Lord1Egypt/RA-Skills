# Serving Visual-Explainer Reports

Quick guide to serving visual reports on your local network.

## Quick Start

### From within visual-explainer directory:

```bash
cd visual-explainer
python3 -m http.server 8080 --directory templates
```

Then open `http://192.168.50.60:8080/visual-explainer-skill-report.html` in any browser.

### Using the convenience script:

```bash
cd visual-explainer
./scripts/serve-report.sh
```

## Available Files

- **Main report:** `visual-explainer-skill-report.html` — Full skill documentation with all components
- **Template examples:**
  - `templates/architecture.html` — CSS Grid architecture layout
  - `templates/mermaid-flowchart.html` — Interactive flowcharts
  - `templates/data-table.html` — Data tables with KPI cards
  - `templates/slide-deck.html` — Slide deck preset
- **Markdown docs:**
  - `CHANGELOG.md` — Version history
  - `README.md` — Overview
  - `references/libraries.md` — Library documentation
  - `references/css-patterns.md` — CSS patterns
  - `references/responsive-nav.md` — Navigation patterns

## Troubleshooting

### Port 8080 Already in Use

Use a different port:

```bash
python3 -m http.server 8090 --directory templates
```

Or kill the existing process:

```bash
lsof -ti:8080 | xargs kill -9
```

### Network Access Issues

1. Check if firewall is blocking port 8080:
```bash
firewall-cmd --list-ports  # Fedora
sudo ufw status            # Ubuntu
```

2. Check network configuration:

```bash
ip addr show  # Linux
ifconfig      # macOS (if installed)
```

## Alternative Methods

### Using Node.js (if Python not available):

```bash
cd visual-explainer/templates
npx serve .
```

### Using PHP's built-in server:

```bash
cd visual-explainer/templates
php -S 0.0.0.0:8080
```

### Using ngrok (for shareable public links):

```bash
cd visual-explainer/templates
ngrok http 8080
```

Copy the public HTTPS URL to share your report anywhere.