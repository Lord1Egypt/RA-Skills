#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid Diagram Generator
Generate diagrams from Mermaid syntax and send to Feishu
"""

import os
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

# Configuration
MERMAID_OUTPUT_DIR = Path("C:/Users/Xiabi/.openclaw/workspace/mermaid-output")
MERMAID_OUTPUT_DIR.mkdir(exist_ok=True)

class MermaidGenerator:
    """Generate diagrams from Mermaid syntax"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or MERMAID_OUTPUT_DIR
    
    def generate(self, mermaid_code: str, filename: str = None, 
                 width: int = 800, height: int = 600, 
                 format: str = "png") -> Path:
        """
        Generate diagram from Mermaid code
        
        Args:
            mermaid_code: Mermaid syntax
            filename: Output filename (without extension)
            width: Image width in pixels
            height: Image height in pixels
            format: Output format (png/svg)
        
        Returns:
            Path to generated image
        """
        # Generate filename
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"diagram-{timestamp}"
        
        # Create temp file for Mermaid code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as f:
            f.write(mermaid_code)
            temp_mmd = f.name
        
        try:
            # Output path
            output_path = self.output_dir / f"{filename}.{format}"
            
            # Generate diagram using mermaid-cli
            cmd = [
                'mmdc',
                '-i', temp_mmd,
                '-o', str(output_path),
                '-w', str(width),
                '-H', str(height),
            ]
            
            print(f"[INFO] Generating diagram: {output_path.name}")
            print(f"[INFO] Command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"[ERROR] Mermaid generation failed: {result.stderr}")
                return None
            
            print(f"[OK] Diagram generated: {output_path}")
            print(f"[OK] Size: {output_path.stat().st_size / 1024:.1f} KB")
            
            return output_path
            
        except subprocess.TimeoutExpired:
            print("[ERROR] Mermaid generation timeout")
            return None
        except Exception as e:
            print(f"[ERROR] Mermaid generation failed: {e}")
            return None
        finally:
            # Cleanup temp file
            try:
                os.unlink(temp_mmd)
            except:
                pass
    
    def generate_flowchart(self, nodes: list, edges: list, 
                           title: str = None, **kwargs) -> Path:
        """
        Generate flowchart diagram
        
        Args:
            nodes: List of (id, label, shape) tuples
            edges: List of (from, to, label) tuples
            title: Diagram title
        
        Returns:
            Path to generated image
        """
        # Build Mermaid code
        code_lines = ["graph TD"]
        
        if title:
            code_lines.insert(0, f"%%{title}")
        
        # Add nodes
        for node_id, label, shape in nodes:
            if shape == "rect":
                code_lines.append(f"    {node_id}[{label}]")
            elif shape == "round":
                code_lines.append(f"    {node_id}({label})")
            elif shape == "diamond":
                code_lines.append(f"    {node_id}{{{label}}}")
            elif shape == "cylinder":
                code_lines.append(f"    {node_id}[({label})]")
            else:
                code_lines.append(f"    {node_id}[{label}]")
        
        # Add edges
        for from_node, to_node, label in edges:
            if label:
                code_lines.append(f"    {from_node} -->|{label}| {to_node}")
            else:
                code_lines.append(f"    {from_node} --> {to_node}")
        
        mermaid_code = "\n".join(code_lines)
        print(f"[INFO] Flowchart Mermaid code:\n{mermaid_code}")
        
        return self.generate(mermaid_code, **kwargs)


# Convenience functions
_generator = None

def get_generator() -> MermaidGenerator:
    """Get or create singleton generator"""
    global _generator
    if _generator is None:
        _generator = MermaidGenerator()
    return _generator


def generate_diagram(mermaid_code: str, **kwargs) -> Path:
    """Generate diagram from Mermaid code"""
    generator = get_generator()
    return generator.generate(mermaid_code, **kwargs)


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("Mermaid Diagram Generator Test")
    print("=" * 60)
    
    generator = MermaidGenerator()
    
    # Test 1: Simple flowchart
    print("\n[Test 1] Simple Flowchart")
    
    mermaid_code = """
graph TD
    A[用户提问] --> B[记忆检索]
    B --> C{有相关记忆？}
    C -->|是 | D[增强回复]
    C -->|否 | E[普通回复]
    D --> F[用户收到回复]
    E --> F
"""
    
    output = generator.generate(mermaid_code, filename="test-flowchart")
    if output:
        print(f"[OK] Generated: {output}")
    else:
        print("[FAIL] Generation failed")
    
    # Test 2: Architecture diagram
    print("\n[Test 2] Architecture Diagram")
    
    mermaid_code = """
graph LR
    subgraph User
        A[用户]
    end
    
    subgraph OpenClaw
        B[阿香]
        C[记忆检索钩子]
        D[LLM]
    end
    
    subgraph External
        E[阿里云 Embedding]
        F[Chroma 向量库]
    end
    
    A --> B
    B --> C
    C --> E
    C --> F
    B --> D
    D --> A
"""
    
    output = generator.generate(mermaid_code, filename="test-architecture", width=1000, height=700)
    if output:
        print(f"[OK] Generated: {output}")
    else:
        print("[FAIL] Generation failed")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
