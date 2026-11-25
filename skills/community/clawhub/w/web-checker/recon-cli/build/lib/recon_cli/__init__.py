"""recon_cli - a low-volume web configuration audit toolkit.

The package is intentionally small and dependency-free:

- :mod:`recon_cli.cli` parses arguments and orchestrates the run.
- :mod:`recon_cli.checks` contains one module per check.
- :mod:`recon_cli.http` wraps curl with urllib fallbacks.
- :mod:`recon_cli.finding` defines the finding/severity model.
- :mod:`recon_cli.report` renders terminal and Markdown output.

See ``README.md`` and the ``docs/`` directory for user and contributor
documentation.
"""
__version__ = "0.1.0"

__all__ = ["__version__"]
