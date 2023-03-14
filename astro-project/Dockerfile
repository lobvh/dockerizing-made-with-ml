FROM quay.io/astronomer/astro-runtime:7.3.0

ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=true
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/local/airflow/gcloud/XXXXX-XXXXX-XXXXX-XXXXXXXXXX.json

#Install dbt into a venv to avoid package dependency conflicts
WORKDIR "/usr/local/airflow"

COPY dbt-requirements.txt ./

RUN python -m virtualenv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir -r dbt-requirements.txt && deactivate
