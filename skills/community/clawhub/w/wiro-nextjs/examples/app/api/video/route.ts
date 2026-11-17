// app/api/video/route.ts
import { runModel, uploadFile } from '../../../lib/wiro';

export const maxDuration = 60;

/**
 * Image to video with Seedance 1 Pro Fast: $0.05 for 5 seconds at 480p.
 * Send every required input; Wiro fills in only the optional ones you leave out.
 */
export async function POST(request: Request) {
  const form = await request.formData().catch(() => null);
  const prompt = form?.get('prompt');
  const image = form?.get('image');
  if (typeof prompt !== 'string' || !prompt.trim() || !(image instanceof File) || !image.type.startsWith('image/')) {
    return Response.json({ error: 'Send a prompt and an image.' }, { status: 400 });
  }
  try {
    const imageUrl = await uploadFile(image); // any public https URL works too
    const webhook = process.env.APP_URL ? new URL('/api/wiro-webhook', process.env.APP_URL).toString() : undefined;
    const token = await runModel('bytedance/seedance-v1-pro-fast', {
      prompt,
      inputImage: [imageUrl], // a combinefileinput takes its URLs in the field itself
      resolution: '480p',
      ratio: 'adaptive',
      duration: '5',
      ...(webhook ? { callbackUrl: webhook } : {}), // public URLs only; on localhost, poll
    });
    return Response.json({ token });
  } catch (error) {
    console.error(error);
    return Response.json({ error: 'Could not start the video.' }, { status: 502 });
  }
}
