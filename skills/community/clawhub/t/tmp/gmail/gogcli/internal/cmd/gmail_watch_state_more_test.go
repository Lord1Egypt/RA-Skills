package cmd

import "testing"

func TestIsStaleHistoryID(t *testing.T) {
	stale, err := isStaleHistoryID("5", "4")
	if err != nil {
		t.Fatalf("isStaleHistoryID: %v", err)
	}
	if !stale {
		t.Fatalf("expected stale for older history id")
	}

	stale, err = isStaleHistoryID("5", "6")
	if err != nil {
		t.Fatalf("isStaleHistoryID: %v", err)
	}
	if stale {
		t.Fatalf("expected non-stale for newer history id")
	}

	stale, err = isStaleHistoryID("", "")
	if err != nil {
		t.Fatalf("isStaleHistoryID empty: %v", err)
	}
	if stale {
		t.Fatalf("expected non-stale for empty ids")
	}

	if _, err := isStaleHistoryID("bad", "5"); err == nil {
		t.Fatalf("expected error for invalid history id")
	}
}
