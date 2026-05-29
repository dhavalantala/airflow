from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


from src.components.data_ingestion import split_insurance_data

default_args = {
    'owner': 'dhaval antala',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'vehicle_insurance_data_split',
    default_args=default_args,
    description='A simple DAG to fetch and split insurance data',
    schedule=timedelta(minutes=2), 
    catchup=False,
) as dag:
    
    split_data_task = PythonOperator(
        task_id='split_insurance_data_task',
        python_callable=split_insurance_data,
    )

    split_data_task