"""
Example 2: Task routing and exception handling.
"""

from workflow_orchestration.src import WorkflowOrchestrator
from workflow_orchestration.src.models import TaskMetadata, ChangeType, SizeLevel, RiskLevel
from workflow_orchestration.src.exceptions import ExceptionType, SeverityLevel


def main():
    orchestrator = WorkflowOrchestrator()

    # Test task routing
    test_cases = [
        (ChangeType.BUGFIX, SizeLevel.S, RiskLevel.LOW, "Expected: hotfix"),
        (ChangeType.DOCS, SizeLevel.XS, RiskLevel.LOW, "Expected: lightweight"),
        (ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM, "Expected: standard"),
    ]

    print("=== Task Routing ===")
    for change_type, size, risk, expected in test_cases:
        metadata = TaskMetadata(
            change_type=change_type,
            change_size=size,
            risk_level=risk
        )
        routed_workflow = orchestrator.route_task(metadata)
        print(f"{change_type.value} ({size.value}, {risk.value}) → {routed_workflow} ({expected})")

    # Test exception handling
    print("\n=== Exception Handling ===")
    instance = orchestrator.start_workflow("standard", {
        "change_type": "feature",
        "artifacts": {"proposal.md": "test"}
    })

    # Minor exception
    result = orchestrator.handle_exception(
        instance.id,
        ExceptionType.TECHNICAL_DEBT,
        SeverityLevel.MINOR
    )
    print(f"Minor exception: {result.action_taken}, rollback: {result.rollback_triggered}")

    # Critical exception
    result = orchestrator.handle_exception(
        instance.id,
        ExceptionType.PRODUCTION_ISSUE,
        SeverityLevel.CRITICAL
    )
    print(f"Critical exception: {result.action_taken}, rollback: {result.rollback_triggered}")
    print(f"Instance status: {instance.status.value}")


if __name__ == "__main__":
    main()