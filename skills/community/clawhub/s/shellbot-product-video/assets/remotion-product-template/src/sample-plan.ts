import type {AidaPlan} from "./scene-types";

export const samplePlan: AidaPlan = {
  productName: "FlowPilot",
  cta: "Start your free trial now",
  incentive: "Get 20% off your first 3 months",
  scenes: [
    {
      id: "attention-problem",
      stage: "attention",
      durationInFrames: 150,
      headline: "Ops chaos slows every order fix",
      subheadline: "Issues are scattered across chats, sheets, and inboxes",
      voiceover: "Your team loses hours every week coordinating simple fixes.",
      assetHint: "high-contrast frustration visual"
    },
    {
      id: "interest-solution",
      stage: "interest",
      durationInFrames: 150,
      headline: "FlowPilot centralizes issue triage",
      subheadline: "One place to detect, route, and resolve incidents",
      voiceover: "FlowPilot unifies triage and routes urgent issues automatically.",
      assetHint: "product-context still or short clip"
    },
    {
      id: "desire-use-case-1",
      stage: "desire",
      durationInFrames: 120,
      headline: "Use case: Morning command center",
      subheadline: "Start each day with one ranked queue",
      voiceover: "Open one dashboard and prioritize the right work in minutes.",
      assetHint: "persona-in-context still"
    },
    {
      id: "desire-use-case-2",
      stage: "desire",
      durationInFrames: 120,
      headline: "Use case: Auto-escalation for urgent issues",
      subheadline: "Critical tickets reach owners instantly",
      voiceover: "Escalations are automatic, so high-impact issues do not sit idle.",
      assetHint: "short motion insert"
    },
    {
      id: "desire-use-case-3",
      stage: "desire",
      durationInFrames: 120,
      headline: "Use case: Weekly proof of impact",
      subheadline: "Share trend snapshots and outcomes with leadership",
      voiceover: "Weekly reviews show exactly what improved and why it mattered.",
      assetHint: "clean data-context still"
    },
    {
      id: "action-cta",
      stage: "action",
      durationInFrames: 150,
      headline: "Start your free trial now",
      subheadline: "Get 20% off your first 3 months",
      voiceover: "Start your free trial now and save twenty percent for three months.",
      assetHint: "subtle loop under CTA card"
    }
  ]
};
