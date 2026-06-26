#!/usr/bin/env python3
"""
Qoder CLI Wrapper for OpenClaw Agent

This script provides a Python interface to call the Qoder programming tool
with various modes and parameters as described in the OpenClaw documentation.
"""

import subprocess
import sys
import json
import os
from typing import Dict, List, Optional

class QoderCLI:
    def __init__(self, qoder_path: str = "qoder"):
        """
        Initialize Qoder CLI wrapper
        
        Args:
            qoder_path: Path to qoder executable (default: "qoder" assumes it's in PATH)
        """
        self.qoder_path = qoder_path
        
    def _run_command(self, args: List[str], input_data: Optional[str] = None) -> Dict:
        """
        Run qoder command and return structured result
        
        Args:
            args: Command line arguments for qoder
            input_data: Optional input data to pipe to the command
            
        Returns:
            Dictionary with 'success', 'output', 'error' keys
        """
        try:
            cmd = [self.qoder_path] + args
            env = os.environ.copy()
            
            # Set environment variables for Qoder if needed
            if 'QODER_MODEL' not in env:
                env['QODER_MODEL'] = 'qwen3-max-2026-01-23'
                
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE if input_data else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            
            stdout, stderr = process.communicate(input=input_data)
            
            return {
                'success': process.returncode == 0,
                'output': stdout,
                'error': stderr,
                'returncode': process.returncode
            }
            
        except FileNotFoundError:
            return {
                'success': False,
                'output': '',
                'error': f'Qoder executable not found at {self.qoder_path}',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'returncode': -1
            }
    
    def generate_code(self, 
                     prompt: str, 
                     language: str = "python",
                     mode: str = "omni") -> Dict:
        """
        Generate code using Qoder
        
        Args:
            prompt: Natural language description of what code to generate
            language: Target programming language
            mode: Qoder mode ("omni", "super-power", "spec-driven")
            
        Returns:
            Dictionary with execution results
        """
        args = [
            "generate",
            "--prompt", prompt,
            "--language", language,
            "--mode", mode
        ]
        
        return self._run_command(args)
    
    def refactor_code(self, 
                     file_path: str,
                     instructions: str = "",
                     max_lines: int = 4000) -> Dict:
        """
        Refactor existing code file
        
        Args:
            file_path: Path to the code file to refactor
            instructions: Specific refactoring instructions
            max_lines: Maximum lines to process (avoid context issues with large files)
            
        Returns:
            Dictionary with execution results
        """
        if not os.path.exists(file_path):
            return {
                'success': False,
                'output': '',
                'error': f'File not found: {file_path}',
                'returncode': -1
            }
            
        # Check file size
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        if len(lines) > max_lines:
            return {
                'success': False,
                'output': '',
                'error': f'File too large ({len(lines)} lines). Split into smaller files first.',
                'returncode': -1
            }
            
        args = [
            "refactor",
            "--file", file_path
        ]
        
        if instructions:
            args.extend(["--instructions", instructions])
            
        return self._run_command(args)
    
    def spec_driven_development(self, 
                               spec_file: str,
                               output_dir: str = ".") -> Dict:
        """
        Generate code from specification file
        
        Args:
            spec_file: Path to SPEC file (Omni SPEC format)
            output_dir: Directory to output generated code
            
        Returns:
            Dictionary with execution results
        """
        if not os.path.exists(spec_file):
            return {
                'success': False,
                'output': '',
                'error': f'SPEC file not found: {spec_file}',
                'returncode': -1
            }
            
        args = [
            "spec",
            "--spec-file", spec_file,
            "--output-dir", output_dir
        ]
        
        return self._run_command(args)
    
    def analyze_codebase(self, 
                        directory: str,
                        analysis_type: str = "dependencies") -> Dict:
        """
        Analyze codebase for various purposes
        
        Args:
            directory: Root directory of codebase to analyze
            analysis_type: Type of analysis ("dependencies", "architecture", "quality")
            
        Returns:
            Dictionary with execution results
        """
        if not os.path.exists(directory):
            return {
                'success': False,
                'output': '',
                'error': f'Directory not found: {directory}',
                'returncode': -1
            }
            
        args = [
            "analyze",
            "--directory", directory,
            "--type", analysis_type
        ]
        
        return self._run_command(args)

def main():
    """Command line interface for testing"""
    if len(sys.argv) < 2:
        print("Usage: python qoder_cli.py <command> [args...]")
        print("Commands: generate, refactor, spec, analyze")
        return
        
    command = sys.argv[1]
    qoder = QoderCLI()
    
    if command == "generate":
        if len(sys.argv) < 3:
            print("Usage: generate <prompt> [--language <lang>] [--mode <mode>]")
            return
        prompt = sys.argv[2]
        result = qoder.generate_code(prompt)
        print(json.dumps(result, indent=2))
        
    elif command == "refactor":
        if len(sys.argv) < 3:
            print("Usage: refactor <file_path> [--instructions <instr>]")
            return
        file_path = sys.argv[2]
        instructions = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
        result = qoder.refactor_code(file_path, instructions)
        print(json.dumps(result, indent=2))
        
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()