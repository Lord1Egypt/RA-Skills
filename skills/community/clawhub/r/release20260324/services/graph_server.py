"""Lightweight HTTP server for interactive graph management.

Serves the HTML graph viewer and provides REST APIs for:
- Adding papers (title / BibTeX / PDF, seed or non-seed)
- Converting nodes to seed papers
- Reading / writing graph JSON

Usage:
    python -m services.graph_server graph.json --port 8787
    # or via CLI: python openpapergraph_cli.py serve graph.json --port 8787

No extra dependencies — uses Python stdlib http.server + json.
"""
import cgi
import io
import json
import os
import sys
import tempfile
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

# Ensure parent is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas import GraphData, Paper
from services.graph_manager import (
    resolve_paper_by_title,
    resolve_paper_by_bibtex,
    resolve_paper_from_pdf,
    expand_as_seed,
    add_non_seed,
    convert_to_seed,
    find_existing,
    save_graph,
    enrich_incomplete_papers,
    RateLimitError,
)
from services.html_export import generate_html

# Global progress tracker for SSE
import threading
_progress = {"step": "", "detail": "", "pct": 0, "done": False}
_progress_lock = threading.Lock()

def set_progress(step: str, detail: str = "", pct: int = 0, done: bool = False):
    with _progress_lock:
        _progress["step"] = step
        _progress["detail"] = detail
        _progress["pct"] = pct
        _progress["done"] = done


