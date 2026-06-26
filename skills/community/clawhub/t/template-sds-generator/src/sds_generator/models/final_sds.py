from __future__ import annotations

from datetime import UTC, datetime

from pydantic import Field

from .common import GenerationMode, ReviewNote, SDSBaseModel, SourceSummary
from .outputs import FieldSourceMapRow
from .sections import (
    Section10StabilityReactivity,
    Section11ToxicologicalInformation,
    Section12EcologicalInformation,
    Section13DisposalConsiderations,
    Section14TransportInformation,
    Section15RegulatoryInformation,
    Section16OtherInformation,
    Section1Identification,
    Section2HazardsIdentification,
    Section3Composition,
    Section4FirstAid,
    Section5FireFighting,
    Section6AccidentalRelease,
    Section7HandlingStorage,
    Section8ExposureControls,
    Section9PhysicalChemicalProperties,
)


class DocumentMeta(SDSBaseModel):
    run_metadata_version: int = 1
    generation_mode: GenerationMode = GenerationMode.DRAFT
    generation_timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    product_name_display: str | None = None
    product_name_canonical: str | None = None
    cas_number: str | None = None
    template_file: str | None = None
    prompt_file: str | None = None
    input_files: list[str] = Field(default_factory=list)
    source_summary: list[SourceSummary] = Field(default_factory=list)
    critical_conflicts_present: bool = False
    release_eligible: bool = False


class AuditTrail(SDSBaseModel):
    review_notes: list[ReviewNote] = Field(default_factory=list)
    field_source_map: list[FieldSourceMapRow] = Field(default_factory=list)


class FinalSDSDocument(SDSBaseModel):
    document_meta: DocumentMeta = Field(default_factory=DocumentMeta)
    section_1: Section1Identification = Field(default_factory=Section1Identification)
    section_2: Section2HazardsIdentification = Field(default_factory=Section2HazardsIdentification)
    section_3: Section3Composition = Field(default_factory=Section3Composition)
    section_4: Section4FirstAid = Field(default_factory=Section4FirstAid)
    section_5: Section5FireFighting = Field(default_factory=Section5FireFighting)
    section_6: Section6AccidentalRelease = Field(default_factory=Section6AccidentalRelease)
    section_7: Section7HandlingStorage = Field(default_factory=Section7HandlingStorage)
    section_8: Section8ExposureControls = Field(default_factory=Section8ExposureControls)
    section_9: Section9PhysicalChemicalProperties = Field(default_factory=Section9PhysicalChemicalProperties)
    section_10: Section10StabilityReactivity = Field(default_factory=Section10StabilityReactivity)
    section_11: Section11ToxicologicalInformation = Field(default_factory=Section11ToxicologicalInformation)
    section_12: Section12EcologicalInformation = Field(default_factory=Section12EcologicalInformation)
    section_13: Section13DisposalConsiderations = Field(default_factory=Section13DisposalConsiderations)
    section_14: Section14TransportInformation = Field(default_factory=Section14TransportInformation)
    section_15: Section15RegulatoryInformation = Field(default_factory=Section15RegulatoryInformation)
    section_16: Section16OtherInformation = Field(default_factory=Section16OtherInformation)
    audit: AuditTrail = Field(default_factory=AuditTrail)

    def ordered_sections(self) -> list[tuple[str, SDSBaseModel]]:
        return [
            ("section_1", self.section_1),
            ("section_2", self.section_2),
            ("section_3", self.section_3),
            ("section_4", self.section_4),
            ("section_5", self.section_5),
            ("section_6", self.section_6),
            ("section_7", self.section_7),
            ("section_8", self.section_8),
            ("section_9", self.section_9),
            ("section_10", self.section_10),
            ("section_11", self.section_11),
            ("section_12", self.section_12),
            ("section_13", self.section_13),
            ("section_14", self.section_14),
            ("section_15", self.section_15),
            ("section_16", self.section_16),
        ]
