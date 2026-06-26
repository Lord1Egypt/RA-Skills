"""
Universal Data Analyst

Data analysis skill based on a four-layer universal analysis framework:
1. Data Ontology - Don't ask "what economy", ask "what existence"
2. Problem Typology - Don't ask "how to profit", ask "what problem to solve"
3. Methodology Mapping - Match domain-recognized analysis methods
4. Validation & Output - Ensure robust conclusions

Key Features:
- Every analysis invokes an LLM for reasoning and judgment
- No hardcoded keyword rules
- Supports both economic and non-economic data
- Supports single-pass full analysis and multi-turn interaction

Main Components:
- UniversalDataAnalyst: Core data operations
- LLMAnalyzer: LLM analysis wrapper
- DataAnalysisOrchestrator: Workflow orchestration

Usage:
    from universal_data_analyst import DataAnalysisOrchestrator

    orchestrator = DataAnalysisOrchestrator()
    results = orchestrator.run_full_analysis(
        file_path="data.csv",
        user_intent="Analyze sales trends and customer behavior"
    )
"""

__version__ = "1.0.0"
__author__ = "Claude"

from .main import UniversalDataAnalyst, DataOntology, AnalysisPlan
from .llm_analyzer import LLMAnalyzer, OntologyResult, AnalysisPlan as LLMAnalysisPlan
from .orchestrator import DataAnalysisOrchestrator

__all__ = [
    'UniversalDataAnalyst',
    'LLMAnalyzer',
    'DataAnalysisOrchestrator',
    'DataOntology',
    'AnalysisPlan',
    'OntologyResult',
]
