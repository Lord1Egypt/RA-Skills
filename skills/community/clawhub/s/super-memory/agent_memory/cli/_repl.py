"""Interactive REPL for Agent Memory CLI."""

import cmd
import sys
from agent_memory import AgentMemory


class MemoryREPL(cmd.Cmd):
    """Interactive Agent Memory shell."""

    intro = "Agent Memory REPL v12.0 | Type 'help' for commands, 'exit' to quit"
    prompt = "memory> "

    def __init__(self, mem=None, **kwargs):
        super().__init__(**kwargs)
        self.mem = mem or AgentMemory()

    def do_remember(self, arg):
        """Remember content: remember <text>"""
        if not arg:
            print("  Usage: remember <text>")
            return
        result = self.mem.remember(arg)
        if isinstance(result, dict):
            if result.get("written"):
                mid = result.get("memory_id", "?")
                print(f"  \u2713 Stored as {mid}")
            else:
                status = result.get("status", "unknown")
                reason = result.get("reason", "")
                print(f"  \u2717 {status}: {reason}")

    def do_recall(self, arg):
        """Recall memories: recall <query>"""
        if not arg:
            print("  Usage: recall <query>")
            return
        result = self.mem.recall(arg)
        if isinstance(result, dict):
            primary = result.get("primary", [])
            if not primary:
                print("  No results found")
            for i, r in enumerate(primary[:5], 1):
                mid = r.get("memory_id", "?")
                content = r.get("content", "")[:80]
                score = r.get("_rrf_score", r.get("score", ""))
                print(f"  {i}. [{mid}] {content}...")
                if score:
                    print(f"     Score: {score}")

    def do_forget(self, arg):
        """Forget a memory: forget <memory_id>"""
        if not arg:
            print("  Usage: forget <memory_id>")
            return
        try:
            self.mem.store.delete_memory(arg.strip())
            print(f"  \u2713 Forgotten: {arg.strip()}")
        except Exception as e:
            print(f"  \u2717 Error: {e}")

    def do_stats(self, arg):
        """Show memory statistics."""
        try:
            count = self.mem.store.count()
            health = self.mem.health_check()
            status = health.get("status", "unknown")
            print(f"  \U0001f4ca {count} memories | Status: {status}")
            if health.get("degraded_features"):
                print(f"  \u26a0 Degraded: {', '.join(health['degraded_features'])}")
        except Exception as e:
            print(f"  \u2717 Error: {e}")

    def do_health(self, arg):
        """Show health check."""
        health = self.mem.health_check()
        print(f"  Status: {health.get('status', 'unknown')}")
        print(f"  Healthy: {health.get('healthy', False)}")
        for comp, status in health.get("components", {}).items():
            icon = "\u2713" if status == "healthy" else ("\u26a0" if status == "degraded" else "\u2717")
            print(f"  {icon} {comp}: {status}")

    def do_search(self, arg):
        """Search memories (alias for recall): search <query>"""
        self.do_recall(arg)

    def do_exit(self, arg):
        """Exit the REPL."""
        self.mem.close()
        print("Goodbye!")
        return True

    def do_quit(self, arg):
        """Exit the REPL."""
        return self.do_exit(arg)

    def do_EOF(self, arg):
        """Handle Ctrl+D."""
        print()
        return self.do_exit(arg)

    def default(self, line):
        """Default handler — try to remember unrecognized input."""
        if line.strip():
            self.do_remember(line)

    def emptyline(self):
        """Do nothing on empty input."""
        pass


def start_repl(mem=None):
    """Start the interactive REPL."""
    repl = MemoryREPL(mem=mem)
    try:
        repl.cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        if repl.mem:
            repl.mem.close()


if __name__ == "__main__":
    start_repl()
