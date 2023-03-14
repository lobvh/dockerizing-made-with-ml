#core Python libs
from pathlib import Path

#Airflow libs
from airflow.decorators import dag
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator


# Default DAG args
default_args = {
            "owner": "airflow",
            #Depending on the start_date and schedule_interval,
            #our workflow should have been triggered several times and Airflow will try to catchup to the current time.
            #We can avoid this by setting catchup=False when defining the DAG. 
            "catch_up": False,
}

AF_DAGS_DIR = Path(__file__).parent.absolute()
GE_ROOT_DIR = Path(AF_DAGS_DIR, "great_expectations")

@dag(
       dag_id="dataops",
       description="DataOps workflows.",
       default_args=default_args,
       schedule_interval=None,
       start_date=days_ago(2),
       tags=["dataops"],
                                )
def dataops():
    #Extract and Load CSVs
    extract_and_load_projects = AirbyteTriggerSyncOperator(
                    task_id="extract_and_load_projects",
                    airbyte_conn_id="airbyte",
                    connection_id="XXXXXXXX", #Replace this!
                    asynchronous=False,
                    timeout=3600,
                    wait_seconds=3,
                                                            )
    extract_and_load_tags = AirbyteTriggerSyncOperator(
                    task_id="extract_and_load_tags",
                    airbyte_conn_id="airbyte",
                    connection_id="XXXXXXXXX",
                    asynchronous=False,
                    timeout=3600,
                    wait_seconds=3,
                            )

    #Validate that columns and rows satisfy suite of expectations
    validate_projects = GreatExpectationsOperator(
					task_id="validate_projects",
					checkpoint_name="projects",
					data_context_root_dir=GE_ROOT_DIR,
					fail_task_on_validation_failure=True,
                                               )
    validate_tags = GreatExpectationsOperator(
					task_id="validate_tags",
					checkpoint_name="tags",
					data_context_root_dir=GE_ROOT_DIR,
					fail_task_on_validation_failure=True,
                                                   )
    validate_transforms = GreatExpectationsOperator(
			   task_id="validate_transforms",
			   checkpoint_name="labeled_projects",
			   data_context_root_dir=GE_ROOT_DIR,
			   fail_task_on_validation_failure=True,
													)
    #dbt Transformation
    transform = BashOperator(task_id="transform",\
                             bash_command=f"source /usr/local/airflow/dbt_venv/bin/activate && \
                                            cd /usr/local/airflow/dbt/data_warehouse_v1 && \
                                            dbt run --profiles-dir /usr/local/airflow/dbt && \
                                            dbt test --profiles-dir /usr/local/airflow/dbt && deactivate")

    extract_and_load_projects >> validate_projects
    extract_and_load_tags >> validate_tags
    [validate_projects, validate_tags] >> transform >> validate_transforms


# Run DAG
do = dataops()


