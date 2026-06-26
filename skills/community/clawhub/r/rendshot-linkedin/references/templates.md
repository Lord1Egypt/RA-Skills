# LinkedIn Recommended Templates

Use `list_templates({ platform: "linkedin_post" })` to browse all available templates.

## By Content Type

### Company Announcement
- Search: `list_templates({ platform: "linkedin_post", q: "announcement milestone" })`
- Variables: `title`, `subtitle`, `company_logo`, `metrics`
- Style: Corporate Professional

### Carousel Slide
- Search: `list_templates({ platform: "linkedin_post", q: "carousel slide" })`
- Variables: `slide_number`, `title`, `body`, `accent_color`
- Style: Consistent with cover slide

### Thought Leadership Quote
- Search: `list_templates({ platform: "linkedin_post", q: "quote insight" })`
- Variables: `quote`, `author_name`, `author_title`, `avatar`
- Style: Warm Thought Leader

### Data / Report
- Search: `list_templates({ platform: "linkedin_post", q: "data report" })`
- Variables: `metric`, `value`, `context`, `chart_type`
- Style: Data-Driven

## Prompt Examples

### Series A Announcement
```
generate_image({
  prompt: "LinkedIn announcement post, professional navy gradient background, large white title 'We just raised $5M', subtitle 'Series A led by Sequoia', three metric cards showing '50K users' '3x ARR growth' '20 team members', company logo top-left, clean corporate design",
  platform: "linkedin_post",
  locale: "en"
})
```

### Carousel Cover
```
generate_image({
  prompt: "LinkedIn carousel cover slide, '7 Hiring Mistakes That Cost Us $500K', warm professional palette, large bold title, author avatar placeholder bottom-left with name and title, slide count '1/8' bottom-right",
  platform: "linkedin_post",
  locale: "en"
})
```

### Data Insight
```
generate_image({
  prompt: "LinkedIn data visualization post, clean white background, central large number '73%' in dark blue, subtitle 'of remote workers are more productive at home', bar chart showing trend below, source 'Gallup 2025' at bottom, professional and clean",
  platform: "linkedin_post",
  locale: "en"
})
```

### Hiring Post
```
generate_image({
  prompt: "LinkedIn hiring post, company brand style, title 'We are Hiring' in bold, three open role cards showing 'Senior Engineer' 'Product Manager' 'Designer', company logo centered at top, modern blue and white palette, 'Apply now' CTA at bottom",
  platform: "linkedin_post",
  locale: "en"
})
```
