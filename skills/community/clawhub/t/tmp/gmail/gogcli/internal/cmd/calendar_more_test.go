package cmd

import (
	"testing"

	"google.golang.org/api/calendar/v3"
)

func TestBuildAttendees(t *testing.T) {
	if got := buildAttendees(""); got != nil {
		t.Fatalf("unexpected: %#v", got)
	}
	got := buildAttendees(" a@b.com, c@d.com ")
	if len(got) != 2 || got[0].Email != "a@b.com" || got[1].Email != "c@d.com" {
		t.Fatalf("unexpected: %#v", got)
	}
}

func TestEventStartEnd(t *testing.T) {
	e := &calendar.Event{
		Start: &calendar.EventDateTime{DateTime: "2025-12-12T10:00:00Z"},
		End:   &calendar.EventDateTime{DateTime: "2025-12-12T11:00:00Z"},
	}
	if got := eventStart(e); got != "2025-12-12T10:00:00Z" {
		t.Fatalf("unexpected: %q", got)
	}
	if got := eventEnd(e); got != "2025-12-12T11:00:00Z" {
		t.Fatalf("unexpected: %q", got)
	}

	allDay := &calendar.Event{
		Start: &calendar.EventDateTime{Date: "2025-12-12"},
		End:   &calendar.EventDateTime{Date: "2025-12-13"},
	}
	if got := eventStart(allDay); got != "2025-12-12" {
		t.Fatalf("unexpected: %q", got)
	}
	if got := eventEnd(allDay); got != "2025-12-13" {
		t.Fatalf("unexpected: %q", got)
	}
}

func TestOrEmpty(t *testing.T) {
	if got := orEmpty("", "x"); got != "x" {
		t.Fatalf("unexpected: %q", got)
	}
	if got := orEmpty("  ", "x"); got != "x" {
		t.Fatalf("unexpected: %q", got)
	}
	if got := orEmpty("y", "x"); got != "y" {
		t.Fatalf("unexpected: %q", got)
	}
}
