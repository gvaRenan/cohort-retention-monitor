# Cohort Retention Monitor

[English](#english) | [Português](#português)

---

## English

A small Python script that shows **how fast each signup cohort churns**, and raises an alert when newer cohorts are churning much faster than older ones.

### Why cohorts instead of per-account risk scores

In a churn diagnosis of a SaaS dataset, no account attribute (industry, plan, channel, MRR, individual usage, satisfaction) separated customers who churned from those who stayed. What changed was **when** the account signed up. Looking at churn by signup cohort exposed a problem that aggregate churn counts hide: new customers were leaving much earlier than before.

Share of each cohort that had already churned N months after signup (excerpt from [`examples/curva_retencao_cohort.csv`](examples/curva_retencao_cohort.csv)):

| Months since signup | 2023 H1 | 2023 H2 | 2024 H1 | 2024 H2 |
|---|---|---|---|---|
| 1 | 5.5% | 10.2% | 16.5% | 31.1% |
| 2 | 8.3% | 16.1% | 31.4% | 48.1% |
| 3 | 15.6% | 22.9% | 38.8% | 60.8% |

### Usage

```bash
pip install -r requirements.txt
python cohort_retention_monitor.py accounts.csv churn_events.csv --cutoff 2024-12-31
```

Options: `--cohort_freq` sets the cohort size (`Q` quarterly, `2Q` semester, `M` monthly).

Input files need these columns: `accounts.csv` with `account_id`, `signup_date`; `churn_events.csv` with `account_id`, `churn_date`.

The output is a table of `% churned` by months since signup, per cohort. Points that cannot be observed yet (cohort too young for that month) are left empty instead of being treated as zero. An alert is printed when the churn at month 2 of the newest cohort is at least 3x the oldest cohort's.

### Data

The example numbers come from the public Kaggle dataset [SaaS Subscription & Churn Analytics](https://www.kaggle.com/datasets/rivalytics/saas-subscription-and-churn-analytics-dataset) (MIT license, synthetic data). The raw dataset is not included here: download it from Kaggle.

### Limitations

- The example dataset is synthetic and ends on 2024-12-31, so the most recent cohort has few accounts and a noisier curve.
- The alert is a heuristic (default factor 3x), not a statistical test. Tune `fator_alerta` to your business.
- A cohort curve shows *that* newer customers churn faster, not *why*. Causes need operational data (onboarding, support, pricing changes).

---

## Português

Script em Python que mostra **com que velocidade cada cohort de signup dá churn** e dispara um alerta quando cohorts novas estão saindo muito mais rápido que as antigas.

### Por que cohort e não score de risco por conta

Num diagnóstico de churn de uma base SaaS, nenhum atributo da conta (indústria, plano, canal, MRR, uso individual, satisfação) separava quem saiu de quem ficou. O que mudou foi **quando** a conta entrou. Olhar o churn por cohort de signup expôs um problema que a contagem agregada de churn esconde: clientes novos estavam saindo muito mais cedo que antes. A tabela acima (em inglês) mostra o percentual de cada cohort que já tinha dado churn N meses após o signup.

### Uso

```bash
pip install -r requirements.txt
python cohort_retention_monitor.py accounts.csv churn_events.csv --cutoff 2024-12-31
```

Opções: `--cohort_freq` define o tamanho da cohort (`Q` trimestral, `2Q` semestral, `M` mensal).

Colunas necessárias: `accounts.csv` com `account_id`, `signup_date`; `churn_events.csv` com `account_id`, `churn_date`.

A saída é uma tabela de `% churned` por meses desde o signup, por cohort. Pontos ainda não observáveis (cohort muito jovem) ficam vazios, não zerados. O alerta aparece quando o churn no mês 2 da cohort mais recente é pelo menos 3x o da mais antiga.

### Dados

Os números de exemplo vêm do dataset público do Kaggle [SaaS Subscription & Churn Analytics](https://www.kaggle.com/datasets/rivalytics/saas-subscription-and-churn-analytics-dataset) (licença MIT, dados sintéticos). Os dados brutos não estão neste repositório: baixe no Kaggle.

### Limitações

- O dataset de exemplo é sintético e termina em 2024-12-31, então a cohort mais recente tem poucas contas e uma curva mais ruidosa.
- O alerta é uma heurística (fator padrão 3x), não um teste estatístico. Ajuste `fator_alerta` ao seu negócio.
- A curva mostra *que* clientes novos saem mais rápido, não *por quê*. As causas exigem dados operacionais (onboarding, suporte, mudanças de preço).

---

MIT License. Author: Renan Vieira.
