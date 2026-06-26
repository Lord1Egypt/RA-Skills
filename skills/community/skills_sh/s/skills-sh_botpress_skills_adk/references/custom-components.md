# Custom Components

Custom components are React UI elements that render in webchat. The LLM can yield them during autonomous execution, or you can send them explicitly from conversation handlers.

The dev console has a **Component Registry** page (`/components`) where you can browse installed components with live previews, inspect their props, and discover new components from the registry. See the `component-registry` reference in the adk-dev-console skill for details on the UI.

## Creating a Component

### 1. Create a `.bp.tsx` file

Place React function components in `src/components/` with the `.bp.tsx` extension:

```tsx
// src/components/TicketCard.bp.tsx
import React from 'react'

type Props = {
  ticketId: string
  title: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  status: string
}

const TicketCard: React.FC<Props> = ({ ticketId, title, priority, status }) => (
  <div style={{ padding: 16, borderRadius: 8, background: '#f8fafc', fontFamily: 'sans-serif' }}>
    <strong>{title}</strong>
    <p style={{ margin: '4px 0', fontSize: 13, color: '#64748b' }}>
      {ticketId} · {priority} · {status}
    </p>
  </div>
)

export default TicketCard
```

A component without props also works:

```tsx
// src/components/WelcomeBanner.bp.tsx
import React from 'react'

const WelcomeBanner: React.FC = () => (
  <div style={{ padding: 12, borderRadius: 8, background: '#f0f4ff', color: '#1e3a5f', fontFamily: 'sans-serif' }}>
    <strong>Acme IT Help Desk</strong>
    <p style={{ margin: '4px 0 0', fontSize: 13 }}>How can we help you today?</p>
  </div>
)

export default WelcomeBanner
```

### 2. Register in `src/components/index.ts`

Wrap each component with `CustomComponent` and provide metadata so the dev console can preview it and the LLM knows when and how to use it:

```typescript
import { CustomComponent, z } from '@botpress/runtime'
import TicketCard from './TicketCard.bp.tsx'
import WelcomeBanner from './WelcomeBanner.bp.tsx'

export const TicketCardComponent = new CustomComponent(TicketCard, {
  description: 'Display a ticket summary card. Use after creating or looking up a ticket.',
  props: z.object({
    ticketId: z.string().describe('The ticket ID'),
    title: z.string().describe('Short summary of the issue'),
    priority: z.enum(['low', 'medium', 'high', 'urgent']).describe('Priority level'),
    status: z.string().describe('Current ticket status'),
  }),
  exampleValues: [
    { ticketId: 'TKT-001', title: 'VPN not working', priority: 'high', status: 'open' },
    { ticketId: 'TKT-042', title: "Can't access email", priority: 'low', status: 'in-progress' },
  ],
})

// Components without metadata can be sent directly but can't be listed
// in Conversation.components (the LLM won't know about them).
export const WelcomeBannerComponent = new CustomComponent(WelcomeBanner)
```

### Metadata Fields

All three fields are required together — provide all or none:

- **description** — shown in the dev console and tells the LLM when to use this component
- **props** — Zod schema for the component's props; drives dev console forms and LLM prop validation
- **exampleValues** — seed values for dev console previews and LLM usage examples

## Using Components in Conversations

### LLM Autonomous Usage

List components in the `components` array so the LLM can yield them during `execute()`:

```typescript
import { Conversation } from '@botpress/runtime'
import { TicketCardComponent } from '../components'

export const Chat = new Conversation({
  channel: 'webchat.channel',
  components: [TicketCardComponent],

  async handler({ execute }) {
    await execute({
      instructions: 'Always use the TicketCard component to display ticket details.',
      tools: [lookupTicket],
    })
  },
})
```

Components in the `components` array must have metadata — the runtime throws an error otherwise.

### Sending Directly

Outside of autonomous execution, send a component message explicitly:

```typescript
import { WelcomeBannerComponent } from '../components'

await conversation.send({
  type: 'customComponent',
  payload: {
    component: WelcomeBannerComponent,
    props: {},
  },
})
```

This works for any component, with or without metadata.

### Channel Fallback

Custom components only work in webchat. For multi-channel bots, fall back to agnostic message types:

```typescript
if (conversation.channel === 'webchat.channel') {
  await conversation.send({
    type: 'customComponent',
    payload: {
      component: TicketCardComponent,
      props: { ticketId: 'TKT-001', title: 'VPN issue', priority: 'high', status: 'open' },
    },
  })
} else {
  await conversation.send({
    type: 'card',
    payload: {
      title: 'TKT-001: VPN issue',
      subtitle: 'Priority: high · Status: open',
      actions: [],
    },
  })
}
```

## Component Lifecycle

1. **Create** — Add a `.bp.tsx` file in `src/components/` and register it in `index.ts`
2. **Preview** — The dev console Installed tab shows live previews with hot reload
3. **Register** — List the component in a `Conversation`'s `components` array for LLM usage
4. **Deploy** — `adk deploy` bundles and uploads components; URLs are resolved automatically
5. **Render** — The webchat renders the component when the LLM yields it or you send it explicitly

## File Naming Conventions

- `.bp.tsx` — React component source
- `.bp.css` — Optional component styles (scoped via shadow DOM in the dev console and webchat)
