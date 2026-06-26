from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import Field, model_validator

from sds_generator.exceptions import InvalidInputBundleError

from .common import SDSBaseModel


class InputRole(str, Enum):
    TEMPLATE_DOCX = "template_docx"
    PROMPT_FILE = "prompt_file"
    SOURCE_SDS = "source_sds"


class RunInputAsset(SDSBaseModel):
    role: InputRole
    path: Path


class RunInputBundle(SDSBaseModel):
    template_docx: Path
    prompt_file: Path
    source_sds: list[Path] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_roles(self) -> "RunInputBundle":
        from sds_generator.config_loader import load_defaults

        parsing_defaults = load_defaults().get("parsing", {})
        min_sources = int(parsing_defaults.get("min_source_inputs", 1))
        max_sources = int(parsing_defaults.get("max_source_inputs", 3))
        template_extensions = {str(item).lower() for item in parsing_defaults.get("template_extensions", [".docx"])}
        prompt_extensions = {str(item).lower() for item in parsing_defaults.get("prompt_extensions", [".txt", ".md"])}
        source_extensions = {
            str(item).lower()
            for item in parsing_defaults.get("source_extensions", [".pdf", ".docx", ".txt"])
        }

        if not self.template_docx.exists():
            raise InvalidInputBundleError(f"Template file does not exist: {self.template_docx}")
        if self.template_docx.suffix.lower() not in template_extensions:
            allowed = ", ".join(sorted(template_extensions))
            raise InvalidInputBundleError(
                f"Template file must use one of {allowed}; got {self.template_docx.name}"
            )

        if not self.prompt_file.exists():
            raise InvalidInputBundleError(f"Prompt file does not exist: {self.prompt_file}")
        if self.prompt_file.suffix.lower() not in prompt_extensions:
            allowed = ", ".join(sorted(prompt_extensions))
            raise InvalidInputBundleError(
                f"Prompt file must use one of {allowed}; got {self.prompt_file.name}"
            )

        if not (min_sources <= len(self.source_sds) <= max_sources):
            raise InvalidInputBundleError(
                f"Expected {min_sources}-{max_sources} source SDS files, got {len(self.source_sds)}."
            )

        seen_paths: dict[Path, str] = {
            self.template_docx.resolve(strict=False): InputRole.TEMPLATE_DOCX.value,
            self.prompt_file.resolve(strict=False): InputRole.PROMPT_FILE.value,
        }
        for path in self.source_sds:
            if not path.exists():
                raise InvalidInputBundleError(f"Source SDS file does not exist: {path}")
            if path.suffix.lower() not in source_extensions:
                allowed = ", ".join(sorted(source_extensions))
                raise InvalidInputBundleError(
                    f"Source SDS files must use one of {allowed}; got {path.name}"
                )
            resolved = path.resolve(strict=False)
            if resolved in seen_paths:
                raise InvalidInputBundleError(
                    f"{path.name} is assigned to both {seen_paths[resolved]} and source_sds."
                )
            seen_paths[resolved] = InputRole.SOURCE_SDS.value
        return self

    @property
    def layout_assets(self) -> list[RunInputAsset]:
        return [RunInputAsset(role=InputRole.TEMPLATE_DOCX, path=self.template_docx)]

    @property
    def rules_assets(self) -> list[RunInputAsset]:
        return [RunInputAsset(role=InputRole.PROMPT_FILE, path=self.prompt_file)]

    @property
    def evidence_assets(self) -> list[RunInputAsset]:
        return [RunInputAsset(role=InputRole.SOURCE_SDS, path=path) for path in self.source_sds]

    @property
    def evidence_paths(self) -> list[Path]:
        return [asset.path for asset in self.evidence_assets]
