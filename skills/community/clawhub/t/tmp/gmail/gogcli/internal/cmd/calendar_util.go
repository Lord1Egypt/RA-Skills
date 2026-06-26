package cmd

import "google.golang.org/api/calendar/v3"

func isAllDayEvent(e *calendar.Event) bool {
	return e != nil && e.Start != nil && e.Start.Date != ""
}
