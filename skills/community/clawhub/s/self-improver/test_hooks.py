#!/usr/bin/env python3
"""
Test script for error and recovery learning hooks.
"""

import sys
import traceback
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from hooks import get_hook_manager, on_error, on_recovery


def test_error_learning():
    """Test error learning hook."""
    print("\n" + "="*60)
    print("🧪 Testing Error Learning Hook")
    print("="*60)
    
    # Get hook manager
    hook_manager = get_hook_manager()
    
    # Simulate an error
    print("\n❌ Simulating an error...")
    try:
        # This will raise a ValueError
        raise ValueError("Test error: Invalid parameter value")
    except Exception as e:
        # Trigger error hook
        on_error(e)
    
    print("\n✅ Error learning complete!")
    print("📝 Check learnings/errors.json for the logged error")


def test_recovery_learning():
    """Test recovery learning hook."""
    print("\n" + "="*60)
    print("🧪 Testing Recovery Learning Hook")
    print("="*60)
    
    # Get hook manager
    hook_manager = get_hook_manager()
    
    # Simulate a recovery
    print("\n✅ Simulating a recovery...")
    
    # Trigger recovery hook
    on_recovery()
    
    print("\n✅ Recovery learning complete!")
    print("📝 Check learnings/recoveries.json for the logged recovery")


def test_full_workflow():
    """Test full error and recovery workflow."""
    print("\n" + "="*60)
    print("🧪 Testing Full Workflow")
    print("="*60)
    
    # Get hook manager
    hook_manager = get_hook_manager()
    
    # Simulate error
    print("\n❌ Step 1: Simulating an error...")
    try:
        raise ValueError("Test error: Database connection failed")
    except Exception as e:
        on_error(e)
    
    # Simulate recovery
    print("\n✅ Step 2: Simulating recovery...")
    on_recovery()
    
    # Review learnings
    print("\n📚 Step 3: Reviewing learnings...")
    review_learnings()
    
    print("\n✅ Full workflow test complete!")


def review_learnings():
    """Review all learnings."""
    import json
    
    workspace = Path(__file__).parent
    learnings_dir = workspace / 'learnings'
    
    # Review errors
    errors_file = learnings_dir / 'errors.json'
    if errors_file.exists():
        with open(errors_file, 'r') as f:
            errors = json.load(f)
        print(f"\n📝 Errors learned: {len(errors)}")
        for error in errors[-3:]:  # Show last 3 errors
            print(f"  - {error['error_type']}: {error['error_message']}")
    
    # Review recoveries
    recoveries_file = learnings_dir / 'recoveries.json'
    if recoveries_file.exists():
        with open(recoveries_file, 'r') as f:
            recoveries = json.load(f)
        print(f"\n✅ Recoveries learned: {len(recoveries)}")
        for recovery in recoveries[-3:]:  # Show last 3 recoveries
            print(f"  - {recovery['recovery_method']}")


def main():
    """Main test function."""
    print("\n" + "="*60)
    print("🧪 Self-Improving Agent - Hook Testing")
    print("="*60)
    
    # Run tests
    test_error_learning()
    test_recovery_learning()
    test_full_workflow()
    
    print("\n" + "="*60)
    print("✅ All tests complete!")
    print("="*60)
    print("\n📁 Check the learnings/ directory for logged learnings:")
    print("  - learnings/errors.json")
    print("  - learnings/recoveries.json")
    print("\n🎉 Testing complete!")


if __name__ == '__main__':
    main()
