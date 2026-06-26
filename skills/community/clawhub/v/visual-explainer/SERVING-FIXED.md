# Fix: Port Already in Use Error

If you're seeing the error:
```
OSError: [Errno 98] Address already in use
```

**Try this instead:**

```bash
cd visual-explainer
./scripts/serve-report-best-port.sh
```

This will:
1. ✅ Check ports 8080, 8081, 8082, 8083, ...
2. ✅ Find and use the first available port
3. ✅ Run server in background
4. ✅ Display the port number and URLs

**Then open in your browser:**
```
http://192.168.50.60:<PORT>/visual-explainer-skill-report.html
```

## If You Still Get Port in Use

Kill all Python HTTP servers:
```bash
cd visual-explainer
./scripts/clean-server.sh
```

Then start fresh:
```bash
./scripts/serve-report-best-port.sh
```