import { Config } from "@remotion/cli/config";

// Same settings as render.mjs so Studio renders match.
Config.setVideoImageFormat("jpeg");
Config.setPixelFormat("yuv420p");
Config.setCodec("h264");
Config.setCrf(18);
