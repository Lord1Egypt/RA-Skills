# YumFu Save/Load Scripts - Quick Reference

## 📋 TL;DR for AI Agents

**Problem**: AI agents used to guess save file format and paths, causing inconsistencies.

**Solution**: Use these standard scripts for ALL save/load operations.

---

## 🔍 Load Game

### Check if user has a save
```bash
uv run ~/clawd/skills/yumfu/scripts/load_game.py \
  --user-id YOUR_USER_ID \
  --universe xiaoao \
  --quiet
```

**Output (JSON):**
```json
{
  "exists": true,
  "data": { "character": {...}, "location": "...", ... },
  "character_name": "小虾米",
  "level": 1,
  "save_path": "..."
}
```

**Or if no save:**
```json
{
  "exists": false,
  "error": "No save found for user YOUR_USER_ID in xiaoao",
  "save_path": ".../user-YOUR_USER_ID.json"
}
```

### Check all worlds for a user
```bash
uv run ~/clawd/skills/yumfu/scripts/load_game.py \
  --user-id YOUR_USER_ID \
  --check-all \
  --quiet
```

**Output:**
```json
{
  "user_id": "YOUR_USER_ID",
  "worlds": {
    "xiaoao": {
      "exists": true,
      "character": "小虾米",
      "level": 1,
      "location": "洛阳城"
    },
    "harry-potter": {
      "exists": true,
      "character": "Tom Brady",
      "level": 1
    },
    "warrior-cats": { "exists": false }
  },
  "active_worlds": ["xiaoao", "harry-potter"]
}
```

---

## 💾 Save Game

### From JSON string
```bash
uv run ~/clawd/skills/yumfu/scripts/save_game.py \
  --user-id YOUR_USER_ID \
  --universe xiaoao \
  --data '{"character": {"name": "小虾米", "level": 2}, "location": "华山派"}'
```

### From stdin (preferred for large saves)
```bash
cat > /tmp/save.json << 'EOF'
{
  "character": {
    "name": "小虾米",
    "level": 2,
    "hp": 85,
    "hp_max": 100
  },
  "location": "华山派·练武场",
  "inventory": [...]
}
EOF

cat /tmp/save.json | \
  uv run ~/clawd/skills/yumfu/scripts/save_game.py \
    --user-id YOUR_USER_ID \
    --universe xiaoao
```

**Output:**
```
✅ Game saved successfully!
📁 Path: ~/clawd/memory/yumfu/saves/xiaoao/user-YOUR_USER_ID.json
💾 Backup: ~/clawd/memory/yumfu/backups/user-YOUR_USER_ID-xiaoao-20260404-101234.json
👤 Character: 小虾米 (Lv.2)
```

### Quiet mode (JSON output only)
```bash
uv run ~/clawd/skills/yumfu/scripts/save_game.py \
  --user-id YOUR_USER_ID \
  --universe xiaoao \
  --data '...' \
  --quiet
```

**Output:**
```json
{
  "success": true,
  "save_path": ".../user-YOUR_USER_ID.json",
  "backup_path": ".../user-YOUR_USER_ID-xiaoao-20260404-101234.json",
  "character_name": "小虾米",
  "level": 2
}
```

---

## 🤖 Agent Integration Pattern

### Standard load-modify-save workflow

```python
import json
import subprocess

def yumfu_load_save(user_id: str, universe: str) -> dict:
    """Load game save. Returns empty dict if doesn't exist."""
    result = subprocess.run([
        "uv", "run",
        f"{os.path.expanduser('~/clawd/skills/yumfu/scripts/load_game.py')}",
        "--user-id", user_id,
        "--universe", universe,
        "--quiet"
    ], capture_output=True, text=True)
    
    data = json.loads(result.stdout)
    return data.get("data", {}) if data.get("exists") else {}

def yumfu_save_game(user_id: str, universe: str, save_data: dict) -> bool:
    """Save game. Returns True if successful."""
    save_json = json.dumps(save_data)
    result = subprocess.run([
        "uv", "run",
        f"{os.path.expanduser('~/clawd/skills/yumfu/scripts/save_game.py')}",
        "--user-id", user_id,
        "--universe", universe,
        "--quiet"
    ], input=save_json, capture_output=True, text=True)
    
    output = json.loads(result.stdout)
    return output.get("success", False)

# Usage
save = yumfu_load_save("YOUR_USER_ID", "xiaoao")
if not save:
    # New user - guide to character creation
    return "Welcome! Use /yumfu start to create your character."

# Modify game state
save["character"]["hp"] -= 15
save["location"] = "华山派·练武场"

# Save back
if yumfu_save_game("YOUR_USER_ID", "xiaoao", save):
    return "⚔️ You arrive at Huashan training grounds..."
else:
    return "❌ ERROR: Failed to save game! Please report this."
```

---

## 📂 File Locations

- **Saves**: `~/clawd/memory/yumfu/saves/{universe}/user-{id}.json`
- **Backups**: `~/clawd/memory/yumfu/backups/user-{id}-{universe}-{timestamp}.json`
- **Emergency fallback**: `/tmp/yumfu-emergency-{id}-{universe}.json`

---

## ⚠️ Important Notes

1. **Always use scripts** - Don't manually construct save logic
2. **Auto-backup** - Scripts automatically backup before overwriting
3. **Error handling** - Scripts will attempt emergency save on failure
4. **Metadata** - Scripts auto-add `user_id`, `universe`, `version`, `last_saved`
5. **UTF-8 encoding** - Handles Chinese characters correctly

---

## 🧪 Testing

```bash
# Test load for existing user
uv run ~/clawd/skills/yumfu/scripts/load_game.py --user-id YOUR_USER_ID --check-all

# Test load for non-existent user
uv run ~/clawd/skills/yumfu/scripts/load_game.py --user-id 999999999 --universe xiaoao

# Test save
echo '{"character": {"name": "测试角色", "level": 1}}' | \
  uv run ~/clawd/skills/yumfu/scripts/save_game.py \
    --user-id 999999999 \
    --universe xiaoao

# Verify save worked
uv run ~/clawd/skills/yumfu/scripts/load_game.py --user-id 999999999 --universe xiaoao --pretty
```

---

## 📜 Script Source

- **save_game.py**: `~/clawd/skills/yumfu/scripts/save_game.py`
- **load_game.py**: `~/clawd/skills/yumfu/scripts/load_game.py`

Full documentation in `~/clawd/skills/yumfu/SKILL.md`
