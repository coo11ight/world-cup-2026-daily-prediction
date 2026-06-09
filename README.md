# World Cup 2026 Daily Prediction Skill

[English](#english) | [中文](#中文)

---

## English

A bilingual, agent-agnostic skill for producing cited FIFA World Cup 2026 daily match predictions. It guides AI agents to verify fixtures first, research current market odds, compare team ratings and recent form, check squad news, de-vig bookmaker odds, and present calibrated probability forecasts.

This skill is designed for Claude, OpenAI/Codex, Grok, Gemini, Qwen, Kimi, and other agents that can read repository instructions.

## What It Does

- Finds the next 48 hours of FIFA World Cup 2026 matches.
- Supports team-specific forecasts, such as "predict Mexico's next match".
- Checks official fixtures before analysis.
- Looks up current 1X2 odds from sportsbooks or odds aggregators.
- Converts odds into no-vig implied probabilities.
- Compares market odds with ratings, form, squads, injuries, and match context.
- Produces bilingual prediction briefs with sources and access times.
- Keeps betting and financial advice out of scope.

## Installation

Clone or download this repository, then copy the skill folder into the directory used by your agent. Run the commands below from the parent folder that contains `world-cup-2026-daily-prediction`.

### Codex / OpenAI-style Skill Directory

```bash
mkdir -p ~/.codex/skills
cp -R world-cup-2026-daily-prediction ~/.codex/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\world-cup-2026-daily-prediction" "$HOME\.codex\skills\"
```

### Claude-style Skill Directory

```bash
mkdir -p ~/.claude/skills
cp -R world-cup-2026-daily-prediction ~/.claude/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\world-cup-2026-daily-prediction" "$HOME\.claude\skills\"
```

### Generic Agents

Tell the agent to read `SKILL.md` before answering World Cup prediction requests. For Chinese output, tell it to read `SKILL.zh-CN.md`.

Example:

```text
Use the skill in ./world-cup-2026-daily-prediction to research the next 48 hours of FIFA World Cup 2026 matches and give a cited prediction brief.
```

## Files

```text
world-cup-2026-daily-prediction/
  SKILL.md
  SKILL.zh-CN.md
  AGENTS.md
  CLAUDE.md
  GEMINI.md
  agents/
    openai.yaml
  references/
    source-checklist.md
    prediction-method.md
    output-templates.md
```

## Example Prompts

```text
Use $world-cup-2026-daily-prediction to give me the odds and prediction for all World Cup matches in the next 48 hours.
```

```text
Use $world-cup-2026-daily-prediction to analyze Mexico's first World Cup 2026 match. Include market odds, no-vig probability, ratings, recent form, and sources.
```

```text
使用 $world-cup-2026-daily-prediction，给我未来两天世界杯比赛的赔率和预测，中文输出。
```

## Demo Output

The table below is a historical example generated on `2026-06-09 10:28:11 +08:00`. It is included to show the expected output shape. It is not live odds.

| Beijing Time | Match | 1X2 American Odds | Decimal Odds | No-Vig Implied Probability |
|---|---|---:|---:|---:|
| 2026-06-12 03:00 | Mexico vs South Africa | Mexico `-225` / Draw `+350` / South Africa `+800` | 1.44 / 4.50 / 9.00 | Mexico 67.5% / Draw 21.7% / South Africa 10.8% |
| 2026-06-12 10:00 | Korea Republic vs Czechia | Korea `+175` / Draw `+215` / Czechia `+190` | 2.75 / 3.15 / 2.90 | Korea 35.4% / Draw 30.9% / Czechia 33.6% |

Demo sources used: [FIFA](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026), [Tom's Guide schedule](https://www.tomsguide.com/entertainment/sports/watch-fifa-world-cup-2026-on-fubo), [Oddschecker World Cup odds](https://www.oddschecker.com/us/soccer/world-cup).

## Research Standard

The agent should:

1. Verify fixtures from FIFA or another official/near-official schedule source.
2. Check at least two odds sources when available.
3. Convert odds to implied probability and remove bookmaker margin.
4. Review team ratings, recent matches, squad news, injuries, suspensions, venue, weather, rest, and travel.
5. Separate market-implied probability from the model estimate.
6. Cite sources with access time.
7. State uncertainty and avoid guaranteed-profit language.

## Disclaimer

Predictions are for informational analysis only. They are not financial advice, betting advice, or a guarantee of results. Odds move quickly and may differ by jurisdiction.

---

## 中文

这是一个中英双语、跨 Agent 通用的 2026 FIFA 世界杯每日比赛预测 Skill。它会引导 AI Agent 先核验赛程，再查询实时赔率、球队评分、近期战绩、阵容伤停和比赛背景，并把博彩公司赔率去水后转换为隐含概率，最终输出带来源和时间戳的概率预测。

适配 Claude、OpenAI/Codex、Grok、Gemini、Qwen、Kimi，以及其他能读取仓库说明文件的 AI Agent。

## 功能

- 查询未来 48 小时的 2026 世界杯比赛。
- 支持指定球队预测，例如「预测墨西哥下一场比赛」。
- 分析前先核验官方或接近官方赛程。
- 查询主流博彩公司、交易所或赔率聚合站的 1X2 赔率。
- 将赔率转换为去水后的市场隐含概率。
- 综合球队评分、近期战绩、阵容、伤停、停赛和比赛背景。
- 输出中英双语预测简报，并附来源和访问时间。
- 明确避免投注建议和财务建议。

## 安装

克隆或下载这个仓库后，把 skill 文件夹复制到对应 Agent 的 skill 目录。下面命令需要在包含 `world-cup-2026-daily-prediction` 文件夹的父目录执行。

### Codex / OpenAI 风格目录

```bash
mkdir -p ~/.codex/skills
cp -R world-cup-2026-daily-prediction ~/.codex/skills/
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\world-cup-2026-daily-prediction" "$HOME\.codex\skills\"
```

### Claude 风格目录

```bash
mkdir -p ~/.claude/skills
cp -R world-cup-2026-daily-prediction ~/.claude/skills/
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\world-cup-2026-daily-prediction" "$HOME\.claude\skills\"
```

### 其他 Agent

让 Agent 在回答世界杯预测问题前读取 `SKILL.md`。如果需要中文输出，让它读取 `SKILL.zh-CN.md`。

示例：

```text
请使用 ./world-cup-2026-daily-prediction 里的 skill，查询未来 48 小时的 2026 世界杯比赛，并输出带来源的预测简报。
```

## 文件结构

```text
world-cup-2026-daily-prediction/
  SKILL.md
  SKILL.zh-CN.md
  AGENTS.md
  CLAUDE.md
  GEMINI.md
  agents/
    openai.yaml
  references/
    source-checklist.md
    prediction-method.md
    output-templates.md
```

## 常用提示词

```text
使用 $world-cup-2026-daily-prediction，给我未来 48 小时所有世界杯比赛的赔率和预测。
```

```text
使用 $world-cup-2026-daily-prediction，分析墨西哥 2026 世界杯第一场比赛，包括市场赔率、去水概率、球队评分、近期战绩和来源。
```

```text
Use $world-cup-2026-daily-prediction to research the next 48 hours of FIFA World Cup 2026 matches and produce a cited prediction brief.
```

## 展示样例

下面是 `2026-06-09 10:28:11 +08:00` 生成的一次历史样例，用来展示输出格式。它不是实时赔率。

| 北京时间 | 比赛 | 1X2 美国赔率 | 十进制赔率 | 去水后隐含概率 |
|---|---|---:|---:|---:|
| 2026-06-12 03:00 | 墨西哥 vs 南非 | 墨西哥 `-225` / 平 `+350` / 南非 `+800` | 1.44 / 4.50 / 9.00 | 墨西哥 67.5% / 平 21.7% / 南非 10.8% |
| 2026-06-12 10:00 | 韩国 vs 捷克 | 韩国 `+175` / 平 `+215` / 捷克 `+190` | 2.75 / 3.15 / 2.90 | 韩国 35.4% / 平 30.9% / 捷克 33.6% |

样例来源：[FIFA](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026)、[Tom's Guide 赛程](https://www.tomsguide.com/entertainment/sports/watch-fifa-world-cup-2026-on-fubo)、[Oddschecker 世界杯赔率](https://www.oddschecker.com/us/soccer/world-cup)。

## 研究标准

Agent 应该：

1. 先从 FIFA 或官方/接近官方来源核验赛程。
2. 可行时至少查询两个赔率来源。
3. 将赔率转换为隐含概率，并去除庄家水位。
4. 检查球队评分、近期比赛、阵容消息、伤停、停赛、场馆、天气、休息和旅行因素。
5. 分开呈现市场隐含概率和模型估计概率。
6. 每次输出都附来源和访问时间。
7. 明确不确定性，避免稳赚、稳赢或保证收益的表达。

## 免责声明

预测仅供信息分析，不构成财务建议、投注建议或结果保证。赔率会快速变化，并且可能因地区和平台不同而不同。
