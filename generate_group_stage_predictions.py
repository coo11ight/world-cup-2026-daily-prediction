#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026 FIFA World Cup Group Stage Prediction Generator
基于真实 Elo 评分生成全部小组赛概率预测，并输出可回测的 CSV/Markdown

数据来源：
- 分组/球队：2026 FIFA World Cup 官方抽签（2025-12-05 华盛顿）+ 2026-03 附加赛结果
- 球队评分：World Football Elo Ratings (eloratings.net, 2026-06-08)
- 东道主优势：美加墨三国东道主及中北美地缘加成
"""

import csv
import math
import sys
import os
from datetime import datetime, timedelta

# Windows 终端 UTF-8 支持
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================
# 1. 球队实力评分（World Football Elo Ratings, 2026-06-08）
# ============================================================
TEAM_RATINGS = {
    # Pot 1（种子队：世界排名前九 + 三位东道主）
    "Spain": 2155,
    "Argentina": 2114,
    "France": 2063,
    "England": 2021,
    "Brazil": 1991,
    "Portugal": 1986,
    "Colombia": 1977,
    "Netherlands": 1944,
    "Germany": 1932,
    "Belgium": 1893,
    "Uruguay": 1892,
    "Switzerland": 1891,
    "Mexico": 1875,   # 东道主
    "Senegal": 1867,
    "USA": 1726,      # 东道主
    "Canada": 1788,   # 东道主

    # Pot 2
    "Norway": 1917,
    "Turkey": 1911,
    "Croatia": 1908,
    "Japan": 1906,
    "Morocco": 1824,
    "Paraguay": 1833,
    "Austria": 1830,
    "South Korea": 1758,
    "Iran": 1772,
    "Australia": 1777,
    "Algeria": 1760,
    "Ecuador": 1935,

    # Pot 3
    "Scotland": 1782,
    "Sweden": 1712,
    "Uzbekistan": 1718,
    "Tunisia": 1628,
    "Egypt": 1696,
    "Ivory Coast": 1695,
    "Jordan": 1685,
    "Saudi Arabia": 1569,
    "New Zealand": 1562,
    "Haiti": 1548,
    "South Africa": 1528,
    "Ghana": 1510,

    # Pot 4（含附加赛晋级球队）
    "Czechia": 1740,
    "Bosnia and Herzegovina": 1595,
    "Cape Verde": 1578,
    "Iraq": 1618,
    "DR Congo": 1661,
    "Panama": 1730,
    "Qatar": 1421,
    "Curacao": 1434,
}

# 东道主及中北美地缘优势（以 Elo 点数加成，全赛事生效）
HOST_ADVANTAGE = {
    "Mexico": 80,   # 东道主 + 高原主场
    "USA": 70,      # 东道主
    "Canada": 70,   # 东道主
    "Panama": 25,   # 中北美地缘
    "Haiti": 20,    # 中北美地缘
    "Curacao": 15,  # 中北美地缘
}

# ============================================================
# 2. 分组（2026 扩军后 12 组 × 4 队，官方抽签结果 + 附加赛胜者）
# ============================================================
GROUPS = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["USA", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

# ============================================================
# 3. 赛程模板（每组 6 场，对应 3 轮）
# ============================================================
MATCH_DAYS = [
    # Round 1 (12 组 × 2 场 = 24 场，6 月 11-16 日，每天 4 场)
    ("A", 0, 1), ("A", 2, 3),  # Jun 11
    ("B", 0, 1), ("B", 2, 3),  # Jun 11
    ("C", 0, 1), ("C", 2, 3),  # Jun 12
    ("D", 0, 1), ("D", 2, 3),  # Jun 12
    ("E", 0, 1), ("E", 2, 3),  # Jun 13
    ("F", 0, 1), ("F", 2, 3),  # Jun 13
    ("G", 0, 1), ("G", 2, 3),  # Jun 14
    ("H", 0, 1), ("H", 2, 3),  # Jun 14
    ("I", 0, 1), ("I", 2, 3),  # Jun 15
    ("J", 0, 1), ("J", 2, 3),  # Jun 15
    ("K", 0, 1), ("K", 2, 3),  # Jun 16
    ("L", 0, 1), ("L", 2, 3),  # Jun 16

    # Round 2 (12 组 × 2 场 = 24 场，6 月 17-22 日，每天 4 场)
    ("A", 0, 2), ("A", 1, 3),  # Jun 17
    ("B", 0, 2), ("B", 1, 3),  # Jun 17
    ("C", 0, 2), ("C", 1, 3),  # Jun 18
    ("D", 0, 2), ("D", 1, 3),  # Jun 18
    ("E", 0, 2), ("E", 1, 3),  # Jun 19
    ("F", 0, 2), ("F", 1, 3),  # Jun 19
    ("G", 0, 2), ("G", 1, 3),  # Jun 20
    ("H", 0, 2), ("H", 1, 3),  # Jun 20
    ("I", 0, 2), ("I", 1, 3),  # Jun 21
    ("J", 0, 2), ("J", 1, 3),  # Jun 21
    ("K", 0, 2), ("K", 1, 3),  # Jun 22
    ("L", 0, 2), ("L", 1, 3),  # Jun 22

    # Round 3（同组同时开球，6 月 24-27 日，每天 6 场 = 3 组）
    ("A", 0, 3), ("A", 1, 2), ("B", 0, 3), ("B", 1, 2), ("C", 0, 3), ("C", 1, 2),  # Jun 24
    ("D", 0, 3), ("D", 1, 2), ("E", 0, 3), ("E", 1, 2), ("F", 0, 3), ("F", 1, 2),  # Jun 25
    ("G", 0, 3), ("G", 1, 2), ("H", 0, 3), ("H", 1, 2), ("I", 0, 3), ("I", 1, 2),  # Jun 26
    ("J", 0, 3), ("J", 1, 2), ("K", 0, 3), ("K", 1, 2), ("L", 0, 3), ("L", 1, 2),  # Jun 27
]

START_DATE = datetime(2026, 6, 11)


def get_match_date(match_index):
    """根据比赛序号返回日期。第三轮为 6 月 24-27 日，每天 6 场。"""
    if match_index < 24:
        return START_DATE + timedelta(days=match_index // 4)
    elif match_index < 48:
        return START_DATE + timedelta(days=6 + (match_index - 24) // 4)
    else:
        day_offset = 13 + (match_index - 48) // 6
        return START_DATE + timedelta(days=day_offset)


# ============================================================
# 4. 概率模型
# ============================================================
def compute_probabilities(team1, team2, neutral=False):
    r1 = TEAM_RATINGS.get(team1, 1500)
    r2 = TEAM_RATINGS.get(team2, 1500)

    adv1 = HOST_ADVANTAGE.get(team1, 0) if not neutral else 0
    adv2 = HOST_ADVANTAGE.get(team2, 0) if not neutral else 0

    diff = (r1 + adv1) - (r2 + adv2)

    w1_raw = 1.0 / (1.0 + 10 ** (-diff / 400.0))
    w2_raw = 1.0 / (1.0 + 10 ** (diff / 400.0))

    # 平局概率：实力越接近平局概率越高，强强对话也不会太低
    draw = 0.25 * math.exp(-(diff / 350.0) ** 2)
    draw = max(0.15, min(0.30, draw))

    rem = 1.0 - draw
    total_raw = w1_raw + w2_raw
    w1 = rem * (w1_raw / total_raw)
    w2 = rem * (w2_raw / total_raw)

    s = w1 + draw + w2
    w1, draw, w2 = w1 / s, draw / s, w2 / s

    return round(w1, 4), round(draw, 4), round(w2, 4)


def fair_odds(prob):
    if prob <= 0:
        return 999.0
    return round(1.0 / prob, 2)


def confidence_label(p1, d, p2):
    entropy = -(p1 * math.log2(p1 + 1e-9) + d * math.log2(d + 1e-9) + p2 * math.log2(p2 + 1e-9))
    max_entropy = math.log2(3)
    norm = entropy / max_entropy
    if norm < 0.78:
        return "High"
    elif norm < 0.86:
        return "Medium"
    return "Low"


def expected_goals(team1, team2):
    """
    基于两队 Elo 差（含东道主加成）计算预期进球。
    强队不仅胜率更高，而且预期进球更多、失球更少；
    弱队面对强队时预期进球会被压缩到较低水平。
    """
    r1 = TEAM_RATINGS.get(team1, 1500) + HOST_ADVANTAGE.get(team1, 0)
    r2 = TEAM_RATINGS.get(team2, 1500) + HOST_ADVANTAGE.get(team2, 0)

    p_win = 1.0 / (1.0 + 10 ** (-(r1 - r2) / 400.0))

    # 势均力敌的比赛往往更开放；强弱悬殊的比赛强队多进球、弱队少进球
    base_total = 2.55 - 0.35 * abs(p_win - 0.5)

    # 按获胜概率分配总进球，强队份额更高
    g1 = base_total * p_win * 1.25
    g2 = base_total * (1 - p_win) * 1.25

    g1 = max(0.5, min(g1, 3.2))
    g2 = max(0.3, min(g2, 2.6))

    return round(g1, 2), round(g2, 2)


def most_likely_score(g1, g2, p1, d, p2):
    """
    将预期进球四舍五入得到最可能比分，并确保与 1/X/2 预测方向一致。
    若四舍五入后出现平局但与预测方向冲突，做最小改动（通常是 2-2 → 2-1 或 1-2），
    避免所有比赛都输出 1-1，也避免弱队被强行打出大比分。
    """
    s1 = round(g1)
    s2 = round(g2)

    if p1 > max(d, p2):
        if s1 <= s2:
            s2 = max(0, s2 - 1) if s2 > 0 else 0
            if s1 <= s2:
                s1 = s2 + 1
    elif p2 > max(p1, d):
        if s2 <= s1:
            s1 = max(0, s1 - 1) if s1 > 0 else 0
            if s2 <= s1:
                s2 = s1 + 1
    else:
        # 平局预测：取相同且尽量接近预期的整数
        if s1 != s2:
            target = min(s1, s2)
            s1 = s2 = target

    return f"{s1}-{s2}"


# ============================================================
# 5. 生成全部比赛
# ============================================================
all_matches = []
match_id = 1

for idx, (group, i, j) in enumerate(MATCH_DAYS):
    t1 = GROUPS[group][i]
    t2 = GROUPS[group][j]
    date = get_match_date(idx)
    p1, d, p2 = compute_probabilities(t1, t2, neutral=False)
    g1, g2 = expected_goals(t1, t2)
    conf = confidence_label(p1, d, p2)

    all_matches.append({
        "match_id": f"G{group}{match_id:03d}",
        "date": date.strftime("%Y-%m-%d"),
        "group": group,
        "team1": t1,
        "team2": t2,
        "team1_rating": TEAM_RATINGS[t1],
        "team2_rating": TEAM_RATINGS[t2],
        "team1_win": p1,
        "draw": d,
        "team2_win": p2,
        "team1_fair_odds": fair_odds(p1),
        "draw_fair_odds": fair_odds(d),
        "team2_fair_odds": fair_odds(p2),
        "confidence": conf,
        "predicted_result": "1" if p1 > max(d, p2) else ("X" if d > max(p1, p2) else "2"),
        "team1_exp_goals": g1,
        "team2_exp_goals": g2,
        "most_likely_score": most_likely_score(g1, g2, p1, d, p2),
    })
    match_id += 1

# ============================================================
# 6. 输出 CSV（用于回测）
# ============================================================
CSV_PATH = "group_stage_predictions.csv"
with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "match_id", "date", "group", "team1", "team2",
        "team1_rating", "team2_rating",
        "team1_win", "draw", "team2_win",
        "team1_fair_odds", "draw_fair_odds", "team2_fair_odds",
        "confidence", "predicted_result",
        "team1_exp_goals", "team2_exp_goals", "most_likely_score"
    ])
    writer.writeheader()
    writer.writerows(all_matches)

print(f"已生成 {len(all_matches)} 场比赛预测 -> {CSV_PATH}")

# ============================================================
# 7. 小组赛排名模拟（蒙特卡洛）
# ============================================================
print("\n=== 小组赛期望积分与概率最大排名 ===\n")


def simulate_group(group_name, teams, matches_in_group):
    import random
    stats = {t: {"w": 0, "d": 0, "l": 0, "pts": 0.0, "gf": 0.0, "ga": 0.0} for t in teams}
    rank_counts = {t: {1: 0, 2: 0, 3: 0, 4: 0} for t in teams}

    probs = {}
    for m in matches_in_group:
        probs[(m["team1"], m["team2"])] = (m["team1_win"], m["draw"], m["team2_win"])

    N = 20000
    for _ in range(N):
        table = {t: {"pts": 0, "gf": 0, "ga": 0, "gd": 0} for t in teams}
        for m in matches_in_group:
            p1, d, p2 = probs[(m["team1"], m["team2"])]
            r = random.random()
            if r < p1:
                table[m["team1"]]["pts"] += 3
                table[m["team1"]]["gf"] += max(1, round(m["team1_exp_goals"]))
                table[m["team2"]]["ga"] += max(1, round(m["team1_exp_goals"]))
                table[m["team2"]]["gf"] += max(0, round(m["team2_exp_goals"]))
                table[m["team1"]]["ga"] += max(0, round(m["team2_exp_goals"]))
            elif r < p1 + d:
                table[m["team1"]]["pts"] += 1
                table[m["team2"]]["pts"] += 1
                g1 = max(0, round(m["team1_exp_goals"]))
                g2 = max(0, round(m["team2_exp_goals"]))
                table[m["team1"]]["gf"] += g1
                table[m["team1"]]["ga"] += g2
                table[m["team2"]]["gf"] += g2
                table[m["team2"]]["ga"] += g1
            else:
                table[m["team2"]]["pts"] += 3
                table[m["team2"]]["gf"] += max(1, round(m["team2_exp_goals"]))
                table[m["team1"]]["ga"] += max(1, round(m["team2_exp_goals"]))
                table[m["team1"]]["gf"] += max(0, round(m["team1_exp_goals"]))
                table[m["team2"]]["ga"] += max(0, round(m["team1_exp_goals"]))

        for t in teams:
            table[t]["gd"] = table[t]["gf"] - table[t]["ga"]

        sorted_teams = sorted(teams, key=lambda t: (table[t]["pts"], table[t]["gd"], table[t]["gf"]), reverse=True)
        for rank, t in enumerate(sorted_teams, 1):
            rank_counts[t][rank] += 1
            stats[t]["pts"] += table[t]["pts"]
            stats[t]["gf"] += table[t]["gf"]
            stats[t]["ga"] += table[t]["ga"]

    for t in teams:
        stats[t]["pts"] /= N
        stats[t]["gf"] /= N
        stats[t]["ga"] /= N
        stats[t]["top2"] = (rank_counts[t][1] + rank_counts[t][2]) / N
        stats[t]["top3"] = (rank_counts[t][1] + rank_counts[t][2] + rank_counts[t][3]) / N

    most_likely_rank = {}
    for t in teams:
        most_likely_rank[t] = max(rank_counts[t], key=rank_counts[t].get)

    return stats, rank_counts, most_likely_rank


group_results = {}
for g, teams in GROUPS.items():
    matches_in_group = [m for m in all_matches if m["group"] == g]
    stats, rank_counts, mlr = simulate_group(g, teams, matches_in_group)
    group_results[g] = {"stats": stats, "rank_counts": rank_counts, "most_likely_rank": mlr}

    print(f"【{g} 组】")
    for t in teams:
        r = mlr[t]
        prob = rank_counts[t][r] / 20000
        print(f"  {t:22s}  期望积分 {stats[t]['pts']:.2f}  最可能排名: {r} ({prob*100:.1f}%)  直接出线概率: {stats[t]['top2']*100:.1f}%")
    print()

# ============================================================
# 8. 计算最可能的小组第三排名（8 个最好第三晋级）
# ============================================================
print("=== 8 个成绩最好的小组第三（基于期望积分）===\n")
third_place_candidates = []
for g, teams in GROUPS.items():
    best_third = max(teams, key=lambda t: group_results[g]["rank_counts"][t][3])
    pts = group_results[g]["stats"][best_third]["pts"]
    p3 = group_results[g]["rank_counts"][best_third][3] / 20000
    third_place_candidates.append((g, best_third, pts, p3))

third_place_candidates.sort(key=lambda x: x[2], reverse=True)
top8_third = third_place_candidates[:8]

for i, (g, t, pts, p3) in enumerate(top8_third, 1):
    print(f"  {i}. {t} (Group {g}) — 期望积分 {pts:.2f}, 获得第三概率 {p3*100:.1f}%")

# ============================================================
# 9. 输出 Markdown 汇总报告
# ============================================================
MD_PATH = "group_stage_predictions_report.md"
with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write("# 2026 FIFA World Cup 小组赛全部预测与概率最大结果汇总\n\n")
    f.write(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("> 模型: Elo-like 综合评分模型（含东道主优势调整）\n")
    f.write("> 数据来源: World Football Elo Ratings (eloratings.net, 2026-06-08); 分组为 FIFA 官方抽签 + 2026-03 附加赛结果\n")
    f.write("> 说明: 本预测基于截至训练数据的球队实力推断，**未接入实时赔率/阵容**，仅供回测框架使用。\n\n")

    f.write("---\n\n")
    f.write("## 一、全部小组赛预测表\n\n")
    f.write("| 日期 | 组别 | 比赛 | 模型胜/平/负 | 公平赔率(1/X/2) | 信心 | 预测 | 预期比分 |\n")
    f.write("|------|------|------|-------------|----------------|------|------|----------|\n")
    for m in all_matches:
        f.write(f"| {m['date']} | {m['group']} | {m['team1']} vs {m['team2']} | "
                f"{m['team1_win']*100:.1f}% / {m['draw']*100:.1f}% / {m['team2_win']*100:.1f}% | "
                f"{m['team1_fair_odds']} / {m['draw_fair_odds']} / {m['team2_fair_odds']} | "
                f"{m['confidence']} | {m['predicted_result']} | {m['most_likely_score']} |\n")

    f.write("\n---\n\n")
    f.write("## 二、各组概率最大的排名结果\n\n")
    for g, teams in GROUPS.items():
        f.write(f"### {g} 组\n\n")
        f.write("| 球队 | 期望积分 | 最可能排名 | 该排名概率 | 直接出线概率(前2) | 晋级概率(含第三) |\n")
        f.write("|------|---------|-----------|-----------|------------------|------------------|\n")
        for t in teams:
            stats = group_results[g]["stats"]
            rc = group_results[g]["rank_counts"]
            r = group_results[g]["most_likely_rank"][t]
            f.write(f"| {t} | {stats[t]['pts']:.2f} | {r} | {rc[t][r]/20000*100:.1f}% | {stats[t]['top2']*100:.1f}% | {stats[t]['top3']*100:.1f}% |\n")
        f.write("\n")

    f.write("---\n\n")
    f.write("## 三、概率最大的 32 强（16 强赛对阵基础）\n\n")
    f.write("### 直接出线（小组前二）\n\n")
    for g in sorted(GROUPS.keys()):
        mlr = group_results[g]["most_likely_rank"]
        rank1_candidates = [(t, group_results[g]["rank_counts"][t][1]) for t in GROUPS[g]]
        rank1_candidates.sort(key=lambda x: -x[1])
        t1 = rank1_candidates[0][0]

        rank2_candidates = [(t, group_results[g]["rank_counts"][t][2]) for t in GROUPS[g] if t != t1]
        rank2_candidates.sort(key=lambda x: -x[1])
        t2 = rank2_candidates[0][0] if rank2_candidates else "TBD"
        f.write(f"- **{g} 组**: 1st {t1}, 2nd {t2}\n")

    f.write("\n### 成绩最好的 8 个小组第三\n\n")
    for i, (g, t, pts, p3) in enumerate(top8_third, 1):
        f.write(f"{i}. {t} (Group {g}) — 期望积分 {pts:.2f}, 该组第三概率 {p3*100:.1f}%\n")

    f.write("\n---\n\n")
    f.write("## 四、回测使用说明\n\n")
    f.write("1. **CSV 文件**: `group_stage_predictions.csv` 包含全部 **72 场** 小组赛（12 组 × 6 场）的完整概率数据。\n")
    f.write("2. **关键字段**: `team1_win`, `draw`, `team2_win` 为模型概率；`predicted_result` 为概率最大结果（1/X/2）。\n")
    f.write("3. **公平赔率**: `fair_odds = 1 / probability`，可用于与市场去水赔率对比。\n")
    f.write("4. **更新方式**: 如获得实时赔率和阵容，可替换 `compute_probabilities()` 中的评分权重，重新运行脚本生成新版预测。\n")
    f.write("5. **回测指标**: 建议记录 Brier Score、Log Loss、预测准确率（top-1 / top-2）、以及预测结果与实际结果的盈亏（若用于 odds 对比）。\n\n")

    f.write("---\n\n")
    f.write("## 五、模型假设与局限\n\n")
    f.write("- **评分来源**: 球队评分为 World Football Elo Ratings（2026-06-08），未实时更新到赛前最后一刻。\n")
    f.write("- **阵容伤停**: 未纳入具体伤停、停赛、首发阵容信息。\n")
    f.write("- **市场赔率**: 未与当前博彩市场赔率进行去水校准。\n")
    f.write("- **天气/旅行**: 未精细建模跨场馆旅行、海拔、气候影响。\n")
    f.write("- **淘汰赛战意**: 第三轮可能出现已出线/已淘汰球队的战意波动，模型未完全捕捉。\n\n")

    f.write("**免责声明**: 预测仅供信息分析与回测框架使用，不构成财务或投注建议。\n")

print(f"\n已生成 Markdown 报告 -> {MD_PATH}")
print(f"总计比赛数: {len(all_matches)} 场")
