# BPMN Diagrams in Syncfusion React Diagram

## Table of Contents
- [Overview](#overview)
- [Module Setup](#module-setup)
- [Events](#events)
- [Activities (Tasks and Subprocesses)](#activities-tasks-and-subprocesses)
- [Gateways](#gateways)
- [Flows (Connectors)](#flows-connectors)
- [Data Objects and Data Sources](#data-objects-and-data-sources)
- [BPMN Groups](#bpmn-groups)
- [Text Annotations](#text-annotations)
- [Complete Example](#complete-example)
- [Shape Reference](#shape-reference)
- [Troubleshooting](#troubleshooting)

---

## Overview

BPMN (Business Process Model and Notation) is the standard for modeling business processes visually. The diagram uses standardized shapes to represent events, activities, gateways, and data flow so that any stakeholder can read and understand the process.

Inject the `BpmnDiagrams` module to enable BPMN shapes.

---

## Module Setup

```tsx
import { BpmnDiagrams, DiagramComponent, Inject, NodeModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'startEvent',
    offsetX: 100, offsetY: 200,
    width: 60, height: 60,
    shape: {
      type: 'Bpmn',
      shape: 'Event',
      event: { event: 'Start', trigger: 'None' }
    }
  },
];

export default function App() {
  return (
       <DiagramComponent id="bpmn" width={'100%'} height={'600px'} nodes={nodes}>
      <Inject services={[BpmnDiagrams]} />
    </DiagramComponent>
  );
}
```

---

## Events

Events are circles that mark the start, middle, or end of a process. Set `shape.shape: 'Event'` and configure `event.event` and `event.trigger`.

### Event types

| `event.event` | Description |
|--------------|-------------|
| `'Start'` | Process begins here |
| `'Intermediate'` | Catching event in the middle of a flow |
| `'NonInterruptingStart'` | Non-interrupting start (dashed border) |
| `'NonInterruptingIntermediate'` | Non-interrupting intermediate |
| `'ThrowingIntermediate'` | Throwing event |
| `'End'` | Process terminates here |

### Event trigger types

`'None'` | `'Message'` | `'Timer'` | `'Error'` | `'Escalation'` | `'Signal'` | `'Link'` | `'Cancel'` | `'Compensation'` | `'Terminate'` | `'Conditional'` | `'Multiple'` | `'ParallelMultiple'`

```tsx
const nodes: NodeModel[] = [
  {
    id: 'startEvent',
    offsetX: 100, offsetY: 200,
    width: 60, height: 60,
    shape: {
      type: 'Bpmn',
      shape: 'Event',
      event: { event: 'Start', trigger: 'None' }
    }
  },
  {
    id: 'timerEvent',
    offsetX: 250, offsetY: 200,
    width: 60, height: 60,
    shape: {
      type: 'Bpmn',
      shape: 'Event',
      event: { event: 'Intermediate', trigger: 'Timer' }
    }
  },
  {
    id: 'endEvent',
    offsetX: 400, offsetY: 200,
    width: 60, height: 60,
    shape: {
      type: 'Bpmn',
      shape: 'Event',
      event: { event: 'End', trigger: 'None' }
    }
  }
];
```

---

## Activities (Tasks and Subprocesses)

Activities represent work. Set `shape.shape: 'Activity'` and configure `activity.activity`.

### Task

```tsx
const nodes: NodeModel[] = [
  {
    id: 'userTask',
    offsetX: 250, offsetY: 200,
    width: 120, height: 60,
    annotations: [{ content: 'Approve Request' }],
    shape: {
      type: 'Bpmn',
      shape: 'Activity',
      activity: {
        activity: 'Task',
        task: {
          type: 'User',    // 'None' | 'User' | 'Service' | 'Manual' | 'BusinessRule' | 'Send' | 'Receive' | 'Script'
          loop: 'None',    // 'None' | 'Standard' | 'ParallelMultiInstance' | 'SequenceMultiInstance'
        }
      }
    }
  }
];
```

### Subprocess

```tsx
const nodes: NodeModel[] = [
  {
    id: 'sub1',
    offsetX: 300, offsetY: 300,
    width: 200, height: 120,
    shape: {
      type: 'Bpmn',
      shape: 'Activity',
      activity: {
        activity: 'SubProcess',
        subProcess: {
          collapsed: true,            // show as collapsed (box with + marker)
          type: 'Transaction',        // 'None' | 'Transaction' | 'EventSubProcess'
          loop: 'None'
        }
      }
    }
  }
];
```

---

## Gateways

Gateways are diamond shapes that represent decision points. Set `shape.shape: 'Gateway'` and configure `gateway.type`.

| `gateway.type` | Symbol | Description |
|---------------|--------|-------------|
| `'None'` | Empty diamond | Unspecified gateway |
| `'Exclusive'` | X | Only one path proceeds |
| `'Inclusive'` | Circle | One or more paths proceed |
| `'Parallel'` | + | All paths proceed simultaneously |
| `'Complex'` | * | Complex conditions |
| `'EventBased'` | Circle+pentagon | Next event determines path |
| `'ExclusiveEventBased'` | Variant | Event-based exclusive |
| `'ParallelEventBased'` | + variant | Event-based parallel |

```tsx
const nodes: NodeModel[] = [
  {
    id: 'gateway1',
    offsetX: 350, offsetY: 200,
    width: 60, height: 60,
    annotations: [{ content: 'Approved?', offset: { x: 0.5, y: 1.3 } }],
    shape: {
      type: 'Bpmn',
      shape: 'Gateway',
      gateway: { type: 'Exclusive' }
    }
  }
];
```

---

## Flows (Connectors)

BPMN uses three types of flows between elements, all set via connector `shape.type: 'Bpmn'`:

### Sequence flow (execution order)

```tsx
const connectors: ConnectorModel[] = [
  {
    id: 'seq1',
    sourceID: 'startEvent', targetID: 'userTask',
    type: 'Orthogonal',
    shape: {
      type: 'Bpmn',
      flow: 'Sequence',
      sequence: 'Normal'   // 'Normal' | 'Default' | 'Conditional'
    }
  }
];
```

### Message flow (communication between pools)

```tsx
const connectors: ConnectorModel[] = [
  {
    id: 'msg1',
    sourcePoint: { x: 100, y: 100 }, targetPoint: { x: 300, y: 200 },
    type: 'Orthogonal',
    shape: {
      type: 'Bpmn',
      flow: 'Message',
      message: 'InitiatingMessage'   // 'Default' | 'InitiatingMessage' | 'NonInitiatingMessage'
    }
  }
];
```

### Association flow (links to text annotations)

```tsx
const connectors: ConnectorModel[] = [
  {
    id: 'assoc1',
    sourcePoint: { x: 200, y: 100 }, targetPoint: { x: 300, y: 200 },
    type: 'Orthogonal',
    shape: {
      type: 'Bpmn',
      flow: 'Association',
      association: 'Directional'   // 'Default' | 'Directional' | 'BiDirectional'
    }
  }
];
```

---

## Data Objects and Data Sources

### Data object

```tsx
const nodes: NodeModel[] = [
  {
    id: 'data1',
    offsetX: 400, offsetY: 150,
    width: 50, height: 70,
    annotations: [{ content: 'Order Form', offset: { x: 0.5, y: 1.3 } }],
    shape: {
      type: 'Bpmn',
      shape: 'DataObject',
      dataObject: {
        type: 'None',    // 'None' | 'Input' | 'Output'
        collection: false
      }
    }
  }
];
```

### Data source (database)

```tsx
const nodes: NodeModel[] = [
  {
    id: 'db1',
    offsetX: 500, offsetY: 300,
    width: 70, height: 70,
    annotations: [{ content: 'Customer DB', offset: { x: 0.5, y: 1.3 } }],
    shape: { type: 'Bpmn', shape: 'DataSource' }
  }
];
```

---

## BPMN Groups

BPMN groups visually bracket related elements without affecting the flow logic.

```tsx
const nodes: NodeModel[] = [
  {
    id: 'group1',
    offsetX: 300, offsetY: 200,
    width: 250, height: 150,
    shape: { type: 'Bpmn', shape: 'Group' }
  }
];
```

---

## Text Annotations

Text annotations add explanatory notes attached to flow elements via association connectors.

```tsx
const nodes: NodeModel[] = [
  {
    id: 'note1',
    offsetX: 500, offsetY: 100,
    width: 120, height: 50,
    shape: {
      type: 'Bpmn',
      shape: 'TextAnnotation',
      textAnnotation:{ textAnnotationDirection:'Auto',textAnnotationTarget:''}
    }
  }
];

// Connect with association flow
const connectors: ConnectorModel[] = [
  {
    id: 'a1',
    sourceID: 'userTask', targetID: 'note1',
    shape: { type: 'Bpmn', flow: 'Association', association: 'Directional' }
  }
];
```

---

## Complete Example

A minimal approval workflow:

```tsx
import { Diagram, DiagramComponent, Inject, NodeModel, ConnectorModel, BpmnDiagrams } from '@syncfusion/ej2-react-diagrams';

Diagram.Inject(BpmnDiagrams);

const nodes: NodeModel[] = [
  { id: 'start',   offsetX: 80,  offsetY: 200, width: 50,  height: 50,
    shape: { type: 'Bpmn', shape: 'Event', event: { event: 'Start', trigger: 'None' } } },
  { id: 'review',  offsetX: 250, offsetY: 200, width: 120, height: 60,
    annotations: [{ content: 'Review' }],
    shape: { type: 'Bpmn', shape: 'Activity', activity: { activity: 'Task', task: { type: 'User' } } } },
  { id: 'approve', offsetX: 430, offsetY: 200, width: 60,  height: 60,
    annotations: [{ content: 'Approved?', offset: { x: 0.5, y: 1.4 } }],
    shape: { type: 'Bpmn', shape: 'Gateway', gateway: { type: 'Exclusive' } } },
  { id: 'end',     offsetX: 580, offsetY: 200, width: 50,  height: 50,
    shape: { type: 'Bpmn', shape: 'Event', event: { event: 'End', trigger: 'None' } } }
];

const connectors: ConnectorModel[] = [
  { id: 'c1', sourceID: 'start',  targetID: 'review',  type: 'Orthogonal',
    shape: { type: 'Bpmn', flow: 'Sequence', sequence: 'Normal' } },
  { id: 'c2', sourceID: 'review', targetID: 'approve', type: 'Orthogonal',
    shape: { type: 'Bpmn', flow: 'Sequence', sequence: 'Normal' } },
  { id: 'c3', sourceID: 'approve', targetID: 'end',    type: 'Orthogonal',
    annotations: [{ content: 'Yes' }],
    shape: { type: 'Bpmn', flow: 'Sequence', sequence: 'Conditional' } }
];

export default function App() {
  return (
    <DiagramComponent id="bpmn" width={'100%'} height={'400px'} nodes={nodes} connectors={connectors}>
      <Inject services={[BpmnDiagrams]} />
    </DiagramComponent>
  );
}
```

---

## Shape Reference

| `shape.shape` | Type | Use |
|--------------|------|-----|
| `'Event'` | Node | Start, Intermediate, End with triggers |
| `'Activity'` | Node | Task, SubProcess |
| `'Gateway'` | Node | Exclusive, Inclusive, Parallel etc. |
| `'DataObject'` | Node | Input/Output data |
| `'DataSource'` | Node | Database/data store |
| `'Group'` | Node | Grouping boundary |
| `'TextAnnotation'` | Node | Explanatory note |
| `'Message'` | Node | Message indicator |

---

## Troubleshooting

**BPMN shapes not rendering**
- Confirm `<Inject services={[BpmnDiagrams]} />` is a child of `<DiagramComponent>`

**Connector flow decorators look wrong**
- Verify `shape.type: 'Bpmn'` and `shape.flow` is `'Sequence'`, `'Association'`, or `'Message'`

**Gateway not showing type icon**
- Set `gateway.type` explicitly; default is `'None'` (empty diamond)

**Related docs:**
- Shapes & Styles → [shapes-and-styles.md](shapes-and-styles.md)
- Connectors → [connectors.md](connectors.md)
