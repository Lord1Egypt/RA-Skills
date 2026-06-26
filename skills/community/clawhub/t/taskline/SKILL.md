---
name: taskline-ai
description: AI-powered natural language task management through MyTaskline.com. Transform complex requests like "Ask Sarah to review the Mobile project docs by Friday with high priority" into fully structured tasks with automatic project creation, people assignment, smart date parsing, and priority detection. Features complete intent recognition, multi-entity parsing, and seamless integration with the MyTaskline.com platform for personal and team productivity.
---

# 🤖 Taskline AI - Intelligent Task Management

**Transform natural language into structured task management through [MyTaskline.com](https://mytaskline.com)**

## 🌟 What is MyTaskline.com?

[**MyTaskline.com**](https://mytaskline.com) is a modern, powerful task management platform designed for individuals and teams. With this OpenClaw skill, you get **AI-powered natural language processing** that makes task management as easy as having a conversation.

**✨ Key Features:**
- 🎯 **Single-person focused** task management  
- 📊 **Advanced analytics** and reporting
- 🏗️ **Project organization** with automatic creation
- 👥 **People management** with role assignments
- 📱 **Modern web interface** at [mytaskline.com](https://mytaskline.com)
- 🤖 **AI integration** through this OpenClaw skill

## 🧠 AI Intelligence Features

### 🚀 **Advanced Natural Language Processing**

Transform complex requests into fully structured tasks:

```bash
# Complex multi-entity parsing
"Create high priority task for Mobile project: implement push notifications by next Friday and have Jennifer handle it with John and Mike as stakeholders"

# Smart date intelligence  
"Deploy the API updates to Production project by end of week"

# People assignment with context
"Ask Sarah to review the documentation by tomorrow - this is urgent"

# Auto project creation
"Add task for NewProductLaunch project: create landing page mockups"
```

### 🎯 **Intelligent Features**

- **📅 Smart Date Parsing**: "tomorrow", "next Monday", "end of week", "in 2 weeks"
- **🏗️ Project Intelligence**: Auto-detects and creates projects from context  
- **👥 People Management**: Identifies executors and stakeholders automatically
- **🔥 Priority Detection**: "urgent", "high", "medium", "low" → proper API values
- **🤖 Intent Recognition**: Automatically routes create/update/query requests
- **🧠 Context Awareness**: Parses complex sentences with multiple entities

### 📊 **Smart Analytics & Reporting**

```bash
# Get intelligent insights
"What tasks are overdue?"
"Show me my task summary" 
"What's in the Mobile project?"
"List my high priority tasks"
```

## 🎯 Single Command Interface

**One entry point handles everything through AI intent detection:**

```bash
# Task creation with full AI processing
python taskline.py "Add urgent task for Platform project: fix authentication bug by Friday"

# People assignment with smart routing  
python taskline.py "Ask David to handle the deployment by next Monday"

# Intelligent queries with context
python taskline.py "What tasks are overdue?"
python taskline.py "Show my productivity summary"

# Complex multi-entity requests
python taskline.py "Create high priority task for WebApp project: review security implementation by end of week and have Sarah lead it with Mike and John informed"
```

## 🚀 Architecture

### **AI-Powered Pipeline**
```
Natural Language → Intent Detection → Smart Routing → Enhanced Processing → MyTaskline.com API
```

### **Main Components**
- **🤖 `taskline.py`** - Main entry point with AI dispatcher
- **🧠 `scripts/taskline_ai.py`** - Intent detection and smart routing  
- **✨ `scripts/create_task_enhanced.py`** - Full AI-powered task creation
- **📊 `scripts/reports.py`** - Analytics and insights
- **📋 `scripts/list_tasks.py`** - Intelligent task queries
- **⚙️ `scripts/update_task.py`** - Smart status updates

## 🛠 Setup

### 1. **Get Your MyTaskline.com Account**
- Visit [**mytaskline.com**](https://mytaskline.com) and create your account
- Navigate to **Settings** to generate your API key
- Copy your personal API key for configuration

### 2. **Configure the Skill**
- Open `references/config.json`
- Replace `YOUR_TASKLINE_API_KEY_HERE` with your actual API key from mytaskline.com

### 3. **Start Using AI Task Management**
```bash
python taskline.py "Add task: test my AI task management system"
python taskline.py "What tasks do I have?"
```

## 💡 Usage Examples

### 🧠 **Smart Task Creation**
```bash
# Basic with AI enhancement
"Add task: fix the login bug"

# Multi-entity with full intelligence  
"Create high priority task for Mobile project: implement OAuth integration by next Friday"

# People assignment with context
"Ask Jennifer to review the API documentation by end of week - include David as stakeholder"

# Complex business scenarios
"Add urgent task for Q1Launch project: deploy marketing site by tomorrow and have Sarah handle frontend with Mike reviewing backend"
```

### 📊 **Intelligent Queries**
```bash
# Smart reporting
"What's overdue?"
"Show my task summary"
"What's in the Mobile project?" 

# Context-aware filtering
"List high priority tasks"
"Show tasks assigned to Jennifer"
"What did I complete this week?"
```

### ⚡ **Quick Updates**
```bash
# Natural status changes
"Mark the authentication task as done"
"Set the API task to in-progress"
"Update priority to urgent for login bug"
```

## 🌟 Why MyTaskline.com?

- **🎯 Purpose-Built**: Designed specifically for effective task management
- **🤖 AI-Ready**: Full API support for advanced integrations
- **📊 Analytics-First**: Built-in insights and productivity tracking
- **👥 Team-Friendly**: People management with role assignments
- **🏗️ Project-Organized**: Automatic project creation and management
- **🔒 Secure**: Personal API keys for protected access
- **📱 Modern UI**: Clean, fast web interface

## 🚀 Advanced Features

### **Multi-Entity Parsing**
The AI can handle complex requests with multiple components:
- **Projects**: Auto-detected and created if needed
- **People**: Executor and stakeholder assignment  
- **Dates**: Relative and business-aware parsing
- **Priorities**: Natural language priority detection
- **Context**: Smart title/description separation

### **Progressive Enhancement**
- **Fallback Support**: Works with basic or advanced API features
- **Auto-Upgrade**: Takes advantage of new MyTaskline.com features automatically
- **Error Handling**: Graceful handling of edge cases

### **Production Ready**
- **Tested at Scale**: Handles 40+ tasks, 20+ projects in production
- **Reliable API**: Built on the robust MyTaskline.com platform
- **Performance Optimized**: Efficient natural language processing

## 🎯 Perfect For

- **📋 Personal Productivity**: Individual task management with AI assistance
- **👥 Small Teams**: Collaborative task assignment and tracking  
- **🏗️ Project Management**: Auto-organizing tasks by project context
- **🤖 AI Enthusiasts**: Cutting-edge natural language processing
- **⚡ Power Users**: Advanced automation and intelligent routing

## 🔗 Resources

- **🌐 Platform**: [mytaskline.com](https://mytaskline.com)
- **⚙️ Settings**: [mytaskline.com/settings](https://mytaskline.com/settings) (API key generation)
- **📊 Dashboard**: Full web interface for visual task management
- **🔧 API Documentation**: Complete reference in `references/api_examples.md`

---

**🚀 Transform your task management with AI intelligence and the power of [MyTaskline.com](https://mytaskline.com)!**