class GraphHandler(BaseHTTPRequestHandler):
    """HTTP handler for graph management APIs + HTML serving."""

    graph: GraphData = None
    graph_path: str = ""
    html_title: str = "Paper Graph"

    def log_message(self, format, *args):
        print(f"[serve] {args[0]}", file=sys.stderr)

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html_response(self, html_content):
        body = html_content.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            # Serve the interactive HTML with server-aware JS injected
            html = generate_html(
                GraphHandler.graph,
                title=GraphHandler.html_title,
                inline_js=False,
            )
            # Inject server-mode: (1) set flag at top, (2) add UI code at bottom
            html = html.replace("var SERVER_MODE = false;", "var SERVER_MODE = true;")
            server_js = _server_mode_js()
            html = html.replace("</script>\n</body>", server_js + "\n</script>\n</body>")
            self._html_response(html)

        elif path == "/api/graph":
            self._json_response(GraphHandler.graph.to_dict())

        elif path == "/api/health":
            self._json_response({"status": "ok", "graph_path": GraphHandler.graph_path})

        elif path == "/api/progress":
            # SSE endpoint for real-time progress
            import time as _time
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self._cors_headers()
            self.end_headers()
            try:
                while True:
                    with _progress_lock:
                        data = json.dumps(_progress)
                        is_done = _progress["done"]
                    self.wfile.write(f"data: {data}\n\n".encode())
                    self.wfile.flush()
                    if is_done:
                        break
                    _time.sleep(0.5)
            except (BrokenPipeError, ConnectionResetError):
                pass

        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path

        try:
            if path == "/api/add-paper":
                self._handle_add_paper()
            elif path == "/api/add-paper-pdf":
                self._handle_add_paper_pdf()
            elif path == "/api/convert-to-seed":
                self._handle_convert_to_seed()
            elif path == "/api/delete-source":
                self._handle_delete_source()
            elif path == "/api/enrich":
                from services.graph_manager import enrich_metadata
                result = enrich_metadata(GraphHandler.graph, GraphHandler.graph_path)
                self._json_response({"status": "ok", **result})
            elif path == "/api/save":
                save_graph(GraphHandler.graph, GraphHandler.graph_path)
                self._json_response({"status": "ok", "message": "Graph saved"})
            else:
                self.send_error(404)
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            self._json_response({"status": "error", "message": str(e)}, status=500)

    def _handle_add_paper(self):
        set_progress("init", "Resolving paper...", 5)
        body = json.loads(self._read_body())
        input_type = body.get("type", "title")  # "title" | "bibtex"
        value = body.get("value", "").strip()
        is_seed = body.get("is_seed", False)

        if not value:
            self._json_response({"status": "error", "message": "No input provided"}, 400)
            return

        paper = None
        pdf_refs = []

        try:
            if input_type == "bibtex":
                paper = resolve_paper_by_bibtex(value)
            elif input_type == "title":
                paper = resolve_paper_by_title(value)
            else:
                self._json_response({"status": "error", "message": f"Unknown type: {input_type}"}, 400)
                return
        except RateLimitError as e:
            sources = ", ".join(e.sources)
            wait_times = {
                "arXiv": "~3 minutes",
                "Semantic Scholar": "~5 minutes",
                "Google Scholar": "~10 minutes",
            }
            wait_msg = "; ".join(f"{s}: {wait_times.get(s, '~5 min')}" for s in e.sources)
            set_progress("error", f"Rate limited by {sources}", 0, done=True)
            self._json_response({
                "status": "rate_limited",
                "message": f"All search sources are rate limited ({sources}). Please wait and retry. Estimated wait: {wait_msg}. Alternatively, use BibTeX or PDF upload which don't require search APIs.",
                "sources": e.sources,
            }, 429)
            return

        if not paper:
            set_progress("error", "Could not resolve paper", 0, done=True)
            self._json_response({
                "status": "error",
                "message": f"Could not resolve paper from {input_type} input. The paper may not be indexed by arXiv or Semantic Scholar. Try adding via BibTeX or PDF upload instead.",
            }, 404)
            return

        set_progress("init", f"Resolved: {(paper.title or 'Unknown')[:50]}", 15)

        # Check if already exists — 5 cases
        existing = find_existing(GraphHandler.graph, paper)

        # Case 1: non-seed add, already exists → just notify
        if existing and not is_seed:
            set_progress("done", "Paper already in graph", 100, done=True)
            self._json_response({
                "status": "exists",
                "paper_id": existing.id,
                "paper_title": existing.title,
                "message": f"Paper \"{existing.title}\" already exists in graph",
            })
            return

        # Case 4: seed add, already is seed → just notify
        if existing and is_seed and existing.is_seed:
            set_progress("done", "Already a seed paper", 100, done=True)
            self._json_response({
                "status": "exists",
                "paper_id": existing.id,
                "paper_title": existing.title,
                "message": f"Paper \"{existing.title}\" is already a seed paper",
            })
            return

        # Case 3: seed add, exists as non-seed → convert to seed
        if existing and is_seed and not existing.is_seed:
            set_progress("converting", f"Converting existing paper to seed: {existing.title[:50]}", 20)
            result = convert_to_seed(GraphHandler.graph, existing.id, GraphHandler.graph_path)
            result["message"] = f"Paper \"{existing.title}\" was already in graph — converted to seed and expanded"
            result["converted"] = True
            self._json_response(result)
            return

        # Case 2 & 5: new paper
        if is_seed:
            result = expand_as_seed(GraphHandler.graph, paper, GraphHandler.graph_path)
        else:
            result = add_non_seed(GraphHandler.graph, paper, GraphHandler.graph_path)

        self._json_response(result)

    def _handle_add_paper_pdf(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._json_response({"status": "error", "message": "Expected multipart/form-data"}, 400)
            return

        # Parse multipart form data
        environ = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': content_type,
            'CONTENT_LENGTH': self.headers.get('Content-Length', '0'),
        }
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ=environ,
        )

        is_seed = form.getfirst("is_seed", "false").lower() in ("true", "1", "yes")

        pdf_field = form["file"] if "file" in form else None
        if pdf_field is None or getattr(pdf_field, "file", None) is None:
            self._json_response({"status": "error", "message": "No PDF file uploaded"}, 400)
            return

        # Save to temp file
        pdf_data = pdf_field.file.read()
        if len(pdf_data) < 100:
            self._json_response({"status": "error", "message": f"PDF file appears empty ({len(pdf_data)} bytes)"}, 400)
            return

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_data)
            tmp_path = tmp.name
        print(f"[serve] PDF uploaded: {len(pdf_data)} bytes -> {tmp_path}", file=sys.stderr)
        set_progress("pdf", "Parsing PDF and extracting references...", 10)

        try:
            paper, pdf_refs = resolve_paper_from_pdf(tmp_path)
            set_progress("pdf", f"Identified paper: {(paper.title or 'Unknown')[:50]}. {len(pdf_refs)} refs resolved.", 30)

            # Check if already exists — same 5 cases as title/bibtex
            existing = find_existing(GraphHandler.graph, paper)

            # Case 1: non-seed add, already exists
            if existing and not is_seed:
                set_progress("done", "Paper already in graph", 100, done=True)
                self._json_response({
                    "status": "exists",
                    "paper_id": existing.id,
                    "paper_title": existing.title,
                    "message": f"Paper \"{existing.title}\" already exists in graph",
                })
                return

            # Case 4: seed add, already is seed
            if existing and is_seed and existing.is_seed:
                set_progress("done", "Already a seed paper", 100, done=True)
                self._json_response({
                    "status": "exists",
                    "paper_id": existing.id,
                    "paper_title": existing.title,
                    "message": f"Paper \"{existing.title}\" is already a seed paper",
                })
                return

            # Case 3: seed add, exists as non-seed → convert to seed
            if existing and is_seed and not existing.is_seed:
                set_progress("converting", f"Converting existing paper to seed: {existing.title[:50]}", 20)
                result = convert_to_seed(GraphHandler.graph, existing.id, GraphHandler.graph_path)
                result["message"] = f"Paper \"{existing.title}\" was already in graph — converted to seed and expanded"
                result["converted"] = True
                self._json_response(result)
                return

            # Case 2 & 5: new paper
            if is_seed:
                result = expand_as_seed(
                    GraphHandler.graph, paper, GraphHandler.graph_path,
                    pre_parsed_refs=pdf_refs,
                )
            else:
                result = add_non_seed(GraphHandler.graph, paper, GraphHandler.graph_path,
                                      pre_parsed_refs=pdf_refs)

            self._json_response(result)
        finally:
            os.unlink(tmp_path)

    def _handle_convert_to_seed(self):
        set_progress("init", "Starting conversion...", 5)
        body = json.loads(self._read_body())
        paper_id = body.get("paper_id", "")

        if not paper_id:
            self._json_response({"status": "error", "message": "No paper_id provided"}, 400)
            return

        result = convert_to_seed(GraphHandler.graph, paper_id, GraphHandler.graph_path)
        self._json_response(result)

    def _handle_delete_source(self):
        body = json.loads(self._read_body())
        seed_id = body.get("seed_id", "")

        if not seed_id:
            self._json_response({"status": "error", "message": "No seed_id provided"}, 400)
            return

        stats = GraphHandler.graph.remove_seed(seed_id)
        save_graph(GraphHandler.graph, GraphHandler.graph_path)
        self._json_response({
            "status": "ok",
            "message": f"Removed seed and {stats['removed_nodes']} exclusive papers",
            **stats,
        })


