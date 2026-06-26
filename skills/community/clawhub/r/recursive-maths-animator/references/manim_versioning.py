"""
Manim Project Versioning System
Git-based version control for Manim animation projects
"""

import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Literal


def _default_scene_class_name(scene_name: str) -> str:
    """Map a scene slug to a Manim class name (e.g. scene_1 -> Scene1, intro -> Intro)."""
    parts = scene_name.replace("-", "_").split("_")
    return "".join(p.capitalize() for p in parts if p)


# Written to new projects by init() when requirements.txt is missing.
# Keep in sync with ../requirements.txt in this skill package.
_REQUIREMENTS_BOILERPLATE = """# Pin in your project; bump after upgrades.
#   pip install -r requirements.txt
# Optional lockfile for CI: pip freeze > requirements.lock.txt

manim>=0.18.0
manim-voiceover[gtts]>=0.3.1

# Optional: Gemini TTS — uncomment if you use references/gemini_tts_service.py
# google-genai>=1.0.0
"""

# Stakeholder signs off on motion and palette using GIF previews before final MP4.
_DESIGN_THEME_BOILERPLATE = """# Design theme

Fill this **before** writing scene code. If the user has not specified a theme, **ask**
for these choices explicitly.

## Built-in design systems

Pick one of the skill's built-in schemes (or override piecemeal):

- **swiss** — Swiss International (Josef Müller-Brockmann). Inter font. Strict grid, clinical precision, black/white + restrained red.
- **bauhaus** — Bauhaus Modern (Herbert Bayer). Space Grotesk. Primary colors, geometric, functional art.
- **braun** — Braun Minimal (Dieter Rams). Work Sans. Warm light grays, systematic, "less but better."
- **editorial** — Editorial Bold (Paula Scher / Pentagram). Playfair Display + Inter. Dramatic scale contrast, deep navy + warm cream.
- **apple** — Apple Precision (Jony Ive). DM Sans. Cool neutrals, generous whitespace, sleek motion.
- **soft** — Soft Enterprise (skill default). Roboto. Warm cream backgrounds, dot grid patterns, gas-spring easing.

Fonts are downloaded on demand into `assets/fonts/` via `design_systems.font_catalog.install_fonts()`.

## Questions to ask

| Topic | Prompt |
|-------|--------|
| Mood | Overall feel (e.g. minimal clinical, playful, cinematic, brutalist). |
| Light / dark | Light mode, dark mode, or high-contrast either way. |
| Palette | Primary, accent, background hex codes (or reference brand guidelines). |
| Design system | Pick one: swiss / bauhaus / braun / editorial / apple / soft (default). |
| Typography | User may override; skill default is **Roboto** (see locked defaults below). |
| Motion | Snappy vs floaty; calm vs energetic; any easing preferences. |
| Brand assets | Paths under `assets/` (logo, watermark, icon set). |
| Deliverable | Aspect ratio (16:9, 9:16), target length, platform (web, social). |

## Locked decisions

- Design system:
- Mood:
- Palette:
- Typography:
- Motion:
- Notes:
"""

# Filled after the user approves the agent's short pitch; see SKILL.md "Brief-first workflow".
_ANIMATION_BRIEF_BOILERPLATE = """# Animation brief

**Status:** DRAFT — do not write scene code until the user approves this brief (or confirms choices in chat).

## One-liner (what the viewer should feel / learn)

(One or two plain sentences. Avoid jargon unless the audience expects it.)

## Beats (order and ~duration)

| # | Beat (what appears) | ~seconds | Notes |
|---|---------------------|----------|-------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## Look & feel (options — user picks)

**Design system (choose one):**

- **A — Swiss grid** (Inter, clinical, data-forward, strict hierarchy)
- **B — Bauhaus primary** (Space Grotesk, geometric, educational, primary colors)
- **C — Braun minimal** (Work Sans, warm gray, product, "less but better")
- **D — Editorial bold** (Playfair + Inter, dramatic, storytelling, magazine confidence)
- **E — Apple precision** (DM Sans, cool, tech, sleek motion)
- **F — Soft enterprise** (Roboto, warm cream, existing default — gas-spring easing)

**Aspect / platform:** (e.g. 16:9 web, 1:1 social, 9:16 short)

**Motion:** (calm / snappy / loop-heavy)

## Manim-native ideas (optional — use the engine, not generic slides)

Ideas to discuss: `MathTex` / `Tex`, `NumberPlane` / `NumberLine`, parametric curves, `Transform` / `ReplacementTransform`, `Indicate`, `Flash`, `ShowPassingFlash`, `LaggedStart`, updaters for continuous motion.

## Approved

- [ ] User approved brief and selected palette / format
- Date / notes:
"""


