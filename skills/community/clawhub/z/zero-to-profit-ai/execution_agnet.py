from roi_monitor import evaluate_roi
from logger import log_journal

def execute_task(task):
    roi = evaluate_roi(task)
    if roi < 1:
        log_journal(f"Skipped {task['name']} due to low ROI ({roi})")
        return f"Skipped {task['name']}"
    # Simulate task execution
    log_journal(f"Executed {task['name']} with ROI {roi}")
    return f"Executed {task['name']}"

def batch_execute(tasks):
    results = [execute_task(task) for task in tasks]
    return results
