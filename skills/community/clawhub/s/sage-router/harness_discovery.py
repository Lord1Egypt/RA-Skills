#!/usr/bin/env python3
"""
Harness-agnostic config discovery for Sage Router.

This module enables Sage Router to discover and import configuration/OAuth/JWT
material from multiple agentic harnesses, not just OpenClaw.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger("harness_discovery")

# Known harness config schemas
HARNESS_SCHEMAS = {
    'openclaw': {
        'config_file': 'openclaw.json',
        'dotenv_file': '.env',
        'auth_dir': 'agents/{agent}/agent',
        'auth_profiles': 'auth-profiles.json',
        'auth_state': 'auth-state.json',
        'models_key': 'models.providers',
        'provider_api_key': 'apiKey',
        'provider_base_url': 'baseUrl',
        'provider_api_type': 'api',
    },
    'hermes': {
        'config_file': 'config.yaml',
        'auth_file': 'auth.yaml',
        'models_key': 'providers',
        'provider_api_key': 'api_key',
        'provider_base_url': 'base_url',
        'provider_api_type': 'api_type',
    },
    'pi': {
        'config_file': 'config.json',
        'auth_file': 'tokens.json',
        'models_key': 'models',
        'provider_api_key': 'apiKey',
        'provider_base_url': 'baseUrl',
        'provider_api_type': 'apiType',
    },
}

# Environment variable names that can point to harness configs
HARNESS_CONFIG_ENV_VARS = [
    'SAGE_ROUTER_CONFIG_SOURCE',      # Primary: path to harness config dir
    'OPENCLAW_CONFIG',                # OpenClaw-specific
    'HERMES_CONFIG',                  # Hermes-specific
    'PI_CONFIG',                      # Pi-specific
    'CODEX_CONFIG',                   # Codex CLI config
]


def detect_harness_in_path(path: str) -> Optional[str]:
    """Detect which harness (if any) is present at the given path."""
    path = os.path.expanduser(path)

    for harness_name, schema in HARNESS_SCHEMAS.items():
        config_file = os.path.join(path, schema['config_file'])
        if os.path.exists(config_file):
            return harness_name

    return None


def scan_app_data_for_harnesses(app_data_dir: str) -> Dict[str, str]:
    """
    Scan APP_DATA_DIR for known harness config directories.

    Returns a dict mapping harness_name -> config_directory_path
    """
    harnesses = {}
    app_data_dir = os.path.expanduser(app_data_dir)

    if not os.path.exists(app_data_dir):
        logger.debug(f"APP_DATA_DIR does not exist: {app_data_dir}")
        return harnesses

    # Direct subdirectories that might contain harness configs
    for entry in os.listdir(app_data_dir):
        entry_path = os.path.join(app_data_dir, entry)
        if not os.path.isdir(entry_path):
            continue

        harness = detect_harness_in_path(entry_path)
        if harness:
            harnesses[harness] = entry_path
            logger.info(f"Detected {harness} harness at {entry_path}")

    # Also check well-known paths within app-data
    well_known = {
        'openclaw': ['.openclaw', 'openclaw', 'config/openclaw'],
        'hermes': ['.hermes', 'hermes', 'config/hermes'],
        'pi': ['.pi', 'pi', 'config/pi'],
    }

    for harness, subdirs in well_known.items():
        if harness in harnesses:
            continue  # Already found
        for subdir in subdirs:
            candidate = os.path.join(app_data_dir, subdir)
            if os.path.exists(candidate):
                harnesses[harness] = candidate
                logger.info(f"Detected {harness} harness at {candidate}")
                break

    return harnesses


def load_openclaw_providers_from_path(config_path: str) -> Dict[str, Any]:
    """Load providers from an OpenClaw config directory."""
    providers = {}
    schema = HARNESS_SCHEMAS['openclaw']

    try:
        config_file = os.path.join(config_path, schema['config_file'])
        if not os.path.exists(config_file):
            return providers

        with open(config_file) as f:
            config = json.load(f)

        # Navigate to models.providers using dot notation
        parts = schema['models_key'].split('.')
        data = config
        for part in parts:
            data = data.get(part, {})

        for provider_name, provider_cfg in data.items():
            providers[provider_name] = {
                'name': provider_name,
                'harness': 'openclaw',
                'base_url': provider_cfg.get(schema['provider_base_url'], ''),
                'api_type': provider_cfg.get(schema['provider_api_type'], 'openai-completions'),
                'api_key': provider_cfg.get(schema['provider_api_key'], ''),
                'models': provider_cfg.get('models', []),
                'source_path': config_path,
            }

        # Load auth profiles if available
        auth_profiles = load_openclaw_auth_profiles(config_path)
        if auth_profiles:
            for profile_name, profile in auth_profiles.items():
                provider_name = profile.get('provider', profile_name.split(':')[0])
                if provider_name in providers:
                    # Merge auth info
                    providers[provider_name]['oauth_profile'] = profile_name
                    providers[provider_name]['oauth_access_token'] = profile.get('access', '')
                    providers[provider_name]['oauth_refresh_token'] = profile.get('refresh', '')
                    providers[provider_name]['oauth_expires'] = profile.get('expires', 0)

        logger.info(f"Loaded {len(providers)} providers from OpenClaw at {config_path}")

    except Exception as e:
        logger.debug(f"Failed to load OpenClaw providers from {config_path}: {e}")

    return providers


def load_openclaw_auth_profiles(config_path: str) -> Dict[str, Any]:
    """Load OAuth auth profiles from OpenClaw agent auth directory."""
    schema = HARNESS_SCHEMAS['openclaw']
    auth_profiles = {}

    # Try to find auth profiles in agents directory
    agents_dir = os.path.join(config_path, 'agents')
    if not os.path.exists(agents_dir):
        return auth_profiles

    # Try main agent first, then others
    for agent in ['main'] + os.listdir(agents_dir):
        agent_dir = os.path.join(agents_dir, agent, 'agent')
        auth_file = os.path.join(agent_dir, schema['auth_profiles'])

        if os.path.exists(auth_file):
            try:
                with open(auth_file) as f:
                    auth = json.load(f)
                profiles = auth.get('profiles', {})
                auth_profiles.update(profiles)
                logger.debug(f"Loaded auth profiles from {auth_file}")
            except Exception as e:
                logger.debug(f"Failed to load auth profiles from {auth_file}: {e}")

    return auth_profiles


def load_hermes_providers_from_path(config_path: str) -> Dict[str, Any]:
    """Load providers from a Hermes config directory (YAML)."""
    providers = {}

    try:
        import yaml
    except ImportError:
        logger.debug("PyYAML not installed, skipping Hermes config loading")
        return providers

    try:
        config_file = os.path.join(config_path, 'config.yaml')
        if not os.path.exists(config_file):
            return providers

        with open(config_file) as f:
            config = yaml.safe_load(f)

        providers_cfg = config.get('providers', {})
        for provider_name, provider_cfg in providers_cfg.items():
            providers[provider_name] = {
                'name': provider_name,
                'harness': 'hermes',
                'base_url': provider_cfg.get('base_url', ''),
                'api_type': provider_cfg.get('api_type', 'openai-completions'),
                'api_key': provider_cfg.get('api_key', ''),
                'models': provider_cfg.get('models', []),
                'source_path': config_path,
            }

        logger.info(f"Loaded {len(providers)} providers from Hermes at {config_path}")

    except Exception as e:
        logger.debug(f"Failed to load Hermes providers from {config_path}: {e}")

    return providers


def load_generic_providers_from_path(config_path: str) -> Dict[str, Any]:
    """Try to load providers from an unknown harness using heuristics."""
    providers = {}
    harness = detect_harness_in_path(config_path)

    if harness == 'openclaw':
        return load_openclaw_providers_from_path(config_path)
    elif harness == 'hermes':
        return load_hermes_providers_from_path(config_path)

    # Try generic JSON config
    try:
        for filename in ['config.json', 'providers.json', 'settings.json']:
            config_file = os.path.join(config_path, filename)
            if os.path.exists(config_file):
                with open(config_file) as f:
                    config = json.load(f)

                # Look for providers key
                if 'providers' in config:
                    for provider_name, provider_cfg in config['providers'].items():
                        providers[provider_name] = {
                            'name': provider_name,
                            'harness': 'unknown',
                            'base_url': provider_cfg.get('baseUrl', provider_cfg.get('base_url', '')),
                            'api_type': provider_cfg.get('api', provider_cfg.get('api_type', 'openai-completions')),
                            'api_key': provider_cfg.get('apiKey', provider_cfg.get('api_key', '')),
                            'models': provider_cfg.get('models', []),
                            'source_path': config_path,
                        }

                logger.info(f"Loaded {len(providers)} providers from generic config at {config_path}")
                break
    except Exception as e:
        logger.debug(f"Failed to load generic providers from {config_path}: {e}")

    return providers


def discover_all_harness_providers(
    app_data_dir: Optional[str] = None,
    explicit_sources: Optional[List[str]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Discover providers from all available harness configs.

    Args:
        app_data_dir: Directory to scan for harness configs (e.g., APP_DATA_DIR/data)
        explicit_sources: Optional list of explicit config source paths

    Returns:
        Dict mapping provider_name -> provider_config, with 'harness' key
        indicating which harness the config came from.
    """
    all_providers = {}
    sources_loaded = []

    # 1. Check explicit sources first (highest priority)
    if explicit_sources:
        for source in explicit_sources:
            if os.path.exists(source):
                providers = load_generic_providers_from_path(source)
                for name, cfg in providers.items():
                    cfg['source_priority'] = 'explicit'
                    all_providers[name] = cfg
                sources_loaded.append(f"explicit:{source}")

    # 2. Check environment variable overrides
    for env_var in HARNESS_CONFIG_ENV_VARS:
        path = os.environ.get(env_var)
        if path and os.path.exists(path):
            providers = load_generic_providers_from_path(path)
            for name, cfg in providers.items():
                if name not in all_providers:
                    cfg['source_priority'] = 'env'
                    all_providers[name] = cfg
            sources_loaded.append(f"env:{env_var}")

    # 3. Scan APP_DATA_DIR for harnesses
    if app_data_dir:
        harnesses = scan_app_data_for_harnesses(app_data_dir)
        for harness_name, harness_path in harnesses.items():
            if harness_name == 'openclaw':
                providers = load_openclaw_providers_from_path(harness_path)
            elif harness_name == 'hermes':
                providers = load_hermes_providers_from_path(harness_path)
            else:
                providers = load_generic_providers_from_path(harness_path)

            for name, cfg in providers.items():
                if name not in all_providers:
                    cfg['source_priority'] = f"scanned:{harness_name}"
                    all_providers[name] = cfg
            sources_loaded.append(f"scanned:{harness_name}:{harness_path}")

    # 4. Fallback: check SAGE_ROUTER_HOME
    sage_router_home = os.environ.get('SAGE_ROUTER_HOME', os.path.expanduser('~/.sage-router'))
    if os.path.exists(sage_router_home):
        harness = detect_harness_in_path(sage_router_home)
        if harness:
            providers = load_generic_providers_from_path(sage_router_home)
            for name, cfg in providers.items():
                if name not in all_providers:
                    cfg['source_priority'] = 'fallback'
                    all_providers[name] = cfg
            sources_loaded.append(f"fallback:{sage_router_home}")

    logger.info(f"Discovered providers from sources: {sources_loaded}")
    logger.info(f"Total unique providers: {len(all_providers)}")

    return all_providers


