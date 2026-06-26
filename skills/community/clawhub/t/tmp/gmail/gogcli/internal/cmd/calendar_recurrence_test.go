package cmd

import (
	"strings"
	"testing"
	"time"

	"google.golang.org/api/calendar/v3"
)

func TestOriginalStartRange(t *testing.T) {
	minRange, maxRange, err := originalStartRange("2025-01-02T10:00:00Z")
	if err != nil {
		t.Fatalf("originalStartRange: %v", err)
	}
	if !strings.Contains(minRange, "2025-01-02") || !strings.Contains(maxRange, "2025-01-02") {
		t.Fatalf("unexpected range: %s %s", minRange, maxRange)
	}

	minRange, maxRange, err = originalStartRange("2025-01-02")
	if err != nil {
		t.Fatalf("originalStartRange date: %v", err)
	}
	if !strings.Contains(minRange, "2025-01-02") || !strings.Contains(maxRange, "2025-01-03") {
		t.Fatalf("unexpected date range: %s %s", minRange, maxRange)
	}
}

func TestMatchesOriginalStart(t *testing.T) {
	event := &calendar.Event{
		OriginalStartTime: &calendar.EventDateTime{DateTime: "2025-01-02T10:00:00Z"},
		Start:             &calendar.EventDateTime{Date: "2025-01-02"},
	}
	if !matchesOriginalStart(event, "2025-01-02T10:00:00Z") {
		t.Fatalf("expected match for datetime")
	}
	if !matchesOriginalStart(event, "2025-01-02") {
		t.Fatalf("expected match for date")
	}
}

func TestTruncateRecurrence_Extra(t *testing.T) {
	rules := []string{"RRULE:FREQ=DAILY;COUNT=10", "EXDATE:20250103T100000Z"}
	updated, err := truncateRecurrence(rules, "2025-01-05T10:00:00Z")
	if err != nil {
		t.Fatalf("truncateRecurrence: %v", err)
	}
	if len(updated) != 2 {
		t.Fatalf("unexpected updated rules: %v", updated)
	}
	if !strings.Contains(updated[0], "UNTIL=") {
		t.Fatalf("expected UNTIL in rule: %v", updated[0])
	}
	if updated[1] != "EXDATE:20250103T100000Z" {
		t.Fatalf("expected exdate preserved")
	}
}

func TestRecurrenceUntil_Extra(t *testing.T) {
	until, err := recurrenceUntil("2025-01-02T10:00:00Z")
	if err != nil {
		t.Fatalf("recurrenceUntil: %v", err)
	}
	if !strings.HasPrefix(until, "20250102") {
		t.Fatalf("unexpected until: %s", until)
	}

	until, err = recurrenceUntil("2025-01-02")
	if err != nil {
		t.Fatalf("recurrenceUntil date: %v", err)
	}
	if until != time.Date(2025, 1, 1, 0, 0, 0, 0, time.UTC).Format("20060102") {
		t.Fatalf("unexpected date until: %s", until)
	}
}
