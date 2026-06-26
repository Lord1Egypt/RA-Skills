# Complex Problem Generation

## Purpose

Use this reference for multi-step word problems, condition filtering, compare-after-intermediate problems, and exam review items.

## Generation Rule

AI may design the item, but the worksheet spec must preserve the structure:

- problem type;
- known quantities;
- unknown quantity;
- required conditions;
- distractor or unused conditions;
- intermediate quantity;
- final operation;
- answer sentence;
- `answer_detail` with the full solving path.

## Review Status

Use one of:

- `draft`: not ready to print.
- `model_reviewed`: reviewed by another model or a second pass.
- `human_review_needed`: print only after parent/teacher confirmation.
- `approved`: ready to print.

Complex items should not be printed when `review_status` is `draft` or missing.

## Difficulty Control

If the target is reading or modeling, keep arithmetic easy enough not to hide the diagnosis.

Change one or two dimensions at a time:

- scenario;
- final question wording;
- condition order;
- distractor condition;
- intermediate quantity;
- calculation load.

## Answer Key

For multi-step items, `answer_detail` must show:

- each intermediate value;
- why a condition is used or ignored;
- the final equation or comparison;
- the final answer sentence and unit.
