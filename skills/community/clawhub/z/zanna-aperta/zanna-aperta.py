#!/usr/bin/env python3
"""
Zanna Aperta - MCP Bridge per OpenClaw
Versione Raid AI - Tool agent/workspace/project/cron/browser/exec/ollama/clawx
"""

import json
import sys
import subprocess
import os
import signal
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configurazione
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", "/home/raid/.openclaw/workspace")
OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "openclaw")

# Directory
MEMORY_DIR = f"{WORKSPACE}/memory/ragretrevers"
AGENTS_DIR = f"{WORKSPACE}/AGENTS"
CONFIG_DIR = f"{WORKSPACE}/config"
CLAWX_DIR = os.path.expanduser("~/.openclaw/workspace/ClawX")
CLAWX_PID_FILE = "/tmp/clawx.pid"

def log(msg: str):
    """Log su stderr per debug"""
    print(f"[ZANNA-APERTA] {msg}", file=sys.stderr, flush=True)

def send_message(msg: Dict[str, Any]):
    """Invia messaggio JSON-RPC valido"""
    print(json.dumps(msg), flush=True)

def run_openclaw_tool(tool: str, **kwargs) -> Dict[str, Any]:
    """Esegue un tool OpenClaw via CLI"""
    try:
        # Costruisci comando openclaw
        cmd = [OPENCLAW_BIN, "tool", tool]
        
        # Aggiungi parametri come JSON
        for key, value in kwargs.items():
            if value is not None:
                cmd.extend([f"--{key}", str(value)])
        
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== AGENT TOOLS ====================

