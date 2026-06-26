---
name: tracker
description: >
  Design, organize, and improve tracking systems for work, goals, follow-ups, pipelines,
  projects, habits, issues, and ongoing operations. Use when someone needs a structured
  way to monitor movement, status, risk, ownership, and next actions over time.
---

# Tracker

A tracker is not just a place to record information.

A tracker is a visibility system.

Most tracking fails because people capture too much, review too little, and define
status too vaguely. They build spreadsheets, lists, dashboards, or boards that store
activity, but do not create clarity about what matters, what is changing, what is stuck,
who owns it, and what should happen next.

This skill helps turn passive record-keeping into useful tracking systems.

## Trigger Conditions

Use this skill when the user needs to:
- build a tracker for work, projects, leads, clients, candidates, issues, or tasks
- monitor status across multiple moving items
- create a follow-up system
- define what fields should be tracked and why
- improve visibility, accountability, or review cadence
- identify stale items, bottlenecks, or risk signals
- organize recurring progress reviews
- move from scattered notes to structured tracking

Also trigger when the user says things like:
- "Help me build a tracker"
- "What should I track"
- "I need a follow-up system"
- "How do I keep visibility on this"
- "My spreadsheet is messy"
- "How do I track progress over time"
- "I need a status tracker"

## Core Principle

A good tracker does not collect everything.

It tracks the few things that make action clearer.

The purpose of a tracker is not memory alone. It is judgment support:
to show what exists, what changed, what matters, what is stale, and what should be done next.

## What This Skill Does

This skill helps:
- define what needs to be tracked and at what level
- design tracking fields, statuses, owners, and review logic
- separate useful visibility from clutter
- improve follow-up and accountability
- detect staleness, risk, and bottlenecks
- match tracker design to the user's workflow
- create structures that support review and action, not just storage

## Default Outputs

Depending on the request, produce one or more of the following:

1. Tracker Design  
A structured model showing fields, statuses, owners, and update rules.

2. Tracker Schema  
A clear specification for columns, definitions, and data logic.

3. Follow-up Tracker  
A tracker focused on next steps, due dates, and stale-item review.

4. Status Review System  
A cadence and checklist for reviewing tracked items consistently.

5. Tracker Audit  
A diagnosis of why an existing tracker feels noisy, unclear, or unusable.

6. Dashboard Input Map  
A reduced set of signals that should feed higher-level reporting.

## Response Rules

When responding:
- define what is being tracked
- identify the decisions the tracker should support
- minimize fields to what changes action
- keep status labels meaningful and distinct
- make ownership visible
- include review cadence where relevant
- distinguish tracking from execution
- prefer clarity and usability over overbuilt systems

## Tracker Architecture
~~~python
TRACKER_ARCHITECTURE = {
  "core_elements": {
    "object": "What is being tracked",
    "status": "Current meaningful state",
    "owner": "Who is responsible",
    "next_action": "What should happen next",
    "date_logic": "When it was updated, due, or last touched",
    "priority": "How much attention it deserves",
    "risk": "Whether anything threatens progress",
    "notes": "Only what adds context that changes action"
  },
  "guiding_questions": [
    "What exactly is being tracked",
    "What decisions should the tracker help make",
    "What fields actually change action",
    "What would count as stale",
    "Who is expected to update it",
    "How often should it be reviewed"
  ]
}
~~~

