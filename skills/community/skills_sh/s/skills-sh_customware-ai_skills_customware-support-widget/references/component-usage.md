# Customware Support Widget Component Usage

This reference explains how to embed the Customware support widget in the React Router App.

The template is a Vite-built React Router v7 SPA:

- `react-router.config.ts` has `ssr: false`.
- `root.tsx`, or the equivalent React Router root file/component, owns the generated HTML document structure.
- Route composition lives in `app/routes.ts`.
- Page and layout UI live under `app/routes/` and `app/layouts/`.
- The app uses the `~/` path alias and validates with `npm run check`.

Because this is client-only, React effects can use `window`, `document`, `customElements`, and element refs.

## Integration Model

The widget is loaded as an external browser script. In this template, prefer adding the script once in `root.tsx` or the equivalent React Router root file/component that defines the HTML document structure, inside the document `<head>`:

```tsx
export function Layout({ children }: { children: ReactNode }): ReactElement {
	return (
		<html lang="en" suppressHydrationWarning>
			<head>
				<meta charSet="utf-8" />
				<meta name="viewport" content="width=device-width, initial-scale=1" />
				<Meta />
				<Links />
				<script
					id="customware-support-widget-script"
					src="https://app.customware.ai/support-widget/customware-chat.js"
					defer
				/>
			</head>
			<body className="overflow-x-hidden bg-background text-foreground antialiased">
				{children}
				<ScrollRestoration />
				<Scripts />
			</body>
		</html>
	);
}
```

That script registers this custom element:

```html
<customware-chat></customware-chat>
```

The React app is responsible for loading the script once in `root.tsx` or the root document component, rendering the element on the route/layout that needs support, placing/sizing it in the SPA layout, and passing the required ids. The widget is responsible for its own Shadow DOM UI, messages, tool badges, service calls, speech input, and page-operation behavior.

Do not add this script to Vite config and do not import the widget script from TypeScript. It is an external runtime script, not an npm dependency and not part of the Vite bundle.

Vite-specific notes:

- No Vite plugin, alias, optimizeDeps entry, or build config is required for the widget script.
- If ids are provided through Vite env, only use public `VITE_*` variables and never store secrets there.
- Prefer passing runtime `orgId` and `projectId` from the generated app's existing project/context state when available.

## Required Inputs

Every widget instance must receive both attributes:

- `org-id`: Customware org id.
- `project-id`: Customware project id.

Do not render the widget without both values. If either id is not available while building the integration, fail the task with a clear missing-id reason. If the SPA loads them asynchronously at runtime, render nothing or a surrounding placeholder until both values exist.

Do not pass task ids, domain ids, user ids, API tokens, session tokens, auth cookies, or credentials into the widget. Optional visitor identity belongs in the `meta` DOM property only.

## TypeScript Setup

Add element/property types if the app does not already have them. In this template, put them in a dedicated file such as `app/customware-chat.d.ts`:

```ts
import type React from 'react';

interface CustomwareChatElement extends HTMLElement {
	meta?: { email?: string; name?: string };
	styleOptions?: Partial<Record<SupportChatStyleOption, string>>;
}

type SupportChatStyleOption =
	| 'width'
	| 'height'
	| 'minHeight'
	| 'maxHeight'
	| 'panelWidth'
	| 'panelHeight'
	| 'panelMinHeight'
	| 'panelMaxHeight'
	| 'launcherSize'
	| 'launcherIconScale'
	| 'gap';

declare module 'react' {
	namespace JSX {
		interface IntrinsicElements {
			'customware-chat': React.DetailedHTMLProps<
				React.HTMLAttributes<CustomwareChatElement>,
				CustomwareChatElement
			> & {
				mode?: 'chat-bubble' | 'full';
				'org-id': string;
				'project-id': string;
				'style-options'?: string;
			};
		}
	}
}

export {};
```

This is a type-only declaration file. Do not import the widget runtime from it.

## Script Loading In root.tsx

Add the external script once in `root.tsx` or the React Router root file/component that defines the HTML document `<head>`. Keep the existing template tags such as `<Meta />`, `<Links />`, `<ScrollRestoration />`, and `<Scripts />`.

Recommended placement:

```tsx
<Meta />
<Links />
<script
	id="customware-support-widget-script"
	src="https://app.customware.ai/support-widget/customware-chat.js"
	defer
/>
```

