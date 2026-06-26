package cmd

import (
	"context"
	"fmt"
	"strings"

	"google.golang.org/api/sheets/v4"
)

func copyDataValidation(ctx context.Context, svc *sheets.Service, spreadsheetID, sourceA1, destA1 string) error {
	sourceRange, err := parseSheetRange(sourceA1, "copy-validation-from")
	if err != nil {
		return err
	}
	destRange, err := parseSheetRange(destA1, "updated")
	if err != nil {
		return err
	}

	sheetIDs, err := fetchSheetIDMap(ctx, svc, spreadsheetID)
	if err != nil {
		return err
	}

	sourceGrid, err := gridRangeFromMap(sourceRange, sheetIDs, "copy-validation-from")
	if err != nil {
		return err
	}
	destGrid, err := gridRangeFromMap(destRange, sheetIDs, "updated")
	if err != nil {
		return err
	}

	req := &sheets.BatchUpdateSpreadsheetRequest{
		Requests: []*sheets.Request{
			{
				CopyPaste: &sheets.CopyPasteRequest{
					Source:      sourceGrid,
					Destination: destGrid,
					PasteType:   "PASTE_DATA_VALIDATION",
				},
			},
		},
	}

	_, err = svc.Spreadsheets.BatchUpdate(spreadsheetID, req).Do()
	if err != nil {
		return fmt.Errorf("apply data validation: %w", err)
	}
	return nil
}

func fetchSheetIDMap(ctx context.Context, svc *sheets.Service, spreadsheetID string) (map[string]int64, error) {
	call := svc.Spreadsheets.Get(spreadsheetID).
		Fields("sheets(properties(sheetId,title))")
	if ctx != nil {
		call = call.Context(ctx)
	}
	resp, err := call.Do()
	if err != nil {
		return nil, fmt.Errorf("get spreadsheet metadata: %w", err)
	}

	ids := make(map[string]int64, len(resp.Sheets))
	for _, sheet := range resp.Sheets {
		if sheet.Properties == nil {
			continue
		}
		ids[sheet.Properties.Title] = sheet.Properties.SheetId
	}
	return ids, nil
}

func toGridRange(r a1Range, sheetID int64) *sheets.GridRange {
	return &sheets.GridRange{
		SheetId:          sheetID,
		StartRowIndex:    int64(r.StartRow - 1),
		EndRowIndex:      int64(r.EndRow),
		StartColumnIndex: int64(r.StartCol - 1),
		EndColumnIndex:   int64(r.EndCol),
	}
}

func parseSheetRange(a1, label string) (a1Range, error) {
	r, err := parseA1Range(a1)
	if err != nil {
		return a1Range{}, fmt.Errorf("parse %s range: %w", label, err)
	}
	if strings.TrimSpace(r.SheetName) == "" {
		return a1Range{}, fmt.Errorf("%s range must include a sheet name", label)
	}
	return r, nil
}

func gridRangeFromMap(r a1Range, sheetIDs map[string]int64, label string) (*sheets.GridRange, error) {
	sheetID, ok := sheetIDs[r.SheetName]
	if !ok {
		return nil, fmt.Errorf("unknown sheet %q in %s range", r.SheetName, label)
	}
	return toGridRange(r, sheetID), nil
}
