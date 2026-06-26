# 🎮 QA Pilot Demo

## Try It Yourself

This demo includes a sample To-Do app ("TaskFlow") with intentional bugs. Use it to see how QA Pilot works in practice.

### The Challenge

The TaskFlow app was "built by an AI agent" that said it was done. But it has issues:

1. ❌ **Missing filter** — The About page claims "Filter tasks by status" but no filter exists
2. ❌ **Settings don't apply** — Default Priority setting is ignored when adding tasks
3. ❌ **Settings don't load** — Saved settings aren't reflected when opening Settings page
4. ❌ **No delete confirmation** — Clicking × instantly deletes with no undo

### How to Test

1. Open `demo/taskflow-app.html` in your browser
2. Read the SKILL.md methodology
3. Follow the 5 phases on the TaskFlow app
4. Try to find all 4 issues without reading the source code comments

### After QA Pilot

The same app with all fixes applied is available at the hosted version — compare to see the difference QA Pilot makes.

### Give It to Your Agent

Copy this prompt to see how your AI agent handles testing:

```
I built a todo app at demo/taskflow-app.html. 
Please follow the QA Pilot methodology in SKILL.md 
to test it. Find and fix any issues before telling me it's done.
```

---

*See the difference between "I'm done" and "I tested it and it actually works."*
