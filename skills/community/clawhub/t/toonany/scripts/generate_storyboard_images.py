#!/usr/bin/env python3
"""Generate storyboard images - one image per cell (shot).

Uses style reference and character reference images for consistency.
Each cell (镜头) generates ONE individual image, no grid splitting.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from utils.api_client import ImageAPIClient
from utils.config_loader import ConfigLoader, ConfigError
from utils.logger import setup_logger
from utils.prompt_optimizer import parse_video_ratio


@dataclass
class Shot:
    """A storyboard shot containing multiple cells."""
    number: int
    segment: int
    title: str
    cells: list[str]
    characters: list[str] = field(default_factory=list)
    scenes: list[str] = field(default_factory=list)
    props: list[str] = field(default_factory=list)


@dataclass
class Asset:
    """An asset from data.json."""
    name: str
    asset_type: str
    file_path: Path


@dataclass
class GenerationResult:
    shot_number: int
    success: bool
    cell_paths: list[Path] = field(default_factory=list)
    error: Optional[str] = None


class StoryboardParser:
    """Parse storyboard markdown files."""

    SEGMENT_PATTERN = re.compile(r'^## 片段(\d+)[:：]\s*(.*)$')
    SHOT_PATTERN = re.compile(r'^### 分镜(\d+)[:：]?\s*(.*)$')
    CELL_PATTERN = re.compile(r'^\s*[-*]\s+\*\*镜头(\d+)\*\*:\s*(.+)$')
    ASSET_PATTERN = re.compile(r'^\s*[-*]\s+\*\*资产\*\*:\s*(.+?)$')

    def __init__(self, logger):
        self.logger = logger

    def parse(self, storyboard_path: Path) -> list[Shot]:
        content = storyboard_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        shots = []
        current_shot = None
        current_cells = []
        current_segment = 1
        current_assets = {}

        for line in lines:
            segment_match = self.SEGMENT_PATTERN.match(line)
            if segment_match:
                if current_shot is not None and current_cells:
                    shots.append(self._build_shot(current_shot, current_cells, current_assets, current_segment))
                current_segment = int(segment_match.group(1))
                current_shot = None
                current_cells = []
                current_assets = {}
                continue

            shot_match = self.SHOT_PATTERN.match(line)
            if shot_match:
                if current_shot is not None and current_cells:
                    shots.append(self._build_shot(current_shot, current_cells, current_assets, current_segment))
                shot_num = int(shot_match.group(1))
                current_shot = shot_num
                current_cells = []
                current_assets = {}
                continue

            if current_shot is not None:
                cell_match = self.CELL_PATTERN.match(line)
                if cell_match:
                    cell_num = int(cell_match.group(1))
                    prompt = cell_match.group(2).strip()
                    while len(current_cells) < cell_num:
                        current_cells.append('')
                    current_cells[cell_num - 1] = prompt

                asset_match = self.ASSET_PATTERN.match(line)
                if asset_match:
                    asset_str = asset_match.group(1).strip()
                    parts = [p.strip() for p in asset_str.split(',') if p.strip()]
                    current_assets = {'characters': parts, 'scenes': [], 'props': []}

        if current_shot is not None and current_cells:
            shots.append(self._build_shot(current_shot, current_cells, current_assets, current_segment))

        self.logger.info(f"Parsed {len(shots)} shots, total cells: {sum(len(s.cells) for s in shots)}")
        return shots

    def _build_shot(self, shot_number: int, cells: list[str], assets: dict, segment: int) -> Shot:
        valid_cells = [c for c in cells if c.strip()]
        return Shot(
            number=shot_number,
            segment=segment,
            title=f'Shot {shot_number}',
            cells=valid_cells,
            characters=assets.get('characters', []),
            scenes=assets.get('scenes', []),
            props=assets.get('props', []),
        )


class AssetIndexLoader:
    """Load and index assets from data.json."""

    def __init__(self, assets_dir: Path, logger):
        self.assets_dir = assets_dir
        self.logger = logger

    def load(self, data_json_path: Path) -> dict[str, Asset]:
        data = json.loads(data_json_path.read_text(encoding='utf-8'))
        index = {}

        for asset_type in ['characters', 'scenes', 'props']:
            for item in data.get(asset_type, []):
                name = item['name']
                file_path = item.get('filePath', '')
                if file_path:
                    full_path = self.assets_dir / file_path
                    index[name] = Asset(name=name, asset_type=asset_type, file_path=full_path)

        self.logger.info(f"Loaded {len(index)} assets")
        return index

    def find_relevant(self, shot: Shot, index: dict[str, Asset], max_count: int = 10) -> list[Asset]:
        """Find assets relevant to a shot based on name matching."""
        relevant = []
        keywords = set(shot.characters + shot.scenes + shot.props)

        for name, asset in index.items():
            if any(kw in name or name in kw for kw in keywords):
                relevant.append(asset)
            if len(relevant) >= max_count:
                break

        return relevant


def calculate_cell_size(video_ratio: tuple[int, int]) -> str:
    """Calculate image size for a single cell matching video ratio.

    Volcengine minimum: 3,686,400 pixels.
    For 9:16 ratio: 1440 x 2560 = 3,686,400.
    For 16:9 ratio: 2560 x 1440 = 3,686,400.
    """
    w_ratio, h_ratio = video_ratio
    min_pixels = 3686400

    # Calculate dimensions that satisfy min pixels with correct ratio
    if w_ratio >= h_ratio:
        # Landscape or square
        height = int((min_pixels * h_ratio / w_ratio) ** 0.5)
        height = (height + 63) // 64 * 64  # Round to 64
        width = int(height * w_ratio / h_ratio)
        width = (width + 63) // 64 * 64
    else:
        # Portrait
        width = int((min_pixels * w_ratio / h_ratio) ** 0.5)
        width = (width + 63) // 64 * 64
        height = int(width * h_ratio / w_ratio)
        height = (height + 63) // 64 * 64

    return f"{width}x{height}"


class StoryboardImageGenerator:
    """Main generator for storyboard images - one image per cell."""

    def __init__(self, project_path: Path, api: ImageAPIClient, logger, video_ratio=(16, 9), art_style=""):
        self.project_path = Path(project_path)
        self.api = api
        self.logger = logger
        self.video_ratio = video_ratio
        self.art_style = art_style
        self.images_dir = self.project_path / "storyboard" / "images"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.cell_size = calculate_cell_size(video_ratio)

    def generate(self, storyboard_file: str, segment: Optional[int] = None) -> list[GenerationResult]:
        storyboard_path = self.project_path / "storyboard" / storyboard_file
        if not storyboard_path.exists():
            raise FileNotFoundError(f"Storyboard file not found: {storyboard_path}")

        parser = StoryboardParser(self.logger)
        shots = parser.parse(storyboard_path)

        if segment:
            shots = [s for s in shots if s.segment == segment]

        # Load asset index
        data_json = self.project_path / "assets" / "data.json"
        asset_index = {}
        if data_json.exists():
            loader = AssetIndexLoader(self.project_path / "assets", self.logger)
            asset_index = loader.load(data_json)

        # Load style reference
        style_ref = None
        style_ref_path = self.project_path / "assets" / "style-sample.jpg"
        if style_ref_path.exists():
            style_ref = ImageAPIClient.load_image_as_base64(style_ref_path)
            self.logger.info("Using style reference")

        results = []
        for shot in shots:
            result = self._generate_shot_cells(shot, asset_index, style_ref)
            results.append(result)

        return results

    def _generate_shot_cells(self, shot: Shot, asset_index: dict, style_ref: Optional[str]) -> GenerationResult:
        cell_count = len(shot.cells)
        if cell_count == 0:
            return GenerationResult(shot_number=shot.number, success=False, error="No cells")

        self.logger.info(f"Shot {shot.number}: {cell_count} cells, size={self.cell_size}")

        # Find relevant assets
        loader = AssetIndexLoader(self.project_path / "assets", self.logger)
        relevant = loader.find_relevant(shot, asset_index)

        reference_images = []
        if style_ref:
            reference_images.append(style_ref)

        for asset in relevant[:10]:
            try:
                if asset.file_path.exists():
                    b64 = ImageAPIClient.load_image_as_base64(asset.file_path)
                    reference_images.append(b64)
            except Exception as e:
                self.logger.warning(f"Failed to load asset {asset.name}: {e}")

        cell_paths = []
        for idx, cell_prompt in enumerate(shot.cells):
            cell_num = idx + 1
            try:
                self.logger.info(f"  Generating cell {cell_num}/{cell_count}...")
                img_bytes = self.api.generate(
                    prompt=cell_prompt,
                    size=self.cell_size,
                    reference_images=reference_images[:10] if reference_images else None,
                )

                cell_path = self.images_dir / f"片段{shot.segment}-分镜{shot.number}-镜头{cell_num}.jpg"
                cell_path.write_bytes(img_bytes)
                self.logger.info(f"  Saved: {cell_path.name}")
                cell_paths.append(cell_path)

            except Exception as e:
                self.logger.error(f"  Cell {cell_num} failed: {e}")

        success = len(cell_paths) == cell_count
        return GenerationResult(
            shot_number=shot.number,
            success=success,
            cell_paths=cell_paths,
            error=None if success else f"{cell_count - len(cell_paths)} cells failed",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate storyboard images (one per cell)")
    parser.add_argument("--project", "-p", type=str, required=True, help="Project directory")
    parser.add_argument("--storyboard", "-s", type=str, default="storyboard-01.md", help="Storyboard filename")
    parser.add_argument("--segment", type=int, default=None, help="Segment number to process")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    project_path = Path(args.project)
    logger = setup_logger("storyboard_generator", verbose=args.verbose)

    try:
        loader = ConfigLoader(project_path)
        config = loader.load()
    except ConfigError as e:
        logger.error(str(e))
        return 1

    missing = loader.check_required_models("image")
    if missing:
        print(loader.format_missing_guide(missing))
        return 1

    api = ImageAPIClient(
        api_key=config.image_model.api_key,
        base_url=config.image_model.base_url or "https://ark.cn-beijing.volces.com/api/v3",
        model=config.image_model.model,
        logger=logger,
    )

    ratio = parse_video_ratio(config.video_ratio)
    generator = StoryboardImageGenerator(project_path, api, logger, video_ratio=ratio, art_style=config.art_style)

    try:
        results = generator.generate(args.storyboard, segment=args.segment)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    total_cells = sum(len(r.cell_paths) for r in results)
    success_shots = sum(1 for r in results if r.success)
    logger.info(f"\nCompleted: {success_shots}/{len(results)} shots, {total_cells} images generated")

    return 0 if success_shots == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
