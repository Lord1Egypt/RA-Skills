#!/usr/bin/env python3
"""
Grasshopper Player automation - run GH definitions with custom parameters.

Usage:
    python3 grasshopper.py run "C:/path/to/file.gh" --Lichthoehe 2200 --Lichtbreite 1000
    python3 grasshopper.py info "C:/path/to/file.gh"  # Show available parameters
    python3 grasshopper.py run "C:/path/to/file.gh" --validate --Lichthoehe 2200
    python3 grasshopper.py batch batch_config.json --dry-run
"""

import argparse
import json
import logging
import sys
import time
import re
from dataclasses import dataclass, field
from typing import List
from rhino_client import RhinoClient
from presets import PresetManager

logger = logging.getLogger("rhinoclaw.grasshopper")

# Parameter alias mapping (GH nicknames → Player prompt names)
PARAM_ALIASES = {
    'Pt': 'Point',
    'Punkt': 'Point',
    'Position': 'Point',
    'Pos': 'Point',
}


def normalize_param_name(name: str) -> str:
    """Map GH nicknames to GrasshopperPlayer prompt names."""
    return PARAM_ALIASES.get(name, name)


# --- Validation ---

@dataclass
class ValidationResult:
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def validate_parameters(params: dict, gh_params: dict) -> ValidationResult:
    """Validate parameters against GH definition constraints.

    Args:
        params: User-provided parameters (already alias-normalized)
        gh_params: Parameter info from get_gh_parameters()
    """
    errors = []
    warnings = []

    for name, value in params.items():
        if name == 'Point':
            # Validate point format
            if isinstance(value, str):
                parts = value.replace(' ', '').split(',')
                if len(parts) != 3:
                    errors.append(f"Point format invalid: '{value}' (expected x,y,z)")
                else:
                    try:
                        [float(p) for p in parts]
                    except ValueError:
                        errors.append(f"Point contains non-numeric values: '{value}'")
            continue

        if name not in gh_params:
            warnings.append(f"Unknown parameter: '{name}'")
            continue

        info = gh_params[name]
        param_type = info.get('type', '')

        # Number validation
        if param_type in ('Number', 'NumberSlider', 'Integer'):
            try:
                num = float(value)
                min_val = info.get('min')
                max_val = info.get('max')
                if min_val is not None and num < float(min_val):
                    errors.append(f"{name}={value} below minimum ({min_val})")
                if max_val is not None and num > float(max_val):
                    errors.append(f"{name}={value} above maximum ({max_val})")
            except (ValueError, TypeError):
                errors.append(f"{name}='{value}' is not a valid number")

        # Boolean validation
        elif param_type == 'Boolean':
            if str(value).lower() not in ('true', 'false', '1', '0', 'yes', 'no'):
                errors.append(f"{name}='{value}' is not a valid boolean")

    return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)


# --- Object GUID Tracking ---

def get_all_object_ids() -> set:
    """Get all object GUIDs in current document."""
    with RhinoClient() as client:
        code = '''
import rhinoscriptsyntax as rs
ids = rs.AllObjects()
if ids:
    print(",".join(str(id) for id in ids))
else:
    print("")
'''
        result = client.send_command('execute_rhinoscript_python_code', {'code': code})
        output = result.get('result', {}).get('output', '').strip()
        if output:
            return set(output.split(','))
        return set()


def get_objects_by_layer(guids: list) -> dict:
    """Group GUIDs by their layer."""
    if not guids:
        return {}
    with RhinoClient() as client:
        guids_str = json.dumps(guids)
        code = f'''
import rhinoscriptsyntax as rs
import json
guids = {guids_str}
by_layer = {{}}
for guid in guids:
    try:
        layer = rs.ObjectLayer(guid)
        if layer not in by_layer:
            by_layer[layer] = []
        by_layer[layer].append(str(guid))
    except:
        pass
print(json.dumps(by_layer))
'''
        result = client.send_command('execute_rhinoscript_python_code', {'code': code})
        output = result.get('result', {}).get('output', '{}').strip()
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {}


