# -*- coding: utf-8 -*-
"""
Coffee Chain Quality & Reliability Analysis — Concept Demo

Demonstrates the dual-track approach:
  Track 1 (Quality): Stacked DiD for extraction failure rate
  Track 2 (Reliability): MTBF for machine breakdowns

The full production system (not published) includes:
- Factorial DiD with mutual covariate control
- Stacked DiD with not-yet-treated controls
- Piecewise Exponential Survival DiD
- Dose-Response analysis
- Counterfactual plots (multiplicative)
- Bathtub curve with automated breakpoint detection
- Barista / shift impact analysis

Author: Go Sato
"""

import numpy as np
import pandas as pd


def generate_coffee_data(n_stores=30, n_months=24, seed=42):
    """Generate synthetic coffee chain data with dual outcomes."""
    np.random.seed(seed)
    rows = []
    upgrades = {'New_Grinder': 0.65, 'Water_Filter': 0.80, 'Maint_Protocol': 0.75}

    for s in range(n_stores):
        store_id = f'STORE_{s+1:03d}'
        base_fail_rate = np.random.uniform(5, 15)
        monthly_cups = np.random.randint(3000, 8000)
        adopt_month = np.random.choice([4, 8, 12, 16, 999])
        upgrade = np.random.choice(list(upgrades.keys()))
        effect = upgrades[upgrade]

        for m in range(1, n_months + 1):
            post = 1 if m >= adopt_month else 0
            rate = base_fail_rate * (effect if post else 1.0)

            # Quality: extraction failures (Poisson)
            failures = np.random.poisson(rate * monthly_cups / 1000)

            # Reliability: machine breakdown (binary event per month)
            breakdown_prob = 0.05 * (0.6 if post else 1.0)
            breakdown = np.random.binomial(1, breakdown_prob)

            rows.append({
                'Store': store_id, 'Month': m,
                'Upgrade': upgrade if post else 'None', 'Post': post,
                'Extraction_Failures': failures, 'MonthlyCups': monthly_cups,
                'Machine_Breakdown': breakdown,
            })

    return pd.DataFrame(rows)


def demo_quality_did():
    """Track 1: Quality impact via DiD."""
    print("=" * 50)
    print("☕ Track 1: Quality — Extraction Failure Rate")
    print("=" * 50)

    df = generate_coffee_data()
    before = df[df['Post'] == 0]
    after = df[df['Post'] == 1]

    rate_b = before['Extraction_Failures'].sum() / before['MonthlyCups'].sum() * 1000
    rate_a = after['Extraction_Failures'].sum() / after['MonthlyCups'].sum() * 1000

    print(f"\n  Stores: {df['Store'].nunique()}")
    print(f"  Before upgrade — Failure rate: {rate_b:.2f} per 1000 cups")
    print(f"  After upgrade  — Failure rate: {rate_a:.2f} per 1000 cups")
    print(f"  Crude IRR: {rate_a/rate_b:.3f} ({(1-rate_a/rate_b)*100:.1f}% reduction)")


def demo_reliability():
    """Track 2: Machine reliability."""
    print(f"\n{'='*50}")
    print("☕ Track 2: Reliability — Machine Breakdowns")
    print("=" * 50)

    df = generate_coffee_data()
    before = df[df['Post'] == 0]
    after = df[df['Post'] == 1]

    bd_b = before['Machine_Breakdown'].mean() * 100
    bd_a = after['Machine_Breakdown'].mean() * 100

    print(f"\n  Before upgrade — Breakdown rate: {bd_b:.1f}% per month")
    print(f"  After upgrade  — Breakdown rate: {bd_a:.1f}% per month")
    print(f"  Reduction: {bd_b - bd_a:.1f} percentage points")
    print(f"\n  [Note] Production system integrates both tracks")
    print(f"  into a unified Stacked DiD + Survival framework.")


if __name__ == '__main__':
    demo_quality_did()
    demo_reliability()
    print(f"\nDemo complete.")
