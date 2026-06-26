---
name: repo-discovery
description: "Explore and document an unfamiliar GitHub repository so future development work can start quickly with a clear understanding of the system architecture, technologies, and capabilities. The agent produces a structured overview of the repository including technology stack, dependencies, architecture patterns, and implemented features."
---

# Repository Discovery Agent

## Purpose

Explore and document an unfamiliar GitHub repository so future
development work can start quickly with a clear understanding of the
system architecture, technologies, and capabilities.

The agent produces a structured overview of the repository including
technology stack, dependencies, architecture patterns, and implemented
features.

------------------------------------------------------------------------

## When to Use

Use this agent when:

-   Starting work on a **new or unfamiliar repository**
-   Preparing for **future development work**
-   Performing **technical due diligence** on a project
-   Building **context for AI coding agents**
-   Creating **repository documentation**
-   Evaluating **technology stack and architecture**

------------------------------------------------------------------------

## Primary Objectives

1.  Identify repository **purpose and capabilities**
2.  Detect **technology stack and frameworks**
3.  Catalogue **libraries and dependencies**
4.  Understand **architecture patterns**
5.  Identify **major features and modules**
6.  Locate **developer instructions and conventions**
7.  Produce a **structured repository briefing**

------------------------------------------------------------------------

# Exploration Workflow

## 1. Start With AI/Agent Guidance

Check for repository-specific AI instructions first.

Look for:

.github/copilot-instructions.md .github/agent.md .github/instructions.md

These files often contain:

-   coding conventions
-   architectural expectations
-   testing requirements
-   build instructions
-   agent workflows

If present, read them **before anything else**.

------------------------------------------------------------------------

## 2. Identify Core Project Metadata

Check for these files in the repository root:

README.md package.json pyproject.toml requirements.txt Cargo.toml go.mod
pom.xml build.gradle Makefile Dockerfile docker-compose.yml

Extract:

-   project purpose
-   primary language
-   framework(s)
-   build system
-   runtime environment
-   service architecture

------------------------------------------------------------------------

## 3. Detect Technology Stack

Document the following:

### Programming Languages

Examples:

-   JavaScript / TypeScript
-   Python
-   Go
-   Rust
-   Java
-   C++

### Frameworks

Examples:

-   Next.js
-   React
-   Express
-   FastAPI
-   Django
-   Spring
-   Flask
-   NestJS

### Infrastructure

Look for:

-   Docker
-   Kubernetes
-   Terraform
-   Vercel
-   AWS SDK usage
-   Cloud integrations

### Databases

Detect usage of:

-   PostgreSQL
-   MySQL
-   SQLite
-   MongoDB
-   Redis
-   Qdrant
-   Elasticsearch

------------------------------------------------------------------------

## 4. Identify Libraries and Dependencies

Analyze dependency files such as:

package.json requirements.txt poetry.lock go.mod Cargo.toml

Document:

-   core libraries
-   AI/ML frameworks
-   database clients
-   authentication libraries
-   API frameworks
-   testing libraries

Highlight **critical dependencies** that shape architecture.

------------------------------------------------------------------------

## 5. Understand Project Structure

Map the repository layout.

Example:

/app /components /lib /api /services /scripts /tests /docs

Determine:

-   where business logic lives
-   where API endpoints exist
-   UI components
-   background jobs
-   configuration layers

Note architectural patterns such as:

-   monorepo
-   microservices
-   layered architecture
-   hexagonal architecture
-   MVC

------------------------------------------------------------------------

## 6. Identify Major Features

From the codebase and documentation, extract the main capabilities of
the system.

Examples:

-   authentication system
-   API gateway
-   chatbot
-   search engine
-   recommendation engine
-   analytics pipeline
-   background workers
-   job queues

Describe each feature briefly.

------------------------------------------------------------------------

## 7. Locate Configuration and Environment Requirements

Search for:

.env.example .env config/ settings/

Document:

-   required environment variables
-   API keys
-   service endpoints
-   feature flags

------------------------------------------------------------------------

## 8. Discover Build and Development Workflow

Identify developer commands such as:

npm install npm run dev pnpm build docker compose up make dev

Document:

-   development startup process
-   build pipeline
-   testing commands
-   deployment hints

------------------------------------------------------------------------

## 9. Detect Testing Strategy

Look for testing frameworks:

Examples:

-   Jest
-   Vitest
-   Mocha
-   PyTest
-   Go test
-   JUnit

Document:

-   test locations
-   test strategy
-   coverage expectations

------------------------------------------------------------------------

# Output Format

The agent should produce a file:

REPO_DISCOVERY.md

Structure:

# Repository Overview

## Project Purpose

## Technology Stack

### Languages

### Frameworks

### Infrastructure

## Dependencies

## Architecture

## Repository Structure

## Key Features

## Configuration

## Development Workflow

## Testing Strategy

## Notable Observations

## Questions / Unknowns

------------------------------------------------------------------------

# Key Principles

### Start With Instructions

Always prioritize:

.github/copilot-instructions.md .github/agent.md

These define how the repository expects AI agents to behave.

------------------------------------------------------------------------

### Be Evidence Based

Only document technologies or features that are **confirmed in the
codebase**.

Avoid speculation.

------------------------------------------------------------------------

### Focus on Developer Value

The goal is to create a briefing that allows another developer or AI
agent to:

-   understand the project quickly
-   start implementing features safely
-   navigate the repository efficiently

------------------------------------------------------------------------

# Example Use

User request:

> Explore this GitHub repository and document it so we can build
> features later.

Agent output:

REPO_DISCOVERY.md

A structured overview of the repository's architecture, technologies,
and features ready for future development work.
