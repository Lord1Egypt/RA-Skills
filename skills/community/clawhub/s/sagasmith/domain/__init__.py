"""SagaSmith domain services — pure Python, no framework dependency.

Usage:
    from domain.db.database import Database
    from domain.db.cli import main as cli_main
    from domain.engine.dice.rolls import roll_d20
"""

__all__ = [
    "Database",
    "CampaignService",
    "CampaignSnapshotService",
    "RuleSearchService",
    "ModuleSearchService",
    "BgeM3Embedder",
]
