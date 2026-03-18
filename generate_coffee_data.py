# -*- coding: utf-8 -*-
"""
Coffee Chain Quality Analysis — Synthetic Data Generator
Generates realistic coffee quality measurement data for analysis demo.

Analogy mapping:
  Wafer yield       →  Coffee quality score
  Tool drift        →  Roasting machine drift
  Lot variation     →  Batch variation
  PM effect         →  Machine maintenance effect
  Recipe            →  Roast profile

Author: Go Sato
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

# ============================================================
# Configuration
# ============================================================
N_MACHINES = 4
ROAST_PROFILES = ['Light', 'Medium', 'Dark', 'Espresso']
ORIGINS = ['Ethiopia', 'Colombia', 'Brazil', 'Guatemala', 'Kenya']
N_BATCHES_PER_MACHINE = 300
SAMPLES_PER_BATCH = 5

QUALITY_METRICS = ['Aroma', 'Flavor', 'Aftertaste', 'Acidity', 'Body', 'Balance']

MAINTENANCE_TYPES = {
    'drum_cleaning': {'frequency': 30, 'effect': 2.0, 'parts': ['drum_brush', 'chaff_collector']},
    'burner_calibration': {'frequency': 60, 'effect': 3.5, 'parts': ['burner_nozzle', 'thermocouple']},
    'bearing_replacement': {'frequency': 120, 'effect': 5.0, 'parts': ['drum_bearing', 'motor_belt']},
    'full_overhaul': {'frequency': 200, 'effect': 8.0,
                      'parts': ['drum_brush', 'chaff_collector', 'burner_nozzle',
                                'thermocouple', 'drum_bearing', 'motor_belt', 'cooling_tray']},
}


def generate_machine_data(machine_id, n_batches, seed=None):
    if seed is not None:
        np.random.seed(seed)

    rows = []
    maint_rows = []
    degradation = 0.0
    maint_count = 0
    cycle_start = 0
    start_date = datetime(2024, 1, 1) + timedelta(hours=np.random.randint(0, 200))

    # Machine-specific bias
    machine_bias = {m: np.random.uniform(-1.5, 1.5) for m in QUALITY_METRICS}

    for batch in range(1, n_batches + 1):
        batch_date = start_date + timedelta(hours=batch * 3 + np.random.randint(-1, 2))
        origin = np.random.choice(ORIGINS)
        profile = np.random.choice(ROAST_PROFILES)
        batches_since_maint = batch - cycle_start

        degradation += np.random.uniform(0.01, 0.05)

        # Check maintenance
        is_maint = False
        maint_type = ''
        maint_parts = []
        for mt_name, mt_info in MAINTENANCE_TYPES.items():
            if batches_since_maint >= mt_info['frequency'] and batch > 1:
                if (maint_count + 1) % (mt_info['frequency'] // 30) == 0 or mt_name == 'drum_cleaning':
                    pass

        if batches_since_maint >= 30 and batch > 1:
            maint_count += 1
            cycle_start = batch
            is_maint = True
            performed = []
            for mt_name, mt_info in MAINTENANCE_TYPES.items():
                if maint_count % (mt_info['frequency'] // 30) == 0:
                    performed.append(mt_name)
                    maint_parts.extend(mt_info['parts'])
                    degradation -= mt_info['effect'] * 0.1
            degradation = max(0, degradation)
            maint_type = '+'.join(performed) if performed else 'drum_cleaning'
            if not performed:
                maint_parts = MAINTENANCE_TYPES['drum_cleaning']['parts']
            maint_rows.append({
                'MachineID': machine_id, 'BatchNumber': batch,
                'Date': batch_date, 'MaintenanceType': maint_type,
                'Parts': ','.join(sorted(set(maint_parts))),
                'MaintenanceCycle': maint_count,
            })

        # Origin effects
        origin_bonus = {'Ethiopia': 2.0, 'Kenya': 1.5, 'Guatemala': 0.5,
                        'Colombia': 1.0, 'Brazil': 0.0}
        # Profile effects
        profile_effects = {
            'Light': {'Aroma': 1.5, 'Acidity': 2.0, 'Body': -1.0},
            'Medium': {'Flavor': 1.0, 'Balance': 1.5},
            'Dark': {'Body': 2.0, 'Acidity': -1.5, 'Aftertaste': -0.5},
            'Espresso': {'Body': 2.5, 'Aroma': 1.0, 'Acidity': -1.0},
        }

        for sample in range(1, SAMPLES_PER_BATCH + 1):
            sample_id = f'{machine_id}_B{batch:04d}_S{sample}'
            row = {
                'SampleID': sample_id, 'MachineID': machine_id,
                'BatchNumber': batch, 'DateTime': batch_date,
                'Origin': origin, 'RoastProfile': profile,
                'BatchesSinceMaint': batches_since_maint,
                'MaintenanceCycle': maint_count,
            }
            total = 0
            for metric in QUALITY_METRICS:
                base = 7.5 + np.random.normal(0, 0.3)
                base += machine_bias[metric] * 0.3
                base += origin_bonus.get(origin, 0) * 0.15
                base += profile_effects.get(profile, {}).get(metric, 0) * 0.2
                base -= degradation * 0.15
                score = np.clip(round(base + np.random.normal(0, 0.2), 2), 0, 10)
                row[metric] = score
                total += score
            row['TotalScore'] = round(total, 2)
            row['Grade'] = 'Specialty' if total >= 48 else ('Premium' if total >= 42 else 'Commercial')
            rows.append(row)

    return pd.DataFrame(rows), pd.DataFrame(maint_rows)


def main():
    print("=" * 60)
    print("☕ Coffee Chain Quality — Data Generator")
    print("=" * 60)

    os.makedirs('data', exist_ok=True)
    all_quality = []
    all_maint = []

    for i in range(1, N_MACHINES + 1):
        machine_id = f'ROASTER_{i:02d}'
        print(f"  Generating: {machine_id}...")
        q_df, m_df = generate_machine_data(machine_id, N_BATCHES_PER_MACHINE, seed=i * 42)
        all_quality.append(q_df)
        all_maint.append(m_df)

    quality_all = pd.concat(all_quality, ignore_index=True)
    maint_all = pd.concat(all_maint, ignore_index=True)

    # Supply chain data
    suppliers = []
    for origin in ORIGINS:
        for grade in ['A', 'B', 'C']:
            suppliers.append({
                'Origin': origin, 'SupplierGrade': grade,
                'AvgMoisture_pct': round(np.random.uniform(9, 12.5), 1),
                'Defects_per300g': np.random.randint(0, 20),
                'PriceUSD_per_kg': round(np.random.uniform(3, 15), 2),
                'CertOrganic': np.random.choice([True, False]),
                'CertFairTrade': np.random.choice([True, False]),
            })
    supplier_df = pd.DataFrame(suppliers)

    quality_all.to_csv('data/coffee_quality_scores.csv', index=False)
    maint_all.to_csv('data/roaster_maintenance_log.csv', index=False)
    supplier_df.to_csv('data/supplier_info.csv', index=False)

    print(f"\n  Quality scores: {len(quality_all):,} rows")
    print(f"  Maintenance events: {len(maint_all):,} rows")
    print(f"  Suppliers: {len(supplier_df)} rows")
    print(f"\n  Files saved to ./data/")
    print(f"\n--- Summary ---")
    print(f"  Machines: {quality_all['MachineID'].nunique()}")
    print(f"  Origins: {quality_all['Origin'].nunique()}")
    print(f"  Total Score range: [{quality_all['TotalScore'].min():.1f}, {quality_all['TotalScore'].max():.1f}]")
    print(f"  Grade distribution:\n{quality_all['Grade'].value_counts().to_string()}")


if __name__ == '__main__':
    main()