def agent_find(agent_id: str = "") -> Dict[str, Any]:
    """Trova agenti usando subagents list e sessions_list"""
    try:
        # Usa subagents per trovare agenti
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "subagents", "action", "list"],
            capture_output=True, text=True, timeout=30
        )
        
        # Cerca anche nelle sessioni
        sessions = subprocess.run(
            [OPENCLAW_BIN, "tool", "sessions_list", "kinds", "subagent"],
            capture_output=True, text=True, timeout=30
        )
        
        output = f"Agenti (subagents):\n{result.stdout}\n\nSessioni:\n{sessions.stdout}"
        
        if agent_id:
            # Filtra per ID specifico
            if agent_id in output:
                return {"content": [{"type": "text", "text": f"Agente trovato: {agent_id}"}]}
            return {"isError": True, "content": [{"type": "text", "text": f"Agente non trovato: {agent_id}"}]}
        
        return {"content": [{"type": "text", "text": output}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def agent_update(agent_id: str, key: str, value: str) -> Dict[str, Any]:
    """Aggiorna agente via sessions_send"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "sessions_send", 
             "sessionKey", agent_id,
             "message", f"UPDATE {key}={value}"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Agente {agent_id} aggiornato: {key}={value}"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def agent_delete(agent_id: str) -> Dict[str, Any]:
    """Elimina agente via subagents kill"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "subagents", "action", "kill", "target", agent_id],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Agente {agent_id} eliminato"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== WORKSPACE TOOLS ====================

def workspace_create(uuid: str = "", workspace_name: str = "") -> Dict[str, Any]:
    """Crea workspace come directory"""
    try:
        ws_path = os.path.join(WORKSPACE, workspace_name or uuid)
        os.makedirs(ws_path, exist_ok=True)
        
        # Crea struttura base
        os.makedirs(os.path.join(ws_path, "memory"), exist_ok=True)
        os.makedirs(os.path.join(ws_path, "projects"), exist_ok=True)
        os.makedirs(os.path.join(ws_path, "config"), exist_ok=True)
        
        # Salva metadata
        meta = {"uuid": uuid, "name": workspace_name, "created": True}
        with open(os.path.join(ws_path, "workspace.json"), "w") as f:
            json.dump(meta, f, indent=2)
        
        return {"content": [{"type": "text", "text": f"Workspace creato: {ws_path}"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def workspace_list(uuid: str = "", workspace_name: str = "") -> Dict[str, Any]:
    """Elenca workspace nella directory workspace"""
    try:
        entries = []
        for entry in os.listdir(WORKSPACE):
            entry_path = os.path.join(WORKSPACE, entry)
            if os.path.isdir(entry_path):
                # Cerca metadata
                meta_file = os.path.join(entry_path, "workspace.json")
                if os.path.exists(meta_file):
                    with open(meta_file) as f:
                        meta = json.load(f)
                    entries.append(f"📁 {entry} (UUID: {meta.get('uuid', 'N/A')}, Name: {meta.get('name', 'N/A')})")
                else:
                    entries.append(f"📁 {entry}")
        
        return {"content": [{"type": "text", "text": "\n".join(entries) if entries else "Nessun workspace trovato"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def workspace_find(uuid: str = "", workspace_name: str = "") -> Dict[str, Any]:
    """Trova workspace specifico"""
    try:
        for entry in os.listdir(WORKSPACE):
            entry_path = os.path.join(WORKSPACE, entry)
            if os.path.isdir(entry_path):
                meta_file = os.path.join(entry_path, "workspace.json")
                if os.path.exists(meta_file):
                    with open(meta_file) as f:
                        meta = json.load(f)
                    if meta.get("uuid") == uuid or meta.get("name") == workspace_name or entry == workspace_name:
                        return {"content": [{"type": "text", "text": f"Trovato: {entry}\n{json.dumps(meta, indent=2)}"}]}
        
        return {"isError": True, "content": [{"type": "text", "text": f"Workspace non trovato: {uuid or workspace_name}"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def workspace_update(uuid: str = "", workspace_name: str = "", key: str = "", value: str = "") -> Dict[str, Any]:
    """Aggiorna metadata workspace"""
    try:
        # Trova workspace
        found = False
        for entry in os.listdir(WORKSPACE):
            entry_path = os.path.join(WORKSPACE, entry)
            if os.path.isdir(entry_path):
                meta_file = os.path.join(entry_path, "workspace.json")
                if os.path.exists(meta_file):
                    with open(meta_file) as f:
                        meta = json.load(f)
                    if meta.get("uuid") == uuid or meta.get("name") == workspace_name:
                        meta[key] = value
                        with open(meta_file, "w") as f:
                            json.dump(meta, f, indent=2)
                        found = True
                        return {"content": [{"type": "text", "text": f"Workspace {entry} aggiornato: {key}={value}"}]}
        
        if not found:
            return {"isError": True, "content": [{"type": "text", "text": "Workspace non trovato"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def workspace_delete(uuid: str = "") -> Dict[str, Any]:
    """Elimina workspace (usa trash se disponibile)"""
    try:
        import shutil
        
        for entry in os.listdir(WORKSPACE):
            entry_path = os.path.join(WORKSPACE, entry)
            if os.path.isdir(entry_path):
                meta_file = os.path.join(entry_path, "workspace.json")
                if os.path.exists(meta_file):
                    with open(meta_file) as f:
                        meta = json.load(f)
                    if meta.get("uuid") == uuid:
                        shutil.rmtree(entry_path)
                        return {"content": [{"type": "text", "text": f"Workspace {entry} eliminato"}]}
        
        return {"isError": True, "content": [{"type": "text", "text": f"Workspace non trovato: {uuid}"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== PROJECT TOOLS ====================

def project_create(uuid: str = "", project_name: str = "") -> Dict[str, Any]:
    """Crea progetto nella memoria OpenClaw"""
    try:
        project_dir = os.path.join(MEMORY_DIR, "projects", project_name or uuid)
        os.makedirs(project_dir, exist_ok=True)
        
        # Crea file progetto
        project_file = os.path.join(project_dir, "project.md")
        content = f"""# {project_name or uuid}

**UUID:** {uuid}
**Nome:** {project_name}
**Stato:** Creato
**Data:** {subprocess.run(['date', '-I'], capture_output=True, text=True).stdout.strip()}

## Task
- [ ] Task 1

## Note
"""
        with open(project_file, "w") as f:
            f.write(content)
        
        # Salva anche in ACTIVE.md
        active_file = os.path.join(MEMORY_DIR, "projects", "ACTIVE.md")
        with open(active_file, "a") as f:
            f.write(f"\n## {project_name or uuid}\n**UUID:** {uuid}\n**Stato:** Attivo\n")
        
        return {"content": [{"type": "text", "text": f"Progetto creato: {project_dir}"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def project_list(uuid: str = "", project_name: str = "") -> Dict[str, Any]:
    """Elenca progetti dalla memoria"""
    try:
        projects_dir = os.path.join(MEMORY_DIR, "projects")
        if not os.path.exists(projects_dir):
            return {"content": [{"type": "text", "text": "Nessun progetto trovato"}]}
        
        entries = []
        for entry in os.listdir(projects_dir):
            entry_path = os.path.join(projects_dir, entry)
            if os.path.isdir(entry_path):
                entries.append(f"📁 {entry}")
        
        # Aggiungi anche da ACTIVE.md
        active_file = os.path.join(projects_dir, "ACTIVE.md")
        if os.path.exists(active_file):
            with open(active_file) as f:
                content = f.read()
                entries.append(f"\n---\nContenuto ACTIVE.md:\n{content[:500]}")
        
        return {"content": [{"type": "text", "text": "\n".join(entries) if entries else "Nessun progetto trovato"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def project_find(uuid: str = "", project_name: str = "") -> Dict[str, Any]:
    """Trova progetto specifico"""
    try:
        projects_dir = os.path.join(MEMORY_DIR, "projects")
        
        # Cerca per nome
        target = project_name or uuid
        project_path = os.path.join(projects_dir, target)
        
        if os.path.exists(project_path):
            project_file = os.path.join(project_path, "project.md")
            if os.path.exists(project_file):
                with open(project_file) as f:
                    content = f.read()
                return {"content": [{"type": "text", "text": content}]}
        
        # Cerca anche in ACTIVE.md
        active_file = os.path.join(projects_dir, "ACTIVE.md")
        if os.path.exists(active_file):
            with open(active_file) as f:
                content = f.read()
                if target.lower() in content.lower():
                    return {"content": [{"type": "text", "text": f"Trovato in ACTIVE.md:\n{content}"}]}
        
        return {"isError": True, "content": [{"type": "text", "text": f"Progetto non trovato: {target}"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def project_update(uuid: str = "", project_name: str = "", key: str = "", value: str = "") -> Dict[str, Any]:
    """Aggiorna progetto"""
    try:
        target = project_name or uuid
        project_path = os.path.join(MEMORY_DIR, "projects", target)
        project_file = os.path.join(project_path, "project.md")
        
        if os.path.exists(project_file):
            with open(project_file) as f:
                content = f.read()
            
            # Aggiorna contenuto
            content += f"\n\n## Aggiornamento {key}\n{value}"
            
            with open(project_file, "w") as f:
                f.write(content)
            
            return {"content": [{"type": "text", "text": f"Progetto {target} aggiornato"}]}
        
        return {"isError": True, "content": [{"type": "text", "text": f"Progetto non trovato: {target}"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def project_delete(uuid: str = "") -> Dict[str, Any]:
    """Elimina progetto"""
    try:
        import shutil
        
        project_path = os.path.join(MEMORY_DIR, "projects", uuid)
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
            return {"content": [{"type": "text", "text": f"Progetto {uuid} eliminato"}]}
        
        return {"isError": True, "content": [{"type": "text", "text": f"Progetto non trovato: {uuid}"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== CRON TOOLS ====================

def cron_list() -> Dict[str, Any]:
    """Elenca job cron"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "cron", "action", "list"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": result.stdout or "Nessun job trovato"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def cron_add(name: str = "", schedule: str = "", payload: str = "") -> Dict[str, Any]:
    """Aggiunge job cron"""
    try:
        # Crea un job con schedule e payload
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "cron", "action", "add",
             "job", json.dumps({"name": name, "schedule": schedule, "payload": payload})],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Job '{name}' aggiunto"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def cron_remove(job_id: str = "") -> Dict[str, Any]:
    """Rimuove job cron"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "cron", "action", "remove", "jobId", job_id],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Job {job_id} rimosso"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def cron_run(job_id: str = "") -> Dict[str, Any]:
    """Esegue job cron immediatamente"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "cron", "action", "run", "jobId", job_id],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Job {job_id} eseguito"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== BROWSER TOOLS ====================

def browser_open(url: str = "") -> Dict[str, Any]:
    """Apre URL nel browser"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "browser", "action", "open", "url", url],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Browser aperto su {url}"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def browser_snapshot(full_page: bool = False) -> Dict[str, Any]:
    """Cattura screenshot pagina corrente"""
    try:
        cmd = [OPENCLAW_BIN, "tool", "browser", "action", "snapshot"]
        if full_page:
            cmd.extend(["fullPage", "true"])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": result.stdout}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def browser_click(selector: str = "") -> Dict[str, Any]:
    """Clicca elemento nel browser"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "browser", "action", "click", "selector", selector],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Click su {selector}"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def browser_type(selector: str = "", text: str = "") -> Dict[str, Any]:
    """Digita testo nel browser"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "browser", "action", "type", "selector", selector, "text", text],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Testo inserito in {selector}"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== EXEC TOOLS (Extended) ====================

def exec_docker(command: str = "") -> Dict[str, Any]:
    """Esegue comando Docker"""
    try:
        result = subprocess.run(
            ["docker"] + command.split(),
            capture_output=True, text=True, timeout=60
        )
        
        output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return {"content": [{"type": "text", "text": output}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def exec_git(command: str = "") -> Dict[str, Any]:
    """Esegue comando Git"""
    try:
        result = subprocess.run(
            ["git"] + command.split(),
            capture_output=True, text=True, timeout=30, cwd=WORKSPACE
        )
        
        output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return {"content": [{"type": "text", "text": output}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== OLLAMA TOOLS ====================

def ollama_list() -> Dict[str, Any]:
    """Elenca modelli Ollama disponibili"""
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            models = data.get("models", [])
            output = []
            for m in models:
                name = m.get("name", "N/A")
                size_mb = m.get("size", 0) / (1024*1024)
                output.append(f"🤖 {name} ({size_mb:.0f}MB)")
            return {"content": [{"type": "text", "text": "\n".join(output) if output else "Nessun modello trovato"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def ollama_chat(model: str = "", message: str = "", stream: bool = False) -> Dict[str, Any]:
    """Chat con modello Ollama"""
    try:
        payload = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "stream": stream
        })
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            responses = []
            for line in lines:
                try:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        responses.append(data["message"]["content"])
                except:
                    pass
            full_response = "".join(responses)
            return {"content": [{"type": "text", "text": full_response or result.stdout[:500]}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def ollama_generate(model: str = "", prompt: str = "") -> Dict[str, Any]:
    """Genera testo con modello Ollama"""
    try:
        payload = json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", "http://localhost:11434/api/generate",
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            response = data.get("response", "Nessuna risposta")
            return {"content": [{"type": "text", "text": response}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def ollama_pull(model: str = "") -> Dict[str, Any]:
    """Scarica modello Ollama"""
    try:
        result = subprocess.run(
            ["ollama", "pull", model],
            capture_output=True, text=True, timeout=300
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Modello {model} scaricato"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== CANVAS TOOLS ====================

def canvas_present(url: str = "", width: int = 1280, height: int = 720) -> Dict[str, Any]:
    """Presenta URL in canvas"""
    try:
        cmd = [OPENCLAW_BIN, "tool", "canvas", "action", "present"]
        if url:
            cmd.extend(["url", url])
        if width:
            cmd.extend(["width", str(width)])
        if height:
            cmd.extend(["height", str(height)])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Canvas presentato: {url}"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def canvas_hide() -> Dict[str, Any]:
    """Nasconde canvas"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "canvas", "action", "hide"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": "Canvas nascosto"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def canvas_eval(javaScript: str = "") -> Dict[str, Any]:
    """Esegue JavaScript nel canvas"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "canvas", "action", "eval", "javaScript", javaScript],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": result.stdout}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== NODES TOOLS ====================

def nodes_list() -> Dict[str, Any]:
    """Elenca nodi collegati"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "nodes", "action", "status"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": result.stdout or "Nessun nodo trovato"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def nodes_notify(device_id: str = "", title: str = "", body: str = "") -> Dict[str, Any]:
    """Invia notifica a nodo"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "nodes", "action", "notify",
             "deviceId", device_id, "title", title, "body", body],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Notifica inviata a {device_id}"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def nodes_camera_snap(device_id: str = "", facing: str = "back") -> Dict[str, Any]:
    """Scatta foto da nodo"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "nodes", "action", "camera_snap",
             "deviceId", device_id, "facing", facing],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Foto scattata da {device_id}"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== MESSAGING TOOLS ====================

def message_send(channel: str = "", target: str = "", message: str = "") -> Dict[str, Any]:
    """Invia messaggio a canale"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "message", "action", "send",
             "channel", channel, "to", target, "message", message],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": f"Messaggio inviato a {target}"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def message_poll(channel: str = "") -> Dict[str, Any]:
    """Crea sondaggio nel canale"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "message", "action", "poll_create",
             "channel", channel],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": "Sondaggio creato"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== GATEWAY TOOLS ====================

def gateway_status() -> Dict[str, Any]:
    """Stato gateway OpenClaw"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "gateway", "action", "status"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": result.stdout}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def gateway_restart() -> Dict[str, Any]:
    """Riavvia gateway"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "tool", "gateway", "action", "restart"],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            return {"content": [{"type": "text", "text": "Gateway riavviato"}]}
        return {"isError": True, "content": [{"type": "text", "text": result.stderr}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== CLAWX TOOLS ====================

def clawx_start() -> Dict[str, Any]:
    """Avvia ClawX (interfaccia desktop OpenClaw)"""
    try:
        # Verifica se già in esecuzione
        if os.path.exists(CLAWX_PID_FILE):
            with open(CLAWX_PID_FILE) as f:
                old_pid = f.read().strip()
            try:
                os.kill(int(old_pid), 0)
                return {"content": [{"type": "text", "text": f"ClawX già in esecuzione (PID: {old_pid})\nDashboard: http://localhost:5173"}]}
            except:
                pass
        
        # Avvia ClawX
        proc = subprocess.Popen(
            ["pnpm", "run", "dev"],
            cwd=CLAWX_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        
        with open(CLAWX_PID_FILE, "w") as f:
            f.write(str(proc.pid))
        
        return {"content": [{"type": "text", "text": f"ClawX avviato (PID: {proc.pid})\nDashboard: http://localhost:5173"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def clawx_stop() -> Dict[str, Any]:
    """Ferma ClawX"""
    try:
        if not os.path.exists(CLAWX_PID_FILE):
            return {"isError": True, "content": [{"type": "text", "text": "ClawX non in esecuzione"}]}
        
        with open(CLAWX_PID_FILE) as f:
            pid = int(f.read().strip())
        
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        os.remove(CLAWX_PID_FILE)
        
        return {"content": [{"type": "text", "text": "ClawX fermato"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def clawx_status() -> Dict[str, Any]:
    """Verifica stato ClawX"""
    try:
        if not os.path.exists(CLAWX_PID_FILE):
            return {"content": [{"type": "text", "text": "ClawX: FERMO\nDashboard: http://localhost:5173 (non raggiungibile)"}]}
        
        with open(CLAWX_PID_FILE) as f:
            pid = f.read().strip()
        
        try:
            os.kill(int(pid), 0)
            return {"content": [{"type": "text", "text": f"ClawX: ATTIVO (PID: {pid})\nDashboard: http://localhost:5173"}]}
        except:
            os.remove(CLAWX_PID_FILE)
            return {"content": [{"type": "text", "text": "ClawX: FERMO (pid file orfano rimosso)"}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

def clawx_restart() -> Dict[str, Any]:
    """Riavvia ClawX"""
    try:
        clawx_stop()
        import time
        time.sleep(2)
        return clawx_start()
    except Exception as e:
        return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

# ==================== TOOL DEFINITIONS ====================

def get_tools() -> List[Dict[str, Any]]:
    """Restituisce lista tool MCP estesa"""
    return [
        # Agent tools
        {
            "name": "agent_find",
            "description": "Trova agenti usando OpenClaw subagents/sessions_list",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string", "description": "ID agente (opzionale)"}
                },
                "required": []
            }
        },
        {
            "name": "agent_update",
            "description": "Aggiorna configurazione agente via sessions_send",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string", "description": "ID agente"},
                    "key": {"type": "string", "description": "Chiave da aggiornare"},
                    "value": {"type": "string", "description": "Nuovo valore"}
                },
                "required": ["agent_id", "key", "value"]
            }
        },
        {
            "name": "agent_delete",
            "description": "Elimina agente via subagents kill",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string", "description": "ID agente da eliminare"}
                },
                "required": ["agent_id"]
            }
        },
        # Workspace tools
        {
            "name": "workspace_create",
            "description": "Crea nuovo workspace",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "UUID workspace"},
                    "workspace_name": {"type": "string", "description": "Nome workspace"}
                },
                "required": []
            }
        },
        {
            "name": "workspace_list",
            "description": "Elenca tutti i workspace",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "Filtra per UUID"},
                    "workspace_name": {"type": "string", "description": "Filtra per nome"}
                },
                "required": []
            }
        },
        {
            "name": "workspace_find",
            "description": "Trova workspace specifico",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "UUID workspace"},
                    "workspace_name": {"type": "string", "description": "Nome workspace"}
                },
                "required": []
            }
        },
        {
            "name": "workspace_update",
            "description": "Aggiorna metadata workspace",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "UUID workspace"},
                    "workspace_name": {"type": "string", "description": "Nome workspace"},
                    "key": {"type": "string", "description": "Chiave"},
                    "value": {"type": "string", "description": "Valore"}
                },
                "required": ["key", "value"]
            }
        },
        {
            "name": "workspace_delete",
            "description": "Elimina workspace",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "UUID workspace"}
                },
                "required": ["uuid"]
            }
        },
        # Project tools
        {
            "name": "project_create",
            "description": "Crea nuovo progetto in memoria OpenClaw",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "UUID progetto"},
                    "project_name": {"type": "string", "description": "Nome progetto"}
                },
                "required": []
            }
        },
        {
            "name": "project_list",
            "description": "Elenca tutti i progetti",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "Filtra per UUID"},
                    "project_name": {"type": "string", "description": "Filtra per nome"}
                },
                "required": []
            }
        },
        {
            "name": "project_find",
            "description": "Trova progetto specifico",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "UUID progetto"},
                    "project_name": {"type": "string", "description": "Nome progetto"}
                },
                "required": []
            }
        },
        {
            "name": "project_update",
            "description": "Aggiorna progetto",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "UUID progetto"},
                    "project_name": {"type": "string", "description": "Nome progetto"},
                    "key": {"type": "string", "description": "Chiave"},
                    "value": {"type": "string", "description": "Valore"}
                },
                "required": ["key", "value"]
            }
        },
        {
            "name": "project_delete",
            "description": "Elimina progetto",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "UUID progetto"}
                },
                "required": ["uuid"]
            }
        },
        # Cron tools
        {
            "name": "cron_list",
            "description": "Elenca job cron attivi",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "cron_add",
            "description": "Aggiunge job cron",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Nome job"},
                    "schedule": {"type": "string", "description": "Schedule (cron expr)"},
                    "payload": {"type": "string", "description": "Payload JSON"}
                },
                "required": ["name", "schedule"]
            }
        },
        {
            "name": "cron_remove",
            "description": "Rimuove job cron",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "job_id": {"type": "string", "description": "ID job"}
                },
                "required": ["job_id"]
            }
        },
        {
            "name": "cron_run",
            "description": "Esegue job cron immediatamente",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "job_id": {"type": "string", "description": "ID job"}
                },
                "required": ["job_id"]
            }
        },
        # Browser tools
        {
            "name": "browser_open",
            "description": "Apre URL nel browser",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL da aprire"}
                },
                "required": ["url"]
            }
        },
        {
            "name": "browser_snapshot",
            "description": "Cattura screenshot pagina",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "full_page": {"type": "boolean", "description": "Cattura pagina intera", "default": false}
                },
                "required": []
            }
        },
        {
            "name": "browser_click",
            "description": "Clicca elemento nel browser",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "CSS selector"}
                },
                "required": ["selector"]
            }
        },
        {
            "name": "browser_type",
            "description": "Digita testo nel browser",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "CSS selector"},
                    "text": {"type": "string", "description": "Testo da digitare"}
                },
                "required": ["selector", "text"]
            }
        },
        # Exec Extended
        {
            "name": "exec_docker",
            "description": "Esegue comando Docker",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Comando Docker (es. 'ps -a')"}
                },
                "required": ["command"]
            }
        },
        {
            "name": "exec_git",
            "description": "Esegue comando Git",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Comando Git (es. 'status')"}
                },
                "required": ["command"]
            }
        },
        # Canvas tools
        {
            "name": "canvas_present",
            "description": "Presenta URL nel canvas",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL da presentare"},
                    "width": {"type": "integer", "description": "Larghezza", "default": 1280},
                    "height": {"type": "integer", "description": "Altezza", "default": 720}
                },
                "required": ["url"]
            }
        },
        {
            "name": "canvas_hide",
            "description": "Nasconde il canvas",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "canvas_eval",
            "description": "Esegue JavaScript nel canvas",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "javaScript": {"type": "string", "description": "Codice JavaScript"}
                },
                "required": ["javaScript"]
            }
        },
        # Nodes tools
        {
            "name": "nodes_list",
            "description": "Elenca nodi collegati",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "nodes_notify",
            "description": "Invia notifica a nodo",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "ID dispositivo"},
                    "title": {"type": "string", "description": "Titolo notifica"},
                    "body": {"type": "string", "description": "Corpo notifica"}
                },
                "required": ["device_id", "title", "body"]
            }
        },
        {
            "name": "nodes_camera_snap",
            "description": "Scatta foto da nodo",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "ID dispositivo"},
                    "facing": {"type": "string", "description": "Camera (front/back)", "default": "back"}
                },
                "required": ["device_id"]
            }
        },
        # Messaging tools
        {
            "name": "message_send",
            "description": "Invia messaggio a canale",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "description": "Canale (telegram, discord, etc.)"},
                    "target": {"type": "string", "description": "Destinatario"},
                    "message": {"type": "string", "description": "Messaggio"}
                },
                "required": ["channel", "target", "message"]
            }
        },
        {
            "name": "message_poll",
            "description": "Crea sondaggio nel canale",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "description": "Canale"}
                },
                "required": ["channel"]
            }
        },
        # Gateway tools
        {
            "name": "gateway_status",
            "description": "Stato gateway OpenClaw",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "gateway_restart",
            "description": "Riavvia gateway",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        # Ollama tools
        {
            "name": "ollama_list",
            "description": "Elenca modelli Ollama disponibili",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "ollama_chat",
            "description": "Chat con modello Ollama",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model": {"type": "string", "description": "Nome modello"},
                    "message": {"type": "string", "description": "Messaggio"},
                    "stream": {"type": "boolean", "description": "Stream risposta", "default": false}
                },
                "required": ["model", "message"]
            }
        },
        {
            "name": "ollama_generate",
            "description": "Genera testo con modello Ollama",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model": {"type": "string", "description": "Nome modello"},
                    "prompt": {"type": "string", "description": "Prompt"}
                },
                "required": ["model", "prompt"]
            }
        },
        {
            "name": "ollama_pull",
            "description": "Scarica modello Ollama",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model": {"type": "string", "description": "Nome modello da scaricare"}
                },
                "required": ["model"]
            }
        },
        # ClawX tools
        {
            "name": "clawx_start",
            "description": "Avvia ClawX (interfaccia desktop OpenClaw)",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "clawx_stop",
            "description": "Ferma ClawX",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "clawx_status",
            "description": "Verifica stato ClawX",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "clawx_restart",
            "description": "Riavvia ClawX",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
    ]

# ==================== MCP HANDLERS ====================

def handle_initialize(request_id):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "experimental": {},
                "prompts": {"listChanged": False},
                "resources": {"subscribe": False, "listChanged": False},
                "tools": {"listChanged": False}
            },
            "serverInfo": {
                "name": "zanna-aperta",
                "version": "3.4.0"
            }
        }
    }

def handle_tools_list(request_id):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {"tools": get_tools()}
    }

def handle_tools_call(request_id, name, arguments):
    """Gestisce chiamata tool"""
    log(f"Tool: {name} args: {json.dumps(arguments)[:200]}")
    
    tools_map = {
        # Agent
        "agent_find": lambda: agent_find(arguments.get("agent_id", "")),
        "agent_update": lambda: agent_update(arguments.get("agent_id", ""), arguments.get("key", ""), arguments.get("value", "")),
        "agent_delete": lambda: agent_delete(arguments.get("agent_id", "")),
        # Workspace
        "workspace_create": lambda: workspace_create(arguments.get("uuid", ""), arguments.get("workspace_name", "")),
        "workspace_list": lambda: workspace_list(arguments.get("uuid", ""), arguments.get("workspace_name", "")),
        "workspace_find": lambda: workspace_find(arguments.get("uuid", ""), arguments.get("workspace_name", "")),
        "workspace_update": lambda: workspace_update(arguments.get("uuid", ""), arguments.get("workspace_name", ""), arguments.get("key", ""), arguments.get("value", "")),
        "workspace_delete": lambda: workspace_delete(arguments.get("uuid", "")),
        # Project
        "project_create": lambda: project_create(arguments.get("uuid", ""), arguments.get("project_name", "")),
        "project_list": lambda: project_list(arguments.get("uuid", ""), arguments.get("project_name", "")),
        "project_find": lambda: project_find(arguments.get("uuid", ""), arguments.get("project_name", "")),
        "project_update": lambda: project_update(arguments.get("uuid", ""), arguments.get("project_name", ""), arguments.get("key", ""), arguments.get("value", "")),
        "project_delete": lambda: project_delete(arguments.get("uuid", "")),
        # Cron
        "cron_list": lambda: cron_list(),
        "cron_add": lambda: cron_add(arguments.get("name", ""), arguments.get("schedule", ""), arguments.get("payload", "")),
        "cron_remove": lambda: cron_remove(arguments.get("job_id", "")),
        "cron_run": lambda: cron_run(arguments.get("job_id", "")),
        # Browser
        "browser_open": lambda: browser_open(arguments.get("url", "")),
        "browser_snapshot": lambda: browser_snapshot(arguments.get("full_page", False)),
        "browser_click": lambda: browser_click(arguments.get("selector", "")),
        "browser_type": lambda: browser_type(arguments.get("selector", ""), arguments.get("text", "")),
        # Exec Extended
        "exec_docker": lambda: exec_docker(arguments.get("command", "")),
        "exec_git": lambda: exec_git(arguments.get("command", "")),
        # Canvas
        "canvas_present": lambda: canvas_present(arguments.get("url", ""), arguments.get("width", 1280), arguments.get("height", 720)),
        "canvas_hide": lambda: canvas_hide(),
        "canvas_eval": lambda: canvas_eval(arguments.get("javaScript", "")),
        # Nodes
        "nodes_list": lambda: nodes_list(),
        "nodes_notify": lambda: nodes_notify(arguments.get("device_id", ""), arguments.get("title", ""), arguments.get("body", "")),
        "nodes_camera_snap": lambda: nodes_camera_snap(arguments.get("device_id", ""), arguments.get("facing", "back")),
        # Messaging
        "message_send": lambda: message_send(arguments.get("channel", ""), arguments.get("target", ""), arguments.get("message", "")),
        "message_poll": lambda: message_poll(arguments.get("channel", "")),
        # Gateway
        "gateway_status": lambda: gateway_status(),
        "gateway_restart": lambda: gateway_restart(),
        # Ollama
        "ollama_list": lambda: ollama_list(),
        "ollama_chat": lambda: ollama_chat(arguments.get("model", ""), arguments.get("message", ""), arguments.get("stream", False)),
        "ollama_generate": lambda: ollama_generate(arguments.get("model", ""), arguments.get("prompt", "")),
        "ollama_pull": lambda: ollama_pull(arguments.get("model", "")),
        # ClawX
        "clawx_start": lambda: clawx_start(),
        "clawx_stop": lambda: clawx_stop(),
        "clawx_status": lambda: clawx_status(),
        "clawx_restart": lambda: clawx_restart(),
    }
    
    if name in tools_map:
        try:
            result = tools_map[name]()
        except Exception as e:
            result = {"isError": True, "content": [{"type": "text", "text": str(e)}]}
    else:
        result = {"isError": True, "content": [{"type": "text", "text": f"Tool sconosciuto: {name}"}]}
    
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    }

def main():
    log("Zanna Aperta v3.4.0 - Starting...")
    log(f"Workspace: {WORKSPACE}")
    log(f"Memory: {MEMORY_DIR}")
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            request = json.loads(line)
            method = request.get("method", "")
            request_id = request.get("id")
            
            log(f"Method: {method}")
            
            if method == "initialize":
                response = handle_initialize(request_id)
            elif method == "tools/list":
                response = handle_tools_list(request_id)
            elif method == "tools/call":
                params = request.get("params", {})
                response = handle_tools_call(
                    request_id,
                    params.get("name", ""),
                    params.get("arguments", {})
                )
            elif method == "notifications/initialized":
                continue
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Metodo non trovato: {method}"}
                }
            
            send_message(response)
            
        except json.JSONDecodeError:
            log(f"JSON invalido: {line[:100]}")
            send_message({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            })
        except Exception as e:
            log(f"Errore: {str(e)}")
            send_message({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            })

if __name__ == "__main__":
    main()
