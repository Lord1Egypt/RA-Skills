# UML Diagrams in Syncfusion React Diagram

## Table of Contents
- [UML Class Diagrams](#uml-class-diagrams)
- [Class Shape](#class-shape)
- [Interface Shape](#interface-shape)
- [Enumeration Shape](#enumeration-shape)
- [UML Class Relationships](#uml-class-relationships)
- [UML Sequence Diagrams](#uml-sequence-diagrams)
- [Sequence Diagram Participants](#sequence-diagram-participants)
- [Sequence Diagram Messages](#sequence-diagram-messages)
- [Advanced Properties](#advanced-properties)
- [Troubleshooting](#troubleshooting)

---

## UML Class Diagrams

UML Class Diagrams model the static structure of a system using classes, interfaces, enumerations, and their relationships. Set `shape.type: 'UmlClassifier'` and configure the `classifier` property to select the element type.

No additional module injection is required for UML Class Diagrams — they work out of the box.

---

## Class Shape

A class has a name, attributes (fields), and methods.

```tsx
import { DiagramComponent, NodeModel, UmlClassifierShapeModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'OrderClass',
    offsetX: 200, offsetY: 250,
    style: { fill: '#26A0DA', strokeColor: '#1a6fa0' },
    shape: {
      type: 'UmlClassifier',
      classifier: 'Class',
      classShape: {
        name: 'Order',
        attributes: [
          { name: 'id',          type: 'int',    scope: 'Private' },
          { name: 'customerName', type: 'string', scope: 'Public' },
          { name: 'total',       type: 'double', scope: 'Protected' }
        ],
        methods: [
          {
            name: 'placeOrder',
            type: 'void',
            scope: 'Public',
            parameters: [
              { name: 'customerId', type: 'int' }
            ]
          },
          { name: 'cancel', type: 'bool', scope: 'Public' }
        ]
      }
    } as UmlClassifierShapeModel
  }
];

export default function App() {
  return (
    <DiagramComponent id="diagram" width={'100%'} height={'600px'} nodes={nodes} />
  );
}
```

### Scope (visibility) values

`'Public'` (+) | `'Private'` (-) | `'Protected'` (#) | `'Package'` (~)

---

## Interface Shape

An interface declares a contract: method signatures without implementation details.

```tsx
const nodes: NodeModel[] = [
  {
    id: 'PaymentInterface',
    offsetX: 450, offsetY: 250,
    style: { fill: '#26A0DA' },
    shape: {
      type: 'UmlClassifier',
      classifier: 'Interface',
      interfaceShape: {
        name: 'IPayment',
        attributes: [
          { name: 'amount', type: 'double', scope: 'Public' }
        ],
        methods: [
          {
            name: 'process',
            type: 'bool',
            scope: 'Public',
            parameters: [{ name: 'amount', type: 'double' }]
          },
          { name: 'refund', type: 'void', scope: 'Public' }
        ]
      }
    } as UmlClassifierShapeModel
  }
];
```

---

## Enumeration Shape

An enumeration defines a fixed set of named constants.

```tsx
const nodes: NodeModel[] = [
  {
    id: 'StatusEnum',
    offsetX: 300, offsetY: 450,
    style: { fill: '#26A0DA' },
    shape: {
      type: 'UmlClassifier',
      classifier: 'Enumeration',
      enumerationShape: {
        name: 'OrderStatus',
        members: [
          { name: 'Pending' },
          { name: 'Processing' },
          { name: 'Shipped' },
          { name: 'Delivered' },
          { name: 'Cancelled' }
        ]
      }
    } as UmlClassifierShapeModel
  }
];
```

---

## UML Class Relationships

Relationships between classes are modeled as connectors with `shape.type: 'UmlClassifier'` and a `relationship` property.

### Relationship types and connector decorators

| `relationship` | Decorator | Description |
|---------------|-----------|-------------|
| `'Association'` | Arrow | General relationship |
| `'Aggregation'` | Hollow diamond at source | Has-A (weak ownership) |
| `'Composition'` | Filled diamond at source | Has-A (strong ownership) |
| `'Inheritance'` | Open triangle at target | Is-A (extends) |
| `'Dependency'` | Dashed arrow | Uses-A |
| `'Realization'` | Dashed open triangle | Implements |

```tsx
import { ConnectorModel } from '@syncfusion/ej2-react-diagrams';

const connectors: ConnectorModel[] = [
  // Inheritance: OrderClass extends BaseEntity
  {
    id: 'inherit1',
    sourceID: 'OrderClass', targetID: 'BaseEntity',
    type: 'Straight',
    shape: {
      type: 'UmlClassifier',
      relationship: 'Inheritance'
    }
  },
  // Aggregation: Order has many Items
  {
    id: 'agg1',
    sourceID: 'OrderClass', targetID: 'ItemClass',
    type: 'Straight',
    shape: {
      type: 'UmlClassifier',
      relationship: 'Aggregation'
    }
  },
  // Realization: PaymentService implements IPayment
  {
    id: 'real1',
    sourceID: 'PaymentService', targetID: 'PaymentInterface',
    type: 'Straight',
    shape: {
      type: 'UmlClassifier',
      relationship: 'Realization'
    }
  },
  // Directional Association
  {
    id: 'assoc1',
    sourceID: 'OrderClass', targetID: 'CustomerClass',
    type: 'Straight',
    shape: {
      type: 'UmlClassifier',
      relationship: 'Association',
      association: 'Directional'   // 'Directional' | 'BiDirectional'
    }
  }
];
```

---

## UML Sequence Diagrams

UML Sequence Diagrams model how objects interact over time through a series of messages. Use the `model` prop on `DiagramComponent` with a `UmlSequenceDiagramModel` object.

```tsx
import { DiagramComponent, SnapConstraints } from '@syncfusion/ej2-react-diagrams';
import { UmlSequenceDiagramModel } from '@syncfusion/ej2-diagrams';

const umlSequenceDiagramModel: UmlSequenceDiagramModel = {
  participants: [...],
  messages: [...]
};

export default function App() {
  return (
    <DiagramComponent
      id="seqDiagram"
      width={'100%'} height={'600px'}
      model={umlSequenceDiagramModel}
      snapSettings={{ constraints: SnapConstraints.None }}
    />
  );
}
```

---

## Sequence Diagram Participants

Participants appear as boxes at the top with vertical lifelines. Set `isActor: true` for human users.

```tsx
const umlSequenceDiagramModel: UmlSequenceDiagramModel = {
  participants: [
    {
      id: 'User',
      content: 'Customer',
      isActor: true                  // displays stick figure
    },
    {
      id: 'WebServer',
      content: 'Web Server',
      isActor: false,
      showDestructionMarker: false   // X marker at lifeline end
    },
    {
      id: 'Database',
      content: 'Database',
      isActor: false,
      showDestructionMarker: true    // shows destruction marker
    }
  ]
};
```

---

## Sequence Diagram Messages

Messages are arrows between lifelines showing communication. Configure in the `messages` array.

```tsx

import {UmlSequenceMessageType } from "@syncfusion/ej2-diagrams";

const umlSequenceDiagramModel: UmlSequenceDiagramModel = {
  participants: [
    { id: 'User',    content: 'Customer', isActor: true },
    { id: 'Server',  content: 'Server' },
    { id: 'DB',      content: 'Database' }
  ],
  messages: [
    {
      id: 'msg1',
      fromParticipantID: 'User',
      toParticipantID: 'Server',
      content: 'POST /orders',
      type: UmlSequenceMessageType.Synchronous   // 'Synchronous' | 'Asynchronous' | 'Reply' | 'Create' | 'Delete' | 'SelfMessage'
    },
    {
      id: 'msg2',
      fromParticipantID: 'Server',
      toParticipantID: 'DB',
      content: 'INSERT order',
      type: UmlSequenceMessageType.Synchronous
    },
    {
      id: 'msg3',
      fromParticipantID: 'DB',
      toParticipantID: 'Server',
      content: 'OK',
      type: UmlSequenceMessageType.Reply
    },
    {
      id: 'msg4',
      fromParticipantID: 'Server',
      toParticipantID: 'User',
      content: '201 Created',
      type: UmlSequenceMessageType.Reply
    }
  ]
};
```

---

## Advanced Properties

### UML Class node properties

| Property | Type | Description |
|----------|------|-------------|
| `classifier` | `'Class' \| 'Interface' \| 'Enumeration'` | Shape type |
| `classShape.name` | `string` | Class name (header) |
| `classShape.attributes` | `UmlClassAttributeModel[]` | Field list |
| `classShape.methods` | `UmlClassMethodModel[]` | Method list |
| `interfaceShape` | `UmlInterfaceModel` | Interface config |
| `enumerationShape.members` | `UmlEnumerationMemberModel[]` | Enum values |

### UML Attribute / Method properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `string` | Field/method name |
| `type` | `string` | Data type or return type |
| `scope` | `'Public' \| 'Private' \| 'Protected' \| 'Package'` | Visibility |
| `parameters` | `UmlClassMethodParametersModel[]` | Method parameters (methods only) |

### UML Class relationship values

`'Association'` | `'Aggregation'` | `'Composition'` | `'Inheritance'` | `'Dependency'` | `'Realization'`

### UML Sequence message types

`'Synchronous'` | `'Asynchronous'` | `'Reply'` | `'Create'` | `'Delete'` | `'SelfMessage'`

---

## Troubleshooting

**Class shape not displaying attributes/methods**
- Confirm `classifier` matches the shape config key: `'Class'` → `classShape`, `'Interface'` → `interfaceShape`, `'Enumeration'` → `enumerationShape`

**Relationship decorator not showing**
- Ensure connector `shape.type: 'UmlClassifier'` and `relationship` is set to a valid value

**Sequence diagram not rendering**
- Use the `model` prop (not `nodes`/`connectors`) to pass `UmlSequenceDiagramModel`
- Import `UmlSequenceDiagramModel` from `'@syncfusion/ej2-diagrams'` (not the react package)

**Scope symbols not appearing**
- Check `scope` is capitalized exactly: `'Public'`, `'Private'`, `'Protected'`, `'Package'`

**Related docs:**
- Shapes & Styles → [shapes-and-styles.md](shapes-and-styles.md)
- BPMN Diagrams → [bpmn-diagrams.md](bpmn-diagrams.md)
- Data Binding → [data-binding.md](data-binding.md)
