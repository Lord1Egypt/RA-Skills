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

## CSV with business data: user-files/, data/, projects/ or reports/?

Use `projects/` if the CSV belongs to one existing project.
Use `reports/` if the CSV is a one-off report generated from a database or is itself part of a standalone deliverable.
Use `data/` if it is part of a durable structured store or maintained as part of a real data workflow.

Use `user-files/` only if the file has a direct personal connection to the user rather than being a generic export.
A useful test is: if you remove the specific user from the picture, does the file lose its meaning? If yes, `user-files/` becomes much more likely.

## Registry of user belongings: user-files/ or data/?

Choose based on how it functions:
- if it is a user-owned standalone file with a direct personal connection to the user, `user-files/`;
- if it functions as part of a durable structured data store, `data/`.

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

If it only serves that one project, keeping it inside the project is fine.
If it becomes reusable across contexts, keep drafting inside the project and promote only the stable production-ready version to `scripts/`.
