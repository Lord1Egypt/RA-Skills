"""Basic sense-memory usage — remember, recall, journal."""

import asyncio
import os

from nostrkey import Identity
from sense_memory import MemoryStore


async def main():
    identity = Identity.from_nsec(os.environ["NOSTR_NSEC"])
    store = MemoryStore(identity, os.environ.get("NOSTR_RELAY", "wss://relay.nostrkeep.com"))

    # Store some memories
    await store.remember("user_name", "Vergel")
    await store.remember("user_timezone", "America/Vancouver")
    print("Memories stored.")

    # Recall a specific memory
    mem = await store.recall("user_timezone")
    if mem:
        print(f"Timezone: {mem.value}")

    # List all memories
    all_memories = await store.recall_all()
    print(f"\nAll memories ({len(all_memories)}):")
    for m in all_memories:
        print(f"  {m.key} = {m.value}")

    # Write a journal entry
    await store.journal("First conversation with this user. They value sovereignty.")
    print("\nJournal entry written.")

    # Read recent journal
    entries = await store.recent(limit=5)
    print(f"\nRecent journal ({len(entries)} entries):")
    for e in entries:
        print(f"  {e.content}")

    # Forget a memory
    await store.forget("user_name")
    print("\nForgot user_name.")


if __name__ == "__main__":
    asyncio.run(main())
