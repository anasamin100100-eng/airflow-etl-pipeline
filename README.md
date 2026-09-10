# Dockerized Apache Airflow ETL Pipeline

A Dockerized **Apache Airflow ETL pipeline** that extracts data from a CSV file, cleans and preprocesses the data using Python and Pandas, performs data aggregation, stores the results in MySQL, and sends an email notification after the workflow completes.

## 🚀 Project Overview

This project demonstrates a complete ETL workflow using Apache Airflow and Docker.

The pipeline performs the following steps:

```text
CSV Dataset
    ↓
Check Input File
    ↓
Preprocess Data
    ↓
Aggregate Data
    ↓
Create MySQL Table
    ↓
Insert Aggregated Data
    ↓
Send Email Notification
```

## 🛠️ Technologies Used

* **Apache Airflow 1.10.9**
* **Docker**
* **Docker Compose**
* **Python**
* **Pandas**
* **MySQL 5.7**
* **PostgreSQL 9.6**
* **SMTP / Gmail**
* **LocalExecutor**

## 📂 Project Structure

```text
docker-airflow-master/
│
├── dags/
│   ├── first_workflow.py
│   ├── pre_process.py
│   └── ...
│
├── ip_files/
│   └── .gitkeep
│
├── op_files/
│   └── .gitkeep
│
├── mysql_data/
│   └── .gitkeep
│
├── docker-compose-LocalExecutor.yml
├── mysql.cnf
├── .env.example
├── .gitignore
└── README.md
```

## 📊 Input Dataset

The pipeline processes a CSV dataset containing the following columns:

```text
InvoiceNo
StockCode
Description
Quantity
InvoiceDate
UnitPrice
CustomerID
Country
```

The input file is placed inside:

```text
ip_files/or.csv
```

For security and repository size reasons, the actual dataset can be excluded from Git using `.gitignore`.

## 🔄 ETL Workflow

### 1. Check Input File

Airflow first checks whether the input file is available before continuing with the pipeline.

### 2. Preprocess Data

The preprocessing task:

* Reads the CSV file using Pandas
* Handles the dataset encoding
* Cleans the `Description` column
* Removes missing values
* Creates a cleaned dataset

The processed file is generated as:

```text
ip_files/or1.csv
```

### 3. Aggregate Data

The aggregation task calculates:

```text
total_price = UnitPrice × Quantity
```

The data is then grouped by:

```text
StockCode
Description
Country
```

The aggregated result is saved for loading into MySQL.

### 4. Create MySQL Table

Airflow uses `MySqlOperator` to create the destination table:

```sql
CREATE TABLE IF NOT EXISTS aggre_res (
    stock_code varchar(100) NULL,
    descb varchar(100) NULL,
    country varchar(100) NULL,
    total_price varchar(100) NULL
);
```

### 5. Insert Data into MySQL

The aggregated CSV data is loaded into the MySQL table using:

```sql
LOAD DATA INFILE
```

### 6. Email Notification

After the ETL workflow completes, Airflow sends an email notification using SMTP.

## 🐳 Running the Project

### Prerequisites

Install:

* Docker Desktop
* Git

Make sure Docker Desktop is running before starting the project.

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### Configure Environment Variables

Create a `.env` file based on `.env.example`:

```bash
copy .env.example .env
```

Add your own credentials and configuration values to `.env`.

**Do not commit `.env` to GitHub.**

### Start the Containers

This project uses a custom Compose filename:

```bash
docker compose -f docker-compose-LocalExecutor.yml up -d
```

Check the running containers:

```bash
docker compose -f docker-compose-LocalExecutor.yml ps
```

### Open Airflow

Once the containers are running, open:

```text
http://localhost:8080
```

## 📈 Airflow DAG

The main workflow follows this dependency chain:

```text
check_file
    ↓
pre_process
    ↓
agg
    ↓
create_table
    ↓
insert_db
    ↓
send_email
```

Each task is managed and monitored through the Airflow web interface.

## 🔐 Security

Sensitive credentials are stored using environment variables.

The following files should **not** be committed:

```text
.env
mysql_data/
logs/
airflow.db
```

The repository contains `.env.example` as a template for configuration.

## 🎯 Learning Objectives

This project was created to practice:

* Apache Airflow DAG development
* ETL pipeline design
* Data preprocessing with Pandas
* Data aggregation
* MySQL integration with Airflow
* Docker and Docker Compose
* Airflow operators
* Environment variable configuration
* SMTP email notifications
* Task dependency management

## 👨‍💻 Author

**Anas Amin**

BS Computer Science — KIET

GitHub: https://github.com/anasamin100100-eng
