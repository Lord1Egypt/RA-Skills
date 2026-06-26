# Database Structure Documentation

_Last Updated: 2026-03-10_

The database forms the backbone for system memory, task delegation, and knowledge retention. Here's an overview of its schema and usage principles:

## Core Principles
1. **Persistence:** All significant memories and logs are stored in the database to ensure they persist across sessions.
2. **Scalability:** Modular schemas support scaling for new agents and workflows.
3. **Maintainability:** Data is well-documented for ease of use and debugging.
4. **Longevity:** The database is designed to last "forever" as Oblio evolves.

## Schemas & Tables

### `memory` Schema
Holds all data related to knowledge retention and agent operations.

| **Table**            | **Purpose**                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `ActivityLog`        | Tracks agent activities, including logs of completed tasks and operations.  |
| `AgentState`         | Stores metadata about active agents, their readiness, and current status.  |
| `ContextSnapshot`    | Holds context dumps for session continuity or debugging.                   |
| `DecisionLog`        | Records decisions made by agents and their justification.                  |
| `KnowledgeIndex`     | Index of key knowledge and their associated domains.                       |
| `Memories`           | Central memory store for facts, patterns, and persistent insights.         |
| `PersonaLog`         | Tracks persona evolution, including changes in Oblio's personality.        |
| `Sessions`           | Metadata about chat and interaction history.                               |
| `SessionLog`         | Detailed logs of session-specific activity.                                |
| `TaskQueue`          | Contains queued, pending, processing, and completed tasks.                 |

### Usage Guidelines
1. Store **everything** meaningful—memories, tasks, logs—to ensure Oblio's long-term growth and reliability.
2. Never overwrite existing data unless explicitly stated (e.g., updates to task statuses).
3. Regularly audit schemas for optimization (e.g., indexes, stored procedures).

### Future Directions
- Add detailed stored procedures for transaction standardization (reduce ad-hoc queries).
- Integrate encrypted storage for sensitive data.
- Explore replication for redundancy and high availability.

<End of documentation.>
