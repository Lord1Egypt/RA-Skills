from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def structuredArgumentation(
    claim: str,
    premises: null,
    conclusion: str,
    argumentId: Optional[str] = None,
    argumentType: str,
    confidence: float,
    respondsTo: Optional[str] = None,
    supports: Optional[null] = None,
    contradicts: Optional[null] = None,
    strengths: Optional[null] = None,
    weaknesses: Optional[null] = None,
    nextArgumentNeeded: bool,
    suggestedNextTypes: Optional[null] = None
) -> Dict[str, Any]:
    """
    A detailed tool for systematic dialectical reasoning and argument analysis.
This tool helps analyze complex questions through formal argumentation structures.
It facilitates the creation, critique, and synthesis of competing arguments.

When to use this tool:
- Evaluating competing perspectives and claims
- Analyzing complex ethical dilemmas
- Assessing policy proposals with multiple stakeholders
- Exploring scientific hypotheses and counter-arguments

Key features:
- Break down arguments into claims, premises, and conclusions
- Track relationships between arguments
- Represent objections and rebuttals
- Facilitate dialectical progression through thesis-antithesis-synthesis
- Evaluate argument strengths and weaknesses
- Visualize argument structures

Parameters explained:
- claim: The central proposition being argued
- premises: Supporting evidence or assumptions
- conclusion: The logical consequence of accepting the claim
- argumentType: Whether this is a thesis, antithesis, synthesis, objection, or rebuttal
- confidence: Your confidence level in this argument (0.0-1.0)
- respondsTo: ID of an argument this directly responds to
- supports/contradicts: IDs of arguments this supports or contradicts
- strengths/weaknesses: Notable strong or weak points of the argument
- nextArgumentNeeded: Whether another argument is needed in the dialectic
    
    Args:
        claim: The central proposition being argued
        premises: Supporting evidence or assumptions
        conclusion: The logical consequence of accepting the claim
        argumentId: Optional unique identifier for this argument
        argumentType: The type of argument being presented
        confidence: Confidence level in this argument (0.0-1.0)
        respondsTo: ID of the argument this directly responds to
        supports: IDs of arguments this supports
        contradicts: IDs of arguments this contradicts
        strengths: Notable strong points of the argument
        weaknesses: Notable weak points of the argument
        nextArgumentNeeded: Whether another argument is needed in the dialectic
        suggestedNextTypes: Suggested types for the next argument
    
    Returns:
        
    """
    arguments = {
        "claim": claim,
        "premises": premises,
        "conclusion": conclusion,
        "argumentId": argumentId,
        "argumentType": argumentType,
        "confidence": confidence,
        "respondsTo": respondsTo,
        "supports": supports,
        "contradicts": contradicts,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "nextArgumentNeeded": nextArgumentNeeded,
        "suggestedNextTypes": suggestedNextTypes
    }
    
    return call_api("1777316659309571", "structuredArgumentation", arguments)

