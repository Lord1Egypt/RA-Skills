package cmd

import (
	"testing"
	"time"

	"google.golang.org/api/calendar/v3"
)

func TestFormatEventTime(t *testing.T) {
	ev := &calendar.Event{
		Start: &calendar.EventDateTime{Date: "2026-01-09"},
		End:   &calendar.EventDateTime{Date: "2026-01-10"},
	}
	start, end := formatEventTime(ev, time.UTC)
	if start != "2026-01-09" || end != "2026-01-10" {
		t.Fatalf("unexpected all-day: %q %q", start, end)
	}

	ev = &calendar.Event{
		Start: &calendar.EventDateTime{DateTime: "2026-01-09T15:30:00Z"},
		End:   &calendar.EventDateTime{DateTime: "2026-01-09T16:15:00Z"},
	}
	start, end = formatEventTime(ev, time.UTC)
	if start != "15:30" || end != "16:15" {
		t.Fatalf("unexpected timed: %q %q", start, end)
	}
}

func TestParseEventStart(t *testing.T) {
	loc := time.UTC
	ev := &calendar.Event{
		Start: &calendar.EventDateTime{DateTime: "2026-01-09T15:30:00Z"},
	}
	got := parseEventStart(ev, loc)
	if got.IsZero() || got.Format(time.RFC3339) != "2026-01-09T15:30:00Z" {
		t.Fatalf("unexpected datetime: %v", got)
	}

	ev = &calendar.Event{
		Start: &calendar.EventDateTime{Date: "2026-01-09"},
	}
	got = parseEventStart(ev, loc)
	if got.IsZero() || got.Format("2006-01-02") != "2026-01-09" {
		t.Fatalf("unexpected date: %v", got)
	}

	if got = parseEventStart(&calendar.Event{}, loc); !got.IsZero() {
		t.Fatalf("expected zero time")
	}
}

func TestDedupeTeamEvents(t *testing.T) {
	events := []teamEvent{
		{ID: "1", Who: "Alice", dedupeKey: "k1"},
		{ID: "2", Who: "Bob", dedupeKey: "k1"},
		{ID: "3", Who: "Cleo", dedupeKey: "k2"},
	}
	deduped := dedupeTeamEvents(events)
	if len(deduped) != 2 {
		t.Fatalf("expected 2 events, got %d", len(deduped))
	}
	if deduped[0].Who != "Alice, Bob" {
		t.Fatalf("unexpected who: %q", deduped[0].Who)
	}
}

func TestEventDedupeKey(t *testing.T) {
	ev := &calendar.Event{ICalUID: "uid-1"}
	key := eventDedupeKey(ev, time.Time{})
	if key != "uid-1" {
		t.Fatalf("unexpected key: %q", key)
	}

	ev = &calendar.Event{Id: "id-1"}
	when := time.Date(2026, 1, 9, 10, 0, 0, 0, time.UTC)
	key = eventDedupeKey(ev, when)
	if key != "id-1|"+when.Format(time.RFC3339) {
		t.Fatalf("unexpected key: %q", key)
	}

	ev = &calendar.Event{}
	if key = eventDedupeKey(ev, when); key != "" {
		t.Fatalf("expected empty key, got %q", key)
	}
}
