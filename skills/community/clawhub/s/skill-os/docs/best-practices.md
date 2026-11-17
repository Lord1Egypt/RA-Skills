# Skill Design Best Practices

> Guidelines for designing skills that are powerful, maintainable, and user-friendly.

---

## 1. Start with the User

```
Before writing a single line of skill code:
→ Who will use this?
→ What do they need?
→ What frustrates them?
→ What would delight them?

Design for the user, not for the technology.
```

## 2. Purpose First

```
The first thing anyone sees is the purpose.
Make it:
→ Crystal clear
→ Specific, not vague
→ Compelling
→ Memorable

Bad: "This skill helps with writing"
Good: "Transforms any agent into an elite copywriter producing 
       high-converting sales copy using proven frameworks"
```

## 3. Reasoning Over Instructions

```
Don't just tell the agent WHAT to do.
Teach it HOW to think.

Instructions: "Write a blog post"
Reasoning: "Analyze audience → Select framework → 
            Craft hook → Build structure → 
            Edit rigorously → Verify quality"

The second produces better output every time.
```

## 4. Frameworks, Not Formulas

```
Provide frameworks that adapt to context,
not rigid formulas that break when context changes.

Formula: "Always use AIDA"
Framework: "For sales pages, use AIDA. 
            For emails, use PAS. 
            For stories, use Hero's Journey."
```

## 5. Quality is a System

```
Don't rely on the agent to "do good work."
Build quality into the system.

→ Quality gates before delivery
→ Checklists for verification
→ Examples of excellent output
→ Standards for every dimension
```

## 6. Handle Failure Gracefully

```
Things will go wrong. Plan for it.

→ Fallback chains
→ Error recovery protocols
→ Graceful degradation
→ Clear escalation paths
```

## 7. Design for All Levels

```
Novices need hand-holding.
Experts need power tools.
Design for both.

→ Quick-start for novices
→ Frameworks for competent
→ Advanced techniques for experts
→ Customization for masters
```

## 8. Keep It Maintainable

```
Skills evolve. Design for change.

→ Clear structure
→ Modular components
→ Version tracking
→ Extension points
→ Documentation
```

## 9. Test Before Shipping

```
Never ship without testing.

→ 10-dimension audit
→ Stress tests
→ Integration tests
→ User testing (novice + expert)
→ Regression tests
```

## 10. Document Everything

```
If it's not documented, it doesn't exist.

→ Purpose and triggers
→ How to use
→ What it produces
→ Known limitations
→ How to customize
→ How to troubleshoot
```