def _server_mode_js():
    """JavaScript injected into HTML when served by graph_server.

    Adds:
    - Add Paper button + modal
    - Convert to Seed button in tooltip/detail
    - API client functions
    - Graph reload after mutations
    """
    return '''
// ====== Server Mode: Interactive Graph Management ======
// SERVER_MODE already set to true via template replacement
const API_BASE = window.location.origin;

// ====== Add Paper Modal Styles ======
(function() {
  const style = document.createElement("style");
  style.textContent = `
    .add-paper-btn {
      padding: 6px 14px; border: 1px solid #4361EE; border-radius: 8px;
      background: #4361EE; color: #fff; cursor: pointer; font-size: 12px;
      font-weight: 500; transition: all 0.15s; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .add-paper-btn:hover { background: #3651D4; }
    .modal-overlay {
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.4); z-index: 500;
      display: flex; align-items: center; justify-content: center;
    }
    .modal-dialog {
      background: #fff; border-radius: 12px; padding: 0; width: 500px; max-width: 90vw;
      box-shadow: 0 20px 60px rgba(0,0,0,0.2); overflow: hidden;
    }
    .modal-header {
      padding: 16px 20px; background: #4361EE; color: #fff;
      display: flex; justify-content: space-between; align-items: center;
    }
    .modal-header h3 { font-size: 15px; font-weight: 600; margin: 0; }
    .modal-close { background: none; border: none; color: rgba(255,255,255,0.8); font-size: 20px; cursor: pointer; padding: 4px 8px; }
    .modal-close:hover { color: #fff; }
    .modal-body { padding: 20px; }
    .modal-body label { display: block; font-size: 13px; font-weight: 600; color: #1A1A2E; margin-bottom: 6px; }
    .modal-body .input-group { margin-bottom: 16px; }
    .modal-body input[type="text"], .modal-body textarea {
      width: 100%; padding: 10px 12px; border: 1px solid #E8ECF0; border-radius: 8px;
      font-size: 13px; outline: none; transition: border 0.15s; background: #FAFBFC;
      font-family: inherit;
    }
    .modal-body input:focus, .modal-body textarea:focus { border-color: #4361EE; background: #fff; }
    .modal-body textarea { min-height: 80px; resize: vertical; font-family: "SF Mono", "Fira Code", monospace; font-size: 12px; }
    .modal-body .file-drop {
      border: 2px dashed #E8ECF0; border-radius: 8px; padding: 20px; text-align: center;
      cursor: pointer; transition: all 0.15s; color: #94A3B8; font-size: 13px;
    }
    .modal-body .file-drop:hover, .modal-body .file-drop.dragover { border-color: #4361EE; background: #F0F4FF; color: #4361EE; }
    .modal-body .file-drop input[type="file"] { display: none; }
    .modal-tabs { display: flex; border-bottom: 2px solid #E8ECF0; margin-bottom: 16px; }
    .modal-tab {
      flex: 1; padding: 8px 12px; text-align: center; cursor: pointer;
      font-size: 12px; font-weight: 500; color: #94A3B8;
      border: none; background: none; border-bottom: 2px solid transparent;
      margin-bottom: -2px; transition: all 0.15s;
    }
    .modal-tab:hover { color: #4361EE; }
    .modal-tab.active { color: #4361EE; border-bottom-color: #4361EE; font-weight: 600; }
    .seed-toggle { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; padding: 12px; background: #F8F9FA; border-radius: 8px; }
    .seed-toggle input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; accent-color: #6C5CE7; }
    .seed-toggle .toggle-label { font-size: 13px; font-weight: 600; color: #1A1A2E; }
    .seed-toggle .toggle-desc { font-size: 11px; color: #64748B; margin-top: 2px; }
    .modal-footer { padding: 12px 20px; border-top: 1px solid #E8ECF0; display: flex; justify-content: flex-end; gap: 8px; }
    .modal-footer button {
      padding: 8px 20px; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.15s;
    }
    .btn-modal-cancel { border: 1px solid #E8ECF0; background: #fff; color: #64748B; }
    .btn-modal-cancel:hover { border-color: #4361EE; color: #4361EE; }
    .btn-modal-submit { border: none; background: #4361EE; color: #fff; }
    .btn-modal-submit:hover { background: #3651D4; }
    .btn-modal-submit:disabled { opacity: 0.5; cursor: not-allowed; }
    .progress-bar { height: 6px; background: #E8ECF0; border-radius: 3px; margin-top: 8px; overflow: hidden; }
    .progress-bar .fill { height: 100%; background: #4361EE; border-radius: 3px; transition: width 0.3s ease; width: 0%; }
    .result-msg { padding: 10px 14px; border-radius: 8px; font-size: 13px; margin-top: 12px; }
    .result-msg.success { background: #E6FFF0; color: #00875A; border: 1px solid #ABF5D1; }
    .result-msg.error { background: #FFF0F0; color: #DE350B; border: 1px solid #FFBDAD; }
    .result-msg.info { background: #E6F4FF; color: #0052CC; border: 1px solid #B3D4FF; }
    .convert-seed-btn {
      margin-top: 6px; padding: 4px 10px; border: 1px solid #6C5CE7; border-radius: 6px;
      background: #fff; color: #6C5CE7; font-size: 11px; cursor: pointer;
      font-weight: 500; transition: all 0.15s;
    }
    .convert-seed-btn:hover { background: #6C5CE7; color: #fff; }
  `;
  document.head.appendChild(style);
})();

// ====== Add "Add Paper" button to toolbar ======
(function() {
  const toolbar = document.querySelector(".toolbar");
  const statsDiv = toolbar.querySelector(".toolbar-stats");

  const btn = document.createElement("button");
  btn.className = "add-paper-btn";
  btn.textContent = "+ Add Paper";
  btn.onclick = openAddPaperModal;
  toolbar.insertBefore(btn, statsDiv);
})();

// ====== Add Paper Modal ======
let addPaperModal = null;
let currentInputTab = "title";
let selectedPdfFile = null;

function openAddPaperModal() {
  if (addPaperModal) addPaperModal.remove();

  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.id = "add-paper-overlay";

  overlay.innerHTML = `
    <div class="modal-dialog">
      <div class="modal-header">
        <h3>Add Paper to Graph</h3>
        <button class="modal-close" onclick="closeAddPaperModal()">&times;</button>
      </div>
      <div class="modal-body">
        <div class="modal-tabs">
          <button class="modal-tab active" onclick="switchInputTab('title')">Title</button>
          <button class="modal-tab" onclick="switchInputTab('bibtex')">BibTeX</button>
          <button class="modal-tab" onclick="switchInputTab('pdf')">PDF</button>
        </div>

        <div id="input-title" class="input-group">
          <label>Paper Title</label>
          <input type="text" id="paper-title-input" placeholder="e.g. Attention Is All You Need">
        </div>

        <div id="input-bibtex" class="input-group" style="display:none">
          <label>BibTeX Entry</label>
          <textarea id="paper-bibtex-input" placeholder="@article{...}"></textarea>
        </div>

        <div id="input-pdf" class="input-group" style="display:none">
          <label>Upload PDF</label>
          <div class="file-drop" id="pdf-drop" onclick="document.getElementById('pdf-file-input').click()">
            <input type="file" id="pdf-file-input" accept=".pdf" onchange="handlePdfSelect(event)">
            <p id="pdf-drop-text">Click or drag PDF here</p>
          </div>
        </div>

        <div class="seed-toggle">
          <input type="checkbox" id="seed-checkbox">
          <div>
            <div class="toggle-label">Treat as Seed Paper</div>
            <div class="toggle-desc">Seed papers trigger full expansion: references parsing + multi-source citation search. Non-seed papers only check relationships with existing seeds.</div>
          </div>
        </div>

        <div id="add-paper-progress" style="display:none">
          <div class="progress-bar"><div class="fill"></div></div>
          <p style="font-size:12px;color:#64748B;margin-top:8px;text-align:center" id="progress-text">Resolving paper...</p>
        </div>

        <div id="add-paper-result" style="display:none"></div>
      </div>
      <div class="modal-footer">
        <button class="btn-modal-cancel" onclick="closeAddPaperModal()">Cancel</button>
        <button class="btn-modal-submit" id="btn-add-submit" onclick="submitAddPaper()">Add to Graph</button>
      </div>
    </div>
  `;

  document.body.appendChild(overlay);
  addPaperModal = overlay;

  // Setup PDF drag-and-drop
  const dropZone = document.getElementById("pdf-drop");
  dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("dragover"); });
  dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0 && e.dataTransfer.files[0].name.endsWith(".pdf")) {
      selectedPdfFile = e.dataTransfer.files[0];
      document.getElementById("pdf-drop-text").textContent = selectedPdfFile.name;
    }
  });

  // Focus title input
  setTimeout(() => document.getElementById("paper-title-input")?.focus(), 100);
}

function closeAddPaperModal() {
  if (addPaperModal) { addPaperModal.remove(); addPaperModal = null; }
  selectedPdfFile = null;
}

function switchInputTab(tab) {
  currentInputTab = tab;
  document.querySelectorAll(".modal-tab").forEach((t, i) => {
    t.classList.toggle("active", ["title","bibtex","pdf"][i] === tab);
  });
  document.getElementById("input-title").style.display = tab === "title" ? "" : "none";
  document.getElementById("input-bibtex").style.display = tab === "bibtex" ? "" : "none";
  document.getElementById("input-pdf").style.display = tab === "pdf" ? "" : "none";
}

function handlePdfSelect(event) {
  if (event.target.files.length > 0) {
    selectedPdfFile = event.target.files[0];
    document.getElementById("pdf-drop-text").textContent = selectedPdfFile.name;
  }
}

async function submitAddPaper() {
  const isSeed = document.getElementById("seed-checkbox").checked;
  const progressDiv = document.getElementById("add-paper-progress");
  const resultDiv = document.getElementById("add-paper-result");
  const submitBtn = document.getElementById("btn-add-submit");
  const progressText = document.getElementById("progress-text");

  progressDiv.style.display = "";
  resultDiv.style.display = "none";
  submitBtn.disabled = true;
  progressText.textContent = isSeed ? "Resolving paper and expanding graph..." : "Resolving paper...";
  const progressFill = progressDiv.querySelector(".fill");
  if (progressFill) progressFill.style.width = "5%";

  // Start SSE progress listener
  let evtSource = null;
  if (isSeed) {
    try {
      evtSource = new EventSource(API_BASE + "/api/progress");
      evtSource.onmessage = function(e) {
        try {
          const p = JSON.parse(e.data);
          if (progressFill) progressFill.style.width = p.pct + "%";
          if (progressText && p.detail) progressText.textContent = p.detail;
          if (p.done) { evtSource.close(); evtSource = null; }
        } catch(_) {}
      };
    } catch(_) {}
  }

  try {
    let response;

    if (currentInputTab === "pdf" && selectedPdfFile) {
      const formData = new FormData();
      formData.append("file", selectedPdfFile);
      formData.append("is_seed", isSeed ? "true" : "false");
      response = await fetch(API_BASE + "/api/add-paper-pdf", { method: "POST", body: formData });
    } else {
      const value = currentInputTab === "title"
        ? document.getElementById("paper-title-input").value.trim()
        : document.getElementById("paper-bibtex-input").value.trim();
      if (!value) {
        showAddResult("error", "Please provide input");
        submitBtn.disabled = false;
        progressDiv.style.display = "none";
        return;
      }
      response = await fetch(API_BASE + "/api/add-paper", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: currentInputTab, value, is_seed: isSeed }),
      });
    }

    const result = await response.json();
    if (evtSource) { evtSource.close(); evtSource = null; }
    progressDiv.style.display = "none";
    submitBtn.disabled = false;

    if (result.status === "ok") {
      const msg = result.converted
        ? (result.message || "Paper converted to seed and expanded")
        : `Added "${result.paper_title}" — ${result.new_nodes || 0} new papers, ${result.new_edges || 0} new edges.`;
      showAddResult("success", msg);
      showToast(msg);
      setTimeout(() => { window.location.reload(); }, 1000);
    } else if (result.status === "already_expanded") {
      showAddResult("info", `"${result.paper_title}" is already in graph as a seed paper (${result.total_nodes} papers, ${result.total_edges} edges).`);
    } else if (result.status === "exists") {
      showAddResult("info", result.message || "Paper already exists in graph");
    } else if (result.status === "rate_limited") {
      showAddResult("error", result.message || "Search APIs are rate limited. Please wait a few minutes and try again, or use BibTeX/PDF upload.");
    } else {
      showAddResult("error", result.message || "Failed to add paper");
    }
  } catch (err) {
    progressDiv.style.display = "none";
    submitBtn.disabled = false;
    showAddResult("error", "Request failed: " + err.message);
  }
}

function showAddResult(type, msg) {
  const div = document.getElementById("add-paper-result");
  div.style.display = "";
  div.innerHTML = '<div class="result-msg ' + type + '">' + escapeHtml(msg) + '</div>';
}

// ====== Convert to Seed ======
// Modify the tooltip to include "Convert to Seed" button for non-seed nodes
const _origShowTooltip = showTooltip;
showTooltip = function(pid, event) {
  _origShowTooltip(pid, event);
  // Add convert button if not already a seed and in server mode
  if (!SEED_SET.has(pid)) {
    const tooltip = document.getElementById("node-tooltip");
    const btn = document.createElement("button");
    btn.className = "convert-seed-btn";
    btn.textContent = "\\u2B06 Convert to Seed Paper";
    btn.style.pointerEvents = "auto";
    btn.onclick = function(e) {
      e.stopPropagation();
      confirmConvertToSeed(pid);
    };
    // Make tooltip temporarily interactive
    tooltip.style.pointerEvents = "auto";
    tooltip.appendChild(btn);
  }
};

function confirmConvertToSeed(pid) {
  const p = paperById[pid];
  const name = p ? (p.title || "Untitled").substring(0, 60) : pid;
  hideTooltip();

  const overlay = document.createElement("div");
  overlay.className = "confirm-overlay";
  overlay.innerHTML = `
    <div class="confirm-dialog">
      <h4>Convert to Seed Paper?</h4>
      <p>This will upgrade <strong>${escapeHtml(name)}</strong> to a seed paper and expand the graph with its references and citations. Changes will be saved to JSON.</p>
      <div id="convert-progress" style="display:none">
        <div class="progress-bar"><div class="fill" id="convert-fill"></div></div>
        <p style="font-size:12px;color:#64748B;margin-top:8px" id="convert-progress-text">Expanding graph...</p>
      </div>
      <div class="btn-group" id="convert-buttons">
        <button class="btn-cancel" id="convert-cancel">Cancel</button>
        <button class="btn-danger" id="convert-confirm" style="background:#6C5CE7">Convert & Expand</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  overlay.querySelector("#convert-cancel").addEventListener("click", () => overlay.remove());
  overlay.querySelector("#convert-confirm").addEventListener("click", async () => {
    const buttons = overlay.querySelector("#convert-buttons");
    const progress = overlay.querySelector("#convert-progress");
    const convertFill = overlay.querySelector("#convert-fill");
    const convertText = overlay.querySelector("#convert-progress-text");
    buttons.style.display = "none";
    progress.style.display = "";
    if (convertFill) convertFill.style.width = "5%";

    // Start SSE progress listener
    let evtSrc = null;
    try {
      evtSrc = new EventSource(API_BASE + "/api/progress");
      evtSrc.onmessage = function(e) {
        try {
          const p = JSON.parse(e.data);
          if (convertFill) convertFill.style.width = p.pct + "%";
          if (convertText && p.detail) convertText.textContent = p.detail;
          if (p.done) { evtSrc.close(); evtSrc = null; }
        } catch(_) {}
      };
    } catch(_) {}

    try {
      const resp = await fetch(API_BASE + "/api/convert-to-seed", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ paper_id: pid }),
      });
      const result = await resp.json();
      if (evtSrc) { evtSrc.close(); evtSrc = null; }
      overlay.remove();

      if (result.status === "ok") {
        showToast("Converted to seed: +" + (result.new_nodes || 0) + " papers, +" + (result.new_edges || 0) + " edges");
        setTimeout(() => window.location.reload(), 1000);
      } else {
        showToast(result.message || "Conversion failed");
      }
    } catch (err) {
      if (evtSrc) { evtSrc.close(); evtSrc = null; }
      overlay.remove();
      showToast("Error: " + err.message);
    }
  });
}
'''


