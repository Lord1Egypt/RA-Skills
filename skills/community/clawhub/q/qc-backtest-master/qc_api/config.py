import os
import re


def _load_dotenv():
    """Load environment variables from a .env file in the project root (does not overwrite existing vars)."""
    # Search upward from the current file's directory for a .env file
    search_dir = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):  # Search up to 6 levels
        env_path = os.path.join(search_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
            return
        parent = os.path.dirname(search_dir)
        if parent == search_dir:
            break
        search_dir = parent


def get_credentials():
    """
    Read QuantConnect API credentials.
    Priority: environment variables > project .env file > ~/.lean/credentials file
    """
    # 0. Attempt to load from .env file
    _load_dotenv()

    # 1. Environment variables (including those loaded from .env)
    user_id = os.environ.get("QC_USER_ID")
    api_token = os.environ.get("QC_API_TOKEN")
    if user_id and api_token:
        return user_id, api_token

    # 2. Fallback to ~/.lean/credentials file
    lean_cred_path = os.path.expanduser("~/.lean/credentials")
    if os.path.exists(lean_cred_path):
        try:
            with open(lean_cred_path) as f:
                content = f.read()
            uid_match = re.search(r'user-id\s*=\s*(\S+)', content)
            token_match = re.search(r'api-token\s*=\s*(\S+)', content)
            if uid_match and token_match:
                return uid_match.group(1), token_match.group(1)
        except Exception:
            pass

    raise ValueError(
        "QuantConnect credentials not configured. Set environment variables:\n"
        "  export QC_USER_ID=your_user_id\n"
        "  export QC_API_TOKEN=your_api_token\n"
        "Or configure user-id and api-token in ~/.lean/credentials"
    )


def get_default_project_id():
    """
    Returns the default project ID from the QC_PROJECT_ID environment variable.
    Raises ValueError if not set.
    """
    project_id = os.environ.get("QC_PROJECT_ID")
    if not project_id:
        raise ValueError(
            "QC_PROJECT_ID not set. Please set it:\n"
            "  export QC_PROJECT_ID=your_project_id"
        )
    return int(project_id)
