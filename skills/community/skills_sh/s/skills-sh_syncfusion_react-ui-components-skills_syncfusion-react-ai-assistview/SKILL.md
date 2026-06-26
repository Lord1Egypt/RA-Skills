---
name: syncfusion-react-ai-assistview
description: Implement the Syncfusion React AI AssistView component. Use this skill to handle AI-powered conversational interfaces, AssistView setup, conversation flow, speech input or output, file attachments, UI customization, state management, and AI service integration such as OpenAI or Azure AI in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion React AI AssistView Component

## Component Overview

The **Syncfusion React AI AssistView** component is a comprehensive interactive chat component designed for building AI-powered conversational interfaces. It provides:

### Core Capabilities
- **Prompt-Response Management**: Manage conversation history with automatic data collection
- **Real-time Streaming**: Stream AI responses character-by-character for live typing effects
- **Template System**: Customize every UI element (banners, prompt items, responses, suggestions, footer)
- **Multi-View Support**: Switch between conversation assist view and custom content views
- **Voice Integration**: Built-in Speech-to-Text (voice input) and Text-to-Speech (voice output)
- **File Attachments**: Upload and include files with prompts
- **Advanced Toolbars**: Configurable toolbars for header, footer, responses, and prompts
- **AI Service Integration**: Direct integration with OpenAI, Azure OpenAI, and other AI services
- **Event-Driven Architecture**: Hooks for prompt submission, changes, and component lifecycle

### Key Features
- **Markdown Support**: Render AI responses as formatted HTML via markdown parsing
- **Conversation History**: Automatic tracking of all prompts and responses
- **Suggestion System**: Display helpful prompt suggestions to guide users
- **Avatar Customization**: Customize user and AI icons/avatars
- **Scroll Management**: Auto-scroll or manual scroll-to-bottom button
- **Clear Functionality**: Clear current prompt or entire conversation
- **Responsive Design**: Works on desktop and mobile with responsive layouts

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Install @syncfusion/ej2-react-interactive-chat package
- Add CSS theme imports
- Create basic component initialization
- Render component to DOM
- First working functional component example

### Configuration Essentials
📄 **Read:** [references/configuration-essentials.md](references/configuration-essentials.md)
- Set initial prompt text and placeholders
- Configure prompt suggestions and suggestion headers
- Customize user and AI avatar icons
- Control clear button visibility
- Enable/disable scroll-to-bottom functionality
- Manage component instance via refs
- **Set component dimensions (height and width)**
- **Apply custom CSS classes for styling**
- **Control header visibility**
- **Configure globalization (locale, RTL support)**
- **Enable state persistence across sessions**

### Conversation Management
📄 **Read:** [references/conversation-management.md](references/conversation-management.md)
- Initialize with pre-configured conversation data
- Add responses (string or object format)
- Access and manage conversation history
- Work with PromptModel data structure
- Render markdown in responses
- Persist and restore conversations

### Events and Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- Handle component lifecycle (created event)
- Respond to prompt submissions (promptRequest event)
- Track prompt text changes (promptChanged event)
- **Access detailed event arguments (PromptChangedEventArgs, PromptRequestEventArgs)**
- **Cancel prompt submissions programmatically**
- **Handle stop responding events for long operations**
- **Modify suggestions and toolbar items dynamically**
- Implement event-driven workflows
- Integrate with AI services via event handlers

### Toolbar Customization
📄 **Read:** [references/toolbar-customization.md](references/toolbar-customization.md)
- Configure four toolbar types (header, footer, response, prompt)
- Add custom toolbar items
- Control toolbar positioning (Inline vs Bottom)
- Customize toolbar icons
- Handle item click events
- **Configure all ToolbarItemModel properties (align, cssClass, disabled, tabIndex, template, type, visible)**
- **Create custom toolbar item templates**
- **Control item visibility and enabled state dynamically**
- **Set tab order for keyboard navigation**
- Manage attachment button behavior

### File Attachments
📄 **Read:** [references/file-attachments.md](references/file-attachments.md)
- Enable file attachment support
- Configure upload endpoints (saveUrl, removeUrl)
- Restrict file types (allowedFileType)
- Set file size limits (maxFileSize)
- Limit number of attachments (maximumCount)
- **Access attached files via attachedFiles array (FileInfo interface)**
- **Handle attachment lifecycle events (beforeAttachmentUpload, attachmentUploadSuccess, attachmentUploadFailure, attachmentRemoved)**
- **Validate files before upload**
- **Initialize prompts with pre-attached files**
- Handle server-side file processing

### Custom Views
📄 **Read:** [references/custom-views.md](references/custom-views.md)
- Create multiple views (Assist and Custom types)
- Set view names and icons
- Define view-specific templates
- **Configure activeView property to set initial view**
- **Switch between views programmatically**
- **Persist active view across sessions**
- **Conditionally set initial view based on user role or state**
- Display side-by-side content panels
- Use cases for multi-view layouts

### Templating System
📄 **Read:** [references/templating-system.md](references/templating-system.md)
- Customize banner templates (welcome content)
- Create prompt item templates (user message display)
- Design response item templates (AI response display)
- Build suggestion item templates
- Create custom footer templates
- Access template context data

### AI Service Integration
📄 **Read:** [references/ai-integration-setup.md](references/ai-integration-setup.md)
- Integrate with Azure OpenAI, OpenAI, Gemini, Claude
- Configure API credentials and authentication
- Handle real-time prompt processing
- Stream responses for live typing effects
- Parse markdown responses with marked library
- Error handling and rate limiting
- Security considerations for API keys

