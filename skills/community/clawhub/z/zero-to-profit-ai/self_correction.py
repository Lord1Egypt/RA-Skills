from logger import log_journal

def self_correct(task_results):
    lessons = []
    for result in task_results:
        if "Skipped" in result:
            lessons.append(f"Action skipped: optimize cost or increase expected gain")
        elif "Executed" in result:
            lessons.append(f"Action executed successfully")
    log_journal("Lessons Learned: " + "; ".join(lessons))
    return lessons
