#!/usr/bin/env python3
"""
Environment Checker for Skills-Coach v2.3.1

Checks for required dependencies before executing skills.
Supports auto-installation with user consent.
"""

import subprocess
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class EnvironmentChecker:
    """Checks environment dependencies for skill execution."""

    def __init__(self, skill_path: Path, auto_install: bool = False):
        self.skill_path = skill_path
        self.auto_install = auto_install
        self.required_commands = set()
        self.missing_commands = []
        self.required_python_packages = set()
        self.missing_python_packages = []

    def extract_required_commands(self) -> List[str]:
        """Extract required commands from SKILL.md."""
        skill_md = self.skill_path / "SKILL.md"

        if not skill_md.exists():
            return []

        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract commands from code blocks
        import re
        code_blocks = re.findall(r'```(?:bash|shell|sh)\n(.*?)```', content, re.DOTALL)

        for block in code_blocks:
            lines = block.strip().split('\n')
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Extract command name (first word)
                parts = line.split()
                if parts:
                    cmd = parts[0]
                    # Common command prefixes
                    if cmd in ['uv', 'python', 'python3', 'node', 'npm', 'yarn', 'go', 'cargo', 'java', 'ruby', 'php']:
                        self.required_commands.add(cmd)

        return list(self.required_commands)

    def extract_python_requirements(self) -> List[str]:
        """Extract Python packages from requirements.txt."""
        requirements_txt = self.skill_path / "requirements.txt"

        if not requirements_txt.exists():
            return []

        with open(requirements_txt, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Extract package name (before any version specifier)
                package = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0].strip()
                if package:
                    self.required_python_packages.add(package)

        return list(self.required_python_packages)

    def check_python_package_installed(self, package: str) -> bool:
        """Check if a Python package is installed."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'show', package],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False

    def install_python_package(self, package: str) -> bool:
        """
        Install a Python package using pip.

        Returns:
            True if installation succeeded, False otherwise
        """
        print(f"  Installing Python package: {package}...")

        # Try multiple installation strategies
        strategies = [
            # Strategy 1: Try --user flag (for externally-managed environments)
            ([sys.executable, '-m', 'pip', 'install', '--user', package], '--user'),
            # Strategy 2: Try --break-system-packages (for PEP 668 environments)
            ([sys.executable, '-m', 'pip', 'install', '--break-system-packages', package], '--break-system-packages'),
            # Strategy 3: Try without flags (for virtual environments)
            ([sys.executable, '-m', 'pip', 'install', package], 'default'),
        ]

        for cmd, strategy_name in strategies:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )

                if result.returncode == 0:
                    print(f"  ✓ Successfully installed {package} (using {strategy_name})")
                    return True

            except subprocess.TimeoutExpired:
                print(f"  ✗ Installation timed out for {package} (strategy: {strategy_name})")
                continue
            except Exception as e:
                print(f"  ✗ Installation error with {strategy_name}: {e}")
                continue

        # All strategies failed
        print(f"  ✗ Failed to install {package} with all strategies")
        if result:
            print(f"    Last error: {result.stderr[:200]}")
        return False

    def check_command_available(self, command: str) -> bool:
        """Check if a command is available in PATH."""
        return shutil.which(command) is not None

    def check_all_dependencies(self) -> Tuple[bool, List[str]]:
        """
        Check all required dependencies.

        Returns:
            (all_available, missing_items)
        """
        self.extract_required_commands()
        self.extract_python_requirements()

        for cmd in self.required_commands:
            if not self.check_command_available(cmd):
                self.missing_commands.append(cmd)

        for package in self.required_python_packages:
            if not self.check_python_package_installed(package):
                self.missing_python_packages.append(package)

        all_missing = self.missing_commands + self.missing_python_packages
        return len(all_missing) == 0, all_missing

    def get_installation_command(self, command: str) -> str:
        """Get installation command for missing dependency."""
        install_commands = {
            'uv': 'brew install uv',
            'python': 'brew install python',
            'python3': 'brew install python',
            'node': 'brew install node',
            'npm': 'brew install node',
            'yarn': 'npm install -g yarn',
            'go': 'brew install go',
            'cargo': 'curl --proto \'=https\' --tlsv1.2 -sSf https://sh.rustup.rs | sh',
            'java': 'brew install openjdk',
            'ruby': 'brew install ruby',
            'php': 'brew install php'
        }
        return install_commands.get(command, None)

    def get_installation_hints(self, command: str) -> str:
        """Get installation hints for missing commands."""
        hints = {
            'uv': 'Install with: brew install uv  OR  curl -LsSf https://astral.sh/uv/install.sh | sh',
            'python': 'Install with: brew install python',
            'python3': 'Install with: brew install python',
            'node': 'Install with: brew install node',
            'npm': 'Install with: brew install node',
            'yarn': 'Install with: npm install -g yarn',
            'go': 'Install with: brew install go',
            'cargo': 'Install with: curl --proto \'=https\' --tlsv1.2 -sSf https://sh.rustup.rs | sh',
            'java': 'Install with: brew install openjdk',
            'ruby': 'Install with: brew install ruby',
            'php': 'Install with: brew install php'
        }
        return hints.get(command, f'Please install {command}')

    def install_dependency(self, command: str) -> bool:
        """
        Attempt to install a missing dependency.

        Returns:
            True if installation succeeded, False otherwise
        """
        install_cmd = self.get_installation_command(command)

        if not install_cmd:
            print(f"  ✗ No automatic installation available for {command}")
            return False

        print(f"  Installing {command}...")
        print(f"  Command: {install_cmd}")

        try:
            result = subprocess.run(
                install_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                print(f"  ✓ Successfully installed {command}")
                return True
            else:
                print(f"  ✗ Failed to install {command}")
                print(f"    Error: {result.stderr[:200]}")
                return False

        except subprocess.TimeoutExpired:
            print(f"  ✗ Installation timed out for {command}")
            return False
        except Exception as e:
            print(f"  ✗ Installation error: {e}")
            return False

    def auto_install_missing(self) -> bool:
        """
        Automatically install missing dependencies.

        Returns:
            True if all dependencies were installed successfully
        """
        if not self.missing_commands and not self.missing_python_packages:
            return True

        print("\n" + "="*60)
        print("Auto-Installing Missing Dependencies")
        print("="*60)

        success_count = 0
        total_count = len(self.missing_commands) + len(self.missing_python_packages)

        # Install missing commands
        for cmd in self.missing_commands:
            if self.install_dependency(cmd):
                success_count += 1

        # Install missing Python packages
        for package in self.missing_python_packages:
            if self.install_python_package(package):
                success_count += 1

        print(f"\nInstalled {success_count}/{total_count} dependencies")

        # Re-check after installation
        _, still_missing = self.check_all_dependencies()

        return len(still_missing) == 0

    def print_report(self):
        """Print dependency check report."""
        print("\n" + "="*60)
        print("Environment Dependency Check")
        print("="*60)

        if not self.required_commands and not self.required_python_packages:
            print("✓ No specific dependencies detected")
            return

        if self.required_commands:
            print(f"\nRequired commands: {', '.join(sorted(self.required_commands))}")

        if self.required_python_packages:
            print(f"Required Python packages: {', '.join(sorted(self.required_python_packages))}")

        if not self.missing_commands and not self.missing_python_packages:
            print("\n✓ All required dependencies are available")
        else:
            if self.missing_commands:
                print(f"\n⚠ Missing commands: {', '.join(self.missing_commands)}")
                print("\nInstallation hints:")
                for cmd in self.missing_commands:
                    print(f"  • {cmd}: {self.get_installation_hints(cmd)}")

            if self.missing_python_packages:
                print(f"\n⚠ Missing Python packages: {', '.join(self.missing_python_packages)}")
                print("\nInstallation hint:")
                print(f"  • Run: pip install {' '.join(self.missing_python_packages)}")

            if self.auto_install:
                print("\n→ Auto-installation is enabled")
            else:
                print("\n⚠ WARNING: Execution may fail due to missing dependencies")
                print("   Use --auto-install flag to automatically install missing dependencies")


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python env_checker.py <skill-path>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])

    checker = EnvironmentChecker(skill_path)
    all_available, missing = checker.check_all_dependencies()
    checker.print_report()

    sys.exit(0 if all_available else 1)


if __name__ == "__main__":
    main()
