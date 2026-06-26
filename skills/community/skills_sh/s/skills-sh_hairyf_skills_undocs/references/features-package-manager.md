---
name: undocs-package-manager
description: Use package manager components to generate cross-package-manager commands
---

# Package Manager Components

Undocs provides components to generate package manager commands that work across npm, pnpm, yarn, bun, and deno.

## Components

### pm-install

Generate install commands for all package managers:

```mdc
:pm-install{name="undocs"}
```

Renders as:
- `npm install undocs`
- `pnpm add undocs`
- `yarn add undocs`
- `bun add undocs`
- `deno add npm:undocs`

### pm-run

Generate run script commands:

```mdc
:pm-run{script="dev"}
```

Renders as:
- `npm run dev`
- `pnpm dev`
- `yarn dev`
- `bun run dev`
- `deno task dev`

### pm-x

Generate execute commands (like `npx`, `pnpm dlx`, etc.):

```mdc
:pm-x{command="giget gh:unjs/undocs/template docs"}
```

Renders as:
- `npx giget gh:unjs/undocs/template docs`
- `pnpm dlx giget gh:unjs/undocs/template docs`
- `yarn dlx giget gh:unjs/undocs/template docs`
- `bun x giget gh:unjs/undocs/template docs`
- `deno run -A npm:giget gh:unjs/undocs/template docs`

## Props

- `name` (pm-install): Package name to install
- `script` (pm-run): Script name to run
- `command` (pm-x): Command to execute

## Usage Examples

### Installation Example

```mdc
Install the package:

:pm-install{name="undocs"}
```

### Development Server

```mdc
Start the development server:

:pm-run{script="dev"}
```

### Template Creation

```mdc
Create a new project:

:pm-x{command="giget gh:unjs/undocs/template docs --install"}
```

## Key Points

- Components automatically generate commands for all supported package managers
- Users can switch between package managers using tabs
- Commands are formatted correctly for each package manager
- Supports npm, pnpm, yarn, bun, and deno
- Reduces documentation maintenance by showing all options automatically

<!--
Source references:
- https://undocs.unjs.io/guide/components/components
-->
