---
name: robust-agent-design
description: Apply robust Agent design patterns for building fault-tolerant, state-driven automation systems. Use when designing or refactoring systems that require high reliability, error recovery, graceful degradation, and distributed component coordination. Triggers on requests involving Agent architecture, fault tolerance design, state management, retry mechanisms, compensation transactions, or system robustness improvements.
---

# Robust Agent Design Patterns

A design methodology based on loose coupling, state-driven architecture, and fault-tolerance-first principles.

## Core Design Principles

### 1. Node-Based vs Function-Based
- Each functional unit is encapsulated as an independent Agent
- Agents communicate via messages/state rather than function calls
- Each Agent has its own lifecycle and state management

### 2. State-Driven vs Flow-Driven
- System state is explicitly stored and managed
- Decisions are based on state rather than hardcoded flows
- Supports checkpoint recovery and state restoration

### 3. Fault-Tolerance-First vs Success-First
- Assume all components can fail
- Design recovery strategies for each failure scenario
- "Failure is the norm, success requires guarantees"

## Three-Level Fault Handling Mechanism

| Level | Fault Type | Handling Strategy | Applicable Scenarios |
|-------|------------|-------------------|---------------------|
| **L1** | Transient Fault | Auto-retry + Exponential Backoff | Network jitter, API rate limiting, temporary unavailability |
| **L2** | Resource Fault | Resource cleanup + State reset | Disk space exhausted, memory overflow, connection pool depleted |
| **L3** | Logic Fault | Human intervention + Compensation | Data inconsistency, business logic errors, external dependency failures |

## Agent Design Template

### Basic Agent Class Structure

```python
class RobustAgent:
    def __init__(self, config):
        self.id = generate_uuid()
        self.state = 'initialized'  # initialized|waiting|processing|completed|failed
        self.input_queue = []
        self.output_queue = []
        self.retry_count = 0
        self.max_retries = config.get('max_retries', 3)
        self.compensation_actions = config.get('compensation_actions', [])
        self.state_persistence = config.get('state_persistence', 'file')  # file|db|memory
    
    async def execute(self, task):
        """Main execution entry point"""
        try:
            # 1. State transition
            self.state = 'processing'
            self._persist_state()
            
            # 2. Execute work
            result = await self._do_work(task)
            
            # 3. Validate result
            await self._validate_result(result)
            
            # 4. Complete state
            self.state = 'completed'
            self._persist_state()
            return result
            
        except Exception as error:
            # 5. Fault handling
            return await self._handle_failure(error, task)
    
    async def _handle_failure(self, error, task):
        """Fault handling logic"""
        # L1: Transient fault - retry
        if self._is_transient_error(error) and self.retry_count < self.max_retries:
            self.retry_count += 1
            await self._exponential_backoff(self.retry_count)
            return await self.execute(task)
        
        # L2: Resource fault - cleanup and reset
        if self._is_resource_error(error):
            await self._cleanup_resources()
            self.state = 'waiting'
            self._persist_state()
            raise ResourceExhaustedError(f"Resource fault: {error}")
        
        # L3: Logic fault - compensation
        self.state = 'failed'
        self._persist_state()
        await self._execute_compensation()
        raise BusinessLogicError(f"Logic fault: {error}")
    
    def _persist_state(self):
        """State persistence"""
        state_data = {
            'agent_id': self.id,
            'state': self.state,
            'retry_count': self.retry_count,
            'timestamp': datetime.now().isoformat()
        }
        # Persist to file/database based on configuration
        save_state(state_data, self.state_persistence)
```

### State Management Protocol

```json
{
  "agent_id": "uuid",
  "current_state": "waiting_for_input|processing|completed|failed",
  "input_state": {
    "data": {},
    "checksum": "md5_hash",
    "source": "previous_agent_id",
    "timestamp": "iso8601"
  },
  "output_state": {
    "data": {},
    "quality_metrics": {},
    "validation_status": "passed|failed",
    "next_step": "agent_id_to_notify"
  },
  "retry_info": {
    "count": 0,
    "max_retries": 3,
    "backoff_strategy": "exponential"
  }
}
```

## Compensation Transaction Pattern

### Compensation Chain

```python
class CompensationChain:
    def __init__(self):
        self.actions = []
    
    def add_action(self, action_func, params, rollback_func=None):
        self.actions.append({
            'action': action_func,
            'params': params,
            'rollback': rollback_func
        })
    
    async def execute(self):
        executed = []
        try:
            for action in self.actions:
                result = await action['action'](**action['params'])
                executed.append(action)
            return True
        except Exception as e:
            # Rollback executed actions
            for action in reversed(executed):
                if action['rollback']:
                    await action['rollback'](**action['params'])
            raise CompensationError(f"Compensation failed: {e}")
```

