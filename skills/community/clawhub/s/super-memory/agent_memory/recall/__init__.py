"""Recall engine package — re-exports from recall.py for backward compatibility.

The actual implementation remains in the parent-level recall.py
This package structure is prepared for future refactoring.
"""

import importlib.util
import os

# The recall/ package directory shadows the recall.py module.
# We load recall.py directly and re-export RecallEngine.
_recall_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "recall.py")
_spec = importlib.util.spec_from_file_location(
    "agent_memory._recall_impl",
    _recall_py_path,
    submodule_search_locations=[],
)
_recall_impl = importlib.util.module_from_spec(_spec)
_recall_impl.__package__ = "agent_memory"
_spec.loader.exec_module(_recall_impl)

RecallEngine = _recall_impl.RecallEngine

__all__ = ["RecallEngine"]
