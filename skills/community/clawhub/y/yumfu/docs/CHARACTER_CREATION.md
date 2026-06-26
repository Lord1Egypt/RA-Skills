# Character Creation Workflow

## 🎭 New: Interactive Character Creation

**For new worlds (Shadow War, etc.), use the character creation script:**

### Step-by-Step Process

When user wants to start a new game in Shadow War or other modern worlds:

1. **Run character creation script**:
```bash
cd ~/clawd/skills/yumfu/scripts
python create_character.py shadow-war
```

2. **The script will prompt for**:
   - Character name/codename
   - Faction choice (6 options with stats)
   - Position/Role (Prime Minister, Defense Minister, etc.)
   - Personality (Aggressive/Diplomatic/Pragmatic/Moral)
   - Background story (optional)

3. **Auto-generates**:
   - Character JSON file
   - AI portrait prompt
   - Default background story if not provided

4. **Character file saved to**:
```
~/.openclaw/yumfu/saves/{world_id}_{user_id}_character.json
```

### Portrait Generation

After character creation, generate portrait:

```python
# The script outputs a portrait_prompt
# Use image_generate tool with that prompt
character_data = load_character(world_id, user_id)
prompt = character_data['portrait_prompt']

# Generate image
image_generate(
    prompt=prompt,
    aspectRatio="2:3",
    filename=f"{character['name'].lower()}-portrait.png"
)
```

### Starting the Game

After character creation + portrait generation:

1. Send character sheet with portrait to user
2. Present opening scenario (from events.json Day 1)
3. Show first decision options
4. Generate tactical map if relevant
5. Begin gameplay loop

### Example Integration

```python
# In your game loop:

# Check if character exists
char_file = f"~/.openclaw/yumfu/saves/{world_id}_{user_id}_character.json"

if not os.path.exists(char_file):
    # New player - run character creation
    print("Running character creation...")
    exec("python ~/clawd/skills/yumfu/scripts/create_character.py {world_id} {user_id}")
    
    # Load newly created character
    character = load_character(world_id, user_id)
    
    # Generate portrait
    portrait_path = generate_portrait(character)
    
    # Send welcome message with portrait
    send_character_sheet(character, portrait_path)
    
    # Start game
    start_game(character)
else:
    # Existing player - load save
    game_state = load_game(world_id, user_id)
    continue_game(game_state)
```

### Character Data Structure

```json
{
  "world_id": "shadow-war",
  "user_id": "default",
  "name": "Damarkil",
  "faction_id": "phoenix_state",
  "faction_name": "Phoenix State",
  "role_id": "defense_minister",
  "role_name": "Defense Minister / 国防部长",
  "personality_id": "pragmatic",
  "personality_name": "Pragmatic / 现实主义",
  "background": "Former special forces operator...",
  "portrait_prompt": "Portrait of Damarkil, a defense minister from Phoenix State...",
  "created_at": "2026-04-05T18:57:00"
}
```

## 🎨 Portrait Prompt Templates

The script auto-generates prompts based on world genre:

### Modern Military (Shadow War)
```
Portrait of {name}, a {role} from {faction}.
Command & Conquer Generals style portrait.
3D render, dramatic military commander aesthetic.
Wearing tactical uniform with rank insignia and faction colors.
Command center background with holographic tactical displays.
Heroic pose, determined expression.
Age 35-50, battle-hardened but stylized features.
Cinematic lighting with red/blue accent lights.
RTS game character portrait style - not photorealistic.
Similar to C&C Generals faction leaders.
{personality_trait}
```

### Fantasy (Harry Potter, LOTR)
```
Portrait of {name}, a {role} from {faction}.
Fantasy art style, magical atmosphere.
Wearing {faction} colors and robes.
{location} background.
Wise and determined expression.
{magical_element}
{personality_trait}
```

### Wuxia (Xiaoao Jianghu)
```
Portrait of {name}, a {role} from {faction}.
Chinese ink painting style.
Traditional martial arts robes.
{sect} temple background.
Heroic pose with weapon.
{personality_trait}
```

Personality traits mapping:
- **Aggressive**: "Fierce, intense gaze."
- **Diplomatic**: "Calm, thoughtful demeanor."
- **Pragmatic**: "Sharp, calculating eyes."
- **Moral**: "Compassionate but firm expression."

## Notes

- Character creation is **separate from game saves**
- Character file is created once, save file tracks game progress
- Portrait is generated during first session and reused
- Background story can be updated later via `/yumfu bio` command
