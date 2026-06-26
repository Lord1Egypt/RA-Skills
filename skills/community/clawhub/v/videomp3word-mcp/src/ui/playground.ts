export function renderPlaygroundHtml() {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>videomp3word MCP</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem auto; max-width: 980px; padding: 0 1rem; color: #111827; }
    textarea, input, select { width: 100%; padding: 0.75rem; margin: 0.5rem 0 1rem; border: 1px solid #d1d5db; border-radius: 8px; }
    fieldset { border: 1px solid #e5e7eb; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; }
    button { background: #111827; color: white; border: 0; padding: 0.75rem 1rem; border-radius: 8px; cursor: pointer; }
    pre { background: #0f172a; color: #e2e8f0; padding: 1rem; border-radius: 10px; overflow: auto; }
    .row { display: grid; grid-template-columns: 1fr 220px; gap: 1rem; }
  </style>
</head>
<body>
  <h1>Structured Knowledge Extraction Engine</h1>
  <p>Paste a remote media URL, choose outputs, and run the single <code>POST /video_to_knowledge</code> workflow.</p>
  <div class="row">
    <div>
      <label for="media_url">Media URL</label>
      <input id="media_url" placeholder="https://example.com/demo.mp4" />
    </div>
    <div>
      <label for="mode">Mode</label>
      <select id="mode">
        <option value="fast">fast</option>
        <option value="balanced" selected>balanced</option>
        <option value="high_accuracy">high_accuracy</option>
      </select>
    </div>
  </div>
  <fieldset>
    <legend>Outputs</legend>
    <label><input type="checkbox" name="outputs" value="summary" checked /> summary</label>
    <label><input type="checkbox" name="outputs" value="topics" checked /> topics</label>
    <label><input type="checkbox" name="outputs" value="qa" checked /> qa</label>
    <label><input type="checkbox" name="outputs" value="flashcards" checked /> flashcards</label>
    <label><input type="checkbox" name="outputs" value="tasks" checked /> tasks</label>
  </fieldset>
  <button id="run">Run</button>
  <h2>Result</h2>
  <pre id="result">{}</pre>
  <script>
    const runButton = document.getElementById('run');
    const resultNode = document.getElementById('result');
    runButton.addEventListener('click', async () => {
      const media_url = document.getElementById('media_url').value.trim();
      const mode = document.getElementById('mode').value;
      const outputs = [...document.querySelectorAll('input[name="outputs"]:checked')].map((node) => node.value);
      resultNode.textContent = 'Running...';
      try {
        const response = await fetch('/video_to_knowledge', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ media_url, outputs, mode, export_formats: ['json', 'markdown'] }),
        });
        const payload = await response.json();
        resultNode.textContent = JSON.stringify(payload, null, 2);
      } catch (error) {
        resultNode.textContent = JSON.stringify({ error: String(error) }, null, 2);
      }
    });
  </script>
</body>
</html>`;
}
