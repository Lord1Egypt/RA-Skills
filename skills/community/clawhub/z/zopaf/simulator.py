"""Orchestrates a turn-based negotiation between two agents."""
from __future__ import annotations

import re

from agent import NegotiationAgent
from case import NegotiationCase

import anthropic


def extract_deal_terms(
    transcript: str, case: NegotiationCase
) -> dict[str, str] | None:
    """Use an LLM call to extract structured deal terms from the transcript."""
    issue_descriptions = []
    for issue in case.issues:
        opts = ", ".join(f'"{o}"' for o in issue.options)
        issue_descriptions.append(f"- {issue.name} (options: {opts})")
    issues_block = "\n".join(issue_descriptions)

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system="You extract structured deal terms from negotiation transcripts. Respond ONLY with the extracted terms in the exact format requested, nothing else.",
        messages=[{
            "role": "user",
            "content": f"""Extract the final agreed deal from this negotiation transcript.

ISSUES AND VALID OPTIONS:
{issues_block}

TRANSCRIPT:
{transcript}

Respond with ONLY the agreed terms, one per line, in this exact format:
issue_name: chosen_option

If no deal was reached, respond with exactly: NO DEAL

Use the exact issue names and option values listed above.""",
        }],
    )

    text = response.content[0].text.strip()
    if "NO DEAL" in text.upper():
        return None

    terms = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"')
            # Match to actual issue names (case-insensitive)
            for issue in case.issues:
                if issue.name.lower() == key.lower():
                    # Match to actual option values
                    for opt in issue.options:
                        if opt.lower() == value.lower():
                            terms[issue.name] = opt
                            break
                    break

    # Verify all issues are covered
    if len(terms) != len(case.issues):
        return None

    return terms


def run_negotiation(case: NegotiationCase, verbose: bool = True) -> dict:
    """Run a full negotiation simulation.

    Returns a dict with:
        - transcript: list of (speaker_name, message) tuples
        - deal: dict of agreed terms or None
        - rounds: number of rounds completed
    """
    agent_a = NegotiationAgent(case, "a")
    agent_b = NegotiationAgent(case, "b")

    transcript: list[tuple[str, str]] = []
    deal_reached = False

    for round_num in range(1, case.max_rounds + 1):
        if verbose:
            print(f"\n{'='*60}")
            print(f"  ROUND {round_num}")
            print(f"{'='*60}")

        # Agent A's turn
        if round_num == 1:
            a_response = agent_a.respond()
        else:
            a_response = agent_a.respond(b_response)

        transcript.append((case.party_a_name, a_response))
        if verbose:
            print(f"\n[{case.party_a_name}]:")
            print(a_response)

        if "DEAL AGREED" in a_response.upper():
            deal_reached = True
            break

        # Agent B's turn
        b_response = agent_b.respond(a_response)
        transcript.append((case.party_b_name, b_response))
        if verbose:
            print(f"\n[{case.party_b_name}]:")
            print(b_response)

        if "DEAL AGREED" in b_response.upper():
            deal_reached = True
            break

    # Extract deal terms from transcript
    deal = None
    if deal_reached:
        full_transcript = "\n\n".join(
            f"[{name}]: {msg}" for name, msg in transcript
        )
        deal = extract_deal_terms(full_transcript, case)

    rounds_completed = min(
        (len(transcript) + 1) // 2, case.max_rounds
    )

    return {
        "transcript": transcript,
        "deal": deal,
        "rounds": rounds_completed,
    }
