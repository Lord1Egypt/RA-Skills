# Deployment Shapes

Choose the lightest shape that still supports the content and publishing workflow.

## Shape 1: Static-only site

Use when:
- the site changes infrequently
- contact and booking are external
- content can be rebuilt on publish
- the user wants the simplest hosting model

## Shape 2: Static site plus serverless helpers

Use when:
- Notion-backed blog or collection data should be fetched securely
- form handling, webhook glue, or CMS endpoints are needed
- the site should stay lightweight without a full backend

## Shape 3: Repo-backed managed site

Use when:
- multiple collaborators need version history
- preview deploys and pull requests matter
- the user wants GitHub as an optional collaboration layer

Rule:
- GitHub is optional
- portability is not optional
