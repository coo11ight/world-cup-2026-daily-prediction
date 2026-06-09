# Prediction Method / 预测方法

Use this method as a disciplined baseline. Adjust weights only when sources are missing or match context clearly demands it.

## Odds Conversion

Decimal odds to raw implied probability:

```text
raw_probability = 1 / decimal_odds
```

American odds to decimal:

```text
positive: decimal = 1 + american / 100
negative: decimal = 1 + 100 / abs(american)
```

Remove bookmaker margin for a 1X2 market:

```text
raw_home = 1 / home_decimal
raw_draw = 1 / draw_decimal
raw_away = 1 / away_decimal
overround = raw_home + raw_draw + raw_away
no_vig_home = raw_home / overround
no_vig_draw = raw_draw / overround
no_vig_away = raw_away / overround
```

Fair decimal odds from model probability:

```text
fair_decimal = 1 / model_probability
```

## Baseline Weights

When all evidence is available:

| Factor | Weight |
|---|---:|
| No-vig market probability | 40% |
| Team ratings and ranking strength | 25% |
| Recent form and match quality | 15% |
| Squad availability and lineup news | 10% |
| Match context | 10% |

When odds are missing:

| Factor | Weight |
|---|---:|
| Team ratings and ranking strength | 40% |
| Recent form and match quality | 25% |
| Squad availability and lineup news | 20% |
| Match context | 15% |

When confirmed lineups are available near kickoff, shift up to 10 percentage points from market/form into squad availability if the lineup materially changes team strength.

## Calibration Rules

- Probabilities must sum to 100%.
- Default to 90-minute regulation 1X2 unless the user asks for "to qualify", extra time, penalties, or outright markets.
- Treat the draw as a real outcome. Do not compress every preview into a win/lose pick.
- Avoid high confidence if odds were checked from only one source, lineups are unconfirmed, or key players have uncertain status.
- Use confidence labels:
  - High: multiple independent sources agree, stable odds, strong team-strength edge, no major lineup uncertainty.
  - Medium: evidence mostly agrees but one major input is uncertain.
  - Low: missing odds, conflicting reports, volatile lineups, or small probability edge.

## Reasonable Output Ranges

These are guardrails, not hard limits:

- Strong favorite in group-stage 1X2: often 55-70%; rarely above 75% unless mismatch is extreme.
- Competitive match: draw often remains 22-30%.
- Heavy underdog: do not assign near-zero chances; international football has high variance.
- Correct score predictions are low-confidence. Present 2-3 likely scorelines, not one guaranteed score.

## Value Language

Use "market disagreement" or "possible value" only when:

1. The model probability exceeds no-vig market probability by at least 3-5 percentage points.
2. Odds were checked recently from reliable sources.
3. The evidence edge is explainable by ratings, form, squad, or context.

Never imply guaranteed profit. If the edge is smaller than normal odds movement, say "no clear edge".

## Chinese Quick Notes / 中文速记

- 先用市场去水概率做锚点，再结合评分、状态、阵容和背景调整。
- 预测结果必须胜/平/负合计 100%。
- 公平赔率 = `1 / 模型概率`。
- 只有模型概率比市场去水概率高 3-5 个百分点以上，才可谨慎说「可能有价值」。
- 比分预测波动很大，应给 2-3 个可能比分，而不是绝对结论。
