---
name: world-cup-2026-daily-prediction
description: Use when an agent needs to produce FIFA World Cup 2026 daily match predictions, next-48-hour previews, team-specific forecasts, odds/probability analysis, recent form checks, squad/injury context, or cited research briefs for upcoming World Cup fixtures.
---

# World Cup 2026 Daily Prediction

## Overview

Produce cited, current FIFA World Cup 2026 match prediction briefs. Treat predictions as probabilistic research, not betting advice. Always browse or query current sources before giving fixtures, odds, lineups, injuries, rankings, or recent results.

Chinese version: use `SKILL.zh-CN.md` when the user asks in Chinese or requests Chinese output.

## Daily Workflow

1. Establish the request scope: current date, user timezone, language, target window, and whether the user asked for all matches in the next 48 hours or a specific team.
2. Verify fixtures from an official or near-official schedule source before doing analysis. Prefer FIFA match centre/schedule for match date, kickoff, venue, teams, stage, and result status.
3. For each match, collect current evidence:
   - Market odds: gather at least two reputable sportsbook or odds-comparison sources when available. Record retrieval time, odds format, market, and whether prices are pre-match or live.
   - Ratings: check FIFA Men's Ranking, World Football Elo, Opta/Analyst power ratings, or another transparent team-strength source.
   - Recent form: review the last 5-10 relevant national-team matches, weighting competitive matches and strong opponents above friendlies.
   - Squad news: confirm squads, suspensions, injuries, likely or confirmed lineups, and manager news from official teams, FIFA, reputable sports desks, or lineup providers.
   - Match context: rest days, travel, venue, altitude/weather when material, home/host advantage, group table incentives, and knockout-stage rules.
4. Convert market odds into implied probabilities and remove bookmaker margin before comparing them with the model estimate. Use `references/prediction-method.md`.
5. Produce a forecast that separates market-implied probability from the agent's estimated probability. Include fair odds, confidence, key drivers, and uncertainty.
6. Cite all sources with access time. If a data point cannot be verified, say so and reduce confidence instead of filling gaps from memory.

## Team-Specific Requests

When the user names a team:

1. Resolve the team unambiguously, including country name variants in the user's language.
2. Check whether the team has a match in the next 48 hours. If yes, prioritize that match. If no, provide the next scheduled World Cup fixture and note that there is no match in the requested window.
3. Gather the same odds, ratings, recent form, squad, and context evidence as the daily workflow.
4. If the user asks for tournament outlook, add group/knockout path, qualification probability only if supported by current market or model sources, and avoid inventing bracket assumptions.

## Output Rules

Use concise tables for daily runs and short match cards for detail. Always include:

- `Fixture`: teams, stage/group, venue, kickoff in local tournament time and user timezone.
- `Market`: best available 1X2 odds, no-vig implied probabilities, and source timestamp.
- `Model`: win/draw/loss probabilities that sum to 100%, fair decimal odds, likely score range, and confidence.
- `Evidence`: 3-5 bullets covering ratings, form, squad availability, and contextual factors.
- `Cautions`: missing data, stale odds, lineup uncertainty, or weather/travel caveats.
- `Sources`: links used, with access time.
- `Disclaimer`: "Prediction is for informational analysis only, not financial or betting advice. Odds move quickly."

For full templates, use `references/output-templates.md`.

## Probability Discipline

Do not present predictions as certainties. Keep estimates calibrated:

- Prefer 90-minute regulation markets for group-stage and most knockout match previews unless the user asks about "to qualify" or outright markets.
- Use de-vigged market probabilities as an anchor, not as the final answer.
- Do not call something "value" unless the model estimate exceeds the no-vig market probability by at least 3-5 percentage points and the evidence quality is strong.
- Avoid extreme probabilities unless multiple independent sources agree and the mismatch is exceptional.
- State "no pick" when evidence is weak, odds are unavailable, or the forecast edge is smaller than normal market noise.

## Source Priority

Use `references/source-checklist.md` before research. In short:

1. Official FIFA and team sources for fixtures, squads, match status, and discipline.
2. Regulated sportsbooks, exchange markets, and odds aggregators for prices.
3. Transparent ratings and stats sources for team strength and recent performance.
4. Reputable sports news for injuries, lineups, and tactical context.

If sources conflict, prefer official fixture/result data and report the disagreement for odds, lineups, or ratings.

## Compliance

Respect local laws and platform policy. Do not encourage illegal gambling, underage gambling, guaranteed-profit claims, chasing losses, or staking systems. If the user asks for bet sizing, steer back to probability, risk, and responsible-gambling framing.
