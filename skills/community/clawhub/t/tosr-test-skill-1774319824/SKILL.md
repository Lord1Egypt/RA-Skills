# TOSR Test Skill

> 0.1.0 — A test skill for TOSR integration testing.

## Description

This skill is created by TOSR automated integration tests to verify the clawhub publish/update/delete workflow.
It exercises the full skill lifecycle: creation, version update, and deletion via the clawhub REST API.

## Features

- Validates skill creation via POST /api/v1/skills
- Validates skill update by publishing a new version
- Validates skill deletion via DELETE /api/v1/skills/{slug}
- Uses unique timestamped slugs to avoid conflicts between test runs

## Usage

This skill is for testing purposes only and will be deleted after the test completes.

## Version

0.1.0
