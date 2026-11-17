#!/usr/bin/env python3
"""
TencentCloud Oceanus CLI – main entry point.

Usage:
    python scripts/oceanus_ops.py <command> [args]

Registers subcommands from modules:
- job_development: Job development lifecycle for SQL & JAR (create/config/publish)
- resource_query: Region/workspace/cluster queries
- job_runtime: Job runtime operations (run/stop/savepoint)
- resource_management: Dependency resource management (upload/version/query)
- job_observability: Job events / logs / COS log files
- folder_management: Folder CRUD operations
- metadata_query: Catalog/database/table metadata browsing
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="oceanus_ops",
        description="TencentCloud Oceanus CLI – operate Oceanus workspace resources via TencentCloud API.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Register modules
    import job_development
    job_development.register(subparsers)

    import resource_query
    resource_query.register(subparsers)

    import job_runtime
    job_runtime.register(subparsers)

    import resource_management
    resource_management.register(subparsers)

    import job_observability
    job_observability.register(subparsers)

    import folder_management
    folder_management.register(subparsers)

    import metadata_query
    metadata_query.register(subparsers)

    # Future modules (uncomment as implemented):
    # import resource
    # resource.register(subparsers)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