def start_server(graph_path: str, port: int = 8787, title: str = "Paper Graph"):
    """Start the graph management server."""
    if not os.path.exists(graph_path):
        print(f"[serve] Error: graph file not found: {graph_path}", file=sys.stderr)
        sys.exit(1)

    GraphHandler.graph = GraphData.load(graph_path)
    GraphHandler.graph_path = os.path.abspath(graph_path)
    GraphHandler.html_title = title

    print(f"[serve] Loaded graph: {GraphHandler.graph.total_papers} papers, "
          f"{len(GraphHandler.graph.edges)} edges", file=sys.stderr)
    print(f"[serve] Graph file: {GraphHandler.graph_path}", file=sys.stderr)
    print(f"[serve] Starting server on http://localhost:{port}", file=sys.stderr)
    print(f"[serve] Open http://localhost:{port} in your browser", file=sys.stderr)

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        daemon_threads = True

    server = ThreadedHTTPServer(("0.0.0.0", port), GraphHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[serve] Server stopped", file=sys.stderr)
        server.server_close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="OpenPaperGraph interactive server")
    parser.add_argument("graph_json", help="Path to graph JSON file")
    parser.add_argument("--port", type=int, default=8787, help="Port (default: 8787)")
    parser.add_argument("--title", default="Paper Graph", help="Page title")
    args = parser.parse_args()
    start_server(args.graph_json, port=args.port, title=args.title)
