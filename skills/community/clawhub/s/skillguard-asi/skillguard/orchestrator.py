"""
SkillGuard — Orchestrator: ZIP extraction, file parsing, pipeline execution
"""

import zipfile
import tempfile
import os
import shutil
from pathlib import Path
from typing import List, Dict
from skillguard.detectors.base import Finding, SkillContext, PipelineContext
from skillguard.pipeline import PipelineRunner
from skillguard.report import JSONReport, MarkdownReport


class SkillExtractor:
    """Extract and parse a Skill ZIP package."""

    @staticmethod
    def extract(zip_path: str) -> SkillContext:
        """Extract ZIP and parse all relevant files into a SkillContext."""
        ctx = SkillContext()
        ctx.package_path = zip_path

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    zf.extractall(tmpdir)
            except (zipfile.BadZipFile, FileNotFoundError) as e:
                ctx.skill_name = os.path.basename(zip_path)
                ctx.skill_description = f"ZIP提取失败: {e}"
                return ctx

            # Walk extracted directory
            for root, dirs, files in os.walk(tmpdir):
                for filename in files:
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_path, tmpdir)

                    try:
                        with open(full_path, 'rb') as f:
                            raw = f.read()
                        ctx.all_files[rel_path] = raw
                    except:
                        continue

                    # Parse text files
                    try:
                        text = raw.decode('utf-8')
                    except UnicodeDecodeError:
                        continue

                    if filename == "SKILL.md" or rel_path == "SKILL.md":
                        ctx.skill_md_content = text
                        ctx.skill_name = SkillExtractor._extract_frontmatter(text, "name") or os.path.basename(zip_path).replace('.zip','')
                        ctx.skill_version = SkillExtractor._extract_frontmatter(text, "version") or "?"
                        ctx.skill_description = SkillExtractor._extract_frontmatter(text, "description") or ""

                    elif filename == "requirements.txt":
                        ctx.requirements_content = text

                    elif filename.endswith('.py'):
                        ctx.python_files[rel_path] = text

            if not ctx.skill_name:
                ctx.skill_name = os.path.basename(zip_path).replace('.zip', '')

        return ctx

    @staticmethod
    def _extract_frontmatter(text: str, key: str) -> str:
        """Extract a YAML frontmatter value."""
        import re
        match = re.search(rf'^{key}\s*:\s*(.+)$', text, re.MULTILINE)
        return match.group(1).strip().strip('"').strip("'") if match else ""


class Orchestrator:
    """Main orchestrator: extract → scan → report."""

    def scan(self, skill_path: str, detector_names: List[str] = None, 
             format: str = "both") -> Dict[str, str]:
        """
        Run full security scan on a skill package.
        
        Returns: dict with 'json' and/or 'md' keys containing report strings.
        """
        # Extract
        extractor = SkillExtractor()
        skill_ctx = extractor.extract(skill_path)

        # Run pipeline
        piperunner = PipelineRunner()
        if detector_names:
            findings, pctx = piperunner.run_named(detector_names, skill_ctx)
        else:
            findings, pctx = piperunner.run(skill_ctx)

        # Generate reports
        result = {}
        if format in ("json", "both"):
            result["json"] = JSONReport().generate(findings, skill_ctx.skill_name, skill_ctx.skill_version)
        if format in ("md", "both"):
            result["md"] = MarkdownReport().generate(findings, skill_ctx.skill_name, skill_ctx.skill_version)

        return result
