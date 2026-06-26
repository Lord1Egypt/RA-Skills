#!/usr/bin/env python3
"""
Team-Discuss Quick Start Example
Multi-agent technology selection discussion
"""

import asyncio
import sys
from pathlib import Path

# Add project path - update this to your team-discuss installation path
# sys.path.insert(0, "/path/to/team-discuss/src")

from core import SharedStore, DiscussionOrchestrator, DialecticEngine
from models import (
    Discussion, DiscussionStatus, DiscussionConfig,
    Participant, ParticipantStatus, AgentRole
)


async def quick_start():
    """Quick start example"""
    
    print("=" * 60)
    print("Team-Discuss Quick Start")
    print("=" * 60)
    
    # 1. Initialize components
    print("\n[1] Initializing...")
    store = SharedStore(base_dir="./discussions")
    orchestrator = DiscussionOrchestrator(store)
    dialectic = DialecticEngine()
    print("✓ Initialization complete")
    
    # 2. Create discussion
    print("\n[2] Creating discussion...")
    import time
    timestamp = int(time.time())
    
    discussion = Discussion(
        id=f"quick-start-demo",
        topic="Which frontend framework should we use?",
        description="React vs Vue technology selection",
        created_at=timestamp,
        status=DiscussionStatus.CREATED,
        current_round=0,
        max_rounds=2,
        config=DiscussionConfig(
            max_rounds=2,
            consensus_threshold=0.75
        ),
        participants=[
            Participant(
                agent_id="architect",
                session_id="session_architect",
                role_id=AgentRole.ARCHITECT,
                status=ParticipantStatus.JOINED,
                joined_at=timestamp
            ),
            Participant(
                agent_id="frontend-dev",
                session_id="session_frontend",
                role_id=AgentRole.DEVOPS,
                status=ParticipantStatus.JOINED,
                joined_at=timestamp
            ),
        ]
    )
    
    store.create_discussion(discussion)
    print(f"✓ Discussion created: {discussion.id}")
    print(f"✓ Topic: {discussion.topic}")
    
    # 3. Define mock agent callbacks
    print("\n[3] Preparing agent callbacks...")
    
    async def mock_agent_callback(agent_id: str, stance: str):
        async def callback(discussion_id: str, round_num: int, messages: list):
            # Round 1: Express initial stance
            if round_num == 1:
                content = f"As {agent_id}, I support using {stance}."
                if stance == "React":
                    content += " React has a rich ecosystem and efficient component-based development."
                else:
                    content += " Vue has a gentle learning curve and intuitive template syntax."
            else:
                # Round 2: Simple response
                content = f"I maintain my position on {stance}."
                if messages:
                    opponent = messages[-1].sender.agent_id
                    content += f" I disagree with @{opponent}'s view."
            
            # Dialectical analysis
            analysis = dialectic.analyze_message(
                type('Message', (), {
                    'id': f'msg_{agent_id}_{round_num}',
                    'sender': type('Sender', (), {'agent_id': agent_id})(),
                    'content': type('Content', (), {'text': content})(),
                })(),
                messages
            )
            
            print(f"\n💬 @{agent_id}:")
            print(f"   {content}")
            print(f"   📊 Quality: {analysis.quality.value} (Score: {analysis.score:.1f})")
            
            return content, "proposal" if round_num == 1 else "statement"
        return callback
    
    callbacks = {
        "architect": await mock_agent_callback("architect", "React"),
        "frontend-dev": await mock_agent_callback("frontend-dev", "Vue"),
    }
    print(f"✓ Prepared {len(callbacks)} callbacks")
    
    # 4. Register event listeners
    print("\n[4] Registering event listeners...")
    
    async def on_round_start(disc, round_num):
        print(f"\n{'='*60}")
        print(f"🔄 Round {round_num} started")
        print(f"{'='*60}")
    
    async def on_round_end(disc, round_num, summary):
        print(f"\n✅ Round {round_num} ended")
    
    orchestrator.register_callbacks(
        on_round_start=on_round_start,
        on_round_end=on_round_end
    )
    print("✓ Event listeners registered")
    
    # 5. Run discussion
    print("\n[5] Starting discussion...")
    print("=" * 60)
    
    result = await orchestrator.run_discussion(discussion.id, callbacks)
    
    print("\n" + "=" * 60)
    print("✓ Discussion completed!")
    print("=" * 60)
    
    # 6. Output results
    print("\n[6] Discussion results...")
    print(f"   Discussion ID: {result.id}")
    print(f"   Final status: {result.status.value}")
    print(f"   Total rounds: {result.current_round}")
    print(f"   Consensus level: {result.consensus_level.value}")
    
    print("\n" + "=" * 60)
    print("Example finished")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    asyncio.run(quick_start())
