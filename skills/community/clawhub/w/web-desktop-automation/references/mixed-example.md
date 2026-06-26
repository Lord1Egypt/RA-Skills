# Real-World Mixed Example

## Scenario
Download a CSV report from a website, open it in a local spreadsheet app, make a small edit, save it, then upload the result back to the website.

## Why this example matters
This is the most common mixed workflow pattern:
- Browser prepares or retrieves the file
- Desktop app edits or transforms it
- Browser submits the result

## Phase 1: Browser download
1. Open the target website in Playwright.
2. Log in if needed.
3. Navigate to the report page.
4. Click the export/download button.
5. Wait until the file appears in the download folder.
6. Record the exact file path.

## Phase 2: Desktop processing
1. Open the downloaded file with the local spreadsheet app.
2. Make the required edit.
3. Save as a new file to avoid losing the original.
4. Verify the new file exists.

## Phase 3: Browser upload
1. Return to the browser.
2. Open the upload page.
3. Upload the edited file.
4. Submit.
5. Confirm success text or page state.

## Recommended safeguards
- Keep the original file unchanged.
- Use a new output filename.
- Verify each phase before continuing.
- If the browser phase fails, do not edit the file yet.
- If the desktop save fails, do not upload partial data.

## Template flow

```text
1. browser.goto(report_page)
2. browser.click(download)
3. wait for file
4. desktop.open(file)
5. desktop.edit_and_save(new_file)
6. browser.goto(upload_page)
7. browser.upload(new_file)
8. browser.submit()
9. verify success
```