def get_gh_parameters(file_path: str) -> dict:
    """Load GH file and get available parameters."""
    with RhinoClient() as client:
        result = client.send_command('load_grasshopper_definition', {'file_path': file_path})
        
        if result.get('status') != 'success':
            raise Exception(f"Failed to load GH file: {result.get('message')}")
        
        definition = result.get('result', {})
        definition_id = definition.get('definition_id')
        
        # Extract unique parameters with their defaults
        params = {}
        for p in definition.get('parameters', []):
            nickname = p.get('nickname', '')
            if nickname and nickname not in params:
                param_info = {
                    'name': p.get('name'),
                    'type': p.get('type'),
                    'value': p.get('value'),
                }
                if 'min' in p:
                    param_info['min'] = p.get('min')
                    param_info['max'] = p.get('max')
                params[nickname] = param_info
        
        # Unload definition (we'll use GrasshopperPlayer instead)
        client.send_command('unload_grasshopper_definition', {'definition_id': definition_id})
        
        return params


def start_grasshopper_player(file_path: str) -> bool:
    """Start GrasshopperPlayer command in Rhino."""
    with RhinoClient() as client:
        # Use RunScript to start GrasshopperPlayer
        # The trick: run it via SendKeystrokes so it doesn't block
        escaped_path = file_path.replace('\\', '\\\\')
        code = f'''
import Rhino
cmd = '_-GrasshopperPlayer "{escaped_path}"'
Rhino.RhinoApp.SendKeystrokes(cmd + chr(13), True)
'''
        result = client.send_command('execute_rhinoscript_python_code', {'code': code})
        return result.get('status') == 'success'


def get_current_prompt() -> str:
    """Get current Rhino command prompt."""
    with RhinoClient() as client:
        result = client.send_command('get_command_history', {'lines': 1})
        return result.get('result', {}).get('command_prompt', '')


def send_input(text: str):
    """Send text input to Rhino command line."""
    with RhinoClient() as client:
        escaped = text.replace('"', '\\"')
        code = f'import Rhino; Rhino.RhinoApp.SendKeystrokes("{escaped}" + chr(13), True)'
        client.send_command('execute_rhinoscript_python_code', {'code': code})


def parse_prompt(prompt: str) -> tuple:
    """Parse a GrasshopperPlayer prompt to extract parameter name and default value.
    
    Examples:
        "Lichthoehe <2100>" -> ("Lichthoehe", "2100")
        "Get Point ( Undo )" -> ("Point", None)
        "RahmenbreiteL <120> ( Undo )" -> ("RahmenbreiteL", "120")
        "Bandseite:" -> ("Bandseite", None)
        "Get String ( Undo )" -> ("Get String", None)
    """
    # Match pattern: Name <default>
    match = re.match(r'([A-Za-z_][A-Za-z0-9_ ]*?)\s*<([^>]+)>', prompt)
    if match:
        return match.group(1).strip(), match.group(2)
    
    # Match "Get Point" or similar
    if 'Point' in prompt:
        return 'Point', None
    
    # Match "Get String" prompt
    if 'Get String' in prompt or 'String' in prompt:
        return 'Get String', None
    
    # Match bare prompt like "Bandseite:" or "Bandseite ( Undo ):"
    match = re.match(r'([A-Za-z_][A-Za-z0-9_äöüÄÖÜ]*)\s*[\(:]', prompt)
    if match:
        return match.group(1).strip(), None
    
    # Match any single-word prompt that looks like a parameter name
    match = re.match(r'^([A-Za-z_][A-Za-z0-9_äöüÄÖÜ]*)\s*$', prompt.strip().rstrip(':'))
    if match:
        return match.group(1).strip(), None
    
    return None, None


