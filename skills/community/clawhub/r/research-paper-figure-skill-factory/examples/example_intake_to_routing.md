# Example Intake to Routing

After the user confirms and provides material, produce:

1. visible current plan;
2. material intake summary;
3. initial figure need diagnosis;
4. taxonomy routing table;
5. default recommended figure type;
6. state update;
7. final next-question help including the unknown-next prompt.

Do not generate images in the same reply.


## v1.0.0 modality note

This example is text-only. It must not be followed by image generation in the same assistant response. If images are needed, the example should ask the user to confirm and leave generation to a later `IMAGE_ONLY` response.
