# Output Templates / 输出模板

Use the user's language by default. Keep tables compact; move details into match cards only for the highest-interest matches or when the user asks.

## English Daily Brief

```markdown
As of {access_time} ({timezone}), I found {match_count} FIFA World Cup 2026 match(es) in the next 48 hours.

| Kickoff | Match | Market no-vig 1X2 | Model 1X2 | Lean | Confidence | Likely scores |
|---|---|---:|---:|---|---|---|
| {date_time} | {team_a} vs {team_b} | {home}/{draw}/{away} | {home}/{draw}/{away} | {lean_or_no_pick} | {High/Medium/Low} | {scores} |

### {Team A} vs {Team B}

- Fixture: {stage/group}, {venue}, kickoff {local_time}; user time {user_time}.
- Market: {odds_summary}; no-vig probabilities {probabilities}; checked {timestamp}.
- Model: {home}% / {draw}% / {away}%; fair odds {fair_odds}.
- Key evidence: {ratings}; {recent_form}; {squad_news}; {context}.
- Cautions: {missing_or_uncertain_data}.

Sources: {links}

Prediction is for informational analysis only, not financial or betting advice. Odds move quickly.
```

## Chinese Daily Brief / 中文每日简报

```markdown
截至 {access_time}（{timezone}），我查到未来 48 小时有 {match_count} 场 2026 世界杯比赛。

| 开球时间 | 比赛 | 市场去水 1X2 | 模型 1X2 | 倾向 | 信心 | 可能比分 |
|---|---|---:|---:|---|---|---|
| {date_time} | {team_a} vs {team_b} | {home}/{draw}/{away} | {home}/{draw}/{away} | {lean_or_no_pick} | {高/中/低} | {scores} |

### {team_a} vs {team_b}

- 赛程：{stage/group}，{venue}，当地 {local_time} 开球；用户时区 {user_time}。
- 市场：{odds_summary}；去水概率 {probabilities}；查询时间 {timestamp}。
- 模型：{home}% / {draw}% / {away}%；公平赔率 {fair_odds}。
- 关键依据：{ratings}；{recent_form}；{squad_news}；{context}。
- 风险提示：{missing_or_uncertain_data}。

来源：{links}

预测仅供信息分析，不构成财务或投注建议；赔率会快速变化。
```

## Team-Specific Template

```markdown
## {team} World Cup 2026 Forecast

- Next verified fixture: {opponent}, {stage/group}, {kickoff}, {venue}.
- Next 48 hours: {has_match_or_no_match}.
- Current market: {odds_and_no_vig_probability}.
- Team strength: {ranking_or_rating_summary}.
- Recent form: {last_5_to_10_summary}.
- Squad context: {availability_or_lineup_summary}.
- Prediction: {win_draw_loss_probability}; fair odds {fair_odds}; confidence {confidence}.
- Practical read: {one_sentence_summary_or_no_pick}.

Sources checked at {timestamp}: {links}
```

## Minimal Answer When Data Is Missing

```markdown
I can verify the fixture, but I cannot verify current odds from reliable sources right now. I will give a lower-confidence ratings/form forecast and label the market section unavailable.
```