def run_grasshopper_player(file_path: str, params: dict = None, timeout: int = 120,
                           track_objects: bool = True, validate: bool = True) -> dict:
    """Run a Grasshopper definition through GrasshopperPlayer with custom parameters.
    
    Args:
        file_path: Path to .gh file (Windows path)
        params: Dict of parameter_name -> value overrides
        timeout: Max seconds to wait
        track_objects: If True, track created object GUIDs via before/after diff
        validate: If True, validate parameters before running
    
    Returns:
        Dict with status and created objects info
    """
    params = params or {}
    
    # Normalize parameter names (aliases)
    params = {normalize_param_name(k): v for k, v in params.items()}
    
    # Validate parameters
    if validate and params:
        try:
            gh_params = get_gh_parameters(file_path)
            validation = validate_parameters(params, gh_params)
            if not validation.valid:
                logger.error(f"Validation failed: {validation.errors}")
                return {
                    'status': 'error',
                    'message': 'Parameter validation failed',
                    'errors': validation.errors,
                    'warnings': validation.warnings
                }
            for w in validation.warnings:
                logger.warning(f"Validation warning: {w}")
        except Exception as e:
            logger.warning(f"Could not validate parameters (continuing anyway): {e}")
    
    # Pre-load GH parameter metadata for smart prompt matching
    gh_param_map = {}  # nickname (lowercase) -> {type, value, min, max}
    gh_prompt_names = set()  # all known parameter nicknames
    try:
        with RhinoClient() as client:
            r = client.send_command('load_grasshopper_definition', {'file_path': file_path})
            gh_meta = r.get('result', {})
            for p in gh_meta.get('parameters', []):
                nick = p.get('nickname', p.get('name', '')).strip()
                if nick:
                    gh_prompt_names.add(nick)
                    ptype = p.get('type', '')
                    # Prefer entries with actual values (NumberSlider over Number)
                    key = nick.lower()
                    if key not in gh_param_map or p.get('value') is not None:
                        gh_param_map[key] = {
                            'name': nick,
                            'type': ptype,
                            'value': p.get('value'),
                            'min': p.get('min'),
                            'max': p.get('max'),
                        }
            defid = gh_meta.get('definition_id')
            if defid:
                client.send_command('unload_grasshopper_definition', {'definition_id': defid})
        logger.info(f"Loaded {len(gh_param_map)} GH parameters for smart matching")
    except Exception as e:
        logger.warning(f"Could not pre-load GH parameters (prompt matching will be basic): {e}")

    # Snapshot object IDs before run
    before_ids = set()
    if track_objects:
        try:
            before_ids = get_all_object_ids()
            logger.debug(f"Objects before run: {len(before_ids)}")
        except Exception as e:
            logger.warning(f"Could not snapshot objects before run: {e}")
            track_objects = False
    
    # Start GrasshopperPlayer
    logger.info(f"Starting GrasshopperPlayer: {file_path}")
    if not start_grasshopper_player(file_path):
        return {'status': 'error', 'message': 'Failed to start GrasshopperPlayer'}
    
    # Wait for player to start
    time.sleep(1)
    
    # Monitor prompts and send inputs
    last_prompt = ''
    start_time = time.time()
    prompts_handled = []
    
    while time.time() - start_time < timeout:
        prompt = get_current_prompt()
        
        if prompt != last_prompt:
            last_prompt = prompt
            
            # Check if player finished
            if prompt.strip() == 'Command':
                if prompts_handled:  # Only finish if we handled at least one prompt
                    logger.info("GrasshopperPlayer finished!")
                    break
                else:
                    time.sleep(0.5)
                    continue
            
            # Parse the prompt
            param_name, default_value = parse_prompt(prompt)
            
            if param_name:
                # Check if we have a custom value for this parameter
                if param_name in params:
                    value = str(params[param_name])
                    logger.info(f"  {param_name}: {value} (custom)")
                elif param_name == 'Point' and 'Point' in params:
                    # Handle point as "x,y,z"
                    pt = params['Point']
                    if isinstance(pt, (list, tuple)):
                        value = f"{pt[0]},{pt[1]},{pt[2]}"
                    else:
                        value = str(pt)
                    logger.info(f"  Point: {value} (custom)")
                elif param_name == 'Point':
                    # Default point to origin
                    value = "0,0,0"
                    logger.info(f"  Point: {value} (default: origin)")
                else:
                    # No custom value — accept default (press Enter)
                    value = ""
                    logger.info(f"  {param_name}: <{default_value}> (default)")
            else:
                # Unrecognized by parse_prompt — try smart matching.
                # Clean up the prompt text to find the parameter name.
                stripped = prompt.strip().rstrip(':').strip()
                # Remove common suffixes like "( Undo )"
                stripped = re.sub(r'\s*\(\s*Undo\s*\)\s*', '', stripped).strip()
                
                if not stripped or stripped == 'Command':
                    time.sleep(0.2)
                    continue
                
                # 1. Check if user passed this param explicitly (case-insensitive)
                matched_key = None
                for k in params:
                    if k.lower() == stripped.lower():
                        matched_key = k
                        break
                
                if matched_key:
                    value = str(params[matched_key])
                    param_name = stripped
                    logger.info(f"  {param_name}: {value} (fuzzy match from --{matched_key})")
                else:
                    # 2. Check GH metadata for info about this parameter
                    gh_info = gh_param_map.get(stripped.lower())
                    if gh_info:
                        param_name = gh_info['name']
                        ptype = gh_info.get('type', '')
                        default_val = gh_info.get('value')
                        if default_val is not None:
                            value = str(default_val)
                            logger.info(f"  {param_name}: {value} (from GH metadata, type={ptype})")
                        else:
                            value = ""
                            logger.info(f"  {param_name}: (GH param, type={ptype}, accepting default)")
                    else:
                        # 3. Completely unknown — just press Enter
                        param_name = stripped
                        value = ""
                        logger.info(f"  {param_name}: (unknown prompt, accepting default)")
            
            # Send the value (works for both recognized and unrecognized prompts)
            send_input(value)
            prompts_handled.append({
                'name': param_name,
                'value': value if value else (default_value or ''),
                'was_custom': param_name in params
            })
            
            time.sleep(0.3)
        else:
            time.sleep(0.2)
    
    # Get final document info
    with RhinoClient() as client:
        result = client.send_command('get_document_info', {})
        doc_info = result.get('result', {})
    
    # Calculate created objects diff
    new_ids = []
    created_by_layer = {}
    if track_objects:
        try:
            after_ids = get_all_object_ids()
            new_ids = list(after_ids - before_ids)
            logger.info(f"Objects created: {len(new_ids)}")
            if new_ids:
                created_by_layer = get_objects_by_layer(new_ids)
        except Exception as e:
            logger.warning(f"Could not calculate object diff: {e}")
    
    return {
        'status': 'success',
        'file': file_path,
        'prompts_handled': prompts_handled,
        'objects_created': len(new_ids) if track_objects else doc_info.get('object_count', 0),
        'created_guids': new_ids if track_objects else [],
        'created_by_layer': created_by_layer if track_objects else {},
        'layers': [l.get('name') for l in doc_info.get('layers', [])]
    }


