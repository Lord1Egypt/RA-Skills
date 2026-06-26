"""Git workflow helper utilities."""
import subprocess

def get_current_branch():
    """Get the current git branch name."""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def get_log(n=10):
    """Get last n commit messages."""
    result = subprocess.run(
        ["git", "log", f"--oneline", f"-{n}"],
        capture_output=True, text=True
    )
    return result.stdout

def create_branch(name):
    """Create and checkout a new branch."""
    subprocess.run(["git", "checkout", "-b", name])

def stage_and_commit(message):
    """Stage all changes and commit."""
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", message])
