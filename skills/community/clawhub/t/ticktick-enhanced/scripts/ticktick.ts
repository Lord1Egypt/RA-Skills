#!/usr/bin/env bun

import { Command } from "commander";
import {
  authenticate,
  authenticateManual,
  checkAuth,
  logout,
  setupCredentials,
} from "./auth";
import { tasksCommand } from "./commands/tasks";
import { taskCreateCommand, taskUpdateCommand } from "./commands/task";
import { completeCommand } from "./commands/complete";
import { abandonCommand } from "./commands/abandon";
import { batchAbandonCommand } from "./commands/batch-abandon";
import { listsCommand } from "./commands/lists";
import { listCreateCommand, listUpdateCommand } from "./commands/list";
import { editCommand } from "./commands/edit";
import { detailsCommand } from "./commands/details";
import { triageCommand } from "./commands/triage";
const { loadConfig, configCommand } = require("./commands/config");

const program = new Command();

program
  .name("ticktick")
  .description("CLI for TickTick task and project management")
  .version("0.2.0");

// Auth command
const authCmd = program
  .command("auth")
  .description("Authenticate with TickTick");

authCmd
  .option("--client-id <id>", "TickTick OAuth client ID")
  .option("--client-secret <secret>", "TickTick OAuth client secret")
  .option("--manual", "Manual auth flow for headless servers (paste redirect URL)")
  .option("--logout", "Clear authentication tokens")
  .option("--status", "Check authentication status")
  .action(async (options) => {
    if (options.status) {
      const isAuthed = await checkAuth();
      if (isAuthed) {
        console.log("✓ Authenticated with TickTick");
      } else {
        console.log("✗ Not authenticated. Run 'ticktick auth' to set up.");
      }
      return;
    }

    if (options.logout) {
      await logout();
      return;
    }

    if (options.clientId && options.clientSecret) {
      await setupCredentials(options.clientId, options.clientSecret);
    }

    // Start OAuth flow
    if (options.manual) {
      await authenticateManual();
    } else {
      await authenticate();
    }
  });

// Tasks command - list tasks (enhanced)
program
  .command("tasks")
  .description("List tasks")
  .option("-l, --list <name>", "Filter by project name or ID")
  .option("-s, --status <status>", "Filter by status: pending or completed")
  .option("--due <filter>", "Filter by due: today, overdue, none, unspecified")
  .option("--priority <level>", "Filter by priority: high, medium, low, none")
  .option("--sort <field>", "Sort by: due, priority, title, created")
  .option("--limit <N>", "Maximum number of tasks")
  .option("--offset <N>", "Skip N tasks (pagination)")
  .option("--group", "Group output by project")
  .option("--format <type>", "Output format: plain, rich, json, yaml")
  .option("--focus <mode>", "Focus mode: today, overdue, upcoming")
  .option("--verbose", "Show API requests for debugging")
  .action(tasksCommand);

// Task command - create task
program
  .command("task <title>")
  .description("Create a new task")
  .option("-l, --list <name>", "Project name or ID (required; can be set via config)")
  .option("-c, --content <description>", "Task description/content")
  .option("-p, --priority <level>", "Priority: none, low, medium, high")
  .option("-d, --due <date>", "Due date: today, tomorrow, 'in N days', or ISO date")
  .option("-t, --tag <tags...>", "Tags for the task")
  .option("--json", "Output as JSON")
  .action(async (title, options) => {
    // Apply default project from config if not specified
    if (!options.list) {
      const config = loadConfig();
      if (config["default.project"]) {
        options.list = config["default.project"];
      }
    }
    if (!options.list) {
      console.error("Error: --list is required when creating a task (or set default.project in config)");
      process.exit(1);
    }
    await taskCreateCommand(title, options);
  });

// Edit command - modify an existing task
program
  .command("edit <task-id>")
  .description("Edit an existing task")
  .option("-l, --list <name>", "Project name or ID to search in")
  .option("--title <new>", "New title")
  .option("--content <text>", "New description/notes")
  .option("--due <date>", "New due date")
  .option("-p, --priority <level>", "New priority: none, low, medium, high")
  .option("-t, --tags <tags...>", "New tags (replaces existing)")
  .option("--json", "Output as JSON")
  .option("--verbose", "Verbose output")
  .action(editCommand);

// Details command - show full task info
program
  .command("details <task-id>")
  .description("Show full details of a task")
  .option("-l, --list <name>", "Project name or ID to search in")
  .option("--json", "Output as JSON")
  .option("--verbose", "Show full task object")
  .action(detailsCommand);

// Complete command - mark task as done
program
  .command("complete <task-id>")
  .description("Mark a task as complete")
  .option("-l, --list <name>", "Project name or ID to search in")
  .option("--json", "Output as JSON")
  .action(completeCommand);

// Alias: done
program
  .command("done <task-id>")
  .description("Alias for complete")
  .option("-l, --list <name>", "Project name or ID to search in")
  .option("--json", "Output as JSON")
  .action(completeCommand);

// Abandon command - mark task as won't do
program
  .command("abandon <task-id>")
  .description("Mark a task as won't do")
  .option("-l, --list <name>", "Project name or ID to search in")
  .option("--json", "Output as JSON")
  .action(abandonCommand);

// Batch abandon command
program
  .command("batch-abandon <taskIds...>")
  .description("Abandon multiple tasks (by IDs) in one call")
  .option("--json", "Output as JSON")
  .action(batchAbandonCommand);

// Config command - subcommands (create parent)
const configCmd = program
  .command("config")
  .description("Configuration commands");

configCmd
  .command("get <key>")
  .description("Get a configuration value")
  .action((key: string) => configCommand("get", key, undefined));

configCmd
  .command("set <key> <value>")
  .description("Set a configuration value")
  .action((key: string, value: string) => configCommand("set", key, value));

configCmd
  .command("list")
  .description("List all configuration values")
  .action(() => configCommand("list"));

// Projects (lists) command
program
  .command("projects")
  .description("List all projects")
  .option("--json", "Output as JSON")
  .action(listsCommand);

// List command - create or update project
program
  .command("list <name>")
  .description("Create or update a project")
  .option("-c, --color <hex>", "Project color in hex format")
  .option("-u, --update", "Update existing project instead of creating")
  .option("-n, --name <newName>", "New name (for update)")
  .option("--json", "Output as JSON")
  .action(async (name, options) => {
    if (options.update) {
      await listUpdateCommand(name, options);
    } else {
      await listCreateCommand(name, options);
    }
  });

// Triage command - ADHD-friendly categories
program
  .command("triage")
  .description("ADHD-friendly task triage by category")
  .option("--urgent", "Show only urgent/overdue tasks")
  .option("--quick-wins", "Show only quick-win tasks")
  .option("--meetings", "Show only meetings/calls")
  .option("--high-priority", "Show only high-priority tasks without due")
  .option("--all", "Show all categories (default)")
  .option("--format <type>", "Output format: plain, rich, json")
  .option("--verbose", "Debug output")
  .action(triageCommand);

// Morning alias - convenient for daily use
program
  .command("morning")
  .description("Morning triage shortcut (shows all categories in rich format)")
  .option("--verbose", "Debug output")
  .action((options) => {
    // Run triage with --all implied
    triageCommand({ all: true, format: "plain", verbose: options.verbose });
  });

program.parse();
