import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.utils.dates import days_ago

DAG_ID = os.path.basename(__file__).replace(".py", "")

DEFAULT_ARGS = {
    "owner": "simonab",
    "depends_on_past": False,
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    dag_id=DAG_ID,
    description="Run AWS Glue ETL Jobs",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["data lake demo", "glue"],
) as dag:
    begin = DummyOperator(task_id="begin")

    start_job = GlueJobOperator(
        task_id = "traffic_etl",
        job_name = "Traffic ETL",
        script_args = {
            "--TARGET_BUCKET": "s3://simona-dms-data-lake-test/transformations/"
        },
        script_location = "s3://simona-data-lake-glue-scripts/glue_jobs/",
        region_name = "eu-central-1",
        dag=dag,
        verbose=True
    )

    end = DummyOperator(task_id="end")

begin >> start_job >> end

