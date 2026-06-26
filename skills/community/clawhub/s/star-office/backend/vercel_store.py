"""Vercel-compatible in-memory store (resets on cold start, but works for demo)"""
import json
import os
from datetime import datetime

# In-memory storage for serverless environment
_memory_store = {
    "state": {"status": "idle", "message": "Star Office Ready", "timestamp": datetime.now().isoformat()},
    "agents": {},
    "asset_positions": {},
    "asset_defaults": {},
    "runtime_config": {},
    "join_keys": {
        "ocj_starteam01": {"maxConcurrent": 3},
        "ocj_starteam02": {"maxConcurrent": 3},
        "ocj_starteam03": {"maxConcurrent": 3},
        "ocj_starteam04": {"maxConcurrent": 3},
        "ocj_starteam05": {"maxConcurrent": 3},
        "ocj_starteam06": {"maxConcurrent": 3},
        "ocj_starteam07": {"maxConcurrent": 3},
        "ocj_starteam08": {"maxConcurrent": 3},
    }
}

def load_agents_state():
    return _memory_store["agents"]

def save_agents_state(data):
    _memory_store["agents"] = data
    return True

def load_asset_positions():
    return _memory_store["asset_positions"]

def save_asset_positions(data):
    _memory_store["asset_positions"] = data
    return True

def load_asset_defaults():
    return _memory_store["asset_defaults"]

def save_asset_defaults(data):
    _memory_store["asset_defaults"] = data
    return True

def load_runtime_config():
    return _memory_store["runtime_config"]

def save_runtime_config(data):
    _memory_store["runtime_config"] = data
    return True

def load_join_keys():
    return _memory_store["join_keys"]

def save_join_keys(data):
    _memory_store["join_keys"] = data
    return True

def load_state():
    return _memory_store["state"]

def save_state(data):
    _memory_store["state"] = data
    return True