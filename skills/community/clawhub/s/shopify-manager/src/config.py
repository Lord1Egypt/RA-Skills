"""Configuration management for Shopify Manager skill."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


DEFAULT_CONFIG = {
    "store": {
        "domain": None,
        "access_token": None,
        "api_version": "2024-01",
    },
    "defaults": {
        "location_id": None,
        "currency": "USD",
        "weight_unit": "lb",
    },
    "permissions": {
        "allow_product_changes": True,
        "allow_order_fulfillment": True,
        "allow_content_updates": True,
        "allow_theme_edits": False,
        "allow_refunds": False,
        "allow_bulk_operations": True,
    },
    "safety": {
        "dry_run_by_default": True,
        "require_confirmation_for": [
            "refunds",
            "inventory_reductions",
            "theme_changes",
            "bulk_operations",
            "product_deletions",
        ],
        "max_products_per_bulk": 50,
        "rate_limit_delay": 0.5,
    },
    "logging": {
        "audit_log_path": "memory/shopify-changes.jsonl",
        "verbose": False,
    },
}


class Config:
    """Shopify Manager configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config()
        self._config = self._load()
    
    def _find_config(self) -> str:
        """Find configuration file in standard locations."""
        search_paths = [
            "shopify-config.yaml",
            "shopify-config.yml",
            os.path.expanduser("~/.config/shopify-manager/config.yaml"),
            os.path.expanduser("~/.shopify-manager/config.yaml"),
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError(
            "No shopify-config.yaml found. "
            "Create one from shopify-config-example.yaml"
        )
    
    def _load(self) -> Dict[str, Any]:
        """Load and merge configuration."""
        config = DEFAULT_CONFIG.copy()
        
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    config = self._deep_merge(config, user_config)
        
        # Override with environment variables
        if os.getenv('SHOPIFY_DOMAIN'):
            config['store']['domain'] = os.getenv('SHOPIFY_DOMAIN')
        if os.getenv('SHOPIFY_ACCESS_TOKEN'):
            config['store']['access_token'] = os.getenv('SHOPIFY_ACCESS_TOKEN')
        
        self._validate(config)
        return config
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def _validate(self, config: Dict[str, Any]):
        """Validate configuration."""
        store = config.get('store', {})
        
        if not store.get('domain'):
            raise ValueError("store.domain is required in configuration")
        
        if not store.get('access_token'):
            raise ValueError("store.access_token is required in configuration")
        
        # Normalize domain
        domain = store['domain']
        if not domain.endswith('.myshopify.com'):
            domain = f"{domain}.myshopify.com"
        config['store']['domain'] = domain
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    @property
    def store_domain(self) -> str:
        return self._config['store']['domain']
    
    @property
    def access_token(self) -> str:
        return self._config['store']['access_token']
    
    @property
    def api_version(self) -> str:
        return self._config['store']['api_version']
    
    @property
    def dry_run_by_default(self) -> bool:
        return self._config['safety']['dry_run_by_default']
    
    @property
    def requires_confirmation(self, operation: str) -> bool:
        return operation in self._config['safety']['require_confirmation_for']
    
    @property
    def audit_log_path(self) -> str:
        return self._config['logging']['audit_log_path']