### Speech Capabilities
📄 **Read:** [references/speech-capabilities.md](references/speech-capabilities.md)
- Enable Speech-to-Text (voice input)
- Configure speech recognition language
- Handle interim transcripts while speaking
- Implement Text-to-Speech (voice output)
- Customize button labels and icons
- Handle speech events (start, stop, transcript, error)
- Browser compatibility notes

### Methods and APIs
📄 **Read:** [references/methods-and-apis.md](references/methods-and-apis.md)
- Use addPromptResponse() method
- Execute prompts dynamically with executePrompt()
- Scroll to bottom programmatically
- Access component instance via refs
- Manage component state
- Common patterns and gotchas

---

## Quick Start Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import * as React from 'react';
import * as ReactDOM from "react-dom";

function App() {
    const assistInstance = React.useRef<AIAssistViewComponent>(null);
    
    const onPromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            let defaultResponse = 'For real-time AI processing, connect to your preferred service (OpenAI, Azure OpenAI, etc.).';
            assistInstance.current.addPromptResponse(defaultResponse);
        }, 1000);
    };
  
    return (
        <AIAssistViewComponent 
            id="aiAssistView" 
            ref={assistInstance} 
            promptRequest={onPromptRequest}
            prompt={'Welcome! How can I help?'}
            promptSuggestions={['Ask about features', 'Get started guide']}
        />
    );
}

ReactDOM.render(<App />, document.getElementById('container'));
```

---

## Common Patterns

### Pattern 1: Basic Chat with Suggestions
Create a simple conversational interface with predefined suggestions:
- Enable prompt suggestions to guide user interactions
- Handle promptRequest event with simple responses
- Display conversation history automatically

### Pattern 2: AI Service Integration
Connect to real AI services for intelligent responses:
- Use promptRequest event to capture user input
- Call AI API with prompt text
- Stream response character-by-character for live effect
- Parse markdown responses for formatted output

### Pattern 3: Multi-View Dashboard
Combine chat with supporting content:
- Create Assist view for conversation
- Add Custom view for settings/sidebar
- Switch activeView based on user interaction
- Share data between views

### Pattern 4: Voice-Enabled Chat
Enable hands-free interaction with speech:
- Enable speechToTextSettings to capture voice
- Configure Text-to-Speech for response audio
- Use toolbar for voice control buttons
- Handle speech events for status feedback

### Pattern 5: File-Attached Prompts
Support file uploads with prompts:
- Enable attachments with enableAttachments property
- Configure attachment endpoints and file restrictions
- Include file data in prompt context
- Send files to backend API

---

## Key Props & Configuration

### Essential Props
- `promptRequest`: Event handler when user submits prompt
- `prompt`: Initial/default text in prompt input
- `promptPlaceholder`: Placeholder text for input area
- `promptSuggestions`: Array of suggested prompts
- `prompts`: Pre-configured conversation data

### Customization Props
- `promptIconCss`: CSS class for user avatar
- `responseIconCss`: CSS class for AI avatar
- `showClearButton`: Show/hide clear button (default: false)
- `showHeader`: Show/hide component header (default: true)
- `enableScrollToBottom`: Show scroll-to-bottom button (default: true)
- `height`: Component height (string | number, default: '100%')
- `width`: Component width (string | number, default: '100%')
- `cssClass`: Custom CSS classes for styling
- `activeView`: Currently displayed view index (number, default: 0)

### Template Props
- `bannerTemplate`: Welcome banner content
- `promptItemTemplate`: User message display
- `responseItemTemplate`: AI response display
- `promptSuggestionItemTemplate`: Suggestion styling
- `footerTemplate`: Custom prompt input area

### Advanced Props
- `enableAttachments`: Enable file uploads (default: false)
- `attachmentSettings`: File upload configuration
- `speechToTextSettings`: Voice input configuration
- `toolbarSettings`: Header toolbar configuration
- `footerToolbarSettings`: Footer toolbar configuration
- `responseToolbarSettings`: Response action toolbar
- `promptToolbarSettings`: Prompt toolbar configuration
- `locale`: Localization/globalization setting (default: 'en-US')
- `enableRtl`: Enable right-to-left rendering (default: false)
- `enablePersistence`: Enable state persistence (default: false)

### Event Props
- `created`: Component lifecycle event
- `promptRequest`: Prompt submission event
- `promptChanged`: Prompt text change event
- `stopRespondingClick`: Stop button click event
- `beforeAttachmentUpload`: Before file upload event
- `attachmentUploadSuccess`: File upload success event
- `attachmentUploadFailure`: File upload failure event
- `attachmentRemoved`: File removal event

---

## Common Use Cases

### Chat Bot with AI Integration
Build a customer service chatbot connected to OpenAI or Azure services:
1. Set up component with suggestions
2. Handle promptRequest to send to AI API
3. Stream responses for real-time feedback
4. Use templates for branded appearance

### Voice-Enabled Assistant
Create hands-free voice interaction:
1. Enable speechToTextSettings
2. Configure Text-to-Speech toolbar button
3. Handle speech events for status
4. Provide visual feedback during voice capture

### File Analysis Chat
Allow users to upload and discuss files:
1. Enable attachments
2. Configure file restrictions (type, size, count)
3. Send files with prompts to backend
4. Display file information in conversation

### Multi-Feature Dashboard
Combine chat with settings and content:
1. Create multiple views (Assist + Custom)
2. Use templates for custom view content
3. Implement view switching logic
4. Share conversation state between views

---