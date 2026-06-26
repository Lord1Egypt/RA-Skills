---
name: syncfusion-blazor-smart-paste
description: Set up and use the Syncfusion Blazor Smart Paste Button — AI-powered clipboard-to-form filling with OpenAI, Azure OpenAI, Ollama, or custom AI backends. Covers NuGet setup, service configuration, field annotations, button customization, and troubleshooting.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Blazor Smart Paste Button

The Syncfusion Blazor Smart Paste Button uses AI to intelligently read clipboard text and populate form fields automatically, eliminating manual data entry.

## When to Use

Use this skill when you need to:
- Add the Smart Paste Button to a Blazor form for AI-powered clipboard-to-field population
- Configure an AI backend (OpenAI, Azure OpenAI, Ollama, or custom)
- Add `[SmartPasteField]` annotations to fine-tune field mapping
- Customize button appearance, content, and behavior
- Integrate a custom `IChatInferenceService` implementation
- Troubleshoot Smart Paste integration or AI connectivity issues

## Prerequisites

- **.NET SDK 8.0** or later
- **Visual Studio 2022** (17.0+) or Visual Studio Code
- Active **OpenAI**, **Azure OpenAI**, or **Ollama** account (or a custom AI backend)
- Basic knowledge of Blazor Web App (Server render mode)

## Quick Setup

Follow these steps in order:

### 1. Initial Setup and NuGet Installation

Start with [getting-started.md](./references/getting-started.md) to:
- Create a new Blazor Web App Server
- Install Syncfusion NuGet packages
- Register Syncfusion Blazor services
- Add necessary namespaces

### 2. Configure AI Service

Proceed here to [Custom AI Integration Steps](https://blazor.syncfusion.com/documentation/smart-paste/custom-inference-backend) to:
- Choose your AI provider (OpenAI, Azure OpenAI, or Ollama)
- Install AI service-specific NuGet packages
- Configure your AI backend in `Program.cs`
- Add theme stylesheets and script resources

### 3. Implement and Customize

Complete with [implementation-and-customization.md](./references/implementation-and-customization.md) to:
- Add the Smart Paste Button component to your form
- Run and test the application
- Add custom field annotations
- Customize button appearance
- Integrate custom AI services
- Troubleshoot common issues

## Key Features

| Feature | Details |
|---------|---------|
| **AI-Powered Form Filling** | Reads clipboard text and maps data to form fields automatically |
| **Multiple AI Backends** | OpenAI, Azure OpenAI, Ollama, and custom `IChatInferenceService` |
| **Field Annotations** | `[SmartPasteField]` attribute for precise field descriptions |
| **Easy Integration** | Single NuGet package + `AddSyncfusionSmartPaste()` service call |
| **Customizable UI** | Inherits all `SfButton` properties — icons, content, CSS classes |

## NuGet Packages

- `Syncfusion.Blazor.SmartComponents` (v28.1.33+)
- `Syncfusion.Blazor.Themes`
- AI provider package — see [ai-service-configuration.md](./references/ai-service-configuration.md)

## Reference Documents

| Document | Purpose |
|----------|---------|
| [getting-started.md](./references/getting-started.md) | Project creation, NuGet installation, service registration |
| [ai-service-configuration.md](./references/ai-service-configuration.md) | AI provider setup (OpenAI, Azure OpenAI, Ollama) |
| [implementation-and-customization.md](./references/implementation-and-customization.md) | Component usage, field annotations, customization, troubleshooting |


