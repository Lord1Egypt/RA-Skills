# Trigger Design

Use this file when creating or reviewing a skill description.

## Goal

Make the skill trigger when it is useful, and stay out of the way when it is not.

## Positive Boundary Questions

Check whether the description clearly answers:

- what the skill does
- when it should be used
- what common user phrases or contexts should activate it
- what kind of output or workflow the skill supports

## Negative Boundary Questions

Check whether the description also makes clear:

- which tasks are adjacent but out of scope
- which requests should not route here
- whether the skill is only for a specific domain, language, or release stage

## Common Failure Modes

- Too narrow: only triggers on exact wording
- Too broad: hijacks adjacent tasks
- Too abstract: sounds good but provides no routing signal
- Missing exclusions: causes accidental activation on nearby tasks
- Missing user phrasing: does not match how real users ask

## Practical Rule

A strong description should help answer:

- "Why would this skill trigger?"
- "Why would it not trigger?"

