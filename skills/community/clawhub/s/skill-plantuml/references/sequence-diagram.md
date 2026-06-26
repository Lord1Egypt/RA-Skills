# Sequence Diagram Syntax

## Participant Syntax

Usage: `<participant> <name> [as <alias>] [<< <Stereotypes> >>] [order <order>] [<color>]`

- `<participant>`: Participant type (required)
- `<name>`: Participant name. Must not be identical to `<participant>` (required)
- `<alias>`: Alias of participant (optional)
- `<Stereotypes>`: Stereotypes to participant (optional)
- `<order>`: Order of participant (optional)
- `<color>`: Participant color. Participant inside a `box` shall not inherit the box's color (optional)

Example: `participant Participant1 as Foo << p >> #lightBlue`

## Supported keywords

**participant**:

- Syntax: Use `## Participant Syntax` to replace `<participant>` with `participant` and `<color>` with `#ADD8E6` .

**actor**:

- Syntax: Use `## Participant Syntax` to replace `<participant>` with `actor` and `<color>` with `#FF9A80` .

**boundary**:

- Syntax: Use `## Participant Syntax` to replace `<participant>` with `boundary` and `<color>` with `#9FA8DA` .

**control**:

- Syntax: Use `## Participant Syntax` to replace `<participant>` with `control` and `<color>` with `#66C9BF` .

**entity**:

- Syntax: Use `## Participant Syntax` to replace `<participant>` with `entity` and `<color>` with `#FFE57F` .

**database**:

- Syntax: Use `## Participant Syntax` to replace `<participant>` with `database` and `<color>` with `#8FC991` .

**collections**:

- Syntax: Use `## Participant Syntax` to replace `<participant>` with `collections` and `<color>` with `#82ACE2` .

**queue**:

- Syntax: Use `## Participant Syntax` to replace `<participant>` with `queue` and `<color>` with `#FFC870` .

## Sequence Diagram Specification

**autonumber Rules**:

- Add `autonumber` after `@startuml` for automatic numbering.

**activation Rules**:

- Use `activate`/`deactivate` to display participant activation status during calls between
  participants

**database Rules**:

- Requests to the database must include the table name (e.g., `SELECT * FROM xxx` or `INSERT INTO xxx`) to indicate
  which
  table is being accessed.

**box Rules**:

- Set default background color of `box` to `#LightBlue`.
- Background color goes **after** the box title, e.g., `box box_title #LightBlue`, not `box #LightBlue box_title`.
- If the box contains changes such as business logic judgments and branches, use `#FFB6C1` instead of `#LightBlue`.

**participant Rules**:

- Participants not wrapped by a box should be colored `#LightBlue`; participants wrapped by a box
  should not be colored separately (inherit the box color).

**alt/else Rules**:

- It is highly recommended to add condition judgments for alt and else if possible

**arrow Rules**:

- Use the `-[#color]>` syntax to change the arrow color.

## Sequence Diagram Usage

[PlantUML Sequence Diagram](https://plantuml.com/en/sequence-diagram)