class ManimProject:
    """Git-versioned Manim animation project manager"""
    
    def __init__(self, name: str, base_path: Optional[str] = None):
        self.name = name
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.project_path = self.base_path / name
        self.scenes_path = self.project_path / "scenes"
        self.media_path = self.project_path / "media"
        self.config_path = self.project_path / "project.json"
        
    def init(self, scheme: Optional[str] = None, install_fonts: bool = False) -> None:
        """Initialize project with git repository and folder structure.

        Creates:
        - ``assets/{images,svgs,fonts}`` for static art (keep binaries out of ``scenes/``).
        - ``exports/approvals`` for low-res GIFs used to sign off motion before final MP4.
        - ``exports/verification`` for frame slices + manifests used in the agent vision loop.
        - ``requirements.txt`` (canonical Manim + voiceover pins) unless already present.
        - ``DESIGN_THEME.md`` template unless already present — agents must fill with user.
        - ``ANIMATION_BRIEF.md`` template unless already present — short pitch + options; code only after approval.

        Args:
            scheme: Optional built-in design system key (swiss, bauhaus, braun,
                editorial, apple, soft). If provided, records it in project config.
            install_fonts: If True and ``scheme`` is given, downloads the scheme's
                fonts into ``assets/fonts/`` using ``design_systems.font_catalog``.
        """
        # Create directories
        self.project_path.mkdir(parents=True, exist_ok=True)
        self.scenes_path.mkdir(exist_ok=True)
        self.media_path.mkdir(exist_ok=True)
        (self.scenes_path / "shared").mkdir(exist_ok=True)

        # Static assets stay here; scene code references them by relative path.
        assets_root = self.project_path / "assets"
        for sub in ("images", "svgs", "fonts"):
            (assets_root / sub).mkdir(parents=True, exist_ok=True)
        assets_readme = assets_root / "README.md"
        if not assets_readme.exists():
            assets_readme.write_text(
                "# Assets\n\n"
                "Place **binary and static** files here so `scenes/` stays code-only.\n\n"
                "- `images/` — PNG, JPG, WebP\n"
                "- `svgs/` — vector sources\n"
                "- `fonts/` — custom font files if not relying on system fonts\n\n"
                "From a scene file under `scenes/<name>/`, reference images as e.g. "
                "`../../assets/images/logo.png`.\n",
                encoding="utf-8",
            )

        # GIF previews for stakeholder approval (fast to share in chat / email).
        approvals = self.project_path / "exports" / "approvals"
        approvals.mkdir(parents=True, exist_ok=True)

        # Still frames + manifest.json from extract_verification_frames.py for multimodal review.
        verification = self.project_path / "exports" / "verification"
        verification.mkdir(parents=True, exist_ok=True)

        req_file = self.project_path / "requirements.txt"
        if not req_file.exists():
            bundled = Path(__file__).resolve().parent.parent / "requirements.txt"
            body = (
                bundled.read_text(encoding="utf-8")
                if bundled.exists()
                else _REQUIREMENTS_BOILERPLATE
            )
            req_file.write_text(body, encoding="utf-8")

        theme_file = self.project_path / "DESIGN_THEME.md"
        if not theme_file.exists():
            theme_file.write_text(_DESIGN_THEME_BOILERPLATE, encoding="utf-8")

        brief_file = self.project_path / "ANIMATION_BRIEF.md"
        if not brief_file.exists():
            brief_file.write_text(_ANIMATION_BRIEF_BOILERPLATE, encoding="utf-8")

        # Optional: download fonts for the chosen design system
        if scheme and install_fonts:
            try:
                self.install_scheme_fonts(scheme)
            except Exception as exc:
                print(f"⚠ Font install for '{scheme}' failed: {exc}. "
                      "System fonts will be used as fallback.")
        
        # Initialize git repo
        if not (self.project_path / ".git").exists():
            self._git("init")
            self._git("config", "user.email", "manim@localhost")
            self._git("config", "user.name", "Manim Animation")
        
        # Create project config
        config = {
            "name": self.name,
            "created": datetime.now().isoformat(),
            "scenes": {},
            "version": "1.0",
            "scheme": scheme,
        }
        self._save_config(config)
        
        # Initial commit
        self._git("add", ".")
        self._git("commit", "-m", "Initial project setup", "--allow-empty")
        
        print(f"✓ Project '{self.name}' initialized at {self.project_path}")

    def install_scheme_fonts(self, scheme: str) -> None:
        """
        Download and install fonts for a built-in design system into
        ``assets/fonts/``.

        Args:
            scheme: One of "swiss", "bauhaus", "braun", "editorial", "apple".

        Raises:
            RuntimeError: If ``curl`` or font extraction fails.
        """
        import sys

        # Ensure the skill's references/ folder is on sys.path so design_systems resolves
        skill_ref = Path(__file__).resolve().parent
        if str(skill_ref) not in sys.path:
            sys.path.insert(0, str(skill_ref))

        from design_systems.font_catalog import (  # type: ignore
            install_fonts as _install_fonts,
            write_attribution_file,
        )

        target = self.project_path / "assets" / "fonts"
        installed = _install_fonts(scheme, target_dir=target)
        write_attribution_file(scheme, target_dir=target)
        print(f"✓ Installed {len(installed)} font files for '{scheme}' into {target}")
    
    def create_scene(self, scene_name: str, code: str, 
                     description: str = "") -> None:
        """Create a new scene with initial code"""
        scene_path = self.scenes_path / scene_name
        scene_path.mkdir(exist_ok=True)
        (scene_path / "versions").mkdir(exist_ok=True)
        (scene_path / "branches").mkdir(exist_ok=True)
        
        # Write initial scene file
        scene_file = scene_path / f"{scene_name}.py"
        scene_file.write_text(code)
        
        # Update config
        config = self._load_config()
        config["scenes"][scene_name] = {
            "created": datetime.now().isoformat(),
            "current_version": 1,
            "description": description,
            "branches": []
        }
        self._save_config(config)
        
        # Commit
        self._git("add", ".")
        self._git("commit", "-m", f"{scene_name} v1: initial creation")
        
        # Save immutable v1 copy
        shutil.copy(scene_file, scene_path / "versions" / "v1.py")
        
        print(f"✓ Scene '{scene_name}' created (v1)")
    
    def update_scene(self, scene_name: str, code: str, 
                     branch: Optional[str] = None) -> None:
        """Update scene code (creates new version on main or specified branch)"""
        scene_path = self._get_scene_path(scene_name, branch)
        scene_file = scene_path / f"{scene_name}.py"
        
        # Write updated code
        scene_file.write_text(code)
        
        # If on branch, just save - no version increment
        if branch:
            print(f"✓ Scene '{scene_name}' updated on branch '{branch}'")
            return
        
        # On main: increment version
        config = self._load_config()
        current = config["scenes"][scene_name]["current_version"]
        new_version = current + 1
        config["scenes"][scene_name]["current_version"] = new_version
        config["scenes"][scene_name]["updated"] = datetime.now().isoformat()
        self._save_config(config)
        
        # Commit
        self._git("add", ".")
        self._git("commit", "-m", f"{scene_name} v{new_version}: update")
        
        # Save immutable copy
        shutil.copy(scene_file, self.scenes_path / scene_name / "versions" / f"v{new_version}.py")
        
        print(f"✓ Scene '{scene_name}' updated (v{new_version})")
    
    def render(
        self,
        scene_name: str,
        branch: Optional[str] = None,
        quality: str = "medium",
        auto_commit: bool = True,
        scene_class: Optional[str] = None,
        output_format: Literal["movie", "gif"] = "movie",
        export_approval_copy: bool = False,
    ) -> str:
        """Render scene and optionally commit.

        scene_class: Manim scene class name inside the file. If omitted, derived from
        scene_name (scene_1 -> Scene1). Override when your class name does not match.

        output_format: ``movie`` (MP4) or ``gif`` for lightweight previews. The value
        ``movie`` is kept for backward compatibility; the Manim CLI is invoked with
        ``--format mp4`` (Manim Community does not accept ``movie`` as a format flag).

        export_approval_copy: If True, copy the output into ``exports/approvals/`` with
        a clear filename for stakeholder sign-off (typical with ``output_format='gif'``).
        """
        scene_path = self._get_scene_path(scene_name, branch)
        scene_file = scene_path / f"{scene_name}.py"
        
        if not scene_file.exists():
            raise FileNotFoundError(f"Scene file not found: {scene_file}")
        
        # Determine quality flags
        quality_flag = {"low": "-ql", "medium": "-qm", "high": "-qh"}.get(quality, "-qm")
        
        cls = scene_class or _default_scene_class_name(scene_name)
        # Manim CLI expects mp4/gif/webm/mov, not "movie".
        cli_format = "mp4" if output_format == "movie" else output_format
        cmd = [
            "manim",
            quality_flag,
            str(scene_file),
            cls,
            "--format",
            cli_format,
            "--disable_caching",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_path)
        
        if result.returncode != 0:
            print(f"Render error: {result.stderr}")
            raise RuntimeError(f"Render failed for {scene_name}")
        
        # Find output file (MP4 for movie, GIF for gif)
        output_dir = self.project_path / "media" / "videos" / scene_name
        if quality == "high":
            output_dir = output_dir / "1080p60"
        elif quality == "medium":
            output_dir = output_dir / "720p30"
        else:
            output_dir = output_dir / "480p15"
        
        suffix = ".gif" if output_format == "gif" else ".mp4"
        candidates = sorted(
            output_dir.glob(f"*{suffix}"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            raise FileNotFoundError(f"No output {suffix} found under {output_dir}")
        
        source_media = candidates[0]
        
        # Copy to media with version tag
        config = self._load_config()
        version = config["scenes"][scene_name]["current_version"]
        branch_tag = f"_{branch}" if branch else ""
        dest_name = f"{scene_name}{branch_tag}_v{version}{suffix}"
        dest_path = self.media_path / dest_name
        
        shutil.copy(source_media, dest_path)
        
        # Symlink to latest (same extension as this render)
        latest_link = self.media_path / f"{scene_name}{branch_tag}_latest{suffix}"
        if latest_link.exists() or latest_link.is_symlink():
            latest_link.unlink()
        try:
            latest_link.symlink_to(dest_path)
        except OSError:
            # Windows or filesystems without symlink support — duplicate file instead.
            shutil.copy2(dest_path, latest_link)

        if export_approval_copy:
            approval_dir = self.project_path / "exports" / "approvals"
            approval_dir.mkdir(parents=True, exist_ok=True)
            approval_name = f"{scene_name}{branch_tag}_v{version}_approval{suffix}"
            shutil.copy(dest_path, approval_dir / approval_name)
            print(f"✓ Approval copy: {approval_dir / approval_name}")
        
        # Auto-commit if on main
        if auto_commit and not branch:
            self._git("add", ".")
            label = "gif preview" if output_format == "gif" else "render"
            self._git("commit", "-m", f"{scene_name} v{version}: {label}", "--allow-empty")
        
        print(f"✓ Rendered: {dest_path}")
        return str(dest_path)

    def render_approval_gif(
        self,
        scene_name: str,
        branch: Optional[str] = None,
        scene_class: Optional[str] = None,
    ) -> str:
        """Low-quality GIF in ``exports/approvals/`` for stakeholder sign-off.

        Does not auto-commit (keeps git history focused on approved MP4 passes).
        After approval, render with ``output_format='movie'`` (MP4 via ``--format mp4``)
        and higher quality.
        """
        return self.render(
            scene_name,
            branch=branch,
            quality="low",
            auto_commit=False,
            scene_class=scene_class,
            output_format="gif",
            export_approval_copy=True,
        )
    
    def versions(self, scene_name: str) -> List[Dict]:
        """List all versions of a scene"""
        scene_path = self.scenes_path / scene_name
        versions_dir = scene_path / "versions"
        
        if not versions_dir.exists():
            return []
        
        versions = []
        for vfile in sorted(versions_dir.glob("v*.py")):
            version_num = int(vfile.stem[1:])  # v1.py -> 1
            stat = vfile.stat()
            versions.append({
                "version": version_num,
                "file": str(vfile),
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        
        return versions
    
    def rollback(self, scene_name: str, version: int) -> None:
        """Restore scene to specific version"""
        scene_path = self.scenes_path / scene_name
        version_file = scene_path / "versions" / f"v{version}.py"
        scene_file = scene_path / f"{scene_name}.py"
        
        if not version_file.exists():
            raise FileNotFoundError(f"Version {version} not found")
        
        # Restore code
        shutil.copy(version_file, scene_file)
        
        # Update config
        config = self._load_config()
        config["scenes"][scene_name]["current_version"] = version
        config["scenes"][scene_name]["rolled_back"] = datetime.now().isoformat()
        self._save_config(config)
        
        # Commit rollback
        self._git("add", ".")
        self._git("commit", "-m", f"{scene_name}: rollback to v{version}")
        
        print(f"✓ Rolled back '{scene_name}' to v{version}")
    
    def branch(self, scene_name: str, branch_name: str) -> None:
        """Create a provisional branch for a scene"""
        scene_path = self.scenes_path / scene_name
        branches_dir = scene_path / "branches" / branch_name
        branches_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy current scene to branch
        scene_file = scene_path / f"{scene_name}.py"
        branch_file = branches_dir / f"{scene_name}.py"
        shutil.copy(scene_file, branch_file)
        
        # Update config
        config = self._load_config()
        if branch_name not in config["scenes"][scene_name]["branches"]:
            config["scenes"][scene_name]["branches"].append(branch_name)
        self._save_config(config)
        
        print(f"✓ Branch '{branch_name}' created for '{scene_name}'")
    
    def merge(self, scene_name: str, branch_name: str) -> None:
        """Merge branch into main, creating new version"""
        scene_path = self.scenes_path / scene_name
        branch_file = scene_path / "branches" / branch_name / f"{scene_name}.py"
        scene_file = scene_path / f"{scene_name}.py"
        
        if not branch_file.exists():
            raise FileNotFoundError(f"Branch '{branch_name}' not found")
        
        # Copy branch code to main
        shutil.copy(branch_file, scene_file)
        
        # Increment version
        config = self._load_config()
        current = config["scenes"][scene_name]["current_version"]
        new_version = current + 1
        config["scenes"][scene_name]["current_version"] = new_version
        config["scenes"][scene_name]["merged_from"] = branch_name
        self._save_config(config)
        
        # Commit
        self._git("add", ".")
        self._git("commit", "-m", f"{scene_name} v{new_version}: merged from {branch_name}")
        
        # Save version copy
        shutil.copy(scene_file, scene_path / "versions" / f"v{new_version}.py")
        
        print(f"✓ Merged '{branch_name}' into '{scene_name}' (v{new_version})")
    
    def delete_branch(self, scene_name: str, branch_name: str) -> None:
        """Delete a provisional branch"""
        branch_path = self.scenes_path / scene_name / "branches" / branch_name
        
        if branch_path.exists():
            shutil.rmtree(branch_path)
        
        # Update config
        config = self._load_config()
        if branch_name in config["scenes"][scene_name]["branches"]:
            config["scenes"][scene_name]["branches"].remove(branch_name)
        self._save_config(config)
        
        print(f"✓ Branch '{branch_name}' deleted")
    
    def tag(self, scene_name: str, version: int, tag: str) -> None:
        """Tag a specific version (e.g., 'approved', 'final')"""
        config = self._load_config()
        
        if "tags" not in config["scenes"][scene_name]:
            config["scenes"][scene_name]["tags"] = {}
        
        config["scenes"][scene_name]["tags"][tag] = version
        self._save_config(config)
        
        # Git tag
        tag_name = f"{scene_name}-v{version}-{tag}"
        self._git("tag", "-f", tag_name)
        
        print(f"✓ Tagged {scene_name} v{version} as '{tag}'")
    
    def diff(self, scene_name: str, v1: int, v2: int) -> str:
        """Show diff between two versions"""
        scene_path = self.scenes_path / scene_name
        file1 = scene_path / "versions" / f"v{v1}.py"
        file2 = scene_path / "versions" / f"v{v2}.py"
        
        result = subprocess.run(
            ["diff", "-u", str(file1), str(file2)],
            capture_output=True, text=True
        )
        
        return result.stdout if result.stdout else "No differences"
    
    def _get_scene_path(self, scene_name: str, branch: Optional[str] = None) -> Path:
        """Get path to scene (main or branch)"""
        if branch:
            return self.scenes_path / scene_name / "branches" / branch
        return self.scenes_path / scene_name
    
    def _load_config(self) -> Dict:
        """Load project configuration"""
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())
        return {"scenes": {}}
    
    def _save_config(self, config: Dict) -> None:
        """Save project configuration"""
        self.config_path.write_text(json.dumps(config, indent=2))
    
    def _git(self, *args) -> subprocess.CompletedProcess:
        """Run git command in project directory"""
        return subprocess.run(
            ["git"] + list(args),
            cwd=self.project_path,
            capture_output=True
        )


# Convenience functions for direct use
def init_project(name: str, path: Optional[str] = None) -> ManimProject:
    """Initialize a new Manim project with versioning"""
    project = ManimProject(name, path)
    project.init()
    return project


def quick_render(scene_file: str, scene_class: str, quality: str = "medium") -> str:
    """Quick render without versioning (for testing)"""
    quality_flag = {"low": "-ql", "medium": "-qm", "high": "-qh"}.get(quality, "-qm")
    
    cmd = ["manim", quality_flag, scene_file, scene_class, "--disable_caching"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Render failed: {result.stderr}")
    
    # Find output
    scene_name = Path(scene_file).stem
    output_dir = Path("media") / "videos" / scene_name
    
    if quality == "high":
        output_dir = output_dir / "1080p60"
    elif quality == "medium":
        output_dir = output_dir / "720p30"
    else:
        output_dir = output_dir / "480p15"
    
    mp4_files = list(output_dir.glob("*.mp4"))
    return str(mp4_files[0]) if mp4_files else ""
