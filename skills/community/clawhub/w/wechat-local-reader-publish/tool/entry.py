"""PyInstaller entry point — avoids relative import issues."""
from wechat_cli.main import cli

if __name__ == "__main__":
    cli()
