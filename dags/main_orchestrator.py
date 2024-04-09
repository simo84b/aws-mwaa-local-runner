import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
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
    description="Run all Data Lake Demonstration DAGs",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=30),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["data lake demo"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")

    trigger_cleanup = TriggerDagRunOperator(
        task_id="trigger_cleanup",
        trigger_dag_id="cleanup",
        wait_for_completion=True,
    )

    trigger_glue_job = TriggerDagRunOperator(
        task_id="trigger_glue_job",
        trigger_dag_id="glue_job",
        wait_for_completion=True,
    )

    trigger_crawler = TriggerDagRunOperator(
        task_id="trigger_crawler",
        trigger_dag_id="crawler",
        wait_for_completion=True,
    )

begin >> trigger_cleanup >> trigger_glue_job >> trigger_crawler >> end