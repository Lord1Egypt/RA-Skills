--[[
hide-details-for-pdf.lua
Pandoc Lua filter to hide HTML <details> blocks when generating PDF

PURPOSE:
When converting Markdown to PDF, this filter removes <details>...</details>
blocks entirely. These blocks often contain source code (like graph-easy
source) that is useful for regeneration in markdown but clutters PDF output.

USAGE:
  pandoc input.md -o output.pdf --lua-filter=hide-details-for-pdf.lua

The filter checks FORMAT to only apply when outputting to LaTeX/PDF,
preserving <details> blocks for HTML output.

AUTHOR: Claude Code (cc-skills plugin)
VERSION: 1.0.0
]]

-- Track whether we're inside a details block
local in_details = false
local details_depth = 0

-- Handle raw HTML blocks
function RawBlock(el)
  if FORMAT:match("latex") or FORMAT:match("pdf") then
    if el.format == "html" then
      -- Check for opening <details> tag
      if el.text:match("<details[^>]*>") then
        details_depth = details_depth + 1
        in_details = true
        return {}  -- Remove the opening tag
      end
      -- Check for closing </details> tag
      if el.text:match("</details>") then
        details_depth = details_depth - 1
        if details_depth <= 0 then
          in_details = false
          details_depth = 0
        end
        return {}  -- Remove the closing tag
      end
      -- If we're inside details, remove the content
      if in_details then
        return {}
      end
    end
  end
  return el
end

-- Handle inline HTML elements
function RawInline(el)
  if FORMAT:match("latex") or FORMAT:match("pdf") then
    if el.format == "html" then
      if el.text:match("<details[^>]*>") or el.text:match("</details>") or
         el.text:match("<summary[^>]*>") or el.text:match("</summary>") then
        return {}
      end
    end
  end
  return el
end

-- Handle blocks that might be inside details
function Block(el)
  if FORMAT:match("latex") or FORMAT:match("pdf") then
    if in_details then
      return {}
    end
  end
  return el
end

-- Handle divs that Pandoc might create from details
function Div(el)
  if FORMAT:match("latex") or FORMAT:match("pdf") then
    -- Check for details class or data attribute
    if el.classes:includes("details") then
      return {}
    end
  end
  return el
end
