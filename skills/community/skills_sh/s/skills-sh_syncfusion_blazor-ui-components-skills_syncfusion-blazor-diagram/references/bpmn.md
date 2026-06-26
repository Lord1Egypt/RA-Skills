# BPMN Shapes in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [BPMN Events](#bpmn-events)
- [BPMN Activities (Tasks and Subprocesses)](#bpmn-activities-tasks-and-subprocesses)
- [BPMN Gateways](#bpmn-gateways)
- [BPMN Data Objects and Data Stores](#bpmn-data-objects-and-data-stores)
- [BPMN Connectors](#bpmn-connectors)
- [BPMN Text Annotation](#bpmn-text-annotation)
- [Expanded Sub-Process](#expanded-sub-process)
- [Common Gotchas](#common-gotchas)

---

## Overview

BPMN (Business Process Model and Notation) shapes model business processes visually. Use `BpmnActivity`, `BpmnEvent`, `BpmnGateway`, etc. as a node's `Shape` property.

---

## BPMN Events

Events represent things that happen during a process (start, end, intermediate):

```razor
@using Syncfusion.Blazor.Diagram

<SfDiagramComponent Height="600px" Nodes="@nodes" />

@code {
    DiagramObjectCollection<Node> nodes = new();

    protected override void OnInitialized()
    {
        // Start event
        nodes.Add(new Node
        {
            ID = "start", OffsetX = 100, OffsetY = 200, Width = 50, Height = 50,
            Shape = new BpmnEvent
            {
                EventType = BpmnEventType.Start,
                Trigger = BpmnEventTrigger.None
            }
        });

        // End event
        nodes.Add(new Node
        {
            ID = "end", OffsetX = 500, OffsetY = 200, Width = 50, Height = 50,
            Shape = new BpmnEvent
            {
                EventType = BpmnEventType.End,
                Trigger = BpmnEventTrigger.None
            }
        });

        // Intermediate event with message trigger
        nodes.Add(new Node
        {
            ID = "intermediate", OffsetX = 300, OffsetY = 200, Width = 50, Height = 50,
            Shape = new BpmnEvent
            {
                EventType = BpmnEventType.Intermediate,
                Trigger = BpmnEventTrigger.Message
            }
        });
    }
}
```

**`BpmnEventType` values:** `Start`, `End`, `Intermediate`, `NonInterruptingStart`, `NonInterruptingIntermediate`, `ThrowingIntermediate`

**`BpmnEventTrigger` values:** `None`, `Message`, `Timer`, `Escalation`, `Conditional`, `Error`, `Cancel`, `Compensation`, `Signal`, `Multiple`, `Terminate`, `Parallel`

---

## BPMN Activities (Tasks and Subprocesses)

Activities describe work being done in a process:

```razor
// Task
nodes.Add(new Node
{
    ID = "task1", OffsetX = 200, OffsetY = 200, Width = 120, Height = 60,
    Shape = new BpmnActivity
    {
        ActivityType = BpmnActivityType.Task,
        TaskType = BpmnTaskType.Service   // or User, Send, Receive, Script, Manual, etc.
    },
    Annotations = new() { new ShapeAnnotation { Content = "Process Order" } }
});

// Subprocess (collapsed)
nodes.Add(new Node
{
    ID = "sub1", OffsetX = 400, OffsetY = 200, Width = 120, Height = 60,
    Shape = new BpmnActivity
    {
        ActivityType = BpmnActivityType.SubProcess,
        Loop = BpmnLoopCharacteristic.None,
        IsCompensation = false,
        IsAdhoc = false,
        IsCall = false
    }
});
```

**`BpmnActivityType`:** `Task`, `SubProcess`

**`BpmnTaskType`:** `None`, `User`, `Send`, `Receive`, `Service`, `Script`, `Manual`, `BusinessRule`

---

## BPMN Gateways

Gateways control the flow of a process (branching/merging):

```razor
// Exclusive gateway (XOR)
nodes.Add(new Node
{
    ID = "gateway1", OffsetX = 300, OffsetY = 200, Width = 50, Height = 50,
    Shape = new BpmnGateway
    {
        GatewayType = BpmnGatewayType.Exclusive
    }
});

// Parallel gateway (AND)
nodes.Add(new Node
{
    ID = "gateway2", OffsetX = 450, OffsetY = 200, Width = 50, Height = 50,
    Shape = new BpmnGateway { GatewayType = BpmnGatewayType.Parallel }
});
```

**`BpmnGatewayType` values:** `None`, `Exclusive`, `Inclusive`, `Parallel`, `Complex`, `EventBased`, `ParallelEventBased`, `ExclusiveEventBased`

---

## BPMN Data Objects and Data Stores

```razor
// Data Object
nodes.Add(new Node
{
    ID = "data1", OffsetX = 200, OffsetY = 350, Width = 50, Height = 60,
    Shape = new BpmnDataObject
    {
        DataObjectType = BpmnDataObjectType.Input   // Input, Output, None
    }
});

// Data Store
nodes.Add(new Node
{
    ID = "store1", OffsetX = 350, OffsetY = 350, Width = 60, Height = 50,
    Shape = new BpmnDataStore()
});
```

---

## BPMN Connectors

Use `BpmnConnectorType` on the connector's shape for BPMN-specific flow lines:

```razor
connectors.Add(new Connector
{
    ID = "seq1",
    SourceID = "start", TargetID = "task1",
    Shape = new BpmnFlow
    {
        Flow = BpmnFlowType.SequenceFlow
    }
});

// Message flow
connectors.Add(new Connector
{
    ID = "msg1",
    SourceID = "task1", TargetID = "task2",
    Shape = new BpmnFlow
    {
        Flow = BpmnFlowType.MessageFlow
    }
});
```

**`BpmnFlowType` values:** `SequenceFlow`, `DefaultSequenceFlow`, `ConditionalSequenceFlow`, `AssociationFlow`, `DirectionalAssociationFlow`, `BiDirectionalAssociationFlow`, `MessageFlow`, `InitiatingMessageFlow`, `NonInitiatingMessageFlow`

---

## BPMN Text Annotation

Text annotations attach explanatory notes to BPMN shapes:

```razor
nodes.Add(new Node
{
    ID = "annotation1", OffsetX = 300, OffsetY = 100, Width = 100, Height = 50,
    Shape = new BpmnTextAnnotation
    {
        TextAnnotationDirection = TextAnnotationDirection.Auto,
        TextAnnotationTarget = "task1"   // ID of the target shape
    },
    Annotations = new() { new ShapeAnnotation { Content = "Must complete in 2hrs" } }
});
```

---

## Expanded Sub-Process

An expanded sub-process is a container for child nodes and connectors:

```razor

// Add child nodes inside
nodes.Add(new Node
{
    ID = "child1", OffsetX = 230, OffsetY = 280, Width = 80, Height = 40,
    ParentID = "subprocess1",
    Shape = new BpmnActivity { ActivityType = BpmnActivityType.Task },
    Annotations = new() { new ShapeAnnotation { Content = "Step 1" } }
});

nodes.Add(new Node
{
    ID = "subprocess1", OffsetX = 300, OffsetY = 300, Width = 300, Height = 200,
    Shape = new BpmnExpandedSubProcess(){
        Children = new DiagramObjectCollection<string>() { "child1" }
    }
});


```

---

## Common Gotchas

- **Use `BpmnFlow`** (not standard `Connector`) for BPMN-typed connectors — otherwise the line style won't match the BPMN notation
- **Event + Trigger combination** controls appearance — e.g., `Start` + `Message` = envelope icon inside circle
- **`BpmnTextAnnotation.TextAnnotationTarget`** must be the ID of an existing node
- **Expanded sub-process children** use `ParentID` to nest inside the container
- **BPMN shapes are nodes** — they go in the `Nodes` collection like any other node
- **Gateway size is typically 50x50** — gateways look best as squares (equal width/height)
