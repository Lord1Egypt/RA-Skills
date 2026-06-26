#!/usr/bin/env python3
"""Emit relationship-coaching worksheets in JSON or Markdown."""
from __future__ import annotations

import argparse
import json
from typing import Any, Iterable, Optional

WORKSHEETS: dict[str, dict[str, Any]] = {
    "soft-startup": {
        "title": "Soft Start-Up Builder",
        "use_when": "A user needs to raise a complaint without blame.",
        "steps": [
            "Observable behaviour: What happened on camera?",
            "Feeling: What did I feel without accusing?",
            "Positive need: What would help?",
            "Small request: What specific action am I asking for?",
        ],
        "template": "I felt {feeling} when {observable_behaviour}. What would help me is {positive_need}. Could we try {small_request}?",
        "avoid": ["global character attacks", "mind-reading", "'you always/never'", "sarcasm"],
        "example": "I felt lonely when we both looked at our phones through dinner. I’d love ten phone-free minutes together. Could we try that tonight?",
    },
    "time-out-and-return": {
        "title": "Flooding Time-Out and Return Plan",
        "use_when": "A conflict is escalating, one partner is flooded, or stonewalling is beginning.",
        "steps": [
            "Call a pause without blame.",
            "Set a return time between 20 and 45 minutes when possible.",
            "Use the break for down-regulation, not rehearsing arguments.",
            "Return with one soft sentence and one listening turn.",
        ],
        "template": "I’m getting overwhelmed and I don’t want to make this worse. I’m taking {minutes} minutes to calm down. I will come back at {return_time} and start by listening.",
        "avoid": ["storming out without a return time", "continuing by text", "using the break to punish"],
    },
    "repair-attempt": {
        "title": "Repair Attempt",
        "use_when": "The user has hurt their partner, snapped, withdrawn, or escalated.",
        "steps": ["Name the behaviour", "Own the impact", "Say what you wish you had done", "Ask what repair would help", "Commit to a future cue"],
        "template": "I’m sorry for {specific_behaviour}. I can see it affected you by {impact}. I wish I had {better_action}. What would help repair this right now?",
        "avoid": ["but you also", "I was just", "sorry you feel that way"],
    },
    "impact-listening": {
        "title": "Impact Listening Turn",
        "use_when": "A partner needs to feel understood before problem-solving.",
        "steps": ["Speaker gets 3-5 uninterrupted minutes", "Listener summarises content", "Listener names emotion", "Speaker corrects", "Only then move to response"],
        "template": "What I’m hearing is {summary}. The feeling underneath seems like {emotion}. Did I get that right?",
        "avoid": ["cross-examination", "defending before summarising", "arguing about intent"],
    },
    "two-turn-listening": {
        "title": "Two-Turn Listening",
        "use_when": "Both partners keep rebutting instead of hearing.",
        "steps": ["Partner A speaks for two minutes", "Partner B summarises", "Partner B validates one understandable part", "Switch", "Then make one concrete request each"],
        "template": "Before I answer, I’m going to say what I heard: {summary}. The part that makes sense to me is {validation}.",
        "avoid": ["rebuttal disguised as validation", "diagnosing motives", "bringing in extra topics"],
    },
    "dreams-within-conflict": {
        "title": "Dreams Within Conflict Interview",
        "use_when": "A recurring issue is stuck because each position protects a value or fear.",
        "steps": [
            "What does your position mean to you?",
            "What history makes this important?",
            "What are you afraid would happen if you gave it up?",
            "What value or dream are you protecting?",
            "What part of this can be flexible without betraying that value?",
        ],
        "template": "Under my position is the value of {value}. The fear is {fear}. The flexible part might be {flexible_area}.",
        "avoid": ["debating facts before understanding meaning", "mocking the dream", "all-or-nothing compromise"],
    },
    "compromise-circles": {
        "title": "Compromise Circles",
        "use_when": "The couple needs a temporary operating agreement on an unsolved problem.",
        "steps": ["Inner circle: non-negotiable needs", "Middle circle: strong preferences", "Outer circle: flexible areas", "Overlap: two-week trial agreement"],
        "template": "My core need is {core_need}. I can be flexible about {flexible_area}. A fair two-week trial would be {trial}.",
        "avoid": ["treating every preference as a core need", "permanent deals under pressure"],
    },
    "attachment-cycle-map": {
        "title": "Attachment Cycle Map",
        "use_when": "Pursue-withdraw, anxious-avoidant, or protest-distance cycles are present.",
        "steps": ["Trigger", "My protection move", "Partner impact", "Partner protection move", "My deeper fear", "My vulnerable request"],
        "template": "When {trigger}, I protect myself by {protection}. Underneath, I’m afraid of {fear}. What I need is {need}.",
        "avoid": ["labelling one partner as the problem", "using attachment labels as insults"],
    },
    "vulnerable-bid": {
        "title": "Vulnerable Bid Reframe",
        "use_when": "The user's complaint hides a softer attachment need.",
        "steps": ["Original protest", "Primary emotion", "Need for connection/autonomy", "Clean bid", "Partner response wanted"],
        "template": "Instead of {protest}, say: I’m feeling {emotion} and I could use {need}. Could you {small_response}?",
        "avoid": ["weaponising vulnerability", "testing the partner without telling them the need"],
    },
    "connection-before-analysis": {
        "title": "Connection Before Analysis",
        "use_when": "Relationship talks reliably make things worse.",
        "steps": ["Pause the analysis", "Choose one bonding action", "Use one-sentence truth", "Schedule deeper talk", "Keep talk under 15 minutes"],
        "template": "I want us to feel like teammates before we analyse this. Can we {bonding_action}, then each say one sentence about what we need?",
        "avoid": ["ambushing", "hours-long post-mortems", "demanding vulnerability on command"],
    },
    "love-map-refresh": {
        "title": "Love Map Refresh",
        "use_when": "A couple feels distant or only talks logistics.",
        "steps": ["Current stress", "Current hopes", "Recent private wins", "What I’m learning about myself", "One thing I want you to understand"],
        "template": "One thing that has changed in me lately is {change}. One thing I wish you knew is {wish}.",
        "avoid": ["interviewing mechanically", "using answers against partner later"],
    },
    "bids-audit": {
        "title": "Bids Audit",
        "use_when": "The relationship feels neglected, lonely, or low in everyday connection.",
        "steps": ["List five small bids each partner makes", "Mark turn-toward, turn-away, turn-against", "Choose two easy turn-toward responses", "Set a daily ritual"],
        "template": "When you {bid}, I can turn toward by {response}.",
        "avoid": ["scorekeeping", "grand gestures that replace daily responsiveness"],
    },
    "state-of-the-relationship": {
        "title": "Weekly State of the Relationship Agenda",
        "use_when": "The couple wants a regular check-in.",
        "steps": ["Two appreciations", "What worked this week", "One issue only", "Each partner summarises", "One agreement with owner and date", "Connection ritual"],
        "template": "This week I appreciated {appreciation}. The one issue I want to discuss is {issue}. My request is {request}.",
        "avoid": ["multiple agenda ambush", "using check-in as a trial", "ending without an agreement"],
    },
    "trust-repair-map": {
        "title": "Trust Repair Map",
        "use_when": "There has been lying, betrayal, infidelity, or broken agreements.",
        "steps": ["Has the harm stopped?", "What exactly happened?", "What impact did it have?", "What boundaries are needed?", "What transparency is reasonable?", "What follow-up rhythm?"],
        "template": "The behaviour I’m accountable for is {behaviour}. The impact I understand is {impact}. The future protection is {protection}.",
        "avoid": ["trickle truth", "blame-shifting", "turning repair into indefinite surveillance"],
    },
    "accountability-statement": {
        "title": "Accountability Statement",
        "use_when": "A user needs to apologise for a breach of trust or repeated hurt.",
        "steps": ["Specific behaviour", "No excuses", "Impact", "Values violated", "Prevention plan", "Repair request"],
        "template": "I did {behaviour}. It hurt you by {impact}. I’m not going to minimise it. My prevention plan is {plan}. What else would help repair?",
        "avoid": ["defensiveness", "asking for instant forgiveness", "performative remorse without behaviour"],
    },
    "brakes-and-accelerators": {
        "title": "Sexual Brakes and Accelerators Map",
        "use_when": "Desire, arousal, or erotic interest is low, inconsistent, or mismatched.",
        "steps": ["External brakes", "Internal brakes", "Relationship brakes", "Erotic accelerators", "Context that helps", "One pressure-free experiment"],
        "template": "My brakes are {brakes}. My accelerators are {accelerators}. The context that helps is {context}.",
        "avoid": ["treating low desire as defect", "pressuring for sex", "using the map to negotiate obligation"],
    },
    "affection-menu": {
        "title": "Affection, Sensuality, Eroticism, Sex Menu",
        "use_when": "Touch has become pressured, avoided, or all-or-nothing.",
        "steps": ["Green: always welcome", "Yellow: ask first", "Red: not now", "Non-sexual affection", "Sensual but not sexual", "Erotic but not intercourse", "Sexual if mutually wanted"],
        "template": "Green touch: {green}. Ask-first touch: {yellow}. Not-now touch: {red}.",
        "avoid": ["assuming all touch leads to sex", "sulking after a no", "withdrawing all affection after rejection"],
    },
    "desire-discrepancy-plan": {
        "title": "Desire Discrepancy Plan",
        "use_when": "One partner wants sex more often than the other.",
        "steps": ["Remove obligation", "Name what rejection means to each", "Name what pressure means to each", "Create affection menu", "Choose no-pressure sensual date", "Review without blame"],
        "template": "When I hear no, I tell myself {meaning}. When you feel pressure, you tell yourself {meaning}. Let’s create a plan that protects both of us.",
        "avoid": ["duty sex", "scorekeeping", "withholding affection as punishment"],
    },
    "pleasure-map": {
        "title": "Pleasure Map",
        "use_when": "A couple wants better sex, female pleasure support, or clearer feedback.",
        "steps": ["Contexts I enjoy", "Touch I like", "Touch I dislike", "Words that help", "Words that turn me off", "Pace", "Aftercare/debrief"],
        "template": "I like {liked_touch}, especially when {context}. Please avoid {avoid_touch}. A helpful cue from me is {cue}.",
        "avoid": ["goal pressure", "orgasm demands", "shaming preferences"],
    },
    "sexual-feedback-debrief": {
        "title": "Sexual Feedback Debrief",
        "use_when": "Partners need to discuss sex without bruising each other.",
        "steps": ["One thing I liked", "One thing I want more of", "One thing to adjust", "One thing I felt emotionally", "One request for next time"],
        "template": "I really liked {liked}. I’d enjoy more of {more}. One adjustment is {adjustment}, and I’m saying that as teamwork.",
        "avoid": ["grading", "body criticism", "comparison to exes", "feedback immediately after vulnerability unless agreed"],
    },
    "erotic-aliveness-audit": {
        "title": "Erotic Aliveness Audit",
        "use_when": "The relationship is loving but sexually flat or over-familiar.",
        "steps": ["When do I feel most alive?", "When do I feel attractive?", "Where have we become over-domesticated?", "What novelty feels safe?", "What separateness helps desire?"],
        "template": "I feel most alive when {alive_context}. I miss {missing_energy}. A small novelty I’d like to try is {novelty}.",
        "avoid": ["blaming familiarity alone", "using novelty to bypass resentment", "springing surprises without consent"],
    },
    "novelty-menu": {
        "title": "Novelty Menu",
        "use_when": "Couples want more passion or play without destabilising trust.",
        "steps": ["Low novelty", "Medium novelty", "High novelty", "Hard no", "Aftercare", "Debrief"],
        "template": "Low novelty I’d try: {low}. Medium: {medium}. Hard no: {no}. Aftercare I’d want: {aftercare}.",
        "avoid": ["surprise escalation", "punishing a no", "using novelty to avoid intimacy"],
    },
    "kink-consent-map": {
        "title": "Kink Consent Map",
        "use_when": "Adults want to discuss BDSM, power exchange, fantasy, dominance/submission, or taboo roleplay.",
        "steps": ["Erotic theme", "Exact acts: yes/maybe/no", "Words/roles", "Safeword or stop signal", "Health and trauma limits", "Privacy", "Aftercare", "Debrief"],
        "template": "The theme I’m interested in is {theme}. Yes: {yes}. Maybe: {maybe}. No: {no}. Stop signal: {stop}. Aftercare: {aftercare}.",
        "avoid": ["assuming fantasy equals consent", "performing to prove love", "ignoring a changed mind"],
    },
    "cnc-discussion-map": {
        "title": "Consensual Non-Consent Fantasy Discussion",
        "use_when": "A user mentions rape fantasy, ravishment fantasy, CNC, or forced-sex roleplay in a consensual adult context.",
        "steps": ["Validate fantasy without assuming enactment", "Separate real consent from roleplay", "Define words/actions that are off-limits", "Choose stop signals that override the scene", "Start symbolic/verbal", "Aftercare and next-day review"],
        "template": "The fantasy theme is {theme}; in real life, my consent rules are {rules}. If I use {stop_signal}, everything stops immediately.",
        "avoid": ["scripts that blur real refusal", "pressure to enact", "minors", "intoxication", "punishment for stopping"],
    },
    "safer-kink-alternatives": {
        "title": "Safer Alternatives to Breath Play / Neck Pressure",
        "use_when": "A user wants choking, strangulation, breath play, or neck pressure as a kink.",
        "steps": ["Identify desired ingredient", "Remove airway/neck restriction", "Choose verbal dominance or surrender", "Use eye contact, pacing, consensual restraint away from neck, or role language", "Debrief"],
        "template": "The ingredient I want is {ingredient}, not literal neck pressure. A safer substitute I’d try is {alternative}.",
        "avoid": ["technique for choking", "duration/intensity guidance", "claims that breath play is safe"],
    },
    "flirting-message-builder": {
        "title": "Flirting Message Builder",
        "use_when": "A user wants a text, dating-app opener, or low-pressure ask-out script.",
        "steps": ["Specific observation", "Warm emotion", "Light play or curiosity", "Clear invitation", "Low-pressure exit"],
        "template": "I liked {specific_observation}. It made me {warm_emotion}. Want to {invitation}? No pressure if your week is packed.",
        "avoid": ["negging", "sexual escalation before reciprocity", "interview-mode", "double texting after no response"],
    },
    "dating-reciprocity-check": {
        "title": "Dating Reciprocity Check",
        "use_when": "A user is unsure whether to escalate or back off.",
        "steps": ["Do they ask questions back?", "Do they make time?", "Do they respond with warmth?", "Do they accept or propose alternatives?", "If not, reduce pursuit"],
        "template": "If the response is {signal}, my next move is {next_move}. If there is no matched effort, I will {graceful_step_back}.",
        "avoid": ["trying to decode silence as hidden desire", "pushing after a soft no", "jealousy tactics"],
    },
    "love-languages-menu": {
        "title": "Love Languages Care Menu",
        "use_when": "A couple wants concrete ways to feel loved and appreciated.",
        "steps": ["Words", "Quality time", "Touch", "Acts of service", "Gifts", "What lands most right now", "Two weekly behaviours"],
        "template": "What lands for me lately is {preferred_signal}. Two actions that would help are {action1} and {action2}.",
        "avoid": ["rigid labels", "using touch language to pressure sex", "ignoring forms of care outside the five categories"],
    },
    "stay-or-leave-clarifier": {
        "title": "Stay-or-Leave Clarifier",
        "use_when": "The user is considering breakup, separation, divorce, or whether the relationship is viable.",
        "steps": ["Safety check", "What is good", "What is harmful", "What repeats", "What has changed with evidence", "Minimum viable conditions", "Timeline", "Practical constraints"],
        "template": "For this to be viable, I would need {conditions}. Evidence would look like {evidence}. My review date is {date}.",
        "avoid": ["using hope without evidence", "ignoring safety", "permanent decisions during acute flooding unless safety requires it"],
    },
    "influence-not-control": {
        "title": "Influence, Not Control",
        "use_when": "Only one partner is present and wants to change the relationship pattern.",
        "steps": ["What I control", "What I can request", "What I can stop doing", "What boundary I can set", "What evidence I will watch"],
        "template": "I can control {my_action}. I can request {request}. If the pattern continues, I will {boundary}.",
        "avoid": ["secret tests", "threats without follow-through", "trying to manage partner's emotions"],
    },
    "clean-request": {
        "title": "Clean Request",
        "use_when": "A user needs a direct request without manipulation or blame.",
        "steps": ["Context", "Feeling/impact", "Request", "Why it matters", "Boundary or next step if needed"],
        "template": "When {context}, I feel/experience {impact}. I’m asking for {request} because {why}. If that isn’t possible, I’ll need {boundary_or_next_step}.",
        "avoid": ["ultimatums disguised as requests", "mind-reading", "guilt trips"],
    },
    "boundary-script": {
        "title": "Boundary Script",
        "use_when": "The user needs to protect their behaviour or access without controlling the partner.",
        "steps": ["Name the boundary", "State the action you will take", "Do not threaten", "Follow through calmly"],
        "template": "I’m not available for {unacceptable_pattern}. If it happens, I will {my_action}. We can continue when {condition}.",
        "avoid": ["boundaries that control another adult", "boundaries as punishment", "negotiating during escalation"],
    },
    "safety-next-step": {
        "title": "Safety Next Step",
        "use_when": "There is danger, coercive control, stalking, non-consent, self-harm, minors, or child-safety concern.",
        "steps": ["Immediate danger?", "Safe device/person?", "Emergency/crisis/domestic-abuse/sexual-assault/safeguarding support", "Do not confront", "Digital safety", "Document only if safe"],
        "template": "My safest next step is {safe_step}. I will use {safe_device_or_person}. I will not confront them with this plan.",
        "avoid": ["couples exercises", "shared blame", "telling the unsafe person plans", "assuming private browsing is fully safe"],
    },
    "values-and-outcome-clarifier": {
        "title": "Values and Outcome Clarifier",
        "use_when": "The user is vague, overwhelmed, or unsure what help they need.",
        "steps": ["What happened", "What I want to be different", "What I value", "What I fear", "Smallest useful next step", "What would count as progress"],
        "template": "The outcome I want is {outcome}. The value underneath is {value}. The smallest useful next step is {next_step}.",
        "avoid": ["over-interviewing", "turning every issue into a diagnosis"],
    },
    "one-sentence-truth": {
        "title": "One-Sentence Truth",
        "use_when": "A long relationship talk needs to be shortened and softened.",
        "steps": ["One sentence about feeling", "One sentence about need", "One request", "Stop"],
        "template": "I feel {feeling}. I need {need}. Could we {request}?",
        "avoid": ["monologues", "history dumps", "using one sentence to smuggle in ten accusations"],
    },
    "appreciation-menu": {
        "title": "Specific Appreciation Menu",
        "use_when": "The couple needs to rebuild fondness and positive sentiment.",
        "steps": ["Behaviour I noticed", "Quality it showed", "Impact on me", "One more appreciation"],
        "template": "When you {behaviour}, it showed {quality}. It made me feel {impact}.",
        "avoid": ["generic praise only", "praise as a setup for criticism"],
    },
}

