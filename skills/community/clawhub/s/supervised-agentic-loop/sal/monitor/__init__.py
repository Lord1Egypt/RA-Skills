"""sal.monitor — AI-powered misalignment detection subpackage.

This subpackage is dependency-free from sal core.
sal.evolve_loop imports sal.monitor, NEVER the reverse.
"""

from sal.monitor.behaviors import BlockDecision, Severity
from sal.monitor.monitor import AgentMonitor

__all__ = ["AgentMonitor", "BlockDecision", "Severity"]
