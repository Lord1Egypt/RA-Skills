# UML Modeling in RSAD

RSAD supports the full UML 2.x specification via an Eclipse-based graphical editor. In FTM
development, specific diagram types are used for specific design purposes.

---

## Diagram Types Used in FTM

### Use Case Diagram
**FTM Purpose:** High-level functional view of a new interface — who sends/receives, what FTM
facilitates, which existing SPs are involved.

Key elements:
- **Actors**: External systems, internal FTM services, operators
- **Use Cases**: Interface capabilities (e.g., "Process Inbound Payment", "Send Acknowledgement")
- **Include/Extend relationships**: Shared sub-use cases (e.g., error handling, logging)
- **System boundary**: Draw FTM as the boundary enclosing all use cases

Typical FTM use case diagram contains:
- Sending bank actor → "Submit Payment" use case
- FTM system boundary with: Receive Payment, Validate, Route, Send Confirmation
- Receiving bank actor ← "Deliver Payment" use case
- Operator actor ← "Resolve Alert" use case

---

### Sequence Diagram
**FTM Purpose:** Shows the message flow and interactions between FTM components and external
systems in time order. Two types are used:

**Functional Sequence Diagram** (high-level):
- Lifelines: External System, PT Flow, MQ Event Queue, EP Flow, Action Subflow, External System
- Shows: message arrival → PT flow processing → ISF creation → event raising → EP processing →
  FSM action → outbound message
- Captures the happy path and key error paths

**Service Interaction Diagram** (technical detail):
- Lifelines: ACE integration server components, DB2, MQ queues
- Shows: DB2 reads/writes, MQ put/get operations, mapper invocations
- Used to validate implementation against design

Standard sequence for inbound payment (Pattern 9.1):
```
ExternalSystem → PTFlow: Raw message (MQ/HTTP)
PTFlow → Mapper: Map to ISF
Mapper → PTFlow: ISF document
PTFlow → DB2: INSERT Transmission + Transaction rows
PTFlow → MQEventQueue: PUT E_MpInMappingComplete event
MQEventQueue → EPFlow: GET event
EPFlow → DB2: SELECT FSM transitions
EPFlow → ActionSubflow: Execute action
ActionSubflow → DB2: UPDATE object state
ActionSubflow → OutboundMQ: PUT outbound message
```

---

### State Machine Diagram (FSM)
**FTM Purpose:** This is the most critical RSAD artifact in FTM. It defines the lifecycle of a
Transaction or Transmission object. RSAD exports this directly to DB2 SQL.

See `fsm-design.md` for full details on states, transitions, events, and stereotypes.

---

### Class Diagram
**FTM Purpose:** Models the Service Participant configuration — attributes, channels, mapper
references, and relationships between SPs.

Key elements for FTM:
- **SP Class**: One class per Service Participant; attributes include SP name, type, role
- **Channel Class**: One per channel; attributes include format, transport, mapper class, queue names
- **Relationships**: SP has-many Channels; Channel references Mapper
- **Tagged values**: Transport endpoint (queue name, URL), format identifier, mapper reference

SP class attributes:
```
ServiceParticipant
  - name: String         // DB2 SERVICE_PARTICIPANT_BASE.SP_NAME
  - type: String         // e.g., BANK, INTERNAL
  - role: String         // e.g., DEBTOR_AGENT, CREDITOR_AGENT
  - status: String       // ACTIVE / INACTIVE
```

Channel attributes:
```
Channel
  - channelName: String
  - format: String       // e.g., SWIFT_MT103, ISO20022_PACS008
  - mapper: String       // ACE subflow name
  - inputQueue: String   // MQ queue name
  - outputQueue: String
  - transport: String    // MQ / HTTP / FILE
```

---

### Activity Diagram
**FTM Purpose:** Models the internal logic of a mapper or action subflow — decision points,
parallel paths, loops. Used when the logic is too complex to capture in a sequence diagram.

Elements:
- Initial/final nodes, actions, decisions, forks/joins, swim lanes
- Swim lanes map to: ESQL module, Java class, external service call

---

### Component Diagram
**FTM Purpose:** Shows the ACE application/library structure and dependencies. Maps RSAD design
to actual ACE project structure.

Typical FTM component diagram:
- FTM_PT_Application → depends on → FTM_Library (shared subflows)
- FTM_EP_Application → depends on → FTM_Actions_Library
- Mapper_Application → depends on → ISF_Schema_Library

---

### Deployment Diagram
**FTM Purpose:** Shows where ACE integration nodes, integration servers, MQ queue managers, DB2,
and WAS run — and how they connect.

Elements for FTM:
- Integration Node (ACE broker)
- Integration Servers (execution groups): PT_Server, EP_Server, Action_Server
- MQ Queue Manager with queue names
- DB2 instance
- WAS node (hosting OAC)
- External system endpoints (banks, clearinghouses)

---

## UML Profile Application

RSAD profiles extend UML with domain-specific stereotypes. In FTM, always apply the FTM UML
Profile before modeling FSMs.

To apply a profile in RSAD:
1. Right-click the UML model → Properties → Profiles
2. Add the FTM profile (available in the RSAD FTM plugin)
3. Stereotypes become available in the state machine diagram palette

---

## RSAD Workspace Organization

```
RSA Workspace/
├── FTM_Design/                  # Master design project
│   ├── UseCases/                # Use case diagrams per interface
│   ├── SequenceDiagrams/        # Functional + technical sequences
│   ├── FSMs/                    # State machine models
│   │   ├── Transaction_FSMs/
│   │   └── Transmission_FSMs/
│   ├── ServiceParticipants/     # SP + Channel class models
│   └── Deployment/              # Deployment topology diagrams
├── FTM_Config/                  # Generated SQL export directory
│   ├── sp_config.sql
│   ├── channel_config.sql
│   ├── fsm_config.sql
│   └── event_type_config.sql
└── FTM_Profiles/                # FTM UML profile definitions
```

---

## Common RSAD Operations

### Creating a new State Machine
1. New → UML Model → State Machine Diagram
2. Apply FTM UML Profile to the model
3. Add Initial pseudostate
4. Add states; apply `PMP_Alert` / `PMP_Terminal` stereotypes as needed
5. Add transitions; set Event, Guard (Object Filter), and Effect (FSM Action = ACE subflow name)
6. Add Final state for each terminal path
7. Right-click model → Transform → Export to SQL

### Exporting SQL from RSAD
1. Select the SP/Channel/FSM model(s) to export
2. Right-click → IBM FTM → Export Configuration
3. Choose output directory (FTM_Config/)
4. Review generated SQL before loading to DB2:
   - `INSERT INTO FSM` — FSM root record
   - `INSERT INTO FSM_STATE_REL` — state records
   - `INSERT INTO FSM_TRANSITION` — transition rules
   - `INSERT INTO SERVICE_PARTICIPANT_BASE` — SP records
   - `INSERT INTO CHANNEL_BASE` — channel records

### Editing an existing model
1. Open the model in RSAD (`.emx` or `.uml` file)
2. Navigate to the specific diagram
3. Make changes — add states, modify transition events, update channel attributes
4. Re-export SQL (generates new INSERT scripts; apply delta to DB2)
5. Commit `.emx` / `.uml` files and updated SQL to version control
