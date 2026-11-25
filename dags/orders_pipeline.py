import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append("/opt/airflow")
from ingestion.extract_orders import extract_orders

default_args = {
    "owner": "mani",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="orders_pipeline",
    start_date=datetime(2026, 11, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["de-project"],
) as dag:

    extract = PythonOperator(
        task_id="extract_to_s3",
        python_callable=extract_orders,
        op_kwargs={"run_date": "{{ ds }}"},
    )