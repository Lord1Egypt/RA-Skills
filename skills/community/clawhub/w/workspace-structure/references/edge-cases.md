# Edge cases

This file covers ambiguous placement cases that often cause inconsistent behavior.

## Manufacturer's PDF documentation for the user's equipment: user-files/ or sources/?

This PDF is external vendor documentation and does not have a direct personal connection to the user. Prefer `sources/`.

## Photos from the user's journey: user-files/ or entertainment/?

If the photoset is a user-owned set of files being kept as content, memory aid, evidence, or document-like personal/work material, prefer `user-files/`.

## Audio or video file the user likes: user-files/ or entertainment/?

Prefer `entertainment/` for the media file itself when it is kept mainly for listening, watching, or reading for enjoyment.
Prefer `user-files/` for lists, notes, rankings, or derived artifacts that are directly about the user's preferences.

## Screenshot for one project: temp/ or projects/?

If the screenshot belongs to one project and you are unsure whether it will remain temporary, prefer that project's folder rather than `temp/`.

## One-off analytical deliverable: reports/ or projects/?

Use `reports/` when the output is a standalone report, deck, or research summary without a broader project context.
Use `projects/` when the output belongs to an ongoing body of work with related source files, drafts, or expected follow-up.

## CSV with business data: apps/, user-files/, data/, projects/ or reports/?

Use `apps/` if the CSV is part of an installed application's persistent working data; follow the application's configured storage layout.
Use `projects/` if the CSV belongs to one existing project.
Use `reports/` if the CSV is a one-off report generated from a database or application, or forms part of a standalone deliverable.
Use `data/` if it is part of an independent or shared durable structured store or maintained data workflow.
Use `user-files/` if it is independent personal material rather than a generic export.

A useful test for personal meaning is: if you remove the specific user from the picture, does the file lose its meaning? This helps distinguish personal material from generic data, but does not override its role as an application's working record.

## Registry of user belongings: apps/, user-files/ or data/?

Choose based on how it functions:
- if it is the working registry owned by an installed application, its location is defined by the application;
- if it is kept as a standalone personal document rather than maintained as a structured store, use `user-files/`;
- if it functions as an independent or shared durable structured store, use `data/`. Direct access by an AI agent does not, by itself, make it part of a separate application.

## File seems both reference and project material

If the file is mainly used within one project, keep it in the project.
If it is reused across many tasks and acts as a durable lookup source, prefer `reference/`.

## Assistant-acquired external file: downloads/ or final destination?

If the file has just been acquired from an outside source and has not yet been classified, placing it in `downloads/` first is the default and usually the safest choice. 
If the final category is immediately obvious, placing it there directly is also acceptable.
Once the final category is clear, place or move the file accordingly.

## Popular science book: sources/ or entertainment/?

Use purpose of use as the deciding factor.
If the material is kept primarily for work, hobby, reference, or project use, prefer `sources/`.
If it is kept primarily for enjoyment, prefer `entertainment/`.
A documentary, podcast, or nonfiction book can reasonably go either way depending on why it is being kept.

## Internet research result you conducted for a user request: reports/ or sources/?

If the file is the result of your own search or synthesis for one task, prefer `reports/`.
If the file is an outside source you are keeping as input material, prefer `sources/`.

## Reusable script created during a project: scripts/ or project folder?

If it only serves development work within one project, keep it in that project. 
If it becomes a standalone helper reusable across contexts, promote the stable production-ready version to `scripts/`. 
If it remains part of an installed application, keep it with that application.

## Development tree and installed product: projects/ or apps/?

For a hypothetical product called `ExampleApp`, use `projects/example-app/` for requirements, research, design, development source, tests, and release preparation; use `apps/ExampleApp/` for the installed version and its operational artifacts.

