"""
Self-Improving Claw - Hooks Manager Module

Supports:
- onSessionEnd: Triggered when session ends
- onError: Triggered when error occurs
- onRecovery: Triggered when recovery from error
"""

from pathlib import Path
from typing import List, Dict, Any
import importlib.util
import traceback


class HookManager:
    """Manager for loading and applying improvement hooks."""
    
    def __init__(self, workspace: Path):
        self.workspace = Path(workspace)
        self.hooks_path = self.workspace / 'hooks'
        self.hooks_path.mkdir(parents=True, exist_ok=True)
        self.loaded_hooks = []
        
    def initialize(self):
        """Initialize and load all hooks."""
        self.loaded_hooks = self._load_hooks()
        print(f"🪝 Loaded {len(self.loaded_hooks)} hooks")
        
    def apply_all(self):
        """Apply all available hooks."""
        for hook in self.loaded_hooks:
            self._apply_hook(hook)
    
    def _load_hooks(self) -> List[Any]:
        """Load all hooks from the hooks directory."""
        hooks = []
        
        for hook_file in self.hooks_path.glob('*.py'):
            hook = self._load_hook(hook_file)
            if hook:
                hooks.append(hook)
        
        return hooks
    
    def _load_hook(self, hook_file: Path):
        """Load a single hook from file."""
        try:
            spec = importlib.util.spec_from_file_location(
                hook_file.stem,
                hook_file
            )
            
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'apply'):
                    return module
            
            return None
        except Exception as e:
            print(f"⚠️  Failed to load hook {hook_file}: {e}")
            return None
    
    def _apply_hook(self, hook):
        """Apply a single hook."""
        try:
            hook.apply()
        except Exception as e:
            print(f"⚠️  Hook failed: {e}")
            # Trigger error hook
            self.trigger_error(e)
    
    def trigger_session_end(self, session: Any = None):
        """Trigger session end hooks for learning."""
        print("📚 Triggering session end learning...")
        
        for hook in self.loaded_hooks:
            try:
                if hasattr(hook, 'onSessionEnd'):
                    hook.onSessionEnd(session)
            except Exception as e:
                print(f"⚠️  Session end hook failed: {e}")
                self.trigger_error(e)
    
    def trigger_error(self, error: Exception):
        """Trigger error hooks for learning from mistakes."""
        print(f"❌ Error occurred: {error}")
        print(f"📝 Stack trace:\n{traceback.format_exc()}")
        
        for hook in self.loaded_hooks:
            try:
                if hasattr(hook, 'onError'):
                    hook.onError(error)
            except Exception as e:
                print(f"⚠️  Error hook failed: {e}")
    
    def trigger_recovery(self):
        """Trigger recovery hooks for learning from recovery."""
        print("✅ Recovering from error...")
        
        for hook in self.loaded_hooks:
            try:
                if hasattr(hook, 'onRecovery'):
                    hook.onRecovery()
            except Exception as e:
                print(f"⚠️  Recovery hook failed: {e}")


# Global hook manager instance
_hook_manager = None


def get_hook_manager(workspace: Path = None) -> HookManager:
    """Get or create the global hook manager."""
    global _hook_manager
    
    if _hook_manager is None:
        if workspace is None:
            workspace = Path(__file__).parent.parent
        _hook_manager = HookManager(workspace)
        _hook_manager.initialize()
    
    return _hook_manager


# Convenience functions for direct use
def on_session_end(session=None):
    """Convenience function to trigger session end."""
    get_hook_manager().trigger_session_end(session)


def on_error(error):
    """Convenience function to trigger error."""
    get_hook_manager().trigger_error(error)


def on_recovery():
    """Convenience function to trigger recovery."""
    get_hook_manager().trigger_recovery()