def run_batch(input_file: str, dry_run: bool = False, continue_on_error: bool = False) -> dict:
    """Run multiple GH definitions from JSON file.

    JSON format:
    {
        "definition": "C:/path/to/file.gh",
        "defaults": {"Rahmendicke": 53},
        "items": [
            {"id": "T01", "Lichthoehe": 2100, "Lichtbreite": 900, "Point": "0,0,0"},
            {"id": "T02", "Lichthoehe": 2000, "Lichtbreite": 800, "Point": "1500,0,0"}
        ]
    }
    """
    with open(input_file) as f:
        config = json.load(f)

    gh_file = config['definition']
    defaults = config.get('defaults', {})
    items = config['items']

    if not items:
        return {'status': 'error', 'message': 'No items in batch file'}

    # Validate all items first
    logger.info(f"Batch: {len(items)} items from {input_file}")
    try:
        gh_params = get_gh_parameters(gh_file)
    except Exception as e:
        logger.warning(f"Could not load GH params for validation: {e}")
        gh_params = {}

    all_valid = True
    for item in items:
        item_id = item.get('id', '?')
        merged = {**defaults, **{k: v for k, v in item.items() if k != 'id'}}
        merged = {normalize_param_name(k): v for k, v in merged.items()}
        validation = validate_parameters(merged, gh_params)
        if not validation.valid:
            logger.error(f"  {item_id}: {validation.errors}")
            all_valid = False
        for w in validation.warnings:
            logger.warning(f"  {item_id}: {w}")

    if not all_valid and not continue_on_error:
        return {'status': 'error', 'message': 'Validation failed. Use --continue to ignore.'}

    if dry_run:
        return {
            'status': 'dry_run',
            'total': len(items),
            'message': 'Validation passed' if all_valid else 'Validation has errors'
        }

    # Run each item
    results = []
    for i, item in enumerate(items):
        item_id = item.get('id', f'item_{i}')
        merged = {**defaults, **{k: v for k, v in item.items() if k != 'id'}}

        logger.info(f"Batch [{i+1}/{len(items)}] {item_id}")

        try:
            result = run_grasshopper_player(gh_file, merged, validate=False)
            result['batch_id'] = item_id
            results.append(result)
        except Exception as e:
            if continue_on_error:
                results.append({'batch_id': item_id, 'status': 'error', 'message': str(e)})
            else:
                return {
                    'status': 'error',
                    'message': f'Failed at {item_id}: {e}',
                    'completed': results
                }

    succeeded = sum(1 for r in results if r.get('status') == 'success')
    failed = sum(1 for r in results if r.get('status') == 'error')

    return {
        'status': 'success' if failed == 0 else 'partial',
        'total': len(items),
        'succeeded': succeeded,
        'failed': failed,
        'results': results
    }


