# Architecture

## Layers

### 1. Core
- Scheduler
- Config loader
- State manager

### 2. Browser Layer
- Playwright wrapper
- Session restoration
- Cookie injection

### 3. Feature Layer
- Streak sender
- Content discovery

### 4. Data Layer
- JSON-based storage

## Flow

main.py
 → load config
 → init session
 → run streak sender
 → persist state
