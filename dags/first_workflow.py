from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.email_operator import EmailOperator

from pre_processing import pre_process
from pre_process import process_data

default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 9, 3)
}

with DAG(
    dag_id="workflow",
    default_args=default_args,
    schedule_interval="@daily"
) as dag:

    check_file = BashOperator(
        task_id="check_file",
        bash_command="shasum ~/ip_files/or.csv",
        retries=2,
        retry_delay=timedelta(seconds=15)
    )

    pre_process_task = PythonOperator(
        task_id="pre_process",
        python_callable=pre_process
    )

    agg = PythonOperator(
        task_id="agg",
        python_callable=process_data
    )

    create_table = MySqlOperator(
        task_id="create_table",
        mysql_conn_id="mysql_db1",
        sql = "CREATE TABLE IF NOT EXISTS aggre_res (stock_code varchar(100) NULL,descb varchar(100) NULL,country varchar(100) NULL,total_price varchar(100) NULL)"
    )

    insert_db = MySqlOperator(
        task_id="insert_db",
        mysql_conn_id="mysql_db1",
        sql="""
        LOAD DATA INFILE '/var/lib/mysql-files/fin.csv'
        INTO TABLE aggre_res
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS
        """
    )

    send_email = EmailOperator(
        task_id="send_email",
        to="anasamin30012000@gmail.com",
        subject="Daily report generated",
        html_content="""
        <h1>Your daily report is ready</h1>
        <p>The Airflow workflow completed successfully.</p>
        """
    )

    check_file >> pre_process_task >> agg >> create_table >> insert_db >> send_email