#!/usr/bin/env python3
"""
Proxmox Multi-Control - Multi-server Proxmox VE management via REST API.
"""

import os
import sys
import json
from proxmoxer import ProxmoxAPI

def jprint(obj, code=0):
    print(json.dumps(obj, indent=2))
    sys.exit(code)

def env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        jprint({"ok": False, "error": f"Missing env var: {name}"}, 2)
    return v

def load_credentials():
    """Load all host configs from credentials JSON or env vars.
    
    Supports three formats:
    1. Multi-host JSON: {"default": "prod", "hosts": {"prod": {...}, "plex": {...}}}
    2. Single-host JSON: {"host": "...", "token_id": "...", "token_secret": "..."}
    3. Env vars fallback: PVE_HOST, PVE_TOKEN_ID, PVE_TOKEN_SECRET
    """
    config_file = os.path.expanduser("~/.openclaw/credentials/proxmox.json")
    
    if os.path.exists(config_file):
        with open(config_file) as f:
            cfg = json.load(f)
        
        # Multi-host format
        if "hosts" in cfg:
            return cfg.get("default", None), cfg["hosts"]
        
        # Single-host format (backward compat)
        name = cfg.get("name", "default")
        return name, {name: cfg}
    
    # Env vars fallback (single host)
    host = os.getenv("PVE_HOST")
    if host:
        return "default", {"default": {
            "host": host,
            "token_id": os.getenv("PVE_TOKEN_ID", ""),
            "token_secret": os.getenv("PVE_TOKEN_SECRET", ""),
            "verify_ssl": os.getenv("PVE_VERIFY_SSL", "false").lower() in ("true", "1", "yes")
        }}
    
    jprint({"ok": False, "error": "No Proxmox credentials found. Set up ~/.openclaw/credentials/proxmox.json or PVE_HOST/PVE_TOKEN_ID/PVE_TOKEN_SECRET env vars."}, 2)

def get_host_config(host_name=None):
    """Get config for a specific host (or default)."""
    default, hosts = load_credentials()
    
    if not host_name:
        host_name = default or list(hosts.keys())[0]
    
    if host_name not in hosts:
        jprint({"ok": False, "error": f"Unknown host: {host_name}", "available": list(hosts.keys())}, 2)
    
    h = hosts[host_name]
    host = h.get("host", "").replace("https://", "").replace("http://", "")
    token_id = h.get("token_id", "")
    token_secret = h.get("token_secret", "")
    verify_ssl = h.get("verify_ssl", False)
    
    if not token_id or "!" not in token_id:
        jprint({"ok": False, "error": f"Token ID for '{host_name}' must be user@realm!tokenname"}, 2)
    
    return host, token_id, token_secret, verify_ssl

def connect(host_name=None) -> ProxmoxAPI:
    host, token_id, token_secret, verify_ssl = get_host_config(host_name)
    user, token_name = token_id.split("!", 1)
    
    return ProxmoxAPI(
        host,
        user=user,
        token_name=token_name,
        token_value=token_secret,
        verify_ssl=verify_ssl,
    )

def connect_all():
    """Connect to all configured hosts. Returns dict of {name: ProxmoxAPI}."""
    default, hosts = load_credentials()
    connections = {}
    errors = []
    for name in hosts:
        try:
            connections[name] = connect(name)
        except Exception as e:
            errors.append({"host": name, "error": str(e)})
    return connections, errors

# --- API functions ---

def list_nodes(p: ProxmoxAPI):
    return p.nodes.get()

def node_health(p: ProxmoxAPI, node: str):
    return p.nodes(node).status.get()

def list_vms(p: ProxmoxAPI):
    return p.cluster.resources.get(type="vm")

def status_current(p: ProxmoxAPI, node: str, kind: str, vmid: str):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).status.current.get()

def action_vm(p: ProxmoxAPI, node: str, kind: str, vmid: str, action: str):
    endpoint = getattr(p.nodes(node), kind)
    return getattr(endpoint(vmid).status, action).post()

def snapshot_vm(p: ProxmoxAPI, node: str, kind: str, vmid: str, snapname: str, vmstate: bool = False):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).snapshot.post(snapname=snapname, vmstate=1 if vmstate else 0)

def list_snapshots(p: ProxmoxAPI, node: str, kind: str, vmid: str):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).snapshot.get()

def delete_snapshot(p: ProxmoxAPI, node: str, kind: str, vmid: str, snapname: str):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).snapshot(snapname).delete()

def rollback_snapshot(p: ProxmoxAPI, node: str, kind: str, vmid: str, snapname: str):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).snapshot(snapname).rollback.post()

def list_storage(p: ProxmoxAPI, node: str):
    return p.nodes(node).storage.get()

def list_tasks(p: ProxmoxAPI, node: str, limit: int = 10):
    return p.nodes(node).tasks.get(limit=limit)

def list_backups(p: ProxmoxAPI, node: str, storage: str = "local"):
    return p.nodes(node).storage(storage).content.get(content="backup")