Rules:

- Use exactly `https://app.customware.ai/support-widget/customware-chat.js`.
- Add it once.
- Use `defer` so it does not block document parsing.
- Do not add a second dynamic hook loader unless the `root.tsx`/root document script cannot be used.
- Do not bundle the widget source into the React app.
- No Vite config change is needed for the script.

## Where To Render In The Template

Render the widget only where the product needs support:

- Use `app/layouts/MainLayout.tsx` when the bubble should be available across the whole app shell.
- Use a route file such as `app/routes/index.tsx` when support should appear only on that page.
- Use a feature-specific layout/route when full mode belongs beside a particular workflow.

If adding a new support-specific route, register it in `app/routes.ts` using the template's React Router route config. Do not create a separate HTML file for the widget.

## Bubble Mode

Use `chat-bubble` when support should float above the app.

```tsx
import { useEffect, useRef } from 'react';

export function SupportBubble(props: {
	orgId: string;
	projectId: string;
	email?: string;
	name?: string;
}) {
	const ref = useRef<CustomwareChatElement | null>(null);

	useEffect(() => {
		if (!ref.current) return;
		ref.current.meta = { email: props.email, name: props.name };
		ref.current.styleOptions = {
			launcherSize: '52px',
			launcherIconScale: '1.16',
			panelWidth: '400px',
			panelHeight: '560px'
		};
	}, [props.email, props.name]);

	if (!props.orgId || !props.projectId) {
		return null;
	}

	return (
		<div className="fixed right-6 bottom-6 z-[999]">
			<customware-chat ref={ref} mode="chat-bubble" org-id={props.orgId} project-id={props.projectId} />
		</div>
	);
}
```

Bubble placement rules:

- Keep the wrapper in a stable viewport position, usually bottom-right.
- Use a high enough `z-index` for the app shell.
- Avoid clipped ancestors such as `overflow: hidden` around the bubble anchor.
- Use `launcherSize` and `launcherIconScale` when the launcher needs to be smaller or the favicon rim should feel lighter.

## Full Mode

Use `full` when support belongs inside a real layout region, such as a right rail, split pane, drawer, or full-height panel.

```tsx
import { useEffect, useRef } from 'react';

export function SupportRail(props: { orgId: string; projectId: string }) {
	const ref = useRef<CustomwareChatElement | null>(null);

	useEffect(() => {
		if (!ref.current) return;
		ref.current.styleOptions = {
			width: '100%',
			height: '100%'
		};
	}, []);

	if (!props.orgId || !props.projectId) {
		return null;
	}

	return (
		<aside className="min-h-0 h-[calc(100vh-64px)] w-[420px] border-l border-zinc-200">
			<customware-chat ref={ref} mode="full" org-id={props.orgId} project-id={props.projectId} />
		</aside>
	);
}
```

Full mode sizing rules:

- Give the whole component or containing region a concrete height.
- Let only the widget's internal messages region scroll.
- Use `min-height: 0` on flex/grid parents when needed.
- Do not try to size the widget's internal message list from the host page.

## Properties And Attributes

Use attributes for simple string configuration:

```tsx
<customware-chat mode="full" org-id={orgId} project-id={projectId} />
```

Use DOM properties through a ref for objects:

```tsx
useEffect(() => {
	if (!ref.current) return;
	ref.current.meta = {
		email: currentUser.email,
		name: currentUser.name
	};
	ref.current.styleOptions = {
		height: '100%',
		width: '100%',
		panelWidth: '420px'
	};
}, [currentUser.email, currentUser.name]);
```

Supported attributes:

- `org-id`: required.
- `project-id`: required.
- `mode`: optional; `chat-bubble` or `full`.
- `style-options`: optional JSON string for static HTML. Prefer `styleOptions` in React when possible.

Supported DOM properties:

- `meta`: optional `{ email?: string; name?: string }`.
- `styleOptions`: optional object of sizing values.

Supported `styleOptions` keys:

| Key | Use |
| --- | --- |
| `width` | Component/panel width |
| `height` | Component/panel height |
| `minHeight` | Minimum component/panel height |
| `maxHeight` | Maximum component/panel height |
| `panelWidth` | Bubble dialog width |
| `panelHeight` | Bubble dialog height |
| `panelMinHeight` | Bubble dialog minimum height |
| `panelMaxHeight` | Bubble dialog maximum height |
| `launcherSize` | Bubble launcher size |
| `launcherIconScale` | Favicon scale inside the launcher |
| `gap` | Space between launcher/dialog and viewport anchor |

