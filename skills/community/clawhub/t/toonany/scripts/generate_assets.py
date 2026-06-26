#!/usr/bin/env python3
"""Generate asset reference images (characters, scenes, props).

Supports four-view character sheets and style reference anchoring.
"""

import argparse
import json
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from PIL import Image

from utils.api_client import ImageAPIClient
from utils.config_loader import ConfigLoader, ConfigError
from utils.logger import setup_logger


@dataclass
class AssetConfig:
    project_path: Path
    data_file: Path = field(init=False)
    images_dir: Path = field(init=False)
    style_reference: Optional[Path] = None
    skip_existing: bool = True
    force: bool = False

    def __post_init__(self):
        self.data_file = self.project_path / "assets" / "data.json"
        self.images_dir = self.project_path / "assets" / "images"


@dataclass
class GenerationResult:
    name: str
    asset_type: str
    success: bool
    file_path: Optional[Path] = None
    seed: Optional[int] = None
    error: Optional[str] = None


class AssetGenerator:
    """Generate asset images with consistency support."""

    def __init__(self, config: AssetConfig, api: ImageAPIClient, logger):
        self.config = config
        self.api = api
        self.logger = logger

    def load_data(self) -> dict:
        with open(self.config.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data: dict) -> None:
        with open(self.config.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def update_project_json(self, character_name: str, seed: int, file_path: str) -> None:
        """Update character info in project.json."""
        project_json = self.config.project_path / "project.json"
        with open(project_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        characters = data.get("characters", [])
        existing = next((c for c in characters if c["name"] == character_name), None)

        if existing:
            existing["seed"] = seed
            existing["filePath"] = file_path
        else:
            characters.append({
                "name": character_name,
                "seed": seed,
                "filePath": file_path,
            })

        data["characters"] = characters

        with open(project_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_style_reference(self) -> Optional[str]:
        """Load style reference image as base64."""
        if not self.config.style_reference or not self.config.style_reference.exists():
            # Try project.json styleReference
            try:
                with open(self.config.project_path / "project.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                ref_path = data.get("styleReference")
                if ref_path:
                    full_path = self.config.project_path / ref_path
                    if full_path.exists():
                        self.config.style_reference = full_path
            except Exception:
                pass

        if self.config.style_reference and self.config.style_reference.exists():
            return ImageAPIClient.load_image_as_base64(self.config.style_reference)
        return None

    def generate_character_four_view(self, character: dict, style_ref: Optional[str]) -> GenerationResult:
        """Generate a true four-view reference sheet for a character.

        Generates 4 individual images (same seed) and combines into a 2x2 grid.
        """
        name = character["name"]
        prompt_base = character.get("prompt", character.get("description", ""))
        seed = character.get("seed")

        if seed is None:
            seed = random.randint(1, 999999)
            self.logger.info(f"  为角色 {name} 生成新 seed: {seed}")

        char_dir = self.config.images_dir / "characters"
        char_dir.mkdir(parents=True, exist_ok=True)

        grid_path = char_dir / f"{name}_grid.jpg"

        if self.config.skip_existing and grid_path.exists() and not self.config.force:
            self.logger.info(f"  [SKIP] {name} 四视图已存在")
            # Update project.json with existing path
            self.update_project_json(name, seed, f"images/characters/{name}_grid.jpg")
            return GenerationResult(name=name, asset_type="character", success=True,
                                    file_path=grid_path, seed=seed)

        # Four view prompts
        view_prompts = [
            f"{prompt_base}, head close-up portrait, top of head to collarbone, clear facial features, completely neutral expression, pure white background, no text, no props",
            f"{prompt_base}, front full body view, 100% complete from head to toe, arms naturally at sides, neutral expression, pure white background, no text, no props",
            f"{prompt_base}, side full body view, exact 90 degree left profile, 100% complete from head to toe, arms at sides, neutral expression, pure white background, no text, no props",
            f"{prompt_base}, back full body view, exact 180 degree rear view, 100% complete from head to heels, arms at sides, neutral expression, pure white background, no text, no props",
        ]

        images = []
        self.logger.info(f"  生成角色 {name} 的四视图 (seed={seed})...")

        try:
            for i, view_prompt in enumerate(view_prompts, 1):
                self.logger.info(f"    视图 {i}/4...")
                refs = [style_ref] if style_ref else None
                img_bytes = self.api.generate(
                    prompt=view_prompt,
                    size="1024x1024",
                    reference_images=refs,
                    seed=seed,
                )
                img = Image.open(__import__("io").BytesIO(img_bytes))
                images.append(img)

            # Create 2x2 grid
            grid = self.create_2x2_grid(images)
            grid.save(grid_path, "JPEG", quality=95)

            # Also save individual views
            for i, img in enumerate(images):
                img.save(char_dir / f"{name}_view{i+1}.jpg", "JPEG", quality=95)

            self.logger.info(f"  [OK] {name} 四视图已保存")

            # Update project.json
            self.update_project_json(name, seed, f"images/characters/{name}_grid.jpg")

            return GenerationResult(name=name, asset_type="character", success=True,
                                    file_path=grid_path, seed=seed)

        except Exception as e:
            self.logger.error(f"  [FAIL] {name}: {e}")
            return GenerationResult(name=name, asset_type="character", success=False,
                                    seed=seed, error=str(e))

    @staticmethod
    def create_2x2_grid(images: list[Image.Image]) -> Image.Image:
        """Create a 2x2 grid from 4 images."""
        if len(images) != 4:
            raise ValueError(f"Expected 4 images, got {len(images)}")

        img_width, img_height = images[0].size
        grid_width = img_width * 2
        grid_height = img_height * 2

        grid = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

        positions = [
            (0, 0),               # top-left: head close-up
            (img_width, 0),       # top-right: front full
            (0, img_height),      # bottom-left: side full
            (img_width, img_height),  # bottom-right: back full
        ]

        for img, (x, y) in zip(images, positions):
            grid.paste(img, (x, y))

        return grid

    def generate_single_image(self, item: dict, item_type: str, style_ref: Optional[str]) -> GenerationResult:
        """Generate a single image for scene or prop."""
        name = item["name"]
        prompt = item.get("prompt", item.get("description", ""))

        item_dir = self.config.images_dir / ("scenes" if item_type == "scene" else "props")
        item_dir.mkdir(parents=True, exist_ok=True)

        output_path = item_dir / f"{name}.jpg"

        if self.config.skip_existing and output_path.exists() and not self.config.force:
            self.logger.info(f"  [SKIP] {name} 图片已存在")
            return GenerationResult(name=name, asset_type=item_type, success=True,
                                    file_path=output_path)

        self.logger.info(f"  生成 {item_type} {name}...")

        try:
            refs = [style_ref] if style_ref else None
            img_bytes = self.api.generate(
                prompt=prompt,
                size="1024x1024",
                reference_images=refs,
            )

            img = Image.open(__import__("io").BytesIO(img_bytes))
            img.save(output_path, "JPEG", quality=95)

            self.logger.info(f"  [OK] {name}")
            return GenerationResult(name=name, asset_type=item_type, success=True,
                                    file_path=output_path)

        except Exception as e:
            self.logger.error(f"  [FAIL] {name}: {e}")
            return GenerationResult(name=name, asset_type=item_type, success=False,
                                    error=str(e))

    def run(self) -> list[GenerationResult]:
        """Process all assets."""
        results = []

        if not self.config.data_file.exists():
            self.logger.error(f"资产数据文件不存在: {self.config.data_file}")
            return results

        data = self.load_data()
        style_ref = self.get_style_reference()

        # Characters
        self.logger.info("\n" + "=" * 50)
        self.logger.info("生成角色四视图")
        self.logger.info("=" * 50)

        for character in data.get("characters", []):
            result = self.generate_character_four_view(character, style_ref)
            results.append(result)

        # Scenes
        self.logger.info("\n" + "=" * 50)
        self.logger.info("生成场景图")
        self.logger.info("=" * 50)

        for scene in data.get("scenes", []):
            result = self.generate_single_image(scene, "scene", style_ref)
            results.append(result)

        # Props
        self.logger.info("\n" + "=" * 50)
        self.logger.info("生成道具图")
        self.logger.info("=" * 50)

        for prop in data.get("props", []):
            result = self.generate_single_image(prop, "prop", style_ref)
            results.append(result)

        # Update data.json with file paths
        self.logger.info("\n更新 data.json...")
        for result in results:
            if result.success and result.file_path:
                # Find and update the item in data
                for item_list in [data.get("characters", []), data.get("scenes", []), data.get("props", [])]:
                    for item in item_list:
                        if item["name"] == result.name:
                            rel_path = result.file_path.relative_to(self.config.project_path / "assets")
                            item["filePath"] = str(rel_path)
                            if result.seed:
                                item["seed"] = result.seed

        self.save_data(data)
        self.logger.info("data.json 已更新")

        # Summary
        success_count = sum(1 for r in results if r.success)
        self.logger.info("\n" + "=" * 50)
        self.logger.info(f"生成完成: {success_count}/{len(results)} 成功")
        self.logger.info("=" * 50)

        return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate asset reference images")
    parser.add_argument("--project", "-p", type=str, default=".", help="Project directory")
    parser.add_argument("--style-reference", type=str, help="Path to style reference image")
    parser.add_argument("--force", action="store_true", help="Force regenerate existing images")
    parser.add_argument("--no-skip", action="store_true", help="Do not skip existing images")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    project_path = Path(args.project)
    logger = setup_logger("generate_assets", verbose=args.verbose)

    # Load config
    try:
        loader = ConfigLoader(project_path)
        config = loader.load()
    except ConfigError as e:
        logger.error(str(e))
        return 1

    # Check required model
    missing = loader.check_required_models("image")
    if missing:
        print(loader.format_missing_guide(missing))
        return 1

    if not config.image_model or not config.image_model.api_key:
        logger.error("图像生成 API Key 未配置")
        return 1

    # Setup
    asset_config = AssetConfig(
        project_path=project_path,
        style_reference=Path(args.style_reference) if args.style_reference else None,
        skip_existing=not args.no_skip,
        force=args.force,
    )

    api = ImageAPIClient(
        api_key=config.image_model.api_key,
        base_url=config.image_model.base_url or "https://ark.cn-beijing.volces.com/api/v3",
        model=config.image_model.model,
        logger=logger,
    )

    generator = AssetGenerator(asset_config, api, logger)
    results = generator.run()

    failed = [r for r in results if not r.success]
    if failed:
        logger.error(f"\n有 {len(failed)} 个资产生成失败")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
