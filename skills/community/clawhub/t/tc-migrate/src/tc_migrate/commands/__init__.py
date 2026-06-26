from .config_cmds import register as register_config
from .scan_cmd import register as register_scan
from .plugins_cmd import register as register_plugins
from .generate_cmd import register as register_generate
from .tf_cmds import register as register_tf
from .run_cmd import register as register_run

__all__ = [
    "register_config",
    "register_scan",
    "register_plugins",
    "register_generate",
    "register_tf",
    "register_run",
]