def usage():
    jprint({
        "ok": False,
        "error": "usage",
        "examples": [
            "proxmox.py [--host <name>] nodes",
            "proxmox.py [--host <name>] node_health <node>",
            "proxmox.py [--host <name>] vms",
            "proxmox.py [--host <name>] status <node> <qemu|lxc> <vmid>",
            "proxmox.py [--host <name>] list_snapshots <node> <qemu|lxc> <vmid>",
            "proxmox.py [--host <name>] snapshot <node> <qemu|lxc> <vmid> <snapname> [vmstate=0|1]",
            "proxmox.py [--host <name>] delete_snapshot <node> <qemu|lxc> <vmid> <snapname>",
            "proxmox.py [--host <name>] rollback <node> <qemu|lxc> <vmid> <snapname>",
            "proxmox.py [--host <name>] <start|stop|reboot|shutdown> <node> <qemu|lxc> <vmid>",
            "proxmox.py [--host <name>] storage <node>",
            "proxmox.py [--host <name>] backups <node> [storage]",
            "proxmox.py [--host <name>] tasks <node> [limit]",
            "proxmox.py hosts                         # list configured hosts",
            "proxmox.py cluster-vms                    # list VMs across ALL hosts",
            "proxmox.py cluster-status                 # health overview of ALL hosts"
        ]
    }, 2)

def main():
    if len(sys.argv) < 2:
        usage()

    # Parse optional --host flag
    args = sys.argv[1:]
    host_name = None
    if args[0] == "--host" and len(args) >= 2:
        host_name = args[1]
        args = args[2:]
    
    if not args:
        usage()

    cmd = args[0].strip().lower()
    cmd_args = args[1:]

    try:
        # --- Multi-host commands (no connection needed upfront) ---
        if cmd == "hosts":
            default, hosts = load_credentials()
            host_list = []
            for name, cfg in hosts.items():
                host_list.append({
                    "name": name,
                    "host": cfg.get("host", ""),
                    "token_id": cfg.get("token_id", ""),
                    "default": name == default
                })
            jprint({"ok": True, "data": host_list})
        
        elif cmd == "cluster-vms":
            connections, errors = connect_all()
            all_vms = []
            for name, p in connections.items():
                try:
                    vms = list_vms(p)
                    for vm in vms:
                        vm["_host"] = name
                    all_vms.extend(vms)
                except Exception as e:
                    errors.append({"host": name, "error": str(e)})
            all_vms.sort(key=lambda x: x.get("vmid", 0))
            result = {"ok": True, "data": all_vms}
            if errors:
                result["errors"] = errors
            jprint(result)
        
        elif cmd == "cluster-status":
            connections, errors = connect_all()
            status = []
            for name, p in connections.items():
                try:
                    nodes = list_nodes(p)
                    for n in nodes:
                        n["_host"] = name
                    status.extend(nodes)
                except Exception as e:
                    errors.append({"host": name, "error": str(e)})
            result = {"ok": True, "data": status}
            if errors:
                result["errors"] = errors
            jprint(result)
        
        # --- Single-host commands ---
        else:
            p = connect(host_name)
            
            if cmd == "nodes":
                jprint({"ok": True, "data": list_nodes(p)})
            
            elif cmd == "node_health":
                jprint({"ok": True, "data": node_health(p, cmd_args[0])})
            
            elif cmd == "vms":
                jprint({"ok": True, "data": list_vms(p)})
            
            elif cmd == "status":
                node, kind, vmid = cmd_args[0:3]
                jprint({"ok": True, "data": status_current(p, node, kind, vmid)})
            
            elif cmd in ("start", "stop", "shutdown", "reboot"):
                node, kind, vmid = cmd_args[0:3]
                jprint({"ok": True, "data": action_vm(p, node, kind, vmid, cmd)})
            
            elif cmd == "snapshot":
                node, kind, vmid, snapname = cmd_args[0:4]
                vmstate = cmd_args[4].lower() in ("1", "true", "yes") if len(cmd_args) > 4 else False
                jprint({"ok": True, "data": snapshot_vm(p, node, kind, vmid, snapname, vmstate)})
            
            elif cmd == "list_snapshots":
                node, kind, vmid = cmd_args[0:3]
                jprint({"ok": True, "data": list_snapshots(p, node, kind, vmid)})
            
            elif cmd == "delete_snapshot":
                node, kind, vmid, snapname = cmd_args[0:4]
                jprint({"ok": True, "data": delete_snapshot(p, node, kind, vmid, snapname)})
            
            elif cmd == "rollback":
                node, kind, vmid, snapname = cmd_args[0:4]
                jprint({"ok": True, "data": rollback_snapshot(p, node, kind, vmid, snapname)})
            
            elif cmd == "storage":
                jprint({"ok": True, "data": list_storage(p, cmd_args[0])})
            
            elif cmd == "backups":
                node = cmd_args[0]
                storage = cmd_args[1] if len(cmd_args) > 1 else "local"
                jprint({"ok": True, "data": list_backups(p, node, storage)})
            
            elif cmd == "tasks":
                node = cmd_args[0]
                limit = int(cmd_args[1]) if len(cmd_args) > 1 else 10
                jprint({"ok": True, "data": list_tasks(p, node, limit)})
            
            else:
                usage()
    
    except IndexError:
        jprint({"ok": False, "error": f"Not enough arguments for '{cmd}'. Run without args for usage."}, 2)
    except Exception as e:
        jprint({"ok": False, "error": str(e)}, 1)

if __name__ == "__main__":
    main()
