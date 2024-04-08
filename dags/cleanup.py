import os
from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

DAG_ID = os.path.basename(__file__).replace(".py", "")

S3_BUCKET = Variable.get("data_lake_bucket")

DEFAULT_ARGS = {
    "owner": "simonab",
    "depends_on_past": False,
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    dag_id=DAG_ID,
    description="Prepare Data Lake Demonstration using BashOperator and AWS CLI vs. AWS Operators",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["data lake demo"],
) as dag:
    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")

    delete_demo_s3_objects = BashOperator(
        task_id="delete_demo_s3_objects",
        bash_command=f'aws s3 rm "s3://{S3_BUCKET}/transformations/" --recursive',
    )

    delete_demo_catalog_table_person = BashOperator(
        task_id="delete_demo_catalog_table_person",
        bash_command='aws glue delete-table --database-name transformations --name person --region eu-central-1 || echo "Table not found"'
    )

    delete_demo_catalog_table_player = BashOperator(
        task_id="delete_demo_catalog_table_player",
        bash_command='aws glue delete-table --database-name transformations --name player --region eu-central-1 || echo "Table not found"'
    )

    delete_demo_catalog_table_sport_team = BashOperator(
        task_id="delete_demo_catalog_table_sport_team",
        bash_command='aws glue delete-table --database-name transformations --name sport_team --region eu-central-1 || echo "Table not Found"'
    )

    delete_demo_catalog_table_sport_type = BashOperator(
        task_id="delete_demo_catalog_table_sport_type",
        bash_command='aws glue delete-table --database-name transformations --name sport_type --region eu-central-1 || echo "Table not found"'
    )

    delete_demo_catalog = BashOperator(
        task_id="delete_demo_catalog",
        bash_command='aws glue delete-database --region eu-central-1 --name transformations || echo "Database transformations not found."',
    )

    create_demo_catalog = BashOperator(
        task_id="create_demo_catalog",
        bash_command="""aws glue create-database --region eu-central-1 --database-input \
            '{"Name": "transformations", "Description": "Datasets from AWS football data"}'""",
    )

begin >> [delete_demo_catalog_table_sport_type, delete_demo_catalog_table_person, delete_demo_catalog_table_player, delete_demo_catalog_table_sport_team, delete_demo_s3_objects] >> delete_demo_catalog >> create_demo_catalog >> end