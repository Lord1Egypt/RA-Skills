from __future__ import annotations

from pydantic import Field

from .common import SDSBaseModel, TransportMode


class ComponentEntry(SDSBaseModel):
    chemical_name: str | None = None
    common_name_and_synonyms: list[str] = Field(default_factory=list)
    cas_number: str | None = None
    ec_number: str | None = None
    index_number: str | None = None
    concentration: str | None = None
    concentration_unit: str | None = None
    notes: str | None = None


class TransportModeEntry(SDSBaseModel):
    mode: TransportMode
    un_number: str | None = None
    proper_shipping_name: str | None = None
    hazard_class: str | None = None
    packing_group: str | None = None
    environmental_hazard: str | None = None
    status_note: str | None = None
    special_precautions: str | None = None
    marine_pollutant: str | None = None


class InventoryStatusEntry(SDSBaseModel):
    jurisdiction: str | None = None
    status: str | None = None
    details: str | None = None


class Section1Identification(SDSBaseModel):
    product_identifier: str | None = None
    product_name: str | None = None
    synonyms: list[str] = Field(default_factory=list)
    product_number: str | None = None
    cas_number: str | None = None
    ec_number: str | None = None
    molecular_formula: str | None = None
    molecular_weight: str | None = None
    relevant_identified_uses: str | None = None
    uses_advised_against: str | None = None
    supplier_company_name: str | None = None
    supplier_address: str | None = None
    supplier_telephone: str | None = None
    supplier_fax: str | None = None
    supplier_website: str | None = None
    supplier_email: str | None = None
    emergency_telephone: str | None = None
    prepared_by: str | None = None


class Section2HazardsIdentification(SDSBaseModel):
    ghs_classifications: list[str] = Field(default_factory=list)
    signal_word: str | None = None
    pictograms: list[str] = Field(default_factory=list)
    hazard_statements: list[str] = Field(default_factory=list)
    precautionary_prevention: list[str] = Field(default_factory=list)
    precautionary_response: list[str] = Field(default_factory=list)
    precautionary_storage: list[str] = Field(default_factory=list)
    precautionary_disposal: list[str] = Field(default_factory=list)
    hazards_not_otherwise_classified: str | None = None
    summary_of_emergency: str | None = None
    physical_hazards: str | None = None
    health_hazards: str | None = None
    environmental_hazards: str | None = None
    other_hazards: str | None = None


class Section3Composition(SDSBaseModel):
    substance_or_mixture: str | None = None
    chemical_name: str | None = None
    common_name_and_synonyms: list[str] = Field(default_factory=list)
    cas_number: str | None = None
    ec_number: str | None = None
    index_number: str | None = None
    formula: str | None = None
    molecular_weight: str | None = None
    impurities_and_stabilizers: str | None = None
    disclosure_statement: str | None = None
    components: list[ComponentEntry] = Field(default_factory=list)


class Section4FirstAid(SDSBaseModel):
    general_advice: str | None = None
    inhalation: str | None = None
    skin_contact: str | None = None
    eye_contact: str | None = None
    ingestion: str | None = None
    most_important_symptoms: str | None = None
    delayed_effects: str | None = None
    immediate_medical_attention: str | None = None
    notes_to_physician: str | None = None


class Section5FireFighting(SDSBaseModel):
    suitable_extinguishing_media: str | None = None
    unsuitable_extinguishing_media: str | None = None
    specific_hazards_arising: str | None = None
    hazardous_combustion_products: str | None = None
    firefighting_advice: str | None = None
    further_information: str | None = None


class Section6AccidentalRelease(SDSBaseModel):
    personal_precautions: str | None = None
    protective_equipment: str | None = None
    emergency_procedures: str | None = None
    environmental_precautions: str | None = None
    containment_methods: str | None = None
    cleanup_methods: str | None = None
    reference_to_other_sections: str | None = None


class Section7HandlingStorage(SDSBaseModel):
    safe_handling_precautions: str | None = None
    storage_conditions: str | None = None
    storage_temperature: str | None = None
    incompatible_storage_materials: str | None = None
    specific_end_uses: str | None = None


