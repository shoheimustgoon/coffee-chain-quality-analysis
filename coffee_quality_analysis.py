# -*- coding: utf-8 -*-
"""
Coffee Chain Quality Analysis — Statistical Analysis
Reads CSV data, performs quality trend / origin impact / machine comparison,
outputs results to Excel.

Author: Go Sato
"""

import numpy as np
import pandas as pd
from scipy import stats
import os


QUALITY_METRICS = ['Aroma', 'Flavor', 'Aftertaste', 'Acidity', 'Body', 'Balance']


def load_data(data_dir='data'):
    quality = pd.read_csv(os.path.join(data_dir, 'coffee_quality_scores.csv'))
    maint = pd.read_csv(os.path.join(data_dir, 'roaster_maintenance_log.csv'))
    supplier = pd.read_csv(os.path.join(data_dir, 'supplier_info.csv'))
    return quality, maint, supplier


def machine_summary(df):
    """Summary statistics per machine."""
    rows = []
    for machine, grp in df.groupby('MachineID'):
        row = {'MachineID': machine, 'N_Samples': len(grp)}
        row['TotalScore_Mean'] = grp['TotalScore'].mean()
        row['TotalScore_SD'] = grp['TotalScore'].std()
        for m in QUALITY_METRICS:
            row[f'{m}_Mean'] = grp[m].mean()
        row['Specialty_Pct'] = (grp['Grade'] == 'Specialty').mean() * 100
        row['Commercial_Pct'] = (grp['Grade'] == 'Commercial').mean() * 100
        rows.append(row)
    return pd.DataFrame(rows)


def origin_impact(df):
    """Quality comparison by origin using ANOVA + pairwise t-tests."""
    rows = []
    origins = sorted(df['Origin'].unique())

    # ANOVA
    groups = [df[df['Origin'] == o]['TotalScore'] for o in origins]
    f_stat, p_val = stats.f_oneway(*groups)
    rows.append({'Comparison': 'ANOVA (all origins)', 'Metric': 'TotalScore',
                 'Statistic': f_stat, 'p_value': p_val, 'Significant': p_val < 0.05})

    # Pairwise
    for i, o1 in enumerate(origins):
        for o2 in origins[i + 1:]:
            g1 = df[df['Origin'] == o1]['TotalScore']
            g2 = df[df['Origin'] == o2]['TotalScore']
            t, p = stats.ttest_ind(g1, g2)
            d = (g1.mean() - g2.mean()) / np.sqrt((g1.std()**2 + g2.std()**2) / 2)
            rows.append({
                'Comparison': f'{o1} vs {o2}', 'Metric': 'TotalScore',
                'Mean_1': g1.mean(), 'Mean_2': g2.mean(),
                'Cohens_d': d, 'Statistic': t, 'p_value': p,
                'Significant': p < 0.05,
            })
    return pd.DataFrame(rows)


def roast_profile_analysis(df):
    """Quality by roast profile."""
    rows = []
    for profile, grp in df.groupby('RoastProfile'):
        row = {'RoastProfile': profile, 'N': len(grp)}
        row['TotalScore_Mean'] = grp['TotalScore'].mean()
        row['TotalScore_SD'] = grp['TotalScore'].std()
        for m in QUALITY_METRICS:
            row[f'{m}_Mean'] = round(grp[m].mean(), 3)
        rows.append(row)
    return pd.DataFrame(rows)


def maintenance_effect(df, maint_df):
    """Before/After maintenance quality comparison."""
    rows = []
    for _, event in maint_df.iterrows():
        machine = event['MachineID']
        batch = event['BatchNumber']
        m_data = df[df['MachineID'] == machine]
        before = m_data[(m_data['BatchNumber'] >= batch - 15) & (m_data['BatchNumber'] < batch)]
        after = m_data[(m_data['BatchNumber'] >= batch) & (m_data['BatchNumber'] < batch + 15)]
        if len(before) < 5 or len(after) < 5:
            continue
        t, p = stats.ttest_ind(after['TotalScore'], before['TotalScore'])
        rows.append({
            'MachineID': machine, 'BatchNumber': batch,
            'MaintenanceType': event['MaintenanceType'],
            'Before_Mean': before['TotalScore'].mean(),
            'After_Mean': after['TotalScore'].mean(),
            'Delta': after['TotalScore'].mean() - before['TotalScore'].mean(),
            'p_value': p, 'Significant': p < 0.05,
            'N_Before': len(before), 'N_After': len(after),
        })
    return pd.DataFrame(rows)


def quality_trend(df):
    """Quality trend over time (batch number)."""
    return df.groupby(['MachineID', 'BatchNumber']).agg(
        TotalScore_Mean=('TotalScore', 'mean'),
        TotalScore_SD=('TotalScore', 'std'),
        N=('TotalScore', 'count'),
        Specialty_Count=('Grade', lambda x: (x == 'Specialty').sum()),
    ).reset_index()


def main():
    print("=" * 60)
    print("☕ Coffee Chain Quality — Statistical Analysis")
    print("=" * 60)

    df, maint, supplier = load_data()
    print(f"  Loaded: {len(df):,} samples, {len(maint)} maintenance events")

    os.makedirs('output', exist_ok=True)

    print("\n[1] Machine summary...")
    ms = machine_summary(df)

    print("[2] Origin impact...")
    oi = origin_impact(df)

    print("[3] Roast profile analysis...")
    rp = roast_profile_analysis(df)

    print("[4] Maintenance effect...")
    me = maintenance_effect(df, maint)

    print("[5] Quality trend...")
    qt = quality_trend(df)

    info = pd.DataFrame([
        {'Item': 'Tool', 'Value': 'coffee_quality_analysis.py'},
        {'Item': 'Author', 'Value': 'Go Sato'},
        {'Item': 'Method_Origin', 'Value': 'One-way ANOVA + pairwise t-tests with Cohen\'s d'},
        {'Item': 'Method_Maintenance', 'Value': 'Before/After comparison (15 batches window)'},
        {'Item': 'Method_Trend', 'Value': 'Batch-level aggregation per machine'},
    ])

    out_path = 'output/coffee_quality_analysis_results.xlsx'
    with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
        ms.to_excel(writer, sheet_name='Machine_Summary', index=False)
        oi.to_excel(writer, sheet_name='Origin_Impact', index=False)
        rp.to_excel(writer, sheet_name='RoastProfile_Analysis', index=False)
        me.to_excel(writer, sheet_name='Maintenance_Effect', index=False)
        qt.to_excel(writer, sheet_name='Quality_Trend', index=False)
        supplier.to_excel(writer, sheet_name='Supplier_Info', index=False)
        info.to_excel(writer, sheet_name='Analysis_Info', index=False)

    ms.to_csv('output/machine_summary.csv', index=False)
    oi.to_csv('output/origin_impact.csv', index=False)

    print(f"\n  Results saved to: {out_path}")
    print(f"\n  Machine Summary:")
    for _, r in ms.iterrows():
        print(f"    {r['MachineID']}: Mean={r['TotalScore_Mean']:.2f}, "
              f"Specialty={r['Specialty_Pct']:.1f}%")


if __name__ == '__main__':
    main()
