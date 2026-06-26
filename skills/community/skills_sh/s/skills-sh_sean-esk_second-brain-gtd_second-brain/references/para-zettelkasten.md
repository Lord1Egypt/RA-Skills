# PARA + Zettelkasten Methodology

> Hybrid organizational system using PARA for structure and Zettelkasten for note-taking

---

## Overview

This system uses a **hybrid approach**:
- **PARA Method** (Tiago Forte) = Folder organization based on actionability
- **Zettelkasten** (Niklas Luhmann) = Note-taking methodology for knowledge building

**Golden Rule:** Use **folders for WHERE** (organization) and **tags for WHAT** (discovery)

---

## PARA Method: The Four Categories

### P - Projects

**Definition:** Active work with a deadline or defined end state

**Examples:**
- Launch Product X by Q2
- Plan vacation
- Complete tax filing

**Location:** `01-Projects/`

**Characteristics:**
- Has end date or completion criteria
- Actively worked on
- Specific deliverable

---

### A - Areas

**Definition:** Ongoing responsibilities with no end date

**Examples:**
- Career Development
- Health & Fitness
- Personal Development

**Location:** `02-Areas/`

**Characteristics:**
- Continuous responsibility
- Standards to maintain
- No completion date

---

### R - Resources

**Definition:** Topics of interest, reference materials, passive knowledge

**Examples:**
- Research materials
- How-to guides
- Reference documentation

**Location:** `03-Resources/`

**Characteristics:**
- Reference material
- Not actively worked on
- Topic-based organization

---

### A - Archives

**Definition:** Completed projects and inactive items

**Location:** `04-Archives/`

**Characteristics:**
- No longer active
- Completed or abandoned
- Kept for reference

---

## PARA Decision Framework

When you have information, ask:

1. **Is it actionable with a deadline?** → Projects
2. **Is it an ongoing responsibility?** → Areas
3. **Is it reference material?** → Resources
4. **Is it completed or inactive?** → Archives
5. **Not sure yet?** → Inbox (process later)

---

## Zettelkasten Principles

### 1. Atomic Notes

**One idea per note**

- Reusable in different contexts
- Easier to link
- Prevents bloat

**Test:** "Can this idea stand alone and be useful in a different context?"

### 2. Connected Notes

**Link everything relevant**

- Use `[[double brackets]]` liberally
- Aim for 3+ links per permanent note
- Emergent insights from connections

### 3. Own Words

**Always paraphrase and interpret**

- Ensures understanding
- Makes it yours
- Forces active processing

### 4. Progressive Elaboration

**Notes improve over time**

- Capture rough notes quickly
- Refine during reviews
- Add links over time

---

## Note Types

### Fleeting Notes

**Quick temporary captures**

- Rough, unprocessed
- Process within 48 hours
- Convert to permanent note OR delete

**Location:** `00-Inbox/Fleeting-Notes/`

### Literature Notes

**Summaries of external sources**

- From books, articles, videos
- In your own words
- Source referenced

**Location:** `03-Resources/Reference-Notes/`

### Permanent Notes

**Atomic, refined, evergreen insights**

- One core idea
- Fully developed
- Well-connected (3+ links)
- Evergreen

**Location:** `Permanent Notes/`

---

## Folder Structure

```
{{vaultPath}}/
├── 00-Inbox/
│   ├── Daily/              # Daily captures
│   └── Fleeting-Notes/     # Quick thoughts
├── 01-Projects/            # Active with deadlines
├── 02-Areas/               # Ongoing responsibilities
│   └── Relationships/      # Individual people notes
├── 03-Resources/
│   └── Reference-Notes/    # External source summaries
├── 04-Archives/            # Completed/inactive
├── Daily Plans/            # Generated daily plans
├── Meeting Notes/          # Meeting documentation
├── Permanent Notes/        # Your synthesized insights
└── Templates/              # Reusable templates
```

---

## Workflows

### Daily: Capture

All captures go to Inbox:
- Daily notes
- Fleeting notes
- Quick ideas

**Goal:** Low friction - just capture

### 3x Weekly: Process

For each inbox item:
1. Is it actionable? → Create project or task
2. Is it insightful? → Create permanent note
3. Is it reference? → Move to Resources
4. None of the above → Delete

**Goal:** Inbox zero regularly

### Weekly: Organize

- Process all inbox items
- Review active projects
- Update project statuses
- Move completed items to Archives
- Identify knowledge gaps

---

## Best Practices

### DO:

- Start in Inbox - All captures begin there
- Link Liberally - More connections = more insights
- Write for Future You - Assume you'll forget context
- One Idea Per Note - Atomic is powerful
- Review Weekly - System decays without maintenance

### DON'T:

- Over-organize upfront - Structure emerges organically
- Hoard everything - Some notes can die
- Aim for perfect notes - Rough > missing
- Deep folder nesting - Max 3 levels
- Skip reviews - Leads to system decay

---

## Maps of Content (MOCs)

**Index notes that organize related notes by topic**

**Purpose:**
- Navigate related notes
- See topic overview
- Identify knowledge gaps

**Example:**
```markdown
# Productivity MOC

## Time Management
- [[Pomodoro Technique]]
- [[Time Blocking]]

## Task Management
- [[GTD Overview]]
- [[Weekly Review Process]]
```

---

**Remember:** "Your mind is for having ideas, not holding them." — David Allen

**Philosophy:** Perfect is the enemy of good. Start messy, iterate, improve. The best system is the one you actually use.