def run_preset(preset_name: str, overrides: dict = None, point: str = None,
               validate_only: bool = False, track_objects: bool = True) -> dict:
    """Run a preset with optional parameter overrides."""
    manager = PresetManager()
    preset = manager.get_preset(preset_name)

    # Start with preset params
    params = dict(preset['params'])

    # Apply alias resolution to overrides
    if overrides:
        resolved = manager.resolve_aliases(overrides, preset['aliases'])
        params.update(resolved)

    # Set point if provided
    if point:
        params['Point'] = point

    logger.info(f"Preset '{preset_name}': {preset['description']}")
    logger.info(f"Template: {preset['template_name']} → {preset['file']}")

    if validate_only:
        # Validate parameters against GH definition
        normalized = {normalize_param_name(k): v for k, v in params.items()}
        try:
            gh_params = get_gh_parameters(preset['file'])
            validation = validate_parameters(normalized, gh_params)
            return {
                'status': 'valid' if validation.valid else 'invalid',
                'preset': preset_name,
                'errors': validation.errors,
                'warnings': validation.warnings,
                'parameters': normalized
            }
        except Exception as e:
            return {'status': 'error', 'message': f'Could not validate: {e}'}

    return run_grasshopper_player(
        preset['file'], params,
        track_objects=track_objects
    )


def show_presets(category: str = None):
    """List available presets."""
    manager = PresetManager()
    presets = manager.list_presets(category)

    if not presets:
        print("No presets found.")
        return

    print(f"Available Presets ({len(presets)}):")
    print("-" * 60)
    for p in presets:
        print(f"  {p['name']:<22} {p['description']}")


def show_templates(category: str = None):
    """List available templates."""
    manager = PresetManager()
    templates = manager.list_templates(category)

    if not templates:
        print("No templates found.")
        return

    print(f"Available Templates ({len(templates)}):")
    print("-" * 60)
    for t in templates:
        print(f"  {t['name']:<22} {t['description']}")


def show_preset_info(preset_name: str):
    """Show detailed info about a preset."""
    manager = PresetManager()
    preset = manager.get_preset(preset_name)

    print(f"Preset: {preset['name']}")
    print(f"Description: {preset['description']}")
    print(f"Template: {preset['template_name']}")
    print(f"GH File: {preset['file']}")
    print(f"Category: {preset['category']}")
    print(f"\nParameters:")
    for k, v in sorted(preset['params'].items()):
        print(f"  --{k} = {v}")
    if preset['aliases']:
        print(f"\nAliases:")
        for alias, target in sorted(preset['aliases'].items()):
            print(f"  --{alias} → --{target}")
    if preset['validation']:
        print(f"\nValidation Rules:")
        for param, rules in sorted(preset['validation'].items()):
            print(f"  {param}: {rules}")


def show_info(file_path: str):
    """Show available parameters for a GH file."""
    print(f"Loading: {file_path}")
    params = get_gh_parameters(file_path)
    
    print(f"\nAvailable Parameters ({len(params)}):")
    print("-" * 60)
    
    for name, info in sorted(params.items()):
        value_str = ""
        if info.get('value') is not None:
            value_str = f" = {info['value']}"
        
        range_str = ""
        if info.get('min') is not None:
            range_str = f" [{info['min']} - {info['max']}]"
        
        print(f"  --{name}{value_str}{range_str}  ({info.get('type', '?')})")


