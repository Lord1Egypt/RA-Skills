"""spec2code — Tools for agent-driven Backtrader strategy generation.

Provides:
  - models: Data structures (CodeModules, ValidationResult, BacktestMetrics, etc.)
  - validator: AST syntax check + structural validation
  - config: Shared configuration (reuses paper2spec .env)

The agent itself generates code, runs backtests, and analyzes results.
These modules provide only the tools the agent cannot do natively.
"""

__version__ = "0.1.0"