def get_harness_discovery_info() -> Dict[str, Any]:
    """Return diagnostic info about harness discovery state."""
    return {
        'known_harnesses': list(HARNESS_SCHEMAS.keys()),
        'config_env_vars': HARNESS_CONFIG_ENV_VARS,
        'sage_router_home': os.environ.get('SAGE_ROUTER_HOME', '~/.sage-router (default)'),
        'detected_harnesses': scan_app_data_for_harnesses(
            os.environ.get('APP_DATA_DIR', '/app-data')
        ),
    }


# Convenience function for router.py integration
def load_harness_agnostic_providers(
    sage_router_home: Optional[str] = None,
    app_data_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Load providers using harness-agnostic discovery.

    This is the main entry point for integrating with router.py.
    """
    # Determine app_data_dir
    if not app_data_dir:
        # Try common locations
        for candidate in [
            os.environ.get('APP_DATA_DIR'),
            os.path.expanduser('~/app-data'),
            '/app-data',
            '/data',
        ]:
            if candidate and os.path.exists(candidate):
                app_data_dir = candidate
                break

    # Check for explicit config source
    explicit_sources = []
    config_source = os.environ.get('SAGE_ROUTER_CONFIG_SOURCE')
    if config_source:
        if config_source == 'auto':
            # Auto-detect from APP_DATA_DIR
            pass
        elif os.path.exists(config_source):
            explicit_sources.append(config_source)

    return discover_all_harness_providers(
        app_data_dir=app_data_dir,
        explicit_sources=explicit_sources
    )


if __name__ == '__main__':
    # Test harness discovery
    logging.basicConfig(level=logging.INFO)

    print("Harness Discovery Diagnostic")
    print("=" * 50)

    info = get_harness_discovery_info()
    print(f"\nKnown harness schemas: {info['known_harnesses']}")
    print(f"SAGE_ROUTER_HOME: {info['sage_router_home']}")
    print(f"\nDetected harnesses:")
    for harness, path in info['detected_harnesses'].items():
        print(f"  - {harness}: {path}")

    # Try loading providers
    print("\n" + "=" * 50)
    providers = load_harness_agnostic_providers()
    print(f"\nDiscovered {len(providers)} providers:")
    for name, cfg in providers.items():
        print(f"  - {name} (from {cfg.get('harness', 'unknown')})")
