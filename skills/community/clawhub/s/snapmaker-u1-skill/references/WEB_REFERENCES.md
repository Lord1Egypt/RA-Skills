# Internet reference photos

When the user authorizes finding images online, search for downloadable originals of one clearly identified subject. A public example of a Jain sculpture or an actor demonstrates the workflow; another person's photos are not extra views of the user's face.

For a sculpture, prefer an official museum record or an original photographer's publication. Match the accession/object ID or the exact physical monument, pose, damage, base and surface details across views. Do not combine different statues depicting the same Jain figure. For an actor, confirm the named subject and recognize that changes of pose, expression, clothing, age and lighting can prevent geometric matching.

Preserve original files and a source manifest with the page and asset URLs, subject identity, photographer or institution, rights/license statement, view labels, download status and SHA-256. Keep full resolution and original framing for a photogrammetry capture set. Respect server retry instructions; metadata or thumbnails must not be mislabeled as successfully downloaded originals.

Inspect the images before selecting a reconstruction route:

- **Overlapping photos of the same static object:** consider native Apple Object Capture after checking coverage, consistency and the device. File count alone does not establish suitability.
- **Sparse front/back or other reference views:** use a tested multi-image generative engine when available. Label missing side surfaces as inferred. Two opposed photographs are not an overlapping 360° scan dataset.
- **Different objects, incompatible poses, screenshots or weak detail:** retain them as research/reference material and state the missing input. Do not silently build from an incompatible collection.

Use Apple Vision for subject isolation where appropriate, then inspect an alpha-composited full-frame preview and narrow gaps. Stored RGB values beneath fully transparent pixels are not visible input colors; assess the composited mask before diagnosing a fringe. Foreground extraction can still retain background or remove delicate details. A clean mask and a high input face-capture score do not validate generated likeness.

Preserve generated versus observed provenance. Rendered turntables of an existing 3D scan are synthetic views. A downloaded museum mesh is a reused scan. Either can be useful for explicit benchmarking or print preparation, but neither demonstrates reconstruction from newly sourced camera photographs.


Primary sources: [Met public-domain image fields](https://metmuseum.github.io/), [Apple capture guidance](https://developer.apple.com/documentation/realitykit/capturing-photographs-for-realitykit-object-capture/).