class Section8ExposureControls(SDSBaseModel):
    occupational_exposure_limits: list[str] = Field(default_factory=list)
    biological_limits: list[str] = Field(default_factory=list)
    engineering_controls: str | None = None
    eye_face_protection: str | None = None
    hand_protection: str | None = None
    skin_body_protection: str | None = None
    respiratory_protection: str | None = None
    thermal_hazards: str | None = None
    environmental_exposure_controls: str | None = None


class Section9PhysicalChemicalProperties(SDSBaseModel):
    physical_state: str | None = None
    appearance_form: str | None = None
    colour: str | None = None
    odour: str | None = None
    odour_threshold: str | None = None
    pH: str | None = None
    melting_point_freezing_point: str | None = None
    initial_boiling_point_and_range: str | None = None
    flash_point: str | None = None
    evaporation_rate: str | None = None
    flammability: str | None = None
    upper_flammability_limit: str | None = None
    lower_flammability_limit: str | None = None
    vapor_pressure: str | None = None
    vapor_density: str | None = None
    relative_density: str | None = None
    density: str | None = None
    water_solubility: str | None = None
    partition_coefficient_log_pow: str | None = None
    autoignition_temperature: str | None = None
    decomposition_temperature: str | None = None
    viscosity: str | None = None
    explosive_properties: str | None = None
    oxidizing_properties: str | None = None
    particle_characteristics: str | None = None
    other_safety_information: str | None = None


class Section10StabilityReactivity(SDSBaseModel):
    reactivity: str | None = None
    chemical_stability: str | None = None
    possibility_of_hazardous_reactions: str | None = None
    conditions_to_avoid: str | None = None
    incompatible_materials: str | None = None
    hazardous_decomposition_products: str | None = None


class Section11ToxicologicalInformation(SDSBaseModel):
    likely_routes_of_exposure: str | None = None
    acute_toxicity_oral: str | None = None
    acute_toxicity_inhalation: str | None = None
    acute_toxicity_dermal: str | None = None
    skin_corrosion_irritation: str | None = None
    serious_eye_damage_irritation: str | None = None
    respiratory_or_skin_sensitization: str | None = None
    germ_cell_mutagenicity: str | None = None
    carcinogenicity: str | None = None
    reproductive_toxicity: str | None = None
    stot_single_exposure: str | None = None
    stot_repeated_exposure: str | None = None
    aspiration_hazard: str | None = None
    symptoms_related_to_characteristics: str | None = None
    toxicological_additional_information: str | None = None
    numerical_measures_of_toxicity: str | None = None


class Section12EcologicalInformation(SDSBaseModel):
    ecotoxicity_fish: str | None = None
    ecotoxicity_daphnia: str | None = None
    ecotoxicity_algae: str | None = None
    ecotoxicity_microorganisms: str | None = None
    persistence_and_degradability: str | None = None
    bioaccumulative_potential: str | None = None
    mobility_in_soil: str | None = None
    pbt_vpvb_assessment: str | None = None
    endocrine_disrupting_properties: str | None = None
    other_adverse_effects: str | None = None


class Section13DisposalConsiderations(SDSBaseModel):
    waste_treatment_methods_product: str | None = None
    waste_treatment_methods_packaging: str | None = None
    sewage_disposal_advice: str | None = None


class Section14TransportInformation(SDSBaseModel):
    transport_general_statement: str | None = None
    transport_modes: list[TransportModeEntry] = Field(default_factory=list)
    un_number: str | None = None
    un_proper_shipping_name: str | None = None
    transport_hazard_class: str | None = None
    packing_group: str | None = None
    environmental_hazards: str | None = None
    special_precautions: str | None = None
    transport_in_bulk: str | None = None
    dot_status: str | None = None
    adr_rid_status: str | None = None
    imdg_status: str | None = None
    iata_status: str | None = None


class Section15RegulatoryInformation(SDSBaseModel):
    regulatory_specific: str | None = None
    inventory_statuses: list[InventoryStatusEntry] = Field(default_factory=list)
    sara_302: str | None = None
    sara_313: str | None = None
    sara_311_312: str | None = None
    proposition_65: str | None = None
    china_registration: str | None = None
    other_regulations: str | None = None


class Section16OtherInformation(SDSBaseModel):
    revision_date: str | None = None
    version_number: str | None = None
    date_of_first_issue: str | None = None
    abbreviations_and_acronyms: list[str] = Field(default_factory=list)
    full_text_h_statements: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    disclaimer: str | None = None
    additional_information: str | None = None
