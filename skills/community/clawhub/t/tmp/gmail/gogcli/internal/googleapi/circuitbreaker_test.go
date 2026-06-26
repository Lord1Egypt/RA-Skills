package googleapi

import (
	"testing"
	"time"
)

func TestCircuitBreaker_OpenAndReset(t *testing.T) {
	cb := NewCircuitBreaker()
	if cb.State() != "closed" {
		t.Fatalf("expected closed, got %q", cb.State())
	}

	for i := 0; i < CircuitBreakerThreshold; i++ {
		opened := cb.RecordFailure()
		if i == CircuitBreakerThreshold-1 && !opened {
			t.Fatalf("expected circuit to open on threshold")
		}
	}

	if !cb.IsOpen() {
		t.Fatalf("expected open")
	}

	if cb.State() != "open" {
		t.Fatalf("expected open state")
	}

	// Force timeout-based reset path.
	cb.lastFailure = time.Now().Add(-(CircuitBreakerResetTime + time.Second))
	if cb.IsOpen() {
		t.Fatalf("expected closed after timeout")
	}

	if cb.State() != "closed" {
		t.Fatalf("expected closed after timeout")
	}

	// Explicit success reset path.
	cb.RecordFailure()
	cb.RecordSuccess()

	if cb.State() != "closed" {
		t.Fatalf("expected closed after success")
	}
}
