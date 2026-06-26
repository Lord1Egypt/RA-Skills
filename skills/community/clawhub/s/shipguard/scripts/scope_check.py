#!/usr/bin/env python3
"""
ShipGuard scope discovery helper.
Usage: python scope_check.py <identifier> <project_root>

Scans who imports a module/model, what has relationships to it,
and which frontend components reference it.
"""
import sys, subprocess, os

def grep(pattern, path, include="*.py", extra_flags=None):
    cmd = ["grep", "-rn", pattern, path, f"--include={include}"]
    if extra_flags:
        cmd.extend(extra_flags)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)

def main():
    if len(sys.argv) < 3:
        print("Usage: scope_check.py <identifier> <project_root>")
        print("Example: scope_check.py Account /path/to/project")
        sys.exit(1)

    identifier = sys.argv[1]
    root = sys.argv[2]
    backend = os.path.join(root, "backend")
    frontend = os.path.join(root, "frontend/src")

    print(f"\nShipGuard Scope Check: '{identifier}'")
    print(f"Project root: {root}")

    section("Backend: Who imports this module?")
    out = grep(f"from.*{identifier}.*import|import.*{identifier}", backend)
    print(out or "  (none)")

    section("Backend: ORM relationships referencing this model?")
    out = grep(f'relationship.*"{identifier}"', backend)
    print(out or "  (none)")

    section("Backend: DB table / class definition?")
    out = grep(f"class {identifier}|__tablename__", backend)
    print(out or "  (none)")

    section("Frontend: Components importing this?")
    out = grep(f"import.*{identifier}|<{identifier}", frontend, "*.vue")
    print(out or "  (none)")

    section("Frontend: API calls to related routes?")
    out = grep(f"api\\..*{identifier.lower()}", frontend, "*.vue")
    print(out or "  (none)")

    section("Celery: Tasks referencing this?")
    tasks_dir = os.path.join(backend, "tasks")
    if os.path.exists(tasks_dir):
        out = grep(identifier, tasks_dir)
        print(out or "  (none)")
    else:
        print("  (no tasks directory found)")

    print(f"\n{'='*50}")
    print("  Scope check complete")
    print('='*50)

if __name__ == "__main__":
    main()
