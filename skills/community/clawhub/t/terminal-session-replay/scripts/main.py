#!/usr/bin/env python3
import argparse
import json
import os
import sys
import subprocess
import time
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

class TerminalSessionManager:
    def __init__(self, sessions_dir: Optional[str] = None):
        if sessions_dir:
            self.sessions_dir = Path(sessions_dir)
        else:
            self.sessions_dir = Path.home() / ".terminal-sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_session_name(self, session_name: str) -> bool:
        """Validate session name to prevent path traversal."""
        if not session_name:
            return False
        # Disallow path separators and parent directory references
        if '/' in session_name or '\\' in session_name:
            return False
        if session_name in ('.', '..'):
            return False
        # Disallow characters that might cause issues
        if any(c in session_name for c in '\0\r\n\t'):
            return False
        # Session name should be a valid filename (no special chars besides -_)
        # Allow alphanumeric, dash, underscore
        if not all(c.isalnum() or c in '-_.' for c in session_name):
            return False
        return True
    
    def get_session_paths(self, session_name: str) -> Dict[str, Path]:
        """Get all file paths for a session."""
        if not self.validate_session_name(session_name):
            raise ValueError(f"Invalid session name: {session_name}")
        base = self.sessions_dir / session_name
        return {
            'typescript': base.with_suffix('.typescript'),
            'timing': base.with_suffix('.timing'),
            'meta': base.with_suffix('.meta.json'),
            'base': base
        }
    
    def session_exists(self, session_name: str) -> bool:
        """Check if a session exists."""
        try:
            paths = self.get_session_paths(session_name)
            return paths['typescript'].exists()
        except ValueError:
            return False
    
    def list_sessions(self, filter_tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """List all recorded sessions."""
        sessions = []
        for file in self.sessions_dir.glob("*.typescript"):
            session_name = file.stem
            meta_path = file.with_suffix('.meta.json')
            meta = {}
            if meta_path.exists():
                try:
                    with open(meta_path) as f:
                        meta = json.load(f)
                except:
                    pass
            
            # Filter by tags if specified
            if filter_tags:
                session_tags = meta.get('tags', [])
                if not any(tag in session_tags for tag in filter_tags):
                    continue
            
            sessions.append({
                'name': session_name,
                'created': meta.get('created', 'Unknown'),
                'title': meta.get('title', ''),
                'description': meta.get('description', ''),
                'tags': meta.get('tags', []),
                'duration': self.get_session_duration(session_name)
            })
        
        return sorted(sessions, key=lambda x: x['created'], reverse=True)
    
    def get_session_duration(self, session_name: str) -> Optional[float]:
        """Get session duration in seconds from timing file."""
        try:
            paths = self.get_session_paths(session_name)
        except ValueError:
            return None
        
        if not paths['timing'].exists():
            return None
        
        try:
            with open(paths['timing']) as f:
                last_line = None
                for line in f:
                    last_line = line.strip()
                if last_line:
                    # Timing file format: timestamp data_length
                    parts = last_line.split()
                    if len(parts) >= 1:
                        return float(parts[0])
        except:
            pass
        return None
    
    def record(self, session_name: str, title: str = "", description: str = "", tags: List[str] = None) -> Dict[str, Any]:
        """Start recording a terminal session."""
        if not self.validate_session_name(session_name):
            return {"status": "error", "message": f"Invalid session name: {session_name}"}
        
        if self.session_exists(session_name):
            return {"status": "error", "message": f"Session '{session_name}' already exists"}
        
        paths = self.get_session_paths(session_name)
        
        # Build script command
        cmd = ['script', '--quiet', '--timing', str(paths['timing']), str(paths['typescript'])]
        
        print(f"Starting recording to session: {session_name}")
        print("Type 'exit' or press Ctrl+D to stop recording.")
        print(f"Files will be saved to: {paths['typescript']}")
        
        # Save metadata
        meta = {
            'created': datetime.now(timezone.utc).isoformat(),
            'title': title,
            'description': description,
            'tags': tags or [],
            'command': ' '.join(cmd)
        }
        
        with open(paths['meta'], 'w') as f:
            json.dump(meta, f, indent=2)
        
        # Execute script command
        try:
            result = subprocess.run(cmd)
            if result.returncode == 0:
                duration = self.get_session_duration(session_name)
                return {
                    "status": "success",
                    "message": f"Recording saved to {session_name}",
                    "duration": duration,
                    "files": {
                        "typescript": str(paths['typescript']),
                        "timing": str(paths['timing']),
                        "meta": str(paths['meta'])
                    }
                }
            else:
                return {"status": "error", "message": f"script command failed with code {result.returncode}"}
        except FileNotFoundError:
            return {"status": "error", "message": "'script' command not found. Install it via your package manager."}
        except Exception as e:
            return {"status": "error", "message": f"Error during recording: {str(e)}"}
    
    def replay(self, session_name: str, speed: float = 1.0, no_timing: bool = False) -> Dict[str, Any]:
        """Replay a recorded session."""
        if not self.validate_session_name(session_name):
            return {"status": "error", "message": f"Invalid session name: {session_name}"}
        
        if not self.session_exists(session_name):
            return {"status": "error", "message": f"Session '{session_name}' not found"}
        
        paths = self.get_session_paths(session_name)
        
        if not paths['timing'].exists():
            return {"status": "error", "message": "Timing file not found, cannot replay"}
        
        # Build scriptreplay command
        if no_timing:
            # Just cat the typescript file
            cmd = ['cat', str(paths['typescript'])]
        else:
            cmd = ['scriptreplay', '--timing', str(paths['timing']), str(paths['typescript'])]
            if speed != 1.0:
                cmd.extend(['--divisor', str(speed)])
        
        try:
            result = subprocess.run(cmd)
            if result.returncode == 0:
                return {"status": "success", "message": f"Replayed session: {session_name}"}
            else:
                return {"status": "error", "message": f"scriptreplay failed with code {result.returncode}"}
        except FileNotFoundError:
            return {"status": "error", "message": "'scriptreplay' command not found. Install it via your package manager."}
        except Exception as e:
            return {"status": "error", "message": f"Error during replay: {str(e)}"}
    
    def export_to_markdown(self, session_name: str, output_file: str, include_timing: bool = False) -> Dict[str, Any]:
        """Export a session to markdown format."""
        if not self.validate_session_name(session_name):
            return {"status": "error", "message": f"Invalid session name: {session_name}"}
        
        if not self.session_exists(session_name):
            return {"status": "error", "message": f"Session '{session_name}' not found"}
        
        paths = self.get_session_paths(session_name)
        
        # Read metadata
        meta = {}
        if paths['meta'].exists():
            try:
                with open(paths['meta']) as f:
                    meta = json.load(f)
            except:
                pass
        
        # Read typescript file
        try:
            with open(paths['typescript']) as f:
                content = f.read()
        except Exception as e:
            return {"status": "error", "message": f"Error reading typescript file: {str(e)}"}
        
        # Parse content (remove script header/footer if present)
        lines = content.split('\n')
        # Script adds header like "Script started on ..." and footer "Script done on ..."
        # Try to detect and remove them
        filtered_lines = []
        for line in lines:
            if line.startswith('Script started on ') or line.startswith('Script done on '):
                continue
            filtered_lines.append(line)
        
        session_content = '\n'.join(filtered_lines).strip()
        
        # Get duration
        duration = self.get_session_duration(session_name)
        duration_str = f"{duration:.1f} seconds" if duration else "Unknown"
        
        # Generate markdown
        markdown = []
        markdown.append(f"# Terminal Session: {meta.get('title', session_name)}")
        markdown.append("")
        markdown.append(f"**Recorded:** {meta.get('created', 'Unknown')}  ")
        markdown.append(f"**Duration:** {duration_str}  ")
        
        if meta.get('description'):
            markdown.append(f"**Description:** {meta['description']}  ")
        
        if meta.get('tags'):
            markdown.append(f"**Tags:** {', '.join(meta['tags'])}  ")
        
        markdown.append("")
        markdown.append("## Session Recording")
        markdown.append("")
        markdown.append("```bash")
        markdown.append(session_content)
        markdown.append("```")
        
        if include_timing and duration:
            markdown.append("")
            markdown.append(f"*Replay with original timing: {duration_str}*")
        
        # Write output
        try:
            with open(output_file, 'w') as f:
                f.write('\n'.join(markdown))
            return {
                "status": "success",
                "message": f"Exported to {output_file}",
                "output_file": output_file,
                "lines": len(markdown)
            }
        except Exception as e:
            return {"status": "error", "message": f"Error writing markdown file: {str(e)}"}
    
    def delete(self, session_name: str) -> Dict[str, Any]:
        """Delete a session."""
        if not self.validate_session_name(session_name):
            return {"status": "error", "message": f"Invalid session name: {session_name}"}
        
        if not self.session_exists(session_name):
            return {"status": "error", "message": f"Session '{session_name}' not found"}
        
        paths = self.get_session_paths(session_name)
        
        try:
            for file_type, path in paths.items():
                if file_type != 'base' and path.exists():
                    path.unlink()
            return {"status": "success", "message": f"Deleted session: {session_name}"}
        except Exception as e:
            return {"status": "error", "message": f"Error deleting session: {str(e)}"}
    
    def info(self, session_name: str) -> Dict[str, Any]:
        """Get information about a session."""
        if not self.validate_session_name(session_name):
            return {"status": "error", "message": f"Invalid session name: {session_name}"}
        
        if not self.session_exists(session_name):
            return {"status": "error", "message": f"Session '{session_name}' not found"}
        
        paths = self.get_session_paths(session_name)
        
        # Read metadata
        meta = {}
        if paths['meta'].exists():
            try:
                with open(paths['meta']) as f:
                    meta = json.load(f)
            except:
                pass
        
        # Get file sizes
        file_sizes = {}
        for file_type, path in paths.items():
            if file_type != 'base' and path.exists():
                file_sizes[file_type] = path.stat().st_size
        
        duration = self.get_session_duration(session_name)
        
        return {
            "status": "success",
            "session": session_name,
            "metadata": meta,
            "duration_seconds": duration,
            "file_sizes": file_sizes,
            "files": {k: str(v) for k, v in paths.items() if k != 'base'}
        }

def run_record(args):
    """Handle record command."""
    manager = TerminalSessionManager()
    tags = args.tags.split(',') if args.tags else []
    result = manager.record(
        session_name=args.output,
        title=args.title or "",
        description=args.desc or "",
        tags=tags
    )
    return result

def run_replay(args):
    """Handle replay command."""
    manager = TerminalSessionManager()
    result = manager.replay(
        session_name=args.input,
        speed=args.speed,
        no_timing=args.no_timing
    )
    return result

def run_export(args):
    """Handle export command."""
    manager = TerminalSessionManager()
    output_file = args.output or f"{args.input}.md"
    result = manager.export_to_markdown(
        session_name=args.input,
        output_file=output_file,
        include_timing=args.include_timing
    )
    return result

def run_list(args):
    """Handle list command."""
    manager = TerminalSessionManager()
    filter_tags = args.filter_tags.split(',') if args.filter_tags else None
    sessions = manager.list_sessions(filter_tags=filter_tags)
    
    result = {
        "status": "success",
        "sessions": sessions,
        "count": len(sessions)
    }
    
    # Also print human-readable summary
    if sessions:
        print(f"Found {len(sessions)} session(s):")
        for session in sessions:
            print(f"  {session['name']}: {session['title']} ({session['created'][:10]})")
    else:
        print("No sessions found.")
    
    return result

def run_info(args):
    """Handle info command."""
    manager = TerminalSessionManager()
    result = manager.info(session_name=args.input)
    return result

def run_delete(args):
    """Handle delete command."""
    manager = TerminalSessionManager()
    result = manager.delete(session_name=args.input)
    return result

def main():
    parser = argparse.ArgumentParser(description='Terminal Session Replay')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Record command
    record_parser = subparsers.add_parser('record', help='Record a terminal session')
    record_parser.add_argument('--output', required=True, help='Session name')
    record_parser.add_argument('--title', help='Session title')
    record_parser.add_argument('--desc', help='Session description')
    record_parser.add_argument('--tags', help='Comma-separated tags')
    
    # Replay command
    replay_parser = subparsers.add_parser('replay', help='Replay a recorded session')
    replay_parser.add_argument('--input', required=True, help='Session name to replay')
    replay_parser.add_argument('--speed', type=float, default=1.0, help='Playback speed multiplier')
    replay_parser.add_argument('--no-timing', action='store_true', help='Skip timing, display immediately')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export session to markdown')
    export_parser.add_argument('--input', required=True, help='Session name to export')
    export_parser.add_argument('--output', help='Output markdown file (default: session_name.md)')
    export_parser.add_argument('--include-timing', action='store_true', help='Include timing information')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List recorded sessions')
    list_parser.add_argument('--filter-tags', help='Filter by tags (comma-separated)')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show session information')
    info_parser.add_argument('--input', required=True, help='Session name')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a session')
    delete_parser.add_argument('--input', required=True, help='Session name to delete')
    
    # Help command
    subparsers.add_parser('help', help='Show help')
    
    args = parser.parse_args()
    
    if args.command == 'record':
        result = run_record(args)
    elif args.command == 'replay':
        result = run_replay(args)
    elif args.command == 'export':
        result = run_export(args)
    elif args.command == 'list':
        result = run_list(args)
    elif args.command == 'info':
        result = run_info(args)
    elif args.command == 'delete':
        result = run_delete(args)
    elif args.command == 'help' or args.command is None:
        parser.print_help()
        return
    else:
        result = {"status": "error", "message": f"Unknown command: {args.command}"}
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()