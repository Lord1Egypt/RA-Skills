# Default design

Current version: **0.1.2**

## Purpose
`rolling-suds-workiz-note-builder` turns cleaned intake or estimate context from Rolling Suds workflows into short internal notes that are easy to paste into Workiz.

## Why this exists
Raw intake is messy.
Estimator output can be a little too rich.
Workiz notes need the operational middle ground.
Virtual quoting is a primary workflow, so notes should treat virtual appointments as normal and operationally valid.

## Default note modes
1. Appointment note
2. Estimate note
3. Comparison note
4. Follow-up note

## Design principle
The note should preserve business meaning, not every detail.

## Good note qualities
- short
- factual
- operational
- easy to paste
- clear about what still needs confirmation

## Bad note qualities
- too fluffy
- too long
- too AI-sounding
- too vague
- too legalistic

## Key learned behavior
If a customer wants only part of the house, the note should preserve the comparison logic:
- recommended full-house quote
- partial-only $250 minimum comparison

## Future improvements
- Add standardized note variants if the sales team develops a fixed internal style
- Add compact and expanded note modes
- Add examples from real leads and quotes