Do not assign a configuration object to `element.style`; that is the browser's native inline CSS object.

## Page Operation

The support agent can operate the visible host page when the user asks it to click, fill, select, navigate, replace values, or submit. The user request must come through the support widget; do not hardcode operation prompts or values into the React app.

Examples of user requests that may trigger page operation:

- `Can you fill this form?`
- `Select High priority and submit.`
- `Replace the requester email.`
- `Open the billing tab.`
- `Click the export button.`

The widget excludes its own chat element from page operation, so the page agent operates the host app rather than the chat UI.

For reliable page operation:

- Use visible, enabled, semantically clear controls.
- Prefer labels for inputs, selects, textareas, and buttons.
- Avoid hiding target controls behind clipped or inaccessible custom UI.
- Do not add custom page-control handlers around the widget.
- Do not expose secrets or private tokens as visible DOM text.

When values are unknown, test with a natural two-step flow:

1. User: `Can you fill this form?`
2. Agent asks for missing values.
3. User provides values.
4. Agent fills/submits the visible page.

## Service Behavior

The page should not call support chat endpoints or tools directly. The widget sends requests to its own service using `org-id`, `project-id`, the user message, and optional `meta`.

The support agent currently has these capabilities:

- Read domain/context.
- List support tasks.
- Create support tasks.
- Operate the visible host page.

Tool calls render inside the widget as compact status badges. They are not user-clickable controls.

## Visual Contract

The host app should place and size the component. The widget renders its own header, messages, assistant text, user messages, tool badges, composer, microphone control when supported, loading states, and light/dark theme.

Do not reach into Shadow DOM or depend on internal class names. Do not recreate the chat UI in React.

## Code Validation

The MITB agent may not have browser automation or visual testing. Validate the integration by inspecting the generated React code and running the app's existing typecheck/build command when available.

Minimum code checks:

- The `root.tsx`/root document script tag uses `https://app.customware.ai/support-widget/customware-chat.js`.
- The script is loaded once in `root.tsx` or the root document component, not once per route render.
- `<customware-chat>` is rendered directly.
- Both `org-id` and `project-id` are always supplied when the element renders.
- The widget is gated when runtime ids are unavailable.
- `meta` and `styleOptions` are assigned through a typed ref when object values are needed.
- Full mode has a wrapper/component height.
- Bubble mode has a stable anchor and no obviously clipped wrapper.
- No host code calls support chat endpoints, page-operation endpoints, or internal widget APIs.
- No Vite config was changed just to load the widget script.

Useful user prompt examples for reasoning about page-operation support:

- `list tasks`
- `read domain`
- `create task verify support widget`
- `Can you fill this form?`
- `Use requester name Asha Iyer, requester email asha.iyer@example.com, priority High, and submit.`

Do not claim visual verification unless the environment explicitly provides browser access and the task asks for it.

## Static Troubleshooting

Use these checks when reviewing generated code or addressing a reported integration issue.

Widget is not present in generated code:

- Check the element tag is exactly `customware-chat`.
- Check both `org-id` and `project-id` are present.
- Check the render path is not permanently returning `null` after ids are available.

Support requests are reported as failing:

- Check the script URL is exactly `https://app.customware.ai/support-widget/customware-chat.js`.
- Check the host app is not calling support chat endpoints directly.
- Check the component is rendered with real `org-id` and `project-id`, not placeholders.
- Check secrets or auth tokens were not added to widget attributes.

Full mode does not scroll correctly:

- Give the containing panel a concrete height.
- Add `min-height: 0` to flex/grid parents.
- Size the whole component, not the internal message list.

Bubble mode is clipped:

- Move the anchor outside clipped content.
- Check ancestors for `overflow: hidden`, transforms, or unexpected stacking contexts.
- Reduce `panelWidth`/`panelHeight` if the viewport is too small.

Page operation does not affect the page:

- Confirm the user typed the request into the widget.
- Make the target controls visible, enabled, and labeled.
- Ensure the widget is not covering the target controls.
- Remove fake operation prompts from the host app.