## Tracker Workflow
~~~python
TRACKER_WORKFLOW = {
  "step_1_define_object": {
    "purpose": "Clarify what unit the tracker is tracking",
    "examples": [
      "lead",
      "task",
      "candidate",
      "client account",
      "support issue",
      "project milestone",
      "habit",
      "follow-up item"
    ]
  },
  "step_2_define_decisions": {
    "purpose": "Clarify what the tracker should help decide",
    "examples": [
      "what needs attention now",
      "what is overdue",
      "what is blocked",
      "what is high risk",
      "what can be closed",
      "what needs escalation"
    ]
  },
  "step_3_define_fields": {
    "purpose": "Choose only fields that support those decisions",
    "common_fields": [
      "name",
      "status",
      "owner",
      "priority",
      "last_updated",
      "due_date",
      "next_action",
      "risk_flag",
      "notes"
    ]
  },
  "step_4_define_status_logic": {
    "purpose": "Create statuses that imply action",
    "rules": [
      "Statuses should be mutually distinct",
      "Each status should suggest what happens next",
      "Avoid vague labels like active unless clarified",
      "Use stale or blocked states when relevant"
    ]
  },
  "step_5_define_review_cadence": {
    "purpose": "Prevent trackers from becoming dead storage",
    "outputs": [
      "daily review",
      "weekly review",
      "stage-based review",
      "stale-item scan",
      "owner check-in"
    ]
  },
  "step_6_define_cleanup_logic": {
    "purpose": "Keep the tracker trustworthy over time",
    "methods": [
      "archive closed items",
      "flag untouched items",
      "merge duplicates",
      "remove abandoned entries",
      "escalate items beyond threshold"
    ]
  }
}
~~~

## Common Tracker Types
~~~python
TRACKER_TYPES = {
  "follow_up_tracker": {
    "use_when": "The user needs to remember and act on pending items",
    "focus": ["next action", "due date", "last contact", "owner", "stale flag"]
  },
  "project_tracker": {
    "use_when": "The user needs visibility into progress across work items",
    "focus": ["milestone", "status", "owner", "dependency", "risk", "target date"]
  },
  "pipeline_tracker": {
    "use_when": "The user needs to monitor movement through stages",
    "focus": ["stage", "owner", "next step", "time in stage", "priority", "blocker"]
  },
  "issue_tracker": {
    "use_when": "The user needs to track problems until resolution",
    "focus": ["issue type", "severity", "owner", "status", "deadline", "resolution"]
  },
  "habit_tracker": {
    "use_when": "The user needs to track repeated behaviors over time",
    "focus": ["frequency", "completion", "streak", "consistency", "review period"]
  },
  "account_tracker": {
    "use_when": "The user needs ongoing visibility into accounts or relationships",
    "focus": ["health", "next milestone", "owner", "risk", "recent activity", "opportunity"]
  }
}
~~~

## Tracker Quality Logic
~~~python
TRACKER_QUALITY = {
  "warning_signs": [
    "Too many fields with no clear purpose",
    "Statuses do not imply action",
    "No owner is assigned",
    "Many items have no next step",
    "The tracker is updated irregularly",
    "Closed items clutter the active view",
    "Everything is marked high priority",
    "People use side channels instead of the tracker"
  ],
  "fixes": [
    "Reduce fields to decision-relevant data",
    "Tighten status definitions",
    "Add next-action discipline",
    "Create stale-item review rules",
    "Archive inactive or closed items",
    "Assign ownership explicitly",
    "Set a regular review cadence"
  ]
}
~~~

## Tracker Output Format

### Tracker Summary
- Object Being Tracked:
- Purpose of Tracking:
- Key Fields:
- Status Logic:
- Ownership Model:
- Review Cadence:
- Risk or Stale Rules:
- Cleanup Rules:
- Recommended Next Step:

## Boundaries

This skill helps design and improve tracking systems, visibility structures,
and review logic.

It does not replace legal, compliance, accounting, HR, or operational judgment.
For regulated, sensitive, or audit-critical environments, outputs should be adapted
to the user's jurisdiction, system requirements, and internal controls.

## Quality Check Before Delivering

- [ ] The object being tracked is clearly defined
- [ ] The tracker supports specific decisions
- [ ] Fields are limited to what changes action
- [ ] Statuses are distinct and meaningful
- [ ] Ownership is visible
- [ ] Review cadence is defined
- [ ] Stale and cleanup logic exist
- [ ] Output ends with a concrete next step
