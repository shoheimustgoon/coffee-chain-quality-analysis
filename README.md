# ☕ Coffee Chain Quality & Machine Reliability Analysis

> **[🇯🇵 日本語の説明はこちら (Click here for Japanese Description)](#japanese-description)**

## 📖 Overview

An integrated framework combining **causal inference (DiD)** and **reliability engineering** to evaluate how espresso machine upgrades affect both **extraction quality** and **machine longevity** across a national coffee chain.

This project uses a **"Coffee Chain" analogy** to demonstrate the integration of two complementary analytical approaches:

1. **Quality Impact** — Did the new grinder reduce extraction failures? (Stacked DiD)
2. **Reliability Impact** — Did machine breakdowns decrease? (Survival Analysis)

---

## ☕ The Analogy

- **Coffee chain** with 50 stores nationwide
- **3 upgrades** phased in at different times:
  - **New Grinder** — precision burr grinder
  - **Water Filter** — mineral content optimization
  - **Maintenance Protocol** — systematic descaling schedule
- **Quality outcome:** Monthly extraction failure count (taste out-of-spec)
- **Reliability outcome:** Time between machine breakdowns

---

## 🔬 Dual Analysis Approach

### Track 1: Quality (DiD)
| Method | Purpose |
|---|---|
| **Stacked DiD (Poisson GLM)** | Causal effect on failure rate (IRR) |
| **Factorial DiD** | Interaction effects of combined upgrades |
| **Parallel Trends** | Validates causal assumption |
| **Counterfactual Plots** | "What if we hadn't upgraded" |

### Track 2: Reliability (Survival)
| Method | Purpose |
|---|---|
| **Exposure-Adjusted MTBF** | Fair comparison across store volumes |
| **Bathtub Curve** | Machine aging phase classification |
| **Kaplan-Meier / Cox PH** | Breakdown survival curves |
| **Barista/Shift Analysis** | Human factor impact on quality |

---

## 📊 Pipeline

```
Store Data → Quality Track: Stacked DiD → IRR + Counterfactual
           → Reliability Track: MTBF + Survival → Hazard Ratio
           → Combined: Upgrade Effectiveness Report
```

---

## 📦 Key Libraries

```
numpy, pandas, scipy, statsmodels, lifelines, matplotlib
```

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**.

---

## 📚 References

1. Callaway & Sant'Anna (2021) "DiD with multiple time periods"
2. Wooldridge (2023) "Simple approaches to nonlinear DiD"
3. Cox (1972) "Regression models and life-tables"
4. Cochrane Handbook Ch.6 — Effect measures
5. Abernethy (2004) "The New Weibull Handbook"

---

## 👨‍💻 Author

**Go Sato** — Data Scientist | Causal Inference & Reliability Engineering

---

---

<a name="japanese-description"></a>

# ☕ コーヒーチェーンの品質・マシン信頼性分析

## 📖 概要

エスプレッソマシンのアップグレードが**抽出品質**と**マシン寿命**の両方にどう影響するかを、**因果推論（DiD）** と **信頼性工学** の統合で評価するフレームワークです。

**「コーヒーチェーン」のたとえ話**を用いて、2つの補完的な分析アプローチの統合を実証しています。

---

## ☕ たとえ話

- 全国**50店舗**のコーヒーチェーン
- **3つのアップグレード**を段階的に導入：
  - **新グラインダー** — 精密バーグラインダー
  - **浄水フィルター** — ミネラル含有量最適化
  - **メンテプロトコル** — 体系的なデスケーリングスケジュール
- **品質アウトカム:** 月次抽出失敗件数（味が基準外）
- **信頼性アウトカム:** マシン故障間隔

---

## 🔬 2軸分析

### 軸1: 品質（DiD）
| 手法 | 目的 |
|---|---|
| **Stacked DiD (Poisson GLM)** | 失敗率への因果効果（IRR） |
| **Factorial DiD** | 複合アップグレードの交互作用 |
| **平行トレンド検定** | 因果推論の前提検証 |
| **反実仮想プロット** | 「アップグレードしなかったら」 |

### 軸2: 信頼性（生存分析）
| 手法 | 目的 |
|---|---|
| **Exposure補正MTBF** | 店舗間の稼働量の違いを補正 |
| **バスタブ曲線** | マシンのエージングフェーズ分類 |
| **KM / Cox PH** | 故障生存曲線 |
| **バリスタ・シフト分析** | 人的要因の品質への影響 |

---

## 📚 主要文献

1. Callaway & Sant'Anna (2021) J. Econometrics
2. Wooldridge (2023) J. Econometrics
3. Cox (1972) J. Royal Statistical Society
4. Abernethy (2004) "The New Weibull Handbook"

---

## 👨‍💻 Author

**佐藤 剛 (Go Sato)** — データサイエンティスト | 因果推論・信頼性工学
