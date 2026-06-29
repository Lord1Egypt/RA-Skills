# Assets Directory

Screenshot images (bar-chart.jpg, help-screen.jpg, pie-chart.jpg, wordcloud.jpg)
are embedded as base64 data URIs in the project [README.md](../README.md).

This is necessary because ClawHub blocks binary image file uploads (.jpg, .png)
at the server level — `.clawhubignore` negation patterns cannot override this filter.
