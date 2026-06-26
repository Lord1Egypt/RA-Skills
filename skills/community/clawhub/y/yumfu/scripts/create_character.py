#!/usr/bin/env python3
"""
Character Creation Script for YumFu
Handles interactive character creation with portrait generation
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def create_character(world_id, user_id="default"):
    """
    Interactive character creation for a specific world
    
    Args:
        world_id: The world identifier (e.g., 'shadow-war', 'harry-potter')
        user_id: User identifier (default: 'default')
    
    Returns:
        dict: Character data including name, role, personality, portrait path
    """
    
    # Load world configuration
    world_path = os.path.join(os.path.dirname(__file__), '..', 'worlds', world_id)
    world_json = os.path.join(world_path, 'world.json')
    factions_json = os.path.join(world_path, 'factions.json')
    
    if not os.path.exists(world_json):
        raise FileNotFoundError(f"World not found: {world_id}")
    
    with open(world_json, 'r', encoding='utf-8') as f:
        world_data = json.load(f)
    
    with open(factions_json, 'r', encoding='utf-8') as f:
        factions_data = json.load(f)
    
    # Get world-specific character creation prompts
    world_name = world_data.get('name', world_id)
    world_genre = world_data.get('genre', 'adventure')
    
    print(f"🎮 Creating character for: {world_name}")
    print("━" * 50)
    
    character = {
        "world_id": world_id,
        "user_id": user_id,
        "created_at": datetime.now().isoformat()
    }
    
    # Step 1: Name
    print("\n👤 Step 1: Character Name")
    character['name'] = input("Enter your character's name (or codename): ").strip()
    
    # Step 2: Faction selection
    print("\n🏛️ Step 2: Choose Your Faction")
    print("━" * 50)
    
    factions = factions_data.get('factions', [])
    for i, faction in enumerate(factions, 1):
        name_zh = faction.get('name_zh', faction.get('name_en', faction['id']))
        name_en = faction.get('name_en', faction['id'])
        specialty = faction.get('specialty', 'Unknown')
        
        print(f"{i}. {name_en} ({name_zh})")
        print(f"   Specialty: {specialty}")
        
        # Show key attributes
        attrs = faction.get('attributes', {})
        top_attrs = sorted(attrs.items(), key=lambda x: x[1], reverse=True)[:3]
        attr_str = ", ".join([f"{k}: {v}/100" for k, v in top_attrs])
        print(f"   Stats: {attr_str}")
        print()
    
    faction_choice = int(input(f"Choose faction (1-{len(factions)}): ")) - 1
    character['faction_id'] = factions[faction_choice]['id']
    character['faction_name'] = factions[faction_choice].get('name_en', '')
    
    # Step 3: Role/Position (world-specific)
    print("\n💼 Step 3: Your Role")
    print("━" * 50)
    
    if world_genre == 'modern_military_strategy':
        # Check if frontline roles exist
        frontline_file = os.path.join(world_path, 'frontline_roles.json')
        
        if os.path.exists(frontline_file):
            print("Choose your path:")
            print("A. Command Level (策略层) - Make strategic decisions")
            print("B. Frontline Combat (前线作战) - Fight on the ground/air/sea")
            print()
            
            path_choice = input("Choose A or B: ").strip().upper()
            
            if path_choice == 'B':
                # Load frontline roles
                with open(frontline_file, 'r', encoding='utf-8') as f:
                    frontline_data = json.load(f)
                
                print("\n🎖️ Frontline Roles:")
                print("━" * 50)
                
                roles = frontline_data['frontline_roles']
                
                # Group by category
                categories = {}
                for role in roles:
                    cat = role['category']
                    if cat not in categories:
                        categories[cat] = []
                    categories[cat].append(role)
                
                # Display by category
                all_roles_list = []
                idx = 1
                for cat_id, cat_roles in categories.items():
                    cat_name = frontline_data['role_selection_system']['categories'].get(cat_id, cat_id)
                    print(f"\n** {cat_name} **")
                    for role in cat_roles:
                        print(f"{idx}. {role['name']} ({role['name_zh']})")
                        print(f"   {role['description']}")
                        print(f"   Risk: {role['risk_level']} | Prestige: {role['prestige']}/100")
                        
                        if 'moral_burden' in role:
                            print(f"   ⚠️ {role['moral_burden']}")
                        
                        print()
                        all_roles_list.append(role)
                        idx += 1
                
                role_choice = int(input(f"Choose role (1-{len(all_roles_list)}): ")) - 1
                selected_role = all_roles_list[role_choice]
                
                character['role_id'] = selected_role['id']
                character['role_name'] = selected_role['name']
                character['role_category'] = selected_role['category']
                character['risk_level'] = selected_role['risk_level']
                character['prestige'] = selected_role['prestige']
                character['is_frontline'] = True
                
                # Add equipment and abilities
                character['equipment'] = selected_role.get('starting_equipment', [])
                character['abilities'] = selected_role.get('special_abilities', [])
                
            else:
                # Command level roles
                roles = [
                    {"id": "prime_minister", "name": "Prime Minister / 总理", "desc": "Political leader"},
                    {"id": "defense_minister", "name": "Defense Minister / 国防部长", "desc": "Military decision-maker"},
                    {"id": "chief_of_staff", "name": "Chief of Staff / 总参谋长", "desc": "Military commander"},
                    {"id": "intelligence_chief", "name": "Intelligence Chief / 情报局长", "desc": "Covert operator"}
                ]
                
                for i, role in enumerate(roles, 1):
                    print(f"{i}. {role['name']}")
                    print(f"   {role['desc']}")
                    print()
                
                role_choice = int(input(f"Choose position (1-{len(roles)}): ")) - 1
                character['role_id'] = roles[role_choice]['id']
                character['role_name'] = roles[role_choice]['name']
                character['is_frontline'] = False
        else:
            # Fallback to command roles only
            roles = [
                {"id": "prime_minister", "name": "Prime Minister / 总理", "desc": "Political leader"},
                {"id": "defense_minister", "name": "Defense Minister / 国防部长", "desc": "Military decision-maker"},
                {"id": "chief_of_staff", "name": "Chief of Staff / 总参谋长", "desc": "Military commander"},
                {"id": "intelligence_chief", "name": "Intelligence Chief / 情报局长", "desc": "Covert operator"}
            ]
    elif world_genre == 'magical-fantasy':
        roles = [
            {"id": "student", "name": "Student", "desc": "Learning magic"},
            {"id": "professor", "name": "Professor", "desc": "Teaching magic"},
            {"id": "auror", "name": "Auror", "desc": "Dark wizard hunter"},
            {"id": "independent", "name": "Independent Wizard", "desc": "Free agent"}
        ]
    else:
        roles = [
            {"id": "warrior", "name": "Warrior", "desc": "Combat specialist"},
            {"id": "scholar", "name": "Scholar", "desc": "Knowledge seeker"},
            {"id": "leader", "name": "Leader", "desc": "Commander"},
            {"id": "wanderer", "name": "Wanderer", "desc": "Free spirit"}
        ]
    
    for i, role in enumerate(roles, 1):
        print(f"{i}. {role['name']}")
        print(f"   {role['desc']}")
        print()
    
    role_choice = int(input(f"Choose position (1-{len(roles)}): ")) - 1
    character['role_id'] = roles[role_choice]['id']
    character['role_name'] = roles[role_choice]['name']
    
    # Step 4: Personality/Play Style
    print("\n🎭 Step 4: Your Personality")
    print("━" * 50)
    
    personalities = [
        {"id": "aggressive", "name": "Aggressive / 鹰派", "desc": "Prioritize military solutions"},
        {"id": "diplomatic", "name": "Diplomatic / 鸽派", "desc": "Prioritize negotiations"},
        {"id": "pragmatic", "name": "Pragmatic / 现实主义", "desc": "Flexible, context-dependent"},
        {"id": "moral", "name": "Moral / 道德主义", "desc": "Minimize civilian harm"}
    ]
    
    for i, p in enumerate(personalities, 1):
        print(f"{i}. {p['name']}")
        print(f"   {p['desc']}")
        print()
    
    personality_choice = int(input(f"Choose personality (1-{len(personalities)}): ")) - 1
    character['personality_id'] = personalities[personality_choice]['id']
    character['personality_name'] = personalities[personality_choice]['name']
    
    # Step 5: Background (optional)
    print("\n📖 Step 5: Background Story (Optional)")
    print("Enter a brief background (press Enter to skip):")
    background = input("> ").strip()
    if background:
        character['background'] = background
    else:
        character['background'] = generate_default_background(character)
    
    # Step 6: Generate portrait prompt
    print("\n🎨 Generating character portrait...")
    character['portrait_prompt'] = generate_portrait_prompt(character, world_data, factions[faction_choice])
    
    # Save character data
    save_character(character)
    
    print("\n✅ Character created successfully!")
    print(f"Name: {character['name']}")
    print(f"Faction: {character['faction_name']}")
    print(f"Role: {character['role_name']}")
    print(f"Personality: {character['personality_name']}")
    
    return character


def generate_default_background(character):
    """Generate a default background based on character choices"""
    
    role = character.get('role_name', 'Leader')
    personality = character.get('personality_id', 'pragmatic')
    
    templates = {
        "defense_minister": {
            "pragmatic": f"{character['name']}, former special forces operator turned Defense Minister. Rose through ranks via field experience. Known for balancing military necessity with humanitarian concerns."
        },
        "intelligence_chief": {
            "pragmatic": f"{character['name']}, career intelligence officer. Spent 20 years in field operations before appointment. Believes in leverage over brute force."
        }
    }
    
    role_id = character.get('role_id', 'leader')
    
    if role_id in templates and personality in templates[role_id]:
        return templates[role_id][personality]
    
    return f"{character['name']}, a {personality} {role} committed to their faction's success."


def generate_portrait_prompt(character, world_data, faction_data):
    """Generate AI image prompt for character portrait"""
    
    name = character['name']
    role = character.get('role_name', 'Leader')
    faction_name = faction_data.get('name_en', 'Unknown')
    world_genre = world_data.get('genre', 'adventure')
    
    # Base prompt structure
    prompt_parts = [
        f"Portrait of {name}, a",
        role.lower(),
        f"from {faction_name}."
    ]
    
    # Add genre-specific details
    if world_genre == 'modern_military_strategy':
        prompt_parts.extend([
            "Command & Conquer Generals style portrait.",
            "3D render, dramatic military commander aesthetic.",
            "Wearing tactical uniform with rank insignia and faction colors.",
            "Command center background with holographic tactical displays.",
            "Heroic pose, determined expression.",
            "Age 35-50, battle-hardened but stylized features.",
            "Cinematic lighting with red/blue accent lights.",
            "RTS game character portrait style - not photorealistic.",
            "Similar to C&C Generals faction leaders."
        ])
    elif world_genre == 'magical-fantasy':
        prompt_parts.extend([
            "Fantasy art style, magical atmosphere.",
            "Wearing wizard robes with house colors.",
            "Hogwarts castle background.",
            "Wise and determined expression.",
            "Wand in hand, magical aura."
        ])
    else:
        prompt_parts.extend([
            "Epic fantasy portrait.",
            "Traditional clothing of their faction.",
            "Atmospheric background.",
            "Noble and determined expression."
        ])
    
    # Add personality traits
    personality = character.get('personality_id', 'pragmatic')
    if personality == 'aggressive':
        prompt_parts.append("Fierce, intense gaze.")
    elif personality == 'diplomatic':
        prompt_parts.append("Calm, thoughtful demeanor.")
    elif personality == 'pragmatic':
        prompt_parts.append("Sharp, calculating eyes.")
    elif personality == 'moral':
        prompt_parts.append("Compassionate but firm expression.")
    
    return " ".join(prompt_parts)


def save_character(character):
    """Save character to JSON file"""
    
    world_id = character['world_id']
    user_id = character['user_id']
    
    # Character file path
    saves_dir = os.path.expanduser("~/.openclaw/yumfu/saves")
    os.makedirs(saves_dir, exist_ok=True)
    
    char_file = os.path.join(saves_dir, f"{world_id}_{user_id}_character.json")
    
    with open(char_file, 'w', encoding='utf-8') as f:
        json.dump(character, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Character saved to: {char_file}")


def main():
    """Main entry point"""
    
    if len(sys.argv) < 2:
        print("Usage: python create_character.py <world_id> [user_id]")
        print("\nAvailable worlds:")
        worlds_dir = os.path.join(os.path.dirname(__file__), '..', 'worlds')
        for world in os.listdir(worlds_dir):
            world_path = os.path.join(worlds_dir, world)
            if os.path.isdir(world_path) and os.path.exists(os.path.join(world_path, 'world.json')):
                print(f"  - {world}")
        sys.exit(1)
    
    world_id = sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else "default"
    
    character = create_character(world_id, user_id)
    
    print("\n🎮 Ready to start your adventure!")
    print(f"Use: python load_game.py {world_id} {user_id}")


if __name__ == "__main__":
    main()
