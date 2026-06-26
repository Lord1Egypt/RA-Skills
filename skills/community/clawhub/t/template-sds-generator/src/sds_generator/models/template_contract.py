from __future__ import annotations

from pydantic import Field

from .common import SDSBaseModel


class TemplatePlaceholderGroup(SDSBaseModel):
    required: list[str] = Field(default_factory=list)
    optional: list[str] = Field(default_factory=list)


class TemplatePlaceholderContract(SDSBaseModel):
    body: TemplatePlaceholderGroup = Field(default_factory=TemplatePlaceholderGroup)
    header: TemplatePlaceholderGroup = Field(default_factory=TemplatePlaceholderGroup)
    footer: TemplatePlaceholderGroup = Field(default_factory=TemplatePlaceholderGroup)


class TemplateAnchorContract(SDSBaseModel):
    section_headings: list[str] = Field(default_factory=list)
    subsection_headings: list[str] = Field(default_factory=list)


class TemplatePreservationRules(SDSBaseModel):
    preserve_logo_media: bool = True
    preserve_separator_lines: bool = True
    preserve_header_footer_tables: bool = True
    preserve_page_number_fields: bool = True


class TemplateFormattingPolicy(SDSBaseModel):
    default_font_family: str | None = None
    default_font_size_pt: float | None = None
    default_text_color: str | None = None


class TemplateValidationPolicy(SDSBaseModel):
    unresolved_placeholder: str = "blocking"
    missing_anchor: str = "blocking"
    missing_header_footer_table: str = "blocking"
    missing_page_number_fields: str = "blocking"


class TemplateContract(SDSBaseModel):
    contract_version: int = 1
    placeholders: TemplatePlaceholderContract = Field(default_factory=TemplatePlaceholderContract)
    anchors: TemplateAnchorContract = Field(default_factory=TemplateAnchorContract)
    preservation: TemplatePreservationRules = Field(default_factory=TemplatePreservationRules)
    formatting: TemplateFormattingPolicy = Field(default_factory=TemplateFormattingPolicy)
    validation: TemplateValidationPolicy = Field(default_factory=TemplateValidationPolicy)


class TemplateValidationReport(SDSBaseModel):
    template_path: str
    contract_version: int
    placeholders_found: dict[str, list[str]] = Field(default_factory=dict)
    missing_placeholders: dict[str, list[str]] = Field(default_factory=dict)
    anchors_found: list[str] = Field(default_factory=list)
    missing_anchors: list[str] = Field(default_factory=list)
    header_table_count: int = 0
    footer_table_count: int = 0
    page_number_fields_present: bool = False


class TemplateFillRange(SDSBaseModel):
    anchor: str
    next_anchor: str | None = None
    insertion_mode: str
    removed_element_count: int = 0
    inserted_element_count: int = 0


class TemplateFillReport(SDSBaseModel):
    template_path: str
    contract_version: int
    placeholders_found: dict[str, list[str]] = Field(default_factory=dict)
    placeholders_replaced: dict[str, int] = Field(default_factory=dict)
    unresolved_placeholders: list[str] = Field(default_factory=list)
    anchors_found: list[str] = Field(default_factory=list)
    missing_anchors: list[str] = Field(default_factory=list)
    duplicate_anchors: dict[str, int] = Field(default_factory=dict)
    content_ranges_replaced: list[TemplateFillRange] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
