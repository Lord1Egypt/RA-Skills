package googleapi

import (
	"testing"
	"time"
)

func TestCircuitBreakerRecordFailureAndReset(t *testing.T) {
	cb := NewCircuitBreaker()

	for i := 0; i < CircuitBreakerThreshold-1; i++ {
		if opened := cb.RecordFailure(); opened {
			t.Fatalf("unexpected open at %d", i)
		}
	}

	if cb.IsOpen() {
		t.Fatalf("expected closed before threshold")
	}

	if opened := cb.RecordFailure(); !opened {
		t.Fatalf("expected circuit to open")
	}

	if !cb.IsOpen() {
		t.Fatalf("expected open")
	}

	cb.lastFailure = time.Now().Add(-CircuitBreakerResetTime - time.Second)
	if cb.IsOpen() {
		t.Fatalf("expected reset after timeout")
	}

	if cb.State() != circuitStateClosed {
		t.Fatalf("expected closed state")
	}

	if cb.failures != 0 {
		t.Fatalf("expected failures reset")
	}
}

func TestCircuitBreakerRecordSuccessResets(t *testing.T) {
	cb := NewCircuitBreaker()
	cb.open = true
	cb.failures = CircuitBreakerThreshold

	cb.RecordSuccess()

	if cb.State() != circuitStateClosed {
		t.Fatalf("expected closed after success")
	}

	if cb.failures != 0 {
		t.Fatalf("expected failures reset")
	}
}