### Usage Example

```python
# Compensation after email sending failure
class MailAgent(RobustAgent):
    async def send_with_compensation(self, email_data):
        try:
            result = await mail_service.send(email_data)
            return result
        except Exception as error:
            compensation = CompensationChain()
            compensation.add_action(
                log_failure, 
                {'error': error, 'email': email_data}
            )
            compensation.add_action(
                notify_monitoring,
                {'severity': 'warning', 'agent_id': self.id}
            )
            compensation.add_action(
                queue_for_retry,
                {'email': email_data, 'delay': 300}
            )
            compensation.add_action(
                fallback_to_sms,
                {'summary': email_data.subject, 'recipient': email_data.to}
            )
            await compensation.execute()
            raise
```

## Graceful Degradation Strategies

```python
DEGRADATION_STRATEGIES = {
    "primary_service_unavailable": {
        "primary": "wait_and_retry",
        "fallback": "use_backup_service",
        "final": "queue_for_manual_processing"
    },
    "resource_exhausted": {
        "primary": "clean_temp_files",
        "fallback": "compress_existing_data",
        "final": "pause_until_manual_cleanup"
    },
    "quality_threshold_not_met": {
        "primary": "retry_with_different_params",
        "fallback": "use_simplified_algorithm",
        "final": "flag_for_human_review"
    }
}
```

## System Architecture Patterns

### Basic Architecture

```
┌─────────────────────────────────────────┐
│           Orchestrator                  │
│  ┌─────┬─────┬─────┬─────┬─────┐       │
│  │Collect│Process│Report│Send│Monitor│  │
│  │Agent  │Agent  │Agent │Agent│Agent │  │
│  └─────┴─────┴─────┴─────┴─────┘       │
└─────────────────────────────────────────┘
         ↓         ↓         ↓
    [State Store] [Message Queue] [Monitoring Log]
```

### Agent Collaboration Flow

```
Input → Agent A → [State A] → Agent B → [State B] → Agent C → Output
         ↓ Failure          ↓ Failure          ↓ Failure
    [Compensation]    [Retry/Degrade]    [Human Intervention]
```

## Implementation Checklist

### Each Agent Must Include
- [ ] Unique identifier (UUID)
- [ ] Clear input/output interface definitions
- [ ] Built-in result validation mechanism
- [ ] State persistence capability
- [ ] Fault recovery logic (three-level handling)
- [ ] Monitoring metrics reporting
- [ ] Logging and tracing integration

### System-Level Guarantees
- [ ] At-least-once message delivery guarantee
- [ ] Eventual state consistency guarantee
- [ ] Data integrity verification (checksum)
- [ ] Operation traceability (full-link tracing)
- [ ] Performance monitoring and alerting

## Application Scenarios

### Scenario 1: Information Collection System
```
CrawlerAgent → ClassifierAgent → ReporterAgent → MailerAgent
     ↓               ↓                ↓              ↓
 [State:Collecting][State:Classifying][State:Generating][State:Sending]
```

### Scenario 2: Data Analysis Pipeline
```
DataFetcherAgent → CleanerAgent → AnalyzerAgent → VisualizationAgent
```

### Scenario 3: Automation Workflow
```
TriggerAgent → ApprovalAgent → ExecutorAgent → NotifyAgent
```

## Best Practices

### 1. Interface Design
- Interfaces are stable and backward compatible
- Versioned API design (v1, v2)
- Clear error code system

### 2. State Management
- State storage separated from business logic
- Support for snapshots and rollback
- State change audit tracking

### 3. Testing Strategy
- Unit tests: Individual Agent functionality
- Integration tests: Agent collaboration
- Chaos engineering: Fault injection testing

### 4. Observability
- Each Agent reports health status
- Real-time monitoring of key metrics
- Full link tracing coverage

## Anti-Pattern Warnings

### ❌ Don't Do This
- Design Agents as pure functions without state management
- Ignore failure scenarios, assume everything works
- Hardcode flows that cannot be dynamically adjusted
- Lack compensation mechanisms, fail and terminate immediately

### ✅ Do This Instead
- Explicitly manage state and lifecycle
- Design recovery strategies for each failure scenario
- Make decisions based on state, support dynamic flows
- Implement compensation transactions, support graceful degradation

## Reference Implementation

See `references/` directory:
- `agent_template.py` - Complete Agent template
- `compensation_example.py` - Compensation transaction examples