def main():
    parser = argparse.ArgumentParser(
        description='Run Grasshopper definitions with custom parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show available parameters
  python3 grasshopper.py info "C:/path/to/file.gh"
  
  # Run with defaults
  python3 grasshopper.py run "C:/path/to/file.gh"
  
  # Run with custom parameters
  python3 grasshopper.py run "C:/path/to/file.gh" --Lichthoehe 2200 --Lichtbreite 1000
  
  # Set insertion point
  python3 grasshopper.py run "C:/path/to/file.gh" --Point 100,200,0
  
  # Validate only (dry-run)
  python3 grasshopper.py run "C:/path/to/file.gh" --validate --Lichthoehe 2200
  
  # Batch processing
  python3 grasshopper.py batch batch_config.json
  python3 grasshopper.py batch batch_config.json --dry-run
  python3 grasshopper.py batch batch_config.json --continue
"""
    )
    
    subparsers = parser.add_subparsers(dest='action', required=True)
    
    # Info command
    info_p = subparsers.add_parser('info', help='Show available parameters')
    info_p.add_argument('file', help='Path to .gh file (Windows path)')
    
    # Run command
    run_p = subparsers.add_parser('run', help='Run GH definition')
    run_p.add_argument('file', help='Path to .gh file (Windows path)')
    run_p.add_argument('--timeout', type=int, default=120, help='Timeout in seconds')
    run_p.add_argument('--validate', '--dry-run', action='store_true', dest='validate_only',
                       help='Validate parameters only, do not run')
    run_p.add_argument('--no-track', action='store_true',
                       help='Disable object GUID tracking')
    
    # Batch command
    batch_p = subparsers.add_parser('batch', help='Run batch from JSON file')
    batch_p.add_argument('file', help='Path to batch JSON file')
    batch_p.add_argument('--dry-run', action='store_true', help='Validate only, do not run')
    batch_p.add_argument('--continue', dest='continue_on_error', action='store_true',
                         help='Continue on errors')
    
    # Presets list
    presets_p = subparsers.add_parser('presets', help='List available presets')
    presets_p.add_argument('--category', '-cat', type=str, help='Filter by category')

    # Templates list
    templates_p = subparsers.add_parser('templates', help='List available templates')
    templates_p.add_argument('--category', '-cat', type=str, help='Filter by category')

    # Preset run
    preset_p = subparsers.add_parser('preset', help='Run a preset')
    preset_p.add_argument('name', type=str, help='Preset name')
    preset_p.add_argument('--info', action='store_true', help='Show preset details without running')
    preset_p.add_argument('--Point', type=str, help='Insertion point (x,y,z)')
    preset_p.add_argument('--validate', '--dry-run', action='store_true', dest='validate_only',
                          help='Validate only')
    preset_p.add_argument('--no-track', action='store_true', help='Disable object tracking')

    # Parse known args first to get the file, then parse remaining as parameters
    args, remaining = parser.parse_known_args()
    
    if args.action == 'info':
        show_info(args.file)
        
    elif args.action == 'run':
        # Parse remaining args as --ParamName value pairs
        custom_params = {}
        i = 0
        while i < len(remaining):
            arg = remaining[i]
            if arg.startswith('--'):
                param_name = arg[2:]
                if i + 1 < len(remaining) and not remaining[i + 1].startswith('--'):
                    value = remaining[i + 1]
                    # Try to convert to number if possible
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                    custom_params[param_name] = value
                    i += 2
                else:
                    custom_params[param_name] = True
                    i += 1
            else:
                i += 1
        
        # Validate-only mode
        if args.validate_only:
            normalized = {normalize_param_name(k): v for k, v in custom_params.items()}
            try:
                gh_params = get_gh_parameters(args.file)
                validation = validate_parameters(normalized, gh_params)
                result = {
                    'status': 'valid' if validation.valid else 'invalid',
                    'errors': validation.errors,
                    'warnings': validation.warnings,
                    'parameters': normalized
                }
            except Exception as e:
                result = {'status': 'error', 'message': f'Could not validate: {e}'}
            print(json.dumps(result, indent=2))
            sys.exit(0 if result.get('status') == 'valid' else 1)
        
        if custom_params:
            print(f"Custom parameters: {custom_params}")
        
        result = run_grasshopper_player(
            args.file, custom_params, args.timeout,
            track_objects=not args.no_track
        )
        print(json.dumps(result, indent=2))
    
    elif args.action == 'batch':
        result = run_batch(
            args.file,
            dry_run=args.dry_run,
            continue_on_error=args.continue_on_error
        )
        print(json.dumps(result, indent=2))
        if result.get('status') == 'error':
            sys.exit(1)

    elif args.action == 'presets':
        show_presets(getattr(args, 'category', None))

    elif args.action == 'templates':
        show_templates(getattr(args, 'category', None))

    elif args.action == 'preset':
        if args.info:
            show_preset_info(args.name)
        else:
            # Parse remaining args as overrides
            custom_params = {}
            i = 0
            while i < len(remaining):
                arg = remaining[i]
                if arg.startswith('--') and arg[2:] not in ('info', 'validate', 'dry-run', 'no-track'):
                    param_name = arg[2:]
                    if i + 1 < len(remaining) and not remaining[i + 1].startswith('--'):
                        value = remaining[i + 1]
                        try:
                            if '.' in value:
                                value = float(value)
                            else:
                                value = int(value)
                        except ValueError:
                            pass
                        custom_params[param_name] = value
                        i += 2
                    else:
                        custom_params[param_name] = True
                        i += 1
                else:
                    i += 1

            result = run_preset(
                args.name,
                overrides=custom_params if custom_params else None,
                point=getattr(args, 'Point', None),
                validate_only=getattr(args, 'validate_only', False),
                track_objects=not getattr(args, 'no_track', False),
            )
            print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
