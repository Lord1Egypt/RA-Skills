"""
Self-Improving Claw - Learning Memory Module
"""

from pathlib import Path
from typing import List, Dict, Any
import json
from datetime import datetime


class LearningMemory:
    """Memory system for storing and retrieving learnings."""
    
    def __init__(self, workspace: Path):
        self.workspace = Path(workspace)
        self.learnings_path = self.workspace / 'learnings'
        self.learnings_path.mkdir(parents=True, exist_ok=True)
        self.learnings = []  # Initialize learnings list
        
    def load(self):
        """Load all learnings from disk."""
        self.learnings = []
        
        # Load active learnings
        active_file = self.learnings_path / 'active_learnings.json'
        if active_file.exists():
            with open(active_file, 'r') as f:
                self.learnings = json.load(f)
        
        # Load archived learnings
        archive_file = self.learnings_path / 'archive.json'
        if archive_file.exists():
            with open(archive_file, 'r') as f:
                self.learnings.extend(json.load(f))
    
    def store(self, learnings: List[Dict[str, Any]]):
        """Store new learnings."""
        for learning in learnings:
            learning['id'] = self._generate_id()
            learning['date'] = datetime.now().isoformat()
            self.learnings.append(learning)
        
        self._save()
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all learnings."""
        return self.learnings
    
    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get learnings by category."""
        return [l for l in self.learnings if l.get('category') == category]
    
    def export(self, output_file: Path):
        """Export learnings to a file."""
        with open(output_file, 'w') as f:
            f.write("# Self-Improving Claw - Learnings Export\n\n")
            f.write(f"Exported: {datetime.now().isoformat()}\n\n")
            f.write(f"Total Learnings: {len(self.learnings)}\n\n")
            f.write("---\n\n")
            
            for i, learning in enumerate(self.learnings, 1):
                f.write(f"## {i}. {learning.get('title', 'Untitled')}\n\n")
                f.write(f"**Category:** {learning.get('category', 'General')}\n\n")
                f.write(f"**Date:** {learning.get('date', 'Unknown')}\n\n")
                f.write(f"**Content:**\n{learning.get('content', '')}\n\n")
                f.write("---\n\n")
    
    def _save(self):
        """Save learnings to disk."""
        active_file = self.learnings_path / 'active_learnings.json'
        with open(active_file, 'w') as f:
            json.dump(self.learnings, f, indent=2)
    
    def _generate_id(self) -> str:
        """Generate a unique ID for a learning."""
        import uuid
        return str(uuid.uuid4())[:8]
