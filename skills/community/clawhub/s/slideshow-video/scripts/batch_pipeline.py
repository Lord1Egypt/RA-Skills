#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

RUN_PIPELINE = Path(__file__).resolve().parent / 'run_pipeline.py'


def run(cmd):
    return subprocess.run(cmd, check=False)


def main():
    parser = argparse.ArgumentParser(description='Run slideshow pipeline for multiple project JSON files in a directory.')
    parser.add_argument('projects_dir', help='Directory containing JSON project files')
    parser.add_argument('--pattern', default='*.json', help='Glob pattern for project files')
    parser.add_argument('--output-root', default='build', help='Root output directory')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite MP4 output if it exists')
    parser.add_argument('--continue-on-error', action='store_true', help='Continue remaining jobs when one fails')
    args = parser.parse_args()

    projects_dir = Path(args.projects_dir).expanduser().resolve()
    if not projects_dir.is_dir():
        raise SystemExit(f'Not a directory: {projects_dir}')

    project_files = sorted(projects_dir.glob(args.pattern))
    if not project_files:
        raise SystemExit(f'No files matched {args.pattern} under {projects_dir}')

    results = []
    for project_path in project_files:
        cmd = [
            'python3',
            str(RUN_PIPELINE),
            str(project_path),
            '--output-root',
            str(Path(args.output_root).expanduser()),
        ]
        if args.overwrite:
            cmd.append('--overwrite')

        proc = run(cmd)
        success = proc.returncode == 0
        results.append({'project': str(project_path), 'status': 'ok' if success else 'failed', 'code': proc.returncode})

        if not success and not args.continue_on_error:
            raise SystemExit(f'Pipeline failed for {project_path}, stopped. Use --continue-on-error to keep going.')

    summary = {
        'count': len(project_files),
        'results': results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if any(item['status'] == 'failed' for item in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
