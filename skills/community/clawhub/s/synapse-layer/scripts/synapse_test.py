#!/usr/bin/env python3
"""
Synapse Layer Connection Test Script

Tests Python SDK connectivity and basic operations.
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synapse_client import SynapseClient


def print_success(message: str):
    print(f"✅ {message}")


def print_error(message: str):
    print(f"❌ {message}")


def print_info(message: str):
    print(f"ℹ️  {message}")


def print_header(message: str):
    print(f"\n{'=' * 60}")
    print(f"{message}")
    print(f"{'=' * 60}\n")


def test_synapse_layer():
    """Run all Synapse Layer tests."""

    # Configuration
    API_KEY = os.environ.get("SYNAPSE_API_KEY")
    AGENT_ID = "test-agent"

    if not API_KEY:
        print_error("SYNAPSE_API_KEY environment variable not set")
        print_info("Set it with: export SYNAPSE_API_KEY=sk_connect_...")
        return False

    print_header("Synapse Layer Connection Test")
    print_info(f"Agent ID: {AGENT_ID}")
    print_info(f"API Key: {API_KEY[:20]}...")

    with SynapseClient(api_key=API_KEY) as client:
        # Test 1: Health Check
        print_header("Test 1: Health Check")
        try:
            health = client.health_check()
            print_success(f"Status: {health.get('status')}")
            print_success(f"Version: {health.get('version')}")
            print_success(f"Engine: {health.get('engine')}")
            print_success(f"Database: {health.get('database')}")

            capabilities = health.get('capabilities', {})
            print_info("Capabilities:")
            for cap, enabled in capabilities.items():
                status = "✅" if enabled else "❌"
                print(f"   {status} {cap}")

        except Exception as e:
            print_error(f"Health check failed: {e}")
            return False

        # Test 2: Save Memory
        print_header("Test 2: Save Memory")
        test_content = "Teste de integração do SynapseLayer via Python SDK!"
        try:
            result = client.remember(
                content=test_content,
                agent=AGENT_ID,
                memory_type="MANUAL",
                importance=5,
                tags=["test", "python-sdk", "integration"]
            )
            print_success("Memory saved successfully")
            print_info(f"   Memory ID: {result.get('memory_id')}")
            print_info(f"   Trust Quotient: {result.get('trust_quotient')}")
            print_info(f"   Intent: {result.get('intent')}")
            print_info(f"   Sanitized: {result.get('sanitized')}")
            print_info(f"   Privacy Applied: {result.get('privacy_applied')}")

            # Check pipeline
            pipeline = result.get('pipeline', {})
            if pipeline:
                print_info("   Security Pipeline:")
                print(f"      ✅ PII Redaction: {pipeline.get('pii_redaction')}")
                print(f"      ✅ Intent Validation: {pipeline.get('intent_validation')}")
                print(f"      ✅ Differential Privacy: {pipeline.get('differential_privacy')}")
                print(f"      ✅ Encryption: {pipeline.get('encryption')}")

        except Exception as e:
            print_error(f"Save memory failed: {e}")
            return False

        # Test 3: Recall Memory
        print_header("Test 3: Recall Memory")
        try:
            result = client.recall(
                query="integração synapse",
                agent=AGENT_ID,
                limit=3
            )

            memories = result.get('memories', [])
            print_success(f"Found {len(memories)} memories")

            for i, mem in enumerate(memories[:3], 1):
                content = mem.get('content', '')
                print_info(f"\n   Memory {i}:")
                print(f"      Content: {content[:80]}..." if len(content) > 80 else f"      Content: {content}")
                print(f"      Trust Quotient: {mem.get('trust_quotient')}")
                print(f"      Intent: {mem.get('intent')}")
                print(f"      Timestamp: {mem.get('timestamp')}")

        except Exception as e:
            print_error(f"Recall memory failed: {e}")
            return False

        # Test 4: Search Cross-Agent
        print_header("Test 4: Cross-Agent Search")
        try:
            result = client.search(
                query="synapse",
                limit=5
            )

            results = result.get('results', [])
            print_success(f"Found {len(results)} memories across all agents")

            for i, mem in enumerate(results[:3], 1):
                content = mem.get('content', '')
                agent = mem.get('agent', 'unknown')
                print_info(f"\n   Result {i} (Agent: {agent}):")
                print(f"      Content: {content[:60]}..." if len(content) > 60 else f"      Content: {content}")
                print(f"      Trust Quotient: {mem.get('trust_quotient')}")

        except Exception as e:
            print_error(f"Search failed: {e}")
            return False

        # Test 5: Process Text
        print_header("Test 5: Process Text")
        test_text = """
        Decidimos usar o SynapseLayer para memória persistente.
        O deadline para implementação é 30 de abril.
        Importante: monitorar o uso de quota mensal.
        """
        try:
            result = client.process_text(
                text=test_text,
                agent=AGENT_ID,
                source="test-script"
            )

            events_detected = result.get('events_detected', 0)
            print_success(f"Detected {events_detected} events")

            results = result.get('results', [])
            for i, event in enumerate(results[:3], 1):
                print_info(f"\n   Event {i}:")
                print(f"      Memory ID: {event.get('memory_id')}")
                print(f"      Intent: {event.get('intent')}")
                print(f"      Trust Quotient: {event.get('trust_quotient')}")

            pipeline = result.get('pipeline', {})
            if pipeline:
                print_info("   Pipeline:")
                print(f"      ✅ Trigger Detection: {pipeline.get('trigger_detection')}")
                print(f"      ✅ Policy Evaluation: {pipeline.get('policy_evaluation')}")
                print(f"      ✅ PII Redaction: {pipeline.get('pii_redaction')}")
                print(f"      ✅ Deduplication: {pipeline.get('deduplication')}")

        except Exception as e:
            print_error(f"Process text failed: {e}")
            return False

    # Summary
    print_header("Summary")
    print_success("All tests passed! 🎉")
    print_info("Synapse Layer is working correctly.")
    return True


if __name__ == "__main__":
    success = test_synapse_layer()
    sys.exit(0 if success else 1)
