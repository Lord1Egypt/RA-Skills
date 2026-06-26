# Update Code from Shorthand Reference

This reference supports the `quasi-coder` skill when a collaborator explicitly wants shorthand
converted into a finished edit. It complements the local skill definition by showing when this flow
applies, how to shape the prompt, what markers to look for, and what a strong conversion looks
like.

## Why This Lives in `references/`

- The agent reads this file for guidance.
- The file is instructional documentation, not a runtime asset consumed as-is.
- The content explains a prompting pattern and a worked transformation, which matches the purpose
  of `references/` in this repo.

## Use This Flow When

- The prompt begins with `UPDATE CODE FROM SHORTHAND`.
- The prompt uses a `quasi-coder ... --update #file:<path>` pattern.
- The target file is explicit, or otherwise unambiguous from the prompt.
- The target file contains `start-shorthand` and `end-shorthand` markers.
- The collaborator is steering with `()=>`, `()->`, or similar shorthand instead of complete syntax.

## Do Not Use This Flow When

- The prompt does not clearly opt into shorthand conversion.
- The target file is missing or ambiguous.
- The user is asking for review, explanation, or brainstorming instead of an edit.
- There is no bounded shorthand block and no other clear shorthand marker to convert.

## Working Stance

Treat the shorthand as intent, not syntax. Your job is to preserve the collaborator's goal and
produce the best valid implementation for the target file:

- Preserve the collaborator's goal even when the wording is rough.
- Correct clearly broken syntax, APIs, methods, or terminology.
- Keep the implementation consistent with the target file and nearby code.
- Remove the shorthand markers and `()=>` lines after converting them.

## Prompt Shapes

### Minimal explicit form

```text
UPDATE CODE FROM SHORTHAND
#file:script.js
Use #file:index.html:94-99 to confirm where the rendered HTML should be inserted.
```

### CLI-style form

```text
quasi-coder --update #file:script.js --prompt
start-prompt:
Use #file:index.html:94-99 to confirm where the rendered HTML should be inserted.
end-prompt
```

If the collaborator forgot the `UPDATE CODE FROM SHORTHAND` or `quasi-coder` trigger, and it is not
immediately obvious that they intend shorthand conversion, ask whether they meant to use this flow
before applying these rules.

## Rules of Conversion

1. Find the target file named after the prompt prefix.
  - Prompt for target file if:
    - Ambiguous instructions
    - Not certain the target file passed is the correct file
2. Locate the section bounded by `${language:comment} start-shorthand` and
   `${language:comment} end-shorthand`.
3. Interpret each `()=>`, `()->`, `()-->`, and similar line as ideation, a quick gist, or general
  intent, not literal syntax.
4. Replace the shorthand with valid code, documentation, or data appropriate for the target file.
5. Remove helper comments such as `REMOVE COMMENT`, `NOTE`, or `// ()=> comment` when they are
  implementation scaffolding rather than intended final documentation.
6. If the prompt says `no need to edit code`, treat the target as a formatting or data-update task
  instead.
7. The final result should not contain shorthand markers or shorthand prefixes.
8. Have the user inspect diffs before accepting edits.

## Practical Example

### Prompt

```text
quasi-coder --update #file:script.js --prompt
start-prompt:
Use #file:index.html:94-99 to see where converted markdown to HTML will be parsed into `id="a"`.
end-prompt
```

### Source File Before Conversion

```js
// script.js
// Parse markdown file, applying HTML to render output.

var file = "file.md";
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
 if (this.readyState == 4 && this.status == 200) {
  let data = this.responseText;
  let a = document.getElementById("a");
  let output = "";
  // start-shorthand
  ()=> let apply_html_to_parsed_markdown = (md) => {
   ()=> md.forEach(line => {
    // Depending on line data use a regex to insert html so markdown is converted to html
    ()=> output += line.replace(/^(regex to add html elements from markdown line)(.*)$/g, $1$1);
   });
   // Output the converted file from markdown to html.
   return output;
  };
  ()=>a.innerHTML = apply_html_to_parsed_markdown(data);
  // end-shorthand
 }
};
xhttp.open("GET", file, true);
xhttp.send();
```

### Result After Conversion

```js
// script.js
// Parse markdown file, applying HTML to render output.

var file = "file.md";
var xhttp = new XMLHttpRequest();

function escapeHtml(value) {
 return value
  .replace(/&/g, "&amp;")
  .replace(/</g, "&lt;")
  .replace(/>/g, "&gt;")
  .replace(/\"/g, "&quot;")
  .replace(/'/g, "&#39;");
}

function renderMarkdownLine(line) {
 var headingMatch = line.match(/^(#{1,6})\s+(.*)$/);
 if (headingMatch) {
  var level = headingMatch[1].length;
  return "<h" + level + ">" + escapeHtml(headingMatch[2]) + "</h" + level + ">";
 }

 return "<p>" + escapeHtml(line) + "</p>";
}

xhttp.onreadystatechange = function() {
 if (this.readyState == 4 && this.status == 200) {
  var data = this.responseText;
  var target = document.getElementById("a");
  var html = data
   .split(/\r?\n/)
   .filter(function(line) {
    return line.trim() !== "";
   })
   .map(function(line) {
    return renderMarkdownLine(line);
   })
   .join("");

  target.innerHTML = html;
 }
};

xhttp.open("GET", file, true);
xhttp.send();
```

### What Improved

- The placeholder regex was replaced with explicit rendering logic.
- Markdown headings and plain paragraphs are handled separately.
- Output is HTML-escaped before insertion.
- The shorthand markers and `()=>` lines are removed from the final result.
- The collaborator's goal is preserved without copying the broken pseudo-code literally.

## Quick Checklist

- The prompt explicitly targets a file.
- The shorthand block was converted into valid output for the file type.
- `start-shorthand`, `end-shorthand`, and `()=>` lines were removed.
- Placeholder comments were removed or rewritten where needed.
- The final result matches the file's language and surrounding style.
