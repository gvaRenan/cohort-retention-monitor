"""Compare churn across signup cohorts with Kaplan-Meier curves and a log-rank test.

Synthetic data: each newer cohort churns faster than the previous one.
Run: uv run --with lifelines --with matplotlib python examples/km_by_signup_cohort.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test

OBSERVATION_MONTHS = 12
WEIBULL_SCALE_BY_COHORT = {"2023H1": 14.0, "2023H2": 9.0, "2024H1": 5.0, "2024H2": 2.5}

rng = np.random.default_rng(42)
frames = []
for cohort, scale in WEIBULL_SCALE_BY_COHORT.items():
    months_to_churn = scale * rng.weibull(1.2, size=300)
    frames.append(
        pd.DataFrame(
            {
                "cohort": cohort,
                "months": np.minimum(months_to_churn, OBSERVATION_MONTHS),
                "churned": months_to_churn <= OBSERVATION_MONTHS,
            }
        )
    )
df = pd.concat(frames, ignore_index=True)

fig, ax = plt.subplots(figsize=(7, 4), dpi=130)
for cohort, grp in df.groupby("cohort"):
    kmf = KaplanMeierFitter(label=cohort)
    kmf.fit(grp["months"], event_observed=grp["churned"])
    kmf.plot_survival_function(ax=ax, ci_show=False)
    print(f"{cohort}: churned by month 2 = {1 - kmf.predict(2):.1%}")
ax.set_xlabel("Months since signup")
ax.set_ylabel("Share of accounts still active")
ax.set_title("Retention by signup cohort (Kaplan-Meier, synthetic data)")
fig.tight_layout()
fig.savefig("examples/km_by_signup_cohort.png")

result = multivariate_logrank_test(df["months"], df["cohort"], df["churned"])
print(f"log-rank test across cohorts: statistic={result.test_statistic:.1f}, p={result.p_value:.2g}")
