package googleauth

import (
	"context"
	"testing"
	"time"
)

func TestWaitPostSuccess_ContextCancellation(t *testing.T) {
	t.Parallel()

	// Create a context that will be cancelled after a short delay
	ctx, cancel := context.WithCancel(context.Background())

	// Cancel context after 50ms
	go func() {
		time.Sleep(50 * time.Millisecond)
		cancel()
	}()

	start := time.Now()
	// Wait for a long duration (1 second) but expect early termination
	waitPostSuccess(ctx, 1*time.Second)
	elapsed := time.Since(start)

	// Should complete well before the 1-second wait duration
	// Allow some tolerance for timing (up to 200ms)
	if elapsed >= 500*time.Millisecond {
		t.Fatalf("waitPostSuccess did not respect context cancellation: took %v, expected < 500ms", elapsed)
	}
}

func TestWaitPostSuccess_FullDuration(t *testing.T) {
	t.Parallel()

	ctx := context.Background()

	start := time.Now()
	// Wait for a short duration
	waitPostSuccess(ctx, 100*time.Millisecond)
	elapsed := time.Since(start)

	// Should complete close to the specified duration
	if elapsed < 90*time.Millisecond {
		t.Fatalf("waitPostSuccess returned too early: %v, expected ~100ms", elapsed)
	}

	if elapsed > 200*time.Millisecond {
		t.Fatalf("waitPostSuccess took too long: %v, expected ~100ms", elapsed)
	}
}

func TestWaitPostSuccess_AlreadyCancelledContext(t *testing.T) {
	t.Parallel()

	// Create an already-cancelled context
	ctx, cancel := context.WithCancel(context.Background())
	cancel()

	start := time.Now()
	// Should return immediately since context is already cancelled
	waitPostSuccess(ctx, 1*time.Second)
	elapsed := time.Since(start)

	// Should complete almost immediately (well under 50ms)
	if elapsed >= 50*time.Millisecond {
		t.Fatalf("waitPostSuccess did not return immediately for cancelled context: took %v", elapsed)
	}
}
