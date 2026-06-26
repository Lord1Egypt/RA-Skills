import { NextRequest, NextResponse } from "next/server";
import { PublicKey } from "@solana/web3.js";
import {
  fetchTicketFromChain,
  fetchGameFromChain,
  computeTicketStatus,
  flipToStr,
  SURVIVAL_FLIPS,
  PREDICTIONS_SIZE,
} from "@/lib/solana";

export const dynamic = "force-dynamic";

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const wallet = searchParams.get("wallet");
  const roundParam = searchParams.get("round");

  if (!wallet) {
    return NextResponse.json(
      { error: "Missing 'wallet' query parameter" },
      { status: 400 }
    );
  }

  let playerPubkey: PublicKey;
  try {
    playerPubkey = new PublicKey(wallet);
  } catch {
    return NextResponse.json(
      { error: "Invalid wallet address" },
      { status: 400 }
    );
  }

  try {
    const game = await fetchGameFromChain();
    const currentRound = game?.currentRound ?? 0;

    let round: number | null = null;

    if (roundParam !== null) {
      round = parseInt(roundParam, 10);
      if (isNaN(round) || round < 0) {
        return NextResponse.json(
          { error: "Invalid 'round' parameter" },
          { status: 400 }
        );
      }
    }

    // If round provided, look up directly; otherwise search recent
    let ticket = null;

    if (round !== null) {
      ticket = await fetchTicketFromChain(playerPubkey, round);
    } else {
      // Search backwards from current round
      for (let r = currentRound; r >= Math.max(0, currentRound - 30); r--) {
        const result = await fetchTicketFromChain(playerPubkey, r);
        if (result) {
          ticket = result;
          round = r;
          break;
        }
      }
    }

    if (!ticket || !game) {
      return NextResponse.json(
        {
          found: false,
          wallet,
          round,
          message: round !== null
            ? `No ticket found for this wallet at round #${round}`
            : "No recent ticket found for this wallet",
        },
        { status: 200 }
      );
    }

    const status = computeTicketStatus(game, ticket);

    return NextResponse.json({
      found: true,
      status: status.status,
      wallet: ticket.player.toBase58(),
      round: ticket.round,

      predictionsAll: ticket.predictions.map(flipToStr).join(""),
      predictionsSurvival: ticket.predictions.slice(0, SURVIVAL_FLIPS).map(flipToStr).join(""),
      predictionsExtra: ticket.predictions.slice(SURVIVAL_FLIPS, PREDICTIONS_SIZE).map(flipToStr).join(""),
      totalPredictions: PREDICTIONS_SIZE,

      flipped: status.flipped,
      survived: status.survived,
      score: status.score,
      maxScore: SURVIVAL_FLIPS,

      winner: ticket.winner,
      collected: ticket.collected,

      comparisons: status.comparisons,

      summary: ticket.winner
        ? ticket.collected
          ? `WINNER! Collected entire jackpot.`
          : `WINNER! Awaiting collection.`
        : !status.flipped
          ? `Waiting for round #${ticket.round} to be flipped.`
          : status.survived && status.score === SURVIVAL_FLIPS
            ? `All ${SURVIVAL_FLIPS} correct! Claim available.`
            : `Eliminated. Scored ${status.score}/${SURVIVAL_FLIPS}.`,
    });
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json(
      { error: "Failed to fetch ticket", details: message },
      { status: 500 }
    );
  }
}
