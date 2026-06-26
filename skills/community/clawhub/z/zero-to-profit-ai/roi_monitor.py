def evaluate_roi(task):
    """
    Simple ROI calculation: expected_gain / cost
    """
    if task['cost'] <= 0:
        return float('inf')
    return task['expected_gain'] / task['cost']

def filter_high_roi_tasks(tasks, threshold=1.0):
    return [t for t in tasks if evaluate_roi(t) >= threshold]
