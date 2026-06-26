# Child Development Tracking Examples

## Example 1: Record Developmental Assessment (Normal)

### User Input
```
/child-development record
```

### System Response
```
Please assess whether the following milestones have been achieved (yes/no):

Gross Motor (6 months)
  Can sit briefly without support
  Can support self on hands when prone
  Can roll from back to stomach
```

### Output After User Confirmation
```
Developmental Assessment - Normal

Assessment Information:
Child: Xiaoming
Age: 6 months
Assessment Date: July 1, 2025

Gross Motor Development:
  Sitting: Achieved (achieved at 5 months)
  Rolling: Achieved (achieved at 4 months)

Overall Assessment:
  Normal development

Data saved
```

## Example 2: Developmental Delay Warning

### User Input
```
/child-development delay
```

### System Output
```
Developmental Delay Warning Signs

Child: Xiaoming
Current Age: 9 months

Warning Signs Requiring Immediate Medical Attention:
Seek immediate medical care if any of the following occurs:

Gross Motor:
  Cannot sit
  Body is stiff or too floppy

Language:
  Does not babble
  No response to name
```

## Example 3: View Milestone List

### User Input
```
/child-development milestone gross
```

### System Output
```
Gross Motor Development Milestones

1mo   Head control briefly
2mo   Lifts head 45 when prone
3mo   Lifts head 90 when prone (stable head control)
4mo   Stable head control, rolling
5mo   Sits briefly with support
6mo   Sits briefly without support
7mo   Sits stably without support
8mo   Crawling, standing with support
9mo   Moves from sitting to lying
10mo  Cruising
11mo  Stands briefly
12mo  Walks a few steps independently
```

## Example 4: View Assessment History

### User Input
```
/child-development history
```

### System Output
```
Developmental Assessment History

Date        Age    Gross Motor    Fine Motor    Language    Social
────────────────────────────────────────────────────────────────
2025-07-01  6m      Normal         Normal        Normal      Normal
2025-04-01  3m      Normal         Normal        Normal      Normal
2025-01-01  0m      Normal         Normal        Normal      Normal
```
