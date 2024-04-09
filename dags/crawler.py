import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
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
    description="Run AWS Glue Crawlers to catalog data",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=15),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["data lake demo", "source"],
) as dag:
    begin = DummyOperator(task_id="begin")

    crawler_run = GlueCrawlerOperator(
        task_id = "dms-data-lake-crawler",
        config={"Name": "dms-data-lake-crawler"},
        wait_for_completion = True
    )

    end = DummyOperator(task_id="end")

begin >> crawler_run >> end