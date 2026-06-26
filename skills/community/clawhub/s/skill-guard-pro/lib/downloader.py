"""
ClawGuard Skill Downloader
Downloads skills from ClawHub registry for analysis.
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional

class SkillDownloader:
    """Download skills from ClawHub"""
    
    @staticmethod
    def download_skill(skill_name: str) -> Optional[Path]:
        """
        Download skill to temporary directory.
        
        Returns:
            Path to downloaded skill directory, or None if failed
        """
        
        # Check if clawhub CLI is available
        if not SkillDownloader._has_clawhub_cli():
            print("⚠️  clawhub CLI not found. Install with: npm install -g clawhub")
            return None
        
        # Create temp directory
        temp_dir = Path(tempfile.mkdtemp(prefix="clawguard_"))
        
        try:
            # Download using clawhub CLI
            result = subprocess.run(
                ["clawhub", "download", skill_name, "--no-install"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            if result.returncode != 0:
                print(f"❌ Failed to download skill: {skill_name}")
                print(result.stderr)
                shutil.rmtree(temp_dir)
                return None
            
            # Find downloaded skill directory
            skill_dirs = list(temp_dir.glob("*"))
            if not skill_dirs:
                print(f"❌ No skill directory found after download")
                shutil.rmtree(temp_dir)
                return None
            
            skill_path = skill_dirs[0]
            print(f"✅ Downloaded skill to: {skill_path}")
            return skill_path
        
        except subprocess.TimeoutExpired:
            print(f"❌ Download timeout for skill: {skill_name}")
            shutil.rmtree(temp_dir)
            return None
        
        except Exception as e:
            print(f"❌ Download error: {e}")
            shutil.rmtree(temp_dir)
            return None
    
    @staticmethod
    def _has_clawhub_cli() -> bool:
        """Check if clawhub CLI is installed"""
        try:
            result = subprocess.run(
                ["clawhub", "--version"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    @staticmethod
    def cleanup(skill_path: Path):
        """Clean up temporary download directory"""
        try:
            # Only clean up if it's in temp directory
            if str(skill_path).startswith(tempfile.gettempdir()):
                shutil.rmtree(skill_path.parent)
                print(f"🧹 Cleaned up: {skill_path.parent}")
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")
