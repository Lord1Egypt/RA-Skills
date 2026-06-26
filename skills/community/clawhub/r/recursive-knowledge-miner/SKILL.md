---
name: My skill
description: Professional multi-layered knowledge extraction and recursive knowledge graph construction.
---

# Professional Knowledge Extraction Skill

Expertly extract core concepts, entities, and logical relationships from complex professional text to build a multi-layered, interactive knowledge graph.

## Core Mission
Transform any professional inquiry or text into a structured, hierarchical knowledge representation that follows a 3-layer information architecture.

## Interaction Protocol

### 1. Response Structure
Always prioritize structured output. Every response MUST be a valid JSON object with the following schema:

```json
{
  "reply": "Your natural language explanation of the user's query.",
  "entities": [
    {
      "id": "unique_id (kebab-case or UUID)",
      "label": "Display Name",
      "group": "layer_type"
    }
  ],
  "relations": [
    {
      "from": "entity_id_A",
      "to": "entity_id_B",
      "label": "Relationship Description"
    }
  ]
}
```

### 2. The 3-Layer Information Architecture
Classify every extracted entity into one of these three `group` values:

*   **`core`**: The central theme or the main subject of the user's inquiry. Usually, there is only **ONE** core node per response.
*   **`primary`**: Key dimensions or high-level frameworks of the core topic (e.g., "Core Components", "Problem Solved", "Application Scenarios", "Historical Context"). Limit this to **3-5** nodes to avoid clutter.
*   **`detail`**: Deep-dive nodes, specific parameters, sub-technologies, references, or granular data points that support the `primary` nodes.

### 3. Relationship Logic
*   Connect `core` to `primary` nodes with descriptive labels.
*   Connect `primary` to their respective `detail` nodes.
*   Avoid cross-linking `detail` nodes unless a critical logical dependency exists.
*   Maintain semantic consistency by reusing provided entity IDs if available.

## Recursive Growth & Consistency
To maintain a growing knowledge network without duplication:

1.  **Reference Check**: Before creating a new entity, check the `existing_terms` list (if provided in the context).
2.  **ID Mapping**: If a concept already exists, use its exact `id`. Do NOT create a duplicate node with a different ID if the meaning is identical.
3.  **Attribute Inheritance**: Ensure new relationships (`relations`) correctly anchor onto these existing nodes, extending the network from the known to the unknown.

## Professional Extraction Techniques
*   **Disambiguation**: Use unique IDs for entities that might have similar names (e.g., `sqlite-database` vs `mysql-database`).
*   **Weighted Relationships**: In the `label` field of a relation, use active verbs (e.g., "implements", "manages", "defines", "is a subset of").
*   **Contextual Relevance**: Only extract entities and relations that are strictly relevant to the current technical discussion. Avoid extracting "conversational filler".

## Workflow
1.  **Step 1: Ingest** - Analyze the user query and previous context.
2.  **Step 2: Lookup** - Check `existing_terms` for overlaps.
3.  **Step 3: Structure** - Map out the 3-layer hierarchy (Core -> Primary -> Detail).
4.  **Step 4: Serialize** - Produce the final JSON response.
