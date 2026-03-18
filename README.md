# ☕ Coffee Chain Quality Analysis

> **[🇯🇵 日本語の説明はこちら](#japanese-description)**

## 📖 Overview

A Python-based analytical framework for **evaluating coffee quality across roasting machines, bean origins, and roast profiles**, using ANOVA, Cohen's d, and before/after maintenance comparison.

These techniques are directly applicable to **manufacturing quality control** scenarios involving multi-factor comparison and periodic maintenance.

---

## ☕ The Analogy

| Semiconductor (Actual) | Coffee Chain (Analogy) | Variable |
|---|---|---|
| Wafer yield | Total quality score | `TotalScore` |
| Tool ID | Roasting machine ID | `MachineID` |
| Process recipe | Roast profile | `RoastProfile` |
| Lot material | Bean origin | `Origin` |
| PM (Preventive Maintenance) | Machine maintenance | `MaintenanceType` |
| ESC / Electrode wear | Drum / Burner degradation | `drum_brush`, `burner_nozzle` |
| CIP overhaul | Full machine overhaul | `full_overhaul` |

### Quality Metrics (6 dimensions, 0–10 scale)
`Aroma`, `Flavor`, `Aftertaste`, `Acidity`, `Body`, `Balance` → **TotalScore** (max 60)

---

## 🛠 Scripts

| Script | Purpose |
|---|---|
| `generate_coffee_data.py` | Generate synthetic data (4 machines × 300 batches × 5 samples = 6,000 records) |
| `coffee_quality_analysis.py` | Statistical analysis → Excel output |

### Analysis Methods

| Analysis | Method | Output Sheet |
|---|---|---|
| Machine Summary | Per-machine stats | `Machine_Summary` |
| Origin Impact | ANOVA + pairwise Cohen's d | `Origin_Impact` |
| Roast Profile | Quality by roast type | `RoastProfile_Analysis` |
| Maintenance Effect | Before/After t-test | `Maintenance_Effect` |
| Quality Trend | Batch-level aggregation | `Quality_Trend` |

---

## 💻 Usage

```bash
pip install numpy pandas scipy openpyxl

python generate_coffee_data.py    # → ./data/*.csv
python coffee_quality_analysis.py  # → ./output/*.xlsx
```

## 👨‍💻 Author

**Go Sato** — Data Scientist | Causal Inference, Spatial Analysis, Reliability Engineering

---

<a name="japanese-description"></a>

# ☕ コーヒーチェーン品質分析

焙煎機・豆の産地・焙煎プロファイルごとのコーヒー品質を、ANOVA・Cohen's d・メンテナンス前後比較で統計的に評価するPython分析フレームワーク。

```bash
python generate_coffee_data.py     # 擬似データ生成
python coffee_quality_analysis.py   # 分析実行 → Excel出力
```

**佐藤 剛 (Go Sato)** — データサイエンティスト