ALIASES = {
    "soft_startup": "soft-startup",
    "timeout": "time-out-and-return",
    "time_out_return": "time-out-and-return",
    "repair": "repair-attempt",
    "listener_summary": "impact-listening",
    "love_maps": "love-map-refresh",
    "state_of_relationship": "state-of-the-relationship",
    "trust_repair": "trust-repair-map",
    "brakes_accelerators": "brakes-and-accelerators",
    "kink_consent": "kink-consent-map",
    "cnc": "cnc-discussion-map",
    "flirting": "flirting-message-builder",
    "love_languages": "love-languages-menu",
    "stay_leave": "stay-or-leave-clarifier",
    "safety": "safety-next-step",
}


def normalise_key(key: str) -> str:
    k = key.strip().lower().replace("_", "-").replace(" ", "-")
    return ALIASES.get(k, k)


def render_markdown(key: str, worksheet: dict[str, Any]) -> str:
    lines = [f"# {worksheet['title']}", "", f"Use when: {worksheet['use_when']}", "", "## Steps"]
    lines.extend(f"{i}. {step}" for i, step in enumerate(worksheet["steps"], start=1))
    lines += ["", "## Template", worksheet.get("template", ""), ""]
    if worksheet.get("example"):
        lines += ["## Example", worksheet["example"], ""]
    if worksheet.get("avoid"):
        lines += ["## Avoid"] + [f"- {item}" for item in worksheet["avoid"]]
    lines += ["", f"Worksheet key: `{key}`"]
    return "\n".join(lines)


def get_worksheet(key: str) -> tuple[str, dict[str, Any]]:
    normalised = normalise_key(key)
    if normalised not in WORKSHEETS:
        available = ", ".join(sorted(WORKSHEETS))
        raise SystemExit(f"Error: unknown worksheet {key!r}. Available worksheets: {available}")
    return normalised, WORKSHEETS[normalised]


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Emit relationship-coaching worksheets in JSON or Markdown.",
        epilog="Example: python3 scripts/worksheet_builder.py --worksheet soft-startup --format markdown",
    )
    parser.add_argument("--worksheet", help="Worksheet key or alias. Use --list to see options.")
    parser.add_argument("--list", action="store_true", help="List available worksheet keys as JSON.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format. Default: json.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    if args.list:
        data = {"worksheets": sorted(WORKSHEETS), "aliases": ALIASES}
        print(json.dumps(data, indent=2 if args.pretty else None, ensure_ascii=False))
        return 0
    if not args.worksheet:
        raise SystemExit("Error: --worksheet is required unless --list is used. Run with --help for usage.")
    key, worksheet = get_worksheet(args.worksheet)
    if args.format == "markdown":
        print(render_markdown(key, worksheet))
    else:
        data = {"key": key, **worksheet}
        print(json.dumps(data, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
